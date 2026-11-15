import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.validation import CsvValidationError, parse_firms_csv


def test_parses_supported_firms_columns_and_preserves_original_metadata():
    records = parse_firms_csv(b"latitude,longitude,acq_date,satellite,bright_ti4,confidence,daynight,version\n-3.1,-60.2,2026-10-01,VIIRS,320,nominal,D,2.0\n")
    assert records[0]["latitude"] == -3.1
    assert records[0]["sensor"] == "VIIRS"
    assert records[0]["version"] == "2.0"
    assert records[0]["brightness"] == 320


def test_reports_missing_columns_actionably():
    with pytest.raises(CsvValidationError, match="Missing required field"):
        parse_firms_csv(b"lat,brightness\n1,300\n")


def test_reports_invalid_coordinates_with_row_number():
    with pytest.raises(CsvValidationError, match="Row 2: coordinates"):
        parse_firms_csv(b"lat,lon,date,sensor\n91,20,2026-10-01,MODIS\n")


def test_refuses_blank_sensor_and_bad_brightness():
    with pytest.raises(CsvValidationError, match="sensor is blank"):
        parse_firms_csv(b"lat,lon,date,sensor\n1,20,2026-10-01,\n")
    with pytest.raises(CsvValidationError, match="brightness must be numeric"):
        parse_firms_csv(b"lat,lon,date,sensor,brightness\n1,20,2026-10-01,MODIS,hot\n")


def test_reports_invalid_date_format():
    with pytest.raises(CsvValidationError, match="ISO date"):
        parse_firms_csv(b"lat,lon,date,sensor\n1,20,10/01/2026,MODIS\n")


def test_date_window_filters_records_and_allows_no_matches():
    from datetime import date
    content = b"latitude,longitude,acq_date,instrument,brightness\n1,20,2025-01-01,MODIS,300\n2,21,2025-01-03,MODIS,301\n"
    result = parse_firms_csv(content, date_start=date(2025, 1, 2), date_end=date(2025, 1, 4))
    assert [row["acquired"] for row in result] == ["2025-01-03"]
    assert parse_firms_csv(content, date_start=date(2025, 2, 1), date_end=date(2025, 2, 2), allow_empty=True) == []


def test_rejects_empty_rows():
    with pytest.raises(CsvValidationError, match="No data rows"):
        parse_firms_csv(b"lat,lon,date,sensor\n")


def test_ingestion_api_returns_clear_validation_error_and_health_status():
    client = TestClient(app)
    health = client.get("/api/health")
    body = health.json()
    assert body["local_analytics_available"] is (body["data_status"] == "Processed local FIRMS archives")
    assert body["harmonization"] in {"not applied", "comparison only; calibration insufficient"}
    result = client.post("/api/ingest/firms", files={"file": ("bad.csv", b"lat,lon\n1,2\n", "text/csv")})
    assert result.status_code == 422
    assert "Missing required field" in result.json()["detail"]


def test_local_archive_reads_country_files_and_keeps_sensors_distinct(tmp_path, monkeypatch):
    from datetime import date
    from app import local_archive
    monkeypatch.setattr(local_archive, "DATA_ROOT", tmp_path)
    modis = tmp_path / "MODIS_SP" / "modis" / "2025"
    viirs = tmp_path / "VIIRS_SNPP_SP" / "viirs-snpp" / "2025"
    modis.mkdir(parents=True); viirs.mkdir(parents=True)
    (modis / "modis_2025_Testland.csv").write_text("latitude,longitude,acq_date,satellite,instrument,brightness,version\n1,20,2025-01-01,TERRA,MODIS,300,6.1\n1,20,2025-01-10,TERRA,MODIS,301,6.1\n", encoding="utf-8")
    (viirs / "viirs-snpp_2025_Testland.csv").write_text("latitude,longitude,acq_date,satellite,instrument,bright_ti4,version\n2,21,2025-01-01,N,VIIRS,320,2.0\n", encoding="utf-8")
    assert local_archive.available_countries() == ["Testland"]
    records = local_archive.load_country_window("Testland", date(2025, 1, 1), date(2025, 1, 2))
    assert {row["firms_dataset"] for row in records} == {"MODIS_SP", "VIIRS_SNPP_SP"}
    assert len(records) == 2
    assert records[0]["original_fields"]["version"] == "6.1"


def test_local_archive_catalog_exposes_sources_by_year_and_future_noaa21(tmp_path, monkeypatch):
    from datetime import date
    from app import local_archive
    monkeypatch.setattr(local_archive, "DATA_ROOT", tmp_path)
    modis = tmp_path / "MODIS_SP" / "modis" / "2010"
    noaa21 = tmp_path / "VIIRS_NOAA21_SP" / "viirs-jpss2" / "2024"
    modis.mkdir(parents=True); noaa21.mkdir(parents=True)
    (modis / "modis_2010_Testland.csv").write_text("latitude,longitude,acq_date,instrument\n1,20,2010-01-01,MODIS\n", encoding="utf-8")
    (noaa21 / "viirs-jpss2_2024_Testland.csv").write_text("latitude,longitude,acq_date,instrument\n2,21,2024-01-01,VIIRS\n", encoding="utf-8")
    assert [p["id"] for p in local_archive.available_products(2010)] == ["MODIS_SP"]
    assert [p["id"] for p in local_archive.available_products(2024)] == ["VIIRS_NOAA21_SP"]
    assert local_archive.available_countries(2024) == ["Testland"]
    records = local_archive.load_country_window("Testland", date(2024, 1, 1), date(2024, 1, 1), 2024)
    assert records[0]["firms_dataset"] == "VIIRS_NOAA21_SP"
    summary = local_archive.summarize_country_month("Testland", 2024, 1)
    assert summary["total"] == 1
    assert summary["days"][0]["by_product"] == {"VIIRS_NOAA21_SP": 1}
    assert summary["days"][1]["count"] == 0
