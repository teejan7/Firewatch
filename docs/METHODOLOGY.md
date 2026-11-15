# FIREWATCH methodology

## Current published metric

The current static data method version is **firewatch-static-0.2**. `backend/scripts/build_daily.py` streams local FIRMS Standard Processing CSVs with DuckDB and writes one small Parquet per source country file under `data/processed/daily/<family>/<platform>/<year>/`. Each Parquet holds daily country/platform rows and 1-degree map-cell rows, distinguished by `aggregation_level`; DuckDB grouping sets calculate both in a single input scan. The builder reads only needed CSV columns, uses a 2 GiB DuckDB memory limit and four threads, and creates a temporary DuckDB spill directory for each sensor-year which is cleaned after that sensor-year. It does not create a row-level Parquet intermediate or modify raw CSVs. The independent checkpoint `data/processed/daily_manifest.json` records source file, size, modification time, row count, aggregate row count, status, output size and metadata. Its schema/aggregate format version prevents old separate daily/grid Parquets from being mistaken for the new format. The static exporter reads only daily aggregate files and this manifest.


Daily outputs also retain vegetation-only count and FRP (FIRMS type = 0), quality-filtered count and FRP, day/night counts and FRP, and a platform-day flag. The flag means at least one detection was reported for that country/platform/date; it is not a sensor observation-opportunity denominator. Original file identity, product, source row count, processing version when present, confidence field name and field-availability metadata remain attached.

The quality-filtered subset is an explicit display filter, not calibration: for MODIS numeric confidence, nominal and high classes are included at confidence >=30; for VIIRS categorical confidence, nominal and high classes are included (`n`/`h` and full labels). NASA's MODIS guide defines low as 0–<30, nominal as 30–<80, and high as 80–100, and notes that nominal+high may be retained to reduce false alarms. The VIIRS guide describes low/nominal/high as product classes with product-specific algorithmic meaning. See [NASA MODIS C6/C6.1 Fire User Guide](https://www.earthdata.nasa.gov/s3fs-public/2023-09/MODIS_C6_C6.1_Fire_User_Guide_1.0.pdf) and [NASA VIIRS Active Fire User Guide](https://www.earthdata.nasa.gov/sites/default/files/imported/VIIRS_activefire_User_Guide.pdf). If confidence is missing, availability is flagged and the qualifying count is zero; this is not a sensor-quality finding.
The activity calendar can display the sensor family values separately or together as a descriptive total. A combined total is **not** a MODIS-equivalent estimate. FRP is an instrument retrieval and the two sensors have different pixel sizes, detection characteristics and overpass opportunities.

## Map aggregation

Map markers aggregate detected rows into 1-degree latitude/longitude display cells by source country label, year, family, platform and product. Cell coordinates are display-bin centers. They do not indicate administrative borders, fire perimeters, detection uncertainty, or comparable sensor resolution. The base map is a remote CARTO style; FIREWATCH data itself is loaded from static JSON.

## Coverage rules

The exporter compares each extracted country/product/year CSV name with the independent daily manifest and expected aggregate output. It marks a product/year complete only when every matching local file has a complete daily aggregate. A processed file's date envelope does not establish that every location was observed on every date. NOAA-21 global files are excluded from the country-level static export because no validated country attribution step is included.

## Harmonization gate

FIREWATCH currently has **no harmonized index**. The common grid in the optional backend tool is a spatial comparison unit, not a sensor correction. Fitting weekly MODIS and VIIRS totals directly would still leave major unresolved issues: non-coincident overpasses, unknown observation opportunity for non-detections, mixed platform/product histories, incomplete source coverage, and no independently validated uncertainty model.

Before a new calibration version can be called harmonization, it needs reviewed official collection/version definitions, documented quality rules, a defensible same-area observation opportunity or event-match design, complete training/holdout coverage, platform continuity checks, country-level independent validation, uncertainty, and review by a fire/remote-sensing domain expert. Training and holdout periods must be selected before fitting. Outputs must keep raw sensor data and make the calibration replaceable.

## Climatology and critical periods

No anomalies, z-scores, percentile rankings, or fire-season start/peak/end are published. Those analyses require a validated metric, documented completeness, a defined seasonal method and a sufficiently long baseline. The dashboard requires at least ten complete baseline years before showing these results; the current packaged years do not satisfy that rule.
