# Competitor Profiles

Each JSON file describes a product that can be benchmarked. These profiles are
not scores. They are the source of truth for setup, inclusion rationale,
research sources, stack signals, feature groups, moat hypotheses, and benchmark
readiness.

Claims that affect public comparison should be verified against current product
documentation before a scored report is published.

Maintainer workflow:

- Read `docs/competitor-intelligence.md` before adding or changing claims.
- Keep factual claims sourced to official pages, docs, repositories, package
  manifests, app stores, or owned Tachyon docs.
- Put unknown implementation details in `research.stack.unknowns` or
  `research.moat.unknowns` instead of guessing.
- Update `research.last_reviewed`, `research.confidence`, `research_status`,
  and `updated_at` in the same change.

Current map: `reports/competitor-map-v0.1.md`.
