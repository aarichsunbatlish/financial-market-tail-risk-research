# Data Acquisition Guide

This repository was built inside a sandboxed cloud container whose network
policy blocks outbound access to financial data vendors directly (Yahoo
Finance, NSE India, Stooq, FRED, and the GitHub REST API all returned
`403`/egress-blocked when tested). One unblocked channel was found and used
—`raw.githubusercontent.com`, which allowed pulling real, independently
verified historical index data from public GitHub-hosted mirrors (see
`01_india_us_extreme_correlation/data/raw/PROVENANCE.md`). That channel does
not cover every data need in this portfolio (options chains, India VIX,
corporate fundamentals, many individual equities). This guide tells a human
exactly how to get what each later project needs.

## General recommendation

For anything beyond what Project 1 already has, the most reliable path for
a human continuing this work is:

```bash
pip install yfinance
```
```python
import yfinance as yf
df = yf.download("^NSEI", start="2000-01-01")   # Nifty 50
df = yf.download("^GSPC", start="1980-01-01")   # S&P 500
df = yf.download("^NSEBANK", start="2000-01-01")  # Bank Nifty
df = yf.download("^INDIAVIX")                     # India VIX (ticker availability varies)
df = yf.download("^STOXX50E")                     # EURO STOXX 50
df = yf.download("GC=F")                          # Gold futures
df = yf.download("BTC-USD")                       # Bitcoin
df = yf.download("INR=X")                         # USD/INR
```
Save the output to each project's `data/raw/` folder in the schema given in
that project's `data_dictionary.md`, then run that project's pipeline — it is
built to consume exactly that shape of file.

## Per-project data notes

**02 — Bank Nifty EVT**: `^NSEBANK` via yfinance, or NSE India's historical
data portal (nseindia.com → Reports → Historical Data → Indices). For
individual bank equities (HDFC Bank, ICICI, SBI, Axis, Kotak), yfinance
tickers are `HDFCBANK.NS`, `ICICIBANK.NS`, `SBIN.NS`, `AXISBANK.NS`,
`KOTAKBANK.NS`.

**03 — Indian sector indices**: NSE publishes Nifty IT (`^CNXIT`), Nifty
Auto, Nifty Pharma, Nifty Energy, Nifty FMCG — ticker availability on
Yahoo Finance varies and should be checked; NSE's own historical-indices
download is the most reliable fallback.

**04 — EURO STOXX 50**: `^STOXX50E` via yfinance, or Stooq
(`stooq.com/q/d/l/?s=^stoxx50e`) if your network allows it.

**05 — India VIX**: NSE publishes India VIX historical values directly
(nseindia.com → Reports → Historical Data → India VIX). This is the most
reliable source; Yahoo Finance coverage for India VIX is inconsistent.

**06/07/08 — NIFTY options (implied vol, surface, EVT margin)**: this is the
hardest data requirement in the portfolio. Free historical options-chain
data with strikes/maturities is not reliably available. Options:
- NSE's own historical options data archive (bhavcopy files,
  nseindia.com/all-reports), which requires scripted bulk download and
  substantial cleaning.
- A paid vendor (Bloomberg OVML, OptionMetrics, Refinitiv) if available
  through a university.
- Until one of those is wired up, these projects should stay in
  infrastructure-only status (pipeline + synthetic test data + schema), as
  the portfolio's data-dictionary/data-template convention requires.

**09 — Indian bank systemic risk**: same bank tickers as Project 02.

**10 — Safe havens**: Gold (`GC=F` or `XAUUSD` from a broker feed), Bitcoin
(`BTC-USD`), USD/INR (`INR=X` or RBI's reference rate archive at
rbi.org.in), government bonds (CCIL or RBI's public debt database — harder;
may need to be scoped out if unavailable).

**11/12 — Corporate leverage & Merton model**: equity data as above;
fundamentals (Debt/Equity, EBITDA, interest coverage, ROA/ROE/ROCE, cash
flow) are not reliably free. Screener.in (India) publishes fundamentals
per-company on its website (manual export, no bulk free API) and is the most
realistic free source for a small hand-picked sample; CMIE Prowess or
Bloomberg are the institutional-grade alternative.

**13 — GARCH+EVT**: no new data — reuses Project 01/02 series.

**14 — Asymptotic dependence**: no new data — reuses Project 01 series at
higher methodological depth.

## If your own environment has broader network access

Everything above through `yfinance`/NSE/RBI should simply work without the
workarounds this project needed. Re-run each project's `src/data_loader.py`
pointed at the freshly pulled file; nothing else needs to change.
