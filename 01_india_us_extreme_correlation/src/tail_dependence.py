"""Empirical tail-dependence coefficients (chi, chi-bar).

These are descriptive diagnostics only in this project (see methodology.md
Section 6) -- a rigorous asymptotic dependence/independence conclusion is
deferred to Project 14.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def _pseudo_observations(series: pd.Series) -> np.ndarray:
    """Rank-transform to (0,1) pseudo-observations: rank / (n+1)."""
    ranks = series.rank(method="average")
    n = len(series)
    return (ranks / (n + 1)).values


def chi_upper(x: pd.Series, y: pd.Series, q: float) -> dict:
    """Empirical upper-tail chi(q) = P(V>q | U>q) estimator, where U, V are
    the rank-transformed pseudo-observations of x and y. chi -> dependence
    strength at quantile q; chi(q) -> 0 as q -> 1 implies asymptotic
    independence, chi(q) -> c > 0 implies asymptotic dependence.
    """
    clean = pd.DataFrame({"x": x, "y": y}).dropna()
    u = _pseudo_observations(clean["x"])
    v = _pseudo_observations(clean["y"])
    n = len(u)
    joint = np.mean((u > q) & (v > q))
    marginal = 1 - q
    chi = joint / marginal if marginal > 0 else np.nan
    n_joint = int(np.sum((u > q) & (v > q)))
    return {"q": q, "chi": float(chi), "n_joint_exceedances": n_joint, "n": n}


def chi_bar_upper(x: pd.Series, y: pd.Series, q: float) -> dict:
    """Coles-Heffernan-Tawn (1999) chi-bar(q) diagnostic.

    chi_bar(q) = 2*log(P(U>q)) / log(P(U>q, V>q)) - 1, in [-1, 1].
    chi_bar = 1 indicates asymptotic dependence is possible; chi_bar < 1
    indicates asymptotic independence.
    """
    clean = pd.DataFrame({"x": x, "y": y}).dropna()
    u = _pseudo_observations(clean["x"])
    v = _pseudo_observations(clean["y"])
    p_joint = np.mean((u > q) & (v > q))
    p_marginal = np.mean(u > q)
    if p_joint <= 0 or p_marginal <= 0:
        return {"q": q, "chi_bar": float("nan")}
    chi_bar = 2 * np.log(p_marginal) / np.log(p_joint) - 1
    return {"q": q, "chi_bar": float(chi_bar)}


def tail_dependence_table(x: pd.Series, y: pd.Series, q_list: list[float],
                           tail: str = "upper") -> pd.DataFrame:
    """chi and chi_bar across a grid of quantiles. tail='lower' flips the
    sign of both series before applying the upper-tail estimators, which is
    the standard trick for studying the lower (left/downside) tail.
    """
    if tail == "lower":
        x, y = -x, -y
    rows = []
    for q in q_list:
        chi_row = chi_upper(x, y, q)
        chi_bar_row = chi_bar_upper(x, y, q)
        rows.append({**chi_row, "chi_bar": chi_bar_row["chi_bar"], "tail": tail})
    return pd.DataFrame(rows)
