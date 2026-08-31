# COMS 6998 · AI-Native Computing — course website

Static course site for **COMS 6998: AI-Native Computing (Fall 2026)**, Columbia University.
The entire schedule, reading list, and calendar are generated from one data file.

## Quick start (local preview)

```bash
pip install pyyaml   # one-time
python3 build.py && python3 -m http.server 8000 -d _site
```

Then open <http://localhost:8000>.

## Weekly updates: edit exactly one file

**`data/schedule.yaml`** is the single source of truth for the schedule, the papers
page, and the `.ics` calendar. To update a week, edit its entry and push; the
GitHub Action rebuilds and redeploys automatically (you can even edit the file in
the GitHub web UI).

Fields a week entry understands:

| Field | Meaning |
|---|---|
| `week`, `date`, `module`, `title`, `type` | Core row data. `type` is `lecture`, `seminar`, `midterm`, or `poster` |
| `papers:` / `background:` | Required readings (seminar weeks use `papers`, lecture weeks use `background`). Each item: `title`, `venue`, `url`, optional `focus`, `extra_link`, `companion_url`, `co_led` |
| `optional:` | List of plain strings, rendered collapsed |
| `guest:` | `{label, topic}` — renders the guest badge |
| `case_study:`, `exercise:` | Extra mini-lecture lines |
| `deadlines:` | List of strings, rendered as highlighted chips |

A paper with `url: null` renders without a link plus an "(arXiv link coming in
September)" note.

The **current week is highlighted automatically by date** (and past weeks are
dimmed). To pin it manually instead, add a top-level `current_week: 5` to
`data/schedule.yaml`.

**Announcements** live in `data/announcements.yaml` (newest first, optional
`link` + `link_text` per entry).

## Deploying to GitHub Pages

1. Push this directory to a GitHub repository (branch `main`).
2. Repository **Settings → Pages → Source: GitHub Actions**.
3. Every push to `main` runs `.github/workflows/deploy.yml`, which builds with
   `python build.py` and deploys `_site/`.
4. Once the URL exists, set `SITE_URL` at the top of `build.py` (enables
   canonical + `og:url` tags).

## Why this stack

The brief allowed Astro, Jekyll, or hand-rolled HTML with a tiny build step.
This site is **hand-rolled HTML/CSS/JS + a single-file Python renderer**
(`build.py`, only dependency: PyYAML) because:

- **Maintenance is the hard requirement.** Weekly updates touch one YAML file;
  there is no node toolchain, no framework versions to bump, no plugin churn.
- The renderer is ~500 readable lines; anyone can see exactly what HTML comes out.
- CI is trivial: `pip install pyyaml && python build.py`.
- It matches the instructor's existing data-driven static-site setup (lab site),
  so there is one mental model across sites.

## What gets built

| Output | Contents |
|---|---|
| `_site/index.html` | Single-page site: hero, announcements, schedule, format & grading, project, policies |
| `_site/papers.html` | Compact reading list of all required/optional papers by week |
| `_site/course.ics` | All 13 class meetings (Fri 10:10–12:00, America/New_York) + milestone deadlines |
| `_site/assets/` | CSS, JS, favicon (copied verbatim) |

Light/dark theme (system default + manual toggle), responsive schedule
(cards on mobile), print stylesheet, keyboard-accessible collapsibles.

## TBD checklist (replace as they land)

- [ ] Location (hero chips + `location:` in `data/schedule.yaml`, used by the `.ics`)
- [ ] Office hours (hero instructor card, `build.py` hero section)
- [ ] Ed / Canvas links (hero instructor card)
- [ ] Guest speaker confirmations (`guest:` labels in `data/schedule.yaml` — never add names before they are confirmed)
- [ ] ArchOrchestra arXiv link (Week 11 `case_study` + optional reading, expected September)
- [ ] `SITE_URL` in `build.py` after the repo/Pages URL exists

## Layout

```
├── build.py                  # renderer (HTML pages + .ics)
├── data/
│   ├── schedule.yaml         # ← EDIT WEEKLY (single source of truth)
│   └── announcements.yaml    # ← edit for announcements
├── assets/                   # style.css, site.js, favicon.svg
├── .github/workflows/deploy.yml
├── handoff/                  # original spec + syllabus (reference only, not built)
└── _site/                    # build output (gitignored)
```
