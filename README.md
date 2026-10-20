# IndiaMetrix

**India, Explained Through Data.**

IndiaMetrix is an independent India data-intelligence platform designed to make public data easier to understand through sourced indicators, charts, rankings, comparisons, historical trends, state and district profiles, data stories, and exploratory tools.

IndiaMetrix is not affiliated with the Government of India.

## Current repository status

This repository contains more than the homepage. Existing modules include the India overview, state/UT profiles, rankings, state comparison, historical trends, India-vs-world comparisons, data stories, Data Explorer with CSV export, Ask IndiaMetrix, data/source registries, validation/build scripts, and a scheduled update workflow. The existence of a module does not guarantee every part is production-ready; see the master roadmap for known gaps and verification status.

**Start here:**
- `ROADMAP.md` — authoritative product plan, verified baseline, priorities, acceptance criteria and batch ledger.
- `NEXT_SESSION.md` — the next proposed batch and the delivery protocol.
- `DATA_MODEL.md` — indicator and source data conventions.
- `ARCHITECTURE.md` — architecture decisions.

## Technology

- Static HTML, CSS and JavaScript, with Python scripts for data validation and page generation.
- Bilingual interface (Hindi and English).
- Data records should retain the source, reference year, unit, methodology/definition and data-quality caveats.
- Never put API keys or other provider secrets in client-side JavaScript.

## Local preview

From the repository root:

```bash
python3 -m http.server 8080
```

Then open `http://localhost:8080`.

## Contribution and delivery workflow

Work is delivered in batches of roughly 10–20 related changes. Each batch is combined into **one commit and one push**, not a chain of small commits. Tell the user the intended scope before starting a batch, run only relevant targeted checks, update the roadmap/handover as needed, and wait for authorization before beginning the next batch.

Only change files relevant to the current batch. Never invent statistics or mark features complete merely because their files exist.
