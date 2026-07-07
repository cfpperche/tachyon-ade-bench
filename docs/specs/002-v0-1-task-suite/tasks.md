# 002 — v0-1-task-suite — tasks

_Generated from `plan.md` on 2026-07-07. Work top-to-bottom. Check boxes as tasks complete. If a task reveals the plan is wrong, update `plan.md` before continuing._

## Implementation

- [x] Add harness support for `post_prepare`, dirty benchmark commit markers, and bytecode suppression.
- [x] Add T002 feature task for checkout discount support.
- [x] Add T003 dirty-worktree safety task.
- [x] Add T004 CI failure/status normalizer task.
- [x] Add T005 static UI responsive card task.
- [x] Add suite-level fixture check script.
- [x] Run local Tachyon/Codex dogfood across all five tasks.
- [x] Write `reports/tachyon-baseline-v0.1.md`.

## Verification

- [x] `python3 harness/bench.py check` passes.
- [x] `scripts/check-suite.sh` passes.
- [x] `scripts/smoke.sh` passes.
- [x] All five `runs/tachyon-v0.1-*` local dogfood runs pass verification.

**Headless check:** `scripts/check-suite.sh`
<!-- A mechanical command an agent can run to validate this spec's implementation
     without a human (tests / build / lint). Kept green = the spec stays delivered.
     To make `/sdd verify` re-run it, also declare it on a **Verify:** line, e.g.:
       **Verify:** `npm test`
     `/sdd verify` reads the FIRST backtick span per **Verify:** line, previews by
     default, and runs only with --run. Multiple **Verify:** lines run in order. -->

**Verify:** `scripts/check-suite.sh`
**Verify:** `scripts/smoke.sh`

## Dogfood

**Dogfood:** `scripts/check-suite.sh`
<!-- A representative command that exercises the shipped behavior end-to-end.
     `/sdd dogfood` previews by default and runs only with --run, then logs under
     notes.md `## Dogfood log`. If no meaningful headless dogfood exists, replace
     the Dogfood line with: **Dogfood-Opt-Out:** <non-empty reason>. -->

**Human dogfood:** inspect `reports/tachyon-baseline-v0.1.md` after the local dogfood run.
<!-- Opt-in: a short walkthrough a human follows to approve the spec (demo steps,
     UI routes, things to eyeball). Name the steps here when human sign-off matters. -->

## Visual QA

**Visual QA Opt-Out:** This spec adds benchmark fixtures and CLI/report artifacts; the UI task itself is verified by static checks, not by changing a live UI surface.
