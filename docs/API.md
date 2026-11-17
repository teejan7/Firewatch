# Optional local FastAPI prototype

The FastAPI service is separate from the active static dashboard. The default frontend entry point renders StaticApp and reads packaged JSON; it does not call these endpoints. Start the API from the project root with npm run api. Interactive OpenAPI documentation is available at http://localhost:8000/docs. The API is intended for local use and is not required to run or build the active dashboard.

## Routes

- GET /api/health reports whether legacy daily-cell data is available and whether a FIRMS key is configured. It does not verify the static dashboard JSON.
- GET /api/firms/latest and GET /api/firms/archive query the NASA FIRMS area CSV service. They require a server-side FIRMS_MAP_KEY. Keep the key out of frontend code.
- POST /api/ingest/firms accepts a UTF-8 FIRMS CSV preview up to 10 MB, validates it, and returns parsed records. It does not save the upload or add it to the dashboard.
- GET /api/local-archive/countries, /api/local-archive/catalog, /api/local-archive/records, and /api/local-archive/calendar query CSVs under data/raw/extracted. That source folder is absent in the current checkout.
- GET /api/data-quality and GET /api/coverage expose legacy local processing metadata. GET /api/coverage/check reports source-file date-envelope ranges and suggestions; spatial observation opportunity remains unassessed.
- GET /api/calendar queries older data/processed/daily_cell data, if available. It supports a date range up to 366 days, SP or NRT selection, optional platform and day/night filters, and either a WGS84 bounding box or GeoJSON Polygon/MultiPolygon. GeoJSON selection uses common-grid cell centers.
- GET /api/climatology, GET /api/anomalies, and GET /api/critical-periods currently return insufficient_baseline with empty results. They do not compute these products.

## Comparison semantics

The API calendar is comparison-only. It reports detected cell-days and same-cell/same-date overlap while keeping sensor and platform statistics separate. It does not count unique fires, perform event matching, estimate missed detections, or convert VIIRS FRP to MODIS-equivalent FRP. Missing detections are not zero-fire evidence. This API path is distinct from the experimental static-dashboard calibration documented in [Harmonization](HARMONIZATION.md).

## Bounds and security

Calendar requests are limited to 366 days and run with a 30-second query interrupt. API requests are limited to 120 per client per minute in-process; the limiter resets on restart and is not a distributed security control. CORS defaults to localhost:5173 and 127.0.0.1:5173; FIREWATCH_CORS_ORIGINS can set a comma-separated list for another frontend origin. Wildcard CORS entries are ignored.

The upload and local archive routes are not persistent storage. Do not expose this development API publicly without a separate security review. FIRMS live/archive access uses the server-side key and is not used by the active static dashboard.