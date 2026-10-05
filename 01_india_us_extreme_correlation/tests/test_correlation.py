import numpy as np
import pandas as pd

from src.correlation import unconditional_correlation, sign_conditional_correlation, rolling_correlation


def test_unconditional_correlation_matches_numpy():
    rng = np.random.default_rng(0)
    a = rng.normal(size=500)
    b = 0.6 * a + rng.normal(size=500) * 0.5
    df = pd.DataFrame({"nifty": a, "sp500": b})
    expected = np.corrcoef(a, b)[0, 1]
    assert abs(unconditional_correlation(df) - expected) < 1e-10


def test_unconditional_correlation_perfect():
    df = pd.DataFrame({"nifty": [1, 2, 3, 4], "sp500": [2, 4, 6, 8]})
    assert abs(unconditional_correlation(df) - 1.0) < 1e-10


def test_sign_conditional_correlation_counts():
    df = pd.DataFrame({"nifty": [-1, -2, 1, 2, -3, 3], "sp500": [-1, -3, 2, 1, -2, 4]})
    result = sign_conditional_correlation(df)
    assert result["n_negative"] == 3
    assert result["n_positive"] == 3


def test_rolling_correlation_window_length():
    rng = np.random.default_rng(1)
    df = pd.DataFrame({"nifty": rng.normal(size=100), "sp500": rng.normal(size=100)})
    roll = rolling_correlation(df, window=10)
    assert roll.isna().sum() == 9  # first (window-1) rows must be NaN
    assert len(roll) == 100
