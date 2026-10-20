# IndiaMetrix — Next Batch Handover
**Updated:** 20 October 2026  
**Repository:** `Akhairkar/indiamatrix` · branch `main`

## Current status — B1 completed
B1 changes are grouped in one commit. Data-side reliability issues were fixed:
- The audit now walks nested indicator/district JSON and supports both indicator collections and one-record-per-file records.
- Validation now rejects non-finite numbers and invalid source URLs, and checks both English and Hindi display values.
- World Bank records for electricity and clean-cooking access now use integer reference years, explicit percentage units, rounded display strings, and complete methodology notes.
- The World Bank adapter uses HTTPS, searches for the latest non-null observation, and surfaces failed fetches as failures.
- The daily pipeline runs conflict/schema checks even when no source values changed, and exits non-zero when an adapter fails.
- GDP comparison values now match the World Bank's 2025 current-US-dollar figures rounded to trillions.
- Sitemap generation no longer stamps every URL with the build date. `lastmod` is omitted until reliable per-page modification dates are available.

## Known limitation — domain configuration
`robots.txt`, sitemap URLs and canonical tags use `https://www.indiametrix.in`; no root `CNAME` file is present in the repository. The GitHub Pages settings could not be independently confirmed through the available read path, and the public URL was not reachable in the browser check. Therefore **no canonical, robots or absolute URL was changed**. Confirm the intended live domain and GitHub Pages custom-domain setting before a URL migration.

## Next proposed batch: B2 — Domain and cross-source consistency
**Do not start until the user authorizes the next batch.**
1. Confirm the actual published domain and Pages custom-domain configuration; then reconcile canonicals, sitemap and robots only if evidence supports a change.
2. Verify year/definition/source metadata for each metric in `data/world.json`, especially literacy, internet use, GDP per capita and poverty.
3. Review the literacy story's unsourced “over 80.5%” claims against the exact survey/source and keep Census 2011 (74.04%) clearly distinguished from later survey estimates.
4. Update the roadmap only after those checks are complete.

## Delivery protocol
- Tell the user the intended scope before starting.
- Group related changes into one batch and create **one commit, one push**.
- Run only targeted checks; avoid repeating a broad audit without cause.
- Report changed files, commit link, verification and known limitations.
- Wait for authorization before the next batch.

## Guardrails
- Work only in `Akhairkar/indiamatrix`.
- Never invent values, years, sources, boundaries or successful automation.
- Never expose API keys in browser code.
- No ad boxes or AdSense application unless separately approved.
