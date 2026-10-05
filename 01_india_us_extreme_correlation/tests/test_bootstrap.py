import numpy as np
import pandas as pd

from src.bootstrap import default_block_length, moving_block_bootstrap_sample, moving_block_bootstrap_ci


def test_default_block_length_grows_with_n():
    assert default_block_length(1000) > default_block_length(10)


def test_moving_block_bootstrap_sample_same_length():
    df = pd.DataFrame({"a": np.arange(100)})
    rng = np.random.default_rng(0)
    resample = moving_block_bootstrap_sample(df, block_length=5, rng=rng)
    assert len(resample) == len(df)


def test_bootstrap_ci_constant_statistic_is_degenerate():
    df = pd.DataFrame({"a": np.arange(200)})
    result = moving_block_bootstrap_ci(df, stat_func=lambda d: 42.0, n_reps=50, seed=0)
    assert result["point_estimate"] == 42.0
    assert result["ci_lower"] == 42.0
    assert result["ci_upper"] == 42.0


def test_bootstrap_ci_mean_reasonable():
    rng = np.random.default_rng(1)
    df = pd.DataFrame({"a": rng.normal(loc=5.0, scale=1.0, size=500)})
    result = moving_block_bootstrap_ci(df, stat_func=lambda d: d["a"].mean(), n_reps=300, seed=1)
    assert result["ci_lower"] < 5.0 < result["ci_upper"]
