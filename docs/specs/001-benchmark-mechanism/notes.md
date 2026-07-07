# 001 — benchmark-mechanism — notes

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

- Claude review found one blocker before publication: the original verifier lived inside the product worktree and could be tampered with. Fixed by making `verify.directory` required, copying a pristine verifier outside the worktree, restoring it before each verify, and passing the product worktree through `BENCH_WORKTREE`.
- `scripts/smoke.sh` now proves the unfixed fixture fails, a tampered copied verifier still fails, a genuine fix passes, and untracked files appear in `artifacts/final.diff`.

## Verification log

- 2026-07-07: `python3 harness/bench.py check` passed.
- 2026-07-07: `scripts/smoke.sh` passed.

## Dogfood log

- 2026-07-07: `scripts/smoke.sh` passed as the representative end-to-end run.

### 2026-07-07T17:06:42Z — pass (1/1) — source: tasks.md — commit: HEAD
unknown
- `scripts/smoke.sh` — pass

### 2026-07-07T17:06:48Z — pass (1/1) — source: tasks.md
- `scripts/smoke.sh` — pass
