# 005 — dashboard-i18n

_Created 2026-07-07._

**Status:** shipped
**Closure:** Added static English/default and Portuguese `/pt/` dashboard routes with localized UI chrome, labels, filters, charts, protocol copy, and profile headings; verified by Astro check/build, harness schema check, and browser screenshots under `runs/visual-qa/005-dashboard-i18n/`.

## Intent

The public dashboard needs to serve both English and Portuguese readers without
forking the benchmark data model. English remains the default public route, and
Portuguese pages live under `/pt/` so GitHub Pages can publish a fully static
site.

Done means navigation, page chrome, labels, filters, charts, protocol copy, and
profile headings are localized, while factual competitor research remains backed
by the canonical `competitors/*.json` source records.

## Acceptance criteria

- [x] **Scenario: English default**
  - **Given** the GitHub Pages dashboard root
  - **When** a reader opens `/tachyon-ade-bench/`
  - **Then** the overview renders in English and links stay on English routes
- [x] **Scenario: Portuguese routes**
  - **Given** the GitHub Pages dashboard root
  - **When** a reader opens `/tachyon-ade-bench/pt/`
  - **Then** the overview renders in Portuguese and links stay under `/pt/`
- [x] **Scenario: Language switch**
  - **Given** any dashboard route with an English and Portuguese equivalent
  - **When** the reader uses the EN/PT language switch
  - **Then** they land on the matching route in the selected language
- [x] Matrix filters, charts, protocol diagram labels, badges, and profile
      headings use localized UI strings.
- [x] Static builds emit both default English pages and Portuguese `/pt/*` pages.

## Non-goals

- Translating canonical competitor research fields inside `competitors/*.json`.
- Adding runtime locale negotiation, cookies, or browser-language redirects.
- Introducing benchmark scores or modifying the benchmark harness.

## Open questions

- None for this iteration.
