# Tachyon overview

**Status:** owned draft surface for ADE Bench  
**Last aligned with profile:** 2026-07-15

## Positioning

Tachyon is an **Agentic Development Environment (ADE)** oriented around:

- multi-agent software work on real repositories
- **isolated worktrees** for delegated work
- **evidence and handoff** that survive agent sessions
- **verification gates** before accepting delivered change

In this repository Tachyon is the **owned reference product** under test. Public
homepage, source URL, license, and packaging are **not asserted** until a public
product surface exists.

## Product class

- Class: `A-local-ade` (local / multi-agent ADE, not enterprise document AI)
- Pricing model: depends on configured agent runtimes (not fixed in this repo)

## Audience

- Teams that care more about **auditable agent operations** than about the
  widest possible feature checklist
- Operators who want the same task to be **reproducible** under a harness
  (identical prompt, worktree, verifier)

## What “done” means for Tachyon work

A change is not done when an agent stops talking. It is done when:

1. the intended workspace contains the change,
2. required evidence/handoff is preserved,
3. an independent verification command can pass (bench or project gate).

## Related docs

- Capability surface: [capabilities.md](./capabilities.md) and
  [capabilities.json](./capabilities.json)
- Operating loops: [workflows.md](./workflows.md)
- Architecture sketch: [architecture.md](./architecture.md)
- Explicit non-claims: [limits-and-non-goals.md](./limits-and-non-goals.md)
