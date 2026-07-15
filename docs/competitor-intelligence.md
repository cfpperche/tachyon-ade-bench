# Competitor Intelligence

This repository keeps competitor research as structured data first. The JSON
profiles in `competitors/` are the source of truth; reports should summarize
that data instead of becoming the only place where claims live.

## Scope

The v0.1 roster covers software Agentic Development Environment competitors:

- Tachyon
- Orca
- HiveTerm
- T3 Code
- Hive
- AgentsRoom
- Augment Code
- OpenADE / ADE App
- Kandev
- Fusion (Runfusion)
- Maestri

LandingAI is intentionally excluded from this roster. Its ADE product is
Agentic Document Extraction, not an agentic software development environment.

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

1. Open the official sources and verify they still say what the profile claims.
2. Edit the profile JSON and keep factual claims separate from hypotheses.
3. Move unverifiable details to `unknowns`; do not infer private architecture.
4. Update `research.last_reviewed`, `research.confidence`, `research_status`,
   and `updated_at`.
5. Run `python3 harness/bench.py check`.
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
