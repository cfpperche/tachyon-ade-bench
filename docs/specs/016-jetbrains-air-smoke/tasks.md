# 016 — jetbrains-air-smoke — tasks

_Generated from `plan.md` on 2026-07-21. Resume only when the interactive prerequisite in `spec.md` is satisfied._

## Setup

- [ ] Install JetBrains Toolbox and Air through the official Linux UI flow.
- [ ] Authenticate Air and one supported guest agent.
- [ ] Record Air, agent, model, effort, subscription, permission mode, OS, and network policy.

## Run

- [ ] Prepare T001 with product `jetbrains-air`.
- [ ] Open only the generated worktree as Local Workspace.
- [ ] Supply the exact prompt and count all intervention/approvals.
- [ ] Run the canonical verifier and complete `result.json` metadata.
- [ ] Update profile readiness and source notes only if qualification passes.

## Verification

**Verify:** `python3 harness/bench.py check`

## Dogfood

**Dogfood-Opt-Out:** Deferred until the required interactive desktop installation and authentication are available.

## Visual QA

**Visual QA Opt-Out:** This spec qualifies runtime behavior; the catalog UI was validated under spec 015.
