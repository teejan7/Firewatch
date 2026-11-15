# FIREWATCH

**Country-level explorer for NASA FIRMS MODIS and VIIRS active-fire records, with a statistical cross-sensor calibration.**

MODIS (since 2000) and VIIRS (since 2012) detect fires differently: pixel sizes are about 1 km and 375 m, and the sensors differ in sensitivity and overpass timing. Their raw fire counts and fire radiative power (FRP) cannot be compared directly. FIREWATCH keeps the raw records visible, calibrates weekly VIIRS FRP onto the MODIS scale using the years when both flew, validates the result on held-out years, and labels how confident each country's calibration is.

Built for NASA Space Apps Challenge 2026: *MODIS and VIIRS Hot Spots*.

## What it does

- **Daily activity calendar** for any country and year, by sensor family, as detection counts or summed FRP.
- **Raw sensors / Harmonized toggle:** compare reported values with calibrated values on one scale.
- **Multi-year calendar (2020–2025)** with weeks above the six-year 90th percentile marked as unusually active.
- **Typical-vs-this-year chart:** the selected year against the day-of-year median and 25th–75th percentile range.
- **Fire-season dates:** start, peak and end, from the cumulative 5%–95% of annual FRP.
- **Confidence label** (High / Medium / Low) and validation summary for every country.
- **Global activity map**, source coverage indicators, and CSV and PNG export.

Multi-year and seasonal views are marked **PRELIMINARY (6-year baseline)**.

## Results

| Measure | Value |
|---|---|
| Country series packaged | 236 country labels |
| Source files processed | 3,859 |
| Input rows | 265,659,156 |
| Years / sensors | 2020–2025 · MODIS (Terra, Aqua), VIIRS (S-NPP, NOAA-20), Standard Processing |
| Country fits with leave-one-year-out metrics | 167 |
| Median R² | 0.798 |
| Median holdout MdAPE | 40.9% |
| Confidence classes | 67 High · 65 Medium · 104 Low |

Example: Australia is rated High, with R² 0.939, holdout MdAPE 13.5% and 312 overlap weeks.

Treat the median error as moderate: the calibration is useful for exploring patterns, not for precise conversion between sensors.

## Quick start

Requirements: Node.js 20+ and npm. The dashboard is static: it needs no backend, API key or NASA request at runtime.

```bash
npm install
npm run start      # development server
npm run build      # production build
npm run preview    # serve the production build locally
npm run check      # typecheck, lint, tests and build
```

The map uses CARTO basemap tiles, so the page needs an internet connection.

## How the data was built

1. **Source:** NASA FIRMS Standard Processing country CSV files for MODIS, VIIRS S-NPP and VIIRS NOAA-20. The raw CSVs (about 46 GB) are not in this repository.
2. `backend/scripts/build_daily.py` streams the CSVs with DuckDB into compact daily aggregates (counts, FRP, vegetation-only and confidence-filtered values, day/night split).
3. `backend/scripts/build_compact.py` generates the static JSON the dashboard reads.
4. `backend/scripts/run_harmonize.py` fits the calibration and writes `frontend/public/data/harmonized/` and `frontend/public/data/methods_validation.json`.

Aggregation totals were checked against direct DuckDB counts on the raw CSVs for India, Australia, Brazil and Bahrain (2020–2025, both sensor families) and matched exactly. This verifies the counting, not the scientific validity of the calibration.

## Calibration method

Implemented in `backend/scripts/harmonize_core.py`:

- Weekly vegetation-only FRP per country, MODIS (Terra + Aqua) and VIIRS (S-NPP + NOAA-20).
- A Theil–Sen log–log fit predicts MODIS FRP from VIIRS FRP on weeks where both families report at least 5 MW. Country fits need at least 40 overlap weeks. Otherwise a deterministic global fit is used and the country is labelled Low.
- **Leave-one-year-out validation** gives R² and median absolute percentage error (MdAPE) on years the fit did not see.
- **Confidence:** High needs R² ≥ 0.7 and MdAPE ≤ 0.35; Medium needs R² ≥ 0.4 and MdAPE ≤ 0.60; everything else is Low.
- **Harmonized value:** where both sensors report, the log-space mean of MODIS and calibrated VIIRS; where only one reports, that value. The uncertainty band is ±1.96 residual standard deviations in log space.

Full detail: [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) and [`docs/VALIDATION.md`](docs/VALIDATION.md).

## Limitations

- This is a **statistical calibration, not a physical retrieval correction**. It does not account for satellite observation opportunity.
- Analysis is **country-level**, not custom areas or polygons.
- The baseline is **six years (2020–2025)**, so seasonal results are preliminary. MODIS data back to 2000 would extend this.
- **104 of 236 country calibrations are Low confidence.**
- **NOAA-21 is not included.**
- Empty dates mean no packaged detections, not confirmed absence of fire.
- Weeks with no fire in either sensor are excluded from fitting.

See [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md).

## Repository structure

```text
frontend/            React + TypeScript + Vite dashboard
  public/data/       packaged JSON the dashboard reads
backend/
  scripts/           data pipeline and calibration
  tests/             pipeline and calibration tests
docs/                methodology, validation, data, limitations, user guide
scripts/             local development launcher
```

## Data and credits

- **NASA FIRMS** (Fire Information for Resource Management System): MODIS and VIIRS 375 m active-fire products. See the [MODIS Active Fire User Guide](https://cdn.earthdata.nasa.gov/conduit/upload/10575/MODIS_C6_Fire_User_Guide_B.pdf) and the [VIIRS Active Fire User Guide](https://viirsland.gsfc.nasa.gov/PDF/VIIRS_activefire_User_Guide.pdf). Data: [firms.modaps.eosdis.nasa.gov](https://firms.modaps.eosdis.nasa.gov/).
- Built with React, TypeScript, Vite, Recharts, MapLibre GL JS, Lucide, DuckDB, pandas and NumPy.
- Basemap © [CARTO](https://carto.com/), map data © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright).

## AI assistance

AI assistants helped write and revise the code, documentation and data-processing scripts. The pipeline was run against the original NASA FIRMS Standard Processing CSV files, and aggregation totals were checked against the raw data as described above. These checks do not replace independent scientific review of the calibration.
