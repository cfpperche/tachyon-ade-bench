# 011 — strategy-swot-dashboard — tasks

_Generated from `plan.md` on 2026-07-08. Work top-to-bottom. Check boxes as tasks complete. If a task reveals the plan is wrong, update `plan.md` before continuing._

## Implementation

- [x] Add strategy/pressure data types and derived rows.
- [x] Add localized Strategy/SWOT copy in EN/PT.
- [x] Add shared StrategyBoard component.
- [x] Add `/strategy/` and `/pt/strategy/` routes.
- [x] Add Strategy to navigation.
- [x] Add responsive styling.

## Verification

_Acceptance checks tied to `spec.md`. Each should map to a checklist item there._

- [x] `npm run dashboard:check` passes.
- [x] `npm run dashboard:build` passes and emits both strategy routes.
- [x] `scripts/check-suite.sh` passes.
- [x] Browser screenshots show the strategy page on desktop/mobile.

**Headless check:** `npm run dashboard:check && npm run dashboard:build && scripts/check-suite.sh`
<!-- A mechanical command an agent can run to validate this spec's implementation
     without a human (tests / build / lint). Kept green = the spec stays delivered.
     To make `/sdd verify` re-run it, also declare it on a **Verify:** line, e.g.:
       **Verify:** `npm test`
     `/sdd verify` reads the FIRST backtick span per **Verify:** line, previews by
     default, and runs only with --run. Multiple **Verify:** lines run in order. -->

**Verify:** `npm run dashboard:check`
**Verify:** `npm run dashboard:build`
**Verify:** `scripts/check-suite.sh`

## Dogfood

**Dogfood:** `npm run dashboard:build`
<!-- A representative command that exercises the shipped behavior end-to-end.
     `/sdd dogfood` previews by default and runs only with --run, then logs under
     notes.md `## Dogfood log`. If no meaningful headless dogfood exists, replace
     the Dogfood line with: **Dogfood-Opt-Out:** <non-empty reason>. -->

**Human dogfood:** Open `/strategy/` and `/pt/strategy/`; confirm SWOT and pressure matrix are readable and do not imply benchmark scores.
<!-- Opt-in: a short walkthrough a human follows to approve the spec (demo steps,
     UI routes, things to eyeball). Name the steps here when human sign-off matters. -->

## Visual QA

_Optional for UI/interface/rendered-output work. Keep prose-based: real surface inspected, evidence captured, verdict recorded. If not useful, declare `**Visual QA Opt-Out:** <reason>`._

- [x] Evidence: `runs/strategy-swot-en-full.png`, `runs/strategy-swot-pt-mobile-full.png`
- [x] Verdict: Strategy page is readable on desktop and mobile; mobile pressure matrix uses cards instead of a cramped table.
