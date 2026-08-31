#!/usr/bin/env python3
"""Build the COMS 6998 course site.

Reads data/schedule.yaml and data/students.yaml, renders the site into
_site/ (index, schedule, format, project, policies, papers, students)
and copies assets/. It also regenerates the student-facing syllabus.md.

Usage:  python3 build.py
Deps:   pyyaml
"""
from __future__ import annotations

import datetime as dt
import html
import os
import pathlib
import re
import shutil
from zoneinfo import ZoneInfo

import yaml

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "_site"

def public_site_url() -> str:
    """Resolve the public origin without hard-coding a repository name.

    SITE_URL wins when set explicitly. On GitHub Actions, infer the normal
    GitHub Pages URL from GITHUB_REPOSITORY (owner/repository).
    """
    explicit = os.environ.get("SITE_URL", "").strip().rstrip("/")
    if explicit:
        return explicit
    repository = os.environ.get("GITHUB_REPOSITORY", "").strip()
    if "/" not in repository:
        return ""
    owner, name = repository.split("/", 1)
    root_repo = f"{owner}.github.io"
    suffix = "" if name.lower() == root_repo.lower() else f"/{name}"
    return f"https://{owner}.github.io{suffix}"


SITE_URL = public_site_url()
COURSE_TZ = ZoneInfo("America/New_York")

MODULE_CLASS = {
    "Computing for AI": "m-comp",
    "AI for Computing": "m-ai",
    "Launch": "m-span",
    "Project": "m-proj",
    "Synthesis": "m-span",
}

# Divider labels inserted before the first week of each module.
MODULE_DIVIDERS = {
    "Computing for AI": ("m-comp", "Module 1: Computing for AI"),
    "AI for Computing": ("m-ai", "Module 2: AI for Computing"),
}

TYPE_NOTE = {
    "midterm": "Team presentations; no mini-lecture and no assigned papers.",
    "poster": "Poster showcase; no mini-lecture and no assigned papers.",
}

COURSE_THESIS = (
    "AI is transforming computing in two directions: emerging AI workloads demand new "
    "hardware and system architectures, while AI is becoming a powerful tool for designing "
    "computing systems themselves."
)

LEARNING_OUTCOMES = [
    ("Profile and diagnose AI systems.",
     "Represent an AI application as a pipeline, dynamic DAG, or feedback loop; measure latency, throughput, utilization, energy, and cost; locate bottlenecks with roofline reasoning, queueing, and trace analysis."),
    ("Reason across the stack.",
     "Connect model, software, runtime, architecture, memory, accelerator, SoC, and deployment decisions, and evaluate joint quality-performance-energy-cost tradeoffs."),
    ("Serve and accelerate emerging workloads.",
     "LLM and agent serving, embodied and physical AI inference, neuro-symbolic acceleration, datacenter accelerators, and SoCs."),
    ("Build AI that designs computing systems.",
     "Formulate system design as an agent environment with state, actions, tools, and feedback; compare LLM agents, RL, Bayesian optimization, and classical heuristics under matched budgets."),
    ("Audit claims like a reviewer.",
     "Read papers and industry claims against baselines, budgets, ablations, and held-out evidence."),
    ("Produce conference-style research.",
     "A semester-long project with meaningful baselines, ablations, failure analysis, and a reproducible artifact."),
]

PREREQUISITES = [
    ("Expected", "Basic computer organization or systems knowledge, familiarity with machine-learning concepts, and the ability to program and run quantitative experiments."),
    ("Helpful, not required", "Experience with CUDA, compilers, digital design, RTL, EDA, robotics simulators, FPGA platforms, LLM agents, or research-paper reading. No one is expected to arrive with expertise across the entire stack."),
    ("Project readiness", "Each team should bring enough complementary expertise to implement, measure, and evaluate its selected project."),
]

REGULAR_FORMAT = [
    ("10:10-10:35", "Instructor mini-lecture: concepts, methods, cross-paper connections"),
    ("10:35-11:00", "Paper 1 - presentation, critique, discussion"),
    ("11:00-11:10", "Break"),
    ("11:10-11:35", "Paper 2 - presentation, critique, discussion"),
    ("11:35-12:00", "Paper 3 - presentation, critique, discussion"),
]

GUEST_FORMAT = [
    ("10:10-10:35", "Paper 1 - presentation, critique, discussion"),
    ("10:35-11:00", "Paper 2 - presentation, critique, discussion"),
    ("11:00-11:10", "Break"),
    ("11:10-12:00", "Guest lecture + Q&A"),
]

DISCUSSION_QUESTIONS = [
    "What is the paper's exact central claim?",
    "Which experiment most directly supports that claim?",
    "What hidden assumption is most likely to break?",
    "Is the baseline fair and budget-matched?",
    "Which conclusion extends beyond the presented evidence?",
    "What single additional experiment would most change confidence in the result?",
]

RESEARCH_STANDARD = [
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

PROJECT_OVERVIEW = (
    "The project is the center of the course: a carefully scoped research effort that could "
    "mature into a top-tier architecture, systems, ML systems, robotics, or EDA paper. Teams "
    "of 1-2 are formed by bidding on a curated portfolio of directions; publication is an "
    "aspiration, not a grading requirement."
)

PROJECT_TRACKS = [
    ("Track A", "Computing for AI",
     "Profile, serve, schedule, map, accelerate, or make reliable an LLM, agentic, physical, or neuro-symbolic workload."),
    ("Track B", "AI for Computing",
     "Build and rigorously evaluate an agent for software optimization, compilers, GPU kernels, architecture DSE, RTL/EDA, or verification."),
]

PROJECT_DIRECTIONS_NOTE = (
    "A titles-only preview of the curated project portfolio. Full briefs with research "
    "questions, baselines, evaluation plans, and platforms will be released at the Week 2 "
    "research marketplace; directions may be added, merged, or refined before bidding opens."
)

PROJECT_DIRECTIONS = [
    ("Module 1: Computing for AI", [
        "SwarmServe - workflow-aware scheduling for multi-agent LLM serving",
        "CacheCraft - program-structure-aware KV-cache retention and tiering",
        "MuxFlow - small-language-model orchestration under real serving load",
        "AgentShield - fault tolerance for multi-step agentic LLM pipelines",
        "ActSpec - deadline-aware speculative action generation for real-time VLAs",
        "VLA-Roof - an analytical performance model for VLA inference",
        "FleetBatch - deadline-aware multi-robot serving on shared GPUs",
        "SceneCache - consumer-aware caching for 3D scene representations",
        "PlanFuse - profiling and co-scheduling hybrid VLA + motion-planning stacks",
        "FaultLine - joint adversarial and soft-error robustness for VLA control",
        "SymKern - demystifying and optimizing neuro-symbolic kernels on GPUs",
        "SysTwo - systems characterization of System-2 (test-time-compute) inference",
        "ESP-Reason - a reasoning-accelerator tile on the ESP SoC platform (FPGA)",
        "HoloCIM - a compute-in-memory noise-budget study for vector-symbolic AI",
        "HotPath - the kernel-to-system conversion rate of component speedups",
        "WattGuard - energy-SLO co-control for edge AI inference",
    ]),
    ("Module 2: AI for Computing", [
        "KernelScope - does profiler feedback make GPU-kernel agents better, per token?",
        "MapSmith - LLM agents vs. classical search for accelerator mapping",
        "FairDSE - a budget-matched showdown: LLM agents vs. BO/RL/GA for architecture DSE",
        "Signals - which feedback modality buys the most design quality per token?",
        "Ouroboros - an agent co-designs an accelerator for its own workload",
        "ProveGen - RTL generation with verification-in-the-loop, scored by mutation testing",
        "Spec2Socket - an agentic flow from spec to HLS to FPGA-measured accelerator",
        "LACE-Next - workload-driven agentic RISC-V instruction extension",
        "HDLGround - structured retrieval and grounding for hardware-design agents",
        "FlowPilot - log-reading LLM agents vs. black-box autotuners on OpenROAD",
        "SysDoctor - a planted-bottleneck benchmark for AI performance diagnosis",
        "AutopilotServe - a guarded closed-loop agent that keeps a serving stack tuned",
        "AutoEmbody - agents that configure VLA deployments for closed-loop success",
        "RedFlag - reward-hacking forensics and hardened audits for design agents",
    ]),
]

FINAL_SUBMISSION = (
    "An eight- to ten-page conference-style paper (excluding references and appendices); a "
    "repository with pinned environment, one-command smoke test, and a documented reproduction "
    "path for one central result; machine-readable results with scripts regenerating principal "
    "figures; an experiment manifest covering seeds, configurations, models, machines, tool "
    "versions, and resource budgets; a response-to-feedback memo and individual contribution statements."
)

AI_POLICY_STANCE = (
    "AI use is permitted and encouraged when it is disclosed, reproducible, and independently "
    "verified. Agent output is not evidence by itself."
)

AI_POLICY_ITEMS = [
    "You may use AI throughout the course - brainstorming, literature discovery, coding, debugging, experiment orchestration, and writing assistance - with meaningful use disclosed.",
    "Every citation must be checked against a primary source, and every numerical result must trace to an actual experiment, simulator output, formal result, or cited source.",
    "AI-generated code must satisfy the same correctness, testing, performance, licensing, and provenance requirements as human-written code.",
]

POLICY_SECTIONS = [
    ("Academic integrity", "Students must follow Columbia academic-integrity policies. Fabricated citations, invented experiments, altered logs, undisclosed result selection, plagiarism, or presenting agent-generated claims as verified evidence are serious violations. When in doubt, disclose the tool, source, assistance, or collaboration."),
    ("Collaboration & authorship", "Course collaboration does not automatically establish publication authorship. If a project continues after the semester, authorship and ordering follow substantive intellectual and technical contributions, manuscript participation, accountability, and venue policies. Students retain credit for their work; continuation plans should be discussed transparently with the instructor and research mentors."),
    ("Accessibility & accommodations", "Students who require disability-related accommodations should contact Columbia Disability Services and inform the instructor as early as possible so approved accommodations can be implemented. Please communicate time-sensitive circumstances before deadlines whenever possible."),
    ("Resource fairness", "Projects report GPU, API, token, simulation, and wall-clock budgets. Grades are not based on access to the largest model or most GPUs. Every project defines a fallback experiment that remains valid if an API, simulator, board, robot, or cloud resource becomes unavailable. Curated starter environments and smoke tests are provided for officially supported directions when feasible."),
    ("Late work", "Each team may use one 48-hour grace pass on a written milestone, requested before the deadline. The grace pass does not apply to in-class presentations, the final poster, or the final submission. Other extensions require prior approval or documented circumstances."),
    ("Changes to the syllabus", "This is a first-offering advanced-topics course in a rapidly changing research area. Individual readings, project briefs, guest-speaker scheduling, or detailed deadlines may be updated when new work appears or infrastructure changes. Material changes will be announced clearly and will not retroactively disadvantage students."),
]


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def fmt_short(d: dt.date) -> str:
    return d.strftime("%b %-d")


def fmt_long(d: dt.date) -> str:
    return d.strftime("%A, %B %-d, %Y")


# ---------------------------------------------------------------- data

data = yaml.safe_load((ROOT / "data" / "schedule.yaml").read_text())
students_data = yaml.safe_load((ROOT / "data" / "students.yaml").read_text())
announcements_data = yaml.safe_load((ROOT / "data" / "announcements.yaml").read_text())

course = data["course"]
inst = course["instructor"]
weeks = data["weeks"]
milestones = data["milestones"]
grading = data["grading"]
registrar = data["registrar_dates"]
students = students_data.get("students") or []
announcements = sorted(
    announcements_data.get("announcements") or [],
    key=lambda item: item["date"],
    reverse=True,
)

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
    social_image = ""
    twitter_card = "summary"
    if SITE_URL:
        image_url = SITE_URL.rstrip("/") + "/assets/og.png"
        canonical = (
            f'\n  <link rel="canonical" href="{esc(SITE_URL.rstrip("/") + "/" + path)}">'
            f'\n  <meta property="og:url" content="{esc(SITE_URL.rstrip("/") + "/" + path)}">'
        )
        social_image = (
            f'\n  <meta property="og:image" content="{esc(image_url)}">'
            '\n  <meta property="og:image:width" content="1734">'
            '\n  <meta property="og:image:height" content="907">'
            '\n  <meta property="og:image:alt" content="COMS 6998 AI-Native Computing">'
            f'\n  <meta name="twitter:image" content="{esc(image_url)}">'
        )
        twitter_card = "summary_large_image"
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
  <meta property="og:site_name" content="COMS 6998 · AI-Native Computing">{social_image}
  <meta name="twitter:card" content="{twitter_card}">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(description)}">{canonical}
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
      <a href="syllabus.md">Syllabus</a><br>
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
      <blockquote class="thesis">{esc(COURSE_THESIS)}</blockquote>
      <ul class="meta-chips">
        <li><strong>Course Time:</strong> {esc(course["meeting"])}</li>
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
      <h2><span class="d-dir" aria-hidden="true">→</span> Module 1: Computing for AI</h2>
      <p>Profile, serve, schedule, map, accelerate, and make reliable emerging LLM, agentic, physical, and compositional AI workloads.</p>
    </div>
    <div class="d-card d-card-ai">
      <h2><span class="d-dir" aria-hidden="true">←</span> Module 2: AI for Computing</h2>
      <p>Use agents to design, optimize, and verify software, compilers, architectures, SoCs, RTL, EDA flows, and chips.</p>
    </div>
    <div class="d-shared">
      <strong>Shared methodology.</strong> Dynamic workflows, closed-loop feedback, cross-layer optimization, heterogeneous resources, quality-performance-cost tradeoffs, and evidence-driven evaluation.
    </div>
  </div>
</section>"""


def dated_deadlines() -> list[dict]:
    """Return display deadlines with machine-readable local timestamps."""
    pattern = re.compile(
        r"^(?P<date>[A-Z][a-z]{2} \d{1,2})(?:, (?P<time>\d{1,2}:\d{2} [AP]M))? - (?P<label>.+)$"
    )
    year = weeks[0]["date"].year
    records = []
    for week in weeks:
        for raw in week.get("deadlines", []):
            match = pattern.match(raw)
            if not match:
                continue
            clock = match.group("time") or "11:59 PM"
            due = dt.datetime.strptime(
                f'{match.group("date")} {year} {clock}', "%b %d %Y %I:%M %p"
            ).replace(tzinfo=COURSE_TZ)
            display = match.group("date")
            if match.group("time"):
                display += f', {match.group("time")}'
            records.append({"due": due, "display": display, "label": match.group("label")})
    return sorted(records, key=lambda item: item["due"])


def now_html() -> str:
    today = dt.date.today()
    visible_week = next((w for w in weeks if w["date"] >= today), weeks[-1])
    class_cards = []
    for week in weeks:
        required = week.get("papers") or week.get("background") or []
        if required:
            reading_items = "".join(
                f'<li><a href="{esc(p["url"])}" target="_blank" rel="noopener">{esc(p["title"])}</a>'
                f' <span class="venue">{esc(p["venue"])}</span></li>'
                if p.get("url") else f'<li>{esc(p["title"])}</li>'
                for p in required
            )
            readings = f'<ol class="now-readings">{reading_items}</ol>'
        else:
            readings = '<p class="now-empty">No assigned readings.</p>'
        hidden = "" if week is visible_week else " hidden"
        class_cards.append(
            f"""<article class="now-class" data-date="{week['date'].isoformat()}" data-week="{week['week']}"{hidden}>
  <p class="now-label"><span class="now-state">Next class</span> · Week {week['week']:02d} · <time datetime="{week['date'].isoformat()}">{esc(fmt_short(week['date']))}</time></p>
  <h3><a href="schedule.html#week-{week['week']}">{esc(week['title'])}</a></h3>
  <p class="now-subhead">Required reading</p>
  {readings}
</article>"""
        )

    deadlines = dated_deadlines()
    now = dt.datetime.now(COURSE_TZ)
    visible_deadline = next((item for item in deadlines if item["due"] >= now), None)
    deadline_items = []
    for item in deadlines:
        hidden = "" if item is visible_deadline else " hidden"
        deadline_items.append(
            f"""<div class="now-deadline-item" data-due="{item['due'].isoformat()}"{hidden}>
  <time datetime="{item['due'].isoformat()}">{esc(item['display'])}</time>
  <p>{esc(item['label'])}</p>
</div>"""
        )
    if not deadline_items:
        deadline_items.append('<p class="now-empty">No upcoming deadlines.</p>')

    news_items = "\n".join(
        f"""<li>
  <time datetime="{item['date'].isoformat()}">{esc(fmt_short(item['date']))}</time>
  <div><strong>{esc(item['title'])}</strong><p>{esc(item['body'])}</p></div>
</li>"""
        for item in announcements[:3]
    )

    return f"""<section class="now-section" id="now" aria-labelledby="now-h">
  <div class="wrap">
    <div class="now-heading">
      <p class="eyebrow">Now</p>
      <h2 id="now-h">Start here this week</h2>
    </div>
    <div class="now-grid">
      <div class="now-panel now-class-panel">
        {chr(10).join(class_cards)}
      </div>
      <div class="now-panel now-deadline-panel">
        <p class="now-kicker">Next deadline</p>
        {chr(10).join(deadline_items)}
        <p class="now-empty" id="now-no-deadline" hidden>No upcoming deadlines.</p>
      </div>
      <div class="now-panel now-news-panel">
        <p class="now-kicker">Announcements</p>
        <ol class="now-news">{news_items}</ol>
      </div>
    </div>
  </div>
</section>"""


def learn_html() -> str:
    items = "\n".join(
        f'<div class="learn-card"><p><strong>{lead}</strong> {body}</p></div>'
        for lead, body in LEARNING_OUTCOMES
    )
    return f"""<section class="section" id="learn" aria-labelledby="learn-h">
  <div class="wrap">
    <h2 id="learn-h">What you'll learn</h2>
    <div class="learn-grid">
      {items}
    </div>
  </div>
</section>"""


def prereq_html() -> str:
    items = "\n".join(
        f"""<div>
          <dt>{esc(label)}</dt>
          <dd>{esc(body)}</dd>
        </div>"""
        for label, body in PREREQUISITES
    )
    return f"""<section class="section" id="prereqs" aria-labelledby="prereqs-h">
  <div class="wrap">
    <h2 id="prereqs-h">Prerequisites &amp; expectations</h2>
    <div class="panel prereq-panel">
      <dl class="prereq-list">
        {items}
      </dl>
      <p class="fine"><strong>Scope note.</strong> The course covers cross-layer computing systems, spanning computer architecture, software systems, and silicon, for emerging AI workloads such as physical, embodied, neuro-symbolic, and agentic AI; and agentic AI methods that design, optimize, and verify computing systems themselves. The two directions close a loop: better computing enables stronger AI, and stronger AI builds better computing.</p>
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
    seen_dividers = set()
    for w in weeks:
        while hi < len(holidays) and holidays[hi]["date"] < w["date"]:
            r = holidays[hi]
            rows.append(
                f'<tr class="g-holiday"><td>-</td><td>{esc(fmt_short(r["date"]))}</td>'
                f'<td colspan="2">{esc(r["note"])}</td></tr>'
            )
            hi += 1
        if w["module"] in MODULE_DIVIDERS and w["module"] not in seen_dividers:
            seen_dividers.add(w["module"])
            mcls, label = MODULE_DIVIDERS[w["module"]]
            rows.append(f'<tr class="g-module {mcls}"><td colspan="4">{esc(label)}</td></tr>')
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
        <thead><tr><th>Wk</th><th>Date</th><th>Topic</th><th>Project Milestone</th></tr></thead>
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
            f'<h2 class="week-title">{esc(w["title"])}</h2>']

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
        opts = "\n".join(f"<li>{optional_entry(o)}</li>" for o in w["optional"])
        body.append(
            f'<details class="optional"><summary>Optional readings <span class="opt-count">({len(w["optional"])})</span></summary>'
            f'<ul class="optional-list">{opts}</ul></details>'
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


def schedule_toc() -> str:
    """Quick-navigation box: weeks grouped by module block, in schedule order.
    Three columns: Launch + Synthesis stacked on the left, one module per column."""
    groups: list[tuple[str, str, list[dict]]] = []
    for w in weeks:
        mod = w["module"]
        if mod in MODULE_DIVIDERS:
            mcls, label = MODULE_DIVIDERS[mod]
        elif not groups:
            mcls, label = MODULE_CLASS.get(mod, "m-span"), mod
        else:
            mcls, label = None, None
        if label and (not groups or groups[-1][1] != label):
            groups.append((mcls, label, []))
        if mod == "Synthesis" and groups[-1][1] != "Synthesis":
            groups.append((MODULE_CLASS.get(mod, "m-span"), "Synthesis", []))
        groups[-1][2].append(w)

    def render(group) -> str:
        mcls, label, ws = group
        lis = "\n".join(
            f'<li><a href="#week-{w["week"]}"><span class="toc-num">{w["week"]:02d}</span> {esc(w["title"])}</a></li>'
            for w in ws
        )
        return f'<div class="toc-group"><p class="toc-head {mcls}">{esc(label)}</p><ol>{lis}</ol></div>'

    edge = [g for g in groups if g[1] in ("Launch", "Synthesis")]
    mods = [g for g in groups if g[1] not in ("Launch", "Synthesis")]
    cols = [f'<div class="toc-col toc-col-edge">{"".join(render(g) for g in edge)}</div>']
    cols += [f'<div class="toc-col">{render(g)}</div>' for g in mods]
    return f'<nav class="sched-toc" aria-label="Weeks by module">{chr(10).join(cols)}</nav>'


def schedule_body() -> str:
    rows, holidays = [], sorted(no_class, key=lambda r: r["date"])
    hi = 0
    seen_dividers = set()
    for w in weeks:
        while hi < len(holidays) and holidays[hi]["date"] < w["date"]:
            rows.append(holiday_article(holidays[hi]))
            hi += 1
        if w["module"] in MODULE_DIVIDERS and w["module"] not in seen_dividers:
            seen_dividers.add(w["module"])
            mcls, label = MODULE_DIVIDERS[w["module"]]
            rows.append(f'<h2 class="module-divider {mcls}"><span>{esc(label)}</span></h2>')
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
    <p class="section-lede">13 Friday meetings, {esc(course["meeting"].replace("Fridays ", ""))}, {esc(course["location"])}. Presentation slides are due 11:59 PM the Thursday before class.</p>
    {schedule_toc()}
    <div class="weeks"{current_attr}>
      {chr(10).join(rows)}
    </div>
    <p class="registrar-line"><strong>Registrar dates:</strong> {reg} · <a href="https://registrar.columbia.edu/content/academic-calendar" target="_blank" rel="noopener">academic calendar</a></p>
  </div>
</section>"""


# ---------------------------------------------------------------- format & grading

def format_body() -> str:
    grading_rows = "\n".join(
        f"""<tr><th scope="row">{esc(g["component"])}</th>
<td class="w-num">{g["weight"]}%</td>
<td class="w-bar" aria-hidden="true"><span style="width:{g["weight"] * 2}%"></span></td></tr>"""
        for g in grading
    )
    q_lis = "\n".join(f"<li>{q}</li>" for q in DISCUSSION_QUESTIONS)
    regular_rows = "\n".join(
        f'<tr><th scope="row">{esc(time)}</th><td>{esc(component)}</td></tr>'
        for time, component in REGULAR_FORMAT
    )
    guest_rows = "\n".join(
        f'<tr><th scope="row">{esc(time)}</th><td>{esc(component)}</td></tr>'
        for time, component in GUEST_FORMAT
    )

    return f"""<section class="section" id="format">
  <div class="wrap">
    {page_head("Course format &amp; grading",
               "Advanced graduate lecture-seminar with a semester-long research project. Nine seminar meetings provide 23 paper-lead slots; every student leads exactly once. There are no exams and no problem sets.")}

    <div class="col2">
      <div class="panel">
        <h2>Regular week · 110 minutes</h2>
        <table class="time-table">
          <caption class="visually-hidden">Regular week schedule</caption>
          <tbody>{regular_rows}</tbody>
        </table>
      </div>
      <div class="panel">
        <h2>Guest-speaker weeks</h2>
        <table class="time-table">
          <caption class="visually-hidden">Guest-speaker week schedule</caption>
          <tbody>{guest_rows}</tbody>
        </table>
      </div>
    </div>

    <div class="panel lead-panel">
      <h2>Student-Led Paper Presentation · the 25-minute block</h2>
      <div class="lead-blocks">
        <div class="lead-block"><span class="lead-min">12 min</span> problem, context, mechanism, and the minimum results needed to understand the paper</div>
        <div class="lead-block"><span class="lead-min">8 min</span> critical analysis of claims, baselines, assumptions, methodology, and missing evidence</div>
        <div class="lead-block"><span class="lead-min">5 min</span> facilitated discussion around two or three precise questions</div>
      </div>
      <p class="fine">Presenters read the full paper, appendices, and artifact documentation. Everyone else reads the abstract, introduction, core method, principal results, and limitations of all assigned papers, and arrives with at least one discussion question. No weekly summary reports.</p>
    </div>

    <div class="col2">
      <div class="panel">
        <h2>Grading</h2>
        <table class="grading-table">
          <caption class="visually-hidden">Grading components and weights</caption>
          <thead class="visually-hidden"><tr><th>Component</th><th>Weight</th><th>Visual proportion</th></tr></thead>
          <tbody>{grading_rows}</tbody>
        </table>
        <p class="fine">Grades reflect research judgment, technical execution, evidence quality, communication, and reproducibility - not whether a project happens to beat the state of the art. A rigorous negative result can earn full credit.</p>
      </div>
      <div class="panel">
        <h2>Evidence-centered discussion</h2>
        <p class="fine">Every paper discussion returns to six questions:</p>
        <ol class="q-list">
          {q_lis}
        </ol>
      </div>
    </div>

  </div>
</section>"""


# ---------------------------------------------------------------- project

def project_body() -> str:
    tl_items = []
    for m in milestones:
        cls = " tl-major" if m["id"] in ("Midterm", "P5", "Final") else ""
        tl_items.append(
            f"""<li class="tl-item{cls}">
  <span class="tl-dot" aria-hidden="true"></span>
  <time datetime="{m["date"].isoformat()}">{esc(fmt_short(m["date"]))}</time>
  <span class="tl-id">{esc(m["id"])}</span>
  <span class="tl-name">{esc(m["name"])}</span>
</li>"""
        )
    std_lis = "\n".join(f"<li>{s}</li>" for s in RESEARCH_STANDARD)
    track_cards = "\n".join(
        f"""<div class="track {'t-comp' if i == 0 else 't-ai'}">
        <p class="track-id">{esc(track_id)}</p>
        <h2>{esc(title)}</h2>
        <p>{esc(description)}</p>
      </div>"""
        for i, (track_id, title, description) in enumerate(PROJECT_TRACKS)
    )
    direction_cols = "\n".join(
        f"""<div class="panel">
        <h2>{esc(module)}</h2>
        <ul class="std-list">
          {chr(10).join(f"<li>{esc(t)}</li>" for t in titles)}
        </ul>
      </div>"""
        for module, titles in PROJECT_DIRECTIONS
    )

    return f"""<section class="section" id="project">
  <div class="wrap">
    {page_head("Semester-long research project", esc(PROJECT_OVERVIEW))}

    <div class="tracks tracks-2">
      {track_cards}
    </div>

    <h2 id="directions">Project Candidates (students are welcome to propose their own projects)</h2>
    <div class="col2">
      {direction_cols}
    </div>
    <p class="fine">{esc(PROJECT_DIRECTIONS_NOTE)}</p>

    <div class="col2 col2-project">
      <div class="panel">
        <h2>Minimum research standard</h2>
        <ul class="std-list">
          {std_lis}
        </ul>
      </div>
      <div class="panel">
        <h2>Milestones</h2>
        <ol class="timeline">
          {chr(10).join(tl_items)}
        </ol>
        <p class="fine">All written deliverables are due 11:59 PM ET. Check-ins P1-P5 are pacing devices, graded on completeness. No course deadline falls on the Thanksgiving holiday.</p>
      </div>
    </div>

    <div class="panel">
      <h2>Final submission</h2>
      <p>{esc(FINAL_SUBMISSION)}</p>
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------- policies

def policies_body() -> str:
    ai_items = "\n".join(f"<li>{esc(item)}</li>" for item in AI_POLICY_ITEMS)
    policy_cards = "\n".join(
        f'<div class="panel"><h2>{esc(title)}</h2><p>{esc(body)}</p></div>'
        for title, body in POLICY_SECTIONS
    )
    return f"""<section class="section" id="policies">
  <div class="wrap">
    {page_head("Policies")}

    <div class="panel policy-ai">
      <h2>AI use and evidence</h2>
      <p class="policy-stance">{esc(AI_POLICY_STANCE)}</p>
      <ul class="policy-list">
        {ai_items}
      </ul>
    </div>

    <div class="policy-grid">
      {policy_cards}
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
            optional_items = "\n".join(f"<li>{optional_entry(o)}</li>" for o in w["optional"])
            opt = f'<p class="p-label">Optional</p><ul class="optional-list papers-optional">{optional_items}</ul>'
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


# ---------------------------------------------------------------- generated syllabus

def md_link(title: str, url: str | None) -> str:
    """Render a Markdown link, preserving pending references as plain text."""
    return f"[{title}]({url})" if url else f"{title} *(link pending)*"


def md_table_cell(value) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def syllabus_markdown() -> str:
    """Generate the student-facing syllabus from the website's canonical source."""
    lines = [
        "<!-- AUTO-GENERATED by build.py. Edit build.py or data/*.yaml, then rebuild. -->",
        f"# {course['number']} | {course['semester']}",
        "# AI-Native Computing",
        "## *Hardware for AI ⇄ AI for Hardware*",
        "",
        "**Columbia University | Department of Computer Science**  ",
        f"Instructor: {inst['name']} · {course['meeting']} · {course['location']}  ",
        f"Generated from the canonical course website on {fmt_long(dt.date.today())}.",
        "",
        "> **Canonical-source notice.** This syllabus is generated from the same source as the course website. "
        "The live website and Canvas announcements govern later schedule or logistics updates.",
        "",
        "## Course overview",
        "",
        f"> **Course thesis - {COURSE_THESIS}**",
        "",
        "This advanced graduate lecture-seminar studies the two directions of AI-native computing:",
        "",
        "- **Computing for AI.** Profile, serve, schedule, map, accelerate, and make reliable emerging LLM, agentic, physical, and compositional AI workloads.",
        "- **AI for Computing.** Use agents to design, optimize, and verify software, compilers, architectures, SoCs, RTL, EDA flows, and chips.",
        "- **Shared methodology.** Dynamic workflows, closed-loop feedback, cross-layer optimization, heterogeneous resources, quality-performance-cost tradeoffs, and evidence-driven evaluation.",
        "",
        "## Course information",
        "",
        "| Item | Details |",
        "|---|---|",
        f"| Course | {md_table_cell(course['number'])} - {md_table_cell(course['title'])} |",
        f"| Instructor | {md_table_cell(inst['name'])} · [{inst['email']}](mailto:{inst['email']}) · [webpage]({inst['homepage']}) |",
        f"| Meeting | {md_table_cell(course['meeting'])} |",
        f"| Location | {md_table_cell(course['location'])} |",
        f"| Office hours | {md_table_cell(inst['office_hours'])} |",
        f"| Enrollment | Cap {course['enrollment_cap']} |",
        f"| Course platform | [Canvas]({inst['canvas']}) |",
        "| Format | Advanced graduate lecture-seminar with a semester-long research project; no exams and no problem sets |",
        "",
        "## Learning outcomes",
        "",
    ]
    lines.extend(
        f"{i}. **{lead}** {body}" for i, (lead, body) in enumerate(LEARNING_OUTCOMES, 1)
    )
    lines.extend(["", "## Prerequisites and expectations", ""])
    lines.extend(f"- **{label}.** {body}" for label, body in PREREQUISITES)

    lines.extend([
        "",
        "## Course format",
        "",
        "Nine seminar meetings provide 23 paper-lead slots; every student leads exactly once. "
        "Presentation slides are due at 11:59 PM ET on the Thursday before class.",
        "",
        "### Regular week (110 minutes)",
        "",
        "| Time | Activity |",
        "|---|---|",
    ])
    lines.extend(f"| {time} | {md_table_cell(activity)} |" for time, activity in REGULAR_FORMAT)
    lines.extend([
        "",
        "### Guest-speaker week",
        "",
        "| Time | Activity |",
        "|---|---|",
    ])
    lines.extend(f"| {time} | {md_table_cell(activity)} |" for time, activity in GUEST_FORMAT)
    lines.extend([
        "",
        "### Student-led paper presentation (25 minutes)",
        "",
        "- **12 minutes:** problem, context, mechanism, and the minimum results needed to understand the paper.",
        "- **8 minutes:** critical analysis of claims, baselines, assumptions, methodology, and missing evidence.",
        "- **5 minutes:** facilitated discussion around two or three precise questions.",
        "",
        "Presenters read the full paper, appendices, and artifact documentation. Everyone else reads the "
        "abstract, introduction, core method, principal results, and limitations of all assigned papers, "
        "and arrives with at least one discussion question. There are no weekly summary reports.",
        "",
        "## Grading",
        "",
        "| Component | Weight |",
        "|---|---:|",
    ])
    lines.extend(
        f"| {md_table_cell(item['component'])} | {item['weight']}% |" for item in grading
    )
    lines.extend([
        "",
        "Grades reflect research judgment, technical execution, evidence quality, communication, and "
        "reproducibility - not whether a project happens to beat the state of the art. A rigorous negative "
        "result can earn full credit.",
        "",
        "### Evidence-centered discussion",
        "",
    ])
    lines.extend(f"{i}. {question}" for i, question in enumerate(DISCUSSION_QUESTIONS, 1))

    lines.extend([
        "",
        "## Semester-long research project",
        "",
        PROJECT_OVERVIEW,
        "",
    ])
    lines.extend(f"- **{track_id}: {title}.** {body}" for track_id, title, body in PROJECT_TRACKS)
    lines.extend(["", "### Minimum research standard", ""])
    lines.extend(f"- {item}" for item in RESEARCH_STANDARD)
    lines.extend([
        "",
        "### Milestones",
        "",
        "| Date | ID | Deliverable |",
        "|---|---|---|",
    ])
    lines.extend(
        f"| {fmt_short(item['date'])} | {item['id']} | {md_table_cell(item['name'])} |"
        for item in milestones
    )
    lines.extend([
        "",
        "All written deliverables are due at 11:59 PM ET. Check-ins P1-P5 are pacing devices, graded "
        "on completeness. No course deadline falls on the Thanksgiving holiday.",
        "",
        "### Final submission",
        "",
        FINAL_SUBMISSION,
        "",
        "## Weekly schedule and readings",
        "",
        "Required readings appear first. Optional readings are listed separately, one paper per line. "
        "Guest-speaker details remain tentative until announced.",
        "",
    ])

    for week in weeks:
        lines.extend([
            f"### Week {week['week']:02d} · {fmt_long(week['date'])}",
            "",
            f"**{week['title']}** · {week['module']}",
            "",
        ])
        if week.get("guest"):
            lines.append(f"- **Guest lecture:** {week['guest']['topic']} ({week['guest']['label']}; confirmation pending).")
        if week.get("case_study"):
            lines.append(f"- **Mini-lecture case study:** {week['case_study']}.")
        if week.get("exercise"):
            lines.append(f"- **In-class exercise:** {week['exercise']}.")
        if week.get("type") in TYPE_NOTE:
            lines.append(f"- **Format note:** {TYPE_NOTE[week['type']]}")
        required = week.get("papers") or week.get("background") or []
        if required:
            label = "Student-led papers" if week.get("papers") else "Instructor-selected background"
            lines.extend(["", f"**{label}**", ""])
            for paper in required:
                detail = f" - {paper['venue']}"
                if paper.get("focus"):
                    detail += f"; focus: {paper['focus']}"
                if paper.get("companion_url"):
                    detail += f"; [companion critique]({paper['companion_url']})"
                if paper.get("extra_link"):
                    detail += f"; [project site]({paper['extra_link']})"
                lines.append(f"- {md_link(paper['title'], paper.get('url'))}{detail}")
        if week.get("optional"):
            optional_links = []
            for item in week["optional"]:
                if isinstance(item, dict):
                    optional_links.append(md_link(item["title"], item.get("url")))
                else:
                    optional_links.append(str(item))
            lines.extend(["", "**Optional readings**", ""])
            lines.extend(f"- {item}" for item in optional_links)
        if week.get("deadlines"):
            lines.extend(["", "**Deadlines**", ""])
            lines.extend(f"- {deadline}" for deadline in week["deadlines"])
        lines.append("")

    lines.extend([
        "## Policies",
        "",
        "### AI use and evidence",
        "",
        f"**{AI_POLICY_STANCE}**",
        "",
    ])
    lines.extend(f"- {item}" for item in AI_POLICY_ITEMS)
    for title, body in POLICY_SECTIONS:
        lines.extend(["", f"### {title}", "", body])

    lines.extend([
        "",
        "## Registrar dates",
        "",
    ])
    lines.extend(f"- **{fmt_long(item['date'])}:** {item['note']}" for item in registrar)
    lines.extend([
        "",
        "See the [Columbia Registrar academic calendar](https://registrar.columbia.edu/content/academic-calendar) "
        "for the authoritative university calendar.",
        "",
    ])
    return "\n".join(lines)


# ---------------------------------------------------------------- build

def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "assets", OUT / "assets")

    syllabus = syllabus_markdown()
    (ROOT / "syllabus.md").write_text(syllabus)
    (OUT / "syllabus.md").write_text(syllabus)

    desc = ("COMS 6998, Columbia University, Fall 2026. Graduate seminar on hardware and systems "
            "for AI workloads, and AI agents for designing computing systems. Fridays 10:10-12:00.")
    pages = {
        "index.html": ("COMS 6998 · AI-Native Computing · Fall 2026", desc,
                       "\n".join([hero(), learn_html(), prereq_html(), now_html(), glance_html()])),
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
