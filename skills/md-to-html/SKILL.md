---
name: md-to-html
description: >
  Convert a Markdown file to a plain HTML file. Use this skill whenever the user passes a .md file path
  and wants an HTML version of it — whether they say "convert", "turn into HTML", "export as HTML",
  or just provide a markdown file path expecting an HTML output. The skill handles all standard
  Markdown elements and produces a complete, valid HTML file saved to the project output folder.
  Trigger this skill any time a .md file is mentioned alongside HTML, convert, export, or output.
---

# md-to-html

Convert a Markdown file to a plain HTML file with no styling.

## What you receive

The file path comes in as `$ARGUMENTS`. It may be:
- An absolute path: `C:\Users\HP\Doc-Intelligence\TWTAI-DocIntelligence-DraftGen\resources\sample-doc.md`
- A relative path: `resources/sample-doc.md`
- Just a filename: `sample-doc.md` (look for it in the `resources/` folder)

## Steps

### 1. Read the Markdown file

Read the full contents of the file at the given path. Do not skip any lines.

### 2. Convert Markdown to HTML

Go through the file line by line and convert each element using the rules below. Process the file in order — do not reorder content.

#### Headings

| Markdown | HTML |
|---|---|
| `# Heading` | `<h1>Heading</h1>` |
| `## Heading` | `<h2>Heading</h2>` |
| `### Heading` | `<h3>Heading</h3>` |
| `#### Heading` | `<h4>Heading</h4>` |

#### Text formatting

| Markdown | HTML |
|---|---|
| `**bold**` or `__bold__` | `<strong>bold</strong>` |
| `*italic*` or `_italic_` | `<em>italic</em>` |
| `` `inline code` `` | `<code>inline code</code>` |

These can appear inside paragraphs, list items, table cells, and blockquotes. Apply them wherever they appear.

#### Paragraphs

Any line that is not a heading, list item, code block, table, image, link, blockquote, or horizontal rule is a paragraph. Wrap it in `<p>` tags.

Group consecutive plain-text lines into a single `<p>` block if they form one paragraph (no blank line between them).

#### Bullet lists

```markdown
- Item one
- Item two
- Item three
```

Converts to:

```html
<ul>
  <li>Item one</li>
  <li>Item two</li>
  <li>Item three</li>
</ul>
```

#### Numbered lists

```markdown
1. First
2. Second
3. Third
```

Converts to:

```html
<ol>
  <li>First</li>
  <li>Second</li>
  <li>Third</li>
</ol>
```

#### Fenced code blocks

A block that starts with ` ``` ` and ends with ` ``` ` (with or without a language label) becomes a `<pre><code>` block. Preserve all whitespace and indentation inside exactly as written.

```html
<pre><code>your code here</code></pre>
```

#### Tables

A Markdown table (rows separated by `|`, with a separator row of `---`) becomes a full HTML table. The first row is the header row.

```html
<table>
  <thead>
    <tr>
      <th>Column 1</th>
      <th>Column 2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Value 1</td>
      <td>Value 2</td>
    </tr>
  </tbody>
</table>
```

#### Images

```markdown
![Alt text](image-url)
```

Converts to:

```html
<img src="image-url" alt="Alt text">
```

#### Links

```markdown
[Link text](https://example.com)
```

Converts to:

```html
<a href="https://example.com">Link text</a>
```

#### Blockquotes

```markdown
> This is a blockquote.
```

Converts to:

```html
<blockquote>This is a blockquote.</blockquote>
```

Remove the leading `> ` but keep the rest of the text exactly as written, including any inline formatting.

#### Horizontal rules

A line with only `---` or `***` or `___` becomes:

```html
<hr>
```

### 3. Build the full HTML document

Wrap the converted content in a complete HTML structure. Use the text of the **first `<h1>`** found in the file as the page title. If there is no `<h1>`, use the filename (without extension) as the title.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title from first H1</title>
</head>
<body>

[all converted HTML content goes here]

</body>
</html>
```

### 4. Save the output file

- Output folder: `C:\Users\HP\Doc-Intelligence\TWTAI-DocIntelligence-DraftGen\output\`
- Output filename: same as the input file, but with `.html` instead of `.md`
  - Example: `sample-doc.md` → `sample-doc.html`
- Write the full HTML string to that file.
- Do not print the HTML to the terminal.

### 5. Confirm the result

After saving, tell the user:
- The output filename
- The full path to the saved file

Example confirmation:
> Saved: sample-doc.html  
> Location: C:\Users\HP\Doc-Intelligence\TWTAI-DocIntelligence-DraftGen\output\sample-doc.html

## Rules

- Include every element from the Markdown file. Do not add anything that is not there.
- Do not remove or skip any content from the Markdown file.
- No CSS, no inline styles, no JavaScript — plain HTML only.
- Keep the order of content exactly as it appears in the source file.
- Preserve all text exactly as written inside elements (no rewording, no summarizing).
