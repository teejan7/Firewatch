# FIREWATCH release checklist

| Requirement | Status | Evidence / remaining action |
|---|---|---|
| Static frontend production build | PASS | `npm run check` includes Vite build. |
| Backend not needed at runtime | PASS | Browser preview ran from static JSON with backend off. |
| No API key or secret required | PASS | Static application does not request a FIRMS key. Never commit local `.env`. |
| Packaged data under 120 MiB | PASS | 115,853,537 bytes (~110.46 MiB); configured cap is 120 MiB. |
| Deployable source/data under 300 MB | PASS (local estimate) | Generated JSON is ~110.46 MiB; source/config/tests are small. Raw CSV and processed Parquet are excluded by `.gitignore`. Confirm after staging if using `git add -f` or changing ignore rules. |
| No country series over 6 MiB | PASS | Largest series is Russian Federation at 2,942,274 bytes; local raw/processed inputs are intentionally not deploy artifacts. |
| Scientific calibration | NOT CLAIMED | No calibrated harmonization model or holdout metrics are supported by the present incomplete coverage; the dashboard publishes no harmonized index. |
| Daily/raw verification | PASS | 48/48 India, Australia, Brazil and Bahrain 2020–2025 country/year/family comparisons match exactly. Full table: `docs/VALIDATION.md`. |
| Backend-off desktop smoke check | PASS | Local production preview loaded Australia series/calendar and map module; CSV download succeeded. |
| Mobile at 375 px | ASSUMED | Responsive implementation exists; visual viewport review still required. |
| GitHub Pages repository subpath | PASS | Tested a non-root `/firewatch-preview/` build and verified its asset URLs; actual repository name and hosted URL still need verification after push. |
| Public live link | PENDING | Publish and open the URL before sharing a live demo claim. |
| Screenshots in `docs/screens/` | FAIL | No verified screenshots were captured. |
| Raw source preservation | PASS | Extracted CSVs were not removed. `data/raw/archives` currently has no ZIP files. |
| Legacy row-level cleanup | NOT RUN | The old `observations`, `cell_shards` and original `manifest.json` remain untouched; the user may decide whether to remove the two old Parquet directories. |

## Commands run

- `.venv\Scripts\python.exe backend\scripts\build_daily.py --force` — PASS: 18 sensor-year groups and 3,859 source files; daily plus grid aggregates only; disk remained above 3 GiB.
- `.venv\Scripts\python.exe backend\scripts\build_compact.py` — PASS: 236 country series, 265,659,156 detections, 115,853,537 JSON bytes.
- `.venv\Scripts\python.exe backend\scripts\verify_daily.py --markdown` — PASS: 48/48 daily/raw comparisons exact; legacy coverage differences are explained in `docs/VALIDATION.md`.
- `npm run check` — PASS: TypeScript, lint, 15 frontend tests, production build, Ruff and 46 backend tests (one Starlette/httpx deprecation warning).
- `npm run preview --workspace frontend -- --port 4173` — PASS after setting `--configLoader runner`; loaded with API/backend off.

## Before publishing

1. Push the source to a public GitHub repository.
2. Enable Pages with GitHub Actions (or connect Netlify).
3. Open the hosted site and verify country/year selection, CSV/PNG export and map behavior.
4. Record the URL and capture release screenshots. Do not claim calibration, anomalies, critical periods or deployment until each is actually verified.
