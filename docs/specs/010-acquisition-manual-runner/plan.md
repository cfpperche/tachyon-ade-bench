# 010 — acquisition-manual-runner — plan

_Drafted from `spec.md` on 2026-07-07. The approach, not the steps (those go in `tasks.md`)._

## Approach

Add `scripts/marketing/plan-scan.py`. The script reads `marketing/registry/advertisers.json`
and `marketing/registry/sources.json`, expands query fields per platform, builds deterministic
source URLs for public library surfaces, and writes a scan manifest through existing
`common.py` helpers. It supports platform/product filters, `--scan-id`, `--country`,
`--output-root`, `--dry-run`, and `--limit-primary`.

## Key decisions

- **Planner, not scraper** — chosen because Phase 2 is about reproducible review setup;
  rejected live scraping because platform behavior varies by region/login and belongs in
  assisted evidence capture.
- **Registry-driven expansion** — chosen because aliases are already curated; rejected
  hard-coded product logic.
- **Existing manifest schema** — chosen so the board/review queue works immediately;
  rejected new schema fields for now to keep CI stable.

## Files touched

- `scripts/marketing/plan-scan.py` — new reproducible scan planner.
- `docs/acquisition-roadmap.md` — Phase 2 command documentation.
- `docs/acquisition-intelligence.md` — usage pointer.
- `docs/specs/010-acquisition-manual-runner/*` — spec tracking.

## Risks & unknowns

- Source URL formats are best-effort public entry points, not proof a page will render results.
- Query expansion can be noisy for generic product names; exact names and domains are preferred.
- Current manifest schema cannot store reason metadata per row; limitations must describe guardrails.

## Visual impact

No direct UI changes. The board will pick up generated manifests when committed.
**Visual QA Opt-Out:** command-line planner only.

## Sources consulted

- `scripts/marketing/common.py`
- `scripts/marketing/new-scan.py`
- `marketing/registry/advertisers.json`
- `marketing/registry/sources.json`
- `schemas/marketing/scan-manifest.schema.json`
- `docs/acquisition-roadmap.md`
