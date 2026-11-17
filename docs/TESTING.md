# Testing and verification

Run from the repository root. The active dashboard uses packaged JSON and can be built or served with the backend stopped.

~~~powershell
npm run check
~~~

This runs TypeScript checks, ESLint, frontend tests, the Vite production build, Ruff, and backend pytest. Backend pytest uses an external temporary directory configured in backend/pyproject.toml. A passing software check does not establish scientific validity of the calibration or seasonal analytics. See [Validation](VALIDATION.md) for the last recorded software and data checks; those historical checks were not rerun as part of this documentation update.

Run npm run start to serve the active static dashboard locally; run npm run build to create the production frontend; npm run preview serves that build. The CARTO basemap needs internet access. Packaged JSON and calendar controls do not require NASA credentials or a running API.

## Rebuilding the static data

The compact builder reads extracted FIRMS CSVs from data/raw/extracted and does not call NASA or require a MAP_KEY. It processes 2020–2025 by default, writes progress to data/processed/daily_manifest.json, logs to logs/build_daily.log, and enforces a 3 GiB free-space guard. Each sensor-year uses a temporary DuckDB spill directory. The original CSVs are intended to remain unchanged.

~~~powershell
.venv\Scripts\python.exe backend\scripts\build_daily.py
.venv\Scripts\python.exe backend\scripts\build_compact.py
.venv\Scripts\python.exe backend\scripts\run_harmonize.py
~~~

The extracted source files are absent from the current checkout. Restore the matching FIRMS CSVs before rebuilding daily aggregates or rerunning raw-count validation. Rebuilding static coverage metadata without the extracted filename inventory can change coverage statuses. The prebuilt dashboard JSON remains available in the repository.

The older backend/scripts/build_processed.py path creates separate legacy products for the optional API; it is not required by the active dashboard. See [Data engine](DATA_ENGINE.md) and [API](API.md).