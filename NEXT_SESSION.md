# NEXT_SESSION.md

## Completed this session

- Homepage (`index.html`) — all sections from the brief: header/nav, hero with search UI,
  India at a Glance, Explore India, Categories (18), Compare preview, Rankings preview,
  Data Stories preview, Why IndiaMetrix, Trust/source section, footer
- Responsive, mobile-first design (`assets/css/style.css`), down to small phone widths
- Hindi / English UI switcher (`assets/js/main.js`), all copy translated, persisted via
  `localStorage`
- Initial on-page SEO: single H1, semantic heading hierarchy, meta description, canonical
  tag, Open Graph tags, JSON-LD `WebSite` schema, accessible nav, skip link, focus states
- No fabricated statistics — every indicator value is explicitly labelled as a placeholder
- `ROADMAP.md` — full 18-phase long-term plan
- `README.md`, `CHANGELOG.md`, `.gitignore`

## Pending — every module not built yet

- Phase 1 — Foundation (architecture, data model, source registry, URL architecture)
- Phase 2 — India Overview (real dashboard, replacing placeholders)
- Phase 3 — Indicators database (target 500–1,000+, real sourced data)
- Phase 4 — State profiles (28 states + 8 UTs)
- Phase 5 — District profiles
- Phase 6 — Rankings engine
- Phase 7 — Comparison engine
- Phase 8 — Historical data / time-series pages
- Phase 9 — India vs World comparisons
- Phase 10 — Data Stories system (editorial content)
- Phase 11 — Data Explorer (search, filter, download)
- Phase 12 — Automated data fetching system (source → validate → publish pipeline)
- Phase 13 — Data validation system
- Phase 14 — AI layer ("Ask IndiaMetrix")
- Phase 15 — Full SEO system (sitemap, robots.txt, structured data at scale)
- Phase 16 — Internal linking engine
- Phase 17 — Trust / data provenance system at the indicator level
- Phase 18 — AdSense readiness pages (About, Privacy, Terms, Disclaimer, Methodology,
  Sources, Contact, Corrections)

Full detail on every phase lives in `ROADMAP.md` — read it before starting new work.

## Recommended next step

Start **Phase 1 — Foundation**, specifically in this order:

1. Decide and document the project's technical architecture (stay static HTML/CSS/JS a
   while longer, or move to a static site generator / lightweight framework — this
   decision should be made once, deliberately, before more pages are built).
2. Define the data model for an indicator (fields: id, category, name, unit, value, year,
   geography, source, source URL, last updated, methodology notes).
3. Build the source registry as a simple structured file (e.g. `data/sources.json`)
   listing official data sources IndiaMetrix intends to use, with license/attribution
   notes — this unblocks every later phase.
4. Only after the data model and source registry exist, start Phase 2 (India Overview)
   using real, verified data — do not wire the homepage's placeholder cards to fabricated
   numbers.

## Session rules going forward

- Do not attempt multiple phases in a single session — usage limits are real.
- From this point on, **do not re-deliver the entire project ZIP**. Only ZIP the files
  that changed in a given session (see `CHANGELOG.md` for the convention), e.g.
  `indiametrix-changes-v2.zip` containing only the modified/added files. Record any
  deletions in `CHANGELOG.md` instead of including them in the ZIP.
- Update `ROADMAP.md` phase statuses as work completes.
- Never present fabricated statistics as real, live, or official.
