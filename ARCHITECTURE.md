# Architecture Decision — IndiaMetrix

## Decision

**Stay static HTML/CSS/JS for now.** Do not introduce a framework, build step, or backend
until Phase 3 (Indicators database) actually requires dynamic rendering at scale.

## Why

- The homepage (Phase 0) has no data-driven pages yet — a framework would add complexity
  with no present benefit.
- Phase 1–2 only need a handful of hand-authored pages (India overview, a few category
  pages). These can still be static HTML sharing the same CSS/JS.
- Once Phase 3 (500+ indicators) and Phase 4–5 (state/district profiles) begin, page
  count grows into the thousands. At that point, move to a static site generator that
  can template pages from data (e.g. Astro, Eleventy, or Next.js in static-export mode).
  This decision should be revisited explicitly at the start of Phase 3, not before.
- Keeping things simple now means every future session can be understood and extended
  without onboarding overhead.

## When to revisit

Trigger to reconsider this decision:
- Starting Phase 3 (Indicators) — page count will demand templating from data files.
- Starting Phase 12 (Automated Data System) — will need a way to regenerate pages from
  fetched data programmatically.

## What this means for Phase 1 work

- `data/sources.json` — plain JSON, no database yet.
- Data model (`DATA_MODEL.md`) is documented now so that whichever templating approach
  is chosen later, the shape of an "indicator" is already agreed and stable.
- URL architecture is decided now (see `DATA_MODEL.md` → "Planned URL patterns") so links
  built today don't need to change later.
