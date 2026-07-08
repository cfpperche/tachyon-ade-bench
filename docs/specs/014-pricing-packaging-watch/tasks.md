# 014 — pricing-packaging-watch — tasks

_Generated from `plan.md` on 2026-07-08. Work top-to-bottom. Check boxes as tasks complete. If a task reveals the plan is wrong, update `plan.md` before continuing._

## Implementation

- [x] Research official pricing/packaging sources for the tracked ADE roster.
- [x] Add conservative pricing/packaging signals to `intelligence/current/signals.json`.
- [x] Update competitive-intelligence documentation with pricing-watch workflow.
- [x] Record source/caveat notes in `notes.md`.

## Verification

- [x] `python3 scripts/intelligence/check-intelligence.py` passes.
- [x] `scripts/check-suite.sh` passes.
- [x] `npm run dashboard:check` passes.
- [x] `npm run dashboard:build` passes.

**Headless check:** `scripts/check-suite.sh && npm run dashboard:check && npm run dashboard:build`

**Verify:** `scripts/check-suite.sh`
**Verify:** `npm run dashboard:check`
**Verify:** `npm run dashboard:build`

## Dogfood

**Dogfood:** `python3 -c 'import json; from pathlib import Path; data=json.loads(Path("intelligence/current/signals.json").read_text()); products={s["product_id"] for s in data["signals"] if s["category"] in {"pricing","packaging"}}; required={"agentsroom","augment-code","hive","hiveterm","kandev","openade","orca","t3-code"}; missing=sorted(required-products); assert not missing, f"missing pricing/packaging signals: {missing}"; print("OK: pricing/packaging signals cover tracked competitors")'`

**Human dogfood:** Open `/battlecards/` and confirm pricing/packaging signals are visible under product cards.

## Visual QA

**Visual QA Opt-Out:** no new UI surface; existing battlecards cards receive more data rows and dashboard build exercises route generation.
