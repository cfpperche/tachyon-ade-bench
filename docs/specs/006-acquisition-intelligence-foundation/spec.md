# 006 — acquisition-intelligence-foundation

_Created 2026-07-07._

**Status:** shipped
**Closure:** Shipped acquisition-intelligence foundation with marketing registries, storage roots, JSON schema contracts, dependency-free validation/normalization/summarization scripts, docs, and CI/check-suite coverage. Evidence: marketing checks, harness check, check-suite, smoke, dashboard check/build, npm audit, and SDD verify/dogfood passed locally on 2026-07-07.

## Intent

Acquisition intelligence should be reproducible over time, not a one-off
snapshot of whichever ads were visible during a manual review. The repository
needs a durable foundation for scheduled or manual scans that records what was
queried, what was found, what was not found, and how observations are derived
into current state.

Done means the repo has schemas, registries, directory conventions, validation,
normalization, and summary tooling for append-only marketing scans. The first
version deliberately avoids platform scraping; it proves the data contract so
collectors can be added safely later.

## Acceptance criteria

- [x] **Scenario: Marketing registry validation**
  - **Given** tracked advertiser and source registries
  - **When** `python3 scripts/marketing/check-marketing.py` runs
  - **Then** every product reference, platform, automation level, and source class is structurally valid
- [x] **Scenario: Raw scan normalization**
  - **Given** a raw manual/exported scan JSON file
  - **When** `scripts/marketing/normalize-scan.py` runs for a product/platform/scan id
  - **Then** a deterministic normalized observation file is written with stable ad fingerprints
- [x] **Scenario: History summarization**
  - **Given** one or more normalized scan files
  - **When** `scripts/marketing/summarize-history.py` runs
  - **Then** append-only scan observations are materialized into `marketing/history/ads.ndjson` and derived current-state JSON
- [x] The marketing layer has tracked empty directories for future scans, history, current summaries, and creative notes.
- [x] CI or check-suite validation covers the marketing registry and any tracked scan data.

## Non-goals

- Implementing live platform scrapers or API collectors.
- Claiming ad spend, CAC, conversion, targeting, or ROI.
- Adding acquisition intelligence to the public dashboard in this iteration.
- Scoring competitors based on marketing activity.

## Open questions

- Which official library should receive the first real collector after the data
  contract is proven: Google, Meta, or X?
