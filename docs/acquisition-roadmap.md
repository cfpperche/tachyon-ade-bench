# Acquisition Intelligence Roadmap

This roadmap turns the acquisition layer from a snapshot archive into a
repeatable monitoring system. It intentionally keeps marketing evidence separate
from benchmark scores: acquisition signals explain market motion, not product
quality.

## Principles

- Persist history before summarizing conclusions.
- Keep `partial` distinct from `not-found`; lack of a captured result is not
  proof of absence.
- Record source URLs, limitations, and review context with every scan.
- Prefer reproducible public-source checks before API-key integrations.
- Require human review before promoting an ambiguous observation to `found`.

## Phase 1 - Board and Review Loop

Status: active; initial board, scan history, and review queue shipped.

Deliverables:

- Public Acquisition Intelligence board in the Astro dashboard.
- Scan history derived from `marketing/scans/*/manifest.json`.
- Review queue derived from partial, blocked, or ambiguous latest-scan rows.
- Visual evidence links for observed ads.
- Roadmap and evidence rules documented in `docs/`.

Acceptance signals:

- A maintainer can open the dashboard and identify what was found, what remains
  partial, and what should be reviewed next.
- The dashboard can be rebuilt from committed JSON with no manual page edits.

## Phase 2 - Reproducible Manual Runner

Status: planned.

Deliverables:

- A single command for creating a timestamped scan folder.
- Query expansion by advertiser aliases: brand, company name, domain, handle,
  and source-visible org when relevant.
- Per-platform adapters that emit manifest rows even when no normalized ads are
  produced.
- Guardrails for generic-domain false positives such as `github.com`.

Acceptance signals:

- A reviewer can run one documented command and get a complete manifest for all
  tracked products and primary platforms.
- Ambiguous results are queued for review rather than silently discarded.

## Phase 3 - Assisted Evidence Capture

Status: planned.

Deliverables:

- Browser-assisted capture recipes for Google, Meta, LinkedIn, X, TikTok,
  Reddit, Product Hunt, newsletters, YouTube, podcasts, and GitHub Sponsors.
- Screenshot and transcript storage conventions under `marketing/creatives/`.
- Normalization helpers for reviewed findings.
- Duplicate detection by product, platform, source URL, headline, and body hash.

Acceptance signals:

- A reviewed public ad can be traced from board card to normalized record, raw
  scan, source URL, and evidence file.
- Re-running a scan does not duplicate existing creatives unless the creative
  changed.

## Phase 4 - Scheduled Monitoring

Status: planned.

Deliverables:

- GitHub Actions cadence, initially weekly or biweekly.
- Scheduled jobs that create scan manifests and mark blocked/partial states
  without requiring secrets.
- Optional API-key jobs for platforms where credentials are approved.
- Review reports opened as pull requests rather than direct writes to `main`.

Acceptance signals:

- The repository accumulates append-only scan history over time.
- New `found` observations require review before they affect current summaries.

## Phase 5 - Intelligence Reporting

Status: planned.

Deliverables:

- Trend charts for status counts, platform coverage, observed creatives, and
  campaign tags.
- Product-level acquisition profiles.
- Exportable markdown reports for leadership review.
- Clear separation between marketing signal strength and benchmark performance.

Acceptance signals:

- A reader can compare acquisition motion across competitors without confusing
  market activity with product capability.
- Reports include limitations and source references by default.

## Current Review Priorities

1. Resolve Meta public-library coverage, currently partial because no-login
   public pages did not expose definitive result lists.
2. Improve Google domain handling for source-visible projects whose current
   domain hint is too generic.
3. Add LinkedIn/X manual-source recipes before introducing automation.
4. Promote only reviewed evidence into `marketing/current`.
