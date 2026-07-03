---
name: doc-intelligence-generator
description: |
  Generates structured technical documentation from source content and provides automated pre-review assessment.
  
  Use this skill whenever a user needs to: convert Confluence wiki pages or JSON files into properly structured HTML documentation (Concept, Task, or Reference topics per DITA standards); generate API or configuration documentation with property/parameter tables; or perform automated quality checks against Microsoft and IBM style guides combined with DITA best practices.
  
  The skill handles both source formats automatically, auto-detects the appropriate documentation type (Concept/Task/Reference), generates HTML output using standard templates, and produces a detailed pre-review report with style violations, suggested improvements, and a compliance score. Perfect for technical writers needing rapid first-pass documentation drafts with built-in quality assessment.
compatibility: Atlassian MCP (Confluence access), Python 3.8+, HTML/CSS support
---

# Document Intelligence Generator

This skill converts multiple source formats (Confluence wiki, JSON/API definitions) into structured technical documentation following DITA principles and industry-standard templates, then validates the output against a comprehensive review framework combining Microsoft Writing Style Guide, IBM Standards, and technical writing best practices.

## Overview

The skill processes source content through this pipeline:

1. **Input Detection** — Automatically identifies whether input is Confluence wiki (Markdown/text), JSON (code/API), or allows manual specification
2. **Type Determination** — Auto-detects whether content maps to a Concept (explanatory), Task (procedural), or Reference (structured data) topic, or accepts user override
3. **Documentation Generation** — Applies DITA-compliant HTML templates and generates well-structured output
4. **Pre-Review Assessment** — Evaluates output against 50+ review rules covering grammar, style, structure, clarity, and completeness
5. **Report Generation** — Produces a detailed report with violations, severity levels, specific references, and improvement suggestions

## When to Use

- **Converting Confluence PRDs to docs**: "Take this product requirements wiki page and turn it into a Concept topic with pre-review checks"
- **Documenting APIs and configuration**: "Generate parameter reference documentation from this JSON schema"
- **Rapid documentation drafting**: "Create a first-pass task guide from this wiki content and tell me what needs fixing"
- **Multi-format source handling**: "I have both a Confluence page AND a JSON config file — generate docs from both and check them"
- **Quality assurance**: "Generate the docs and give me a detailed pre-review report on style, clarity, and completeness"

## How to Use

### Providing Input

Provide a **Confluence wiki page URL** with attached JSON file:

```
Input: Confluence page URL (e.g., https://your-org.atlassian.net/wiki/spaces/DOCS/pages/12345/Feature-Name)
Attachment: JSON file attached to the Confluence page (API specs, configuration schemas, code structure)
```

The skill will:
1. Fetch the Confluence page via **Atlassian MCP**
2. Parse the Confluence Markup content (PRD, requirements, feature description)
3. Extract and download the JSON attachment
4. Process both sources together into structured documentation

**Prerequisites**: Atlassian MCP must be configured with access to your Confluence workspace.

### Specifying Document Type (Optional)

The skill auto-detects whether content should become a **Concept** (explanatory), **Task** (procedural), or **Reference** (structured reference) topic. You can optionally specify:

```
Type: Concept  — explanatory docs, background, how things work
Type: Task     — step-by-step procedures, how to do something
Type: Reference — API docs, parameters, configuration options
```

If not specified, the skill analyzes content structure to determine the best fit.

### Expected Outputs

The skill generates:

1. **HTML Documentation** — A ready-to-use HTML file following DITA conventions:
   - Concept topics: introduction, purpose, when to use, key concepts
   - Task topics: overview, prerequisites, steps, post-task information
   - Reference topics: structured properties/parameters with descriptions, types, defaults

2. **Pre-Review Report** — A detailed assessment including:
   - **Compliance Score**: Overall adherence to standards (0-100%)
   - **Violations List**: Categorized by severity (Critical, Warning, Info)
   - **Specific References**: Line/section numbers where violations occur
   - **Suggested Fixes**: Actionable recommendations for each violation
   - **Standards Applied**: Microsoft Writing Style Guide, IBM Standards, DITA best practices

### Review Framework

The skill validates output against rules covering:

- **Grammar & Mechanics**: Punctuation, capitalization, contractions, active voice
- **Heading & Structure**: Proper hierarchy, consistent formatting, DITA compliance
- **Terminology**: Consistency, definitions, acronyms defined on first use
- **Style**: Tone, clarity, conciseness, audience appropriateness
- **Readability**: Sentence length, paragraph structure, visual hierarchy
- **Completeness**: Required sections present, examples provided, cross-references
- **Formatting**: Lists, tables, code blocks, hyperlinks formatted correctly
- **Accessibility**: Alternative text, color contrast, screen-reader friendly

## Examples

### Example 1: Confluence PRD (with JSON attachment) to Concept + Reference

**Input**: 
- Confluence URL: `https://your-org.atlassian.net/wiki/spaces/PRODUCT/pages/54321/OAuth2-Integration-PRD`
- Attached JSON file: `oauth2-config.json` containing API configuration

**Confluence Content** (Confluence Markup):
```
h1. OAuth2 Integration Feature

h2. Overview
Users need secure, industry-standard authentication instead of legacy token system.

h2. Purpose
Implement OAuth2 flow with refresh tokens and support for multiple identity providers.

h2. Key Benefits
* Enhanced security with industry-standard protocols
* User choice of identity provider
* SSO capability across applications
```

**Automatically Detected Types**: 
- Wiki content → Concept topic
- JSON attachment → Reference topic

**Output**: 
- HTML Concept topic: Introduction, Purpose, Key Concepts, Benefits, When to Use
- HTML Reference topic: API parameters table from JSON config
- Pre-review report for both documents (compliance score, style violations, suggestions)

---

### Example 2: Confluence API Documentation (with config JSON)

**Input**:
- Confluence URL: `https://your-org.atlassian.net/wiki/spaces/API/pages/67890/Search-API-Specification`
- Attached JSON file: `search-api.json` with endpoint schemas and parameters

**Confluence Content** (procedural with steps):
```
h1. Setting Up Advanced Search API

h2. Prerequisites
* Admin access to the platform
* Node.js 14+ installed

h2. Configuration Steps
# Install the search service package
# Configure semantic search engine
# Set up ML model integration
# Enable and test the feature

h2. Verification
Test your setup by running: curl https://api.example.com/search
```

**Automatically Detected Type**: Task (procedural content detected)

**Output**:
- HTML Task topic with proper prerequisites, numbered steps, verification section
- HTML Reference topic for API parameters
- Pre-review report checking procedural clarity and completeness

---

## Review Rules Applied

The skill uses a comprehensive rule set (see `references/review-rules.json`) including:

| Category | Sample Rules |
|----------|--------------|
| **Grammar** | Use active voice, avoid contractions in formal docs, consistent punctuation |
| **Structure** | Proper heading hierarchy (H1 → H2 → H3), consistent section order |
| **Terminology** | Define acronyms on first use, use consistent term forms |
| **Clarity** | Sentences under 25 words, paragraphs under 5 sentences |
| **Completeness** | All required sections present for doc type, examples provided |
| **Formatting** | Proper list formatting, code blocks with language markers |

See `references/review-rules.json` for the complete ruleset.

---

## Bundled Resources

- **`scripts/doc-generator.py`** — Main processing pipeline (input detection, type determination, HTML generation, review assessment)
- **`references/review-rules.json`** — Complete set of 50+ review rules with severity levels and examples
- **`references/templates.html`** — HTML templates for Concept, Task, Reference topics (DITA-compliant)
- **`references/style-guide-rules.md`** — Summary of Microsoft, IBM, and DITA style standards applied

---

## Enhancement Features (Iteration 2+)

### Smart Hyperlink Generation
- Automatically detects cross-references in "Related Topics" sections
- Generates navigation links between related documents
- Maintains reference integrity across documentation sets
- Supports both internal wiki links and external URL references

### Screenshot Placeholder System (Task Topics)
- Automatically identifies UI interaction steps
- Inserts screenshot placeholders with descriptive captions
- Includes alt text for accessibility
- Provides guidance on where screenshots should be inserted
- Example: "Click the button" → image placeholder + "Click the **Save** button" caption

### Automatic Error Documentation (API References)
- Extracts common HTTP error codes from API context
- Generates error response tables with status codes
- Documents error message structures
- Includes troubleshooting guidance for common errors
- Supports custom error codes specific to your API

### Glossary Extraction (All Topics)
- Automatically identifies technical terms and jargon
- Extracts definitions from context
- Generates glossary section for complex topics
- Marks first use of terms for reader reference
- Creates cross-references to glossary items

### JSON Schema in Reference Topics
- Automatically includes full JSON schema/specification in Reference documents
- Displays JSON in professional code block with dark background (#1e1e1e)
- Makes documentation self-contained and complete
- Easy for developers to copy and reference JSON directly
- Positioned after parameters table for logical flow
- Supports any valid JSON content (API schemas, configurations, definitions)
- Monospace font with proper syntax highlighting readiness
- Scroll support for large JSON files

## Notes

- The skill performs a **first-pass** pre-review; it does not replace formal human review
- **Technical accuracy** is not validated — the skill checks documentation quality, not product feature validity
- **SME review** is still required for content verification
- For Confluence input, if a URL is provided, the skill attempts to fetch the page content; if paste is provided, it processes directly
- The pre-review report flags issues but does not auto-correct output—all suggestions are recommendations
- Screenshot placeholders indicate where images should be inserted; actual image generation/capture is handled separately
- Hyperlinks generated for Related Topics; full URL mapping configured in documentation map file

