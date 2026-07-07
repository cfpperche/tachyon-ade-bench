# 001 — benchmark-mechanism

_Created 2026-07-07._

**Status:** shipped
**Closure:** Shipped the initial public benchmark repository scaffold with protocol docs, competitor profiles, schemas, a dependency-free harness, an external verifier model, and one smoke task.
<!-- Bare enum only: draft | in-progress | shipped | shipped-partial | superseded | abandoned | deferred.
     When this ships, add a **Closure:** line here recording what shipped (commit/evidence);
     `/sdd close` flags a shipped spec that still lacks one (alongside unchecked boxes,
     placeholders, and missing dogfood proof or opt-out). -->

## Intent

Tachyon needs a public, repeatable way to compare itself against direct ADE
competitors without relying on marketing claims or subjective impressions. The
first version should establish a separate benchmark repository, a documented
protocol, seed competitor profiles, a task fixture, and a harness that prepares
and verifies runs with product-independent artifacts.

Done means a reviewer can clone the repository, run a smoke check, prepare the
same task for any listed product, and inspect comparable run output.

## Acceptance criteria

- [x] **Scenario: Metadata check**
  - **Given** a fresh clone of the repository
  - **When** `python3 harness/bench.py check` runs
  - **Then** competitor profiles and task metadata are structurally validated
- [x] **Scenario: Run preparation**
  - **Given** product `tachyon` and task `T001-python-bugfix`
  - **When** `python3 harness/bench.py prepare --product tachyon --task T001-python-bugfix --run-id smoke` runs
  - **Then** `runs/smoke` contains a copied fixture worktree, prompt, task metadata, product metadata, and `result.json`
- [x] **Scenario: Independent verification**
  - **Given** a prepared run whose worktree has been fixed by a product under test
  - **When** `python3 harness/bench.py verify runs/<id>` runs
  - **Then** the verifier exits zero and stores stdout, stderr, git status, diff stat, final diff, and structured result metadata
- [x] The competitor roster includes Tachyon, Orca, HiveTerm, T3 Code, Hive, AgentsRoom, Augment Code, OpenADE, and Kandev.
- [x] LandingAI is documented as excluded because it is not a software-development ADE competitor.
- [x] The repository can be published publicly as `cfpperche/tachyon-ade-bench`.

## Non-goals

- It does not publish scored competitor results.
- It does not automate every competitor UI.
- It does not claim verified stack details for competitors before source review.
- It does not attempt hidden tests or LLM-as-judge scoring in v0.

## Open questions

- Which tasks should become the first public scored suite after the smoke task?
- Which competitor adapters can move from manual to CLI/API runners?
