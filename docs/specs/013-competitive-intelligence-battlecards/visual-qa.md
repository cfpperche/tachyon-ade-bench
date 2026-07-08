# 013 — Visual QA Evidence

Captured with `agent-browser` against local preview:

- `http://localhost:4322/tachyon-ade-bench/battlecards/`
- `http://localhost:4322/tachyon-ade-bench/pt/battlecards/`

Viewports:

- `1440x1200`
- `390x1200`

Anchor:

Battlecards should be an operational, dense, readable dashboard surface
consistent with the existing Tachyon ADE Bench design, with no text overlap or
horizontal overflow on desktop/mobile.

Observations:

- Desktop EN/PT pages keep the existing dashboard header, nav, metric cards,
  section spacing, badge styling, and two-column battlecard layout.
- Mobile EN/PT pages collapse to a readable single-column layout.
- The five workflow blocks wrap without horizontal overflow.
- Product battlecard internals, including objections, Tachyon response, source
  signal metadata, evidence paths, and next actions, wrap inside their cards.
- Long source-language signal text remains readable in the Portuguese page; UI
  chrome is localized while the underlying signal evidence is not duplicated by
  locale.

Verdict: pass.
