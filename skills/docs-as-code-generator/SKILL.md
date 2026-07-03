---
name: docs-as-code-generator
description: Convert raw technical communication (chat logs, transcripts, notes) into clean, structured HTML documentation. Use this skill whenever you need to transform noisy developer communication, meeting transcripts, or raw technical notes into semantic HTML5 documents (Task topics, conceptual guides, reference docs). The skill automatically extracts procedural intent, filters noise, validates against Microsoft Manual of Style using the Microsoft Learn MCP server, and flags missing content to prevent hallucination. Invoke with the source file name and desired documentation structure type. Essential for Docs-as-Code workflows where team members need to convert unstructured communication into build-ready documentation.
compatibility: Requires access to local Git repository workspace and active Microsoft Learn MCP server connection.
---

## Overview

This skill transforms messy, unstructured technical communication into clean, structured HTML5 documentation that conforms to the Microsoft Manual of Style (MSTP). It is designed for technical writers working in Docs-as-Code environments who receive developer chat logs, meeting transcripts, or raw notes and need to extract procedural intent while filtering noise.

The workflow:
1. Reads the specified `.txt` log file from the local workspace
2. Intelligently extracts procedural content, prerequisites, and validation steps while filtering conversational noise
3. Generates semantic HTML5 fragments (no `<html>`, `<head>`, or `<body>` tags)
4. Validates style compliance using the Microsoft Learn MCP server for MSTP enforcement
5. Flags missing procedural elements with HTML comments to prevent hallucination
6. Outputs build-ready HTML ready for import into structured authoring systems

## Input Requirements

- **Source file:** A `.txt` file containing raw technical communication (Slack export, Teams transcript, meeting notes, etc.) located in your working directory
- **MCP connection:** Active Microsoft Learn MCP server connection (Claude will call `microsoft_docs_search` and `microsoft_docs_fetch` to retrieve MSTP guidance as needed)
- **Documentation type:** Specify the desired output structure: `task` (procedural steps), `concept` (explanatory content), or `reference` (technical reference)

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
2. The desired documentation structure type (`task`, `concept`, or `reference`)
3. Optional: Specific output constraints (e.g., "Task topic with prerequisites, steps, and troubleshooting")

**Example prompt:**
> "Convert `v10_12_rate_limit_chat.txt` into a Task topic HTML. Extract the procedural steps for configuring custom API rate limits, include prerequisites and expected results, and flag any missing validation steps."

## Execution Instructions

Process the source file and any requested parameters provided here: $ARGUMENTS

## Workflow

### Phase 1: Parse and Extract
1. Read the `.txt` file specified in $ARGUMENTS from the working directory
2. Identify and isolate procedural intent (steps, prerequisites, configuration, validation)
3. Filter out all conversational noise: timestamps, usernames, tangents, failed attempts, timezone discussions, or banter
4. Map extracted content to the appropriate documentation structure:
   - **Task topics:** Prerequisites, step-by-step procedures, expected results, troubleshooting
   - **Concept topics:** Introduction, key concepts, relationships, examples
   - **Reference topics:** Structure, parameters, return values, examples

### Phase 2: Style Validation (MSTP)
1. Query the Microsoft Learn MCP server for MSTP guidance on:
   - Active voice enforcement (rewrite passive constructions)
   - Second-person perspective ("you" instead of "the user")
   - Imperative verb forms for procedures
   - Consistent terminology
   - Proper capitalization and punctuation
2. Apply corrections to align extracted content with Microsoft style before generating HTML
3. **Do not output HTML until MSTP validation is complete**

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

### Phase 4: Generate HTML
Produce clean semantic HTML5 fragments following these conventions:
- Use `<h1>` for the main title (usually derived from task name)
- Use `<h3>` for major sections (Prerequisites, Steps, Expected Results, Troubleshooting, Concepts, Parameters)
- Use `<ol>` for numbered step sequences in Task topics
- Use `<ul>` for non-sequential lists
- Wrap code snippets in `<code>` (inline) or `<pre>` (blocks); preserve formatting
- Wrap configuration file paths and filenames in `<code>`
- Include introductory `<p>` explaining the goal before steps begin

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

## Style and Voice (MSTP Compliance)

The skill enforces:
- **Active voice:** "You configure the file" (not "The file is configured by you")
- **Second person:** "You open..." (not "The user opens..." or "One opens...")
- **Imperative procedures:** "Click the button" (not "You should click the button")
- **Consistent terminology:** Use the same term for the same concept throughout (query MCP if unsure)
- **Proper capitalization:** Feature names, product names, menu items must match official documentation style

## Handling Variations

The skill adapts to different documentation structures based on the prompt:

- **Task topics:** Extract procedural steps, prerequisites, results, troubleshooting
- **Concept topics:** Extract explanatory content, relationships, key ideas, examples
- **Reference topics:** Extract structure, parameters, properties, return values, error codes

Always ask for clarification if the source material does not align with the requested output structure.
