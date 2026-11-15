# FIREWATCH processed data engine

## Scope and source safety

`backend/scripts/build_processed.py` discovers FIRMS CSV files below `data/raw/extracted/`, classifies known MODIS, VIIRS S-NPP, NOAA-20 and NOAA-21 products, and writes normalized Parquet plus manifests below `data/processed/`. It never writes to the raw archive. The processor distinguishes country/year files from NOAA-21 global files and labels `fire_archive_*` as SP and `fire_nrt_*` as NRT.

Run a small country/year subset first:

```powershell
.venv\Scripts\python.exe backend\scripts\build_processed.py --product MODIS_SP --product VIIRS_SNPP_SP --product VIIRS_NOAA20_SP --year 2025 --country India --build-daily-cells
```

Process every discovered eligible Standard Processing and Near Real-Time source by default:

```powershell
.venv\Scripts\python.exe backend\scripts\build_processed.py --build-daily-cells
```

For a smaller, submission-friendly 2020–2026 build on a low-space drive, double-click `process_2020_2026_compact.bat`. It writes per-file cell summaries instead of a duplicate row-level Parquet archive, then assembles the partitioned daily-cell dataset. Existing row-level Parquet outputs are converted to compact shards from those outputs rather than rereading their CSVs. The original CSVs remain the source of truth; manifests retain file provenance and row-quality counts. The estimate uses conservative compact-output and daily-output factors; if a per-file reserve check stops the run, free space or narrow the years and rerun.

The run is resumable and idempotent: unchanged source files with a completed output are skipped using the source path and file-size/mtime signature. A changed source file is reprocessed into a temporary Parquet file and atomically replaces its prior output only after conversion succeeds. Startup estimates the selected work and keeps a 2 GiB reserve; use product/year filters or free disk space if the estimate does not fit. `--allow-partial` opts into processing until the per-file space guard stops work. `--sp-only` excludes NRT files. `--force` intentionally reprocesses unchanged files.

## Outputs

- `data/processed/archive_index.json`: discovered file paths, product/platform/processing type, year, scope, size, status, and coverage when processing has completed.
- `data/processed/manifest.json`: file signatures, validation counts, output partitions, observed date limits, missing-field counts, processing versions, and exact duplicate counts.
- `data/processed/quality_report.json`: run timing, file totals, failures and row-quality summaries by sensor/year/product.
- `data/processed/observations/`: Parquet partitions by sensor family, year, product type and source product.
- `data/processed/cell_shards/`: compact per-source cell summaries used by low-space builds.
- `data/processed/daily_cell/product_type=…/sensor_family=…/year=…/`: optional 0.25-degree daily Parquet partitions.
- `data/processed/quarantine_report.json`: per-file processing failures and reasons; source CSVs are never moved or changed.

The full observation Parquet schema includes acquisition date/time, coordinates, satellite, instrument, sensor family, platform, product type, confidence, day/night, FRP, MODIS brightness, VIIRS `bright_ti4`/`bright_ti5`, source filename, source record ID, processing version, product ID, an exact-row fingerprint, and JSON with original source columns. Compact shards keep cell date, grid indices, sensor family, platform, stream, day/night, raw row count, cell presence, source-file count, and FRP summary. The original CSV remains at the source path recorded in the manifest; compact shards do not duplicate its columns. The daily-cell dataset is partitioned by product type, sensor family, and year. Acquisition time, platform, and day/night are preserved in the full observation outputs; compact mode does not calculate observation opportunity. Sensor-specific brightness fields are never converted into one another. Missing values remain null.

Rows with invalid dates or out-of-range/missing coordinates are reported and omitted from the analytical Parquet. Non-numeric optional measurements are reported separately and remain null in the normalized fields. Their source CSV rows remain untouched. The source record ID is the discovered source-file identity plus CSV row number. The exact duplicate metric uses a fingerprint of all original fields and is reported per source file. Raw source rows remain present. `daily_cell.n_raw` counts valid rows; `n_dedup` is one cell-day presence for each date/cell/sensor/platform/product/daynight group. It is not a count of unique fires. This definition collapses repeated rows into cell presence within each group, while retaining raw rows and exact-duplicate diagnostics. It does not infer duplicates from proximity or merge sensors. NOAA-21 SP takes precedence through the latest successfully processed SP date; NRT is included only afterward. Original NRT source rows remain available in the observations partitions.

The grid uses 0.25-degree cells. `lat_i` and `lon_i` are zero-based indices of the cell's lower-left edge at `(-90 + 0.25*lat_i, -180 + 0.25*lon_i)`. Points at +90/+180 are clamped into the last valid cell. `n_raw` and `n_dedup` stay separate; FRP sums/maxima use available raw FRP observations and null FRP is not replaced with zero.

## Current integration boundary

`GET /api/coverage` reports expected and processed files plus source date envelopes by product type, platform, and year. `GET /api/coverage/check?start=…&end=…&product_type=…&platform=…&bbox=…` checks the selected source-file date envelopes and suggests an alternate stream when available. These checks do not imply observation opportunity or zero activity; spatial coverage remains unassessed.

The dashboard's broader selection flow, map aggregation, calibration, and anomaly analysis remain later phases. The processor does not perform scientific harmonization.
