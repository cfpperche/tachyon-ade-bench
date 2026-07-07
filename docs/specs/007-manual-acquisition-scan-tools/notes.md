# 007 — manual-acquisition-scan-tools — notes

_Created 2026-07-07._

_In-flight design memory — decisions, deviations, tradeoffs, and open questions surfaced **while building** that weren't pre-empted by `spec.md` or `plan.md`. Append-only by convention._

## Design decisions

- Helper commands accept `--output-root` so smoke tests can write under
  `runs/` without polluting tracked `marketing/scans/`.

## Deviations

- None so far.

## Tradeoffs

- Duplicate raw ad entries are not prevented yet. The next real scan can show
  whether a dedupe guard should compare platform IDs or fingerprints at entry
  time.

## Open questions

- None.

## Dogfood log

### 2026-07-07T21:17:11Z — pass (1/1) — source: tasks.md — commit: a0cf9aaee1660322b64ec42faf3b17180e72194d
- `bash -lc 'rm -rf runs/manual-scan-smoke && scripts/marketing/new-scan.py --scan-id 20260707T210000Z --product agentsroom --platform google --query AgentsRoom --source-url https://adstransparency.google.com/ --output-root runs/manual-scan-smoke && scripts/marketing/add-not-found.py --scan-id 20260707T210000Z --product augment-code --platform meta --query "Augment Code" --source-url https://www.facebook.com/ads/library/ --output-root runs/manual-scan-smoke && scripts/marketing/add-manual-ad.py --scan-id 20260707T210000Z --product agentsroom --platform google --advertiser-name AgentsRoom --source-url https://adstransparency.google.com/example --landing-url https://agentsroom.dev/pt --headline "Coordinate coding agents" --body "Run many agents across projects." --cta "Try now" --country US --claim multi-agent --tag orchestration --output-root runs/manual-scan-smoke && python3 scripts/marketing/check-marketing.py'` — pass

## Verification log

### 2026-07-07T21:17:11Z — pass (2/2) — source: tasks.md
- `python3 scripts/marketing/check-marketing.py` — pass
- `scripts/check-suite.sh` — pass
