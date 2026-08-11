# NEXT_SESSION.md

## Completed so far

**Session 1 — Homepage:**
- Full homepage (`index.html`, `assets/css/style.css`, `assets/js/main.js`) — bilingual
  EN/HI, all sections from the brief, no fabricated statistics, basic on-page SEO.

**Session 2 — Phase 1 Foundation (partial):**
- `ARCHITECTURE.md` — decision to stay static HTML/CSS/JS until Phase 3, with a clear
  trigger for when to revisit.
- `DATA_MODEL.md` — indicator record schema, source record schema, planned URL
  architecture for every future page type, and the non-negotiable rule that `value` is
  never fabricated.
- `data/sources.json` — registry of 11 real official/verified data publishers (Census of
  India, MoSPI, RBI, NITI Aayog, data.gov.in, MoHFW, NCRB, MoEFCC, MeitY, World Bank, UN
  Data). Registry only — no indicator values populated yet.

## Pending — every module not built yet

- Phase 1 remainder — design system extraction into a documented component library;
  core reusable components (data card, chart wrapper, ranking row, comparison table,
  source citation badge) — build these alongside Phase 2's first real page.
- Phase 2 — India Overview (real dashboard, replacing homepage placeholders)
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

Start the **India Overview page** (Phase 2), scoped small:

1. Build a single new static page, `india.html` (or repurpose the homepage's "India at a
   Glance" section into a full page) — reuse the existing design tokens and CSS from
   Phase 0, don't restyle.
2. Pick 4–6 headline indicators to actually populate with real numbers (population, GDP,
   literacy rate, life expectancy are natural starting points) using the schema in
   `DATA_MODEL.md`. Store them as a small JSON file (e.g. `data/indicators/india-overview.json`)
   rather than hardcoding numbers in HTML, so Phase 3 can reuse the same file pattern.
3. Every value must have a `source_id` that exists in `data/sources.json` (add more
   source entries first if a needed one is missing) and a real `year` — never today's
   date.
4. Update the homepage's "India at a Glance" cards to link to this new page once it
   exists (don't wire them to fabricated numbers).
5. Do not start Phase 3 (the full indicators database) in the same session as this —
   keep the India Overview page as its own scoped unit of work.

## Session rules going forward

- Do not attempt multiple phases in a single session — usage limits are real.
- From this point on, **do not re-deliver the entire project ZIP**. Only ZIP the files
  that changed in a given session (see `CHANGELOG.md` for the convention). Record any
  deletions in `CHANGELOG.md` instead of including them in the ZIP.
- Update `ROADMAP.md` phase statuses as work completes.
- Never present fabricated statistics as real, live, or official.
