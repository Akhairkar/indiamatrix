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

## Future session convention

Starting with v2, only list and package files that actually changed in that session.
Do not re-zip the entire project. If a file is deleted, record it here under "Files
deleted" instead of including it in the ZIP.
