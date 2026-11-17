# FIREWATCH validation record

Recorded on 2026-11-15 after rebuilding the local 2020–2025 daily aggregates. This is a record of that historical run, not a fresh validation run. In the current checkout, data/raw/extracted is absent, so the raw comparisons below cannot currently be repeated without restoring the matching source CSVs.

## Four-country aggregate verification

For India, Australia, Brazil and Bahrain, DuckDB raw CSV row counts were compared with daily detection totals for MODIS and VIIRS in every year from 2020 through 2025. All 48 daily/raw comparisons are exact (0.000% difference), below the 0.1% threshold. The verifier reads local extracted CSVs only and makes no NASA requests.

| Country | Year | Sensor family | Raw DuckDB rows | New daily detections | Existing series detections | Daily vs raw | Daily vs existing | Explanation |
|---|---:|---|---:|---:|---:|---:|---:|---|
| India | 2020 | MODIS | 76021 | 76021 | 76021 | 0.000% | 0.000% | Within 0.1%. |
| India | 2020 | VIIRS | 984366 | 984366 | 984366 | 0.000% | 0.000% | Within 0.1%. |
| India | 2021 | MODIS | 111267 | 111267 | 111267 | 0.000% | 0.000% | Within 0.1%. |
| India | 2021 | VIIRS | 1536735 | 1536735 | 1536735 | 0.000% | 0.000% | Within 0.1%. |
| India | 2022 | MODIS | 81525 | 81525 | 81525 | 0.000% | 0.000% | Within 0.1%. |
| India | 2022 | VIIRS | 1198449 | 1198449 | 1198449 | 0.000% | 0.000% | Within 0.1%. |
| India | 2023 | MODIS | 78425 | 78425 | 78425 | 0.000% | 0.000% | Within 0.1%. |
| India | 2023 | VIIRS | 1170878 | 1170878 | 591145 | 0.000% | 98.070% | New daily build includes source product(s) absent from the baseline JSON: VIIRS_SNPP_SP. |
| India | 2024 | MODIS | 74029 | 74029 | 74029 | 0.000% | 0.000% | Within 0.1%. |
| India | 2024 | VIIRS | 1130374 | 1130374 | 0 | 0.000% | n/a | No baseline JSON detections; daily build adds VIIRS_NOAA20_SP, VIIRS_SNPP_SP. |
| India | 2025 | MODIS | 94917 | 94917 | 94917 | 0.000% | 0.000% | Within 0.1%. |
| India | 2025 | VIIRS | 1301930 | 1301930 | 1301930 | 0.000% | 0.000% | Within 0.1%. |
| Australia | 2020 | MODIS | 155524 | 155524 | 155524 | 0.000% | 0.000% | Within 0.1%. |
| Australia | 2020 | VIIRS | 1677524 | 1677524 | 1677524 | 0.000% | 0.000% | Within 0.1%. |
| Australia | 2021 | MODIS | 171948 | 171948 | 171948 | 0.000% | 0.000% | Within 0.1%. |
| Australia | 2021 | VIIRS | 1631599 | 1631599 | 1631599 | 0.000% | 0.000% | Within 0.1%. |
| Australia | 2022 | MODIS | 160278 | 160278 | 160278 | 0.000% | 0.000% | Within 0.1%. |
| Australia | 2022 | VIIRS | 1631255 | 1631255 | 1631255 | 0.000% | 0.000% | Within 0.1%. |
| Australia | 2023 | MODIS | 395733 | 395733 | 395733 | 0.000% | 0.000% | Within 0.1%. |
| Australia | 2023 | VIIRS | 3637610 | 3637610 | 3637610 | 0.000% | 0.000% | Within 0.1%. |
| Australia | 2024 | MODIS | 223807 | 223807 | 223807 | 0.000% | 0.000% | Within 0.1%. |
| Australia | 2024 | VIIRS | 2039276 | 2039276 | 0 | 0.000% | n/a | No baseline JSON detections; daily build adds VIIRS_NOAA20_SP, VIIRS_SNPP_SP. |
| Australia | 2025 | MODIS | 255336 | 255336 | 255336 | 0.000% | 0.000% | Within 0.1%. |
| Australia | 2025 | VIIRS | 2499289 | 2499289 | 2499289 | 0.000% | 0.000% | Within 0.1%. |
| Brazil | 2020 | MODIS | 405388 | 405388 | 405388 | 0.000% | 0.000% | Within 0.1%. |
| Brazil | 2020 | VIIRS | 3299892 | 3299892 | 3299892 | 0.000% | 0.000% | Within 0.1%. |
| Brazil | 2021 | MODIS | 340582 | 340582 | 340582 | 0.000% | 0.000% | Within 0.1%. |
| Brazil | 2021 | VIIRS | 2637945 | 2637945 | 2637945 | 0.000% | 0.000% | Within 0.1%. |
| Brazil | 2022 | MODIS | 362785 | 362785 | 362785 | 0.000% | 0.000% | Within 0.1%. |
| Brazil | 2022 | VIIRS | 2858264 | 2858264 | 2858264 | 0.000% | 0.000% | Within 0.1%. |
| Brazil | 2023 | MODIS | 357737 | 357737 | 357737 | 0.000% | 0.000% | Within 0.1%. |
| Brazil | 2023 | VIIRS | 2658150 | 2658150 | 2658150 | 0.000% | 0.000% | Within 0.1%. |
| Brazil | 2024 | MODIS | 527894 | 527894 | 527894 | 0.000% | 0.000% | Within 0.1%. |
| Brazil | 2024 | VIIRS | 3924144 | 3924144 | 0 | 0.000% | n/a | No baseline JSON detections; daily build adds VIIRS_NOAA20_SP, VIIRS_SNPP_SP. |
| Brazil | 2025 | MODIS | 236731 | 236731 | 236731 | 0.000% | 0.000% | Within 0.1%. |
| Brazil | 2025 | VIIRS | 1715530 | 1715530 | 1715530 | 0.000% | 0.000% | Within 0.1%. |
| Bahrain | 2020 | MODIS | 7 | 7 | 7 | 0.000% | 0.000% | Within 0.1%. |
| Bahrain | 2020 | VIIRS | 3165 | 3165 | 3165 | 0.000% | 0.000% | Within 0.1%. |
| Bahrain | 2021 | MODIS | 9 | 9 | 9 | 0.000% | 0.000% | Within 0.1%. |
| Bahrain | 2021 | VIIRS | 2623 | 2623 | 2623 | 0.000% | 0.000% | Within 0.1%. |
| Bahrain | 2022 | MODIS | 14 | 14 | 14 | 0.000% | 0.000% | Within 0.1%. |
| Bahrain | 2022 | VIIRS | 2145 | 2145 | 2145 | 0.000% | 0.000% | Within 0.1%. |
| Bahrain | 2023 | MODIS | 8 | 8 | 8 | 0.000% | 0.000% | Within 0.1%. |
| Bahrain | 2023 | VIIRS | 1959 | 1959 | 1959 | 0.000% | 0.000% | Within 0.1%. |
| Bahrain | 2024 | MODIS | 11 | 11 | 11 | 0.000% | 0.000% | Within 0.1%. |
| Bahrain | 2024 | VIIRS | 2220 | 2220 | 0 | 0.000% | n/a | No baseline JSON detections; daily build adds VIIRS_NOAA20_SP, VIIRS_SNPP_SP. |
| Bahrain | 2025 | MODIS | 4 | 4 | 4 | 0.000% | 0.000% | Within 0.1%. |
| Bahrain | 2025 | VIIRS | 2001 | 2001 | 2001 | 0.000% | 0.000% | Within 0.1%. |
## Scope of the count validation

The 48 exact comparisons check that aggregated detection counts matched CSV row counts for four selected countries and six years. They do not validate FRP sums, country attribution, detection completeness, observation opportunity, the MODIS–VIIRS calibration, its uncertainty band, or the seasonal analytics.

## Comparison with pre-refresh static series

Most existing series totals match exactly. India 2023 VIIRS is 98.070% higher because the refreshed aggregate includes VIIRS S-NPP Standard Processing files absent from the baseline series. For 2024, the previous series JSON has no VIIRS detections for India, Australia, Brazil or Bahrain; the rebuilt totals include VIIRS NOAA-20 and S-NPP Standard Processing files. These are source-coverage additions, not changed observation values. No other comparison differs by more than 0.1%.

## Pipeline and package checks

- Daily build: 18 sensor-year groups, 3,859 country-scoped source files; all files completed. Per product-year Parquet totals are approximately 2.5–2.9 MB. The builder logged free disk after every sensor-year and never crossed the 3 GiB stop threshold. `data/raw/extracted` was read-only.
- Static export: 236 country series, 265,659,156 daily detections, years 2020–2025; the compact exporter output was 115,853,537 bytes (about 110.46 MiB), under its 120 MiB cap. This figure excludes the separate calibration package. The current full frontend/public/data package is about 346 MiB, including 236 harmonized country JSON files (about 235 MiB).
- `npm run check`: PASS in the recorded prior run — TypeScript, ESLint, 15 frontend tests, Vite production build, Ruff, and 46 backend tests (one upstream Starlette/httpx deprecation warning). Not rerun during this documentation-only update.
- Vite reports the lazy MapLibre chunk at about 1.06 MB before gzip; the interactive map remains a separate lazy-loaded chunk.
- Production preview smoke check: PASS — `/`, `data/countries.json`, `data/quality.json` and `data/series/india.json` returned HTTP 200; JSON responses had `application/json` content type.
## Packaged calibration diagnostics (not scientific validation)

The generated methods_validation.json reports method version loglog-theilsen-loyo-v1, median R² 0.79769 in log-FRP space, median holdout MdAPE 0.409015 (about 40.9%), and 167 country fits with LOYO metrics. Confidence counts are 67 High, 65 Medium, and 104 Low. These metrics summarize the implemented experimental statistical method; the raw-count comparisons above do not independently validate them.

The implemented operating-week rule requires both families to have at least one detection on all seven dates somewhere in the combined processed country archive. It does not establish observation opportunity for a selected country or pixel. The calibration metrics are conditional on that selection and on weeks with at least 5 MW vegetation FRP in both families. No independent scientific validation is documented.

- No harmonization, calibration, anomaly or trend claim is validated by the raw-count comparisons.
- At the time of the recorded run, the legacy observations, cell_shards, and manifest were left untouched. In the current checkout, the observations and cell_shards directories are absent; the daily aggregate artifacts remain. This does not change the historical validation result, but it means the old row-level artifacts are not available here.
