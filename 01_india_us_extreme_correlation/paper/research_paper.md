# Extreme Correlation Between Indian and US Equity Markets: An EVT-Based Replication and Extension

## Abstract

We examine whether the bear-market extreme-correlation asymmetry documented
for developed equity markets by Longin & Solnik (2001) — correlation rising
in joint downturns more than a bivariate-normal benchmark implies, with no
corresponding rise in joint upturns — is present between the Nifty 50 and
the S&P 500. Using daily data from 2007-09-18 to 2026-04-13/09-25 (indices'
respective native ranges, ~4,553 overlapping India trading days under our
primary alignment), we compute exceedance correlation at multiple
thresholds, benchmark it by Monte Carlo simulation against a bivariate
normal matched to the sample's unconditional correlation, fit a
Generalized Pareto Distribution to each market's own tail, and estimate
empirical tail-dependence coefficients. We find, contrary to the classic
asymmetry result, that **upside (right-tail) exceedance correlation is
larger than downside (left-tail) exceedance correlation** at every
threshold we can estimate with a reportable sample size, and that only the
right tail's excess over the normal benchmark is statistically distinguishable
from chance at conventional levels after accounting for multiple testing.
Results are highly sensitive to how the two markets' trading-hour mismatch
is handled: the naive same-calendar-day alignment, a US-lagged-by-one-day
alignment, and a weekly alignment give materially different point
estimates. Crisis-subperiod (GFC, COVID) exceedance correlation cannot be
estimated reliably in most cells because the tail sample sizes are too
small — a limitation we report rather than paper over. We interpret these
results as **not** replicating the bear-market correlation asymmetry for
this specific market pair and sample, while finding that both markets'
individual tails are, as expected, much heavier than a normal model
implies (GPD tail index $\hat\xi \approx 0.23$ for Nifty 50, $\approx 0.28$
for S&P 500).

## 1. Introduction

Standard portfolio theory treats diversification benefits as roughly
constant across market conditions. A substantial empirical literature,
beginning with Longin & Solnik (2001) and Ang & Chen (2002), has
challenged this by showing that major developed equity markets become
more correlated specifically during joint downturns, beyond what their
unconditional correlation and a normal-distribution assumption would
predict — i.e., diversification can fail exactly when it is most needed.
This project asks whether the same pattern holds for a pair not studied in
the original literature: India's Nifty 50 and the US S&P 500.

## 2. Research question

Does the bear-market extreme-correlation asymmetry documented in the
international-equity literature persist between the Nifty 50 and the S&P
500, once the data are available to test it directly?

## 3. Motivation

India is a large, increasingly globally integrated emerging equity market
with a market structure, trading calendar, and investor base that differ
substantially from the developed markets in the original Longin–Solnik
sample (five large developed markets, 1958–1996 monthly data). Whether the
developed-market asymmetry extends to an emerging/developed pair, and at
daily frequency, is an open empirical question with direct relevance to
anyone holding both Indian and US equity exposure.

## 4. Literature review

See `literature_review.md` for the full literature matrix. In brief: this
project's methodology is a direct application of Longin & Solnik (2001)'s
exceedance-correlation test, cross-checked against Ang & Chen (2002)'s
independent asymmetry estimator, interpreted with reference to the
asymptotic-dependence diagnostics in Poon, Rockinger & Tawn (2004) and the
emerging-market evidence in Ergen (2014) that most emerging markets show
asymptotic independence even while finite-level tail dependence exceeds
the normal benchmark. No India–US-specific prior study was confirmed to
exist in this session's (non-exhaustive) literature search; this project
is classified as an **extension of established methodology to a new
market pair**, not a replication of a specific prior India-focused paper.

## 5. Data

Real daily closing levels for the Nifty 50 (2007-09-18 to 2026-04-13,
n=4,553 returns) and the S&P 500 (1980-01-03 to 2026-09-25, n=11,778
returns), sourced from third-party GitHub mirrors of Yahoo Finance pulls
and independently validated against documented historical closing lows
(GFC, COVID) before use — full provenance and validation detail in
`data/raw/PROVENANCE.md`. Both series' known extreme days were correctly
flagged by the pipeline's automated sanity check (e.g. the S&P 500's
1987-10-19 Black Monday return), which is itself a further authenticity
check on the data. See `data_dictionary.md` for every derived variable and
`methodology.md` for the full mathematical methodology; both are
summarized, not repeated, below.

## 6. Methodology (summary)

Exceedance correlation at $\theta \in \{1,1.5,2,2.5,3\}$ standard
deviations, in both tails, on three alignments of the daily return series
(same-calendar-day; Nifty day *t* vs. the most recently completed US
session, i.e. US lag-1; and weekly). A Monte Carlo bivariate-normal
benchmark (5,000-equivalent per-replication draws matched to the sample's
unconditional correlation and marginal volatilities, 1,000 replications)
provides the normal-model comparison. GPD tail fits (MLE, threshold at
each market's own 95th-percentile loss, selected via mean-excess and
threshold-stability diagnostics) give VaR/ES estimates compared against
empirical, normal, and Student-$t$ benchmarks. Empirical $\chi(q)$/$\bar\chi(q)$
tail-dependence coefficients are reported descriptively. Moving block
bootstrap (block length 17, from $n^{1/3}$) gives confidence intervals
accounting for serial dependence. Full detail: `methodology.md`.

## 7. Empirical strategy

The primary specification uses the **US lag-1 alignment** (Nifty return on
day *t* vs. the most recently completed S&P 500 session, strictly before
*t*), because the naive same-calendar-day alignment implicitly uses
US-market information that did not exist yet when Nifty traded that day
(see `data_dictionary.md`). The same-day and weekly alignments are
reported as robustness checks, not as alternative "main" results — and, as
Section 9 shows, the choice materially changes the answer, which is itself
a finding.

## 8. Results

All numbers below are read directly from `results/pipeline_summary.json`
and the CSVs in `tables/`, produced by `src/pipeline.py` run against the
real data described above — nothing here is hand-entered or invented.

### 8.1 Descriptive statistics (full sample, daily log returns)

| | Nifty 50 | S&P 500 |
|---|---|---|
| n | 4,553 | 11,778 |
| Mean | 0.000366 | 0.000365 |
| Std. dev. | 0.01304 | 0.01126 |
| Skewness | -0.281 | -1.045 |
| Excess kurtosis | 14.995 | 24.239 |
| Jarque–Bera stat (p-value) | 42,716 (<0.001) | 290,478 (<0.001) |

Both series overwhelmingly reject normality (fat tails and negative
skew, S&P 500 more strongly than Nifty 50 over its longer sample, which
includes 1987 and 2008–09).

### 8.2 Unconditional and sign-conditional correlation (US lag-1 alignment)

Unconditional correlation: **0.254** (moving block bootstrap 95% CI:
**[0.211, 0.297]**, 1,000 replications, block length 17). Conditional on
Nifty's own return being negative: 0.213; conditional on positive: 0.124.
This simple sign-based cut already hints at *some* asymmetry (more
co-movement when India is down), but it is not yet the Longin–Solnik test.

### 8.3 Exceedance correlation vs. the normal benchmark — the core result

| Tail | θ (σ) | n (joint exceed.) | Observed ρ | Normal-benchmark median | MC p-value (one-sided) | Bonferroni p-value |
|---|---|---|---|---|---|---|
| Left (bear) | 1.0 | 143 | **0.218** | 0.065 | 0.023 | 0.092 |
| Left (bear) | 1.5 | 63 | **0.031** | 0.045 | 0.536 | 1.000 |
| Left (bear) | 2.0 | 29 | 0.093 | — (insufficient sim.) | — | — |
| Right (bull) | 1.0 | 108 | **0.466** | 0.069 | **0.000** | **0.000** |
| Right (bull) | 1.5 | 31 | **0.620** | 0.039 | **0.000** | **0.000** |
| Right (bull) | 2.0 | 18 | 0.612 | — (insufficient sim.) | — | — |

(θ=2.5, 3.0 omitted from this table: fewer than 15 joint exceedances,
below our pre-specified minimum reportable sample size — see
`tables/exceedance_correlation_full_sample.csv` for the unfiltered values,
which we do not interpret.)

**This is the opposite pattern from the classic Longin–Solnik finding.**
In this sample, it is the *upside* exceedance correlation that is both
large in absolute terms and far above the normal-model benchmark at the
1σ and 1.5σ thresholds (Monte Carlo p-value indistinguishable from zero,
robust to a Bonferroni correction across all ten threshold×tail tests).
The *downside* exceedance correlation is, at best, marginally distinguishable
from the normal benchmark at the 1σ threshold (p=0.023 raw, p=0.092 after
Bonferroni correction — not significant at 5% once multiple testing is
accounted for) and is **not** monotonic across thresholds (0.218 → 0.031 →
0.093 as θ rises from 1.0 to 1.5 to 2.0), which is itself evidence that
these left-tail point estimates are dominated by small-sample noise rather
than a stable underlying relationship. See
`figures/exceedance_correlation_vs_normal_benchmark.png`.

### 8.4 Why the left tail is unreliable here: bootstrap confidence intervals

The moving block bootstrap 95% CI for the 2σ left-tail exceedance
correlation is **[-0.272, 0.357]** around a point estimate of 0.093 — wide
enough to include zero and substantially negative values. We do not treat
this statistic as informative. This is exactly the "tail sample too small"
problem the methodology document flags in advance (Section 10), not a
post-hoc excuse.

### 8.5 Sub-period results: mostly not estimable

Splitting the US-lag-1 sample into pre-GFC (71 obs), GFC (362 obs),
interim (2,590 obs), COVID (227 obs), and post-2020 (1,303 obs) windows and
re-running the exceedance-correlation table shows that **GFC and COVID
windows do not have enough joint exceedances to report a single reliable
exceedance-correlation cell** at any threshold ≥1.0σ (all flagged
`sufficient=False` in `tables/exceedance_correlation_by_subperiod.csv`).
Only the long "interim" (2009-07 to 2020-01) and "post_2020" windows have
enough observations to report 1.0σ and 1.5σ cells, and both show the same
qualitative pattern as the full sample (left-tail ρ around 0.04–0.23,
broadly smaller than or comparable to right-tail ρ, though the interim
right-tail 1.5σ estimate of -0.012 is itself a small-sample artifact given
only 25 exceedances). **We explicitly do not claim a crisis-specific
finding** — the data cannot support one at this frequency with only ~0.5–1
year crisis windows.

### 8.6 Individual-market tail risk (GPD)

| | Threshold (loss) | $\hat\xi$ (shape) | $\hat\beta$ (scale) | n exceedances |
|---|---|---|---|---|
| Nifty 50 | 1.87% daily loss | 0.232 | 0.00953 | 228 |
| S&P 500 | 1.67% daily loss | 0.277 | 0.00718 | 589 |

Both shape estimates are comfortably positive (heavy-tailed, Fréchet-type
domain), consistent with the descriptive kurtosis. The S&P 500's slightly
higher $\hat\xi$ over its much longer sample (which includes 1987 and
2008–09) should not be read as "the US market has a heavier tail than
India" in general — the two fits use different, non-overlapping-in-length
samples (see Section 10, robustness).

VaR/Expected-Shortfall comparison (99.9% level, daily, Nifty 50):

| Model | VaR | ES |
|---|---|---|
| Empirical | 7.35% | 10.52% |
| Normal | 3.99% | 4.36% |
| Student-t | 8.50% | — |
| GPD | 7.95% | 11.03% |

The normal model understates the 99.9% VaR by roughly **45%** relative to
the empirical quantile; the GPD estimate (7.95%) is much closer to the
empirical value (7.35%) than the normal model is, and closer than the
Student-$t$ fit (8.50%, which overshoots). This is the clearest, least
ambiguous result in this project: **a normal-distribution risk model would
have materially understated extreme single-day loss risk in both
markets**, exactly the motivation for EVT-based approaches. The full
comparison table (both markets, p=0.99/0.995/0.999) is in
`tables/var_es_comparison_{nifty,sp500}.csv`.

### 8.7 Tail dependence diagnostics ($\chi$, $\bar\chi$)

| q | $\hat\chi(q)$ | $\hat{\bar\chi}(q)$ | n joint exceedances |
|---|---|---|---|
| 0.90 | 0.299 | 0.312 | 136 |
| 0.95 | 0.259 | 0.380 | 59 |
| 0.975 | 0.246 | 0.452 | 28 |
| 0.99 | 0.110 | 0.355 | 5 |

$\hat\chi(q)$ declining toward the most extreme quantile (and $\hat{\bar\chi}(q)$
staying below 1 throughout, though noisily at q=0.99 with only 5 joint
exceedances) is directionally consistent with the **asymptotic
independence** pattern Ergen (2014) reports for emerging markets generally
— dependence well above zero at moderately extreme levels, weakening
toward the most extreme observable quantile. We stop short of a formal
asymptotic-dependence/-independence conclusion (that is Project 14's
job); at q=0.99 the estimate rests on 5 data points and should not be
over-interpreted.

### 8.8 Signed single-conditioning (robustness)

Conditioning on only one market's exceedance (rather than requiring both)
gives much smaller correlations (roughly 0.03–0.16 across thresholds and
tails — `tables/signed_single_conditioning.csv`) than the joint-exceedance
figures in 8.3, especially at the 1.5–2σ thresholds where joint
exceedance correlation reached 0.6+. This gap is itself informative: the
very high *joint*-exceedance correlations in Section 8.3 are estimated
from small, mutually-selected samples (requiring *both* series to exceed
the threshold *simultaneously*), which is a more demanding — and noisier —
conditioning event than conditioning on one series alone. We read this as
reinforcing Section 8.4's point: the headline right-tail numbers in 8.3,
while statistically distinguishable from the normal benchmark, are
estimated from tens of observations and should be treated as suggestive,
not definitive.

### 8.9 Alignment robustness

| Alignment | n | Unconditional ρ | Left ρ, 1.5σ (n) | Left ρ, 2.0σ (n) |
|---|---|---|---|---|
| Same calendar day | 4,428 | 0.291 | 0.263 (51) | 0.042 (28) |
| US lag-1 (primary) | 4,553 | 0.254 | 0.031 (63) | 0.093 (29) |
| Weekly | 969 | 0.538 | 0.642 (24) | n/a (10, insufficient) |

The unconditional correlation roughly doubles from daily (≈0.25–0.29) to
weekly (0.54) aggregation — an expected effect of temporal aggregation
smoothing out the non-synchronous-trading noise — but the *exceedance*
correlation estimates differ so much across alignments (e.g. left-tail
1.5σ: 0.263 same-day vs. 0.031 lag-1) that **the choice of alignment is not
a minor technical detail: it changes the empirical answer**. We consider
the lag-1 alignment the economically correct one (Section 7) and treat the
same-day result as the methodologically naive one the literature on
non-synchronous trading warns against.

## 9. Robustness checks

Performed: (1) three alignments (8.9); (2) Bonferroni-adjusted multiple
testing correction (8.3); (3) comparison against normal, Student-$t$, and
empirical benchmarks (8.6); (4) descriptive tail-dependence diagnostics as
a cross-check on the exceedance-correlation result (8.7); (5) signed
single-conditioning as a cross-check on joint exceedance correlation
(8.8); (6) sub-period splits, with an honest report of where the sample is
too small to say anything (8.5). **Not** performed in this pass (flagged
as future work, Section 13): threshold sensitivity for the GPD fit beyond
the diagnostics already in `figures/evt_threshold_diagnostics_*.png`;
Ang–Chen (2002)'s independent asymmetry estimator as a second methodology
cross-check (currently only Longin–Solnik's own estimator is implemented).

## 10. Economic interpretation

Three findings matter economically. First, **both markets' own tails are
far heavier than a normal model implies**, and an EVT/GPD approach tracks
the empirical extreme-loss quantiles much more closely than normal or
Student-$t$ alternatives — this alone supports using EVT-based risk
measures (VaR/ES) for either market individually, independent of any
cross-market question. Second, **the cross-market exceedance-correlation
result for this pair, at daily frequency over 2007–2026, does not
replicate the classic bear-market asymmetry** — if anything, this sample
shows the opposite pattern (stronger upside co-movement), and the
strongest evidence for *any* exceedance-correlation effect beyond the
normal benchmark is on the upside, not the downside. This should not be
read as "India-US diversification is safe in crises" — it should be read
as "this particular test, on this particular sample, does not find the
classic asymmetry," which is a narrower and more defensible claim. Third,
**alignment matters as much as the headline statistic** — a researcher or
risk manager who naively compared same-calendar-day closes would reach a
different conclusion than one who correctly accounts for the India/US
trading-hour mismatch.

## 11. Limitations

- **Small tail samples.** Most of the striking right-tail numbers in
  Section 8.3 rest on 18–31 joint exceedances; the left-tail numbers are
  explicitly shown to be unstable (8.4). This is the central limitation of
  this project and is not hidden in any section above.
- **Fixed, full-sample standardization** (not rolling/volatility-adjusted)
  means some of the "extreme correlation" signal could be a volatility-
  clustering artifact rather than a dependence-structure effect — addressed
  directly by Project 13 (GARCH+EVT), not resolved here.
- **Sub-period boundaries are a modeling choice**, not a detected
  structural break; and the GFC/COVID windows are simply too short at
  daily frequency to populate a 1–3σ joint-exceedance table reliably.
- **Data provenance**: both series come from unofficial third-party GitHub
  mirrors of Yahoo Finance pulls, validated by spot-checking four
  well-documented historical values (Section 5, `PROVENANCE.md`) rather
  than a full audit.
- **Non-overlapping sample lengths** between Nifty 50 (starts 2007) and
  S&P 500 (starts 1980) mean the GPD fits in 8.6 are not fit on the same
  calendar window and should not be read as a like-for-like comparison of
  "which market has heavier tails" in general.
- **Only one dependence estimator (Longin–Solnik) is implemented**; the
  pre-registered robustness plan to also apply the Ang & Chen (2002)
  estimator was not completed in this pass.
- **No causal claims are made or implied anywhere in this paper.** All
  statements are about statistical dependence, not about one market
  causing the other's extreme returns.

## 12. Conclusion

We examined whether the Longin & Solnik (2001) bear-market extreme-
correlation asymmetry extends to the Nifty 50–S&P 500 pair, using real,
independently validated daily data from 2007 to 2026. We do not find
evidence of the classic asymmetry in this sample: downside exceedance
correlation is small, unstable across thresholds, and not reliably
distinguishable from a bivariate-normal benchmark once multiple testing is
accounted for, while upside exceedance correlation is large and clearly
distinguishable from that benchmark. We find strong, much more robust
evidence that each market's own return distribution is heavy-tailed well
beyond what a normal model implies, and that EVT/GPD-based tail-risk
estimates track empirical extreme quantiles far better than normal or
Student-$t$ alternatives. We find that the choice of how to align the two
markets' non-synchronous trading days materially changes the cross-market
results. None of these findings is presented as final: the sample's tail
cells are small, and Projects 13 and 14 in this portfolio are designed
specifically to probe the volatility-clustering and asymptotic-dependence
questions this project's design cannot resolve on its own.

## 13. Future research

- Apply a rolling/GARCH-filtered standardization before re-running the
  exceedance-correlation test (Project 13), to separate a volatility-
  clustering explanation from a genuine dependence-structure explanation
  for the right-tail result in 8.3.
- Add the Ang & Chen (2002) asymmetry estimator as an independent
  methodology cross-check on the Longin–Solnik result.
- Extend the sample backward if a reliable pre-2007 Nifty 50 series can be
  sourced, to get a usable pre-GFC window (currently only 71 observations).
- Pursue a formal asymptotic-dependence/-independence test (Project 14)
  rather than the descriptive $\chi/\bar\chi$ diagnostics used here.
- Add a third market (EURO STOXX 50, Project 4) to see whether the
  upside-asymmetry pattern found here is specific to the India–US pair or
  more general.
- Confirm whether Ergen (2014)'s emerging-market sample includes India, to
  sharpen the Section 8.7 comparison.

## References

Ang, A. & Chen, J. (2002). Asymmetric Correlations of Equity Portfolios.
*Journal of Financial Economics*, 63(3), 443–494.

Bae, K.-H., Karolyi, G.A. & Stulz, R.M. (2003). A New Approach to Measuring
Financial Contagion. *Review of Financial Studies*, 16(3), 717–763.

Embrechts, P., Klüppelberg, C. & Mikosch, T. (1997). *Modelling Extremal
Events for Insurance and Finance*. Springer.

Ergen, I. (2014). Tail Dependence and Diversification Benefits in Emerging
Market Stocks: An Extreme Value Theory Approach. *Applied Economics*,
46(19), 2215–2227.

Hartmann, P., Straetmans, S. & de Vries, C.G. (2004). Asset Market Linkages
in Crisis Periods. *Review of Economics and Statistics*, 86(1), 313–326.

Karmakar, M. (2013). Estimation of Tail-Related Risk Measures in the
Indian Stock Market: An Extreme Value Approach. *Review of Financial
Economics*, 22(3), 79–85.

Longin, F. & Solnik, B. (2001). Extreme Correlation of International
Equity Markets. *Journal of Finance*, 56(2), 649–676.

McNeil, A.J. & Frey, R. (2000). Estimating Tail-Related Risk Measures for
Heteroscedastic Financial Time Series: An Extreme Value Approach. *Journal
of Empirical Finance*, 7(3–4), 271–300.

Poon, S.-H., Rockinger, M. & Tawn, J. (2004). Extreme Value Dependence in
Financial Markets: Diagnostics, Models, and Financial Implications.
*Review of Financial Studies*, 17(2), 581–610.

## Appendix: output index

All figures, tables, and the full results JSON referenced above are in
`figures/`, `tables/`, and `results/pipeline_summary.json` respectively,
and are reproducible by running `python -m src.pipeline` after `pip
install -r requirements.txt` (see `docs/REPRODUCIBILITY.md`).
