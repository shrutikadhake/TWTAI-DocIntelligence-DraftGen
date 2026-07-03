---
name: api-docs-generator
description: Convert unstructured developer API notes into professional, semantic HTML5 API documentation. Use this skill whenever a user provides raw API specifications, informal endpoint descriptions, or free-form developer notes and wants to transform them into publishable HTML documentation. The skill extracts endpoint details, request parameters, responses, and authentication methods from plain-text, markdown, or partially-structured notes and generates a standalone, browser-ready HTML5 page following the Microsoft Writing Style Guide. Triggers on phrases like "convert these API notes to HTML", "generate API documentation from these notes", "create a documentation page from this specification", or when the user shares raw API information and wants structured output.
compatibility: Read, Write, Edit (for file operations)
---

## Purpose

Transform unstructured API notes into professional, semantic HTML5 documentation suitable for publication with minimal editing. Extract key information and present it in a clear, structured format following Microsoft Writing Style Guide principles.

## What This Skill Does

1. **Extracts API information** from free-form notes:
   - API name
   - HTTP method
   - Endpoint URL
   - Authentication method
   - Request parameters
   - Success responses
   - Error responses
   - Constraints or additional notes

2. **Generates semantic HTML5** with:
   - Proper document structure (`<!DOCTYPE>`, `<html>`, `<head>`, `<body>`)
   - Accessible headings and sections
   - Semantic HTML5 tables (`<table>`, `<thead>`, `<tbody>`)
   - CSS classes for styling: `api-parameters`, `api-success-responses`, `api-error-responses`
   - Basic inline CSS for readability

3. **Applies Microsoft Writing Style Guide principles**:
   - Active voice where possible
   - Clear, direct language
   - Consistent terminology
   - Concise descriptions

4. **Preserves information exactly**: Does not invent missing details. If a section is absent from the source notes (e.g., authentication, error responses), omit that section from the HTML rather than adding placeholders.

## How to Use This Skill

When a user provides API notes in any format (plain text, markdown, bulleted lists, or mixed structure), follow these steps:

### Step 1: Parse the Input

Read the provided notes and identify sections. Look for:
- API name or endpoint title
- HTTP method (GET, POST, PUT, DELETE, PATCH, etc.)
- Endpoint path or URL
- Authentication requirements
- Request parameters (query, body, headers)
- Success response(s)
- Error response(s)
- Constraints, rate limits, or additional notes

Do not assume structure. Extract what's explicitly stated. If a section is missing, note it but do not invent data.

### Step 2: Generate HTML

Generate a complete standalone HTML5 document containing:

- <!DOCTYPE html>
- html
- head
- body

The document should contain:

- API title
- Endpoint section
- Description section (if present)
- Authentication section (if present)
- Request parameters table
- Success responses table
- Error responses table
- Notes section (if present)

Use semantic HTML5 elements and include basic CSS styling for readability.

### Step 3: Apply Microsoft Writing Style Guide

Use the Microsoft Docs plugin to apply the Microsoft Writing Style Guide.

Apply Microsoft recommendations for:
- voice and tone
- terminology
- active voice
- sentence case
- technical writing conventions

### Step 4: Render and Save

Save the HTML to a file and ensure it is immediately viewable in a browser. The document should be publication-ready with minimal further editing.

## Important Guidelines

- **Do not invent information.** If the source notes do not mention authentication, do not add an Authentication section. If error responses are not described, omit that section.   Do not generate example payloads unless explicitly provided.
- **Preserve exact details.** If the source specifies "Bearer token" or "API key in header", preserve that exact wording.
- **Tables over prose.** Render parameters, responses, and errors as tables for clarity and scannability.
- **One endpoint per document.** If notes describe multiple endpoints, generate separate HTML documents.
- **Semantic HTML.** Use proper HTML5 semantics: `<table>`, `<thead>`, `<tbody>`, `<code>`, `<h1>`–`<h6>` for hierarchy.

## Example

**Input (unstructured notes):**
```
User Service API

Gets information about a user by their ID.

GET /users/{id}

Authentication: Bearer token required in Authorization header

Parameters:
- id (path, required) - The unique user identifier
- include_profile (query, optional) - Set to true to include profile data

Returns:
200 response with user object:
{ "id": "123", "name": "John Doe", "email": "john@example.com" }

Errors:
404 - User not found
401 - Unauthorized
```

**Output:** 

## Output Formatting

Request parameters must always be rendered as HTML tables.

Columns:
- Parameter
- Type
- Description
- Required

Success responses must always be rendered as HTML tables.

Columns:
- HTTP Status Code
- Description

Error responses must always be rendered as HTML tables.

Columns:
- HTTP Status Code
- Error Description
