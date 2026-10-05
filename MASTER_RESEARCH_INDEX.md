# Master Research Index

Live tracker for all 14 projects. "Status" reflects what has actually been
done in this repository, not what is planned — see
`00_master_research/RESEARCH_ROADMAP.md` for the build order and rationale.

| # | Project | Research question | Methodology | Data | Status | Main result | Potential contribution | Future extension |
|---|---|---|---|---|---|---|---|---|
| 01 | India–US extreme correlation | Does bear-market extreme-correlation asymmetry (Longin & Solnik, 2001) persist between Nifty 50 and S&P 500? | Exceedance correlation, GPD/EVT, bootstrap CIs, normal-model benchmark | **Real, verified** Nifty 50 & S&P 500 daily data, 2007–2026 | **Built & run** | Classic bear-market asymmetry **not found**; if anything, upside exceedance correlation (~0.47–0.62) exceeds downside (~0.03–0.22) and the normal benchmark, though tail samples are small (18–63 obs). Normal models understate 99.9% VaR by ~45% vs. empirical/GPD. See `01_india_us_extreme_correlation/paper/research_paper.md` §8 | Extension of Longin–Solnik methodology to India–US pair | GARCH-filtered re-test (→ Project 13); Ang–Chen cross-check; add Europe (→ Project 4) |
| 02 | Bank Nifty EVT | Tail risk of the Indian banking sector via POT/GPD | Peaks-over-threshold, GPD, VaR/ES, return-period analysis | Needs Bank Nifty series (not yet sourced) | Scaffolded only | — | Extension of Karmakar (2013)-style EVT to Bank Nifty specifically | Compare individual bank equities |
| 03 | Indian sector extreme dependence | Does diversification across Indian sectors break down in extreme downturns? | Project 1's exceedance-correlation toolkit, multi-asset | Needs sector indices (not yet sourced) | Scaffolded only | — | Domestic application of Project 1 methodology | Network/graph representation of sector dependence |
| 04 | India–US–Europe dependence | Three-market extreme dependence / contagion | Exceedance correlation; multivariate EVT only if estimation is actually sound | Needs EURO STOXX 50 | Scaffolded only | — | Extends Project 1 to a third market | Formal tail-dependence-coefficient estimation |
| 05 | India VIX & extreme equity risk | Does India VIX predict extreme Nifty losses? | Distributional analysis of VIX, lagged regressions on VaR/ES | Needs India VIX series (hard to source here) | Scaffolded only | — | Volatility-risk linkage, Indian context | Predictive backtesting |
| 06 | NIFTY option-implied tail risk | What do NIFTY options imply about extreme downside probability? | IV smile/skew, risk-neutral density (Breeden–Litzenberger), physical vs. risk-neutral comparison | Needs historical options chain (not freely available in this env.) | Scaffolded only | — | Physical-vs-risk-neutral tail comparison for India | — |
| 07 | NIFTY vol surface & crash risk | Does the surface predict future tail risk? | Strike×maturity IV surface, skew/term-structure dynamics | Same options-data constraint as 06 | Scaffolded only | — | — | — |
| 08 | EVT-based option margin | Would EVT-based risk estimates differ materially from conventional margining? | EVT loss simulation on short option positions | Depends on 06/07 | Scaffolded only | — | Academic comparison only — not a margin-rule proposal | — |
| 09 | Indian bank systemic risk | Does extreme dependence among major banks rise disproportionately in downturns? | Pairwise/multivariate tail dependence, network view | Needs bank equity series | Scaffolded only | — | Extreme dependence as a systemic-risk proxy (not causal) | — |
| 10 | Safe-haven extreme dependence | Do gold/Bitcoin/USD-INR diversify Nifty specifically in left-tail events? | Ordinary vs. extreme correlation | Needs gold/BTC/INR series | Scaffolded only | — | — | — |
| 11 | Corporate leverage & tail risk | Does leverage predict heavier downside equity tails? | Panel regression of VaR/ES/tail index on leverage & fundamentals | Needs fundamentals (not freely available) | Scaffolded only | — | — | — |
| 12 | Merton structural default + EVT | Do higher-default-risk firms show different equity tail behavior? | Merton model (distance-to-default) + EVT on equity returns | Needs fundamentals + equity | Scaffolded only | — | Connects corporate finance, options theory, and EVT | — |
| 13 | GARCH + EVT | Does volatility filtering before EVT improve tail-risk estimation? | Normal / Student-t / GARCH / GARCH+EVT comparison, VaR/ES backtesting | Reuses Project 01/02 data | Scaffolded only | — | Extension of Karmakar (2013)/McNeil–Frey (2000) to India–US context | — |
| 14 | Asymptotic dependence vs. independence | Do India/US remain tail-dependent at arbitrarily extreme levels? | Tail-dependence-coefficient estimation, logistic-model limitations | Reuses Project 01 data | Scaffolded only | — | Advanced methodological follow-up to Project 1; connects to Ergen (2014) emerging-market evidence | — |

## Legend

- **Scaffolded only** = directory structure + stub docs exist; literature
  review, data, methodology, code, and analysis have not yet been done.
- **Built & run** = literature review, methodology, code, tests, real-data
  analysis, robustness checks, and paper are complete for the current scope.
