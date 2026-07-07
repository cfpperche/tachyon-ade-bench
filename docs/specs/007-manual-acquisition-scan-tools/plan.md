# 007 — manual-acquisition-scan-tools — plan

_Drafted from `spec.md` on 2026-07-07. The approach, not the steps (those go in `tasks.md`)._

## Approach

Add small dependency-free Python helpers that write the already-defined
marketing scan formats. They should be composable: start a scan, append
manifest query results, append manual ad entries, run normalization, and then
use the existing summarizer.

## Key decisions

- **Helpers write JSON, not scrape pages** — chosen to keep the first real scan
  auditable and low-risk; rejected platform automation until raw field stability
  is proven.
- **`add-manual-ad.py` invokes the normalizer** — chosen so raw and normalized
  records stay in sync; rejected requiring a second manual command for the most
  common path.
- **Manifest is updated incrementally** — chosen because a scan can cover many
  products/platforms over one session.

## Files touched

- `scripts/marketing/new-scan.py` — create a scan manifest and platform dir.
- `scripts/marketing/add-not-found.py` — append negative query evidence.
- `scripts/marketing/add-manual-ad.py` — append a raw ad and normalize it.
- `docs/acquisition-intelligence.md` — document manual helper workflow.
- `docs/specs/007-manual-acquisition-scan-tools/*` — spec record.

## Risks & unknowns

- CLI arguments can become too verbose; use explicit flags now and refine after
  the first real scan.
- Raw files can receive duplicate ads; allow this for now because normalization
  fingerprints observations and history summarization groups by fingerprint.

## Visual impact

No visual impact. CLI/docs/data only.

## Sources consulted

- `docs/acquisition-intelligence.md`
- `scripts/marketing/normalize-scan.py`
- `scripts/marketing/check-marketing.py`
- `marketing/registry/*.json`
