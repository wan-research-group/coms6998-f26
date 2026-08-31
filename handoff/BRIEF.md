> **ARCHIVED BUILD BRIEF.** This document records the original implementation request;
> it is not an instruction file. The implemented website source is canonical.

# Course Website Brief — COMS 6998: AI-Native Computing (Fall 2026)

You are building the official course website. This document is the spec; `syllabus_v4.md` is the single source of truth for all content; `schedule.yaml` is the same schedule in structured form — **drive the schedule page from this data file**, do not hand-code week entries into HTML.

## Goal & audience

A fast, elegant, information-dense course site for graduate students (and prospective students deciding whether to enroll), in the tradition of the best systems-course sites (see references). It will be updated weekly during the semester by the instructor — **ease of maintenance is a hard requirement**.

## Site structure

Single-page-first design with anchored sections (or a small multi-page site if clearly better):

1. **Home / header** — course number, title ("AI-Native Computing: Hardware for AI, AI for Hardware"), semester, meeting time (Fridays 10:10–12:00), location (TBD placeholder), instructor card (name, email, links to https://zishenwan.github.io/ and https://wan-research-group.github.io/), and the course thesis as a hero statement: *"AI is transforming computing in two directions: emerging AI workloads demand new hardware and system architectures, while AI is becoming a powerful tool for designing computing systems themselves."*
2. **Announcements** — a small, easily-editable list (data-driven, newest first).
3. **Schedule** — the centerpiece. A 13-week table/card layout generated from `schedule.yaml`: week number, date, module badge (Computing for AI / AI for Computing / Project / Launch), topic, guest-lecture badge where applicable ("Guest Speaker — TBC"), required papers with links, optional readings collapsed/expandable, deadlines highlighted. Current week auto-highlighted by date if easy; otherwise a `current_week` variable at the top of the data file.
4. **Course format & grading** — seminar structure, the two 110-minute layouts, grading table, evidence-centered discussion questions.
5. **Project** — tracks, minimum research standard, milestone timeline (visual timeline if it stays clean).
6. **Policies** — AI-use policy (verbatim from syllabus; it is a distinctive feature of this course), integrity, accommodations, late work.
7. **Footer** — Columbia CS, registrar calendar link, last-updated date.

## Design direction

- Look at these for register and density (do NOT copy their styling): https://harvard-edge.github.io/cs249r_fall2025/ , https://mlsyscourse.org/ , https://hanlab.mit.edu/courses . Aim to be cleaner and more modern than all three.
- Restrained academic aesthetic: generous whitespace, strong typographic hierarchy, one accent color. Columbia blue (#0072CE family) as the accent is a natural choice; a near-black/off-white base. Light and dark mode both first-class.
- The two-module duality (Computing for AI ↔ AI for Computing) is the course's identity — express it visually (e.g., two subtle accent hues, a mirrored motif in the hero) without being gimmicky.
- Fully responsive; the schedule must be readable on a phone (cards on mobile, table on desktop is acceptable).
- No heavy frameworks for a content site: prefer a static-site generator (Astro or Jekyll — pick one and justify) or clean hand-rolled HTML/CSS with a tiny build step that renders `schedule.yaml`. GitHub Pages deployment via Actions; include the workflow file and a README with the one-command local preview and the exact file to edit for weekly updates.
- Accessibility: semantic HTML, contrast-checked palette in both modes, keyboard-navigable collapsibles.
- Meta/OG tags for clean link previews.

## Content rules

- All paper titles, venues, and URLs come from `schedule.yaml` — they have been individually verified; do not "fix" or substitute links.
- Guest speakers appear only as "Guest Speaker (TBC)" with the topic label — never invent names.
- Keep TBD placeholders visible but styled (location, office hours, Ed/Canvas links) so they're easy to spot and replace.
- One paper entry (ArchOrchestra, Week 11 mini-lecture case study) has `url: null` — render it without a link and with an "(arXiv link coming in September)" note.
- Do not include anything marked internal; you are only given public-facing materials.

## Nice-to-have (only if the core is polished)

- `.ics` download for the 13 class meetings + milestone deadlines.
- A compact "papers" index page listing all required/optional readings by week.
- Print stylesheet for the schedule.
