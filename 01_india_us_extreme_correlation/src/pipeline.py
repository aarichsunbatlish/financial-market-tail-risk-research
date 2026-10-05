"""End-to-end pipeline for Project 1: India-US extreme correlation.

Running this module as a script loads the real data, runs every analysis
described in methodology.md, and writes figures/tables/results to disk.
Every number that ends up in the research paper is produced by this
pipeline -- nothing is hand-entered.
"""
from __future__ import annotations

import json
import logging

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from . import config
from .data_loader import (
    load_nifty, load_sp500, align_same_day, align_lagged, align_weekly,
    add_subperiod_labels,
)
from .descriptive import compute_descriptive_stats, qq_points
from .correlation import rolling_correlation, unconditional_correlation, sign_conditional_correlation
from .exceedance import exceedance_correlation, exceedance_correlation_table, signed_single_conditioning
from .evt import mean_excess_function, fit_gpd, threshold_stability, compare_tail_estimators
from .tail_dependence import tail_dependence_table
from .normal_benchmark import normal_benchmark_test
from .bootstrap import moving_block_bootstrap_ci

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)


def _ensure_dirs() -> None:
    for d in (config.FIGURES_DIR, config.TABLES_DIR, config.RESULTS_DIR, config.PROCESSED_DATA_DIR):
        d.mkdir(parents=True, exist_ok=True)


def run_full_pipeline(
    normal_benchmark_reps: int = 1000,
    bootstrap_reps: int = 1000,
) -> dict:
    _ensure_dirs()
    summary: dict = {}

    logger.info("Loading raw data...")
    nifty = load_nifty()
    sp500 = load_sp500()
    summary["data_coverage"] = {
        "nifty_start": str(nifty.index.min().date()), "nifty_end": str(nifty.index.max().date()),
        "nifty_n_obs": int(len(nifty)),
        "sp500_start": str(sp500.index.min().date()), "sp500_end": str(sp500.index.max().date()),
        "sp500_n_obs": int(len(sp500)),
    }

    same_day = align_same_day(nifty, sp500)
    lagged = align_lagged(nifty, sp500)
    weekly = align_weekly(nifty, sp500)
    summary["alignment_n_obs"] = {
        "same_day": int(len(same_day)), "us_lag1": int(len(lagged)), "weekly": int(len(weekly)),
    }
    logger.info("Alignment sample sizes: %s", summary["alignment_n_obs"])

    # ---- 1. Descriptive statistics ----
    desc_rows = []
    for name, series in [("nifty_daily", nifty["log_return"]), ("sp500_daily", sp500["log_return"])]:
        desc_rows.append({"series": name, **compute_descriptive_stats(series).to_dict()})
    desc_df = pd.DataFrame(desc_rows)
    desc_df.to_csv(config.TABLES_DIR / "descriptive_stats.csv", index=False)
    summary["descriptive_stats"] = desc_df.to_dict(orient="records")

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    for ax, (name, series) in zip(axes, [("Nifty 50", nifty["log_return"]), ("S&P 500", sp500["log_return"])]):
        theo, samp = qq_points(series)
        ax.scatter(theo, samp, s=4, alpha=0.5)
        lo, hi = min(theo.min(), samp.min()), max(theo.max(), samp.max())
        ax.plot([lo, hi], [lo, hi], "r--", linewidth=1)
        ax.set_title(f"QQ plot (normal): {name}")
        ax.set_xlabel("Theoretical quantile")
        ax.set_ylabel("Sample quantile (standardized)")
    fig.tight_layout()
    fig.savefig(config.FIGURES_DIR / "qq_plots.png", dpi=150)
    plt.close(fig)

    # ---- 2. Rolling correlation ----
    fig2, ax2 = plt.subplots(figsize=(12, 5))
    for w in config.ROLLING_WINDOWS:
        roll = rolling_correlation(lagged, w)
        roll.to_csv(config.TABLES_DIR / f"rolling_correlation_{w}d.csv", header=["correlation"])
        ax2.plot(roll.index, roll.values, label=f"{w}-day rolling", linewidth=1)
    ax2.axhline(0, color="black", linewidth=0.5)
    ax2.set_title("Rolling Nifty 50 - S&P 500 correlation (US lag-1 alignment)")
    ax2.set_ylabel("Pearson correlation")
    ax2.legend()
    fig2.tight_layout()
    fig2.savefig(config.FIGURES_DIR / "rolling_correlation.png", dpi=150)
    plt.close(fig2)

    sign_cond = sign_conditional_correlation(lagged)
    summary["sign_conditional_correlation"] = sign_cond

    # ---- 3. Exceedance correlation (core result) ----
    exc_table = exceedance_correlation_table(lagged, config.SIGMA_THRESHOLDS)
    exc_table.to_csv(config.TABLES_DIR / "exceedance_correlation_full_sample.csv", index=False)

    signed_rows = []
    for tail in ("left", "right"):
        for thr in config.SIGMA_THRESHOLDS:
            signed_rows.append(signed_single_conditioning(lagged, thr, tail, "nifty", "sp500"))
            signed_rows.append(signed_single_conditioning(lagged, thr, tail, "sp500", "nifty"))
    signed_df = pd.DataFrame(signed_rows)
    signed_df.to_csv(config.TABLES_DIR / "signed_single_conditioning.csv", index=False)

    # ---- 4. Normal-model benchmark (Longin-Solnik test) ----
    logger.info("Running normal-benchmark Monte Carlo (this takes a bit)...")
    nb_table = normal_benchmark_test(lagged, config.SIGMA_THRESHOLDS, normal_benchmark_reps, config.RANDOM_SEED)
    nb_table.to_csv(config.TABLES_DIR / "normal_benchmark_test.csv", index=False)

    fig3, ax3 = plt.subplots(figsize=(8, 6))
    for tail, marker, color in [("left", "o", "tab:red"), ("right", "s", "tab:blue")]:
        sub = nb_table[nb_table["tail"] == tail].dropna(subset=["observed_rho"])
        ax3.plot(sub["threshold"], sub["observed_rho"], marker=marker, color=color, label=f"observed ({tail})")
        valid = sub.dropna(subset=["sim_median"])
        if len(valid) > 0:
            ax3.plot(valid["threshold"], valid["sim_median"], linestyle="--", color=color, alpha=0.6, label=f"normal benchmark ({tail})")
            ax3.fill_between(valid["threshold"], valid["sim_ci_lower"], valid["sim_ci_upper"], color=color, alpha=0.15)
    ax3.set_xlabel("Threshold (standard deviations)")
    ax3.set_ylabel("Exceedance correlation")
    ax3.set_title("Exceedance correlation vs. bivariate-normal benchmark\n(Nifty 50 - S&P 500, US lag-1 alignment)")
    ax3.legend(fontsize=8)
    fig3.tight_layout()
    fig3.savefig(config.FIGURES_DIR / "exceedance_correlation_vs_normal_benchmark.png", dpi=150)
    plt.close(fig3)

    # ---- 5. Sub-period exceedance correlation ----
    lagged_labeled = add_subperiod_labels(lagged)
    subperiod_rows = []
    for label in lagged_labeled["sub_period"].unique():
        subset = lagged_labeled[lagged_labeled["sub_period"] == label]
        if len(subset) < 30:
            logger.info("Sub-period '%s' has only %d obs; skipping exceedance table.", label, len(subset))
            continue
        tbl = exceedance_correlation_table(subset, [1.0, 1.5, 2.0])
        tbl["sub_period"] = label
        tbl["n_obs_in_period"] = len(subset)
        subperiod_rows.append(tbl)
    subperiod_df = pd.concat(subperiod_rows, ignore_index=True) if subperiod_rows else pd.DataFrame()
    subperiod_df.to_csv(config.TABLES_DIR / "exceedance_correlation_by_subperiod.csv", index=False)

    # ---- 6. EVT / GPD tail modelling (each market's own return series) ----
    gpd_summary = {}
    gpd_compare_tables = {}
    for name, returns in [("nifty", nifty["log_return"]), ("sp500", sp500["log_return"])]:
        losses = -returns.dropna()
        candidate_q = [0.90, 0.92, 0.94, 0.95, 0.96, 0.97, 0.98]
        candidate_thresholds = np.quantile(losses, candidate_q)
        me_df = mean_excess_function(losses, candidate_thresholds)
        me_df["quantile"] = candidate_q
        me_df.to_csv(config.TABLES_DIR / f"mean_excess_{name}.csv", index=False)

        stab_df = threshold_stability(losses, candidate_thresholds)
        stab_df["quantile"] = candidate_q
        stab_df.to_csv(config.TABLES_DIR / f"threshold_stability_{name}.csv", index=False)

        fig4, (ax4a, ax4b) = plt.subplots(1, 2, figsize=(11, 4.5))
        ax4a.plot(me_df["threshold"], me_df["mean_excess"], marker="o")
        ax4a.set_title(f"Mean excess plot: {name}")
        ax4a.set_xlabel("Threshold (loss)")
        ax4a.set_ylabel("Mean excess")
        ax4b.plot(stab_df["threshold"], stab_df["shape_xi"], marker="o")
        ax4b.set_title(f"Threshold stability (shape ξ): {name}")
        ax4b.set_xlabel("Threshold (loss)")
        ax4b.set_ylabel("Shape ξ")
        fig4.tight_layout()
        fig4.savefig(config.FIGURES_DIR / f"evt_threshold_diagnostics_{name}.png", dpi=150)
        plt.close(fig4)

        chosen_threshold = float(np.quantile(losses, 0.95))
        gpd_fit = fit_gpd(losses, chosen_threshold)
        gpd_summary[name] = gpd_fit.to_dict()

        compare_df = compare_tail_estimators(returns, gpd_fit, config.TAIL_PROBABILITIES)
        compare_df.to_csv(config.TABLES_DIR / f"var_es_comparison_{name}.csv", index=False)
        gpd_compare_tables[name] = compare_df.to_dict(orient="records")

    summary["gpd_fits_95th_percentile_threshold"] = gpd_summary
    summary["var_es_comparison"] = gpd_compare_tables

    # ---- 7. Tail dependence (chi, chi-bar) ----
    td_table = tail_dependence_table(lagged["nifty"], lagged["sp500"], [0.90, 0.95, 0.975, 0.99], tail="lower")
    td_table.to_csv(config.TABLES_DIR / "tail_dependence_chi.csv", index=False)

    fig5, ax5 = plt.subplots(figsize=(7, 5))
    ax5.plot(td_table["q"], td_table["chi"], marker="o", label="chi(q)")
    ax5.plot(td_table["q"], td_table["chi_bar"], marker="s", label="chi_bar(q)")
    ax5.set_xlabel("Quantile q")
    ax5.set_ylabel("Coefficient")
    ax5.set_title("Lower-tail dependence diagnostics: Nifty 50 vs. S&P 500")
    ax5.legend()
    fig5.tight_layout()
    fig5.savefig(config.FIGURES_DIR / "tail_dependence_chi.png", dpi=150)
    plt.close(fig5)

    # ---- 8. Bootstrap confidence intervals ----
    logger.info("Running moving block bootstrap...")
    corr_ci = moving_block_bootstrap_ci(
        lagged, lambda d: unconditional_correlation(d), n_reps=bootstrap_reps, seed=config.RANDOM_SEED,
    )
    exc_ci_left_2sigma = moving_block_bootstrap_ci(
        lagged, lambda d: exceedance_correlation(d, 2.0, "left")["rho"],
        n_reps=max(300, bootstrap_reps // 2), seed=config.RANDOM_SEED + 1,
    )
    summary["bootstrap_ci"] = {
        "unconditional_correlation": corr_ci,
        "exceedance_correlation_left_2sigma": exc_ci_left_2sigma,
    }

    # ---- 9. Robustness: alignment comparison ----
    alignment_rows = []
    for name, data in [("same_day", same_day), ("us_lag1", lagged), ("weekly", weekly)]:
        row = {"alignment": name, "n_obs": len(data), "unconditional_corr": unconditional_correlation(data)}
        for thr in (1.5, 2.0):
            row[f"exceedance_left_{thr}sigma"] = exceedance_correlation(data, thr, "left")["rho"]
            row[f"exceedance_left_{thr}sigma_n"] = exceedance_correlation(data, thr, "left")["n_exceedances"]
        alignment_rows.append(row)
    alignment_df = pd.DataFrame(alignment_rows)
    alignment_df.to_csv(config.TABLES_DIR / "robustness_alignment_comparison.csv", index=False)
    summary["robustness_alignment_comparison"] = alignment_df.to_dict(orient="records")

    # ---- Save master summary ----
    with open(config.RESULTS_DIR / "pipeline_summary.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)

    logger.info("Pipeline complete. Outputs in figures/, tables/, results/.")
    return summary


if __name__ == "__main__":
    run_full_pipeline()
