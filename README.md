# Tachyon ADE Bench

Tachyon ADE Bench is a reproducible benchmark harness for comparing Tachyon
against other Agentic Development Environments.

The repository starts with a conservative scope: prepare identical task
worktrees, capture comparable run artifacts, and verify the final result with
task-owned checks. It does not publish scored claims until every competitor run
has replayable evidence.

## Included products

The initial roster is limited to products that can reasonably compete with an
agentic software development environment:

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

LandingAI is intentionally excluded from the first benchmark roster because its
ADE product is Agentic Document Extraction, not an agentic software development
environment.

## Quickstart

Requirements: Python 3 and Git. The dashboard also requires Node.js 22+.

```sh
python3 harness/bench.py check
python3 harness/bench.py list-products
python3 harness/bench.py list-tasks
scripts/check-suite.sh

python3 harness/bench.py prepare --product tachyon --task T001-python-bugfix --run-id local-smoke

# Point the product under test at runs/local-smoke/worktree and give it
# runs/local-smoke/prompt.md.

python3 harness/bench.py verify runs/local-smoke
```

Every run writes a `result.json` plus collected artifacts under its run
directory. The verifier is independent of the product under test. Run reports
also include `metrics` for intervention burden, timing, cost slots, artifact
completeness, isolation, review burden, and failure recovery; see
`docs/run-report-metrics.md`.

## Dashboard

The public presentation app lives in `apps/bench-dashboard`. It renders the
structured competitor profiles from `competitors/*.json` as an Astro dashboard
with an overview, matrix, profile pages, charts, protocol view, and source
index.

```sh
npm install
npm run dashboard:dev
npm run dashboard:check
npm run dashboard:build
```

GitHub Pages deployment is defined in `.github/workflows/pages.yml`. Enable
Pages in repository settings with source "GitHub Actions"; pushes to `main`
will publish the dashboard at:

```text
https://cfpperche.github.io/tachyon-ade-bench/
https://cfpperche.github.io/tachyon-ade-bench/pt/
```

## Repository layout

```text
competitors/   Seed profiles for products under test
apps/          Static dashboard and presentation surfaces
docs/product/  Owned canonical Tachyon product surface (SSOT)
docs/specs/    Spec-driven development records for benchmark changes
harness/       Local reproducibility tooling
marketing/     Acquisition-intelligence registries, scans, and summaries
reports/       Human-readable benchmark summaries
runs/          Ignored local run outputs
schemas/       JSON schemas for tracked benchmark documents
scripts/product/  Validate/sync Tachyon capabilities SSOT
tasks/         Versioned benchmark tasks and fixtures
```

Research docs:

- `docs/product/` is the owned canonical Tachyon product surface
  (`capabilities.json` SSOT; sync into `competitors/tachyon.json` via
  `scripts/product/sync-tachyon-profile.py`).
- `docs/competitor-intelligence.md` covers stack, infrastructure, features,
  moat hypotheses, and benchmark caveats.
- `docs/acquisition-intelligence.md` covers paid channels, launch surfaces,
  sponsorships, newsletters, podcasts, and other marketing/distribution
  signals.
- `docs/competitive-intelligence.md` maps SaaS-style CI workflows into
  repo-native battlecards, digital imports, source intelligence, pricing watch,
  and reproducible collectors.
- `docs/run-report-metrics.md` defines the run-level indicators required before
  any scored leaderboard.

Tachyon product surface checks:

```sh
python3 scripts/product/check-capabilities.py
python3 scripts/product/sync-tachyon-profile.py
python3 harness/bench.py check
```

Marketing acquisition checks:

```sh
python3 scripts/marketing/check-marketing.py
python3 scripts/intelligence/check-intelligence.py
python3 scripts/marketing/summarize-history.py --check
scripts/marketing/new-scan.py --help
scripts/marketing/add-manual-ad.py --help
scripts/intelligence/add-signal.py --help
```

## Benchmark principles

- Same starting repo, prompt, model constraints, and time budget per comparable
  run.
- Product claims are not accepted as evidence. The harness collects diffs,
  verification output, timestamps, and run metadata.
- Manual products are allowed, but manual intervention must be counted.
- Raw measurements stay visible even when a summary score is introduced.
- Competitor profile claims must remain sourced or marked as needing
  verification.

## Status

Alpha. The first commit establishes the protocol, schemas, seed competitors,
one fixture task, and a local harness. It is not a scored public benchmark yet.
