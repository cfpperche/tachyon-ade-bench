# 016 — jetbrains-air-smoke — plan

_Drafted from `spec.md` on 2026-07-21._

## Approach

Use the manual-product protocol without changing the task fixture. Prepare
T001, open only the generated worktree as an Air Local Workspace, select a guest
agent/model that can be recorded and compared, provide the exact prompt, count
all intervention, and let the harness verifier determine the result.

## Key decisions

- Use Local Workspace rather than an Air-created worktree for artifact containment.
- Keep Air version separate from guest agent, model, effort, and subscription metadata.
- Do not use optional cross-agent review in the first correctness smoke.
- Promote readiness only after a passing verifier and complete evidence.

## Expected run

```sh
python3 harness/bench.py prepare \
  --product jetbrains-air \
  --task T001-python-bugfix \
  --run-id jetbrains-air-<version>-T001
```

After the interactive Air task completes:

```sh
python3 harness/bench.py verify runs/jetbrains-air-<version>-T001
```

## Risks

- Toolbox/Air installation and authentication are interactive on Linux.
- Available models and permission modes can change between preview versions.
- Opening an Air worktree instead of Local Workspace can place changes outside the run artifact boundary.
