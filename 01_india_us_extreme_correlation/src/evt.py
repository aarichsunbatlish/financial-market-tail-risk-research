"""Peaks-over-threshold / Generalized Pareto Distribution tail modelling.

Operates on a *loss* series (positive numbers = losses), i.e. callers
should pass `-returns` for left-tail (downside) analysis.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import stats


def mean_excess_function(losses: pd.Series, thresholds: np.ndarray) -> pd.DataFrame:
    """Mean excess e(u) = E[loss - u | loss > u] at each candidate threshold.

    Used as a threshold-selection diagnostic: e(u) should be approximately
    linear in u over the range where a GPD fit is appropriate.
    """
    rows = []
    for u in thresholds:
        exceed = losses[losses > u] - u
        rows.append({
            "threshold": u,
            "mean_excess": float(exceed.mean()) if len(exceed) > 0 else np.nan,
            "n_exceedances": int(len(exceed)),
        })
    return pd.DataFrame(rows)


@dataclass
class GPDFit:
    threshold: float
    shape: float       # xi (tail index)
    scale: float        # beta
    n_exceedances: int
    n_total: int
    loglikelihood: float

    def to_dict(self) -> dict:
        return {
            "threshold": self.threshold,
            "shape_xi": self.shape,
            "scale_beta": self.scale,
            "n_exceedances": self.n_exceedances,
            "n_total": self.n_total,
            "loglikelihood": self.loglikelihood,
        }


def fit_gpd(losses: pd.Series, threshold: float) -> GPDFit:
    """Fit a GPD by MLE to exceedances of `threshold` in a loss series."""
    exceedances = (losses[losses > threshold] - threshold).dropna()
    n_exceed = len(exceedances)
    if n_exceed < 10:
        raise ValueError(
            f"Only {n_exceed} exceedances above threshold {threshold}; "
            "need at least 10 for a minimally stable GPD fit."
        )
    # Fix loc=0 since we've already shifted by the threshold.
    shape, loc, scale = stats.genpareto.fit(exceedances.values, floc=0)
    loglik = float(np.sum(stats.genpareto.logpdf(exceedances.values, shape, loc=0, scale=scale)))
    return GPDFit(
        threshold=threshold,
        shape=float(shape),
        scale=float(scale),
        n_exceedances=n_exceed,
        n_total=len(losses.dropna()),
        loglikelihood=loglik,
    )


def threshold_stability(losses: pd.Series, thresholds: np.ndarray) -> pd.DataFrame:
    """Fit a GPD at each candidate threshold and report shape/scale, for a
    threshold-stability plot. Thresholds with too few exceedances are
    skipped (reported as NaN rows), not silently dropped from the table.
    """
    rows = []
    for u in thresholds:
        try:
            fit = fit_gpd(losses, u)
            rows.append(fit.to_dict())
        except ValueError:
            rows.append({
                "threshold": u, "shape_xi": np.nan, "scale_beta": np.nan,
                "n_exceedances": int((losses > u).sum()), "n_total": len(losses.dropna()),
                "loglikelihood": np.nan,
            })
    return pd.DataFrame(rows)


def gpd_var_es(fit: GPDFit, p: float) -> dict:
    """VaR and Expected Shortfall at tail probability p (e.g. 0.99) from a
    fitted GPD, using the standard POT formulas. Requires p to correspond
    to a probability *beyond* the fitted threshold's exceedance rate.
    """
    xi, beta, u = fit.shape, fit.scale, fit.threshold
    exceed_rate = fit.n_exceedances / fit.n_total
    if (1 - p) >= exceed_rate:
        raise ValueError(
            f"Tail probability p={p} is not beyond the fitted threshold's "
            f"exceedance rate ({exceed_rate:.4f}); VaR/ES formula is invalid here."
        )
    if abs(xi) < 1e-8:
        var = u + beta * np.log(exceed_rate / (1 - p))
    else:
        var = u + (beta / xi) * (((fit.n_total / fit.n_exceedances) * (1 - p)) ** (-xi) - 1)
    if xi >= 1:
        es = np.nan  # ES undefined/infinite for xi >= 1
    else:
        es = (var + beta - xi * u) / (1 - xi)
    return {"p": p, "VaR": float(var), "ES": float(es)}


def compare_tail_estimators(returns: pd.Series, gpd_fit: GPDFit, p_list: list[float]) -> pd.DataFrame:
    """Compare empirical quantile, normal, Student-t, and GPD VaR/ES at each
    tail probability in p_list, on the LOSS scale (positive = loss).
    """
    losses = -returns.dropna()
    mu, sigma = losses.mean(), losses.std(ddof=1)
    t_params = stats.t.fit(losses.values)
    rows = []
    for p in p_list:
        empirical_var = float(losses.quantile(p))
        tail_losses = losses[losses >= empirical_var]
        empirical_es = float(tail_losses.mean()) if len(tail_losses) > 0 else np.nan

        normal_var = float(stats.norm.ppf(p, loc=mu, scale=sigma))
        normal_es = float(mu + sigma * stats.norm.pdf(stats.norm.ppf(p)) / (1 - p))

        t_df, t_loc, t_scale = t_params
        t_var = float(stats.t.ppf(p, t_df, loc=t_loc, scale=t_scale))

        try:
            gpd_result = gpd_var_es(gpd_fit, p)
            gpd_var, gpd_es = gpd_result["VaR"], gpd_result["ES"]
        except ValueError:
            gpd_var, gpd_es = np.nan, np.nan

        rows.append({
            "p": p,
            "empirical_VaR": empirical_var, "empirical_ES": empirical_es,
            "normal_VaR": normal_var, "normal_ES": normal_es,
            "student_t_VaR": t_var,
            "gpd_VaR": gpd_var, "gpd_ES": gpd_es,
        })
    return pd.DataFrame(rows)
