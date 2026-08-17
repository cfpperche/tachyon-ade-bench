# Competitor Intelligence

This repository keeps competitor research as structured data first. The JSON
profiles in `competitors/` are the source of truth; reports should summarize
that data instead of becoming the only place where claims live.

**Operational playbook** (add / update / exclude / publish site):
[`docs/competitor-runbook.md`](./competitor-runbook.md).

**Near-term roadmap** (catalog closeout, runtime model, harness evidence):
[`docs/bench-roadmap.md`](./bench-roadmap.md).

## Scope

The v0.1 roster covers software Agentic Development Environment competitors:

- Tachyon
- Orca
- Herdr
- HiveTerm
- T3 Code
- Hive
- AgentsRoom
- Augment Code
- OpenADE / ADE App
- Kandev
- Fusion (Runfusion)
- Maestri
- JetBrains Air
- Conductor
- Warp
- Kiro
- Overclock
- Synara
- Falou (OpusBR)
- Xirp
- Emdash
- GitHub Copilot app
- Compozy (CompozyOS)
- Paseo

LandingAI is intentionally excluded from this roster. Its ADE product is
Agentic Document Extraction, not an agentic software development environment.

Macro (https://macro.com/) is intentionally excluded. It is an open-source
agentic office suite / company OS (email, chat, docs, tasks, CRM, agents) with
GitHub task/PR linking and MCP for coding agents—not a software multi-agent ADE
control plane with worktree/coding-CLI orchestration as the core product.

Note: Falou’s HTML meta still emphasizes Mac voice dictation, but the official
SPA product body (Agent Board, Squads, Claude Code/Codex from the notch) is a
software multi-agent ADE control plane—cataloged as Class A, not excluded.

## Source Rules

Use official or owned sources for factual claims:

- `official-site`: product pages controlled by the vendor/project.
- `official-docs`: vendor/project documentation.
- `source-repo`: upstream GitHub/GitLab repository files and READMEs.
- `package-manifest`: package metadata such as `package.json`.
- `app-store`: official app store listing.
- `owned`: Tachyon-owned evidence or documentation.

Do not use community posts, launch comments, social posts, or search snippets as
facts. They can be leads, but the recorded claim must point to an official
source. If an implementation detail is not published, record it as unknown.

Open-source peers can also be inspected from checkout. That path is
`docs/inspect-harness.md` (`list-inspectable`, static detectors, then
Claude Code / Codex / Grok Build on the same prompt). Detector hits are
**not** copied into `research.features` without a human review.

## Runtime model

Every competitor profile must declare top-level `runtime_model`: who owns the
**coding agent loop** (tools/edits/shell), not the ADE chrome.

| Value | Meaning |
| --- | --- |
| `guest-cli` | Product is a control plane / OS / cockpit; coding runs in third-party CLIs (Claude Code, Codex, Grok Build, …). |
| `hybrid` | Product ships a first-party coding agent **and** supports third-party CLIs. |
| `first-party` | Primary coding path is the product's own agent runtime (plan/account). |
| `unknown` | Insufficient official evidence (avoid for roster peers). |

Optional companion fields:

- `guest_runtimes[]` — short stable ids (`claude-code`, `codex`, …)
- `own_runtimes[]` — short stable ids (`warp-agent`, `kiro-agent`, …)
- `runtime_model_notes` — one-line nuance (e.g. Conductor “first-party support” is still `guest-cli`)

Do **not** confuse with `class` (A/B) or benchmark readiness. Single-task
correctness often measures the guest agent more than the ADE when
`runtime_model` is `guest-cli`.

## Confidence Levels

- `owned`: Tachyon-owned reference data. Public reports should still avoid
  private implementation details unless a public source exists.
- `official-sourced`: factual claims are backed by official sources reviewed in
  the current pass.
- `partial-official`: core product claims are official, but some stack,
  platform, or pricing details remain unpublished or unverified.
- `seed`: placeholder data only. Do not publish public comparisons from seed
  profiles.

## Required Research Fields

Every competitor profile must include `research`:

- `last_reviewed`: date the sources were checked.
- `confidence`: one of the confidence levels above.
- `sources`: source list with URL, source kind, and what the source supports.
- `positioning`: short description of what the product is trying to be.
- `stack`: runtime, frontend, backend, packaging, data, and unknowns.
- `infrastructure`: how the product runs and where code/state lives.
- `features`: grouped capability surface.
- `benchmarking`: readiness, install surface, parity risks, and first tasks.
- `moat`: hypotheses, evidence, and unknowns.

Keep the top-level fields useful for quick listing, but put detailed research
inside `research`.

## Update Workflow

Short form (research edit). For the full path including advertisers, roster
lists, and GitHub Pages publish, use `docs/competitor-runbook.md`.

1. Open the official sources and verify they still say what the profile claims.
2. Edit the profile JSON and keep factual claims separate from hypotheses.
3. Move unverifiable details to `unknowns`; do not infer private architecture.
4. Update `research.last_reviewed`, `research.confidence`, `research_status`,
   and `updated_at`.
5. Run `python3 harness/bench.py check` (and marketing/dashboard checks if
   adding a product or before expecting the public site to update).
6. If the change affects comparison language, update
   `reports/competitor-map-v0.1.md`.

### Tachyon special case

Agents may **read** the product monorepo at `~/tachyon` (or `cfpperche/tachyon`
on GitHub) for grounding. They must **not write** to that repository. Durable
rules live in root `AGENTS.md` and `CLAUDE.md`.

For bench-visible claims, write the owned product surface in this repo:

- `docs/product/` (Markdown)
- `docs/product/capabilities.json` (SSOT for radar axes)

Do not invent Tachyon features only inside `competitors/tachyon.json`. Prefer:

```sh
# optional: read ~/tachyon for real capabilities (read only)
# then edit docs/product/capabilities.json and docs
python3 scripts/product/check-capabilities.py
python3 scripts/product/sync-tachyon-profile.py
python3 harness/bench.py check
```

Hierarchy: product repo (read) → `docs/product/` (write) →
`competitors/tachyon.json` (derived) → dashboard.

## Benchmark Readiness

Use `research.benchmarking.readiness` consistently:

- `manual-ready`: can be benchmarked manually with the current harness.
- `needs-install`: likely benchmarkable, but install/runtime path must be
  exercised before scoring.
- `enterprise-gated`: requires account, billing, enterprise setup, or hosted
  configuration that changes parity.
- `owned-reference`: Tachyon reference profile.
- `research-only`: keep in research docs but do not run as a software ADE
  competitor.

Class A products are direct local or multi-agent ADE competitors. Class B
products can be measured with the same artifact contract, but reports must not
mix them into a Class A leaderboard without caveats.

## Report Hygiene

Reports must state whether they are research-only or scored. A research map can
compare stack, infrastructure, features, and moat hypotheses. A scored benchmark
requires reproducible run artifacts, task verifier output, product/version
metadata, model/subscription notes, and human intervention counts.

## Acquisition Intelligence

Marketing and distribution signals live in
`docs/acquisition-intelligence.md`. Keep those records separate from technical
competitor facts: ad creative, launch channels, sponsorships, and newsletter or
podcast placements can explain positioning and go-to-market strategy, but they
are not benchmark evidence.

## Battlecards and Competitive Signals

Battlecards, pricing-watch records, market observations, and imported
third-party intelligence live in `docs/competitive-intelligence.md` and
`intelligence/current/signals.json`. Use them to summarize positioning,
objections, freshness, confidence, and Tachyon responses without bloating
`competitors/*.json` with sales-facing analysis.
