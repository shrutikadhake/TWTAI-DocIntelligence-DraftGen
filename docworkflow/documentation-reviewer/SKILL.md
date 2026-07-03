---
name: documentation-reviewer
description: |
  Reviews markdown documentation against Microsoft writing standards and quality guidelines. Use this skill to quality-assure technical documentation created by documentation-author or other sources. Evaluates clarity, conciseness, active voice, accessibility, heading hierarchy, task orientation, terminology consistency, and Microsoft writing compliance. Produces detailed review reports in JSON and HTML formats with findings, severity levels, and recommended fixes. Use whenever you need to ensure documentation meets professional Microsoft-style standards or before publishing technical guides.
compatibility: |
  - Input: Markdown file paths (.md files)
  - Output: review.json (structured findings) + review.html (human-readable report)
  - Reference: Microsoft Learn API (learn.microsoft.com/api/mcp) or Microsoft writing guidelines
---

# Documentation Reviewer

Reviews markdown documentation against Microsoft writing standards and produces detailed quality assurance reports with findings and recommendations.

## Input Format

The skill expects a markdown file path:

```
Review this documentation: /path/to/document.md
```

The markdown file should be technical documentation (typically from documentation-author skill) with:
- Title (# heading)
- Introduction section
- Prerequisites
- Procedure with tasks and steps
- Expected results or conclusion

## Review Categories

The skill evaluates documentation against 8 key categories:

### 1. **Clarity**
Content is clear and easy to understand. Sentences avoid jargon without explanation. Concepts are explained before use.
- ✅ Pass: Ideas are clearly expressed, technical terms are defined, audience is obvious
- ❌ Fail: Ambiguous language, undefined jargon, unclear references

### 2. **Conciseness**
Content is concise without sacrificing clarity. No redundancy or unnecessary words.
- ✅ Pass: Sentences are tight, no repeated explanations, removes filler
- ❌ Fail: Wordy explanations, redundant information, overly long sentences

### 3. **Active Voice**
Writing uses active voice ("You click the button") rather than passive ("The button should be clicked").
- ✅ Pass: Sentences primarily use active voice with clear subjects and actions
- ❌ Fail: Excessive passive voice, unclear who performs actions

### 4. **Accessibility**
Content is accessible to users with varying abilities and technical backgrounds. Includes alternative descriptions, clear formatting, logical structure.
- ✅ Pass: Headings are descriptive, lists are used appropriately, steps are numbered, plain language used
- ❌ Fail: Poor formatting, unclear hierarchy, assumes prior knowledge, missing descriptions

### 5. **Heading Hierarchy**
Headings follow a logical hierarchy. H1 is the title, H2 sections flow logically, no levels skipped (no H2 to H4 jumps).
- ✅ Pass: Hierarchy is logical and consistent, levels don't skip
- ❌ Fail: Inconsistent hierarchy, levels skipped, unclear structure

### 6. **Task Orientation**
Content is organized around user tasks and outcomes. Each procedure includes what user will accomplish.
- ✅ Pass: Tasks are clearly defined, outcomes are stated, steps are action-oriented
- ❌ Fail: Feature-focused rather than task-focused, missing context on why steps matter

### 7. **Terminology Consistency**
Technical terms are used consistently throughout. Same concept always uses same term.
- ✅ Pass: Terms are consistent, synonyms are avoided for the same concept
- ❌ Fail: Same concept called different names, inconsistent terminology

### 8. **Microsoft Writing Guidance Compliance**
Content follows Microsoft's official writing style guide standards: direct address ("You"), active voice, task-focused, clear formatting, professional tone without marketing.
- ✅ Pass: Uses "You" addressing, action-oriented, professional tone, follows Microsoft patterns
- ❌ Fail: Marketing language, unclear audience, deviates from Microsoft style

## Output Format: review.json

```json
{
  "document_info": {
    "title": "Document title extracted from markdown",
    "file_path": "/path/to/document.md",
    "review_timestamp": "2026-07-03T12:00:00Z"
  },
  "overall_score": 87.5,
  "category_results": {
    "clarity": {
      "passed": true,
      "score": 100
    },
    "conciseness": {
      "passed": false,
      "score": 75,
      "issues": 2
    },
    "active_voice": {
      "passed": true,
      "score": 95
    },
    "accessibility": {
      "passed": true,
      "score": 90
    },
    "heading_hierarchy": {
      "passed": true,
      "score": 100
    },
    "task_orientation": {
      "passed": true,
      "score": 85
    },
    "terminology_consistency": {
      "passed": false,
      "score": 70
    },
    "microsoft_compliance": {
      "passed": true,
      "score": 80
    }
  },
  "findings": [
    {
      "id": "CLR-001",
      "category": "clarity",
      "severity": "info",
      "line_number": 45,
      "issue": "Technical term 'OAuth 2.0' used without explanation on first mention",
      "context": "...the OAuth 2.0 security protocol...",
      "recommendation": "Add: 'OAuth 2.0 is a widely-used security standard that allows safe access sharing'",
      "suggested_fix": "...the OAuth 2.0 security standard (a widely-used protocol for secure access)..."
    },
    {
      "id": "CON-002",
      "category": "conciseness",
      "severity": "warning",
      "line_number": 78,
      "issue": "Redundant explanation of the same concept",
      "context": "...when you see the green message. That message indicates success...",
      "recommendation": "Remove redundancy: 'when you see the green success message'",
      "suggested_fix": "...when you see the green success message..."
    },
    {
      "id": "TRM-001",
      "category": "terminology_consistency",
      "severity": "warning",
      "line_number": 62,
      "issue": "Inconsistent terminology: 'Copilot' used instead of 'Microsoft 365 Copilot' used elsewhere",
      "context": "...ask Copilot to show...",
      "recommendation": "Use consistent term: 'Microsoft 365 Copilot' throughout",
      "suggested_fix": "...ask Microsoft 365 Copilot to show..."
    }
  ],
  "severity_summary": {
    "critical": 0,
    "warning": 2,
    "info": 1
  }
}
```

## Output Format: review.html

Naming convention: `<topic-title>-review.html`
Example: `learn-basic-html-with-m365-copilot-review.html`

HTML contents:
- **Header**: Document title, review timestamp, overall score (visual gauge)
- **Quick summary**: Pass/fail for each category with scores
- **Findings table**: ID | Category | Severity | Line | Issue | Recommendation
- **Detailed findings**: Expandable sections per category showing context and suggested fixes
- **Severity indicators**: Color-coded (🔴 Critical, 🟡 Warning, 🔵 Info)
- **Export options**: Links to download review.json

## Review Process

1. **Parse the markdown file** — Extract title, headings, content structure
2. **Reference Microsoft guidelines** — Fetch from learn.microsoft.com/api/mcp if available; otherwise use official Microsoft writing guidelines
3. **Evaluate each category** — Apply pass/fail criteria
4. **Identify specific issues** — Find line-by-line problems with context
5. **Calculate scores** — Per-category score (0-100) and overall average
6. **Generate findings** — Create actionable recommendations with suggested fixes
7. **Classify severity** — Mark as Critical (blocks publishing), Warning (should fix), or Info (nice-to-have)
8. **Output JSON and HTML** — Create both review.json and review.html

## Severity Levels

- **🔴 Critical**: Blocks publishing; violates core Microsoft standards or breaks accessibility. Examples: Missing alt text for critical content, major clarity issues that confuse users
- **🟡 Warning**: Should be fixed before publishing; deviates from best practices. Examples: Inconsistent terminology, excessive passive voice, verbose explanations
- **🔵 Info**: Nice-to-have improvements; doesn't block publishing. Examples: Minor wording suggestions, optional clarity enhancements

## When to Use This Skill

- You have markdown documentation and want to ensure it meets professional standards
- You need quality assurance on output from documentation-author skill
- You're preparing documentation for publication and need a review checklist
- You want to verify compliance with Microsoft writing guidelines
- You need detailed feedback on specific writing issues with line numbers and fixes

## When NOT to Use This Skill

- Input is not markdown (convert first)
- You need content creation (use documentation-author instead)
- You need to normalize transcripts (use transcript-normalizer instead)
- Documentation is not technical/procedural in nature

## How to Use This Skill

**Provide the markdown file path:**
```
Review this documentation: C:\path\to\my-document.md
```

**Or with additional context:**
```
Review this markdown file and save the HTML report: /users/docs/guide.md
```

The skill will:
1. Read and parse the markdown file
2. Evaluate against all 8 categories
3. Generate review.json with detailed findings
4. Generate review.html with formatted report
5. Return both files ready for download or integration

## Example Workflow

**Input:** `learn-basic-html-with-m365-copilot.md` (from documentation-author)

**Outputs:**
- `review.json` — Machine-readable findings with scores and recommendations
- `learn-basic-html-with-m365-copilot-review.html` — Human-readable report ready for stakeholder review

**Use cases:**
- Editor reviews findings before approving publication
- Developer uses suggestions to improve documentation
- Team tracks quality metrics across documentation set
- QA verifies compliance before launch
