# 013 — competitive-intelligence-battlecards

_Created 2026-07-08._

**Status:** shipped
**Closure:** Shipped the five-block competitive-intelligence foundation: battlecards, digital import slots, source intelligence, pricing/packaging watch, and manual-first reproducible collector. Verification, dogfood, and Visual QA evidence are recorded in `notes.md`.
<!-- Bare enum only: draft | in-progress | shipped | shipped-partial | superseded | abandoned | deferred.
     When this ships, add a **Closure:** line here recording what shipped (commit/evidence);
     `/sdd close` flags a shipped spec that still lacks one (alongside unchecked boxes,
     placeholders, and missing dogfood proof or opt-out). -->

## Intent

The repository should adopt the useful primitives from competitive-intelligence
SaaS products without making a paid vendor the source of truth. The goal is not
to clone Crayon, Klue, Similarweb, Semrush, AlphaSense, Contify, CIx, or Apify.
The goal is to map their strongest workflows into repo-native, reviewable, and
reproducible artifacts.

Done means the repo implements all five proposed blocks:

1. **Battlecards** inspired by Crayon/Klue.
2. **Digital and marketing intelligence imports** inspired by Similarweb/Semrush.
3. **Source intelligence** inspired by AlphaSense/Contify: source, freshness,
   confidence, and evidence stay attached to every insight.
4. **Pricing and packaging watch** inspired by SaaS/CIx-style competitive intel.
5. **Reproducible collectors** inspired by Apify, starting manual-first with a
   CLI and schema instead of automatic scraping.

## Acceptance criteria

- [x] **Scenario: signal validation**
  - **Given** tracked competitive-intelligence records
  - **When** the validation script runs
  - **Then** it rejects unknown competitor ids, invalid categories, invalid confidence levels, invalid freshness values, and missing source URLs
- [x] **Scenario: manual signal capture**
  - **Given** a maintainer has a sourced observation from a SaaS tool or manual review
  - **When** they run the capture helper
  - **Then** the signal is appended to a signal file in the canonical schema
- [x] **Scenario: battlecard dashboard**
  - **Given** seed competitive signals exist
  - **When** the Astro dashboard builds
  - **Then** English and Portuguese battlecard routes render product-level battlecards with evidence, confidence, objections, and Tachyon response
- [x] Documentation maps all five blocks above into the repo workflow.
- [x] `scripts/check-suite.sh` includes competitive-intelligence validation.

## Non-goals

- Buying or integrating paid SaaS APIs in this pass.
- Scraping competitor sites automatically.
- Turning battlecards into benchmark scores.
- Treating marketing traffic estimates as product capability evidence.

## Open questions

- Which paid tools, if any, Tachyon will actually subscribe to later.
- Whether the next ingestion layer should be CSV import, API adapters, or
  scheduled browser captures.
