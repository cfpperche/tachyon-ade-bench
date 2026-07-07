# 003 — competitor-intel — plan

_Drafted from `spec.md` on 2026-07-07. The approach, not the steps (those go in `tasks.md`)._

## Approach

Extend the competitor profile contract with a nested `research` object. Keep
claims conservative: sourced facts are recorded separately from hypotheses and
unknowns. Update the harness validation to reject profiles without research
sources and required research sections.

Populate the first v0.1 dataset from official product pages, docs, GitHub
READMEs, and package manifests where available. Then add maintainer docs and a
human-readable report that summarizes stack, infrastructure, capabilities,
moat, and benchmark-readiness.

## Key decisions

- **Structured JSON first** - chosen because benchmark runners and reports can
  consume the data later; rejected markdown-only notes because they are harder
  to validate.
- **Official sources only for factual claims** - chosen because competitor data
  is volatile and reputationally sensitive; rejected community posts except as
  optional leads.
- **Confidence and unknowns are first-class** - chosen because closed-source
  products expose less stack detail; rejected guessing implementation internals.
- **Report from curated data** - chosen because the report should explain the
  dataset, not become the only source of truth.

## Files touched

- `schemas/competitor.schema.json` - document the enriched research contract.
- `harness/bench.py` - validate minimal research completeness.
- `competitors/*.json` - populate research sections for the initial roster.
- `docs/competitor-intelligence.md` - update workflow and field meanings.
- `reports/competitor-map-v0.1.md` - concise comparison matrix.
- `docs/specs/003-competitor-intel/**` - SDD record.

## Risks & unknowns

- Official pages can change quickly; every profile records `last_reviewed`.
- Closed-source products may not publish stack details; record unknowns instead
  of inferring.
- Some products are not equal classes: Augment remains Class B enterprise and
  should not be mixed into a Class A leaderboard without caveats.
- Stack claims from package manifests can identify dependencies but not runtime
  architecture by themselves.

## Visual impact

No live UI surface changes. This spec adds docs, JSON data, and reports.

## Sources consulted

- `competitors/*.json`
- `schemas/competitor.schema.json`
- `harness/bench.py`
- Official product pages/docs/READMEs listed in each competitor profile source list
