# Master Literature Review (Cross-Project Foundations)

This file covers the foundational papers that motivate *multiple* projects
in this portfolio. Each project's own `literature_review.md` adds
project-specific papers and a full literature matrix; this file is the
shared backbone so that isn't repeated 14 times.

**Important caveat on sourcing:** the citations below are drawn from the
assistant's trained knowledge of well-established, widely taught papers in
the international finance / extreme value literature, cross-checked where
possible with live web search in this session. They are not a substitute
for a proper database search (Google Scholar, SSRN, JSTOR, EconLit) before
any of these projects is treated as submission-ready — in particular,
**India-specific prior work has deliberately not been asserted here**
without being able to verify it live; each project's literature_review.md
flags this explicitly rather than inventing Indian citations.

## Extreme / exceedance correlation

- **Longin, F. & Solnik, B. (2001), "Extreme Correlation of International
  Equity Markets," *Journal of Finance* 56(2).** The direct methodological
  source for Project 1. Introduces exceedance correlation conditioned on
  returns beyond a threshold and an EVT-based test against the
  bivariate-normal benchmark; finds that correlation between major equity
  markets increases in bear markets (joint downside) relative to what
  normality would imply, but not symmetrically in bull markets. This
  asymmetry is the central empirical fact Project 1 tries to replicate for
  India–US.
- **Ang, A. & Chen, J. (2002), "Asymmetric Correlations of Equity
  Portfolios," *Journal of Financial Economics* 63(3).** Documents the same
  downside-correlation asymmetry using a different conditional-correlation
  estimator and a different test (a quantile-based statistic), and connects
  it to regime-switching / downside-risk pricing implications. Used as a
  methodological cross-check against the Longin–Solnik exceedance-
  correlation estimator in Project 1's robustness section.
- **Poon, S.-H., Rockinger, M. & Tawn, J. (2004), "Extreme Value Dependence
  in Financial Markets: Diagnostics, Models, and Financial Implications,"
  *Review of Financial Studies* 17(2).** Brings formal multivariate EVT
  (tail dependence coefficients, diagnostics for asymptotic dependence vs.
  independence) to the same question Longin–Solnik raise descriptively. The
  main source for Project 14's distinction between asymptotic dependence and
  independence, and a caution against assuming one-parameter dependence
  models (e.g. logistic) fit well without checking.
- **Bae, K.-H., Karolyi, G.A. & Stulz, R.M. (2003), "A New Approach to
  Measuring Financial Contagion," *Review of Financial Studies* 16(3).**
  Proposes a multinomial-logit "coexceedance" approach as an alternative to
  correlation-based contagion measures; relevant to Projects 1, 4, and 9 as
  a robustness alternative to exceedance correlation specifically.
- **Hartmann, P., Straetmans, S. & de Vries, C.G. (2004), "Asset Market
  Linkages in Crisis Periods," *Review of Economics and Statistics* 86(1).**
  Applies EVT-based tail-dependence estimators across equity and FX markets
  jointly; relevant background for Project 4 (India–US–Europe) and Project
  10 (safe havens, since it also treats FX).

## Peaks-over-threshold / GPD and risk measurement

- **Embrechts, P., Klüppelberg, C. & Mikosch, T. (1997), *Modelling
  Extremal Events for Insurance and Finance*, Springer.** The standard
  reference text for POT/GPD theory, threshold selection, and the
  Pickands–Balkema–de Haan theorem underlying GPD tail fitting; backbone
  reference for Projects 2, 6, 8, 13, 14.
- **McNeil, A.J. & Frey, R. (2000), "Estimating Tail-Related Risk Measures
  for Heteroscedastic Financial Time Series: An Extreme Value Approach,"
  *Journal of Empirical Finance* 7(3–4).** The direct methodological source
  for "GARCH-filter then EVT on standardized residuals" (Project 13), and
  for EVT-based VaR/Expected Shortfall estimation generally (Project 2, 8).
- **DuMouchel, W.H. (1983), "Estimating the Stable Index α in Order to
  Measure Tail Thickness: A Critique," *Journal of the American Statistical
  Association* 78(383).** Early reference for the long-standing
  "how much of the tail to use" threshold-selection problem, relevant to the
  threshold-stability robustness checks required across every POT project.

## Options / risk-neutral density

- **Breeden, D.T. & Litzenberger, R.H. (1978), "Prices of State-Contingent
  Claims Implicit in Option Prices," *Journal of Business* 51(5).** The
  foundational result letting a risk-neutral density be recovered from the
  second derivative of the call-price function with respect to strike;
  methodological basis for Projects 6 and 7's risk-neutral density work.
- **Jackwerth, J.C. (2000), "Recovering Risk Aversion from Option Prices and
  Realized Returns," *Review of Financial Studies* 13(2).** Standard
  reference for comparing risk-neutral and physical distributions and the
  pitfalls (numerical instability of the Breeden–Litzenberger second
  derivative, need for smoothing) relevant to Project 6.

## Corporate finance / structural default

- **Merton, R.C. (1974), "On the Pricing of Corporate Debt: The Risk
  Structure of Interest Rates," *Journal of Finance* 29(2).** The structural
  default model at the center of Project 12: equity as a call option on firm
  assets, from which asset volatility, distance-to-default, and a default
  probability are backed out.
- **Crosbie, P. & Bohn, J. (2003), Moody's KMV technical document, "Modeling
  Default Risk."** Describes the practical implementation adjustments
  (iterative asset-value/volatility estimation, empirical default
  mapping) used when applying Merton's model to real firms; relevant to
  Project 12's implementation choices.

## India-specific literature (verified via live search this session)

Unlike the rest of this file, these two were confirmed through live web
search during this session (not from trained memory alone), which is why
they can be stated with more confidence than a blanket "no India-specific
literature was checked" caveat would suggest. Full text was not accessible
(publisher paywalls are blocked by this environment's network policy), so
only the searchable abstract/metadata could be verified — treat method and
result details below as abstract-level, to be confirmed against full text
before being relied on in a submission-grade paper.

- **Karmakar, M. (2013), "Estimation of Tail-Related Risk Measures in the
  Indian Stock Market: An Extreme Value Approach," *Review of Financial
  Economics* 22(3), 79–85.** Applies the McNeil & Frey (2000) two-stage
  conditional-EVT approach (GARCH filter, then EVT on standardized
  residuals) to the Indian stock market to estimate dynamic VaR and
  Expected Shortfall. This is directly on point for **Project 13
  (GARCH+EVT)** and **Project 2 (Bank Nifty EVT)** — it means Project 13 in
  particular should be framed as "we apply/extend the Karmakar (2013)
  conditional-EVT approach" rather than as untouched ground, and its full
  text should be read before Project 13 is built.
- **Ergen, I. (2014), "Tail Dependence and Diversification Benefits in
  Emerging Market Stocks: An Extreme Value Theory Approach," *Applied
  Economics* 46(19), 2215–2227.** Finds that most emerging equity markets
  studied show **asymptotic independence** (tail dependence vanishes at the
  most extreme quantiles) even though dependence at finite extreme levels is
  still much stronger than a multivariate-normal benchmark would imply, and
  that correlation-based diversification measures understate joint-crash
  risk relative to EVT-based tail-dependence measures. This is directly
  relevant to **Project 1** (normal-benchmark comparison) and **Project 14**
  (asymptotic dependence vs. independence) — whether India/the specific
  markets in Ergen (2014) overlap with India has not been confirmed from the
  abstract alone and must be checked in the full text before this paper is
  cited as being about India specifically; it is safe to cite only as
  "emerging-market evidence" until then.

These two results change how Projects 1, 2, 13, and 14 should be framed:
closer to "replication/extension of a documented approach" than "no prior
India-specific work exists." The literature search above was not
exhaustive (single search session, abstract-level only) and should be
treated as a starting point, not a complete systematic review.

## How this shapes project classification

None of the India-specific empirical projects in this portfolio (1–14) can
be classified as "replication" in the strict sense of re-running a published
India-specific study, because no such study has been verified here. They are
better described, until a live literature search says otherwise, as
**extensions of internationally-established methodology to the Indian
market context** (exceedance correlation → India–US; POT/GPD → Bank Nifty;
Merton → Indian firms, etc.), with the possibility that a genuinely
India-specific prior literature exists and should be checked and cited
before any claim of being first.
