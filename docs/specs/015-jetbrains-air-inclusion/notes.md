# 015 — jetbrains-air-inclusion — notes

_Created 2026-07-21._

_In-flight design memory — decisions, deviations, tradeoffs, and open questions surfaced while building. Append-only by convention._

## Design decisions

- Used `jetbrains-air` instead of `air` because the short name is too generic for acquisition queries and stable signal identifiers.
- Kept readiness at `needs-install`; official download availability is not hands-on runtime evidence.
- Kept future cloud execution, automation, and Air Team claims outside current feature lists.
- Selected T001, T003, and T005 as the first probes for basic completion, dirty-state preservation, and UI-oriented work.

## Drift found

- Herdr already had a competitor profile and appeared in the main README/map, but was absent from `SPEC.md`, the two roster docs, the advertiser registry, and current intelligence signals. The inclusion pass repairs that directly related roster drift.

## Source notes

- Current official changelog version reviewed: `262.132.21`, dated 2026-07-15.
- Linux uses JetBrains Toolbox and Git worktrees; Docker task execution is not available on Linux in the reviewed release.
- Current built-in agents are Codex, Claude Agent, Gemini CLI, and Junie; current ACP support expands the available agent harnesses.
- JetBrains AI Pro/Ultimate and BYOK/personal-subscription paths are documented; AI Free and Enterprise are not supported in the current Air preview.

## Deviations

- Hands-on qualification was split into deferred spec 016 after local inspection confirmed that neither JetBrains Toolbox nor Air is installed. JetBrains documents no silent Linux Toolbox installation, and Air additionally requires interactive account/provider authentication.

## Verification log

- 2026-07-21: `git diff --check` — pass.
- 2026-07-21: JSON parse checks for the Air profile, advertiser registry, and current signals — pass.
- 2026-07-21: `python3 harness/bench.py check` — pass.
- 2026-07-21: `python3 scripts/intelligence/check-intelligence.py` — pass.
- 2026-07-21: `python3 scripts/marketing/check-marketing.py` — pass with complete 13-profile advertiser coverage.
- 2026-07-21: `python3 scripts/marketing/summarize-history.py --check` — pass; existing three observations remain reproducible.
- 2026-07-21: `scripts/check-suite.sh` — pass across all task fixtures.
- 2026-07-21: `scripts/smoke.sh` — pass.
- 2026-07-21: `npm run dashboard:check` — pass, 0 errors/warnings/hints; Vite printed pre-existing deprecation notices.
- 2026-07-21: `npm run dashboard:build` — pass, 42 pages including EN/PT JetBrains Air routes; Vite printed pre-existing deprecation and chunk-size notices.

## Dogfood log

- 2026-07-21: `python3 harness/bench.py list-products` includes `jetbrains-air`, `JetBrains Air`, `A-local-ade`, `manual`.
- 2026-07-21: acquisition dry run generated primary-platform queries for `jetbrains-air` using the qualified `air.dev` domain on Meta, Google, LinkedIn, and X.

## Visual QA

- Pass: Chrome headless rendered the English desktop and Portuguese mobile competitor profiles without clipping or overflow.
- Pass: Chrome headless rendered the desktop battlecards surface with updated signal counts.
- Pass: Chrome headless rendered the Portuguese mobile strategy page with responsive navigation and cards.
- Static build inspection confirms JetBrains Air appears in matrix, strategy, battlecards, sources, and EN/PT profile routes.
