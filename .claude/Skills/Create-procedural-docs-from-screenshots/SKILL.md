---
name: Create-procedural-docs-from-screenshots
description: |
  Analyze screenshots of desktop, web, and SaaS applications and generate task-based procedural documentation in HTML format following the Microsoft Style Guide. Use this skill whenever you have screenshots of an application workflow and need to produce professional, MS-compliant procedural docs — provide 5–10 numbered screenshots (*1, *2, *3...) and a brief task description (e.g., "document how to create a branch in GitHub"). The skill analyzes the UI, reconstructs the workflow, and produces a formatted HTML document ready for review.
compatibility: |
  - Requires: screenshot files (.png, .jpg, .jpeg, .webp)
  - Requires: Microsoft Learn MCP server (for style guide reference)
  - Output: standalone HTML file
---

## Overview

This skill transforms application screenshots into professional, Microsoft Style Guide–compliant procedural documentation in HTML format. It is designed for technical writers and teams that need to scale documentation production without sacrificing quality or consistency.

**When to use:**
- You have 5–10 screenshots of an application workflow
- You need task-based procedural documentation (steps, prerequisites, results)
- The output must comply with Microsoft Style Guide for technical writing
- You want HTML output suitable for review, editing, or publication

**Workflow:**
1. Provide numbered screenshots (*1, *2, *3...) and a brief task description
2. Skill analyzes the screenshots for UI elements, state changes, and workflow logic
3. Skill generates a markdown preview of the HTML structure
4. You review and approve; skill writes the final HTML file

---

## Input Requirements

### Screenshots
- **Count:** 5–10 typical (variable based on task complexity)
- **Format:** .png, .jpg, .jpeg, .webp
- **Naming:** Filenames must include sequence numbers (*1, *2, *3...) to establish order. If not present, you will be asked to clarify the sequence. And if there are two ways of doing the same thing, screenshot need to be named as *1a and *1b.
- **Content:** Full application windows, showing UI elements, dialogs, toolbars, forms, and state changes clearly

### Task Description
- **Format:** Brief, imperative phrase
- **Example:** "Create a branch in GitHub", "Export a report from Salesforce", "Enable two-factor authentication"
- **Details:** The description frames the goal; screenshots provide the visual evidence of each step

### Optional Metadata
If provided, include in the HTML output:
- Product name and version
- Date generated
- Author
- Review status

If not provided, metadata is omitted.

---

## Analysis Process

### Step 1: Understand Your Inputs

Before analyzing, identify what you have:
- **Screenshots only** → infer task goal from visual content; flag any uncertainty
- **Screenshots + task description** → use description to frame goal; screenshots override conflicting detail
- **Screenshots + conflicting text** → document the conflict; do not silently adopt the text


### Step 2: Analyze Screenshots

Scan each screenshot systematically. Identify and note:
- Page or window title
- Navigation elements (menus, breadcrumbs, tabs, sidebars)
- Toolbars and ribbons
- Buttons and links (exact label text)
- Dialog boxes and modal titles
- Form fields (label and current value if visible)
- Tables, grids, and data views
- Status messages, banners, tooltips, and notifications
- Visible workflow progression (step indicators, wizard panels, progress bars)
- Highlighted, focused, or active UI elements (indicating current action)

**Hard rules:**
- Note only what is clearly visible. Do not infer off-screen elements.
- Do not assume application behavior from prior product knowledge.
- If a UI label is partially obscured, mark it as `[unreadable label]` and add a reviewer note.
- If the same UI state appears in multiple screenshots without visible change, treat as the same step unless there is a reason to distinguish.

**Analyzing Variant Screenshots (A/B, 1a/1b patterns):**

When screenshots are named with variants (e.g., 2A + 2B, 3a + 3b), analyze what differs between them:

1. **Identify the variation type:**
   - **Alternative paths:** Both variants achieve the same outcome but use different UI paths (e.g., one uses a menu, another uses a button). Document as two separate optional approaches.
   - **Progressive refinement:** Variant B shows the same moment as A but with a focused field, highlighted element, or next state. Document as a single step; choose the clearer variant for the figure.
   - **State progression:** Variant A shows the action trigger, Variant B shows the immediate result. Merge into one step with the result state (Variant B).
   - **Intermediate state vs. final state:** Variant A shows a menu mid-selection, Variant B shows the resulting dialog. Use Variant B (the final state).

2. **Decide on documentation approach:**
   - **Two alternative approaches worth documenting:** Present both as separate steps (e.g., "You can do this by either [Method A] or [Method B]"). Example: "Select the **+** icon next to Subtasks OR select **Add subtask**."
   - **One approach is clearer/preferred:** Show only the preferred variant; note the alternative in an "Additional information" section if relevant.
   - **Variants show the same moment at different zoom/focus levels:** Use the variant that most clearly shows the user action and result state.
   - **One variant is an intermediate state:** Use only the final state (result after the action).

3. **Flag ambiguities for review:**
   - If it's unclear whether variants represent two legitimate paths or states within one path, flag it: "REVIEWER NOTE: Screenshots 2A and 2B show the same area with different focus states. Confirm whether these should be presented as two optional methods or as one step with the final state."

### Step 3: Reconstruct the Workflow

When multiple screenshots are provided:

1. Examine each screenshot for temporal or state-change cues (dialog opened, field filled, confirmation appeared, page changed).
2. Arrange screenshots in the logical sequence. Use filename numbers (1, 2, 3...) as the primary ordering. For variants (1a, 1b; 2a, 2b), determine whether they represent sequential steps or alternative paths:
   - **Sequential:** 1a → 1b shows progression (action → result); merge into one step using the final state (1b).
   - **Alternative paths:** 1a is "path A" and 1b is "path B"; document as two separate optional approaches in the same step.
   - If ambiguity exists, choose the most logical sequence and flag it for review.
3. Identify the user action that caused each state transition (select, type, upload, navigate, etc.).
4. Generate the minimum number of steps needed to complete the task. Do not pad steps. Consolidate variants into a single step when they represent state progression; document alternatives explicitly when two distinct methods exist.
5. For every transition you are uncertain about, add a reviewer note. Do not omit the step—include it with the flag.

**Handling Alternative Methods in Documentation:**

When screenshots show two legitimate ways to accomplish the same goal (e.g., using a menu vs. a button):
- Present both methods in a single step using this format:
  - "Select the **+** icon next to **Subtasks**, or select **Add subtask**. A menu opens displaying options including **Create subtask**..."
  - Show the result state (both methods lead here); choose one variant figure or show both with separate captions if both are essential to understanding the options.
- Alternatively, create separate sub-steps (Step 2a and Step 2b) only if the methods diverge significantly after the initial choice.

** Verify screenshot-to-step mapping (Critical):**
- For each step you create, identify which screenshot shows the result state AFTER the user action.
- Each figure must show the result state, not an intermediate state (e.g., a menu open mid-selection or a button being hovered).
- If a step describes "Select Clone repository..." the figure should show the dialog that opened, NOT the File menu still visible.
- If no screenshot clearly shows the result state, flag this as a gap: "REVIEWER NOTE: Step N text describes '[action]' but no screenshot shows the resulting [state]. Please provide a screenshot or clarify the workflow."
- When choosing between variant screenshots (2a vs. 2b), select the one that most clearly shows the result state. If both are needed, explain why in the preview.

**Hard rule:** Do not use a screenshot showing an intermediate state as the final result of a step unless you explicitly describe it as such in the step text and figcaption.

---

## HTML Output Structure

The skill generates standalone HTML with the following structure:

```
<H1> Topic Title (imperative phrase, sentence case)
<p> Short description (one sentence; what the user will accomplish)

<H2> Prerequisites (only if prerequisites are visible or explicitly provided)
<ul>
  <li>Prerequisite 1</li>
  <li>Prerequisite 2</li>
</ul>

<H2> name of the task for example Clone a repository 
<ol>
  <li>
     [System response; may span multiple sentences]
    <figure>
      <img src="step-NN.png" alt="[Alt text following MS rules]">
      <figcaption>Figure N: [Caption describing the UI state]</figcaption>
    </figure>
    [Optional note: Important information the user should notice about this step]
  </li>
  ...
</ol>

<H2> Result (describes the confirmed outcome)
<p>Text describing what the user should see after completing all steps.</p>

<H2> Additional Information (optional)
<p>Related links, tips, troubleshooting, or other helpful context.</p>
```

---

## Microsoft Style Guide Rules

### Verbs and Voice
- **Imperative verbs** start every step: Select, Enter, Upload, Clear, Expand, Navigate, Confirm, etc.
- **Active voice** throughout. Never use passive construction.
- Avoid: "click", "hit", "press" (except for physical keyboard keys: "Press Enter", "Press Escape").
  - For buttons: **Select** the button
  - For checkboxes/radio buttons: **Select** or **Clear**
  - For typing: **Enter** the text
  - For fields: **Clear** the field

### Capitalization and Formatting
- **Sentence-style capitalization** for all headings (capitalize first word and proper nouns only).
- **Bold** headings and only those UI elements which user needs to click or select.
  - Example: Select **Save**. **Prerequisites**.
- **Menu paths**: File > Save As(use > with spaces on both sides).
- **Keyboard shortcuts**: Ctrl+S (Windows), Command+S (Mac). Format as shown, no bold.
- **Code or placeholders**: Use monospace or as-is notation, e.g., `example@domain.com`.

### Step Format and Language
- **One action per step.** Each numbered item is one user action, followed by the system response.
- **System response** appears in the same list item, after the action. Introduce it with "The" or the application name:
  - "Select **Save**. The Confirmation dialog box appears."
  - "Enter your branch name. GitHub creates the branch and displays it in the branch dropdown."

**System Response Templates** (use to ensure clarity):
- For dialogs/panels opening: "The [dialog name] [opens/appears], if necessary then add "...displaying [key elements] also only if there is something to bring to the notice of user."
- For field changes: "[Application name] [auto-populates/updates/changes] the **[field name]** to [state/value]."
- For state transitions: "The **[element]** [changes/switches/updates] to [new state]."
- For confirmations: "[Application name] [displays/shows] a confirmation [message/dialog] indicating [outcome]."

Example: Instead of "Select **Clone repository...**. [Figure shows dialog]" use "Select **Clone repository...**. The Clone a repository dialog opens with the **GitHub.com** tab selected by default. [Figure shows dialog with GitHub.com tab active]"

- **Screenshot placement**: One screenshot per step, embedded in the `<figure>` element with `<figcaption>`. The figcaption must accurately describe the visible UI state shown in the screenshot.
- **Notes under screenshots**: Use a brief note (not a full sentence) to highlight important UI state or user attention required. Example: "Note: The toggle is now **On**."
- **Concise language**: No filler words. Avoid "then", "afterwards", "next" (the numbering implies sequence).
- **Avoid marketing or value language**: Never use "simply", "easily", "just", "straightforward", "intuitive", etc.

### Alt Text Rules

Alt text must describe the **visible state of the UI**, not the action the user takes.

**For action steps:**
- Structure: `"[Window or page name] with [key visible element and its state]"`
- Good: `"The User Settings page with the Notifications tab selected"`, `"The Email alerts toggle switched on"`
- Bad: `"Screenshot of settings"`, `"User clicks the toggle"`

**For result/outcome steps:**
- Structure: `"Result: [what changed or appeared]"`
- Example: `"Result: GitHub repository page with the new branch listed in the branch dropdown"`

**Figcaption Accuracy (Critical):**
- The figcaption must accurately describe what is VISIBLE in the screenshot, not what you want it to show.
- If the figcaption says "Clone dialog with GitHub.com tab selected" but the screenshot shows a File menu, this is a red flag. Either:
  - The figcaption text is wrong (fix it to match the visible content), OR
  - The wrong screenshot was used (replace it with the correct one), OR
  - A screenshot is missing from the workflow (flag for reviewer)
- Do not allow text-screenshot mismatches. Validate every figcaption against the actual image content before finalizing.

---

## Output Workflow

### Step 1: Preview
After analyzing screenshots and constructing steps, the skill generates a **markdown preview** of the HTML structure. This includes:
- Topic title
- Short description
- Prerequisites (if any)
- Numbered procedure steps with screesnhotsnotes
- Result section
- Any reviewer notes or flags

**Visual Verification Checklist** (for reviewers to validate before approval):
- [ ] Each step text describes ONE user action (imperative verb + UI element)
- [ ] Each figure shows the RESULT state, not an intermediate state
- [ ] Figcaption text accurately matches the visible screenshot content
- [ ] Steps flow sequentially from one result state to the next
- [ ] System responses are explicit (use "The" or app name to introduce what happens)
- [ ] All UI element names are bolded
- [ ] All imperative verbs are correct (Select, Enter, Clear — not Click, Hit, Press)
- [ ] Alt text describes visible UI state, not user action
- [ ] No filler words (simply, easily, just, straightforward)
- [ ] No gaps where screenshots are missing for a step result

### Step 2: Review
You review the preview against the checklist and provide feedback or approval. The skill does NOT write the HTML file until you confirm.

### Step 3: Generate HTML
On your approval, the skill writes a standalone, pretty-printed HTML file with:
- Professional formatting and structure
- Embedded screenshots referenced in the `<figure>` elements
- Formal, official presentation norms (not over-decorated)
- Compliance with all Microsoft Style Guide rules

---

## What NOT to Do

- **Do not infer UI elements** that are not visible in the screenshots.
- **Do not use product knowledge** to fill in steps not shown in screenshots.
- **Do not create steps** that cannot be verified from at least one screenshot.
- **Do not silently resolve conflicts** between screenshots and provided text—flag them for reviewer attention.
- **Do not reproduce UI content verbatim** as prose; extract and reference it structurally (bold the element names).
- **Do not pad steps.** Each step must correspond to one distinct user action.
- **Do not add a step for opening the application** unless a screenshot shows the launch state.
- **Do not end the procedure** on an action step. The final step should confirm an outcome or show a result state.
- **Do not use passive voice.** Rewrite any passive construction in active voice.

**Screenshot-Specific Rules:**
- **Do not use intermediate states as result states.** If a step says "Select File menu" and shows the menu open, that's correct. If a step says "Select Clone repository..." but shows the File menu still open (not the resulting dialog), that's incorrect.
- **Do not allow figcaption-screenshot mismatches.** Every figcaption must accurately describe the visible content of its screenshot. Validate before finalizing.
- **Do not omit steps when screenshots show clear state transitions.** If a screenshot shows a dialog opening, you need a step+figure showing that dialog as a result state.
- **Do not create a step without a corresponding result screenshot.** Each numbered step must have a figure showing its outcome.

**Variant Screenshot Rules (2A/2B, 3a/3b patterns):**
- **Do not automatically split variants into separate steps.** First determine: are these two methods, or state progression? Only split if they represent genuinely different paths.
- **Do not use intermediate variants (Variant A) as the result state.** If Variant A shows a focused field and Variant B shows the same field populated, use Variant B (the final state).
- **Do not omit alternative methods from documentation.** If 2A (use menu) and 2B (use button) both work and both are visible/discoverable, mention both: "Select the **+** icon or **Add subtask**."
- **Do not silently choose one variant without noting the choice.** If multiple variants show the same moment, flag in the preview which variant you selected and why.

---

## Common Mistakes to Avoid

### 1. Showing Action-in-Progress Instead of Result State
**❌ WRONG:**
```
2. Select **Clone repository...**.
Figure: [File menu open with Clone repository highlighted]
```
The figure shows the action being selected, not the result (dialog opening).

**✓ RIGHT:**
```
2, Select **Clone repository...**.
The **Clone a repository** dialog opens.
Figure: [Clone dialog displayed with GitHub.com tab active]
```

### 2. Creating a Step Without a Corresponding Result Screenshot
**❌ WRONG:**
```
3. Enter the repository URL.
[No figure, or figure shows previous state]
```
The screenshot doesn't show the URL field populated (the result of the action).

**✓ RIGHT:**
```
3. Enter the repository URL, for example, https://github.com/namitar4/repo.
[Figure shows the URL field populated with the example URL]
```

### 3. Figcaption That Contradicts Visible Screenshot
**❌ WRONG:**
```
Figcaption: "Clone a repository dialog with GitHub.com tab selected"
Actual image: File menu dropdown open
```
The text and image don't match—one of them is wrong.

**✓ RIGHT:**
```
Figcaption: "File menu open showing Clone repository option"
Image: [File menu clearly visible with Clone repository option highlighted]
```
Figcaption accurately describes what's visible.

### 4. Implicit or Missing System Response
**❌ WRONG:**
```
Step 4: Enter the repository URL.
[Figure shows URL field filled]
```
Doesn't explain what happens next (e.g., field auto-population).

**✓ RIGHT:**
```
Step 4: Enter the repository URL, for example, https://github.com/namitar4/repo.
GitHub Desktop automatically populates the **Local path** field.
[Figure shows both URL and Local path fields populated]
```

### 5. Combining Multiple Actions Into One Step
**❌ WRONG:**
```
Step 3: Select the **URL** tab and enter the repository URL.
```
This is two actions in one step.

**✓ RIGHT:**
```
Step 3: Select the **URL** tab.
[Figure showing URL tab active and empty fields]

Step 4: Enter the repository URL.
[Figure showing URL field populated]
```

### 6. Missing Explicit System Response
**❌ WRONG:**
```
1. Select the **File** menu.
[Figure]
```
Doesn't state what appears after the selection.

**✓ RIGHT:**
```
1. Select the **File** menu.
The File menu opens, displaying options including options for....
[Figure]
```

### 7. Mishandling Variant Screenshots (2A/2B, 3a/3b)
**❌ WRONG:**
```
Step 2. [Screenshot 2A: Menu with Create option highlighted]
Step 2a. [Screenshot 2B: Same menu, field below now focused]
```
Creates unnecessary steps when 2A and 2B show the same moment at different focus states.

**✓ RIGHT (if 2A→2B is state progression):**
```
Step 2. Select **Create subtask**.
A menu opens displaying options. The **Create subtask** option is visible.
[Figure 2B: Menu with result state clearly shown]
```
Use 2B (the final state with focus/clarity). Discard 2A if it's just an intermediate state.

**✓ RIGHT (if 2A and 2B are two different methods):**
```
Step 2. Select the **+** icon next to Subtasks, or select **Add subtask**.
A menu opens displaying options including **Create subtask**, **Link work item**, and other actions.
[Figure 2A or 2B: Either variant works; choose the clearer one]
```
Document both methods in one step. Note that both lead to the same result.

---

## Example Output

### Input
- Screenshots: *1 (empty repo page), *2 (branch dropdown), *3 (new branch dialog), *4 (branch created)
- Task: "Create a branch in GitHub"

### Preview (before HTML generation)
```
How to Create a Branch in GitHub

Create a new branch from an existing repository so you can work on changes without affecting the main branch.

Prerequisites
- You have write access to the repository
- You are signed into GitHub.com

Task e.g Clone a repository

1. Navigate to your repository on GitHub.com.
   [Figure 1: GitHub repository page with Code tab active]

2. Click the branch dropdown (shows "main" or current branch name).
   [Figure 2: Repository page with branch dropdown highlighted]

3. Type your new branch name in the search field.
   [Figure 3: Branch dropdown open with search field active]

4. Select "Create branch: [name]" from the dropdown.
   GitHub creates the branch and switches your view to the new branch. The branch dropdown now shows your new branch name.
   [Figure 4: Repository page showing new branch in dropdown]

Result
GitHub has created your branch. You can now open pull requests, push commits, or make changes on this branch without affecting the main branch.
```

### Final HTML
A standalone HTML file with proper structure, embedded screenshots, figure captions, alt text, and Microsoft Style Guide compliance.

---

## Notes for the Skill

- When analyzing ambiguous workflow sequences, prefer the most common or logical order and flag the ambiguity for review.
- If prerequisites are not visible or mentioned, do not invent them; omit the Prerequisites section.
- Use the Microsoft Learn MCP server to reference current Microsoft Style Guide rules if needed during analysis.
- Always show the markdown preview before writing the HTML file. Wait for user approval.

**Variant Screenshot Analysis:**
- When you encounter variant screenshots (named 2A/2B, 3a/3b, *1a/*1b, etc.), explicitly analyze them in your preview:
  - State what differs between variants (focus state, menu open, different buttons used, etc.)
  - Explain your decision: Are they two methods, or state progression? Will both be shown, or only one?
  - If consolidating variants, state which one you chose and why (clearer state, final result, etc.)
  - If documenting both methods, show how they'll appear in the final procedure
- Flag for reviewer if the distinction between variants is unclear or if both methods seem equally important to document.
