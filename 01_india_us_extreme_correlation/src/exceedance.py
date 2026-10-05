"""Exceedance correlation (Longin & Solnik, 2001) and the signed
single-conditioning robustness check.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

MIN_EXCEEDANCE_COUNT_DEFAULT = 15


def _zscore(series: pd.Series) -> pd.Series:
    return (series - series.mean()) / series.std(ddof=1)


def exceedance_correlation(
    df: pd.DataFrame,
    threshold: float,
    tail: str,
    col_a: str = "nifty",
    col_b: str = "sp500",
    min_count: int = MIN_EXCEEDANCE_COUNT_DEFAULT,
) -> dict:
    """Joint exceedance correlation at a given sigma threshold.

    tail='left': both z_a < -threshold and z_b < -threshold.
    tail='right': both z_a > threshold and z_b > threshold.

    Returns a dict with the correlation estimate, exceedance count, and a
    `sufficient` flag -- callers should not treat `rho` as meaningful when
    `sufficient` is False (count below `min_count`).
    """
    if tail not in ("left", "right"):
        raise ValueError("tail must be 'left' or 'right'")
    clean = df[[col_a, col_b]].dropna()
    z_a = _zscore(clean[col_a])
    z_b = _zscore(clean[col_b])
    if tail == "left":
        mask = (z_a < -threshold) & (z_b < -threshold)
    else:
        mask = (z_a > threshold) & (z_b > threshold)
    n = int(mask.sum())
    sufficient = n >= min_count
    rho = float(clean.loc[mask, col_a].corr(clean.loc[mask, col_b])) if n >= 2 else float("nan")
    return {
        "threshold": threshold,
        "tail": tail,
        "n_exceedances": n,
        "sufficient": sufficient,
        "rho": rho if sufficient else float("nan"),
        "rho_unfiltered": rho,  # kept for transparency/debugging, not for reporting
    }


def exceedance_correlation_table(
    df: pd.DataFrame,
    thresholds: list[float],
    col_a: str = "nifty",
    col_b: str = "sp500",
    min_count: int = MIN_EXCEEDANCE_COUNT_DEFAULT,
) -> pd.DataFrame:
    """Exceedance correlation across thresholds and both tails."""
    rows = []
    for tail in ("left", "right"):
        for thr in thresholds:
            rows.append(exceedance_correlation(df, thr, tail, col_a, col_b, min_count))
    return pd.DataFrame(rows)


def signed_single_conditioning(
    df: pd.DataFrame,
    threshold: float,
    tail: str,
    condition_on: str = "nifty",
    other: str = "sp500",
    min_count: int = MIN_EXCEEDANCE_COUNT_DEFAULT,
) -> dict:
    """Correlation conditioning on only ONE market's exceedance (rather than
    both jointly), as a robustness check of whether the joint-exceedance
    result depends on which market's tail defines the conditioning set.
    """
    if tail not in ("left", "right"):
        raise ValueError("tail must be 'left' or 'right'")
    clean = df[[condition_on, other]].dropna()
    z_cond = _zscore(clean[condition_on])
    mask = (z_cond < -threshold) if tail == "left" else (z_cond > threshold)
    n = int(mask.sum())
    sufficient = n >= min_count
    rho = (
        float(clean.loc[mask, condition_on].corr(clean.loc[mask, other]))
        if n >= 2 else float("nan")
    )
    return {
        "threshold": threshold,
        "tail": tail,
        "condition_on": condition_on,
        "n_exceedances": n,
        "sufficient": sufficient,
        "rho": rho if sufficient else float("nan"),
    }
