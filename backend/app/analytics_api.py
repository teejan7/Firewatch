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
DAILY_CELLS = PROCESSED_ROOT / "daily_cell.parquet"
QUALITY_REPORT = PROCESSED_ROOT / "quality_report.json"
MAX_CALENDAR_DAYS = 366
MAX_BASELINE_DAYS = 366 * 27
QUERY_TIMEOUT_SECONDS = 30


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
    if not DAILY_CELLS.is_file():
        raise AnalyticsQueryError("Processed daily-cell data is not available yet. Run backend/scripts/build_processed.py --build-daily-cells.")
    con = duckdb.connect(database=":memory:")
    con.execute("SET memory_limit='1GB'")
    con.execute("SET threads=4")
    timer = threading.Timer(QUERY_TIMEOUT_SECONDS, con.interrupt)
    timer.start()
    try:
        result = query_common_grid_comparison(
            con, [DAILY_CELLS], start_date, end_date,
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
    return {
        "status": "partial_local_archive" if report.get("files_processed_total", 0) < report.get("files_discovered", 0) else "indexed_local_archive",
        "files_discovered": report.get("files_discovered", 0),
        "files_processed": report.get("files_processed_total", 0),
        "files_failed": report.get("files_failed_total", 0),
        "rows_by_sensor_year_product": report.get("rows_by_sensor_year_product", {}),
        "coverage": report.get("coverage"),
        "daily_cells": report.get("daily_cells"),
        "interpretation": "Local processed-file coverage only. Missing dates or products are not evidence of zero fire activity.",
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
