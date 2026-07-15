# CLAUDE.md — Tachyon ADE Bench

Follow **[AGENTS.md](./AGENTS.md)** as the primary agent context for this repository.

## Non-negotiable boundaries

1. **This repo** (`tachyon-ade-bench`): you may edit when the task requires it.
2. **Product repo** (`~/tachyon`, remote `cfpperche/tachyon`): **read only**.
   - Do **not** write, commit, push, open PRs, or modify git state there.
   - Do **read** it freely to ground Tachyon product claims (README, `docs/`, `src/`, `CHANGELOG.md`, `tachyon.yml`, etc.).
3. When product facts need to land in the bench, write to **`docs/product/`** (especially `capabilities.json`), then:

   ```sh
   python3 scripts/product/check-capabilities.py
   python3 scripts/product/sync-tachyon-profile.py
   python3 harness/bench.py check
   ```

## Quick orientation

- **Purpose:** fair ADE benchmark harness + competitor intelligence dashboard.
- **Protocol:** `SPEC.md`, `harness/bench.py`, `tasks/`.
- **Competitors:** `competitors/*.json` (validate with `python3 harness/bench.py check`).
- **Tachyon SSOT inside the bench:** `docs/product/` (mirror of product knowledge; not a substitute for inventing features).
- **Charts:** radar/positioning are profile heuristics, not scored runs. See AGENTS.md.

## Claude-specific notes

- Prefer tools that read `~/tachyon` over guessing product capabilities.
- Do not “helpfully” apply fixes inside `~/tachyon` even if a bug is obvious; report findings or mirror allowed public/owned claims into the bench docs.
- If the user asks to change the product, clarify that product work belongs in `~/tachyon` under a separate session/policy — this session’s write scope is **ade-bench only** unless they explicitly change that rule in these files.
