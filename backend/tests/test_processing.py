import json
import sys
from pathlib import Path

import duckdb
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts import build_processed
from scripts.build_processed import (
    build_daily_cells,
    coverage_table,
    discover_csv_files,
    parser,
    process_entry,
    run,
)


def test_discovers_country_and_noaa21_global_streams(tmp_path):
    raw = tmp_path / "raw"
    modis = raw / "MODIS_SP" / "modis" / "2025"
    noaa21 = raw / "VIIRS_NOAA21_SP" / "viirs-jpss2" / "2026"
    modis.mkdir(parents=True)
    noaa21.mkdir(parents=True)
    (modis / "modis_2025_Testland.csv").write_text("latitude,longitude,acq_date,instrument\n1,2,2025-01-01,MODIS\n", encoding="utf-8")
    (noaa21 / "fire_archive_J2V-C2_1.csv").write_text("latitude,longitude,acq_date,instrument\n1,2,2026-01-01,VIIRS\n", encoding="utf-8")
    (noaa21 / "fire_nrt_J2V-C2_1.csv").write_text("latitude,longitude,acq_date,instrument\n1,2,2026-08-01,VIIRS\n", encoding="utf-8")

    entries = discover_csv_files(raw)
    assert sorted((row["product"], row["product_type"], row["scope"]) for row in entries) == sorted([
        ("MODIS_SP", "SP", "country"),
        ("VIIRS_NOAA21_SP", "SP", "global"),
        ("VIIRS_NOAA21_NRT", "NRT", "global"),
    ])


def test_processing_validates_normalizes_and_aggregates_exact_duplicates(tmp_path):
    raw = tmp_path / "raw"
    source_dir = raw / "VIIRS_NOAA21_SP" / "viirs-jpss2" / "2025"
    source_dir.mkdir(parents=True)
    source = source_dir / "fire_archive_J2V-C2_test.csv"
    header = "latitude,longitude,acq_date,acq_time,satellite,instrument,confidence,daynight,frp,bright_ti4,version"
    valid = "10.1,20.1,2025-01-01,0130,N21,VIIRS,n,D,5.5,320.1,2"
    invalid_measurement = "10.1,20.1,2025-01-01,0130,N21,VIIRS,n,D,not-a-number,unknown,2"
    source.write_text(f"{header}\n{valid}\n{valid}\n{invalid_measurement}\n91,20,2025-01-01,0130,N21,VIIRS,n,D,1,320,2\n1,2,bad-date,0130,N21,VIIRS,n,D,1,320,2\n", encoding="utf-8")
    processed = tmp_path / "processed"
    entry = discover_csv_files(raw)[0]
    connection = duckdb.connect(":memory:")
    try:
        result = process_entry(entry, processed, connection)
        assert result["rows_source"] == 5
        assert result["rows_processed"] == 3
        assert result["invalid_coordinates"] == 1
        assert result["invalid_dates"] == 1
        assert result["exact_duplicate_rows_within_file"] == 1
        assert result["invalid_numeric_counts"] == {"frp": 1, "brightness": 0, "bright_ti4": 1, "bright_ti5": 0}
        rows = connection.execute("SELECT acq_date, platform, product_type, brightness, bright_ti4, original_fields FROM read_parquet(?)", [str(processed / result["output_file"])]).fetchall()
        assert rows[0][0].isoformat() == "2025-01-01"
        assert rows[0][1:4] == ("NOAA-21", "SP", None)
        assert rows[0][4] == 320.1
        assert '"version":"2"' in rows[0][5]
        assert process_entry(entry, processed, connection)["status"] == "skipped"
        summary = build_daily_cells(processed, connection)
        cell_files = [str(path) for path in Path(summary["output_file"]).rglob("*.parquet")]
        cell = connection.execute("SELECT n_raw, n_dedup, frp_sum, frp_max FROM read_parquet(?, hive_partitioning=true)", [cell_files]).fetchone()
        assert cell == (3, 1, 11.0, 5.5)
    finally:
        connection.close()

    manifest = json.loads((processed / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["files"][entry["file_id"]]["status"] == "processed"


def test_compact_cell_shard_preserves_sensor_metrics_and_cell_presence(tmp_path):
    raw = tmp_path / "raw"
    source_dir = raw / "VIIRS_NOAA21_SP" / "viirs-jpss2" / "2025"
    source_dir.mkdir(parents=True)
    source = source_dir / "fire_archive_J2V-C2_test.csv"
    source.write_text(
        "latitude,longitude,acq_date,acq_time,satellite,instrument,confidence,daynight,frp,bright_ti4,version\n"
        "10.1,20.1,2025-01-01,0130,N21,VIIRS,n,D,5.5,320.1,2\n"
        "10.2,20.2,2025-01-01,0132,N21,VIIRS,n,D,2.5,319.0,2\n", encoding="utf-8")
    processed = tmp_path / "processed"
    con = duckdb.connect(":memory:")
    try:
        entry, = discover_csv_files(raw)
        result = process_entry(entry, processed, con, compact=True)
        assert result["storage_mode"] == "cell_shards"
        shard = processed / result["output_file"]
        n_raw, n_dedup, frp_sum, source_files = con.execute(
            "SELECT n_raw, n_dedup, frp_sum, source_files FROM read_parquet(?)", [str(shard)]).fetchone()
        assert (n_raw, n_dedup, frp_sum, source_files) == (2, 1, 8.0, 1)
        assert "original_fields" not in {row[0] for row in con.execute("DESCRIBE SELECT * FROM read_parquet(?)", [str(shard)]).fetchall()}
        summary = build_daily_cells(processed, con)
        daily_files = [str(path) for path in Path(summary["output_file"]).rglob("*.parquet")]
        daily = con.execute("SELECT n_raw, n_dedup, source_files FROM read_parquet(?, hive_partitioning=true)", [daily_files]).fetchone()
        assert daily == (2, 1, 1)
    finally:
        con.close()


def test_compact_mode_converts_existing_observation_parquet_without_raw_csv(tmp_path):
    raw = tmp_path / "raw"
    source_dir = raw / "MODIS_SP" / "modis" / "2025"
    source_dir.mkdir(parents=True)
    source = source_dir / "modis_2025_Testland.csv"
    source.write_text("latitude,longitude,acq_date,instrument,frp\n1,2,2025-01-01,MODIS,4\n", encoding="utf-8")
    processed = tmp_path / "processed"
    entry, = discover_csv_files(raw)
    con = duckdb.connect(":memory:")
    try:
        original = process_entry(entry, processed, con)
        source.unlink()
        compact = process_entry(entry, processed, con, compact=True)
        assert compact["status"] == "converted"
        assert compact["storage_mode"] == "cell_shards"
        assert (processed / compact["output_file"]).is_file()
        assert (processed / original["output_file"]).is_file()
    finally:
        con.close()


@pytest.mark.parametrize("compact", [False, True])
def test_noaa21_sp_precedes_nrt_until_the_latest_sp_date(tmp_path, compact):
    raw = tmp_path / "raw"
    source_dir = raw / "VIIRS_NOAA21_SP" / "viirs-jpss2" / "2025"
    source_dir.mkdir(parents=True)
    header = "latitude,longitude,acq_date,platform,instrument,frp"
    (source_dir / "fire_archive_J2V-C2_test.csv").write_text(
        f"{header}\n1,2,2025-01-01,N21,VIIRS,3\n1,2,2025-01-02,N21,VIIRS,4\n", encoding="utf-8")
    (source_dir / "fire_nrt_J2V-C2_test.csv").write_text(
        f"{header}\n1,2,2025-01-02,N21,VIIRS,5\n1,2,2025-01-03,N21,VIIRS,6\n", encoding="utf-8")
    processed = tmp_path / "processed"
    con = duckdb.connect(":memory:")
    try:
        entries = discover_csv_files(raw)
        for entry in entries:
            process_entry(entry, processed, con, compact=compact)
        (processed / "archive_index.json").write_text(json.dumps({"files": [
            {"file_id": entry["file_id"], "status": "processed"} for entry in entries
        ]}), encoding="utf-8")
        result = build_daily_cells(processed, con)
        cell_files = [str(path) for path in Path(result["output_file"]).rglob("*.parquet")]
        rows = con.execute("SELECT acq_date, product_type FROM read_parquet(?, hive_partitioning=true) ORDER BY acq_date", [cell_files]).fetchall()
        assert all("product_type=" in path and "sensor_family=" in path and "year=" in path for path in cell_files)
        assert [(day.isoformat(), stream) for day, stream in rows] == [
            ("2025-01-01", "SP"), ("2025-01-02", "SP"), ("2025-01-03", "NRT")
        ]
        assert result["noaa21_precedence"]["sp_end_date"] == "2025-01-02"
    finally:
        con.close()


def test_run_records_corrupt_file_in_quarantine_report_and_resumes(tmp_path):
    raw = tmp_path / "raw"
    source_dir = raw / "MODIS_SP" / "modis" / "2025"
    source_dir.mkdir(parents=True)
    corrupt = source_dir / "modis_2025_Testland.csv"
    original = "longitude,acq_date\n2,2025-01-01\n"
    corrupt.write_text(original, encoding="utf-8")
    processed = tmp_path / "processed"
    report = run(parser().parse_args(["--raw-root", str(raw), "--processed-root", str(processed)]))
    quarantine = json.loads((processed / "quarantine_report.json").read_text(encoding="utf-8"))
    assert report["files_expected"] == 1
    assert report["files_failed_total"] == 1
    assert quarantine["source_files_preserved"] is True
    assert quarantine["quarantined_files"][0]["source_file"].endswith("modis_2025_Testland.csv")
    assert corrupt.read_text(encoding="utf-8") == original


def test_coverage_table_counts_expected_processed_and_failed():
    entry = {"file_id": "one", "product_type": "SP", "platform": "Terra", "year": 2025,
             "supported": True, "size_bytes": 10, "modified_ns": 20, "scope": "country"}
    processed = {"signature": {"size_bytes": 10, "modified_ns": 20}, "status": "processed", "output_file": "ok.parquet",
                 "date_min": "2025-01-01", "date_max": "2025-12-31", "rows_processed": 123}
    row, = coverage_table([entry], {"files": {"one": processed}})
    assert row["files_expected"] == row["files_processed"] == 1
    assert row["row_count"] == 123
    assert row["status"] == "complete"


def test_full_run_disk_preflight_stops_without_touching_raw_files(tmp_path, monkeypatch):
    raw = tmp_path / "raw" / "MODIS_SP" / "modis" / "2025"
    raw.mkdir(parents=True)
    source = raw / "modis_2025_Testland.csv"
    original = "latitude,longitude,acq_date\n1,2,2025-01-01\n"
    source.write_text(original, encoding="utf-8")
    fake_disk = type("DiskUsage", (), {"free": 1024**3})()
    monkeypatch.setattr(build_processed.shutil, "disk_usage", lambda _: fake_disk)
    processed = tmp_path / "data" / "processed"
    with pytest.raises(OSError, match="No source files were changed"):
        run(parser().parse_args(["--raw-root", str(source.parents[3]), "--processed-root", str(processed)]))
    assert source.read_text(encoding="utf-8") == original
    assert not (processed / "observations").exists()


def test_catalog_records_unsupported_csv_without_processing_it(tmp_path):
    raw = tmp_path / "raw"
    raw.mkdir()
    (raw / "unrecognized_export.csv").write_text("x,y\n1,2\n", encoding="utf-8")
    entry, = discover_csv_files(raw)
    assert entry["supported"] is False
    assert entry["product"] == "UNSUPPORTED"
