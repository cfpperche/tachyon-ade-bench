# 007 — manual-acquisition-scan-tools

_Created 2026-07-07._

**Status:** shipped
**Closure:** Shipped manual acquisition scan helpers for creating scan manifests, recording not-found queries, appending manual ad observations, and normalizing raw scans. Evidence: marketing checks, check-suite, SDD verify, and SDD dogfood passed locally on 2026-07-07.

## Intent

Manual acquisition scans should use the same durable data contract as future
collectors. Without helpers, the first real scan is likely to hand-edit raw JSON,
forget manifest queries, or fail to record negative results consistently.

Done means a maintainer can create a scan, record "not found" evidence, add a
manual ad observation, normalize it, and summarize history using repo commands
instead of ad hoc JSON edits.

## Acceptance criteria

- [x] **Scenario: Start manual scan**
  - **Given** a scan id, product, platform, query, and source URL
  - **When** `scripts/marketing/new-scan.py` runs
  - **Then** it creates `marketing/scans/<scan_id>/manifest.json` and a platform directory
- [x] **Scenario: Record no public result**
  - **Given** an existing scan directory
  - **When** `scripts/marketing/add-not-found.py` runs
  - **Then** the manifest records the query with `result: not-found`
- [x] **Scenario: Add manual ad**
  - **Given** an existing scan directory
  - **When** `scripts/marketing/add-manual-ad.py` runs
  - **Then** the product raw file is updated and a normalized scan file is generated
- [x] The helper workflow is documented in `docs/acquisition-intelligence.md`.
- [x] Existing marketing checks validate helper output.

## Non-goals

- Scraping or automating external ad libraries.
- Capturing screenshots or media assets.
- Running a real competitor acquisition scan.

## Open questions

- None for this helper-only iteration.
