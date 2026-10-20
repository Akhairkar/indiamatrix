# IndiaMetrix — Master Roadmap
**Replaced and consolidated:** 20 October 2026  
**Repository:** `Akhairkar/indiamatrix` · **Default branch:** `main`

IndiaMetrix is an independent India data-intelligence platform: make trustworthy Indian public data understandable through clear explanations, comparable indicators, interactive charts, maps, downloadable datasets, and transparent sources. It is not affiliated with the Government of India.

This document supersedes the older phase-by-phase roadmap. It is the single source of truth for future work. Older notes, changelog entries, and generated pages may describe intended functionality rather than verified current behaviour; use this roadmap's status ledger and the actual files as the starting point.

## Working rules

1. **One batch = 10–20 related changes where practical.** Before each batch, tell the user what will change and which files/features are in scope.
2. **One commit per batch.** Stage the whole batch in one Git tree, create one commit, then push that commit once. Do not create a sequence of small commits for the same batch.
3. Do not begin the next batch until the user says “Next” or otherwise authorizes it.
4. Keep work inside this repository. Do not change SarkariSewaIndia or Landrecordes.
5. Do not repeatedly run broad audits. Use targeted checks relevant to the batch, plus one concise final verification.
6. Never invent statistics, sources, APIs, district values, map boundaries, freshness, or working features. A data value must carry its true reference year and source.
7. Do not call a phase complete merely because a file exists. Mark it complete only after checking the implementation and a relevant output/build.
8. Preserve the static HTML/CSS/JS architecture unless a concrete requirement proves a backend is necessary. Do not expose API keys in browser code.
9. No broad destructive SEO changes. Keep URL changes, redirects, noindex rules, and mass title/canonical changes out of scope unless separately justified and approved.
10. No AdSense application or ad-box insertion as part of this roadmap. Prepare trustworthy site structure only; add advertising only after explicit approval.

## Verified baseline at roadmap reset

The repository contains a substantial static site, despite the README's stale claim that it contains only the homepage. Existing modules include India overview, state pages, rankings, comparison, history, world comparison, stories, Explorer, Ask IndiaMetrix, source registry, data validation, build scripts, and a daily-update workflow.

- India overview has six sourced headline indicators; a population history chart is present.
- All 36 state/UT profile pages exist, but their state JSON records currently contain only population and literacy rate, both tied to Census 2011. The pages therefore need meaningful, sourced depth rather than more thin URLs.
- Rankings and state comparison are implemented, but their usefulness is limited by the two-indicator state dataset.
- History includes population, GDP and life expectancy; the literacy story expects a literacy history key that is missing, so that story's chart needs repair.
- India-vs-world data currently covers only a small subset of the intended topics; GDP figures on different pages need year-aware reconciliation.
- Three data stories exist; the planned digital-transformation story is missing.
- Explorer and CSV export are implemented, but the dataset is narrow.
- Data audit and World Bank adapter scripts exist; successful scheduled workflow execution has not yet been confirmed.
- Ask IndiaMetrix must be treated as **not production-ready** until the current implementation is rechecked. Never place a Gemini/LLM key in client-side JavaScript; if an LLM is approved later, it needs a protected server-side endpoint and source-grounded answers.
- SEO files and a sitemap exist, but the custom-domain vs GitHub Pages URL setup needs a live configuration check before changing canonical URLs or absolute links.
- The old README and NEXT_SESSION handover contradict the actual repository state. This reset updates those documents and makes future handovers batch-specific.

This baseline is a starting inventory, not a claim that every live page or automation was exhaustively tested on this date.

## Product priorities

**Default strategy: data-first foundation, then visual exploration, then growth.** The differentiator should be trust and usability, not a large number of low-value pages.

### Data domains to build toward

1. Economy and public finance: GDP/GSDP, per-capita income, inflation, labour-market indicators, state finances and exports.
2. People and education: population, age structure where reliable, literacy, school participation, dropout and higher education.
3. Health and nutrition: life expectancy, maternal/child health, immunisation, health infrastructure and nutrition.
4. Agriculture and water: production/yield, irrigation, rainfall, groundwater, reservoirs and mandi prices where licence/access allows.
5. Infrastructure, energy and environment: electricity, renewable energy, roads, forest cover, air quality and water stress.
6. Society and governance: crime, courts, elections/representation, public expenditure and welfare indicators where definitions are comparable.
7. Digital development: internet access, digital services and technology adoption.

Start with **50–100 high-value indicators** with traceable provenance; grow toward 200–300 and later 500+ only as sourcing and validation capacity allows. These are targets, not current counts. State/district coverage is indicator-specific: never manufacture a complete map from partial data.

## Phased execution plan

### Phase 0 — Roadmap and repository truth reset
**Status: DONE — this documentation batch**
- Replace stale roadmap content with this master plan.
- Align README and next-session notes with the actual modules already present.
- Enforce the single-commit, 10–20-change batch workflow.

### Phase 1 — Data and URL reliability
**Priority: P0 · Next technical batch**
- Recheck the existing data schema and audit script against real indicator files.
- Identify conflicting values/years and missing time-series keys; reconcile only from documented sources.
- Verify live deployment base URL, custom-domain configuration, canonical tags, robots and sitemap before making URL changes.
- Check scheduled workflow status/logs if available; distinguish “workflow configured” from “workflow successfully running.”
- Standardize the meaning of reference year, last checked, last updated, estimate, methodology and source.
**Acceptance:** no unexplained same-metric conflicts; broken data keys identified; URL strategy is confirmed before edits; no unsupported freshness claims.

### Phase 2 — Reusable UI and data provenance
**Priority: P0**
- Extract shared visual patterns for indicator cards, source labels, charts, ranking rows, comparison tables and data-quality notices.
- Make source, reference year, definition/methodology and limitations consistent across overview, state, history, world, ranking and story pages.
- Make the independent-platform disclaimer visible on interior pages.
**Acceptance:** shared patterns work in Hindi and English, on mobile and desktop, and existing pages retain their intended navigation.

### Phase 3 — Repair current broken or misleading features
**Priority: P0**
- Repair literacy history/story chart using reliable data or clearly show why a series is unavailable.
- Reconcile India/world metric year differences and display comparable years explicitly.
- Fix links that point to dead anchors or pages that are only planned.
- Check current Ask IndiaMetrix behaviour; disable misleading “AI” claims until the implementation works safely.
**Acceptance:** each repaired feature has a visible, meaningful outcome and no fabricated fallback.

### Phase 4 — Core indicator expansion
**Priority: P1**
- Select an initial 50–100 indicator catalogue based on user value, data availability, stable definitions and source rights.
- Add data records through the existing schema and source registry, not hand-copied values in HTML.
- Prioritize national and state-level economy, labour, education, health, agriculture and digital access.
- Add historical series only where definitions and years are comparable.
**Acceptance:** every published indicator has source, reference year, unit, methodology/definition and validation; missing observations are explicit.

### Phase 5 — State profiles and comparison/rankings
**Priority: P1**
- Expand state profiles beyond the current two indicators where sourced data supports it.
- Make rankings and comparison selector options data-driven, show years and units, and explain differences in definitions.
- Add “not comparable / data unavailable” states instead of silently dropping records.
**Acceptance:** rankings and comparisons use consistent units and years or explicitly disclose the mismatch.

### Phase 6 — Charts and Data Explorer
**Priority: P1**
- Reuse a consistent chart layer for trend lines, ranked bars, multi-state comparison, composition charts and scatter/correlation where the data supports it.
- Add filters for indicator, geography and time where those dimensions exist.
- Improve CSV export with source, unit, reference year, and indicator metadata.
- Keep charts accessible with labels, table alternatives and clear missing-data states.
**Acceptance:** charts accurately represent underlying data, mobile layout works, and exports preserve provenance.

### Phase 7 — India map and district coverage
**Priority: P1/P2**
- Confirm licensing, boundaries and a reliable geography-to-data mapping before implementing choropleths.
- Build India → state → district drill-down only for indicators with verified district-level data.
- Include legends, reference year, source, missing-data treatment and map/table alternatives.
- Add district profiles incrementally; do not generate empty SEO pages merely to claim nationwide coverage.
**Acceptance:** every mapped value is traceable, geography matches the data, and incomplete coverage is visible.

### Phase 8 — Stories, search and reports
**Priority: P2**
- Repair and deepen the three existing data stories; add the digital-transformation story only when its data is sourced.
- Add a universal search across indicators, states, districts, stories and tools.
- Add shareable comparison views and a lightweight report/export flow after the underlying data layer is stable.
**Acceptance:** stories make claims supported by visible data; search returns real destinations; reports include sources and years.

### Phase 9 — Ask IndiaMetrix, safely
**Priority: P2 · Depends on Phases 1–6**
- First decide whether an LLM is needed or a deterministic data-answer engine is sufficient.
- If using an LLM, route requests through a server-side function with secrets stored server-side, rate limits, input limits and cost controls.
- Ground answers in IndiaMetrix records, return source links and years, and say when the data is insufficient.
- Never expose a provider key in a static JS file.
**Acceptance:** tested end-to-end without client-side secrets; answer claims link to supporting data; unsupported questions are declined or qualified.

### Phase 10 — SEO, performance and publishing quality
**Priority: P1, after content quality**
- Verify domain/canonical/sitemap/robots consistency before editing URLs.
- Include only useful, canonical pages in the sitemap; refresh lastmod only when content materially changes.
- Add valid structured data only where it matches visible page content.
- Improve internal links and page performance without mass URL changes or thin-page proliferation.
- Build useful About, Contact, Privacy, Terms and Disclaimer pages before any monetization review.
**Acceptance:** no known broken internal links or sitemap-only URLs; page metadata matches the live domain; no empty policy placeholders.

### Phase 11 — Growth and advanced analytics
**Priority: P2/P3**
- Add data-quality scores, cross-indicator analysis, downloadable reports, embed/share links and guided explainers where user demand justifies them.
- Consider update alerts only after the relevant source pipeline is reliable.
- Expand toward 200–300 then 500+ indicators based on measured demand and maintenance capacity.
**Acceptance:** advanced features are useful, explainable, maintainable and backed by data rights and a working update process.

## Batch ledger

Update this section at the end of every batch.

| Batch | Scope | Status |
|---|---|---|
| R0 | Replace roadmap; align README and handover notes | DONE — documentation only |
| B1 | Data/URL reliability investigation and prioritized fixes | NOT STARTED |
| B2 | Shared UI and provenance conventions | NOT STARTED |
| B3 | Existing feature/data integrity repairs | NOT STARTED |
| B4+ | Indicator expansion, state comparison, Explorer, maps, stories, AI, SEO and growth | PLANNED |

## Definition of done for every batch

- The intended 10–20 related changes are grouped into one coherent batch (smaller batches are acceptable for documentation or when a safe scope is smaller).
- All changes are committed together in **one commit** and pushed once.
- Only relevant targeted checks are run; results and any limitations are stated.
- This roadmap and `NEXT_SESSION.md` are updated in the same batch when status or next steps change.
- The final note lists the changed files, single commit link, what was verified, and the next batch proposed. Do not start that next batch until authorized.
