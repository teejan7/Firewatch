"""Discover and read bounded windows from extracted, all-country FIRMS CSV archives."""
import calendar
import csv
from functools import lru_cache
from datetime import date
from pathlib import Path
from typing import Any

from app.firms import FirmsApiError
from app.validation import ALIASES, CsvValidationError, parse_firms_csv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = PROJECT_ROOT / "data" / "raw" / "extracted"
PRODUCTS: dict[str, dict[str, str]] = {
    "MODIS_SP": {"folder": "MODIS_SP", "prefix": "modis", "sensor": "MODIS", "label": "MODIS Standard Processing"},
    "VIIRS_SNPP_SP": {"folder": "VIIRS_SNPP_SP", "prefix": "viirs-snpp", "sensor": "VIIRS", "label": "VIIRS S-NPP Standard Processing"},
    "VIIRS_NOAA20_SP": {"folder": "VIIRS_NOAA20_SP", "prefix": "viirs-jpss1", "sensor": "VIIRS", "label": "VIIRS NOAA-20 Standard Processing"},
    # NOAA-21 files are optional and only appear in the catalog once extracted.
    "VIIRS_NOAA21_SP": {"folder": "VIIRS_NOAA21_SP", "prefix": "viirs-jpss2", "sensor": "VIIRS", "label": "VIIRS NOAA-21 Standard Processing"},
}
MAX_COUNTRY_FILE_BYTES = 150_000_000
MAX_WINDOW_DAYS = 31
MIN_YEAR = 2000
MAX_YEAR = 2026


def _year_dir(product: str, year: int) -> Path:
    if product not in PRODUCTS:
        raise FirmsApiError(f"Unsupported local product. Choose one of: {', '.join(PRODUCTS)}.")
    if year < MIN_YEAR or year > MAX_YEAR:
        raise FirmsApiError(f"Local archive year must be between {MIN_YEAR} and {MAX_YEAR}.")
    spec = PRODUCTS[product]
    return DATA_ROOT / spec["folder"] / spec["prefix"] / str(year)


def available_products(year: int) -> list[dict[str, str]]:
    """Return products with extracted CSVs in a year, not merely placeholder folders."""
    found = []
    for product, spec in PRODUCTS.items():
        folder = _year_dir(product, year)
        if folder.is_dir() and any(folder.glob("*.csv")):
            found.append({"id": product, "sensor": spec["sensor"], "label": spec["label"]})
    return found


def _countries_for_product(product: str, year: int) -> set[str]:
    folder = _year_dir(product, year)
    prefix = PRODUCTS[product]["prefix"]
    start = f"{prefix}_{year}_"
    countries: set[str] = set()
    if not folder.is_dir():
        return countries
    for path in folder.glob("*.csv"):
        if path.stem.startswith(start):
            country = path.stem[len(start):]
            if country:
                countries.add(country)
    return countries


def available_countries(year: int = 2025, products: list[str] | None = None) -> list[str]:
    """Return the union of countries with a source CSV for the requested year."""
    selected = products or [item["id"] for item in available_products(year)]
    countries: set[str] = set()
    for product in selected:
        if product not in PRODUCTS:
            raise FirmsApiError(f"Unsupported local product {product!r}. Choose one of: {', '.join(PRODUCTS)}.")
        countries.update(_countries_for_product(product, year))
    return sorted(countries, key=str.casefold)


def _country_file(product: str, country: str, year: int) -> Path | None:
    folder = _year_dir(product, year)
    spec = PRODUCTS[product]
    exact = folder / f"{spec['prefix']}_{year}_{country}.csv"
    if exact.is_file():
        return exact
    return None


def load_country_window(
    country: str,
    start_date: date,
    end_date: date,
    year: int = 2025,
    products: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Load source rows for one country and a bounded date window; never harmonize."""
    if start_date > end_date:
        raise FirmsApiError("Start date must be on or before end date.")
    if start_date.year != year or end_date.year != year:
        raise FirmsApiError(f"Both dates must be within the selected year ({year}).")
    if (end_date - start_date).days >= MAX_WINDOW_DAYS:
        raise FirmsApiError(f"Local map queries are limited to {MAX_WINDOW_DAYS} days. Choose a shorter date window.")
    selected = products or [item["id"] for item in available_products(year)]
    if not selected:
        raise FirmsApiError(f"No extracted FIRMS source files were found for {year}.")
    unknown = [product for product in selected if product not in PRODUCTS]
    if unknown:
        raise FirmsApiError(f"Unsupported local product(s): {', '.join(unknown)}.")
    country_names = available_countries(year, selected)
    if country not in country_names:
        raise FirmsApiError(f"No FIRMS country CSV was found for {country!r} in {year} for the selected source(s).")

    records: list[dict[str, Any]] = []
    for product in selected:
        path = _country_file(product, country, year)
        if path is None:
            # Some countries have no file for a product/year; leave the other
            # sensor's source records intact instead of fabricating zero rows.
            continue
        if path.stat().st_size > MAX_COUNTRY_FILE_BYTES:
            raise FirmsApiError(f"{path.name} exceeds the {MAX_COUNTRY_FILE_BYTES // 1_000_000} MB local preview limit. Choose a different country or smaller source file.")
        try:
            found = parse_firms_csv(path.read_bytes(), date_start=start_date, date_end=end_date, allow_empty=True)
        except CsvValidationError as exc:
            raise FirmsApiError(f"Could not validate {path.name}: {exc}") from exc
        for record in found:
            record["firms_dataset"] = product
            record["provenance"] = f"NASA FIRMS country archive · {product} · {year} · {country}"
        records.extend(found)
    return records


@lru_cache(maxsize=128)
def _daily_record_counts(path_text: str, file_size: int, modified_ns: int, year: int) -> dict[str, int]:
    """Stream-validate a source file and cache its daily detection row counts."""
    path = Path(path_text)
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            if not reader.fieldnames:
                raise FirmsApiError(f"{path.name} is empty or has no CSV header row.")
            normalized = {header.strip().lower(): header for header in reader.fieldnames if header and header.strip()}
            columns = {}
            for field in ("latitude", "longitude", "acquired", "sensor"):
                columns[field] = next((normalized[alias] for alias in ALIASES[field] if alias in normalized), None)
            missing = [field for field, column in columns.items() if column is None]
            if missing:
                raise FirmsApiError(f"{path.name} is missing required FIRMS column(s): {', '.join(missing)}.")
            counts: dict[str, int] = {}
            for line, row in enumerate(reader, start=2):
                if not any((value or "").strip() for value in row.values()):
                    continue
                try:
                    latitude = float((row.get(columns["latitude"]) or "").strip())
                    longitude = float((row.get(columns["longitude"]) or "").strip())
                except ValueError as exc:
                    raise FirmsApiError(f"{path.name} row {line} has non-numeric coordinates.") from exc
                if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
                    raise FirmsApiError(f"{path.name} row {line} has coordinates outside valid ranges.")
                acquired = (row.get(columns["acquired"]) or "").strip()
                try:
                    acquired_day = date.fromisoformat(acquired[:10])
                except ValueError as exc:
                    raise FirmsApiError(f"{path.name} row {line} has an invalid acquisition date {acquired!r}; expected YYYY-MM-DD.") from exc
                if acquired_day.year != year:
                    raise FirmsApiError(f"{path.name} row {line} is dated {acquired_day.year}, outside its {year} archive file.")
                if not (row.get(columns["sensor"]) or "").strip():
                    raise FirmsApiError(f"{path.name} row {line} has a blank instrument/sensor field.")
                key = acquired_day.isoformat()
                counts[key] = counts.get(key, 0) + 1
            return counts
    except UnicodeDecodeError as exc:
        raise FirmsApiError(f"{path.name} is not UTF-8 CSV data.") from exc
    except csv.Error as exc:
        raise FirmsApiError(f"Could not parse {path.name}: {exc}.") from exc


def summarize_country_month(
    country: str,
    year: int,
    month: int,
    products: list[str] | None = None,
) -> dict[str, Any]:
    """Return whole-month source row counts for a calendar without loading map points."""
    if month < 1 or month > 12:
        raise FirmsApiError("Calendar month must be between 1 and 12.")
    selected = products or [item["id"] for item in available_products(year)]
    if not selected:
        raise FirmsApiError(f"No extracted FIRMS source files were found for {year}.")
    unknown = [product for product in selected if product not in PRODUCTS]
    if unknown:
        raise FirmsApiError(f"Unsupported local product(s): {', '.join(unknown)}.")

    product_counts: dict[str, dict[str, int]] = {}
    for product in selected:
        path = _country_file(product, country, year)
        if path is None:
            continue
        size = path.stat().st_size
        counts = _daily_record_counts(str(path.resolve()), size, path.stat().st_mtime_ns, year)
        product_counts[product] = {
            f"{year}-{month:02d}-{day:02d}": count
            for day in range(1, calendar.monthrange(year, month)[1] + 1)
            if (count := counts.get(f"{year}-{month:02d}-{day:02d}", 0))
        }
    if not product_counts:
        raise FirmsApiError(f"No source files for {country!r} were found for the selected product(s) in {year}.")

    days = []
    for day in range(1, calendar.monthrange(year, month)[1] + 1):
        acquired = f"{year}-{month:02d}-{day:02d}"
        by_product = {product: counts.get(acquired, 0) for product, counts in product_counts.items()}
        days.append({"date": acquired, "count": sum(by_product.values()), "by_product": by_product})
    return {
        "country": country,
        "year": year,
        "month": month,
        "products": list(product_counts),
        "days": days,
        "total": sum(day["count"] for day in days),
        "data_status": "Local NASA FIRMS Standard Processing country archives",
        "harmonization": "not applied",
        "count_method": "daily source-record row counts; product/platform records remain separate",
    }
