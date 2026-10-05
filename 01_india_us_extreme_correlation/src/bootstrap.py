"""Moving block bootstrap for confidence intervals under serial dependence
(volatility clustering) -- see methodology.md Section 8.
"""
from __future__ import annotations

from typing import Callable

import numpy as np
import pandas as pd


def default_block_length(n: int) -> int:
    """Standard rule-of-thumb block length, ceil(n^(1/3))."""
    return max(2, int(np.ceil(n ** (1 / 3))))


def moving_block_bootstrap_sample(df: pd.DataFrame, block_length: int, rng: np.random.Generator) -> pd.DataFrame:
    """Build one bootstrap resample of the same length as `df` by
    concatenating randomly-chosen overlapping blocks of `block_length` rows.
    """
    n = len(df)
    n_blocks_needed = int(np.ceil(n / block_length))
    max_start = n - block_length
    if max_start < 0:
        raise ValueError("block_length exceeds sample length")
    starts = rng.integers(0, max_start + 1, size=n_blocks_needed)
    pieces = [df.iloc[s : s + block_length] for s in starts]
    resampled = pd.concat(pieces, ignore_index=True).iloc[:n]
    return resampled


def moving_block_bootstrap_ci(
    df: pd.DataFrame,
    stat_func: Callable[[pd.DataFrame], float],
    n_reps: int = 2000,
    block_length: int | None = None,
    confidence: float = 0.95,
    seed: int = 0,
) -> dict:
    """Moving block bootstrap confidence interval for a scalar statistic.

    `stat_func` takes a DataFrame (same columns as `df`) and returns a
    float. Returns the point estimate on the original data, the bootstrap
    distribution's mean/std, and the percentile confidence interval.
    """
    rng = np.random.default_rng(seed)
    n = len(df)
    bl = block_length or default_block_length(n)
    point_estimate = stat_func(df)
    draws = np.full(n_reps, np.nan)
    for i in range(n_reps):
        resample = moving_block_bootstrap_sample(df, bl, rng)
        try:
            draws[i] = stat_func(resample)
        except Exception:
            draws[i] = np.nan
    valid = draws[~np.isnan(draws)]
    alpha = 1 - confidence
    lower = float(np.percentile(valid, 100 * alpha / 2)) if len(valid) > 0 else np.nan
    upper = float(np.percentile(valid, 100 * (1 - alpha / 2))) if len(valid) > 0 else np.nan
    return {
        "point_estimate": point_estimate,
        "bootstrap_mean": float(np.mean(valid)) if len(valid) > 0 else np.nan,
        "bootstrap_std": float(np.std(valid, ddof=1)) if len(valid) > 1 else np.nan,
        "ci_lower": lower,
        "ci_upper": upper,
        "n_valid_reps": int(len(valid)),
        "block_length": bl,
    }
