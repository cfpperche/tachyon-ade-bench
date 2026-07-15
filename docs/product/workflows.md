# Tachyon core workflows

Owned operating loops that the ADE Bench is designed to stress. Keep these
aligned with `harness/` protocol language.

## 1. Benchmark / fair-run loop

```text
prepare worktree + prompt
    → product works only in worktree
    → independent verify
    → preserve result.json + artifacts
```

Rules:

- Same prompt and fixture for comparable products
- Count human interventions
- Product claims are not evidence; verifier exit code is

See `SPEC.md` and `docs/run-report-metrics.md`.

## 2. Delegated agent work (isolation)

```text
task arrives
    → allocate isolated workspace (worktree / owned path boundary)
    → agent(s) execute
    → handoff / evidence captured
    → merge or accept only after gates
```

Probe targets: dirty trees, parallel tasks, path escape, accidental edits
outside the owned boundary.

## 3. Multi-agent handoff

```text
parent / orchestrator delegates
    → sub-agent works in isolated scope
    → returns evidence + change
    → parent reviews / continues
```

Probe targets: lost context, missing evidence, unclear ownership of the final
diff.

## 4. Verification-first completion

```text
agent proposes done
    → run verification gate
    → on fail: recover or rework with recorded retries
    → on pass: accept handoff
```

Probe targets: false “done”, missing logs, unverifiable claims.

## 5. Review / shipping (owned)

```text
change + evidence
    → human or policy review
    → ship (commit/PR/merge) under project rules
```

Exact PR host integrations are **not** claimed here until documented in
`capabilities.json` as `claimed`.

## Recording product runs in this repo

1. `python3 harness/bench.py prepare --product tachyon --task <id> --run-id <id>`
2. Point Tachyon only at `runs/<id>/worktree` with `prompt.md`
3. `python3 harness/bench.py verify runs/<id>`
4. Fill `run_config` / intervention fields before any public comparison
