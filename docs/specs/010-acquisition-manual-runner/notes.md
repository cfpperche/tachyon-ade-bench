# 010 — acquisition-manual-runner — notes

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

- Added `scripts/marketing/plan-scan.py` as a registry-driven planner, not a
  live scraper.
- Dry-run prints tab-separated planned rows; write mode emits a manifest through
  the existing `common.py` helpers.
- Kandev's Google query keeps `github.com/kdlbs/kandev` as context and encodes
  it in the URL parameter instead of collapsing to `github.com`.
- Added `npm run acquisition:plan` as the documented entry point.

## Dogfood log

### 2026-07-07T22:41:15Z — pass (1/1) — source: tasks.md — commit: 71483f11ed021953a79ba2313b1cf317fa29bf3c
- `python3 scripts/marketing/plan-scan.py --scan-id 20260707T230000Z --platform google --platform meta --output-root /tmp/tachyon-ade-bench-scans` — pass

## Verification log

### 2026-07-07T22:41:15Z — pass (3/3) — source: tasks.md
- `python3 scripts/marketing/plan-scan.py --scan-id 20260707T230000Z --platform google --platform meta --dry-run` — pass
- `python3 scripts/marketing/check-marketing.py` — pass
- `scripts/check-suite.sh` — pass
