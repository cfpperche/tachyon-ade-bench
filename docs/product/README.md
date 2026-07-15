# Tachyon product surface (owned canonical source)

This directory is the **owned system of record** for Tachyon capabilities as
far as this benchmark repository is allowed to assert them.

It is intentionally separate from:

- `competitors/tachyon.json` — **derived** research profile for the ADE roster
  and dashboard charts
- `runs/` — **measured** benchmark evidence
- marketing / battlecards — go-to-market narrative

## Rules

1. **Canonical first (inside the bench).** New product claims for the roster
   start here (Markdown + `capabilities.json`), then mirror into
   `competitors/tachyon.json`. Prefer grounding claims by **reading** the
   product repo at `~/tachyon` (and its GitHub remote) — **never write** there.
   See root `AGENTS.md` / `CLAUDE.md`.
2. **No invention.** If a capability is not implemented or not ready to claim,
   mark it `status: not-claimed` or `placeholder`. Do not pad lists to look
   better on the Capability Radar.
3. **Public vs owned.** Do not put private implementation detail here if this
   repo is public and the product is not yet documented elsewhere. Prefer
   benchmark-visible behavior and high-level product intent. Prefer citing
   public product docs/README when they already say it.
4. **Radar axes map 1:1** to groups under `capabilities` in
   `capabilities.json` (same keys as `research.features` in competitor
   profiles).
5. **Dates.** When you change claims, bump `updated_at` in `capabilities.json`
   and, if you re-export to the profile, `research.last_reviewed` /
   `updated_at` on `competitors/tachyon.json`.

## Layout

| Path | Role |
| --- | --- |
| `overview.md` | What Tachyon is (positioning, class, who it is for) |
| `capabilities.md` | Human-readable capability surface by ADE axis |
| `capabilities.json` | Machine-readable SSOT for feature lists / radar |
| `architecture.md` | High-level runtime model (owned, non-private) |
| `workflows.md` | Core operating loops (worktree, handoff, verify) |
| `limits-and-non-goals.md` | Explicit non-claims and out-of-scope |

## Maintainer workflow

1. Edit the relevant Markdown section and/or `capabilities.json`.
2. Keep YAML `items[].name` short and stable (they feed charts if exported).
3. Run `python3 scripts/product/check-capabilities.py` to validate the YAML.
4. Optionally re-sync the owned competitor profile:

   ```sh
   python3 scripts/product/sync-tachyon-profile.py
   python3 harness/bench.py check
   ```

5. Commit docs and profile together when claims change.

## Relationship to the dashboard

The Capability Radar scores **list length** in `competitors/*.json`, not this
folder directly. Until you run the sync script (or hand-update the profile),
enriching docs alone will not move the Tachyon polygon.
