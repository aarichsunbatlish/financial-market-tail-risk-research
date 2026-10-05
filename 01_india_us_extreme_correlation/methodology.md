# Methodology — Project 1: Extreme Correlation Between Indian and US Equity Markets

Notation: let $X_t$, $Y_t$ denote daily log returns of Nifty 50 and S&P 500
respectively (standardized, as needed, to z-scores $x_t, y_t$ using each
market's own full-sample or sub-period mean/standard deviation — see
`data_dictionary.md`).

## 1. Descriptive statistics

For each market and sub-period: mean, standard deviation, skewness,
excess kurtosis, minimum/maximum, and the Jarque–Bera test statistic

$$JB = \frac{n}{6}\Big(S^2 + \frac{(K-3)^2}{4}\Big)$$

where $S$ is sample skewness and $K$ is sample kurtosis, tested against a
$\chi^2_2$ null of normality. QQ plots against a normal reference
distribution are produced for each market and sub-period.

## 2. Rolling and conditional correlation

- **Rolling Pearson correlation**: computed on daily log returns over
  rolling windows of 60 and 250 trading days (reported on the same-day and
  US-lag-1 alignments — see `data_dictionary.md`).
- **Conditional correlation on sign**: unconditional correlation,
  correlation conditional on $X_t<0$, and correlation conditional on
  $X_t>0$, as a simple first look at asymmetry before the formal
  exceedance-correlation test.

## 3. Exceedance correlation (Longin & Solnik, 2001)

For a threshold $\theta \ge 0$ (expressed in standard deviations), define
the **joint exceedance correlation** in the left (lower) tail as

$$\rho^{-}(\theta) = \mathrm{Corr}(x_t, y_t \mid x_t < -\theta,\; y_t < -\theta)$$

and in the right (upper) tail as

$$\rho^{+}(\theta) = \mathrm{Corr}(x_t, y_t \mid x_t > \theta,\; y_t > \theta).$$

This project also reports the **signed single-conditioning** correlation,
conditioning on only one market's exceedance (e.g. $x_t < -\theta$ alone),
as a check of whether the result depends on which market's tail defines the
joint-exceedance set — a robustness point raised in the asymmetric-
dependence literature.

Thresholds are evaluated at $\theta \in \{1, 1.5, 2, 2.5, 3\}$ standard
deviations, continuing further only where the exceedance sample size
remains large enough to report (a minimum effective sample size of 15 joint
exceedances is required to report a point estimate at all, flagged in every
output table — small tail samples are a known limitation of this
methodology, not hidden).

## 4. Peaks-over-threshold and the Generalized Pareto Distribution

For a (negated, for the left tail) return series and a high threshold $u$,
let $Y = -X - u$ for exceedances $-X > u$. The Pickands–Balkema–de Haan
theorem motivates approximating the conditional exceedance distribution by
a **Generalized Pareto Distribution (GPD)**:

$$G_{\xi,\beta}(y) = \begin{cases} 1-\left(1+\xi y/\beta\right)^{-1/\xi} & \xi \ne 0 \\ 1-\exp(-y/\beta) & \xi = 0 \end{cases}, \quad y \ge 0$$

with shape (tail index) $\xi$ and scale $\beta>0$, fit by maximum likelihood
(`scipy.stats.genpareto`).

**Threshold selection** uses two diagnostics, not a single rule:
1. The **mean excess function** $e(u) = E[{-X-u} \mid -X>u]$, which should
   be approximately linear in $u$ over the range where a GPD is appropriate.
2. A **threshold-stability plot**: $\hat\xi(u)$ and $\hat\beta(u)$ (reparam.
   to be threshold-invariant) plotted across a grid of candidate thresholds,
   looking for a stable region rather than picking a single arbitrary
   quantile.

The threshold ultimately used is reported explicitly alongside the
resulting number of exceedances, and results are re-run at two alternative
thresholds as a robustness check (Section 8).

## 5. VaR and Expected Shortfall from the fitted GPD

Given a fitted GPD above threshold $u$ with $n$ total observations and
$N_u$ exceedances, the tail probability is modeled as
$P(-X>u) \approx N_u/n$, giving, for a tail probability $p < N_u/n$:

$$VaR_p = u + \frac{\beta}{\xi}\left[\left(\frac{n}{N_u}(1-p)\right)^{-\xi}-1\right]$$

$$ES_p = \frac{VaR_p + \beta - \xi u}{1-\xi}, \quad \xi<1$$

These are compared against: the empirical historical quantile, a fitted
normal model, and a fitted Student-$t$ model, at $p \in \{0.99, 0.995,
0.999\}$.

## 6. Empirical tail-dependence coefficient ($\chi$, $\bar\chi$)

Using the rank-transformed (empirical copula) data $u_t = \hat F_X(x_t)$,
$v_t = \hat F_Y(y_t) \in (0,1)$, the standard EVT tail-dependence
coefficient is estimated as

$$\hat\chi(q) = \frac{\#\{t : u_t > q,\, v_t > q\}}{n(1-q)}$$

for $q$ close to 1 (e.g. 0.95, 0.975, 0.99), with the Coles–Heffernan–Tawn
(1999) $\bar\chi$ diagnostic also computed to distinguish asymptotic
dependence ($\chi>0$ as $q\to1$) from asymptotic independence
($\chi\to0$, $\bar\chi<1$). **This project reports $\hat\chi(q)$ and
$\hat{\bar\chi}(q)$ at finite $q$ as descriptive evidence only** — a
rigorous asymptotic-dependence/-independence conclusion requires the
dedicated treatment in Project 14 and is not claimed here.

## 7. Normal-model benchmark (simulation-based inference)

Longin & Solnik's central test compares the *observed* exceedance
correlation against the exceedance correlation **implied by a
bivariate-normal distribution with the same unconditional correlation**.
This project implements that benchmark by Monte Carlo rather than the
closed-form asymptotic formula, for transparency and ease of extension:

1. Estimate the unconditional correlation $\hat\rho$ and marginal
   standard deviations from the data (per sub-period).
2. Simulate $M=5{,}000$ draws from $N(0,\Sigma)$ with $\Sigma$ matched to
   $\hat\rho$ and the observed marginal variances.
3. Compute the same exceedance-correlation statistic on each simulated
   draw's empirical exceedance set, repeated $R=1{,}000$ times (resampling
   $n$-sized draws) to build a Monte Carlo distribution of the
   normal-implied exceedance correlation at each threshold.
4. Report the observed statistic against this simulated distribution's
   median and 95% interval, and a one-sided Monte Carlo p-value: the
   fraction of simulated draws with exceedance correlation $\ge$ the
   observed value.

**Hypotheses** (per threshold, per tail):
$H_0$: the observed exceedance correlation is consistent with a
bivariate-normal model at the sample's unconditional correlation.
$H_1$: the observed left-tail exceedance correlation exceeds the
normal-implied benchmark (the Longin–Solnik asymmetry hypothesis).
Significance level: 5%, one-sided, per threshold — **not** corrected
across thresholds by default; a Bonferroni-adjusted version across the 5
thresholds × 2 tails × number of sub-periods is also reported given the
multiple-testing concern this involves.

## 8. Bootstrap confidence intervals

Daily financial returns exhibit volatility clustering (serial dependence in
magnitude even when returns themselves are roughly uncorrelated), so a
naive i.i.d. bootstrap understates uncertainty. This project uses a
**moving block bootstrap** with block length
$\ell = \lceil n^{1/3} \rceil$ (a standard rule of thumb), $B=2{,}000$
replications, for confidence intervals on: unconditional correlation,
exceedance correlation at each threshold, and the GPD tail-index estimate.

## 9. Robustness checks (mandatory, Section 7 of the paper)

1. **Alignment**: same-calendar-day vs. US-lag-1 vs. weekly (see
   `data_dictionary.md` for why same-day is the economically naive
   alignment given the trading-hour mismatch).
2. **Threshold choice**: GPD threshold varied by one quantile step up and
   down from the selected value.
3. **Sub-period boundaries**: results re-run shifting each crisis window's
   start/end by ±1 month.
4. **Alternative benchmark**: Student-$t$ (fit by MLE) in addition to the
   normal benchmark, since fat-tailed-but-still-elliptical benchmarks are a
   natural intermediate case.
5. **Multiple testing**: Bonferroni-adjusted significance alongside raw
   p-values (Section 7).

## 10. Known limitations of this design (stated upfront, not discovered after the fact)

- Fixed (non-rolling) standardization in the main specification likely
  understates how much of the "extreme correlation" effect is really a
  volatility-clustering effect rather than a dependence-structure effect —
  this is exactly the question Project 13 (GARCH+EVT) is designed to
  answer, and this project's results should be read as a first pass, not
  the final word.
- Two markets, ~18 overlapping years of daily data: tail sample sizes at
  the most extreme thresholds (e.g. 3σ) will be small, and this project
  reports — rather than hides — wherever a cell falls below the minimum
  reportable exceedance count.
- Sub-period boundaries are a modeling choice, not a statistically detected
  break.
