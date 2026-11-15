# FIREWATCH comparison method (exploratory)

## Status

This module implements a versioned, comparison-only common-grid summary. It does **not** calibrate MODIS and VIIRS, estimate missed detections, or claim that the sensors are equivalent. The API returns `calibration_status: insufficient_calibration` and `harmonized_index: null` by design.

## Method v1.0.0

MODIS active-fire products use an approximately 1 km nominal pixel, while the VIIRS 375 m active-fire product uses a finer nominal pixel. Their detection characteristics, confidence fields, overpass timing, FRP retrievals, and platform/processing histories differ. Processed detections are assigned to a global 0.25-degree latitude/longitude grid by `build_processed.py`; this supports an exploratory common spatial index but does not make those sensor measurements equivalent. For a requested date interval, the comparison query:

1. Selects one processing stream (`SP` or `NRT`) explicitly, and optionally platform, day/night, and bounding-box filters.
2. Treats a cell on a UTC date with at least one source record as one **detected cell-day** for that sensor family and platform.
3. Reports the union of positive cell-days, MODIS/VIIRS detected-cell-days, and same-cell/same-date overlap. This overlap is not an event match or a unique-fire count.
4. Reports raw record totals and FRP only by product/platform. FRP values are never summed across sensors.

No absent row is converted to zero fire activity. A CSV detection archive does not supply per-cell observation opportunity, so the query cannot tell whether an undetected cell was observed or whether a fire was missed. The grid is intentionally coarse relative to nominal sensor pixels; it is a shared spatial index, not a resolution correction. Bounding boxes crossing the antimeridian are rejected.

## Calibration gate

No cross-sensor regression, scaling coefficient, anomaly, or comparable trend is published. A future calibration must be a separately versioned replacement with documented product collection/version, quality filters, co-observation opportunity, event matching, duplicate rules, spatial/temporal validation split, independent validation metrics, uncertainty, and coverage. It must retain all sensor-specific source records. The official challenge resources and product documentation must be reviewed before selecting that method.

SP and NRT are deliberately separated. NASA documentation notes that NRT data are operational and may have coverage gaps; prefer Standard Processing for latency-insensitive retrospective work. Never pool streams silently.

## References

- [NASA MODIS active fire product user guide](https://cdn.earthdata.nasa.gov/conduit/upload/10575/MODIS_C6_Fire_User_Guide_B.pdf)
- [NASA VIIRS 375 m active fire product user guide](https://www.earthdata.nasa.gov/s3fs-public/2024-07/VIIRS_C2_AF-375m_User_Guide_1.0.pdf)
- [FIRMS active fire archive notes](https://firms.modaps.eosdis.nasa.gov/content/active_fire/)
- [NASA FIRMS data and tools](https://www.earthdata.nasa.gov/data/tools/firms)

The guide links describe product characteristics; they do not validate FIREWATCH's exploratory grid metric as a scientific harmonization product.
