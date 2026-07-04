---
name: Table Border and Styling CSS
description: Reusable CSS for adding borders and professional styling to HTML tables in documentation
---

# Table Border and Styling Specification

This CSS provides professional table styling with borders, header differentiation, and improved readability.

## How to Use

Add the following CSS within the `<style>` tag in the `<head>` section of your HTML document:

```css
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  line-height: 1.6;
  color: #333;
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}

table th,
table td {
  border: 1px solid #999;
  padding: 12px;
  text-align: left;
}

table th {
  background-color: #f5f5f5;
  font-weight: 600;
}

table tbody tr:nth-child(odd) {
  background-color: #fafafa;
}

code {
  background-color: #f4f4f4;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: "Courier New", monospace;
}

pre {
  background-color: #f4f4f4;
  padding: 15px;
  border-radius: 5px;
  overflow-x: auto;
  border: 1px solid #ddd;
}

pre code {
  background-color: transparent;
  padding: 0;
  border-radius: 0;
}
```

## CSS Features

### Table Styling
- **Borders:** 1px solid borders on all table cells (color: #999)
- **Collapse:** `border-collapse` ensures single borders between cells
- **Margins:** 20px spacing above and below tables
- **Padding:** 12px padding in all cells for comfortable spacing

### Header Styling
- **Background Color:** Light gray (#f5f5f5) for visual distinction
- **Font Weight:** Bold (600) for emphasis

### Row Alternation
- **Odd Rows:** Light background color (#fafafa) for improved readability
- **Zebra Striping:** Alternating row colors reduce eye strain

### Code Block Styling
- **Inline Code:** Light gray background with padding and rounded corners
- **Code Blocks:** Light gray background with border and rounded corners
- **Monospace Font:** "Courier New" or monospace fallback

### Body Styling
- **Font Family:** System fonts for optimal rendering
- **Line Height:** 1.6 for comfortable reading
- **Max Width:** 900px for optimal line length
- **Responsive Padding:** 20px margins for mobile-friendly display

## Customization

To customize colors and spacing, modify these values:

| Property | Default | Purpose |
|----------|---------|---------|
| `border` (table cells) | `1px solid #999` | Table cell borders |
| `table th` background-color | `#f5f5f5` | Header background |
| `table tbody tr:nth-child(odd)` background-color | `#fafafa` | Odd row background |
| `padding` (table cells) | `12px` | Cell padding |
| `code` background-color | `#f4f4f4` | Inline code background |
| `max-width` | `900px` | Maximum document width |

## Example Implementation

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Documentation</title>
  <style>
    /* Paste the CSS above here */
  </style>
</head>
<body>
  <article>
    <!-- Your HTML content with tables -->
  </article>
</body>
</html>
```
