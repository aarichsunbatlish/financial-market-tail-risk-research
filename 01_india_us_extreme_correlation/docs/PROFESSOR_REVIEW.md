# Professor-Level Review — Project 1

Self-review in the voice of a referee specializing in extreme value theory
and international finance, applied to `paper/research_paper.md` as it
currently stands. This is written to find real problems, not to reassure.

**1. Is the research question precise?** Yes — "does the Longin-Solnik
bear-market asymmetry hold for India-US" is a specific, testable question.

**2. Is the methodology correct?** The exceedance-correlation and GPD
machinery is standard and correctly implemented (verified by unit tests
against synthetic known-answer cases, e.g. recovering known GPD
parameters). The Monte Carlo normal benchmark is a reasonable
implementation choice, though a referee would ask why the closed-form
asymptotic Longin-Solnik test statistic wasn't also reported alongside
the simulation — the answer ("simulation is more transparent and easier
to extend") is defensible but should be stated in the paper itself, not
just here.

**3. Is the data appropriate?** Partially. The two series are the right
economic objects (index levels), but they come from unofficial
third-party GitHub mirrors rather than an audited vendor. The spot-check
validation (matching two famous historical values exactly) is a
reasonable plausibility check but is not equivalent to a full data audit.
A referee at a journal would require vendor-sourced data before
publication; this paper says so explicitly (Limitations, Section 11) and
that is the right call, but it caps how seriously the specific numbers in
Section 8 can be taken as final.

**4. Is the sample large enough?** For the headline cross-market claims,
no — not at the extreme thresholds. 4,553 daily observations sounds large,
but the thing actually being estimated (joint exceedance correlation at
1.5-2σ) rests on 18-63 observations, and the paper itself shows (Section
8.4) that the 2σ left-tail bootstrap CI spans -0.27 to +0.36. This is the
single biggest weakness of the project, and the paper does not hide it —
but a referee would still say the headline abstract claim ("upside
exceedance correlation... far above the normal-model benchmark") needs the
sample-size caveat attached every time it's repeated, not just once in
Section 8.4.

**5. Are the tails sufficiently populated?** For the 1σ and 1.5σ cells,
marginally yes (29-143 joint exceedances); for 2.5σ and 3σ, explicitly no,
and the paper correctly declines to report those cells rather than present
a misleadingly precise number.

**6. Is the threshold defensible?** The GPD threshold (95th percentile) is
chosen with mean-excess and threshold-stability diagnostics as supporting
evidence (Section 4 of methodology.md), which is the right process. The
paper does not, however, show a formal sensitivity table of VaR/ES at
neighboring thresholds (e.g. 93rd vs. 97th percentile) — it only shows the
diagnostic plots. That specific robustness table is listed as not yet
done (Section 9) and should be added before this is submission-grade.

**7. Is the statistical inference valid?** Mostly. The bootstrap correctly
uses a block structure to account for serial dependence (good — a naive
i.i.d. bootstrap would understate uncertainty here). The multiple-testing
correction (Bonferroni across 10 threshold x tail cells) is applied and
changes the left-tail 1σ conclusion from "marginally significant" to "not
significant," which the paper reports honestly rather than quietly using
only the uncorrected number.

**8. Are there synchronization issues?** This is actually the project's
strongest methodological contribution: Section 8.9 shows explicitly that
the same-day, lag-1, and weekly alignments give materially different
answers. Many informal analyses of India-US correlation online use naive
same-day comparisons; this paper shows why that is a real problem, not a
pedantic one.

**9. Are volatility dynamics handled correctly?** No, and the paper says
so (Limitations): standardization is full-sample, not rolling or
GARCH-filtered. This means part of the "extreme correlation" signal could
mechanically be a volatility-clustering artifact (both markets having wide
swings during the same calm-to-turbulent regime shift) rather than a
genuine change in dependence structure. This is exactly the gap Project 13
is designed to close, and the paper is explicit that this project does not
resolve it.

**10. Is the normal benchmark appropriate?** As a benchmark for "what would
exceedance correlation look like with no extra tail dependence beyond
linear correlation," yes, this is the standard choice in this literature
(it's the Longin-Solnik benchmark itself). A referee might additionally
want a Student-t copula benchmark, which the paper lists as a planned but
not-yet-completed robustness check.

**11. Are we confusing correlation with causation?** No causal language
appears anywhere in the results or conclusion, and this is checked
explicitly in Limitations. Good.

**12. Are the conclusions supported?** The strongest conclusion (normal
models understate tail risk, Section 8.6) is well supported — large effect
size, big sample, consistent across both markets. The headline
cross-market conclusion (no bear-market asymmetry in this sample; if
anything an upside asymmetry) is supported by the data as presented, but
is correctly hedged throughout as sample-specific rather than a general
claim about "India and the US." That hedging is appropriate given point 4
above, not excessive caution.

**13. What would a referee criticize most?** Three things, in order: (a)
unverified third-party data provenance, (b) the small tail sample sizes
driving the most interesting (upside-asymmetry) result, and (c) the
absence of a second independent dependence-asymmetry estimator (Ang-Chen)
to cross-check the one Longin-Solnik estimator used throughout.

**14. What would make the paper stronger?** Vendor-sourced data; the
Ang-Chen cross-check; a GARCH-filtered version of the same test (i.e.,
doing Project 13 and folding it back in); extending the pre-GFC window if
a longer reliable Nifty 50 series can be found; and a Student-t copula
benchmark alongside the normal one.

**15. What is the natural next research question?** Whether the
GARCH-filtered (volatility-adjusted) version of this same test still shows
an upside-dominant pattern, or whether that pattern disappears once
time-varying volatility is accounted for — i.e., is this a dependence-
structure finding or a volatility-regime artifact? That is Project 13.

## Verdict

This project is methodologically sound and honestly reported, with its
major limitation (small tail samples driving the headline result) stated
repeatedly rather than buried. It should be read as a careful first pass
that found something genuinely unexpected (upside > downside exceedance
correlation) rather than confirming the textbook story — and it correctly
declines to oversell that unexpected finding given the sample sizes
involved. It is not submission-ready for a peer-reviewed finance journal
without vendor-sourced data and at least one additional dependence
estimator; it is a strong, honest foundation for a research portfolio.
