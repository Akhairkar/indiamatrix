# IndiaMetrix — Master Roadmap (CORRECTED — verified against actual repo, 2026-08-12)

> **This file replaces the previous ROADMAP.md, which had drifted badly out of sync with**
> **the actual code and data in the repo — some phases were marked DONE despite being**
> **broken or unimplemented, and some phases were marked PENDING despite being fully built.**
> **Every status below was verified by opening the actual file, running the actual script,**
> **or diffing the actual data — not by re-reading old notes. Do not trust a status in this**
> **file (or any future one) without spot-checking it the same way.**

IndiaMetrix is an independent India Data Intelligence Platform. It is **not** a metals/rates
site, and it is **not** an attempt to copy NDAP, India Data Portal, or any government portal.
The mission: *understand India through data* — verified statistics, charts, rankings,
comparisons, historical trends, and state/district profiles, told clearly for general users,
students, researchers, journalists, content creators, businesses, and policy enthusiasts.

---

## How to use this file

- Each phase is a self-contained unit of work. Read the whole file before starting new work —
  several phases below are **partially built in ways the old roadmap never recorded**, so
  skipping this reading step risks redoing work or building on a broken foundation (e.g. the
  AI chat feature looks "done" from the file list alone but does not function at all).
- Never mark a phase `DONE` unless the corresponding code/data actually exists AND actually
  works — "the file exists" is not the same as "the feature works." Verify by running the
  script or opening the page, not by inspecting file names.
- If a phase is partially done, say so explicitly with a percentage-style breakdown (see
  Phase 4, 9, 10 below for the format) — a bare "IN PROGRESS" hides too much.
- When you finish part of a phase, update this file **in the same session**, with today's date
  and exactly what was verified. Do not defer roadmap updates to "next session."

---

## Phase 0 — Homepage — DONE (2026-08-11) — verified accurate

- Static homepage (`index.html`, `assets/css/style.css`, `assets/js/main.js`)
- Bilingual UI (English/Hindi), client-side switch
- Hero, India at a Glance (placeholder cards, see Phase 2), Explore India, 18 Category cards
  (all explicitly labelled "planned" — honest, not a hidden overclaim), Compare/Rankings/Data
  Stories previews, Why IndiaMetrix, Trust section, Footer
- No real statistics on the homepage itself — all placeholder text is honest
  ("Data coming soon" / "डेटा जल्द आ रहा है")
- Basic on-page SEO present: single H1, meta description, canonical tag, OG tags, JSON-LD
  `WebSite` schema

## Phase 1 — Foundation — MOSTLY DONE — verified accurate

- DONE — `ARCHITECTURE.md` exists, records the static-HTML decision — confirmed on disk.
- DONE — `DATA_MODEL.md` exists, documents indicator/source schema and `year` handling —
  confirmed on disk, and the schema it documents is what `audit.py` actually enforces
  (checked — they match).
- DONE — `data/sources.json` exists with 11 real publisher entries (Census of India, MoSPI,
  RBI, NITI Aayog, data.gov.in, MoHFW, NCRB, MoEFCC, MeitY, World Bank, UN Data) — confirmed.
- DONE — URL architecture documented in `DATA_MODEL.md`.
- STILL PENDING — Design system extraction into a documented component library (tokens
  exist in `style.css` but aren't promoted into reusable, documented components).
- STILL PENDING — Core reusable components (data card, chart wrapper, ranking row,
  comparison table, source citation badge) — every page currently hand-styles its own inline
  `style="..."` blocks instead of using shared components. This is now overdue — Phases 4-11
  were built without this, so there are 40+ pages each redefining the same card/badge CSS
  inline. Worth doing before Phase 3 (500+ indicator pages) multiplies the problem.

## Phase 2 — India Overview — DONE (2026-08-11) — verified accurate

- `india.html` has 6 real, sourced headline indicators (population, GDP, literacy rate,
  unemployment rate, life expectancy, internet users) — confirmed every value traces to
  `data/indicators/india-overview.json`, and every `source_id` used
  (`world-bank`, `census-india`, `mospi`) is a valid entry in `data/sources.json`.
- `scripts/build.py` injects these values from the JSON into `india.html` at build time —
  confirmed this is a real pipeline, not hand-copied numbers.
- Homepage "India at a Glance" links to `india.html`; homepage cards remain honest
  placeholders — confirmed.
- NOT PREVIOUSLY CREDITED — `india.html` already has one working historical trend
  chart (Population Trend, Chart.js, sourced from
  `data/indicators/india-population-history.json`). The old roadmap listed this as fully
  pending; it is 1 of 6 done.
- PENDING — Trend charts for the other 5 indicators (GDP, literacy, unemployment, life
  expectancy, internet users). Note: `data/history.json` (used by the separate Phase 8
  history page) already has GDP and life expectancy time series — those two could be wired
  into `india.html` quickly by reusing existing data, no new sourcing needed.
- NEW ISSUE FOUND — `world.html` (Phase 9) shows India's GDP as **$3.5 trillion**
  (World Bank, 2023) while `india.html` shows **$3.96 trillion** (World Bank, 2025). Same
  site, same metric, two different numbers on two different pages. Needs reconciling —
  either update `data/world.json` to the same 2025 figure, or explicitly label both with
  their year so the difference reads as "different year" rather than "inconsistent data."

## Phase 3 — Indicators (Target 500-1,000+) — PENDING — verified accurate, not started

- Confirmed: only 78 total indicator records exist across the entire repo (36 states x 2
  each + 6 India-overview + a few history series). None of the 18 promised categories
  (Economy, Healthcare, Agriculture, Infrastructure, Energy, Poverty, Crime & Safety, etc.)
  have a single dedicated page or indicator file.
- Homepage itself is honest about this — it literally says "18 planned categories" and
  "500+ verified indicators... planned," not implying they exist yet.
- **This is the correct next phase to actually do properly**, since Phases 4, 6, 7 already
  got built ahead of schedule on top of only 2 indicators per state — expanding Phase 3
  first will make those pages meaningfully better without extra plumbing work.

## Phase 4 — State Profiles — PARTIALLY BUILT, NOT MATCHING SPEC — status was WRONG (said PENDING)

**What actually exists:** All 36 state/UT pages (`states/*.html`) are built, styled, and
linked from navigation, rankings, and compare tools.

**What's actually in them — verified via `data/indicators/states/*.json`:**
- Every single state file has **exactly 2 indicators**: Population and Literacy Rate.
- Both are sourced from **Census 2011** — a 15-year-old dataset — for every one of the 36
  states, with no newer figure available or flagged as pending.
- None of the other promised categories are present: economy, healthcare, employment,
  agriculture, infrastructure, environment, digital development, social indicators,
  state-level rankings, or historical trends.
- Every record's `last_checked` / `last_updated` field says `2026-08-12` (today), even
  though the underlying value hasn't changed since 2011. This is not fabrication (the value
  itself is real and correctly dated `"year": 2011`), but it visually implies more freshness
  and rigor than what's actually there — a reader skimming "last checked today" could
  reasonably assume the number itself was refreshed today.

**To actually finish Phase 4:**
1. Add at least GDP/GSDP, unemployment rate, and one health indicator per state (these are
   the same World Bank / MoSPI / Census sources already registered — no new source vetting
   needed, just new indicator records following the existing JSON schema).
2. Either source updated post-2011 population/literacy figures where available (e.g. NFHS-5,
   PLFS-derived estimates) or add a visible note on each state page explaining that Census
   2011 remains the latest full count pending Census 2021's delayed release — `india.html`
   already does this exact thing correctly for the national literacy figure; reuse that
   pattern on state pages.
3. Only after (1) is done should `rankings.html` and `compare.html` be considered complete
   for state data — right now they can only ever rank/compare 2 metrics.

## Phase 5 — District Profiles — PENDING — verified accurate, not started

- No `districts/` folder, no district JSON, nothing. Roadmap status was correct here.

## Phase 6 — Rankings — BUILT, status was WRONG (said PENDING)

- `rankings.html` (31KB) exists, is statically pre-built by `scripts/build_rankings.py`, and
  is fully wired into navigation — confirmed functional.
- Limitation carried over from Phase 4: since state data only has 2 indicators, rankings can
  only ever be "by population" or "by literacy rate" until Phase 4 is actually finished.

## Phase 7 — Comparison Engine — BUILT, status was WRONG (said PENDING)

- `compare.html` + `assets/js/compare.js` are fully functional — state-vs-state comparison
  with a real dropdown of all 36 states, confirmed working against the state JSON files.
- Same Phase-4-data limitation applies: only 2 indicators to compare per state pair.

## Phase 8 — Historical Data — PARTIALLY DONE — status was WRONG (said fully DONE)

- `data/history.json` has real time series (1960-2023, World Bank) for **Population, GDP,
  and Life Expectancy** — confirmed rendered correctly on `history.html` via Chart.js.
- **Literacy history is missing entirely** from `data/history.json`, despite being one of
  the four series the roadmap explicitly promised ("population history, literacy history,
  GDP history, life expectancy history").
- **Direct consequence, confirmed by reading the code:** `stories/literacy.html` looks for
  `data["literacy_rate"]` in `assets/js/stories.js` — that key does not exist in
  `history.json`, so the chart on that story page silently fails to render (no error shown
  to the user, it just never appears). This is a live bug on a page that's linked from the
  homepage, not a theoretical gap.
- **To finish:** add a `literacy_rate` series to `history.json` (Census/NSSO historical
  literacy figures are available back to at least 1991, 2001, 2011) and verify the
  `stories/literacy.html` chart renders after the fix.

## Phase 9 — India vs World — PARTIALLY DONE — status was WRONG (said fully DONE)

- `world.html` + `data/world.json` exist and work, but only cover **3 of the ~11 promised
  comparison indicators**: GDP, Population, Life Expectancy (vs. China, USA, World).
- Missing: GDP per capita, literacy, internet penetration, poverty, healthcare, education,
  environment — all explicitly named in the original phase description.
- Also carries the GDP figure inconsistency noted under Phase 2 above (2023 data here vs.
  2025 data on `india.html`).

## Phase 10 — Data Stories — PARTIALLY DONE — status was WRONG (said fully DONE)

- 3 of the 4 promised stories exist and are wired up: `stories/population.html`,
  `stories/literacy.html` (chart broken — see Phase 8), `stories/growth.html`.
- **Missing entirely:** "India's digital transformation" — the fourth story named in the
  original phase description was never built.

## Phase 11 — Data Explorer — DONE — verified accurate

- `explorer.html` + `assets/js/explorer.js` are fully functional: filter/visualize across all
  36 states, and a working CSV download (`downloadCSV()` — confirmed it builds a real CSV
  blob from state/indicator/value/year/source and triggers a download).
- `data/explorer.json` (59KB) is a real compiled file built by
  `scripts/build_explorer_data.py` — confirmed it aggregates all 36 state JSON files
  correctly.
- Same underlying limitation: only 2 indicators per state to explore, so the tool is
  functionally complete but data-thin until Phase 4 is finished.

## Phase 12 — Automated Data System — BUILT BUT UNVERIFIED — status may be optimistic

- `scripts/run_pipeline.py`, `scripts/adapters/base_adapter.py`, and a real
  `worldbank_adapter.py` (uses `urllib.request` against the actual World Bank API, no fake
  data) all exist and read correctly as a real pipeline: fetch -> audit -> rebuild rankings
  -> rebuild explorer data -> rebuild HTML -> linkify -> sitemap.
- `.github/workflows/daily_update.yml` exists, runs on a daily cron, and calls
  `run_pipeline.py`.
- **Not verified — could not test:** whether the workflow has actually run successfully on
  GitHub (this can't be checked from a local zip export). The workflow's dependency step
  only runs `pip install --upgrade pip` — if any adapter needs a package beyond the Python
  standard library, the workflow will fail silently at import time. Currently the only
  adapter (`worldbank_adapter.py`) uses only `urllib.request`, so it should be fine as-is —
  but the **next new adapter that uses `requests` or similar will break the workflow** unless
  a `requirements.txt` + install step is added first.
- The pipeline also re-runs `scripts/linkify.py` on every automated run — but since linkify
  currently only touches `stories/` in practice (see Phase 16), the automation won't fix the
  state-page gap on its own; that needs the target directory list in `linkify.py` fixed and
  re-verified first.

## Phase 13 — Data Validation — DONE — verified accurate

- `scripts/audit.py` is real and was run directly: it checks duplicate IDs, missing required
  fields, non-numeric values, invalid years, missing units, unregistered source IDs, and
  range validation (percentages 0-100, life expectancy 40-100, no unexpected negatives).
- Ran it against the current repo — **passed with zero errors** across all 36 state files
  plus india-overview.
- On failure it correctly writes `validation_report.md` and exits with a non-zero code,
  which `run_pipeline.py` checks — confirmed this would actually halt the automated pipeline
  on bad data, not just log a warning.

## Phase 14 — AI Layer ("Ask IndiaMetrix") — NOT FUNCTIONAL — status was WRONG (said DONE)

- `ask.html` + `assets/js/ask.js` exist and are wired into navigation, but:
  1. `GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"` — a literal placeholder. Every real user
     who opens this page and asks a question gets "System Error: API Key not configured."
  2. **Architectural problem, not just a missing key:** the fetch call goes directly from
     client-side JavaScript to `https://generativelanguage.googleapis.com/...?key=API_KEY`.
     If a real key is ever pasted in here, it will be visible to anyone who opens browser
     dev tools or views page source — it will leak within hours of going live. The original
     phase description explicitly said "using an open LLM API or Gemini API **with a
     serverless function**" — that serverless proxy was never built; the key was put
     directly in client code instead.
- **To actually finish this phase:** do not just add a key to `ask.js`. Build a small
  serverless function (Cloudflare Worker, Vercel function, or similar — static GitHub Pages
  hosting needs an external endpoint for this) that holds the key server-side, forwards the
  user's question, and returns the answer. `ask.js` should call that function's URL, never
  Google's API directly.
- The RAG-style system prompt logic itself (restricting answers to `explorer.json`, refusing
  off-topic questions) is well written and can be reused as-is once the proxy exists.

## Phase 15 — SEO System — MOSTLY DONE, one gap — status was contradictory (listed twice)

- The old roadmap had this phase listed twice — once PENDING, once DONE, left over from an
  edit. Removing that confusion here.
- `sitemap.xml`, `robots.txt`, canonical tags, and clean URL structure are present.
- **Gap found:** `methodology.html` exists as a real page but is **missing from
  `sitemap.xml`** entirely (diffed all 47 sitemap URLs against 48 actual top-level/state/
  story HTML files — this was the only one missing).
- **Needs verifying, not confirmable from the zip alone:** `robots.txt` points to
  `https://www.indiametrix.in/sitemap.xml` and the internal-linking script (Phase 16) writes
  absolute paths like `/states/maharashtra.html`. Both of these are only correct if the site
  is actually served from that custom domain — there is **no `CNAME` file anywhere in this
  repo**, which GitHub Pages normally needs to serve a custom domain. If the custom domain
  isn't configured in the GitHub Pages settings, the site is actually being served at
  something like `username.github.io/indiamatrix/`, and every absolute path in this repo
  (sitemap URLs, internal links) would be broken in production. **Check the actual GitHub
  Pages settings for this repo before trusting any of the absolute URLs in this codebase.**

## Phase 16 — Internal Linking — HALF DONE — status was WRONG (said fully DONE across "articles and state pages")

- `scripts/linkify.py` is a real, well-written script (proper HTML tokenizer, respects
  `<a>`/`<script>`/`<style>`/heading tags, one link per keyword per file).
- Ran it in analysis: it targets exactly two directories — `states/` and `stories/`.
- Confirmed by grep: **`stories/*.html` has real injected links** (checked `growth.html` —
  Maharashtra, Gujarat, Tamil Nadu, Karnataka, Uttar Pradesh, Madhya Pradesh, GDP, and
  Population are all correctly hyperlinked in the prose).
- Confirmed by grep: **all 36 `states/*.html` files have zero `internal-link` class
  occurrences** — even though the same keywords (GDP, Population, Literacy Rate) do appear
  as plain text in those pages. The script's target list includes `states/`, so either it
  was run once before the state pages existed, or something about the state page template
  prevented matches — either way, the promised "across articles and state pages" outcome is
  only true for articles.
- **To fix:** re-run `python scripts/linkify.py` after confirming the `states/` directory
  path resolves correctly, then re-check with `grep -c "internal-link" states/*.html`.
- This also depends on resolving the absolute-path domain question under Phase 15 — no point
  re-running it broadly until it's confirmed the `/states/...`-style links will actually
  resolve on the live site.

## Phase 17 — Trust / Data Provenance — PARTIALLY BUILT, status understates progress

- `india.html` and `states/*.html` both already show a live "Source: [Publisher] ->" link per
  indicator, pointing to the real source URL — confirmed on both page types.
- What's still genuinely missing: a dedicated, sitewide "last updated" / "last checked"
  display standard applied consistently (the JSON has `last_checked`/`last_updated` fields
  per Phase 4's note above, but they aren't rendered anywhere on the page itself — only the
  data `year` is shown), and an explicit "IndiaMetrix is independent of the Government of
  India" statement — confirmed this exists in the homepage's Trust section but not on
  interior pages like state profiles.

## Phase 18 — AdSense Readiness — PENDING — verified accurate, not started

- Confirmed: no `about.html`, `privacy.html`, `terms.html`, `contact.html`, or
  `disclaimer.html` exist anywhere in the repo.
- Footer links to these on every page currently point to `href="../#"` (a dead anchor to the
  top of the current page) — clickable, but goes nowhere. This is consistent with the phase
  being genuinely not started, but is a live broken-link UX issue on every single page today,
  worth a one-line fix (e.g. `aria-disabled` styling or a "coming soon" tooltip) even before
  the real pages are written.

---

## Non-negotiable principles (apply to every future phase)

1. Never invent or fabricate statistics — placeholder clearly, or omit.
2. Every indexable page must provide genuine, non-thin value. **Phase 4's 36 state pages are
   currently borderline on this rule — 2 stale indicators per page, sitewide, is exactly
   the kind of thinness this principle was written to prevent. Fix before Phase 18.**
3. IndiaMetrix is independent and not affiliated with the Government of India — keep visible
   sitewide, not just on the homepage (see Phase 17).
4. Automation claims must match what is actually implemented — no faked "live" or "daily
   updated" labels before the automated system in Phase 12 is confirmed actually running
   successfully on GitHub (not just present in the repo).
5. New rule, added this session: before marking any phase DONE, the person or model
   doing so must state which file they opened or which command they ran to confirm it — not
   just that the relevant files exist by name. This roadmap's previous version was wrong on
   6 of 18 phases specifically because file-existence was mistaken for feature-completeness.
6. Only changed files are packaged into delivery ZIPs going forward, not the whole project.
