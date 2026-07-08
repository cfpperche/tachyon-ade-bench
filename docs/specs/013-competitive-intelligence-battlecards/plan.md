# 013 — competitive-intelligence-battlecards — plan

_Drafted from `spec.md` on 2026-07-08. The approach, not the steps (those go in `tasks.md`)._

## Approach

Add a new `intelligence/` data layer for competitive signals that are broader
than paid acquisition and more granular than static competitor profiles. Keep the
first version manual-first and reproducible: a JSON schema, current signal file,
CLI helper to append observations, validator in `scripts/check-suite.sh`, and a
dashboard page that turns the records into battlecards.

The five SaaS-inspired workflows map this way:

- **Crayon/Klue:** dashboard battlecards and objection handling.
- **Similarweb/Semrush:** importable signal categories for traffic, SEO, paid
  search, backlinks, and share-of-search observations.
- **AlphaSense/Contify:** each signal carries source URL, source type,
  observed date, confidence, freshness, summary, and evidence fields.
- **CIx/pricing intel:** first-class `pricing` and `packaging` categories.
- **Apify:** reproducible collector shape begins as manual CLI capture and can
  later be extended with scheduled URL snapshots or external actors.

## Key decisions

- **Separate `intelligence/` from `marketing/`** — acquisition remains about
  paid/launch channels; competitive signals can include pricing, packaging,
  feature, stack, market, review, and objection data.
- **Current signal file first** — a compact `intelligence/current/signals.json`
  is enough to render battlecards and validate the model; append-only history can
  come after the shape proves useful.
- **Tool-agnostic source fields** — paid SaaS outputs, manual review, ad
  libraries, SEO tools, and official sources all map to the same signal contract.
- **Battlecards are evidence views** — they summarize source-backed records;
  they do not replace benchmark reports or scored run artifacts.

## Files touched

- `docs/competitive-intelligence.md` — workflow and SaaS-to-repo mapping.
- `schemas/intelligence/signal.schema.json` — signal contract.
- `intelligence/current/signals.json` — seed data.
- `scripts/intelligence/*` — capture and validation tooling.
- `scripts/check-suite.sh` — CI validation.
- `apps/bench-dashboard/src/*` — bilingual battlecards page.
- `docs/specs/013-competitive-intelligence-battlecards/*` — delivery record.

## Risks & unknowns

- Initial signals are curated from existing repo profiles and should be treated
  as seed intelligence, not exhaustive market coverage.
- Without paid APIs, Similarweb/Semrush/AlphaSense-style data stays importable
  but not automatically fetched.
- Battlecard wording can drift from source facts if summaries are not reviewed
  with the same discipline as competitor profiles.

## Visual impact

Adds `/battlecards/` and `/pt/battlecards/` to the Astro dashboard. Visual risk
is dense text crowding on mobile; render cards as responsive grids and avoid
wide-only tables for the primary experience.

## Sources consulted

- `docs/acquisition-intelligence.md`
- `docs/competitor-intelligence.md`
- `apps/bench-dashboard/src/lib/data.ts`
- `apps/bench-dashboard/src/lib/i18n.ts`
- `apps/bench-dashboard/src/components/StrategyBoard.astro`
- `apps/bench-dashboard/src/styles/global.css`
- `scripts/marketing/check-marketing.py`
- `scripts/marketing/add-manual-ad.py`
