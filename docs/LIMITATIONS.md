# FIREWATCH limitations

- Packaged country data covers 3,859 available Standard Processing source files, 265,659,156 detections, 236 country labels, and years 2020–2025. It is not a complete global historical archive; years before 2020 and NOAA-21 country records are not in the package.
- `data/raw/archives/` is empty in this workspace. The extracted CSVs remain local and are not committed. Future processing cannot be independently reproduced from the submitted source package unless the matching archive files are retained or redownloaded.
- NOAA-21 global products are excluded from the country series; a verified country attribution pipeline is not included.
- The dashboard reports source detections and FRP separately by sensor family/platform. No calibrated MODIS-equivalent VIIRS value or cross-sensor comparable trend is published.
- FIRMS active-fire rows do not provide complete sensor observation-opportunity denominators. No detection row cannot be interpreted as confirmed no fire.
- The calendar groups by UTC acquisition date. Overpass time, scan geometry, pixel footprint, confidence/quality filtering, and SP/NRT latency are not normalized into a shared sensor measurement.
- The display map uses 1-degree aggregation and observed coordinates. It is not a fire perimeter or country polygon/choropleth; a Natural Earth boundary crosswalk was not included.
- Climatology, anomaly scores, percentile ranks, critical-period dates, and early-warning flags are not implemented in the active dashboard.
- The map basemap is a third-party CARTO hosted style and needs an internet connection. The data dashboard itself is static and needs no backend.
- This software/data audit is not an independent scientific review. See [Methodology](METHODOLOGY.md) and [Validation](VALIDATION.md).
