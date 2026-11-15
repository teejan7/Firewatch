"""Export small, source-aware country summaries from validated Parquet.

This script does not harmonize MODIS and VIIRS. It is resumable at the export
level (replace-on-success JSON writes) and never modifies raw CSV inputs.
Only already processed country-scoped Standard Processing files are included.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = ROOT / "frontend" / "public" / "data"
METHOD_VERSION = "firewatch-static-0.2"


def _atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    temporary.replace(path)


def _load_sources(processed_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Load only the compact daily-aggregate manifest; never read row-level Parquet."""
    manifest_path = processed_root / "daily_manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Daily aggregate manifest not found: {manifest_path}. Run backend/scripts/build_daily.py first.")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    legacy = [entry for entry in manifest.get("files", {}).values()
              if entry.get("status") == "complete" and entry.get("product_type") == "SP"
              and entry.get("country") and entry.get("aggregation_format") != 2]
    if legacy:
        raise ValueError(f"{len(legacy):,} daily files use the previous aggregate format. "
                         "Run backend/scripts/build_daily.py --force before exporting static data.")
    sources = []
    for file_id, entry in manifest.get("files", {}).items():
        if entry.get("status") != "complete" or entry.get("product_type") != "SP" or not entry.get("country"):
            continue
        relative, grid_relative = entry.get("output_file"), entry.get("grid_file")
        if not relative or not grid_relative:
            continue
        def resolve_output(value: str) -> Path:
            candidate = Path(value)
            if candidate.is_absolute():
                return candidate.resolve()
            base = ROOT if candidate.parts[:2] == ("data", "processed") else processed_root
            return (base / candidate).resolve()

        output, grid_output = resolve_output(relative), resolve_output(grid_relative)
        if not output.is_file() or not grid_output.is_file():
            continue
        family = entry.get("sensor_family")
        platform = entry.get("platform")
        if family not in {"MODIS", "VIIRS"} or not platform:
            continue
        sources.append({
            "file_id": file_id,
            "source_file": entry.get("source_file", ""),
            "country": entry["country"],
            "year": int(entry["year"]),
            "sensor_family": family,
            "platform": platform,
            "product_type": "SP",
            "product": entry.get("product", ""),
            "output_file": output,
            "grid_file": grid_output,
            "rows_processed": int(entry.get("aggregated_detection_count") or 0),
            "rows_source": int(entry.get("row_count") or 0),
            "duplicates": 0,
            "invalid": max(0, int(entry.get("row_count") or 0) - int(entry.get("aggregated_detection_count") or 0)),
            "processing_versions": entry.get("processing_versions", []),
        })
    return manifest, sources


def load_sources(processed_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Public testable wrapper for source inventory selection."""
    return _load_sources(processed_root)


def _daily_rows(connection: duckdb.DuckDBPyConnection, sources: list[dict[str, Any]]) -> list[tuple[Any, ...]]:
    paths = [str(source["output_file"]) for source in sources]
    if not paths:
        return []
    return connection.execute("""
        SELECT country, CAST(acq_date AS VARCHAR), sensor_family, platform,
               product_type, SUM(n_detections)::BIGINT, SUM(frp_sum_mw)::DOUBLE,
               CASE WHEN SUM(n_detections)>0
                    THEN SUM(day_n_detections)::DOUBLE/SUM(n_detections) ELSE NULL END,
               SUM(vegetation_n_detections)::BIGINT, SUM(vegetation_frp_sum_mw)::DOUBLE,
               SUM(high_quality_n_detections)::BIGINT, SUM(high_quality_frp_sum_mw)::DOUBLE,
               SUM(day_n_detections)::BIGINT, SUM(day_frp_sum_mw)::DOUBLE,
               SUM(night_n_detections)::BIGINT, SUM(night_frp_sum_mw)::DOUBLE,
               MAX(platform_day_observed)::INTEGER,
               BOOL_OR(type_available), BOOL_OR(confidence_available), BOOL_OR(daynight_available)
        FROM read_parquet(?, union_by_name=true)
        WHERE aggregation_level='daily'
        GROUP BY country, acq_date, sensor_family, platform, product_type
        ORDER BY country, acq_date, sensor_family, platform
    """, [paths]).fetchall()


def _grid_rows(connection: duckdb.DuckDBPyConnection, sources: list[dict[str, Any]]) -> list[tuple[Any, ...]]:
    paths = [str(source["output_file"]) for source in sources]
    if not paths:
        return []
    return connection.execute("""
        SELECT country, year, sensor_family, platform, product_type, lat_bin, lon_bin,
               SUM(n_detections)::BIGINT, SUM(frp_sum_mw)::DOUBLE
        FROM read_parquet(?, union_by_name=true)
        WHERE aggregation_level='grid'
        GROUP BY country, year, sensor_family, platform, product_type, lat_bin, lon_bin
    """, [paths]).fetchall()


def _expected_coverage(sources: list[dict[str, Any]]) -> dict[str, Any]:
    """Compare processed files to local extracted filenames; never contacts NASA."""
    sys.path.insert(0, str(ROOT / "backend"))
    try:
        from scripts.build_processed import discover_csv_files
        discovered = discover_csv_files(ROOT / "data" / "raw" / "extracted")
    except (ImportError, OSError):
        discovered = []
    processed_paths = {s["source_file"] for s in sources}
    groups: dict[tuple[str, int], dict[str, int]] = defaultdict(lambda: {"expected": 0, "processed": 0, "rows": 0})
    country_groups: dict[tuple[str, str, int], dict[str, int]] = defaultdict(lambda: {"expected": 0, "processed": 0, "rows": 0})
    for item in discovered:
        if not item.get("supported") or item.get("scope") != "country" or item.get("product_type") != "SP":
            continue
        key = (item["product"], int(item["year"]))
        groups[key]["expected"] += 1
        country_key = (item["country"], item["product"], int(item["year"]))
        country_groups[country_key]["expected"] += 1
        if item["source_file"] in processed_paths:
            groups[key]["processed"] += 1
            country_groups[country_key]["processed"] += 1
    for source in sources:
        groups[(source["product"], source["year"])]["rows"] += source["rows_processed"]
        country_groups[(source["country"], source["product"], source["year"])]["rows"] += source["rows_processed"]
    coverage = []
    for (product, year), counts in sorted(groups.items()):
        coverage.append({"product": product, "year": year, **counts,
                         "status": "complete" if counts["expected"] and counts["expected"] == counts["processed"] else "partial" if counts["processed"] else "not_processed"})
    country_coverage = []
    for (country, product, year), counts in sorted(country_groups.items()):
        country_coverage.append({"country": country, "product": product, "year": year, **counts,
                                 "status": "complete" if counts["expected"] and counts["expected"] == counts["processed"] else "partial" if counts["processed"] else "not_processed"})
    return {"files_discovered_supported_country_sp": sum(1 for item in discovered if item.get("supported") and item.get("scope") == "country" and item.get("product_type") == "SP"),
            "processed_country_files_in_export": len(sources), "by_product_year": coverage,
            "by_country_product_year": country_coverage,
            "years_present": sorted({s["year"] for s in sources}),
            "years_missing_from_export": sorted(set(range(2000, 2027)) - {s["year"] for s in sources}),
            "global_noaa21_scope": "excluded from country dataset; source records remain in local processed inputs where present"}


def build(processed_root: Path = ROOT / "data" / "processed", output: Path = DEFAULT_OUTPUT) -> dict[str, Any]:
    manifest, sources = _load_sources(processed_root)
    if not sources:
        raise ValueError("No country-scoped processed SP Parquet files are available. Run the source processor first.")
    print(f"Reading {len(sources):,} processed country SP files from the local manifest; raw CSVs are untouched.", flush=True)
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="firewatch-duckdb-") as temp_dir:
        connection = duckdb.connect(":memory:")
        connection.execute("PRAGMA memory_limit='2GB'")
        connection.execute("PRAGMA threads=4")
        connection.execute("SET temp_directory=?", [str(Path(temp_dir).resolve())])
        connection.execute("SET max_temp_directory_size='2GB'")
        print("Aggregating daily source metrics and 1-degree map cells (sensor/platform kept separate)…", flush=True)
        daily_rows = _daily_rows(connection, sources)
        grid_rows = _grid_rows(connection, sources)
        connection.close()

    daily_by_country: dict[str, list[list[Any]]] = defaultdict(list)
    grid_by_country: dict[str, list[list[Any]]] = defaultdict(list)
    for row in daily_rows:
        (country, day, family, platform, product_type, count, frp, day_fraction,
         vegetation_n, vegetation_frp, high_quality_n, high_quality_frp,
         day_n, day_frp, night_n, night_frp, observed, type_available,
         confidence_available, daynight_available) = row
        # Preserve the existing compact browser-series schema. The complete
        # quality/type/day-night metrics are appended for the detailed CSV export.
        daily_by_country[country].append([
            day, family, platform, product_type, int(count or 0), round(float(frp or 0), 2),
            round(day_fraction, 4) if day_fraction is not None else None,
            int(vegetation_n or 0), round(float(vegetation_frp or 0), 2),
            int(high_quality_n or 0), round(float(high_quality_frp or 0), 2),
            int(day_n or 0), round(float(day_frp or 0), 2), int(night_n or 0),
            round(float(night_frp or 0), 2), int(observed or 0),
            bool(type_available), bool(confidence_available), bool(daynight_available),
        ])
    bounds: dict[str, list[float]] = {}
    for country, year, family, platform, product_type, lat_bin, lon_bin, count, frp in grid_rows:
        lat, lon = -90 + int(lat_bin) + 0.5, -180 + int(lon_bin) + 0.5
        grid_by_country[country].append([int(year), family, platform, product_type, lat, lon, int(count or 0), round(float(frp or 0), 2)])
        if country not in bounds:
            bounds[country] = [lon, lat, lon, lat]
        else:
            b = bounds[country]
            b[0] = min(b[0], lon)
            b[1] = min(b[1], lat)
            b[2] = max(b[2], lon)
            b[3] = max(b[3], lat)

    coverage = _expected_coverage(sources)
    per_country: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for source in sources:
        per_country[source["country"]].append(source)
    print(f"Writing {len(set(daily_by_country) | set(per_country)):,} country series and coverage reports…", flush=True)
    countries = []
    map_activity = []
    for name in sorted(set(daily_by_country) | set(per_country)):
        slug = re.sub(r"[^a-z0-9]+", "-", name.casefold()).strip("-")
        records = daily_by_country[name]
        dates = [row[0] for row in records]
        item = per_country[name]
        products = sorted({s["product"] for s in item})
        # The processed row-level platform is populated from the source
        # satellite field (e.g. Terra/Aqua for MODIS), unlike the manifest's
        # broad product label (`MODIS`).
        platforms = sorted({row[2] for row in records})
        years = sorted({s["year"] for s in item})
        activity: dict[int, dict[str, float]] = defaultdict(lambda: {"modis_detections": 0, "viirs_detections": 0, "modis_frp_sum_mw": 0.0, "viirs_frp_sum_mw": 0.0})
        monthly_activity: dict[tuple[int, int], dict[str, float]] = defaultdict(lambda: {"modis_detections": 0, "viirs_detections": 0, "modis_frp_sum_mw": 0.0, "viirs_frp_sum_mw": 0.0})
        for row in records:
            year_month = (int(row[0][:4]), int(row[0][5:7]))
            stats = activity[year_month[0]]
            month_stats = monthly_activity[year_month]
            family_prefix = row[1].lower()
            stats[f"{family_prefix}_detections"] += int(row[4])
            stats[f"{family_prefix}_frp_sum_mw"] += float(row[5])
            month_stats[f"{family_prefix}_detections"] += int(row[4])
            month_stats[f"{family_prefix}_frp_sum_mw"] += float(row[5])
        cells = grid_by_country[name]
        weight = sum(row[6] for row in cells)
        centroid = None if not weight else [
            round(sum(row[5] * row[6] for row in cells) / weight, 3),
            round(sum(row[4] * row[6] for row in cells) / weight, 3),
        ]
        country_coverage = [row for row in coverage["by_country_product_year"] if row["country"] == name]
        series = {
            "schema_version": 1,
            "method_version": METHOD_VERSION,
            "country": name,
            "country_name_source": "FIRMS extracted source filename; no external boundary crosswalk applied",
            "data_status": "Partial local NASA FIRMS Standard Processing archive; see file-level coverage",
            "coverage": {"first_date": min(dates) if dates else None, "last_date": max(dates) if dates else None,
                         "years": years, "products": products, "platforms": platforms,
                         "processed_source_files": len(item),
                         "source_rows_processed": sum(s["rows_processed"] for s in item),
                         "by_product_year": [row for row in coverage["by_country_product_year"] if row["country"] == name]},
            "metric_definition": "Daily source detections and FRP are aggregated by FIRMS country file, acquisition date, sensor family and platform. Daily records also contain vegetation (type=0), confidence-filtered and day/night counts and FRP, and a reported-detection platform-day flag. The platform-day flag is not an observation-opportunity denominator. Missing dates are omitted, not zero-filled.",
            "harmonization_status": "not applied; FRP and detection counts remain sensor-specific",
            "daily_columns": ["acq_date_utc", "sensor_family", "platform", "product_type", "n_detections", "frp_sum_mw", "day_fraction", "vegetation_n_detections", "vegetation_frp_sum_mw", "high_quality_n_detections", "high_quality_frp_sum_mw", "day_n_detections", "day_frp_sum_mw", "night_n_detections", "night_frp_sum_mw", "platform_day_observed", "type_available", "confidence_available", "daynight_available"],
            "daily": sorted(records, key=lambda r: (r[0], r[1], r[2], r[3])),
            "grid_columns": ["year", "sensor_family", "platform", "product_type", "latitude_1deg_cell_center", "longitude_1deg_cell_center", "n_detections", "frp_sum_mw"],
            "grid": sorted(grid_by_country[name], key=lambda r: (r[0], r[1], r[2], r[4], r[5])),
            "grid_definition": "1-degree display aggregation of detected records; not a calibrated sensor comparison or boundary polygon",
            "source_files": [{"source_file": s["source_file"], "file_id": s["file_id"], "product": s["product"],
                              "sensor_family": s["sensor_family"], "platform_product_label": s["platform"], "year": s["year"],
                              "rows_source": s["rows_source"], "rows_processed": s["rows_processed"],
                              "processing_versions": s["processing_versions"]} for s in sorted(item, key=lambda s: (s["year"], s["product"]))],
        }
        _atomic_json(output / "series" / f"{slug}.json", series)
        map_activity.append({"name": name,
                           "activity_by_year": [{"year": y, **{k: round(v, 2) if k.endswith("frp_sum_mw") else int(v) for k, v in stats.items()}} for y, stats in sorted(activity.items())],
                           "activity_by_month": [{"year": y, "month": m, **{k: round(v, 2) if k.endswith("frp_sum_mw") else int(v) for k, v in stats.items()}} for (y, m), stats in sorted(monthly_activity.items())],
                           "coverage_by_product_year": country_coverage})
        countries.append({"name": name, "slug": slug, "coverage_years": years, "first_date": series["coverage"]["first_date"],
                          "last_date": series["coverage"]["last_date"], "products": products, "platforms": platforms,
                          "processed_source_files": len(item), "observed_bbox": bounds.get(name),
                          "bbox_note": "Extent of aggregated detected cells, not official country boundary.",
                          "observed_centroid_lon_lat": centroid})

    _atomic_json(output / "countries.json", {"schema_version": 1, "method_version": METHOD_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "data_status": "PARTIAL LOCAL FIRMS SP ARCHIVE — NOT A COMPLETE GLOBAL TIME SERIES",
        "countries": countries})
    _atomic_json(output / "map_activity.json", {"schema_version": 1, "method_version": METHOD_VERSION,
        "data_status": "PARTIAL LOCAL FIRMS SP ARCHIVE — MAP SUMMARIES ONLY",
        "countries": map_activity})
    _atomic_json(output / "quality.json", {"schema_version": 1, "method_version": METHOD_VERSION,
        "files_processed": len(sources), "rows_processed": sum(s["rows_processed"] for s in sources),
        "invalid_date_or_coordinate_rows_reported": sum(s["invalid"] for s in sources),
        "exact_duplicate_rows_reported": sum(s["duplicates"] for s in sources),
        "coverage": coverage,
        "source_name_mapping": "Original FIRMS country strings retained; Natural Earth crosswalk/boundary file was not available and has not been fabricated.",
        "calibration": "not performed; no harmonized index, anomaly, trend, or validated critical period is published.",
        "input_provenance": "data/processed/daily_manifest.json and original source_file metadata; daily aggregation Parquet only"})
    _atomic_json(output / "methods_validation.json", {"schema_version": 1, "method_version": METHOD_VERSION,
        "status": "not_calibrated", "harmonized_index": None,
        "validation_metrics": None,
        "reason": "The current processed snapshot does not provide the required 2012–2022 complete paired calibration years across MODIS and VIIRS, a complete 2023–2025 holdout, or sensor observation-opportunity denominators. Fitting a scale from these partial source detections would not establish comparable measurements.",
        "available_source_years": coverage["years_present"],
        "methods_required_before_calibration": ["review the official product/collection documentation", "define quality filters and same-area observation opportunities", "pre-register temporal training/holdout rules", "validate platform continuity and uncertainty", "publish independent country-level holdout metrics"]})
    output_bytes = sum(path.stat().st_size for path in output.rglob("*.json") if path.is_file())
    if output_bytes > 120 * 1024 * 1024:
        raise ValueError(f"Static country JSON is {output_bytes / 1024**2:.1f} MB; maximum is 120 MiB. Reduce the packaged coverage before deployment.")
    return {"files_processed": len(sources), "rows_processed": sum(s["rows_processed"] for s in sources),
            "countries": len(countries), "years": coverage["years_present"], "output_bytes": output_bytes, "output": str(output)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--processed", type=Path, default=ROOT / "data" / "processed")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = build(args.processed.resolve(), args.output.resolve())
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
