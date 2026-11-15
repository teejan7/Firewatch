# Data coverage and interpretation limits

- FIRMS active-fire detections are satellite detections, not verified wildfire perimeters or a complete census of fires.
- MODIS and VIIRS differ in nominal pixel size, sensitivity, overpass timing, confidence conventions, and FRP retrieval. Raw counts and FRP are not sensor-equivalent.
- Same 0.25-degree cell and date is a spatial-temporal overlap indicator, not a matched fire event. A cell can contain multiple fires; one event may span cells.
- The processed archive is determined by files present on the local machine and listed in `data/processed/manifest.json`. Missing years, products, countries, or failed files must not be interpreted as no activity.
- The archive does not supply observation-opportunity denominators for each cell/time. A missing detection cannot be treated as a confirmed zero.
- NRT is operational and can contain gaps or later be replaced by SP records. Product type is selected explicitly and must not be pooled silently.
- No anomaly scores, calibrated trends, global rankings, or scientific harmonization claims are produced by the comparison module.
- Input CSVs may be locally obtained FIRMS files. FIREWATCH preserves source/product/platform metadata but does not independently checksum or certify provenance; retain original downloads and their accompanying documentation.

See [HARMONIZATION.md](HARMONIZATION.md) for the exploratory comparison definition and [DATA_ENGINE.md](DATA_ENGINE.md) for local processing and quality manifests.
