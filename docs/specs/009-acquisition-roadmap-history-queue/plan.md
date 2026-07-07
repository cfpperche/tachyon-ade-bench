# 009 — acquisition-roadmap-history-queue — plan

_Drafted from `spec.md` on 2026-07-07. The approach, not the steps (those go in `tasks.md`)._

## Approach

Add `docs/acquisition-roadmap.md` as the durable roadmap, linked conceptually from the
existing acquisition docs. Extend the dashboard acquisition data loader to derive scan
history from every manifest and review items from latest scan rows whose result is not a
confirmed `found`/`not-found`. Render two new static board sections in the existing
`AcquisitionBoard.astro`: Scan History and Review Queue.

## Key decisions

- **Roadmap as docs, not issue text** — chosen because the repo is public and should carry
  the repeatability plan with the benchmark artifacts; rejected only keeping it in chat
  because it would not guide future scans.
- **Derive queue from manifests** — chosen because it makes the queue reproducible from
  committed data; rejected a hand-maintained queue because it would drift.
- **Static board sections** — chosen because the dataset is small and build-time rendering
  is enough for the current phase; rejected interactive filters until history volume grows.

## Files touched

- `docs/acquisition-roadmap.md` — phased roadmap for acquisition intelligence.
- `apps/bench-dashboard/src/lib/types.ts` — scan history and review queue types.
- `apps/bench-dashboard/src/lib/data.ts` — derived history/queue summaries.
- `apps/bench-dashboard/src/lib/i18n.ts` — localized labels for new sections.
- `apps/bench-dashboard/src/components/AcquisitionBoard.astro` — render history and queue.
- `apps/bench-dashboard/src/styles/global.css` — section layout/card styles.
- `docs/specs/009-acquisition-roadmap-history-queue/*` — spec tracking.

## Risks & unknowns

- Older manifests may have different degrees of detail; summary derivation should tolerate
  absent optional fields.
- Review queue could be noisy if it lists every partial row; cap it or make reasons concise
  if the list becomes too long later.
- Mobile tables must remain readable with many scan rows.

## Visual impact

Adds two new sections to the acquisition board. Main visual risks are vertical length and
table/card density on mobile. Capture English desktop and Portuguese mobile screenshots.

## Sources consulted

- `docs/acquisition-intelligence.md`
- `docs/specs/008-acquisition-intelligence-board/*`
- `marketing/scans/*/manifest.json`
- `apps/bench-dashboard/src/components/AcquisitionBoard.astro`
- `apps/bench-dashboard/src/lib/data.ts`
- `apps/bench-dashboard/src/lib/i18n.ts`
