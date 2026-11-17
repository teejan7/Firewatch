# FIREWATCH data engine

FIREWATCH has a compact pipeline for the active static dashboard and an older processing path for optional local API queries. They write different products and should not be confused.

## Active static-dashboard pipeline

The active browser app reads only JSON under frontend/public/data. It does not access raw CSVs, Parquet, FastAPI, or NASA at runtime.

1. **Daily aggregation — backend/scripts/build_daily.py.** Discovers supported local FIRMS country CSVs under data/raw/extracted and uses DuckDB to aggregate directly from CSV. The default build covers 2020–2025. It writes compact Parquet outputs under data/processed/daily and a resumable data/processed/daily_manifest.json. Aggregates include daily country/platform rows and 1-degree display-grid rows, detection and FRP summaries, vegetation (type=0), nominal/high-confidence subset, day/night fields, a reported-detection platform-day flag, and source metadata. DuckDB uses a 2 GiB memory limit and four threads; a 3 GiB free-space guard stops work before or after each sensor-year. Temporary spill directories are removed after each sensor-year.
2. **Static export — backend/scripts/build_compact.py.** Reads current-format daily aggregates and their manifest, then generates countries.json, country series, map_activity.json, quality.json, and related JSON in frontend/public/data. The active map uses country-level observed centroids and summary totals; it does not create boundaries or fire perimeters.
3. **Experimental analytics — backend/scripts/run_harmonize.py and backend/scripts/harmonize_core.py.** Reads the 2020–2025 daily aggregates, filters to vegetation records, fits the exploratory weekly FRP calibration, and writes per-country analytics plus methods_validation.json. See METHODOLOGY.md and HARMONIZATION.md.

The source CSVs are not in the repository and are absent from the current checkout. The compact build and raw validation therefore cannot be fully reproduced here until matching inputs are restored. If build_compact.py is run without the extracted CSV inventory, its source-coverage discovery cannot recreate the original coverage statuses.

## Older local-API processing path

backend/scripts/build_processed.py is a separate processor for local analytics. It can create normalized row-level observation Parquet, manifests and quality reports, plus daily-cell summaries under data/processed. Its daily-cell data uses a 0.25-degree spatial grid and is consumed by the optional FastAPI comparison API. It does not power the active static dashboard or perform scientific cross-sensor calibration. This checkout currently lacks the observations and cell_shards directories; the daily-cell artifact and related metadata may be local and are not packaged with a fresh Git clone.

The daily-cell comparison query reports sensor/platform-specific detected cell-days and same-cell/date overlap. It is not event matching, a count of unique fires, or a calibrated MODIS/VIIRS conversion. Coverage endpoints use file inventories and date envelopes; their spatial coverage is not assessed.

## Run commands

From the repository root, after placing supported FIRMS country CSVs under data/raw/extracted and installing Python dependencies:

~~~powershell
.venv\Scripts\python.exe backend\scripts\build_daily.py
.venv\Scripts\python.exe backend\scripts\build_compact.py
.venv\Scripts\python.exe backend\scripts\run_harmonize.py
~~~

To use the older API query data, run the documented build_processed.py command in [API documentation](API.md) only when that separate dataset path is needed. Do not assume the two pipelines produce interchangeable Parquet schemas.

## Data integrity notes

Source CSVs are intended to remain read-only. Detection totals are record counts, not unique-fire counts. The reported platform-day flag is not an observation-opportunity denominator. The builder filters invalid dates/coordinates but does not independently count exact duplicate input rows in the compact export metadata. The recorded raw-count validation is limited to four countries and six years and does not validate the calibration scientifically.

## Related documentation

- [Data and coverage](DATA.md)
- [Optional FastAPI endpoints](API.md)
- [Methodology](METHODOLOGY.md)
- [Validation record](VALIDATION.md)