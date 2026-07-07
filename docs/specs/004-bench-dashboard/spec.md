# 004 — bench-dashboard

_Created 2026-07-07._

**Status:** shipped
**Closure:** Shipped Astro dashboard, data loaders, interactive matrix/charts, competitor detail pages, source/protocol views, root npm scripts, GitHub Pages workflow, and visual QA evidence. Verification passed locally on 2026-07-07.
<!-- Bare enum only: draft | in-progress | shipped | shipped-partial | superseded | abandoned | deferred.
     When this ships, add a **Closure:** line here recording what shipped (commit/evidence);
     `/sdd close` flags a shipped spec that still lacks one (alongside unchecked boxes,
     placeholders, and missing dogfood proof or opt-out). -->

## Intent

The repository now has structured competitor intelligence, but the primary
consumer experience is still JSON files and markdown. Because this repo is
public, it should expose a polished GitHub Pages dashboard that makes the data
easy to inspect, compare, and present.

This spec adds an Astro-based static dashboard under `apps/bench-dashboard`.
The dashboard reads the tracked benchmark data, renders an executive overview,
competitor matrix, individual competitor detail pages, charts, and a protocol
view, and can be deployed from GitHub Actions to GitHub Pages.

Done means a maintainer can run the site locally, build it in CI, and publish it
to Pages without manually copying data or maintaining a second source of truth.

## Acceptance criteria

- [x] **Scenario: Local dashboard build**
  - **Given** the repository with competitor JSON profiles
  - **When** `npm run dashboard:build` runs from the repo root
  - **Then** the Astro dashboard builds static assets successfully from the tracked data
- [x] **Scenario: Structured presentation**
  - **Given** a viewer opens the dashboard
  - **When** they navigate the overview, matrix, and competitor detail pages
  - **Then** they can compare stack, infra, features, moat, sources, and benchmark readiness without reading raw JSON
- [x] **Scenario: GitHub Pages deployment**
  - **Given** changes land on `main`
  - **When** the Pages workflow runs
  - **Then** it builds `apps/bench-dashboard` and publishes the static output to GitHub Pages
- [x] The dashboard uses `competitors/*.json` as the data source of truth.
- [x] The app remains static-first and avoids duplicating competitor facts in page code.
- [x] The UI is responsive and suitable for presenting the benchmark map on desktop and mobile.
- [x] LandingAI remains excluded from the ADE dashboard roster.

## Non-goals

- It does not run scored competitor benchmarks.
- It does not add a database or server runtime.
- It does not scrape live competitor sites at runtime.
- It does not create a marketing landing page detached from the actual data.
- It does not claim new competitor facts beyond the existing structured profiles.

## Open questions

- What custom domain, if any, should GitHub Pages use later?
- Should future versions include screenshots from hands-on competitor runs?
