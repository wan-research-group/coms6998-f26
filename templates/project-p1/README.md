# COMS 6998 P1 Template

AI-Native Computing · Fall 2026 · Exploration & Progress

## Getting started

1. In Overleaf, choose **New Project → Upload Project** and upload
   `coms6998-project-p1.zip`.
2. Select `main.tex` and the **pdfLaTeX** compiler.
3. Fill in your project title and team members. Replace the guidance and
   bracketed fields with your progress report.
4. Compile and submit the PDF through the instructor's submission channel.

## Format and content

Write **two pages, excluding references**, in the supplied two-column,
10-point, US Letter format. Figures and tables count toward the two pages.

| Section | What to include |
| --- | --- |
| Project Direction and Updates | Your project goal, the research problem, why it is important and challenging, and any updates since the proposal with their reasons. |
| Exploration and Findings | Ideas or designs explored, what you learned, and the reasons for your current direction. |
| Implementation and Infrastructure Progress | Progress on code and tools, work in development, technical challenges, and any available observations or results. Please note that you need to submit your code with the final report on Dec 18. |
| Next Steps | Your next steps and plans for the midterm and Milestone 2. |

P1 summarizes the three weeks of exploration since the proposal. Support your
discussion with concrete examples such as a design diagram, a comparison of
approaches, findings from relevant readings, or small experiments. Explain how
these findings shape your next steps.

Submit the report as a PDF.

**P1 is due October 26, 2026, at 11:59 PM ET.** The next milestones are the
**November 6 midterm presentation** and **November 9 Milestone 2 submission**.
Dates follow the latest `data/schedule.yaml` course schedule. The
[course project page](https://wan-research-group.github.io/coms6998-f26/project.html)
provides the milestone requirements.

For references, add your sources to `references.bib`, use `\cite{key}` in the
text, and uncomment the bibliography commands at the end of `main.tex`.
The included citation is an example to replace with sources relevant to your work.

## Local compilation

With TeX Live or MacTeX:

```sh
latexmk -pdf main.tex
```

Alternatively, use `pdflatex main.tex` twice. If you enable the bibliography,
run `pdflatex main.tex`, `bibtex main`, and `pdflatex main.tex` twice more.
Tectonic also works with `tectonic main.tex`.

## Files and source

- `main.tex`: editable P1 report template.
- `references.bib`: optional bibliography with a demonstration entry.
- `IEEEtran.cls` and `IEEEtran_HOWTO.pdf`: official class and documentation.
- `README.md`: these instructions.

Based on the course proposal template and the
[official ISCA 2026 IEEE template](https://iscaconf.org/isca2026/submit/ISCA2026_IEEE_template.zip).
The class is unchanged and retains its authorship and LPPL license notices.
