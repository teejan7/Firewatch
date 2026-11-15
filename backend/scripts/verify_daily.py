"""Compare daily aggregates to independent DuckDB raw counts and old static JSON."""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import duckdb

ROOT = Path(__file__).resolve().parents[2]
COUNTRIES = ("India", "Australia", "Brazil", "Bahrain")
YEARS = tuple(range(2020, 2026))
BASELINE_PATH = ROOT / "docs" / "internal" / "daily_legacy_baseline.json"


def _percent_difference(left: int, right: int) -> float | None:
    if right == 0:
        return 0.0 if left == 0 else None
    return abs(left - right) / right * 100.0


def capture_legacy_baseline(countries: tuple[str, ...] = COUNTRIES, years: tuple[int, ...] = YEARS) -> None:
    snapshot: dict[str, Any] = {"source": "pre-daily frontend/public/data/series JSON", "countries": {}}
    for country in countries:
        slug = country.lower().replace(" ", "-")
        path = ROOT / "frontend" / "public" / "data" / "series" / f"{slug}.json"
        if not path.is_file():
            continue
        series = json.loads(path.read_text(encoding="utf-8"))
        grouped: dict[str, dict[str, Any]] = {}
        for row in series.get("daily", []):
            year, family = int(str(row[0])[:4]), row[1]
            if year not in years:
                continue
            key = f"{year}|{family}"
            grouped.setdefault(key, {"detections": 0, "source_files": []})
            grouped[key]["detections"] += int(row[4])
        for source in series.get("source_files", []):
            year, product = int(source["year"]), source.get("product", "")
            family = "MODIS" if product == "MODIS_SP" else "VIIRS"
            if year not in years:
                continue
            key = f"{year}|{family}"
            grouped.setdefault(key, {"detections": 0, "source_files": []})
            grouped[key]["source_files"].append(source.get("source_file", ""))
        snapshot["countries"][country] = grouped
    BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    BASELINE_PATH.write_text(json.dumps(snapshot, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def verify(countries: tuple[str, ...] = COUNTRIES, years: tuple[int, ...] = YEARS) -> list[dict[str, Any]]:
    sys.path.insert(0, str(ROOT / "backend"))
    from scripts.build_processed import discover_csv_files

    daily_manifest_path = ROOT / "data" / "processed" / "daily_manifest.json"
    if not daily_manifest_path.is_file():
        raise FileNotFoundError(f"Daily manifest missing: {daily_manifest_path}")
    daily_manifest = json.loads(daily_manifest_path.read_text(encoding="utf-8"))
    selected = {country.casefold() for country in countries}
    raw_entries = [entry for entry in discover_csv_files(ROOT / "data" / "raw" / "extracted")
                   if entry.get("supported") and entry.get("scope") == "country"
                   and entry.get("product_type") == "SP" and entry["country"].casefold() in selected
                   and int(entry["year"]) in years]
    raw_counts: dict[str, int] = {}
    con = duckdb.connect(":memory:")
    con.execute("PRAGMA memory_limit='2GB'")
    con.execute("PRAGMA threads=4")
    try:
        paths = [Path(entry["source_path"]).relative_to(ROOT).as_posix() for entry in raw_entries]
        if paths:
            for filename, count in con.execute("""
                SELECT filename, COUNT(*)::BIGINT
                FROM read_csv(?, header=true, all_varchar=true, delim=',',
                              null_padding=true, strict_mode=false,
                              union_by_name=true, filename=true)
                GROUP BY filename
            """, [paths]).fetchall():
                raw_counts[Path(filename.replace("\\", "/")).as_posix()] = int(count)
    finally:
        con.close()

    aggregate_counts: dict[tuple[str, int, str], int] = defaultdict(int)
    aggregate_files: dict[tuple[str, int, str], int] = defaultdict(int)
    for record in daily_manifest.get("files", {}).values():
        if record.get("status") != "complete" or record.get("product_type") != "SP":
            continue
        country, year = record.get("country"), int(record.get("year", 0))
        family = record.get("sensor_family")
        if not country or country.casefold() not in selected or year not in years:
            continue
        key = (country, year, family)
        aggregate_counts[key] += int(record.get("aggregated_detection_count", 0))
        aggregate_files[key] += 1

    series_records: dict[tuple[str, int, str], int] = defaultdict(int)
    legacy_source_files: dict[tuple[str, int, str], set[str]] = defaultdict(set)
    if BASELINE_PATH.is_file():
        snapshot = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
        for country, groups in snapshot.get("countries", {}).items():
            for group_key, values in groups.items():
                year_text, family = group_key.split("|", 1)
                series_records[(country, int(year_text), family)] = int(values.get("detections", 0))
                legacy_source_files[(country, int(year_text), family)] = set(values.get("source_files", []))
    else:
        for country in countries:
            slug = country.lower().replace(" ", "-")
            path = ROOT / "frontend" / "public" / "data" / "series" / f"{slug}.json"
            if not path.is_file():
                continue
            series = json.loads(path.read_text(encoding="utf-8"))
            for row in series.get("daily", []):
                year, family = int(str(row[0])[:4]), row[1]
                if year in years:
                    series_records[(country, year, family)] += int(row[4])
            for source in series.get("source_files", []):
                year, product = int(source["year"]), source.get("product", "")
                family = "MODIS" if product == "MODIS_SP" else "VIIRS"
                if year in years:
                    legacy_source_files[(country, year, family)].add(str(source.get("source_file", "")))

    raw_by_key: dict[tuple[str, int, str], int] = defaultdict(int)
    raw_files: dict[tuple[str, int, str], int] = defaultdict(int)
    raw_sources_by_key: dict[tuple[str, int, str], list[dict[str, Any]]] = defaultdict(list)
    for entry in raw_entries:
        key = (entry["country"], int(entry["year"]), entry["sensor_family"])
        source_relative = Path(entry["source_path"]).relative_to(ROOT).as_posix()
        raw_by_key[key] += raw_counts.get(source_relative, 0)
        raw_files[key] += 1
        raw_sources_by_key[key].append(entry)

    report = []
    for country in countries:
        for year in years:
            for family in ("MODIS", "VIIRS"):
                key = (country, year, family)
                raw_total = raw_by_key[key]
                daily_total = aggregate_counts[key]
                existing_total = series_records[key]
                raw_diff = _percent_difference(daily_total, raw_total)
                existing_diff = _percent_difference(daily_total, existing_total)
                explanation = ""
                if raw_diff is not None and raw_diff > 0.1:
                    explanation = "DAILY/RAW DIFFERENCE >0.1%; inspect invalid dates/coordinates or dropped records."
                elif existing_diff is not None and existing_diff > 0.1:
                    new_products = sorted({
                        entry["product"] for entry in raw_sources_by_key[key]
                        if entry["source_file"] not in legacy_source_files[key]
                    })
                    explanation = (f"New daily build includes source product(s) absent from the baseline JSON: {', '.join(new_products)}."
                                   if new_products else
                                   "Legacy static total differs despite matching source-file counts; investigate before retiring old data.")
                elif existing_total == 0 and daily_total:
                    missing_products = sorted({entry["product"] for entry in raw_sources_by_key[key]})
                    explanation = f"No baseline JSON detections; daily build adds {', '.join(missing_products)}."
                report.append({
                    "country": country, "year": year, "sensor_family": family,
                    "raw_files": raw_files[key], "daily_files": aggregate_files[key],
                    "legacy_files": len(legacy_source_files[key]), "raw_duckdb_rows": raw_total,
                    "daily_detections": daily_total, "existing_series_detections": existing_total,
                    "daily_vs_raw_pct": raw_diff, "daily_vs_existing_pct": existing_diff,
                    "explanation": explanation,
                })
    return report


def markdown_table(rows: list[dict[str, Any]]) -> str:
    lines = [
        "| Country | Year | Sensor family | Raw DuckDB rows | New daily detections | Existing series detections | Daily vs raw | Daily vs existing | Explanation |",
        "|---|---:|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        pct_raw = "n/a" if row["daily_vs_raw_pct"] is None else f'{row["daily_vs_raw_pct"]:.3f}%'
        pct_old = "n/a" if row["daily_vs_existing_pct"] is None else f'{row["daily_vs_existing_pct"]:.3f}%'
        explanation = row["explanation"].replace("|", "/") or "Within 0.1%."
        lines.append(
            f'| {row["country"]} | {row["year"]} | {row["sensor_family"]} | '
            f'{row["raw_duckdb_rows"]} | {row["daily_detections"]} | '
            f'{row["existing_series_detections"]} | {pct_raw} | {pct_old} | {explanation} |'
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--country", action="append", dest="countries")
    parser.add_argument("--year", action="append", type=int, dest="years")
    parser.add_argument("--markdown", action="store_true", help="Print a Markdown verification table.")
    parser.add_argument("--snapshot-baseline", action="store_true", help="Save compact pre-daily series totals before replacing static JSON.")
    args = parser.parse_args()
    if args.snapshot_baseline:
        capture_legacy_baseline(tuple(args.countries or COUNTRIES), tuple(args.years or YEARS))
        print(f"Saved legacy series totals to {BASELINE_PATH}")
        return
    rows = verify(tuple(args.countries or COUNTRIES), tuple(args.years or YEARS))
    if args.markdown:
        print(markdown_table(rows))
    else:
        print(json.dumps(rows, indent=2))
    failed = [row for row in rows if row["daily_vs_raw_pct"] is None or row["daily_vs_raw_pct"] > 0.1]
    if failed:
        raise SystemExit(f"{len(failed)} daily/raw comparisons exceed the 0.1% verification threshold.")


if __name__ == "__main__":
    main()
