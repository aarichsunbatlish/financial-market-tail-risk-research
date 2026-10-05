# Research Roadmap: Project Ranking and Tiering

Ranking criteria (A–J, as specified for this portfolio):
A. methodological importance · B. feasibility · C. relevance to financial
markets · D. relevance to EVT research · E. relevance to derivatives ·
F. relevance to corporate finance · G. potential research contribution ·
H. data availability (in practice, and in this sandboxed environment
specifically) · I. potential for future publication/extension ·
J. suitability for an undergraduate/early-career research assistant.

Scores below are qualitative (High/Med/Low), based on what is actually known
about each project's data requirements after testing this environment's
network access (see `DATA_ACQUISITION_GUIDE.md`) — not aspirational.

| # | Project | A | B | C | D | E | F | G | H (this env.) | I | J |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 | India–US extreme correlation | H | H | H | H | M | L | M | **H (verified real data)** | M | H |
| 02 | Bank Nifty EVT (POT/GPD) | H | H | H | H | L | L | M | M (needs 1 more series) | M | H |
| 13 | GARCH + EVT | H | M | M | H | L | L | M | H (reuses 01/02 data) | M | M |
| 03 | Indian sector extreme dependence | M | M | H | M | L | L | M | M | L | M |
| 09 | Indian bank systemic risk | M | M | H | M | L | M | M | M | M | M |
| 10 | Safe-haven extreme dependence | M | M | H | M | L | L | M | M | L | M |
| 04 | India–US–Europe dependence | M | M | M | M | L | L | L–M | M | L | M |
| 05 | India VIX & extreme equity risk | M | L | H | M | M | L | M | L (India VIX hard to source here) | M | M |
| 14 | Asymptotic dependence (advanced) | H | L | L | H | L | L | M | M (reuses 01 data, needs care) | M | L |
| 11 | Corporate leverage & tail risk | M | L | M | L | L | H | M | L (fundamentals not free) | M | L |
| 12 | Merton structural default + EVT | H | L | M | M | M | H | M | L (needs fundamentals + equity) | H | L |
| 06 | Option-implied tail risk (NIFTY) | H | L | H | H | H | L | M–H | **L (no free options data)** | H | L |
| 07 | Vol surface & crash risk | M | L | H | M | H | L | M | **L (same options constraint)** | M | L |
| 08 | EVT-based option margin | M | L | M | H | H | L | M | **L (depends on 06/07)** | M | L |

## Tiers

### Tier 1 — build first
1. **Project 1** (India–US extreme correlation) — real data verified and in
   hand; this is the foundational replication the rest of the portfolio's
   methodology (exceedance correlation, GPD, bootstrap CIs) is built on.
2. **Project 2** (Bank Nifty EVT) — single-series POT/GPD; same tooling as
   Project 1, different question (sector tail risk vs. cross-market
   dependence); data gettable the same way once a Bank Nifty series is
   sourced.
3. **Project 13** (GARCH + EVT) — directly reuses Project 1/2 data and asks
   whether filtering volatility clustering first changes the tail estimates;
   natural, cheap extension once 1 and 2 exist.
4. **Project 3** (Indian sector extreme dependence) — extends Project 1's
   exceedance-correlation machinery to a domestic multi-asset setting.

### Tier 2 — build next
5. **Project 9** (Indian bank systemic risk) — pairwise/multivariate
   extension of the same tail-dependence tools to systemically important
   banks.
6. **Project 10** (Safe-haven extreme dependence) — gold/Bitcoin/USDINR vs.
   Nifty; likely gettable via the same GitHub-mirror or yfinance route.
7. **Project 4** (India–US–Europe) — adds a third market; explicitly scoped
   to avoid overclaiming a full multivariate EVT model unless the estimation
   is actually done correctly.
8. **Project 5** (India VIX & extreme risk) — valuable but data-constrained
   in this environment; needs NSE's own India VIX archive.

### Tier 3 — advanced / harder data or methodology
9. **Project 14** (Asymptotic dependence vs. independence) — explicitly an
   advanced methodological project; the brief itself says to attempt it only
   after the simpler replications work. Placed here deliberately.
10. **Project 12** (Merton structural default + EVT) — mathematically the
    most demanding corporate-finance project; high potential contribution,
    but needs both balance-sheet and equity data together.
11. **Project 11** (Corporate leverage & tail risk) — panel-data project;
    blocked mainly by free fundamentals access, not methodology.
12. **Project 6/7/8** (options, vol surface, EVT margin) — highest
    derivatives relevance and arguably the most distinctive contribution in
    the portfolio, but also the hardest data problem: free historical NIFTY
    options-chain data with strikes/maturities was not found to be
    available in this environment. These should remain **infrastructure +
    documented data requirement** until real options data is supplied,
    rather than being faked with synthetic "results."

## Why Project 1 first (and only Project 1 so far)

The brief's own execution rule is explicit: build one project properly,
test it, review it, improve it, *then* proceed sequentially — not build
shallow versions of all 14 at once. Project 1 was chosen because (a) it is
the direct empirical replication target most explicitly named in the brief,
(b) its methodology (exceedance correlation + GPD + bootstrap) is reused by
Projects 2, 3, 9, 13, 14, so getting it right first has the highest
portfolio-wide leverage, and (c) real, independently validated data for it
was actually obtainable in this environment — unlike several other projects.
