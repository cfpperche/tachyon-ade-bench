# 015 — jetbrains-air-inclusion

_Created 2026-07-21._

**Status:** shipped
**Closure:** Shipped the official-source JetBrains Air Class A profile, synchronized roster/map/acquisition/intelligence/strategy surfaces, repaired Herdr roster drift, added advertiser coverage validation, and verified the dashboard routes and responsive presentation on 2026-07-21. Runtime qualification remains separately deferred in spec 016 until interactive Linux installation and authentication are available.

## Intent

Add JetBrains Air to the software ADE roster as a source-backed Class A
competitor. Done means the profile is valid, every roster-facing surface is in
sync, acquisition and battlecard systems recognize the product, the dashboard
renders it in both locales, and no scored or runtime-readiness claim is made
before a hands-on run.

## Acceptance criteria

- [x] **Scenario: source-backed competitor profile**
  - **Given** current official JetBrains Air sources
  - **When** `competitors/jetbrains-air.json` is inspected
  - **Then** current capabilities, unknowns, install surface, parity risks, and benchmark tasks are represented without counting announced future features
- [x] **Scenario: complete roster inclusion**
  - **Given** the tracked software ADE roster
  - **When** documentation, acquisition, intelligence, and dashboard surfaces are inspected
  - **Then** JetBrains Air appears as `A-local-ade` with `needs-install` readiness
- [x] **Scenario: roster consistency**
  - **Given** competitor profiles and the acquisition advertiser registry
  - **When** `python3 scripts/marketing/check-marketing.py` runs
  - **Then** every competitor profile has exactly one advertiser entry
- [x] **Scenario: validation and presentation**
  - **Given** the completed inclusion
  - **When** repository checks and the dashboard build run
  - **Then** metadata remains valid and English/Portuguese Air routes build successfully
- [x] Existing Herdr roster drift is repaired in the touched roster, acquisition, and intelligence surfaces.

## Non-goals

- Running or scoring JetBrains Air before desktop installation and authentication.
- Treating cloud execution, automation, or Air Team announcements as shipped features.
- Inferring proprietary implementation details.
- Tailoring benchmark tasks to favor JetBrains Air.
- Publishing or committing ignored `runs/` evidence.

## Open questions

- Should JetBrains Air replace Fusion in the default radar selection after a successful smoke run?
- Should a later harness revision capture Air-created worktrees outside the prepared run directory?
