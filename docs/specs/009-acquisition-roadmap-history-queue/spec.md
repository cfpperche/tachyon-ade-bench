# 009 — acquisition-roadmap-history-queue

_Created 2026-07-07._

**Status:** shipped
**Closure:** Shipped `docs/acquisition-roadmap.md` plus derived Scan History and Review Queue sections on the bilingual Acquisition Intelligence board.
<!-- Bare enum only: draft | in-progress | shipped | shipped-partial | superseded | abandoned | deferred.
     When this ships, add a **Closure:** line here recording what shipped (commit/evidence);
     `/sdd close` flags a shipped spec that still lacks one (alongside unchecked boxes,
     placeholders, and missing dogfood proof or opt-out). -->

## Intent

The Acquisition Intelligence board now exposes the latest persisted state, but the project
still needs a documented roadmap for turning it into a repeatable acquisition-monitoring
system. The next useful product increment is to show scan history and a review queue so the
team can decide what to verify next instead of treating the latest snapshot as the whole
system.

Done means the roadmap is documented in `docs/`, and the dashboard starts the roadmap by
showing historical scan summaries plus a review queue derived from partial, blocked, or
ambiguous scan results.

## Acceptance criteria

_Observable outcomes. Given/When/Then scenarios for behavior; plain checkbox bullets for static facts. If every box can be ticked, the spec is delivered. Each criterion should be verifiable without re-reading the plan._

- [x] **Scenario: Roadmap is durable**
  - **Given** a maintainer opens the repository documentation
  - **When** they read the acquisition roadmap
  - **Then** they can see phases, deliverables, acceptance signals, and sequencing for acquisition intelligence
- [x] **Scenario: Scan history**
  - **Given** multiple scan manifests exist under `marketing/scans`
  - **When** a user opens `/acquisition/`
  - **Then** the board shows a scan-history section with per-scan query/status totals and timestamps
- [x] **Scenario: Review queue**
  - **Given** the latest scan contains partial or ambiguous coverage rows
  - **When** a user opens `/acquisition/`
  - **Then** the board lists next review items with product, platform, query, reason, and source link
- [x] **Scenario: Bilingual parity**
  - **Given** the English and Portuguese dashboard routes exist
  - **When** `/acquisition/` and `/pt/acquisition/` are built
  - **Then** both routes expose the new history and review sections with localized labels

## Non-goals

- Running new acquisition scans.
- Adding GitHub Actions cadence.
- Building API-key integrations.
- Adding interactive client-side filters.
- Reclassifying existing partial results as not-found.

## Open questions

- Exact SLA/cadence for recurring scans remains a later roadmap phase.
