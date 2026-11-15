# FIREWATCH

FIREWATCH is a responsive exploration dashboard for the NASA Space Apps Challenge “Harmonization of MODIS and VIIRS Hot Spots.” It starts with a deterministic **Simulated demo data** fixture, and can now load current NASA FIRMS near-real-time CSV feeds when a server-side FIRMS MAP_KEY is configured. Simulated values are invented interface fixtures and are never presented as NASA observations.

## Run locally

Requirements: Node.js 20+, npm, and Python 3.10+.

```powershell
# Terminal 1: API (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
python -m uvicorn app.main:app --reload --app-dir backend

# Terminal 2: frontend
npm install
npm run dev
```

To enable NASA requests, create a `.env` file in the project root (`C:\Users\teeja\program\nasa`) with this one line:

```text
FIRMS_MAP_KEY=paste-your-free-key-here
```

`.env` is git-ignored. Never paste the key into chat or frontend code. Restart the backend after creating or editing `.env`. Without the key, the API, demo dashboard, and local CSV upload still work and live controls explain what is missing. Request the key from the [NASA FIRMS MAP_KEY page](https://firms.modaps.eosdis.nasa.gov/api/map_key). Open the Vite URL printed in the terminal. API docs are at `http://localhost:8000/docs`. Set `VITE_API_URL` to use another API origin; the local default is `http://localhost:8000`.

## What the live FIRMS connection loads

The **NASA FIRMS LIVE** control fetches a 1, 3, or 5 day window for the selected bounding area using one of these official API sources:

- `VIIRS_NOAA21_NRT`
- `VIIRS_NOAA20_NRT`
- `MODIS_NRT`

The backend queries NASA FIRMS' area CSV endpoint, caps a response at 10 MB, validates the returned records, and includes the dataset identifier plus original CSV fields in the response/export. The MAP_KEY stays on the backend. Worldwide requests can be large; use an area and shorter window when possible. FIRMS documents a MAP_KEY transaction limit and asks users to request a key for API access.

The **NASA FIRMS ARCHIVE** control queries a selected 1, 3, or 5 day window from a chosen date using a Standard Processing feed: `MODIS_SP`, `VIIRS_NOAA20_SP`, `VIIRS_NOAA21_SP`, or historical `VIIRS_SNPP_SP`. This supports bounded inspection of the archive; broad multi-year analysis should use downloaded FIRMS files in manageable segments. Do not combine NRT and SP records without accounting for processing stream, latency, version, and possible duplicate detections.

## Architecture

- `frontend/`: React, TypeScript, Vite, MapLibre GL JS, and Recharts. Filters drive the map, activity calendar, selected-record counts, and CSV export.
- `backend/app/firms.py`: bounded NASA FIRMS API client. It uses an allowlist of current operational NRT products and fixed area extents.
- `backend/app/validation.py`: strict FIRMS CSV schema validation, coordinate/date checks, and retention of original fields.
- `backend/app/local_archive.py`: discovers available country/year/source CSVs and reads bounded windows while keeping MODIS and each VIIRS platform separately tagged.
- `backend/scripts/build_processed.py`: incrementally validates FIRMS CSVs and writes resumable normalized Parquet partitions and quality manifests under `data/processed/`.
- `backend/app/main.py`: FastAPI health, live FIRMS, and CSV upload endpoints.
- `backend/app/analytics_api.py`: bounded local Parquet calendar queries, AOI validation, coverage reporting, and explicit insufficient-baseline responses for unvalidated historical analyses.

The demo dataset lives in `frontend/src/data/demo.ts`; it is static and explicitly marked as simulated. It is independent of NASA data loading.

### Load the downloaded country archives

The current local archive endpoints discover extracted MODIS (2000–2025), VIIRS S-NPP (2012–2025), and VIIRS NOAA-20 (2018–2025) country CSVs. NOAA-21 CSVs are also present, but their large global `fire_archive_*` and `fire_nrt_*` files require processing before the local country query UI can use them. The archive folders preserve each ZIP's internal directories:

```text
data/raw/archives/MODIS_SP/modis_2025_all_countries.zip
data/raw/extracted/MODIS_SP/modis/2025/modis_2025_India.csv
data/raw/archives/VIIRS_SNPP_SP/viirs-snpp_2025_all_countries.zip
data/raw/extracted/VIIRS_SNPP_SP/viirs-snpp/2025/viirs-snpp_2025_India.csv
```

Each downloaded ZIP is stored under `data/raw/archives/<SOURCE>/`. In Windows **Extract All**, choose the matching source directory itself as the destination (for example, `data/raw/extracted/MODIS_SP`); the ZIP creates `modis/<year>/` beneath it. Do not extract into a year folder, or the internal folders will be duplicated. The same pattern applies to VIIRS S-NPP (`viirs-snpp/<year>/`) and NOAA-20 (`viirs-jpss1/<year>/`). Start the backend and select an archive year, country, product, and date window in **LOCAL GLOBAL ARCHIVE**. The map query is bounded to 31 days; the activity calendar separately streams/caches full-month daily row counts from the selected country files. Both are local and require no MAP_KEY. Counts remain sensor/product-specific and are not harmonized. Data stays under `data/raw/`, which is git-ignored; do not commit large source files or `.env`. A submitted source-code copy will need the recipient to obtain/extract NASA files separately.

The browser upload preview remains limited to 10 MB. The existing raw-CSV local query path has a 150 MB per-country-file limit; the DuckDB processor does not impose that arbitrary file limit. See [docs/DATA_ENGINE.md](docs/DATA_ENGINE.md) for processing. The processed Parquet comparison utility is an exploratory backend module and does not replace the dashboard's source-specific live/archive views. The API exposes `/api/calendar`, `/api/data-quality`, `/api/climatology`, `/api/anomalies`, and `/api/critical-periods`; the last three explicitly return insufficient-baseline until documented validation and coverage exist. See [docs/API.md](docs/API.md). NOAA-21 global CSVs are not exposed to the local country-archive selectors, but processed NOAA-21 rows are included in Parquet calendar queries when present.

The **Harmonization Explorer** is the **Compare** section below the activity calendar. It queries `/api/calendar` independently of the map's currently selected record source. It supports a date interval of up to 366 days, an optional WGS84 bounding box, SP or NRT, and optional satellite-platform filters. Draw an AOI box on the map by clicking **Draw AOI box** and then two map corners; the bbox is copied into the comparison panel. Its calendar and CSV export describe gridded detected cell-days and per-platform source metrics. No-detection dates remain marked as unknown coverage; they are not filled with zeros. The map and overview retain their own visible source label, so the panel's aggregate metric is not presented as map points. The **Data Explorer** searches and paginates the currently selected point records and exports only matching rows; CSV formula-like cells are prefixed for spreadsheet safety. The overview calendar has month navigation, and selecting a day updates the overview's date filter. The date range filters whichever dataset is currently loaded; it does not itself request new NASA records.

## Current data transition and provenance

NASA FIRMS reported that new Suomi NPP active-fire data stopped on **2 November 2026**. FIRMS recommends NOAA-20 and NOAA-21 VIIRS for continuing VIIRS feeds. Historical Suomi NPP records remain available. MODIS Terra/Aqua remains available, with a coarser nominal fire product resolution and a longer-term continuity caveat described by NASA. FIREWATCH's live selector therefore defaults to NOAA-21 and offers NOAA-20 and MODIS; it does not offer Suomi NPP as a current feed.

Every loaded result keeps its source dataset, instrument, platform/satellite, version and other raw CSV columns. The visible status identifies simulated, user-uploaded, or NASA FIRMS API records. Exports include canonical view columns plus `original_*` columns for source fields.

NASA links:

- [FIRMS data and tools](https://www.earthdata.nasa.gov/data/tools/firms)
- [Official Space Apps challenge brief](https://www.spaceappschallenge.org/2026/challenges/modis-and-viirs-hot-spots/)
- [FIRMS API area endpoint and supported sources](https://firms.modaps.eosdis.nasa.gov/api/area)
- [FIRMS MAP_KEY setup](https://firms.modaps.eosdis.nasa.gov/api/map_key)
- [FIRMS transition guidance for Suomi NPP users](https://www.earthdata.nasa.gov/news/blog/transitioning-from-suomi-npp-viirs-omps-what-firms-users-need-know)
- [NASA LANCE transition guidance](https://www.earthdata.nasa.gov/news/blog/transitioning-from-suomi-npp-noaa-20-noaa-21-what-lance-users-need-know)

## Scientific limits and harmonization

The live records are operational NASA FIRMS source data, but that does not make the dashboard's cross-sensor counts scientifically harmonized. Map/calendar/chart summaries are descriptive counts of the rows returned for the active source and filters. They are not anomaly scores, fire radiative power totals, calibrated trends, or sensor-equivalence results. MODIS and VIIRS have different instruments, nominal pixel sizes, detection characteristics, overpass schedules, confidence schemes, and processing streams. A direct count comparison can therefore mislead.

An exploratory common-grid comparison utility is documented in [docs/HARMONIZATION.md](docs/HARMONIZATION.md). It reports detected cell-days and same-cell/day overlap while keeping sensor/platform/processing stream fields separate; it does **not** calibrate or harmonize detections. It always reports `insufficient_calibration` until a defensible method is developed and validated against documented inputs. See [docs/LIMITATIONS.md](docs/LIMITATIONS.md) before interpreting archive coverage or comparison output. No anomalies or calibrated trends are presented.

## Checks

```bash
npm test
npm run build
pip install -r backend/requirements.txt
python -m pytest backend/tests
```
