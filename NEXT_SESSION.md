# NEXT_SESSION.md

## Completed so far

**Session 1 — Homepage:** full homepage, bilingual EN/HI, all brief sections, no
fabricated statistics, basic on-page SEO.

**Session 2 — Phase 1 Foundation (partial):** `ARCHITECTURE.md`, `DATA_MODEL.md`,
`data/sources.json` (11 real official sources).

**Session 3 — Phase 2 India Overview (started):**
- `india.html` — a real India Overview page with six sourced headline indicators:
  population, GDP, literacy rate, unemployment rate, life expectancy, internet users.
- `data/indicators/india-overview.json` — the six indicator records, each with a real
  value, true data year, `source_id` matching `data/sources.json`, source URL, and a
  methodology note. Sources used: World Bank (population, GDP, life expectancy,
  internet users), Census of India (literacy rate), MoSPI/PLFS (unemployment rate).
- `assets/js/india-overview.js` — fetches the JSON and renders the cards, including a
  live language re-render on EN/HI switch.
- Homepage's "India at a Glance" section now links to `india.html`; the homepage's own
  placeholder cards were deliberately left untouched (still "Data coming soon") to keep
  this session scoped — see rationale in `ROADMAP.md` Phase 2.

**Session 4 — Phase 2 Deepening & Tooling:**
- Added pre-push audit script (`scripts/audit.py` & `scripts/pre-push`) to automatically validate indicator JSON files before every push.
- Deepened Phase 2 by adding a Historical Trend chart for Population to `india.html`, driven by `data/indicators/india-population-history.json` and Chart.js.

## Pending — every module not built yet

- Phase 1 remainder — design system extraction into a documented component library.
- Phase 2 remainder — historical trend charts for the remaining five indicators; expanding beyond six indicators once Phase 3 exists.
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
- Phase 18 — AdSense readiness pages

Full detail on every phase lives in `ROADMAP.md` — read it before starting new work.

## Recommended next step

**Start Phase 4 narrowly:** build a single state profile page (e.g. `states/maharashtra.html`) using the same JSON-plus-render pattern established in `data/indicators/india-overview.json` and `assets/js/india-overview.js` — reuse that pattern rather than inventing a new one. This will prove the architecture works for states.

Do not start the full Phase 3 indicators database yet — that's a large, multi-session effort and should wait until the JSON-plus-render pattern has been proven on a couple more pages first.

## Session rules going forward

- Do not attempt multiple phases in a single session — usage limits are real.
- From this point on, **do not re-deliver the entire project ZIP**. Only ZIP the files
  that changed in a given session (see `CHANGELOG.md` for the convention). Record any
  deletions in `CHANGELOG.md` instead of including them in the ZIP.
- Update `ROADMAP.md` phase statuses as work completes.
- Never present fabricated statistics as real, live, or official — every new indicator
  value needs a real `source_id`, real `source_url`, and true `year`.
