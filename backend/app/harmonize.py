"""Sensor-aware comparison on shared cells; no cross-sensor calibration is applied.

The common 0.25-degree UTC cell-day is an analytical comparison unit, not a fire
count. Source detections, products, platforms, and SP/NRT processing remain distinct.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Sequence

METHOD_NAME = "common-grid sensor comparison"
METHOD_VERSION = "1.0.0"
PRODUCT_TYPES = {"SP", "NRT"}
PLATFORMS = {"Terra", "Aqua", "S-NPP", "NOAA-20", "NOAA-21"}


class HarmonizationQueryError(ValueError):
    """Invalid request for the sensor-comparison layer."""


def _as_date(value: date | str, field: str) -> date:
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise HarmonizationQueryError(f"{field} must be a calendar date in YYYY-MM-DD format.") from exc


def _validate_bbox(bbox: Sequence[float] | None) -> tuple[float, float, float, float] | None:
    if bbox is None:
        return None
    if len(bbox) != 4:
        raise HarmonizationQueryError("bbox must contain west, south, east, north.")
    try:
        west, south, east, north = (float(value) for value in bbox)
    except (TypeError, ValueError) as exc:
        raise HarmonizationQueryError("bbox coordinates must be numeric.") from exc
    if not (-180 <= west < east <= 180 and -90 <= south < north <= 90):
        raise HarmonizationQueryError("bbox must satisfy -180 ≤ west < east ≤ 180 and -90 ≤ south < north ≤ 90; antimeridian-crossing boxes are not supported yet.")
    return west, south, east, north


def _orientation(a: Sequence[float], b: Sequence[float], c: Sequence[float]) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _rings_sql(polygons: Sequence[Sequence[Sequence[Sequence[float]]]]) -> tuple[str, tuple[float, float, float, float]]:
    """Validate GeoJSON lon/lat rings and return a DuckDB center-in-polygon predicate."""
    if not polygons or len(polygons) > 10:
        raise HarmonizationQueryError("GeoJSON must contain between 1 and 10 polygons.")
    normalized: list[list[list[tuple[float, float]]]] = []
    for polygon in polygons:
        if not polygon:
            raise HarmonizationQueryError("Each polygon must have an exterior ring.")
        rings: list[list[tuple[float, float]]] = []
        for ring in polygon:
            if not isinstance(ring, (list, tuple)) or not 4 <= len(ring) <= 257:
                raise HarmonizationQueryError("Each ring needs 4 to 257 positions (including its closing position).")
            points: list[tuple[float, float]] = []
            for coord in ring:
                try:
                    lon, lat = float(coord[0]), float(coord[1])
                except (TypeError, ValueError, IndexError) as exc:
                    raise HarmonizationQueryError("GeoJSON positions must contain numeric longitude and latitude.") from exc
                if not (-180 <= lon <= 180 and -90 <= lat <= 90):
                    raise HarmonizationQueryError("GeoJSON coordinates must use WGS84 longitude/latitude bounds.")
                points.append((lon, lat))
            if points[0] != points[-1]:
                raise HarmonizationQueryError("GeoJSON rings must be closed (first and last positions must match).")
            if max(p[0] for p in points) - min(p[0] for p in points) > 180:
                raise HarmonizationQueryError("Antimeridian-crossing polygons are not supported yet.")
            edges = list(zip(points[:-1], points[1:]))
            for i, (a, b) in enumerate(edges):
                for j in range(i + 1, len(edges)):
                    if j in (i, i + 1) or (i == 0 and j == len(edges) - 1):
                        continue
                    c, d = edges[j]
                    o1, o2, o3, o4 = _orientation(a, b, c), _orientation(a, b, d), _orientation(c, d, a), _orientation(c, d, b)
                    def on_segment(p, q, r):
                        return min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and min(p[1], r[1]) <= q[1] <= max(p[1], r[1])
                    intersects = (o1 * o2 < 0 and o3 * o4 < 0) or (o1 == 0 and on_segment(a, c, b)) or (o2 == 0 and on_segment(a, d, b)) or (o3 == 0 and on_segment(c, a, d)) or (o4 == 0 and on_segment(c, b, d))
                    if intersects:
                        raise HarmonizationQueryError("GeoJSON ring self-intersects; provide a valid Polygon or MultiPolygon.")
            if abs(sum(points[i][0] * points[i + 1][1] - points[i + 1][0] * points[i][1] for i in range(len(points) - 1))) < 1e-12:
                raise HarmonizationQueryError("GeoJSON rings must enclose a non-zero area.")
            rings.append(points)
        normalized.append(rings)

    lat_expr = "(-90.0 + 0.25 * (lat_i + 0.5))"
    lon_expr = "(-180.0 + 0.25 * (lon_i + 0.5))"

    def ring_test(points: list[tuple[float, float]]) -> str:
        terms = []
        for (x1, y1), (x2, y2) in zip(points[:-1], points[1:]):
            if y1 == y2:
                continue
            terms.append(
                f"CASE WHEN (({y1!r} > {lat_expr}) <> ({y2!r} > {lat_expr})) "
                f"AND ({lon_expr}) < (({x2!r} - {x1!r}) * ({lat_expr} - {y1!r}) / ({y2!r} - {y1!r}) + {x1!r}) THEN 1 ELSE 0 END"
            )
        if not terms:
            return "FALSE"
        return "((" + " + ".join(terms) + ") % 2 = 1)"

    polygon_exprs = []
    for rings in normalized:
        expr = ring_test(rings[0])
        for hole in rings[1:]:
            expr += f" AND NOT {ring_test(hole)}"
        polygon_exprs.append(f"({expr})")
    all_points = [point for rings in normalized for ring in rings for point in ring]
    bounds = (min(p[0] for p in all_points), min(p[1] for p in all_points), max(p[0] for p in all_points), max(p[1] for p in all_points))
    return "(" + " OR ".join(polygon_exprs) + ")", bounds


def query_common_grid_comparison(
    connection: Any,
    parquet_paths: Sequence[str | Path],
    start_date: date | str,
    end_date: date | str,
    *,
    product_type: str = "SP",
    platforms: Sequence[str] | None = None,
    daynight: str | None = None,
    bbox: Sequence[float] | None = None,
    polygons: Sequence[Sequence[Sequence[Sequence[float]]]] | None = None,
) -> dict[str, Any]:
    """Compare active detection footprints without estimating unobserved fires.

    Returned `unique_detected_cell_days` are distinct positive 0.25-degree cells
    per UTC date across the selected sources. A cell detected by two sensor
    families counts once in the union and is also reported as an overlap. This
    metric does not equate to unique fires or harmonized detection counts.
    """
    start = _as_date(start_date, "start_date")
    end = _as_date(end_date, "end_date")
    if start > end:
        raise HarmonizationQueryError("start_date must be on or before end_date.")
    if product_type not in PRODUCT_TYPES:
        raise HarmonizationQueryError("product_type must be SP or NRT; do not combine processing streams implicitly.")
    if daynight not in (None, "D", "N"):
        raise HarmonizationQueryError("daynight must be D, N, or omitted.")
    selected_platforms = list(platforms or [])
    unknown = sorted(set(selected_platforms) - PLATFORMS)
    if unknown:
        raise HarmonizationQueryError(f"Unsupported platform(s): {', '.join(unknown)}.")
    selected_paths = [str(Path(path)) for path in parquet_paths if Path(path).is_file()]
    if not selected_paths:
        raise HarmonizationQueryError("No processed daily-cell Parquet file is available for this query.")
    bounds = _validate_bbox(bbox)
    if polygons is not None and bounds is not None:
        raise HarmonizationQueryError("Provide either bbox or GeoJSON polygon, not both.")
    polygon_condition = None
    if polygons is not None:
        polygon_condition, bounds = _rings_sql(polygons)

    conditions = ["acq_date BETWEEN ? AND ?", "product_type = ?"]
    params: list[Any] = [selected_paths, start, end, product_type]
    if daynight:
        conditions.append("daynight = ?")
        params.append(daynight)
    if bounds:
        west, south, east, north = bounds
        conditions.extend([
            "(-90.0 + 0.25 * (lat_i + 0.5)) BETWEEN ? AND ?",
            "(-180.0 + 0.25 * (lon_i + 0.5)) BETWEEN ? AND ?",
        ])
        params.extend([south, north, west, east])
    if polygon_condition:
        conditions.append(polygon_condition)
    if selected_platforms:
        conditions.append("platform IN (" + ", ".join("?" for _ in selected_platforms) + ")")
        params.extend(selected_platforms)
    where = " AND ".join(conditions)

    product_rows = connection.execute(f"""
        WITH product_cells AS (
          SELECT acq_date, lat_i, lon_i, sensor_family, platform, product_type,
                 SUM(n_raw)::BIGINT AS raw_records,
                 SUM(frp_sum) AS frp_sum,
                 MAX(frp_max) AS frp_max
          FROM read_parquet(?, hive_partitioning=true)
          WHERE {where}
          GROUP BY acq_date, lat_i, lon_i, sensor_family, platform, product_type
        )
        SELECT acq_date, sensor_family, platform, product_type,
               COUNT(*)::BIGINT AS detected_cell_days,
               SUM(raw_records)::BIGINT AS raw_records,
               SUM(frp_sum) AS frp_sum,
               MAX(frp_max) AS frp_max
        FROM product_cells
        GROUP BY acq_date, sensor_family, platform, product_type
        ORDER BY acq_date, sensor_family, platform, product_type
    """, params).fetchall()

    union_rows = connection.execute(f"""
        WITH product_cells AS (
          SELECT acq_date, lat_i, lon_i, sensor_family, SUM(n_raw)::BIGINT AS raw_records
          FROM read_parquet(?, hive_partitioning=true)
          WHERE {where}
          GROUP BY acq_date, lat_i, lon_i, sensor_family
        ), family_cells AS (
          SELECT acq_date, lat_i, lon_i,
                 MAX(CASE WHEN sensor_family = 'MODIS' THEN 1 ELSE 0 END) AS has_modis,
                 MAX(CASE WHEN sensor_family = 'VIIRS' THEN 1 ELSE 0 END) AS has_viirs
          FROM product_cells
          GROUP BY acq_date, lat_i, lon_i
        )
        SELECT acq_date, COUNT(*)::BIGINT AS unique_detected_cell_days,
               SUM(has_modis)::BIGINT AS modis_detected_cell_days,
               SUM(has_viirs)::BIGINT AS viirs_detected_cell_days,
               COUNT(*) FILTER (WHERE has_modis = 1 AND has_viirs = 1)::BIGINT AS cross_sensor_overlap_cell_days
        FROM family_cells
        GROUP BY acq_date
        ORDER BY acq_date
    """, params).fetchall()

    product_daily = [{
        "date": row[0].isoformat(), "sensor_family": row[1], "platform": row[2],
        "product_type": row[3], "detected_cell_days": int(row[4]),
        "raw_records": int(row[5]), "frp_sum_mw": row[6], "frp_max_mw": row[7],
    } for row in product_rows]
    daily_union = [{
        "date": row[0].isoformat(), "unique_detected_cell_days": int(row[1]),
        "modis_detected_cell_days": int(row[2]), "viirs_detected_cell_days": int(row[3]),
        "cross_sensor_overlap_cell_days": int(row[4]),
    } for row in union_rows]
    return {
        "status": "comparison_only",
        "method": METHOD_NAME,
        "method_version": METHOD_VERSION,
        "harmonized_index": None,
        "calibration_status": "insufficient_calibration",
        "calibration_reason": "A shared grid and date do not correct sensor-specific detection sensitivity, observation opportunity, or FRP retrieval differences. No validated cross-sensor calibration is configured.",
        "calibration": {
            "status": "insufficient_calibration",
            "method": None,
            "coefficients": None,
            "training_period": None,
            "validation_period": None,
            "region": None,
            "season_group": None,
            "sample_size": None,
            "validation_metrics": None,
            "confidence_intervals": None,
            "spread": None,
            "reason": "The FIRMS detection archive lacks per-cell sensor observation-opportunity denominators. A non-detection cannot be treated as an observed zero for presence calibration.",
        },
        "product_type": product_type,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "bbox": list(bounds) if bounds else None,
        "platforms": selected_platforms or "all available",
        "daynight": daynight or "all available",
        "daily_union": daily_union,
        "daily_by_product_platform": product_daily,
        "uncertainty": None,
        "coverage_status": "detection-record coverage only; absence of a row is not interpreted as zero activity or confirmed lack of observation",
        "metric_definition": "Unique positive 0.25-degree cell-days on the same UTC date. This is a gridded detection-footprint metric, not a count of fires, burned area, or sensor-equivalent observations.",
        "limitations": [
            "MODIS and VIIRS products have different spatial footprints and detection characteristics.",
            "Same-cell/day co-detections are not event matches; distinct fires can occupy one cell and one fire can span multiple cells.",
            "The CSV archive does not provide a per-cell observation-opportunity denominator, so missing detections cannot be classified as zero fire activity.",
            "Raw FRP is kept per product/platform and is not added across sensors as if it were calibrated.",
        ],
    }
