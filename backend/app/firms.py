"""Small, bounded client for the official NASA FIRMS area CSV API."""
import os
from datetime import date
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import urlopen

from app.validation import CsvValidationError, parse_firms_csv

FIRMS_API = "https://firms.modaps.eosdis.nasa.gov/api/area/csv"
SOURCES = {"MODIS_NRT", "VIIRS_NOAA20_NRT", "VIIRS_NOAA21_NRT"}
ARCHIVE_SOURCES = {"MODIS_SP", "VIIRS_NOAA20_SP", "VIIRS_NOAA21_SP", "VIIRS_SNPP_SP"}
AREAS = {
    "world": "world",
    "South America": "-85,-57,-32,14",
    "North America": "-168,5,-52,72",
    "Oceania": "112,-44,154,-10",
    "Asia": "60,5,150,60",
    "Africa": "-20,-35,52,38",
    "Europe": "-12,35,40,72",
}


class FirmsApiError(RuntimeError):
    pass


def _load(source: str, area: str, days: int, start_date: date | None = None) -> list[dict]:
    key = os.getenv("FIRMS_MAP_KEY", "").strip()
    if not key:
        raise FirmsApiError("FIRMS_MAP_KEY is not configured. Request a free FIRMS MAP_KEY and set it in the backend environment; the key is never sent to the browser.")
    if area not in AREAS:
        raise FirmsApiError(f"Unsupported area {area!r}. Choose one of: {', '.join(AREAS)}.")
    if not 1 <= days <= 5:
        raise FirmsApiError("The FIRMS area API accepts 1 to 5 days per request.")
    parts = [FIRMS_API, quote(key, safe=""), source, quote(AREAS[area], safe=","), str(days)]
    if start_date is not None:
        parts.append(start_date.isoformat())
    url = "/".join(parts)
    try:
        with urlopen(url, timeout=45) as response:
            content = response.read(10_000_001)
    except HTTPError as exc:
        if exc.code in (401, 403):
            raise FirmsApiError("FIRMS rejected the configured MAP_KEY. Check the key and retry.") from exc
        raise FirmsApiError(f"FIRMS returned HTTP {exc.code}. Try again later or use a downloaded CSV.") from exc
    except (URLError, TimeoutError) as exc:
        raise FirmsApiError("Could not reach the NASA FIRMS API. Check the backend network connection or use a downloaded CSV.") from exc
    if len(content) > 10_000_000:
        raise FirmsApiError("FIRMS returned more than the 10 MB preview limit. Choose a smaller area or fewer days.")
    try:
        records = parse_firms_csv(content)
    except CsvValidationError as exc:
        message = str(exc)
        if "No data rows" in message:
            return []
        raise FirmsApiError(f"FIRMS returned a CSV that did not match the supported schema: {message}") from exc
    for record in records:
        record["firms_dataset"] = source
        record["provenance"] = "NASA FIRMS API"
    return records


def load_latest(source: str, area: str, days: int) -> list[dict]:
    if source not in SOURCES:
        raise FirmsApiError(f"Unsupported live source {source!r}. Choose MODIS_NRT, VIIRS_NOAA20_NRT, or VIIRS_NOAA21_NRT.")
    return _load(source, area, days)


def load_archive(source: str, area: str, days: int, start_date: date) -> list[dict]:
    if source not in ARCHIVE_SOURCES:
        raise FirmsApiError(f"Unsupported Standard Processing source {source!r}. Choose one of: {', '.join(sorted(ARCHIVE_SOURCES))}.")
    return _load(source, area, days, start_date)
