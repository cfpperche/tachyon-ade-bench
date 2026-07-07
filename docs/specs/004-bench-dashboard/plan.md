# 004 — bench-dashboard — plan

_Drafted from `spec.md` on 2026-07-07. The approach, not the steps (those go in `tasks.md`)._

## Approach

Create an npm workspace in the repo root with an Astro app at
`apps/bench-dashboard`. The app reads `../../competitors/*.json` and task
metadata at build time through TypeScript utilities. Pages render static HTML
for overview, matrix, protocol, sources, and per-competitor profiles. Small
React islands provide interactive filtering and charts.

The app should feel like a dense analytical product surface rather than a
generic landing page: compact header, comparison-first layout, clear source
links, and restrained charts.

Configure Astro with `site` and `base` values suitable for
`https://cfpperche.github.io/tachyon-ade-bench/`. Add a GitHub Actions workflow
that builds the dashboard and deploys `apps/bench-dashboard/dist` with the
official Pages actions.

## Key decisions

- **Astro static build** - chosen because the repo data is tracked and public;
  rejected server rendering because Pages needs static assets.
- **React islands for interactivity** - chosen for filters/charts only, keeping
  the rest of the site static and fast.
- **ECharts for charts** - chosen because it handles multi-dimensional
  analytical views and responsive rendering well.
- **Mermaid as diagram source** - chosen for maintainable protocol diagrams,
  rendered in the page using Mermaid at runtime for v0.1.
- **JSON files stay canonical** - chosen to avoid a second data-maintenance
  channel in Astro page code.

## Files touched

- `package.json` - root npm workspace and dashboard scripts.
- `apps/bench-dashboard/**` - Astro app, data loaders, pages, components, CSS.
- `.github/workflows/pages.yml` - GitHub Pages deployment.
- `README.md` - dashboard usage/deploy notes.
- `docs/specs/004-bench-dashboard/**` - SDD record.

## Risks & unknowns

- GitHub Pages must be enabled in repository settings with source "GitHub
  Actions".
- Astro base path must match `/tachyon-ade-bench/` for the public repo URL.
- Interactive charts must not obscure the more important source/data tables.
- Mobile layout needs explicit inspection because matrix tables can overflow.

## Visual impact

New public dashboard UI. The main visual risks are unreadable dense tables,
charts that fail to render after base-path deployment, and mobile overflow.

## Sources consulted

- `competitors/*.json`
- `docs/competitor-intelligence.md`
- `reports/competitor-map-v0.1.md`
- Existing benchmark README/protocol docs
