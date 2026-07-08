# 012 — run-report-metrics — plan

_Drafted from `spec.md` on 2026-07-08. The approach, not the steps (those go in `tasks.md`)._

## Approach

Extend `schemas/run-result.schema.json` with a `metrics` object. Add helpers in
`harness/bench.py` to initialize metrics during prepare and update timing plus
artifact/review counts during verify. Add documentation under `docs/` describing
the metric contract and why intervention burden plus time-to-verified-change are
leaderboard prerequisites.

## Key decisions

- **Single `metrics` object** — chosen because it keeps the run report extensible;
  rejected scattering fields across the top level.
- **Initialize unknowns explicitly** — chosen so missing data is distinguishable from
  zero burden; rejected leaving fields absent because downstream reporting would guess.
- **No auto-scoring yet** — chosen because metrics need real run data before weights are defensible.

## Files touched

- `schemas/run-result.schema.json` — metric contract.
- `harness/bench.py` — initialize and update metrics.
- `docs/run-report-metrics.md` — metric definitions and scoring guardrails.
- `docs/specs/012-run-report-metrics/*` — spec tracking.

## Risks & unknowns

- Wall-clock timing from prepare to verify includes idle time if a human pauses a run.
  That is acceptable for `time_to_verified_change`; later telemetry can split active
  agent time from calendar time.
- Intervention minutes remain manual-entry for now.
- Existing untracked run reports may not match the new schema; tracked CI only validates
  metadata and freshly prepared runs.

## Visual impact

No UI change in this spec.
**Visual QA Opt-Out:** schema/harness documentation only.

## Sources consulted

- `schemas/run-result.schema.json`
- `harness/bench.py`
- `scripts/check-suite.sh`
- `docs/specs/001-benchmark-mechanism/*`
- `docs/specs/011-strategy-swot-dashboard/*`
