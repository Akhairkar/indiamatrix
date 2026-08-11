# IndiaMetrix

**India, Explained Through Data.**

IndiaMetrix is an independent India Data Intelligence Platform. It makes Indian
public/government data easy to understand through verified data, charts, rankings,
comparisons, historical trends, state/district profiles, India-vs-world comparisons and
data stories.

IndiaMetrix is not affiliated with the Government of India.

## Status

This repository currently contains **the homepage only**. See `ROADMAP.md` for the full
18-phase long-term plan and `NEXT_SESSION.md` for what to build next.

## Project structure

```
indiametrix/
├── index.html
├── assets/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
├── ROADMAP.md
├── NEXT_SESSION.md
├── CHANGELOG.md
├── README.md
└── .gitignore
```

## Local preview

No build step is required — it's plain HTML/CSS/JS. From the project root:

```bash
python3 -m http.server 8080
```

Then open `http://localhost:8080` in a browser.

## Tech notes

- Pure HTML/CSS/JS, no framework, no backend — kept deliberately simple at this stage.
- Fonts: Fraunces (display), Inter (body/Latin), Noto Sans Devanagari (Hindi), JetBrains
  Mono (data/labels), loaded from Google Fonts.
- Bilingual UI (English / Hindi) via `data-en` / `data-hi` attributes and a small JS
  switcher in `assets/js/main.js`; the selected language persists in `localStorage`.
- All indicator values shown are explicit placeholders — no fabricated statistics.

## Contributing to future sessions

Read `ROADMAP.md` and `NEXT_SESSION.md` before starting new work. From the second
session onward, only changed files should be delivered/packaged — not the whole project.
