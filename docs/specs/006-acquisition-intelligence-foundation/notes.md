# 006 — acquisition-intelligence-foundation — notes

_Created 2026-07-07._

_In-flight design memory — decisions, deviations, tradeoffs, and open questions surfaced **while building** that weren't pre-empted by `spec.md` or `plan.md`. Append-only by convention._

## Design decisions

- The foundation stores no real competitor ad observations yet. Empty history is
  valid because the first goal is contract reproducibility.

## Deviations

- No `marketing/history/ads.ndjson` or `marketing/current/*.json` files are
  committed until real scan observations exist, to avoid generated timestamp
  churn from empty derived files.

## Tradeoffs

- The scripts perform explicit structural checks instead of full JSON Schema
  validation to avoid adding a Python dependency before collectors exist.

## Open questions

- The first collector should be chosen after one manual scan proves which
  fields are stable enough to automate.

## Verification log

### 2026-07-07T21:00:52Z — pass (3/3) — source: tasks.md
- `python3 scripts/marketing/check-marketing.py` — pass
- `python3 scripts/marketing/summarize-history.py --check` — pass
- `python3 harness/bench.py check` — pass

## Dogfood log

### 2026-07-07T21:00:52Z — pass (1/1) — source: tasks.md — commit: 8d3db978b0489cf51c75b7e97e30fa6808c2a481
- `scripts/check-suite.sh` — pass
