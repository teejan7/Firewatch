# FIREWATCH methodology

## Active dashboard and source metrics

FIREWATCH is a country-level explorer of packaged NASA FIRMS Standard Processing (SP) active-fire records. The active React app loads static JSON; it does not call NASA or the FastAPI service. The package covers 2020–2025 and includes MODIS Terra/Aqua, VIIRS Suomi-NPP, and VIIRS NOAA-20 country records. NOAA-21 country records are not included.

Daily source-series records are grouped by source country label, UTC acquisition date, sensor family, platform, and product. Detection counts count FIRMS records, not unique fires or fire perimeters. FRP is the reported sum in megawatts (MW). The default raw calendar summaries include all detection types. Separate generated fields retain vegetation-only values (FIRMS type=0), nominal/high-confidence-filtered values, day/night values, and a platform-day detection flag. That flag means at least one detection was reported; it does not measure whether the satellite observed the country or location.

For the confidence-filtered aggregate, MODIS numeric confidence values of 30 or higher and VIIRS nominal/high categorical values are included. NASA's MODIS guide defines low as 0–<30, nominal as 30–<80, and high as 80–100, and describes nominal-plus-high filtering as one possible tradeoff against false alarms. VIIRS confidence classes have product-specific meanings. This is a documented data filter, not evidence that confidence values are interchangeable between sensors. See the [NASA MODIS guide](https://www.earthdata.nasa.gov/s3fs-public/2023-09/MODIS_C6_C6.1_Fire_User_Guide_1.0.pdf) and [NASA VIIRS guide](https://viirsland.gsfc.nasa.gov/PDF/VIIRS_activefire_User_Guide.pdf).

## Processing path

1. Local FIRMS country CSVs are read-only inputs to backend/scripts/build_daily.py. The builder uses DuckDB to aggregate the CSVs directly, rather than retaining a row-level copy in this pipeline.
2. Compact Parquet outputs retain daily country/platform rows and 1-degree display-grid rows, plus source filename, product, platform, source row count, available processing-version metadata, and field-availability flags. The daily manifest records per-source processing state and file signatures.
3. backend/scripts/build_compact.py reads the daily manifest and Parquet aggregates to generate the browser JSON. It writes the country index and series, map summaries, coverage metadata, and quality metadata under frontend/public/data.
4. backend/scripts/run_harmonize.py reads vegetation-only daily Parquet aggregates and writes separate country-level calibration, multi-year, and seasonal JSON outputs. It does not modify the raw source series.

The original CSV files are not in the GitHub repository and are absent from the current development checkout. Restoring the matching source files is necessary to reproduce the full source-coverage inventory and repeat raw-count validation. See [Data and coverage](DATA.md) and [Data engine](DATA_ENGINE.md).

## Experimental MODIS–VIIRS calibration

The static analytics use vegetation-only FRP (type=0), aggregated by country and week. The model treats MODIS weekly FRP as the reference and fits it from VIIRS weekly FRP with a Theil–Sen log-log relationship:

- ln(MODIS weekly FRP) = intercept + slope × ln(VIIRS weekly FRP).
- A week enters the country fit only when each sensor family has at least 5 MW of vegetation FRP.
- A country-specific fit requires at least 40 qualifying weeks. Otherwise, a deterministic global fallback is used and the country is marked Low confidence.
- Leave-one-calendar-year-out (LOYO) predictions calculate country fit metrics where a fold has enough training and test weeks. Final country coefficients are then fit on all qualifying weeks.
- R² is computed between log observed MODIS FRP and log predicted MODIS FRP. MdAPE is the median absolute percentage error in the original FRP scale.

The generated methods_validation.json reports median R² 0.79769 and median holdout MdAPE 0.409015 (about 40.9%) across 167 country fits with LOYO metrics. It reports 67 High, 65 Medium, and 104 Low country calibrations. These are internal method outputs, not independent scientific validation. The confidence thresholds are internal decision rules, not NASA quality categories.

The operating-week rule is a limitation: a week is considered eligible when both sensor families have at least one detection on each of its seven dates somewhere in the processed country archive. It does not establish country-specific or pixel-level observation opportunity. Country series are expanded against this shared week set; missing country-week values are filled with zero for parts of the generated analytics. Therefore blank or absent detections must not be interpreted as proof of no fire or confirmed observation.

The weekly output combines MODIS and calibrated VIIRS FRP by a geometric mean when both are present, and uses the one available value when only one is present. Its displayed band is based on ±1.96 residual standard deviations in log space; it is not an independently calibrated uncertainty interval. The calendar's daily harmonized display instead adds raw MODIS daily FRP to VIIRS daily FRP multiplied by that week's scale. This daily display formula differs from the core weekly composite.

This is an exploratory statistical calibration, not a physical retrieval correction, a sensor-equivalence claim, or independently validated harmonization. Differences in spatial footprint, detection algorithm, overpass time, platform mix, and observation opportunity remain. The internal LOYO evaluation is conditional on the selected qualifying weeks and does not validate missed detections or fire-free periods.

## Preliminary multi-year calculations

The dashboard marks the multi-year calendar, typical activity chart, unusual-week flags, and fire-season dates as preliminary, using the 2020–2025 six-year package. Typical ranges are day-of-year medians and 25th–75th percentiles over the generated series. “Unusual” means strictly above the selected country's six-year 90th percentile; it is a descriptive percentile flag, not a validated anomaly or risk score. Fire-season start/end use cumulative 5%/95% of annual weekly FRP and peak is the maximum weekly FRP date. The operating-week and missing-value limitations also affect these summaries.

## Maps and coverage

The active global map shows country-level summary bubbles at observed-record centroids, with totals filtered by year and optionally month. It is not a point map, fire perimeter, country boundary map, or spatially matched sensor comparison. Its CARTO basemap is hosted externally and requires internet access.

Coverage indicators describe completeness of discovered source files represented in the packaged metadata. A complete source-file set does not mean continuous observation opportunity. The absence of a row or calendar record is not a confirmed zero-fire observation.

## Related documentation

- [Data and coverage](DATA.md)
- [Exploratory calibration and API comparison](HARMONIZATION.md)
- [Validation record](VALIDATION.md)
- [Limitations](LIMITATIONS.md)