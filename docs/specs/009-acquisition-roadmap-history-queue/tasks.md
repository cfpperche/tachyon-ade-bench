# 009 — acquisition-roadmap-history-queue — tasks

_Generated from `plan.md` on 2026-07-07. Work top-to-bottom. Check boxes as tasks complete. If a task reveals the plan is wrong, update `plan.md` before continuing._

## Implementation

- [x] Add the acquisition roadmap document.
- [x] Add scan-history and review-queue types.
- [x] Derive scan-history rows from all manifests.
- [x] Derive review-queue rows from latest non-final/ambiguous results.
- [x] Render history and review sections on the acquisition board.
- [x] Localize new labels in EN/PT.
- [x] Add responsive styles for the new sections.

## Verification

_Acceptance checks tied to `spec.md`. Each should map to a checklist item there._

- [x] `npm run dashboard:check` passes.
- [x] `npm run dashboard:build` passes.
- [x] `scripts/check-suite.sh` passes.
- [x] Screenshots show the new sections on desktop/mobile.

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

**Human dogfood:** Open `/acquisition/` and `/pt/acquisition/`; confirm Scan History and
Review Queue are visible, useful, and do not imply partial equals absence.
<!-- Opt-in: a short walkthrough a human follows to approve the spec (demo steps,
     UI routes, things to eyeball). Name the steps here when human sign-off matters. -->

## Visual QA

_Optional for UI/interface/rendered-output work. Keep prose-based: real surface inspected, evidence captured, verdict recorded. If not useful, declare `**Visual QA Opt-Out:** <reason>`._

- [x] Evidence: `runs/acquisition-roadmap-history-en-full.png`, `runs/acquisition-roadmap-history-pt-mobile-full.png`
- [x] Verdict: Scan History and Review Queue render on desktop and mobile without incoherent overlap.
