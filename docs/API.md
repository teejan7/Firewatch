# Local analytics API

Run the FastAPI app locally with the commands in `README.md`; interactive OpenAPI docs are at `http://localhost:8000/docs`.

## Processed archive endpoints

- `GET /api/data-quality` returns the local quality report and processed source coverage. A partial archive is labeled `partial_local_archive`.
- `GET /api/coverage` returns expected/processed file counts and source date envelopes by product type, platform, and year. `GET /api/coverage/check?start=2025-01-01&end=2025-01-31&product_type=SP&platform=NOAA-20&bbox=-1,-1,1,1` reports full/partial/no date-envelope coverage and the nearest range or alternate-stream suggestion. A bbox is validated, but spatial coverage remains `not_assessed`; this does not claim observation opportunity.
- `GET /api/calendar?start_date=2025-01-01&end_date=2025-01-31&bbox=-1,-1,1,1&product_type=SP` queries `data/processed/daily_cell/`, partitioned by product type, sensor family, and year. Date windows are limited to 366 days. `bbox` is WGS84 `west,south,east,north`; use either that or `geojson` (a URL-encoded GeoJSON Polygon/MultiPolygon). Optional repeated `platform` values select `Terra`, `Aqua`, `S-NPP`, `NOAA-20`, or `NOAA-21`; `daynight` is `D` or `N`. SP and NRT are queried separately. GeoJSON selection uses grid-cell centers on the common 0.25° grid.
- `GET /api/climatology`, `/api/anomalies`, and `/api/critical-periods` currently return `status: insufficient_baseline` and an empty `results` array. The current files do not support validated multi-year climatology, anomaly, or seasonal claims. These endpoints state why rather than filling missing dates with zeros.

The calendar response is `comparison_only`, carries `calibration_status: insufficient_calibration`, keeps daily sensor/platform statistics distinct, and includes same-cell/date overlap. This is not a count of unique fires or a scientific MODIS/VIIRS conversion. Missing detections are never interpreted as zero activity.

## Bounds and security

Calendar requests are limited to 366 days and run with a 30-second query interrupt. API requests are limited to 120 per client per minute in-process. This lightweight limiter resets on restart and is intended for local use, not as a distributed security control. CORS defaults to `http://localhost:5173` and `http://127.0.0.1:5173`; set `FIREWATCH_CORS_ORIGINS` to a comma-separated list for another frontend origin. Wildcard CORS entries are ignored.

The existing FIRMS live endpoint remains separate and is not called by these local analytics routes. Its MAP_KEY stays server-side. Local archive country endpoints and the Parquet calendar are separate query paths; the calendar currently accepts bbox/GeoJSON and does not invent country polygons.
