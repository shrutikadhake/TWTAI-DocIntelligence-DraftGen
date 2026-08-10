# Document Intelligence: Draft Generator & Automated Pre-Review

**Tagline:** *Raw demo transcript to publication-ready HTML — four skills, zero manual formatting.*

*(This tagline is drawn directly from the wording already used in this repository's own workflow diagram — [output/workflow-diagram.svg](../output/workflow-diagram.svg) — and formalized here as the project's tagline.)*

---

## 1. What This Is

This project is a proof of concept for an AI-driven documentation pipeline. It takes a raw, unedited software demo transcript and turns it into a polished, publication-ready HTML guide — with an automated quality check in between — using four purpose-built AI skills chained together, and no manual formatting step.

It is one specific workstream ("Demo Transcripts," input format `.vtt`) within the broader **Document Intelligence Platform** initiative — an effort to reduce the manual work technical writers spend converting scattered source material into documentation and running repetitive pre-review checks (style, formatting, terminology, readability).

## 2. The Problem

Technical writers repeatedly perform the same sequence of manual work for every new demo recording or walkthrough:

- Watch or re-listen to the transcript and take notes
- Structure the raw narration into a goal, prerequisites, and step-by-step tasks
- Draft the material into clear, user-facing prose
- Run a style-guide review pass (clarity, tone, terminology, accessibility)
- Hand-build or re-style the final HTML page

Each step is repetitive, and demo transcripts specifically add extra friction: they are noisy and verbose, contain filler words and tangents, and require extracting an ordered sequence of steps from spoken narration while mapping on-screen UI actions to written instructions.

## 3. The Solution: A Four-Skill Pipeline

The solution is a chain of four custom Claude Code skills, each with a single, well-defined responsibility. The output of one skill is the exact input of the next:

| # | Skill | Responsibility | Output |
|---|-------|-----------------|--------|
| 1 | `transcript-normalizer-custom` | Strips timestamps, filler words, false starts, and side conversations from the raw `.vtt` transcript; extracts topic, goal, prerequisites, technical facts, and task/step structure | Structured JSON |
| 2 | `documentation-author-custom` | Writes a task-oriented Markdown guide — introduction, prerequisites, numbered steps, expected outcomes — addressed directly to the reader ("You") | Draft Markdown |
| 3 | `documentation-reviewer-custom` | Scores the draft against 8 professional writing standards (clarity, conciseness, active voice, accessibility, heading hierarchy, task orientation, terminology consistency, Microsoft writing-style compliance), producing line-numbered findings with severity levels and suggested fixes | `review.json` + a standalone QA `review.html` dashboard |
| 4 | `documentation-finalizer-custom` | Renders the reviewed Markdown into a clean, single-column, publication-ready HTML page (one accent color, no sidebar, no external dependencies) | Final published HTML guide |

Each skill is defined with a Role-Task-Context-Constraints-Objective (RTCCO) specification, versioned, and reusable — the same four skills apply to every future demo transcript, not just this one.

## 4. The Proof of Concept, End to End

The pipeline was run against a real artifact: **`M365CopilotDemoTranscript.vtt`**, a demo recording of using Microsoft 365 Copilot Chat to learn HTML basics.

**Stage 1 — Normalize.** The raw transcript was converted into structured JSON:
- **Topic:** "Learning Basic HTML with Microsoft 365 Copilot Chat"
- **Goal:** Use Microsoft 365 Copilot Chat to learn HTML basics, generate a working page example, and understand individual HTML elements
- **Prerequisites:** Access to Microsoft 365 Copilot Chat; basic familiarity with chat interfaces
- **4 tasks, 8 total steps** — asking Copilot what HTML is, requesting a simple HTML example, exploring individual elements (`h1`, `h2`), and using follow-up questions to build fuller pages

**Stage 2 — Author.** The JSON was turned into a full Markdown guide: an introduction, a prerequisites section, four numbered tasks with steps and expected outcomes, a validation checklist, and a troubleshooting section — all addressed directly to the reader.

**Stage 3 — Review.** The Markdown draft was scored against the 8 writing-standard categories:

| Category | Score | Passed? |
|---|---|---|
| Clarity | 90 | Yes |
| Conciseness | 92 | Yes |
| Active voice | 88 | Yes |
| Accessibility | 90 | Yes |
| Heading hierarchy | 100 | Yes |
| Task orientation | 82 | Yes |
| Terminology consistency | 75 | **No** |
| Microsoft writing-guidance compliance | 88 | Yes |

**Overall score: 88.1 / 100.** Severity breakdown: **0 critical, 4 warnings, 3 info-level findings.** The only failed category was terminology consistency — the reviewer caught that the Copilot-generated example was referred to by three different names across the document ("HTML page structure," "sample web page," "HTML page example"). Publication readiness was assessed as *"READY TO PUBLISH — meets standards; recommended to tighten terminology consistency and step phrasing before external distribution."*

**Stage 4 — Finalize.** The reviewed Markdown was rendered into the final HTML guide at `output/M365CopilotDemoTranscript.html`, following a single-column reading layout with one accent color, an inline "On this page" jump list, and numbered steps only for multi-step tasks.

## 5. Effort & Time — Estimated, Not Measured

There is no instrumented timer and no human baseline run on this same transcript (n = 1, one small, single-topic document). The numbers below are the project's own reasoned estimate of a typical manual technical-writing workflow, compared against the time this session actually took using the four skills:

| Step | Manual (typical, no AI) | AI-skill pipeline (this session) |
|---|---|---|
| Watch/re-listen to transcript, take notes | 10–15 min | 0 (skill parses text directly) |
| Structure into goal/prerequisites/tasks/steps | 10–15 min | ~instant (`transcript-normalizer`) |
| Draft Markdown prose | 20–30 min | ~instant (`documentation-author`) |
| Style-guide review pass | 15–20 min *(often skipped in practice)* | ~instant, with accuracy caveats below |
| Hand-build/style HTML page | 20–40 min (template exists) to 60–90 min (from scratch) | ~instant (`documentation-finalizer`; template already encoded in the skill) |
| Human oversight (reading/approving outputs) | — | ~5–10 min (4 commands, skim 4 output files) |
| **Total active human time** | **~75–170 min** | **~5–10 min** |

That implies a large relative reduction (roughly 85–90%), but this is directional, not statistical:

- This is a tiny document (77-line transcript, 4 tasks, 8 steps). A real 45-minute multi-feature demo would look different — potentially more absolute time saved, but also more room for the AI to miss things.
- If a writer already had a reusable HTML template, manual time drops toward the low end of the range, shrinking the gap.
- The one-time cost of building and tuning the four skills is a sunk cost that only pays off with repeated use, not on document #1.

## 6. What "88.1/100" Actually Means (and Doesn't)

The QA score is a real, measured output of this session — but it comes with an important limitation: **the same model authored, reviewed, and finalized the document.** This is self-grading, not independent QA. A model is structurally biased toward not flagging its own blind spots — if the authoring skill has a systematic habit, the reviewing skill is likely to share that habit and miss it. So 88.1/100 tells you *"this document survived a self-consistency check,"* not *"this document is 88% accurate against ground truth."*

A concrete process gap surfaced during this proof of concept: the finalizer stage added two lines to the published HTML that were never reviewed —

- `Time: ~10 minutes` — a completely invented estimate, not derived from the transcript or the JSON.
- `Audience: Anyone new to HTML` — a reasonable inference, but still unsourced.

Both are visible today in `output/M365CopilotDemoTranscript.html`. They exist because review happens *before* finalize, so anything the finalize stage adds on its own is never checked. That is a defect in the pipeline's ordering, not a defect in any single skill.

**What cannot be honestly claimed:** whether a human writer would have produced more or fewer errors on this same transcript — there is no baseline run to compare against. The directional claim that holds up is narrower: the AI pipeline's errors on this document were minor (style/consistency, not factual), and its critical-error rate was 0.

## 7. Bottom Line

- **Effort savings are real and large for this pipeline** on this artifact, but the number is a rough estimate on a single small document, not a validated benchmark. Treat "~90% less active time" as a plausible order of magnitude, not a metric to cite as measured fact.
- **Accuracy cannot be honestly quoted as a single percentage.** 88.1/100 is a real, measured self-consistency score, but it overstates confidence because the same system graded its own homework, and it doesn't cover content the finalizer added after review ran.
- **The pipeline works end to end**, on a real artifact, with zero critical defects and a documented, reusable set of four skills.

## 8. What's Next

Based on the gaps this proof of concept surfaced:

- Add an instrumented timer to replace estimated effort numbers with measured ones.
- Run an independent review pass (a different model, or a human) to validate the QA score isn't just self-consistency.
- Fix the pipeline ordering so content the finalizer adds (like time estimates or audience inferences) is reviewed too — either review after finalize, or restrict the finalizer to formatting only, with zero new factual content.
- Test the same four-skill pipeline against a larger, multi-feature demo transcript to see whether effort savings and error rates hold at scale.

## 9. Project Resources

- **Input:** Demo transcripts in `.vtt` format (e.g. `resources/M365CopilotDemoTranscript.vtt`)
- **Output:** Publication-ready HTML page with the structured walkthrough (`output/M365CopilotDemoTranscript.html`)
- **Skills:** `.claude/skills/transcript-normalizer-custom`, `.claude/skills/documentation-author-custom`, `.claude/skills/documentation-reviewer-custom`, `.claude/skills/documentation-finalizer-custom`
- **QA artifacts:** `resources/M365CopilotDemoTranscript-review.json`, `resources/M365CopilotDemoTranscript-review.html`
- **Effort/accuracy analysis:** `output/effort-accuracy-metrics.md`
- **Workflow diagram:** `output/workflow-diagram.svg`

---

*This is one individual workstream ("Demo Transcripts") within the wider Document Intelligence Platform initiative (AI Adoption in Technical Writing: Draft Generator & Automated Pre-Review). Figures above describe only this workstream's proof of concept and are not claims about the platform as a whole.*
