# 002 — v0-1-task-suite — notes

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
# Notes

- The v0.1 suite commit is `454290b40eb0`; local dogfood runs were regenerated after that commit so `result.json.benchmark_commit` points at a clean suite commit.
- The dirty-worktree task intentionally includes an initial tracked `README.md` modification and an untracked `local-user-note.txt`. The harness now stores `artifacts/initial-git-status.txt` and `artifacts/initial-dirty.diff` at prepare time so reports can separate user dirty state from product work.
- `PYTHONDONTWRITEBYTECODE=1` is set for verifier execution to avoid product worktree `__pycache__` noise in status and diff artifacts.

## Local Tachyon/Codex dogfood

- `T001-python-bugfix`: pass
- `T002-python-discount-feature`: pass
- `T003-dirty-worktree-safety`: pass
- `T004-ci-status-normalizer`: pass
- `T005-ui-responsive-cards`: pass

## Dogfood log

### 2026-07-07T17:52:55Z — fail (0/1) — source: tasks.md — commit: 454290b40eb07c76b92e0dee5f6c7bb0fe02d339
- `scripts/check-suite.sh` — fail


### 2026-07-07T17:53:13Z — pass (1/1) — source: tasks.md — commit: 454290b40eb07c76b92e0dee5f6c7bb0fe02d339
- `scripts/check-suite.sh` — pass
## Verification log

### 2026-07-07T17:52:55Z — pass (2/2) — source: tasks.md
- `scripts/check-suite.sh` — pass
- `scripts/smoke.sh` — pass

### 2026-07-07T17:53:08Z — pass (2/2) — source: tasks.md
- `scripts/check-suite.sh` — pass
- `scripts/smoke.sh` — pass
