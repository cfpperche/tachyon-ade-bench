# Source inspection task

You are inspecting **one** open-source ADE checkout to answer a fixed feature catalog.
This prompt is vendor-neutral. It must work the same way for Claude Code, Codex, and Grok Build.

## What you may touch

- **Read** `checkout/` (the product source). Do not edit it.
- **Read** `detectors.json` (optional static pre-scan). Treat it as hints, not truth.
- **Read** `feature-catalog.json` and `product.json`.
- **Write only** `inspection.json` at the run directory root (the directory that contains this prompt).

Do not modify `checkout/`, `prompt.md`, `product.json`, or the catalog.

## How to inspect

1. For every feature in `feature-catalog.json`, decide `present`, `partial`, `absent`, or `unknown`.
2. Prefer **code** evidence over README/marketing. Docs-only support is `partial`, never `present`.
3. Every `present` or `partial` verdict needs at least one citation:
   - `path` relative to `checkout/`
   - `line` (1-based)
   - `snippet` copied from that line (or a short surrounding phrase that appears there)
   - `layer`: `code` | `docs` | `config`
4. Do not invent files, lines, or snippets. If you cannot find evidence, use `absent` or `unknown` and say why in `notes`.
5. A DAG is a **directed acyclic graph used to schedule tasks/agents**. Kanban columns or parallel worktrees are not a DAG. Use `task_graph` for a generic graph without topological/acyclic scheduling.

## Output contract

Write a single JSON object to `inspection.json`:

```json
{
  "schema_version": "inspect-0.1",
  "product_id": "<id from product.json>",
  "inspector": {
    "kind": "agent",
    "runtime": "claude-code | codex | grok-build",
    "model": "<optional model id or null>"
  },
  "features": {
    "<feature_id>": {
      "verdict": "present | partial | absent | unknown",
      "notes": "<one or two sentences>",
      "evidence": [
        {
          "path": "src/example.ts",
          "line": 12,
          "snippet": "dependsOn",
          "layer": "code",
          "pattern_id": "<optional catalog pattern id>"
        }
      ]
    }
  }
}
```

Include **every** feature id from the catalog. Empty `evidence` is allowed only for `absent` or `unknown`.

When you are done, do not run the product. Stop after writing `inspection.json`.
