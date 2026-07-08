# 012 — run-report-metrics

_Created 2026-07-08._

**Status:** shipped
**Closure:** Shipped the run report metrics contract in schema, harness, and documentation. Verification and dogfood evidence are recorded in `notes.md`.
<!-- Bare enum only: draft | in-progress | shipped | shipped-partial | superseded | abandoned | deferred.
     When this ships, add a **Closure:** line here recording what shipped (commit/evidence);
     `/sdd close` flags a shipped spec that still lacks one (alongside unchecked boxes,
     placeholders, and missing dogfood proof or opt-out). -->

## Intent

Benchmark results should not collapse to pass/fail. For ADEs, a run that passes
after heavy human steering is strategically different from a run that reaches a
verified change with low intervention. The repository already has a
`run-result.schema.json`, but it only has a coarse `human_interventions` field
and does not encode the intervention burden, elapsed-to-verification, artifact
completeness, isolation, review burden, cost, or recovery indicators needed
before publishing a leaderboard.

Done means new run reports have explicit metric slots for intervention burden
and time-to-verified-change, the schema documents the contract, and the harness
initializes/verifies those fields consistently.

## Acceptance criteria

_Observable outcomes. Given/When/Then scenarios for behavior; plain checkbox bullets for static facts. If every box can be ticked, the spec is delivered. Each criterion should be verifiable without re-reading the plan._

- [x] **Scenario: prepared run metrics**
  - **Given** a maintainer prepares a run with `harness/bench.py prepare`
  - **When** `result.json` is written
  - **Then** it includes initialized `metrics` sections for intervention burden, timing, cost, artifacts, isolation, review, and recovery
- [x] **Scenario: verified timing**
  - **Given** a prepared run is verified
  - **When** `harness/bench.py verify` updates `result.json`
  - **Then** `metrics.timing.time_to_verified_change_seconds` is populated from run creation to verification end
- [x] **Scenario: intervention detail**
  - **Given** no human intervention has been recorded yet
  - **When** the run report is created
  - **Then** intervention count and minutes default to zero while detailed intervention events remain an empty list
- [x] The schema names the core metrics and constrains their basic types.
- [x] Documentation explains why these metrics are required before scoring.

## Non-goals

- Building a leaderboard.
- Auto-detecting every human intervention from external tools.
- Pricing model tokens/costs automatically.
- Changing benchmark task fixtures.

## Open questions

- Later work should decide whether interventions are recorded by CLI subcommand,
  UI event log, or imported product telemetry.
