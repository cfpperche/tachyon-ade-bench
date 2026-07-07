# 002 — v0-1-task-suite — plan

_Drafted from `spec.md` on 2026-07-07. The approach, not the steps (those go in `tasks.md`)._

## Approach

Extend the public benchmark suite from one smoke task to five v0.1 tasks. Keep
each task dependency-light and verifier-owned so any product can run it without
installing a large toolchain. Add minimal harness support for reproducible dirty
worktree state through a `post_prepare` overlay.

After the suite is committed, run a local Tachyon/Codex dogfood pass against
all five tasks, keep run artifacts under ignored `runs/`, and commit a human
report with raw outcomes and caveats.

## Key decisions

- **Five small tasks** - chosen because category breadth matters more than deep
  difficulty at v0.1; rejected a single complex repo because it would obscure
  which workflow the benchmark is measuring.
- **Python/stdlib fixtures** - chosen because they are easy to verify anywhere;
  rejected npm/Playwright-heavy fixtures for v0.1 to avoid setup noise.
- **External verifier remains mandatory** - chosen to preserve the integrity fix
  from spec 001; rejected worktree-local verifiers because products can tamper
  with them.
- **`post_prepare` overlay for dirty worktree** - chosen because dirty state must
  be reproducible after the baseline commit; rejected manual setup because it
  would make competitor runs non-comparable.
- **Dogfood report, not leaderboard** - chosen because this validates the
  protocol before competitor claims; rejected scoring until at least Tachyon,
  Orca, and Kandev have comparable evidence.

## Files touched

- `harness/bench.py` - add dirty checkout commit marker, bytecode suppression,
  task listing detail, and `post_prepare` overlay support.
- `schemas/task.schema.json` - document `post_prepare`.
- `tasks/T002-python-discount-feature/**` - multi-file feature fixture.
- `tasks/T003-dirty-worktree-safety/**` - dirty worktree safety fixture.
- `tasks/T004-ci-status-normalizer/**` - CI-style status normalizer fixture.
- `tasks/T005-ui-responsive-cards/**` - static UI/CSS regression fixture.
- `scripts/check-suite.sh` - validate all fixtures fail before product fixes.
- `reports/tachyon-baseline-v0.1.md` - local dogfood result summary.
- `README.md`, `SPEC.md`, `tasks/README.md` - protocol/docs updates.

## Risks & unknowns

- Verifiers can become too implementation-specific; keep them focused on
  observable behavior.
- The dirty-worktree task can inflate final diff stats with pre-existing user
  changes, so the harness captures initial dirty artifacts separately.
- The UI task uses static checks instead of real browser rendering; reports must
  call that limitation out.
- Local dogfood is useful protocol evidence, but it is not a competitor-grade
  Tachyon product benchmark.

## Visual impact

The benchmark includes a static UI/CSS task, but this spec changes no rendered
application surface in the benchmark repo. Visual QA is not useful for the repo
itself.

## Sources consulted

- `README.md`
- `SPEC.md`
- `harness/bench.py`
- `schemas/task.schema.json`
- `tasks/T001-python-bugfix/**`
- `docs/specs/001-benchmark-mechanism/**`
