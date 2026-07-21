# 016 — jetbrains-air-smoke

_Created 2026-07-21._

**Status:** deferred
**Closure:** Deferred before product execution because this Linux host has neither JetBrains Toolbox nor Air installed, JetBrains documents no silent Linux Toolbox installation, and the Air/guest-agent flow requires interactive authentication. No run was fabricated and readiness remains `needs-install`.

## Intent

Qualify JetBrains Air for manual benchmarking by completing a real T001 run in
the harness-owned worktree and preserving the exact Air, agent, model,
authentication, permission, intervention, and verification evidence.

## Acceptance criteria

- [ ] JetBrains Air is installed from the official Linux Toolbox channel and its exact version is recorded.
- [ ] A supported guest agent is authenticated and its model/effort/subscription path is recorded.
- [ ] Air opens only the prepared `runs/<run-id>/worktree` in Local Workspace mode.
- [ ] The exact T001 `prompt.md` is supplied without corrective context.
- [ ] Human interventions and permission approvals are counted.
- [ ] `python3 harness/bench.py verify runs/<run-id>` passes with complete artifacts and run metadata.
- [ ] `competitors/jetbrains-air.json` moves to `manual-ready` only after all gates pass.

## Non-goals

- Using an Air-created worktree outside the harness run directory.
- Exercising Docker on Linux, where the reviewed release does not support it.
- Treating a failed or interrupted setup as a scored result.
- Publishing ignored run artifacts without an explicit decision.

## Resume condition

Resume when JetBrains Toolbox and Air are interactively installed on this host
and a supported Air/guest-agent authentication path is available.
