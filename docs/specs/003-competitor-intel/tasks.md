# 003 — competitor-intel — tasks

_Generated from `plan.md` on 2026-07-07. Work top-to-bottom. Check boxes as tasks complete. If a task reveals the plan is wrong, update `plan.md` before continuing._

## Implementation

- [x] Extend the competitor schema with a structured `research` object.
- [x] Add harness validation for required research fields and source URLs.
- [x] Populate enriched research data for every product in `competitors/`.
- [x] Add maintainer documentation for competitor research updates.
- [x] Add a v0.1 competitor map report.
- [x] Verify metadata, suite checks, and SDD close hygiene.

## Verification

- [x] `python3 harness/bench.py check` passes.
- [x] `scripts/check-suite.sh` passes after the schema/harness changes.
- [x] `scripts/smoke.sh` passes after the schema/harness changes.

**Headless check:** `python3 harness/bench.py check`
<!-- A mechanical command an agent can run to validate this spec's implementation
     without a human (tests / build / lint). Kept green = the spec stays delivered.
     To make `/sdd verify` re-run it, also declare it on a **Verify:** line, e.g.:
       **Verify:** `npm test`
     `/sdd verify` reads the FIRST backtick span per **Verify:** line, previews by
     default, and runs only with --run. Multiple **Verify:** lines run in order. -->

**Verify:** `python3 harness/bench.py check`
**Verify:** `scripts/check-suite.sh`
**Verify:** `scripts/smoke.sh`

## Dogfood

**Dogfood:** `python3 harness/bench.py list-products`
<!-- A representative command that exercises the shipped behavior end-to-end.
     `/sdd dogfood` previews by default and runs only with --run, then logs under
     notes.md `## Dogfood log`. If no meaningful headless dogfood exists, replace
     the Dogfood line with: **Dogfood-Opt-Out:** <non-empty reason>. -->

**Human dogfood:** read `reports/competitor-map-v0.1.md` and confirm it is useful before running competitors.
<!-- Opt-in: a short walkthrough a human follows to approve the spec (demo steps,
     UI routes, things to eyeball). Name the steps here when human sign-off matters. -->

## Visual QA

**Visual QA Opt-Out:** Docs and JSON only; no rendered UI surface changes.
