# Research Notes — Project 1 (working log)

- 2026-10-05: Network test confirmed this environment cannot reach Yahoo
  Finance, NSE, Stooq, or FRED directly (all egress-blocked), but
  `raw.githubusercontent.com` is reachable. Located and validated two
  third-party GitHub-hosted mirrors of Yahoo Finance `^NSEI` and `^GSPC`
  pulls against independently documented historical closing lows (GFC,
  COVID) — both matched exactly. Used these as real data rather than
  falling back to synthetic data for this project. See
  `data/raw/PROVENANCE.md`.
- 2026-10-05: Live web search (this session) confirmed the exact empirical
  finding of Longin & Solnik (2001) — correlation rises in bear markets but
  not bull markets, driven by trend not volatility — and located two
  India-adjacent papers (Karmakar 2013 on conditional EVT in the Indian
  market; Ergen 2014 on emerging-market tail dependence/asymptotic
  independence) that were not assumed from memory alone. Full text of
  neither was accessible (publisher sites blocked); both are cited at
  abstract-level with that caveat stated in `literature_review.md`.
- Decision: standardization (z-scores) in the main specification uses
  full-sample, not rolling, mean/sd. This is a known simplification —
  documented as a limitation, deferred to Project 13 (GARCH+EVT) rather
  than solved here, to keep this project's scope matched to the
  Longin–Solnik replication it is built on.
- Open question for extension: does Ergen (2014)'s emerging-market sample
  include India? Could not confirm from search abstract; flagged for
  follow-up before citing more specifically.
