# 010 — acquisition-manual-runner — tasks

_Generated from `plan.md` on 2026-07-07. Work top-to-bottom. Check boxes as tasks complete. If a task reveals the plan is wrong, update `plan.md` before continuing._

## Implementation

- [x] Implement `scripts/marketing/plan-scan.py`.
- [x] Add dry-run output and deterministic manifest writing.
- [x] Add generic-domain guardrails for GitHub repository aliases.
- [x] Document runner usage in acquisition docs and roadmap.
- [x] Exercise dry-run and write mode against a temporary output root.

## Verification

_Acceptance checks tied to `spec.md`. Each should map to a checklist item there._

- [x] `python3 scripts/marketing/plan-scan.py --scan-id 20260707T230000Z --platform google --platform meta --dry-run` prints planned rows.
- [x] `python3 scripts/marketing/plan-scan.py --scan-id 20260707T230000Z --platform google --platform meta --output-root /tmp/tachyon-ade-bench-scans` writes a valid manifest.
- [x] `python3 scripts/marketing/check-marketing.py` passes.
- [x] `scripts/check-suite.sh` passes.

**Headless check:** `python3 scripts/marketing/plan-scan.py --scan-id 20260707T230000Z --platform google --platform meta --dry-run && python3 scripts/marketing/check-marketing.py && scripts/check-suite.sh`
<!-- A mechanical command an agent can run to validate this spec's implementation
     without a human (tests / build / lint). Kept green = the spec stays delivered.
     To make `/sdd verify` re-run it, also declare it on a **Verify:** line, e.g.:
       **Verify:** `npm test`
     `/sdd verify` reads the FIRST backtick span per **Verify:** line, previews by
     default, and runs only with --run. Multiple **Verify:** lines run in order. -->

**Verify:** `python3 scripts/marketing/plan-scan.py --scan-id 20260707T230000Z --platform google --platform meta --dry-run`
**Verify:** `python3 scripts/marketing/check-marketing.py`
**Verify:** `scripts/check-suite.sh`

## Dogfood

**Dogfood:** `python3 scripts/marketing/plan-scan.py --scan-id 20260707T230000Z --platform google --platform meta --output-root /tmp/tachyon-ade-bench-scans`
<!-- A representative command that exercises the shipped behavior end-to-end.
     `/sdd dogfood` previews by default and runs only with --run, then logs under
     notes.md `## Dogfood log`. If no meaningful headless dogfood exists, replace
     the Dogfood line with: **Dogfood-Opt-Out:** <non-empty reason>. -->

**Human dogfood:** Inspect the generated manifest and confirm Kandev keeps repository context instead of collapsing to generic `github.com`.
<!-- Opt-in: a short walkthrough a human follows to approve the spec (demo steps,
     UI routes, things to eyeball). Name the steps here when human sign-off matters. -->

## Visual QA

_Optional for UI/interface/rendered-output work. Keep prose-based: real surface inspected, evidence captured, verdict recorded. If not useful, declare `**Visual QA Opt-Out:** <reason>`._

**Visual QA Opt-Out:** command-line planner only.
