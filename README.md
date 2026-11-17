# FIREWATCH

FIREWATCH is a country-level fire activity explorer built using NASA FIRMS satellite observations. It brings together historical MODIS and VIIRS data through interactive daily calendars, geospatial visualization, data processing pipelines, and exploratory cross-sensor FRP calibration.

The active dashboard is a static React application backed by packaged JSON. It is a historical exploration tool, not a live monitoring service, validated fire prediction system, or early-warning system. The calibration and six-year analytics are preliminary experiments; see the methodology and limitations before interpreting them.

## Run the dashboard

Requirements: Node.js 20+ and npm.

~~~powershell
npm install
npm run start
~~~

Vite serves the dashboard locally, normally at http://localhost:5173. The active dashboard does not require the Python API or a NASA API key. Build with npm run build; serve the production build locally with npm run preview. The CARTO basemap needs an internet connection; the packaged dashboard data does not.

## What the active dashboard includes

- Country selection and year, sensor-family, and metric filters.
- Daily calendar and historical MODIS/VIIRS summaries for the packaged years 2020–2025.
- A global country-level activity map, CSV export, and calendar PNG export.
- Preliminary multi-year heatmap, typical activity ranges, percentile-based unusual-week flags, and fire-season estimates.
- Experimental country-level statistical calibration of weekly MODIS and VIIRS vegetation FRP.

The package includes MODIS Terra/Aqua, VIIRS Suomi-NPP, and VIIRS NOAA-20 Standard Processing country records. NOAA-21 country records and live FIRMS updates are not part of the active dashboard. The map uses country-level summary bubbles at observed-record centroids, not individual fire detections, fire perimeters, or administrative boundaries. Arbitrary area-of-interest drawing is not available.

## Architecture

- **Active frontend:** React, TypeScript, and Vite. The entry point renders the static dashboard and loads JSON from frontend/public/data.
- **Runtime data:** countries.json, map_activity.json, per-country series JSON, calibration JSON, and methods_validation.json. The dashboard does not call NASA at runtime.
- **Current compact processing path:** backend/scripts/build_daily.py aggregates extracted FIRMS CSVs with DuckDB to daily Parquet; backend/scripts/build_compact.py exports the main static JSON; backend/scripts/run_harmonize.py produces the separate preliminary calibration and seasonal analytics JSON.
- **Optional FastAPI prototype:** backend/app contains API routes for FIRMS requests, CSV preview validation, local archive queries, and a comparison-only spatial query. An older API-driven frontend exists in frontend/src/ui/App.tsx but is not mounted by the default entry point. It is not needed to run the active dashboard.

Original source CSVs, credentials, and local Parquet files are not included in the repository. In the current development checkout, the extracted raw CSV folder is absent. Restore the matching FIRMS country CSVs before attempting a full raw-data rebuild or raw-count revalidation. Without those inputs, rebuilding the compact JSON may not reproduce source-file coverage indicators.

## Data provenance and interpretation

The packaged snapshot was generated from NASA FIRMS Standard Processing country CSVs. Its generated metadata reports 3,859 processed source files, 265,659,156 detection records, 236 country labels, and coverage years 2020–2025. These are detection-record totals, not counts of unique fires. Raw calendar summaries include all detection types. Calibration analytics use vegetation-only records where type equals 0.

FRP is reported in megawatts. MODIS and VIIRS products differ in pixel footprint, detection behavior, FRP retrieval, platforms, and observation opportunities. Their values are not automatically equivalent. Missing calendar records do not establish that a satellite observed a location or that no fire occurred.

The calibration fits a Theil–Sen log-log relationship between weekly country-level VIIRS and MODIS vegetation FRP, using a 5 MW qualifying threshold and a 40-week minimum for country-specific fits. The generated median holdout MdAPE is about 40.9%; R² is computed in log-FRP space. This internal leave-one-year-out evaluation is not independent scientific validation. The operating-week rule does not establish country-specific observation opportunity. The result is exploratory statistical calibration, not a physical retrieval correction or validated harmonized observation product.

The multi-year, typical-range, unusual-week, and fire-season displays are preliminary and based on only six packaged years. For details, see [Methodology](docs/METHODOLOGY.md), [Harmonization](docs/HARMONIZATION.md), [Data and coverage](docs/DATA.md), [Limitations](docs/LIMITATIONS.md), and [Validation record](docs/VALIDATION.md).

Official references: [NASA FIRMS](https://www.earthdata.nasa.gov/data/tools/firms), [MODIS active-fire user guide](https://cdn.earthdata.nasa.gov/conduit/upload/10575/MODIS_C6_Fire_User_Guide_B.pdf), [VIIRS active-fire user guide](https://viirsland.gsfc.nasa.gov/PDF/VIIRS_activefire_User_Guide.pdf), and [FIRMS citation guidance](https://www.earthdata.nasa.gov/data/projects/lance#ed-firms-citation).

## Optional local API

The API is a separate prototype and is not used by the active dashboard. Start it from the project root with:

~~~powershell
npm run api
~~~

It serves at http://localhost:8000. NASA FIRMS endpoints require a server-side FIRMS_MAP_KEY; do not put a key in frontend code. See [API documentation](docs/API.md). The default frontend entry point remains static even if the API is running.

## Checks and validation

Run npm run check for type checking, linting, frontend tests, production build, and backend checks. Backend pytest uses a temporary directory outside the project as configured in backend/pyproject.toml. Software checks do not establish scientific validity. Historical run details and the scope of the raw-count comparison are documented in [Validation](docs/VALIDATION.md).

The validation record documents 48 exact raw-row/daily-count comparisons for India, Australia, Brazil, and Bahrain across 2020–2025. The raw files used for those comparisons are not present in the current checkout, so that verification cannot currently be repeated here.

## AI assistance

Code was developed with AI assistance; the documented data-processing count validation was performed against original FIRMS files. This statement concerns the recorded historical validation run, not an independent scientific review of the calibration.

## Largest tracked files

The last repository inventory found no tracked file over 50 MB. The following were the ten largest tracked files at that inventory:

| File | Size |
|---|---:|
| package-lock.json | 0.17 MB |
| backend/scripts/build_processed.py | 0.04 MB |
| frontend/src/ui/App.tsx | 0.03 MB |
| frontend/src/styles.css | 0.02 MB |
| backend/tests/test_analytics_api.py | 0.01 MB |
| frontend/src/ui/ProcessedComparison.tsx | 0.01 MB |
| docs/DATA_ENGINE.md | 0.01 MB |
| frontend/src/ui/MapView.tsx | 0.01 MB |
| backend/tests/test_processing.py | 0.01 MB |
| backend/app/local_archive.py | 0.01 MB |
