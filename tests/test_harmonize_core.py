from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend" / "scripts"))
import harmonize_core as core


def _weekly_relationship(years: int = 6, weeks_per_year: int = 12) -> pd.DataFrame:
    rows = []
    for year in range(2020, 2020 + years):
        for week_index in range(weeks_per_year):
            index = (year - 2020) * weeks_per_year + week_index
            viirs = 12.0 + (index % 17) * 8.0 + index * 0.07
            noise = 1.0 + 0.012 * np.sin(index * 1.7)
            rows.append({
                "country": "Synthetic",
                "week": pd.Timestamp(year=year, month=1, day=6) + pd.Timedelta(weeks=week_index),
                "frp_VIIRS": viirs,
                "frp_MODIS": viirs / 3.0 * noise,
                "n_VIIRS": 10,
                "n_MODIS": 10,
            })
    return pd.DataFrame(rows)


def test_theil_sen_recovers_three_to_one_viirs_relationship_with_small_loyo_error():
    weekly = _weekly_relationship()
    calibration = core.calibrate_country(weekly)

    assert calibration is not None
    assert calibration["fit"] == "country"
    assert calibration["b"] == pytest.approx(1.0, abs=0.01)
    assert calibration["a"] == pytest.approx(-np.log(3.0), abs=0.02)
    assert calibration["mdape"] < 0.04
    assert calibration["r2"] > 0.99


def test_country_with_too_few_overlap_weeks_uses_low_confidence_fallback():
    weekly = _weekly_relationship(years=1, weeks_per_year=12)
    fallback = {"a": -np.log(3.0), "b": 1.0, "sd": 0.08}

    calibration = core.calibrate_country(weekly, fallback)

    assert calibration is not None
    assert calibration["fit"] == "global_fallback"
    assert calibration["confidence"] == "Low"
    assert calibration["n_weeks"] < core.MIN_BOTH_WEEKS
    assert calibration["r2"] is None
    assert calibration["mdape"] is None
