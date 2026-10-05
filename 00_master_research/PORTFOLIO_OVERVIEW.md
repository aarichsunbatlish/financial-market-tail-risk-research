# Research Portfolio: Extreme Risk and Financial Markets in India

## The connecting argument

1. **Financial risk lives disproportionately in the tails.** Standard
   deviation and ordinary correlation describe "typical" co-movement; crises
   are, by definition, not typical. A model fit to the whole distribution can
   be a poor guide to the 1-in-100 or 1-in-1000 day.

2. **Ordinary correlation can hide crisis dependence.** The exceedance-
   correlation literature (Longin & Solnik, 2001; Ang & Chen, 2002) shows
   that equity markets that look moderately linked unconditionally can move
   together much more strongly in joint downturns than a normal/Gaussian
   benchmark implied by that same unconditional correlation would predict —
   and the effect is typically asymmetric (more pronounced in joint losses
   than joint gains). Project 1 asks whether this holds between India and
   the US; Projects 3, 4, 9, 10 ask the same question across other pairs
   (Indian sectors, India/US/Europe, Indian banks, safe-haven assets).

3. **EVT provides tools for modelling extreme outcomes directly**, rather
   than extrapolating from a distribution fit to the center of the data.
   Projects 2 and 13 apply peaks-over-threshold/GPD modelling to single
   series (Bank Nifty); Project 14 asks the deeper methodological question
   of whether extreme dependence between two series persists at arbitrarily
   extreme levels (asymptotic dependence) or vanishes (asymptotic
   independence) — a distinction ordinary correlation cannot even express.

4. **Options contain forward-looking information about tail risk.**
   Projects 6, 7, and 8 turn from the historical (physical) distribution to
   the risk-neutral distribution implied by option prices, asking whether
   the market's own pricing of downside protection is consistent with what
   historical extremes would suggest, and what that implies for how short
   option positions should be risk-managed (Project 8, explicitly as an
   academic exercise, not an exchange-margin proposal).

5. **Corporate leverage can interact with downside risk at the firm level.**
   Project 11 asks whether balance-sheet leverage predicts heavier downside
   equity tails; Project 12 connects this to options theory and default risk
   directly via the Merton structural model, estimating distance-to-default
   and asking whether riskier-by-that-measure firms also show different
   tail behavior in their equity returns.

6. **Systemic risk emerges when extreme dependence increases disproportionately
   among connected institutions.** Project 9 studies this among major Indian
   banks — being explicit that elevated extreme co-movement is a *proxy* for
   systemic risk under discussion in the literature, not proof of a causal
   transmission channel.

7. **Diversification can fail precisely when it is needed most.** This is
   the thread tying nearly every project together: Projects 1, 3, 4, 9, and
   10 each test, in a different market context, whether assets that
   diversify a portfolio in normal times continue to do so during extreme
   stress — and report honestly when they don't.

## How the projects connect methodologically

Projects 1 → 2 → 13 → 14 form a methodological spine: cross-market
dependence (1), single-series tail modelling (2), volatility-filtered tail
modelling (13), and the deepest dependence question the portfolio asks
(14). Projects 3, 4, 9, 10 are applications of Project 1's toolkit to new
asset sets. Projects 6, 7, 8 form a derivatives spine built on the physical-
vs-risk-neutral distinction. Projects 11, 12 form a corporate-finance spine
connecting leverage, structural default modelling, and the same tail
machinery used everywhere else.

## Current state of this argument

As of this writing, only Project 1 has been carried through to real
empirical analysis (see its `paper/research_paper.md`). The claims above
describe the portfolio's intended structure and the literature motivating
it — they are not yet all empirically verified within this repository.
`MASTER_RESEARCH_INDEX.md` tracks, project by project, which of these
connections are backed by completed analysis versus still a research design.
