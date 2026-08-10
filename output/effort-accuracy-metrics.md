# Effort & Accuracy Metrics — AI Skills Pipeline vs. Manual Process

**Document reviewed:** M365CopilotDemoTranscript (normalize → author → review → finalize)
**Date:** 2026-07-05

Before the numbers, the honest caveat: there is no instrumented timer, no human baseline run on this same transcript, and n=1 (one small, single-topic document). Every number below is labeled **measured** (something traceable to this session's actual output) or **estimated** (a reasoned ballpark that cannot be verified). Estimates are not dressed up as measurements.

## Effort — estimated, not measured

| Step | Manual (typical, no AI) | AI-skill pipeline (this session) |
|---|---|---|
| Watch/re-listen transcript, take notes | 10–15 min | 0 (skill parses text directly) |
| Structure into goal/prereqs/tasks/steps | 10–15 min | ~instant (transcript-normalizer) |
| Draft markdown prose | 20–30 min | ~instant (documentation-author) |
| Style-guide review pass | 15–20 min *(often skipped in practice)* | ~instant, but see accuracy caveats below |
| Hand-build/style HTML page | 20–40 min (template exists) to 60–90 min (from scratch) | ~instant (finalizer, template already encoded in skill) |
| Human oversight (reading/approving outputs) | — | ~5–10 min (4 commands, skim 4 output files) |
| **Total active human time** | **~75–170 min** | **~5–10 min** |

That implies a large relative reduction (roughly 85–90%), but treat that as directional, not statistical, for these reasons:

- This is a tiny document (77-line transcript, 4 tasks, 8 steps). Savings on a real 45-minute multi-feature demo would look different — potentially more absolute time saved, but also more room for the AI to miss things.
- The manual estimate assumes a writer builds from scratch each time. If they already had a reusable HTML template (likely, since this org has `DESIGN_STANDARDS.md`), manual time drops toward the low end of the range, shrinking the gap.
- The one-time cost of building and tuning the 4 skills themselves isn't in this number — it's a sunk cost that only pays off with repeated use, not on document #1.

## Accuracy — measured from this session, with a real limitation

| Metric | Value | Source |
|---|---|---|
| QA review overall score | 88.1 / 100 | `M365CopilotDemoTranscript-review.json` |
| Critical defects | 0 | same |
| Warnings (style/consistency, not factual) | 4 | same |
| Info-level | 3 | same |
| Category that failed threshold | terminology consistency (75) | same |

**The critical problem with citing that score as "accuracy": the same model authored, reviewed, and finalized the document.** This is self-grading, not independent QA. A model is structurally biased toward not flagging its own blind spots — if the authoring skill has a systematic habit (e.g., always shortening a term the same wrong way), the reviewing skill is likely to share that habit and miss it. So 88.1/100 tells you "this document survived a self-consistency check," not "this document is 88% accurate against ground truth."

A real process gap surfaced during this critique: the finalizer added two lines that were never reviewed —

- `Time: ~10 minutes` — a completely invented estimate, not derived from the transcript or JSON.
- `Audience: Anyone new to HTML` — a reasonable inference, but still unsourced.

Both were added *after* the QA step ran, so they exist in the published HTML with zero QA coverage. That's a defect in the pipeline ordering (review-then-finalize means finalize-stage content is never checked), not a defect in any single skill.

**What cannot be honestly claimed:** whether a human writer would have produced more or fewer errors on this same transcript. There is no baseline run to compare against. Directionally, a rushed human writer often introduces similar issues (terminology drift, passive voice creeping in) — the same categories the reviewer caught here — so there is no confident claim that the AI path is more accurate, only that its errors were minor (style/consistency, not factual) and its critical-error rate was 0 on this one document.

## Bottom line

- **Effort savings are real and large for this pipeline**, but the number is a rough estimate on a single small artifact, not a validated benchmark — treat "~90% less active time" as a plausible order of magnitude, not a metric to cite as measured fact.
- **Accuracy cannot be honestly quoted as a single percentage.** The 88.1/100 is a real, measured self-consistency score, but it overstates confidence because the same system graded its own homework, and it doesn't cover content added after the review step ran.
