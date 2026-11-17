# MODIS–VIIRS comparison and exploratory calibration

FIREWATCH contains two distinct cross-sensor paths. They serve different purposes and should not be conflated.

## Active static-dashboard calibration (experimental)

The active dashboard loads precomputed country results produced by backend/scripts/run_harmonize.py using the model in backend/scripts/harmonize_core.py. The input is weekly country-level vegetation FRP (FIRMS type=0) from MODIS Terra/Aqua and VIIRS Suomi-NPP/NOAA-20. MODIS is the target/reference; Theil–Sen regression fits a log-log relationship from VIIRS FRP to MODIS FRP.

A weekly country record qualifies for fitting only when both families have at least 5 MW vegetation FRP. A country model requires at least 40 such weeks. Countries below that requirement use the deterministic global fallback and receive Low confidence. Leave-one-calendar-year-out (LOYO) metrics are computed where folds have enough training and test weeks. The packaged methods_validation.json reports median R² 0.79769 and median holdout MdAPE 0.409015 (about 40.9%) for 167 country fits with LOYO metrics. R² is computed in log-FRP space. These results are exploratory and do not constitute independent scientific validation. The confidence thresholds are method rules, not NASA quality classes.

The eligibility rule is not an observation-opportunity model: both families must have detections on each of seven dates somewhere in the combined processed country archive. It does not prove that a given country or pixel was observed on those dates. The subsequent country-week expansion fills missing values with zero for some outputs. Missing dates therefore must not be read as confirmed no-fire observations.

For weeks where both families have FRP, the core weekly output combines MODIS and calibrated VIIRS with a geometric mean; where only one has a value, it uses that value. The displayed residual band uses ±1.96 log-residual standard deviations and is not an independently validated confidence interval. The daily calendar applies a weekly scale to daily VIIRS and adds it to raw daily MODIS; this display formula is not the same as the core weekly composite. The lower multi-year views use the preliminary six-year baseline. Full details are in [Methodology](METHODOLOGY.md) and [Limitations](LIMITATIONS.md).

This is exploratory statistical calibration, not a physical retrieval correction, sensor-equivalence claim, or independently validated harmonization product.

## Optional FastAPI comparison API (not the static calibration)

The separate backend/app/harmonize.py module and GET /api/calendar endpoint produce a comparison-only common-grid summary from legacy daily-cell Parquet files. They report detected cell-days and same-cell/same-date overlap, plus sensor/platform-specific record totals and FRP. Cell overlap is not event matching, a unique-fire count, or a MODIS-to-VIIRS conversion. The API response deliberately reports insufficient calibration and does not produce a harmonized index.

That API is optional and is not called by the default static React dashboard. The API may query a 0.25-degree grid; the active dashboard's map is a different country-centroid summary. See [API documentation](API.md) and [Data engine](DATA_ENGINE.md).

## Why comparison needs care

MODIS and VIIRS active-fire products differ in spatial footprint, detection characteristics, confidence conventions, overpass timing, FRP retrieval, platforms, and processing histories. A common grid or country-week regression does not correct these differences. FIRMS detection records also do not provide complete per-location observation-opportunity denominators. Do not infer that a missing record means a sensor observed the location and found no fire.

The active package contains 2020–2025 Standard Processing country files for MODIS Terra/Aqua, VIIRS Suomi-NPP, and VIIRS NOAA-20. NOAA-21 country records, live updates, arbitrary AOI selection, and independent validation of cross-sensor harmonization are not available in the active dashboard.

## References

- [NASA MODIS active-fire user guide](https://cdn.earthdata.nasa.gov/conduit/upload/10575/MODIS_C6_Fire_User_Guide_B.pdf)
- [NASA VIIRS active-fire user guide](https://viirsland.gsfc.nasa.gov/PDF/VIIRS_activefire_User_Guide.pdf)
- [FIRMS active-fire archive notes](https://firms.modaps.eosdis.nasa.gov/content/active_fire/)
- [NASA FIRMS data and tools](https://www.earthdata.nasa.gov/data/tools/firms)