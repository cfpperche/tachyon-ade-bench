# Tachyon capabilities

Human-readable view of the owned capability surface. The machine-readable SSOT
is [capabilities.json](./capabilities.json). Keep them in sync.

Each section maps to one ADE radar axis used by the bench dashboard.

Statuses used in YAML:

| Status | Meaning |
| --- | --- |
| `claimed` | Safe to mirror into the competitor profile as an owned claim |
| `placeholder` | Intended direction; not ready for public/profile claims |
| `not-claimed` | Explicitly out of profile claims for now |

---

## Agent support (`agent_support`)

What agent runtimes or roles Tachyon can drive.

**Claimed (owned):**

- Configured local agent runtimes
- Sub-agent workflows

**Not claimed yet:** public list of every supported vendor CLI, cloud-only
agents without local control, etc. Add only when product docs allow.

## Orchestration (`orchestration`)

How work is split, delegated, and closed.

**Claimed (owned):**

- Multi-agent delegation
- Review handoff
- Task-specific verification

## Workspace isolation (`workspace_isolation`)

How concurrent or delegated work stays separated.

**Claimed (owned):**

- Git worktree isolation
- Explicit owned path boundaries for delegated work

## Review and shipping (`review_shipping`)

How humans and systems accept or reject change.

**Claimed (owned):**

- Evidence records
- Verification logs
- Human-readable handoff and review flow

## Remote and mobile (`remote_mobile`)

**Not claimed** in the public competitor profile. Keep empty of marketing claims
until a product surface documents remote/mobile control.

## Context and memory (`context_memory`)

What persists across steps and agents.

**Claimed (owned):**

- Handoff context
- Task evidence
- Spec-driven development records when used

## Integrations (`integrations`)

How Tachyon attaches to host tools and repos.

**Claimed (owned):**

- Plugins
- Host action governance
- Repository-local verification commands

---

## How to extend

1. Add an item under the right key in `capabilities.json` with `status`.
2. Mirror the sentence here if it needs prose context.
3. Run `python3 scripts/product/check-capabilities.py`.
4. Sync the profile when you want the radar to reflect the change.
