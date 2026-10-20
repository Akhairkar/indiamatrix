# IndiaMetrix — Next Batch Handover
Updated: 20 October 2026
Repository: Akhairkar/indiamatrix · branch main

## B2 completed
- World comparison now omits literacy and poverty rows whose displayed values did not have adequately comparable reference years/definitions.
- The world-chart fallback GDP values are synchronized with data/world.json: 2025 current US dollars, in trillions.
- Literacy story distinguishes Census 2011 (74.04%) from the PLFS 2023–24 estimate (80.9% for people aged 7+). This is a survey estimate, not a new Census result.

## Hosting decision
The user confirmed GitHub Pages only for now. Intended base URL: https://akhairkar.github.io/indiamatrix/ . Existing absolute canonical, robots and structured-data URLs still use the old custom-domain hostname. Do not configure a custom domain. Next batch should migrate all URLs together, including sitemap and robots, and keep relative navigation/assets unchanged.

## Delivery rules
Only Akhairkar/indiamatrix. One related batch = one commit and one push. Avoid broad repeated audits. Never invent data or claim unverified deployment success. Wait for user authorization before starting another batch.
