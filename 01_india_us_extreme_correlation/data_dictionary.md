# Data Dictionary — Project 1

## Raw files (`data/raw/`)

### `nifty50_NSEI_daily.csv`

| Variable | Definition | Frequency | Source | Units | Notes |
|---|---|---|---|---|---|
| `Date` | Trading date | Daily (NSE trading days) | Third-party GitHub mirror of a Yahoo Finance `^NSEI` pull — see `data/raw/PROVENANCE.md` | ISO date | Indian trading calendar; NSE holidays differ from NYSE holidays |
| `Open`, `High`, `Low`, `Close` | OHLC index level | Daily | same | Index points | `Close` and `Adj Close` are identical in this file (index has no dividend adjustment in the usual equity sense) |
| `Volume` | Reported volume | Daily | same | Index-level volume (often 0 for index series — not a tradable instrument) | Not used in this project |

### `sp500_GSPC_daily.csv`

| Variable | Definition | Frequency | Source | Units | Notes |
|---|---|---|---|---|---|
| `date` | Trading date | Daily (NYSE trading days) | Third-party GitHub mirror of a Yahoo Finance `^GSPC` pull — see `PROVENANCE.md` | ISO date | US trading calendar |
| `ticker` | Constant `^GSPC` | — | — | — | Dropped after load |
| `open`, `high`, `low`, `close` | OHLC index level | Daily | same | Index points | |
| `volume` | Reported volume | Daily | same | Shares | Not used in this project |

## Derived / processed variables (`src/data_loader.py`, `src/config.py`)

| Variable | Definition | Transformation | Missing-value treatment | Potential bias |
|---|---|---|---|---|
| `log_return` | `ln(Close_t / Close_{t-1})` for each series | Natural-log return, computed independently per market on each market's own trading calendar | Rows with no valid prior close are dropped (first observation) | None introduced — standard return definition |
| `aligned_same_day` | India and US log returns joined on calendar date | Inner join on date — **both markets must have traded that day** | Days where only one market traded are dropped from this specific alignment | **Non-synchronous trading bias**: India's session closes (~09:15–15:30 IST) *before* the US session opens (~09:30–16:00 ET, i.e. ~19:00–01:30 IST the same/next day). A "same-day" match of Nifty's close to S&P 500's close for the *same calendar date* actually compares Nifty's close to an S&P 500 close that happened ~5–6 hours *later*, after Nifty's market had already closed. This is flagged explicitly and is why the lagged-US-return alignment (below) is the economically more defensible comparison for contemporaneous dependence. |
| `aligned_us_lag1` | Nifty return on day *t* vs. S&P 500 return on day *t-1* | Shift US series forward by one US trading day before joining | Same inner-join missing-day handling | Addresses the non-synchronous-trading bias above: by the time Nifty trades on day *t*, the most recently *completed* S&P 500 session is day *t-1* (US time), so this alignment is closer to "information actually available to Indian traders" |
| `aligned_weekly` | Weekly (Friday-to-Friday, or last available trading day each week) log returns for each market | Resample daily log returns to weekly by summing within each ISO week | Weeks with fewer than 3 valid daily observations on either side are dropped | Reduces (does not eliminate) the non-synchronous-trading and thin-tail-sample problems, at the cost of a much smaller tail sample |
| `z_score` | Return standardized by its own full-sample mean and standard deviation, per market | `(r - mean(r)) / std(r)`, computed separately for each market and each sub-period defined below | — | Standardizing over the *full* sample (vs. a rolling window) means thresholds are **not** adaptive to time-varying volatility — this is a deliberate simplification for Project 1, addressed directly by Project 13 (GARCH+EVT) |
| Sub-period labels | `pre_gfc`, `gfc`, `covid`, `post_2020` | Fixed calendar date ranges — see `src/config.py` | — | Boundary choice is a modeling decision, not derived from a statistical break test; this is disclosed as a limitation, and threshold/period-boundary robustness is checked |

## Sub-period definitions (see `src/config.py` for exact dates)

| Label | Window | Rationale |
|---|---|---|
| `pre_gfc` | 2007-09-17 → 2007-12-31 | Short pre-crisis window available in this dataset (Nifty series starts Sept 2007) |
| `gfc` | 2008-01-01 → 2009-06-30 | Global Financial Crisis and immediate aftermath |
| `interim` | 2009-07-01 → 2020-01-31 | Between-crises period (includes 2013 taper tantrum, 2015–16 China-led selloff — not separately labeled) |
| `covid` | 2020-02-01 → 2020-12-31 | COVID-19 shock and initial recovery |
| `post_2020` | 2021-01-01 → end of sample | Post-COVID period |

These boundaries are judgment calls made for interpretability, not the
output of a formal structural-break test (e.g. Bai–Perron). A robustness
check using an automatically detected break instead of these fixed dates is
listed as a limitation/future extension.

## Known biases and data-quality caveats (see also `PROVENANCE.md`)

- **Survivorship bias**: not applicable — these are index levels, not a
  hand-picked stock universe.
- **Look-ahead bias**: none introduced by this pipeline — all
  transformations use only information available at or before time *t*.
- **Selection bias**: the choice of India and the US specifically (rather
  than, say, India and the UK) is motivated by the research question, not
  by data availability; this is disclosed as a design choice, not a flaw.
- **Non-synchronous trading**: see `aligned_same_day` vs. `aligned_us_lag1`
  above — this is the most important data-methodology issue in this project
  and is treated as a first-class robustness axis, not a footnote.
- **Data provenance**: both raw files come from unofficial third-party
  GitHub mirrors, not an audited vendor feed (see `PROVENANCE.md` for the
  specific historical-fact checks performed to validate them).
