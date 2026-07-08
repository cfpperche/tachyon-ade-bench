# 014 — pricing-packaging-watch — notes

_Created 2026-07-08._

_In-flight design memory — decisions, deviations, tradeoffs, and open questions surfaced **while building** that weren't pre-empted by `spec.md` or `plan.md`. Append-only by convention._

## Design decisions

- Added product-level pricing/packaging signals instead of a normalized pricing
  table. This keeps source-backed observations visible without pretending all
  products expose comparable commercial terms.
- Used `freshness: watch` for AgentsRoom because the same official page exposed
  both a free/Pro FAQ and copy saying the product never charges.

## Deviations

- None.

## Tradeoffs

- Official site snippets and pages were enough for this pass. No paid SaaS/API
  exports were used, so traffic and demand data remain out of scope.
- Shell expansion removed dollar amounts in two CLI-created summaries during the
  first insertion. The JSON was corrected directly and the documentation now
  warns to single-quote or escape dollar amounts.

## Open questions

- Future work should decide whether pricing snapshots preserve raw HTML/hash
  evidence alongside normalized signals.

## Source notes

- Orca: official homepage supports free/open-source and BYO subscription claims.
- T3 Code: official homepage supports free/open-source, MIT, and BYO subscription claims.
- AgentsRoom: official homepage supports free tier/Pro pricing claims but has
  internally inconsistent copy, so the signal remains watch.
- Augment Code: official pricing page supports Business and Enterprise pricing.
- HiveTerm: official homepage and terms support Free/Pro/BYO claims.
- Hive: official homepage supports local, no account/key, BYO CLI login, BSL
  packaging claims.
- OpenADE: official homepage supports free download, open source, no login/cloud,
  and local/offline packaging claims.
- Kandev: upstream GitHub repository supports AGPL, self-hostable, no telemetry
  packaging claims.

## Dogfood log

### 2026-07-08T23:37:49Z — fail (0/1) — source: tasks.md — commit: fe0c782342c14be03f5ce1a32940fa4b9932a6da
- `27:**Dogfood:** `python3 - <<'PY'` — fail


### 2026-07-08T23:38:11Z — pass (1/1) — source: tasks.md — commit: fe0c782342c14be03f5ce1a32940fa4b9932a6da
- `python3 -c 'import json; from pathlib import Path; data=json.loads(Path("intelligence/current/signals.json").read_text()); products={s["product_id"] for s in data["signals"] if s["category"] in {"pricing","packaging"}}; required={"agentsroom","augment-code","hive","hiveterm","kandev","openade","orca","t3-code"}; missing=sorted(required-products); assert not missing, f"missing pricing/packaging signals: {missing}"; print("OK: pricing/packaging signals cover tracked competitors")'` — pass
## Verification log

### 2026-07-08T23:37:49Z — pass (3/3) — source: tasks.md
- `scripts/check-suite.sh` — pass
- `npm run dashboard:check` — pass
- `npm run dashboard:build` — pass
