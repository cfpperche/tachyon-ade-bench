# 003 — competitor-intel

_Created 2026-07-07._

**Status:** shipped
**Closure:** Shipped competitor research schema, validation, enriched profiles, maintainer docs, and v0.1 map. Evidence: `python3 harness/bench.py check`, `scripts/check-suite.sh`, and `scripts/smoke.sh` pass locally on 2026-07-07.
<!-- Bare enum only: draft | in-progress | shipped | shipped-partial | superseded | abandoned | deferred.
     When this ships, add a **Closure:** line here recording what shipped (commit/evidence);
     `/sdd close` flags a shipped spec that still lacks one (alongside unchecked boxes,
     placeholders, and missing dogfood proof or opt-out). -->

## Intent

Before running benchmarks against competitors, the repository needs an auditable
competitor intelligence layer. The current profiles are seed placeholders; they
do not consistently record sources, stack signals, infrastructure model,
feature surface, moat hypotheses, or benchmarking caveats.

This spec adds a structured mechanism for competitor research and populates the
initial direct-competitor roster from official sources. Done means each product
profile can be used to decide how to install, run, and fairly compare the
product without relying on memory or unsourced claims.

## Acceptance criteria

- [x] **Scenario: Competitor metadata validation**
  - **Given** the enriched competitor profiles
  - **When** `python3 harness/bench.py check` runs
  - **Then** every competitor has research sources, stack notes, feature groups, moat notes, and benchmarking readiness
- [x] **Scenario: Research documentation**
  - **Given** a maintainer wants to update a competitor profile
  - **When** they read `docs/competitor-intelligence.md`
  - **Then** they can see the required fields, source rules, confidence levels, and update workflow
- [x] **Scenario: Comparison report**
  - **Given** the seeded research data
  - **When** a maintainer opens `reports/competitor-map-v0.1.md`
  - **Then** they see a concise stack/infra/features/moat matrix with source links and benchmark caveats
- [x] The initial roster covers Tachyon, Orca, HiveTerm, T3 Code, Hive, AgentsRoom, Augment Code, OpenADE, and Kandev.
- [x] LandingAI remains excluded from software ADE competitor research.

## Non-goals

- It does not run benchmark tasks against competitors.
- It does not claim private implementation details for closed-source products.
- It does not scrape non-official commentary as fact.
- It does not assign final scores or ranking.
- It does not resolve every unknown stack detail in v0.1.

## Open questions

- Which direct competitor should get the first full manual benchmark run after research: Orca, Kandev, or Hive?
- Should future reports include screenshots or only source-linked text evidence?
