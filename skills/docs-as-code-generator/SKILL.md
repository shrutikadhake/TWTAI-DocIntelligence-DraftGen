---
name: docs-as-code-generator
description: Convert raw technical communication (chat logs, transcripts, notes) into clean, structured HTML documentation. Use this skill whenever you need to transform noisy developer communication, meeting transcripts, or raw technical notes into semantic HTML5 documents (Task topics, conceptual guides, reference docs). The skill automatically identifies which documentation topic types (task, concept, reference) the source material can support and generates each applicable topic, extracts procedural intent, filters noise, validates against Microsoft Manual of Style using the Microsoft Learn MCP server, and flags missing content to prevent hallucination. Invoke with the source file name; the topic type is detected automatically from the content. Essential for Docs-as-Code workflows where team members need to convert unstructured communication into build-ready documentation.
compatibility: Requires access to local Git repository workspace and active Microsoft Learn MCP server connection.
---

## Overview

This skill transforms messy, unstructured technical communication into clean, structured HTML5 documentation that conforms to the Microsoft Manual of Style (MSTP). It is designed for technical writers working in Docs-as-Code environments who receive developer chat logs, meeting transcripts, or raw notes and need to extract procedural intent while filtering noise.

The workflow:
1. Reads the specified `.txt` log file from the local workspace
2. Analyzes the content to determine which documentation topic types (`task`, `concept`, `reference`) the source material can actually support — the skill decides this, the user does not specify it
3. Intelligently extracts procedural content, prerequisites, and validation steps while filtering conversational noise
4. Generates semantic HTML5 fragments (no `<html>`, `<head>`, or `<body>` tags) for **each** applicable topic type
5. Validates style compliance using the `/microsoft-docs` skill against MSTP guidelines (sentence case, active voice, second person, terminology)
6. Verifies that all procedural elements are grounded in the source log (anti-hallucination protocol)
7. Flags missing procedural elements and style violations with HTML comments
8. Outputs build-ready, MSTP-compliant HTML ready for import into structured authoring systems

## Input Requirements

- **Source file:** A `.txt` file containing raw technical communication (Slack export, Teams transcript, meeting notes, etc.) located in your working directory
- **MCP connection:** Active Microsoft Learn MCP server connection (Claude will call `microsoft_docs_search` and `microsoft_docs_fetch` to retrieve MSTP guidance as needed)
- **Documentation type:** Determined automatically. The skill analyzes the source content and produces every topic type it can support — `task` (procedural steps), `concept` (explanatory content), and/or `reference` (technical reference). The user does not need to specify a type, though they may optionally request a specific type to restrict the output.
- **Output location:** HTML files are written to `docs-as-code-generator-workspace/output/` relative to your working directory. If the directory doesn't exist, it will be created automatically.

## Output Format

All output is **semantic HTML5 fragments** — no boilerplate tags. Valid output includes:
- `<h1>`, `<h2>`, `<h3>` for headings
- `<p>` for paragraphs
- `<ol>` and `<ul>` for lists
- `<code>` and `<pre>` for code blocks
- `<table>` for structured data
- HTML comments `<!-- ... -->` for validation flags

## How to Invoke This Skill

Provide:
1. The name of the `.txt` file in your working directory
2. Optional: A specific documentation structure type (`task`, `concept`, or `reference`) if you want to restrict the output to that type. If omitted, the skill auto-detects and generates every applicable type.
3. Optional: Specific output constraints (e.g., "include prerequisites, steps, and troubleshooting")

**Example prompt:**
> "Convert `v10_12_rate_limit_chat.txt` into HTML documentation. Extract everything useful for docs, and generate whichever topic types the content supports."

## Execution Instructions

**Output files will be written directly to `docs-as-code-generator-workspace/output/` — not displayed in the Claude interface.**

Process the source file and any requested parameters provided here: $ARGUMENTS

File naming convention:
- Task topics: `task_<topic-name>.html`
- Concept topics: `concept_<topic-name>.html`
- Reference topics: `reference_<topic-name>.html`

Where `<topic-name>` is derived from the main heading in sentence case, slugified (lowercase, hyphens for spaces).

## Workflow

### Phase 0: Detect Applicable Topic Types
Before extracting or generating anything, analyze the source content to decide **which** documentation topic types it can genuinely support. Do not ask the user for a type — infer it from the material. Unless the user has explicitly restricted the output to a specific type, evaluate all three independently:

- **Task** is applicable when the source contains a concrete procedure the reader could follow: ordered steps, commands to run, configuration changes, prerequisites, or expected results.
- **Concept** is applicable **only** when the source contains genuine explanatory content that goes *beyond restating the procedure or the reference facts* — that is, content that would be lost if you generated only the task and reference topics. Qualifying content includes: a definition of *what* the feature is and the problem it solves, the *design rationale* for why it behaves as it does, or an explanation of *how components relate* architecturally. **Threshold test — generate a concept topic only if you can write at least two sentences of explanatory prose that (a) are grounded in the source and (b) are not simply a paraphrase of a step, a prerequisite, or a parameter definition.** If the only "why" content is a restatement of a procedural step (e.g., "you must enable X before the CLI works" — already a prerequisite), that does **not** meet the threshold: skip the concept topic and flag the gap instead.
- **Reference** is applicable when the source contains lookup-style facts: parameters, types, valid values, CLI signatures, return codes, or configuration schemas.

Rules for the decision:
- A single source can support **multiple** types. If more than one applies, generate a separate topic for each applicable type.
- Generate **only** the types the content actually supports — do not force a type that isn't grounded in the source. Apply the concept threshold test above strictly and consistently: the same source should always yield the same set of topics.
- When a type does **not** meet its threshold, do not generate a partial or padded topic. Instead emit a `<!-- TOPIC NOT GENERATED: <type> -->` marker followed by a `<!-- MISSING_ELEMENT: ... -->` comment listing the specific content that would be required to author it.
- If the source supports **no** documentation topic type (e.g., pure banter with no technical substance), do not fabricate one. Emit a short HTML comment explaining why no topic could be generated, and stop.
- State your detection outcome briefly to the user (which types were detected, which were skipped, and why).

Then, for **each** detected topic type, run Phases 1–3 below and **write each topic to a separate HTML file** in `docs-as-code-generator-workspace/output/` using the Write tool. Use the naming convention above. Do not display HTML in the chat — only report the filenames and file paths created.

### Phase 1: Parse and Extract
1. Read the `.txt` file specified by the user from the working directory
2. Identify and isolate procedural intent (steps, prerequisites, configuration, validation)
3. Filter out all conversational noise: timestamps, usernames, tangents, failed attempts, timezone discussions, or banter
4. Map extracted content to each documentation structure detected in Phase 0:
   - **Task topics:** Prerequisites, step-by-step procedures, expected results, troubleshooting
   - **Concept topics:** Introduction, key concepts, relationships, examples
   - **Reference topics:** Structure, parameters, return values, examples

### Phase 2: Style Validation (MSTP)
1. Generate initial semantic HTML5 from extracted content following the output format specification
2. Invoke the `/microsoft-docs` skill to validate the generated HTML against Microsoft Manual of Style (MSTP) guidelines:
   - Sentence case for titles and headings (only first word and proper nouns capitalized)
   - Active voice enforcement (rewrite passive constructions)
   - Second-person perspective ("you" instead of "the user")
   - Imperative verb forms for procedures
   - Consistent terminology
   - Proper capitalization and punctuation
3. Review the style validation results from `/microsoft-docs`:
   - If violations found: either flag them with HTML comments (`<!-- STYLE_VIOLATION: ... -->`) or re-process the content for corrections
   - If compliant: proceed to Phase 3
4. **Do not output final HTML until MSTP validation is complete and all violations are resolved or flagged**

### Phase 3: Anti-Hallucination Protocol
Before finalizing output, verify that all procedural elements are grounded in the source log:
- **For Task topics:** Confirm presence of title, introduction, prerequisites, at least 3 steps, expected results, and troubleshooting
- **For Concept topics:** Confirm presence of introduction, at least 2 key concepts, and examples
- **For Reference topics:** Confirm presence of structure definition and parameter documentation

If any critical element is **missing from the source log**, insert an HTML comment flagging it:
```html
<!-- MISSING_ELEMENT: Expected Results section not found in source log. Manual verification required. -->
```

Do **not** invent missing steps, parameters, or validation results.

### Phase 4: HTML Output Format (Applied in Phase 2)
When generating semantic HTML5 in Phase 2, follow these conventions:
- Use `<h1>` for the main title (usually derived from task name) — apply sentence case per MSTP
- Use `<h3>` for major sections (Prerequisites, Steps, Expected Results, Troubleshooting, Concepts, Parameters)
- Use `<ol>` for numbered step sequences in Task topics
- Use `<ul>` for non-sequential lists
- Wrap code snippets in `<code>` (inline) or `<pre>` (blocks); preserve formatting
- Wrap configuration file paths and filenames in `<code>`
- Include introductory `<p>` explaining the goal before steps begin
- Do not include `<html>`, `<head>`, `<body>`, or `<DOCTYPE>` tags — output semantic fragments only

### Phase 5: Write Files and Report

After generating all topics:

1. **Construct the output path**: `docs-as-code-generator-workspace/output/<source-filename-without-extension>/`
   - Example: For `resources/v10_12_rate_limit_chat.txt`, output goes to `docs-as-code-generator-workspace/output/v10_12_rate_limit_chat/`
2. **Write each topic** to its own HTML file in this directory using the Write tool with the naming convention:
   - `task_<topic-name>.html` for task topics
   - `concept_<topic-name>.html` for concept topics
   - `reference_<topic-name>.html` for reference topics
3. **Do NOT display the full HTML in the chat.** Instead, return a summary listing:
   - Which topic types were detected
   - The filenames and full paths of all generated files
   - Any flagged issues or missing elements (from HTML comments inside the files)

Example summary output:
```
✓ Analysis complete

Detected topic types: task, reference

Generated files:
- docs-as-code-generator-workspace/output/v10_12_rate_limit_chat/task_configure-custom-api-rate-limits.html
- docs-as-code-generator-workspace/output/v10_12_rate_limit_chat/reference_api-rate-limit-configuration.html

Files are ready for import into your documentation build system.

Flagged issues:
- concept topic not generated: missing conceptual content (definition, design rationale)
```

## Example Output Structure (Task Topic)

```html
<h1>Configure Custom API Rate Limits</h1>

<p>Learn how to set up custom rate limits for your API using the configuration file and CLI commands.</p>

<h3>Prerequisites</h3>
<ul>
<li>Access to the global configuration file at <code>/etc/scanner/config.yml</code></li>
<li>Daemon must be stopped before applying changes</li>
<li>Admin privileges required</li>
</ul>

<h3>Steps</h3>
<ol>
<li>Open the global configuration file: <code>/etc/scanner/config.yml</code></li>
<li>Add the rate limit configuration block...</li>
<li>Restart the daemon...</li>
<li>Validate the configuration...</li>
</ol>

<h3>Expected Results</h3>
<p>When the rate limit is exceeded, the API returns a <code>429 Too Many Requests</code> response.</p>

<h3>Troubleshooting</h3>
<p>If you receive a <code>403 Forbidden</code> error...</p>
```

## Critical Rules

1. **No hallucination:** Every step, parameter, error code, and CLI command must be verifiable in the source log. If uncertain, flag with an HTML comment.
2. **Style enforcement is mandatory:** Always validate against MSTP before outputting HTML. Rewrite passive voice to active; use second person; use imperative verbs in procedures.
3. **Semantic HTML only:** No boilerplate `<html>`, `<head>`, `<body>`, or `<DOCTYPE>` tags. Outputs must be importable into structured authoring systems.
4. **Code formatting:** All CLI commands, file paths, and configuration snippets must be wrapped in `<code>` or `<pre>` tags with preserved formatting.
5. **Comments for gaps:** Missing procedural elements (prerequisites, steps, expected results, troubleshooting) must be explicitly flagged with HTML comments. Do not skip sections.
6. **Auto-detect topic types:** Do not ask the user which topic type to produce. Analyze the source and generate every topic type it supports (task, concept, and/or reference) — all of them, a subset, or none. Never force a topic type the source cannot ground. Only restrict to a single type when the user explicitly requests it.
7. **Write files, do not display HTML:** Use the Write tool to create HTML files in `docs-as-code-generator-workspace/output/`. Do NOT paste the full HTML into the chat. Report only the summary: which topic types were detected, which files were created, and any flagged issues.

## Style and Voice (MSTP Compliance)

The skill enforces:
- **Active voice:** "You configure the file" (not "The file is configured by you")
- **Second person:** "You open..." (not "The user opens..." or "One opens...")
- **Imperative procedures:** "Click the button" (not "You should click the button")
- **Consistent terminology:** Use the same term for the same concept throughout (query MCP if unsure)
- **Proper capitalization:** Feature names, product names, menu items must match official documentation style

## Handling Variations

The skill adapts to different documentation structures by detecting them automatically from the source content (see Phase 0):

- **Task topics:** Extract procedural steps, prerequisites, results, troubleshooting
- **Concept topics:** Extract explanatory content, relationships, key ideas, examples
- **Reference topics:** Extract structure, parameters, properties, return values, error codes

Behavior:
- If the source supports several types, generate a topic for each one.
- If the source supports only one type, generate just that one.
- If the source supports none, emit an HTML comment explaining why and generate nothing — do not force an unsupported structure.
- If the user explicitly names a type, restrict the output to that type only.
