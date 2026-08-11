# Data Model — IndiaMetrix

This defines the shape of the data every future phase builds on. Nothing in this file is
live yet — it's the agreed schema for Phase 2 onward.

## Indicator (core record)

```json
{
  "id": "literacy-rate",
  "category": "education",
  "name": { "en": "Literacy Rate", "hi": "साक्षरता दर" },
  "unit": "%",
  "geography_level": "country | state | district",
  "geography_id": "india | maharashtra | maharashtra/nagpur",
  "year": 2011,
  "value": null,
  "source_id": "census-india",
  "source_url": "https://censusindia.gov.in/",
  "last_checked": null,
  "last_updated": null,
  "methodology_note": "",
  "is_estimate": false
}
```

Field rules:

- `value` must be `null` (not a fabricated number) until a real, sourced figure is
  entered.
- `year` is always the year the data actually refers to — never the current year, unless
  that happens to be the data year too. Never advance `year` just because time has
  passed; the automated system (Phase 12) must preserve the true data year and instead
  update `last_checked`.
- `source_id` must reference an entry in `data/sources.json`.
- `geography_id` for states/districts uses lowercase-hyphenated slugs, e.g.
  `uttar-pradesh`, `maharashtra/nagpur`.

## Source (registry record)

See `data/sources.json` for the live registry. Each entry:

```json
{
  "id": "census-india",
  "name": "Census of India",
  "publisher": "Office of the Registrar General & Census Commissioner, India",
  "url": "https://censusindia.gov.in/",
  "category": ["population", "social-development"],
  "update_frequency": "decennial",
  "notes": "Most recent full census: 2011. 2021 census was delayed."
}
```

## Planned URL patterns

| Page type          | Pattern                                  | Example                                  |
|---------------------|-------------------------------------------|-------------------------------------------|
| India overview      | `/`                                       | `/`                                        |
| Category            | `/categories/:category`                   | `/categories/education`                    |
| Indicator           | `/indicators/:indicator`                  | `/indicators/literacy-rate`                |
| State profile        | `/states/:state`                          | `/states/maharashtra`                      |
| District profile     | `/districts/:state/:district`             | `/districts/maharashtra/nagpur`            |
| Ranking              | `/rankings/:indicator`                    | `/rankings/literacy-rate`                  |
| Comparison (states)  | `/compare/:state-a-vs-state-b`            | `/compare/maharashtra-vs-gujarat`          |
| Comparison (countries) | `/compare/:country-a-vs-country-b`      | `/compare/india-vs-china`                  |
| Data story           | `/stories/:slug`                          | `/stories/indias-changing-population`      |

Slugs are always lowercase, hyphenated, English — Hindi content is served at the same URL
with the language switched client-side (consistent with the homepage pattern already
built in Phase 0), not on separate `/hi/` routes, to avoid splitting SEO authority.

## Non-negotiables carried over from ROADMAP.md

- No `value` is ever fabricated or estimated without `is_estimate: true` and a
  methodology note.
- No page is generated for an indicator that has no real sourced value yet.
