# Three-minute demo script (current verified feature set)

**0:00–0:20 — Problem and integrity**

Say: “MODIS and VIIRS see fires at different spatial resolutions. Adding their raw counts together can mislead. FIREWATCH keeps the source measurements separate and makes data coverage visible.”

**0:20–0:50 — Choose an area and period**

1. Open the published URL (currently a placeholder; deploy and verify it first).
2. Search and select **Australia** in the country field.
3. Point out the observed date extent, available years and source-file coverage badge.
4. Explain that incomplete years and blank dates are not zeros.

**0:50–1:40 — Calendar and source comparison**

1. Select an available year, such as 2020.
2. Toggle between source detections and FRP sum.
3. Switch MODIS, VIIRS and All; explain that family totals combine platforms within a family but are not cross-sensor calibrated.
4. Click an active calendar day and read the MODIS/VIIRS values separately.
5. Export the selected-year CSV and calendar PNG.

**1:40–2:10 — Map and history**

1. Scroll to the spatial overview; the interactive map loads when approached.
2. Move the month slider and click a country bubble to select its country.
3. Explain that each bubble is based on observed coordinate centroids and is not a fire perimeter or a country choropleth.
4. Show historical source totals, clearly noting partial coverage.

**2:10–2:40 — Harmonization status**

1. Open **How it works** or the harmonization panel.
2. Say: “This build does not claim a calibrated harmonized index. We need complete paired inputs, observation-opportunity treatment and independent holdout validation first. The comparison panel reports source records only.”

**2:40–3:00 — Limitations and next steps**

Say: “The static snapshot has coverage gaps, NOAA-21 global files are excluded, and the map basemap needs internet access. Next we would validate the complete source archive, calibrate with a predeclared holdout, then add climatology and early-warning measures only after validation.”

Do not demonstrate non-existent anomaly, critical-period or harmonized before/after views. Replace the URL placeholder only after deployment and smoke-testing the hosted site.
