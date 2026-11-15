# Next steps after the deadline

1. **Complete data inventory:** acquire/verify matching archives for missing years and products. Keep extracted CSVs when the matching archive is absent. Verify country-name and product mappings before processing. NOAA-21 global files need an explicit, validated country-attribution workflow before inclusion.
2. **Rebuild full coverage:** process one sensor/year at a time into validated compact outputs. Record source checksums, product collection, processing stream, file completeness and quality-rule counts.
3. **Design calibration with domain review:** predefine matched spatial/temporal units, quality filters, FRP/count metrics, training period, holdout period and confidence thresholds. Account for footprint size, scan geometry, overpass timing and sensor/platform changes. Keep raw measurements unchanged and the transform versioned/replaceable.
4. **Validate independently:** publish training and holdout metrics by sensor, platform, country and period; report failure and low-confidence cases. Seek remote-sensing/fire-science review before using “harmonized”.
5. **Add decision analytics only when supported:** compute climatology, percentile/anomaly and fire-season summaries only for areas with adequate complete baseline and a validated metric. Document missingness, uncertainty and leave-one-year-out decisions.
6. **Add AOI options:** support verified administrative polygons or user-supplied geometry, with area calculations and boundary provenance.
7. **Operational sources:** consider live near-real-time FIRMS only with server-side key handling, quotas, caching, attribution and a clear distinction between NRT and Standard Processing data. This static version has no live NRT connection.
8. **Release assurance:** verify clean-clone build, deployed base path, mobile interaction, downloads, map network fallback and hosted URL; capture screenshots only from that verified release.
