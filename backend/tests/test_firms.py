import io
import os
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from fastapi.testclient import TestClient

from app.firms import FirmsApiError, load_archive, load_latest
from app.main import app

CSV = b"latitude,longitude,bright_ti4,acq_date,satellite,instrument,confidence,version,daynight,frp\n35.1,-117.2,330.4,2026-11-13,N21,VIIRS,n,2.0NRT,D,4.2\n"


def test_live_client_uses_allowlisted_source_and_keeps_provenance():
    with patch.dict(os.environ, {"FIRMS_MAP_KEY": "test-key"}), patch("app.firms.urlopen", return_value=io.BytesIO(CSV)) as request:
        records = load_latest("VIIRS_NOAA21_NRT", "North America", 3)
    assert records[0]["sensor"] == "VIIRS"
    assert records[0]["satellite"] == "N21"
    assert records[0]["version"] == "2.0NRT"
    assert records[0]["original_fields"]["frp"] == "4.2"
    assert records[0]["firms_dataset"] == "VIIRS_NOAA21_NRT"
    assert "/VIIRS_NOAA21_NRT/-168,5,-52,72/3" in request.call_args.args[0]


def test_live_client_requires_a_key_and_rejects_unsupported_legacy_feed():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(FirmsApiError, match="FIRMS_MAP_KEY"):
            load_latest("VIIRS_NOAA21_NRT", "world", 1)
    with patch.dict(os.environ, {"FIRMS_MAP_KEY": "test-key"}):
        with pytest.raises(FirmsApiError, match="Unsupported live source"):
            load_latest("VIIRS_SNPP_NRT", "world", 1)


def test_latest_route_reports_key_setup_and_rejects_retired_feed():
    client = TestClient(app)
    with patch.dict(os.environ, {}, clear=True):
        response = client.get("/api/firms/latest")
    assert response.status_code == 503
    assert "FIRMS_MAP_KEY" in response.json()["detail"]
    retired = client.get("/api/firms/latest", params={"source": "VIIRS_SNPP_NRT"})
    assert retired.status_code == 422
    assert "Unsupported live source" in retired.json()["detail"]
    with patch.dict(os.environ, {}, clear=True):
        archive = client.get("/api/firms/archive", params={"source": "VIIRS_SNPP_SP", "area": "world", "start_date": "2026-11-01", "days": 3})
    assert archive.status_code == 503
    assert "FIRMS_MAP_KEY" in archive.json()["detail"]


def test_archive_client_uses_date_bounded_standard_processing_feed():
    from datetime import date
    with patch.dict(os.environ, {"FIRMS_MAP_KEY": "test-key"}), patch("app.firms.urlopen", return_value=io.BytesIO(CSV)) as request:
        records = load_archive("VIIRS_SNPP_SP", "world", 3, date(2026, 11, 11))
    assert records[0]["firms_dataset"] == "VIIRS_SNPP_SP"
    assert "/VIIRS_SNPP_SP/world/3/2026-11-11" in request.call_args.args[0]
