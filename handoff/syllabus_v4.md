> **ARCHIVED INPUT — DO NOT EDIT.** The website source is now canonical. The current
> student-facing syllabus is generated at `../syllabus.md` by `../build.py`.

# COMS 6998 | Fall 2026
# AI-Native Computing
## *Hardware for AI, AI for Hardware*

**Columbia University | Department of Computer Science**
Instructor: Prof. Zishen Wan · Fridays, 10:10 AM–12:00 PM · Location: TBD · Enrollment cap: 30
Detailed Syllabus **v4** | August 31, 2026
*Student-facing draft; readings and logistics may be refined before the semester begins*

---

# 1. Course Overview

> **COURSE THESIS — AI is transforming computing in two directions: emerging AI workloads demand new hardware and system architectures, while AI is becoming a powerful tool for designing computing systems themselves.**

This course covers computer architecture, hardware–software co-design, SoCs, ML systems, and domain-specific architectures for LLMs, agentic AI, and physical AI. It also examines how AI agents can automate the design, optimization, and verification of architectures, systems, and chips. Through lectures, research-paper discussions, and semester-long research projects, students will explore the foundations and frontiers of computer architecture and systems.

## Course identity

- **Computing for AI.** Profile, serve, schedule, map, accelerate, and make reliable emerging LLM, agentic, physical, and compositional AI workloads.
- **AI for Computing.** Use agents to design, optimize, and verify software, compilers, architectures, SoCs, RTL, EDA flows, and chips.
- **Shared methodology.** Dynamic workflows, closed-loop feedback, cross-layer optimization, heterogeneous resources, quality–performance–cost tradeoffs, and evidence-driven evaluation.

## Course information

| | |
|---|---|
| **Course** | COMS 6998 — AI-Native Computing: Hardware for AI, AI for Hardware |
| **Instructor** | Prof. Zishen Wan |
| **Time** | Fridays, 10:10 AM–12:00 PM |
| **Location** | TBD |
| **Enrollment** | Cap 30; instructor-managed waitlist |
| **Format** | Advanced graduate lecture-seminar with a semester-long research project |
| **Guest speakers** | Up to four invited talks (Weeks 3, 6, 10, 11), to be confirmed; an unfilled guest slot becomes a regular paper-discussion week |
| **Website** | Course website to be published; announcements and submissions through the designated course platform |

## Learning objectives

1. Represent an AI application as a model pipeline, dynamic DAG, state machine, or feedback-control loop.
2. Measure end-to-end behavior using latency distributions, throughput, critical path, utilization, memory traffic, energy, cost, and task-quality metrics.
3. Apply trace analysis, roofline reasoning, queueing, scaling analysis, and controlled interventions to diagnose systems bottlenecks.
4. Reason across model, software, runtime, architecture, memory, accelerator, SoC, and deployment layers.
5. Evaluate joint tradeoffs among task quality, latency, throughput, energy, cost, reliability, safety, and adaptability.
6. Formulate computing-system design as an agent environment with state, actions, tools, feedback, constraints, budgets, and validity checks.
7. Compare LLM agents, RL, Bayesian optimization, evolutionary search, and classical heuristics using budget-matched evaluation.
8. Produce a conference-style research result with meaningful baselines, ablations, held-out evaluation, failure analysis, and a reproducible artifact.

## Audience and prerequisites

The course is intended for graduate students in CS and EE interested in computer architecture, systems, ML systems, hardware–software co-design, robotics and physical AI, VLSI/EDA, or adjacent areas. Students are not expected to arrive with expertise across the entire computing stack.

- **Expected.** Basic computer organization or systems knowledge, familiarity with machine-learning concepts, and the ability to program and conduct quantitative experiments.
- **Helpful but not required.** Experience with CUDA, compilers, digital design, RTL, EDA, robotics simulators, FPGA platforms, LLM agents, or research-paper reading.
- **Project readiness.** Every team must include enough complementary expertise to implement, measure, and evaluate its selected project.

**Scope note.** This course deliberately concentrates on inference-side and emerging AI workloads and on AI-driven design. Deep coverage of large-scale *training* systems (parallelism strategies, collectives, fault tolerance) and model-compression algorithms is left to ML-systems courses such as CMU 15-442; Week 2 provides the working knowledge needed for this course, and optional readings point further.

# 2. Enrollment and Course Launch

## Waitlist and readiness assessment

Because enrollment is capped at 30, students seeking admission from the waitlist may be asked to complete a short Course Readiness and Project-Fit Assessment during Week 1. The assessment is not a graded exam and does not reward narrow trivia. It evaluates the technical reasoning, evidence analysis, project alignment, and collaboration readiness needed for an intensive research seminar.

| Criterion | Weight | Evidence |
|---|---|---|
| Technical readiness | 25% | Relevant foundation in at least one course area |
| Systems reasoning | 30% | Bottleneck analysis and design of a discriminating experiment |
| Project fit | 25% | Alignment with available project directions and complementary skills |
| Commitment and collaboration | 20% | Time commitment, reliability, and readiness for team research |

*Selection will not be based on institutional prestige, number of prior publications, or mastery of every course area. The goal is a prepared and intellectually diverse class spanning architecture, systems, ML, physical AI, and hardware design.*

## Enrollment timeline

- **Sep 8.** Background and project-fit form released to enrolled and waitlisted students.
- **Sep 11.** First class and in-class reasoning assessment.
- **Sep 12, 5:00 PM.** Assessment and background form close.
- **Sep 14–15.** Enrollment decisions communicated.
- **Sep 18.** End of Columbia's Change of Program period; last day to add courses.

## Team and paper matching

Project teams are formed through individual bidding plus instructor matching. Students rank projects and report skills, preferred roles, and at most one preferred teammate. The instructor forms approximately eight teams of three to four students, balancing interest, complementary expertise, mentoring capacity, and project feasibility. A pre-formed team is a preference, not a guarantee.

Paper assignments also use ranked preferences rather than first-come-first-served signup. Nine seminar meetings provide **23 lead slots** (three papers in regular weeks, two in guest-speaker weeks). If the class reaches 30 students, the seven most methodologically dense papers are co-led by pairs so that every student leads exactly once. If a guest talk cannot be scheduled, that week reverts to three student-led papers and the slot count rises accordingly.

# 3. Course Format and Expectations

## Regular 110-minute seminar

| Time | Component |
|---|---|
| 10:10–10:35 | Instructor mini-lecture: concepts, methods, and cross-paper connections |
| 10:35–11:00 | Paper 1 — presentation, critique, and discussion |
| 11:00–11:10 | Break |
| 11:10–11:35 | Paper 2 — presentation, critique, and discussion |
| 11:35–12:00 | Paper 3 — presentation, critique, and discussion |

## Guest-speaker weeks (Weeks 3, 6, 10, 11 — to be confirmed)

| Time | Component |
|---|---|
| 10:10–10:25 | Instructor mini-lecture |
| 10:25–11:05 | Guest lecture + Q&A |
| 11:05–11:10 | Break |
| 11:10–11:35 | Paper 1 — presentation, critique, and discussion |
| 11:35–12:00 | Paper 2 — presentation, critique, and discussion |

## Paper leadership

Each 25-minute paper block follows a common structure: **12 minutes** — problem, context, mechanism, and the minimum results needed to understand the paper; **8 minutes** — critical analysis of claims, baselines, assumptions, methodology, and missing evidence; **5 minutes** — facilitated discussion around two or three precise questions.

Presenters must read the full paper, appendices, and artifact documentation when available. All other students should read the abstract, introduction, core method, principal results, and limitations of all assigned papers and arrive with at least one discussion question. There are no weekly summary reports.

Presentation slides are due by **8:00 PM on the Thursday before class**. A one-page evidence capsule, revised after discussion, is due by **5:00 PM the following Monday**.

## Evidence-centered discussion

- What is the paper's exact central claim?
- Which experiment most directly supports that claim?
- What hidden assumption is most likely to break?
- Is the baseline fair and budget-matched?
- Which conclusion extends beyond the presented evidence?
- What single additional experiment would most change confidence in the result?

## Attendance and engagement

The course depends on prepared discussion and peer feedback. Students should attend every meeting, notify the instructor in advance when absence is unavoidable, and contribute constructively without monopolizing discussion. Repeated unexcused absences or lack of preparation will affect the engagement grade.

# 4. Assessment and Grading

> **ASSESSMENT PRINCIPLE — Grades reflect research judgment, technical execution, evidence quality, communication, and reproducibility — not whether a project happens to beat the state of the art.**

| Component | Weight | Primary evidence |
|---|---|---|
| Paper presentation & discussion leadership | 15% | Presentation, critique, facilitation, and evidence capsule |
| Engagement & participation | 10% | Preparation, discussion, project feedback, professional collaboration |
| Project P0 — Proposal | 5% | Question, hypothesis, baselines, metrics, plan, risks, and roles |
| Project check-ins P1–P5 | 10% | Five milestone updates, graded on completeness (2% each) |
| Midterm presentation | 10% | Claim, system design, evidence, risk, and revised plan |
| Final poster | 10% | Clear technical communication and response to expert feedback |
| Final paper & artifact | 40% | Conference-style paper and reproducible package |
| **Total** | **100%** | |

*There are no exams and no problem sets. Milestone check-ins P1–P5 are pacing devices: they are reviewed lightly and graded on completeness, not on results. A rigorous negative result can earn full credit on the final paper when the question is important, the experiment is sound, the evidence is complete, and the failure is analyzed honestly.*

# 5. Semester-Long Research Project

## Project philosophy

The project is the center of the course. The objective is not a lightweight demonstration; it is a carefully scoped research effort that could mature into a top-tier architecture, systems, ML systems, robotics, or EDA paper. Publication is an aspiration rather than a grading requirement.

The instructor provides a curated portfolio of research directions connected to active architecture, systems, physical-AI, and AI-for-computing work. Students bid on these topics and are matched into complementary teams. Student-proposed projects are considered only when they present an unusually strong, course-aligned question and receive approval before project bidding closes.

## Project tracks

- **Track A — Computing for AI.** Profile, serve, schedule, map, accelerate, or make reliable an LLM, agentic, physical, or neuro-symbolic workload.
- **Track B — AI for Computing.** Build and rigorously evaluate an agent for software optimization, compilers, GPU kernels, architecture DSE, RTL/EDA, or verification.
- **Track C — Closing the Loop.** Build a system that profiles an AI workload, diagnoses a bottleneck, changes model/runtime/hardware decisions, and experimentally verifies the improvement.

## Minimum research standard

- A falsifiable research question and a precise intended claim.
- At least two meaningful baselines, including a classical or non-agentic baseline where applicable.
- A mechanism, not only a correlation or leaderboard result.
- At least one ablation or controlled intervention tied to the central claim.
- Joint reporting of task quality or success and relevant systems metrics.
- A held-out workload, configuration, system scale, or design budget.
- Explicit compute, GPU, API, token, simulation, and wall-clock budgets.
- Failure-case analysis, including invalid actions and tool failures for agentic design systems.
- Reproducible code, environment instructions, configurations, data, and figure-generation scripts.

## Milestone check-in format

Each check-in is a concise two- to three-page update plus repository links: current question and claim; work completed; new evidence and what it does or does not demonstrate; failures, surprises, and hypothesis changes; plan and exit criteria for the next two weeks; risks and specific help requested; individual contribution log.

## Milestones and deadlines

| Date | Checkpoint | Required evidence |
|---|---|---|
| Oct 2 | P0 Proposal | Question, claim, method, baselines, metrics, infrastructure, risks, roles |
| Oct 16 | P1 Infrastructure | Smoke test, measurement validation, reference baseline, reproducibility seed |
| Oct 30 | P2 Prototype | Method v1, pilot result, feasibility, failed attempt, pivot rationale |
| Nov 6 | Midterm talk | Claim, system design, strongest evidence, highest risk (8–10 min per team) |
| Nov 13 | P3 Evaluation | Frozen evaluation matrix, initial results, ablation and held-out plan |
| Nov 24 | P4 Main results | Main plots, ablations, failure cases, generalization, remaining gaps |
| Dec 9 | P5 Complete draft | Full draft, artifact candidate, reproducibility checklist, poster |
| Dec 21 | Final | Revised paper, artifact, response memo, contribution statements |

All written deliverables due 5:00 PM ET. No course deadline falls on the Thanksgiving holiday.

## Final submission

- Six- to eight-page conference-style paper, excluding references and appendices.
- Repository with pinned environment, one-command smoke test, and documented reproduction path for one central result.
- Machine-readable experiment results and scripts regenerating principal figures and tables.
- Experiment manifest covering seeds, configurations, models, machines, simulator or tool versions, and resource budgets.
- Response-to-feedback memo and individual contribution statements.

# 6. Semester Schedule at a Glance

Fall 2026 classes begin Tuesday, September 8 and end Monday, December 14. The course meets on 13 Fridays; there is no class on Friday, November 27 (Thanksgiving). 🎤 marks guest-speaker weeks.

| Wk | Date | Module | Topic | Deadline |
|---|---|---|---|---|
| 1 | Sep 11 | Launch | AI as Workload, AI as Designer | Assessment Sep 12 |
| 2 | Sep 18 | Computing for AI | How to Study an AI Computing System + LLM Inference Fundamentals | Paper preferences Sep 18 |
| 3 | Sep 25 | Computing for AI | Serving LLMs and AI Agents 🎤 Guest Speaker | Teams announced |
| 4 | Oct 2 | Computing for AI | Physical AI I: Inference Systems and Serving for Embodied AI | P0 Proposal |
| 5 | Oct 9 | Computing for AI | Physical AI II: HW–SW Co-Design and Architecture | — |
| 6 | Oct 16 | Computing for AI | AI Hardware: Datacenter Accelerators and SoCs 🎤 Guest Speaker | P1 Infrastructure |
| 7 | Oct 23 | Computing for AI | Neuro-Symbolic and Compositional AI | — |
| 8 | Oct 30 | AI for Computing | AI for Software, Compilers, and GPU Kernels | P2 Prototype |
| 9 | Nov 6 | Project | Midterm Project Presentations | Midterm talk |
| 10 | Nov 13 | AI for Computing | AI for Computer Architecture I: Measuring and Exploring 🎤 Guest Speaker | P3 Evaluation |
| 11 | Nov 20 | AI for Computing | AI for Computer Architecture II: Agentic Design Systems 🎤 Guest Speaker | P4 due Nov 24 |
| — | Nov 27 | Holiday | No class — Thanksgiving | — |
| 12 | Dec 4 | AI for Computing | AI for RTL and Chip Physical Design | P5 due Dec 9 |
| 13 | Dec 11 | Synthesis | Final Project Poster Session | Final due Dec 21 |

## Major non-class deadlines

- **Sep 20.** Deadline to request approval for a student-proposed project.
- **Sep 23.** Project bidding deadline.
- **Nov 24.** P4 due before Thanksgiving.
- **Dec 9.** Complete project draft, artifact candidate, and poster due.
- **Dec 21.** Final project paper and artifact due (final-examination period).

## Registrar dates to know (Fall 2026)

Last day to add: **Sep 18** · Course drop deadline: **Oct 13** · Pass/fail & withdrawal deadline: **Nov 19** · Last day of classes: **Dec 14** · Final exams: Dec 17–23 (this course has no exam).

---

# Week 1 — Friday, September 11
## AI as Workload, AI as Designer
**Course launch | Instructor-led session; no paper presentations**

### Learning goals
- Understand the two course pillars — Computing for AI and AI for Computing — and how they close a loop: better computing enables stronger AI, and stronger AI builds better computing.
- See how AI changes workloads, system architecture, SoC design, and the design process itself.
- Understand course logistics, research expectations, project tracks, and paper discussions.

### Session plan

| Time | Activity |
|---|---|
| 10:10–10:30 | Course vision: why AI is simultaneously a workload and a designer |
| 10:30–10:55 | Technical overview of the workload–model–runtime–architecture–SoC–chip stack |
| 10:55–11:05 | Break |
| 11:05–11:25 | Schedule, grading, paper discussions, collaboration, and AI-use policy |
| 11:25–11:40 | Preview of curated project directions and reading map |
| 11:40–12:00 | Course-readiness and project-fit assessment; questions |

### Instructor-selected background (no student presentation)
- **A New Golden Age for Computer Architecture** — Hennessy & Patterson, CACM 2019. [paper](https://doi.org/10.1145/3282307)
- **GenAI for Systems: Recurring Challenges and Design Principles from Software to Silicon** — arXiv 2026. [paper](https://arxiv.org/abs/2602.15241)
- Optional: Sutton, *The Bitter Lesson* (2019); Reddi et al., *Architecture 2.0: Why Computer Architects Need a Data-Centric AI Gymnasium*, IEEE CAL 2023.

### Questions to carry into discussion
- Which aspects of an AI workload should influence architecture, and which should remain hidden behind abstractions?
- What distinguishes an AI system designer from an expensive black-box optimizer?

### Deadlines
- **Sep 12, 5:00 PM.** Background survey and readiness assessment close.
- **Sep 14–15.** Enrollment and waitlist decisions communicated.

# Week 2 — Friday, September 18
## How to Study an AI Computing System + LLM Inference Fundamentals
**Module I — Computing for AI | Instructor-led double lecture and research marketplace; no paper presentations**

### Learning goals
- Represent an AI application as a dynamic computation graph, state machine, or closed-loop workflow.
- Select metrics that jointly capture performance, efficiency, task quality, reliability, and cost; use traces, critical paths, roofline reasoning, queueing, and scaling sweeps to generate bottleneck hypotheses.
- Master the anatomy of transformer inference — prefill vs. decode, attention and GEMM kernels, KV-cache growth, arithmetic intensity — as the running example for the rest of the semester.

### Session plan

| Time | Activity |
|---|---|
| 10:10–10:45 | Lecture A: workloads, measurement, bottlenecks, and causal evidence |
| 10:45–11:20 | Lecture B: transformer inference anatomy — compute, memory, batching, parallelism, TTFT/TPOT/goodput |
| 11:20–11:30 | Break |
| 11:30–11:50 | Curated final-project marketplace |
| 11:50–12:00 | Paper-presentation guidelines, paper preferences, and key deadlines |

### Lecture threads
- **Represent the workload.** Model graphs vs. workflow DAGs, branching trajectories, retries, speculation, physical feedback loops.
- **Measure the system.** Component and end-to-end latency, tail behavior, throughput and goodput, utilization, memory traffic, energy, cost, task success.
- **Locate the bottleneck.** Critical paths, overlap, arithmetic intensity, roofline limits, queueing, head-of-line blocking, contention.
- **Establish causality.** From trace observation to hypothesis, controlled intervention, mechanism validation, and joint metric reporting.
- **LLM inference anatomy.** Prefill vs. decode, KV-cache memory growth, IO-aware kernels (FlashAttention), continuous batching, tensor/pipeline parallelism, SLO-aware serving metrics.

### Instructor-selected background (no student presentation)
- **Roofline: An Insightful Visual Performance Model for Multicore Architectures** — CACM 2009. [paper](https://doi.org/10.1145/1498765.1498785)
- **The Tail at Scale** — Dean & Barroso, CACM 2013. [paper](https://research.google/pubs/the-tail-at-scale/)
- **FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness** — NeurIPS 2022. [paper](https://arxiv.org/abs/2205.14135)
- Optional: MLPerf Inference Benchmark (ISCA 2020); *Efficient Processing of Deep Neural Networks* survey (Proc. IEEE 2017).

### Questions to carry into discussion
- What is the correct unit of analysis: kernel, request, workflow, episode, or deployed service?
- When can a component-level speedup fail to improve end-to-end task completion time?

### Deadlines
- **Sep 18, 5:00 PM.** Paper preference form due; rank at least six papers and report date conflicts.
- **Sep 20, 5:00 PM.** Deadline to request approval for a student-proposed project.
- **Sep 23, 5:00 PM.** Individual project bidding form due.

# Week 3 — Friday, September 25
## Serving LLMs and AI Agents
**Module I — Computing for AI | 🎤 Guest lecture: LLM serving and efficiency (speaker TBC) | Two student-led papers**

### Learning goals
- Connect transformer inference phases to compute, memory, communication, and serving bottlenecks; evaluate serving systems using TTFT, TPOT, throughput, goodput, and SLO attainment.
- Distinguish request-level LLM serving from workflow-level agent serving: semantic dependencies, KV reuse across program structure, and program-aware scheduling.
- Hear how serving efficiency plays out in research and production systems from the guest's perspective.

### Mini-lecture: From serving requests to serving agents (includes instructor case study)
KV-cache pressure, continuous batching, prefill–decode interference, and disaggregation as a datacenter-scale pattern (building on Week 2's fundamentals); what agents change — branching workflows, retries, tool calls, cumulative waiting, per-node model choice. **Case study: DyServe** (instructor's work) — a workflow-aware serving layer making joint model–verifier–backend decisions under workload-dependent pressure.

### Student-led papers
1. **Efficient Memory Management for Large Language Model Serving with PagedAttention** — SOSP 2023. [paper](https://arxiv.org/abs/2309.06180)
   *Focus: KV-cache virtualization, fragmentation, batching, and vLLM — the canonical serving-systems paper.*
2. **SGLang: Efficient Execution of Structured Language Model Programs** — NeurIPS 2024. [paper](https://arxiv.org/abs/2312.07104)
   *Focus: RadixAttention, KV-cache reuse across program structure, and the runtime–language interface for agentic workloads.*

### Optional readings
Splitwise (ISCA 2024) · Agentix (NSDI 2026, formerly Autellix) · DyServe (arXiv 2026) · DistServe (OSDI 2024) · Mooncake (FAST 2025) · Parrot (OSDI 2024) · Leviathan et al., Speculative Decoding (ICML 2023) · Sarathi-Serve (OSDI 2024) · MemGPT (2023)

### Questions to carry into discussion
- At what point does optimizing a kernel stop being the dominant lever for serving performance?
- What workflow information must cross the boundary between an agent framework and a serving system?
- When should the system optimize a node, a critical path, or the probability of successful task completion?

### Deadlines
- **In class.** Project teams and assigned topics announced; proposal template and team charter released.

# Week 4 — Friday, October 2
## Physical AI I: Inference Systems and Serving for Embodied AI
**Module I — Computing for AI | Mini-lecture plus three student-led papers**

### Learning goals
- Describe physical AI as a perception–reasoning–planning–control feedback loop rather than a standalone model, and understand where inference latency enters that loop.
- Analyze the system optimization space for VLA inference: runtimes, asynchrony, performance modeling, and edge–cloud placement.
- Distinguish open-loop model evaluation from episode-level, closed-loop evaluation.

### Mini-lecture: The physical AI model stack and its system demands
The VLA landscape in 20 minutes — autoregressive vs. diffusion/flow action heads, π0/OpenVLA/GR00T as reference points (algorithm background for the week's systems papers); temporal semantics — observation-to-action latency, control frequency, deadlines, stale actions; episode behavior — long-horizon error propagation, retries, task success; the system-optimization toolbox — asynchronous and speculative execution, early exit, caching, quantization, edge–cloud partitioning.

### Student-led papers
1. **Embodied.cpp: A Portable Inference Runtime of Embodied AI Models on Heterogeneous Robots** — arXiv 2026. [paper](https://arxiv.org/abs/2607.02501)
   *Focus: what a deployable embodied-AI runtime requires across heterogeneous robot platforms.*
2. **VLASH: Real-Time VLAs via Future-State-Aware Asynchronous Inference** — arXiv 2025. [paper](https://arxiv.org/abs/2512.01031)
   *Focus: overlapping inference with action execution; latency hiding for dynamic real-time tasks.*
3. **How Fast Can I Run My VLA? Demystifying VLA Inference Performance with VLA-Perf** — arXiv 2026. [paper](https://arxiv.org/abs/2602.18397)
   *Focus: analytical performance modeling of VLA inference; on-device vs. edge vs. cloud placement.*

### Optional readings
π0 (RSS 2025) · OpenVLA (CoRL 2024) · DeeR-VLA (NeurIPS 2024) · RT-2 (CoRL 2023) · GR00T N1 (NVIDIA 2025) · *Generative AI in Embodied Systems* (ISPASS 2025)

### Questions to carry into discussion
- Which latency matters most: model latency, control-loop latency, or episode completion time?
- When does asynchrony change what the model must predict, and when is it purely a systems trick?
- Which optimizations remain valid when evaluated on real closed-loop task success?

### Deadlines
- **Oct 2, 5:00 PM.** P0 Project proposal and team charter due.

# Week 5 — Friday, October 9
## Physical AI II: Hardware–Software Co-Design and Architecture
**Module I — Computing for AI | Mini-lecture plus three student-led papers**

### Learning goals
- Move from profiling embodied workloads to designing architectures for them.
- Evaluate algorithm–architecture co-design: what changes in the algorithm enable what changes in the hardware, and vice versa.
- Reason about real-time guarantees, energy budgets, and multi-agent scaling on autonomy SoCs and edge platforms.

### Mini-lecture: Co-designing the embodied stack
Where cycles go in embodied pipelines; decoupling perception, reasoning, and control; trajectory prediction vs. per-frame action; accelerator support for heterogeneous kernels; CPU–GPU–NPU contention, shared memory, and power modes; hardware-in-the-loop measurement; cooperative multi-agent systems.

### Student-led papers
1. **DaDu-Corki: Algorithm-Architecture Co-Design for Embodied AI-Powered Robotic Manipulation** — ASPLOS 2024. [paper](https://arxiv.org/abs/2407.04292)
   *Focus: decoupling LLM inference from robotic control via trajectory prediction; co-design across the control boundary.*
2. **ReCA: Integrated Acceleration for Real-Time and Efficient Cooperative Embodied Autonomous Agents** — ASPLOS 2025. [paper](https://doi.org/10.1145/3676641.3716016)
   *Focus: cross-layer algorithm–system–architecture co-design for cooperative embodied agents.*
3. **Deltoris: Enabling Real-Time VLA Inference in Embodied AI via Bit-Level Sparsity and Speculative Inference** — arXiv 2026. [paper](https://arxiv.org/abs/2608.04428)
   *Focus: hardware–software co-design for diffusion-based VLA inference on edge devices.*

### Optional readings
OctoCache (ASPLOS 2025) · RobotPerf (ICRA 2024) · Dadu-P/Dadu-series robotic accelerators · autonomy SoC papers (e.g., NVIDIA Orin/Thor analyses)

### Questions to carry into discussion
- Which co-design wins survive a model-generation change, and which are tied to today's VLA architectures?
- When is a robotics accelerator justified over a well-utilized general-purpose SoC?
- How should real-time guarantees be reported alongside average-case speedups?

# Week 6 — Friday, October 16
## AI Hardware: Datacenter Accelerators and SoCs
**Module I — Computing for AI | 🎤 Guest lecture: AI accelerator and SoC design (speaker TBC) | Two student-led papers**

### Learning goals
- Understand the hardware that actually runs frontier AI: GPUs/TPUs, tensor cores, HBM, and scale-up/scale-out interconnects.
- Relate data reuse and dataflow to processing elements, local storage, NoCs, and off-chip memory.
- Explain why a useful accelerator requires a full-stack interface, generator, software support, and SoC integration.

### Mini-lecture: From dataflow taxonomy to deployed silicon
Systolic arrays and the TPU lineage; GPU execution model and tensor cores; dataflow taxonomies (weight/output/row-stationary — Eyeriss, MAESTRO) in 15 minutes; mapping and design-space coupling; how to read a chip announcement critically.

### Student-led papers
1. **In-Datacenter Performance Analysis of a Tensor Processing Unit** — ISCA 2017. [paper](https://doi.org/10.1145/3079856.3080246)
   *Focus: read as a ten-year retrospective — which predictions held, which were overturned by LLMs.*
2. **Agile SoC Development with Open ESP** — ICCAD 2020. [paper](https://arxiv.org/abs/2009.01178)
   *Focus: Columbia's open-source platform for heterogeneous SoC integration — tile-based architecture, accelerator design flows, and FPGA prototyping; infrastructure available for course projects ([esp.cs.columbia.edu](https://www.esp.cs.columbia.edu/)).*

### Optional readings
Gemmini (DAC 2021) · TPU v4 (ISCA 2023) · Eyeriss (ISCA 2016) · MAESTRO (MICRO 2019) · Timeloop (ISPASS 2019) · NVIDIA Hopper/Blackwell architecture whitepapers

### Questions to carry into discussion
- When is a new dataflow a general principle rather than a workload-specific optimization?
- What system-integration costs are commonly omitted from accelerator evaluations?

### Deadlines
- **Oct 16, 5:00 PM.** P1 Infrastructure and baselines check-in due.

# Week 7 — Friday, October 23
## Neuro-Symbolic and Compositional AI
**Module I — Computing for AI | Mini-lecture plus three student-led papers**

### Learning goals
- Characterize neural, symbolic, and probabilistic kernels by computation, memory, and control-flow behavior.
- Explain why tensor-centric accelerators underutilize hardware on irregular reasoning workloads.
- Evaluate algorithm, dataflow, architecture, and scheduling co-design for compositional systems.

### Mini-lecture: Heterogeneous computation beyond dense tensors
Compositional pipelines — neural perception, symbolic deduction, probabilistic inference, solvers, tools; kernel characteristics — irregular traversal, dynamic control, low arithmetic intensity, memory divergence; representations — graphs, factorized programs, logic circuits, DAGs; co-design levers — factorization, reconfigurable processing, heterogeneous scheduling.

### Student-led papers
1. **CogSys: Efficient and Scalable Neurosymbolic Cognition System via Algorithm-Hardware Co-Design** — HPCA 2025. [paper](https://research.ibm.com/publications/cogsys-efficient-and-scalable-neurosymbolic-cognition-system-via-algorithm-hardware-co-design)
   *Focus: workload characterization, reconfigurable processing, dataflow, and scheduling.*
2. **REASON: Accelerating Probabilistic Logical Reasoning for Scalable Neuro-Symbolic Intelligence** — HPCA 2026. [paper](https://arxiv.org/abs/2601.20784)
   *Focus: unified DAGs, irregular reasoning acceleration, and compositional system integration.*
3. **Lobster: A GPU-Accelerated Framework for Neurosymbolic Programming** — ASPLOS 2026. [paper](https://arxiv.org/abs/2503.21937)
   *Focus: compiling a Datalog-based neurosymbolic language end-to-end to GPUs; the systems path to scalable reasoning.*

### Optional readings
Scallop (PLDI 2023) · DeepProbLog (NeurIPS 2018) · NSFlow (DAC 2025) · *Towards Cognitive AI Systems* survey (ISPASS 2024)

### Questions to carry into discussion
- What is the correct abstraction for jointly mapping neural, symbolic, and probabilistic computation?
- Which speedups come from algorithmic transformation versus hardware specialization?
- How should an accelerator preserve programmability as reasoning algorithms evolve?

# Week 8 — Friday, October 30
## AI for Software, Compilers, and GPU Kernels
**Module II — AI for Computing | Bridge mini-lecture plus three student-led papers**

### Learning goals
- Formulate software and system design as an interactive agent environment: state, actions, tools, feedback, budgets, validity checks.
- Treat correctness and performance as two coupled feedback loops.
- Evaluate generated code with tests, compiler feedback, profiling, portability, and held-out workloads — and audit agent claims.

### Mini-lecture (bridge into Module II): The design loop as an agent environment
From human heuristics to agentic design; action abstraction — knobs vs. code vs. mechanisms; the agent loop — observe, hypothesize, act, compile/simulate, diagnose, revise; search comparison — heuristics, BO, evolution, RL, LLM reasoning; evidence — budget matching, invalid actions, held-out workloads, trajectory audits. Failure modes: correct-but-slow, fast-but-wrong, benchmark overfitting, hidden compilation cost.

### Student-led papers
1. **Faster Sorting Algorithms Discovered Using Deep Reinforcement Learning (AlphaDev)** — Nature 2023. [paper](https://www.nature.com/articles/s41586-023-06004-9)
   *Focus: algorithm discovery, low-level action spaces, reward design, and validation.*
2. **AlphaEvolve: A Coding Agent for Scientific and Algorithmic Discovery** — Google DeepMind, 2025. [paper](https://arxiv.org/abs/2506.13131)
   *Focus: evolutionary LLM code search that improved datacenter scheduling, TPU circuits, and kernels — the strongest single evidence for the course thesis; read with attention to evaluation scope.*
3. **KernelBench: Can LLMs Write Efficient GPU Kernels?** — 2025. [paper](https://arxiv.org/abs/2502.10517)
   *Focus: correctness–speedup benchmark design; discussed together with the Sakana AI "AI CUDA Engineer" episode and its post-hoc corrections — a case study in auditing agent claims.*

### Optional readings
CompilerGym (CGO 2022) · LLMs for Compiler Optimization (Meta, 2023) · Kevin: Multi-Turn RL for CUDA (2025) · Sakana AI CUDA Engineer report + community post-mortem (2025) · ECO (2025)

### Questions to carry into discussion
- What evidence proves that generated code is faster for the intended reason?
- How should compilation failures, invalid kernels, and unsuccessful attempts enter the reported budget?
- What held-out test distinguishes genuine optimization skill from benchmark memorization?

### Deadlines
- **Oct 30, 5:00 PM.** P2 Prototype and pilot check-in due, including an explicit continue/pivot decision.

# Week 9 — Friday, November 6
## Midterm Project Presentations
**Project checkpoint | Team presentations; no mini-lecture and no assigned papers**

### Session plan

| Time | Activity |
|---|---|
| 10:10–10:15 | Framing and review criteria |
| 10:15–10:55 | Project presentations, first half |
| 10:55–11:05 | Break |
| 11:05–11:45 | Project presentations, second half |
| 11:45–12:00 | Cross-project synthesis, risks, and next-step decisions |

Each team presents 8–10 minutes plus questions; exact timing adjusted to the final number of teams. The talk draws directly on the P2 check-in — no separate document is required.

### Questions every talk must answer
- What is the intended claim, and what evidence currently supports it?
- What is the highest-risk assumption that can be tested in the next two weeks?
- Which part of the current system or method should be removed, narrowed, or redesigned?

### Deadlines
- **Nov 5, 8:00 PM.** Midterm slides due.
- **Nov 9.** Instructor decision memo returned to each team.

# Week 10 — Friday, November 13
## AI for Computer Architecture I: Measuring and Exploring
**Module II — AI for Computing | 🎤 Guest lecture: AI-assisted architecture design (speaker TBC) | Two student-led papers**

### Learning goals
- Survey how AI enters the architecture pipeline: learned components inside the microarchitecture, learned performance prediction, design-space exploration, and agentic architecture design.
- Compare architectural DSE methods under equal simulator and wall-clock budgets; distinguish parameter tuning from semantic mechanism discovery.
- Understand how to *measure* AI architects — benchmarks, evaluator scope, and auditable design trajectories.

### Mini-lecture: The AI-for-architecture landscape
Design spaces: parameters, mappings, policies, mechanisms, RTL; evaluation fidelity from analytical models to cycle-accurate simulation to synthesis; optimizer bias — heuristics, BO, RL, evolution, LLM priors; gymnasium-style environments (ArchGym) and why benchmarking agents is harder than benchmarking optimizers.

### Student-led papers
1. **ArchEval: Measuring AI Agents as Computer Architects** — arXiv 2026. [paper](https://arxiv.org/abs/2607.03601)
   *Focus: benchmarking LLM agents on architecture design/optimization tasks across difficulty levels and feedback regimes.*
2. **PF-LLM: Large Language Model Hinted Hardware Prefetching** — ASPLOS 2026. [paper](https://doi.org/10.1145/3779212.3790202)
   *Focus: AI inside the microarchitecture — a concrete learned mechanism, evaluated on architecture's own terms.*

### Optional readings
ArchGym (ISCA 2023) · AgentDSE (MLArchSys 2026) · LLM-DSE (arXiv 2025) · ConfuciuX (MICRO 2020) · Concorde (2025) · QuArch (2025) · learned memory-access patterns (ICML 2018)

### Questions to carry into discussion
- What must a benchmark control for its leaderboard to mean anything about "AI architects"?
- When is a learned mechanism inside the pipeline preferable to a designed one — and how would you know?
- Which feedback signal (score, trace, report, waveform) most improves an agent's design ability per unit cost?

### Deadlines
- **Nov 13, 5:00 PM.** P3 Evaluation-readiness check-in due.

# Week 11 — Friday, November 20
## AI for Computer Architecture II: Agentic Design Systems
**Module II — AI for Computing | 🎤 Guest lecture: agentic hardware design frameworks (speaker TBC) | Two student-led papers**

### Learning goals
- Move from evaluating AI architects to building them: end-to-end agentic design systems, their environments, and their trust boundaries.
- Analyze how representation, simulator fidelity, seed design, and objective definition shape what agents can discover.
- Reason about evaluator scope: what happens when a proposed design lies outside what existing tools can score?

### Mini-lecture: Inside an agentic architecture-design system
The agent loop for hardware — observe, hypothesize, act, simulate, diagnose, revise; composable design loops and tool orchestration. **Case study: ArchOrchestra** (instructor's current work, released Sep 2026) — an end-to-end agentic accelerator-design system: evaluator-scope analysis (why agents confined to scoreable designs cannot discover new mechanisms), machine-readable capability cards, measured performance envelopes for unsupported components, and trust separation between Grounder, Designer, and Implementor.

### Student-led papers
1. **CHIA: An Open-Source Framework for Principled, Agentic AI-Driven Hardware/Software Co-Design Research** — UC Berkeley, arXiv 2026. [paper](https://arxiv.org/abs/2606.27350)
   *Focus: composable design loops that let agents automate HW/SW co-design workflows across simulators and learned models.*
2. **Agentic Architect: An Agentic AI Framework for Architecture Design Exploration and Optimization** — arXiv 2026. [paper](https://arxiv.org/abs/2604.25083)
   *Focus: LLM-driven microarchitecture evolution with cycle-accurate feedback — and the finding that seed quality bounds what agents discover.*

### Optional readings
ArchOrchestra (arXiv, Sep 2026) · AgentDSE (MLArchSys 2026) · LLM-DSE (arXiv 2025) · AlphaEvolve's TPU-circuit result (from Week 8) · FireSim (ISCA 2018) · Chipyard (2020)

### Questions to carry into discussion
- When does a richer action space create discovery rather than simply increase search cost?
- How strongly do seed quality and human-specified constraints bound an agent's apparent creativity?
- What should the division of labor be between the environment, the agent, and the human architect?

### Deadlines
- **Nov 24, 5:00 PM.** P4 Main-results check-in due (before Thanksgiving; no deadline on the holiday).

# Week 12 — Friday, December 4
## AI for RTL and Chip Physical Design
**Module II — AI for Computing | Mini-lecture plus three student-led papers**

### Learning goals
- Map AI-driven design onto the specification-to-RTL-to-GDSII flow, and differentiate generation, prediction, search, and tool-orchestration roles.
- Evaluate RTL-generation benchmarks and what "passing the testbench" does and does not prove — design automation requires verification automation.
- Critically evaluate high-profile claims in this space, from the field's most contested Nature paper to industry white papers.

### Mini-lecture: The hardware design flow, the evidence hierarchy, and the failure modes
Spec → microarchitecture → RTL → simulation → synthesis → place-and-route → timing → signoff; AI roles at each stage — domain adaptation, code and script generation, QoR prediction, placement, tool orchestration, verification (assertion generation, formal aids); the evidence hierarchy (syntax → unit tests → assertions → equivalence → formal → PPA); failure modes — weak testbenches, reward hacking, contaminated benchmarks, unaudited agent actions. **Short critical-reading exercise:** the *RedWood* white paper (Architect Labs, 2026) — an accelerator claimed to be designed, verified, and deployed by AI in two weeks; the class applies the evidence-centered checklist to an industry claim.

### Student-led papers
1. **A Graph Placement Methodology for Fast Chip Design (AlphaChip)** — Nature 2021, read together with the 2024 addendum and Markov's critique ["The False Dawn" (2023)](https://arxiv.org/abs/2306.09633). [paper](https://www.nature.com/articles/s41586-021-03544-w)
   *Focus: the most celebrated and most contested result in AI-for-chip-design — claims, baselines, reproducibility, and what the controversy teaches about evidence. Co-led by a pair.*
2. **ChipNeMo: Domain-Adapted LLMs for Chip Design** — NVIDIA, 2024. [paper](https://arxiv.org/abs/2311.00176)
   *Focus: domain adaptation, retrieval, EDA scripts, and industrial chip-design knowledge.*
3. **VerilogEval: Evaluating Large Language Models for Verilog Code Generation** — ICCAD 2023. [paper](https://arxiv.org/abs/2309.07544)
   *Focus: RTL-generation benchmarks, testbench-based correctness, and evaluation limitations.*

### Optional readings
AssertLLM (2024) · Using LLMs to Facilitate Formal Verification of RTL (2023) · DREAMPlace (DAC 2019) · CVDP benchmark (NVIDIA 2025) · ChatEDA (TCAD 2024) · VeriMaAS (2025) · SpecLLM (2024) · Chip-Chat (MLCAD 2023) · RedWood white paper (2026)

### Questions to carry into discussion
- Which claims in the AlphaChip saga survive all three documents — the paper, the addendum, and the critique?
- Which verification layer is sufficient for each type of hardware-design claim?
- Applying the evidence checklist to RedWood: what would you need to see to believe it?

### Deadlines
- **Dec 9, 5:00 PM.** P5 Complete paper draft, artifact candidate, and poster due.

# Week 13 — Friday, December 11
## Final Project Poster Session
**Course synthesis | Poster showcase; no mini-lecture and no assigned papers**

### Session plan

| Time | Activity |
|---|---|
| 10:10–10:20 | Setup, welcome, and two-minute lightning introductions |
| 10:20–10:55 | Poster Round A — half the teams present, half review |
| 10:55–11:05 | Break and rotation |
| 11:05–11:40 | Poster Round B — presenters and reviewers switch |
| 11:40–12:00 | Course synthesis: closing the loop between AI as workload and AI as designer; research-continuation decisions |

### Questions to carry into discussion
- What is the strongest result, and does it support the exact claim on the poster?
- What is the most informative failure or negative result?
- What additional experiment would most increase confidence for a conference submission?

### Deadlines
- **Dec 11, 10:00 AM.** Final poster and artifact card available in the shared course folder.
- **Dec 21, 5:00 PM.** Final project paper, reproducible artifact, response-to-feedback memo, and individual contribution statements due.

# 7. Course Policies

## AI use and evidence

> **POLICY STANCE — AI use is permitted and encouraged when it is disclosed, reproducible, and independently verified. Agent output is not evidence by itself.**

- Students may use AI for brainstorming, literature discovery, coding, debugging, experiment orchestration, writing assistance, and design-space exploration.
- Projects must disclose the models, major prompts or tool workflows, relevant settings, API/token cost, and substantive human modifications.
- Every citation must be checked against a primary source. Every numerical result must trace to an actual experiment, simulator output, formal result, or cited source.
- AI-generated code must satisfy the same correctness, testing, performance, licensing, and provenance requirements as human-written code.
- The final artifact must distinguish agent actions, human decisions, tool feedback, and verified outcomes.

## Collaboration, authorship, and research continuation

Course collaboration does not automatically establish publication authorship. If a project continues after the semester, authorship and ordering will follow substantive intellectual and technical contributions, manuscript participation, accountability, and applicable venue policies. Students retain credit for their work, and any continuation plan should be discussed transparently with the instructor and research mentors.

## Academic integrity

Students must follow Columbia academic-integrity policies. Fabricated citations, invented experiments, altered logs, undisclosed result selection, plagiarism, or presenting agent-generated claims as verified evidence are serious violations. When in doubt, disclose the tool, source, assistance, or collaboration.

## Accessibility and accommodations

Students who require disability-related accommodations should contact Columbia Disability Services and inform the instructor as early as possible so approved accommodations can be implemented. Students are encouraged to communicate time-sensitive circumstances before deadlines whenever possible.

## Resource fairness

- Projects will report GPU, API, token, simulation, and wall-clock budgets.
- Grades will not be based on access to the largest model, most GPUs, or specialized hardware.
- Every project must define a fallback experiment that remains valid if an API, simulator, board, robot, or cloud resource becomes unavailable.
- Curated starter environments and smoke tests will be provided for officially supported project directions when feasible.

## Late work

Each project team may use one 48-hour grace pass on a written milestone, requested before the deadline. The grace pass does not apply to in-class presentations, the final poster, or the final submission. Other extensions require prior approval or documented circumstances.

## Changes to the syllabus

This is a first-offering advanced-topics course in a rapidly changing research area. The instructor may update individual readings, project briefs, guest-speaker scheduling, or detailed deadlines when new work appears or infrastructure changes. Material changes will be announced clearly and will not retroactively disadvantage students.

# 8. Sources

- **Columbia University Registrar, Fall 2026 Academic Calendar** — [registrar.columbia.edu/content/academic-calendar](https://registrar.columbia.edu/content/academic-calendar)
- **Instructor website** — [zishenwan.github.io](https://zishenwan.github.io/)
- **Wan Lab** — [wan-research-group.github.io](https://wan-research-group.github.io/)

*All assigned-paper links appear in the corresponding weekly entries and were individually verified against their primary sources in August 2026. The course website will provide a consolidated reading list, presentation assignments, project briefs, and downloadable templates.*

---
*Changelog v3 → v4: guest speakers listed without names pending invitations (an unfilled guest slot reverts to a regular three-paper week); Week 4 refocused from VLA algorithms to inference systems and serving for embodied AI (Embodied.cpp, VLASH, VLA-Perf student-led; π0/OpenVLA/DeeR-VLA → optional, covered as algorithm background in the mini-lecture); Week 6 second paper changed from Gemmini to Columbia's ESP platform (Gemmini → optional); the standalone verification week removed — AI for Computer Architecture expanded to two weeks (W10 Measuring & Exploring: ArchEval + PF-LLM; W11 Agentic Design Systems: CHIA + Agentic Architect, ArchOrchestra case study moved here), and AI for RTL and Chip Physical Design moved to W12 with verification folded into its mini-lecture and optional readings. Guest weeks now 3, 6, 10, 11; milestone dates unchanged.*

*Changelog v2 → v3: LLM serving and agentic serving merged into a single Week 3 ("Serving LLMs and AI Agents"), rebalancing to five Computing-for-AI + four AI-for-Computing seminar weeks; all Module I weeks shifted one week earlier.*

*Changelog v1 → v2: class perspective paper removed (may return in a future offering); grading consolidated from 13 to 7 components with P1–P5 check-ins graded on completeness; methodology and LLM-fundamentals lectures combined in Week 2; Physical AI expanded to two weeks; guest-speaker slots embedded; paper list revised and all links verified; registrar citation corrected and drop/pass-fail dates added.*
