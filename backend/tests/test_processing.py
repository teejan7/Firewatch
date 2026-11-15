import json
import sys
from pathlib import Path

import duckdb

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.build_processed import build_daily_cells, discover_csv_files, process_entry


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
        cell = connection.execute("SELECT n_raw, n_dedup, frp_sum, frp_max FROM read_parquet(?)", [summary["output_file"]]).fetchone()
        assert cell == (3, 1, 11.0, 5.5)
    finally:
        connection.close()

    manifest = json.loads((processed / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["files"][entry["file_id"]]["status"] == "processed"


def test_catalog_records_unsupported_csv_without_processing_it(tmp_path):
    raw = tmp_path / "raw"
    raw.mkdir()
    (raw / "unrecognized_export.csv").write_text("x,y\n1,2\n", encoding="utf-8")
    entry, = discover_csv_files(raw)
    assert entry["supported"] is False
    assert entry["product"] == "UNSUPPORTED"
