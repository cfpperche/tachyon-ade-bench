# Competitive Intelligence

This layer turns competitor research into reusable battlecards and monitored
signals. It is separate from benchmark scoring: a strong market signal can guide
positioning, but only reproducible run artifacts can prove task performance.

## SaaS patterns mapped to this repo

### 1. Battlecards

Inspired by Crayon and Klue, the repo should produce product-level battlecards
for sales, positioning, roadmap, and devlog planning.

Tracked primitives:

- competitor positioning
- likely objections
- Tachyon response
- evidence links
- confidence level
- freshness status
- impact tags

Battlecards are rendered from `intelligence/current/signals.json` and
competitor profiles. They are not hand-maintained slides.

### 2. Digital and marketing intelligence imports

Inspired by Similarweb and Semrush, the repo supports signal categories for:

- traffic
- SEO
- paid search
- backlinks
- share of search
- campaign positioning

No paid API is required for the current workflow. If a report is exported from a
tool later, record each observation as a signal with the original source URL,
export reference, confidence, and observed date.

### 3. Source intelligence

Inspired by AlphaSense and Contify, every insight should carry:

- `source_type`
- `source_url`
- `observed_at`
- `confidence`
- `freshness`
- `summary`
- optional `evidence_path`

This keeps insights auditable and prevents old claims from being mistaken for
current market facts.

### 4. Pricing and packaging watch

Inspired by SaaS-focused competitive-intelligence workflows, pricing and
packaging are first-class categories:

- pricing tiers
- free trial or free plan
- seat-based vs usage-based pricing
- enterprise gating
- model/provider inclusion
- limits on agents, repositories, context, seats, or runs
- local, cloud, self-hosted, or hybrid packaging

Pricing claims should prefer official pricing, docs, app-store, or source
metadata. If pricing is absent or unclear, record that absence as a watch signal
instead of inferring a business model.

### 5. Reproducible collectors

Inspired by Apify-style collectors, the first collector is intentionally simple:
`scripts/intelligence/add-signal.py` appends a normalized signal to a JSON file.

This gives the project a reproducible path before automatic scraping:

1. Capture the source URL or exported report reference.
2. Add the signal with the CLI.
3. Validate with `python3 scripts/intelligence/check-intelligence.py`.
4. Render the battlecards in the dashboard.

Later collectors can add URL snapshots, HTML hashes, screenshots, or third-party
API imports while writing the same signal contract.

## Data layout

```text
intelligence/
  current/
    signals.json       # current curated signal set
schemas/
  intelligence/
    signal.schema.json # JSON Schema contract
scripts/
  intelligence/
    add-signal.py
    check-intelligence.py
```

## Signal categories

- `battlecard`
- `positioning`
- `feature`
- `stack`
- `pricing`
- `packaging`
- `traffic`
- `seo`
- `paid_search`
- `backlink`
- `share_of_search`
- `market`
- `review`
- `objection`
- `source_watch`

## Confidence and freshness

Confidence:

- `high`: direct official, owned, or reproducible evidence.
- `medium`: credible source or tool export, but limited fields or partial
  verification.
- `low`: useful lead that needs follow-up before public claims.

Freshness:

- `current`: reviewed recently enough for public use.
- `watch`: useful but should be rechecked before strong claims.
- `stale`: retained for history, not for current positioning.

## CLI examples

Add a pricing watch signal:

```sh
python3 scripts/intelligence/add-signal.py \
  --product orca \
  --category pricing \
  --source-type official-site \
  --source-url https://www.onorca.dev/ \
  --summary "Pricing details require a fresh pass before public comparison." \
  --confidence medium \
  --freshness watch \
  --tag pricing-watch \
  --impact objection \
  --tachyon-response "Keep pricing evidence separate from benchmark claims."
```

Validate the intelligence layer:

```sh
python3 scripts/intelligence/check-intelligence.py
```

## Guardrails

- Do not mix Class A local ADE competitors with Class B enterprise platforms in
  one scored leaderboard.
- Do not use traffic or paid-media estimates as proof of product capability.
- Do not copy long proprietary SaaS report text into the repo. Record short
  summaries, source references, and derived tags.
- Keep official product facts in `competitors/*.json`; keep market and
  positioning signals in `intelligence/current/signals.json`.
