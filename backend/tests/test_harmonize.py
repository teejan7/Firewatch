from datetime import date

import duckdb
import pytest

from app.harmonize import HarmonizationQueryError, query_common_grid_comparison


@pytest.fixture
def daily_cells(tmp_path):
    path = tmp_path / "daily_cell.parquet"
    db = duckdb.connect()
    db.execute("""CREATE TABLE cells (
      acq_date DATE, lat_i INTEGER, lon_i INTEGER, sensor_family VARCHAR,
      platform VARCHAR, product_type VARCHAR, daynight VARCHAR, n_raw BIGINT,
      n_dedup BIGINT, frp_sum DOUBLE, frp_max DOUBLE)""")
    db.executemany("INSERT INTO cells VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [
        (date(2025, 1, 1), 360, 720, "MODIS", "Terra", "SP", "D", 4, 1, 10.0, 6.0),
        (date(2025, 1, 1), 360, 720, "VIIRS", "S-NPP", "SP", "D", 6, 1, 20.0, 12.0),
        (date(2025, 1, 1), 360, 720, "VIIRS", "NOAA-20", "SP", "D", 2, 1, 3.0, 3.0),
        (date(2025, 1, 1), 361, 720, "MODIS", "Aqua", "SP", "D", 1, 1, None, None),
        (date(2025, 1, 2), 360, 720, "VIIRS", "NOAA-21", "NRT", "N", 1, 1, None, None),
    ])
    db.execute("COPY cells TO ? (FORMAT PARQUET)", [str(path)])
    db.close()
    return path


def test_comparison_keeps_sources_separate_and_reports_cell_overlap(daily_cells):
    db = duckdb.connect()
    result = query_common_grid_comparison(db, [daily_cells], "2025-01-01", "2025-01-01")
    db.close()
    assert result["status"] == "comparison_only"
    assert result["harmonized_index"] is None
    assert result["calibration_status"] == "insufficient_calibration"
    assert result["calibration"]["coefficients"] is None
    assert result["calibration"]["validation_metrics"] is None
    assert result["daily_union"] == [{
        "date": "2025-01-01", "unique_detected_cell_days": 2,
        "modis_detected_cell_days": 2, "viirs_detected_cell_days": 1,
        "cross_sensor_overlap_cell_days": 1,
    }]
    assert {row["platform"] for row in result["daily_by_product_platform"]} == {"Terra", "Aqua", "S-NPP", "NOAA-20"}
    assert sum(row["raw_records"] for row in result["daily_by_product_platform"]) == 13


def test_nrt_and_platform_filter_are_explicit(daily_cells):
    db = duckdb.connect()
    result = query_common_grid_comparison(db, [daily_cells], "2025-01-01", "2025-01-02", product_type="NRT", platforms=["NOAA-21"])
    db.close()
    assert result["daily_union"][0]["date"] == "2025-01-02"
    assert result["daily_by_product_platform"][0]["platform"] == "NOAA-21"


@pytest.mark.parametrize("kwargs", [
    {"product_type": "MIXED"}, {"daynight": "X"}, {"platforms": ["unknown"]},
    {"bbox": [170, -10, -170, 10]}, {"bbox": [0, 0, 0, 10]},
])
def test_invalid_comparison_filters_are_actionable(daily_cells, kwargs):
    db = duckdb.connect()
    with pytest.raises(HarmonizationQueryError):
        query_common_grid_comparison(db, [daily_cells], "2025-01-01", "2025-01-02", **kwargs)
    db.close()
