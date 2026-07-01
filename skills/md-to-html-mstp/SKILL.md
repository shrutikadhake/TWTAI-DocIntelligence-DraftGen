---
name: md-to-html-mstp
description: Convert a Markdown file to three HTML outputs — a raw HTML conversion, a styled MSTP violation report, and a polished MSTP-compliant HTML rewrite. Use this skill whenever the user passes a .md file path and wants HTML output with style checking or rewriting — whether they say "convert and check", "convert with MSTP review", "fix my doc", "polish this", "give me three outputs", or provides a markdown file path in a technical writing context. Always runs all three parts in sequence. Trigger any time a .md file is mentioned alongside HTML, convert, output, review, polish, or fix, especially for API docs, developer docs, or technical writing quality.
---

# md-to-html-mstp

This skill always runs three parts in sequence. Never stop early.

- **Part 1** — Convert the Markdown file to plain HTML. Save as `[filename].html`.
- **Part 2** — Review the original content against 5 Microsoft Style Guide rules. Save the violation report as a styled HTML file: `[filename]-style-review.html`.
- **Part 3** — Rewrite the content to fix all violations, then convert it to HTML. Save as `[filename]-polished.html`.

## What you receive

The file path comes in as `$ARGUMENTS`. It may be:
- An absolute path: `C:\Users\HP\Doc-Intelligence\project\resources\sample-doc.md`
- A relative path: `resources/sample-doc.md`
- Just a filename: `sample-doc.md` (look for it in the `resources/` folder)

**Output folder for all three files:** `C:\Users\HP\Doc-Intelligence\TWTAI-DocIntelligence-DraftGen\output\`

---

## PART 1 — Convert Markdown to HTML

### Step 1: Read the Markdown file

Read the full contents of the file. Do not skip any lines.

### Step 2: Convert each element

Process the file in order, top to bottom.

#### Headings
| Markdown | HTML |
|---|---|
| `# Heading` | `<h1>Heading</h1>` |
| `## Heading` | `<h2>Heading</h2>` |
| `### Heading` | `<h3>Heading</h3>` |
| `#### Heading` | `<h4>Heading</h4>` |

#### Text formatting (apply inside paragraphs, list items, table cells, blockquotes)
| Markdown | HTML |
|---|---|
| `**bold**` or `__bold__` | `<strong>bold</strong>` |
| `*italic*` or `_italic_` | `<em>italic</em>` |
| `` `inline code` `` | `<code>inline code</code>` |

#### Paragraphs
Any line that is not a heading, list item, code block, table, image, link, blockquote, or horizontal rule is a paragraph. Wrap in `<p>` tags. Group consecutive lines with no blank line between them into a single `<p>`.

#### Bullet lists → `<ul><li>...</li></ul>`
#### Numbered lists → `<ol><li>...</li></ol>`
#### Fenced code blocks → `<pre><code>...</code></pre>` (preserve all whitespace exactly)
#### Tables → `<table>` with `<thead>` for the first row and `<tbody>` for data rows. Skip separator rows (`---`).
#### Images → `<img src="url" alt="Alt text">`
#### Links → `<a href="url">Link text</a>`
#### Blockquotes → `<blockquote>Text</blockquote>` (remove the `> ` prefix; keep inline formatting)
#### Horizontal rules → `<hr>` (lines with only `---`, `***`, or `___`)

### Step 3: Build the full HTML document

Use the first `<h1>` text as the `<title>`. If none exists, use the filename without extension.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title here</title>
</head>
<body>

[converted content]

</body>
</html>
```

No CSS, no inline styles, no JavaScript. Include every element exactly as it appears. Keep order intact.

### Step 4: Save

Filename: `[input-filename].html`
Tell the user the full path.

---

## PART 2 — MSTP Violation Report

Run all five `microsoft_docs_search` calls first, then compile everything into one styled HTML file. Do not output the review to the conversation — save it directly as a file.

### The five checks

#### Check 1 — Active voice
```
microsoft_docs_search("active voice technical writing")
```
Flag passive voice: "is [verb]ed by", "was [verb]ed", "will be [verb]ed", "can be [verb]ed", "has been [verb]ed".
*Skip code blocks, inline code, and quoted error messages.*

#### Check 2 — Second person
```
microsoft_docs_search("second person you documentation")
```
Flag third-person references to the reader: "the user", "users", "the developer", "the reader". Microsoft style addresses the reader as "you" or "your".

#### Check 3 — Present tense
```
microsoft_docs_search("present tense technical writing")
```
Flag future tense in instructional or descriptive prose: "will be", "will need to", "will return", "will happen". Prefer present tense: "returns" not "will return".

#### Check 4 — Sentence length
```
microsoft_docs_search("sentence length readability")
```
Flag any prose sentence with more than 25 words. Count every word including articles and prepositions.

#### Check 5 — Heading case
```
microsoft_docs_search("headings sentence case")
```
Flag headings that use Title Case (most words capitalised). Microsoft style uses sentence case: only the first word and proper nouns are capitalised.

### Save as styled HTML

Save the report as `[input-filename]-style-review.html` using this exact structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>MSTP Style Review — [filename]</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 2em; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #555; padding: 8px 12px; text-align: left; vertical-align: top; }
    thead th { background-color: #2c2c2c; color: #fff; }
    tbody tr:nth-child(even) { background-color: #f5f5f5; }
    tbody tr:hover { background-color: #eaf3fb; }
  </style>
</head>
<body>
<h1>MSTP Style Review — [filename]</h1>
<table>
  <thead>
    <tr>
      <th>#</th><th>Rule</th><th>Location</th><th>Issue</th><th>Recommended fix</th>
    </tr>
  </thead>
  <tbody>
    [one <tr> per violation]
  </tbody>
</table>
<h2>Summary</h2>
<ul>
  <li><strong>Total issues found:</strong> N</li>
  <li><strong>Rules with violations:</strong> [list]</li>
</ul>
<h2>Requires human review</h2>
<ul>
  <li>[anything ambiguous — e.g. intentional future tense, product names in headings]</li>
</ul>
</body>
</html>
```

For *Location*, be specific enough to find the sentence: heading name, paragraph number, list item number, or table column name.

If a rule has no violations, include a row: `<td colspan="4">No violations found</td>`.

Tell the user the full path once saved.

---

## PART 3 — Polished MSTP-Compliant HTML

Take the **original Markdown content** and rewrite the prose to fix all five violation types, then convert the result to HTML using the same rules as Part 1. Save as `[input-filename]-polished.html`.

### What to fix

Apply all five fixes to every prose sentence in the document. Work through the file top to bottom.

#### Fix 1 — Active voice
Rewrite passive constructions so the actor is the subject.

- "The token will be validated by the system" → "The system validates the token"
- "An API key will be generated by the system" → "The system generates an API key"
- "A code will be returned to the user" → "The system returns a code"

When there is no clear actor, use an imperative instead:
- "The key will be included in the header" → "Include the key in the header"

#### Fix 2 — Second person
Replace third-person references to the reader with "you" or "your". Rewrite surrounding sentence structure as needed.

- "The user must select one of the following" → "Select one of the following"
- "the user's application" → "your application"
- "The user should generate a new token" → "Generate a new token"

#### Fix 3 — Present tense
Replace future tense with present tense in instructional and descriptive prose.

- "will generate" → "generates"
- "will be sent" → "sends" or "is sent"
- "will need to" → "needs to"
- "will return" → "returns"

Exception: keep future tense only for genuinely scheduled events ("will be removed in v4.0", "will expire after 24 hours").

#### Fix 4 — Sentence length
Split any sentence over 25 words into two or more shorter sentences. Preserve all meaning.

- Long: "An API key will be generated by the system and it will be sent to the user via email after the registration process has been completed by the user." (29 words)
- Fixed: "After you complete registration, the system generates your API key and emails it to you."

#### Fix 5 — Heading case
Convert Title Case headings to sentence case. Keep the first word and proper nouns capitalised; lowercase everything else.

- "Authentication Methods And Their Descriptions" → "Authentication methods and their descriptions"
- "OAuth 2.0 Authentication Method And Token Management" → "OAuth 2.0 authentication method and token management"
- "API Key Authentication Method" → "API key authentication method"

### What NOT to change

- Code blocks and inline code — leave exactly as written
- Technical terms, product names, and acronyms — keep their established capitalisation (OAuth, REST, JWT, etc.)
- Table data that is not prose (e.g., parameter names, type values, error codes)
- Quoted error messages and quoted strings in prose
- The document structure — headings stay at the same level, lists stay as lists, tables keep the same columns

### Convert to HTML

After rewriting, convert the polished content to HTML using exactly the same rules as Part 1. Build the full HTML document with `<!DOCTYPE html>`, `<html lang="en">`, `<head>` (with `<meta charset="UTF-8">` and `<title>`), and `<body>`. No CSS, no inline styles.

### Save

Filename: `[input-filename]-polished.html`
Tell the user the full path.

---

## Confirmation message

End with a summary of all three outputs:

> **All three files saved:**
>
> 1. `[filename].html` — raw HTML conversion  
>    `C:\Users\HP\Doc-Intelligence\TWTAI-DocIntelligence-DraftGen\output\[filename].html`
>
> 2. `[filename]-style-review.html` — MSTP violation report (N issues across M rules)  
>    `C:\Users\HP\Doc-Intelligence\TWTAI-DocIntelligence-DraftGen\output\[filename]-style-review.html`
>
> 3. `[filename]-polished.html` — rewritten to follow all 5 MSTP rules  
>    `C:\Users\HP\Doc-Intelligence\TWTAI-DocIntelligence-DraftGen\output\[filename]-polished.html`
