# Benchmark Protocol v0

This document defines the first reproducible protocol for Tachyon ADE Bench.

## Goal

Measure whether an Agentic Development Environment can complete realistic
software engineering work correctly, with auditable evidence and minimal human
intervention.

The benchmark asks:

> Given the same repository, prompt, constraints, and verification command,
> which ADE produces a correct, reviewable, reproducible change?

## Product classes

Class A products are direct local or multi-agent ADE competitors:

- Tachyon
- Orca
- Herdr
- HiveTerm
- T3 Code
- Hive
- AgentsRoom
- OpenADE / ADE App
- Kandev
- Fusion (Runfusion)
- Maestri
- JetBrains Air

Class B products are enterprise agentic platforms:

- Augment Code

Class B can be measured with the same artifacts, but reports should avoid
mixing its score with Class A without explaining the setup difference.

## Exclusions

LandingAI is excluded from this roster because its ADE is Agentic Document
Extraction, which is a document AI product category rather than a software
development environment.

## Run invariants

Each comparable run must declare:

- product id and version
- task id and benchmark repository commit
- model or subscription used when known
- network policy
- time budget
- human intervention count
- intervention burden, time-to-verified-change, artifact completeness,
  isolation, review burden, and recovery indicators from `result.json.metrics`
- starting fixture commit
- final diff and verification output

Each task owns its verifier. A run passes only when the task verifier exits
zero in the final worktree.

## Artifact contract

Each run directory should contain:

- `result.json`: structured run metadata and final status
- `result.json.metrics`: intervention burden, timing, cost, artifact
  completeness, isolation, review burden, and failure recovery fields
- `result.json.run_config`: product version, model, network policy, time
  budget, cost, and notes when available
- `prompt.md`: exact user-facing prompt supplied to the product
- `task.json`: copied task metadata
- `product.json`: copied product profile
- `worktree/`: isolated copy of the fixture repository, which is the only path
  the product under test should edit
- optional `post_prepare/` overlay effects: reproducible dirty state applied
  after the baseline fixture commit
- `verifier/`: task-owned verifier copy restored from the tracked task
  definition before each verification
- `artifacts/verify.stdout.txt`
- `artifacts/verify.stderr.txt`
- `artifacts/initial-git-status.txt`
- `artifacts/initial-dirty.diff`
- `artifacts/git-status.txt`
- `artifacts/git-diff-stat.txt`
- `artifacts/final.diff`: tracked changes plus untracked text files

## Initial scoring model

The first public reports should keep raw data primary and scoring secondary.
When a score is introduced, use a weighted model like:

- 40% correctness
- 20% autonomy
- 15% reproducibility
- 10% cost and time efficiency
- 10% code quality
- 5% evidence quality

The harness does not yet compute this score. It preserves the raw evidence
needed to calculate it later.

## Manual product protocol

For a product without a scriptable CLI:

1. Run `prepare`.
2. Open only the generated `worktree/` in the product.
3. Provide `prompt.md` exactly as written.
4. Count each human correction or additional instruction.
5. Run `verify` after the product finishes.
6. Record any unavailable metadata in `result.json` before publishing a report.
