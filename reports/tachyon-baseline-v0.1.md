# Tachyon Baseline v0.1

Generated on 2026-07-07.

## Scope

This is a local Tachyon/Codex dogfood pass over the first v0.1 task suite. It
validates that the benchmark protocol, fixtures, verifiers, and evidence
capture work end to end.

This is not a public leaderboard and should not be compared against competitor
runs until those products are run with the same protocol.

## Run Context

- Product profile: `tachyon`
- Runner: current Codex session inside Tachyon
- Benchmark suite commit: `454290b40eb0`
- Network policy: not relevant to these local fixtures
- Human interventions: 0 after task prompts were accepted for this dogfood block
- Run artifacts: local ignored directories under `runs/tachyon-v0.1-*`

## Results

| Task | Category | Status | Verify Time | Diff Footprint |
|---|---|---:|---:|---|
| `T001-python-bugfix` | bugfix | pass | 0.043s | 1 file, +1/-2 |
| `T002-python-discount-feature` | feature | pass | 0.046s | 2 files, +18/-6 |
| `T003-dirty-worktree-safety` | dirty-worktree | pass | 0.045s | 2 files, +6/-6 plus preserved untracked note |
| `T004-ci-status-normalizer` | ci-failure | pass | 0.090s | 1 file, +3/-2 |
| `T005-ui-responsive-cards` | ui-regression | pass | 0.046s | 1 file, +12/-3 |

## Evidence Notes

- `scripts/check-suite.sh` confirms all five fixtures fail before product work.
- Each run was prepared with `python3 harness/bench.py prepare`.
- Each final result passed with `python3 harness/bench.py verify`.
- The dirty-worktree task records `artifacts/initial-git-status.txt` so the
  pre-existing `README.md` modification and `local-user-note.txt` are
  distinguishable from product work.
- Verifiers run outside the product worktree and receive the worktree path via
  `BENCH_WORKTREE`.

## Limitations

- The UI task uses static HTML/CSS checks rather than browser rendering.
- The dogfood runner was this Tachyon/Codex session, not a packaged Tachyon
  release driven through the full GUI.
- Timing numbers are verifier runtime only, not total task completion time.
- Cost and token data were not captured in this local pass.

## Next Runs

The next comparable product runs should start with:

1. Orca
2. Kandev

They should use the same five task IDs and preserve their run artifacts before
any scored report is published.

