# Financial Market Tail-Risk Research Portfolio

A research portfolio on **extreme risk in financial markets**, built around
extreme value theory (EVT), extreme dependence, options/derivatives, systemic
risk, and corporate finance — with a geographic anchor in Indian equity
markets and their dependence on global markets.

This is a research portfolio, not a collection of generic data-science demos.
Every project follows the same discipline: research question → literature
review → data methodology → mathematical methodology → implementation →
empirical analysis → robustness checks → paper → critique. See
`00_master_research/RESEARCH_PRINCIPLES.md` for the non-negotiable rules this
portfolio is built under (most importantly: **no fabricated data, no
fabricated results**).

## Central theme

Financial risk lives disproportionately in the tails. Ordinary correlation,
ordinary volatility models, and ordinary risk measures are calibrated to
"typical" market behavior and can understate what happens during crises —
precisely when accurate risk measurement matters most. This portfolio applies
EVT and related tools across equity markets, derivatives, systemic risk, and
corporate finance to study that gap empirically. See
`00_master_research/PORTFOLIO_OVERVIEW.md` for the full argument connecting
all 14 projects.

## Status of this portfolio (read this first)

This portfolio is being built incrementally, in the order recommended by
`00_master_research/RESEARCH_ROADMAP.md`, not all at once. Building every
project superficially in parallel would produce exactly the kind of shallow,
unreliable work this portfolio is explicitly designed to avoid. Current state:

| Project | Status |
|---|---|
| 01 — India–US extreme correlation | **Complete — literature review, real-data analysis, paper, blog article, and critique all done** |
| 02–14 | Directory architecture scaffolded; literature review, data, and analysis not yet done |

See `MASTER_RESEARCH_INDEX.md` for the live per-project tracker.

## A note on data

This repository was built inside a sandboxed cloud environment with no
outbound network access to financial data vendors (Yahoo Finance, NSE, FRED,
Stooq, Bloomberg — all blocked at the network level). Where real historical
index data could be sourced and independently validated against documented
historical facts (see each project's `data/raw/PROVENANCE.md`), real data was
used and real empirical results were computed from it — nothing in a
project's `results/` or `paper/` folder is invented. Where real data could
not be obtained in this environment (e.g. options chains, India VIX,
corporate fundamentals), the project's pipeline is built to run correctly
against a documented data schema, tested with clearly-labeled synthetic data,
and the paper says so explicitly rather than presenting placeholder numbers
as findings.

## Repository layout

```
financial-market-tail-risk-research/
├── 00_master_research/        Portfolio-level docs (roadmap, lit review, principles)
├── 01_india_us_extreme_correlation/
├── 02_bank_nifty_evt/
├── 03_indian_sector_extreme_dependence/
├── 04_india_us_europe_dependence/
├── 05_india_vix_tail_risk/
├── 06_nifty_option_tail_risk/
├── 07_volatility_surface/
├── 08_evt_option_margin/
├── 09_indian_bank_systemic_risk/
├── 10_safe_haven_extreme_dependence/
├── 11_corporate_leverage_tail_risk/
├── 12_merton_evt/
├── 13_garch_evt/
├── 14_asymptotic_dependence/
└── MASTER_RESEARCH_INDEX.md
```

Each project folder follows the same internal structure:

```
<project>/
├── data/{raw,processed,templates}
├── src/            reusable Python modules (not notebook-only code)
├── notebooks/       thin notebooks that call src/
├── tests/          pytest unit tests
├── figures/        generated plots (PNG, high-res)
├── tables/         generated tables (CSV)
├── results/        pipeline outputs (JSON/CSV)
├── paper/          research_paper.md, blog_article.md, references
├── docs/           REPRODUCIBILITY.md, PROFESSOR_REVIEW.md
├── README.md
├── methodology.md
├── data_dictionary.md
├── literature_review.md
├── research_notes.md
└── requirements.txt
```

## Master documents

- `00_master_research/RESEARCH_PRINCIPLES.md` — the ground rules (no
  fabrication, bias checklist, overclaiming language to avoid).
- `00_master_research/RESEARCH_ROADMAP.md` — project ranking and tiering
  (Tier 1 / 2 / 3) with the criteria used.
- `00_master_research/MASTER_LITERATURE_REVIEW.md` — cross-project
  foundational literature.
- `00_master_research/PORTFOLIO_OVERVIEW.md` — the connecting narrative across
  all 14 projects.
- `00_master_research/DATA_ACQUISITION_GUIDE.md` — exactly how a human should
  pull the real data each project needs, since this environment largely
  cannot.
- `MASTER_RESEARCH_INDEX.md` — the live project tracker table.

## Reproducing a project

Each project is self-contained: `cd <project>/ && pip install -r
requirements.txt`, then follow that project's `docs/REPRODUCIBILITY.md`.
Random seeds are fixed in each project's `src/config.py`.

## License / use

This is an academic research portfolio intended to demonstrate research
methodology. It is not investment advice, and the EVT-based risk estimates in
projects like `08_evt_option_margin` are explicitly academic models, not
exchange margin methodology.
