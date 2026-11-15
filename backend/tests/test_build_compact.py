import json

from scripts.build_compact import load_sources


def test_load_sources_keeps_country_sp_and_omits_global_and_nrt(tmp_path):
    root = tmp_path / "processed"
    root.mkdir()
    (root / "daily" / "country.parquet").parent.mkdir(parents=True)
    (root / "daily" / "country.parquet").write_bytes(b"fixture")
    manifest = {"files": {
        "country": {"status": "complete", "product_type": "SP", "country": "Example",
                    "aggregation_format": 2, "output_file": "daily/country.parquet", "grid_file": "daily/country.parquet",
                    "year": 2020, "sensor_family": "MODIS", "platform": "MODIS",
                    "source_file": "MODIS_SP/modis/2020/modis_2020_Example.csv",
                    "row_count": 5, "aggregated_detection_count": 4},
        "global": {"status": "complete", "product_type": "SP", "country": None,
                   "output_file": "daily/country.parquet", "grid_file": "daily/grid.parquet",
                   "year": 2020, "sensor_family": "VIIRS", "platform": "NOAA-21"},
        "nrt": {"status": "complete", "product_type": "NRT", "country": "Example",
                "output_file": "daily/country.parquet", "grid_file": "daily/grid.parquet",
                "year": 2020, "sensor_family": "VIIRS", "platform": "NOAA-20"},
    }}
    (root / "daily_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    _, sources = load_sources(root)

    assert len(sources) == 1
    assert sources[0]["country"] == "Example"
    assert sources[0]["product_type"] == "SP"
    assert sources[0]["rows_processed"] == 4
    assert sources[0]["rows_source"] == 5


def test_load_sources_reports_actionable_missing_manifest(tmp_path):
    try:
        load_sources(tmp_path)
    except FileNotFoundError as error:
        assert "daily_manifest.json" in str(error)
    else:
        raise AssertionError("Expected a missing-manifest error")
