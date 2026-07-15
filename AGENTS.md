# Agent context — Tachyon ADE Bench

This repository is **Tachyon ADE Bench**: a reproducible harness and competitor-intelligence surface for comparing Tachyon against other Agentic Development Environments (ADEs).

Agents working here must follow the boundaries below without re-asking.

## Repository map (this machine)

| Path | Role | Write? |
| --- | --- | --- |
| `/home/goat/tachyon-ade-bench` (this repo) | Benchmark harness, competitor profiles, dashboard, marketing/intelligence | **Yes** (when the task requires it) |
| `/home/goat/tachyon` | **Tachyon product** (VS Code extension monorepo) | **No — read only** |
| `git@github.com:cfpperche/tachyon.git` | Product remote | **No writes, no PRs, no pushes** |
| `git@github.com:cfpperche/tachyon-ade-bench.git` | Bench remote | OK when the user asks to commit/push |

Also acceptable for **read-only** product research:

- Local clone: `~/tachyon`
- GitHub: `cfpperche/tachyon` (fetch/browse only)
- Public product site if published: check `~/tachyon/README.md` (Marketplace / site links)

## Hard rule: product repo is read-only

**You may read** `~/tachyon` (and its GitHub remote) to learn real product capabilities, architecture, docs, `tachyon.yml`, CHANGELOG, etc.

**You must not:**

- edit, create, or delete files under `~/tachyon`
- run `git commit`, `git push`, `gh pr create`, amend history, or change remotes in that repo
- install hooks, rewrite config, or “fix” things in place inside the product tree
- treat product `node_modules`/build as a write playground

If product-facing claims need to land somewhere agents **can** write, use **this** repo:

1. Update `docs/product/` (especially `docs/product/capabilities.json`)
2. Run `python3 scripts/product/sync-tachyon-profile.py`
3. Run `python3 harness/bench.py check`
4. Optionally refresh `competitors/tachyon.json` notes/sources

Never invent Tachyon features only inside the competitor JSON to look better on charts.

## What this bench repo is for

- Fair ADE comparison protocol (`SPEC.md`, `harness/`, `tasks/`)
- Competitor research profiles (`competitors/*.json`) — structured data, not scores
- Dashboard presentation (`apps/bench-dashboard`)
- Acquisition / battlecard intelligence (`marketing/`, `intelligence/`)
- Owned Tachyon product surface **mirror** for the bench (`docs/product/`)

It is **not** the Tachyon product source of truth. The product lives in `~/tachyon`.

## Canonical sources hierarchy (Tachyon claims)

```text
~/tachyon  (product, READ ONLY)
    →  docs/product/  (bench-owned mirror you may edit)
    →  competitors/tachyon.json  (derived roster profile)
    →  dashboard radar / matrix
```

- `docs/product/capabilities.json` = machine-readable SSOT **inside the bench**
- Prefer aligning that SSOT with real product docs/code from `~/tachyon` when enriching claims
- `runs/` = measured evidence only (gitignored); not a substitute for product docs

## Competitor profiles

- Source of truth for roster claims: `competitors/*.json`
- Rules: `docs/competitor-intelligence.md`, `competitors/README.md`
- Schema: `schemas/competitor.schema.json`
- Map: `reports/competitor-map-v0.1.md`
- Validate: `python3 harness/bench.py check`

**Class A** = local/multi-agent ADE peers (Orca, Herdr, Hive, Fusion, Maestri, …).  
**Class B** = enterprise platforms (e.g. Augment) — report separately.  
**Excluded example:** LandingAI-style document ADE (not software ADE).

Update workflow is **manual / on-demand** (no required cron job): re-check official sources, edit JSON, bump `last_reviewed` / `updated_at`, run `bench.py check`, update the map when comparison language changes.

## Dashboard charts (do not over-claim)

Capability Radar and Positioning Map scores are **heuristics from profile text/feature lists**, not harness results:

- Radar: roughly `min(100, feature_list_length × 12.5)` per feature group
- Positioning: keyword local-first score × orchestration list formula
- Real product quality lives in `runs/` + verifiers, not the radar polygon

Tachyon can look “weaker” on the radar when `competitors/tachyon.json` is intentionally sparse. Fix by enriching `docs/product/` from **read-only** product research, then sync — not by fabricating bullets.

## Harness basics

```sh
python3 harness/bench.py check
python3 harness/bench.py list-products
python3 harness/bench.py list-tasks
python3 harness/bench.py prepare --product <id> --task <task-id> --run-id <run-id>
# product works only in runs/<run-id>/worktree with prompt.md
python3 harness/bench.py verify runs/<run-id>
```

- Same prompt/fixture for comparable products
- Count human interventions
- Product marketing claims are not evidence

## Product surface scripts (bench repo)

```sh
python3 scripts/product/check-capabilities.py
python3 scripts/product/sync-tachyon-profile.py
python3 harness/bench.py check
```

## Useful paths

| Path | Content |
| --- | --- |
| `docs/product/` | Owned Tachyon surface for the bench |
| `docs/competitor-intelligence.md` | How to update competitor JSON |
| `docs/competitive-intelligence.md` | Battlecards / signals |
| `docs/acquisition-intelligence.md` | Marketing/acquisition |
| `docs/run-report-metrics.md` | Run metrics contract |
| `intelligence/current/signals.json` | Competitive signals |
| `marketing/registry/advertisers.json` | Acquisition advertiser aliases |

## Git / publish discipline (this repo)

- Prefer reversible local edits; confirm before force-push, history rewrite, or shared destructive ops
- `runs/*` is gitignored — keep smoke evidence local unless the user asks otherwise
- Commit/push only when the user asks

## Language

Respond in the user’s language when they write in Portuguese or English. Keep code/identifiers as in the repo.
