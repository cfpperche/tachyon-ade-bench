# 014 — pricing-packaging-watch — plan

_Drafted from `spec.md` on 2026-07-08. The approach, not the steps (those go in `tasks.md`)._

## Approach

Use official product pages, official pricing pages, terms pages, and upstream
repositories to add pricing/packaging signals into
`intelligence/current/signals.json`. Keep claims conservative:

- explicit price or free/open-source language gets `confidence: high` or
  `medium` depending on source strength;
- absent or incomplete pricing becomes `freshness: watch`;
- source URLs point to the page that supports the short summary.

## Key decisions

- **Signals, not a table** — the current dashboard is evidence-first; normalized
  pricing tables should come only after repeated snapshots and enough comparable
  fields.
- **Official-only for current facts** — search snippets and third-party pages can
  guide discovery, but stored signals point to official project/vendor pages.
- **Preserve ambiguity** — when a page says "free" but the product also has Pro,
  record both the free entry point and the need to refresh plan limits.

## Files touched

- `intelligence/current/signals.json` — add product-level pricing/packaging signals.
- `docs/competitive-intelligence.md` — add pricing watch update guidance.
- `docs/specs/014-pricing-packaging-watch/*` — delivery record.

## Risks & unknowns

- Pricing pages can change quickly; these signals must be refreshed before
  public sales use.
- Some projects publish packaging/license facts but no commercial pricing.
- Hive/HiveTerm naming is easy to confuse; source URLs must match the tracked
  competitor ids.

## Visual impact

No new UI component. Existing battlecards will show more signal rows. Visual QA
is covered by dashboard build and the prior battlecards responsive check.

## Sources consulted

- `intelligence/current/signals.json`
- `docs/competitive-intelligence.md`
- Official competitor homepages, pricing pages, terms pages, and source repos.
