# IndiaMetrix — Master Roadmap

> **CURRENT SESSION STATUS: PHASE 2 IN PROGRESS — a real, sourced India Overview page
> (`india.html`) is live with six headline indicators. Phase 1 Foundation (architecture,
> data model, source registry) and Phase 0 (homepage) were completed in prior sessions.**
> **ALL OTHER MODULES: PENDING FOR FUTURE SESSIONS**

IndiaMetrix is an independent India Data Intelligence Platform. It is **not** a metals/rates
site, and it is **not** an attempt to copy NDAP, India Data Portal, or any government portal.
The mission: *understand India through data* — verified statistics, charts, rankings,
comparisons, historical trends, and state/district profiles, told clearly for general users,
students, researchers, journalists, content creators, businesses, and policy enthusiasts.

This document is the single source of truth for the long-term build. Every future session
should read this file before writing code, and update it as phases are completed.

---

## How to use this file

- Each phase below is a self-contained unit of future work.
- Nothing outside "Phase 0 — Homepage" has been built yet.
- When a future session completes part of a phase, mark it `DONE` with the date and a one-line
  note, and move any newly-discovered follow-up work into the relevant phase.
- Never mark a phase `DONE` unless the corresponding code/data actually exists in the repo.

---

## Phase 0 — Homepage (THIS SESSION — ✅ DONE)

- Static homepage (`index.html`, `assets/css/style.css`, `assets/js/main.js`)
- Bilingual UI (English / Hindi) with client-side language switch
- Hero, India at a Glance, Explore India, Categories (18), Compare preview,
  Rankings preview, Data Stories preview, Why IndiaMetrix, Trust section, Footer
- No real statistics are shown — all indicator values are explicitly labelled as
  "Data coming soon" / "डेटा जल्द आ रहा है" placeholders
- Basic on-page SEO (single H1, heading hierarchy, meta description, canonical tag,
  Open Graph tags, JSON-LD `WebSite` schema, alt text conventions, mobile-first CSS)
- No backend, no database, no build tooling — plain HTML/CSS/JS by design

---

## Phase 1 — Foundation — IN PROGRESS

- ✅ **DONE (2026-08-11)** — Architecture decision recorded: stay static HTML/CSS/JS for
  now, revisit at Phase 3. See `ARCHITECTURE.md`.
- ✅ **DONE (2026-08-11)** — Data model documented (indicator + source record shape,
  field rules on fabricated values, `year` handling). See `DATA_MODEL.md`.
- ✅ **DONE (2026-08-11)** — Source registry created with 11 real official/verified
  publishers (Census of India, MoSPI, RBI, NITI Aayog, data.gov.in, MoHFW, NCRB,
  MoEFCC, MeitY, World Bank, UN Data). See `data/sources.json`. No indicator values are
  populated yet — registry only.
- ✅ **DONE (2026-08-11)** — URL architecture decided and documented in
  `DATA_MODEL.md` → "Planned URL patterns" (states, districts, indicators, rankings,
  comparisons, stories — English slugs, language switched client-side, not split into
  `/hi/` routes).
- ⏳ PENDING — Design system extraction (tokens already defined in `style.css` —
  promote to a documented, reusable component library as real pages are built).
- ⏳ PENDING — Core reusable components (data card, chart wrapper, ranking row,
  comparison table, source citation badge) — build these when Phase 2 needs its first
  real page, not before.

## Phase 2 — India Overview — IN PROGRESS

- ✅ **DONE (2026-08-11)** — `india.html` built: a real India Overview page with six
  sourced headline indicators (population, GDP, literacy rate, unemployment rate, life
  expectancy, internet users), each rendered from `data/indicators/india-overview.json`
  with a data year, source name/link, and methodology note per the `DATA_MODEL.md`
  schema. No fabricated values — every figure traces to an official publisher already
  listed in `data/sources.json` (World Bank, Census of India, MoSPI/PLFS).
- ✅ **DONE (2026-08-11)** — Homepage's "India at a Glance" section links out to
  `india.html`; the homepage cards themselves remain explicit placeholders, as decided
  in the prior session — they were not wired to real numbers to keep this session
  scoped.
- ⏳ PENDING — Historical trend charts (time series) for these same indicators.
- ⏳ PENDING — Expand beyond the six starting indicators toward the full India
  dashboard once Phase 3's indicator database exists.

## Phase 3 — Indicators (Target 500–1,000+, quality over quantity) — PENDING — FUTURE SESSION

Eighteen categories (already represented as placeholder cards on the homepage):

1. Economy
2. Population
3. Education
4. Healthcare
5. Employment
6. Poverty
7. Agriculture
8. Infrastructure
9. Energy
10. Environment
11. Crime & Safety
12. Women & Children
13. Social Development
14. Digital India
15. Banking & Finance
16. Government & Governance
17. States & Districts
18. India vs World

**Rule: never create a thin page just to raise the page count.** Every indicator page must
carry real, sourced, useful data before it is published.

## Phase 4 — State Profiles — PENDING — FUTURE SESSION

Every state/UT (28 states + 8 UTs) gets a profile covering population, economy, education,
healthcare, employment, agriculture, infrastructure, environment, digital development,
social indicators, rankings, and historical trends.

## Phase 5 — District Profiles — PENDING — FUTURE SESSION

Example route: `/districts/maharashtra/nagpur`. Only meaningful, available indicators are
shown per district — no forced completeness.

## Phase 6 — Rankings — PENDING — FUTURE SESSION

Routes such as `/rankings/literacy-rate`, `/rankings/gdp`, `/rankings/unemployment`,
`/rankings/life-expectancy`. Supports top states, bottom states, district rankings where
data exists, and historical rank movement.

## Phase 7 — Comparison Engine — PENDING — FUTURE SESSION

State vs. state, district vs. district, India vs. country, year vs. year. Routes such as
`/compare/maharashtra-vs-gujarat`, `/compare/india-vs-china`. Auto-calculates difference,
percentage difference where meaningful, which value is better/worse, historical comparison,
and charts.

## Phase 8 — Historical Data — PENDING — FUTURE SESSION

Dedicated historical trend pages (population history, literacy history, GDP history, life
expectancy history) using line charts and full available time series.

## Phase 9 — India vs World — PENDING — FUTURE SESSION

Country comparisons (GDP, population, GDP per capita, literacy, life expectancy, internet
penetration, poverty, healthcare, education, environment, and other verified indicators)
using reliable international sources.

## Phase 10 — Data Stories — PENDING — FUTURE SESSION

Editorial-style stories such as "How India's literacy changed over time," "Which Indian
states are growing fastest?," "How India's population changed," "India's digital
transformation." Every story must cite verified data and sources.

## Phase 11 — Data Explorer — PENDING — FUTURE SESSION

Search indicators, filter by state/district, select years, compare entities, download data.

## Phase 12 — Automated Data System — PENDING — FUTURE SESSION

```
Official Source → Daily Check → Detect New/Changed Data → Fetch → Validate → Store
→ Calculate Derived Metrics → Update Charts → Update Rankings → Update Comparisons
→ Update Relevant Pages → Update Internal Links → Update Sitemap → Deploy
```

Must never fake daily updates. If a source has not released new data, the original data
year is preserved and the page shows data year, last checked, last updated, and source.

## Phase 13 — Data Validation — PENDING — FUTURE SESSION

Before publishing automated data: missing-value check, duplicate check, invalid-value
check, wrong-year check, unit check, source check, range validation, calculation
validation. Failing validation blocks publishing and produces an error/validation report
instead.

## Phase 14 — AI Layer ("Ask IndiaMetrix") — PENDING — FUTURE SESSION

```
User Question → Intent Detection → Verified Database Query → Data Retrieval
→ AI Explanation → Answer + Source
```

The AI may generate explanations, but numerical facts must always come from the verified
database — never invented.

## Phase 15 — SEO System — PENDING — FUTURE SESSION

Clean URLs, canonical URLs, unique titles/descriptions, Open Graph, breadcrumbs,
appropriate structured data, XML sitemaps, robots.txt, internal linking, image SEO, fast
mobile pages, accessible HTML, 404 handling, redirect management. No mass-generated
low-value programmatic pages.

## Phase 16 — Internal Linking Engine — PENDING — FUTURE SESSION

Automatically connect India ↔ Categories ↔ Indicators ↔ States ↔ Districts ↔ Rankings ↔
Comparisons ↔ Data Stories so no important page becomes an orphan.

## Phase 17 — Trust / Data Provenance — PENDING — FUTURE SESSION

Every statistic eventually shows source, official source URL, dataset, data year, last
updated, methodology, and calculation method where applicable. Platform independence from
the Government of India is stated clearly throughout.

## Phase 18 — AdSense Readiness — PENDING — FUTURE SESSION

About, Contact, Privacy Policy, Terms & Conditions, Disclaimer, Data Methodology, Data
Sources, and Corrections Policy pages. Avoid thin AI pages, fake statistics, misleading
government branding, copied content, keyword stuffing, excessive ads, and auto-generated
useless pages. Approval or ranking is never represented as guaranteed.

---

## Non-negotiable principles (apply to every future phase)

1. Never invent or fabricate statistics — placeholder clearly, or omit.
2. Every indexable page must provide genuine, non-thin value.
3. IndiaMetrix is independent and not affiliated with the Government of India — this must
   stay visible in the trust section and footer at all times.
4. Automation claims must match what is actually implemented — no faked "live" or "daily
   updated" labels before the automated system in Phase 12 actually exists.
5. From the session that follows this one onward, only changed files are packaged into
   delivery ZIPs (see `NEXT_SESSION.md`), not the whole project.
