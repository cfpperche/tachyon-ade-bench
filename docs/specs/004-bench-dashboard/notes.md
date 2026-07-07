# 004 — bench-dashboard — notes

_Created 2026-07-07._

_In-flight design memory — decisions, deviations, tradeoffs, and open questions surfaced **while building** that weren't pre-empted by `spec.md` or `plan.md`. Append-only by convention._

## Design decisions

_Choices made where the spec/plan was ambiguous. The decision + why this option over the others considered in the moment._

- 2026-07-07: Kept the dashboard inside the benchmark repo as
  `apps/bench-dashboard`, so GitHub Pages renders the same tracked JSON data
  used by the harness and reports.
- 2026-07-07: Used Astro static output with React islands only for the matrix,
  charts, and protocol diagram. This keeps most pages static while preserving
  useful interactivity.
- 2026-07-07: Configured Astro with `base: "/tachyon-ade-bench"` for the public
  GitHub Pages URL.

## Deviations

_Where implementation intentionally departed from `plan.md`, and why it was necessary or better._

- 2026-07-07: Matrix mobile uses a dedicated card rendering instead of a
  horizontally scrolling table. The first QA pass showed the table was readable
  but awkward on narrow screens.

## Tradeoffs

_Alternatives weighed mid-build. The chosen path + what was given up + why it was worth it._

- 2026-07-07: Chose ECharts for analytical charts and Mermaid runtime for the
  protocol diagram. The build emits non-fatal chunk-size warnings; acceptable
  for v0.1, but a future static SVG diagram could reduce protocol-page JS.
- 2026-07-07: Upgraded to Astro 7 and ECharts 6 during implementation because
  the initial package set had npm audit advisories. `npm audit --audit-level=moderate`
  is clean after the upgrade.

## Open questions

_Questions surfaced during the build with no answer yet. Owner or path to resolution if known._

- GitHub Pages must be enabled in repository settings with source "GitHub
  Actions" before the workflow can publish.
- Future optimization: replace Mermaid runtime with a build-time or static SVG
  diagram if bundle size matters.

## Verification log

- 2026-07-07: `python3 harness/bench.py check` passed.
- 2026-07-07: `npm run dashboard:check` passed.
- 2026-07-07: `npm run dashboard:build` passed.
- 2026-07-07: `npm audit --audit-level=moderate` passed with 0 vulnerabilities.

## Visual QA

Evidence:

- `runs/visual-qa/dashboard-overview-desktop-v2.png`
- `runs/visual-qa/dashboard-matrix-mobile-v3.png`
- `runs/visual-qa/dashboard-protocol-desktop.png`
- `runs/visual-qa/dashboard-orca-mobile.png`
- `runs/visual-qa/dashboard-sources-desktop.png`

Verdict: desktop overview renders charts and metrics correctly; matrix mobile
uses readable cards; protocol diagram, source index, and competitor detail pages
are legible without observed text overlap.

## Dogfood log

### 2026-07-07T20:00:42Z — pass (1/1) — source: tasks.md — commit: 0f99cf212b9232089faf7a7881a2b4f396200dc8
- `npm run dashboard:build` — pass

### 2026-07-07T20:00:42Z — pass (3/3) — source: tasks.md
- `python3 harness/bench.py check` — pass
- `npm run dashboard:check` — pass
- `npm run dashboard:build` — pass
