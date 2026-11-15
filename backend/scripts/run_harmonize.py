"""Build the FIREWATCH statistical calibration and preliminary baseline JSON."""
from __future__ import annotations

import json
import math
import sys
from datetime import date
from pathlib import Path
from typing import Any

import duckdb
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "data" / "processed" / "daily_manifest.json"
OUTPUT = ROOT / "frontend" / "public" / "data"
YEARS = tuple(range(2020, 2026))

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harmonize_core as core  # noqa: E402


def _json_number(value: Any, digits: int = 6) -> float | None:
    if value is None:
        return None
    number = float(value)
    return round(number, digits) if math.isfinite(number) else None


def _atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, allow_nan=False, separators=(",", ":")), encoding="utf-8")
    temporary.replace(path)


def _load_daily() -> tuple[pd.DataFrame, list[str], int]:
    if not MANIFEST.is_file():
        raise FileNotFoundError(f"Daily aggregate manifest missing: {MANIFEST}")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = [entry for entry in manifest.get("files", {}).values()
               if entry.get("status") == "complete" and entry.get("product_type") == "SP"
               and entry.get("country") and int(entry.get("year", 0)) in YEARS
               and entry.get("aggregation_format") == 2 and entry.get("output_file")]
    paths = sorted({str((ROOT / entry["output_file"]).resolve()) for entry in entries})
    if not paths:
        raise ValueError("No current-format 2020–2025 country SP aggregates are available.")
    connection = duckdb.connect(":memory:")
    connection.execute("PRAGMA memory_limit='2GB'")
    connection.execute("PRAGMA threads=4")
    try:
        rows = connection.execute("""
            SELECT country, CAST(acq_date AS DATE) AS date, sensor_family AS family,
                   SUM(vegetation_frp_sum_mw)::DOUBLE AS frp,
                   SUM(vegetation_n_detections)::BIGINT AS n
            FROM read_parquet(?, union_by_name=true)
            WHERE aggregation_level='daily' AND type_available
              AND acq_date >= DATE '2020-01-01' AND acq_date < DATE '2026-01-01'
              AND sensor_family IN ('MODIS','VIIRS')
            GROUP BY country, acq_date, sensor_family
            ORDER BY country, acq_date, sensor_family
        """, [paths]).fetchdf()
    finally:
        connection.close()
    if rows.empty:
        raise ValueError("No vegetation-type aggregates are available; the calibration will not substitute total FRP.")
    rows["family"] = rows["family"].replace({"MODIS": "MODIS", "VIIRS": "VIIRS"})
    rows["date"] = pd.to_datetime(rows["date"])
    return rows[["country", "date", "family", "frp", "n"]], paths, len(entries)


def _country_weeks(country: str, all_weekly: pd.DataFrame, operating: list[pd.Timestamp]) -> pd.DataFrame:
    rows = all_weekly.loc[all_weekly["country"] == country].set_index("week")
    expanded = rows.reindex(operating)
    expanded.index.name = "week"
    expanded = expanded.reset_index()
    expanded["country"] = country
    for column in ("frp_MODIS", "frp_VIIRS", "n_MODIS", "n_VIIRS"):
        expanded[column] = expanded[column].fillna(0.0)
    return expanded


def _season(weekly: pd.DataFrame, value_column: str = "harmonized") -> dict[str, Any]:
    values = weekly[value_column].to_numpy(float)
    total = float(values.sum())
    if not len(values) or total <= 0:
        return {"start": None, "peak": None, "end": None, "annual_frp": 0.0}
    order = weekly.reset_index(drop=True)
    cumulative = np.cumsum(values)
    start_index = int(np.searchsorted(cumulative, total * 0.05, side="left"))
    end_index = int(np.searchsorted(cumulative, total * 0.95, side="left"))
    peak_index = int(np.argmax(values))
    def iso(index: int) -> str:
        return pd.Timestamp(order.iloc[index]["week"]).date().isoformat()
    return {"start": iso(start_index), "peak": iso(peak_index), "end": iso(end_index),
            "annual_frp": round(total, 3)}


def _daily_series(country: str, raw: pd.DataFrame, weeks: pd.DataFrame,
                  operating: list[pd.Timestamp]) -> list[dict[str, Any]]:
    subset = raw.loc[raw["country"] == country]
    by_date: dict[date, dict[str, float]] = {}
    for row in subset.itertuples(index=False):
        day = pd.Timestamp(row.date).date()
        values = by_date.setdefault(day, {"frp_MODIS": 0.0, "frp_VIIRS": 0.0,
                                          "n_MODIS": 0.0, "n_VIIRS": 0.0})
        values[f"frp_{row.family}"] += float(row.frp or 0.0)
        values[f"n_{row.family}"] += float(row.n or 0.0)

    week_lookup = {pd.Timestamp(row.week): row for row in weeks.itertuples(index=False)}
    operating_set = set(operating)
    generated_days = set(by_date)
    for week in operating:
        for offset in range(7):
            generated_days.add((week + pd.Timedelta(days=offset)).date())

    result = []
    for day in sorted(day for day in generated_days if 2020 <= day.year <= 2025):
        timestamp = pd.Timestamp(day)
        week = timestamp.to_period("W-SUN").start_time
        values = by_date.get(day, {"frp_MODIS": 0.0, "frp_VIIRS": 0.0,
                                   "n_MODIS": 0.0, "n_VIIRS": 0.0})
        weekly_row = week_lookup.get(week)
        is_operating = week in operating_set and weekly_row is not None
        scale = float(weekly_row.daily_scale_for_viirs) if is_operating else None
        raw_sum = values["frp_MODIS"] + values["frp_VIIRS"]
        harmonized_daily = (values["frp_MODIS"] + values["frp_VIIRS"] * scale) if scale is not None else None
        result.append({
            "date": day.isoformat(), "year": day.year, "doy": day.timetuple().tm_yday,
            "raw_modis_frp": round(values["frp_MODIS"], 3),
            "raw_viirs_frp": round(values["frp_VIIRS"], 3),
            "raw_frp_sum": round(raw_sum, 3),
            "modis_n": int(values["n_MODIS"]), "viirs_n": int(values["n_VIIRS"]),
            "week": week.date().isoformat(), "operating_week": is_operating,
            "daily_scale_for_viirs": _json_number(scale) if scale is not None else None,
            "scaled_viirs_frp": round(values["frp_VIIRS"] * scale, 3) if scale is not None else None,
            "harmonized_frp_daily": round(harmonized_daily, 3) if harmonized_daily is not None else None,
            "raw_unusual_week": bool(getattr(weekly_row, "raw_unusual", False)) if is_operating else False,
            "harmonized_unusual_week": bool(weekly_row.unusual) if is_operating else False,
            "has_source_record": day in by_date,
        })
    return result


def _climatology(daily: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[int, dict[int, list[float]]] = {}
    for row in daily:
        if not row["operating_week"]:
            continue
        by_year = grouped.setdefault(int(row["doy"]), {})
        by_year[int(row["year"])] = [
            float(row["raw_frp_sum"]), float(row["harmonized_frp_daily"] or 0.0),
            bool(row["raw_unusual_week"]), bool(row["harmonized_unusual_week"]),
        ]
    output = []
    for doy in range(1, 367):
        year_values = grouped.get(doy, {})
        raw_values = [pair[0] for pair in year_values.values()]
        harmonized_values = [pair[1] for pair in year_values.values()]
        def stats(values: list[float]) -> tuple[float | None, float | None, float | None]:
            if not values:
                return None, None, None
            q25, median, q75 = np.quantile(values, [0.25, 0.5, 0.75])
            return round(float(median), 3), round(float(q25), 3), round(float(q75), 3)
        raw_median, raw_q25, raw_q75 = stats(raw_values)
        cal_median, cal_q25, cal_q75 = stats(harmonized_values)
        output.append({
            "doy": doy, "sample_years": len(year_values),
            "raw_median": raw_median, "raw_q25": raw_q25, "raw_q75": raw_q75,
            "harmonized_median": cal_median, "harmonized_q25": cal_q25,
            "harmonized_q75": cal_q75,
            "raw_by_year": {str(year): pair[0] for year, pair in sorted(year_values.items())},
            "harmonized_by_year": {str(year): pair[1] for year, pair in sorted(year_values.items())},
            "raw_unusual_by_year": {str(year): pair[2] for year, pair in sorted(year_values.items())},
            "harmonized_unusual_by_year": {str(year): pair[3] for year, pair in sorted(year_values.items())},
        })
    return output


def _finite_median(values: list[Any]) -> float | None:
    finite = [float(value) for value in values if value is not None and math.isfinite(float(value))]
    return round(float(np.median(finite)), 6) if finite else None


def run() -> dict[str, Any]:
    daily, source_paths, source_file_count = _load_daily()
    operating_set = core.operating_weeks(daily)
    operating = sorted(pd.Timestamp(value) for value in operating_set)
    if not operating:
        raise ValueError("The selected archive contains no weeks meeting the method's 7-day paired operating rule.")
    all_weekly = core.weekly(daily)
    operating_weekly = all_weekly.loc[all_weekly["week"].isin(operating)].copy()
    eligible_global = operating_weekly.loc[
        (operating_weekly.frp_MODIS >= core.MIN_FRP) & (operating_weekly.frp_VIIRS >= core.MIN_FRP)
    ]
    if len(eligible_global) < 2:
        raise ValueError("Fewer than two globally eligible overlap weeks; a global fallback cannot be fit honestly.")
    fallback = core.global_fallback(operating_weekly)
    countries = sorted(daily["country"].unique())
    country_metrics: dict[str, dict[str, Any]] = {}
    weekly_outputs: dict[str, pd.DataFrame] = {}
    weekly_json: dict[str, list[dict[str, Any]]] = {}
    all_continuity = []
    raw_continuity = []
    fit_r2 = []
    fit_mdape = []
    confidence_counts = {"High": 0, "Medium": 0, "Low": 0}
    excluded_country_weeks = max(0, len(all_weekly) - len(operating_weekly))
    excluded_fit_weeks = 0

    for country in countries:
        country_weeks = _country_weeks(country, all_weekly, operating)
        eligible = (country_weeks.frp_MODIS >= core.MIN_FRP) & (country_weeks.frp_VIIRS >= core.MIN_FRP)
        excluded_fit_weeks += int((~eligible).sum())
        calibration = core.calibrate_country(country_weeks, fallback)
        if calibration is None:
            calibration = {**fallback, "n_weeks": int(eligible.sum()), "fit": "global_fallback",
                           "r2": None, "mdape": None, "corr": None, "bias": None, "confidence": "Low"}
        continuity = core.continuity(country_weeks, calibration)
        if continuity:
            raw_continuity.append(continuity["raw_ratio_median"])
            all_continuity.append(continuity["calibrated_ratio_median"])
        if calibration["fit"] == "country" and calibration["r2"] is not None:
            fit_r2.append(calibration["r2"])
            fit_mdape.append(calibration["mdape"])
        confidence_counts[calibration["confidence"]] += 1

        harmonized = core.harmonize_weeks(country_weeks, calibration)
        raw_weekly = harmonized.frp_MODIS.to_numpy(float) + harmonized.frp_VIIRS.to_numpy(float)
        raw_p90 = float(np.quantile(raw_weekly, 0.90))
        harmonized["raw_unusual"] = raw_weekly > raw_p90
        harmonized["raw_unusual_threshold_p90"] = raw_p90
        p90 = float(np.quantile(harmonized.harmonized.to_numpy(float), 0.90))
        harmonized["unusual"] = harmonized.harmonized > p90
        weekly_outputs[country] = harmonized
        weekly_json[country] = [{
            "week": pd.Timestamp(row.week).date().isoformat(),
            "frp_modis": round(float(row.frp_MODIS), 3),
            "frp_viirs": round(float(row.frp_VIIRS), 3),
            "n_modis": int(row.n_MODIS), "n_viirs": int(row.n_VIIRS),
            "viirs_calibrated": round(float(row.viirs_calibrated), 3),
            "harmonized": round(float(row.harmonized), 3),
            "lower": round(float(row.lower), 3), "upper": round(float(row.upper), 3),
            "daily_scale_for_viirs": round(float(row.daily_scale_for_viirs), 6),
            "confidence": calibration["confidence"], "unusual": bool(row.unusual),
            "unusual_threshold_p90": round(p90, 3),
            "raw_unusual": bool(row.raw_unusual), "raw_unusual_threshold_p90": round(raw_p90, 3),
        } for row in harmonized.itertuples(index=False)]
        country_metrics[country] = {
            "confidence": calibration["confidence"], "fit": calibration["fit"],
            "n_overlap_weeks": int(calibration["n_weeks"]),
            "r2": _json_number(calibration["r2"]), "mdape": _json_number(calibration["mdape"]),
            "correlation": _json_number(calibration["corr"]), "median_log_bias": _json_number(calibration["bias"]),
            "residual_log_sd": _json_number(calibration["sd"]),
            "slope": _json_number(calibration["b"]), "intercept": _json_number(calibration["a"]),
            "continuity": continuity,
            "excluded_non_operating_weeks": int(len(all_weekly.loc[all_weekly.country == country]) - len(operating)),
            "excluded_fit_weeks": int((~eligible).sum()),
        }

    per_country_files = []
    for country in countries:
        slug = "-".join("".join(ch.lower() if ch.isalnum() else " " for ch in country).split())
        weekly = weekly_outputs[country]
        daily_rows = _daily_series(country, daily, weekly, operating)
        climatology = _climatology(daily_rows)
        seasons = {}
        for year in YEARS:
            year_rows = weekly.loc[weekly.week.dt.year == year].copy()
            year_rows["raw_total"] = year_rows.frp_MODIS + year_rows.frp_VIIRS
            seasons[str(year)] = {"raw": _season(year_rows, "raw_total"),
                                  "harmonized": _season(year_rows, "harmonized")}
        payload = {
            "schema_version": 1, "method_version": core.METHOD_VERSION,
            "country": country, "slug": slug, "years": list(YEARS),
            "confidence": country_metrics[country]["confidence"],
            "fit": country_metrics[country]["fit"], "metrics": country_metrics[country],
            "daily": daily_rows, "weekly": weekly_json[country],
            "climatology_by_doy": climatology, "fire_season_by_year": seasons,
            "metric_definition": "Vegetation-only FRP. In harmonized calendar mode, daily VIIRS FRP is multiplied by the fitted scale for its week and added to raw daily MODIS FRP; the result is a display aggregation and is not the core weekly log-mean estimate.",
            "operating_rule": "Only weeks in which both sensor families reported at least one detection on each of all seven dates somewhere in the processed country archive enter the weekly comparison. This is not pixel-level observation-opportunity information.",
            "missing_days_rule": "No source record is not proof that a place was observed or fire-free. Daily calendar entries outside operating weeks are not calibrated.",
        }
        path = OUTPUT / "harmonized" / f"{slug}.json"
        _atomic_json(path, payload)
        per_country_files.append(path)

    methods = {
        "schema_version": 1, "method_version": core.METHOD_VERSION,
        "status": "preliminary_statistical_calibration",
        "input": {"years": list(YEARS), "source_files": source_file_count,
                  "aggregate_parquet_files": len(source_paths), "aggregation": "vegetation-only type=0; MODIS Terra+Aqua and VIIRS S-NPP+NOAA-20 grouped by country/date/family"},
        "thresholds": {
            "minimum_weekly_frp_mw_per_family": core.MIN_FRP,
            "minimum_country_overlap_weeks": core.MIN_BOTH_WEEKS,
            "confidence": {"High": {"minimum_r2": 0.7, "maximum_mdape": 0.35},
                           "Medium": {"minimum_r2": 0.4, "maximum_mdape": 0.60},
                           "Low": "Below Medium or global fallback"},
            "uncertainty_band": "harmonized weekly FRP +/- 1.96 residual log-space standard deviations",
            "unusual_week": "strictly greater than the 90th percentile of the country's six-year weekly FRP distribution; raw and harmonized distributions are stored separately",
            "continuity": "median calibrated VIIRS/MODIS weekly FRP ratio; target is approximately 1",
        },
        "validation_metrics": {
            "median_r2": _finite_median(fit_r2), "median_holdout_mdape": _finite_median(fit_mdape),
            "confidence_counts": confidence_counts,
            "median_continuity_ratio_before": _finite_median(raw_continuity),
            "median_continuity_ratio_after": _finite_median(all_continuity),
            "country_fits_with_loyo_metrics": len(fit_r2), "countries": len(countries),
            "operating_weeks": len(operating),
            "excluded_country_weeks_non_operating": excluded_country_weeks,
            "excluded_country_weeks_below_fit_threshold": excluded_fit_weeks,
            "excluded_country_weeks_total": excluded_country_weeks + excluded_fit_weeks,
        },
        "per_country": country_metrics,
        "plain_language_rule": "Fit MODIS weekly vegetation FRP from VIIRS weekly vegetation FRP using a Theil-Sen log-log model on weeks with at least 5 MW in both families. Fit a country model with at least 40 overlap weeks and leave one calendar year out at a time; otherwise use the deterministic global fallback and mark Low confidence. Weekly output uses the core method's sensor combination and 95% residual band.",
        "limitations": [
            "Statistical cross-sensor calibration, not a physical retrieval correction.",
            "The operating-week rule is global within the processed country archive and does not establish country-pixel observation opportunity.",
            "Calibration fits only weeks with vegetation FRP of at least 5 MW from both families; weeks without fire in either sensor are not part of the fit.",
            "Country coverage and the VIIRS platform mix vary; NOAA-21 is not included.",
            "The 2020–2025 seasonal baseline is preliminary and only six years long.",
            "Daily harmonized display is raw MODIS daily FRP plus VIIRS daily FRP scaled by its weekly factor; it is not the core weekly log-mean value.",
        ],
        "source": "NASA FIRMS local Standard Processing country CSVs, transformed to daily aggregates; raw CSVs were not modified or reread by this script.",
    }
    _atomic_json(OUTPUT / "methods_validation.json", methods)

    printed = {
        "method_version": methods["method_version"],
        "median_r2": methods["validation_metrics"]["median_r2"],
        "median_holdout_mdape": methods["validation_metrics"]["median_holdout_mdape"],
        "confidence_counts": confidence_counts,
        "median_continuity_ratio_before": methods["validation_metrics"]["median_continuity_ratio_before"],
        "median_continuity_ratio_after": methods["validation_metrics"]["median_continuity_ratio_after"],
        "selected_countries": {name: country_metrics.get(name) for name in ("India", "Australia", "Brazil")},
        "country_files": len(per_country_files),
        "operating_weeks": len(operating),
        "source_files": source_file_count,
    }
    print(json.dumps(printed, indent=2, allow_nan=False))
    return methods


if __name__ == "__main__":
    run()
