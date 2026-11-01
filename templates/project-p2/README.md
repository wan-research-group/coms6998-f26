# COMS 6998 P2 Template

AI-Native Computing · Fall 2026 · Prototype & Pilot Results

## Getting started

1. In Overleaf, choose **New Project → Upload Project** and upload
   `coms6998-project-p2.zip`.
2. Select `main.tex` and the **pdfLaTeX** compiler.
3. Fill in your project title and team members. Replace the guidance and
   bracketed fields with your progress report.
4. Compile and submit the PDF through the instructor's submission channel.

## Format and content

Write **two pages, excluding references**, in the supplied two-column,
10-point, US Letter format. Figures and tables count toward the two pages.

| Section | What to include |
| --- | --- |
| Project Goal and Updates | Your project goal and research problem, and any updates to your scope or direction since Milestone 1 with their reasons. |
| Method Overview | Your current approach, its main components, how they work together, and the key design choices. A diagram can help illustrate your method. |
| Prototype and Pilot Results | What runs end to end, implementation progress, and at least one pilot comparison figure with its workload, baseline, metric, and key configuration. Explain your findings. |
| Next Steps | Your next steps toward Milestone 3, the main remaining risk and how you will investigate it, and the comparisons and experiments you plan to complete. |

Build on your earlier work and describe your current project direction.
Use the report to connect your method, prototype, and pilot findings
to a concrete plan for the next stage.

Submit the report as a PDF.

**P2 is due November 9, 2026, at 11:59 PM ET.** The next written milestone is
**Milestone 3 on November 23**. Dates follow `data/schedule.yaml` in the
course website repository. The
[course project page](https://wan-research-group.github.io/coms6998-f26/project.html#milestones)
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

- `main.tex`: editable P2 report template.
- `references.bib`: optional bibliography with a demonstration entry.
- `IEEEtran.cls` and `IEEEtran_HOWTO.pdf`: official class and documentation.
- `README.md`: these instructions.

Based on the course proposal and P1 templates and the
[official ISCA 2026 IEEE template](https://iscaconf.org/isca2026/submit/ISCA2026_IEEE_template.zip).
The class is unchanged and retains its authorship and LPPL license notices.
