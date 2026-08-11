# CHANGELOG

## v1 — Homepage session — 2026-08-11

### Files created

- `index.html` — full homepage markup (header, hero, glance, explore, categories,
  compare, rankings, stories, why, trust, footer)
- `assets/css/style.css` — full design system and responsive layout
- `assets/js/main.js` — language switching, mobile nav, category grid rendering
- `ROADMAP.md` — 18-phase long-term project roadmap
- `NEXT_SESSION.md` — session handoff notes for the next Claude session
- `README.md` — project overview and local preview instructions
- `.gitignore` — standard ignores for a static front-end project
- `CHANGELOG.md` — this file

### Files modified

- None (first session)

### What changed

- Initial homepage built end-to-end per the brief: bilingual (EN/HI), premium
  navy/saffron/teal theme with a subtle data-grid + dot-map background, hero with
  non-functional search UI, six placeholder "India at a Glance" cards, an Explore
  India level-breakdown section, 18 category cards, a compare-preview UI, a
  rankings-preview section, three data-story preview cards, a "Why IndiaMetrix"
  section, a trust/source section, and a full footer with required disclaimer and
  policy links.
- All indicator values are explicit placeholders ("Data coming soon" /
  "डेटा जल्द आ रहा है") — no fabricated statistics anywhere on the page.
- Basic SEO implemented: single H1, semantic heading order, meta description,
  canonical link, Open Graph tags, JSON-LD `WebSite` schema, descriptive nav
  labelling, and mobile-first responsive CSS.

### What remains pending

- Everything in `ROADMAP.md` Phases 1–18 (data model, real indicators, state/district
  profiles, rankings engine, comparison engine, historical data, India vs World, data
  stories, data explorer, automated fetching, validation, AI layer, full SEO system,
  internal linking engine, provenance system, AdSense-readiness pages). See
  `NEXT_SESSION.md` for the recommended next step.

---

## v2 — Phase 1 Foundation (partial) — 2026-08-11

### Files created

- `ARCHITECTURE.md` — records the decision to stay static HTML/CSS/JS until Phase 3,
  with an explicit trigger for revisiting it
- `DATA_MODEL.md` — indicator and source record schemas, plus the full planned URL
  architecture for states, districts, indicators, rankings, comparisons, and stories
- `data/sources.json` — registry of 11 real official/verified data publishers (Census of
  India, MoSPI, RBI, NITI Aayog, data.gov.in, MoHFW, NCRB, MoEFCC, MeitY, World Bank, UN
  Data)

### Files modified

- `ROADMAP.md` — Phase 1 status updated to reflect the architecture decision, data
  model, source registry, and URL architecture as done; remaining Phase 1 items
  (component library, reusable components) left pending, to be built alongside Phase 2
- `NEXT_SESSION.md` — rewritten to point the next session at Phase 2 (India Overview
  page), scoped to a single small page with real sourced values rather than the full
  indicators database

### What changed

- No indicator values were populated — this session only built the foundation
  (architecture decision, schema, and source list) that Phase 2 will build real pages
  on top of.

### What remains pending

- Everything in `ROADMAP.md` Phases 2–18. See `NEXT_SESSION.md` for the recommended
  next step (a scoped India Overview page).

### This session's delivery ZIP

Per the "changes only" rule, `indiametrix-changes-v2.zip` contains only:
- `ARCHITECTURE.md` (new)
- `DATA_MODEL.md` (new)
- `data/sources.json` (new)
- `ROADMAP.md` (modified)
- `NEXT_SESSION.md` (modified)
- `CHANGELOG.md` (modified)

It does **not** include `index.html`, `assets/`, or `README.md`, since those were not
touched this session.

## v3 — Phase 2 India Overview (started) — 2026-08-11

### Files created

- `india.html` — a real India Overview page with six sourced headline indicators
  (population, GDP, literacy rate, unemployment rate, life expectancy, internet users)
- `data/indicators/india-overview.json` — the six indicator records, each with a real
  value, true data year, source, source URL, and methodology note
- `assets/js/india-overview.js` — fetches the JSON and renders indicator cards, with
  live re-render on language switch

### Files modified

- `index.html` — homepage's "India at a Glance" section now links to `india.html`;
  placeholder cards in that section were intentionally left untouched
- `ROADMAP.md` — Phase 2 status updated to "in progress" with details of what was built
- `NEXT_SESSION.md` — rewritten to offer two scoped next-step options (a historical
  chart, or one state profile page)

### What changed

- Six real, sourced statistics now exist on the platform for the first time, each
  citing an official publisher already listed in `data/sources.json`:
  - Population: 1.45 billion (2024, World Bank)
  - GDP: $3.91 trillion (2024, World Bank)
  - Literacy rate: 74.04% (2011, Census of India)
  - Unemployment rate: 3.1% (2025, MoSPI/PLFS)
  - Life expectancy: 72.0 years (2023, World Bank)
  - Internet users: 55.9% (2022, World Bank/ITU)
- No value was estimated or invented; every figure traces to a real, checkable source
  with the correct data year (which is not the same as today's date).

### What remains pending

- Everything in `ROADMAP.md` Phases 2 (remainder) through 18. See `NEXT_SESSION.md` for
  the two recommended next-step options.

### This session's delivery ZIP

Per the "changes only" rule, `indiametrix-changes-v3.zip` contains only:
- `india.html` (new)
- `data/indicators/india-overview.json` (new)
- `assets/js/india-overview.js` (new)
- `index.html` (modified)
- `ROADMAP.md` (modified)
- `NEXT_SESSION.md` (modified)
- `CHANGELOG.md` (modified)

It does **not** include `assets/css/style.css`, `assets/js/main.js`, `data/sources.json`,
`ARCHITECTURE.md`, `DATA_MODEL.md`, or `README.md`, since those were not touched this
session.

## v4 — Phase 2 Deepening & Tooling — 2026-08-11

### Files created

- `scripts/audit.py` — pre-push hook script to validate JSON structure and data fields
- `scripts/pre-push` — git hook to trigger the audit
- `data/indicators/india-population-history.json` — 10-year historical trend data for India's population from World Bank

### Files modified

- `india.html` — added Chart.js CDN and `<canvas>` container for historical trend chart
- `assets/js/india-overview.js` — added logic to fetch history JSON and render line chart using Chart.js, with language switching support
- `CHANGELOG.md` — this file
- `NEXT_SESSION.md` — updated for the next session

### What changed

- Implemented an "auto-audit before push" automation using a git `pre-push` hook that checks for missing fields or fabricated data in indicator JSONs.
- Completed "Option A" from the previous session's recommendations: added a real, sourced historical trend chart (Population) to the `india.html` page.

### What remains pending

- Start Phase 4 narrowly (a single state profile) or continue adding more historical charts to Phase 2.

### This session's delivery ZIP

Per the "changes only" rule, `indiametrix-changes-v4.zip` contains only:
- `scripts/audit.py` (new)
- `scripts/pre-push` (new)
- `data/indicators/india-population-history.json` (new)
- `india.html` (modified)
- `assets/js/india-overview.js` (modified)
- `CHANGELOG.md` (modified)
- `NEXT_SESSION.md` (modified)

## v5 — Phase 2 Completion & SEO Build System — 2026-08-12

### Files created

- `scripts/build.py` — Python script to statically generate HTML from JSON for SEO.

### Files modified

- `india.html` — Updated to include data injected directly into HTML (pre-rendered) instead of empty `div`.
- `assets/js/india-overview.js` — Removed the client-side JSON fetching for overview cards since they are now pre-rendered.
- `CHANGELOG.md` — this file.

### What changed

- **Major Architectural Update:** Transitioned from client-side JSON fetching to a static HTML build process (`scripts/build.py`) for better SEO (Google Console indexing), while keeping bilingual switching fully functional via data attributes.

### What remains pending

- Start Phase 4 (State Profiles) using the new static build architecture.

## Future session convention

Starting with v2, only list and package files that actually changed in that session.
Do not re-zip the entire project. If a file is deleted, record it here under "Files
deleted" instead of including it in the ZIP.

