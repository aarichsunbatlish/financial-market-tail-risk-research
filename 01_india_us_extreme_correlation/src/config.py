"""Configuration constants for Project 1 (India-US extreme correlation).

Centralizing these here means every module and every notebook uses the same
thresholds, sub-period boundaries, and random seed -- consistent with the
portfolio's reproducibility rules.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
FIGURES_DIR = PROJECT_ROOT / "figures"
TABLES_DIR = PROJECT_ROOT / "tables"
RESULTS_DIR = PROJECT_ROOT / "results"

NIFTY_RAW_PATH = RAW_DATA_DIR / "nifty50_NSEI_daily.csv"
SP500_RAW_PATH = RAW_DATA_DIR / "sp500_GSPC_daily.csv"

RANDOM_SEED = 20261005  # fixed for reproducibility across the whole project

# Exceedance-correlation thresholds, in standard deviations.
SIGMA_THRESHOLDS = [1.0, 1.5, 2.0, 2.5, 3.0]

# Minimum number of joint exceedances required to report a point estimate
# at a given threshold -- below this, the pipeline reports "insufficient
# sample" rather than a misleadingly precise number.
MIN_EXCEEDANCE_COUNT = 15

# Monte Carlo / bootstrap parameters.
N_MONTE_CARLO_DRAWS = 5_000
N_BOOTSTRAP_REPLICATIONS = 2_000
BOOTSTRAP_CONFIDENCE_LEVEL = 0.95

# GPD tail-risk probabilities to report VaR/ES at.
TAIL_PROBABILITIES = [0.99, 0.995, 0.999]

# Rolling-correlation window lengths, in trading days.
ROLLING_WINDOWS = [60, 250]


@dataclass(frozen=True)
class SubPeriod:
    label: str
    start: str  # ISO date, inclusive
    end: str    # ISO date, inclusive
    description: str


SUB_PERIODS: list[SubPeriod] = [
    SubPeriod("pre_gfc", "2007-09-17", "2007-12-31",
              "Short pre-crisis window available in this dataset"),
    SubPeriod("gfc", "2008-01-01", "2009-06-30",
              "Global Financial Crisis and immediate aftermath"),
    SubPeriod("interim", "2009-07-01", "2020-01-31",
              "Between-crises period"),
    SubPeriod("covid", "2020-02-01", "2020-12-31",
              "COVID-19 shock and initial recovery"),
    SubPeriod("post_2020", "2021-01-01", "2026-12-31",
              "Post-COVID period (end date is a cap, not a claim about "
              "data availability beyond the actual sample end)"),
]

FULL_SAMPLE_LABEL = "full_sample"
