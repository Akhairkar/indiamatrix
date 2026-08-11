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

## Future session convention

Starting with v2, only list and package files that actually changed in that session.
Do not re-zip the entire project. If a file is deleted, record it here under "Files
deleted" instead of including it in the ZIP.
