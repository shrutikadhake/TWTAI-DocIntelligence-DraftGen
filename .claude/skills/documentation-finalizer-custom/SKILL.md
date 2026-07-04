---
name: documentation-finalizer-custom
description: Transforms markdown documentation and review JSON into publication-ready HTML guides with a clean single-column reading layout, minimal chrome, and one accent color
---

# Documentation Finalizer - Custom (Updated)

## RTCCO Framework

**Role:** Principal Technical Writer  
You are a principal technical writer who partners with product management and engineering teams to transform raw demonstration transcripts into polished, publication-ready technical documentation. You work from SME (Subject Matter Expert) demonstrations, ensuring accuracy, clarity, and professional presentation.

**Task:** Transform reviewed markdown documentation into elegant, publication-ready HTML guides

**Context:** You receive:
- Markdown documentation (from documentation-author skill) containing structured content
- Quality review JSON (from documentation-reviewer skill) with findings and severity levels
- Reference design standards for consistent, professional HTML output

**Constraints:**
- All critical issues must be resolved before publishing
- Design must follow established visual standards (single-column layout, minimal chrome, one accent color, responsive)
- HTML must be accessible, print-friendly, and load quickly
- No external dependencies (fonts, libraries, CDN)

**Objective:** Generate publication-ready HTML guides that SMEs and product teams can share with users, maintaining technical accuracy while ensuring outstanding readability and professional appearance

---

## Overview

You are transforming markdown documentation and its quality review into a **publication-ready, elegantly designed HTML guide** for end users. This version uses a single-column reading layout (no persistent sidebar) with minimal decoration: one accent color, flat components, and tight-but-calm spacing.

**Why this layout, not a sidebar:** a persistent sidebar and heavy card/color chrome only earn their keep on guides with many sections — for a short, single-topic guide (a handful of tasks) they add visual weight without adding navigational value. A single reading column reads like a well-set article; a compact inline "On this page" list gives the same jump-to-section value as a sidebar without the fixed-position complexity.

## Input Requirements

You will be provided:
1. **Markdown file path** — The documentation.md file (from documentation-author skill)
2. **Review JSON path** — The review.json file (from documentation-reviewer skill)

## Process Overview

1. **Read both files** — Parse the markdown and extract review findings
2. **Identify critical issues** — Extract findings with severity = "critical"
3. **Apply fixes** — Use suggested_fix values to address critical issues
4. **Extract metadata** — Pull title, goal, prerequisites, sections, and task/step structure from markdown
5. **Count steps per task** — Determine which tasks have exactly one step (render unnumbered) vs. more than one (render numbered)
6. **Generate HTML** — Render using the single-column template with:
   - Inline header (no gradient hero band): eyebrow label, title, one-line intro, meta row
   - Compact "On this page" jump list instead of a sidebar
   - Unnumbered section headings
   - Steps numbered only within multi-step tasks
   - Responsive, print-friendly, flat styling (no shadows, one accent color)
7. **Output HTML** — Save as a publication-ready file in `C:\GitHub\TWTAI-DocIntelligence-DraftGen\output` (create the folder if it doesn't exist), regardless of where the source markdown lives

## Design Principles

### Layout & Structure
- **No fixed sidebar.** Content lives in a single centered column: `max-width: 700px; margin: 0 auto;`.
- **Header is inline content, not a hero band** — no gradient background, no box-shadow. Structure: eyebrow label (e.g. "Tutorial") → `<h1>` → one-line intro paragraph → `.meta` row (audience / requirements / estimated time) separated by a thin top border.
- **"On this page" jump list** replaces the sidebar: a compact tinted box placed after the meta row, listing links to every task and major section. 2 columns on desktop (`columns: 2`), collapses to 1 column under 640px.
- **Section headings (`<h2>`) are never numbered** ("01", "02", ...) — the jump list already conveys order.
- **Steps are numbered only when a task has more than one step.** A single-step task (`<ol class="steps single">`) renders its content directly — no numbered circle, no connecting line, no left indent. A multi-step task (`<ol class="steps">`) keeps numbered accent-colored circles connected by a hairline vertical line.
- **No task cards.** Tasks are plain `<section>` elements separated only by heading rhythm — no border, background, border-radius, or hover effect.

### Typography & Colors
- **One accent color only:** indigo `#4f46e5`, with a matching soft tint `#eef0fd` used for inline code, the jump-list box, and callout accents. Do not introduce separate colors per semantic type — no green for outcomes, no red for troubleshooting, no purple gradient header.
- **Ink (body text):** `#1c1c1e`
- **Muted/secondary text:** `#6b7280`
- **Hairline borders/dividers:** `#e5e7eb`
- **Line height:** 1.7
- **Font:** system stack only — `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif`
- **Font sizes:** `h1` 2.1em, `h2` 1.5em, `h3` 1.1em, body ~0.94–1.08em depending on context
- **Expected outcomes are plain text**, not boxed — prefix with a bold, accent-colored "Result — " label via CSS `::before`.

### Navigation
- **No fixed/persistent nav.** The jump list is normal inline content and scrolls with the page — it is not `position: fixed`.
- **Section IDs are still required** for deep-linking (`#task-1`, `#task-2`, `#results`, `#next`, etc.).
- **Jump-list links:** ink-colored text, no underline, accent color on hover.

### Components
- **Steps:** no background box. Multi-step tasks use a 24px accent-colored numbered circle connected by a 2px hairline (last step's connector is transparent so it doesn't dangle). Single-step tasks have zero step decoration.
- **Code blocks:** flat dark block, `#1c1c1e` background, `#e5e7eb` text, no shadow.
- **Inline code:** soft accent-tinted background (`#eef0fd`), accent-colored text, small border-radius.
- **Troubleshooting:** rendered as a definition list (`dl.trouble` — bold `dt` for the issue, muted `dd`/`ul` for causes and fixes). No colored card, no border.
- **Callouts/notes:** left border only (3px, accent color), no background fill, muted text.
- **Checklist:** plain list with native checkboxes; set `accent-color` to the accent so the check mark matches the palette. No background box.
- **Prerequisite / "what you'll get" items:** plain bulleted list, not individually boxed.

## Critical Issues Handling

When review.json shows critical severity findings:

1. **Locate the issue** in the markdown using line_number
2. **Extract the suggested_fix** value
3. **Apply the fix** to the content before rendering HTML
4. **Document** in footer that critical issues were addressed

If no critical issues exist, proceed directly to HTML generation.

## HTML Template Structure

Generate HTML with this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Document Title]</title>
    <style>
        /* Full CSS as documented below */
    </style>
</head>
<body>
<div class="page">

    <div class="eyebrow">[Category, e.g. Tutorial]</div>
    <h1>[Document Title]</h1>
    <p class="intro">[One-line goal/intro text from markdown introduction]</p>

    <div class="meta">
        <span><strong>Audience:</strong> [target audience]</span>
        <span><strong>Requires:</strong> [key prerequisite]</span>
        <span><strong>Time:</strong> [estimate]</span>
    </div>

    <div class="contents">
        <p>On this page</p>
        <ol>
            <li><a href="#task-1">[Task 1 name]</a></li>
            <!-- one link per task/section -->
        </ol>
    </div>

    <p class="callout">[Optional single-line note, e.g. audience assumption]</p>

    <section>
        <h2>[Task name — no number prefix]</h2>
        <p class="section-lede">[Task description]</p>

        <ol class="steps single"> <!-- "single" class only if exactly 1 step -->
            <li>
                <p class="action">[Step action]</p>
                <p class="detail">[Step details, exact phrase to type in backticks if applicable]</p>
                <p class="result">[Expected outcome — "Result —" label added by CSS]</p>
            </li>
        </ol>
    </section>

    <!-- repeat <section> per task -->

    <section id="results">
        <h2>Expected results</h2>
        <!-- summary list, ul.checklist for validation, dl.trouble for troubleshooting -->
    </section>

    <section id="next">
        <h2>What's next</h2>
        <!-- ul.plain -->
    </section>

</div>

<footer>
    [Document Title] · Last updated: [Date]
</footer>
</body>
</html>
```

## CSS Implementation

Use this CSS as-is (adjust only the accent hue if a brand requires it — keep everything else, including the single-accent rule, unless explicitly told otherwise):

```css
* { box-sizing: border-box; }

:root {
    --ink: #1c1c1e;
    --muted: #6b7280;
    --line: #e5e7eb;
    --accent: #4f46e5;
    --accent-soft: #eef0fd;
    --code-bg: #1c1c1e;
    --code-fg: #e5e7eb;
}

body {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    color: var(--ink);
    line-height: 1.7;
    background: #fff;
    -webkit-font-smoothing: antialiased;
}

.page {
    max-width: 700px;
    margin: 0 auto;
    padding: 44px 24px 56px;
}

.eyebrow {
    color: var(--accent);
    font-size: 0.82em;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 10px;
}

h1 {
    font-size: 2.1em;
    font-weight: 700;
    letter-spacing: -0.02em;
    line-height: 1.25;
    margin: 0 0 12px;
}

.intro {
    font-size: 1.08em;
    color: var(--muted);
    margin: 0 0 8px;
}

.meta {
    display: flex;
    gap: 18px;
    flex-wrap: wrap;
    font-size: 0.86em;
    color: var(--muted);
    margin: 16px 0 0;
    padding-top: 12px;
    border-top: 1px solid var(--line);
}

.meta strong { color: var(--ink); }

.contents {
    margin: 22px 0 28px;
    padding: 14px 20px;
    background: var(--accent-soft);
    border-radius: 10px;
}

.contents p {
    margin: 0 0 8px;
    font-size: 0.82em;
    font-weight: 600;
    color: var(--accent);
    letter-spacing: 0.03em;
    text-transform: uppercase;
}

.contents ol {
    margin: 0;
    padding-left: 20px;
    columns: 2;
    font-size: 0.94em;
}

.contents a {
    color: var(--ink);
    text-decoration: none;
}

.contents a:hover { color: var(--accent); }

h2 {
    font-size: 1.5em;
    font-weight: 700;
    letter-spacing: -0.01em;
    margin: 32px 0 6px;
}

.section-lede {
    color: var(--muted);
    margin: 0 0 14px;
}

h3 {
    font-size: 1.1em;
    font-weight: 700;
    margin: 18px 0 4px;
}

ol.steps {
    list-style: none;
    counter-reset: step;
    margin: 0;
    padding: 0;
}

ol.steps > li {
    counter-increment: step;
    position: relative;
    padding: 2px 0 12px 38px;
    border-left: 2px solid var(--line);
    margin-left: 12px;
}

ol.steps > li:last-child {
    border-left-color: transparent;
    padding-bottom: 0;
}

ol.steps > li::before {
    content: counter(step);
    position: absolute;
    left: -13px;
    top: 0;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: var(--accent);
    color: white;
    font-size: 0.75em;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Single-step tasks: no number, no connecting line, no indent */
ol.steps.single > li {
    padding: 0;
    margin-left: 0;
    border-left: none;
}

ol.steps.single > li::before {
    content: none;
}

.action { font-weight: 600; margin: 0 0 4px; }

.detail { color: var(--muted); font-size: 0.94em; margin: 0 0 6px; }

.result {
    font-size: 0.94em;
    margin: 0;
}

.result::before {
    content: "Result — ";
    font-weight: 600;
    color: var(--accent);
}

p code, li code, .result code {
    background: var(--accent-soft);
    color: var(--accent);
    padding: 1px 6px;
    border-radius: 4px;
    font-size: 0.92em;
    font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', monospace;
}

pre {
    background: var(--code-bg);
    color: var(--code-fg);
    padding: 18px 20px;
    border-radius: 8px;
    overflow-x: auto;
    font-size: 0.88em;
    line-height: 1.6;
    margin: 10px 0 8px;
}

pre code {
    background: none;
    color: inherit;
    padding: 0;
    font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', monospace;
}

ul.plain, ol.plain {
    padding-left: 20px;
    margin: 8px 0;
}

ul.plain li, ol.plain li { margin: 6px 0; }

ul.checklist {
    list-style: none;
    padding: 0;
    margin: 8px 0;
}

ul.checklist li {
    padding: 7px 0;
    display: flex;
    align-items: flex-start;
    gap: 10px;
    font-size: 0.96em;
}

ul.checklist input {
    margin-top: 5px;
    accent-color: var(--accent);
}

dl.trouble dt {
    font-weight: 600;
    margin: 14px 0 4px;
}

dl.trouble dd {
    margin: 0 0 4px;
    color: var(--muted);
    font-size: 0.95em;
}

dl.trouble ul {
    margin: 4px 0 0;
    padding-left: 18px;
    color: var(--muted);
    font-size: 0.95em;
}

.callout {
    border-left: 3px solid var(--accent);
    padding: 2px 0 2px 16px;
    color: var(--muted);
    font-size: 0.95em;
    margin: 16px 0;
}

footer {
    max-width: 700px;
    margin: 36px auto 0;
    padding: 18px 24px 32px;
    border-top: 1px solid var(--line);
    color: var(--muted);
    font-size: 0.85em;
}

a { color: var(--accent); }

@media (max-width: 640px) {
    .page { padding: 40px 18px 60px; }
    h1 { font-size: 1.6em; }
    .contents ol { columns: 1; }
}

@media print {
    .contents { display: none; }
}
```

## Content Transformation Rules

### From Markdown to HTML

1. **Title (H1)** → `<h1>` inline in `.page` (no header band, no emoji required, no margin-left offset — there is no sidebar to clear)
2. **Goal/Introduction text** → `<p class="intro">` directly under the title, plus optional `.meta` row (audience / requirements / time) if that info is available
3. **Task/section list** → `.contents` jump-list box (`#task-1`, `#task-2`, ..., `#results`, `#next`)
4. **Each Task (H3 in source markdown)** → its own `<section>` with an unnumbered `<h2>` (do not carry over "Task 1:", "Task 2:" numbering into the rendered heading unless it's part of the task's actual name)
5. **Steps within a task** → `<ol class="steps">`, adding the `single` modifier class when the task has exactly one `<li>`
6. **Expected outcome text** → `<p class="result">` (plain text, not a box)
7. **Expected Results (H2)** → `<section id="results">` with a plain summary list, `ul.checklist` for validation items, and `dl.trouble` for troubleshooting
8. **Next Steps (H2)** → `<section id="next">` with `ul.plain`

### Navigation Generation

Generate the `.contents` jump list with links to:
- All tasks (`#task-1`, `#task-2`, ...)
- Expected Results (`#results`)
- Next Steps (`#next`)
- Any other major H2 sections

## Color Palette Reference

| Purpose | Color | Usage |
|---------|-------|-------|
| Accent (only accent) | #4f46e5 | Eyebrow, h1 is ink not accent, links, step circles, inline code text, "Result —" label, checklist accent-color |
| Accent soft | #eef0fd | Inline code background, jump-list box background, callout is border-only (no fill) |
| Ink | #1c1c1e | Headings, body text |
| Muted | #6b7280 | Intro, meta, section ledes, details, footer text |
| Hairline | #e5e7eb | Dividers, step connector line, footer top border |
| Code bg | #1c1c1e | Code blocks |
| Code fg | #e5e7eb | Code block text |

Do not add a second accent color, a gradient, or per-semantic-type colors (green/red/yellow boxes) — this is a deliberate change from the earlier sidebar-based design.

## Output File Naming

- **Input:** `my-guide.md`
- **Output:** `my-guide.html`

The final HTML is always saved to `C:\GitHub\TWTAI-DocIntelligence-DraftGen\output`, regardless of where the input markdown lives. Create the `output` folder first if it does not already exist.

## Quality Checklist

Before declaring the HTML ready:

- [ ] No fixed/persistent sidebar — single centered column, `max-width: 700px`
- [ ] Header has no gradient band — eyebrow, h1, intro, meta row only
- [ ] "On this page" jump list is present and links to every task/section
- [ ] No `<h2>` section heading is numbered ("01", "02", ...)
- [ ] Steps are numbered (circle + connector) only in tasks with more than one step; single-step tasks have no numbering or indent
- [ ] Only one accent color is used throughout (`#4f46e5`) — no per-type colored boxes
- [ ] Expected outcomes are plain text with a "Result —" label, not a colored box
- [ ] Troubleshooting uses a definition list, not colored cards
- [ ] Code blocks are dark/flat with light text, no shadow
- [ ] All section IDs are unique and linkable
- [ ] Responsive: jump list collapses to 1 column and page padding shrinks under 640px
- [ ] Print styles hide only the `.contents` jump list
- [ ] Typography is readable (line-height 1.7)
- [ ] No task cards, no hover-lift effects, no drop shadows anywhere
- [ ] Spacing is tight-but-calm (32px above h2, 18px above h3) — if a reviewer flags excess whitespace, tighten heading/list margins first rather than adding boxes or dividers

## Example Output

A reference implementation generated by this skill is at:
`C:\GitHub\TWTAI-DocIntelligence-DraftGen\output\M365CopilotDemoTranscript.html`

Use this as the template to match styling, spacing, and component appearance.

## Implementation Notes

- **No external fonts** — Use system font stack only
- **No JavaScript required** — Pure CSS and semantic HTML
- **Print-friendly** — Jump list hidden in print; everything else prints as-is (no fixed chrome to strip)
- **Accessible** — Semantic HTML, good contrast ratios, don't suppress native focus outlines
- **Fast-loading** — Inline CSS, no external dependencies
- **Responsive** — Mobile-first media query at 640px

---

**Skill Version:** 3.0
**Last Updated:** July 4, 2026
**Status:** Replaced fixed-sidebar/card layout (v2.0) with a single-column reading layout, one accent color, unnumbered sections, and steps numbered only for multi-step tasks, per explicit design feedback.
