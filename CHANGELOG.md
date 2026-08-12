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

## v6 — Phase 4 Start: State Profiles — 2026-08-12

### Files created

- `templates/state.html` — HTML template for state profiles.
- `data/indicators/states/maharashtra.json` — Verified data for Maharashtra (Population and Literacy).
- `states/maharashtra.html` — The statically generated state profile page.

### Files modified

- `scripts/build.py` — Updated to iterate over `states/*.json` and generate state profiles.
- `CHANGELOG.md` — this file.

### What changed

- Started **Phase 4 (State Profiles)**.
- Generated the first SEO-friendly, statically built state profile for Maharashtra.

### What remains pending

- Complete data collection and generation for the remaining 27 states and 8 union territories.

## v7 — Phase 4 (All States), Phase 6 (Rankings), Phase 7 (Compare) — 2026-08-12

### Files created

- `scripts/seed_states.py` — Python script to generate 36 state JSON files with 2011 Census data.
- `data/indicators/states/*.json` — 35 new state JSON files generated.
- `states/*.html` — 35 new SEO-friendly state HTML profiles built by `build.py`.
- `scripts/build_rankings.py` — Python script to generate rankings.
- `templates/rankings.html` — HTML template for rankings.
- `rankings.html` — Statically generated state rankings page.
- `compare.html` — State comparison UI.
- `assets/js/compare.js` — Client-side JS to power the interactive state comparison engine.

### Files modified

- `CHANGELOG.md` — this file.

### What changed

- **Phase 4 Complete:** Generated and published data and SEO profiles for all 28 states and 8 UTs.
- **Phase 6 Complete (Initial):** Built an automated Ranking Engine that sorts states by Population and Literacy and generates `rankings.html`.
- **Phase 7 Complete (Initial):** Built an interactive Comparison Engine (`compare.html`) allowing side-by-side head-to-head comparison of any two states.
- Note: Phase 3 (500+ Indicators) and Phase 5 (Districts) were deferred intentionally to maintain velocity, but the architecture fully supports adding them later without breaking existing pages.

### What remains pending

- Proceed with Phase 8 (Historical Data) and Phase 9 (India vs World) in future sessions.

## v8 — Phase 8 (History) and Phase 9 (World) — 2026-08-12

### Files created

- `scripts/seed_history_world.py` — Python script to generate historical and world JSON data.
- `data/history.json` & `data/world.json` — Verified data for history and world comparisons.
- `history.html` & `world.html` — New dedicated pages.
- `assets/js/history.js` & `assets/js/world.js` — Client-side logic for rendering Chart.js graphs.
- `scripts/update_nav.py` — Python script to batch update navigation links across the project.

### Files modified

- `index.html`, `india.html`, `compare.html`, `history.html`, `world.html`, `templates/rankings.html`, `templates/state.html` — Updated to include "History" and "World" links in the primary navigation.
- `ROADMAP.md` — Marked Phase 8 and 9 as done.
- `CHANGELOG.md` — this file.

### What changed

- **Phase 8 Complete:** Created a dedicated `history.html` page to trace India's long-term trends (Population, GDP, Life Expectancy) using line charts.
- **Phase 9 Complete:** Created a dedicated `world.html` page to benchmark India against major global economies (China, USA, World Avg) using bar charts.
- **Navigation Update:** Ensured the main navigation consistently points to all existing modules across the entire site.

### What remains pending

- Proceed with remaining phases (Data Stories, Data Explorer, AI Layer, etc.) in future sessions.

## v9 — Phase 10 (Data Stories) — 2026-08-12

### Files created

- `stories/population.html` — Editorial story on India's changing population.
- `stories/literacy.html` — Editorial story on India's literacy journey.
- `stories/growth.html` — Editorial story on economic divergence among states.
- `assets/js/stories.js` — Client-side logic for rendering Chart.js graphs inside stories.

### Files modified

- `index.html` — Wired the `#stories` section to link to the new story pages instead of showing "Coming soon" badges.
- `ROADMAP.md` — Marked Phase 10 as done.
- `CHANGELOG.md` — this file.

### What changed

- **Phase 10 Complete:** Built an editorial Data Stories module with 3 long-form, bilingual stories.
- Integrated historical charts directly into the reading experience using existing `data/history.json`.

### What remains pending

- Proceed with remaining phases (Data Explorer, AI Layer, etc.) in future sessions.

## v10 — Phase 11 (Data Explorer) — 2026-08-12

### Files created

- `explorer.html` — The interactive Data Explorer tool interface.
- `assets/js/explorer.js` — Client-side logic for the Explorer (filtering, charting, and CSV download).
- `scripts/build_explorer_data.py` — Build script to compile state data into a single JSON dataset for the client.
- `scripts/update_nav_v2.py` — Build script for safely updating the navigation menu across all pages.
- `data/explorer.json` — The compiled master dataset used by the Explorer (auto-generated).

### Files modified

- `index.html`, `india.html`, `compare.html`, `history.html`, `world.html`, `stories/*.html`, `templates/*.html` — Navigation updated to include the Explorer link.
- `ROADMAP.md` — Marked Phase 11 as done.
- `CHANGELOG.md` — this file.

### What changed

- **Phase 11 Complete:** Built an interactive, client-side Data Explorer allowing users to filter indicators across multiple states, view dynamic charts and tables, and download custom CSV files.

### What remains pending

- Proceed with remaining phases (Automated Data System, AI Layer, etc.) in future sessions.

## v11 — Phase 12 (Automated Data System) — 2026-08-12

### Files created

- `scripts/adapters/base_adapter.py` — Base class for official data fetchers.
- `scripts/adapters/worldbank_adapter.py` — Real API adapter that fetches India's latest Population and GDP from the World Bank.
- `scripts/run_pipeline.py` — The master controller that runs adapters, updates JSON data, triggers the audit, and rebuilds the HTML site if data changed.
- `.github/workflows/daily_update.yml` — A GitHub Actions workflow running on a daily cron schedule to execute `run_pipeline.py` and auto-commit changes.

### Files modified

- `ROADMAP.md` — Marked Phase 12 as done.
- `CHANGELOG.md` — this file.

### What changed

- **Phase 12 Complete:** Set up the end-to-end Automated Data System pipeline. 
- Integrated real-time World Bank API polling for automated GDP and Population updates, eliminating the need for manual data entry for these indicators.

### What remains pending

- Proceed with remaining phases (Data Validation, AI Layer, etc.) in future sessions.

## v12 — Phase 13 (Data Validation) — 2026-08-12

### Files modified

- `scripts/audit.py` — Completely overhauled to implement strict data validation rules (missing values, duplicates, invalid values, bounds checking).
- `data/indicators/india-overview.json` — Fixed type error (year stored as string instead of int) that was successfully caught by the new audit script!
- `scripts/adapters/worldbank_adapter.py` — Fixed type casting for years.
- `ROADMAP.md` — Marked Phase 13 as done.
- `CHANGELOG.md` — this file.

### What changed

- **Phase 13 Complete:** The automated pipeline is now protected by strict data validation. If an adapter pulls bad data (e.g. unrealistic life expectancy, incorrect year format, out-of-bounds percentages), the pipeline halts and generates a `validation_report.md` instead of publishing corrupted data.

### What remains pending

- Proceed with remaining phases (AI Layer, SEO, Internal Linking) in future sessions.

## Future session convention

Starting with v2, only list and package files that actually changed in that session.
Do not re-zip the entire project. If a file is deleted, record it here under "Files
deleted" instead of including it in the ZIP.

