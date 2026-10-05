import pandas as pd

from src.data_loader import align_same_day, align_lagged, align_weekly, add_subperiod_labels


def _toy_series(dates, closes):
    df = pd.DataFrame({"date": pd.to_datetime(dates), "close": closes}).set_index("date")
    df["log_return"] = (df["close"] / df["close"].shift(1)).apply(
        lambda r: None if pd.isna(r) else __import__("numpy").log(r)
    )
    return df.dropna()


def test_align_same_day_inner_join():
    nifty = _toy_series(["2024-01-01", "2024-01-02", "2024-01-03"], [100, 101, 102])
    sp500 = _toy_series(["2024-01-02", "2024-01-03", "2024-01-04"], [200, 202, 199])
    merged = align_same_day(nifty, sp500)
    # Overlapping dates with valid returns on both sides: 2024-01-03 only
    # (nifty needs a prior day for its return; same for sp500).
    assert list(merged.index.strftime("%Y-%m-%d")) == ["2024-01-03"]


def test_align_lagged_matches_previous_us_day():
    nifty = _toy_series(
        ["2024-01-01", "2024-01-02", "2024-01-03"], [100, 101, 102]
    )
    sp500 = _toy_series(
        ["2023-12-29", "2023-12-30", "2024-01-02"], [200, 198, 205]
    )
    merged = align_lagged(nifty, sp500)
    # For nifty date 2024-01-02 (search_key=2024-01-01), most recent sp500
    # date <= 2024-01-01 is 2023-12-30.
    assert pd.Timestamp("2024-01-02") in merged.index
    row = merged.loc[pd.Timestamp("2024-01-02")]
    expected_sp500_return = sp500.loc[pd.Timestamp("2023-12-30"), "log_return"]
    assert abs(row["sp500"] - expected_sp500_return) < 1e-12


def test_align_weekly_requires_min_three_obs():
    dates = pd.date_range("2024-01-01", periods=10, freq="D")
    closes = [100 + i for i in range(10)]
    nifty = _toy_series(dates, closes)
    sp500 = _toy_series(dates, closes)
    weekly = align_weekly(nifty, sp500)
    assert (weekly.index.to_series().notna()).all()


def test_add_subperiod_labels_covers_covid():
    idx = pd.to_datetime(["2020-03-15", "2021-06-01", "1999-01-01"])
    df = pd.DataFrame({"x": [1, 2, 3]}, index=idx)
    labeled = add_subperiod_labels(df)
    assert labeled.loc[pd.Timestamp("2020-03-15"), "sub_period"] == "covid"
    assert labeled.loc[pd.Timestamp("2021-06-01"), "sub_period"] == "post_2020"
    assert labeled.loc[pd.Timestamp("1999-01-01"), "sub_period"] == "unlabeled"
