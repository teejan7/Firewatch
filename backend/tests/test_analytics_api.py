import json
import sys
from datetime import date
from pathlib import Path

import duckdb
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.analytics_api import AnalyticsQueryError, check_coverage, get_calendar
from app.main import app


@pytest.fixture
def cells_file(tmp_path, monkeypatch):
    path = tmp_path / "daily_cell.parquet"
    con = duckdb.connect()
    con.execute("""CREATE TABLE c (
      acq_date DATE, lat_i INTEGER, lon_i INTEGER, sensor_family VARCHAR,
      platform VARCHAR, product_type VARCHAR, daynight VARCHAR, n_raw BIGINT,
      n_dedup BIGINT, frp_sum DOUBLE, frp_max DOUBLE)""")
    con.executemany("INSERT INTO c VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [
        (date(2025, 1, 1), 360, 720, "MODIS", "Terra", "SP", "D", 3, 1, 8.0, 5.0),
        (date(2025, 1, 1), 360, 720, "VIIRS", "NOAA-20", "SP", "D", 4, 1, 12.0, 8.0),
        (date(2025, 1, 2), 361, 721, "MODIS", "Aqua", "SP", "N", 1, 1, None, None),
        (date(2025, 1, 1), 360, 720, "VIIRS", "NOAA-21", "NRT", "D", 1, 1, None, None),
    ])
    con.execute("COPY c TO ? (FORMAT PARQUET)", [str(path)])
    con.close()
    monkeypatch.setattr("app.analytics_api.DAILY_CELLS", path)
    return path


def test_calendar_bbox_query_is_bounded_and_keeps_product_streams(cells_file):
    result = get_calendar(date(2025, 1, 1), date(2025, 1, 2), bbox=[-1, -1, 1, 1])
    assert result["data_status"] == "Processed local FIRMS archives"
    assert result["time_standard"] == "UTC acquisition date"
    assert result["daily_union"][0]["cross_sensor_overlap_cell_days"] == 1
    assert {x["product_type"] for x in result["daily_by_product_platform"]} == {"SP"}


def test_calendar_geojson_filters_cell_centers(cells_file):
    geometry = {"type": "Polygon", "coordinates": [[[-0.2, -0.2], [0.2, -0.2], [0.2, 0.2], [-0.2, 0.2], [-0.2, -0.2]]]}
    result = get_calendar(date(2025, 1, 1), date(2025, 1, 1), geojson=json.dumps(geometry))
    assert result["aoi_mode"] == "GeoJSON polygon by cell center"
    assert result["daily_union"][0]["unique_detected_cell_days"] == 1


def test_calendar_reads_product_family_year_partitioned_dataset(tmp_path, monkeypatch):
    dataset = tmp_path / "daily_cell"
    con = duckdb.connect()
    con.execute("""CREATE TABLE cells AS SELECT DATE '2025-01-01' AS acq_date, 360::INTEGER AS lat_i,
      720::INTEGER AS lon_i, 'MODIS'::VARCHAR AS sensor_family, 'Terra'::VARCHAR AS platform,
      'SP'::VARCHAR AS product_type, 2025::INTEGER AS year, 'D'::VARCHAR AS daynight,
      1::BIGINT AS n_raw, 1::BIGINT AS n_dedup, 4.0::DOUBLE AS frp_sum, 4.0::DOUBLE AS frp_max""")
    con.execute("COPY cells TO ? (FORMAT PARQUET, PARTITION_BY (product_type, sensor_family, year))", [str(dataset)])
    con.close()
    monkeypatch.setattr("app.analytics_api.DAILY_CELLS", dataset)
    result = get_calendar(date(2025, 1, 1), date(2025, 1, 1), product_type="SP")
    assert result["daily_union"][0]["unique_detected_cell_days"] == 1


def test_calendar_rejects_bad_polygon_and_long_window(cells_file):
    invalid = {"type": "Polygon", "coordinates": [[[0, 0], [1, 1], [0, 1], [1, 0], [0, 0]]]}
    with pytest.raises(AnalyticsQueryError, match="self-intersects"):
        get_calendar(date(2025, 1, 1), date(2025, 1, 1), geojson=json.dumps(invalid))
    with pytest.raises(AnalyticsQueryError, match="limited to"):
        get_calendar(date(2024, 1, 1), date(2025, 1, 2))


def test_api_calendar_and_insufficient_anomaly_status(cells_file, monkeypatch, tmp_path):
    report = tmp_path / "quality.json"
    report.write_text(json.dumps({"files_discovered": 4, "files_processed_total": 3, "files_failed_total": 0, "coverage": {"date_min": "2025-01-01"}, "rows_by_sensor_year_product": {}}))
    monkeypatch.setattr("app.analytics_api.QUALITY_REPORT", report)
    client = TestClient(app)
    calendar = client.get("/api/calendar", params={"start_date": "2025-01-01", "end_date": "2025-01-02", "bbox": "-1,-1,1,1"})
    assert calendar.status_code == 200
    anomaly = client.get("/api/anomalies", params={"start_date": "2025-01-01", "end_date": "2025-01-02"})
    assert anomaly.status_code == 200
    assert anomaly.json()["status"] == "insufficient_baseline"
    assert anomaly.json()["results"] == []


def test_api_returns_actionable_errors(cells_file):
    client = TestClient(app)
    invalid = client.get("/api/calendar", params={"start_date": "2025-01-01", "end_date": "2025-01-02", "bbox": "bad"})
    assert invalid.status_code == 422
    assert "west,south,east,north" in invalid.json()["detail"]
    missing = client.get("/api/calendar", params={"start_date": "2025-01-01", "end_date": "2026-01-02"})
    assert missing.status_code == 422


def test_coverage_check_labels_date_envelopes_and_spatial_uncertainty(monkeypatch, tmp_path):
    report = tmp_path / "quality.json"
    report.write_text(json.dumps({
        "files_discovered": 2, "files_expected": 2, "files_processed_total": 2,
        "files_failed_total": 0, "coverage_by_product_platform_year": [{
            "product_type": "SP", "platform": "NOAA-21", "year": 2025,
            "first_date": "2025-01-01", "last_date": "2025-12-31",
            "files_expected": 2, "files_processed": 2, "files_failed": 0,
            "status": "complete", "source_scope": "global",
        }],
    }), encoding="utf-8")
    monkeypatch.setattr("app.analytics_api.QUALITY_REPORT", report)
    result = check_coverage(date(2025, 3, 1), date(2025, 3, 3), product_type="SP", platform="NOAA-21", bbox=[-1, -1, 1, 1])
    assert result["status"] == "fully_covered"
    assert result["spatial_coverage"] == "not_assessed"
    assert "not establish daily observation opportunity" in result["coverage_basis"]


def test_coverage_check_suggests_alternate_processing_stream(monkeypatch, tmp_path):
    report = tmp_path / "quality.json"
    report.write_text(json.dumps({"coverage_by_product_platform_year": [{
        "product_type": "NRT", "platform": "NOAA-21", "year": 2026,
        "first_date": "2026-08-01", "last_date": "2026-11-01",
        "files_expected": 1, "files_processed": 1, "status": "complete", "source_scope": "global",
    }]}), encoding="utf-8")
    monkeypatch.setattr("app.analytics_api.QUALITY_REPORT", report)
    result = check_coverage(date(2026, 10, 1), date(2026, 10, 5), product_type="SP", platform="NOAA-21")
    assert result["status"] == "not_covered"
    assert result["suggested_product_type"] == "NRT"


def test_coverage_endpoints_publish_file_completeness_and_validate_selection(monkeypatch, tmp_path):
    report = tmp_path / "quality.json"
    report.write_text(json.dumps({
        "files_discovered": 1, "files_expected": 1, "files_processed_total": 1,
        "files_failed_total": 0, "coverage_by_product_platform_year": [{
            "product_type": "SP", "platform": "Terra", "year": 2025,
            "first_date": "2025-01-01", "last_date": "2025-12-31",
            "files_expected": 1, "files_processed": 1, "status": "complete", "source_scope": "country_files",
        }],
    }), encoding="utf-8")
    monkeypatch.setattr("app.analytics_api.QUALITY_REPORT", report)
    client = TestClient(app)
    assert client.get("/api/coverage").json()["coverage"][0]["files_expected"] == 1
    checked = client.get("/api/coverage/check", params={
        "start": "2025-04-01", "end": "2025-04-30", "platform": "Terra", "bbox": "-1,-1,1,1",
    })
    assert checked.status_code == 200
    assert checked.json()["status"] == "fully_covered"
    assert checked.json()["spatial_coverage"] == "not_assessed"
    invalid = client.get("/api/coverage/check", params={"start": "2025-04-30", "end": "2025-04-01"})
    assert invalid.status_code == 422
