# 011 — strategy-swot-dashboard — notes

_Created 2026-07-08._

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

- Added a bilingual `/strategy/` dashboard surface for Tachyon SWOT, competitive
  pressure, and strategic bets.
- Competitive pressure rows are derived from existing competitor profiles and
  current acquisition campaign observations, not from benchmark scores.
- Mobile visual QA initially showed the pressure table was cramped, so the page
  now renders mobile cards for the pressure matrix.
- Visual evidence:
  - `runs/strategy-swot-en-full.png`
  - `runs/strategy-swot-pt-mobile-full.png`

## Dogfood log

### 2026-07-08T21:46:29Z — pass (1/1) — source: tasks.md — commit: f569def42d58701bfab01a9135ce21f398744b01
- `npm run dashboard:build` — pass

## Verification log

### 2026-07-08T21:46:29Z — pass (3/3) — source: tasks.md
- `npm run dashboard:check` — pass
- `npm run dashboard:build` — pass
- `scripts/check-suite.sh` — pass
