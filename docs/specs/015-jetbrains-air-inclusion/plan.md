# 015 — jetbrains-air-inclusion — plan

_Drafted from `spec.md` on 2026-07-21._

## Approach

Create a closed-source manual-runner profile from current official Air and
JetBrains sources. Keep runtime readiness at `needs-install`, feed existing
data-driven dashboard routes from the new profile, and update the few curated
roster, acquisition, intelligence, and SWOT surfaces that are not derived.

Repair the pre-existing Herdr drift encountered in the same surfaces and add a
marketing completeness check so profile/advertiser divergence fails validation
in the future.

## Key decisions

- **ID `jetbrains-air`** — avoids ambiguous `air` searches and keeps acquisition signals attributable.
- **Class A** — Air is a local, multi-agent software ADE rather than an enterprise platform.
- **`needs-install` first** — official availability proves eligibility, not a working run on this host.
- **Local Workspace for v0.1** — keeps product edits inside the harness-owned worktree; Air-created worktrees are a separate future probe.
- **Guest metadata is first-class** — Air, agent, model, effort, authentication, and permission mode must be recorded independently.
- **Current capabilities only** — announced cloud execution and team workflows stay in unknowns/non-goals.

## Files touched

- `competitors/jetbrains-air.json`
- `README.md`
- `SPEC.md`
- `docs/competitor-intelligence.md`
- `docs/acquisition-intelligence.md`
- `reports/competitor-map-v0.1.md`
- `marketing/registry/advertisers.json`
- `scripts/marketing/check-marketing.py`
- `intelligence/current/signals.json`
- `apps/bench-dashboard/src/lib/i18n.ts`
- `docs/specs/015-jetbrains-air-inclusion/*`

## Risks and unknowns

- Fast preview releases can make version-specific claims stale quickly.
- Feature-list heuristics affect radar shape; bullets must represent distinct sourced capabilities, not marketing fragments.
- Generic `Air` acquisition queries create false positives; use product/domain-qualified aliases.
- The current Linux release does not support Docker task execution.
- A GUI login may block hands-on qualification even after catalog inclusion ships.

## Visual impact

Existing data-driven routes gain one competitor profile, matrix row, chart
point/radar toggle, source entries, strategy row, and battlecard. Curated SWOT
copy gains one threat in English and Portuguese. Visual QA covers both locales
and mobile/desktop layouts.

## Sources consulted

- `https://air.dev/`
- `https://air.dev/download`
- `https://air.dev/changelog`
- `https://blog.jetbrains.com/air/2026/03/air-launches-as-public-preview-a-new-wave-of-dev-tooling-built-on-26-years-of-experience/`
- `https://blog.jetbrains.com/air/2026/06/jetbrains-air-lands-on-windows/`
- `https://blog.jetbrains.com/air/2026/07/what-s-new-air-gets-more-agents-local-models-and-java-kotlin-code-intelligence/`
