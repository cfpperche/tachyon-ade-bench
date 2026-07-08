# 011 — strategy-swot-dashboard

_Created 2026-07-08._

**Status:** shipped
**Closure:** Shipped bilingual Strategy/SWOT dashboard routes with Tachyon SWOT, derived competitive-pressure matrix, strategic bets, and responsive mobile cards.
<!-- Bare enum only: draft | in-progress | shipped | shipped-partial | superseded | abandoned | deferred.
     When this ships, add a **Closure:** line here recording what shipped (commit/evidence);
     `/sdd close` flags a shipped spec that still lacks one (alongside unchecked boxes,
     placeholders, and missing dogfood proof or opt-out). -->

## Intent

The dashboard has competitor profiles, acquisition intelligence, and benchmark protocol
surfaces, but it does not yet synthesize those inputs into an explicit strategic view for
Tachyon. Maintainers need a structured SWOT and competitive-pressure map so product,
benchmark, and acquisition work can point at the same strategic bets.

Done means the public dashboard includes a bilingual Strategy/SWOT page that makes the
Tachyon strategic position clear without inventing benchmark scores or unsupported product
claims.

## Acceptance criteria

_Observable outcomes. Given/When/Then scenarios for behavior; plain checkbox bullets for static facts. If every box can be ticked, the spec is delivered. Each criterion should be verifiable without re-reading the plan._

- [x] **Scenario: English strategy page**
  - **Given** the dashboard is built
  - **When** a user opens `/strategy/`
  - **Then** they see Tachyon SWOT, competitive pressure, and strategic bets in English
- [x] **Scenario: Portuguese strategy page**
  - **Given** the dashboard is built
  - **When** a user opens `/pt/strategy/`
  - **Then** they see the same strategic synthesis in Portuguese
- [x] **Scenario: evidence boundary**
  - **Given** no scored benchmark runs exist yet
  - **When** the strategy page presents opportunities and threats
  - **Then** it avoids ranking competitors as winners and frames claims as strategy derived from mapped evidence
- [x] The top navigation links to Strategy in both locales.
- [x] The competitive-pressure table includes the tracked competitors and highlights which axes pressure Tachyon.

## Non-goals

- Running benchmarks.
- Changing competitor profile facts.
- Adding scored leaderboards.
- Adding new acquisition scans.
- Making private Tachyon implementation claims.

## Open questions

- Whether SWOT should later be stored as JSON. Initial implementation can be static page data
  plus derived competitor pressure rows.
