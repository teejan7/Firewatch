# FIREWATCH

FIREWATCH is a static, country-level dashboard for exploring NASA FIRMS MODIS and VIIRS active-fire records over time. It includes a global activity map, a daily activity calendar, source coverage indicators, CSV export, and a preliminary multi-year seasonal view.

## Run locally

Requirements: Node.js 20+ and npm. The static dashboard does not need the Python API or a NASA key at runtime.

```powershell
npm install
npm run start
```

Vite opens the dashboard in your browser. For a production build, run `npm run build`; to view that build locally, run `npm run preview`.

## Data provenance and processing

The packaged data comes from NASA FIRMS Standard Processing (SP) MODIS and VIIRS country CSV files available locally to this project. The raw source CSVs are not included in the repository. Their source product, platform, country, acquisition date and available processing-version metadata are retained in generated outputs.

`backend/scripts/build_daily.py` streams local CSV input to compact daily Parquet aggregates. `backend/scripts/build_compact.py` generates the static JSON used by the dashboard. `backend/scripts/run_harmonize.py` creates country-level weekly calibration and seasonal analytics JSON under `frontend/public/data/harmonized/` and `frontend/public/data/methods_validation.json`.

## Calibration method and limitations

The selected statistical method is implemented in [backend/scripts/harmonize_core.py](backend/scripts/harmonize_core.py). It fits MODIS weekly vegetation FRP from VIIRS using a Theil-Sen log-log model, leave-one-year-out validation, confidence rules, and a deterministic global fallback. The app makes the calibration visible as preliminary statistical cross-sensor calibration. It is not a physical retrieval correction and does not establish comparable satellite observation opportunity. Weeks with no fire in either sensor are excluded from fitting.

The multi-year chart and fire-season line are labelled **PRELIMINARY (6-year baseline)**. The analysis is country-level. The current packaged span is 2020–2025; NOAA-21 is not included. Platform mix and local archive coverage vary by country and year, and missing dates do not mean zero fire activity. The method, validation metrics, assumptions and data limits are recorded in [frontend/public/data/methods_validation.json](frontend/public/data/methods_validation.json), [docs/METHODOLOGY.md](docs/METHODOLOGY.md), [docs/VALIDATION.md](docs/VALIDATION.md), and [docs/LIMITATIONS.md](docs/LIMITATIONS.md).

Official source references: [NASA FIRMS](https://www.earthdata.nasa.gov/data/tools/firms), [MODIS active-fire user guide](https://cdn.earthdata.nasa.gov/conduit/upload/10575/MODIS_C6_Fire_User_Guide_B.pdf), [VIIRS active-fire user guide](https://viirsland.gsfc.nasa.gov/PDF/VIIRS_activefire_User_Guide.pdf), [FIRMS citation guidance](https://www.earthdata.nasa.gov/data/projects/lance#ed-firms-citation).

## Verification

Run the project checks with:

```powershell
npm run check
```

Backend pytest uses a temporary directory outside the project (configured in `backend/pyproject.toml`). Data pipeline validation is documented in [docs/VALIDATION.md](docs/VALIDATION.md). Software tests do not replace scientific review.

## Largest tracked files

Checked against the files currently tracked by Git. All are below 50 MB.

| File | Size |
|---|---:|
| `package-lock.json` | 0.17 MB |
| `backend/scripts/build_processed.py` | 0.04 MB |
| `frontend/src/ui/App.tsx` | 0.03 MB |
| `frontend/src/styles.css` | 0.02 MB |
| `backend/tests/test_analytics_api.py` | 0.01 MB |
| `frontend/src/ui/ProcessedComparison.tsx` | 0.01 MB |
| `docs/DATA_ENGINE.md` | 0.01 MB |
| `frontend/src/ui/MapView.tsx` | 0.01 MB |
| `backend/tests/test_processing.py` | 0.01 MB |
| `backend/app/local_archive.py` | 0.01 MB |

Code was developed with AI assistance; data processing was verified against the original FIRMS files.
