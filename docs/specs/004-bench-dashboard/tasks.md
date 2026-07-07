# 004 — bench-dashboard — tasks

_Generated from `plan.md` on 2026-07-07. Work top-to-bottom. Check boxes as tasks complete. If a task reveals the plan is wrong, update `plan.md` before continuing._

## Implementation

- [x] Add root npm workspace scripts for the dashboard.
- [x] Scaffold Astro app under `apps/bench-dashboard`.
- [x] Implement typed data loaders for competitors and tasks.
- [x] Build overview, matrix, protocol, sources, and competitor detail pages.
- [x] Add React/ECharts islands for filters and charts.
- [x] Add responsive styling and view transitions.
- [x] Add GitHub Pages workflow.
- [x] Update README with local and Pages usage.
- [x] Run build/checks and visual QA.

## Verification

- [x] `python3 harness/bench.py check` passes.
- [x] `npm run dashboard:check` passes.
- [x] `npm run dashboard:build` passes.

**Headless check:** `npm run dashboard:build`
<!-- A mechanical command an agent can run to validate this spec's implementation
     without a human (tests / build / lint). Kept green = the spec stays delivered.
     To make `/sdd verify` re-run it, also declare it on a **Verify:** line, e.g.:
       **Verify:** `npm test`
     `/sdd verify` reads the FIRST backtick span per **Verify:** line, previews by
     default, and runs only with --run. Multiple **Verify:** lines run in order. -->

**Verify:** `python3 harness/bench.py check`
**Verify:** `npm run dashboard:check`
**Verify:** `npm run dashboard:build`

## Dogfood

**Dogfood:** `npm run dashboard:build`
<!-- A representative command that exercises the shipped behavior end-to-end.
     `/sdd dogfood` previews by default and runs only with --run, then logs under
     notes.md `## Dogfood log`. If no meaningful headless dogfood exists, replace
     the Dogfood line with: **Dogfood-Opt-Out:** <non-empty reason>. -->

**Human dogfood:** open the local dashboard, inspect overview, matrix, one competitor detail page, protocol, and sources at desktop and mobile widths.
<!-- Opt-in: a short walkthrough a human follows to approve the spec (demo steps,
     UI routes, things to eyeball). Name the steps here when human sign-off matters. -->

## Visual QA

- [x] Evidence: screenshots captured under `runs/visual-qa/` for overview desktop, matrix mobile, protocol desktop, Orca mobile detail, and sources desktop.
- [x] Verdict: dashboard is readable, responsive, charts render, matrix uses mobile cards, and no incoherent text overlap was observed.
