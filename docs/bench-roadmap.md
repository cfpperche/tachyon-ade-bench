# ADE Bench Near-Term Roadmap

**Status:** draft for maintainer approval (recorded 2026-08-11)  
**Scope:** this repository (`tachyon-ade-bench`) unless a row explicitly names the product monorepo  
**Related:** `docs/competitor-runbook.md`, `docs/competitor-intelligence.md`, `docs/acquisition-roadmap.md` (acquisition only), `docs/run-report-metrics.md`

This roadmap is **working intuition**, not a scored plan and not a substitute for Board tasks in the product repo. Refine by editing this file; do not let dashboard radar heuristics pretend to be delivery evidence.

## Principles

- **Roster honest and publishable** — public site is a static build from `main`; every new `competitors/*.json` needs an advertiser row and roster prose.
- **Comparison language before pretty charts** — answer “guest CLI harness vs own agent loop” with structured data, not only conversation.
- **Harness evidence > radar polygons** — capability radar is a feature-list heuristic; real quality lives in `runs/` + verifiers.
- **Do not invent Tachyon features** in competitor JSON; product claims go `~/tachyon` (read) → `docs/product/` → sync scripts.
- **Agent pane / product composer work** is owned in the product monorepo when accepted there; this file only tracks the dependency so the bench does not steal that thread.

## Legend

| Tag | Meaning |
| --- | --- |
| **P0** | Do early |
| **P1** | High value after P0 |
| **P2** | When capacity allows |
| **//** | Can run in parallel |
| **→** | Depends on prior item |

## North star (why this order)

1. Ship what is already researched (catalog live on Pages).
2. Formalize **runtime model** so battlecards and fair scoring stay honest.
3. Measure a few peers with fixed dimensions (guest runtime + ADE product).
4. Leave product agent-pane composer to the assigned product agent unless reassigned.

---

## Phase 0 — Close in-flight catalog work

**Status:** profiles committed on branch `catalog/xirp-emdash-copilot-app-macro-exclude` (2026-08-11); **not** assumed merged to `main` until verified.

| ID | Item | Where | Done when |
| --- | --- | --- | --- |
| **0.1 P0** | Push + PR (or maintainer merge) of catalog branch | git / GitHub | PR open or landed on `main` |
| **0.2 P0** | After merge: confirm GitHub Pages | CI + site | `/competitors/xirp/`, `emdash/`, `github-copilot-app/` live; Macro **not** Class A |
| **0.3 P0** | Project handoff note if merge changes shared state | Bridge / HANDOFF | One durable note if applicable |

**In this change set (branch):**

- Catalog Class A: **Xirp**, **Emdash**, **GitHub Copilot app**
- Exclude (documented): **Macro** (agentic office suite / company OS, not software ADE control plane)
- Advertisers + roster: `docs/competitor-intelligence.md`, `reports/competitor-map-v0.1.md`, `README.md`, `SPEC.md`

**Do not in Phase 0:** hand-tune radar scores; invent feature bullets; re-open product agent-pane implementation from the bench.

---

## Phase 1 — Runtime model (guest vs own)

**Status:** shipped 2026-08-11 (enum + lists + dashboard filter/badge; map table column still optional polish).  
**Goal:** machine-readable answer to “who orchestrates third-party coding CLIs vs who owns a coding agent loop?”

| ID | Item | Done when |
| --- | --- | --- |
| **1.1 P0** | Spec the field (short doc section or schema comments) | Stable enum: `guest-cli` · `hybrid` · `first-party` (optional `unknown`) — **done** (`docs/competitor-intelligence.md`) |
| **1.2 P0** | Add field to schema + fill every `competitors/*.json` | `python3 harness/bench.py check` green — **done** |
| **1.3 P1** | Optional `guest_runtimes[]` / `own_runtimes[]` | Filled on all profiles — **done** |
| **1.4 P1** | Map and/or dashboard badge/filter | Matrix filter + profile badge — **done**; map markdown column optional |
| **1.5 P2** | Method note: single-task correctness often measures guest agent | Caveat in `SPEC.md` and/or competitor map |

### Initial classification heuristic (validate when filling)

Re-check each profile against official sources at fill time; this table is a starting point only.

| Model | Meaning | Initial peers (illustrative) |
| --- | --- | --- |
| **guest-cli** | Control plane; coding loop is external CLI (BYO) | Tachyon, Orca, Conductor, Emdash, Xirp, T3 Code, Synara, Hive, HiveTerm, Herdr, Maestri, AgentsRoom, OpenADE, Kandev, Overclock |
| **hybrid** | First-party agent **and** third-party CLIs | Warp, JetBrains Air, Falou, Fusion, GitHub Copilot app |
| **first-party** | Own agent loop is the primary coding path | Kiro; Augment Code (Class B platform) |

Notes:

- Hive / HiveTerm may have strong orchestration of their own; coding execution remains guest CLI → prefer **guest-cli** with a one-line note if needed.
- Fusion mixes Pi/providers with ACP CLI paths → **hybrid** until a hands-on pass says otherwise.
- Conductor “first-party support” means first-class **integration** of guest CLIs, not an owned coding model.

---

## Phase 2 — Roster and research hygiene

**Status:** continuous, small slices.

| ID | Item | Priority | Notes |
| --- | --- | --- | --- |
| **2.1** | Enrich **AgentsRoom** profile: own composer over xterm.js PTY; not an agent harness | P1 | Official `llms.txt` / site only |
| **2.2** | Re-review **Xirp** when beta leaves macOS-only | P2 | OS matrix / readiness |
| **2.3** | Watchlist only: HumanLayer; Macro adjacency (MCP workspace) | P2 | Macro already excluded |
| **2.4** | Periodic `last_reviewed` for hot Class A (Warp, Kiro, Copilot app, Emdash, Xirp) | P2 | Follow competitor runbook |
| **2.5** | Short battlecards: Tachyon vs Emdash / Xirp / Copilot app | P1 | `docs/competitive-intelligence.md` / intelligence layer |

---

## Phase 3 — Harness evidence (not radar)

**Status:** planned.  
**Goal:** comparable runs with dimensions that separate ADE chrome from guest model quality.

| ID | Item | Priority | Done when |
| --- | --- | --- | --- |
| **3.1** | Smoke **Emdash** on Linux (e.g. T001) | P1 | Local `runs/…` + parity note on profile (gitignored runs stay local unless asked) |
| **3.2** | Explicit run dimensions: ADE product + guest runtime + plan/cloud | P0 if scoring | Align `docs/run-report-metrics.md` |
| **3.3** | Protocol fairness note for Class A leaderboards | P1 | Fixed guest/model **or** separate reports by harness |
| **3.4** | Smoke Copilot app / Xirp | P2 | Needs Mac + accounts; schedule, do not block Linux work |
| **3.5** | First multi-task scored set on one pure guest-cli peer | P2 | e.g. Emdash or Orca; full five-task suite later |

---

## Phase 4 — Dashboard and acquisition surfaces

**Status:** after Phase 0–1 are clean.

| ID | Item | Priority |
| --- | --- | --- |
| **4.1** | Dashboard badge/filter for `runtime_model` | P1 (after 1.2) |
| **4.2** | Positioning heuristic: orchestration vs own-agent if current map is weak | P2 |
| **4.3** | Re-validate advertiser aliases / acquisition scans for new product ids | P2 |

Acquisition-specific phases remain in `docs/acquisition-roadmap.md` — do not merge those tracks into this file.

---

## Phase 5 — Product monorepo dependency (Agent Pane composer)

**Status:** proposal relayed 2026-08-11 to product agent `claude-fork-2`  
**Artifact:** `/tmp/tachyon-agent-pane-composer-proposal.md` (session-local; re-home under product docs if the product agent accepts)  
**Bench role:** **do not implement** here unless the human reassigns.

| ID | Item | Owner (suggested) | Notes |
| --- | --- | --- | --- |
| **5.1** | Viability reply (Q1 composer extension / Q2 hide native TUI bars) | Product agent | Guest loops stay Claude/Codex/Grok/… |
| **5.2** | MVP: multi-line stage + single submit path + occupancy + layer 1 intact | Product | Extend layer 2; dual surface forever |
| **5.3** | Superpowers: queue, pin→stage, input lock, inject markers | Product | After MVP |
| **5.4** | Hide native CLI composer chrome | Product optional | **Not** MVP gate; measure per runtime |
| **5.5** | Explicit non-goal: Tachyon-native agent loop (layer 3) | Product | Architecture note SoT |

Product architecture SoT (read-only from this repo’s perspective):  
`~/tachyon/docs/architecture/agent-pane-first-party-surface.md`

---

## Suggested sequence

```text
Now (Phase 0)
  0.1 → 0.2 catalog live on Pages
  // 1.1–1.2 runtime_model can start same day after merge

Next (Phase 1–2)
  1.3–1.4 surfaces
  2.1 AgentsRoom enrichment
  3.2 run dimensions if any scoring is imminent
  3.1 Emdash smoke

Later (Phase 3–4)
  2.5 battlecards
  3.3 fairness language
  4.x dashboard polish

Parallel (Phase 5)
  Product agent pane work — separate session/ownership
```

### Default next actions if this roadmap is approved as-is

1. **0.1** — push/PR catalog branch.  
2. **1.1 + 1.2** — specify and fill `runtime_model` across competitors.

---

## Anti-patterns

| Avoid | Why |
| --- | --- |
| Scoring Tachyon vs Kiro without fixing guest/model | Compares ADE chrome to an owned AWS agent loop |
| Fattening JSON only to grow radar polygons | Heuristic, not harness evidence |
| Treating “hide native TUI bar” as product P0 | Fragile across CLI versions |
| Two agents implementing agent-pane in the same product worktree | Collision; product already has a proposed owner |
| Cataloging Macro as Class A because it has “agents” | Office OS / company suite; exclusion documented |

---

## Open decisions (maintainer)

Record answers here when refined:

1. Priority of **go-to-market battlecards** vs **fair bench metrics/smoke**?
2. `runtime_model` **minimal** (enum only) or **rich** (guest/own lists)?
3. Catalog land path: **GitHub PR** required vs local fast-forward to `main`?
4. Until product viability returns: bench **ignores** Phase 5 entirely, or only tracks a pin/handoff?

---

## Changelog

| Date | Note |
| --- | --- |
| 2026-08-11 | Initial roadmap written from research/catalog session (Xirp, Emdash, Copilot app, Macro exclude; runtime-model gap; agent-pane proposal to `claude-fork-2`). |
| 2026-08-11 | Cataloged **Compozy (CompozyOS)** as Class A (`competitors/compozy.json`); guest-cli agent OS peer. |
| 2026-08-11 | Phase 1: required `runtime_model` (+ optional guest/own runtime lists) on all profiles; schema/bench validation; dashboard matrix filter + profile badges. |
