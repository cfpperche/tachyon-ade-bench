# 010 — acquisition-manual-runner

_Created 2026-07-07._

**Status:** shipped
**Closure:** Shipped `scripts/marketing/plan-scan.py`, `npm run acquisition:plan`, docs for Phase 2 usage, and generic-domain guardrails for repository aliases.
<!-- Bare enum only: draft | in-progress | shipped | shipped-partial | superseded | abandoned | deferred.
     When this ships, add a **Closure:** line here recording what shipped (commit/evidence);
     `/sdd close` flags a shipped spec that still lacks one (alongside unchecked boxes,
     placeholders, and missing dogfood proof or opt-out). -->

## Intent

Phase 2 of the acquisition roadmap needs a reproducible manual runner: one
command should create a complete scan manifest for tracked products and selected
platforms, using registry aliases and deterministic source URLs. The runner
should not pretend to have queried ad libraries; it prepares reviewable rows and
keeps ambiguous cases such as generic GitHub domains explicit.

Done means maintainers can run a script to generate a timestamped manifest for
all included advertisers across selected platforms, then use the existing board
and review queue to drive assisted verification.

## Acceptance criteria

_Observable outcomes. Given/When/Then scenarios for behavior; plain checkbox bullets for static facts. If every box can be ticked, the spec is delivered. Each criterion should be verifiable without re-reading the plan._

- [x] **Scenario: complete planned scan**
  - **Given** the marketing registries are present
  - **When** a maintainer runs the scan planner for primary platforms
  - **Then** it writes one manifest with deterministic query rows for all included advertisers
- [x] **Scenario: dry run**
  - **Given** a maintainer wants to inspect planned work without writing files
  - **When** they run the planner with `--dry-run`
  - **Then** it prints the rows that would be created and leaves the worktree unchanged
- [x] **Scenario: generic-domain guardrail**
  - **Given** an advertiser alias uses a generic host such as `github.com/kdlbs/kandev`
  - **When** the planner emits Google domain rows
  - **Then** it marks the row `partial` with the specific repository path as query context rather than attributing generic `github.com`
- [x] The roadmap documents the runner command as the start of Phase 2.

## Non-goals

- Calling live ad-library APIs.
- Taking browser screenshots.
- Promoting any planned row to `found`.
- Replacing manual evidence review.

## Open questions

- Later phases can decide whether planned rows should use a separate result state; for now
  they use existing `partial`/`blocked` manifest states.
