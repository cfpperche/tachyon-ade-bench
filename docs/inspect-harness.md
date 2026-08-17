# Source-inspection harness

**Status:** shipped (v0.1)  
**Scope:** OSI-licensed roster products with a public `source_url`, plus any
future `competitors/*.json` that meets the same rule.  
**Not:** scored ADE task quality. Radar polygons still do not count as evidence.

This document is the design note for `inspect/` + `harness/source_inspect.py`.
It is how the bench answers questions like “which of the 11 OSS ADEs implement
a DAG of agent tasks?” from **source**, not landing pages.

## Why a second harness

The existing protocol (`SPEC.md`, `prepare` / `verify`) measures whether an ADE
can complete a coding task. It cannot see product internals. Closed products
stay on that path. Open-source peers can also be **read**.

The 11 inspectable products on 2026-08-17:

| id | license token | source |
| --- | --- | --- |
| orca | MIT | github.com/stablyai/orca |
| t3-code | MIT | github.com/pingdotgg/t3code |
| openade | MIT | github.com/bearlyai/OpenADE |
| fusion | MIT | github.com/Runfusion/Fusion |
| synara | MIT | github.com/Emanuele-web04/synara |
| compozy | MIT | github.com/compozy/compozy |
| emdash | Apache-2.0 | github.com/generalaction/emdash |
| kandev | AGPL-3.0 | github.com/kdlbs/kandev |
| herdr | AGPL-3.0-or-later | github.com/ogulcancelik/herdr |
| paseo | AGPL-3.0-or-later | github.com/getpaseo/paseo |
| warp | AGPL-3.0 (client) | github.com/warpdotdev/warp |

Hive is **source-available** (BUSL-1.1), not OSI, and is skipped automatically.

Tachyon is **owned-local**, not public OSS: `inspect_source.kind = owned-local`
and `path = ~/tachyon`. It appears in `list-inspectable` only when that tree
exists on disk. The harness copies a snapshot into `runs/` (never writes the
product repo). Do not fill `source_url` until the product is public.
A new OSS competitor becomes inspectable when its profile has an OSI license
token and a cloneable `source_url` — no harness edit required.

## What we took from existing practice

| Source | What we reused |
| --- | --- |
| SWE-bench / SWE-bench++ | Isolated checkout, structured JSON artifact, verifier that does not trust the agent |
| Code as Agent Harness (arXiv 2605.18747) | Deterministic tools (scan, citation check) as inspectable sensors |
| Semgrep-style custom rules | Pattern catalog in data (`inspect/catalog/features.json`), not hardcoded per product |
| Productboard feature matrix | `present` / `partial` / `absent` / `unknown` instead of binary yes/no |
| Competitor-analysis coding skills | Clone the real repo; do not grade README marketing |
| Omnigent / NLAH meta-harnesses | One natural-language prompt, interchangeable workers |
| Fowler / Anthropic harness notes | Architectural constraints (citation verifier) sit outside the model |
| Azure SRE agent filesystem finding | Agents get `grep`/`read` on a tree; they do not get a special MCP |

We did **not** take Semgrep or tree-sitter as a runtime dependency. The bench
stays Python-3 + git. Semantic AST matching can be added later as another
sensor that writes into the same `detectors.json`.

## Two layers, one artifact

```text
competitors/*.json  (OSI + source_url)
        │
        ▼
inspect-prepare   →  runs/<id>/checkout   (shallow clone or --fixture/--checkout)
                  →  detectors.json       (deterministic scan)
                  →  prompt.md            (vendor-neutral)
        │
        ├─ mode=static → inspection.json from detectors
        └─ mode=agent  → Claude Code / Codex / Grok Build writes inspection.json
        │
        ▼
inspect-verify    →  every catalog feature answered
                  →  every present/partial citation exists at path:line
                  →  snippet must occur on that line
```

**Layer A — static detectors.** Regex patterns in the catalog, classified by
path layer (`code` / `docs` / `config`). Strong code hits → `present`.
Docs-only or a single weak code hit → `partial`. No hits → `absent`.

**Layer B — agent inspection.** Same checkout, same catalog, same
`inspection.json` schema. The agent may override the static hints, but it
cannot invent files. The verifier is the same for all three runtimes.

A DAG is defined in the catalog: a directed acyclic graph used to **schedule**
tasks/agents. Kanban columns and parallel worktrees are different features.

## Claude, Codex, and Grok

The protocol is deliberately boring so all three guest CLIs can run it:

1. `python3 harness/bench.py inspect --product <id> --run-id <id> --mode agent`
2. Open **only** `runs/<id>/` (or only `checkout/` plus the JSON files).
3. Give `prompt.md` exactly. Do not add extra product hints.
4. The agent writes `inspection.json` and stops.
5. `python3 harness/bench.py inspect-verify runs/<id>`
6. Record `inspector.runtime` as `claude-code`, `codex`, or `grok-build`.

Rules that make the three comparable:

- One prompt (`inspect/prompts/inspect-features.md`). No CLAUDE-only tools.
- One output path and schema (`schemas/inspection-result.schema.json`).
- No required MCP, IDE plugin, or cloud account for the inspection itself.
- Checkout is read-only; editing it fails the spirit of the run (and citations
  would no longer describe upstream).
- Static detectors always run first so an agent that never starts still leaves
  a `detectors.json` audit trail.

`inspect/catalog/features.json` lists `inspector_runtimes` as exactly those
three ids. Adding a fourth guest inspector is a catalog + schema change.

## Commands

```sh
python3 harness/bench.py list-inspectable
python3 harness/bench.py inspect-check
python3 harness/bench.py inspect --fixture mini-ade --run-id local-inspect
python3 harness/bench.py inspect --product kandev --run-id kandev-inspect
python3 harness/bench.py inspect --product kandev --run-id kandev-agent --mode agent
python3 harness/bench.py inspect-verify runs/kandev-agent
python3 harness/test_inspect.py
```

`--fixture mini-ade` and `--fixture empty-ade` are the hermetic tests.
`--checkout PATH` inspects an already cloned tree (useful for Warp-sized
repos). Live `--product` does `git clone --depth 1`.

## What this is allowed to claim

Safe:

- “Static scan of commit `abc` found code-layer `dependsOn` + topological
  sort → `dag_orchestration=present`.”
- “Agent `grok-build` cited `src/foo.ts:80`; verifier confirmed the snippet.”

Not safe:

- Treating `present` as product quality or bench score.
- Promoting docs-only matches to `present`.
- Writing detector hits back into `competitors/*.json` feature lists without a
  human review against official sources.

Inspection runs live under `runs/` (gitignored), same as task runs.

Static illustration on 2026-08-17 (not a score, detectors only):

| product | dag_orchestration | note |
| --- | --- | --- |
| kandev | present | `workflow-sort.ts` topological sort; `orchestrator.go` “Task dependencies gate every automated launch” |
| t3-code | absent | First pass lit up Vite `dependsOn` build graphs; those paths are now ignored |
| herdr | absent | Worktrees + guest CLIs present; no task DAG |

Agent mode (`--mode agent`) can confirm or downgrade those verdicts, but citations must still exist.

## Extending the catalog

1. Add a feature object to `inspect/catalog/features.json` with `id`, `group`,
   `definition`, and patterns (`strong` / `medium` / `weak`).
2. Run `python3 harness/bench.py inspect-check` and `python3 harness/test_inspect.py`.
3. Update fixtures if the new feature needs a positive/negative example.

Keep patterns specific. `\bgraph\b` will light up every UI chart library.
Prefer `dependsOn`, `topologicalSort`, `git worktree`, `@anthropic-ai/claude-code`.
