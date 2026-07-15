# Tachyon architecture (owned sketch)

**Status:** owned, intentionally non-private  
**Purpose:** orient maintainers and benchmark operators without publishing
internal implementation secrets.

## Principles

1. **Repo-local truth** — the working tree (or owned worktree) is the unit of
   change under test.
2. **Isolation before parallelism** — delegated agent work should not silently
   collide with other tasks.
3. **Evidence over chat** — durable artifacts (diffs, logs, handoff records)
   matter more than transcript length.
4. **Independent verification** — acceptance uses a gate outside the agent’s
   self-report (project command or bench verifier).
5. **Governed host power** — plugins and host actions are capability surfaces
   that need explicit policy, not unbounded shell freedom as the product story.

## Logical components (product-level)

These names are conceptual for docs/bench alignment. Map them to real packages
only when public or owned product docs allow.

| Component | Responsibility |
| --- | --- |
| Operator surface | How a human starts/steers work (CLI, app, or other — TBD public) |
| Agent runtime adapters | Configured local agents / sub-agents |
| Workspace manager | Worktrees, path boundaries, isolation |
| Orchestration | Delegation, handoff, multi-step task flow |
| Evidence store | Handoff records, verification logs, review artifacts |
| Verification gate | Runs project/bench checks before “done” |
| Plugin / host-action layer | Controlled extensions into the host environment |

## Data the bench is allowed to see

Aligned with the owned competitor profile:

- prepared worktree state
- run metadata (`result.json` and friends)
- handoff / evidence records when produced
- verification command output

## Explicit gaps

- Public homepage, source repo, license, and packaging: **not asserted**
- Internal package graph, languages, and deploy topology: **owned/internal**
  until published elsewhere

Update this file when product architecture becomes publicly citable; prefer
linking to the product monorepo docs over duplicating secrets here.
