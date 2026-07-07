# 009 — acquisition-roadmap-history-queue — notes

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

- Added `docs/acquisition-roadmap.md` as the durable roadmap, with phases from
  board/review loop through scheduled monitoring and reporting.
- Added scan history derived from all manifests and review queue derived from
  latest coverage rows that are partial, blocked, or too generic to attribute.
- Kandev's `github.com` Google row is explicitly queued as `generic-domain`
  instead of treated as an attributable Google result.
- Visual evidence captured from local preview:
  - `runs/acquisition-roadmap-history-en-full.png`
  - `runs/acquisition-roadmap-history-pt-mobile-full.png`

## Dogfood log

### 2026-07-07T22:33:36Z — pass (1/1) — source: tasks.md — commit: 017e5eb787c5dc6e2eaca2658ee34ba993262d4b
- `npm run dashboard:build` — pass

## Verification log

### 2026-07-07T22:33:36Z — pass (3/3) — source: tasks.md
- `npm run dashboard:check` — pass
- `npm run dashboard:build` — pass
- `scripts/check-suite.sh` — pass
