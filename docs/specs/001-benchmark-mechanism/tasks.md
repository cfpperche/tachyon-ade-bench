# 001 — benchmark-mechanism — tasks

_Generated from `plan.md` on 2026-07-07. Work top-to-bottom. Check boxes as tasks complete. If a task reveals the plan is wrong, update `plan.md` before continuing._

## Implementation

- [x] Create public-facing README, license, and protocol document.
- [x] Add seed competitor profiles for the initial ADE roster.
- [x] Add schemas for competitor profiles, tasks, and run results.
- [x] Implement dependency-free harness commands: check, list-products, list-tasks, prepare, verify.
- [x] Add one smoke benchmark task with a fixture repository and verifier.
- [x] Add a smoke script that proves check, prepare, failing baseline, fixed baseline, and verify pass.

## Verification

- [x] `python3 harness/bench.py check` passes.
- [x] `scripts/smoke.sh` passes.
- [x] The repository is committed and pushed to `cfpperche/tachyon-ade-bench`.

**Headless check:** `scripts/smoke.sh`
<!-- A mechanical command an agent can run to validate this spec's implementation
     without a human (tests / build / lint). Kept green = the spec stays delivered.
     To make `/sdd verify` re-run it, also declare it on a **Verify:** line, e.g.:
       **Verify:** `npm test`
     `/sdd verify` reads the FIRST backtick span per **Verify:** line, previews by
     default, and runs only with --run. Multiple **Verify:** lines run in order. -->

**Verify:** `scripts/smoke.sh`

## Dogfood

**Dogfood:** `scripts/smoke.sh`
<!-- A representative command that exercises the shipped behavior end-to-end.
     `/sdd dogfood` previews by default and runs only with --run, then logs under
     notes.md `## Dogfood log`. If no meaningful headless dogfood exists, replace
     the Dogfood line with: **Dogfood-Opt-Out:** <non-empty reason>. -->

**Human dogfood:** inspect the generated `runs/dogfood` directory, then delete it.
<!-- Opt-in: a short walkthrough a human follows to approve the spec (demo steps,
     UI routes, things to eyeball). Name the steps here when human sign-off matters. -->

## Visual QA

**Visual QA Opt-Out:** This spec ships repository infrastructure and CLI output only.
