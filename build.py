#!/usr/bin/env python3
"""Build the COMS 6998 course site.

Reads data/schedule.yaml and data/students.yaml, renders the site into
_site/ (index, schedule, format, project, policies, papers, students)
and copies assets/.

Usage:  python3 build.py
Deps:   pyyaml
"""
from __future__ import annotations

import datetime as dt
import html
import pathlib
import shutil

import yaml

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "_site"

# Set once the repository has a public URL (used for canonical/og:url).
SITE_URL = ""

MODULE_CLASS = {
    "Computing for AI": "m-comp",
    "AI for Computing": "m-ai",
    "Launch": "m-span",
    "Project": "m-proj",
    "Synthesis": "m-span",
}

TYPE_NOTE = {
    "midterm": "Team presentations; no mini-lecture and no assigned papers.",
    "poster": "Poster showcase; no mini-lecture and no assigned papers.",
}


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def fmt_short(d: dt.date) -> str:
    return d.strftime("%b %-d")


def fmt_long(d: dt.date) -> str:
    return d.strftime("%A, %B %-d, %Y")


# ---------------------------------------------------------------- data

data = yaml.safe_load((ROOT / "data" / "schedule.yaml").read_text())
students_data = yaml.safe_load((ROOT / "data" / "students.yaml").read_text())

course = data["course"]
inst = course["instructor"]
weeks = data["weeks"]
milestones = data["milestones"]
grading = data["grading"]
registrar = data["registrar_dates"]
students = students_data.get("students") or []

no_class = [r for r in registrar if str(r["note"]).lower().startswith("no class")]


# ---------------------------------------------------------------- shared page shell

NAV_ITEMS = [
    ("schedule.html", "Schedule"),
    ("format.html", "Format"),
    ("project.html", "Project"),
    ("policies.html", "Policies"),
    ("papers.html", "Papers"),
    ("students.html", "Students"),
]


def page(*, title: str, description: str, body: str, path: str) -> str:
    canonical = ""
    if SITE_URL:
        canonical = (
            f'\n  <link rel="canonical" href="{esc(SITE_URL.rstrip("/") + "/" + path)}">'
            f'\n  <meta property="og:url" content="{esc(SITE_URL.rstrip("/") + "/" + path)}">'
        )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:site_name" content="COMS 6998 · AI-Native Computing">
  <meta name="twitter:card" content="summary">{canonical}
  <meta name="theme-color" media="(prefers-color-scheme: light)" content="#fbfbf8">
  <meta name="theme-color" media="(prefers-color-scheme: dark)" content="#0e1116">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..600;1,8..60,400..600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/style.css">
  <script>
    (function () {{
      var t = null;
      try {{ t = localStorage.getItem("cs6998-theme"); }} catch (e) {{}}
      var q = new URLSearchParams(location.search).get("theme");
      if (q === "light" || q === "dark") t = q;
      if (t === "light" || t === "dark") document.documentElement.setAttribute("data-theme", t);
    }})();
  </script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
{nav(path)}
<main id="main">
{body}
</main>
{footer()}
<script src="assets/site.js"></script>
</body>
</html>
"""


def nav(path: str) -> str:
    links = []
    for href, label in NAV_ITEMS:
        cls = ' class="active"' if path == href else ""
        links.append(f'<a href="{href}"{cls}>{label}</a>')
    links.append(
        f'<a href="{esc(inst["lab"])}" target="_blank" rel="noopener">Group<span class="ext" aria-hidden="true">↗</span></a>'
    )
    return f"""<header class="site-head">
  <nav class="wrap" aria-label="Site">
    <a class="brand" href="index.html">
      <span class="brand-mark" aria-hidden="true">⇄</span>
      <span><strong>COMS 6998</strong> <span class="brand-sub">AI-Native Computing</span></span>
    </a>
    <div class="nav-links">
      {chr(10).join(links)}
      <button id="theme-toggle" type="button" aria-label="Toggle color theme" title="Toggle color theme">
        <span class="ico-sun" aria-hidden="true">☀</span><span class="ico-moon" aria-hidden="true">☾</span>
      </button>
    </div>
  </nav>
</header>"""


def footer() -> str:
    today = fmt_long(dt.date.today())
    return f"""<footer class="site-foot">
  <div class="wrap foot-grid">
    <div>
      <strong>COMS 6998 · AI-Native Computing</strong><br>
      {esc(course["semester"])} · Columbia University<br>
      <a href="https://www.cs.columbia.edu/" target="_blank" rel="noopener">Department of Computer Science</a>
    </div>
    <div>
      <a href="https://registrar.columbia.edu/content/academic-calendar" target="_blank" rel="noopener">Registrar academic calendar</a><br>
      <a href="papers.html">Reading list</a><br>
      <a href="{esc(inst["homepage"])}" target="_blank" rel="noopener">Instructor Webpage</a> · <a href="{esc(inst["lab"])}" target="_blank" rel="noopener">Research Group</a>
    </div>
    <div class="foot-meta">
      Last updated {esc(today)}.
    </div>
  </div>
</footer>"""


def page_head(title: str, lede: str = "") -> str:
    lede_html = f'<p class="section-lede">{lede}</p>' if lede else ""
    return f'<h1 class="page-title">{title}</h1>\n{lede_html}'


# ---------------------------------------------------------------- home

def hero() -> str:
    return f"""<section class="hero" id="top">
  <div class="wrap hero-grid">
    <div class="hero-main">
      <p class="eyebrow">{esc(course["number"])} · Columbia University · {esc(course["semester"])}</p>
      <h1>AI-Native Computing</h1>
      <p class="duality-line">
        <span class="d-comp">Hardware for AI</span>
        <span class="d-arrows" aria-hidden="true">⇄</span>
        <span class="d-ai">AI for Hardware</span>
      </p>
      <blockquote class="thesis">AI is transforming computing in two directions: emerging AI workloads demand new hardware and system architectures, while AI is becoming a powerful tool for designing computing systems themselves.</blockquote>
      <ul class="meta-chips">
        <li><strong>Time:</strong> {esc(course["meeting"])}</li>
        <li><strong>Location:</strong> {esc(course["location"])}</li>
      </ul>
    </div>
    <aside class="instructor-card" aria-label="Instructor">
      <p class="card-kicker">Instructor</p>
      <p class="inst-name">{esc(inst["name"])}</p>
      <ul class="inst-links">
        <li><a href="mailto:{esc(inst["email"])}">Email</a></li>
        <li><a href="{esc(inst["homepage"])}" target="_blank" rel="noopener">Instructor Webpage</a></li>
        <li><a href="{esc(inst["lab"])}" target="_blank" rel="noopener">Research Group</a></li>
        <li><a href="{esc(inst["canvas"])}" target="_blank" rel="noopener">Canvas</a></li>
      </ul>
      <ul class="tbd-list">
        <li><span>Office hours</span> <span class="oh">{esc(inst["office_hours"])}</span></li>
      </ul>
    </aside>
  </div>
  <div class="wrap duality-panel">
    <div class="d-card d-card-comp">
      <h2><span class="d-dir" aria-hidden="true">→</span> Computing for AI</h2>
      <p>Profile, serve, schedule, map, accelerate, and make reliable emerging LLM, agentic, physical, and compositional AI workloads.</p>
    </div>
    <div class="d-card d-card-ai">
      <h2><span class="d-dir" aria-hidden="true">←</span> AI for Computing</h2>
      <p>Use agents to design, optimize, and verify software, compilers, architectures, SoCs, RTL, EDA flows, and chips.</p>
    </div>
    <div class="d-shared">
      <strong>Shared methodology.</strong> Dynamic workflows, closed-loop feedback, cross-layer optimization, heterogeneous resources, quality-performance-cost tradeoffs, and evidence-driven evaluation.
    </div>
  </div>
</section>"""


def short_deadlines(w: dict) -> str:
    """Compress a week's deadline strings for the at-a-glance table."""
    outs = []
    for d in w.get("deadlines", []):
        outs.append(d.split(" - ", 1)[1].strip() if " - " in d else d)
    return "; ".join(outs)


def glance_html() -> str:
    rows, holidays, hi = [], sorted(no_class, key=lambda r: r["date"]), 0
    for w in weeks:
        while hi < len(holidays) and holidays[hi]["date"] < w["date"]:
            r = holidays[hi]
            rows.append(
                f'<tr class="g-holiday"><td>-</td><td>{esc(fmt_short(r["date"]))}</td>'
                f'<td colspan="2">{esc(r["note"])}</td></tr>'
            )
            hi += 1
        dot = f'<span class="dot g-dot {MODULE_CLASS.get(w["module"], "m-span")}" aria-hidden="true"></span>'
        dl = esc(short_deadlines(w))
        rows.append(
            f'<tr><td>{w["week"]}</td><td>{esc(fmt_short(w["date"]))}</td>'
            f'<td>{dot}<a href="schedule.html#week-{w["week"]}">{esc(w["title"])}</a></td>'
            f'<td class="g-dl">{dl or "-"}</td></tr>'
        )
    return f"""<section class="section" id="glance" aria-labelledby="glance-h">
  <div class="wrap">
    <div class="section-head">
      <h2 id="glance-h">Schedule at a glance</h2>
      <div class="sched-tools">
        <span class="legend"><span class="dot dot-comp" aria-hidden="true"></span>Computing for AI</span>
        <span class="legend"><span class="dot dot-ai" aria-hidden="true"></span>AI for Computing</span>
        <a class="tool-link" href="schedule.html">Full schedule with readings →</a>
      </div>
    </div>
    <div class="table-scroll">
      <table class="glance-table">
        <thead><tr><th>Wk</th><th>Date</th><th>Topic</th><th>Project Deadline</th></tr></thead>
        <tbody>
          {chr(10).join(rows)}
        </tbody>
      </table>
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------- schedule

def paper_li(p: dict, kind: str) -> str:
    title = esc(p["title"])
    if p.get("url"):
        title_html = f'<a href="{esc(p["url"])}" target="_blank" rel="noopener">{title}</a>'
        note = ""
    else:
        title_html = title
        note = ' <span class="pending">(arXiv link coming in September)</span>'
    bits = [f'<span class="p-title">{title_html}</span>{note}',
            f'<span class="venue">{esc(p["venue"])}</span>']
    if p.get("co_led"):
        bits.append('<span class="chip chip-coled">co-led by a pair</span>')
    extras = []
    if p.get("companion_url"):
        extras.append(f'<a class="p-extra" href="{esc(p["companion_url"])}" target="_blank" rel="noopener">companion critique</a>')
    if p.get("extra_link"):
        extras.append(f'<a class="p-extra" href="{esc(p["extra_link"])}" target="_blank" rel="noopener">project site</a>')
    bits.extend(extras)
    focus = f'<span class="focus">{esc(p["focus"])}</span>' if p.get("focus") else ""
    return f'<li class="{kind}"><div class="p-head">{" ".join(bits)}</div>{focus}</li>'


def optional_entry(o) -> str:
    """An optional reading is either a plain string or {title, url}."""
    if isinstance(o, dict):
        if o.get("url"):
            return f'<a href="{esc(o["url"])}" target="_blank" rel="noopener">{esc(o["title"])}</a>'
        return esc(o["title"])
    return esc(o)


def week_article(w: dict) -> str:
    mod = w["module"]
    mcls = MODULE_CLASS.get(mod, "m-span")
    date = w["date"]

    tags = [f'<span class="chip chip-mod">{esc(mod)}</span>']
    if w.get("guest"):
        tags.append(f'<span class="chip chip-guest">🎤 {esc(w["guest"]["label"])}</span>')

    body = [f'<div class="week-tags">{"".join(tags)}<span class="chip chip-now" hidden>this week</span></div>',
            f'<h3 class="week-title">{esc(w["title"])}</h3>']

    if w.get("guest"):
        body.append(f'<p class="week-note">Guest lecture: {esc(w["guest"]["topic"])}.</p>')
    if w.get("case_study"):
        cs = esc(w["case_study"])
        if "ArchOrchestra" in w["case_study"]:
            cs += ' <span class="pending">(arXiv link coming in September)</span>'
        body.append(f'<p class="week-note"><strong>Mini-lecture case study:</strong> {cs}</p>')
    if w.get("exercise"):
        body.append(f'<p class="week-note"><strong>In-class exercise:</strong> {esc(w["exercise"])}</p>')
    if w["type"] in TYPE_NOTE:
        body.append(f'<p class="week-note">{TYPE_NOTE[w["type"]]}</p>')

    if w.get("papers"):
        lis = "\n".join(paper_li(p, "req") for p in w["papers"])
        body.append(f'<p class="p-label">Student-led papers</p><ol class="papers">{lis}</ol>')
    elif w.get("background"):
        lis = "\n".join(paper_li(p, "req") for p in w["background"])
        body.append(f'<p class="p-label">Instructor-selected background · no student presentation</p><ol class="papers">{lis}</ol>')

    if w.get("optional"):
        opts = " · ".join(optional_entry(o) for o in w["optional"])
        body.append(
            f'<details class="optional"><summary>Optional readings <span class="opt-count">({len(w["optional"])})</span></summary>'
            f'<p class="opt-body">{opts}</p></details>'
        )

    if w.get("deadlines"):
        chips = "".join(f'<li>{esc(d)}</li>' for d in w["deadlines"])
        body.append(f'<ul class="deadlines">{chips}</ul>')

    return f"""<article class="week {mcls}" id="week-{w["week"]}" data-date="{date.isoformat()}">
  <div class="week-rail">
    <span class="wk-num">{w["week"]:02d}</span>
    <time class="wk-date" datetime="{date.isoformat()}" title="{esc(fmt_long(date))}">{esc(fmt_short(date))}</time>
  </div>
  <div class="week-body">
    {chr(10).join(body)}
  </div>
</article>"""


def holiday_article(r: dict) -> str:
    date = r["date"]
    return f"""<article class="week m-holiday" data-date="{date.isoformat()}" data-noclass="1">
  <div class="week-rail">
    <span class="wk-num" aria-hidden="true">-</span>
    <time class="wk-date" datetime="{date.isoformat()}">{esc(fmt_short(date))}</time>
  </div>
  <div class="week-body"><p class="week-title holiday-title">{esc(r["note"])}</p></div>
</article>"""


def schedule_body() -> str:
    rows, holidays = [], sorted(no_class, key=lambda r: r["date"])
    hi = 0
    for w in weeks:
        while hi < len(holidays) and holidays[hi]["date"] < w["date"]:
            rows.append(holiday_article(holidays[hi]))
            hi += 1
        rows.append(week_article(w))
    for r in holidays[hi:]:
        rows.append(holiday_article(r))

    current_attr = f' data-current-week="{data["current_week"]}"' if data.get("current_week") else ""
    reg = " · ".join(f'{esc(fmt_short(r["date"]))}: {esc(r["note"])}' for r in registrar)
    return f"""<section class="section" id="schedule">
  <div class="wrap">
    <div class="section-head">
      {page_head("Schedule")}
      <div class="sched-tools">
        <span class="legend"><span class="dot dot-comp" aria-hidden="true"></span>Computing for AI</span>
        <span class="legend"><span class="dot dot-ai" aria-hidden="true"></span>AI for Computing</span>
        <button type="button" id="toggle-optionals" data-state="closed">Expand optional readings</button>
      </div>
    </div>
    <p class="section-lede">13 Friday meetings, {esc(course["meeting"].replace("Fridays ", ""))}, {esc(course["location"])}. Presentation slides are due 11:59 PM the Thursday before class; evidence capsules 11:59 PM the following Monday.</p>
    <div class="weeks"{current_attr}>
      {chr(10).join(rows)}
    </div>
    <p class="registrar-line"><strong>Registrar dates:</strong> {reg} · <a href="https://registrar.columbia.edu/content/academic-calendar" target="_blank" rel="noopener">academic calendar</a></p>
  </div>
</section>"""


# ---------------------------------------------------------------- format & grading

def format_body() -> str:
    grading_rows = "\n".join(
        f"""<tr><td>{esc(g["component"])}</td>
<td class="w-num">{g["weight"]}%</td>
<td class="w-bar"><span style="width:{g["weight"] * 2}%"></span></td></tr>"""
        for g in grading
    )
    questions = [
        "What is the paper's exact central claim?",
        "Which experiment most directly supports that claim?",
        "What hidden assumption is most likely to break?",
        "Is the baseline fair and budget-matched?",
        "Which conclusion extends beyond the presented evidence?",
        "What single additional experiment would most change confidence in the result?",
    ]
    q_lis = "\n".join(f"<li>{q}</li>" for q in questions)

    return f"""<section class="section" id="format">
  <div class="wrap">
    {page_head("Course format &amp; grading",
               "Advanced graduate lecture-seminar with a semester-long research project. Nine seminar meetings provide 23 paper-lead slots; every student leads exactly once. There are no exams and no problem sets.")}

    <div class="col2">
      <div class="panel">
        <h3>Regular seminar · 110 minutes</h3>
        <table class="time-table">
          <tr><td>10:10-10:35</td><td>Instructor mini-lecture: concepts, methods, cross-paper connections</td></tr>
          <tr><td>10:35-11:00</td><td>Paper 1 - presentation, critique, discussion</td></tr>
          <tr><td>11:00-11:10</td><td>Break</td></tr>
          <tr><td>11:10-11:35</td><td>Paper 2 - presentation, critique, discussion</td></tr>
          <tr><td>11:35-12:00</td><td>Paper 3 - presentation, critique, discussion</td></tr>
        </table>
      </div>
      <div class="panel">
        <h3>Guest-speaker weeks</h3>
        <table class="time-table">
          <tr><td>10:10-10:35</td><td>Paper 1 - presentation, critique, discussion</td></tr>
          <tr><td>10:35-11:00</td><td>Paper 2 - presentation, critique, discussion</td></tr>
          <tr><td>11:00-11:10</td><td>Break</td></tr>
          <tr><td>11:10-12:00</td><td>Guest lecture + Q&amp;A</td></tr>
        </table>
      </div>
    </div>

    <div class="panel lead-panel">
      <h3>Student-Led Paper Presentation · the 25-minute block</h3>
      <div class="lead-blocks">
        <div class="lead-block"><span class="lead-min">12 min</span> problem, context, mechanism, and the minimum results needed to understand the paper</div>
        <div class="lead-block"><span class="lead-min">8 min</span> critical analysis of claims, baselines, assumptions, methodology, and missing evidence</div>
        <div class="lead-block"><span class="lead-min">5 min</span> facilitated discussion around two or three precise questions</div>
      </div>
      <p class="fine">Presenters read the full paper, appendices, and artifact documentation. Everyone else reads the abstract, introduction, core method, principal results, and limitations of all assigned papers, and arrives with at least one discussion question. No weekly summary reports.</p>
    </div>

    <div class="col2">
      <div class="panel">
        <h3>Grading</h3>
        <table class="grading-table">
          {grading_rows}
        </table>
        <p class="fine">Grades reflect research judgment, technical execution, evidence quality, communication, and reproducibility - not whether a project happens to beat the state of the art. A rigorous negative result can earn full credit.</p>
      </div>
      <div class="panel">
        <h3>Evidence-centered discussion</h3>
        <p class="fine">Every paper discussion returns to six questions:</p>
        <ol class="q-list">
          {q_lis}
        </ol>
      </div>
    </div>

    <div class="panel">
      <h3>Who should take this course</h3>
      <p>Graduate students in CS and EE interested in computer architecture, systems, ML systems, hardware-software co-design, robotics and physical AI, VLSI/EDA, or adjacent areas. Expected: basic computer organization or systems knowledge, familiarity with ML concepts, and the ability to program and run quantitative experiments. CUDA, compilers, RTL, robotics simulators, or LLM-agent experience is helpful but not required - no one is expected to arrive with expertise across the entire stack.</p>
      <p class="fine"><strong>Scope note.</strong> The course concentrates on inference-side and emerging AI workloads and on AI-driven design; deep coverage of large-scale training systems and model-compression algorithms is left to ML-systems courses. Week 2 provides the working knowledge needed here.</p>
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------- project

def project_body() -> str:
    tl_items = []
    for m in milestones:
        cls = " tl-major" if m["id"] in ("Midterm", "Poster", "Final") else ""
        tl_items.append(
            f"""<li class="tl-item{cls}">
  <span class="tl-dot" aria-hidden="true"></span>
  <time datetime="{m["date"].isoformat()}">{esc(fmt_short(m["date"]))}</time>
  <span class="tl-id">{esc(m["id"])}</span>
  <span class="tl-name">{esc(m["name"])}</span>
</li>"""
        )
    standard = [
        "A falsifiable research question and a precise intended claim.",
        "At least two meaningful baselines, including a classical or non-agentic baseline where applicable.",
        "A mechanism, not only a correlation or leaderboard result.",
        "At least one ablation or controlled intervention tied to the central claim.",
        "Joint reporting of task quality or success and relevant systems metrics.",
        "A held-out workload, configuration, system scale, or design budget.",
        "Explicit compute, GPU, API, token, simulation, and wall-clock budgets.",
        "Failure-case analysis, including invalid actions and tool failures for agentic design systems.",
        "Reproducible code, environment instructions, configurations, data, and figure-generation scripts.",
    ]
    std_lis = "\n".join(f"<li>{s}</li>" for s in standard)

    return f"""<section class="section" id="project">
  <div class="wrap">
    {page_head("Semester-long research project",
               "The project is the center of the course: a carefully scoped research effort that could mature into a top-tier architecture, systems, ML systems, robotics, or EDA paper. Teams of 1-2 are formed by bidding on a curated portfolio of directions; publication is an aspiration, not a grading requirement.")}

    <div class="tracks tracks-2">
      <div class="track t-comp">
        <p class="track-id">Track A</p>
        <h3>Computing for AI</h3>
        <p>Profile, serve, schedule, map, accelerate, or make reliable an LLM, agentic, physical, or neuro-symbolic workload.</p>
      </div>
      <div class="track t-ai">
        <p class="track-id">Track B</p>
        <h3>AI for Computing</h3>
        <p>Build and rigorously evaluate an agent for software optimization, compilers, GPU kernels, architecture DSE, RTL/EDA, or verification.</p>
      </div>
    </div>

    <div class="col2 col2-project">
      <div class="panel">
        <h3>Minimum research standard</h3>
        <ul class="std-list">
          {std_lis}
        </ul>
      </div>
      <div class="panel">
        <h3>Milestones</h3>
        <ol class="timeline">
          {chr(10).join(tl_items)}
        </ol>
        <p class="fine">All written deliverables are due 11:59 PM ET. Check-ins P1-P5 are pacing devices, graded on completeness. No course deadline falls on the Thanksgiving holiday.</p>
      </div>
    </div>

    <div class="panel">
      <h3>Final submission</h3>
      <p>An eight- to ten-page conference-style paper (excluding references and appendices); a repository with pinned environment, one-command smoke test, and a documented reproduction path for one central result; machine-readable results with scripts regenerating principal figures; an experiment manifest covering seeds, configurations, models, machines, tool versions, and resource budgets; a response-to-feedback memo and individual contribution statements.</p>
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------- policies

def policies_body() -> str:
    return f"""<section class="section" id="policies">
  <div class="wrap">
    {page_head("Policies")}

    <div class="panel policy-ai">
      <h3>AI use and evidence</h3>
      <p class="policy-stance">AI use is permitted and encouraged when it is disclosed, reproducible, and independently verified. Agent output is not evidence by itself.</p>
      <ul class="policy-list">
        <li>You may use AI throughout the course - brainstorming, literature discovery, coding, debugging, experiment orchestration, and writing assistance - with meaningful use disclosed.</li>
        <li>Every citation must be checked against a primary source, and every numerical result must trace to an actual experiment, simulator output, formal result, or cited source.</li>
        <li>AI-generated code must satisfy the same correctness, testing, performance, licensing, and provenance requirements as human-written code.</li>
      </ul>
    </div>

    <div class="policy-grid">
      <div class="panel">
        <h3>Academic integrity</h3>
        <p>Students must follow Columbia academic-integrity policies. Fabricated citations, invented experiments, altered logs, undisclosed result selection, plagiarism, or presenting agent-generated claims as verified evidence are serious violations. When in doubt, disclose the tool, source, assistance, or collaboration.</p>
      </div>
      <div class="panel">
        <h3>Collaboration &amp; authorship</h3>
        <p>Course collaboration does not automatically establish publication authorship. If a project continues after the semester, authorship and ordering follow substantive intellectual and technical contributions, manuscript participation, accountability, and venue policies. Students retain credit for their work; continuation plans should be discussed transparently with the instructor and research mentors.</p>
      </div>
      <div class="panel">
        <h3>Accessibility &amp; accommodations</h3>
        <p>Students who require disability-related accommodations should contact Columbia Disability Services and inform the instructor as early as possible so approved accommodations can be implemented. Please communicate time-sensitive circumstances before deadlines whenever possible.</p>
      </div>
      <div class="panel">
        <h3>Resource fairness</h3>
        <p>Projects report GPU, API, token, simulation, and wall-clock budgets. Grades are not based on access to the largest model or most GPUs. Every project defines a fallback experiment that remains valid if an API, simulator, board, robot, or cloud resource becomes unavailable. Curated starter environments and smoke tests are provided for officially supported directions when feasible.</p>
      </div>
      <div class="panel">
        <h3>Late work</h3>
        <p>Each team may use one 48-hour grace pass on a written milestone, requested before the deadline. The grace pass does not apply to in-class presentations, the final poster, or the final submission. Other extensions require prior approval or documented circumstances.</p>
      </div>
      <div class="panel">
        <h3>Changes to the syllabus</h3>
        <p>This is a first-offering advanced-topics course in a rapidly changing research area. Individual readings, project briefs, guest-speaker scheduling, or detailed deadlines may be updated when new work appears or infrastructure changes. Material changes will be announced clearly and will not retroactively disadvantage students.</p>
      </div>
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------- students

def initials(name: str) -> str:
    parts = [p for p in name.split() if p]
    return "".join(p[0].upper() for p in parts[:2]) or "?"


def students_body() -> str:
    if not students:
        cards = """<div class="panel roster-empty">
      <p>The class roster will appear here once enrollment is finalized in September.</p>
    </div>"""
    else:
        items = []
        for s in students:
            if s.get("photo"):
                avatar = f'<img class="stu-photo" src="{esc(s["photo"])}" alt="" loading="lazy">'
            else:
                avatar = f'<span class="stu-photo stu-initials" aria-hidden="true">{esc(initials(s["name"]))}</span>'
            name = esc(s["name"])
            if s.get("link"):
                name = f'<a href="{esc(s["link"])}" target="_blank" rel="noopener">{name}</a>'
            items.append(f'<li class="stu-card">{avatar}<span class="stu-name">{name}</span></li>')
        cards = f'<ul class="students-grid">{chr(10).join(items)}</ul>'
    return f"""<section class="section" id="students">
  <div class="wrap">
    {page_head("Students",
               "The people of COMS 6998, Fall 2026.")}
    {cards}
  </div>
</section>"""


# ---------------------------------------------------------------- papers page

def papers_body() -> str:
    blocks = []
    n_req = sum(len(w.get("papers", []) or w.get("background", [])) for w in weeks)
    n_opt = sum(len(w.get("optional", [])) for w in weeks)
    for w in weeks:
        req = w.get("papers") or w.get("background")
        if not req and not w.get("optional"):
            continue
        label = "Student-led papers" if w.get("papers") else "Instructor-selected background"
        lis = "\n".join(paper_li(p, "req") for p in (req or []))
        opt = ""
        if w.get("optional"):
            opt = f'<p class="p-label">Optional</p><p class="opt-body">{" · ".join(optional_entry(o) for o in w["optional"])}</p>'
        blocks.append(
            f"""<article class="papers-week {MODULE_CLASS.get(w["module"], "m-span")}">
  <div class="week-tags"><span class="chip chip-mod">{esc(w["module"])}</span></div>
  <h2><span class="wk-tag">Wk {w["week"]:02d} · {esc(fmt_short(w["date"]))}</span> {esc(w["title"])}</h2>
  <p class="p-label">{label}</p>
  <ol class="papers">{lis}</ol>
  {opt}
</article>"""
        )
    return f"""<section class="section papers-index">
  <div class="wrap">
    {page_head("Reading list",
               f'All {n_req} required readings and {n_opt} optional readings, by week. Links were individually verified against primary sources in August 2026. <a href="schedule.html">Back to the schedule.</a>')}
    <div class="sched-tools papers-legend">
      <span class="legend"><span class="dot dot-comp" aria-hidden="true"></span>Computing for AI</span>
      <span class="legend"><span class="dot dot-ai" aria-hidden="true"></span>AI for Computing</span>
    </div>
    {chr(10).join(blocks)}
  </div>
</section>"""


# ---------------------------------------------------------------- build

def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "assets", OUT / "assets")

    desc = ("COMS 6998, Columbia University, Fall 2026. Graduate seminar on hardware and systems "
            "for AI workloads, and AI agents for designing computing systems. Fridays 10:10-12:00.")
    pages = {
        "index.html": ("COMS 6998 · AI-Native Computing · Fall 2026", desc,
                       "\n".join([hero(), glance_html()])),
        "schedule.html": ("Schedule · COMS 6998 AI-Native Computing",
                          "Weekly schedule with required and optional readings for COMS 6998 (Fall 2026).",
                          schedule_body()),
        "format.html": ("Format & grading · COMS 6998 AI-Native Computing",
                        "Seminar format, paper presentations, and grading for COMS 6998 (Fall 2026).",
                        format_body()),
        "project.html": ("Project · COMS 6998 AI-Native Computing",
                         "Semester-long research project: tracks, research standard, and milestones.",
                         project_body()),
        "policies.html": ("Policies · COMS 6998 AI-Native Computing",
                          "Course policies for COMS 6998 (Fall 2026), including the AI-use policy.",
                          policies_body()),
        "papers.html": ("Reading list · COMS 6998 AI-Native Computing",
                        "All required and optional readings for COMS 6998 (Fall 2026), by week.",
                        papers_body()),
        "students.html": ("Students · COMS 6998 AI-Native Computing",
                          "The students of COMS 6998 (Fall 2026).",
                          students_body()),
    }
    for path, (title, d, body) in pages.items():
        (OUT / path).write_text(page(title=title, description=d, body=body, path=path))

    print(f"Built {OUT} ({sum(1 for _ in OUT.rglob('*') if _.is_file())} files)")


if __name__ == "__main__":
    main()
