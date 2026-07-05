# HTML5 Conversion Guide

## Overview

This guide provides detailed instructions for converting Microsoft Word documents to standards-compliant HTML5 while preserving structure, formatting, and technical accuracy.

## Word to HTML5 Element Mapping

### Text Formatting

| Word Style | HTML5 Element | Example |
|-----------|--------------|---------|
| Bold | `<strong>` | `<strong>important text</strong>` |
| Italic | `<em>` | `<em>emphasized text</em>` |
| Code/Monospace | `<code>` | `<code>function_name()</code>` |
| Underline | `<u>` or `<ins>` | `<u>underlined text</u>` |
| Strikethrough | `<del>` | `<del>removed text</del>` |

### Headings

Word headings map directly to HTML5 heading levels:

| Word Heading | HTML5 Element |
|-------------|--------------|
| Heading 1 | `<h1>` |
| Heading 2 | `<h2>` |
| Heading 3 | `<h3>` |
| Heading 4 | `<h4>` |
| Heading 5 | `<h5>` |
| Heading 6 | `<h6>` |

**Important**: Never skip heading levels (e.g., don't go from `<h1>` directly to `<h3>`). This breaks document structure and accessibility.

### Lists

#### Unordered Lists (Bullets)
```html
<ul>
  <li>First item</li>
  <li>Second item</li>
  <li>Nested item
    <ul>
      <li>Sub-item 1</li>
      <li>Sub-item 2</li>
    </ul>
  </li>
</ul>
```

#### Ordered Lists (Numbered)
```html
<ol>
  <li>First step</li>
  <li>Second step</li>
  <li>Numbered sublist
    <ol>
      <li>Sub-step 1</li>
      <li>Sub-step 2</li>
    </ol>
  </li>
</ol>
```

#### Definition Lists
```html
<dl>
  <dt>Term 1</dt>
  <dd>Definition of term 1</dd>
  <dt>Term 2</dt>
  <dd>Definition of term 2</dd>
</dl>
```

### Tables

Preserve table structure with semantic elements:

```html
<table>
  <thead>
    <tr>
      <th>Column Header 1</th>
      <th>Column Header 2</th>
      <th>Column Header 3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Data 1</td>
      <td>Data 2</td>
      <td>Data 3</td>
    </tr>
    <tr>
      <td>Data 4</td>
      <td>Data 5</td>
      <td>Data 6</td>
    </tr>
  </tbody>
</table>
```

**Table Best Practices:**
- Use `<thead>` for header rows
- Use `<tbody>` for data rows
- Use `<th>` for header cells (with `scope` attribute if needed)
- Use `<td>` for data cells
- Include `<caption>` if the table has a title
- Preserve merged cells using `colspan` and `rowspan` attributes

### Special Content Blocks

#### Notes
```html
<section class="note">
  <strong>Note:</strong> This is important information the user should know.
</section>
```

#### Warnings
```html
<section class="warning">
  <strong>Warning:</strong> This action may have serious consequences.
</section>
```

#### Cautions
```html
<section class="caution">
  <strong>Caution:</strong> Please be careful when performing this action.
</section>
```

#### Tips
```html
<section class="tip">
  <strong>Tip:</strong> This is helpful advice for better results.
</section>
```

### Images and Figures

#### With Image File
```html
<figure>
  <img src="images/diagram.png" alt="System architecture diagram">
  <figcaption>Figure 1: System architecture showing component relationships</figcaption>
</figure>
```

#### Image Placeholder (when image cannot be embedded)
```html
<figure class="image-placeholder">
  <p>[Image: system-architecture-diagram.png]</p>
  <figcaption>Figure 1: System architecture showing component relationships</figcaption>
</figure>
```

### Links and Cross-References

#### External Links
```html
<a href="https://example.com/page">Link text</a>
```

#### Internal Links / Cross-References
```html
<a href="#section-id">Reference to Section 2.3</a>
```

**Important**: When converting cross-references, create corresponding anchor IDs in the target sections:
```html
<section id="section-2-3">
  <h2>Section 2.3: Details</h2>
  <!-- content -->
</section>
```

### Code Blocks

#### Inline Code
```html
<p>Use the <code>print()</code> function to display output.</p>
```

#### Code Blocks
```html
<pre><code>function helloWorld() {
  console.log("Hello, World!");
}
</code></pre>
```

Or with syntax highlighting class:
```html
<pre><code class="language-javascript">function helloWorld() {
  console.log("Hello, World!");
}
</code></pre>
```

## Document Structure Best Practices

### Main Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document Title</title>
  <meta name="author" content="Author Name">
  <meta name="description" content="Brief document description">
</head>
<body>
  <header>
    <h1>Main Title</h1>
    <p>Document metadata or introduction</p>
  </header>
  
  <main>
    <section id="introduction">
      <h2>Introduction</h2>
      <!-- content -->
    </section>
    
    <section id="overview">
      <h2>Overview</h2>
      <!-- content -->
    </section>
    
    <!-- Additional sections -->
  </main>
  
  <footer>
    <p>Footer information</p>
  </footer>
</body>
</html>
```

### Semantic Sectioning

Use semantic HTML5 elements for better document structure:

- **`<header>`**: Contains introductory content, page title, navigation
- **`<main>`**: Contains the main content of the document
- **`<section>`**: Groups thematic content with its own heading
- **`<article>`**: Self-contained composition
- **`<nav>`**: Navigation links
- **`<aside>`**: Side content, tangentially related
- **`<footer>`**: Contains footer information, metadata, links

## Handling Special Formatting

### Lists with Complex Items
```html
<ul>
  <li>
    <strong>Item Title:</strong> Item description with additional details.
    <p>Additional paragraph within list item.</p>
  </li>
</ul>
```

### Mixed Content in Sections
```html
<section>
  <h2>Requirements Overview</h2>
  <p>Introduction paragraph.</p>
  
  <h3>Functional Requirements</h3>
  <ul>
    <li>Requirement 1</li>
    <li>Requirement 2</li>
  </ul>
  
  <h3>Non-Functional Requirements</h3>
  <ul>
    <li>Requirement 3</li>
    <li>Requirement 4</li>
  </ul>
</section>
```

## Validation and Testing

After conversion, ensure:

1. **Valid HTML5**: Use W3C HTML Validator (https://validator.w3.org/)
2. **Heading Hierarchy**: No skipped levels, proper nesting
3. **Accessible Structure**: Screen reader compatible, semantic elements used
4. **Links**: All links are functional and point to correct destinations
5. **Tables**: Proper semantic structure with headers
6. **Metadata**: Title and author information in `<head>`

## Common Pitfalls to Avoid

❌ **Don't**: Use `<b>` for bold (use `<strong>` instead)
❌ **Don't**: Use `<i>` for italic (use `<em>` instead)
❌ **Don't**: Skip heading levels (no `<h1>` to `<h3>` jumps)
❌ **Don't**: Use tables for layout
❌ **Don't**: Use inline styles instead of classes
❌ **Don't**: Forget alt text for images
❌ **Don't**: Omit metadata and document structure

✓ **Do**: Use semantic HTML5 elements
✓ **Do**: Follow heading hierarchy strictly
✓ **Do**: Include proper document metadata
✓ **Do**: Use classes for styling and organization
✓ **Do**: Include descriptive alt text and captions
✓ **Do**: Validate against HTML5 standards
