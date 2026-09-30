# COMS 6998 Project Proposal Template

Columbia University · AI-Native Computing · Fall 2026

## Getting started

1. In Overleaf, choose **New Project → Upload Project** and upload
   `coms6998-project-proposal.zip`.
2. Select `main.tex` and the **pdfLaTeX** compiler.
3. Fill in your title, team members, and topic. Replace the guidance and bracketed
   fields with your proposal, and add your references to `references.bib`.
4. Compile and submit the PDF through the instructor's submission channel.

## Format and content

Write **two pages**, excluding references. The two pages include figures,
tables, and the team plan. Retain the supplied two-column, 10-point, US Letter
format. The brief template guidance fits on one page; expand it into your team's
two-page proposal.

| Section | What to describe |
| --- | --- |
| Problem and Motivation | Three short paragraphs: Problem, Motivation, and Research Question. |
| Related Work | Relevant work and how your project builds on or differs from it. |
| Proposed Approach | Your main idea, implementation plan, and expected contribution. |
| Evaluation Plan | Initial ideas for workloads, comparisons, and metrics. |
| Timeline and Team Responsibilities | Your planned work and deliverables for the course dates below, and the overall division of work. |

Use **October 19, November 2, November 23, December 7, and December 18** as
the timeline dates. Fill in your team's own planned work and deliverables for
each date.

The **midterm presentation is November 6**. The **final poster session is
December 11**.

An initial evaluation plan is sufficient at this stage; details can be refined
as the project develops.

**Proposal deadline: October 5, 2026, 11:59 PM ET.** Refer to the
[course project page](https://wan-research-group.github.io/coms6998-f26/project.html)
for submission instructions.

## Local compilation

With TeX Live or MacTeX:

```sh
latexmk -pdf main.tex
```

Alternatively, run `pdflatex main.tex`, `bibtex main`, and `pdflatex main.tex`
twice more. Tectonic also works with `tectonic main.tex`.

## Files and source

- `main.tex`: editable template.
- `references.bib`: a demonstration citation to replace with your sources.
- `IEEEtran.cls` and `IEEEtran_HOWTO.pdf`: official class and documentation.
- `README.md`: these instructions.

Adapted from the [official ISCA 2026 IEEE template](https://iscaconf.org/isca2026/submit/ISCA2026_IEEE_template.zip).
The class is unchanged and retains its authorship and LPPL license notices.
