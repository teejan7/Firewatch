"""Stream FIRMS country SP CSVs into small daily and 1-degree aggregates.

Raw input is read-only. This pipeline never writes observation-level rows.
The daily manifest is independent from the legacy processing manifest.
"""
from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import re
import shutil
import sys
import tempfile
import time
import uuid
from collections import defaultdict
from pathlib import Path
from time import sleep
from typing import Any

import duckdb

ROOT = Path(__file__).resolve().parents[2]
RAW_ROOT = ROOT / "data" / "raw" / "extracted"
DAILY_ROOT = ROOT / "data" / "processed" / "daily"
MANIFEST_PATH = ROOT / "data" / "processed" / "daily_manifest.json"
LOG_PATH = ROOT / "logs" / "build_daily.log"
SCHEMA_VERSION = 2
AGGREGATE_FORMAT = 2
DEFAULT_YEARS = tuple(range(2020, 2026))
MIN_FREE_BYTES = 3 * 1024**3


def _safe(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.=-]+", "_", value.strip()).strip("._") or "unknown"


def _quote_ident(value: str) -> str:
    return '"' + value.replace('"', '""') + '"'


def _sql_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def _atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + "." + uuid.uuid4().hex + ".tmp")
    try:
        temp.write_text(json.dumps(value, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        for attempt in range(6):
            try:
                os.replace(temp, path)
                return
            except PermissionError:
                if attempt == 5:
                    raise
                sleep(0.2 * (attempt + 1))
    finally:
        temp.unlink(missing_ok=True)


def _load_manifest() -> dict[str, Any]:
    if MANIFEST_PATH.is_file():
        value = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        if value.get("schema_version") not in {1, SCHEMA_VERSION}:
            raise ValueError(f"Unsupported daily manifest schema version: {value.get('schema_version')!r}")
        value["schema_version"] = SCHEMA_VERSION
        return value
    return {"schema_version": SCHEMA_VERSION, "files": {}}


def _header(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        try:
            return next(csv.reader(stream))
        except StopIteration as exc:
            raise ValueError("CSV is empty and has no header row.") from exc


def _field(headers: list[str], aliases: tuple[str, ...]) -> str | None:
    normalized = {h.strip().lower(): h for h in headers if h.strip()}
    return next((normalized[key] for key in aliases if key in normalized), None)


def _expressions(headers: list[str], family: str) -> dict[str, Any]:
    selected = {
        "date": _field(headers, ("acq_date", "acquired", "date")),
        "latitude": _field(headers, ("latitude", "lat")),
        "longitude": _field(headers, ("longitude", "lon", "long")),
    }
    missing = [key for key in ("date", "latitude", "longitude") if not selected[key]]
    if missing:
        raise ValueError(f"Missing required FIRMS columns: {', '.join(missing)}. Required aliases: date=acq_date, latitude=latitude, longitude=longitude.")
    optional = {
        "frp": ("frp",), "satellite": ("satellite", "sat"), "confidence": ("confidence", "conf"),
        "type": ("type",), "daynight": ("daynight", "dn"), "version": ("version",),
    }
    for key, aliases in optional.items():
        selected[key] = _field(headers, aliases)

    def text(key: str) -> str:
        name = selected[key]
        return f"NULLIF(TRIM(CAST({_quote_ident(name)} AS VARCHAR)), '')" if name else "CAST(NULL AS VARCHAR)"

    def number(key: str) -> str:
        name = selected[key]
        return f"TRY_CAST(NULLIF(TRIM(CAST({_quote_ident(name)} AS VARCHAR)), '') AS DOUBLE)" if name else "CAST(NULL AS DOUBLE)"

    satellite = f"UPPER({text('satellite')})"
    if family == "MODIS":
        platform = f"CASE WHEN {satellite} IN ('T','TERRA') THEN 'Terra' WHEN {satellite} IN ('A','AQUA') THEN 'Aqua' ELSE COALESCE({text('satellite')}, 'MODIS') END"
    else:
        platform = "source_platform"

    confidence = text("confidence")
    confidence_number = number("confidence")
    confidence_text = f"LOWER({confidence})"
    # NASA guidance: MODIS numeric confidence is low <30, nominal 30..79,
    # high 80..100. FIRMS VIIRS CSV encodes its documented categorical classes
    # as l/n/h (also accept full labels). The qualifying subset is nominal/high;
    # this is a quality filter, not evidence of inter-sensor equivalence.
    quality = (f"COALESCE({confidence_number} >= 30, FALSE)" if family == "MODIS"
               else f"{confidence_text} IN ('n', 'h', 'nominal', 'high')")
    type_expr = f"TRY_CAST({text('type')} AS INTEGER)" if selected["type"] else "CAST(NULL AS INTEGER)"
    daynight = f"UPPER({text('daynight')})" if selected["daynight"] else "CAST(NULL AS VARCHAR)"
    return {
        "date": f"TRY_CAST(SUBSTR({text('date')}, 1, 10) AS DATE)",
        "latitude": number("latitude"),
        "longitude": number("longitude"),
        "frp": f"COALESCE({number('frp')}, 0.0)" if selected["frp"] else "0.0",
        "platform": platform, "type": type_expr, "quality": quality,
        "day": f"{daynight} = 'D'", "night": f"{daynight} = 'N'",
        "has_type": selected["type"] is not None,
        "has_confidence": selected["confidence"] is not None,
        "has_daynight": selected["daynight"] is not None,
        "confidence_column": selected["confidence"],
        "version": text("version"),
        "has_version": selected["version"] is not None,
    }


def _make_source_query(entry: dict[str, Any], expr: dict[str, Any]) -> str:
    country, family = _sql_literal(entry["country"]), _sql_literal(entry["sensor_family"])
    product, product_type = _sql_literal(entry["product"]), _sql_literal(entry["product_type"])
    platform = expr["platform"] if entry["sensor_family"] == "MODIS" else _sql_literal(entry["platform"])
    valid = "acq_date IS NOT NULL AND latitude BETWEEN -90 AND 90 AND longitude BETWEEN -180 AND 180"
    common = f"""
      WITH parsed AS (
        SELECT {expr['date']} AS acq_date,
               {expr['latitude']} AS latitude, {expr['longitude']} AS longitude,
               YEAR({expr['date']})::INTEGER AS year,
               FLOOR({expr['latitude']} + 90)::INTEGER AS lat_bin,
               FLOOR({expr['longitude']} + 180)::INTEGER AS lon_bin,
               {expr['frp']} AS frp, {expr['type']} AS detection_type,
               {expr['version']} AS source_version,
               {expr['quality']} AS is_quality, {expr['day']} AS is_day,
               {expr['night']} AS is_night, {platform} AS platform
        FROM read_csv(?, header=true, all_varchar=true, delim=',',
                      null_padding=true, strict_mode=false, auto_detect=true)
      )
    """
    return common + f"""
          SELECT CASE WHEN GROUPING(acq_date)=1 THEN 'grid' ELSE 'daily' END AS aggregation_level,
                 {country} AS country,
                 CASE WHEN GROUPING(acq_date)=1 THEN NULL::DATE ELSE acq_date END AS acq_date,
                 CASE WHEN GROUPING(acq_date)=1 THEN year ELSE NULL::INTEGER END AS year,
                 {family} AS sensor_family,
                 platform, {product_type} AS product_type, {product} AS product,
                 CASE WHEN GROUPING(acq_date)=1 THEN lat_bin ELSE NULL::INTEGER END AS lat_bin,
                 CASE WHEN GROUPING(acq_date)=1 THEN lon_bin ELSE NULL::INTEGER END AS lon_bin,
                 COUNT(*)::BIGINT AS n_detections, SUM(frp)::DOUBLE AS frp_sum_mw,
                 CASE WHEN GROUPING(acq_date)=1 THEN 0 ELSE COUNT(*) FILTER (WHERE detection_type=0) END::BIGINT AS vegetation_n_detections,
                 CASE WHEN GROUPING(acq_date)=1 THEN 0.0 ELSE COALESCE(SUM(frp) FILTER (WHERE detection_type=0),0) END::DOUBLE AS vegetation_frp_sum_mw,
                 CASE WHEN GROUPING(acq_date)=1 THEN 0 ELSE COUNT(*) FILTER (WHERE is_quality) END::BIGINT AS high_quality_n_detections,
                 CASE WHEN GROUPING(acq_date)=1 THEN 0.0 ELSE COALESCE(SUM(frp) FILTER (WHERE is_quality),0) END::DOUBLE AS high_quality_frp_sum_mw,
                 CASE WHEN GROUPING(acq_date)=1 THEN 0 ELSE COUNT(*) FILTER (WHERE is_day) END::BIGINT AS day_n_detections,
                 CASE WHEN GROUPING(acq_date)=1 THEN 0.0 ELSE COALESCE(SUM(frp) FILTER (WHERE is_day),0) END::DOUBLE AS day_frp_sum_mw,
                 CASE WHEN GROUPING(acq_date)=1 THEN 0 ELSE COUNT(*) FILTER (WHERE is_night) END::BIGINT AS night_n_detections,
                 CASE WHEN GROUPING(acq_date)=1 THEN 0.0 ELSE COALESCE(SUM(frp) FILTER (WHERE is_night),0) END::DOUBLE AS night_frp_sum_mw,
                 CASE WHEN GROUPING(acq_date)=1 THEN 0 ELSE 1 END::INTEGER AS platform_day_observed,
                 CASE WHEN GROUPING(acq_date)=1 THEN FALSE ELSE {str(bool(expr['has_type'])).lower()} END AS type_available,
                 CASE WHEN GROUPING(acq_date)=1 THEN FALSE ELSE {str(bool(expr['has_confidence'])).lower()} END AS confidence_available,
                 CASE WHEN GROUPING(acq_date)=1 THEN FALSE ELSE {str(bool(expr['has_daynight'])).lower()} END AS daynight_available,
                 CASE WHEN GROUPING(acq_date)=1 THEN '' ELSE {_sql_literal(str(expr['confidence_column'] or 'missing'))} END AS confidence_column,
                 CASE WHEN GROUPING(acq_date)=1 THEN '' ELSE COALESCE(STRING_AGG(DISTINCT source_version, ','), '') END AS processing_versions
          FROM parsed WHERE {valid}
          GROUP BY GROUPING SETS ((acq_date, platform), (year, platform, lat_bin, lon_bin))
    """


def _atomic_parquet(con: duckdb.DuckDBPyConnection, query: str, source: Path,
                    output: Path) -> tuple[int, int, int]:
    output.parent.mkdir(parents=True, exist_ok=True)
    temp = output.with_name(output.stem + "." + uuid.uuid4().hex + ".tmp.parquet")
    try:
        con.execute(f"COPY ({query}) TO {_sql_literal(str(temp))} (FORMAT PARQUET, COMPRESSION ZSTD)", [str(source)])
        daily_rows, detections, grid_rows = con.execute(
            "SELECT COUNT(*) FILTER (WHERE aggregation_level='daily'), "
            "COALESCE(SUM(n_detections) FILTER (WHERE aggregation_level='daily'),0), "
            "COUNT(*) FILTER (WHERE aggregation_level='grid') FROM read_parquet(?)", [str(temp)]
        ).fetchone()
        os.replace(temp, output)
        con.execute("SELECT COUNT(*) FROM read_parquet(?)", [str(output)]).fetchone()
        return int(daily_rows), int(detections), int(grid_rows)
    except BaseException:
        temp.unlink(missing_ok=True)
        raise


def _output_paths(entry: dict[str, Any]) -> tuple[Path, Path]:
    family, platform, year = _safe(entry["sensor_family"]), _safe(entry["platform"]), int(entry["year"])
    stem = f"{_safe(entry['country'])}--{entry['file_id']}"
    base = DAILY_ROOT / family / platform / str(year)
    output = base / f"{stem}.parquet"
    return output, output


def _disk_free() -> int:
    return shutil.disk_usage(ROOT).free


def _signature(entry: dict[str, Any]) -> dict[str, int]:
    return {"size_bytes": int(entry["size_bytes"]), "modified_ns": int(entry["modified_ns"])}


def _recover_manifest(entries: list[dict[str, Any]]) -> dict[str, Any]:
    """Rebuild a lost checkpoint from completed aggregate files; never reads legacy Parquet."""
    output_entries = []
    for item in entries:
        daily_path, grid_path = _output_paths(item)
        if daily_path.is_file():
            output_entries.append((item, daily_path, grid_path))
    recovered: dict[str, Any] = {"schema_version": SCHEMA_VERSION, "files": {}}
    if not output_entries:
        return recovered

    con = duckdb.connect(":memory:")
    con.execute("PRAGMA memory_limit='2GB'")
    con.execute("PRAGMA threads=4")
    try:
        for item, daily_path, grid_path in output_entries:
            try:
                aggregate = con.execute("""
                    SELECT SUM(n_detections) FILTER (WHERE aggregation_level='daily')::BIGINT,
                           COUNT(*) FILTER (WHERE aggregation_level='daily')::BIGINT,
                           COUNT(*) FILTER (WHERE aggregation_level='grid')::BIGINT,
                           BOOL_OR(confidence_available) FILTER (WHERE aggregation_level='daily'),
                           BOOL_OR(type_available) FILTER (WHERE aggregation_level='daily'),
                           BOOL_OR(daynight_available) FILTER (WHERE aggregation_level='daily'),
                           ANY_VALUE(confidence_column) FILTER (WHERE aggregation_level='daily'),
                           ANY_VALUE(processing_versions) FILTER (WHERE aggregation_level='daily')
                    FROM read_parquet(?)
                """, [str(daily_path)]).fetchone()
            except Exception:
                logging.warning("Ignoring incomplete/corrupt aggregate during checkpoint recovery: %s", daily_path)
                continue
            detections, daily_rows, grid_rows, has_confidence, has_type, has_daynight, confidence_column, versions = aggregate
            record = {
                "source_file": item["source_file"], "file": item["filename"],
                "signature": _signature(item), "size_bytes": int(item["size_bytes"]),
                "mtime_ns": int(item["modified_ns"]), "row_count": int(detections or 0),
                "aggregated_detection_count": int(detections or 0), "daily_row_count": int(daily_rows or 0),
                "grid_row_count": int(grid_rows or 0), "output_file": daily_path.relative_to(ROOT).as_posix(),
                "grid_file": grid_path.relative_to(ROOT).as_posix(),
                "output_size_bytes": daily_path.stat().st_size,
                "sensor_family": item["sensor_family"], "platform": item["platform"],
                "product": item["product"], "product_type": item["product_type"],
                "year": int(item["year"]), "country": item["country"], "status": "complete",
                "confidence_available": bool(has_confidence),
                "confidence_column": confidence_column,
                "type_available": bool(has_type), "daynight_available": bool(has_daynight),
                "processing_versions": [v for v in str(versions or "").split(",") if v],
                "aggregation_format": AGGREGATE_FORMAT, "checkpoint_recovered_from_aggregate": True,
            }
            recovered["files"][item["file_id"]] = record
    finally:
        con.close()
    return recovered


def run(years: set[int] | None = None, countries: set[str] | None = None,
        products: set[str] | None = None, force: bool = False,
        min_free_bytes: int = MIN_FREE_BYTES) -> dict[str, Any]:
    min_free_bytes = max(MIN_FREE_BYTES, int(min_free_bytes))
    sys.path.insert(0, str(ROOT / "backend"))
    from scripts.build_processed import discover_csv_files

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename=LOG_PATH, level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s", force=True)
    country_filter = {c.casefold() for c in countries} if countries else None
    entries = [item for item in discover_csv_files(RAW_ROOT)
               if item.get("supported") and item.get("scope") == "country"
               and item.get("product_type") == "SP"
               and (years is None or int(item["year"]) in years)
               and (country_filter is None or item["country"].casefold() in country_filter)
               and (products is None or item["product"] in products)]
    if not entries:
        raise ValueError("No matching country-scoped FIRMS Standard Processing CSV files were found.")

    manifest_path = MANIFEST_PATH
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if manifest.get("schema_version") not in {1, SCHEMA_VERSION}:
                raise ValueError(f"Unsupported daily manifest schema version: {manifest.get('schema_version')!r}")
            manifest["schema_version"] = SCHEMA_VERSION
        except (json.JSONDecodeError, UnicodeDecodeError):
            backup = manifest_path.with_name("daily_manifest.corrupt.json")
            if not backup.exists():
                shutil.copy2(manifest_path, backup)
            manifest = _recover_manifest(entries)
            logging.warning("Recovered unreadable daily manifest from aggregate Parquet: %d files", len(manifest["files"]))
            _atomic_json(manifest_path, manifest)
    else:
        manifest = {"schema_version": SCHEMA_VERSION, "files": {}}

    groups: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for item in entries:
        groups[(item["product"], int(item["year"]))].append(item)
    results = []

    for (product, year), group in sorted(groups.items()):
        free = _disk_free()
        if free < min_free_bytes:
            message = (f"STOP before {product} {year}: free disk {free / 1024**3:.2f} GiB; "
                       f"at least {min_free_bytes / 1024**3:.2f} GiB required. To continue, review Windows Settings > System > Storage "
                       "and Downloads for files you personally recognize as disposable (such as duplicate ZIP downloads after "
                       "confirming extracted CSVs are intact). Do not delete data/raw/extracted or project intermediates before validation.")
            print(message, flush=True)
            logging.error(message)
            break
        start = time.monotonic()
        logging.info("START sensor-year=%s/%d files=%d free_bytes=%d", product, year, len(group), free)
        year_records = []
        with tempfile.TemporaryDirectory(prefix=f"firewatch-daily-{product}-{year}-") as temp_dir:
            con = duckdb.connect(":memory:")
            con.execute("PRAGMA memory_limit='2GB'")
            con.execute("PRAGMA threads=4")
            con.execute("SET temp_directory=?", [temp_dir])
            con.execute("SET max_temp_directory_size='1500MB'")
            try:
                for item in group:
                    output, grid_output = _output_paths(item)
                    previous = manifest["files"].get(item["file_id"], {})
                    signature = _signature(item)
                    if (not force and previous.get("status") == "complete"
                            and previous.get("aggregation_format") == AGGREGATE_FORMAT
                            and previous.get("signature") == signature
                            and output.is_file()):
                        year_records.append(previous)
                        continue
                    source = Path(item["source_path"])
                    try:
                        expr = _expressions(_header(source), item["sensor_family"])
                        query = _make_source_query(item, expr)
                        daily_rows, detections, grid_rows = _atomic_parquet(con, query, source, output)
                        # Each eligible CSV record has a valid date and coordinate in FIRMS SP files.
                        # Independent raw DuckDB row-count validation is performed by verify_daily.py.
                        row_count = detections
                        version_row = con.execute(
                            "SELECT ANY_VALUE(processing_versions) FROM read_parquet(?) "
                            "WHERE aggregation_level='daily'", [str(output)]
                        ).fetchone()
                        processing_versions = [v for v in str(version_row[0] or "").split(",") if v]
                        result = {
                            "source_file": item["source_file"], "file": item["filename"],
                            "signature": signature, "size_bytes": signature["size_bytes"],
                            "mtime_ns": signature["modified_ns"], "row_count": row_count,
                            "aggregated_detection_count": detections, "daily_row_count": daily_rows,
                            "grid_row_count": grid_rows,
                            "output_file": output.relative_to(ROOT).as_posix(),
                            "grid_file": grid_output.relative_to(ROOT).as_posix(),
                            "output_size_bytes": output.stat().st_size,
                            "sensor_family": item["sensor_family"], "platform": item["platform"],
                            "product": item["product"], "product_type": item["product_type"],
                            "year": year, "country": item["country"], "status": "complete",
                            "confidence_available": expr["has_confidence"],
                            "confidence_column": expr["confidence_column"],
                            "type_available": expr["has_type"], "daynight_available": expr["has_daynight"],
                            "processing_versions": processing_versions,
                            "aggregation_format": AGGREGATE_FORMAT,
                        }
                        manifest["files"][item["file_id"]] = result
                        year_records.append(result)
                        _atomic_json(manifest_path, manifest)
                    except Exception as exc:
                        manifest["files"][item["file_id"]] = {
                            "source_file": item["source_file"], "file": item["filename"],
                            "signature": signature, "size_bytes": signature["size_bytes"],
                            "mtime_ns": signature["modified_ns"], "row_count": None,
                            "status": "failed", "error": f"{type(exc).__name__}: {exc}",
                        }
                        _atomic_json(manifest_path, manifest)
                        logging.exception("FAILED source=%s", item["source_file"])
                        raise RuntimeError(f"Could not aggregate {item['source_file']}: {type(exc).__name__}: {exc}") from exc
            finally:
                con.close()

        free_after = _disk_free()
        summary = {
            "product": product, "year": year, "files": len(group),
            "rows": sum(int(record.get("row_count") or 0) for record in year_records),
            "detections": sum(int(record.get("aggregated_detection_count") or 0) for record in year_records),
            "aggregate_bytes": sum(int(record.get("output_size_bytes") or 0) for record in year_records),
            "free_bytes_after": free_after, "seconds": round(time.monotonic() - start, 2),
        }
        results.append(summary)
        logging.info("END sensor-year=%s/%d rows=%d detections=%d output_bytes=%d free_bytes=%d elapsed_seconds=%.2f",
                     product, year, summary["rows"], summary["detections"],
                     summary["aggregate_bytes"], free_after, summary["seconds"])
        print(json.dumps(summary), flush=True)
        if free_after < min_free_bytes:
            message = (f"STOP after {product} {year}: free disk fell below {min_free_bytes / 1024**3:.2f} GiB; "
                       f"{free_after / 1024**3:.2f} GiB remains. Review Windows Settings > System > Storage and Downloads "
                       "for files you personally recognize as disposable; do not delete data/raw/extracted or project intermediates before validation.")
            print(message, flush=True)
            logging.error(message)
            break
    return {"groups_processed": len(results), "files_complete": sum(
        1 for record in manifest["files"].values() if record.get("status") == "complete"),
        "results": results, "manifest": str(manifest_path), "log": str(LOG_PATH)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--year", type=int, action="append", help="Restrict to a year (repeatable). Defaults to 2020-2025.")
    parser.add_argument("--country", action="append", help="Restrict to a country (repeatable).")
    parser.add_argument("--product", action="append", help="Restrict product (e.g. MODIS_SP or VIIRS_SNPP_SP).")
    parser.add_argument("--all-years", action="store_true", help="Process every supported local SP country CSV year.")
    parser.add_argument("--force", action="store_true", help="Rebuild outputs even when the input signature is unchanged.")
    parser.add_argument("--min-free-gb", type=float, default=3.0, help="Free-space floor before and after each sensor-year (minimum 3 GiB; may be raised).")
    args = parser.parse_args()
    years = None if args.all_years else set(args.year if args.year else DEFAULT_YEARS)
    result = run(years, set(args.country) if args.country else None,
                 set(args.product) if args.product else None, args.force,
                 int(args.min_free_gb * 1024**3))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
