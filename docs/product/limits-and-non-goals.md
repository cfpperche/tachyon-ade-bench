# Limits and non-goals

Owned honesty layer. Prefer adding lines here over silent over-claim in
capabilities.

## Not claimed in this repository (today)

- Public product homepage or marketing site
- Public source repository URL for Tachyon itself
- SPDX license for the Tachyon product binary/app
- Mobile companion or multi-device mesh as a product feature
- Enterprise SaaS control plane / org-wide context engine
- “Always fully autonomous / zero human” operation
- Victory over named competitors without scored `runs/` artifacts

## Non-goals of this docs surface

- Replacing the real product monorepo docs when those exist
- Acting as a sales battlecard (see `docs/competitive-intelligence.md`)
- Acting as scored leaderboard evidence (see `runs/` + harness)
- Inflating feature lists so the Capability Radar matches Orca/Fusion

## Benchmark bias warning

Because Tachyon is owned, operators can accidentally:

- write prompts that only Tachyon understands
- intervene more or less than for competitors
- use private knowledge not available to other products

Mitigations: identical `prompt.md`, recorded interventions, independent
verifiers, no private claims in public reports.

## When to promote a claim

A capability may move to `status: claimed` in `capabilities.json` when:

1. it is true in the product you run for benchmarks, and
2. you are willing to defend it under the same rules as competitor research
   (owned evidence is fine; fiction is not), and
3. it does not require leaking private implementation the public repo forbids.
