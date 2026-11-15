"""Bounded local API queries over processed Parquet; no NASA network access."""
from __future__ import annotations

import json
import threading
from datetime import date
from pathlib import Path
from typing import Any

import duckdb

from app.harmonize import HarmonizationQueryError, _validate_bbox, query_common_grid_comparison

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_ROOT = PROJECT_ROOT / "data" / "processed"
DAILY_CELLS = PROCESSED_ROOT / "daily_cell"
QUALITY_REPORT = PROCESSED_ROOT / "quality_report.json"
MAX_CALENDAR_DAYS = 366
MAX_BASELINE_DAYS = 366 * 27
QUERY_TIMEOUT_SECONDS = 30


def daily_cell_paths() -> list[Path]:
    if DAILY_CELLS.is_file():
        return [DAILY_CELLS]
    if DAILY_CELLS.is_dir():
        return sorted(DAILY_CELLS.rglob("*.parquet"))
    legacy = PROCESSED_ROOT / "daily_cell.parquet"
    return [legacy] if legacy.is_file() else []


class AnalyticsQueryError(ValueError):
    """Actionable local-analytics query error."""


class AnalyticsTimeout(TimeoutError):
    """A bounded DuckDB query exceeded its time budget."""


def validate_bbox(bbox: list[float] | None) -> None:
    try:
        _validate_bbox(bbox)
    except HarmonizationQueryError as exc:
        raise AnalyticsQueryError(str(exc)) from exc


def parse_geojson_polygon(value: str | None) -> list[list[list[list[float]]]] | None:
    if value is None:
        return None
    try:
        geometry = json.loads(value)
    except json.JSONDecodeError as exc:
        raise AnalyticsQueryError("geojson must be valid JSON containing a GeoJSON Polygon or MultiPolygon.") from exc
    if not isinstance(geometry, dict) or geometry.get("type") not in {"Polygon", "MultiPolygon"}:
        raise AnalyticsQueryError("geojson must be a GeoJSON Polygon or MultiPolygon in WGS84 longitude/latitude coordinates.")
    if geometry.get("crs") not in (None, {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}):
        raise AnalyticsQueryError("Only WGS84 longitude/latitude GeoJSON coordinates are supported.")
    coordinates = geometry.get("coordinates")
    if geometry["type"] == "Polygon":
        polygons = [coordinates]
    else:
        polygons = coordinates
    if not isinstance(polygons, list):
        raise AnalyticsQueryError("GeoJSON coordinates must contain Polygon rings.")
    if sum(len(ring) for polygon in polygons if isinstance(polygon, list) for ring in polygon if isinstance(ring, list)) > 2570:
        raise AnalyticsQueryError("GeoJSON AOI is too detailed; limit to 10 polygons and 257 positions per ring.")
    return polygons


def _validate_range(start_date: date, end_date: date, maximum: int) -> None:
    if start_date > end_date:
        raise AnalyticsQueryError("start_date must be on or before end_date.")
    if (end_date - start_date).days + 1 > maximum:
        raise AnalyticsQueryError(f"This query is limited to {maximum} days. Split the date range and retry.")


def get_calendar(
    start_date: date,
    end_date: date,
    *,
    product_type: str = "SP",
    platforms: list[str] | None = None,
    daynight: str | None = None,
    bbox: list[float] | None = None,
    geojson: str | None = None,
) -> dict[str, Any]:
    _validate_range(start_date, end_date, MAX_CALENDAR_DAYS)
    polygons = parse_geojson_polygon(geojson)
    if bbox is not None and polygons is not None:
        raise AnalyticsQueryError("Provide either bbox or geojson, not both.")
    cell_files = daily_cell_paths()
    if not cell_files:
        raise AnalyticsQueryError("Processed daily-cell data is not available yet. Run backend/scripts/build_processed.py --build-daily-cells.")
    con = duckdb.connect(database=":memory:")
    con.execute("SET memory_limit='1GB'")
    con.execute("SET threads=4")
    timer = threading.Timer(QUERY_TIMEOUT_SECONDS, con.interrupt)
    timer.start()
    try:
        result = query_common_grid_comparison(
            con, cell_files, start_date, end_date,
            product_type=product_type, platforms=platforms, daynight=daynight,
            bbox=bbox, polygons=polygons,
        )
    except duckdb.InterruptException as exc:
        raise AnalyticsTimeout(f"Analytics query exceeded {QUERY_TIMEOUT_SECONDS} seconds. Reduce the date range or AOI.") from exc
    except HarmonizationQueryError as exc:
        raise AnalyticsQueryError(str(exc)) from exc
    finally:
        timer.cancel()
        con.close()
    result.update({
        "data_status": "Processed local FIRMS archives",
        "coverage_manifest": "data/processed/quality_report.json",
        "aoi_mode": "GeoJSON polygon by cell center" if polygons is not None else ("bounding box" if bbox else "global"),
        "time_standard": "UTC acquisition date",
    })
    return result


def coverage_status() -> dict[str, Any]:
    if not QUALITY_REPORT.is_file():
        return {"status": "no_processed_data", "processed_files": 0, "coverage": None}
    try:
        report = json.loads(QUALITY_REPORT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AnalyticsQueryError("The processed-data quality report is unreadable; rerun the archive processor.") from exc
    coverage_rows = report.get("coverage_by_product_platform_year", [])
    return {
        "status": "partial_local_archive" if report.get("files_processed_total", 0) < report.get("files_discovered", 0) else "indexed_local_archive",
        "files_discovered": report.get("files_discovered", 0),
        "files_processed": report.get("files_processed_total", 0),
        "files_failed": report.get("files_failed_total", 0),
        "files_expected": report.get("files_expected", report.get("files_discovered", 0)),
        "rows_by_sensor_year_product": report.get("rows_by_sensor_year_product", {}),
        "coverage": report.get("coverage"),
        "coverage_by_product_platform_year": coverage_rows,
        "daily_cells": report.get("daily_cells"),
        "interpretation": "Local processed-file coverage only. Missing dates or products are not evidence of zero fire activity.",
    }


def check_coverage(
    start_date: date,
    end_date: date,
    *,
    product_type: str,
    platform: str | None = None,
    bbox: list[float] | None = None,
) -> dict[str, Any]:
    """Check source-file date envelopes without claiming observation opportunity."""
    if start_date > end_date:
        raise AnalyticsQueryError("start must be on or before end.")
    if product_type not in {"SP", "NRT"}:
        raise AnalyticsQueryError("product_type must be SP or NRT.")
    validate_bbox(bbox)
    table = coverage_status().get("coverage_by_product_platform_year", [])
    candidates = [row for row in table if row.get("product_type") == product_type
                 and (platform is None or row.get("platform") == platform)]
    overlapping = []
    partial_overlapping = []
    for row in candidates:
        if not row.get("first_date") or not row.get("last_date"):
            continue
        first, last = date.fromisoformat(row["first_date"]), date.fromisoformat(row["last_date"])
        if last < start_date or first > end_date:
            continue
        summary = {key: row.get(key) for key in ("product_type", "platform", "year", "first_date", "last_date", "files_expected", "files_processed", "status", "source_scope")}
        (overlapping if row.get("status") == "complete" else partial_overlapping).append(summary)

    spans = []
    for item in overlapping:
        first = max(start_date, date.fromisoformat(item["first_date"]))
        last = min(end_date, date.fromisoformat(item["last_date"]))
        if first <= last:
            spans.append((first, last))
    spans.sort()
    cursor = start_date
    fully_covered = bool(spans)
    for first, last in spans:
        if first > cursor:
            fully_covered = False
            break
        cursor = max(cursor, last.fromordinal(last.toordinal() + 1))
        if cursor > end_date:
            break
    if cursor <= end_date:
        fully_covered = False
    if fully_covered:
        status = "fully_covered"
    elif spans or partial_overlapping:
        status = "partly_covered"
    else:
        status = "not_covered"

    nearest_pool = candidates or table
    nearest = min(nearest_pool, key=lambda row: min(
        abs((start_date - date.fromisoformat(row["last_date"])).days) if row.get("last_date") and date.fromisoformat(row["last_date"]) < start_date else 10**9,
        abs((date.fromisoformat(row["first_date"]) - end_date).days) if row.get("first_date") and date.fromisoformat(row["first_date"]) > end_date else 10**9,
    ), default=None)
    alternatives = []
    if not overlapping and not partial_overlapping:
        alternate_type = "NRT" if product_type == "SP" else "SP"
        alternatives = [row for row in table if row.get("product_type") == alternate_type
                       and (platform is None or row.get("platform") == platform)
                       and row.get("first_date") and row.get("last_date")
                       and date.fromisoformat(row["first_date"]) <= end_date
                       and date.fromisoformat(row["last_date"]) >= start_date]
    return {
        "status": status,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "product_type": product_type,
        "platform": platform,
        "complete_source_ranges": overlapping,
        "partial_source_ranges": partial_overlapping,
        "nearest_valid_range": None if nearest is None else {"product_type": nearest.get("product_type"), "platform": nearest.get("platform"), "year": nearest.get("year"), "first_date": nearest.get("first_date"), "last_date": nearest.get("last_date"), "status": nearest.get("status")},
        "suggested_product_type": alternatives[0]["product_type"] if alternatives else None,
        "spatial_coverage": "not_assessed" if bbox is not None else "global_date_envelope_only",
        "coverage_basis": "Completeness of discovered source files and their observed date envelopes; this does not establish daily observation opportunity or zero fire activity.",
    }


def unavailable_analysis(name: str, start_date: date, end_date: date) -> dict[str, Any]:
    _validate_range(start_date, end_date, MAX_BASELINE_DAYS)
    coverage = coverage_status()
    return {
        "status": "insufficient_baseline",
        "analysis": name,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "results": [],
        "sample_size": 0,
        "baseline_coverage": coverage,
        "reason": "A validated, adequately covered multi-year baseline and observation-opportunity inputs are not available for this local archive. No zero-fill or scientific anomaly/season estimate was produced.",
        "method_version": None,
    }
