# 006 — acquisition-intelligence-foundation — plan

_Drafted from `spec.md` on 2026-07-07. The approach, not the steps (those go in `tasks.md`)._

## Approach

Create a repo-native acquisition intelligence subsystem under `marketing/` with
tracked registry files and append-only scan/history conventions. Add JSON
schemas for the intended document shapes and dependency-free Python scripts for
validation, normalization, and current-state derivation.

## Key decisions

- **No collectors in v0** — chosen because each platform has different access,
  rate-limit, and regional behavior; rejected scraping first because it would
  make the data contract harder to review.
- **Append-only scan inputs, generated current state** — chosen so historical
  observations are auditable while dashboards can consume compact summaries.
- **Dependency-free Python scripts** — chosen to match the current harness and
  keep GitHub Actions simple.
- **Manual/export raw format first** — chosen because it supports official
  library exports, browser captures, and hand-entered observations before APIs
  exist.

## Files touched

- `marketing/registry/advertisers.json` — product aliases and handles to query.
- `marketing/registry/sources.json` — channel catalog and automation levels.
- `marketing/scans/.gitkeep`, `marketing/history/.gitkeep`,
  `marketing/current/.gitkeep`, `marketing/creatives/.gitkeep` — tracked
  storage roots.
- `schemas/marketing/*.schema.json` — documented data contracts.
- `scripts/marketing/check-marketing.py` — structural validation.
- `scripts/marketing/normalize-scan.py` — raw scan to normalized observations.
- `scripts/marketing/summarize-history.py` — normalized observations to history
  and current derived files.
- `scripts/check-suite.sh` and `.github/workflows/pages.yml` — CI coverage.
- `docs/acquisition-intelligence.md` and `README.md` — workflow docs.

## Risks & unknowns

- Manual raw inputs may drift unless the schema is documented and validated.
- Fingerprints can accidentally merge distinct ads if platform IDs are absent;
  include normalized body, landing URL, creative URL/hash, and platform identity.
- Some platforms expose no stable ad ID, so `inactive` status must be inferred
  from repeated missing observations rather than asserted as fact.

## Visual impact

No visual surface changes. This is repository structure and CLI tooling only.

## Sources consulted

- `docs/acquisition-intelligence.md`
- `harness/bench.py`
- `scripts/check-suite.sh`
- `.github/workflows/pages.yml`
- `competitors/*.json`
