# Competitor Map v0.1

Reviewed: 2026-07-15 (full roster source refresh)

This is a research map, not a scored benchmark. It summarizes official-source
claims captured in `competitors/*.json` so we can choose fair benchmark runs
later. Unknown closed-source internals remain unknown by design.

## Roster

| Product | Class | Stack / Infra Signals | Feature Surface | Moat Hypothesis | Benchmark Readiness |
| --- | --- | --- | --- | --- | --- |
| Tachyon | A-local-ade | Owned reference profile; public stack intentionally not asserted yet. Benchmark-visible model is worktrees, evidence, handoff, and verification gates. | Multi-agent delegation, worktree isolation, evidence records, verification-first handoff, plugin/host-action governance. | Trust through auditable operations and verification-first delivery. | `owned-reference`; run as baseline/reference, avoid private public claims. |
| Orca | A-local-ade | TypeScript/Electron/React/Vite desktop, node-pty/xterm, CLI/server (~1.4.x rc), git worktrees, remote server/SSH; high GH activity. | Fleet of parallel CLI agents, worktrees, diff annotations, browser/design mode, GitHub/Linear, mobile companion, remote server. | Open-source visibility plus worktree-first fleet UX across desktop/mobile/remote. | `manual-ready`; start with T001, T003, T005. |
| Herdr | A-local-ade | Rust single binary, ratatui/PTY runtime, Unix socket NDJSON API, AGPL; no Electron. | Terminal multiplexer for coding agents, semantic agent state, worktrees, plugins, SSH/mobile attach, agent skill API. | Terminal-native PTY + agent-shaped control surface with broad CLI detection. | `manual-ready`; record guest agent/model separately from Herdr runtime. |
| HiveTerm | A-local-ade | Rust + Tauri desktop, local Queen MCP server, `hive.yml`, local-first project/process management. | Split terminals, MCP sub-agents, live tree, pins/notes, config-as-code, inline diff/commit/PR, voice. | MCP-native nested agent teamwork and terminal-first low-footprint UX. | `manual-ready`; start with T001, T002, T004. |
| T3 Code | A-local-ade | TypeScript monorepo; npx/desktop/winget/brew install; provider CLI orchestration. | Control plane for Claude Code, Codex, OpenCode, Cursor; session/provider management. | T3 distribution plus simple BYO-subscription control plane. | `needs-install`; path `npx t3@latest` confirmed in upstream README. |
| Hive | A-local-ade | Node >= 22 npm package, local browser app on 127.0.0.1, real CLI processes, `.hive/tasks.md`; BSL. | Orchestrator/worker protocol, `team send/report`, auto-staff, team memory, role templates, remote phone access. | Repo-native task graph and explicit team protocol make orchestration observable. | `needs-install`; start with T002 and T004; note slower GH push cadence vs peers. |
| AgentsRoom | A-local-ade | Closed-source desktop app; official site shows local project folders, CLI agent sessions, remote fleet, mobile companion. | Multi-project cockpit, role agents, backlog, agent teams, scheduled tasks, review by agent, voice/drawing/screenshot/browser pointer. | Visual cockpit plus remote/mobile/fleet control for many agents. | `manual-ready`; use desktop app, not simulated browser demo. |
| Augment Code | B-enterprise-agentic-platform | Enterprise SaaS plus Auggie CLI, IDE clients, local/remote Context Engine MCP, GitHub App indexing. | Cosmos, Auggie CLI, code review, ticket-to-PR, security remediation, Context Engine retrieval, MCP. | Organizational Context Engine plus enterprise governance and SDLC integrations. | `enterprise-gated`; report separately from Class A. |
| OpenADE / ADE App | A-local-ade | TypeScript, Electron/web app, local/offline, Claude Code/Codex harnesses, git snapshots/worktrees. | Plan -> Revise -> Do, HyperPlan multi-agent planning, comments on files/diffs/messages, MCP integrations, diff/file/terminal/process manager. | Plan-first local workflow with snapshots/rollback and free open-source distribution. | `needs-install`; start with T001, T002, T005; re-check LICENSE packaging before legal claims. |
| Kandev | A-local-ade | Go backend, Next.js frontend, CLI, Tauri desktop, self-hostable, worktrees, executor model. | Kanban/pipeline + workflow import/export, subtasks, multi-repo/branch, broad ACP agent list, voice mode, PRs, MCP/integrations. | Workflow-first self-hosted control plane with kanban-native operations and executor breadth. | `needs-install`; record executor choice. |
| Fusion (Runfusion) | A-local-ade | TypeScript pnpm monorepo; React/Vite dashboard; Electron desktop; Capacitor mobile; Pi coding agent; embedded-postgres; MIT npm CLI. | Software factory board, plan/review/execute gates, worktree isolation, multi-node mesh, missions, agent companies, Command Center cost telemetry. | Open-source multi-agent factory with quality gates, worktree shipping, and multi-surface control. | `manual-ready`; T001 smoke passed after 1 merge intervention; nested worktrees + stuck auto-merge are parity risks. |

## Direct Benchmark Set

Use Class A for the first direct comparison:

- Tachyon
- Orca
- Herdr
- HiveTerm
- T3 Code
- Hive
- AgentsRoom
- OpenADE / ADE App
- Kandev
- Fusion (Runfusion)

Keep Augment Code in a separate Class B report unless the setup is explicitly
normalized and the caveats are visible.

## Source Index

- Tachyon: owned reference profile in this repository.
- Orca: https://github.com/stablyai/orca, https://raw.githubusercontent.com/stablyai/orca/main/package.json, https://www.onorca.dev/docs/remote-servers, https://www.onorca.dev/docs/agents/custom-cli
- Herdr: https://herdr.dev/, https://github.com/ogulcancelik/herdr, https://herdr.dev/docs/socket-api/, https://herdr.dev/docs/agent-skill/, https://formulae.brew.sh/formula/herdr
- HiveTerm: https://hiveterm.com/, https://hiveterm.com/agents/, https://hiveterm.com/docs/, https://hiveterm.com/compare/t3/
- T3 Code: https://t3.codes/, https://github.com/pingdotgg/t3code, https://raw.githubusercontent.com/pingdotgg/t3code/main/package.json, https://pingdotgg-t3code.mintlify.app/installation
- Hive: https://hivehq.dev/en/, https://github.com/tt-a1i/hive
- AgentsRoom: https://agentsroom.dev/, https://agentsroom.dev/pt
- Augment Code: https://www.augmentcode.com/, https://docs.augmentcode.com/introduction, https://docs.augmentcode.com/cli/overview, https://www.augmentcode.com/context-engine, https://docs.augmentcode.com/context-services/mcp/overview
- OpenADE / ADE App: https://openade.ai/, https://www.ade-app.dev/, https://github.com/bearlyai/OpenADE
- Kandev: https://github.com/kdlbs/kandev, https://raw.githubusercontent.com/kdlbs/kandev/main/README.md, https://raw.githubusercontent.com/kdlbs/kandev/main/docs/features.md
- Fusion (Runfusion): https://runfusion.ai/, https://github.com/Runfusion/Fusion, https://www.npmjs.com/package/@runfusion/fusion, https://raw.githubusercontent.com/Runfusion/Fusion/main/package.json, https://raw.githubusercontent.com/Runfusion/Fusion/main/packages/cli/package.json, https://raw.githubusercontent.com/Runfusion/Fusion/main/packages/dashboard/package.json, https://raw.githubusercontent.com/Runfusion/Fusion/main/packages/desktop/package.json, https://raw.githubusercontent.com/Runfusion/Fusion/main/packages/mobile/package.json

## Caveats Before Scoring

- No product has a full five-task scored set in this report. Fusion has a local
  T001 smoke only (`runs/fusion-v0.1-T001-python-bugfix`, gitignored).
- Manual-ready means the harness protocol can capture artifacts, not that setup
  parity is already proven.
- Enterprise-gated products need account/configuration notes before any result
  is compared to local ADEs.
- Closed-source stack details must remain unknown unless published by the
  vendor or observed in a hands-on install.
- 2026-07-15 refresh re-probed official URLs/GitHub for the full roster; chart
  surface scores remain profile heuristics, not benchmark results.
