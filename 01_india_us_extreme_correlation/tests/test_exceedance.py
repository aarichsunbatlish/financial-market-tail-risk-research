import numpy as np
import pandas as pd

from src.exceedance import exceedance_correlation, exceedance_correlation_table, signed_single_conditioning


def _make_df(n=2000, seed=0, rho=0.5):
    rng = np.random.default_rng(seed)
    cov = [[1.0, rho], [rho, 1.0]]
    draws = rng.multivariate_normal([0, 0], cov, size=n)
    return pd.DataFrame({"nifty": draws[:, 0], "sp500": draws[:, 1]})


def test_exceedance_correlation_flags_insufficient_sample():
    df = _make_df(n=50, rho=0.5)
    result = exceedance_correlation(df, threshold=3.5, tail="left", min_count=15)
    assert result["n_exceedances"] < 15
    assert result["sufficient"] is False
    assert np.isnan(result["rho"])


def test_exceedance_correlation_manual_count_matches():
    df = pd.DataFrame({
        "nifty": [-3, -2, -1, 0, 1, 2, 3, -2.5, -2.2, -2.1],
        "sp500": [-3, -2, -1, 0, 1, 2, 3, -2.5, -0.1, -2.1],
    })
    # z-scores computed internally; just check the function runs end-to-end
    # and n_exceedances for threshold=0 (both negative) matches manual count.
    result = exceedance_correlation(df, threshold=0.0, tail="left", min_count=1)
    z_nifty = (df["nifty"] - df["nifty"].mean()) / df["nifty"].std(ddof=1)
    z_sp500 = (df["sp500"] - df["sp500"].mean()) / df["sp500"].std(ddof=1)
    expected_n = int(((z_nifty < 0) & (z_sp500 < 0)).sum())
    assert result["n_exceedances"] == expected_n


def test_exceedance_correlation_table_covers_both_tails():
    df = _make_df(n=3000, rho=0.4)
    table = exceedance_correlation_table(df, thresholds=[1.0, 1.5])
    assert set(table["tail"]) == {"left", "right"}
    assert len(table) == 4  # 2 tails x 2 thresholds


def test_signed_single_conditioning_runs():
    df = _make_df(n=2000, rho=0.3)
    result = signed_single_conditioning(df, threshold=1.0, tail="left", condition_on="nifty", other="sp500")
    assert result["n_exceedances"] > 0
    assert "rho" in result


def test_higher_threshold_gives_fewer_or_equal_exceedances():
    df = _make_df(n=5000, rho=0.5)
    low = exceedance_correlation(df, threshold=1.0, tail="left", min_count=1)
    high = exceedance_correlation(df, threshold=2.5, tail="left", min_count=1)
    assert high["n_exceedances"] <= low["n_exceedances"]
