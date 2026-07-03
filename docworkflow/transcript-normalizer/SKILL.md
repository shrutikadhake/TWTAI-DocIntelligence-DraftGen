---
name: transcript-normalizer
description: |
  Converts software product demonstration transcripts from VTT format into structured JSON documentation. Use this skill whenever you have raw demo transcripts that need to become technical documentation with clear goals, prerequisites, tasks, and steps. Handles real-world transcript messiness: removes timestamps and filler words, consolidates fragmented explanations, filters out side conversations, extracts prerequisites and expected outcomes, and identifies procedures and technical facts. Ideal for turning unedited demo recordings into clean, actionable technical content.
compatibility: |
  - Input: VTT (WebVTT) format transcripts
  - Output: JSON with structured documentation fields
  - Processing: Text cleanup, NLP-based extraction, procedural identification
---

# Transcript Normalizer for Software Demos

Use this skill to transform raw software demonstration transcripts into structured technical documentation JSON.

## How to Use This Skill

When you want to normalize a transcript, provide the file path to your VTT file in one of these ways:

**Option 1: Direct file reference**
```
Normalize this transcript: /path/to/your/transcript.vtt
```

**Option 2: Explicit instruction with path**
```
Use the transcript-normalizer skill on this file: C:\Users\name\documents\demo_recording.vtt
```

**Option 3: In a task description**
```
Convert the software demo transcript at /home/user/transcripts/product_demo_2024.vtt into structured documentation JSON
```

The skill will:
1. Read the VTT file from the provided path
2. Parse the transcript content
3. Clean up timestamps, filler words, false starts, and side conversations
4. Extract topics, goals, prerequisites, technical facts, and procedures
5. Generate structured JSON optimized for documentation
6. Return the JSON output for you to save or use

## Input Format

The skill expects VTT (WebVTT) format transcripts. Example:

```
WEBVTT

00:00:05.000 --> 00:00:10.000
Speaker 1: Okay so uh, today we're gonna walk through how to set up the new dashboard feature

00:00:10.500 --> 00:00:15.000
Speaker 2: Yeah, I'm excited about this, it's pretty cool
Speaker 1: So, um, first you need to have API access...
```

## Output JSON Structure

The skill produces JSON with these fields:

```json
{
  "topic_title": "string — the main topic/feature being demonstrated",
  "goal": "string — what the user will accomplish after following this",
  "prerequisites": [
    "list of things needed before starting (API keys, accounts, permissions, software versions, etc)"
  ],
  "technical_facts": [
    "key technical details, constraints, limitations mentioned during demo"
  ],
  "tasks": [
    {
      "task_name": "high-level action the user performs",
      "description": "brief description of why/when to do this task",
      "steps": [
        {
          "step_number": 1,
          "action": "specific action to take (UI click, command to run, etc)",
          "details": "additional context or options mentioned",
          "expected_outcome": "what should happen after this step"
        }
      ]
    }
  ]
}
```

## Processing Rules

### Text Cleanup
- **Timestamps**: Remove all VTT timestamps (00:00:05.000 format)
- **Speaker labels**: Clean up (keep context if helpful, remove if just "Speaker 1")
- **Filler words**: Remove "um", "uh", "like", "you know", "basically", "so basically", "I mean", etc.
- **False starts**: Remove incomplete thoughts that are immediately corrected
  - Example: "You'll uh, I mean you should, no wait, you definitely need to set up..." → "You need to set up..."
- **Side conversations**: Remove back-and-forth acknowledgments not related to the demo content
  - Keep: "That's an important security constraint"
  - Remove: "Yeah for sure, totally agree, right right"

### Content Organization
- **Consolidate fragmented explanations**: When one idea is explained across multiple speaker turns or false starts, merge into a single coherent explanation
- **Identify task boundaries**: Look for phrases like "Next, let's...", "Now we'll...", "The first thing you do is..."—these often demarcate task/step boundaries
- **Extract prerequisites**: Look for "You need X first", "Make sure you have Y", "This assumes Z" language
- **Extract expected outcomes**: Look for "Now you should see...", "At this point you'll have...", "The result is..."

### Handling Edge Cases
- **If topic/goal unclear**: Infer from context (demo feature name, what problems it solves)
- **Multiple speakers**: Treat as one coherent speaker (consolidate into single narrative)
- **Technical jargon**: Keep all technical terms intact
- **Code snippets or commands**: Preserve exactly as stated
- **Timestamps in content**: If the demo mentions "at the 5-minute mark" or similar, convert to step context

## When to Use This Skill

- You have a VTT transcript from a product demo/webinar/tutorial recording
- You need to turn that transcript into documentation
- The source material is conversational and unedited (contains natural speech patterns, false starts, interruptions)
- You want clean, structured JSON suitable for automated documentation generation, training materials, or knowledge bases

## Practical Example

**Your request:**
```
Normalize this transcript: C:\Users\username\Downloads\api_demo.vtt
```

**What happens:**
1. Skill reads the VTT file from that path
2. Extracts content like:
   ```
   00:00:15.000 --> 00:00:22.000
   Speaker: So uh, today we're gonna show you, um, how to set up the API. 
   You know, it's basically really important for, like, integration.
   ```
3. Cleans and normalizes to:
   ```json
   {
     "topic_title": "API Setup",
     "goal": "Learn how to set up the API for integration",
     "prerequisites": ["Developer account", "API credentials"],
     "tasks": [...]
   }
   ```

**Output:** Clean, structured JSON ready for documentation systems, training portals, or knowledge bases.

## When to Use This Skill

- You have a VTT transcript from a product demo/webinar/tutorial recording
- You need to turn that transcript into documentation
- The source material is conversational and unedited (contains natural speech patterns, false starts, interruptions)
- You want clean, structured JSON suitable for automated documentation generation, training materials, or knowledge bases
- You want to extract key information (prerequisites, steps, technical facts) from raw demo content

## When NOT to Use This Skill

- Input is already structured (already JSON, markdown, etc.)
- You need to transcribe audio yourself (use a transcription service first)
- Input is not software/product related (this is optimized for demos, not general conversations)
- Your transcript is in a different format (use a format converter first if needed)
