# 002 — v0-1-task-suite

_Created 2026-07-07._

**Status:** in-progress
<!-- Bare enum only: draft | in-progress | shipped | shipped-partial | superseded | abandoned | deferred.
     When this ships, add a **Closure:** line here recording what shipped (commit/evidence);
     `/sdd close` flags a shipped spec that still lacks one (alongside unchecked boxes,
     placeholders, and missing dogfood proof or opt-out). -->

## Intent

The benchmark currently has only one smoke task. That proves the harness shape,
but it is not enough to evaluate an ADE across the workflows that matter for
Tachyon: multi-file feature work, dirty worktree safety, CI failure debugging,
and UI regression handling.

This spec delivers the first v0.1 task suite and a local Tachyon dogfood
baseline report. The baseline is not a public leaderboard; it is a protocol
check that proves the suite is solvable and that the harness captures useful
evidence.

## Acceptance criteria

- [ ] **Scenario: Suite metadata**
  - **Given** the repository after this spec
  - **When** `python3 harness/bench.py list-tasks` runs
  - **Then** it lists five tasks covering bugfix, feature, dirty-worktree, CI failure, and UI regression categories
- [ ] **Scenario: Baseline fixtures fail before product work**
  - **Given** the v0.1 task suite
  - **When** `scripts/check-suite.sh` runs
  - **Then** every task prepares successfully and fails verification before a product fix
- [ ] **Scenario: Dirty worktree setup**
  - **Given** task `T003-dirty-worktree-safety`
  - **When** it is prepared
  - **Then** the worktree contains a tracked README modification and an untracked `local-user-note.txt` after the baseline commit
- [ ] **Scenario: Tachyon dogfood baseline**
  - **Given** a clean benchmark commit containing the v0.1 suite
  - **When** local Tachyon/Codex dogfood runs each task and verifies the result
  - **Then** all five task verifiers pass and a report records status, diff footprint, and evidence limitations
- [ ] Harness run metadata marks dirty benchmark checkouts with `-dirty`.
- [ ] Verifier execution avoids writing Python bytecode into product worktrees.

## Non-goals

- It does not compare Tachyon against competitors yet.
- It does not create hidden tests.
- It does not automate GUI products.
- It does not publish a scored leaderboard.
- It does not treat local Tachyon/Codex dogfood as a final product benchmark.

## Open questions

- Which competitor should be run first after Tachyon dogfood: Orca or Kandev?
- Should future task suites include hidden verifiers outside the public repo?
