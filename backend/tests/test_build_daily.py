import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts import build_daily


def _seed(tmp_path: Path, monkeypatch, filename: str, product_folder: str, rows: str):
    root = tmp_path / "project"
    raw = root / "data" / "raw" / "extracted" / product_folder
    raw.mkdir(parents=True)
    source = raw / filename
    source.write_text(rows, encoding="utf-8")
    monkeypatch.setattr(build_daily, "ROOT", root)
    monkeypatch.setattr(build_daily, "RAW_ROOT", root / "data" / "raw" / "extracted")
    monkeypatch.setattr(build_daily, "DAILY_ROOT", root / "data" / "processed" / "daily")
    monkeypatch.setattr(build_daily, "MANIFEST_PATH", root / "data" / "processed" / "daily_manifest.json")
    monkeypatch.setattr(build_daily, "LOG_PATH", root / "logs" / "build_daily.log")
    monkeypatch.setattr(build_daily, "_disk_free", lambda: 10 * 1024**3)
    return root, source


def test_build_daily_streams_modis_metrics_and_resumes(tmp_path, monkeypatch):
    root, source = _seed(
        tmp_path,
        monkeypatch,
        "modis_2020_Bahrain.csv",
        "modis",
        "latitude,longitude,acq_date,frp,satellite,confidence,type,daynight,version\n"
        "26.1,50.5,2020-01-01,1.5,Terra,30,0,D,6.1\n"
        "26.2,50.6,2020-01-01,2.5,Aqua,29,2,N,6.1\n"
        "26.3,50.7,2020-01-01,3.5,Terra,80,0,D,6.1\n",
    )
    first = build_daily.run({2020})
    assert first["files_complete"] == 1
    manifest = json.loads(build_daily.MANIFEST_PATH.read_text(encoding="utf-8"))
    record = next(iter(manifest["files"].values()))
    assert record["row_count"] == 3
    assert record["aggregated_detection_count"] == 3
    assert record["aggregation_format"] == 2
    assert record["processing_versions"] == ["6.1"]

    import duckdb

    daily_path = root / record["output_file"]
    con = duckdb.connect()
    rows = con.execute(
        "SELECT platform,n_detections,vegetation_n_detections,high_quality_n_detections,"
        "day_n_detections,night_n_detections,platform_day_observed "
        "FROM read_parquet(?) WHERE aggregation_level='daily' ORDER BY platform",
        [str(daily_path)],
    ).fetchall()
    levels = dict(con.execute(
        "SELECT aggregation_level,COUNT(*) FROM read_parquet(?) GROUP BY aggregation_level",
        [str(daily_path)],
    ).fetchall())
    con.close()
    assert rows == [("Aqua", 1, 0, 0, 0, 1, 1), ("Terra", 2, 2, 2, 2, 0, 1)]
    assert levels == {"daily": 2, "grid": 2}
    assert source.is_file()
    resumed = build_daily.run({2020})
    assert resumed["files_complete"] == 1
    assert resumed["results"][0]["detections"] == 3


def test_viirs_high_quality_uses_nominal_and_high_classes(tmp_path, monkeypatch):
    root, _ = _seed(
        tmp_path,
        monkeypatch,
        "viirs-snpp_2020_Bahrain.csv",
        "viirs-snpp",
        "latitude,longitude,acq_date,frp,satellite,confidence,type,daynight\n"
        "26.1,50.5,2020-01-01,1.5,N,n,0,D\n"
        "26.2,50.6,2020-01-01,2.5,N,h,1,N\n"
        "26.3,50.7,2020-01-01,3.5,N,l,0,D\n",
    )
    result = build_daily.run({2020})
    assert result["files_complete"] == 1
    manifest = json.loads(build_daily.MANIFEST_PATH.read_text(encoding="utf-8"))
    record = next(iter(manifest["files"].values()))
    import duckdb

    con = duckdb.connect()
    daily_path = root / record["output_file"]
    row = con.execute(
        "SELECT n_detections,vegetation_n_detections,high_quality_n_detections,"
        "high_quality_frp_sum_mw,day_n_detections,night_n_detections "
        "FROM read_parquet(?) WHERE aggregation_level='daily'",
        [str(daily_path)],
    ).fetchone()
    con.close()
    assert row == (3, 2, 2, 4.0, 2, 1)


def test_disk_guard_stops_before_sensor_year(tmp_path, monkeypatch, capsys):
    _seed(
        tmp_path,
        monkeypatch,
        "modis_2020_Bahrain.csv",
        "modis",
        "latitude,longitude,acq_date\n26.1,50.5,2020-01-01\n",
    )
    monkeypatch.setattr(build_daily, "_disk_free", lambda: 2 * 1024**3)
    result = build_daily.run({2020}, min_free_bytes=0)
    assert result["groups_processed"] == 0
    assert not build_daily.MANIFEST_PATH.exists()
    assert "STOP before" in capsys.readouterr().out


def test_missing_required_column_has_actionable_error(tmp_path, monkeypatch):
    _seed(
        tmp_path,
        monkeypatch,
        "modis_2020_Bahrain.csv",
        "modis",
        "latitude,acq_date\n26.1,2020-01-01\n",
    )
    with pytest.raises(RuntimeError, match="Missing required FIRMS columns: longitude"):
        build_daily.run({2020})
