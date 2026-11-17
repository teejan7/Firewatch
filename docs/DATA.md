# Data and coverage

## Provenance and runtime

The active dashboard uses packaged JSON generated from NASA FIRMS Standard Processing country CSVs. It does not call NASA services at runtime and does not require a NASA API key. The repository includes derived JSON; it does not include the original FIRMS CSVs, local Parquet aggregates, or credentials.

The current package covers 2020–2025 and generated metadata reports 3,859 processed country-scoped source files, 265,659,156 detection records, and 236 country labels. Products/platforms are MODIS Terra/Aqua, VIIRS Suomi-NPP, and VIIRS NOAA-20. NOAA-21 country records are not included in the active static data.

## Packaged files

- countries.json is the country-label index used by the selector.
- map_activity.json contains country summaries loaded when the map is displayed.
- series/<slug>.json contains one country's daily sensor/platform records and source metadata.
- harmonized/<slug>.json contains experimental vegetation-FRP calibration, daily and weekly values, and preliminary multi-year and season summaries.
- methods_validation.json contains method settings, internal LOYO metrics, confidence counts, and limitations.
- quality.json contains source-file inventory and processing summary metadata.

Daily raw series include all detection types and retain vegetation-only (type=0), confidence-filtered, day/night, platform-day, and source metadata fields. The active raw calendar summarizes all types; calibration and lower multi-year analytics use vegetation-only records. Detection totals count FIRMS records, not unique fires. FRP is in MW.

## Rebuild and reproducibility

The recommended compact pipeline is backend/scripts/build_daily.py, then backend/scripts/build_compact.py, then backend/scripts/run_harmonize.py. The daily builder reads extracted files from data/raw/extracted, creates compact Parquet aggregates under data/processed/daily, and updates data/processed/daily_manifest.json. It uses DuckDB with a 2 GiB memory limit, four threads, and a 3 GiB free-disk stop guard. The static exporter reads the daily manifest and aggregates; it does not need the older observations or cell_shards outputs.

The original extracted CSVs are absent from the current checkout. Restore the matching FIRMS country CSVs before rebuilding daily aggregates or repeating raw-count validation. Existing daily Parquet may support regenerating some products, but without the extracted source inventory the exporter cannot reconstruct the original source-file coverage. Do not treat a rebuild without those inputs as equivalent to the packaged release.

~~~powershell
.venv\Scripts\python.exe backend\scripts\build_daily.py
.venv\Scripts\python.exe backend\scripts\build_compact.py
.venv\Scripts\python.exe backend\scripts\run_harmonize.py
~~~

The derived dashboard JSON is required for the static app. Raw CSVs, Parquet, .env files, and credentials should not be published. The optional older FastAPI path uses separate processed daily-cell artifacts; it is not the runtime data path for the active dashboard. See [Data engine](DATA_ENGINE.md) and [API](API.md).

## Coverage and interpretation

Coverage is based on discovered source filenames and which files were successfully aggregated. It does not indicate per-location satellite observation opportunity. A missing date or row does not prove no fire occurred. MODIS and VIIRS have different footprints and detection behavior; their FRP and counts are not automatically comparable. The calibration's operating-week method does not establish country-specific observation opportunity. See [Methodology](METHODOLOGY.md), [Harmonization](HARMONIZATION.md), and [Limitations](LIMITATIONS.md).