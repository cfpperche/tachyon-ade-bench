# 013 — competitive-intelligence-battlecards — tasks

_Generated from `plan.md` on 2026-07-08. Work top-to-bottom. Check boxes as tasks complete. If a task reveals the plan is wrong, update `plan.md` before continuing._

## Implementation

- [x] Add competitive-intelligence documentation and five-block workflow mapping.
- [x] Add signal schema and seed current signals.
- [x] Add validation and manual capture scripts.
- [x] Wire competitive-intelligence validation into `scripts/check-suite.sh`.
- [x] Add dashboard data types and loader.
- [x] Add bilingual battlecards page and navigation.
- [x] Add responsive styles for battlecards.

## Verification

- [x] `python3 scripts/intelligence/check-intelligence.py` passes.
- [x] Capture helper can append a valid signal to a temporary copy.
- [x] `scripts/check-suite.sh` passes.
- [x] `npm run dashboard:check` passes.
- [x] `npm run dashboard:build` passes.

**Headless check:** `scripts/check-suite.sh && npm run dashboard:check && npm run dashboard:build`

**Verify:** `scripts/check-suite.sh`
**Verify:** `npm run dashboard:check`
**Verify:** `npm run dashboard:build`

## Dogfood

**Dogfood:** `tmp_dir="$(mktemp -d)" && cp -R intelligence "$tmp_dir/intelligence" && python3 scripts/intelligence/add-signal.py --signals-file "$tmp_dir/intelligence/current/signals.json" --product orca --category pricing --source-type manual-research --source-url https://www.onorca.dev/ --summary "Temporary pricing watch dogfood signal." --confidence medium --freshness watch --tag pricing-watch --impact objection --tachyon-response "Keep pricing evidence separate from benchmark claims." && python3 scripts/intelligence/check-intelligence.py --signals-file "$tmp_dir/intelligence/current/signals.json" && rm -rf "$tmp_dir"`

**Human dogfood:** Open `/battlecards/` and `/pt/battlecards/` in the dashboard and confirm that cards are readable on desktop and mobile.

## Visual QA

- [x] Evidence: `docs/specs/013-competitive-intelligence-battlecards/visual-qa.md`
- [x] Verdict: pass — responsive layout is readable in EN/PT at desktop and mobile widths, with no observed overlap or horizontal overflow.
