import numpy as np
import pandas as pd
from scipy import stats

from src.evt import mean_excess_function, fit_gpd, threshold_stability, gpd_var_es, compare_tail_estimators


def test_fit_gpd_recovers_known_parameters():
    rng = np.random.default_rng(42)
    true_xi, true_beta = 0.25, 1.5
    exceedances = stats.genpareto.rvs(true_xi, loc=0, scale=true_beta, size=5000, random_state=rng)
    losses = pd.Series(exceedances)  # threshold = 0, losses are exceedances directly
    fit = fit_gpd(losses, threshold=0.0)
    assert abs(fit.shape - true_xi) < 0.08
    assert abs(fit.scale - true_beta) < 0.2
    assert fit.n_exceedances == 5000


def test_fit_gpd_raises_on_too_few_exceedances():
    losses = pd.Series([0.1, 0.2, 0.05, 0.3])
    try:
        fit_gpd(losses, threshold=0.0)
        assert False, "should have raised"
    except ValueError:
        pass


def test_mean_excess_function_decreasing_count():
    losses = pd.Series(np.abs(np.random.default_rng(1).normal(size=2000)))
    thresholds = np.array([0.5, 1.0, 1.5, 2.0])
    me_df = mean_excess_function(losses, thresholds)
    counts = me_df["n_exceedances"].values
    assert all(counts[i] >= counts[i + 1] for i in range(len(counts) - 1))


def test_threshold_stability_returns_row_per_threshold():
    losses = pd.Series(np.abs(np.random.default_rng(2).normal(size=3000)))
    thresholds = np.array([0.5, 1.0, 1.5])
    stab = threshold_stability(losses, thresholds)
    assert len(stab) == 3


def test_gpd_var_es_exponential_case_xi_zero():
    # xi=0 reduces the GPD to an exponential; VaR has a closed form we can
    # check directly: VaR_p = u + beta*ln((n/Nu)*(1-p)) ... our code's
    # formula branch for |xi|<1e-8 should match this closed form exactly.
    from src.evt import GPDFit
    fit = GPDFit(threshold=1.0, shape=0.0, scale=2.0, n_exceedances=500, n_total=10000, loglikelihood=0.0)
    result = gpd_var_es(fit, p=0.999)
    exceed_rate = 500 / 10000
    expected_var = 1.0 + 2.0 * np.log(exceed_rate / (1 - 0.999))
    assert abs(result["VaR"] - expected_var) < 1e-9


def test_gpd_var_es_rejects_invalid_probability():
    from src.evt import GPDFit
    fit = GPDFit(threshold=1.0, shape=0.2, scale=1.0, n_exceedances=100, n_total=10000, loglikelihood=0.0)
    # exceed_rate = 0.01; p=0.5 implies (1-p)=0.5 >> 0.01, invalid
    try:
        gpd_var_es(fit, p=0.5)
        assert False, "should have raised"
    except ValueError:
        pass


def test_compare_tail_estimators_runs_and_orders_sensibly():
    rng = np.random.default_rng(3)
    returns = pd.Series(rng.standard_t(df=4, size=4000) * 0.01)
    losses = -returns
    threshold = float(np.quantile(losses, 0.95))
    fit = fit_gpd(losses, threshold)
    table = compare_tail_estimators(returns, fit, [0.99, 0.999])
    assert len(table) == 2
    # ES should be >= VaR at the same probability for every estimator reported
    assert (table["empirical_ES"] >= table["empirical_VaR"]).all()
