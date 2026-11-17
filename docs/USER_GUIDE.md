# FIREWATCH user guide

FIREWATCH is a country-level fire activity explorer built using NASA FIRMS satellite observations. It brings together historical MODIS and VIIRS data through interactive daily calendars, geospatial visualization, data processing pipelines, and exploratory cross-sensor FRP calibration.

The active dashboard is static and uses packaged data for 2020–2025. It is not a live NASA service, fire prediction system, or early-warning system. The multi-year views and calibration are preliminary.

## Explore the dashboard

1. Use **Country** to search for and select a country label present in the packaged index. The selection is country-level; arbitrary AOI drawing and boundary selection are not available.
2. Choose a year listed for that country. The main calendar shows one full UTC year, not an arbitrary date range.
3. Choose **All**, **MODIS**, or **VIIRS**, and select **Source detections** or **FRP sum (MW)**. Raw calendar values include all detection types and are descriptive totals. MODIS and VIIRS values are not equivalent measurements.
4. Read the file-coverage badge. It describes source-file completeness represented in the package; even a complete file set does not prove that a satellite observed every place on every date.
5. Select a calendar day to see separate MODIS and VIIRS totals. A blank day means no packaged record for that selection, not confirmed absence of fire.
6. In the spatial overview, set the map to a full year or a month. Bubbles show country summary totals at observed-record centroids; they are not fire detections, perimeters, or country boundaries. The map basemap needs an internet connection.
7. Use the **Raw sensors / Harmonized** toggle to switch the calendar and preliminary multi-year views. The experimental calibration uses vegetation-only records (type=0); raw calendar totals include all types. In harmonized mode, the sensor selector is disabled and detection counts remain raw; the calibration applies to FRP only. The map and historical source-total chart remain raw descriptive summaries.
8. The lower analytics show a 2020–2025 day-of-year heatmap and typical range, flags for values above the six-year 90th percentile, and preliminary 5%–95% cumulative-FRP season dates. These are descriptive experimental calculations, not validated anomalies or forecasts.

## Exports

- **Export selected year CSV** exports the selected country's source-series aggregates for the selected year and sensor filter, with available source-file and processing metadata. It does not export the calibrated series.
- **Save calendar PNG** saves an image of the currently displayed calendar. Its explanatory caption may still describe values as source-only while the calendar is in harmonized FRP mode; interpret the selected mode in the dashboard itself.

## How to run

Install Node.js 20+ and npm, then from the project root run:

~~~powershell
npm install
npm run start
~~~

The static dashboard does not require FastAPI, a NASA key, or local source CSVs. The map basemap requires network access. See [README](../README.md) for the optional API and [Methodology](METHODOLOGY.md) for processing details.

## Interpretation and method

FIRMS detection counts are detection records, not unique fires. FRP is reported in MW. The static calibration is an exploratory Theil–Sen log-log fit of weekly country vegetation FRP with a 5 MW qualifying threshold and a minimum of 40 qualifying weeks for a country-specific fit. The median holdout MdAPE is approximately 40.9%, and the internal LOYO evaluation is not independent scientific validation. The operating-week rule does not establish country-specific observation opportunity. Missing dates must not be interpreted as zero fire activity. Read [Harmonization](HARMONIZATION.md), [Limitations](LIMITATIONS.md), and [Validation](VALIDATION.md) before interpreting comparisons.