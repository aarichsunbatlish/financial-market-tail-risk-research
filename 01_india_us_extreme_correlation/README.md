# Project 1 — Extreme Correlation Between Indian and US Equity Markets

**Working title:** *Extreme Correlation Between Indian and US Equity
Markets: An EVT-Based Replication and Extension*

## Research question

Does the bear-market extreme-correlation asymmetry documented in the
international equity literature (Longin & Solnik, 2001) persist between
the Nifty 50 and the S&P 500?

## Status: built and run on real data

Real, independently validated daily data for both indices
(2007-09-17 → 2026-04-13 overlap) was sourced and used — see
`data/raw/PROVENANCE.md` for exactly where it came from and how it was
checked. All figures, tables, and results in this project were produced by
running the code in `src/` against that data; nothing here is invented.

## Read these in order

1. `literature_review.md` — what this project replicates/extends, and why.
2. `data_dictionary.md` — exact variables, transformations, and the
   non-synchronous-trading issue central to this project's design.
3. `methodology.md` — the full mathematical methodology.
4. `paper/research_paper.md` — the complete write-up with results.
5. `paper/blog_article.md` — a plain-language version.
6. `docs/PROFESSOR_REVIEW.md` — a critical self-review of this project's
   limitations, in the voice the brief requested.
7. `docs/REPRODUCIBILITY.md` — how to re-run everything, and how to extend
   it with better data.

## Quickstart

```bash
cd 01_india_us_extreme_correlation
pip install -r requirements.txt
python -m pytest tests/ -q
python src/pipeline.py --config src/config.py
```

Outputs land in `figures/`, `tables/`, and `results/`.
