# md-to-html skill

Converts a Markdown file to a plain HTML file and automatically reviews the content against 5 Microsoft Style Guide (MSTP) rules.

## What it does

**Part 1 — Convert**  
Reads the source `.md` file and converts every Markdown element to HTML: headings, paragraphs, bold/italic, inline code, bullet and numbered lists, fenced code blocks, tables (with `<thead>`/`<tbody>`), images, links, blockquotes, and horizontal rules. Saves the result as `[filename].html` with no CSS or JavaScript.

**Part 2 — MSTP review**  
Runs 5 live `microsoft_docs_search` calls to retrieve official Microsoft guidance, then checks the document content against those rules and outputs a violation table.

| Rule checked | What is flagged |
|---|---|
| Active voice | Passive constructions: "is Xed by", "was Xed", "will be Xed" |
| Second person | Third-person references to the reader: "the user", "the developer" |
| Present tense | Future tense in instructional prose: "will return", "will show" |
| Sentence length | Any prose sentence over 25 words |
| Heading case | Title Case headings (only first word and proper nouns should be capitalised) |

Code blocks and inline code are excluded from the style review.

## How to invoke

```
/md-to-html resources\sample-docs\your-file.md
```

The argument can be an absolute path, a relative path, or just a filename (looks in `resources/` by default).

## Output

| File | Location |
|---|---|
| `[filename].html` | `output\` folder |
| MSTP violation table | Printed to the conversation |

## What requires human review

- Factual accuracy of the content
- Context-specific exceptions to MSTP rules (e.g. intentional future tense for scheduled events)
- Technical correctness of code examples

## Skill file

`skills\md-to-html\SKILL.md`
