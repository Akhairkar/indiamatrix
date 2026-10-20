# Data Model — IndiaMetrix

This document describes the indicator and source records used by the current static site. It is an active contract for records in `data/indicators/`, state profiles, and district profiles—not merely a future-phase proposal.

## Indicator record

A collection file uses an `indicators` array; a single-record dataset may store one indicator object directly. Both forms use the following fields:

```json
{
  "id": "literacy-rate",
  "category": "education",
  "name": { "en": "Literacy Rate", "hi": "साक्षरता दर" },
  "unit": "%",
  "geography_level": "country",
  "geography_id": "india",
  "year": 2011,
  "value": 74.04,
  "display": { "en": "74.04%", "hi": "74.04%" },
  "source_id": "census-india",
  "source_url": "https://censusindia.gov.in/",
  "last_checked": "2026-08-11",
  "last_updated": "2026-08-11",
  "methodology_note": "Latest full Census figure; population aged 7 and above.",
  "is_estimate": false
}
```

## Field rules

- `year` is an integer for the year the value refers to, not the year it was accessed or published.
- `value` must be a finite number. Do not fabricate a value; use `null` only where the data contract explicitly permits an unavailable observation, and never publish a made-up display value.
- `unit` must be explicit. Use `%` for percentages and keep the underlying value on a 0–100 scale.
- `display.en` and `display.hi` should both be present and readable. They are presentation strings; do not use them as the source of calculations.
- `source_id` must reference an entry in `data/sources.json`; `source_url` must point to the relevant source or indicator page.
- `last_checked` records when the source was checked. `last_updated` records when the local value was last materially changed. Do not update the reference year merely because time has passed.
- `methodology_note` should explain the population, period, definition or limitation needed to interpret the value. Set `is_estimate: true` when a value is an estimate and explain its basis.
- State and district records must use the actual geography and year to which each source value applies. Do not infer district-level values from state-level data.

## Source registry

Every `source_id` must match an entry in `data/sources.json`. Each source record includes its name, publisher, canonical URL, category, update frequency, and notes. A registry entry alone does not mean a dataset has been fetched or validated.

## URL patterns

| Page type | Pattern | Example |
|---|---|---|
| India overview | `/` | `/` |
| Indicator | `/indicators/:indicator` | `/indicators/literacy-rate.html` |
| State profile | `/states/:state` | `/states/maharashtra.html` |
| District profile | `/districts/:state/:district` | `/districts/maharashtra/nagpur.html` |
| Data story | `/stories/:slug` | `/stories/population.html` |

Hindi and English content share a URL with the language switcher; avoid creating duplicate language URLs without a deliberate SEO plan.

## Validation

`python scripts/audit.py` checks indicator collections and single-record JSON files recursively under `data/indicators/` and `data/districts/`. It validates required fields, numeric values, reference years, units, source registry membership, source URLs, bilingual display values, and basic value ranges.
