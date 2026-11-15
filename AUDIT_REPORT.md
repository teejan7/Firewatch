# FIREWATCH Read-Only Audit

**Audit date:** 15 November 2026 (Asia/Kolkata).  
**Scope:** Local files and localhost HTTP only. No NASA API calls were made. No `.env` values or credential contents are included. The audit-launched API process was stopped at the end.

## 1. ENVIRONMENT

### Runtime

| Item | Observed value | Evidence |
|---|---|---|
| OS | Microsoft Windows 10.0.22621 | PowerShell `[System.Runtime.InteropServices.RuntimeInformation]::OSDescription` and `[System.Environment]::OSVersion.VersionString` output |
| Python | 3.12.10 | `python --version` |
| Node.js | v24.11.1 | `node --version` |
| npm | 11.8.0 | `npm --version` |
| DuckDB | 2.0.0 in project `.venv` | `.venv\Scripts\python.exe -c "import importlib.metadata as m; print(m.version('duckdb'))"` |
| pandas | Not installed in project `.venv` | `importlib.metadata` package check |
| pyarrow | Not installed in project `.venv` | `importlib.metadata` package check |
| TypeScript / Vite / Vitest | 5.8.3 / 6.4.5 / 3.2.7 | Local executable version output |

### Dependencies

Backend list from [backend/requirements.txt](backend/requirements.txt):

```text
fastapi>=0.115,<1
uvicorn[standard]>=0.30,<1
python-multipart>=0.0.9,<1
python-dotenv>=1.0,<2
pytest>=8,<9
httpx>=0.27,<1
duckdb>=1.2,<3
```

Frontend dependencies from [frontend/package.json](frontend/package.json):

```text
dependencies:
  maplibre-gl ^5.6.0
  react ^19.1.0
  react-dom ^19.1.0
  recharts ^2.15.4
  lucide-react ^0.468.0
devDependencies:
  @types/react ^19.1.0
  @types/react-dom ^19.1.0
  @vitejs/plugin-react ^4.6.0
  typescript ~5.8.3
  vite ^6.3.5
  vitest ^3.2.4
  jsdom ^26.1.0
  @testing-library/react ^16.3.0
  @testing-library/jest-dom ^6.6.4
```

Root scripts are in [package.json](package.json:6). The current `dev` script points to `node scripts/dev.mjs`; that launcher starts the API and Vite on 127.0.0.1 ports 8000 and 5173 ([scripts/dev.mjs](scripts/dev.mjs:33)). The launcher was not run as part of this read-only audit; its behavior is **ASSUMED from source**. The documented two-terminal commands remain in [README.md](README.md:7).

### Git and addresses

- **No Git repository is present at the project root.** `git rev-parse --show-toplevel`, `git status --short`, and `git log -15 --oneline` each returned `fatal: not a git repository (or any of the parent directories): .git`. There is therefore no commit history to list.
- Frontend API base is exactly `const api = import.meta.env.VITE_API_URL || 'http://localhost:8000';` ([frontend/src/ui/App.tsx](frontend/src/ui/App.tsx:11)). Override variable: `VITE_API_URL`.
- Vite's normal workspace script is `vite --host 0.0.0.0`; Vite's default port is 5173 ([frontend/package.json](frontend/package.json:6)). Backend default command in README is `python -m uvicorn app.main:app --reload --app-dir backend`, with port 8000 by Uvicorn default ([README.md](README.md:10)). The added launcher explicitly sets both ports ([scripts/dev.mjs](scripts/dev.mjs:32)).

## 2. RUNNING STATE

### State at audit start

- `curl.exe -i --max-time 5 http://localhost:8000/api/health` failed with `curl: (7) Failed to connect to localhost port 8000`; the API was not listening when first checked.
- `curl.exe -i --max-time 3 http://localhost:5173/` failed with `curl: (7) Failed to connect to localhost port 5173`; the frontend dev server was not listening when checked.
- `Get-CimInstance Win32_Process` returned `Access denied`; process enumeration by command line was unavailable. Port probes and curl results above establish the observed listener state.

### Audit-only API run

For localhost endpoint checks only, the backend was temporarily started with:

```text
.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Observed process ID 6056, start time **15-11-2026 11:13:23 local time**, port 8000. It was stopped after the checks. No frontend server was started. No NASA host was contacted.

Health response after starting the API (`curl.exe -i http://localhost:8000/api/health`):

```text
HTTP/1.1 200 OK
{"status":"ok","data_status":"Processed local FIRMS archives","local_analytics_available":true,"firms_api_configured":true,"harmonization":"comparison only; calibration insufficient"}
```

This reports whether a MAP_KEY is configured, not its value. The key was not printed.

`curl.exe -sS http://localhost:8000/openapi.json` route extraction returned:

```text
GET /api/health
GET /api/firms/latest
GET /api/firms/archive
POST /api/ingest/firms
GET /api/local-archive/countries
GET /api/local-archive/catalog
GET /api/local-archive/records
GET /api/local-archive/calendar
GET /api/data-quality
GET /api/calendar
GET /api/climatology
GET /api/anomalies
GET /api/critical-periods
```

### Captured backend console output

The audit-launched Uvicorn console logged the following requests and startup; no traceback appeared in captured output. There were fewer than 80 log lines in the session, so this is the complete captured request-log excerpt (the API was stopped after it):

```text
INFO: Started server process [6056]
INFO: Waiting for application startup.
INFO: Application startup complete.
INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
GET /api/health 200
GET /openapi.json 200
OPTIONS /api/calendar 200
GET /api/health 200
GET /api/local-archive/catalog?year=2025 200
GET /api/local-archive/catalog?year=2023 200
GET /api/local-archive/countries?year=2025 200
GET /api/local-archive/records?country=India&year=2025&start_date=2025-01-01&end_date=2025-01-05 200
GET /api/local-archive/records?country=India&year=2025&start_date=2025-01-05&end_date=2025-01-01 422
GET /api/local-archive/records?country=India&year=2023&start_date=2023-01-01&end_date=2023-01-05 200
GET /api/local-archive/calendar?country=India&year=2025&month=1 200
GET /api/local-archive/calendar?country=India&year=2023&month=1 200
GET /api/data-quality 200
GET /api/calendar?start_date=2025-01-01&end_date=2025-01-22&product_type=NRT 200
GET /api/calendar?start_date=2025-01-01&end_date=2025-01-05&bbox=68,6,98,36&product_type=SP 200
GET /api/calendar?start_date=2025-01-01&end_date=2025-01-03&product_type=SP 200
GET /api/calendar?start_date=2025-01-05&end_date=2025-01-01&product_type=SP 422
GET /api/calendar?start_date=2025-01-01&end_date=2025-01-05&bbox=-179,-89,-178,-88&product_type=SP 200
GET /api/calendar?start_date=2023-01-01&end_date=2023-01-05&bbox=68,6,98,36&product_type=SP 200
GET /api/climatology?start_date=2025-01-01&end_date=2025-01-05 200
GET /api/anomalies?start_date=2025-01-01&end_date=2025-01-05 200
GET /api/critical-periods?start_date=2025-01-01&end_date=2025-01-05 200
GET /api/climatology?start_date=2025-01-05&end_date=2025-01-01 422
GET /api/calendar?start_date=2025-01-01&end_date=2025-01-22&product_type=NRT 200
GET /api/calendar?start_date=2025-01-01&end_date=2025-01-22&product_type=SP 200
GET /api/calendar?start_date=2025-01-01&end_date=2025-01-05&bbox=-179,-89,-178,-88&product_type=SP 200
GET /api/calendar?start_date=2023-01-01&end_date=2023-01-05&bbox=68,6,98,36&product_type=SP 200
GET /api/calendar?start_date=2025-01-01&end_date=2025-01-05&bbox=68,6,98,36&product_type=SP 200
GET /api/calendar?start_date=2025-02-01&end_date=2025-02-28&product_type=SP 200
GET /api/local-archive/records?country=India&year=2025&start_date=2025-01-01&end_date=2025-01-05&products=VIIRS_NOAA21_SP 422
GET /api/local-archive/records?country=Aland_Islands&year=2025&start_date=2025-01-01&end_date=2025-01-05 200
GET /api/local-archive/calendar?country=Aland_Islands&year=2025&month=1 200
GET /api/local-archive/records?country=India&year=2026&start_date=2026-01-01&end_date=2026-01-05&products=VIIRS_NOAA21_SP 422
GET /api/climatology?start_date=2025-01-01&end_date=2025-01-05&bbox=68,6,98,36 200
GET /api/climatology?start_date=2025-01-01&end_date=2025-01-05 200
GET /api/climatology?start_date=2025-01-05&end_date=2025-01-01 422
GET /api/climatology?start_date=2025-01-01&end_date=2025-01-05&bbox=-179,-89,-178,-88 200
GET /api/climatology?start_date=2023-01-01&end_date=2023-01-05&bbox=68,6,98,36 200
GET /api/anomalies?start_date=2025-01-01&end_date=2025-01-05&bbox=68,6,98,36 200
GET /api/anomalies?start_date=2025-01-01&end_date=2025-01-05 200
GET /api/anomalies?start_date=2025-01-05&end_date=2025-01-01 422
GET /api/anomalies?start_date=2025-01-01&end_date=2025-01-05&bbox=-179,-89,-178,-88 200
GET /api/anomalies?start_date=2023-01-01&end_date=2023-01-05&bbox=68,6,98,36 200
GET /api/critical-periods?start_date=2025-01-01&end_date=2025-01-05&bbox=68,6,98,36 200
GET /api/critical-periods?start_date=2025-01-01&end_date=2025-01-05 200
GET /api/critical-periods?start_date=2025-01-05&end_date=2025-01-01 422
GET /api/critical-periods?start_date=2025-01-01&end_date=2025-01-05&bbox=-179,-89,-178,-88 200
GET /api/critical-periods?start_date=2023-01-01&end_date=2023-01-05&bbox=68,6,98,36 200
GET /openapi.json 200
GET /api/health 200
```

Frontend console output: **not available** because no frontend dev server was running at audit time. `curl` to port 5173 failed as above.

## 3. DATA INVENTORY

### Extracted and processed storage

Counts are recursive Windows filesystem counts from `Get-ChildItem -Recurse -File`; sizes are actual byte totals, displayed in MiB (1 MiB = 1,048,576 bytes).

```text
data/raw/extracted                         10,154 files  49,472,632,913 bytes  47,180.78 MiB
  MODIS_SP                                  5,302 files                   8,308.04 MiB
  VIIRS_NOAA20_SP                           1,766 files                  12,024.63 MiB
  VIIRS_NOAA21_SP                               9 files                   5,720.88 MiB
  VIIRS_SNPP_SP                             3,077 files                  21,127.23 MiB

data/processed                             1,154 files   7,478,659,221 bytes   7,132.21 MiB
  observations                             1,150 files                   6,913.19 MiB
  archive_index.json                       present
  manifest.json                            present
  daily_cell.parquet                       present
  quality_report.json                      present
```

NOAA-21 extracted paths include `VIIRS_NOAA21_SP\viirs-jpss2\<year>\fire_archive_*.csv` and `fire_nrt_*.csv`. The largest listed CSV is 1,676.39 MiB. Counts and file sizes were measured with PowerShell; no source archive was changed.

### `daily_cell.parquet` profile

Read with project DuckDB using `DESCRIBE SELECT * FROM read_parquet(...)` and aggregate SELECTs.

| Column | Type |
|---|---|
| acq_date | DATE |
| lat_i | INTEGER |
| lon_i | INTEGER |
| sensor_family | VARCHAR |
| platform | VARCHAR |
| product_type | VARCHAR |
| daynight | VARCHAR |
| n_raw | BIGINT |
| n_dedup | BIGINT |
| frp_sum | DOUBLE |
| frp_max | DOUBLE |

Observed total: **24,755,782 rows**, dates **2023-01-01 through 2026-11-14**, two sensor families, five platforms, four calendar years. This is the processed subset, not full raw archive coverage.

| Family/platform | First date | Last date | Years represented |
|---|---|---|---|
| MODIS / Terra | 2023-01-01 | 2025-12-31 | 2023–2025 |
| MODIS / Aqua | 2023-01-01 | 2025-12-31 | 2023–2025 |
| VIIRS / S-NPP | 2023-01-01 | 2025-12-31 | 2023–2025 |
| VIIRS / NOAA-20 | 2023-01-01 | 2025-12-31 | 2023–2025 |
| VIIRS / NOAA-21 | 2023-03-01 | 2026-11-14 | 2023–2026 |

By product type, processed NRT contains NOAA-21 records only from **2026-08-01 to 2026-11-14** (1,300,459 deduplicated cell rows; 7,177,402 raw records). Processed SP is present for 2023–2025. These are database aggregates, not independently validated observation totals.

### Requested period checks

- India 2023-01-01 through 2023-01-05 local country endpoint: **200, 8,818 records**.
- India 2025-01-01 through 2025-01-05 local country endpoint: **200, 15,837 records**.
- Global processed SP, February 2025: **200, 28 dates and 404,642 detected cell-days**. This metric is grid occupancy, not fires.
- India January daily source-row calendar: 2023 and 2025 both returned 31 days; January 2025 had 31 active days in the local India archive. January 2023 also returned source rows (Jan 1 sample at 1,795 source rows).
- Global processed NRT for 2025-01-01 through 2025-01-22 returned **zero detection dates**. The processed NRT index starts 2026-08-01.
- `quality_report.json` reports **1,149 processed of 10,100 discovered files**, zero file failures, status `partial_local_archive` (11.38% by file count). `files_discovered` is the processor's scan count; 10,154 is the filesystem count.

## 4. API ENDPOINT TESTS

Tests were made against the temporary localhost backend only. Each result below records HTTP status, elapsed time, and the first response excerpt (maximum 300 characters). Responses were read locally; no live FIRMS endpoint was invoked.

### Catalog, countries, and local archive

| Request / case | Result |
|---|---|
| `GET /api/local-archive/catalog?year=2025` | 200 · 2.156s · `{"year":2025,"products":[{"id":"MODIS_SP"...` (catalog returns MODIS, S-NPP, NOAA-20 and NOAA-21 product identifiers) |
| `GET /api/local-archive/catalog?year=2023` | 200 · 2.137s · `{"year":2023,"products":[{"id":"MODIS_SP"...` |
| `GET /api/local-archive/countries?year=2025` | 200 · 2.110s · `{"year":2025,"countries":["Afghanistan","Aland_Islands"...` |
| Records: India 2025-01-01..05 | 200 · 14.903s · `{"count":15837,"records":[...` |
| Records: India 2025-01-05..01 (reversed) | 422 · 2.031s · `{"detail":"Start date must be on or before end date."}` |
| Records: India 2023-01-01..05 | 200 · 13.185s · `{"count":8818,"records":[...` |
| Records: Aland Islands 2025-01-01..05 (no detections) | 200 · 2.148s · `{"count":0,"records":[],"country":"Aland_Islands"...` |
| Records: India 2026 NOAA-21 SP country selection | 422 · 2.053s · `{"detail":"No FIRMS country CSV was found for 'India' in 2026 for the selected source(s)."}` |
| Records: India 2025 NOAA-21 SP country selection | 422 · 2.050s · `{"detail":"No FIRMS country CSV was found for 'India' in 2025 for the selected source(s)."}` |
| India local calendar, Jan 2025 | 200 · 11.853s · `{"country":"India","year":2025,"month":1,"products":["MODIS_SP","VIIRS_SNPP_SP","VIIRS_NOAA20_SP"],"days":[...]}` |
| India local calendar, Jan 2023 | 200 · 10.855s · `{"country":"India","year":2023,"month":1,"products":[...]...` |
| Aland Islands local calendar, Jan 2025 (no detections) | 200 · 2.045s · 31 days, 0 active days; body begins `{"country":"Aland_Islands","year":2025,"month":1,...` |

For local country endpoints, global/blank AOI and reversed date-window cases are **not applicable** to the calendar route (it accepts country/year/month only) and global AOI is **not applicable** to the records route (it accepts a named country and date window, not bbox). A 2023 date was exercised on both routes. A no-data result was verified for both local routes.

### Processed calendar / comparison route

The UI builds `start_date`, `end_date`, `product_type`; adds `bbox` only when nonblank and adds each selected platform as a repeated `platform` query parameter ([frontend/src/ui/ProcessedComparison.tsx](frontend/src/ui/ProcessedComparison.tsx:53)).

| Request / case | Result |
|---|---|
| Exact screenshot selection: `start_date=2025-01-01&end_date=2025-01-22&product_type=NRT` (blank AOI, no platforms) | 200 · 2.443s · first 300 chars begin `{"status":"comparison_only","method":"common-grid sensor comparison","method_version":"1.0.0","harmonized_index":null,"calibration_status":"insufficient_calibration"...`; parsed result had 0 dates and 0 cell-days |
| Same dates, SP, blank AOI (global) | 200 · 3.379s · 22 dates, 293,242 cell-days; Jan 1 union 11,961 (MODIS 2,891; VIIRS 11,665; overlap 2,595) |
| India bbox `68,6,98,36`, SP, Jan 1..5 2025 | 200 · 3.122s · 5 dates, 5,677 cell-days; Jan 1 916 cell-days |
| Blank bbox, global Jan 1..3 2025, SP | 200 · 3.099s · 3 dates; body begins `{"status":"comparison_only"...` |
| Reversed dates Jan 5..1 2025 | 422 · 2.049s · `{"detail":"start_date must be on or before end_date."}` |
| Ocean bbox `-179,-89,-178,-88`, Jan 1..5 2025 SP (no detections) | 200 · 2.935s · parsed result 0 dates / 0 cell-days |
| India bbox, Jan 1..5 2023 SP | 200 · 3.046s · 5 dates, 3,328 cell-days; Jan 1 601 cell-days |
| Global February 2025 SP | 200 · 3.439s · 28 dates, 404,642 cell-days |

The three historical-analysis endpoints were each tested with India bbox, blank/global AOI, reversed dates, a no-detection ocean bbox, and 2023 India dates. For each route the four ordered-date queries returned **200** with `status=insufficient_baseline`, `results=[]`, `sample_size=0`; each reversed-date query returned **422** with `start_date must be on or before end_date`. Per-call elapsed times ranged from **2.026s to 2.086s**. First-300-character sample: `{"status":"insufficient_baseline","analysis":"historical_climatology","start_date":"2025-01-01","end_date":"2025-01-05","results":[],"sample_size":0...`; analysis names are `historical_climatology`, `historical_anomalies`, and `critical_periods`.

### CORS and screenshot diagnosis

Request with `Origin: http://localhost:5173` returned:

```text
HTTP/1.1 200 OK
access-control-allow-origin: http://localhost:5173
vary: Origin
```

An OPTIONS preflight also returned 200 with `access-control-allow-methods: GET, POST, OPTIONS`. CORS did not block the tested origin. The screenshot's `Failed to fetch` is consistent with the observed API not listening at initial check. When the API was started, the exact NRT query in the screenshot returned HTTP 200 but an empty result because no NRT data is processed for January 2025. The frontend surfaces raw `fetch` failure text in its catch handler ([ProcessedComparison.tsx](frontend/src/ui/ProcessedComparison.tsx:62)).

## 5. FRONTEND LOGIC

### State and control behavior

| Control/state | Handler / source | API call or in-memory behavior | Validation |
|---|---|---|---|
| Main time range (`filters.start/end`) | `withDateBound` from date inputs; initial values at App lines 10, 21; filter at [filters.ts](frontend/src/lib/filters.ts:3) | In-memory filter on the currently loaded `records`; no API fetch | Current inputs call a helper that collapses a crossed range to the chosen date ([App.tsx](frontend/src/ui/App.tsx:186), [filters.ts](frontend/src/lib/filters.ts:6)). Helper unit tests passed before the later incomplete API-status edit; browser behavior not retested. |
| Main region and sensor family | App `filters.region/sensor`, lines 21 and 185–187 | In-memory filter; map, timeline, calendar, and data explorer use selected records | Region choices are fixed labels; sensor filter is MODIS/VIIRS family, not satellite platform. |
| Map AOI box | `comparisonBbox` App line 47; `MapView` two map clicks | Copies bbox into processed comparison state; no request until Query processed data is clicked ([MapView.tsx](frontend/src/ui/MapView.tsx:32), [App.tsx](frontend/src/ui/App.tsx:185)) | Backend validates WGS84 bbox; anti-meridian crossing unsupported. |
| Comparison dates, product stream, platforms | `ProcessedComparison` state lines 22–33 and handlers at lines 53–58, 90–93 | Query button calls `/api/calendar`; stream is SP/NRT; platform checkboxes append repeated `platform` values | Frontend permits at most 366 days; backend validates start <= end and product type. |
| Local archive year | `localYear`, App line 36 | Changes year and triggers `/api/local-archive/catalog?year=...` through effect ([App.tsx](frontend/src/ui/App.tsx:59)) | UI year list excludes 2026 although backend limit allows it (line 14 versus [local_archive.py](backend/app/local_archive.py:24)). |
| Local archive country/product/date | `localCountry/localSource/localStart/localEnd`, App lines 35–39 | Values are state only until **Load local records**, then `/api/local-archive/records`; month counts call `/api/local-archive/calendar` | Backend requires same year, start <= end, and date window shorter than 31 days (max 30 elapsed days; see local_archive.py:88–94). |
| NASA live source/days | `liveSource/liveDays`, App lines 26–28 | Selectors only change state; load button calls `/api/firms/latest` | API supports 1–5 days; live operation requires configured server key. Not tested against NASA. |
| NASA archive source/date/days | App lines 29–32 | Selectors only change state; load button calls `/api/firms/archive` | Requires start date and 1–5 days; live API not contacted. |
| Overview calendar month/day | `calendarMonth`, `moveCalendarMonth`, App lines 73–83 and 169–176 | Day click sets main date filters only. Month navigation sets the displayed interval; for loaded local archives it also calls monthly local-calendar API. | Main dates now cross-clamp; local archive month changes can request years absent from UI catalog. |
| Reset | App line 184 | Sets filters to fixed `initial`; does not change records or restore demo | Assumes data has dates in Oct 2026, so reset can empty an already loaded 2023/2025 dataset. |

### Status, empty states, and error handling

- `dataStatus` initializes to `Simulated demo data` and a note expressly says values are not NASA observations ([App.tsx](frontend/src/ui/App.tsx:23)). The map label is `DEMO MAP` only for that exact value; otherwise `DATA MAP` ([App.tsx](frontend/src/ui/App.tsx:185)); the notice also shows `dataStatus` and `dataNote` (line 183). Selected count is `selected.length`. A valid date window outside the loaded records therefore displays 0 records and “No records match these filters”; this is an empty selection, not a data-fetch operation.
- Error catches that replace/ignore the original error: App health check catch (line 56; state is not rendered and currently causes TypeScript unused-variable errors), local catalog catch (line 69; silently clears product/country choices), CSV/live/archive/local-record catches (lines 103, 116, 131, 163; set upload status), local calendar catch (line 144; displays a message), MapLibre constructor catch ([MapView.tsx](frontend/src/ui/MapView.tsx:16); sets map error state), comparison quality catch ([ProcessedComparison.tsx](frontend/src/ui/ProcessedComparison.tsx:43); silently sets coverage unknown), comparison query catch (line 62; displays browser's `Failed to fetch` verbatim). The backend-start state is not currently rendered in the sidebar.
- Initial demo filters are **2026-10-01 through 2026-10-31**, matching the mock data's October 2026 dates ([App.tsx](frontend/src/ui/App.tsx:10), [demo.ts](frontend/src/data/demo.ts:11)). `restoreDemo()` restores both records and those dates (App.tsx:166–167). The separate **Reset** only resets filters, not dataset.

## 6. HARMONIZATION WORKFLOW

### Current end-to-end operation

1. The Compare section starts with 2025-01-01..2025-01-31 and SP. User may choose dates, SP/NRT, optional platform(s), and bbox; map AOI drawing fills the bbox field ([ProcessedComparison.tsx](frontend/src/ui/ProcessedComparison.tsx:22), :53–58, :90–93; [MapView.tsx](frontend/src/ui/MapView.tsx:32)).
2. Clicking **Query processed data** sends `GET /api/calendar` with those parameters ([ProcessedComparison.tsx](frontend/src/ui/ProcessedComparison.tsx:53); [main.py](backend/app/main.py:184)). The route validates bbox and delegates to `get_calendar` ([main.py](backend/app/main.py:184–200); [analytics_api.py](backend/app/analytics_api.py:67–102)).
3. `get_calendar` reads `data/processed/daily_cell.parquet` and calls `query_common_grid_comparison` ([analytics_api.py](backend/app/analytics_api.py:78–102)). Each grid cell is 0.25° per side; index formulas and lower-left-edge convention are in [build_processed.py](backend/scripts/build_processed.py:334–352).
4. Processing first groups rows by UTC acquisition date, grid cell, sensor family, platform, SP/NRT, and day/night, recording `n_raw=COUNT(*)`, `n_dedup=1`, FRP sum/max ([build_processed.py](backend/scripts/build_processed.py:334–352)). Comparison filters `acq_date`, product type, optional day/night, bbox/polygon and platform ([harmonize.py](backend/app/harmonize.py:159–176)).
5. It returns platform-level detected cell-days and a cross-family union where one positive cell/date is counted once; same-cell/date detections from both families are reported as overlap ([harmonize.py](backend/app/harmonize.py:178–229)). No observation/no-fire rows are inferred.

### Scientific and processing conclusions

- **Calibration/correction: none.** Response has `harmonized_index: null`, `calibration_status: insufficient_calibration`, and explicit reason; see [harmonize.py](backend/app/harmonize.py:230–261). A common grid is a spatial grouping mechanism, not a harmonization correction.
- **Duplicates:** Exact duplicate source rows are counted in the processor manifest, not removed as a scientific event match. `n_dedup=1` represents cell presence for one date/sensor/platform/product/day-night group; `n_raw` counts rows. Cross-sensor overlaps remain separate source metrics, then are reported in the union.
- **Day/night:** Source label is retained and included in source-grid grouping; API can optionally filter `D` or `N` ([harmonize.py](backend/app/harmonize.py:143–144), :159–176, :334–342 in builder).
- **Dates/time:** Parquet `acq_date` is a `DATE`; code uses the source acquisition date and describes it as UTC. No timestamp/time-zone conversion appears in this query path; acquisition time remains part of source metadata in raw feeds.
- **NRT vs SP:** UI sends one `product_type`; SQL filters `product_type = ?` and backend rejects unsupported values or implicit combination ([harmonize.py](backend/app/harmonize.py:141–160)). The filter works in the tested endpoint. However, NRT for Jan 2025 returns empty because local processed NRT coverage starts in Aug 2026; UI permits selecting that incompatible period without an availability hint.

## 7. CONFIGURATION & SECURITY

- CORS is configured from `FIREWATCH_CORS_ORIGINS`, defaulting to `http://localhost:5173,http://127.0.0.1:5173`; wildcard entries are removed; middleware allows GET/POST/OPTIONS and Content-Type ([backend/app/main.py](backend/app/main.py:18–20)). Preflight and GET for `Origin: http://localhost:5173` both returned `Access-Control-Allow-Origin: http://localhost:5173`.
- API rate limiter caps at **120 requests per client per 60 seconds** ([backend/app/main.py](backend/app/main.py:25–40)).
- Upload reads at most 10,000,001 bytes and rejects above 10,000,000 bytes ([backend/app/main.py](backend/app/main.py:90–97)); FIRMS response cap is 10,000,000 bytes ([backend/app/firms.py](backend/app/firms.py:47–50)). Local country preview limit is 150,000,000 bytes and date-window limit is 31 elapsed days ([backend/app/local_archive.py](backend/app/local_archive.py:21–24, :88–113)).
- `.env` is loaded from project root ([backend/app/main.py](backend/app/main.py:15)). Key lookup/use is backend-only at [backend/app/firms.py](backend/app/firms.py:28–36); health reports only a configured boolean ([backend/app/main.py](backend/app/main.py:44–50)). The value was not printed or requested from NASA. `.env` is listed in [.gitignore](.gitignore:10); Git repository is absent, so actual Git exclusion could not be checked.
- There are no hard-coded `C:/Users/...` paths in runtime source from the searched paths. README does contain machine-specific `C:\Users\teeja\program\nasa` in its `.env` instructions ([README.md](README.md:17–27)). Hard-coded dates include demo defaults October 2026, comparison default January 2025, local archive default year/dates 2025, and local UI year list 2000–2025 ([App.tsx](frontend/src/ui/App.tsx:10, :14, :36–39; ProcessedComparison.tsx:22–23). Backend allows year 2026 ([local_archive.py](backend/app/local_archive.py:24)).
- CSV exports prefix formula-leading `=`, `+`, `-`, `@` cells ([frontend/src/lib/filters.ts](frontend/src/lib/filters.ts:24–27); comparison export in [ProcessedComparison.tsx](frontend/src/ui/ProcessedComparison.tsx:67–73)).

## 8. TESTS & QUALITY

| Check | Command/result |
|---|---|
| Backend tests | `..\.venv\Scripts\python.exe -m pytest -q` from `backend`: **29 passed, 1 warning** in 3.13s. Warning: Starlette TestClient/httpx deprecation. |
| Frontend tests, audit attempt | `npm test` from project workspace failed during Vite/esbuild config load with `Cannot read directory "../../..": Access is denied` / config path unresolved; tests did not start in this attempt. A pre-audit run before the incomplete health-status patch had 8 passing frontend tests; it is not a current-state verification. |
| Frontend type-check/build | `npm run build` failed at TypeScript: `src/ui/App.tsx(48,10): error TS6133: 'apiStatus' is declared but its value is never read.` and `(49,20): error TS6133: 'setApiRetry' is declared but its value is never read.` `tsc -b && vite build` stops before Vite build. |
| Lint | `npm run lint` returned `Missing script: "lint"`; no lint command is configured in root or frontend package scripts. |
| Browser/e2e | Not run. No frontend server was running and this audit was constrained to read-only project inspection/localhost checks. Browser behavior is **ASSUMED from code** where indicated. |

The previous successful production build (before the incomplete App health-state edit) emitted a MapLibre chunk of about 1.06 MB and Vite's >500 kB chunk warning. Current build cannot reach bundling because type-check fails.

## 9. KNOWN-ISSUE CHECKLIST

| Item | Status | Evidence / detail |
|---|---|---|
| Date pickers refetch or constrain to loaded data | **PARTIAL** | Main date picker only filters in-memory `records` ([filters.ts](frontend/src/lib/filters.ts:3)); helper now prevents reversed bounds, but dates are not constrained to data availability. Comparison is submitted separately. |
| Start date cannot be after end date | **FIXED IN SOURCE; BROWSER NOT RETESTED** | `withDateBound` collapses a crossed range to the chosen day ([filters.ts](frontend/src/lib/filters.ts:6–10); App.tsx:186); helper test exists at [filters.test.ts](frontend/src/lib/filters.test.ts:23–28). Screenshot showed pre-fix state. |
| NOAA-21 global files indexed and queryable | **PARTIAL** | NOAA-21 appears in processed Parquet for SP (2023–2025) and NRT (2026-08 onward), but selecting NOAA-21 in local country records returns 422 because the downloaded NOAA-21 CSVs are global, not country-named. See API test and [local_archive.py](backend/app/local_archive.py:36–59). |
| Files above 150 MB now queryable | **PARTIAL** | DuckDB batch processor scans extracted CSVs and processed Parquet contains NOAA-21 metrics; raw local country preview still rejects any selected country CSV above 150,000,000 bytes ([local_archive.py](backend/app/local_archive.py:21, :111–113)). The largest raw file is 1,676.39 MiB; global NOAA-21 is not a country endpoint input. |
| Calendar month navigation works; years include 2026 | **PARTIAL** | Month buttons update interval and query local month counts when dataStatus is local ([App.tsx](frontend/src/ui/App.tsx:169–176)); year options are 2000–2025, so 2026 is missing (line 14). Browser interaction not retested. |
| Platform-level filter Terra/Aqua/S-NPP/NOAA-20/NOAA-21 | **FIXED IN COMPARISON VIEW** | Checkboxes in `ProcessedComparison.tsx` lines 93–95; repeated query params; backend validates platform allowlist ([harmonize.py](backend/app/harmonize.py:144–146, :170–176)). Overview map only filters MODIS/VIIRS families. |
| Map label reflects real vs simulated | **FIXED** | `DEMO MAP` for exact simulated status; otherwise `DATA MAP`; banner shows detailed status/note ([App.tsx](frontend/src/ui/App.tsx:183, :185)). |
| CORS restricted; CSV formula injection protected | **FIXED** | Restricted origin configuration and live CORS header verified ([main.py](backend/app/main.py:18–20)); formula-prefix code in filters and comparison export cited above. |
| README matches actual folders | **PARTIAL** | Main MODIS/S-NPP/NOAA-20 patterns match README examples (README.md:55–64). README acknowledges NOAA-21 global files, but catalog advertises NOAA-21 as a country product and country query fails. README still describes two-terminal startup while root `npm run dev` now points to an unverified combined launcher. |

## 10. REPRODUCTION OF REPORTED BUGS

### (a) Selecting a date shows “No records match these filters”

**Reproduced from source/data:** demo points are assigned dates in October 2026 ([frontend/src/data/demo.ts](frontend/src/data/demo.ts:11)); the screenshot selection was February 2025. `filterRecords` applies date bounds to current in-memory records ([frontend/src/lib/filters.ts](frontend/src/lib/filters.ts:3)), so selection count becomes zero and MapView shows its empty message ([frontend/src/ui/MapView.tsx](frontend/src/ui/MapView.tsx:52)). To see archive data, a local/API dataset must first be loaded. A zero count in an unselected period does not mean no fires occurred.

### (b) “Failed to fetch” in Harmonization Explorer

**Root cause observed:** at audit start port 8000 refused connections. CORS was subsequently verified working for the configured frontend origin. With the API running, the exact screenshot request (Jan 1–22 2025, NRT, blank AOI) returned **200 with an empty `daily_union`** because processed NRT dates start in August 2026. Therefore there are two distinct states: stopped API produces browser `Failed to fetch`; started API plus historical NRT produces no results. The UI catch displays the raw fetch message ([ProcessedComparison.tsx](frontend/src/ui/ProcessedComparison.tsx:57–63)).

### (c) “0 active days shown in January 2023”

**Root cause reproduced:** the calendar uses selected in-memory rows unless `dataStatus` is a local archive and the corresponding full-month API result is loaded ([App.tsx](frontend/src/ui/App.tsx:81–83)). Default demo records are October 2026, so January 2023 shows 0 for the demo selection. Local January 2023 India queries return real source rows (8,818 map rows over Jan 1–5; monthly calendar endpoint 200). The screenshot message is not a claim about global fire absence.

### (d) Time range showing 04-02-2025 to 02-02-2025

The screenshot reflects the earlier state where each date input changed only one endpoint, without ordering validation (historical screenshot/source behavior). Current source now routes both inputs through `withDateBound`, which collapses a crossed interval to the selected date ([App.tsx](frontend/src/ui/App.tsx:186); [filters.ts](frontend/src/lib/filters.ts:6–10)). Unit test covers both crossing directions ([filters.test.ts](frontend/src/lib/filters.test.ts:23–28)). **ASSUMED:** actual browser interaction after that code change was not re-run in this audit.

## TOP 10 PROBLEMS

1. **Frontend production build is currently blocked.** `App.tsx:48–49` declares `apiStatus` and `setApiRetry` but does not render/use them. TypeScript 5.8.3 fails with TS6133. **Fix:** complete the backend-status UI/retry flow or remove the unfinished state/effect.
2. **App shows no backend availability guidance and the screenshot's API was stopped.** `App.tsx:56` catches health errors into unused state; `ProcessedComparison.tsx:43,62` hides coverage failure and exposes generic `Failed to fetch`. **Fix:** finish visible health state, provide a retry/start instruction, and make all API-backed controls clearly unavailable while offline.
3. **Historical NRT selection silently yields an empty comparison.** January 2025 NRT returned HTTP 200 with zero dates; indexed NRT is NOAA-21 2026-08 to 2026-11. UI permits it (`ProcessedComparison.tsx:89–93`). **Fix:** show per-product date availability or default to SP for historical periods.
4. **Reset can empty non-demo datasets.** `App.tsx:184` resets filters to Oct 2026 but leaves loaded records untouched. **Fix:** reset to the selected dataset's date extent, or make reset explicitly restore demo data.
5. **NOAA-21 country selector advertises unsupported global files.** `available_products` sees any year CSV, while `_countries_for_product` expects country filename prefixes ([local_archive.py](backend/app/local_archive.py:36–59)); API test for India NOAA-21 returns 422. **Fix:** separate NOAA-21 global files from the country catalog and expose them only through processed Parquet or a dedicated global query.
6. **Processed archive is highly incomplete.** Quality report is 1,149/10,100 files, while raw extraction is 10,154 files; comparing periods/platforms is biased by source availability. **Fix:** process remaining eligible files, then report per-sensor/product/year coverage visibly.
7. **2026 cannot be selected in local archive UI.** `App.tsx:14` constructs only 2025 down to 2000 while backend max year is 2026 ([local_archive.py](backend/app/local_archive.py:24). **Fix:** expose 2026 only for products/structures the local loader can actually query, otherwise state the global-only path.
8. **Large raw country files remain blocked at 150 MB.** `local_archive.py:21,111–113`; extracted NOAA-21 CSVs reach 1,676.39 MiB. **Fix:** use bounded streaming/processed partitions for large sources; do not read the whole file into memory.
9. **The challenge's actual harmonization result is not implemented.** `harmonize.py:230–261` explicitly returns null index and `insufficient_calibration`; current metric is shared-grid detection overlap only. **Fix:** after reviewing official inputs and methods, define and validate an explicit, replaceable calibration using observation opportunity and sensor-specific performance; until then keep the limitation prominent.
10. **Frontend quality gates are incomplete.** No lint script exists; current frontend tests were blocked by the sandbox config-loader error in this audit; no App/Map E2E test covers startup, empty state, local archive, or AOI flow. **Fix:** configure lint, make tests run in the supported environment, and add end-to-end coverage for the high-risk paths.

## Commands not completed

- `git status --short` and `git log -15 --oneline`: unavailable because the workspace is not a Git repository.
- `Get-CimInstance Win32_Process`: blocked with `Access denied`; listener state was checked with curl and local port probes instead.
- `npm test` in the audit attempt: Vite/esbuild could not read the parent directory in this sandbox, so test collection did not start. A prior pre-health-patch frontend run passed 8 tests, but is not current-state evidence.
- `npm run lint`: unavailable because no lint script is defined.
- Frontend dev-server log and browser E2E: no frontend listener/process was running; not started under the read-only audit.
- NASA FIRMS API/live feed: intentionally not called.
