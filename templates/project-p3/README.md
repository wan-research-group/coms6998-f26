# COMS 6998 P3 Template

AI-Native Computing · Fall 2026 · Evaluation Plan & Initial Results

## Getting started

1. In Overleaf, choose **New Project → Upload Project** and upload
   `coms6998-project-p3.zip`.
2. Select `main.tex` and the **pdfLaTeX** compiler.
3. Fill in your project title and team members. Replace the guidance and
   bracketed fields with your evaluation plan and initial results.
4. Compile and submit the PDF through the instructor's submission channel.

## Format and content

Write **two pages, excluding references**, in the supplied two-column,
10-point, US Letter format. Figures and tables count toward the two pages.

| Section | What to include |
| --- | --- |
| Project Goal and Updates | Your project goal, research question, and intended claim, and any updates since Milestone 2 (including responses to midterm and P2 feedback) with their reasons. |
| Evaluation Setup | The setup for your main results, organized in the way that fits your project. This may include workloads (with at least one held-out workload, configuration, or system scale), at least two meaningful baselines (a classical or non-agentic one where applicable), metrics that report task quality or success together with systems metrics, and the platform and tools you use. |
| Initial Results | Initial comparisons between your method and the baselines, with at least one figure or table stating the workload, baselines, metrics, configuration, and number of runs. Explain your findings. |
| Planned Ablations and Next Steps | The ablations or controlled interventions you plan to run, what each tests, and the expected outcome; a failure or boundary case to study; and your plan for Milestone 4. |

P3 fixes the evaluation you will use for your main results. Build on your
P2 prototype and pilot results, and make the setup concrete enough that the
experiments for Milestone 4 can follow from it directly.

Submit the report as a PDF.

**P3 is due Wednesday, November 25, 2026, at 11:59 PM ET** (before the
Thanksgiving break). The next written milestone is
**Milestone 4 on December 7** (main results, an ablation, a failure or
boundary case, and repeated measurements or uncertainty where relevant).
Dates follow `data/schedule.yaml` in the course website repository. The
[course project page](https://wan-research-group.github.io/coms6998-f26/project.html#milestones)
provides the milestone requirements and the minimum research standard.

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

- `main.tex`: editable P3 report template.
- `references.bib`: optional bibliography with a demonstration entry.
- `IEEEtran.cls` and `IEEEtran_HOWTO.pdf`: official class and documentation.
- `README.md`: these instructions.

Based on the course proposal, P1, and P2 templates and the
[official ISCA 2026 IEEE template](https://iscaconf.org/isca2026/submit/ISCA2026_IEEE_template.zip).
The class is unchanged and retains its authorship and LPPL license notices.
