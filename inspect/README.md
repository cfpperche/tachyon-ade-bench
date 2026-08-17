# Source inspection harness

Inspect **open-source** ADE checkouts for a fixed feature catalog. This is
not a scored ADE task run. Marketing text in `competitors/*.json` is not
evidence.

Protocol and design: [`docs/inspect-harness.md`](../docs/inspect-harness.md).

```sh
python3 harness/bench.py list-inspectable
python3 harness/bench.py inspect-check
python3 harness/bench.py inspect --fixture mini-ade --run-id local-inspect
python3 harness/test_inspect.py

# Live product (clones source_url, shallow):
python3 harness/bench.py inspect --product kandev --run-id kandev-inspect

# Claude Code / Codex / Grok Build (same prompt):
python3 harness/bench.py inspect --product kandev --run-id kandev-agent --mode agent
# open runs/kandev-agent, give prompt.md exactly, write inspection.json
python3 harness/bench.py inspect-verify runs/kandev-agent
```
