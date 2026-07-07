# 003 — competitor-intel — notes

_Created 2026-07-07._

_In-flight design memory — decisions, deviations, tradeoffs, and open questions surfaced **while building** that weren't pre-empted by `spec.md` or `plan.md`. Append-only by convention._

## Design decisions

_Choices made where the spec/plan was ambiguous. The decision + why this option over the others considered in the moment._

- 2026-07-07: Kept `competitors/*.json` as the source of truth and made
  `reports/competitor-map-v0.1.md` a curated summary. This keeps future
  benchmark tooling able to consume the data directly.
- 2026-07-07: Used only official/vendor/project sources for factual claims.
  Closed-source implementation details are captured as `unknowns` rather than
  inferred.
- 2026-07-07: Kept Augment Code in the roster as Class B
  `enterprise-gated`, but excluded it from the first direct Class A comparison
  set in the report.
- 2026-07-07: Kept LandingAI excluded because its ADE means Agentic Document
  Extraction, not a software development environment competitor.

## Deviations

_Where implementation intentionally departed from `plan.md`, and why it was necessary or better._

- 2026-07-07: Added stricter harness checks for source kind, source URI shape,
  `last_reviewed`, `positioning`, and `infrastructure` so the Python validator
  stays closer to `schemas/competitor.schema.json`.

## Tradeoffs

_Alternatives weighed mid-build. The chosen path + what was given up + why it was worth it._

- 2026-07-07: Did not attempt hands-on installs of competitors in this spec.
  The repo now has enough research structure to choose install order, but
  scored benchmark evidence is still intentionally absent.
- 2026-07-07: Tachyon's public profile uses `owned/internal` placeholders
  instead of private stack details. This preserves public report hygiene until
  public Tachyon docs/source links exist.

## Open questions

_Questions surfaced during the build with no answer yet. Owner or path to resolution if known._

- Which Class A product should be the first manual run: Orca, HiveTerm,
  AgentsRoom, OpenADE, Kandev, T3 Code, or Hive?

## Sources reviewed

- Orca: `https://github.com/stablyai/orca`,
  `https://raw.githubusercontent.com/stablyai/orca/main/package.json`,
  `https://www.onorca.dev/docs/remote-servers`,
  `https://www.onorca.dev/docs/agents/custom-cli`.
- HiveTerm: `https://hiveterm.com/`, `https://hiveterm.com/agents/`,
  `https://hiveterm.com/docs/`, `https://hiveterm.com/compare/t3/`.
- T3 Code: `https://t3.codes/`, `https://github.com/pingdotgg/t3code`,
  `https://raw.githubusercontent.com/pingdotgg/t3code/main/package.json`,
  `https://pingdotgg-t3code.mintlify.app/installation`.
- Hive: `https://hivehq.dev/en/`, `https://github.com/tt-a1i/hive`.
- AgentsRoom: `https://agentsroom.dev/pt`.
- Augment Code: `https://www.augmentcode.com/`,
  `https://docs.augmentcode.com/introduction`,
  `https://docs.augmentcode.com/cli/overview`,
  `https://www.augmentcode.com/context-engine`,
  `https://docs.augmentcode.com/context-services/mcp/overview`.
- OpenADE / ADE App: `https://openade.ai/`,
  `https://www.ade-app.dev/`, `https://github.com/bearlyai/OpenADE`.
- Kandev: `https://github.com/kdlbs/kandev`,
  `https://raw.githubusercontent.com/kdlbs/kandev/main/README.md`,
  `https://raw.githubusercontent.com/kdlbs/kandev/main/docs/features.md`.

## Verification log

- 2026-07-07: `python3 -m py_compile harness/bench.py` passed.
- 2026-07-07: `python3 harness/bench.py check` passed.
- 2026-07-07: `scripts/check-suite.sh` passed.
- 2026-07-07: `scripts/smoke.sh` passed.

## Review log

- 2026-07-07: Claude CLI review found no blocking issues, but flagged harness
  schema-divergence risks, a future task placeholder in
  `suggested_first_tasks`, an omitted Orca source in the report, a Hive license
  SPDX nit, and one editorial HiveTerm claim. The follow-up patch tightened
  validator type/extra-key/source-note checks, validated suggested task IDs,
  removed the future task placeholder, added the Orca package-manifest source
  to the report, normalized Hive to `BUSL-1.1`, and changed HiveTerm's agent
  support text to `Antigravity`.

## Dogfood log

### 2026-07-07T18:28:09Z — pass (1/1) — source: tasks.md — commit: f8f38319d79b025af3da0e797b45354fbf0480da
- `python3 harness/bench.py list-products` — pass

### 2026-07-07T18:28:09Z — pass (3/3) — source: tasks.md
- `python3 harness/bench.py check` — pass
- `scripts/check-suite.sh` — pass
- `scripts/smoke.sh` — pass

### 2026-07-07T18:34:27Z — pass (1/1) — source: tasks.md — commit: f8f38319d79b025af3da0e797b45354fbf0480da
- `python3 harness/bench.py list-products` — pass

### 2026-07-07T18:34:27Z — pass (3/3) — source: tasks.md
- `python3 harness/bench.py check` — pass
- `scripts/check-suite.sh` — pass
- `scripts/smoke.sh` — pass

### 2026-07-07T18:35:37Z — pass (1/1) — source: tasks.md — commit: f8f38319d79b025af3da0e797b45354fbf0480da
- `python3 harness/bench.py list-products` — pass

### 2026-07-07T18:35:37Z — pass (3/3) — source: tasks.md
- `python3 harness/bench.py check` — pass
- `scripts/check-suite.sh` — pass
- `scripts/smoke.sh` — pass
