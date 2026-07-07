#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${BENCH_WORKTREE:-}" ]]; then
  echo "BENCH_WORKTREE is required" >&2
  exit 2
fi

python3 -m unittest discover -s . -p 'test_*.py'

