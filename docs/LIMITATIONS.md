# FIREWATCH limitations

## Data and coverage

- The packaged dashboard covers 2020–2025 and its generated metadata reports 3,859 Standard Processing source files, 265,659,156 detection records, and 236 country labels. It includes MODIS Terra/Aqua, VIIRS Suomi-NPP, and VIIRS NOAA-20. It is not a complete global archive or a complete history of every platform.
- NOAA-21 country records are not included in the active dashboard. Its optional API prototype has separate source options, but those are not the packaged static data.
- Original FIRMS CSVs are not in the repository. In the current development checkout, data/raw/extracted is absent. The raw-count validation documented in VALIDATION.md therefore cannot be repeated in this checkout until inputs are restored.
- The compact pipeline can be rebuilt from extracted FIRMS country CSVs. Rebuilding coverage metadata without those CSVs can report missing expected source-file coverage even if daily Parquet aggregates remain.
- Generated quality metadata reports zero invalid and duplicate rows, but the current compact exporter does not independently count duplicates and derives its invalid counter from aggregate counts that are set equal. Do not use those zeros as evidence that source files contain no invalid or duplicate records.

## Scientific interpretation

- Detection counts are FIRMS records, not counts of unique fires, fire perimeters, or a complete census of wildfire events. Raw calendar/map summaries include all detection types. The experimental calibration uses vegetation-only records (type=0).
- FRP is the product-reported fire radiative power in MW. MODIS and VIIRS FRP values are not automatically equivalent and are not normalized for spatial footprint, detection behavior, overpass opportunity, or platform differences.
- The active static calibration is an exploratory country-week statistical fit, not a physical retrieval correction or independently validated harmonized observation product. Its median holdout MdAPE is about 40.9%; R² is computed in log-FRP space. See [Harmonization](HARMONIZATION.md) and [Validation](VALIDATION.md).
- The operating-week criterion is based on detections from both families on all seven dates somewhere in the processed country archive. It does not establish observation opportunity for a specific country or pixel. Some generated views fill missing country-week values with zero; missing records still do not establish confirmed no fire.
- The multi-year typical ranges, >90th-percentile unusual-week flags, and cumulative-FRP fire-season dates are preliminary calculations over only six years. They are not validated anomalies, risk estimates, or predictions.
- Source-file completeness means files in the local discovered inventory were processed; it does not mean continuous satellite observations or spatially complete coverage.
- Country names come from FIRMS source-file labels. The active map shows country-level summary bubbles at observed centroids, not official boundaries or fire perimeters.

## Application boundary

- The active dashboard is static and uses packaged JSON. It does not fetch live NASA FIRMS data, include persistent uploads, or require FastAPI at runtime.
- The FastAPI and API-driven frontend path are separate optional prototypes and are not mounted by the default React entry point. FIRMS API endpoints require a server-side key; CSV upload is a limited preview, not persistent ingestion.
- The CARTO basemap is hosted externally and requires internet access.
- This documentation describes implementation and stored validation records. It is not an independent scientific review or endorsement for operational response decisions.