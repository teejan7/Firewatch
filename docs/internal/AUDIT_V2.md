# FIREWATCH v2 Read-Only Audit

Audit date: 2026-11-15. Project root: `[LOCAL_PROJECT_ROOT]`.

Scope: read-only inspection. No NASA requests were made. No `.env` value or MAP_KEY is reproduced. Only this report is created. All quantitative output below is from the local project snapshot; where browser behavior or commands were not exercised, it is marked ASSUMED.

## 1. SNAPSHOT

### Disk and directory sizes

| Item | Observed size | Evidence |
|---|---:|---|
| Free C: space | 11.6 GB | PowerShell disk-space query in this audit session |
| Project worktree, excluding `.git`, `node_modules`, `.venv` | 57,176,619,976 bytes (57.18 GB decimal) | Read-only recursive file-size walk; includes raw and processed data |
| `frontend/public/data` | 44,173,175 bytes (42.1 MiB); 238 files; largest 2,586,033 bytes | Recursive inventory |
| `data/raw` | 49,472,634,077 bytes (46.08 GiB); 10,155 files | Recursive inventory |
| `data/processed` | 7,612,755,739 bytes (7.09 GiB); 2,363 files | Recursive inventory |
| `node_modules` | 306,786,100 bytes (0.286 GiB) | Recursive inventory |
| `.venv` | 100,925,695 bytes (0.094 GiB) | Recursive inventory |

`data/raw/extracted` contains 10,154 files, 46.075 GiB, with filenames spanning 2000–2025. `data/raw/archives` exists but is empty. Raw/extracted contents are excluded from the tree below as requested.

### Project tree (depth ≤6; data file listings summarized)

```
FIREWATCH/
├── .env [present; contents not inspected]
├── .env.example
├── .github/
│   └── workflows/
│       └── pages.yml
├── .gitignore
├── AUDIT_REPORT.md
├── PROJECT_STRUCTURE.md
├── README.md
├── RELEASE_CHECKLIST.md
├── backend/
│   ├── app/
│   ├── scripts/
│   ├── tests/
│   ├── check.ps1
│   └── pyproject.toml
├── backups/
├── data/
│   ├── raw/
│   │   ├── archives/ [0 files]
│   │   └── extracted/ [10,154 files; 46.075 GiB; 2000–2025]
│   └── processed/ [2,363 files; 7.09 GiB]
├── disk_report.txt
├── docs/
│   ├── API.md
│   ├── DATA_ENGINE.md
│   ├── HARMONIZATION.md
│   ├── LIMITATIONS.md
│   ├── METHODOLOGY.md
│   └── VALIDATION.md
├── eslint.config.mjs
├── frontend/
│   ├── public/
│   │   └── data/ [238 JSON files; 42.1 MiB]
│   │       └── series/ [country JSON series]
│   ├── src/
│   │   ├── data/
│   │   ├── lib/
│   │   ├── ui/
│   │   ├── main.tsx
│   │   └── static.css
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
├── netlify.toml
├── package-lock.json
├── package.json
├── process_2020_2026_compact.bat
├── scripts/
├── start.bat
└── submission/
    ├── criteria_checklist.md
    ├── demo_script.md
    ├── next_steps.md
    └── summary.txt
```

Other observed excluded/generated folders: `node_modules/`, `.venv/`, `.git/`, `frontend/dist/`, `.pytest_cache/`, `.ruff_cache/`, `.test-tmp/`, `.tmp/`. Some tree subdirectory details are intentionally summarized here; exact complete nested source inventory was not regenerated in this audit.

### Git snapshot

- Repository: **yes** (`git rev-parse --is-inside-work-tree` returned true).
- `git status --short`:

```
 M .gitignore
 M README.md
 M backend/check.ps1
 M backend/pyproject.toml
 M docs/DATA_ENGINE.md
 M docs/LIMITATIONS.md
 M frontend/index.html
 M frontend/package.json
 M frontend/src/main.tsx
 M frontend/vite.config.ts
 M package.json
 M start.bat
?? .env.example
?? .github/
?? PROJECT_STRUCTURE.md
?? RELEASE_CHECKLIST.md
?? backend/scripts/build_compact.py
?? backend/tests/test_build_compact.py
?? data/
?? disk_report.txt
?? docs/METHODOLOGY.md
?? docs/VALIDATION.md
?? frontend/public/
?? frontend/src/data/
?? frontend/src/static.css
?? frontend/src/ui/GlobalMap.tsx
?? frontend/src/ui/StaticApp.test.tsx
?? frontend/src/ui/StaticApp.tsx
?? frontend/src/ui/StaticMap.tsx
?? netlify.toml
?? submission/
```

- Last commits (`git log -10 --oneline`; only three exist):

```
8ac8cc9 feat: complete resumable FIRMS processing layer
33f0b0e feat: harden FIREWATCH local development flow
a408386 chore: baseline FIREWATCH prototype
```

- `git count-objects -vH`: count 115; size 274.46 KiB; in-pack 0; packs 0; garbage 0; size-garbage 0.
- The active static frontend, its JSON data, new docs, and submission pack are untracked. README says JSON is committed (`README.md:27,35`), which is currently inaccurate for this Git worktree. A Pages deployment built from committed branch content would not contain these untracked files. No staging or committing was performed.

### Largest tracked files and tracked data scan

| Rank | Tracked path | Bytes |
|---:|---|---:|
| 1 | `package-lock.json` | 174,622 |
| 2 | `backend/scripts/build_processed.py` | 43,046 |
| 3 | `AUDIT_REPORT.md` | 38,789 |
| 4 | `frontend/src/ui/App.tsx` | 35,496 |
| 5 | `frontend/src/styles.css` | 22,067 |
| 6 | `backend/app/harmonize.py` | 13,609 |
| 7 | `backend/app/main.py` | 12,475 |
| 8 | `frontend/src/ui/ProcessedComparison.tsx` | 12,150 |
| 9 | `backend/app/analytics_api.py` | 10,831 |
| 10 | `backend/app/local_archive.py` | 10,574 |
| 11 | `backend/tests/test_processing.py` | 10,443 |
| 12 | `backend/tests/test_analytics_api.py` | 7,731 |
| 13 | `docs/DATA_ENGINE.md` | 6,823 |
| 14 | `frontend/src/ui/MapView.tsx` | 6,668 |
| 15 | `README.md` | 6,518 |

No tracked file exceeds 50 MB. A tracked-file scan found no raw `.csv`, `.zip`, `.parquet`, `.env`, backup, or cache files. This is consistent with the current large `data/` directory being untracked/ignored.

## 2. DATA BUILD (Phase 1)

### Processed file coverage

Evidence: `data/processed/manifest.json` (2,357 manifest entries; 2,354 country outputs plus 3 global outputs) and `frontend/public/data/quality.json` (2,354 country files, 163,334,036 rows). Counts below are observed in that quality report; file completeness is relative to the report's discovered expected country source filenames, not an independent completeness guarantee.

| Product | Years with processed files | Expected / processed per year | Result |
|---|---|---|---|
| MODIS SP | 2020, 2021, 2023, 2025 | 2020 211/211; 2021 204/204; 2023 207/207; 2025 202/202 | Complete for these reported years. Missing 2000–2019, 2022 (204), 2024 (206). |
| VIIRS NOAA-20 SP | 2020, 2021, 2023, 2024, 2025 | 2020 223/223; 2021 219/219; 2023 219/219; 2024 1/219; 2025 217/217 | 2024 is partial. Missing 2018, 2019, 2022. |
| VIIRS S-NPP SP | 2020, 2021, 2023, 2025 | 2020 218/218; 2021 133/216; 2023 81/216; 2025 219/219 | 2021 and 2023 are partial. Missing 2012–2019, 2022, 2024. |

**Why missing:** the quality report shows no processed country outputs for the listed expected files. `data/raw/archives` is empty and `deletion_log.txt` is absent, so this audit cannot establish whether missing source years were never downloaded, removed, or otherwise unavailable. Do not interpret missing data as zero fire.

### Static export

- `frontend/public/data`: 238 files, 44,173,175 bytes; maximum file 2,586,033 bytes.
- `countries.json`: 235 country entries (catalog is 2,586,033 bytes).
- Country series JSON: 235 files (India 537,360 bytes, Australia 861,649, Brazil 950,052, United States 931,158; Andorra 3,542).
- `quality.json`: reports 2,354 source files and 163,334,036 rows; years represented: 2020, 2021, 2023, 2024, 2025. NOAA-21 global exports are excluded from the country series (`README.md:5`, `docs/DATA_ENGINE.md:47`).

### Spot checks (January 2020)

Direct DuckDB counts over the raw CSV and corresponding packed series totals matched. Percentage difference is `(compact - raw) / raw × 100`.

| Country / product | Raw CSV rows | Compact total | Difference |
|---|---:|---:|---:|
| India MODIS | 2,843 | 2,843 | 0% |
| India NOAA-20 | 21,494 | 21,494 | 0% |
| India S-NPP | 20,971 | 20,971 | 0% |
| Australia MODIS | 36,994 | 36,994 | 0% |
| Australia NOAA-20 | 191,225 | 191,225 | 0% |
| Australia S-NPP | 199,080 | 199,080 | 0% |
| Brazil MODIS | 6,147 | 6,147 | 0% |
| Brazil NOAA-20 | 22,130 | 22,130 | 0% |
| Brazil S-NPP | 22,000 | 22,000 | 0% |

This checks row-count preservation for one month; it does not validate sensor equivalence, geolocation, source completeness, or scientific accuracy.

### Boundaries and data lineage

- `world.geojson`: **not present** (no size or feature count available). Static map is an observed-record centroid bubble map, explicitly “Not a boundary choropleth” (`frontend/src/ui/GlobalMap.tsx:69`).
- Series-country names with polygon match: **0 matches could be checked**, because no boundary file exists. All 235 series countries are consequently unmatched. Polygons without data: 0 because there are no polygons to test.
- `deletion_log.txt`: absent. Archive folder contains 0 files; cannot confirm any deleted year has a retained archive. No deletion claims can be verified.

## 3. HARMONIZATION (Phase 2)

- Calibration code is **not implemented** in the active static build. The prior API comparison implementation returns `harmonized_index: None` and `calibration_status: insufficient_calibration` (`backend/app/harmonize.py:234-235`); `docs/HARMONIZATION.md:5` calls it comparison-only. There is no fitted metric, aggregation fit, regression method, fallback rule, or blending rule to quote. These are **N/A**, not zero-valued results.
- `methods_validation.json`: status `not_calibrated`; harmonized index, validation metrics are null. Required paired coverage and observation-opportunity denominators are absent. Calibrated country count: 0; median R², median 2023–2025 holdout error, correlation: unavailable; low-confidence countries: none can be calculated. Country-specific metrics for India, Australia, Brazil, USA, Indonesia: unavailable.
- Continuity at platform starts (e.g. NOAA-20 in 2018): **not assessed**. No calibrated output exists to test continuity.
- Independent recalculation of India calibration: **not possible** because no fitted calibration or reported slope/intercept/R² exists. The January 2020 row-count spot-check in section 2 is not a substitute.
- UI does not display an index without a band/flag: it explicitly states no index is shown and marks the package NOT CALIBRATED (`frontend/src/ui/StaticApp.tsx:180`).
- Simulated data: the mounted static UI loads `frontend/public/data/*.json`; however a dormant older implementation remains in `frontend/src/ui/App.tsx` and `frontend/src/data/demo.ts`, including demo/live/archive controls (`App.tsx:208-211`). `frontend/src/main.tsx:5-6` mounts `StaticApp`, so that older UI is not in the active component tree. Whether other placeholder/simulated records occur in every raw/processed input is **ASSUMED**; no comprehensive value-level scan was run. The static app's generated source data is not labeled simulated.
- Scientific defensibility: **not a harmonization result**. The comparison-only snapshot is defensible as a transparent exploratory display with limitations, not as a scientifically validated MODIS/VIIRS harmonization.
- Three weakest assumptions/limitations: (1) detections from different sensor footprints, overpasses, and detection thresholds cannot be treated as equivalent counts; (2) no observed opportunity/missed-detection denominator exists in the packaged active-fire records; (3) available years are sparse and partly incomplete, preventing robust training, independent holdout, and continuity assessment.

## 4. ANALYTICS (Phase 3)

- Baseline: UI requires 10 complete baseline years (`frontend/src/ui/StaticApp.tsx:181`). Smoothing window: none implemented. Leave-one-year-out validation: no. No climatology/anomaly algorithm is applied; the panel expressly says anomaly ranking and season dates are not calculated (`StaticApp.tsx:181`).
- Five-country season dates and top anomalous weeks: **not calculable**, not reported. There is no validated season/anomaly method and no sufficient baseline. Australia 2019–20 extremity and India fire-season timing: **not testable** in this build; 2019 is not in the static export, and no seasonal model is provided.
- Countries marked insufficient baseline: all 235 catalog countries are below the 10-complete-year threshold. Names: Afghanistan; Aland Islands; Albania; Algeria; American Samoa; Andorra; Angola; Antarctica; Antigua and Barbuda; Argentina; Armenia; Aruba; Australia; Austria; Azerbaijan; Bahamas; Bahrain; Bangladesh; Barbados; Belarus; Belgium; Belize; Benin; Bermuda; Bhutan; Bolivia; Bosnia and Herzegovina; Botswana; Brazil; British Virgin Islands; Brunei Darussalam; Bulgaria; Burkina Faso; Burundi; Cambodia; Cameroon; Canada; Cape Verde; Cayman Islands; Central African Republic; Chad; Chile; China; Colombia; Comoros; Cook Islands; Costa Rica; Cote d'Ivoire; Croatia; Cuba; Curacao; Cyprus; Czech Republic; Dem. Rep. Korea; Democratic Republic of the Congo; Denmark; Djibouti; Dominica; Dominican Republic; Ecuador; Egypt; El Salvador; Equatorial Guinea; Eritrea; Estonia; Ethiopia; Faeroe Islands; Falkland Islands; Federated States of Micronesia; Fiji; Finland; France; French Guiana; French Polynesia; French Southern and Antarctic Lands; Gabon; Georgia; Germany; Ghana; Greece; Greenland; Grenada; Guadeloupe; Guam; Guatemala; Guernsey; Guinea; Guinea-Bissau; Guyana; Haiti; Heard Island and McDonald Islands; Honduras; Hong Kong; Hungary; Iceland; India; Indonesia; Iran; Iraq; Ireland; Isle of Man; Israel; Italy; Jamaica; Japan; Jersey; Jordan; Kazakhstan; Kenya; Kiribati; Kosovo; Kuwait; Kyrgyzstan; Lao PDR; Latvia; Lebanon; Lesotho; Liberia; Libya; Liechtenstein; Lithuania; Luxembourg; Macedonia; Madagascar; Malawi; Malaysia; Maldives; Mali; Malta; Martinique; Mauritania; Mauritius; Mayotte; Mexico; Moldova; Monaco; Mongolia; Montenegro; Montserrat; Morocco; Mozambique; Myanmar; Namibia; Nauru; Nepal; Netherlands; New Caledonia; New Zealand; Nicaragua; Niger; Nigeria; Niue; Norfolk Island; Northern Mariana Islands; Norway; Oman; Pakistan; Palau; Palestine; Panama; Papua New Guinea; Paraguay; Peru; Philippines; Poland; Portugal; Puerto Rico; Qatar; Republic of Congo; Republic of Korea; Reunion; Romania; Russian Federation; Rwanda; Saint Barthelemy; Saint Martin; Saint Helena; Saint Kitts and Nevis; Saint Lucia; Saint Pierre and Miquelon; Saint Vincent and the Grenadines; Samoa; San Marino; Sao Tome and Principe; Saudi Arabia; Senegal; Serbia; Seychelles; Sierra Leone; Singapore; Sint Maarten; Slovakia; Slovenia; Solomon Islands; Somalia; South Africa; South Sudan; Spain; Sri Lanka; Sudan; Suriname; Svalbard and Jan Mayen; Swaziland; Sweden; Switzerland; Syria; Taiwan; Tajikistan; Tanzania; Thailand; The Gambia; Timor-Leste; Togo; Tonga; Trinidad and Tobago; Tunisia; Turkey; Turkmenistan; Turks and Caicos Islands; Uganda; Ukraine; United Arab Emirates; United Kingdom; United States; United States Minor Outlying Islands; United States Virgin Islands; Uruguay; Uzbekistan; Vanuatu; Venezuela; Vietnam; Wallis and Futuna Islands; Yemen; Zambia; Zimbabwe.

## 5. WEB APP (Phase 4)

### Runtime data calls and removed modules

- Active entry point mounts `StaticApp` (`frontend/src/main.tsx:5-6`). The active UI calls only `${import.meta.env.BASE_URL}data/countries.json` and `${base}data/series/${slug}.json` (`frontend/src/ui/StaticApp.tsx:13,60,72`). No active API backend is required for these data calls.
- Source grep hits for runtime fetch/API plumbing include the two static JSON calls above and dormant `frontend/src/lib/apiClient.ts:40` (`fetch(url, ...)`), with `apiGet`/`apiPost` wrappers at lines 74-75. The dormant older `frontend/src/ui/App.tsx` still contains FIRMS live, archive, local archive, CSV upload, demo return, and API status UI (`App.tsx:202,208-211`). They are not mounted by `main.tsx`.
- A separate `frontend/src/ui/StaticMap.tsx` remains in source; map style uses public CARTO tiles (`frontend/src/ui/GlobalMap.tsx:17`), so the basemap needs network access. It does not call NASA. Static source records remain usable when basemap tiles fail (`GlobalMap.tsx:69`).
- All active data calls use the Vite base (`StaticApp.tsx:13,60,72`); base config is `frontend/vite.config.ts:4`. No `localhost:8000/api/` runtime URL is in the mounted static app.

### Checks and production serving

- `npm run lint`: **PASS**, exit code 0, no diagnostics.
- `.venv\Scripts\ruff.exe check --no-cache backend\app backend\scripts backend\tests`: **PASS**, output `All checks passed!`.
- `npm ls --depth=0 playwright @playwright/test`: **not available**, output `(empty)`; no Playwright browser test could run.
- Existing local Vite preview at `http://127.0.0.1:4173/` returned HTTP 200 and title `FIREWATCH · Active-fire records`. A fresh production build was not run in this read-only audit.
- Read-only HTTP fetches against that preview: `/` 200; `/data/countries.json` 200; India, Australia, Brazil, United States and Andorra JSON 200. A nonexistent `/data/series/no-such-country.json` returned **200 HTML** due to Vite SPA fallback, not a JSON 404. This can produce a JSON parse error rather than a useful missing-series response (`StaticApp.tsx:72` checks status, not content type).
- Country calendar displays source values for available selected years; country-with-no-data behavior could not be tested because all catalog entries have a series JSON file. The nonexistent slug is not a selectable country.

### Feature checklist

| Requirement | Status | Evidence |
|---|---|---|
| Country dropdown/search | PASS | Active `StaticApp.tsx` catalog/select state |
| Click-on-map selection | PARTIAL | Centroid bubbles select country; not polygon selection (`GlobalMap.tsx:69`) |
| Day-by-year calendar | PARTIAL | One selected year with daily buttons; not a multi-year heatmap (`StaticApp.tsx:167-170`) |
| Colorblind-safe palette | ASSUMED | Palette was not evaluated with a color-vision simulation |
| Tooltip content | PARTIAL | Date, sensor-specific counts/FRP and source coverage (`StaticApp.tsx:168`); no harmonized value |
| Index vs counts toggle | PARTIAL | Metric selection is count or FRP sum; no calibrated index (`StaticApp.tsx:168,180`) |
| Raw vs Harmonized toggle | FAIL | No harmonized values; explicit not-calibrated status (`StaticApp.tsx:180`) |
| Climatology panel | PARTIAL | Honest insufficiency state only; no computed climatology (`StaticApp.tsx:181`) |
| Critical periods panel | PARTIAL | Explicitly “not calculated” (`StaticApp.tsx:181`) |
| World choropleth + slider | PARTIAL | Centroid bubbles and month slider; no boundaries/choropleth (`StaticApp.tsx:175`, `GlobalMap.tsx:69`) |
| Method quality badge | PARTIAL | Partial archive / not-calibrated disclosures; no fit metrics (`StaticApp.tsx:128,180`) |
| Limitations panel | PASS | Method modal and limitations messaging (`StaticApp.tsx:180,190`) |
| CSV export, formula guard, provenance | PASS by code; not freshly browser-exercised | `safeCell` at `StaticApp.tsx:17`; source/provenance rows at `:105` and export at `:111` |
| PNG export | PASS by code; not freshly browser-exercised | `StaticApp.tsx:22` and `:152,170` |
| Loading/empty/error | PARTIAL | Loading/empty/error UI at `StaticApp.tsx:160-161`; invalid JSON MIME/200 case can produce parser error |
| Mobile layout at 375 px | ASSUMED | No screenshot or viewport run; requested screenshot folder is absent |
| Keyboard navigation | PARTIAL | Native controls/calendar buttons work by keyboard; map interaction is pointer-focused; no browser audit |
| Truthful ARIA labels | PARTIAL | Calendar buttons labeled; map has image role/description; no screen-reader review (`StaticApp.tsx:168`, `GlobalMap.tsx:69`) |

### Performance

- Measured time-to-first-load and country-switch latency: **ASSUMED / not measured in a browser**. HTTP response times from the local preview were 326 ms for the index, 54–93 ms for representative country series, and 6 ms for Andorra; these are server response durations, not interaction or rendering timings.
- Approximate raw payload for first app data load: country index + Australia series = 3,447,682 bytes (3.29 MiB), before HTTP compression or map tiles. This is the sum of the observed file sizes, not a network transfer measurement.
- No console inspection, real network capture, mobile screenshot, fresh CSV/PNG download, or screen-reader session was performed.

## 6. DEPLOYMENT (Phase 5)

- Vite base: `process.env.VITE_BASE_PATH || '/'` (`frontend/vite.config.ts:4`). GitHub Pages workflow sets `VITE_BASE_PATH: /${{ github.event.repository.name }}/` (`.github/workflows/pages.yml:31`). Netlify config sets base `/` (`netlify.toml:6`).
- Build under a subpath and asset verification: **not rerun in this audit** because build writes generated files and the instruction restricts project writes to this report. `docs/VALIDATION.md:16` records a prior successful `/firewatch-preview/` build, but that result is historical and was not independently reproduced here.
- Live URL: none. README and submission script retain deployment placeholders (`README.md:58`, `submission/summary.txt:13`, `submission/demo_script.md:9`). Missing: push/commit current static app and data, configure/enable a host workflow, publish, then verify hosted assets and JSON.
- Docs present: README, `docs/METHODOLOGY.md`, `docs/VALIDATION.md`, `docs/LIMITATIONS.md`, `docs/DATA_ENGINE.md`, `docs/HARMONIZATION.md`, `docs/API.md`, plus AI-use disclosure (`README.md:81-83`).
- Accuracy caveat: README says the generated static JSON is committed (`README.md:27,35`), but Git status shows the entire `frontend/public/` and its JSON untracked. Live demo placeholder remains. README’s counts match the local `quality.json` values: 2,354 source files, 163,334,036 rows, 235 country series, 2020/2021/2023/2024/2025. Those metrics describe this generated export, not complete historical coverage. Internal documentation run commands on a clean checkout were not tested; there is no clean checkout attempt.
- Broken external/internal links: **not checked**; no web requests were made.
- Secret scan: tracked-file scan reported no MAP_KEY/token-like matches and no tracked `.env`; `.env` exists locally but its contents were not read. `.env` history query returned no tracked history. A tracked audit document contains one absolute user-path hit at `AUDIT_REPORT.md:333`; value redacted here as `[REDACTED]`. No other absolute path hit was reported in the scan. Git history content-wide credential scanning was not performed, so secret absence from every historical blob is **ASSUMED**.
- `.gitignore` excludes raw data, Parquet, archives, CSV, `.env`, backups, caches, `node_modules`, and `.venv`; public JSON is explicitly allowed (verified from `.gitignore:1-25`).

## 7. SUBMISSION PACK (Phase 6)

- `/submission/summary.txt`: 196 words (under 300); numeric claims 2020/2021/2023/2024/2025, 235 countries, 2,354 files, 163,334,036 rows, and 9 exact January 2020 source-row checks match the generated quality report / spot checks. The public demo URL is still a placeholder (`summary.txt:13`).
- `/submission/demo_script.md`: about 3:00 total by its listed segment timings; it explicitly says hosted URL is a placeholder and not to claim unavailable analytics (`demo_script.md:9,38`).
- `criteria_checklist.md`, `next_steps.md`, root `RELEASE_CHECKLIST.md`: present. Their operational completion was not executed here.
- README numerical claims match `quality.json` for processed row/file/country/year totals. The statement that JSON is committed does not match `git status` (`README.md:27,35`).

### Challenge requirement mapping

| Challenge requirement | Assessment | Evidence |
|---|---|---|
| Harmonizes MODIS and VIIRS records | NOT met | No calibrated index; explicit `NOT CALIBRATED` (`StaticApp.tsx:180`, `methods_validation.json`) |
| Burning activity calendar | PARTIALLY met | Daily, sensor-separated detection/FRP calendar for included years; archive gaps marked (`StaticApp.tsx:167-170`) |
| Selected area of interest | PARTIALLY met | Select a country and inspect country aggregate; no drawn AOI in active static view |
| Historical fire patterns | PARTIALLY met | Sparse/incomplete 2020–25 snapshot, no long-baseline analytics (`quality.json`, `StaticApp.tsx:181`) |
| Unusual conditions | NOT met | Anomaly ranking not calculated (`StaticApp.tsx:181`) |
| Critical periods | NOT met | Season start/peak/end not calculated (`StaticApp.tsx:181`) |
| Early warning | NOT met | No alert/forecast/validated signal in active static app |
| Useful to responders, scientists, land managers | PARTIALLY met | Transparent exploratory counts/provenance can support browsing, but no validated comparable index, alert, or decision support |

## 8. SCORECARD

| Criterion | Score | Justification |
|---|---:|---|
| Impact | 2/5 | Explorable source detections are useful context, but no validated harmonized signal or early warning is provided. |
| Creativity | 3/5 | The polished calendar, provenance and transparent incomplete-baseline treatment are thoughtful. |
| Validity | 3/5 | Source-specific rows are preserved and spot checks match, but the core calibration and independent validation are absent. |
| Relevance | 2/5 | The challenge's central MODIS/VIIRS harmonization requirement is not met. |
| Presentation | 3/5 | The static dashboard and submission materials are organized, but there is no live URL and current release files are uncommitted. |

## 9. FINAL VERDICT

**NOT READY** for a claim of a completed harmonization solution. It can be presented accurately as a comparison-only exploratory prototype if its current files are committed and hosted, but it does not satisfy calibration, unusual-condition analysis, critical periods, or early warning. A live submission URL is absent.

### TOP 10 PROBLEMS (ranked by severity)

1. **Core science absent** — `frontend/src/ui/StaticApp.tsx:180`; calibration output is null / `not_calibrated`. Root cause: no validated paired training/holdout and observation-opportunity inputs. Fix: implement and validate a documented sensor-specific calibration only after acquiring appropriate inputs. **>60 min; scientific validation cannot be responsibly estimated as a quick patch.**
2. **Release is not in Git** — `git status --short`; active static UI/data/submission/docs are untracked. Root cause: latest working version has not been committed. Fix: carefully stage only intended source, docs, and export files; exclude `.env`, raw and processed data. **10–20 min.**
3. **No live demo URL** — `README.md:58`, `submission/summary.txt:13`. Root cause: no published deployment verified. Fix: deploy the committed static app, then smoke-test URL and JSON assets. **15–30 min after commit/host access.**
4. **No choropleth or boundary data** — `frontend/src/ui/GlobalMap.tsx:69`; `world.geojson` absent. Root cause: map uses detection centroids. Fix: add a sourced boundary file and verified country-name crosswalk, then test all 235 series. **30–90 min.**
5. **No validated anomalies, seasons, or critical-period analytics** — `frontend/src/ui/StaticApp.tsx:181`. Root cause: fewer than 10 complete baseline years and no implemented validated method. Fix: obtain complete years and document/test climatology and holdout methods. **>60 min.**
6. **Historical data incomplete** — `frontend/public/data/quality.json`; data coverage table in section 2. Root cause: years/products absent or partial; no deletion log or retained archives. Fix: recover/acquire desired source files, process, and reconcile completeness before claiming coverage. **>60 min, dependent on data.**
7. **Invalid static series URL returns HTML 200** — local preview `/data/series/no-such-country.json`; `frontend/src/ui/StaticApp.tsx:72`. Root cause: SPA fallback and no MIME validation. Fix: detect non-JSON response and show a precise missing-series error or configure host 404 behavior. **5–15 min.**
8. **Dormant legacy UI contradicts active static product** — `frontend/src/ui/App.tsx:202,208-211`, `frontend/src/data/demo.ts`; not mounted by `main.tsx`. Root cause: old API/demo controls remain in source. Fix: remove from release source or label as archived and ensure reviewers understand they are inactive. **10–20 min.**
9. **First-load data payload is sizable** — `countries.json` 2,586,033 bytes plus a representative country series ~0.5–0.95 MB. Root cause: catalog includes full summary/map metadata. Fix: slim catalog, compress JSON, or lazy-load map detail; then measure actual transfer and render time. **20–40 min.**
10. **Mobile, keyboard, and accessibility are unverified** — no 375 px screenshot or browser automation available. Root cause: no Playwright installed and no visual audit run. Fix: run viewport/keyboard/screen-reader checks and save required screenshot after final release. **20–30 min.**

### Fix in the next 60 minutes

1. Make a reviewed release commit by staging only the new static frontend, `frontend/public/data`, workflow/config/docs and submission pack; explicitly exclude `.env`, `data/raw`, `data/processed`, backups, and temporary reports. Check staged names and total size before committing.
2. Correct README’s “committed JSON” wording if the verified release branch does not actually include the JSON. Do not claim the host works until the source is pushed and a public URL plus JSON paths are verified.
3. Deploy the comparison-only build to GitHub Pages or Netlify and perform a short hosted smoke test for index, India, Australia and a tiny-country series. Replace placeholders only after success.
4. Fix missing-series handling for HTML fallback responses and remove/label dormant API/demo UI source so users do not encounter controls that are not part of the active app.
5. Keep the presentation honest: state **comparison-only / not calibrated**. Do not claim harmonization, anomalies, critical periods, early warning, or complete 2000–2025 coverage.

### Commands not run and why

- `npm ci` / clean-checkout setup: not run because it modifies `node_modules` and the audit permits only this report file to be created.
- `npm run typecheck`, `npm test`, `npm run build`, subpath rebuild: not rerun because build/typecheck/test commands can write `dist`, caches, or TypeScript metadata; prior recorded results in `docs/VALIDATION.md` are not fresh verification.
- Playwright/browser tests, console/network capture, 375 px screenshot, CSV/PNG download tests: Playwright packages are absent (`npm ls ...` returned `(empty)`), and no browser automation was available in this audit.
- Live deploy URL fetch and external documentation link checks: no URL exists in project docs; no external network requests were made.
- NASA endpoints/APIs: explicitly not called.
- Credential scan across all historical Git blobs: not run; `.env` content was intentionally not read. Tracked working-tree scan found no key-like values; historical credential cleanliness is **ASSUMED**.
