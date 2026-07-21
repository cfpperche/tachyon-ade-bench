# 015 — jetbrains-air-inclusion — tasks

_Generated from `plan.md` on 2026-07-21. Work top-to-bottom. If implementation reveals the plan is wrong, update `plan.md` before continuing._

## Implementation

- [x] Add the official-source JetBrains Air competitor profile.
- [x] Synchronize all human-readable rosters and the competitor map.
- [x] Register JetBrains Air and repair Herdr coverage in acquisition intelligence.
- [x] Add battlecard/packaging signals for JetBrains Air and a baseline Herdr signal.
- [x] Add English and Portuguese SWOT threat copy.
- [x] Enforce complete competitor coverage in the advertiser registry.
- [x] Record validation, dogfood, and visual QA evidence in `notes.md`.

## Verification

- [x] `python3 harness/bench.py check` passes.
- [x] `python3 scripts/intelligence/check-intelligence.py` passes.
- [x] `python3 scripts/marketing/check-marketing.py` passes.
- [x] `python3 scripts/marketing/summarize-history.py --check` passes.
- [x] `scripts/check-suite.sh` passes.
- [x] `scripts/smoke.sh` passes.
- [x] `npm run dashboard:check` passes.
- [x] `npm run dashboard:build` passes.

**Headless check:** `scripts/check-suite.sh && scripts/smoke.sh && npm run dashboard:check && npm run dashboard:build`

**Verify:** `python3 harness/bench.py check`
**Verify:** `python3 scripts/intelligence/check-intelligence.py`
**Verify:** `python3 scripts/marketing/check-marketing.py`
**Verify:** `scripts/check-suite.sh`
**Verify:** `scripts/smoke.sh`
**Verify:** `npm run dashboard:check`
**Verify:** `npm run dashboard:build`

## Dogfood

**Dogfood:** `python3 harness/bench.py list-products`

**Human dogfood:** Open `/competitors/jetbrains-air/`, `/pt/competitors/jetbrains-air/`, `/matrix/`, `/strategy/`, `/battlecards/`, and `/sources/`; confirm Air is correctly classified, sourced, readable, and not presented as scored.

## Visual QA

Inspect the new profile, matrix row, chart toggle, strategy row, battlecard, and source list in English and Portuguese at desktop and mobile widths.
