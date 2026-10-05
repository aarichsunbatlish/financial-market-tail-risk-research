# Research Principles (binding across every project in this portfolio)

These rules govern every project folder in this repository. A project that
violates one of these is not finished — it is broken, regardless of how
complete its code or paper looks.

## 1. Never fabricate

- Never fabricate data. If real data cannot be obtained in this environment,
  say so explicitly, build the pipeline anyway, and use clearly-labeled
  synthetic data **only** for testing the pipeline — never present it as an
  empirical finding.
- Never fabricate empirical results: regression coefficients, p-values,
  correlations, tail indices, VaR, Expected Shortfall, option prices,
  implied volatilities, default probabilities, or conclusions. Every number
  that appears in a `paper/` or `results/` file must have been produced by
  code in that project's `src/` actually being run — not estimated from
  memory or "plausible" invented values.
- If a result has not been computed yet, the paper must say
  `RESULTS TO BE COMPLETED AFTER DATA EXECUTION` in that section rather than
  presenting a placeholder as if it were a finding.

## 2. Distinguish claim types explicitly

Every empirical statement in a paper should be identifiable as one of:
established literature, replication, extension, original analysis,
hypothesis, interpretation, or speculation. Don't blur these.

## 3. Never overclaim

Do not use "novel," "first study," "new contribution," "proves," or
"causes" unless the literature review and the identification strategy
actually support it (and in practice, for an individual research-portfolio
project, they rarely do for "novel"/"first"/"proves"/"causes"). Prefer:
"we investigate," "we examine," "our analysis suggests," "consistent with,"
"we find evidence of," "we replicate," "we extend."

## 4. Literature review before claiming contribution

Every project does a literature pass before deciding what kind of
contribution it is (replication / extension / application / methodological
comparison / potentially novel). Build a literature matrix: paper, author,
year, question, data, method, main result, limitation, relevance,
potential extension. Summarizing is not enough — each entry should say how
it shaped this project's design.

## 5. Take the standard biases and pitfalls seriously

For every empirical project, explicitly check for and discuss (not just
list): look-ahead bias, survivorship bias, selection bias, data leakage,
non-synchronous trading (critical for India/US same-day comparisons),
multiple testing, small-sample problems in the tails specifically,
structural breaks, volatility clustering, and regime changes.

## 6. Statistical rigor for tail estimation specifically

- State null/alternative hypotheses, confidence levels, and test statistics
  explicitly.
- For POT/GPD work: justify the threshold (mean excess plot + stability
  plot), report tail-index uncertainty, and address dependence between
  exceedances (clustering) — decluster or discuss why not.
- Use bootstrap (block bootstrap where serial dependence is present) for
  confidence intervals on correlation/tail statistics, and say how many
  replications and why.

## 7. Robustness is mandatory, not optional

Every empirical paper tests sensitivity to at least: alternative thresholds,
alternative sub-periods, alternative frequencies (daily vs weekly), and an
alternative benchmark distribution. If a result does not survive these, the
paper says so.

## 8. Code quality

Modular `src/` functions with docstrings and type hints, reusable from thin
notebooks (never notebook-only logic), fixed random seeds, and pytest unit
tests for every quantitative module. No single giant notebook.

## 9. Visuals and tables answer a question

Every figure/table exists to answer part of the stated research question.
No decorative charts.

## 10. Honesty about scope

A project that has only built infrastructure (no real data run yet) should
say exactly that in its README and paper — not imply more progress than has
actually happened.
