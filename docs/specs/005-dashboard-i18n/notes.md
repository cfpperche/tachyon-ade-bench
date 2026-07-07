# 005 — dashboard-i18n — notes

_Created 2026-07-07._

_In-flight design memory — decisions, deviations, tradeoffs, and open questions surfaced **while building** that weren't pre-empted by `spec.md` or `plan.md`. Append-only by convention._

## Design decisions

- Portuguese pages localize product-facing UI text, but source-backed competitor
  research remains in the canonical English JSON records for this iteration.

## Deviations

- None so far.

## Tradeoffs

- Mirrored static pages duplicate small Astro wrappers, but keep GitHub Pages
  output simple and make route inspection explicit.

## Open questions

- Whether to add translated competitor research later should be handled as a
  separate source-review workflow.

## Dogfood log

### 2026-07-07T20:18:26Z — pass (1/1) — source: tasks.md — commit: bd9388748300b205fd080e397102cb55ff7e92d9
- `npm run dashboard:build` — pass


### 2026-07-07T20:19:55Z — pass (1/1) — source: tasks.md — commit: bd9388748300b205fd080e397102cb55ff7e92d9
- `npm run dashboard:build` — pass

### 2026-07-07T20:23:08Z — pass (1/1) — source: tasks.md — commit: bd9388748300b205fd080e397102cb55ff7e92d9
- `npm run dashboard:build` — pass
## Verification log

### 2026-07-07T20:18:26Z — pass (3/3) — source: tasks.md
- `npm run dashboard:check` — pass
- `npm run dashboard:build` — pass
- `python3 harness/bench.py check` — pass

### 2026-07-07T20:19:55Z — pass (3/3) — source: tasks.md
- `npm run dashboard:check` — pass
- `npm run dashboard:build` — pass
- `python3 harness/bench.py check` — pass

### 2026-07-07T20:23:03Z — pass (3/3) — source: tasks.md
- `npm run dashboard:check` — pass
- `npm run dashboard:build` — pass
- `python3 harness/bench.py check` — pass
