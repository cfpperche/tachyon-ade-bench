# 014 — pricing-packaging-watch

_Created 2026-07-08._

**Status:** shipped
**Closure:** Shipped official-source pricing and packaging watch signals for the tracked ADE roster. Verification and dogfood evidence are recorded in `notes.md`.

## Intent

The battlecards layer has a pricing-watch placeholder. The next natural step is
to replace that placeholder with sourced, product-level pricing and packaging
signals from official pages or upstream repositories where possible.

Done means the current intelligence file records pricing/packaging signals for
the tracked ADE roster with source URLs, confidence, freshness, Tachyon
responses, and caveats when a product does not expose enough pricing detail.

## Acceptance criteria

- [x] **Scenario: official pricing/packaging signals**
  - **Given** the tracked competitor roster
  - **When** `intelligence/current/signals.json` is inspected
  - **Then** direct competitors have product-level pricing or packaging signals with source URLs
- [x] **Scenario: validation**
  - **Given** the expanded signal set
  - **When** `python3 scripts/intelligence/check-intelligence.py` runs
  - **Then** the file remains structurally valid
- [x] The documentation explains that missing public pricing is a watch state, not evidence of free or paid positioning.
- [x] Dashboard build still renders battlecards with the expanded pricing/packaging signals.

## Non-goals

- Buying paid Similarweb, Semrush, Crayon, Klue, AlphaSense, or CIx access.
- Inferring hidden pricing from unofficial sources.
- Building a pricing comparison table with normalized dollar totals.
- Changing competitor technical profile claims.

## Open questions

- Whether future pricing snapshots should store raw HTML/hash evidence in
  addition to normalized signals.
