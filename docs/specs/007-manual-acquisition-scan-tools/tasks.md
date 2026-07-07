# 007 — manual-acquisition-scan-tools — tasks

_Generated from `plan.md` on 2026-07-07. Work top-to-bottom. Check boxes as tasks complete. If a task reveals the plan is wrong, update `plan.md` before continuing._

## Implementation

- [x] Add `new-scan.py`.
- [x] Add `add-not-found.py`.
- [x] Add `add-manual-ad.py`.
- [x] Document the manual helper workflow.
- [x] Dogfood helpers on a synthetic scan under `runs/`.

## Verification

- [x] `python3 scripts/marketing/check-marketing.py` passes.
- [x] Synthetic helper workflow creates valid manifest, raw, and normalized files.
- [x] `scripts/check-suite.sh` passes.

**Headless check:** `python3 scripts/marketing/check-marketing.py && scripts/check-suite.sh`
**Verify:** `python3 scripts/marketing/check-marketing.py`
**Verify:** `scripts/check-suite.sh`

## Dogfood

**Dogfood:** `bash -lc 'rm -rf runs/manual-scan-smoke && scripts/marketing/new-scan.py --scan-id 20260707T210000Z --product agentsroom --platform google --query AgentsRoom --source-url https://adstransparency.google.com/ --output-root runs/manual-scan-smoke && scripts/marketing/add-not-found.py --scan-id 20260707T210000Z --product augment-code --platform meta --query "Augment Code" --source-url https://www.facebook.com/ads/library/ --output-root runs/manual-scan-smoke && scripts/marketing/add-manual-ad.py --scan-id 20260707T210000Z --product agentsroom --platform google --advertiser-name AgentsRoom --source-url https://adstransparency.google.com/example --landing-url https://agentsroom.dev/pt --headline "Coordinate coding agents" --body "Run many agents across projects." --cta "Try now" --country US --claim multi-agent --tag orchestration --output-root runs/manual-scan-smoke && python3 scripts/marketing/check-marketing.py'`

**Human dogfood:** Use the documented helper workflow for the first real Google
or Meta scan.

## Visual QA

**Visual QA Opt-Out:** CLI/docs/data only.
