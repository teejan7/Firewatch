# FIREWATCH user guide

FIREWATCH is a local, static explorer for the packaged FIRMS Standard Processing (SP) active-fire records. It presents source detections and fire radiative power (FRP) by sensor family. It does not currently produce a harmonized index, climatology, anomaly, critical-period, or early-warning result.

## Explore the dashboard

1. Use **Country** to search and select one of the packaged country series. The selected country is the area of interest; custom drawn areas are not available.
2. Choose a year available for that country. The calendar is one year at a time and follows UTC acquisition dates.
3. Choose **All**, **MODIS**, or **VIIRS**, then select source detections or FRP sum. The values remain source-specific and should not be compared as equivalent measurements across sensors.
4. Read the coverage badge before interpreting an empty date. Partial source-file coverage means some expected files are not included. Even a complete file set does not mean continuous satellite observation.
5. Select a calendar cell to read that date's sensor-family totals. A date with no packaged detections is not evidence that no fire occurred.
6. Use the spatial overview to inspect country activity centroids. Points are not fire perimeters or country boundaries; the map needs an internet connection for basemap tiles.
7. Export the selected country and year as CSV, or save the calendar as PNG. Exports identify source-only values and do not present calibrated estimates.

## Try these views

Select India, Australia, Indonesia, or Brazil from the country selector, then use only the years actually listed for that country. Do not expect a 2019–20 Australia event comparison in this package: the packaged country series do not include 2019.

## Method and limits

Open **How it works** for the current processing outline and limitations. MODIS and VIIRS records remain separate. FIREWATCH has not fitted or validated a cross-sensor calibration. The historical panel is a source-total view, not an anomaly or trend analysis.
