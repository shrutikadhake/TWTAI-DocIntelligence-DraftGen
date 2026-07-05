# HTML5 Semantic Elements Reference

## What is Semantic HTML?

Semantic HTML uses markup elements that carry meaning about the content they contain. Instead of using generic `<div>` tags everywhere, semantic elements clearly describe the purpose of the content to both browsers and developers.

## Primary Document Structure Elements

### `<header>`
Contains introductory content at the top of a page or section.

**Usage:**
- Page header with title and introduction
- Section header with metadata
- Navigation area

```html
<header>
  <h1>Document Title</h1>
  <p>Version 1.0 | Author: John Doe | Date: July 1, 2026</p>
</header>
```

---

### `<nav>`
Contains navigation links to other pages or sections.

**Usage:**
- Main navigation menu
- Table of contents
- Breadcrumb navigation
- Sidebar navigation

```html
<nav>
  <ul>
    <li><a href="#overview">Overview</a></li>
    <li><a href="#requirements">Requirements</a></li>
    <li><a href="#specifications">Specifications</a></li>
  </ul>
</nav>
```

---

### `<main>`
Contains the primary content of the document. Should be unique per page.

**Usage:**
- Wraps all primary document content
- Excludes headers, footers, sidebars

```html
<main>
  <article>
    <!-- main content -->
  </article>
</main>
```

---

### `<article>`
Contains a self-contained composition that could stand alone.

**Usage:**
- Complete requirement specification
- Feature description
- Use case scenario
- Technical specification section

```html
<article>
  <h2>User Authentication Requirements</h2>
  <p>The system shall support...</p>
</article>
```

---

### `<section>`
Groups thematically related content with its own heading.

**Usage:**
- Functional requirements section
- Technical specifications section
- Configuration information section

```html
<section id="functional-requirements">
  <h2>Functional Requirements</h2>
  <p>Overview text...</p>
  <ul>
    <li>Requirement 1</li>
    <li>Requirement 2</li>
  </ul>
</section>
```

---

### `<aside>`
Contains content tangentially related to the main content.

**Usage:**
- Sidebar notes
- Related references
- Additional information boxes

```html
<aside>
  <h3>Related Documents</h3>
  <ul>
    <li><a href="#">Design Document</a></li>
    <li><a href="#">API Reference</a></li>
  </ul>
</aside>
```

---

### `<footer>`
Contains footer content at the bottom of a page or section.

**Usage:**
- Page footer with copyright and links
- Section footer with related information
- Document revision information

```html
<footer>
  <p>&copy; 2026 TWTAI. All rights reserved.</p>
  <p>Version 1.0 | Last Updated: July 1, 2026</p>
</footer>
```

---

## Content Organization Elements

### `<h1>` through `<h6>`
Heading hierarchy for document structure.

**Rules:**
- `<h1>`: Main document title (usually one per page)
- `<h2>`: Major sections
- `<h3>`: Subsections
- `<h4>`: Sub-subsections
- Continue hierarchically without skipping levels

**Example:**
```html
<h1>Product Requirements Document</h1>
<h2>Overview</h2>
<h3>Product Purpose</h3>
<h3>Product Scope</h3>
<h2>Functional Requirements</h2>
<h3>Authentication</h3>
<h4>Login Functionality</h4>
<h4>Password Reset</h4>
```

---

### `<p>`
Paragraph of text content.

**Usage:**
- Body text and descriptions
- Explanations and details
- Supporting information

```html
<p>This feature enables users to securely authenticate using their credentials.</p>
```

---

## Text-Level Semantic Elements

### `<strong>`
Indicates strong importance (bold).

**Usage:**
- Critical information
- Important emphasis
- Key terms

```html
<p>This is a <strong>critical requirement</strong> for system security.</p>
```

---

### `<em>`
Indicates emphasis (italic).

**Usage:**
- Stress emphasis
- Technical terms
- Definitions

```html
<p>The <em>user interface</em> must be intuitive and responsive.</p>
```

---

### `<code>`
Indicates code content.

**Usage:**
- Function names
- Variable names
- Command syntax
- Code snippets

```html
<p>Use the <code>getUserData(userId)</code> function to retrieve user information.</p>
```

---

### `<pre>`
Preformatted text (preserves whitespace).

**Usage:**
- Code blocks
- Configuration examples
- ASCII diagrams

```html
<pre><code>
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}
</code></pre>
```

---

### `<mark>`
Highlights important text.

**Usage:**
- Highlighted text for reference
- Important terms
- Key information

```html
<p>The deadline is <mark>July 15, 2026</mark>.</p>
```

---

### `<del>` and `<ins>`
Deleted and inserted text (track changes).

**Usage:**
- Track document revisions
- Show removed content
- Highlight additions

```html
<p>The price was <del>$100</del> <ins>$80</ins>.</p>
```

---

## List Elements

### `<ul>` - Unordered List
Items without specific order.

```html
<ul>
  <li>Feature 1</li>
  <li>Feature 2</li>
  <li>Feature 3</li>
</ul>
```

---

### `<ol>` - Ordered List
Items in specific order.

```html
<ol>
  <li>First step</li>
  <li>Second step</li>
  <li>Third step</li>
</ol>
```

---

### `<dl>` - Definition List
Term-definition pairs.

```html
<dl>
  <dt>Authentication</dt>
  <dd>The process of verifying user identity.</dd>
  <dt>Authorization</dt>
  <dd>The process of determining what authenticated users can access.</dd>
</dl>
```

---

### `<li>`
List item within `<ul>`, `<ol>`, or `<dl>`.

---

## Table Elements

### `<table>`
Container for tabular data.

```html
<table>
  <thead>
    <tr>
      <th>Header 1</th>
      <th>Header 2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Data 1</td>
      <td>Data 2</td>
    </tr>
  </tbody>
</table>
```

---

### `<thead>`
Groups header rows of a table.

---

### `<tbody>`
Groups body rows of a table.

---

### `<tfoot>`
Groups footer rows of a table.

---

### `<tr>`
Table row.

---

### `<th>`
Table header cell (semantic header).

---

### `<td>`
Table data cell.

---

### `<caption>`
Title for a table.

```html
<table>
  <caption>System Requirements Summary</caption>
  <!-- table content -->
</table>
```

---

## Media and Figure Elements

### `<figure>`
Self-contained illustration, diagram, photo, or code.

```html
<figure>
  <img src="architecture.png" alt="System architecture diagram">
  <figcaption>Figure 1: High-level system architecture</figcaption>
</figure>
```

---

### `<figcaption>`
Caption or legend for `<figure>` content.

---

### `<img>`
Embedded image.

```html
<img src="image.png" alt="Descriptive alternative text">
```

---

## Special Content Elements

### `<blockquote>`
Extended quotation or reference.

```html
<blockquote>
  <p>The system shall provide comprehensive audit logging of all user activities.</p>
  <cite>Section 4.2.3</cite>
</blockquote>
```

---

### `<cite>`
Citation or reference source.

```html
<p>As stated in <cite>RFC 5234</cite>, the format must be...</p>
```

---

## Custom Semantic Sections for Technical Documentation

### Notes
```html
<section class="note">
  <strong>Note:</strong> Additional information or helpful context.
</section>
```

### Warnings
```html
<section class="warning">
  <strong>Warning:</strong> Important cautions or potential issues.
</section>
```

### Cautions
```html
<section class="caution">
  <strong>Caution:</strong> Risk of undesired results if not followed.
</section>
```

### Tips
```html
<section class="tip">
  <strong>Tip:</strong> Helpful advice for improved results.
</section>
```

---

## Semantic Structure Example

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Product Requirements Document</title>
</head>
<body>
  <header>
    <h1>Product Requirements Document</h1>
    <p>Version 1.0 | July 1, 2026</p>
  </header>
  
  <nav>
    <ul>
      <li><a href="#overview">Overview</a></li>
      <li><a href="#requirements">Requirements</a></li>
    </ul>
  </nav>
  
  <main>
    <section id="overview">
      <h2>Product Overview</h2>
      <p>Description of product...</p>
    </section>
    
    <section id="requirements">
      <h2>Functional Requirements</h2>
      <article>
        <h3>User Authentication</h3>
        <p>Requirements for user login...</p>
        <ul>
          <li>Requirement 1</li>
          <li>Requirement 2</li>
        </ul>
      </article>
    </section>
  </main>
  
  <footer>
    <p>&copy; 2026. All rights reserved.</p>
  </footer>
</body>
</html>
```

---

## Why Semantic HTML Matters

1. **Accessibility**: Screen readers understand document structure
2. **SEO**: Search engines better understand content meaning
3. **Maintainability**: Code is more readable and maintainable
4. **Responsiveness**: Semantic structure helps with CSS styling
5. **Standards Compliance**: Follows HTML5 best practices
