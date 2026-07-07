# 005 — dashboard-i18n — tasks

_Generated from `plan.md` on 2026-07-07. Work top-to-bottom. Check boxes as tasks complete. If a task reveals the plan is wrong, update `plan.md` before continuing._

## Implementation

- [x] Add shared locale dictionaries and locale-aware route helpers.
- [x] Localize the dashboard shell, badges, charts, protocol diagram, and matrix.
- [x] Wire English pages to the shared dictionary while preserving default routes.
- [x] Add mirrored Portuguese pages under `/pt/`.
- [x] Document the public English and Portuguese dashboard URLs.

## Verification

- [x] Astro type/content check passes.
- [x] Static build emits English and Portuguese route trees.
- [x] Repository benchmark/schema checks still pass.

**Headless check:** `npm run dashboard:check && npm run dashboard:build && python3 harness/bench.py check`
**Verify:** `npm run dashboard:check`
**Verify:** `npm run dashboard:build`
**Verify:** `python3 harness/bench.py check`

## Dogfood

**Dogfood:** `npm run dashboard:build`

**Human dogfood:** Open `/tachyon-ade-bench/`, `/tachyon-ade-bench/pt/`, and `/tachyon-ade-bench/pt/matrix/`; verify the language switch and localized labels.

## Visual QA

- [x] Evidence: `runs/visual-qa/005-dashboard-i18n/en-root.png`, `pt-root.png`, `pt-matrix.png`, `pt-profile.png`, `pt-root-mobile.png`, and `pt-matrix-mobile.png`.
- [x] Verdict: English default and Portuguese `/pt/` pages render with localized navigation, controls, headings, and badges; desktop and mobile layouts have no observed text collisions.
