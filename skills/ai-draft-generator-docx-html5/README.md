# AI Draft Generator - Microsoft Word to HTML5 Converter Skill

## Overview

This Claude AI Skill converts Microsoft Word Product Requirements and Specifications documents (.docx) into standards-compliant HTML5 Technical Documentation. It preserves document structure, formatting, technical accuracy, and semantic meaning while generating professional HTML5 output ready for web publishing or browser preview.

## What This Skill Does

The AI Draft Generator skill:
- **Reads** complete Microsoft Word (.docx) documents
- **Extracts** and **Analyzes** technical content from all sections
- **Converts** content into well-structured semantic HTML5
- **Preserves** document hierarchy, formatting, and technical accuracy
- **Validates** against HTML5 standards and quality requirements
- **Delivers** publication-ready HTML5 documents

## Key Features

### Content Handling
✓ Product overview, purpose, scope, and features  
✓ Functional and non-functional requirements  
✓ Technical specifications and architecture  
✓ User Interface and Configuration information  
✓ Procedures, tables, lists (ordered/unordered)  
✓ Notes, warnings, cautions, and tips  
✓ Hyperlinks and cross-references  
✓ Images (embedded or placeholder preservation)  
✓ Code snippets and technical documentation  

### HTML5 Quality
✓ Semantic HTML5 markup using standard elements  
✓ Proper heading hierarchy (h1-h6) without skipping levels  
✓ Tables with semantic structure (thead, tbody, th, td)  
✓ Accessibility-ready (screen reader compatible)  
✓ Standards-compliant (W3C HTML5 validator ready)  
✓ Browser preview ready  
✓ Publication-ready output  

### Preservation
✓ Original document structure maintained  
✓ All technical content retained  
✓ Formatting preserved (bold, italic, code, hyperlinks)  
✓ Document metadata included (title, author, version)  
✓ Logical flow and readability preserved  
✓ Cross-references converted to working internal links  

## When to Use This Skill

Use this skill when you need to:
- Convert a .docx Product Requirements document to HTML5
- Create web-publishable technical documentation from Word
- Transform specifications into browser-viewable format
- Generate standards-compliant HTML from Word documents
- Preserve document structure while changing format
- Create documentation suitable for CMS or website hosting
- Convert business requirements to technical documentation

**Trigger phrases:**
- "Convert this Word document to HTML5"
- "Generate HTML from a .docx Product Requirements document"
- "Transform a specifications document to HTML"
- "Convert Word to HTML5"
- "Create HTML5 from a docx file"

## Skill Structure

```
ai-draft-generator-docx-html5/
├── SKILL.md                           # Main skill definition
├── README.md                          # This file
├── references/
│   ├── html5-conversion-guide.md      # Detailed conversion guide
│   ├── semantic-elements.md           # HTML5 semantic elements reference
│   └── quality-checklist.md           # Quality verification checklist
├── scripts/
│   ├── convert-docx-to-html.py        # (Optional) Python conversion helper
│   └── validate-html5.py              # (Optional) HTML5 validation script
└── evals/
    └── evals.json                     # Test cases and evaluation prompts
```

## Using the Skill

### Basic Workflow

1. **Prepare your Word document** (.docx format)
   - Save in standard .docx format
   - Place in accessible location
   - Document can be in resources folder

2. **Request the conversion**
   - Ask Claude to convert your document to HTML5
   - Provide file path or upload the .docx file
   - Specify any special requirements

3. **Receive HTML5 output**
   - Get a complete HTML5 document
   - Ready for browser preview
   - Can be published directly or further customized
   - Includes all document content and metadata

### Example Usage

```
"I have a Product Requirements Document for a mobile app. Please convert 
the file 'mobile-app-prd.docx' from the resources folder into HTML5 format. 
The document has functional requirements, technical specs, warnings, and 
some tables. I need the HTML to be valid and ready for web publishing."
```

## Reference Materials

### Key References
- **[html5-conversion-guide.md](references/html5-conversion-guide.md)** — Detailed guide for Word-to-HTML5 element mapping and best practices
- **[semantic-elements.md](references/semantic-elements.md)** — Complete reference for HTML5 semantic elements
- **[quality-checklist.md](references/quality-checklist.md)** — Comprehensive quality verification checklist

### Learning Resources
- [W3C HTML5 Specification](https://html.spec.whatwg.org/)
- [MDN Web Docs - HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [HTML5 Validator](https://validator.w3.org/)

## Quality Standards

The skill ensures:
- ✓ All content from source document is preserved
- ✓ No technical information is omitted or modified
- ✓ Heading hierarchy is correct (no skipped levels)
- ✓ Semantic HTML5 elements are used appropriately
- ✓ Tables use proper semantic structure
- ✓ Lists maintain correct nesting and order
- ✓ Special elements (notes, warnings) are properly marked
- ✓ Links are functional and cross-references work
- ✓ Output passes HTML5 validation
- ✓ Document is accessible and screen-reader friendly

## Output Format

The skill delivers:
- **Format**: Complete HTML5 document (.html file)
- **Structure**: Semantic HTML5 with proper DOCTYPE, head, body
- **Metadata**: Document title, author, version, date
- **Content**: All sections from source document
- **Validation**: Standards-compliant, no validation errors
- **Readiness**: Suitable for immediate browser preview or web publishing

### Example Output Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Product Requirements Document</title>
  <meta name="author" content="...">
</head>
<body>
  <header>
    <h1>Document Title</h1>
    <p>Metadata</p>
  </header>
  
  <main>
    <section id="overview">
      <h2>Overview</h2>
      <!-- Content -->
    </section>
    <!-- More sections -->
  </main>
  
  <footer>
    <p>Footer information</p>
  </footer>
</body>
</html>
```

## Common Questions

### Q: What file formats does this skill support?
**A:** This skill is designed for Microsoft Word (.docx) files. Other formats would require conversion to .docx first.

### Q: Can the skill handle images in the Word document?
**A:** Yes. Images can be embedded in the HTML output, or image placeholders can be created with figure/figcaption elements if full embedding isn't possible.

### Q: Will the HTML5 output be styled?
**A:** The output includes semantic CSS classes (like `class="note"`, `class="warning"`) but doesn't include built-in styling. You can add CSS separately for visual styling.

### Q: Is the HTML5 output valid?
**A:** Yes, the skill generates standards-compliant HTML5 that passes W3C validation without errors.

### Q: Can I edit the HTML5 output afterward?
**A:** Yes, the output is clean, readable HTML5 that can be easily edited in any text editor or HTML editor.

### Q: How long does the conversion take?
**A:** Conversion time depends on document size and complexity. Most Product Requirements documents convert in a few minutes.

## Troubleshooting

### Issue: Complex formatting not preserved
**Solution:** The skill preserves standard Word formatting. Very complex custom formatting may need post-conversion adjustments.

### Issue: Images not appearing
**Solution:** Images may be handled as placeholders. Check the output for `<figure>` elements with image descriptions.

### Issue: Tables don't look right
**Solution:** Tables are preserved with semantic HTML structure. Visual styling requires CSS. Check table structure in HTML source.

### Issue: Links broken in output
**Solution:** External links are preserved as-is. Cross-references are converted to internal anchors. Verify all target sections exist.

## Best Practices

1. **Prepare Documents Carefully**
   - Use standard Word formatting (Heading 1, 2, 3, etc.)
   - Keep document structure clean and logical
   - Use meaningful hyperlinks

2. **Review Output**
   - Preview HTML in browser
   - Check heading hierarchy
   - Verify all tables and lists
   - Test links

3. **Post-Conversion**
   - Add CSS styling as needed
   - Test in target browsers
   - Validate with W3C validator
   - Deploy or publish as needed

## Specifications

| Aspect | Details |
|--------|---------|
| **Skill Name** | ai-draft-generator-docx-html5 |
| **Version** | 1.0 |
| **Author** | Kayalvizhi |
| **Input Format** | Microsoft Word (.docx) |
| **Output Format** | HTML5 (.html) |
| **Validation** | W3C HTML5 compliant |
| **Accessibility** | WCAG 2.1 ready |
| **Browser Support** | All modern browsers |

## Support and Feedback

For questions, issues, or suggestions:
1. Review the reference materials in the `references/` folder
2. Check the quality checklist for validation
3. Consult the conversion guide for best practices

## License

This skill is part of the TWTAI DocIntelligence DraftGen project.

---

**Last Updated:** July 1, 2026  
**Skill Version:** 1.0  
**Status:** Production Ready
