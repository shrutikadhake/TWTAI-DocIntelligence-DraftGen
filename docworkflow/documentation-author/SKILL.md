---
name: documentation-author
description: |
  Converts structured transcript JSON into customer-facing technical documentation. Use this skill whenever you have normalized transcript data (from transcript-normalizer or similar sources) and need to generate polished markdown documentation for end users. Produces clear, task-oriented guides with actionable steps, balanced technical depth for both experienced and novice users, and comprehensive expected results including validation and troubleshooting. Perfect for creating user guides, tutorials, and how-to documentation from demo recordings or structured procedural data.
compatibility: |
  - Input: JSON with topic_title, goal, prerequisites, technical_facts, tasks (each with steps)
  - Output: Markdown (.md) documentation
  - Audience: End users (mixed technical skill levels)
---

# Documentation Author

Converts structured transcript data into customer-facing markdown documentation that balances technical accuracy with accessibility for all user skill levels.

## Input Format

The skill expects JSON with this structure (typically from transcript-normalizer):

```json
{
  "topic_title": "Using Microsoft 365 Copilot Chat to Learn Basic HTML",
  "goal": "Learn how to use Copilot Chat to ask questions about HTML",
  "prerequisites": [
    "Access to Microsoft 365 Copilot",
    "Familiarity with chat interfaces"
  ],
  "technical_facts": [
    "HTML stands for HyperText Markup Language",
    "The h1 element defines a top-level heading"
  ],
  "tasks": [
    {
      "task_name": "Open Copilot and Ask About HTML Basics",
      "description": "Start by opening Microsoft 365 Copilot and asking fundamental questions",
      "steps": [
        {
          "step_number": 1,
          "action": "Open Microsoft 365 Copilot",
          "details": "Launch the Copilot application",
          "expected_outcome": "Copilot interface is open and ready"
        }
      ]
    }
  ]
}
```

## Output Format

The skill produces markdown documentation with this structure:

```markdown
# [Title]

## Introduction
[Goal with context, what user will accomplish, why it matters]

## Prerequisites
- [Prerequisite 1]
- [Prerequisite 2]
> Note: [Any important prerequisites context]

## Procedure

### Task 1: [Task Name]
[Task description with purpose]

**Step 1: [Action]**
Details about what to do and any options.

Expected result: You should see X or Y happens.

**Step 2: [Action]**
...continue...

### Task 2: [Task Name]
[Continue with remaining tasks]

## Expected Results

### What You Should See
[Description of successful completion indicators]

### Validation
- [ ] Check that X is correct
- [ ] Verify that Y shows up
- [ ] Confirm that Z is working

### Troubleshooting
**Issue: X isn't showing up**
- Try Y
- Check Z setting
- Restart and retry

**Issue: Getting an error message**
- This usually means...
- Solution: ...
```

## Writing Guidelines

### Audience & Tone
- **Address the reader as "You"** — Use direct language: "You can...", "You'll see...", "You should..."
- **Balance technical and everyday language** — Explain technical terms briefly when first introduced
  - Example: "Click the API Configuration section (this is where you add your credentials)"
- **Assume mixed skill levels** — Don't assume prior knowledge, but don't over-explain either
- **Focus on tasks, not features** — Emphasize what the user accomplishes, not product capabilities

### Step Writing
- **Each step = one action** — Break complex tasks into discrete steps
- **Action as imperative** — "Click X", "Open Y", "Type Z" (not "You can click X if you want")
- **Details field** — Provide context: options available, examples, edge cases, or clarifications
- **Expected outcome** — Always state what success looks like. Use present tense:
  - ✅ "You should see the API Connected message in green"
  - ❌ "The connection will be validated" (unclear what to look for)

### Technical Facts → Callouts
- Weave technical facts into the introduction, prerequisites, or step details
- Use blockquotes or notes for important technical context:
  - `> **Note:** Client secrets must never be shared or committed to code`
  - `> **Technical detail:** OAuth 2.0 scopes define what permissions your app requests`

### Validation & Troubleshooting
- **Validation** — Provide a checklist of success criteria the user can verify themselves
- **Troubleshooting** — Anticipate common failure modes and provide specific solutions
  - Problem → Why it happens → How to fix it
  - Example: "Getting 'Connection Refused'? This usually means the service isn't running. Restart the application and try again."

## When to Use This Skill

- You have structured JSON from transcript-normalizer or similar structured documentation data
- You need to generate end-user documentation from demo recordings or procedural transcripts
- You want clear, task-oriented guides that balance technical accuracy with accessibility
- You're creating tutorials, how-to guides, or instructional documentation
- The audience is end users with varying technical expertise

## When NOT to Use This Skill

- Input is not structured JSON (preprocess first)
- Documentation is for internal technical staff or developers (use different tone)
- Content is not procedural/task-based (use general writing instead)
- You need to transcribe or normalize transcripts first (use transcript-normalizer skill first)

## How to Use This Skill

**Provide the JSON file path:**
```
Convert this structured transcript data to documentation: /path/to/normalized-transcript.json
```

**Or embed the JSON directly:**
```
Generate documentation from this JSON:
{
  "topic_title": "...",
  "goal": "...",
  ...
}
```

The skill will:
1. Extract the topic title as the main heading
2. Transform the goal into an engaging introduction
3. List prerequisites with context
4. Create a procedure section with all tasks and steps
5. Build validation, results, and troubleshooting sections
6. Generate markdown ready to save or publish

## Example Workflow

**Input:** M365CopilotDemoTranscript.json (normalized transcript)
**Output:** M365CopilotDemoTranscript.md (customer documentation)

The resulting markdown is ready to be saved, converted to other formats (HTML, PDF, DOCX), or published to documentation sites.
