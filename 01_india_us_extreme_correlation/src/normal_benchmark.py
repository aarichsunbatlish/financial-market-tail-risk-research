"""Monte Carlo bivariate-normal benchmark for exceedance correlation
(Longin & Solnik, 2001 test), implemented by simulation rather than the
closed-form asymptotic formula -- see methodology.md Section 7.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .exceedance import exceedance_correlation


def simulate_normal_exceedance_distribution(
    n_obs: int,
    rho: float,
    sigma_a: float,
    sigma_b: float,
    threshold: float,
    tail: str,
    n_reps: int,
    seed: int,
    min_count: int = 15,
) -> np.ndarray:
    """Simulate `n_reps` samples of size `n_obs` from a bivariate normal
    with correlation `rho` and the given marginal standard deviations, and
    compute the exceedance correlation at `threshold`/`tail` for each.

    Returns an array of length n_reps (NaN where a given replication had
    too few exceedances to report, matching the real-data convention).
    """
    rng = np.random.default_rng(seed)
    cov = np.array([
        [sigma_a ** 2, rho * sigma_a * sigma_b],
        [rho * sigma_a * sigma_b, sigma_b ** 2],
    ])
    results = np.full(n_reps, np.nan)
    for i in range(n_reps):
        draws = rng.multivariate_normal(mean=[0.0, 0.0], cov=cov, size=n_obs)
        sim_df = pd.DataFrame({"a": draws[:, 0], "b": draws[:, 1]})
        res = exceedance_correlation(sim_df, threshold, tail, "a", "b", min_count)
        results[i] = res["rho"]
    return results


def normal_benchmark_test(
    df: pd.DataFrame,
    thresholds: list[float],
    n_reps: int,
    seed: int,
    col_a: str = "nifty",
    col_b: str = "sp500",
    min_count: int = 15,
) -> pd.DataFrame:
    """For each threshold and tail, compare the observed exceedance
    correlation against a bivariate-normal Monte Carlo benchmark matched to
    the sample's unconditional correlation and marginal volatilities.

    One-sided Monte Carlo p-value (left tail): fraction of simulated
    normal-benchmark exceedance correlations >= the observed value, testing
    H1: observed left-tail dependence exceeds what normality implies
    (the Longin-Solnik asymmetry hypothesis).
    """
    clean = df[[col_a, col_b]].dropna()
    rho = float(clean[col_a].corr(clean[col_b]))
    sigma_a = float(clean[col_a].std(ddof=1))
    sigma_b = float(clean[col_b].std(ddof=1))
    n_obs = len(clean)

    rows = []
    for tail in ("left", "right"):
        for thr in thresholds:
            observed = exceedance_correlation(clean, thr, tail, col_a, col_b, min_count)
            sim = simulate_normal_exceedance_distribution(
                n_obs, rho, sigma_a, sigma_b, thr, tail, n_reps, seed, min_count,
            )
            sim_valid = sim[~np.isnan(sim)]
            if not observed["sufficient"] or len(sim_valid) < n_reps * 0.5:
                rows.append({
                    "tail": tail, "threshold": thr,
                    "observed_rho": observed["rho"], "n_exceedances": observed["n_exceedances"],
                    "sim_median": np.nan, "sim_ci_lower": np.nan, "sim_ci_upper": np.nan,
                    "mc_pvalue_one_sided": np.nan, "note": "insufficient exceedances",
                })
                continue
            p_value = float(np.mean(sim_valid >= observed["rho"]))
            rows.append({
                "tail": tail, "threshold": thr,
                "observed_rho": observed["rho"], "n_exceedances": observed["n_exceedances"],
                "sim_median": float(np.median(sim_valid)),
                "sim_ci_lower": float(np.percentile(sim_valid, 2.5)),
                "sim_ci_upper": float(np.percentile(sim_valid, 97.5)),
                "mc_pvalue_one_sided": p_value,
                "note": "",
            })
    result = pd.DataFrame(rows)
    n_tests = int(result["mc_pvalue_one_sided"].notna().sum())
    if n_tests > 0:
        result["bonferroni_pvalue"] = (result["mc_pvalue_one_sided"] * n_tests).clip(upper=1.0)
    else:
        result["bonferroni_pvalue"] = np.nan
    return result
