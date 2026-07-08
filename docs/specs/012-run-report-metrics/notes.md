# 012 — run-report-metrics — notes

_Created 2026-07-08._

_In-flight design memory — decisions, deviations, tradeoffs, and open questions surfaced **while building** that weren't pre-empted by `spec.md` or `plan.md`. Append-only by convention._

## Design decisions

- `metrics` is required for new run reports. Unknown values are explicit `null`
  slots rather than omitted fields, so dashboards can distinguish unavailable
  telemetry from zero cost or zero work.
- `harness/bench.py verify` refreshes the task verifier from the canonical task
  directory before every verification and records that in
  `metrics.isolation.verifier_refreshed_from_canonical`.

## Deviations

- None.

## Tradeoffs

- Intervention minutes, token usage, and retry/rollback recovery remain manual
  or runner-supplied for now. Auto-inferring them from shell state would create
  false precision before product runners expose reliable telemetry.

## Open questions

- Later runner work should decide whether intervention events are recorded by a
  harness CLI subcommand, imported agent telemetry, or dashboard annotation.

## Dogfood log

### 2026-07-08T21:57:19Z — pass (1/1) — source: tasks.md — commit: d9330ae0ecb0419c302de0420853abf9f6a468ba
- `rm -rf runs/metrics-smoke && python3 harness/bench.py prepare --product tachyon --task T001-python-bugfix --run-id metrics-smoke && python3 harness/bench.py verify runs/metrics-smoke || true` — pass

## Verification log

### 2026-07-08T21:57:19Z — pass (2/2) — source: tasks.md
- `scripts/check-suite.sh` — pass
- `npm run dashboard:check` — pass
