# Raw Data Provenance — Project 1 (India–US Extreme Correlation)

This file documents exactly where the raw price series in this folder came from,
how they were obtained, and how their authenticity was checked. Per the
portfolio's research-integrity rules, no price data in this repository is
fabricated or simulated and presented as real; everything below is traceable.

## 1. Nifty 50 — `nifty50_NSEI_daily.csv`

- **Underlying series:** NSE Nifty 50 index (Yahoo Finance ticker `^NSEI`), daily OHLCV.
- **Immediate source (this file):** `https://raw.githubusercontent.com/kalilurrahman/NIFTY_50_STOCK_DATA/main/NIFTY50_stock_history.csv`
  (public GitHub repository, fetched 2026-10-05).
- **Underlying original source (per uploader):** Yahoo Finance, pulled via the
  `yfinance` Python library.
- **Coverage as fetched:** 2007-09-17 to 2026-04-13, 4,555 rows (trading days),
  columns `Date, Adj Close, Close, High, Low, Open, Volume`.
- **Known limitation:** the repository is an unofficial, third-party mirror
  with no listed maintainer verification process. It is **not** an
  NSE-official or paid-vendor feed. Treat this as "data obtained from a
  public secondary mirror of a Yahoo Finance pull," not as an audited source.

## 2. S&P 500 — `sp500_GSPC_daily.csv`

- **Underlying series:** S&P 500 index (Yahoo Finance ticker `^GSPC`), daily OHLCV.
- **Immediate source (this file):** `https://raw.githubusercontent.com/Muhammad-Ibrahim324/S-P-500-Historical-Prices-Analysis/main/data/processed/sp500_daily_clean.csv`
  (public GitHub repository, fetched 2026-10-05).
- **Underlying original source (per uploader):** Yahoo Finance, pulled via `yfinance`.
- **Coverage as fetched:** 1980-01-02 to 2026-09-25, 11,780 rows,
  columns `date, ticker, open, high, low, close, volume`.
- **Known limitation:** same third-party-mirror caveat as above.

## 3. Authenticity checks performed

Because neither source is an audited vendor feed, both series were spot-checked
against independently well-documented historical closing levels before being
treated as usable real data for this project:

| Event | Date | Value in file | Independently documented value |
|---|---|---|---|
| S&P 500 GFC closing low | 2009-03-09 | 676.53 | 676.53 (widely cited as the GFC closing bottom) |
| S&P 500 COVID closing low | 2020-03-23 | 2237.40 | 2237.40 (widely cited COVID-19 closing bottom) |
| Nifty 50 COVID closing low | 2020-03-23 | 7610.25 | 7610.25 (widely cited COVID-19 closing bottom for Nifty 50) |
| Nifty 50 GFC-era trough | 2008-10-24 | 2584.00 | Consistent with the ~2,500–2,600 range documented for Nifty 50's Oct–Nov 2008 crisis lows |

All four checks matched to the exact rupee/dollar figure (or, for the Nifty
GFC trough, the documented range), which is strong evidence these are genuine
historical index levels rather than corrupted or synthetic series. This is a
**plausibility check, not a full audit** — it does not rule out isolated
errors elsewhere in the series (gaps, stale-quote days, corporate-action
artifacts). The processed-data pipeline (`src/data_loader.py`) runs additional
automated sanity checks (monotonic dates, no negative prices, return-magnitude
outlier flags) and logs anything suspicious.

## 4. Recommendation for anyone extending this project

For publication-grade work, replace these files with data pulled directly by
you from a primary source, e.g.:

- `yfinance` (`^NSEI`, `^GSPC`) run locally — `pip install yfinance`, then
  `yfinance.download("^NSEI", start=..., end=...)`.
- NSE India's own historical data portal (nseindia.com → Reports → Historical
  Data) for Nifty 50.
- A paid vendor (Bloomberg, Refinitiv, CMIE Prowess) if institutional access
  is available.

This sandboxed research environment has no outbound network access to
Yahoo Finance, NSE, stooq, or FRED directly (all return `403`/egress-blocked
from this container), which is why a GitHub-mirrored copy was used instead of
a direct pull. `raw.githubusercontent.com` happened to be reachable; this is
an artifact of this container's network allowlist, not a general recommendation
to prefer unofficial mirrors over primary sources.
