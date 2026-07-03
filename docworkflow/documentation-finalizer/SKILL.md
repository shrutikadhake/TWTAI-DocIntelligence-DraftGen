---
name: documentation-finalizer
description: |
  Transforms reviewed and corrected documentation into publication-ready HTML for end users. Use this skill as the final step in the documentation pipeline: provide the markdown file and review.json report, and it will automatically fix all critical issues, apply corrections, and generate an elegant, professionally designed HTML guide. Produces beautiful, responsive documentation ready to publish or distribute. Perfect for converting markdown documentation into polished end-user guides with modern or minimalist design themes. Always use this skill when you have reviewed documentation that needs to be converted to final HTML form for users.
compatibility: |
  - Input: Markdown file path + review.json file path
  - Output: Elegant HTML file ready for publication
  - Design themes: Modern (contemporary, gradient-based) or Minimalist (clean, professional)
---

# Documentation Finalizer

Transforms markdown documentation and its quality review into publication-ready, elegantly designed HTML guides for end users.

## Input Format

The skill requires two files:

**1. Markdown file path:**
```
path/to/documentation.md
```

**2. Review JSON file path:**
```
path/to/documentation-review.json
```

Example usage:
```
Finalize this documentation:
- Markdown: C:\docs\learn-html.md
- Review: C:\docs\learn-html-review.json
- Theme: modern
```

## Process

1. **Read both files** — Parse the markdown and review.json
2. **Identify critical issues** — Extract all findings with severity level "critical"
3. **Apply fixes** — Modify the markdown content to address critical issues based on suggested_fix values
4. **Extract metadata** — Pull title, goal, prerequisites from markdown and review
5. **Design and render** — Generate elegant HTML using selected theme
6. **Output** — Save as publication-ready HTML file

## Design Theme: Modern (Default)

The skill uses the **Modern Theme** for all output:
- Contemporary gradient backgrounds (purple/blue)
- Clean typography with generous spacing
- Interactive elements (hover effects, smooth transitions)
- Accent colors and visual hierarchy
- Card-based layouts for task sections
- Responsive grid design
- Color palette: Gradients (667eea → 764ba2), white, light gray accents
- Professional and contemporary appearance

**Ideal for:** Tech products, SaaS platforms, modern audiences, contemporary organizations

**Note:** The minimalist theme is available as an alternative if needed, but modern is the default for publication-ready output.

## HTML Structure

Both themes follow this structure:

```html
<html>
  <header>
    <!-- Logo area / branding -->
    <!-- Navigation (optional breadcrumb) -->
    <!-- Page title and introduction -->
  </header>

  <nav>
    <!-- Sticky/floating navigation or table of contents -->
    <!-- Links to main sections -->
  </nav>

  <main>
    <!-- Prerequisites section -->
    <!-- Procedure section with tasks and steps -->
    <!-- Expected results section -->
    <!-- Troubleshooting section (if present) -->
  </main>

  <footer>
    <!-- Document metadata (last updated, source) -->
    <!-- Back-to-top link -->
  </footer>
</html>
```

## Content Organization

The HTML guide includes:

- **Header**: Document title, introductory goal, visual hierarchy
- **Navigation**: Quick links to major sections
- **Prerequisites**: Clearly highlighted requirements with context
- **Procedure**: Tasks organized with clear step-by-step instructions
  - Each step shows: action (bold), details (context), expected outcome
  - Visual separators between tasks
  - Progress through steps
- **Expected Results**: Validation checklist and troubleshooting
- **Footer**: Publication metadata

## Critical Issue Handling

When critical issues are found in the review:

1. **Identify** — Find each issue with severity = "critical"
2. **Apply fix** — Use the `suggested_fix` value to correct the markdown
3. **Verify** — Ensure the fix improves clarity and correctness
4. **Document** — Note in footer that critical issues were addressed

Example critical issue fix:
```
Original: "...the Copilot Chat interface..."
Issue: Terminology inconsistency
Fix: "...the Microsoft 365 Copilot interface..."
```

## When to Use This Skill

- You have markdown documentation + review.json from the documentation pipeline
- You need to convert reviewed documentation to publication-ready HTML
- You want an elegant, professional-looking guide for end users
- You need both modern and minimalist design options
- Documentation has been quality-checked and needs final formatting

## When NOT to Use This Skill

- You haven't reviewed the documentation yet (use documentation-reviewer first)
- You only have markdown without a review report
- You need to make content changes (fix in the markdown before finalizing)
- You don't need HTML output (markdown is sufficient)

## How to Use This Skill

**Provide both file paths and theme choice:**

```
Finalize this documentation:
- Markdown file: C:\docs\my-guide.md
- Review file: C:\docs\my-guide-review.json
- Theme: modern
- Output: C:\output\my-guide.html
```

Or:

```
Generate the final HTML guide from this documentation:
- Markdown: /users/docs/tutorial.md
- Review: /users/docs/tutorial-review.json
- Theme: minimalist
```

The skill will:
1. Read both input files
2. Fix all critical issues automatically
3. Generate elegant HTML using your chosen theme
4. Save as ready-to-publish HTML file
5. Include metadata about fixes applied

## Output File Naming

The HTML file is named based on the markdown filename:
- Input: `learn-basic-html.md`
- Output: `learn-basic-html.html`

Both modern and minimalist versions are fully responsive and work on all devices (desktop, tablet, mobile).

## Design Features

Both themes include:

✓ **Responsive design** — Works on all screen sizes  
✓ **Print-friendly** — Looks great in print  
✓ **Readable typography** — Optimized for readability  
✓ **Visual hierarchy** — Clear content organization  
✓ **Accessibility** — Semantic HTML, color contrast  
✓ **Performance** — Lightweight, no external dependencies  
✓ **Publication metadata** — Shows last updated, fixes applied  

## Example Workflow

```
Input Files:
  - documentation-author output: using-m365-copilot.md
  - documentation-reviewer output: using-m365-copilot-review.json
  
Process:
  1. Read markdown and review
  2. Identify critical issues (if any)
  3. Apply suggested fixes automatically
  4. Choose design theme (modern or minimalist)
  5. Render elegant HTML
  
Output:
  - using-m365-copilot.html (publication-ready)
  - Includes fix annotations in footer
  - Ready to share with end users
```
