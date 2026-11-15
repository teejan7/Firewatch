"""Statistical cross-sensor calibration: VIIRS -> MODIS-equivalent weekly FRP.
Input: daily DataFrame with columns country, date, family ('MODIS'|'VIIRS'), frp, n.
Not a physical retrieval correction: a log-log robust fit on overlap weeks,
validated leave-one-year-out."""
from __future__ import annotations
import numpy as np
import pandas as pd

MIN_FRP = 5.0          # MW per week per family to enter the fit
MIN_BOTH_WEEKS = 40    # usable overlap weeks for a country-specific fit
METHOD_VERSION = "loglog-theilsen-loyo-v1"


def theil_sen(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    i, j = np.triu_indices(len(x), 1)
    dx = x[j] - x[i]
    ok = dx != 0
    if ok.sum() == 0:
        return 1.0, float(np.median(y - x))
    slope = float(np.median((y[j][ok] - y[i][ok]) / dx[ok]))
    return slope, float(np.median(y - slope * x))


def operating_weeks(daily: pd.DataFrame) -> set:
    """Weeks where BOTH families reported detections somewhere on all 7 days."""
    g = daily[daily["n"] > 0].copy()
    g["date"] = pd.to_datetime(g["date"])
    g = g.drop_duplicates(["family", "date"])
    g["week"] = g["date"].dt.to_period("W-SUN").dt.start_time
    c = g.groupby(["family", "week"]).size().unstack(0).fillna(0)
    return set(c.index[(c["MODIS"] == 7) & (c["VIIRS"] == 7)])


def weekly(daily: pd.DataFrame) -> pd.DataFrame:
    d = daily.copy()
    d["date"] = pd.to_datetime(d["date"])
    d["week"] = d["date"].dt.to_period("W-SUN").dt.start_time
    w = d.groupby(["country", "week", "family"], as_index=False)[["frp", "n"]].sum()
    p = w.pivot(index=["country", "week"], columns="family", values=["frp", "n"]).fillna(0.0)
    p.columns = [f"{a}_{b}" for a, b in p.columns]
    for c in ("frp_MODIS", "frp_VIIRS", "n_MODIS", "n_VIIRS"):
        if c not in p:
            p[c] = 0.0
    return p.reset_index()


def _fit(v, m):
    b, a = theil_sen(np.log(v), np.log(m))
    return a, b


def _confidence(r2, mdape):
    if r2 >= 0.7 and mdape <= 0.35:
        return "High"
    if r2 >= 0.4 and mdape <= 0.60:
        return "Medium"
    return "Low"


def calibrate_country(wk: pd.DataFrame, fallback=None):
    """wk: weekly rows for ONE country, operating weeks only."""
    use = wk[(wk.frp_MODIS >= MIN_FRP) & (wk.frp_VIIRS >= MIN_FRP)].copy()
    use["year"] = use["week"].dt.year
    own = len(use) >= MIN_BOTH_WEEKS
    if not own:
        if fallback is None:
            return None
        a, b, sd = fallback["a"], fallback["b"], fallback["sd"]
        return {"a": a, "b": b, "sd": sd, "n_weeks": int(len(use)), "fit": "global_fallback",
                "r2": None, "mdape": None, "corr": None, "bias": None, "confidence": "Low"}
    errs = []
    for y in sorted(use.year.unique()):
        tr, te = use[use.year != y], use[use.year == y]
        if len(tr) < MIN_BOTH_WEEKS or len(te) < 5:
            continue
        a, b = _fit(tr.frp_VIIRS, tr.frp_MODIS)
        errs.append(pd.DataFrame({"obs": te.frp_MODIS.values,
                                  "pred": np.exp(a + b * np.log(te.frp_VIIRS.values))}))
    a, b = _fit(use.frp_VIIRS, use.frp_MODIS)
    if not errs:
        return None
    e = pd.concat(errs)
    lo, lp = np.log(e.obs), np.log(e.pred)
    ss = ((lo - lo.mean()) ** 2).sum()
    r2 = float(1 - ((lo - lp) ** 2).sum() / ss) if ss > 0 else float("nan")
    mdape = float(np.median(np.abs(e.pred - e.obs) / e.obs))
    corr = float(np.corrcoef(lo, lp)[0, 1])
    lr = lp - lo
    return {"a": a, "b": b, "sd": float(np.std(lr, ddof=1)), "n_weeks": int(len(use)),
            "fit": "country", "r2": r2, "mdape": mdape, "corr": corr,
            "bias": float(np.median(lr)),
            "confidence": _confidence(r2, mdape) if np.isfinite(r2) else "Low"}


def global_fallback(all_weekly: pd.DataFrame, seed=0):
    use = all_weekly[(all_weekly.frp_MODIS >= MIN_FRP) & (all_weekly.frp_VIIRS >= MIN_FRP)]
    use = use.sample(min(600, len(use)), random_state=seed)
    a, b = _fit(use.frp_VIIRS, use.frp_MODIS)
    resid = np.log(use.frp_MODIS) - (a + b * np.log(use.frp_VIIRS))
    return {"a": a, "b": b, "sd": float(np.std(resid, ddof=1))}


def harmonize_weeks(wk: pd.DataFrame, cal: dict) -> pd.DataFrame:
    """Rule: both sensors -> log-mean of MODIS and calibrated VIIRS; VIIRS only ->
    calibrated VIIRS; MODIS only -> MODIS. Band = +/-1.96 * residual SD (log space)."""
    out = wk.copy()
    m = out.frp_MODIS.to_numpy(float); v = out.frp_VIIRS.to_numpy(float)
    hat = np.exp(cal["a"] + cal["b"] * np.log(np.where(v > 0, v, 1.0)))
    hat = np.where(v > 0, hat, 0.0)
    both = (m > 0) & (v > 0)
    mix = np.exp(0.5 * np.log(np.where(m > 0, m, 1.0)) + 0.5 * np.log(np.where(hat > 0, hat, 1.0)))
    h = np.where(both, mix, np.where(m > 0, m, hat))
    f = np.exp(1.96 * cal["sd"])
    out["viirs_calibrated"] = hat
    out["harmonized"] = h
    out["lower"] = h / f
    out["upper"] = h * f
    out["daily_scale_for_viirs"] = np.where(v > 0, h / np.where(v > 0, v, 1.0), 1.0)
    return out


def continuity(wk: pd.DataFrame, cal: dict):
    """Median VIIRS/MODIS ratio before vs after calibration (target ~1.0 after)."""
    use = wk[(wk.frp_MODIS >= MIN_FRP) & (wk.frp_VIIRS >= MIN_FRP)]
    if use.empty:
        return None
    raw = float(np.median(use.frp_VIIRS / use.frp_MODIS))
    cal_v = np.exp(cal["a"] + cal["b"] * np.log(use.frp_VIIRS))
    return {"raw_ratio_median": raw, "calibrated_ratio_median": float(np.median(cal_v / use.frp_MODIS))}