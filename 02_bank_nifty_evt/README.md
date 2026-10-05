# Project 02 — Extreme Returns and Tail Risk in the Indian Banking Sector: A Peak-Over-Threshold EVT Analysis

## Status: scaffolded, not yet built

This project's directory structure (`data/`, `src/`, `notebooks/`,
`tests/`, `figures/`, `tables/`, `results/`, `paper/`, `docs/`) is in
place, following the same layout as Project 1
(`../01_india_us_extreme_correlation/`), but its literature review, data,
methodology, code, and empirical analysis have not yet been done.

See `../00_master_research/RESEARCH_ROADMAP.md` for why this project is
sequenced where it is, and `../MASTER_RESEARCH_INDEX.md` for the
portfolio-wide tracker.

## Data status

Needs a Bank Nifty (^NSEBANK) daily series and/or individual bank equities. Not yet sourced in this environment. See `../00_master_research/DATA_ACQUISITION_GUIDE.md` for how a
human with normal network access should source it.

## Before starting this project

1. Read `../00_master_research/RESEARCH_PRINCIPLES.md` (binding rules:
   no fabricated data or results, overclaiming language to avoid, required
   bias checks).
2. Do a literature review first (`literature_review.md` in this folder)
   before writing any code -- see Project 1's for the expected depth and
   format (a literature matrix, not just a summary).
3. Follow Project 1's module layout in `src/` as a template: keep
   computation in small, tested, documented functions; keep orchestration
   (I/O, plotting, figure/table writing) in a single `pipeline.py`.
4. Do not write `paper/research_paper.md`'s results section until the
   pipeline has actually been run on real (or clearly-labeled synthetic
   test-only) data -- if real data is not yet available, say so explicitly
   rather than inventing numbers.
