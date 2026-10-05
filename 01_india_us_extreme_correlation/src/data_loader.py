"""Data loading, validation, and alignment for Project 1.

Loads the raw Nifty 50 and S&P 500 daily series, computes log returns,
flags (does not silently fix) data-quality issues, and produces three
distinct alignments of the two return series -- same-calendar-day,
US-lagged-by-one-day, and weekly -- because which alignment is used
materially changes the answer to this project's research question (see
data_dictionary.md).
"""
from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from . import config

logger = logging.getLogger(__name__)

# A single-day log return larger than this in absolute value is flagged
# (not removed) as worth a human's attention -- real markets do move this
# much on genuine crisis days, so this is a flag, not a filter.
EXTREME_RETURN_FLAG_THRESHOLD = 0.20


def _sanity_check(df: pd.DataFrame, name: str, price_col: str = "close") -> None:
    """Log warnings for common data-quality problems. Never mutates df."""
    if df.index.has_duplicates:
        n_dup = df.index.duplicated().sum()
        logger.warning("%s: %d duplicate dates found in raw data.", name, n_dup)
    if not df.index.is_monotonic_increasing:
        logger.warning("%s: dates are not sorted ascending.", name)
    if (df[price_col] <= 0).any():
        n_bad = int((df[price_col] <= 0).sum())
        logger.warning("%s: %d non-positive prices found.", name, n_bad)
    gaps = df.index.to_series().diff().dt.days
    big_gaps = gaps[gaps > 10]
    if len(big_gaps) > 0:
        logger.warning(
            "%s: %d calendar gaps longer than 10 days (check for missing "
            "data vs. genuine market closures).", name, len(big_gaps),
        )


def load_nifty(path: Path = config.NIFTY_RAW_PATH) -> pd.DataFrame:
    """Load the raw Nifty 50 CSV and compute log returns.

    Returns a DataFrame indexed by Date with columns ['close', 'log_return'].
    """
    raw = pd.read_csv(path, parse_dates=["Date"])
    raw = raw.rename(columns={"Date": "date", "Close": "close"})
    raw = raw[["date", "close"]].drop_duplicates(subset="date").sort_values("date")
    df = raw.set_index("date")
    _sanity_check(df, "Nifty 50")
    df["log_return"] = np.log(df["close"] / df["close"].shift(1))
    flagged = df.index[df["log_return"].abs() > EXTREME_RETURN_FLAG_THRESHOLD]
    if len(flagged) > 0:
        logger.info(
            "Nifty 50: %d days with |log return| > %.0f%% (plausible crisis "
            "days, not removed): %s",
            len(flagged), EXTREME_RETURN_FLAG_THRESHOLD * 100,
            list(flagged.strftime("%Y-%m-%d")),
        )
    return df.dropna(subset=["log_return"])


def load_sp500(path: Path = config.SP500_RAW_PATH) -> pd.DataFrame:
    """Load the raw S&P 500 CSV and compute log returns.

    Returns a DataFrame indexed by date with columns ['close', 'log_return'].
    """
    raw = pd.read_csv(path, parse_dates=["date"])
    raw = raw[["date", "close"]].drop_duplicates(subset="date").sort_values("date")
    df = raw.set_index("date")
    _sanity_check(df, "S&P 500")
    df["log_return"] = np.log(df["close"] / df["close"].shift(1))
    flagged = df.index[df["log_return"].abs() > EXTREME_RETURN_FLAG_THRESHOLD]
    if len(flagged) > 0:
        logger.info(
            "S&P 500: %d days with |log return| > %.0f%% (plausible crisis "
            "days, not removed): %s",
            len(flagged), EXTREME_RETURN_FLAG_THRESHOLD * 100,
            list(flagged.strftime("%Y-%m-%d")),
        )
    return df.dropna(subset=["log_return"])


def align_same_day(nifty: pd.DataFrame, sp500: pd.DataFrame) -> pd.DataFrame:
    """Naive same-calendar-day alignment (inner join on date).

    This is the economically naive alignment: because the Nifty session
    closes hours before the S&P 500 session of the *same calendar date*
    even opens, matching them on the same date implicitly uses information
    (the US close) that did not exist yet when Nifty traded that day. Kept
    for comparison against `align_lagged`, which corrects for this.
    """
    merged = nifty[["log_return"]].join(
        sp500[["log_return"]], how="inner", lsuffix="_nifty", rsuffix="_sp500",
    )
    merged = merged.rename(
        columns={"log_return_nifty": "nifty", "log_return_sp500": "sp500"}
    )
    return merged


def align_lagged(nifty: pd.DataFrame, sp500: pd.DataFrame) -> pd.DataFrame:
    """Nifty return on day t vs. the most recently *completed* S&P 500
    session as of Nifty's trading time on day t (i.e. the most recent US
    trading day strictly before t).

    Implemented with merge_asof: for each Nifty date t, find the latest
    S&P 500 trading date <= (t - 1 calendar day).
    """
    left = nifty[["log_return"]].reset_index().rename(
        columns={"date": "nifty_date", "log_return": "nifty"}
    )
    right = sp500[["log_return"]].reset_index().rename(
        columns={"date": "us_date", "log_return": "sp500"}
    )
    left["search_key"] = left["nifty_date"] - pd.Timedelta(days=1)
    merged = pd.merge_asof(
        left.sort_values("search_key"),
        right.sort_values("us_date"),
        left_on="search_key",
        right_on="us_date",
        direction="backward",
    )
    merged = merged.dropna(subset=["nifty", "sp500"]).set_index("nifty_date")
    return merged[["nifty", "sp500"]].sort_index()


def align_weekly(nifty: pd.DataFrame, sp500: pd.DataFrame) -> pd.DataFrame:
    """Weekly log returns (sum of daily log returns within each ISO week,
    Monday-anchored), joined on week. Reduces (does not eliminate) the
    non-synchronous-trading issue at the cost of a much smaller sample.
    """
    nifty_weekly = nifty["log_return"].resample("W-FRI").sum()
    sp500_weekly = sp500["log_return"].resample("W-FRI").sum()
    merged = pd.DataFrame({"nifty": nifty_weekly, "sp500": sp500_weekly}).dropna()
    # Require at least 3 underlying daily observations on each side within
    # the week to avoid weeks dominated by a single holiday-shortened session.
    nifty_counts = nifty["log_return"].resample("W-FRI").count()
    sp500_counts = sp500["log_return"].resample("W-FRI").count()
    valid_weeks = (nifty_counts >= 3) & (sp500_counts >= 3)
    return merged[merged.index.isin(valid_weeks[valid_weeks].index)]


def add_subperiod_labels(df: pd.DataFrame) -> pd.DataFrame:
    """Add a 'sub_period' column based on config.SUB_PERIODS. Rows outside
    all defined windows are labeled 'unlabeled' rather than silently dropped.
    """
    out = df.copy()
    out["sub_period"] = "unlabeled"
    for sp in config.SUB_PERIODS:
        mask = (out.index >= pd.Timestamp(sp.start)) & (out.index <= pd.Timestamp(sp.end))
        out.loc[mask, "sub_period"] = sp.label
    return out


def zscore_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Full-sample z-scores for the given columns. See methodology.md
    Section 10 for why full-sample (not rolling) standardization is used
    here, and its limitation.
    """
    out = df.copy()
    for col in columns:
        mu, sigma = out[col].mean(), out[col].std(ddof=1)
        out[f"{col}_z"] = (out[col] - mu) / sigma
    return out
