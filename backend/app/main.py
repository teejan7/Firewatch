import os
import threading
import time
from datetime import date
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from app.validation import CsvValidationError, parse_firms_csv
from app.firms import AREAS, ARCHIVE_SOURCES, FirmsApiError, SOURCES, load_archive, load_latest
from app.local_archive import available_countries, available_products, load_country_window, summarize_country_month
from app.analytics_api import DAILY_CELLS, AnalyticsQueryError, AnalyticsTimeout, coverage_status, get_calendar, unavailable_analysis, validate_bbox

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

app = FastAPI(title="FIREWATCH data API", version="0.3.0", description="Local NASA FIRMS exploration and sensor-aware comparison. No cross-sensor calibration is claimed.")
cors_origins = [origin.strip() for origin in os.getenv("FIREWATCH_CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",") if origin.strip()]
cors_origins = [origin for origin in cors_origins if origin != "*"]
app.add_middleware(CORSMiddleware, allow_origins=cors_origins, allow_methods=["GET", "POST", "OPTIONS"], allow_headers=["Content-Type"])

_rate_lock = threading.Lock()
_rate_windows: dict[str, list[float]] = {}


@app.middleware("http")
async def limit_api_rate(request, call_next):
    """Apply a modest per-client API request limit without storing request paths or keys."""
    if request.url.path.startswith("/api/"):
        now = time.monotonic()
        client = request.client.host if request.client else "unknown"
        with _rate_lock:
            recent = [stamp for stamp in _rate_windows.get(client, []) if now - stamp < 60]
            if len(recent) >= 120:
                from starlette.responses import JSONResponse
                return JSONResponse(status_code=429, content={"detail": "Request limit reached; wait a minute and retry."})
            recent.append(now)
            _rate_windows[client] = recent
            if len(_rate_windows) > 10000:
                _rate_windows.clear()
    return await call_next(request)


@app.get("/api/health")
def health():
    local_ready = DAILY_CELLS.is_file()
    return {"status": "ok", "data_status": "Processed local FIRMS archives" if local_ready else "Simulated demo data",
            "local_analytics_available": local_ready,
            "firms_api_configured": bool(os.getenv("FIRMS_MAP_KEY", "").strip()),
            "harmonization": "comparison only; calibration insufficient" if local_ready else "not applied"}


@app.get("/api/firms/latest")
def firms_latest(
    source: str = Query("VIIRS_NOAA21_NRT"),
    area: str = Query("world"),
    days: int = Query(1, ge=1, le=5),
):
    if source not in SOURCES:
        raise HTTPException(status_code=422, detail=f"Unsupported live source. Choose one of: {', '.join(sorted(SOURCES))}.")
    if area not in AREAS:
        raise HTTPException(status_code=422, detail=f"Unsupported area. Choose one of: {', '.join(AREAS)}.")
    try:
        records = load_latest(source, area, days)
    except FirmsApiError as exc:
        status = 503 if "FIRMS_MAP_KEY is not configured" in str(exc) else 502
        raise HTTPException(status_code=status, detail=str(exc)) from exc
    return {"count": len(records), "records": records, "data_status": "NASA FIRMS API", "dataset": source, "area": area, "days": days, "harmonization": "not applied", "source_metadata": "original CSV fields retained"}


@app.get("/api/firms/archive")
def firms_archive(
    source: str = Query("VIIRS_NOAA21_SP"),
    area: str = Query("world"),
    start_date: date = Query(...),
    days: int = Query(1, ge=1, le=5),
):
    if source not in ARCHIVE_SOURCES:
        raise HTTPException(status_code=422, detail=f"Unsupported Standard Processing source. Choose one of: {', '.join(sorted(ARCHIVE_SOURCES))}.")
    if area not in AREAS:
        raise HTTPException(status_code=422, detail=f"Unsupported area. Choose one of: {', '.join(AREAS)}.")
    try:
        records = load_archive(source, area, days, start_date)
    except FirmsApiError as exc:
        status = 503 if "FIRMS_MAP_KEY is not configured" in str(exc) else 502
        raise HTTPException(status_code=status, detail=str(exc)) from exc
    return {"count": len(records), "records": records, "data_status": "NASA FIRMS Standard Processing archive", "dataset": source, "area": area, "start_date": start_date.isoformat(), "days": days, "harmonization": "not applied", "source_metadata": "original CSV fields retained"}


@app.post("/api/ingest/firms")
async def ingest_firms(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=415, detail="Upload a .csv file exported from FIRMS.")
    content = await file.read(10_000_001)
    if len(content) > 10_000_000:
        raise HTTPException(status_code=413, detail="File exceeds the 10 MB preview limit. Split the CSV into smaller files and retry.")
    try:
        records = parse_firms_csv(content)
    except CsvValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"count": len(records), "records": records, "data_status": "User-provided FIRMS CSV", "harmonization": "not applied", "source_metadata": "original columns retained"}


@app.get("/api/local-archive/countries")
def local_archive_countries(year: int = Query(2025, ge=2000, le=2100)):
    try:
        countries = available_countries(year)
        products = available_products(year)
    except FirmsApiError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"year": year, "countries": countries, "products": products, "data_status": "Local NASA FIRMS country archives"}


@app.get("/api/local-archive/catalog")
def local_archive_catalog(year: int = Query(..., ge=2000, le=2026)):
    try:
        products = available_products(year)
        countries = available_countries(year)
    except FirmsApiError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"year": year, "products": products, "countries": countries, "data_status": "Local NASA FIRMS Standard Processing archives"}


@app.get("/api/local-archive/records")
def local_archive_records(
    country: str = Query(..., min_length=1, max_length=80),
    year: int = Query(2025, ge=2000, le=2100),
    start_date: date = Query(...),
    end_date: date = Query(...),
    products: str | None = Query(None, description="Comma-separated local products; defaults to products available for the selected year"),
):
    try:
        selected_products = [value.strip() for value in products.split(",") if value.strip()] if products else None
        records = load_country_window(country, start_date, end_date, year, selected_products)
        source_products = selected_products or [item["id"] for item in available_products(year)]
    except FirmsApiError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"count": len(records), "records": records, "country": country, "year": year,
            "start_date": start_date.isoformat(), "end_date": end_date.isoformat(),
            "data_status": "Local NASA FIRMS country archives", "harmonization": "not applied",
            "products": source_products,
            "source_metadata": "MODIS and VIIRS source/platform rows remain separate; original CSV fields retained"}


@app.get("/api/local-archive/calendar")
def local_archive_calendar(
    country: str = Query(..., min_length=1, max_length=80),
    year: int = Query(..., ge=2000, le=2026),
    month: int = Query(..., ge=1, le=12),
    products: str | None = Query(None, description="Comma-separated local products; defaults to products available for the selected year"),
):
    try:
        selected_products = [value.strip() for value in products.split(",") if value.strip()] if products else None
        summary = summarize_country_month(country, year, month, selected_products)
    except FirmsApiError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return summary


def _parse_bbox(value: str | None) -> list[float] | None:
    if value is None:
        return None
    try:
        parts = [float(part.strip()) for part in value.split(",")]
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="bbox must be comma-separated west,south,east,north numeric coordinates.") from exc
    if len(parts) != 4:
        raise HTTPException(status_code=422, detail="bbox must contain west,south,east,north.")
    try:
        validate_bbox(parts)
    except AnalyticsQueryError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return parts


@app.get("/api/data-quality")
def local_data_quality():
    try:
        return coverage_status()
    except AnalyticsQueryError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.get("/api/calendar")
def analytics_calendar(
    start_date: date = Query(...),
    end_date: date = Query(...),
    bbox: str | None = Query(None, description="west,south,east,north in WGS84"),
    geojson: str | None = Query(None, max_length=50000, description="URL-encoded GeoJSON Polygon or MultiPolygon in WGS84"),
    product_type: str = Query("SP"),
    platform: list[str] | None = Query(None),
    daynight: str | None = Query(None),
):
    try:
        return get_calendar(start_date, end_date, product_type=product_type, platforms=platform,
                            daynight=daynight, bbox=_parse_bbox(bbox), geojson=geojson)
    except AnalyticsTimeout as exc:
        raise HTTPException(status_code=504, detail=str(exc)) from exc
    except AnalyticsQueryError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/api/climatology")
def analytics_climatology(
    start_date: date = Query(...), end_date: date = Query(...),
    bbox: str | None = Query(None, description="west,south,east,north in WGS84"),
):
    try:
        _parse_bbox(bbox)
        return unavailable_analysis("historical_climatology", start_date, end_date)
    except AnalyticsQueryError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/api/anomalies")
def analytics_anomalies(
    start_date: date = Query(...), end_date: date = Query(...),
    bbox: str | None = Query(None, description="west,south,east,north in WGS84"),
):
    try:
        _parse_bbox(bbox)
        return unavailable_analysis("historical_anomalies", start_date, end_date)
    except AnalyticsQueryError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/api/critical-periods")
def analytics_critical_periods(
    start_date: date = Query(...), end_date: date = Query(...),
    bbox: str | None = Query(None, description="west,south,east,north in WGS84"),
):
    try:
        _parse_bbox(bbox)
        return unavailable_analysis("critical_periods", start_date, end_date)
    except AnalyticsQueryError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
