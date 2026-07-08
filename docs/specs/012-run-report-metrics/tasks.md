# 012 — run-report-metrics — tasks

_Generated from `plan.md` on 2026-07-08. Work top-to-bottom. Check boxes as tasks complete. If a task reveals the plan is wrong, update `plan.md` before continuing._

## Implementation

- [x] Extend run-result schema with metric sections.
- [x] Initialize metrics in `prepare`.
- [x] Update timing/artifact/review metrics in `verify`.
- [x] Add run report metrics documentation.
- [x] Exercise prepare/verify on a temporary run.

## Verification

_Acceptance checks tied to `spec.md`. Each should map to a checklist item there._

- [x] `python3 harness/bench.py prepare --product tachyon --task T001-python-bugfix --run-id metrics-smoke` writes initialized metrics.
- [x] `python3 harness/bench.py verify runs/metrics-smoke` updates time-to-verified-change.
- [x] `scripts/check-suite.sh` passes.
- [x] `npm run dashboard:check` passes.

**Headless check:** `scripts/check-suite.sh && npm run dashboard:check`
<!-- A mechanical command an agent can run to validate this spec's implementation
     without a human (tests / build / lint). Kept green = the spec stays delivered.
     To make `/sdd verify` re-run it, also declare it on a **Verify:** line, e.g.:
       **Verify:** `npm test`
     `/sdd verify` reads the FIRST backtick span per **Verify:** line, previews by
     default, and runs only with --run. Multiple **Verify:** lines run in order. -->

**Verify:** `scripts/check-suite.sh`
**Verify:** `npm run dashboard:check`

## Dogfood

**Dogfood:** `rm -rf runs/metrics-smoke && python3 harness/bench.py prepare --product tachyon --task T001-python-bugfix --run-id metrics-smoke && python3 harness/bench.py verify runs/metrics-smoke || true`
<!-- A representative command that exercises the shipped behavior end-to-end.
     `/sdd dogfood` previews by default and runs only with --run, then logs under
     notes.md `## Dogfood log`. If no meaningful headless dogfood exists, replace
     the Dogfood line with: **Dogfood-Opt-Out:** <non-empty reason>. -->

**Human dogfood:** Inspect `runs/metrics-smoke/result.json` and confirm metrics are present and timing is populated.
<!-- Opt-in: a short walkthrough a human follows to approve the spec (demo steps,
     UI routes, things to eyeball). Name the steps here when human sign-off matters. -->

## Visual QA

_Optional for UI/interface/rendered-output work. Keep prose-based: real surface inspected, evidence captured, verdict recorded. If not useful, declare `**Visual QA Opt-Out:** <reason>`._

**Visual QA Opt-Out:** schema/harness documentation only.
