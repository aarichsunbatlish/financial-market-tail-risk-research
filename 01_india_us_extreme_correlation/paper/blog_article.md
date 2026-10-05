# Does India Fall With America When Markets Crash? What the Data Actually Says

## Why this matters

If you hold both Indian and US stocks, you're probably counting on them
not to crash at exactly the same time — that's the whole point of
diversifying across countries. A well-known finding in finance research is
that this protection can quietly disappear exactly when you need it most:
developed stock markets tend to move together *more* strongly during joint
crashes than during joint rallies, and more than simple correlation
numbers would suggest. We asked: does the same thing happen between
India's Nifty 50 and the US S&P 500?

## The intuition

Ordinary correlation is an average over all days — calm days, good days,
and bad days alike. But what actually worries an investor is a narrower
question: "when both markets are having a bad day, how much do they move
together?" That's a different number, called *exceedance correlation*,
and it can be much higher (or lower) than the everyday correlation.
Researchers Longin and Solnik found, for pairs of developed markets, that
this "bad-day correlation" rises well above what a normal bell-curve
model would predict — but only on the downside, not the upside.

## The data

We used real daily closing prices for the Nifty 50 (back to September
2007) and the S&P 500 (back to 1980), pulled from public data mirrors and
checked against two very well-documented historical facts — the exact
closing low of each index during the 2008 financial crisis and the March
2020 COVID crash — before trusting them. Both matched exactly, which gave
us confidence this was genuine market history, not placeholder numbers.

## The methodology, in plain terms

1. Turn each day's price into a return, and flag how many standard
   deviations it was from average (a "how extreme was this day" score).
2. Look only at days where *both* Nifty and the S&P 500 had an extreme day
   in the same direction, and compute the correlation just within that
   small, extreme subset.
3. Compare that number against what you'd expect if returns followed a
   simple bell-curve (normal distribution) with the same everyday
   correlation — using computer simulation rather than a textbook formula,
   so the comparison is transparent and checkable.
4. Separately, fit a statistical model built specifically for extreme
   events (extreme value theory) to each market's worst days, to get a
   more realistic picture of how bad a "really bad day" can be.

## The results

This is the part where we have to be honest about something counter to
the textbook story: **in this data, it's the good-day correlation that's
unusually high, not the bad-day correlation.** When both markets have a
strongly positive day, they move together far more than a bell-curve model
would predict. When both have a strongly negative day, the extra
co-movement is much smaller and, once you account for how few truly
extreme joint-crash days exist in the sample (around 2–3 dozen in nearly
two decades), not reliably different from what you'd expect by chance.

Two other results are much more solid. First, both markets' worst days
are far worse than a normal bell-curve would suggest — a normal model
would have underestimated the worst 1-in-1000-day loss by roughly 45%.
The extreme-value model got much closer to what actually happened.
Second, *how* you line up the two markets' trading days — same calendar
day, versus accounting for India trading hours before the US market even
opens that day, versus comparing week-to-week — changes the answer by a
lot. That's a strong reminder that "just look at the correlation" can be
misleading when two markets don't trade at the same time.

## What we learn

- Don't assume the textbook "crashes travel together more than rallies
  do" result automatically applies to every market pair — it's an
  empirical question, and for India-US daily data over this period, we
  don't find it.
- Individual market crash risk is still very real and very underestimated
  by simple bell-curve models — that part of the extreme-value story holds
  up clearly here.
- When comparing markets that trade at different times of day, how you
  line up the days matters as much as the statistic itself.

## Limitations

The number of truly extreme joint-crash days in this sample is small
(think dozens, not thousands), so some of these numbers come with wide
uncertainty — we report that uncertainty explicitly rather than hiding it.
The 2008 and 2020 crisis windows specifically are too short, at daily
data, to say anything reliable on their own.

## Further reading

Longin, F. & Solnik, B. (2001), "Extreme Correlation of International
Equity Markets," *Journal of Finance* — the original paper this project
is built on. See `literature_review.md` in this project folder for more.

## Code / reproducibility

Everything here was computed by the open code in this project's `src/`
folder, run against the data in `data/raw/` (with its sourcing fully
documented in `data/raw/PROVENANCE.md`). See `docs/REPRODUCIBILITY.md` to
re-run it yourself.
