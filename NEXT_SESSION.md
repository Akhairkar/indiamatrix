# IndiaMetrix — Next Batch Handover
**Updated:** 20 October 2026  
**Repository:** `Akhairkar/indiamatrix` · branch `main`

## Current status
The master roadmap has been reset in `ROADMAP.md`. This batch is documentation-only; no product code, data, SEO configuration, or site behaviour has been changed.

The previous handover described phases that were already built or had changed status. Use `ROADMAP.md` as the authoritative plan from now on.

## Next proposed batch: B1 — Data and URL reliability
**Do not start until the user authorizes the next batch.**

Planned scope (aim for 10–20 related changes, all in one commit):
1. Check the schema/audit rules against the current indicator JSON.
2. Identify the missing literacy-history series and any related broken chart references.
3. Compare national/world GDP figures by source and reference year; correct only where a verified source supports it.
4. Verify the current canonical, sitemap and robots base URLs against the actual GitHub Pages/custom-domain setup before changing any URLs.
5. Check the daily workflow's recent status if accessible and record whether it actually succeeds.
6. Make only the necessary fixes justified by these checks; do not perform a broad site rewrite.

## Delivery protocol
- Before starting, tell the user the batch scope.
- Bundle all related file changes into one Git tree and create one commit.
- Push once after the batch is ready. Never create multiple sequential commits for the same batch.
- Run targeted checks only; do not repeat a broad audit without a specific reason.
- Report changed files, commit link, checks and known limitations.
- Wait for explicit authorization before starting the next batch.

## Guardrails
- Work only in this repository.
- Never fabricate data or claim an automation is working because its workflow file exists.
- Never expose AI-provider secrets in browser code.
- No AdSense application or ad-box insertion unless separately approved.
