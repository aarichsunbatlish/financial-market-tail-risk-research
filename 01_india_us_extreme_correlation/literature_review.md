# Literature Review — Project 1: Extreme Correlation Between Indian and US Equity Markets

## Scope and sourcing caveat

This review combines (a) well-established papers known with high confidence
from training knowledge and (b) results confirmed via live web search during
this session (noted explicitly where used). It is **not** a systematic
database search (no Google Scholar/JSTOR/EconLit access from this
environment) and should be treated as a strong starting point, not a
complete review, before this project is treated as submission-ready.

## Literature matrix

| Paper | Author(s) | Year | Research question | Data | Method | Main result | Limitation | Relevance to this project | Potential extension |
|---|---|---|---|---|---|---|---|---|---|
| Extreme Correlation of International Equity Markets | Longin & Solnik | 2001 | Does correlation between equity markets rise in extreme/bear markets beyond what normality implies? | Monthly returns, 5 largest equity markets, 1958–1996 | Exceedance correlation conditioned on threshold; EVT-based test vs. bivariate normal | Correlation increases in bear markets (not bull); driven by market trend, not volatility; reject normality in the negative tail | Monthly frequency only; 5 developed markets, no emerging markets | **This is the direct methodology this project replicates**, applied to Nifty 50 vs. S&P 500 | Apply at daily frequency; add emerging-market pair (done here) |
| Asymmetric Correlations of Equity Portfolios | Ang & Chen | 2002 | Is downside correlation asymmetry robust to a different estimator? | US equity portfolios, daily/monthly | Conditional correlation (different estimator from Longin–Solnik) + a specific asymmetry test statistic | Confirms downside correlation asymmetry; links it to downside risk | US-only (no international pair) | Used as a **robustness cross-check estimator** against exceedance correlation in this project | Extend asymmetry test to India–US pair |
| Extreme Value Dependence in Financial Markets: Diagnostics, Models, and Financial Implications | Poon, Rockinger & Tawn | 2004 | Is dependence between markets asymptotically dependent or independent at the most extreme levels? | International equity indices | Multivariate EVT; diagnostics for asymptotic (in)dependence; caution on one-parameter (logistic) dependence models | Dependence structure, and whether it persists at the extreme limit, varies by market pair; naive one-parameter models can mislead | Requires large tail samples; diagnostics are technically demanding | Motivates **why this project must not overclaim** a full multivariate-EVT asymptotic-dependence conclusion from a two-market, ~18-year daily sample — that deeper question is deferred to Project 14 | Formal asymptotic dependence test (Project 14) |
| A New Approach to Measuring Financial Contagion | Bae, Karolyi & Stulz | 2003 | How to measure "contagion" without relying on correlation breakdown arguments | Emerging + developed equity markets | Multinomial logit on coexceedances | Coexceedance-based contagion measures differ from, and can be more robust than, correlation-based ones | Requires defining joint-exceedance bins; less intuitive economically | Alternative robustness check to exceedance correlation | Could be added as a robustness alternative |
| Asset Market Linkages in Crisis Periods | Hartmann, Straetmans & de Vries | 2004 | How linked are asset markets (equity, FX) specifically during crises? | Equity + FX, developed markets | EVT-based tail-dependence estimators | Tail linkages across asset classes rise in crises, consistent with Longin–Solnik's equity-only finding | Developed markets only | Background for extending to FX (relevant later to Project 10) | — |
| Tail Dependence and Diversification Benefits in Emerging Market Stocks: An Extreme Value Theory Approach | Ergen | 2014 | Does tail dependence survive at the most extreme quantiles in emerging markets, and does it matter for diversification? | Emerging equity markets (specific country list not confirmed from abstract alone — **verify in full text**) | Multivariate EVT tail-dependence coefficients vs. correlation | Most emerging markets show asymptotic independence, but dependence at finite extreme levels still exceeds the normal benchmark; EVT tail measures explain diversification loss better than correlation | Abstract-level only in this review; country coverage unconfirmed | **Closest India-adjacent prior evidence found**; motivates comparing this project's exceedance-correlation result against the normal benchmark explicitly, and flags that "asymptotically independent but finite-level dependent" is a real possibility this project's results should be read against | If India is confirmed in Ergen's sample, this becomes a direct comparison point |
| Modelling Extremal Events for Insurance and Finance | Embrechts, Klüppelberg & Mikosch | 1997 | (Textbook) EVT foundations | — | POT/GPD theory, Pickands–Balkema–de Haan theorem | Standard reference | — | Theoretical basis for the GPD fitting module | — |

## How each paper shaped this project's design

- **Longin & Solnik (2001)** is why this project computes exceedance
  correlation at multiple thresholds (±1σ, ±2σ, ±3σ, further if sample size
  allows), separately for the left and right tail, and benchmarks against a
  bivariate-normal simulation calibrated to the same unconditional
  correlation — this is their test, not an original design choice.
- **Ang & Chen (2002)**'s different estimator is why the pipeline includes a
  second, independent asymmetry check rather than relying on exceedance
  correlation alone.
- **Poon, Rockinger & Tawn (2004)** is why this project explicitly declines
  to claim a full asymptotic-dependence/-independence conclusion — that
  requires more data and more careful tail-dependence-coefficient estimation
  than a first project should attempt; it is deferred to Project 14.
- **Ergen (2014)** is why the results section interprets any "dependence
  stronger than normal, but weaker at the furthest thresholds" pattern as
  consistent with a known phenomenon in the emerging-market literature,
  rather than as a surprising or project-specific finding.

## Project classification

Given what could be verified in this session, **no India–US-specific
extreme-correlation study was confirmed to exist** (the closest hit,
Ergen 2014, studies emerging markets generally, with India's inclusion
unconfirmed from the abstract). This project is therefore classified as:

> **An extension of the Longin & Solnik (2001) exceedance-correlation
> methodology to the India–US equity market pair**, cross-checked against
> the Ang & Chen (2002) estimator, and interpreted in light of the
> asymptotic-(in)dependence evidence in Poon, Rockinger & Tawn (2004) and
> Ergen (2014).

It is **not** described as a "replication" (no specific prior India–US paper
is being reproduced), and **not** described as "novel" or a "first study" —
those claims would require a literature search this session cannot perform.

## Open items for a more complete review

- Confirm whether Ergen (2014)'s emerging-market sample includes India.
- Search specifically for India–US or India–developed-market
  exceedance-correlation studies in Indian finance journals (e.g. *Journal
  of Emerging Market Finance*, IIMB Management Review) not well indexed in
  general web search.
- Check for more recent (2015–2026) extensions of Longin–Solnik using
  copula-GARCH or dynamic conditional correlation (DCC) approaches, which
  this project's robustness section could be compared against.
