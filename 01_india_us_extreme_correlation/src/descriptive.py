"""Descriptive statistics and distributional diagnostics."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import stats


@dataclass
class DescriptiveStats:
    n: int
    mean: float
    std: float
    skewness: float
    excess_kurtosis: float
    minimum: float
    maximum: float
    jarque_bera_stat: float
    jarque_bera_pvalue: float

    def to_dict(self) -> dict:
        return {
            "n": self.n,
            "mean": self.mean,
            "std": self.std,
            "skewness": self.skewness,
            "excess_kurtosis": self.excess_kurtosis,
            "min": self.minimum,
            "max": self.maximum,
            "jarque_bera_stat": self.jarque_bera_stat,
            "jarque_bera_pvalue": self.jarque_bera_pvalue,
        }


def compute_descriptive_stats(returns: pd.Series) -> DescriptiveStats:
    """Compute standard descriptive statistics and a Jarque-Bera normality
    test for a series of returns. Requires at least 8 observations (scipy's
    jarque_bera minimum); raises ValueError otherwise so a silently
    meaningless result is never produced for a too-small sub-sample.
    """
    clean = returns.dropna()
    if len(clean) < 8:
        raise ValueError(
            f"Need at least 8 observations for Jarque-Bera test, got {len(clean)}."
        )
    jb_stat, jb_pvalue = stats.jarque_bera(clean)
    return DescriptiveStats(
        n=len(clean),
        mean=float(clean.mean()),
        std=float(clean.std(ddof=1)),
        skewness=float(stats.skew(clean)),
        excess_kurtosis=float(stats.kurtosis(clean, fisher=True)),
        minimum=float(clean.min()),
        maximum=float(clean.max()),
        jarque_bera_stat=float(jb_stat),
        jarque_bera_pvalue=float(jb_pvalue),
    )


def qq_points(returns: pd.Series) -> tuple[np.ndarray, np.ndarray]:
    """Theoretical (normal) vs. sample quantiles for a QQ plot.

    Returns (theoretical_quantiles, sample_quantiles), both standardized.
    """
    clean = returns.dropna()
    standardized = (clean - clean.mean()) / clean.std(ddof=1)
    sample_sorted = np.sort(standardized.values)
    n = len(sample_sorted)
    probs = (np.arange(1, n + 1) - 0.5) / n
    theoretical = stats.norm.ppf(probs)
    return theoretical, sample_sorted
