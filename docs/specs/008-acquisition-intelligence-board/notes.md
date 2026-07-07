# 008 — acquisition-intelligence-board — notes

_Created 2026-07-07._

_In-flight design memory — decisions, deviations, tradeoffs, and open questions surfaced **while building** that weren't pre-empted by `spec.md` or `plan.md`. Append-only by convention._

## Design decisions

_Choices made where the spec/plan was ambiguous. The decision + why this option over the others considered in the moment._

## Deviations

_Where implementation intentionally departed from `plan.md`, and why it was necessary or better._

## Tradeoffs

_Alternatives weighed mid-build. The chosen path + what was given up + why it was worth it._

## Open questions

_Questions surfaced during the build with no answer yet. Owner or path to resolution if known._
## Implementation notes

- Added a static Astro Acquisition Intelligence board rather than a React-heavy
  filter surface because current acquisition history is still small.
- The board keeps scan coverage and observed ads separate: query status comes
  from the latest manifest, while creative cards come from `marketing/current/ads.json`.
- Visual evidence captured from local preview:
  - `runs/acquisition-board-en-full.png`
  - `runs/acquisition-board-pt-mobile-full.png`

## Dogfood log

### 2026-07-07T22:24:28Z — pass (1/1) — source: tasks.md — commit: 4c2847e06967f5a2d8c1b31421ff5d54c3565c48
- `npm run dashboard:build` — pass

## Verification log

### 2026-07-07T22:24:28Z — pass (3/3) — source: tasks.md
- `npm run dashboard:check` — pass
- `npm run dashboard:build` — pass
- `scripts/check-suite.sh` — pass
