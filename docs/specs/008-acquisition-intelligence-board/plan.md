# 008 — acquisition-intelligence-board — plan

_Drafted from `spec.md` on 2026-07-07. The approach, not the steps (those go in `tasks.md`)._

## Approach

Extend the existing Astro dashboard with a new `/acquisition/` route and matching
`/pt/acquisition/` route. Reuse the current data-loading pattern in `src/lib/data.ts`,
adding typed loaders for `marketing/current/ads.json`, `campaigns.json`,
`coverage.json`, and scan manifests. Render a board that is useful with the current small
dataset and scales when more scans are added: metric strip, scan coverage matrix, campaign
summary cards, representative ad cards, and evidence/limitations panels.

Keep the board static at build time rather than client-heavy. The current data volume does
not require interactive filtering, and static rendering keeps GitHub Pages output auditable.

## Key decisions

- **Static Astro page first** — chosen because the dataset is small and public Pages should be
  easy to audit; rejected a React-heavy board because filters/charts can be added later when
  history grows.
- **Load committed JSON** — chosen because it keeps the board reproducible from repository
  artifacts; rejected hard-coded page literals because they would drift from the acquisition
  data model.
- **Partial remains partial** — chosen because public ad-library reads often expose search
  shells without definitive absence signals; rejected converting missing observations into
  `not-found` because that would overstate the evidence.

## Files touched

- `apps/bench-dashboard/src/lib/types.ts` — add acquisition data types.
- `apps/bench-dashboard/src/lib/data.ts` — add loaders and summaries for marketing data.
- `apps/bench-dashboard/src/lib/i18n.ts` — add English/Portuguese acquisition labels and nav.
- `apps/bench-dashboard/src/layouts/BaseLayout.astro` — add Acquisition to top navigation.
- `apps/bench-dashboard/src/pages/acquisition.astro` — English board route.
- `apps/bench-dashboard/src/pages/pt/acquisition.astro` — Portuguese board route.
- `apps/bench-dashboard/src/styles/global.css` — board layout, metric, status, and ad-card styles.
- `docs/specs/008-acquisition-intelligence-board/*` — spec, plan, tasks, and verification notes.

## Risks & unknowns

- The marketing schema is intentionally lightweight; loaders should tolerate absent current
  files by rendering empty states instead of failing unrelated dashboard work.
- Long ad headlines and URLs can overflow compact cards; visual QA must cover desktop and
  mobile.
- Manifest query statuses and observed ad summaries are related but not identical; copy must
  keep coverage separate from creative observations.

## Visual impact

Adds a new top-level dashboard page with dense operational UI. Visual risks are cramped
tables, badge wrapping, ad cards with long headlines, and language switch/navigation wrapping.
Capture screenshots for `/acquisition/` and `/pt/acquisition/` after implementation.

## Sources consulted

- `apps/bench-dashboard/src/layouts/BaseLayout.astro`
- `apps/bench-dashboard/src/lib/data.ts`
- `apps/bench-dashboard/src/lib/i18n.ts`
- `apps/bench-dashboard/src/lib/types.ts`
- `apps/bench-dashboard/src/pages/index.astro`
- `marketing/current/ads.json`
- `marketing/current/campaigns.json`
- `marketing/current/coverage.json`
- `marketing/scans/20260707T220758Z/manifest.json`
