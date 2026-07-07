# 006 — acquisition-intelligence-foundation — tasks

_Generated from `plan.md` on 2026-07-07. Work top-to-bottom. Check boxes as tasks complete. If a task reveals the plan is wrong, update `plan.md` before continuing._

## Implementation

- [x] Add marketing registry files for advertisers and source channels.
- [x] Add marketing storage roots for scans, history, current summaries, and creatives.
- [x] Add JSON schemas for advertiser registry, source registry, scan manifest, raw scan, normalized scan, ad observation, current ads, campaigns, and coverage.
- [x] Add validation, normalization, and summarization scripts.
- [x] Wire marketing validation into check-suite and GitHub Actions.
- [x] Update docs with the implemented commands and persistence model.

## Verification

- [x] `python3 scripts/marketing/check-marketing.py` passes.
- [x] `python3 scripts/marketing/summarize-history.py --check` passes on an empty scan set.
- [x] `python3 harness/bench.py check` still passes.
- [x] `scripts/check-suite.sh` passes.

**Headless check:** `python3 scripts/marketing/check-marketing.py && python3 scripts/marketing/summarize-history.py --check && python3 harness/bench.py check`
**Verify:** `python3 scripts/marketing/check-marketing.py`
**Verify:** `python3 scripts/marketing/summarize-history.py --check`
**Verify:** `python3 harness/bench.py check`

## Dogfood

**Dogfood:** `scripts/check-suite.sh`

**Human dogfood:** Read `docs/acquisition-intelligence.md` and confirm that the
registry/scan/history model is understandable before the first real platform
collector is added.

## Visual QA

**Visual QA Opt-Out:** CLI/docs/data only; no rendered interface changes.
