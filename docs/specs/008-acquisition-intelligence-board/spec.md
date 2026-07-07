# 008 — acquisition-intelligence-board

_Created 2026-07-07._

**Status:** shipped
**Closure:** Shipped the bilingual Acquisition Intelligence board with static Astro routes,
typed marketing-data loaders, navigation entries, responsive styles, and visual evidence.
<!-- Bare enum only: draft | in-progress | shipped | shipped-partial | superseded | abandoned | deferred.
     When this ships, add a **Closure:** line here recording what shipped (commit/evidence);
     `/sdd close` flags a shipped spec that still lacks one (alongside unchecked boxes,
     placeholders, and missing dogfood proof or opt-out). -->

## Intent

The repository already persists acquisition-intelligence data under `marketing/current`,
`marketing/history`, and `marketing/scans`, but the public dashboard does not expose that
layer as a structured decision surface. Users can see competitor profiles and benchmark
readiness, but cannot quickly answer which competitors have observed ads, which platforms
were scanned, what evidence exists, and which results are only partial.

Done means the Astro dashboard has a first-class Acquisition Intelligence board in English
and Portuguese. The board renders tracked coverage, campaigns, representative ads, evidence
links, and scan limitations from the persisted JSON data without presenting partial scans as
proof of absence.

## Acceptance criteria

_Observable outcomes. Given/When/Then scenarios for behavior; plain checkbox bullets for static facts. If every box can be ticked, the spec is delivered. Each criterion should be verifiable without re-reading the plan._

- [x] **Scenario: English board**
  - **Given** the GitHub Pages dashboard is built from the repository data
  - **When** a user opens `/acquisition/`
  - **Then** they see acquisition metrics, platform coverage, campaign summaries, ad cards, and evidence/limitations in English
- [x] **Scenario: Portuguese board**
  - **Given** the GitHub Pages dashboard is built from the repository data
  - **When** a user opens `/pt/acquisition/`
  - **Then** they see the same acquisition board in Portuguese with localized navigation and labels
- [x] **Scenario: Evidence boundaries**
  - **Given** a product/platform query is only `partial`
  - **When** the board renders scan coverage
  - **Then** it marks the result as partial and does not imply no ads exist
- [x] **Scenario: Observed ads**
  - **Given** Augment Code has observed Google ads in `marketing/current/ads.json`
  - **When** the board renders campaigns and creatives
  - **Then** it shows the Google platform, campaign tags, representative headlines, claims, dates, and source/evidence references
- [x] The top-level navigation links to the Acquisition board in both locales.
- [x] The board is generated from committed JSON files, not hard-coded ad data in the page.

## Non-goals

- Running new ad-library scans.
- Adding API-key based integrations.
- Introducing spend, targeting, or performance estimates not present in public sources.
- Scoring competitors by marketing sophistication.
- Replacing the existing benchmark/competitor matrix pages.

## Open questions

- Whether the board should later get interactive filters. Initial implementation can be static
  and scannable because the current dataset is small.
