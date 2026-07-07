#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 harness/bench.py check

for task_json in tasks/T*/task.json; do
  task_id="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["id"])' "$task_json")"
  run_id="suite-check-$$-$task_id"
  rm -rf "runs/$run_id"
  python3 harness/bench.py prepare --product tachyon --task "$task_id" --run-id "$run_id" >/dev/null
  if python3 harness/bench.py verify "runs/$run_id" >/dev/null; then
    echo "Expected baseline fixture to fail for $task_id" >&2
    exit 1
  fi
  rm -rf "runs/$run_id"
done

echo "OK: all task fixtures validate structurally and fail before a product fix"
