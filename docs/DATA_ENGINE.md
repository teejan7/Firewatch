# FIREWATCH processed data engine

## Scope and source safety

`backend/scripts/build_processed.py` discovers FIRMS CSV files below `data/raw/extracted/`, classifies known MODIS, VIIRS S-NPP, NOAA-20 and NOAA-21 products, and writes normalized Parquet plus manifests below `data/processed/`. It never writes to the raw archive. The processor distinguishes country/year files from NOAA-21 global files and labels `fire_archive_*` as SP and `fire_nrt_*` as NRT.

Run a small country/year subset first:

```powershell
.venv\Scripts\python.exe backend\scripts\build_processed.py --product MODIS_SP --product VIIRS_SNPP_SP --product VIIRS_NOAA20_SP --year 2025 --country India --build-daily-cells
```

Process all discovered Standard Processing files, then include NRT files explicitly when desired:

```powershell
.venv\Scripts\python.exe backend\scripts\build_processed.py --build-daily-cells
.venv\Scripts\python.exe backend\scripts\build_processed.py --include-nrt --build-daily-cells
```

The run is resumable: unchanged source files with a completed output are skipped. A changed source file is reprocessed into a temporary Parquet file and atomically replaces its prior output only after conversion succeeds. A 2 GiB free-space reserve is maintained; process a smaller selection or free disk space if preflight stops a file. Do not use `--force` unless reprocessing is intentional.

## Outputs

- `data/processed/archive_index.json`: discovered file paths, product/platform/processing type, year, scope, size, status, and coverage when processing has completed.
- `data/processed/manifest.json`: file signatures, validation counts, output partitions, observed date limits, missing-field counts, processing versions, and exact duplicate counts.
- `data/processed/quality_report.json`: run timing, file totals, failures and row-quality summaries by sensor/year/product.
- `data/processed/observations/`: Parquet partitions by sensor family, year, product type and source product.
- `data/processed/daily_cell.parquet`: optional 0.25-degree daily aggregation built from successfully processed outputs.

The common Parquet schema includes acquisition date/time, coordinates, satellite, instrument, sensor family, platform, product type, confidence, day/night, FRP, MODIS brightness, VIIRS `bright_ti4`/`bright_ti5`, source filename, source record ID, processing version, product ID, an exact-row fingerprint, and JSON with original source columns. Sensor-specific brightness fields are never converted into one another. Missing values remain null.

Rows with invalid dates or out-of-range/missing coordinates are reported and omitted from the analytical Parquet. Non-numeric optional measurements are reported separately and remain null in the normalized fields. Their source CSV rows remain untouched. The source record ID is the discovered source-file identity plus CSV row number. The exact duplicate metric uses a fingerprint of all original fields and is reported per source file. Raw source rows remain present. `daily_cell.n_raw` counts valid rows; `n_dedup` is one cell-day presence for each date/cell/sensor/platform/product/daynight group. It is not a count of unique fires. This definition collapses repeated rows into cell presence within each group, while retaining raw rows and exact-duplicate diagnostics. It does not infer duplicates from proximity or merge sensors.

The grid uses 0.25-degree cells. `lat_i` and `lon_i` are zero-based indices of the cell's lower-left edge at `(-90 + 0.25*lat_i, -180 + 0.25*lon_i)`. Points at +90/+180 are clamped into the last valid cell. `n_raw` and `n_dedup` stay separate; FRP sums/maxima use available raw FRP observations and null FRP is not replaced with zero.

## Current integration boundary

This is Phase 1 data preparation. The dashboard and API have not yet been migrated to query these Parquet outputs. Existing local archive endpoints still read their current CSV-backed country data path; NOAA-21 global-file query integration, unified calendar APIs, map aggregation, calibration and anomaly analysis remain later phases. The processor does not perform scientific harmonization.
