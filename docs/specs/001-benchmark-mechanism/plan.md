# 001 — benchmark-mechanism — plan

_Drafted from `spec.md` on 2026-07-07. The approach, not the steps (those go in `tasks.md`)._

## Approach

Create a standalone repository with a dependency-free harness. Keep the first
mechanism small and auditable: JSON profiles for products, JSON metadata for
tasks, fixture repositories copied into ignored run directories, and a verifier
that records product-independent artifacts after the product under test finishes.

The harness should support manual products first because several competitors do
not expose scriptable runners. CLI/API adapters can be added later without
changing the artifact contract.

## Key decisions

- **Standalone repository** - chosen because benchmark fixtures, reports, and run
  artifacts should evolve independently from Tachyon product code; rejected
  embedding in the Tachyon repo because it would couple public comparison assets
  to product implementation.
- **Python stdlib harness** - chosen because it keeps the public repo easy to run
  on a fresh machine; rejected a Node or Python dependency stack for v0 because
  reproducibility matters more than framework convenience.
- **Manual runner first** - chosen because most competitors have GUI or desktop
  workflows; rejected pretending every product is automatable until adapters are
  verified.
- **Raw evidence before scores** - chosen because public benchmark credibility
  depends on replayable artifacts; rejected publishing a single leaderboard
  before the protocol is proven.

## Files touched

- `README.md` - public overview and quickstart.
- `SPEC.md` - benchmark protocol v0.
- `harness/bench.py` - prepare, verify, list, and check commands.
- `schemas/*.json` - tracked shape of competitor, task, and result data.
- `competitors/*.json` - initial roster metadata.
- `tasks/T001-python-bugfix/**` - smoke fixture and verifier.
- `scripts/smoke.sh` - end-to-end harness smoke test.
- `docs/specs/001-benchmark-mechanism/**` - SDD record for this first mechanism.

## Risks & unknowns

- Competitor profile stack claims may drift; keep claims conservative until
  individually sourced.
- Manual runners introduce human variance; count interventions and preserve the
  exact prompt.
- Initial fixture is intentionally small and should not be treated as a real
  leaderboard task.
- The harness should not mutate product-created diffs while collecting evidence.

## Visual impact

No UI surface is changed. Visual QA is not useful for this spec.

## Sources consulted

- Conversation request to create `tachyon-ade-bench` as a public repo and start
  the reproducible benchmark mechanism.
- SDD skill scaffold for spec structure.
- GitHub authenticated user context: `cfpperche`.
