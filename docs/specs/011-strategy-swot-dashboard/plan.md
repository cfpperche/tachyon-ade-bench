# 011 — strategy-swot-dashboard — plan

_Drafted from `spec.md` on 2026-07-08. The approach, not the steps (those go in `tasks.md`)._

## Approach

Add a new Strategy page in the Astro dashboard with shared component rendering for EN/PT.
Add localized copy for Tachyon SWOT, competitor pressure-axis labels, and strategic bets.
Add a small derived strategy helper in `data.ts` that maps competitor profiles into pressure
signals using existing features/readiness/class/source/acquisition data.

## Key decisions

- **Strategy page, not benchmark score** — chosen because no scored product runs exist yet;
  rejected ranking competitors because it would overstate current evidence.
- **Localized copy in `i18n.ts`** — chosen to match the existing dashboard pattern; rejected a
  separate markdown renderer to avoid adding a content system for one page.
- **Derived pressure rows** — chosen so every tracked competitor appears automatically; rejected
  hand-written competitor table rows that could drift as profiles change.

## Files touched

- `apps/bench-dashboard/src/components/StrategyBoard.astro` — shared strategy page UI.
- `apps/bench-dashboard/src/pages/strategy.astro` — English route.
- `apps/bench-dashboard/src/pages/pt/strategy.astro` — Portuguese route.
- `apps/bench-dashboard/src/layouts/BaseLayout.astro` — navigation link.
- `apps/bench-dashboard/src/lib/i18n.ts` — localized strategy copy.
- `apps/bench-dashboard/src/lib/types.ts` — pressure-row type.
- `apps/bench-dashboard/src/lib/data.ts` — derive pressure rows from competitor/acquisition data.
- `apps/bench-dashboard/src/styles/global.css` — SWOT, pressure, and bet styles.
- `docs/specs/011-strategy-swot-dashboard/*` — spec tracking.

## Risks & unknowns

- Long SWOT statements can overcrowd cards on mobile.
- Pressure axes are strategic heuristics, not measured scores; labels must make that clear.
- Navigation now has more items and must still wrap cleanly.

## Visual impact

Adds a new top-level dashboard page and nav item. Capture desktop and mobile screenshots for
English/Portuguese routes.

## Sources consulted

- `competitors/*.json`
- `marketing/current/campaigns.json`
- `apps/bench-dashboard/src/lib/data.ts`
- `apps/bench-dashboard/src/lib/i18n.ts`
- `apps/bench-dashboard/src/layouts/BaseLayout.astro`
- `docs/specs/008-acquisition-intelligence-board/*`
- `docs/specs/009-acquisition-roadmap-history-queue/*`
