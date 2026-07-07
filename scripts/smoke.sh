#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 harness/bench.py check
python3 harness/bench.py list-products >/dev/null
python3 harness/bench.py list-tasks >/dev/null

rm -rf runs/smoke
python3 harness/bench.py prepare --product tachyon --task T001-python-bugfix --run-id smoke >/dev/null
printf '#!/usr/bin/env bash\nexit 0\n' > runs/smoke/verifier/verify.sh
if python3 harness/bench.py verify runs/smoke >/dev/null; then
  echo "Expected initial fixture verification to fail before an ADE fixes it" >&2
  exit 1
fi

python3 - <<'PY'
from pathlib import Path
path = Path("runs/smoke/worktree/string_math.py")
text = path.read_text()
path.write_text(text.replace("product = 0", "product = 1"))
Path("runs/smoke/worktree/NOTES.md").write_text("untracked evidence\n")
PY

python3 harness/bench.py verify runs/smoke >/dev/null
grep -q "NOTES.md" runs/smoke/artifacts/final.diff
rm -rf runs/smoke

echo "OK: smoke check passed"
