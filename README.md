# COMS 6998 · AI-Native Computing - course website

Static course site for **COMS 6998: AI-Native Computing (Fall 2026)**, Columbia University.
The website source is canonical; the schedule, reading list, and student-facing
syllabus are generated from the same course data.

## Quick start (local preview)

```bash
pip install pyyaml   # one-time
python3 build.py && python3 -m http.server 8000 -d _site
```

Then open <http://localhost:8000>.

## Weekly updates

**`data/schedule.yaml`** is the single source of truth for the home-page
"Now" and "at a glance" views, schedule page, papers page, and the generated
`syllabus.md`. Edit it and push; the GitHub Action rebuilds and redeploys
automatically (you can even edit the file in the GitHub web UI).

Fields a week entry understands:

| Field | Meaning |
|---|---|
| `week`, `date`, `module`, `title`, `type` | Core row data. `type` is `lecture`, `seminar`, `midterm`, or `poster` |
| `papers:` / `background:` | Required readings (seminar weeks use `papers`, lecture weeks use `background`). Each item: `title`, `short_title` (home-page label), `venue`, `url`, optional `focus`, `extra_link`, `extra_label`, `co_led` |
| `optional:` | Optional readings: either `{title, url}` maps or plain strings (rendered without a link) |
| `guest:` | Confirmed speakers only: `{label, name, affiliation, url}`. Omit until confirmed; `url` links to the speaker's homepage. |
| `research_question:` | One concise research question per week; shared by Schedule, Papers, Now, and the syllabus |
| `slides:` | Optional lecture PDF URL; shown in Now, the home-page schedule, full Schedule, and syllabus. Store local slides under `assets/slides/`. |
| `case_study:`, `exercise:` | Extra mini-lecture lines |
| `deadlines:` | List of strings, rendered as highlighted chips. The home-page table shows the part after the "-" |
| `deadline_links:` | Optional mapping from a deadline label (the text after " - ") to its form/submission URL; makes the deadline clickable in Now, the home-page table, Schedule, and syllabus. |
| `deadline_notes:` | Optional mapping from a deadline label to a plain-text reminder; displayed beside the deadline, outside its link, in all the same views. |
| `glance_deadline:` | Optional concise deadline label for the home-page table only |

A required paper with `url: null` renders without a link plus an "(arXiv link
coming in September)" note.

The **current week is highlighted automatically by date** (and past weeks are
dimmed). To pin it manually instead, add a top-level `current_week: 5` to
`data/schedule.yaml`.

**Announcements**: edit `data/announcements.yaml`; keep the newest entries at
the top or rely on the date sort. The home page displays the latest three.

**Syllabus**: `python3 build.py` regenerates both `syllabus.md` and
`_site/syllabus.md`. Do not edit the generated syllabus directly; edit
`build.py` for shared course prose or `data/schedule.yaml` for structured
course information, then rebuild.

**Milestones**: each entry in `data/schedule.yaml` has a concise `checklist`.
When a template is ready, add `template_url` to that milestone; its link appears
in both the project page and syllabus. No placeholder links are shown.
The project proposal (P0) and P1-P4 are due on Mondays at 11:59 PM ET;
presentation materials, P5, and the final submission follow their listed dates.
Keep milestone dates and the corresponding weekly `deadlines` aligned. The
home-page table explicitly shows due dates that differ from the Friday class date.

**Teaching assistants**: edit `course.teaching_assistants` in `data/schedule.yaml`
with each TA's `name` and `email`. They appear below the instructor information on
the home page and in the syllabus, with clickable email links.

**Project candidates**: edit `data/project_modules.yaml` for the six project
research modules, grouped under Computing for AI and AI for Computing after
Final submission. These are distinct from the course's two lecture modules.
Module overviews, helpful background, and evidence of success are always visible;
“Explore project ideas” reveals the 26 concise starting points. Each idea can
reference original detailed briefs by name in its `briefs` list.

The 26 original briefs remain in `data/projects.yaml`, with their full `title`,
`question`, `approach`, `evaluation`, `caution`, and `background` intact. The legacy
grouping in that file is only storage; `project_modules.yaml` controls display
order. Every brief must be assigned exactly once. Existing `#project-name` links
still work and open the relevant disclosures. The generated syllabus mirrors
the six-module guide and links to the detailed briefs. Printing reveals all ideas
and briefs, then restores the previous disclosure state.

Regression checks: `python3 -m unittest discover -s tests` and
`node tests/test_site_behaviors.js` (no extra test dependencies).

**Local readings**: put handouts and slides in `assets/readings/` and use a
relative URL such as `assets/readings/openai-jalapeno-hot-chips-2026.pdf`.
The build copies these assets unchanged into the published site.

**Students page**: add entries to `data/students.yaml` (`name`, optional
`link` and `photo`; put photo files under `assets/students/`). While the list
is empty the page shows a placeholder.
Use First name + Last name for `name`, sorted by last name and then first name.
Without `photo`, a circular avatar shows the first and last initials; adding a
student-provided photo replaces it automatically. The current list contains 36
enrolled students from the September 17 roster, with instructor name corrections.
Do not include student IDs, email addresses, or the source roster PDF in website assets.

## Deploying to GitHub Pages

1. Push this directory to a GitHub repository (branch `main`).
2. Repository **Settings → Pages → Source: GitHub Actions**.
3. Every push to `main` runs `.github/workflows/deploy.yml`, which builds with
   `python build.py` and deploys `_site/`.
4. The build infers the standard GitHub Pages URL from `GITHUB_REPOSITORY` and
   emits canonical, `og:url`, and `og:image` tags. For a custom domain, set the
   `SITE_URL` environment variable in the workflow or local build.

## Why this stack

The brief allowed Astro, Jekyll, or hand-rolled HTML with a tiny build step.
This site is **hand-rolled HTML/CSS/JS + a single-file Python renderer**
(`build.py`, only dependency: PyYAML) because:

- **Maintenance is the hard requirement.** Weekly updates touch one YAML file;
  there is no node toolchain, no framework versions to bump, no plugin churn.
- The renderer is a few hundred readable lines; anyone can see exactly what HTML comes out.
- CI is trivial: `pip install pyyaml && python build.py`.
- It matches the instructor's existing data-driven static-site setup (lab site),
  so there is one mental model across sites.

## What gets built

| Output | Contents |
|---|---|
| `_site/index.html` | Home: hero, current week/readings, next deadline, announcements, course info, schedule at a glance |
| `_site/schedule.html` | Full weekly schedule with readings, guests, deadlines |
| `_site/format.html` | Seminar format, presentation structure, grading |
| `_site/project.html` | Project tracks, milestones, final submission, six research modules, and expandable ideas/briefs |
| `_site/policies.html` | AI-use policy and course policies |
| `_site/papers.html` | Compact reading list of all required/optional papers by week |
| `_site/students.html` | Class roster (from `data/students.yaml`) |
| `_site/syllabus.md` | Generated student-facing syllabus (also written to root `syllabus.md`) |
| `_site/assets/` | CSS, JS, favicon, and social preview image (copied verbatim) |

Light/dark theme (system default + manual toggle), responsive schedule
(cards on mobile), print stylesheet, keyboard-accessible collapsibles.
The research-group link lives in the footer to keep the mobile navigation compact.

The browser favicon (`assets/favicon-columbia.png`) is the unmodified Columbia
crown PNG from the University's [favicon guidelines](https://visualidentity.columbia.edu/content/favicons)
([source asset](https://visualidentity.columbia.edu/sites/visualidentity.columbia.edu/files/content/Components/favicon.png)).
The in-page blue/purple course mark and social preview image remain separate.

## TBD checklist (replace as they land)

- [ ] Guest speaker confirmations (`guest:` labels in `data/schedule.yaml` - never add names before they are confirmed)
- [ ] Student-provided photos in `assets/students/`; add each `photo` path to `data/students.yaml`

## Layout

```
├── build.py                  # renderer
├── data/
│   ├── schedule.yaml         # ← EDIT WEEKLY (single source of truth)
│   ├── announcements.yaml    # ← latest home-page announcements
│   ├── project_modules.yaml  # ← six-module guide and detailed-brief assignments
│   ├── projects.yaml         # ← original detailed briefs (referenced by name)
│   └── students.yaml         # ← class roster for students.html
├── assets/                   # style.css, site.js, favicon-columbia.png, og.png (+ students/ photos)
├── syllabus.md               # generated; do not edit directly
├── .github/workflows/deploy.yml
├── handoff/                  # archived original spec + syllabus (reference only)
└── _site/                    # build output (gitignored)
```
