# 013 — competitive-intelligence-battlecards — notes

_Created 2026-07-08._

_In-flight design memory — decisions, deviations, tradeoffs, and open questions surfaced **while building** that weren't pre-empted by `spec.md` or `plan.md`. Append-only by convention._

## Design decisions

- Implemented all five proposed SaaS-inspired blocks in one repo-native layer:
  battlecards, digital/marketing imports, source intelligence, pricing and
  packaging watch, and reproducible collectors.
- Kept signal data language-neutral rather than duplicating per locale. The UI
  chrome is translated; source summaries remain as recorded evidence.

## Deviations

- `attach_evidence` through `tachyon_bridge` timed out after 300 seconds while
  attaching Visual QA artifacts. Screenshots were inspected locally, then
  summarized in the versioned `visual-qa.md` evidence note instead of committing
  binary PNGs.

## Tradeoffs

- The first collector is manual-first. This avoids brittle scraping and paid API
  dependencies while establishing the durable signal contract that future
  adapters can write into.

## Open questions

- Later work should decide whether imported paid-tool reports are stored as CSV
  extracts, raw JSON exports, or normalized signal-only records.

## Visual QA log

### 2026-07-08 — pass

Anchor: battlecards should be an operational, dense, readable dashboard surface
consistent with the existing Tachyon ADE Bench design, with no text overlap or
horizontal overflow on desktop/mobile.

Routes:

- `http://localhost:4322/tachyon-ade-bench/battlecards/`
- `http://localhost:4322/tachyon-ade-bench/pt/battlecards/`

Viewports:

- `1440x1200`
- `390x1200`

Evidence: `docs/specs/013-competitive-intelligence-battlecards/visual-qa.md`.

Verdict: pass. Header, metrics, workflow blocks, and product cards are readable
in both locales. Long signal text wraps inside mobile cards without observed
overlap.

## Dogfood log

### 2026-07-08T22:19:53Z — pass (1/1) — source: tasks.md — commit: 8ba9b91d1906e36e5b2c0d0068d9cd4db270c69b
- `tmp_dir="$(mktemp -d)" && cp -R intelligence "$tmp_dir/intelligence" && python3 scripts/intelligence/add-signal.py --signals-file "$tmp_dir/intelligence/current/signals.json" --product orca --category pricing --source-type manual-research --source-url https://www.onorca.dev/ --summary "Temporary pricing watch dogfood signal." --confidence medium --freshness watch --tag pricing-watch --impact objection --tachyon-response "Keep pricing evidence separate from benchmark claims." && python3 scripts/intelligence/check-intelligence.py --signals-file "$tmp_dir/intelligence/current/signals.json" && rm -rf "$tmp_dir"` — pass

## Verification log

### 2026-07-08T22:19:53Z — pass (3/3) — source: tasks.md
- `scripts/check-suite.sh` — pass
- `npm run dashboard:check` — pass
- `npm run dashboard:build` — pass
