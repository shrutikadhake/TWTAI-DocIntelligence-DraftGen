---
name: generate-product-docs
description: Generate professional product documentation from feature specification files. Use this skill whenever a user needs to create customer-facing HTML documentation from feature specs in a folder. Supports files like .md, .txt, .rst, .json, .png, and .jpg. Automatically skips .docx files and generates one polished HTML document per feature following technical writing standards. Ideal for product documentation, API docs, feature guides, and customer-facing materials.
compatibility: Read, Write, Glob, Grep tools required
---

# Generate Product Documentation

## Purpose

This skill transforms feature specification files into professional, customer-facing HTML product documentation. It reads specification files from a folder, extracts feature information, and creates polished documentation following technical writing best practices.

## Input Requirements

**Required:**
- Folder path containing feature specification files

**Supported file types:**
- `.md` (Markdown)
- `.txt` (Plain text)
- `.rst` (reStructuredText)
- `.json` (JSON)
- `.png`, `.jpg` (Images for reference)
- `.html` (HTML content)

**Files to skip:**
- `.docx` files (inform user that Word documents cannot be processed and were skipped)

## Output Format

For each feature found in the specification files:

1. **Feature Name** - As H1 heading
2. **Brief Description** - What the feature does (1-2 sentences)
3. **How to Access** - Step-by-step instructions
4. **Applications** - Use cases and when to use the feature
5. **UI Options** - For each option:
   - **Description**: What the option does
   - **Default Value**: The default setting
   - **Available Options**: List of choices with descriptions
   - **Application**: When/how to use each option

## Documentation Structure

Generate ONE HTML file per feature with the naming format: `<Feature-Name>output.html`

**HTML Template Structure:**
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Feature Name</title>
  <style>
    /* Include basic styling: Arial/Helvetica font, 1.6 line-height, max-width 900px, clean layout */
    /* Use professional colors and spacing */
  </style>
</head>
<body>
  <h1>Feature Name</h1>
  <p>[Brief description]</p>
  <h2>How to Access</h2>
  <p>[Access instructions]</p>
  <h2>Applications</h2>
  <p>[Use cases]</p>
  <h2>UI Options</h2>
  <!-- For each option... -->
  <h3>Option Name</h3>
  <p>Description: ...</p>
  <p>Default: ...</p>
  <p>Options: ...</p>
</body>
</html>
```

## Workflow

1. **Scan the folder** - Use Glob to find all files with supported extensions
2. **Identify features** - Look for feature names in filenames or content (e.g., "Feature Name: Weld Extension")
3. **Extract information** - Read each file and extract:
   - Feature name
   - Overview/description
   - How to access instructions
   - Application use cases
   - UI options with their properties
4. **Handle missing data gracefully** - If a feature spec doesn't have all sections, include what's available. Don't force empty sections.
5. **Skip .docx files** - Do not attempt to read .docx files; inform the user which .docx files were encountered and skipped
6. **Generate HTML** - Create professional, well-formatted HTML output for each feature
7. **Save to output folder** - Write all HTML files to the `output/` folder in the same directory as the input folder

## Key Guidelines

- **Technical Writing Standards**: Use clear, concise language. Be specific and objective.
- **Format consistency**: Follow the example structure provided by the user
- **User-facing**: Write for external customers, not internal developers
- **No unnecessary sections**: Don't include sections if the data doesn't exist
- **Professional styling**: Use clean, readable HTML with proper spacing and typography
- **File naming**: Use exact format `<Feature-Name>output.html` (preserve case, replace spaces with hyphens)

## Example Section Structure

```
Weld Extension

Weld Extension control allows you to create weld body extensions and generate layers of quad elements on the weld extensions. Weld Extension control enables you to scope the bodies having weld features. The feature supports both planar welds and solid welds.

To access the Weld Extension control,

Right-click Mesh object and click Insert > Weld Extension.

When you click Weld Extension, the Details view displays the Weld Extension options:

Scoping Method

Scoping Method: Allows you to define the method for scoping the bodies that contain weld features. The default option is Geometry Selection.

Geometry Selection: Scope the geometry bodies to be extended as weld components.

Named Selection: Scope the geometry bodies to be suppressed in the named selection.
```

## Error Handling

- **Skipped files**: Log which .docx files were skipped
- **Missing sections**: Include available sections, omit missing ones
- **Encoding issues**: Handle text encoding gracefully
- **Large images**: Reference images descriptively rather than embedding them if too large
