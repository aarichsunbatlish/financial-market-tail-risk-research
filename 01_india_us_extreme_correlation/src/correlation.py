"""Rolling and conditional (sign-based) correlation."""
from __future__ import annotations

import numpy as np
import pandas as pd


def rolling_correlation(df: pd.DataFrame, window: int,
                         col_a: str = "nifty", col_b: str = "sp500") -> pd.Series:
    """Rolling Pearson correlation over `window` trading days."""
    return df[col_a].rolling(window).corr(df[col_b])


def unconditional_correlation(df: pd.DataFrame,
                               col_a: str = "nifty", col_b: str = "sp500") -> float:
    clean = df[[col_a, col_b]].dropna()
    if len(clean) < 2:
        return float("nan")
    return float(clean[col_a].corr(clean[col_b]))


def sign_conditional_correlation(df: pd.DataFrame,
                                  col_a: str = "nifty",
                                  col_b: str = "sp500") -> dict[str, float]:
    """Correlation conditional on the sign of `col_a` (the India leg by
    convention) -- a simple first look at asymmetry before the formal
    exceedance-correlation test in exceedance.py.
    """
    clean = df[[col_a, col_b]].dropna()
    negative = clean[clean[col_a] < 0]
    positive = clean[clean[col_a] > 0]
    return {
        "unconditional": unconditional_correlation(clean, col_a, col_b),
        "conditional_negative": (
            float(negative[col_a].corr(negative[col_b])) if len(negative) >= 2 else float("nan")
        ),
        "conditional_positive": (
            float(positive[col_a].corr(positive[col_b])) if len(positive) >= 2 else float("nan")
        ),
        "n_negative": int(len(negative)),
        "n_positive": int(len(positive)),
    }
