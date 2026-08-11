# Run report metrics

Benchmark reports must preserve enough context to explain how a result was
achieved. A pass/fail verifier outcome is necessary, but it is not sufficient
for comparing ADEs because two passing runs can have very different operator
burden, latency, cost, review load, and evidence quality.

The canonical contract lives in `schemas/run-result.schema.json`. New runs
created by `harness/bench.py prepare` initialize a top-level `metrics` object.
`harness/bench.py verify` then updates the fields it can measure from the run
directory.

## Required metric groups

### Intervention burden

`metrics.intervention_burden` records how much human steering was required:

- `count`: number of human interventions.
- `minutes`: estimated human time spent intervening.
- `operator_decision_points`: number of explicit operator choices.
- `interventions`: typed event log for prompts, manual edits, restarts,
  rollbacks, retries, environment fixes, or other steering.

Prepared runs default to zero burden and an empty intervention list. That means
"none recorded yet", not proof that a real external run needed no intervention.
Publishing scored reports should require either a completed intervention log or
an explicit note explaining why the product runner emits no such telemetry yet.

### Timing

`metrics.timing` separates benchmark latency from verifier runtime:

- `prepared_at`: timestamp when the run directory was created.
- `verified_at`: timestamp when verification ended.
- `time_to_verified_change_seconds`: wall-clock time from prepare to verifier
  completion.
- `verification_elapsed_seconds`: runtime of the verifier command itself.

`time_to_verified_change_seconds` intentionally includes idle time between
prepare and verify. Later telemetry can add active-agent time, but the first
reproducible baseline is "how long until a verified change exists".

### Cost

`metrics.cost` reserves slots for:

- `usd`
- `input_tokens`
- `output_tokens`
- `tool_calls`

These are nullable until a product runner can report them consistently. Missing
cost data must remain visible instead of being silently treated as free.

### Artifact completeness

`metrics.artifact_completeness` records whether the report contains the core
evidence needed for review:

- `result.json`
- prompt
- final diff
- verifier stdout
- verifier stderr
- git status

Leaderboard rows should discount or withhold results with incomplete artifacts.

### Isolation

`metrics.isolation` records whether the verifier was refreshed from the
canonical task definition before execution and whether the worktree had changes
at verification time. This protects against a run mutating its own verifier or
publishing a pass without a reviewable worktree state.

### Review burden

`metrics.review_burden` records change size:

- changed files from `git status --short`
- final diff line count
- final diff byte size

This is not a quality metric by itself. It is a reviewability signal that should
be interpreted alongside pass/fail, task type, and intervention burden.

### Failure recovery

`metrics.failure_recovery` reserves slots for retry, rollback, and recovery
signals. They default to zero or null until runners record them explicitly.

## Run configuration dimensions (fairness)

`run_config` must make comparable runs distinguishable. `harness/bench.py prepare`
initializes these fields (null means "not filled yet"):

| Field | Meaning |
| --- | --- |
| `product_version` | ADE / product version under test |
| `runtime_model` | From competitor profile: `guest-cli` \| `hybrid` \| `first-party` \| `unknown` |
| `guest_runtime` | Guest coding CLI/harness id (e.g. `claude-code`, `codex`) when used |
| `own_runtime` | Product-owned agent id when used (e.g. `warp-agent`, `kiro-agent`) |
| `model` | Model/subscription tier behind the agent loop |
| `execution_surface` | How the task was driven: `product-gui` \| `product-cli` \| `guest-cli-direct` \| `install-smoke-only` \| `other` |
| `network_policy` | Network constraints for the run |
| `time_budget_minutes` | Task budget |
| `cost_usd` | Optional total cost |
| `notes` | Free-form caveats |

### Fairness rules

1. **Separate ADE chrome from coding loop.** On `guest-cli` (and most `hybrid`)
   products, single-task correctness largely measures `guest_runtime` + `model`.
   Do not treat a green verifier as proof of ADE quality without recording those
   dimensions.
2. **Do not mix runtime models in one leaderboard row without labels.** A Kiro
   (`first-party`) pass and an Orca+Claude (`guest-cli`) pass answer different
   questions. Either fix guest/model across Class A rows or publish separate
   slices.
3. **`guest-cli-direct` is not a product orchestration score.** Fixing the
   fixture with a CLI outside the ADE UI may be valid for fixture/verifier
   debugging, but it must not be sold as an ADE-controlled run.
4. **`install-smoke-only` is research evidence, not a scored pass.** Package
   install, AppImage extract, and process start can update readiness notes; they
   do not set `status: pass` for a task.
5. **Hybrid runs must name which loop ran.** Set `own_runtime` and/or
   `guest_runtime` so readers know whether Warp Agent vs Claude Code (etc.)
   executed the task.

Related: competitor `runtime_model` in `docs/competitor-intelligence.md` and
`docs/bench-roadmap.md` Phase 1/3.

## Scoring guardrails

Do not publish a product ranking from pass/fail alone. A defensible scorecard
needs at minimum:

- verifier outcome
- intervention burden
- time-to-verified-change
- artifact completeness
- isolation signal
- review burden
- cost when available
- failure recovery when available
- **run_config dimensions** above (especially `runtime_model`, guest/own runtime,
  model, execution_surface)

Until enough runs have complete metric coverage, dashboards should present these
fields as evidence and confidence context, not as a single aggregate leaderboard.
