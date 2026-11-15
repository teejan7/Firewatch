# FIREWATCH test plan

| Feature | Steps | Expected result | Current verification |
|---|---|---|---|
| Static data startup | Run `npm run start` with backend stopped | App loads the packaged country index; no API key is needed | Unit-tested request URLs; browser check pending |
| Country selection | Search and select a country | Corresponding series and coverage display | Unit test covers selection/load; full browser interaction pending |
| Missing series response | Return HTML with HTTP 200 for a JSON series URL | Actionable non-JSON data error; no parser-only blank screen | Unit test added |
| Calendar | Choose year and sensor/metric | UTC daily cells reflect packaged source values; empty dates are not described as no fire | Browser/e2e verification pending |
| Spatial overview | Load map and select a country marker | Marker selection updates country; basemap failure leaves other controls usable | Browser/e2e verification pending |
| Coverage and method disclosure | Select a country/year | Partial archive and non-calibrated status are visible | Unit test covers partial coverage and method dialog |
| CSV export | Export selected year | CSV includes source/provenance columns and guards spreadsheet formula prefixes | Manual download/content verification pending |
| PNG export | Save calendar | Downloaded image includes country, year, metric, and non-harmonized source note | Manual download verification pending |
| Responsive layout | Inspect at narrow viewport | Controls remain usable without page-level horizontal overflow | Viewport screenshot and keyboard review pending |
| Data integrity | Compare exported counts to raw sources and scan JSON for invalid numeric values | Counts reconcile and JSON has no non-finite numeric values | Existing January 2020 spot checks; broader checks pending |

Run `npm run typecheck`, `npm run lint`, `npm test`, `npm run build`, and `.venv\Scripts\python.exe -m pytest backend\tests` before release. Mark checks with the command output and date in `docs/VALIDATION.md`; do not record unrun checks as passing.
