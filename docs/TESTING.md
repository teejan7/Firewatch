# Testing and verification

Run from the project root. The dashboard itself uses static JSON and should work while the backend is stopped.

```powershell
npm run typecheck
npm run lint
npm test
npm run build
.venv\Scripts\python.exe -m pytest backend\tests
```

`npm run start` starts the local frontend and opens the browser. `npm run preview` serves the production build. The CARTO basemap requires network access; static data and calendar controls do not require NASA credentials or a running backend.

The repository's validation record describes previously run checks. Update `docs/VALIDATION.md` with the actual output and date after running checks on the current working tree. Software tests establish application behavior only; they do not establish scientific validity of cross-sensor comparisons.

## Rebuild local FIRMS aggregates

The daily builder reads extracted files in `data/raw/extracted/` and does not call NASA or require a MAP_KEY. It processes 2020–2025 by default, saves progress after each source file in `data/processed/daily_manifest.json`, and writes a run log to `logs/build_daily.log`. Before each sensor-year it requires 3 GiB free and it stops after a sensor-year if the free space falls below 3 GiB. Each sensor-year's DuckDB spill directory is temporary. `--force` refreshes an existing daily aggregate format; use it when changing aggregation code or quality rules.

```powershell
# Build/refresh the packaged 2020–2025 window
.venv\Scripts\python.exe backend\scripts\build_daily.py --force

# Export static frontend JSON after every local aggregate has the current format
.venv\Scripts\python.exe backend\scripts\build_compact.py

# Compare four countries, all 2020–2025, with raw DuckDB counts and legacy series totals
.venv\Scripts\python.exe backend\scripts\verify_daily.py --markdown
```

To continue after interruption, rerun `build_daily.py`; completed, unchanged files in the current aggregate format are skipped. `run_remaining_years.ps1` and `.bat` call this same builder and preserve its disk guard. Do not remove `data/processed/observations`, `data/processed/cell_shards`, or the original `data/processed/manifest.json` until the validation table is reviewed. Even after a passing validation, this project does not delete those folders automatically.
