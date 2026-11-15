# Data and coverage

## Provenance

The packaged snapshot was generated from local NASA FIRMS Standard Processing CSV files using the DuckDB streaming pipeline, then exported as static JSON. FIRMS is the data source; this application does not call NASA services at runtime. Keep product, platform, original filename and processing metadata attached to derived rows. See [NASA FIRMS](https://www.earthdata.nasa.gov/data/tools/firms) and the product references in the README.

## What is included

The generated frontend/public/data/quality.json is the source of truth for file and row totals. It reports 3,859 processed country-scoped files and 265,659,156 detections across 236 country labels for the packaged 2020–2025 set. Consult quality.json for product/year coverage. Do not treat absent dates or years as zero activity.

The country selector index is `countries.json`; larger activity summaries for the interactive map are in `map_activity.json` and loaded only when the map is opened. Country daily series are loaded on demand from `series/<slug>.json`.

Daily country series retain source detections and FRP plus vegetation-only counts/FRP (type=0), quality-filtered counts/FRP, day/night counts/FRP, a platform-day detected flag, and availability flags. Confidence inclusion follows the sensor-specific rule in Methodology. NOAA-21 global files remain excluded from country summaries because verified country attribution is not implemented; no boundary polygons are included.

## Reproduce locally

Original extracted files are under data/raw/extracted/ and were read-only inputs; data/raw/archives/ is empty. Preserve the raw CSVs. The recommended pipeline is backend/scripts/build_daily.py followed by backend/scripts/build_compact.py. The daily builder writes only aggregates to data/processed/daily/ and its independent data/processed/daily_manifest.json; it has a 2 GiB DuckDB memory limit, four threads and a 3 GiB free-disk stop guard. The static exporter reads only daily aggregates, never observations/ or cell_shards/.

Build the default 2020–2025 local daily aggregates, then export static browser data:

```powershell
.venv\Scripts\python.exe backend\scripts\build_daily.py
.venv\Scripts\python.exe backend\scripts\build_compact.py
```

The static JSON folder is required for a deployable release. Raw CSVs, Parquet, .env and credentials must not be published. The daily builder and exporter do not delete legacy observations/cell_shards; review the validation table before deciding whether to remove those old intermediates yourself.

## Interpretation

FRP and detection totals are observations from different instruments with different pixel footprints, overpass times, and detection behavior. They are not interchangeable. Source-file completeness does not indicate continuous coverage or absence of fire. The package does not estimate missed detections or sensor observation opportunity.
