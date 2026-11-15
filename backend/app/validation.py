import csv
import io
from datetime import date
from typing import Any

ALIASES = {
    "latitude": ("latitude", "lat"),
    "longitude": ("longitude", "lon", "long"),
    "acquired": ("acq_date", "acquired", "date"),
    "sensor": ("instrument", "sensor", "satellite"),
    "brightness": ("bright_ti4", "bright_ti5", "brightness", "bright_t31"),
    "confidence": ("confidence",),
    "daynight": ("daynight", "day_night"),
}
REQUIRED = ("latitude", "longitude", "acquired", "sensor")


class CsvValidationError(ValueError):
    """An actionable CSV schema or row validation error."""


def _normalized_headers(headers: list[str]) -> dict[str, str]:
    return {header.strip().lower(): header for header in headers if header and header.strip()}


def _value(row: dict[str, str], normalized: dict[str, str], field: str) -> str | None:
    for alias in ALIASES[field]:
        original = normalized.get(alias)
        if original is not None:
            value = row.get(original, "").strip()
            if value:
                return value
    return None


def parse_firms_csv(
    content: bytes,
    date_start: date | None = None,
    date_end: date | None = None,
    allow_empty: bool = False,
) -> list[dict[str, Any]]:
    """Parse supported FIRMS CSV rows without harmonizing or discarding source fields."""
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise CsvValidationError("CSV must be UTF-8 encoded. Export or convert the file to UTF-8 and retry.") from exc
    try:
        reader = csv.DictReader(io.StringIO(text))
        if not reader.fieldnames:
            raise CsvValidationError("The file is empty or has no CSV header row.")
        normalized = _normalized_headers(reader.fieldnames)
        missing = [field for field in REQUIRED if not any(alias in normalized for alias in ALIASES[field])]
        if missing:
            expected = "latitude (latitude/lat), longitude (longitude/lon), acquired date (acq_date/acquired/date), and sensor (satellite/sensor/instrument)"
            raise CsvValidationError(f"Missing required field(s): {', '.join(missing)}. Expected columns include {expected}.")
        results: list[dict[str, Any]] = []
        for line, row in enumerate(reader, start=2):
            if not any((v or "").strip() for v in row.values()):
                continue
            lat_raw, lon_raw = _value(row, normalized, "latitude"), _value(row, normalized, "longitude")
            try:
                lat, lon = float(lat_raw or ""), float(lon_raw or "")
            except ValueError as exc:
                raise CsvValidationError(f"Row {line}: latitude and longitude must be numeric (received {lat_raw!r}, {lon_raw!r}).") from exc
            if not -90 <= lat <= 90 or not -180 <= lon <= 180:
                raise CsvValidationError(f"Row {line}: coordinates are outside valid ranges (latitude -90..90, longitude -180..180).")
            acquired = _value(row, normalized, "acquired")
            sensor = _value(row, normalized, "sensor")
            if not acquired:
                raise CsvValidationError(f"Row {line}: acquisition date is blank. Add an acq_date/acquired/date value.")
            try:
                acquired_day = date.fromisoformat(acquired[:10])
            except ValueError as exc:
                raise CsvValidationError(f"Row {line}: acquisition date must begin with an ISO date (YYYY-MM-DD); received {acquired!r}.") from exc
            if date_start and acquired_day < date_start or date_end and acquired_day > date_end:
                continue
            if not sensor:
                raise CsvValidationError(f"Row {line}: sensor is blank. Add a satellite/sensor value so source records stay identifiable.")
            raw_fields = {key: (value.strip() if value else "") for key, value in row.items() if key}
            record: dict[str, Any] = {"original_fields": raw_fields}
            record.update({"latitude": lat, "longitude": lon, "acquired": acquired, "sensor": sensor})
            for name in ("satellite", "instrument", "version", "frp", "bright_ti4", "bright_ti5", "bright_t31", "confidence", "daynight", "acq_time", "scan", "track"):
                if name in raw_fields:
                    record[name] = raw_fields[name]
            brightness = _value(row, normalized, "brightness")
            if brightness:
                try:
                    record["brightness"] = float(brightness)
                except ValueError as exc:
                    raise CsvValidationError(f"Row {line}: brightness must be numeric when present (received {brightness!r}).") from exc
            else:
                record["brightness"] = None
            record["confidence"] = _value(row, normalized, "confidence") or "unknown"
            record["daynight"] = _value(row, normalized, "daynight") or "unknown"
            results.append(record)
        if not results and not allow_empty:
            raise CsvValidationError("No data rows were found. Add at least one FIRMS record below the header.")
        return results
    except csv.Error as exc:
        raise CsvValidationError(f"Could not parse CSV: {exc}. Check quoting and delimiters, then retry.") from exc
