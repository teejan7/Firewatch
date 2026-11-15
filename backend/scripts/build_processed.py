"""Incrementally validate FIRMS CSVs and convert them to query-ready Parquet.

Original files under ``data/raw/extracted`` are read-only inputs. Outputs and
the resumable processing manifest live under ``data/processed``.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import time
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb

ROOT = Path(__file__).resolve().parents[2]
PRODUCT_RULES = (
    ("modis", re.compile(r"^modis_(?P<year>\d{4})_(?P<country>.+)\.csv$", re.I), "MODIS", "MODIS", "SP"),
    ("viirs-snpp", re.compile(r"^viirs-snpp_(?P<year>\d{4})_(?P<country>.+)\.csv$", re.I), "VIIRS", "S-NPP", "SP"),
    ("viirs-jpss1", re.compile(r"^viirs-jpss1_(?P<year>\d{4})_(?P<country>.+)\.csv$", re.I), "VIIRS", "NOAA-20", "SP"),
    ("viirs-jpss2", re.compile(r"^viirs-jpss2_(?P<year>\d{4})_(?P<country>.+)\.csv$", re.I), "VIIRS", "NOAA-21", "SP"),
)
GLOBAL_RULE = re.compile(r"^fire_(?P<stream>archive|nrt)_.+\.csv$", re.I)
SCHEMA_VERSION = 2
REQUIRED_ALIASES = {
    "latitude": ("latitude", "lat"),
    "longitude": ("longitude", "lon", "long"),
    "acq_date": ("acq_date", "acquired", "date"),
}


def _safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.=-]+", "_", value)


def discover_csv_files(raw_root: Path) -> list[dict[str, Any]]:
    """Find known FIRMS products; ignore unrelated files and documentation."""
    found: list[dict[str, Any]] = []
    for path in raw_root.rglob("*.csv"):
        relative = path.relative_to(raw_root)
        parts = relative.parts
        product = sensor_family = platform = product_type = country = None
        year = None
        match = next((rule[1].match(path.name) for rule in PRODUCT_RULES if rule[1].match(path.name)), None)
        if match:
            rule = next(rule for rule in PRODUCT_RULES if rule[1].match(path.name))
            _, _, sensor_family, platform, product_type = rule
            year = int(match.group("year"))
            country = match.group("country")
            product = {"MODIS": "MODIS_SP", "S-NPP": "VIIRS_SNPP_SP", "NOAA-20": "VIIRS_NOAA20_SP", "NOAA-21": "VIIRS_NOAA21_SP"}[platform]
            scope = "country"
        else:
            global_match = GLOBAL_RULE.match(path.name)
            if not global_match or len(parts) < 2:
                stat = path.stat()
                identity = hashlib.sha256(relative.as_posix().encode("utf-8")).hexdigest()[:16]
                found.append({"file_id": identity, "source_file": relative.as_posix(), "source_path": str(path.resolve()),
                              "filename": path.name, "product": "UNSUPPORTED", "sensor_family": None, "platform": None,
                              "product_type": None, "year": int(path.parent.name) if path.parent.name.isdigit() else None,
                              "country": None, "scope": "unknown", "size_bytes": stat.st_size,
                              "modified_ns": stat.st_mtime_ns, "supported": False})
                continue
            platform = "NOAA-21" if "noaa21" in str(relative).lower() or "jpss2" in str(relative).lower() else None
            # These five global products were downloaded into the NOAA-21 folder.
            if platform is None:
                stat = path.stat()
                identity = hashlib.sha256(relative.as_posix().encode("utf-8")).hexdigest()[:16]
                found.append({"file_id": identity, "source_file": relative.as_posix(), "source_path": str(path.resolve()),
                              "filename": path.name, "product": "UNSUPPORTED", "sensor_family": None, "platform": None,
                              "product_type": None, "year": int(path.parent.name) if path.parent.name.isdigit() else None,
                              "country": None, "scope": "unknown", "size_bytes": stat.st_size,
                              "modified_ns": stat.st_mtime_ns, "supported": False})
                continue
            sensor_family = "VIIRS"
            stream = global_match.group("stream").lower()
            product_type = "SP" if stream == "archive" else "NRT"
            product = f"VIIRS_NOAA21_{product_type}"
            year = int(path.parent.name) if path.parent.name.isdigit() else None
            country = None
            scope = "global"
        if year is None:
            continue
        stat = path.stat()
        identity = hashlib.sha256(relative.as_posix().encode("utf-8")).hexdigest()[:16]
        found.append({
            "file_id": identity,
            "source_file": relative.as_posix(),
            "source_path": str(path.resolve()),
            "filename": path.name,
            "product": product,
            "sensor_family": sensor_family,
            "platform": platform,
            "product_type": product_type,
            "year": year,
            "country": country,
            "scope": scope,
            "size_bytes": stat.st_size,
            "modified_ns": stat.st_mtime_ns,
            "supported": True,
        })
    return sorted(found, key=lambda item: (item["year"], item["product"], item["source_file"].casefold()))


def _qident(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def _literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def _open_csv(connection: duckdb.DuckDBPyConnection, path: Path) -> list[str]:
    result = connection.execute("DESCRIBE SELECT * FROM read_csv(?, all_varchar=true, header=true, null_padding=true)", [str(path)])
    return [row[0] for row in result.fetchall()]


def _normalize_headers(headers: list[str]) -> dict[str, str]:
    return {header.strip().lower(): header for header in headers if header.strip()}


def _expr(normalized: dict[str, str], aliases: tuple[str, ...], cast: str = "VARCHAR") -> str:
    column = next((normalized[name] for name in aliases if name in normalized), None)
    if column is None:
        return f"CAST(NULL AS {cast})"
    identifier = _qident(column)
    if cast == "VARCHAR":
        return f"NULLIF(TRIM(CAST({identifier} AS VARCHAR)), '')"
    return f"TRY_CAST(NULLIF(TRIM(CAST({identifier} AS VARCHAR)), '') AS {cast})"


def _source_select(entry: dict[str, Any], headers: list[str]) -> str:
    norm = _normalize_headers(headers)
    for required, aliases in REQUIRED_ALIASES.items():
        if not any(name in norm for name in aliases):
            raise ValueError(f"Missing required FIRMS column {required} (accepted: {', '.join(aliases)}).")
    date_expr = _expr(norm, ("acq_date", "acquired", "date"))
    date_expr = f"TRY_CAST(SUBSTR({date_expr}, 1, 10) AS DATE)"
    lat_expr = _expr(norm, REQUIRED_ALIASES["latitude"], "DOUBLE")
    lon_expr = _expr(norm, REQUIRED_ALIASES["longitude"], "DOUBLE")
    time_expr = _expr(norm, ("acq_time", "acquisition_time"))
    satellite_expr = _expr(norm, ("satellite", "platform"))
    instrument_expr = _expr(norm, ("instrument", "sensor"))
    confidence_expr = _expr(norm, ("confidence",))
    daynight_expr = _expr(norm, ("daynight", "day_night"))
    frp_expr = _expr(norm, ("frp",), "DOUBLE")
    brightness_expr = _expr(norm, ("brightness",), "DOUBLE")
    ti4_expr = _expr(norm, ("bright_ti4",), "DOUBLE")
    ti5_expr = _expr(norm, ("bright_ti5",), "DOUBLE")
    version_expr = _expr(norm, ("version", "processing_version"))
    original_fields = "struct_pack(" + ", ".join(f"{_qident(header)} := {_qident(header)}" for header in headers) + ")"
    platform_expr = satellite_expr if entry["platform"] == "MODIS" else _literal(entry["platform"])
    source = _literal(entry["source_file"])
    file_hash = _literal(entry["file_id"])
    return f"""SELECT
        {date_expr} AS acq_date,
        {time_expr} AS acq_time,
        {lat_expr} AS latitude,
        {lon_expr} AS longitude,
        {satellite_expr} AS satellite,
        {instrument_expr} AS instrument,
        {_literal(entry['sensor_family'])} AS sensor_family,
        {platform_expr} AS platform,
        {_literal(entry['product_type'])} AS product_type,
        {confidence_expr} AS confidence,
        {daynight_expr} AS daynight,
        {frp_expr} AS frp,
        {brightness_expr} AS brightness,
        {ti4_expr} AS bright_ti4,
        {ti5_expr} AS bright_ti5,
        {source} AS source_file,
        {file_hash} || ':' || CAST(ROW_NUMBER() OVER () AS VARCHAR) AS source_record_id,
        {version_expr} AS processing_version,
        {_literal(entry['product'])} AS source_product,
        MD5(TO_JSON({original_fields})) AS source_record_fingerprint,
        TO_JSON({original_fields}) AS original_fields
    FROM read_csv({_literal(entry['source_path'])}, all_varchar=true, header=true, null_padding=true)"""


def _atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(temporary, path)


def _output_path(entry: dict[str, Any], processed_root: Path) -> Path:
    partition = f"sensor_family={_safe_name(entry['sensor_family'])}/year={entry['year']}/product_type={entry['product_type']}/product={_safe_name(entry['product'])}"
    return processed_root / "observations" / partition / f"{entry['file_id']}.parquet"


def process_entry(entry: dict[str, Any], processed_root: Path, connection: duckdb.DuckDBPyConnection, force: bool = False) -> dict[str, Any]:
    output = _output_path(entry, processed_root)
    manifest_path = processed_root / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {"schema_version": SCHEMA_VERSION, "files": {}}
    previous = manifest.get("files", {}).get(entry["file_id"], {})
    signature = {key: entry[key] for key in ("size_bytes", "modified_ns")}
    if not force and previous.get("status") == "processed" and previous.get("signature") == signature and output.is_file():
        cached = connection.execute(f"""SELECT LIST(DISTINCT processing_version) FILTER (WHERE processing_version IS NOT NULL),
          COUNT(*) FILTER (WHERE acq_time IS NULL), COUNT(*) FILTER (WHERE satellite IS NULL),
          COUNT(*) FILTER (WHERE instrument IS NULL), COUNT(*) FILTER (WHERE daynight IS NULL),
          COUNT(*) FILTER (WHERE brightness IS NULL), COUNT(*) FILTER (WHERE bright_ti4 IS NULL),
          COUNT(*) FILTER (WHERE bright_ti5 IS NULL), COUNT(*) FILTER (WHERE confidence IS NULL),
          COUNT(*) FILTER (WHERE frp IS NULL),
          COUNT(*) FILTER (WHERE NULLIF(TRIM(JSON_EXTRACT_STRING(original_fields, '$.frp')), '') IS NOT NULL AND frp IS NULL),
          COUNT(*) FILTER (WHERE NULLIF(TRIM(JSON_EXTRACT_STRING(original_fields, '$.brightness')), '') IS NOT NULL AND brightness IS NULL),
          COUNT(*) FILTER (WHERE NULLIF(TRIM(JSON_EXTRACT_STRING(original_fields, '$.bright_ti4')), '') IS NOT NULL AND bright_ti4 IS NULL),
          COUNT(*) FILTER (WHERE NULLIF(TRIM(JSON_EXTRACT_STRING(original_fields, '$.bright_ti5')), '') IS NOT NULL AND bright_ti5 IS NULL)
          FROM read_parquet({_literal(str(output))})""").fetchone()
        previous["processing_versions"] = cached[0] or []
        previous["null_counts"] = {"acq_time": int(cached[1]), "satellite": int(cached[2]), "instrument": int(cached[3]),
                                    "confidence": int(cached[8]), "daynight": int(cached[4]),
                                    "frp": int(cached[9]), "brightness": int(cached[5]),
                                    "bright_ti4": int(cached[6]), "bright_ti5": int(cached[7])}
        previous["invalid_numeric_counts"] = {"frp": int(cached[10]), "brightness": int(cached[11]),
                                              "bright_ti4": int(cached[12]), "bright_ti5": int(cached[13])}
        previous["schema_version"] = SCHEMA_VERSION
        manifest["schema_version"] = SCHEMA_VERSION
        manifest.setdefault("files", {})[entry["file_id"]] = previous
        _atomic_json(manifest_path, manifest)
        return {**previous, "status": "skipped", "reason": "unchanged source and processed output exists"}

    headers = _open_csv(connection, Path(entry["source_path"]))
    select_sql = _source_select(entry, headers)
    normalized = _normalize_headers(headers)
    lat = _expr(normalized, REQUIRED_ALIASES["latitude"], "DOUBLE")
    lon = _expr(normalized, REQUIRED_ALIASES["longitude"], "DOUBLE")
    raw_date = _expr(normalized, ("acq_date", "acquired", "date"))
    date_valid = f"TRY_CAST(SUBSTR({raw_date}, 1, 10) AS DATE) IS NOT NULL"
    valid_coords = f"{lat} BETWEEN -90 AND 90 AND {lon} BETWEEN -180 AND 180"
    raw_frp = _expr(normalized, ("frp",), "DOUBLE")
    raw_confidence = _expr(normalized, ("confidence",))
    raw_time = _expr(normalized, ("acq_time", "acquisition_time"))
    raw_satellite = _expr(normalized, ("satellite", "platform"))
    raw_instrument = _expr(normalized, ("instrument", "sensor"))
    raw_daynight = _expr(normalized, ("daynight", "day_night"))
    raw_brightness = _expr(normalized, ("brightness",), "DOUBLE")
    raw_ti4 = _expr(normalized, ("bright_ti4",), "DOUBLE")
    raw_ti5 = _expr(normalized, ("bright_ti5",), "DOUBLE")
    text_frp = _expr(normalized, ("frp",))
    text_brightness = _expr(normalized, ("brightness",))
    text_ti4 = _expr(normalized, ("bright_ti4",))
    text_ti5 = _expr(normalized, ("bright_ti5",))
    raw_version = _expr(normalized, ("version", "processing_version"))
    source = f"read_csv({_literal(entry['source_path'])}, all_varchar=true, header=true, null_padding=true)"
    metrics = connection.execute(f"""SELECT COUNT(*) AS rows_source,
      COUNT(*) FILTER (WHERE NOT ({date_valid}) OR {raw_date} IS NULL) AS invalid_dates,
      COUNT(*) FILTER (WHERE NOT ({valid_coords}) OR {lat} IS NULL OR {lon} IS NULL) AS invalid_coordinates,
      COUNT(*) FILTER (WHERE {date_valid} AND {valid_coords}) AS rows_valid,
      MIN(TRY_CAST(SUBSTR({raw_date}, 1, 10) AS DATE)) FILTER (WHERE {date_valid} AND {valid_coords}) AS date_min,
      MAX(TRY_CAST(SUBSTR({raw_date}, 1, 10) AS DATE)) FILTER (WHERE {date_valid} AND {valid_coords}) AS date_max,
      COUNT(*) FILTER (WHERE {date_valid} AND {valid_coords} AND {raw_frp} IS NULL) AS null_frp,
      COUNT(*) FILTER (WHERE {date_valid} AND {valid_coords} AND {raw_confidence} IS NULL) AS null_confidence,
      COUNT(*) FILTER (WHERE {date_valid} AND {valid_coords}) -
        COUNT(DISTINCT MD5(TO_JSON(struct_pack({', '.join(f'{_qident(header)} := {_qident(header)}' for header in headers)}))))
          FILTER (WHERE {date_valid} AND {valid_coords}) AS exact_duplicate_rows,
      LIST(DISTINCT {raw_version}) FILTER (WHERE {raw_version} IS NOT NULL) AS processing_versions,
      COUNT(*) FILTER (WHERE {date_valid} AND {valid_coords} AND {raw_time} IS NULL) AS null_acq_time,
      COUNT(*) FILTER (WHERE {date_valid} AND {valid_coords} AND {raw_satellite} IS NULL) AS null_satellite,
      COUNT(*) FILTER (WHERE {date_valid} AND {valid_coords} AND {raw_instrument} IS NULL) AS null_instrument,
      COUNT(*) FILTER (WHERE {date_valid} AND {valid_coords} AND {raw_daynight} IS NULL) AS null_daynight,
      COUNT(*) FILTER (WHERE {date_valid} AND {valid_coords} AND {raw_brightness} IS NULL) AS null_brightness,
      COUNT(*) FILTER (WHERE {date_valid} AND {valid_coords} AND {raw_ti4} IS NULL) AS null_bright_ti4,
      COUNT(*) FILTER (WHERE {date_valid} AND {valid_coords} AND {raw_ti5} IS NULL) AS null_bright_ti5,
      COUNT(*) FILTER (WHERE {date_valid} AND {valid_coords} AND {text_frp} IS NOT NULL AND {raw_frp} IS NULL) AS invalid_frp,
      COUNT(*) FILTER (WHERE {date_valid} AND {valid_coords} AND {text_brightness} IS NOT NULL AND {raw_brightness} IS NULL) AS invalid_brightness,
      COUNT(*) FILTER (WHERE {date_valid} AND {valid_coords} AND {text_ti4} IS NOT NULL AND {raw_ti4} IS NULL) AS invalid_bright_ti4,
      COUNT(*) FILTER (WHERE {date_valid} AND {valid_coords} AND {text_ti5} IS NOT NULL AND {raw_ti5} IS NULL) AS invalid_bright_ti5
      FROM {source}""").fetchone()
    valid_where = f"WHERE {date_valid} AND {valid_coords}"

    # Reserve room for a temporary output and protect the user's remaining disk.
    free = shutil.disk_usage(processed_root.parent).free if processed_root.parent.exists() else shutil.disk_usage(processed_root.anchor).free
    reserve = 2 * 1024**3
    if free - reserve < max(64 * 1024**2, int(entry["size_bytes"] * 0.75)):
        raise OSError(f"Insufficient free space to process {entry['filename']} safely; keeping a 2 GiB reserve. Free space or process a smaller subset.")

    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(output.stem + "." + uuid.uuid4().hex + ".tmp.parquet")
    try:
        connection.execute(f"COPY ({select_sql} {valid_where}) TO {_literal(str(temporary))} (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 100000)")
        os.replace(temporary, output)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise

    result = {
        **entry,
        "signature": signature,
        "status": "processed",
        "output_file": str(output.relative_to(processed_root)).replace("\\", "/"),
        "schema_version": SCHEMA_VERSION,
        "rows_source": int(metrics[0]),
        "rows_processed": int(metrics[3]),
        "invalid_dates": int(metrics[1]),
        "invalid_coordinates": int(metrics[2]),
        "exact_duplicate_rows_within_file": int(metrics[8]),
        "null_frp_rows": int(metrics[6]),
        "null_confidence_rows": int(metrics[7]),
        "null_counts": {"acq_time": int(metrics[10]), "satellite": int(metrics[11]), "instrument": int(metrics[12]),
                        "confidence": int(metrics[7]), "daynight": int(metrics[13]), "frp": int(metrics[6]),
                        "brightness": int(metrics[14]), "bright_ti4": int(metrics[15]), "bright_ti5": int(metrics[16])},
        "invalid_numeric_counts": {"frp": int(metrics[17]), "brightness": int(metrics[18]),
                                   "bright_ti4": int(metrics[19]), "bright_ti5": int(metrics[20])},
        "processing_versions": metrics[9] or [],
        "date_min": str(metrics[4]) if metrics[4] else None,
        "date_max": str(metrics[5]) if metrics[5] else None,
    }
    manifest.setdefault("files", {})[entry["file_id"]] = result
    manifest["schema_version"] = SCHEMA_VERSION
    manifest["updated_at_utc"] = datetime.now(timezone.utc).isoformat()
    _atomic_json(manifest_path, manifest)
    return result


def build_daily_cells(processed_root: Path, connection: duckdb.DuckDBPyConnection) -> dict[str, Any]:
    manifest_path = processed_root / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {"files": {}}
    outputs = [str(processed_root / item["output_file"]) for item in manifest.get("files", {}).values()
               if item.get("status") == "processed" and item.get("output_file") and (processed_root / item["output_file"]).is_file()]
    if not outputs:
        raise ValueError("No processed observation files are available to aggregate.")
    target = processed_root / "daily_cell.parquet"
    temporary = target.with_name(target.stem + "." + uuid.uuid4().hex + ".tmp.parquet")
    connection.execute("SET memory_limit='1GB'")
    connection.execute("SET threads=4")
    query = """SELECT acq_date,
      CAST(GREATEST(0, LEAST(719, FLOOR((latitude + 90.0) / 0.25))) AS INTEGER) AS lat_i,
      CAST(GREATEST(0, LEAST(1439, FLOOR((longitude + 180.0) / 0.25))) AS INTEGER) AS lon_i,
      sensor_family, platform, product_type, daynight,
      COUNT(*)::BIGINT AS n_raw,
      1::BIGINT AS n_dedup,
      SUM(frp) AS frp_sum, MAX(frp) AS frp_max
      FROM read_parquet(?)
      GROUP BY acq_date, lat_i, lon_i, sensor_family, platform, product_type, daynight"""
    try:
        connection.execute(f"COPY ({query}) TO {_literal(str(temporary))} (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 100000)", [outputs])
        rows = int(connection.execute(f"SELECT COUNT(*) FROM read_parquet({_literal(str(temporary))})").fetchone()[0])
        os.replace(temporary, target)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
    return {"output_file": str(target), "cell_rows": rows, "source_files": len(outputs), "grid_degrees": 0.25,
            "grid_convention": "lat_i/lon_i are zero-based indices of cells whose lower-left edge is (-90 + 0.25*lat_i, -180 + 0.25*lon_i); coordinates at +90/+180 are clamped into the last cell.",
            "n_dedup_policy": "One detected cell-day presence per sensor/platform/product/daynight group; n_raw retains the number of rows. Exact duplicate source rows are counted per source file in manifest.json. Potentially overlapping observations across sensors remain separate."}


def run(args: argparse.Namespace) -> dict[str, Any]:
    raw_root = Path(args.raw_root).resolve()
    processed_root = Path(args.processed_root).resolve()
    if not raw_root.is_dir():
        raise FileNotFoundError(f"Archive root does not exist: {raw_root}")
    entries = discover_csv_files(raw_root)
    selected = [entry for entry in entries
                if entry.get("supported", False)
                and (not args.product or entry["product"] in args.product)
                and (not args.year or entry["year"] in args.year)
                and (not args.country or (entry["country"] or "").casefold() == args.country.casefold())
                and (args.include_nrt or entry["product_type"] != "NRT")]
    processed_root.mkdir(parents=True, exist_ok=True)
    _atomic_json(processed_root / "archive_index.json", {
        "schema_version": SCHEMA_VERSION,
        "indexed_at_utc": datetime.now(timezone.utc).isoformat(),
        "raw_root": str(raw_root),
        "files_discovered": len(entries),
        "unsupported_csv_files": sum(not item.get("supported", False) for item in entries),
        "files_selected": len(selected),
        "files": [{k: v for k, v in entry.items() if k != "source_path"} for entry in entries],
    })
    manifest_path = processed_root / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {"schema_version": SCHEMA_VERSION, "files": {}}
    connection = duckdb.connect(database=":memory:")
    connection.execute("SET memory_limit='1GB'")
    connection.execute("SET threads=4")
    failures: list[dict[str, str]] = []
    skipped = 0
    started = time.monotonic()
    try:
        for index, entry in enumerate(selected, 1):
            try:
                result = process_entry(entry, processed_root, connection, args.force)
                if result["status"] == "skipped":
                    skipped += 1
                    print(f"[{index}/{len(selected)}] unchanged: {entry['source_file']}", flush=True)
                    continue
                print(f"[{index}/{len(selected)}] {result['rows_processed']:,} rows {result['date_min']}..{result['date_max']} : {entry['source_file']}", flush=True)
            except Exception as exc:
                message = f"{type(exc).__name__}: {exc}"
                failures.append({"source_file": entry["source_file"], "error": message})
                manifest.setdefault("files", {})[entry["file_id"]] = {**entry, "status": "failed", "error": message,
                    "signature": {"size_bytes": entry["size_bytes"], "modified_ns": entry["modified_ns"]}}
                manifest["schema_version"] = SCHEMA_VERSION
                manifest["updated_at_utc"] = datetime.now(timezone.utc).isoformat()
                _atomic_json(manifest_path, manifest)
                print(f"[{index}/{len(selected)}] FAILED {entry['source_file']}: {message}", file=sys.stderr, flush=True)
    finally:
        connection.close()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {"files": {}}
    all_files = list(manifest.get("files", {}).values())
    status_report: dict[str, Any] = defaultdict(lambda: {"files": 0, "rows_source": 0, "rows_processed": 0, "invalid_dates": 0, "invalid_coordinates": 0, "exact_duplicate_rows_within_file": 0, "null_counts": {}, "invalid_numeric_counts": {}})
    for item in all_files:
        group = f"{item.get('sensor_family','unknown')}|{item.get('year','unknown')}|{item.get('product_type','unknown')}"
        counts = status_report[group]
        counts["files"] += 1
        for field in ("rows_source", "rows_processed", "invalid_dates", "invalid_coordinates", "exact_duplicate_rows_within_file"):
            counts[field] += int(item.get(field, 0))
        for field, value in item.get("null_counts", {}).items():
            counts["null_counts"][field] = counts["null_counts"].get(field, 0) + int(value)
        for field, value in item.get("invalid_numeric_counts", {}).items():
            counts["invalid_numeric_counts"][field] = counts["invalid_numeric_counts"].get(field, 0) + int(value)
    quality = {
        "schema_version": SCHEMA_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "duration_seconds": round(time.monotonic() - started, 3),
        "files_discovered": len(entries),
        "files_unsupported": sum(not item.get("supported", False) for item in entries),
        "files_selected": len(selected),
        "files_processed_total": sum(item.get("status") == "processed" for item in all_files),
        "files_failed_total": sum(item.get("status") == "failed" for item in all_files),
        "files_skipped_this_run": skipped,
        "files_failed_this_run": failures,
        "rows_by_sensor_year_product": dict(status_report),
        "coverage": {"date_min": min((item["date_min"] for item in all_files if item.get("date_min")), default=None),
                     "date_max": max((item["date_max"] for item in all_files if item.get("date_max")), default=None),
                     "note": "Per-file date_min/date_max are recorded in manifest.json; date gaps remain distinguishable by file and source."},
    }
    indexed_files = []
    manifest_by_id = manifest.get("files", {})
    for entry in entries:
        state = manifest_by_id.get(entry["file_id"], {})
        current_signature = {key: entry[key] for key in ("size_bytes", "modified_ns")}
        is_current = state.get("signature") == current_signature and state.get("status") == "processed"
        indexed_files.append({
            **{key: value for key, value in entry.items() if key != "source_path"},
            "status": state.get("status") if state.get("signature") == current_signature else "discovered_pending",
            "date_min": state.get("date_min") if is_current else None,
            "date_max": state.get("date_max") if is_current else None,
            "processing_version": state.get("processing_versions", []) if is_current else [],
            "output_file": state.get("output_file") if is_current else None,
        })
    _atomic_json(processed_root / "archive_index.json", {
        "schema_version": SCHEMA_VERSION,
        "indexed_at_utc": datetime.now(timezone.utc).isoformat(),
        "raw_root": str(raw_root),
        "files_discovered": len(entries),
        "files_selected_this_run": len(selected),
        "files": indexed_files,
    })
    _atomic_json(processed_root / "quality_report.json", quality)
    if args.build_daily_cells:
        con = duckdb.connect(database=":memory:")
        try:
            quality["daily_cells"] = build_daily_cells(processed_root, con)
        finally:
            con.close()
        _atomic_json(processed_root / "quality_report.json", quality)
    return quality


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--raw-root", default=str(ROOT / "data" / "raw" / "extracted"))
    cli.add_argument("--processed-root", default=str(ROOT / "data" / "processed"))
    cli.add_argument("--product", action="append", help="Filter to a product ID; repeat to select several.")
    cli.add_argument("--year", action="append", type=int, help="Filter to a year; repeat to select several.")
    cli.add_argument("--country", help="Exact country-partition name, case-insensitive.")
    cli.add_argument("--include-nrt", action="store_true", help="Include files classified as NRT; default processes SP only.")
    cli.add_argument("--force", action="store_true", help="Reprocess matching source files even when unchanged.")
    cli.add_argument("--build-daily-cells", action="store_true", help="Atomically build daily_cell.parquet from processed outputs.")
    return cli


if __name__ == "__main__":
    report = run(parser().parse_args())
    print(json.dumps(report, indent=2, ensure_ascii=False))
