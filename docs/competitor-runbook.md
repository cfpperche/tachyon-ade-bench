# Runbook: competitors → dashboard → GitHub Pages

Playbook for agents (and humans) who **add**, **update**, or **remove/exclude**
competitor profiles and need the public site to show the result.

Related docs (do not replace them):

| Doc | Role |
| --- | --- |
| `docs/competitor-intelligence.md` | Scope, source rules, confidence, research field meaning |
| `competitors/README.md` | What a profile file is |
| `schemas/competitor.schema.json` | Machine contract for `competitors/*.json` |
| `docs/acquisition-intelligence.md` | Ads/scans (separate from technical claims) |
| `AGENTS.md` | Bench write scope; product repo `~/tachyon` is read-only |

Public site:

```text
https://cfpperche.github.io/tachyon-ade-bench/
https://cfpperche.github.io/tachyon-ade-bench/competitors/
https://cfpperche.github.io/tachyon-ade-bench/pt/competitors/
```

---

## Mental model (read this first)

```text
official sources
    → competitors/<id>.json          # technical SSOT
    → marketing/registry/advertisers.json   # REQUIRED 1:1 with every competitor id
    → roster prose (docs/map/README/SPEC)   # human lists must not diverge
    → python3 harness/bench.py check
    → python3 scripts/marketing/check-marketing.py
    → push main
    → GitHub Actions pages.yml builds Astro from JSON
    → GitHub Pages serves apps/bench-dashboard/dist
```

Hard facts agents get wrong:

1. **The site does not read JSON at request time.** It is a static Astro build
   produced only when CI succeeds on `main`.
2. **Every `competitors/<id>.json` needs a matching advertiser** in
   `marketing/registry/advertisers.json`. Missing advertiser → Pages job fails
   at “Validate marketing metadata” and the live site stays stale.
3. **Roster prose is not auto-synced.** Updating only the JSON leaves
   `docs/competitor-intelligence.md`, `reports/competitor-map-v0.1.md`,
   `README.md`, and `SPEC.md` lying about who is in scope.
4. **Do not invent features** to fatten radar heuristics. Unknowns go in
   `research.stack.unknowns` / `research.moat.unknowns`.
5. **Write only in this repo** (`tachyon-ade-bench`). Never edit `~/tachyon`
   for competitor work. Tachyon claims: `docs/product/` → sync scripts →
   `competitors/tachyon.json`.

---

## 0. Preconditions

```sh
cd /path/to/tachyon-ade-bench
git status -sb
git fetch origin
git checkout main
git pull --ff-only origin main
```

Prefer a feature branch for non-trivial research; merge/ff to `main` only when
checks are green. Node **22+** is required for dashboard check/build.

Copy shape from a solid peer profile (e.g. `conductor.json`, `herdr.json`,
`synara.json`) rather than inventing a new schema shape.

---

## 1. Add a new competitor

### 1.1 Research and classify

1. Open **official** pages only for facts: homepage, docs, source repo,
   package manifests, app store. Kinds allowed:
   `official-site` | `official-docs` | `source-repo` | `package-manifest` |
   `app-store` | `owned`.
2. **Do not trust HTML meta alone.** SPAs often put the real product in JS
   (incident: Falou meta said “dictation”; SPA sold coding agents + Agent Board).
   Read product body / changelog / install docs.
3. Classify:
   - **`A-local-ade`**: local or multi-agent software ADE peer (cockpit, terminal
     ADE, worktree control plane, agent IDE/CLI fleet, etc.).
   - **`B-enterprise-agentic-platform`**: enterprise platform that is not a clean
     Class A local peer (report separately).
   - **Exclude**: not a software ADE (document AI, pure voice dictation with no
     coding-agent control plane, non-dev product). Document exclusion with URL
     and one-line reason in `docs/competitor-intelligence.md` **and** the map;
     do **not** invent a fake Class A row.
4. Choose `id`: `^[a-z0-9-]+$`, stable, matches filename stem
   (`competitors/<id>.json`).

### 1.2 Create `competitors/<id>.json`

Required top-level keys (schema): `id`, `name`, `class`, `homepage`,
`source_url`, `license`, `runner`, `inclusion`, `runtime_model`, `research`,
`research_status`, `updated_at`.

`runtime_model` must be one of `guest-cli` | `hybrid` | `first-party` |
`unknown` (who owns the coding agent loop). Prefer also `guest_runtimes` /
`own_runtimes` short ids and optional `runtime_model_notes`. See
`docs/competitor-intelligence.md` § Runtime model.

Inside `research` required: `last_reviewed`, `confidence`, `sources`,
`positioning`, `stack`, `infrastructure`, `features`, `benchmarking`, `moat`.

Checklist for the JSON:

- [ ] `id` equals filename stem
- [ ] `homepage` is the canonical product URL
- [ ] Every factual bullet is backed by a `research.sources[]` entry of an
      allowed kind (no Twitter/Reddit-as-fact)
- [ ] `research.last_reviewed` and `updated_at` = today (`YYYY-MM-DD`)
- [ ] `research.confidence` honest (`official-sourced` | `partial-official` |
      `seed` | `owned`)
- [ ] `research.benchmarking.readiness` one of:
      `manual-ready` | `needs-install` | `enterprise-gated` |
      `owned-reference` | `research-only`
- [ ] Stack unknowns listed explicitly — no guessed Electron/Rust unless sourced
- [ ] `runner.notes` tell a later agent how to run a harness task against it

### 1.3 Register the advertiser (mandatory for CI)

Edit `marketing/registry/advertisers.json`:

1. Bump top-level `updated_at`.
2. Append an object:

```json
{
  "product_id": "<same as competitors id>",
  "display_name": "<human name>",
  "included": true,
  "aliases": {
    "names": ["Primary name", "Alt brand"],
    "domains": ["example.com"],
    "handles": [],
    "github_orgs": []
  },
  "notes": "Disambiguation for ad/search scans; note generic-name collisions."
}
```

`product_id` **must** match a competitor file stem. Every competitor id must
appear exactly once. `included: false` is only for deliberately skipping
acquisition scans while keeping the technical profile — still requires the row.

### 1.4 Sync roster surfaces

If the product is in scope (or explicitly excluded), update **all** lists that
enumerate products:

| Surface | What to update |
| --- | --- |
| `docs/competitor-intelligence.md` | Scope bullet list; exclusion note if any |
| `reports/competitor-map-v0.1.md` | Roster table row **or** exclusion line; Source Index; Direct Benchmark Set; bump Reviewed date |
| `README.md` | Included products list |
| `SPEC.md` | Class A / Class B / Exclusions |

Do not leave “excluded” language for a product you just cataloged.

### 1.5 Validate (local, before push)

Run the **same gates CI runs for Pages** (order matters for fail-fast):

```sh
python3 harness/bench.py check
python3 scripts/marketing/check-marketing.py
python3 scripts/marketing/summarize-history.py --check
npm run dashboard:check
# optional but recommended before claiming UI is fine:
npm run dashboard:build
ls apps/bench-dashboard/dist/competitors/<id>/
python3 harness/bench.py list-products | grep <id>
```

All must exit 0. `dashboard:build` should emit `/competitors/<id>/index.html`
(and `/pt/competitors/<id>/`).

### 1.6 Commit and land on `main`

Stage **explicit paths only** (never `git add -A`):

```sh
git add \
  competitors/<id>.json \
  marketing/registry/advertisers.json \
  docs/competitor-intelligence.md \
  reports/competitor-map-v0.1.md \
  README.md \
  SPEC.md

git commit -m "Catalog <Name> competitor profile

Official-sourced Class A|B profile; register advertiser; sync roster docs."
```

Push path:

```sh
# feature branch (preferred)
git push -u origin HEAD
# then merge to main (PR or local ff) and:
git push origin main
```

Pushing **`main`** is what triggers `.github/workflows/pages.yml`.

---

## 2. Update an existing competitor

1. Re-open every URL in `research.sources` (and any new official pages).
2. Edit claims; move dead claims to unknowns or delete with source proof.
3. Refresh in the **same** change:
   - `research.last_reviewed`
   - `research.confidence` (upgrade/downgrade if evidence changed)
   - `research_status` (one-line what changed)
   - `updated_at`
4. If comparison language or readiness class changed → update
   `reports/competitor-map-v0.1.md`.
5. Advertiser row: update only if name/domain/aliases changed; bump registry
   `updated_at` if you touch the file.
6. Run the validation block in §1.5.
7. Commit + push `main` (§1.6).

**Tachyon-only path** (do not hand-edit features into the JSON as fiction):

```sh
# read ~/tachyon (read-only) if needed, then:
# edit docs/product/capabilities.json and related docs
python3 scripts/product/check-capabilities.py
python3 scripts/product/sync-tachyon-profile.py
python3 harness/bench.py check
```

---

## 3. Exclude or retire a product

### 3.1 Never was a software ADE (research disposition)

- Do **not** create `competitors/<id>.json` only to “fill the gap.”
- Add an explicit exclusion in:
  - `docs/competitor-intelligence.md`
  - `reports/competitor-map-v0.1.md` (Excluded section + optional Source Index)
  - `SPEC.md` Exclusions if it was previously listed
- One line: product name, URL, reason (e.g. “document ADE”, “voice dictation only”).
- Commit those docs; no advertiser row required if there is no competitor JSON.

### 3.2 Was cataloged, now out of roster

Prefer **keep the JSON** with honest `research.benchmarking.readiness:
research-only` and a clear `inclusion` / `research_status` note, **or** remove
the file only if maintainers want it gone — then also remove:

- `marketing/registry/advertisers.json` entry
- every roster list entry
- map row / source index line

Run full §1.5 checks after removal (marketing check fails if advertisers and
competitors diverge in either direction).

---

## 4. Publish the site (GitHub Pages)

### 4.1 What publishes

Workflow: `.github/workflows/pages.yml`

Triggers: `push` to `main`, or `workflow_dispatch`.

Job steps (must all pass):

1. `npm ci`
2. `python3 harness/bench.py check`
3. `python3 scripts/marketing/check-marketing.py` + summarize-history `--check`
4. `npm run dashboard:check`
5. `npm run dashboard:build` → artifact `apps/bench-dashboard/dist`
6. `actions/deploy-pages`

### 4.2 After you push `main`

1. Open Actions → **Deploy dashboard to GitHub Pages** for your commit SHA.
2. Wait for **success** (failure = live site unchanged).
3. Verify the **whole site**, not one route (cache-bust with `?v=$SHA`):

```sh
SHA=$(git rev-parse --short HEAD)
BASE="https://cfpperche.github.io/tachyon-ade-bench"
NAME="<Name>"   # e.g. Warp
ID="<id>"       # e.g. warp

for path in \
  "/" \
  "/matrix/" \
  "/competitors/" \
  "/competitors/${ID}/" \
  "/sources/" \
  "/strategy/" \
  "/battlecards/" \
  "/pt/" \
  "/pt/matrix/" \
  "/pt/competitors/" \
  "/pt/competitors/${ID}/"
do
  code=$(curl -sL -o /tmp/page.html -w "%{http_code}" "${BASE}${path}?v=${SHA}")
  hit=$(grep -c "$NAME\|$ID" /tmp/page.html || true)
  echo "$code  hits=$hit  $path"
done
# expect HTTP 200 everywhere; hits>=1 on list routes; profile routes 200
```

One green Pages build regenerates **all** Astro routes from `competitors/*.json`
(home charts, matrix, sources, strategy, battlecards, EN + PT). There is no
per-route publish. If `/competitors/` is new but `/matrix/` looks old, that is
almost always **browser/CDN cache** or a **failed** deploy — not a partial publish.

4. Optional: seed `intelligence/current/signals.json` rows for new product_ids so
   battlecards are not empty “no signals mapped” stubs. Still not benchmark scores.

### 4.3 If the site still shows old roster

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| JSON on `main`, site old | Pages workflow **failed** | Open failed run; fix check; push again |
| Fail at marketing validate | Missing/extra advertiser vs `competitors/*.json` | Edit `advertisers.json`; re-run checks |
| Fail at bench check | Schema/profile invalid | Fix JSON; `python3 harness/bench.py check` |
| Fail at dashboard check/build | Astro/type error | `npm run dashboard:check` locally |
| Workflow green, browser old | CDN/browser cache | Hard refresh or `?v=sha` query |
| No workflow run | Push was not to `main` | Merge/push `main` or `workflow_dispatch` |
| Pages 404 whole site | Pages not enabled / wrong source | Repo Settings → Pages → source **GitHub Actions** |

You cannot “publish” by only committing JSON without a green Pages deploy.

### 4.4 Local preview (optional)

```sh
npm install
npm run dashboard:dev
# or
npm run dashboard:build && npm run dashboard:preview
```

Local preview proves rendering; **only CI deploy updates github.io**.

---

## 5. Minimal checklists

### New competitor (copy/paste)

```text
[ ] Official sources read (not meta-only)
[ ] Class A / B / exclude decided with reason
[ ] competitors/<id>.json schema-complete, sourced, dated
[ ] marketing/registry/advertisers.json row + updated_at
[ ] Scope lists: competitor-intelligence, map, README, SPEC
[ ] python3 harness/bench.py check
[ ] python3 scripts/marketing/check-marketing.py
[ ] python3 scripts/marketing/summarize-history.py --check
[ ] npm run dashboard:check  (+ build if UI-sensitive)
[ ] Commit explicit paths; push main
[ ] Pages workflow success on that SHA
[ ] Live /competitors/ and /competitors/<id>/ show product
```

### Refresh only

```text
[ ] Re-verify sources
[ ] Edit JSON + last_reviewed + updated_at
[ ] Map if comparison language changed
[ ] Same validation + push main + confirm Pages
```

### Exclusion only

```text
[ ] Reason + URL in competitor-intelligence + map (+ SPEC if needed)
[ ] No orphan competitor JSON / advertiser mismatch
[ ] Checks green; push main if site text must update
```

---

## 6. Incident notes (so we do not repeat them)

1. **2026-08-10 — roster on main, site stale**  
   Pages failed because new competitors lacked `advertisers.json` rows. Fix:
   always add advertiser when adding `competitors/<id>.json`; run
   `check-marketing.py` before push.

2. **2026-08-10 — Falou false exclusion**  
   Meta title said voice dictation; SPA sold coding agents, Agent Board, Squads.
   Always inspect real product surface before exclude.

3. **Radar / positioning charts**  
   Scores are heuristics from profile feature lists (`AGENTS.md`), **not**
   harness scores. Do not invent bullets to win the polygon.

---

## 7. Quick command card

```sh
# full pre-push gate (Pages parity)
python3 harness/bench.py check \
  && python3 scripts/marketing/check-marketing.py \
  && python3 scripts/marketing/summarize-history.py --check \
  && npm run dashboard:check

# see who is loaded
python3 harness/bench.py list-products

# after main push — watch latest Pages run (needs network)
# https://github.com/cfpperche/tachyon-ade-bench/actions/workflows/pages.yml
```

Done means: **green Pages run on the commit that contains your profile**, and
the live `/competitors/` page lists the product with a working profile URL.
