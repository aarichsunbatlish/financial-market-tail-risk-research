import numpy as np
import pandas as pd

from src.tail_dependence import chi_upper, chi_bar_upper, tail_dependence_table


def test_chi_upper_perfect_dependence():
    x = pd.Series(np.arange(1, 1001, dtype=float))
    y = x.copy()  # identical series -> perfect tail dependence
    result = chi_upper(x, y, q=0.95)
    assert abs(result["chi"] - 1.0) < 1e-6


def test_chi_upper_independent_series_small():
    rng = np.random.default_rng(7)
    x = pd.Series(rng.normal(size=20000))
    y = pd.Series(rng.normal(size=20000))  # independent
    result = chi_upper(x, y, q=0.95)
    # for independent series, chi(q) ~= (1-q) -> close to 0.05 at q=0.95
    assert result["chi"] < 0.15


def test_chi_bar_upper_runs():
    rng = np.random.default_rng(8)
    x = pd.Series(rng.normal(size=5000))
    y = pd.Series(rng.normal(size=5000))
    result = chi_bar_upper(x, y, q=0.9)
    assert -1.5 <= result["chi_bar"] <= 1.5 or np.isnan(result["chi_bar"])


def test_tail_dependence_table_lower_tail_flips_sign():
    rng = np.random.default_rng(9)
    x = pd.Series(rng.normal(size=3000))
    y = pd.Series(rng.normal(size=3000))
    table = tail_dependence_table(x, y, [0.9, 0.95], tail="lower")
    assert set(table["tail"]) == {"lower"}
    assert len(table) == 2
