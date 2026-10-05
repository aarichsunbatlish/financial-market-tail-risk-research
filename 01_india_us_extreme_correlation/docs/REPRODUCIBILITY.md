# Reproducibility — Project 1

## Re-running exactly what produced this project's results

```bash
cd 01_india_us_extreme_correlation
pip install -r requirements.txt
python -m pytest tests/ -q          # 28 tests, should all pass
python -m src.pipeline               # writes figures/, tables/, results/
```

Random seed is fixed (`src/config.py: RANDOM_SEED = 20261005`); the Monte
Carlo normal-benchmark and bootstrap results will be numerically identical
to the ones reported in `paper/research_paper.md` if re-run as-is on the
same data files.

## Upgrading to vendor-sourced data

This project currently uses the CSVs in `data/raw/`, whose provenance
(third-party GitHub mirrors of Yahoo Finance pulls) is documented in
`data/raw/PROVENANCE.md`, along with an explicit recommendation to replace
them with directly-sourced data for anything beyond a research-portfolio
demonstration. To do so:

```python
import yfinance as yf
nifty = yf.download("^NSEI", start="2000-01-01")
sp500 = yf.download("^GSPC", start="1980-01-01")
```

Save each as a CSV matching the column names `src/data_loader.py` expects
(see `data_dictionary.md`), overwrite the files in `data/raw/`, and re-run
`python -m src.pipeline` — no code changes are required.

## Extending the analysis

- To add the Ang & Chen (2002) asymmetry estimator: implement it as a new
  function in `src/exceedance.py` (or a new `src/asymmetry.py` module) and
  call it from `src/pipeline.py` alongside the existing exceedance-
  correlation table.
- To add a GARCH filter before this project's statistics (Project 13's
  question, previewed here): fit a GARCH(1,1) to each return series (the
  `arch` package), take standardized residuals, and re-run
  `exceedance_correlation_table` / `normal_benchmark_test` on the residual
  series instead of the raw returns.
- To extend the sample pre-2007: source a longer Nifty 50 series (e.g. BSE
  Sensex as a proxy, with the caveat that it is a different index) and
  update `src/config.py`'s `NIFTY_RAW_PATH` and `SUB_PERIODS`.

## What NOT to change silently

If you change the raw data files, the alignment logic, or the sub-period
boundaries, re-run the full pipeline and regenerate `paper/research_paper.md`'s
numbers from the new `results/pipeline_summary.json` and `tables/*.csv` —
do not hand-edit the paper's numbers to match a new run without
re-deriving them, per this portfolio's no-fabrication rule
(`00_master_research/RESEARCH_PRINCIPLES.md`).
