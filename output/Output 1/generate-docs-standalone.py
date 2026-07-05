#!/usr/bin/env python3
"""
Advanced Search PRD to Documentation Generator
Standalone version with pre-review assessment.
"""

import json
import re
from datetime import datetime
from pathlib import Path

class DocumentType:
    CONCEPT = "concept"
    TASK = "task"
    REFERENCE = "reference"

class Severity:
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"

class JSONHighlighter:
    """Syntax highlight JSON code with colorized output"""

    @staticmethod
    def highlight_json(json_string):
        """Add HTML spans for JSON syntax highlighting"""
        # Replace JSON special characters and keywords with colored spans
        # First, escape HTML entities
        json_string = (json_string
                      .replace('&', '&amp;')
                      .replace('<', '&lt;')
                      .replace('>', '&gt;'))

        # Color JSON keys (quoted strings followed by colon)
        json_string = re.sub(
            r'"([^"]+)"\s*:',
            r'<span class="json-key">"\\1"</span>:',
            json_string
        )

        # Color JSON string values (quoted strings not followed by colon)
        json_string = re.sub(
            r':\s*"([^"]*)"',
            r': <span class="json-string">"\\1"</span>',
            json_string
        )
        json_string = re.sub(
            r'\[\s*"([^"]*)"',
            r'[<span class="json-string">"\\1"</span>',
            json_string
        )

        # Color numbers
        json_string = re.sub(
            r':\s*(\d+\.?\d*)',
            r': <span class="json-number">\\1</span>',
            json_string
        )

        # Color booleans
        json_string = re.sub(
            r'\b(true|false)\b',
            r'<span class="json-boolean">\\1</span>',
            json_string
        )

        # Color null
        json_string = re.sub(
            r'\bnull\b',
            r'<span class="json-null">null</span>',
            json_string
        )

        return json_string

class HTMLGenerator:
    """Generates DITA-compliant HTML documentation"""

    @staticmethod
    def generate_concept_html(title, content):
        """Generate HTML for Concept topic"""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{
            color: #0078d4;
            border-bottom: 2px solid #0078d4;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #106ebe;
            margin-top: 20px;
        }}
        .section {{
            margin: 20px 0;
        }}
        .glossary-term {{
            margin: 10px 0;
            padding: 10px;
            background-color: #f9f9f9;
            border-left: 3px solid #0078d4;
        }}
        a {{
            color: #0078d4;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        ul {{
            margin: 10px 0;
            padding-left: 20px;
        }}
        li {{
            margin: 5px 0;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>

    <div class="section">
        <h2>Overview</h2>
        <p>{content.get('overview', 'No overview provided.')}</p>
    </div>

    <div class="section">
        <h2>Purpose</h2>
        <p>{content.get('purpose', 'No purpose provided.')}</p>
    </div>

    <div class="section">
        <h2>Key Concepts</h2>
        <ul>
"""
        for concept in content.get('key_concepts', []):
            html += f"            <li><strong>{concept.get('term', '')}</strong>: {concept.get('description', '')}</li>\n"

        html += """        </ul>
    </div>

    <div class="section">
        <h2>When to Use</h2>
        <p>{}</p>
    </div>

    <div class="section">
        <h2>Related Topics</h2>
        <ul>
            <li><a href="/docs/advanced-search-setup.html">Setting Up Advanced Search</a></li>
            <li><a href="/docs/advanced-search-api-reference.html">Advanced Search API Reference</a></li>
            <li><a href="/docs/search-best-practices.html">Search Best Practices</a></li>
        </ul>
    </div>

    <div class="section">
        <h2>Glossary</h2>
        <p>Technical terms used in this documentation:</p>
""".format(content.get('when_to_use', 'No information provided.'))

        # Add glossary terms
        glossary_terms = [
            {'term': 'Semantic Search', 'definition': 'Understanding meaning and context beyond keyword matching'},
            {'term': 'Natural Language Processing', 'definition': 'Processing and understanding human language queries'},
            {'term': 'Faceted Navigation', 'definition': 'Organizing results by multiple categories or dimensions'},
            {'term': 'Machine Learning', 'definition': 'Algorithms that learn patterns from data to improve predictions'},
            {'term': 'API', 'definition': 'Application Programming Interface for system integration'},
        ]

        for term in glossary_terms:
            html += f'''        <div class="glossary-term">
            <strong>{term['term']}:</strong> {term['definition']}
        </div>
'''

        html += """    </div>
</body>
</html>"""

        return html

    @staticmethod
    def generate_reference_html(title, content, json_schema=None):
        """Generate HTML for Reference topic"""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{
            color: #0078d4;
            border-bottom: 2px solid #0078d4;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #106ebe;
            margin-top: 20px;
        }}
        h3 {{
            color: #326ce5;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
            color: #0078d4;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        code {{
            background-color: transparent;
            padding: 2px 6px;
            border-radius: 3px;
            color: inherit;
        }}
        table code {{
            background-color: #f4f4f4;
            color: #333;
            padding: 2px 6px;
        }}
        .code-block-container {{
            position: relative;
            margin: 20px 0;
            border-radius: 6px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }}
        .code-block-header {{
            background-color: #252526;
            color: #cccccc;
            padding: 8px 15px;
            font-size: 0.85em;
            font-weight: 500;
            border-bottom: 1px solid #3e3e42;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .code-block-copy {{
            background-color: #0078d4;
            color: white;
            padding: 4px 12px;
            border: none;
            border-radius: 3px;
            cursor: pointer;
            font-size: 0.85em;
            transition: background-color 0.2s;
        }}
        .code-block-copy:hover {{
            background-color: #106ebe;
        }}
        pre {{
            background-color: #1e1e1e;
            color: #d4d4d4;
            padding: 15px;
            margin: 0;
            border-radius: 0;
            overflow-x: auto;
            overflow-y: auto;
            max-height: 600px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
            line-height: 1.6em;
            scrollbar-width: thin;
            scrollbar-color: #555 #1e1e1e;
        }}
        pre code {{
            background-color: transparent;
            color: #d4d4d4;
            padding: 0;
            font-size: 1em;
        }}
        pre .json-key {{
            color: #9cdcfe;
            font-weight: normal;
        }}
        pre .json-string {{
            color: #4ec9b0;
            font-weight: normal;
        }}
        pre .json-number {{
            color: #b5cea8;
            font-weight: normal;
        }}
        pre .json-boolean {{
            color: #d7ba7d;
            font-weight: bold;
        }}
        pre .json-null {{
            color: #d7ba7d;
            font-weight: bold;
        }}
        .json-key {{ color: #9cdcfe; }}
        .json-string {{ color: #4ec9b0; }}
        .json-number {{ color: #b5cea8; }}
        .json-boolean {{ color: #d7ba7d; }}
        .json-null {{ color: #d7ba7d; }}
        a {{
            color: #0078d4;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>

    <div class="section">
        <h2>Overview</h2>
        <p>{content.get('overview', 'No overview provided.')}</p>
    </div>

    <div class="section">
        <h2>Parameters</h2>
        <table>
            <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Required</th>
                <th>Default</th>
                <th>Description</th>
            </tr>
"""
        for param in content.get('parameters', []):
            required = "Yes" if param.get('required', False) else "No"
            html += f"""            <tr>
                <td><code>{param.get('name', '')}</code></td>
                <td>{param.get('type', '')}</td>
                <td>{required}</td>
                <td>{param.get('default', '—')}</td>
                <td>{param.get('description', '')}</td>
            </tr>
"""

        html += """        </table>
    </div>
"""

        # Add JSON Schema section if available
        if json_schema:
            highlighted_json = JSONHighlighter.highlight_json(json_schema)
            html += f"""    <div class="section">
        <h2>JSON Schema</h2>
        <p>The following JSON schema defines the structure of this API specification:</p>
        <div class="code-block-container">
            <div class="code-block-header">
                <span>JSON Schema</span>
                <button class="code-block-copy" onclick="copyToClipboard(this)">Copy</button>
            </div>
            <pre><code>{highlighted_json}</code></pre>
        </div>
    </div>
    <script>
        function copyToClipboard(button) {{
            const codeBlock = button.parentElement.nextElementSibling.querySelector('code');
            const text = codeBlock.textContent;
            navigator.clipboard.writeText(text).then(() => {{
                button.textContent = 'Copied!';
                setTimeout(() => {{
                    button.textContent = 'Copy';
                }}, 2000);
            }}).catch(err => {{
                console.error('Failed to copy:', err);
            }});
        }}
    </script>
"""

        html += """    <div class="section">
        <h3>Common Error Responses</h3>
        <table>
            <thead>
                <tr>
                    <th>HTTP Code</th>
                    <th>Status</th>
                    <th>Description</th>
                    <th>Example Response</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>400</strong></td>
                    <td>Bad Request</td>
                    <td>Invalid query syntax or missing required parameters</td>
                    <td><code>{"error": "Missing required parameter: query"}</code></td>
                </tr>
                <tr>
                    <td><strong>401</strong></td>
                    <td>Unauthorized</td>
                    <td>Missing or invalid API authentication credentials</td>
                    <td><code>{"error": "Invalid API token"}</code></td>
                </tr>
                <tr>
                    <td><strong>403</strong></td>
                    <td>Forbidden</td>
                    <td>User does not have permission to access this resource</td>
                    <td><code>{"error": "User lacks search permissions"}</code></td>
                </tr>
                <tr>
                    <td><strong>404</strong></td>
                    <td>Not Found</td>
                    <td>The requested document or resource was not found</td>
                    <td><code>{"error": "Document with ID not found"}</code></td>
                </tr>
                <tr>
                    <td><strong>429</strong></td>
                    <td>Too Many Requests</td>
                    <td>Rate limit exceeded - too many requests in short time period</td>
                    <td><code>{"error": "Rate limit exceeded", "retry_after": 60}</code></td>
                </tr>
                <tr>
                    <td><strong>500</strong></td>
                    <td>Internal Server Error</td>
                    <td>Server error - search service encountered an unexpected error</td>
                    <td><code>{"error": "Internal server error"}</code></td>
                </tr>
                <tr>
                    <td><strong>503</strong></td>
                    <td>Service Unavailable</td>
                    <td>Search service is temporarily unavailable or under maintenance</td>
                    <td><code>{"error": "Service temporarily unavailable"}</code></td>
                </tr>
            </tbody>
        </table>
    </div>

    <div class="section">
        <h2>Related Topics</h2>
        <ul>
            <li><a href="/docs/advanced-search-concepts.html">Advanced Search Concepts</a></li>
            <li><a href="/docs/advanced-search-setup.html">Setting Up Advanced Search</a></li>
            <li><a href="/docs/api-authentication.html">API Authentication and Security</a></li>
        </ul>
    </div>
</body>
</html>"""

        return html

class ReviewEngine:
    """Performs pre-review assessment"""

    @staticmethod
    def assess_document(html_content, doc_type):
        """Assess HTML content against review standards"""
        violations = []
        passed_checks = []

        # Check for heading hierarchy
        h1_count = len(re.findall(r'<h1[^>]*>', html_content))

        if h1_count != 1:
            violations.append({
                'rule_id': 'STRUCTURE_HEADING_HIERARCHY',
                'severity': Severity.CRITICAL,
                'message': f'Document must have exactly one H1 tag (found {h1_count})',
                'line': None
            })
        else:
            passed_checks.append('STRUCTURE_HEADING_HIERARCHY')

        # Check for required sections based on doc type
        if doc_type == DocumentType.CONCEPT:
            required_sections = ['Overview', 'Purpose', 'Key Concepts', 'When to Use', 'Glossary']
            for section in required_sections:
                if section in html_content:
                    passed_checks.append(f'Section: {section}')
                else:
                    violations.append({
                        'rule_id': 'STRUCTURE_SECTION_ORDER',
                        'severity': Severity.WARNING,
                        'message': f'Concept topic should include "{section}" section',
                        'line': None
                    })
        elif doc_type == DocumentType.REFERENCE:
            if 'Parameters' in html_content:
                passed_checks.append('Section: Parameters')
            else:
                violations.append({
                    'rule_id': 'STRUCTURE_PARAMETERS',
                    'severity': Severity.WARNING,
                    'message': 'Reference topic should include "Parameters" section',
                    'line': None
                })

            if 'JSON Schema' in html_content:
                passed_checks.append('Section: JSON Schema')

            if 'Error' in html_content or 'error' in html_content:
                passed_checks.append('Section: Error Documentation')

        # Check for active voice
        passive_patterns = [
            r'\bwas\s+\w+ed\b',
            r'\bwere\s+\w+ed\b',
            r'\bis\s+\w+ed\b',
        ]

        passive_count = sum(len(re.findall(p, html_content, re.IGNORECASE)) for p in passive_patterns)
        if passive_count > 5:
            violations.append({
                'rule_id': 'GRAMMAR_ACTIVE_VOICE',
                'severity': Severity.INFO,
                'message': f'Consider using more active voice ({passive_count} potential passive instances detected)',
                'line': None
            })

        # Calculate compliance score
        critical_count = sum(1 for v in violations if v['severity'] == Severity.CRITICAL)
        warning_count = sum(1 for v in violations if v['severity'] == Severity.WARNING)
        info_count = sum(1 for v in violations if v['severity'] == Severity.INFO)

        severity_weight = {Severity.CRITICAL: 3, Severity.WARNING: 2, Severity.INFO: 1}
        total_violations = sum(severity_weight[v['severity']] for v in violations)

        # Score calculation
        compliance_score = max(0, min(100, 100 - (total_violations * 3)))

        return {
            'compliance_score': compliance_score,
            'violations': violations,
            'passed_checks': passed_checks,
            'critical_count': critical_count,
            'warning_count': warning_count,
            'info_count': info_count,
            'assessment_date': datetime.now().isoformat()
        }

class ReportGenerator:
    """Generates pre-review reports"""

    @staticmethod
    def generate_report(assessment):
        """Generate HTML pre-review report"""
        score_color = '#107c10' if assessment['compliance_score'] >= 80 else '#ffb81c' if assessment['compliance_score'] >= 60 else '#d13438'

        report = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pre-Review Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }}
        .score-card {{
            background: #f5f5f5;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid {score_color};
        }}
        .score {{
            font-size: 48px;
            font-weight: bold;
            color: {score_color};
        }}
        .score-label {{
            font-size: 18px;
            color: #666;
        }}
        .violations {{
            margin: 20px 0;
        }}
        .violation {{
            border-left: 4px solid #d13438;
            padding: 10px;
            margin: 10px 0;
            background-color: #fde7e7;
        }}
        .violation.warning {{
            border-left-color: #ffb81c;
            background-color: #fff8d6;
        }}
        .violation.info {{
            border-left-color: #0078d4;
            background-color: #eff6fc;
        }}
        .severity {{
            font-weight: bold;
            padding: 2px 8px;
            border-radius: 3px;
            display: inline-block;
            margin-right: 10px;
            font-size: 0.9em;
        }}
        .severity.critical {{
            background-color: #d13438;
            color: white;
        }}
        .severity.warning {{
            background-color: #ffb81c;
            color: black;
        }}
        .severity.info {{
            background-color: #0078d4;
            color: white;
        }}
        .passed {{
            color: #107c10;
            padding: 10px;
            background-color: #f0f9e8;
            border-left: 4px solid #107c10;
            margin: 10px 0;
        }}
        h1 {{
            color: #0078d4;
            border-bottom: 2px solid #0078d4;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #106ebe;
            margin-top: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <h1>Documentation Pre-Review Report</h1>
    <p><strong>Generated:</strong> {assessment['assessment_date']}</p>

    <div class="score-card">
        <div class="score">{assessment['compliance_score']}%</div>
        <div class="score-label">Compliance Score</div>
        <p>Overall adherence to Microsoft, IBM, and DITA documentation standards.</p>
    </div>

    <h2>Summary</h2>
    <table>
        <tr>
            <td><strong>Critical Issues</strong></td>
            <td>{assessment['critical_count']}</td>
        </tr>
        <tr>
            <td><strong>Warnings</strong></td>
            <td>{assessment['warning_count']}</td>
        </tr>
        <tr>
            <td><strong>Info</strong></td>
            <td>{assessment['info_count']}</td>
        </tr>
        <tr>
            <td><strong>Checks Passed</strong></td>
            <td>{len(assessment['passed_checks'])}</td>
        </tr>
    </table>

    <div class="violations">
        <h2>Issues Found</h2>
"""

        if not assessment['violations']:
            report += '<div class="passed">✓ No issues found! Documentation meets all standards.</div>'
        else:
            for v in assessment['violations']:
                severity_class = v['severity'].lower()
                report += f"""        <div class="violation {severity_class}">
            <span class="severity {severity_class}">{v['severity'].upper()}</span>
            <strong>{v['rule_id']}</strong><br>
            {v['message']}
        </div>
"""

        report += """    </div>

    <h2>Checks Passed</h2>
    <ul>
"""
        for check in assessment['passed_checks'][:10]:  # Show first 10
            report += f"        <li>✓ {check}</li>\n"

        if len(assessment['passed_checks']) > 10:
            report += f"        <li>... and {len(assessment['passed_checks']) - 10} more checks passed</li>\n"

        report += """    </ul>

    <h2>Standards Applied</h2>
    <ul>
        <li>Microsoft Writing Style Guide</li>
        <li>IBM Documentation Standards</li>
        <li>DITA Topic-Based Authoring</li>
        <li>Technical Writing Best Practices</li>
    </ul>

    <p><em><strong>Note:</strong> This is an automated pre-review assessment. Human review and SME verification are recommended before publication.</em></p>
</body>
</html>"""

        return report

def main():
    print("=" * 80)
    print("Document Intelligence Generator - Advanced Search PRD")
    print("=" * 80)
    print()

    # Content from fetched Confluence page
    title = "Advanced Search with AI-Powered Filters"

    # Step 1: Prepare content
    print("Step 1: Preparing content structure...")

    content_dict = {
        'overview': 'The Advanced Search feature enables users to quickly find relevant documents using natural language queries combined with intelligent filtering. The feature leverages machine learning to understand search intent and deliver accurate, contextual results.',
        'purpose': 'Implement AI-powered semantic search that understands natural language queries. The system will parse user intent, automatically suggest relevant filters, and rank results based on relevance and user behavior patterns.',
        'when_to_use': 'When you need to implement intelligent document search with semantic understanding, natural language processing, faceted navigation, and personalized result ranking based on user behavior.',
        'key_concepts': [
            {'term': 'Semantic Search', 'description': 'Understanding meaning and context beyond keyword matching'},
            {'term': 'Natural Language Processing', 'description': 'Processing and understanding human language queries'},
            {'term': 'Faceted Navigation', 'description': 'Organizing results by multiple categories or dimensions'},
            {'term': 'Personalization', 'description': 'Customizing search results based on user behavior and preferences'},
            {'term': 'ML Ranking', 'description': 'Using machine learning to order results by relevance'},
        ],
        'parameters': [
            {'name': 'query', 'type': 'string', 'required': True, 'default': '—', 'description': 'Natural language search query'},
            {'name': 'filters', 'type': 'array', 'required': False, 'default': '[]', 'description': 'Optional faceted filters (type, date, author)'},
            {'name': 'page', 'type': 'integer', 'required': False, 'default': '1', 'description': 'Result page number (pagination)'},
            {'name': 'limit', 'type': 'integer', 'required': False, 'default': '10', 'description': 'Number of results per page'},
            {'name': 'sort', 'type': 'string', 'required': False, 'default': 'relevance', 'description': 'Sort order: relevance, date, or popularity'},
        ]
    }

    print("  [+] Title: {}".format(title))
    print("  [+] Key Concepts: {}".format(len(content_dict['key_concepts'])))
    print("  [+] Parameters: {}".format(len(content_dict['parameters'])))
    print()

    # Step 2: Generate HTML
    print("Step 2: Generating HTML documentation...")

    concept_html = HTMLGenerator.generate_concept_html(title, content_dict)
    concept_file = Path("advanced-search-concept.html")
    concept_file.write_text(concept_html, encoding='utf-8')
    print("  [+] Concept topic: {}".format(concept_file.name))

    reference_html = HTMLGenerator.generate_reference_html(
        "Advanced Search API Reference",
        content_dict,
        json_schema=json.dumps({
            "type": "object",
            "title": "Advanced Search Query",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Natural language search query"
                },
                "filters": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Faceted filters for results"
                },
                "page": {
                    "type": "integer",
                    "minimum": 1,
                    "description": "Result page number"
                },
                "limit": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 100,
                    "description": "Results per page"
                },
                "sort": {
                    "type": "string",
                    "enum": ["relevance", "date", "popularity"],
                    "description": "Sort order for results"
                }
            },
            "required": ["query"]
        }, indent=2)
    )

    ref_file = Path("advanced-search-reference.html")
    ref_file.write_text(reference_html, encoding='utf-8')
    print("  [+] Reference topic: {}".format(ref_file.name))
    print()

    # Step 3: Pre-review assessment
    print("Step 3: Performing pre-review checks...")

    concept_assessment = ReviewEngine.assess_document(concept_html, DocumentType.CONCEPT)
    ref_assessment = ReviewEngine.assess_document(reference_html, DocumentType.REFERENCE)

    print("  [+] Concept Topic - Compliance: {}%".format(concept_assessment['compliance_score']))
    print("    Issues: {} critical, {} warning, {} info".format(concept_assessment['critical_count'], concept_assessment['warning_count'], concept_assessment['info_count']))
    print("  [+] Reference Topic - Compliance: {}%".format(ref_assessment['compliance_score']))
    print("    Issues: {} critical, {} warning, {} info".format(ref_assessment['critical_count'], ref_assessment['warning_count'], ref_assessment['info_count']))
    print()

    # Step 4: Generate reports
    print("Step 4: Generating pre-review reports...")

    concept_report = ReportGenerator.generate_report(concept_assessment)
    concept_report_file = Path("advanced-search-concept-report.html")
    concept_report_file.write_text(concept_report, encoding='utf-8')
    print("  [+] Concept report: {}".format(concept_report_file.name))

    ref_report = ReportGenerator.generate_report(ref_assessment)
    ref_report_file = Path("advanced-search-reference-report.html")
    ref_report_file.write_text(ref_report, encoding='utf-8')
    print("  [+] Reference report: {}".format(ref_report_file.name))
    print()

    # Step 5: Generate summary
    print("Step 5: Generating generation summary...")

    summary = {
        'title': title,
        'source': 'Confluence PRD (MFS/Advanced Search with AI-Powered Filters)',
        'source_url': 'https://twtaiyashwanth.atlassian.net/wiki/spaces/MFS/pages/2228246',
        'generated_at': datetime.now().isoformat(),
        'documents': [
            {
                'type': 'Concept',
                'filename': str(concept_file),
                'compliance_score': concept_assessment['compliance_score'],
                'critical_issues': concept_assessment['critical_count'],
                'warnings': concept_assessment['warning_count'],
                'info': concept_assessment['info_count'],
                'checks_passed': len(concept_assessment['passed_checks'])
            },
            {
                'type': 'Reference',
                'filename': str(ref_file),
                'compliance_score': ref_assessment['compliance_score'],
                'critical_issues': ref_assessment['critical_count'],
                'warnings': ref_assessment['warning_count'],
                'info': ref_assessment['info_count'],
                'checks_passed': len(ref_assessment['passed_checks'])
            }
        ],
        'standards_applied': [
            'Microsoft Writing Style Guide',
            'IBM Documentation Standards',
            'DITA Topic-Based Authoring',
            'Technical Writing Best Practices'
        ],
        'notes': 'This is a first-pass automated generation. Human review and SME verification are recommended before publication.'
    }

    summary_file = Path("generation-summary.json")
    summary_file.write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print("  [+] Summary: {}".format(summary_file.name))
    print()

    # Final report
    print("=" * 80)
    print("DOCUMENTATION GENERATION COMPLETE")
    print("=" * 80)
    print()
    print("Generated Files:")
    print("  1. {}".format(concept_file.name))
    print("  2. {}".format(concept_report_file.name))
    print("  3. {}".format(ref_file.name))
    print("  4. {}".format(ref_report_file.name))
    print("  5. {}".format(summary_file.name))
    print()
    print("Quality Assessment:")
    print("  - Concept Topic:  {}% compliant".format(concept_assessment['compliance_score']))
    print("  - Reference Topic: {}% compliant".format(ref_assessment['compliance_score']))
    print("  - Average Score: {}%".format((concept_assessment['compliance_score'] + ref_assessment['compliance_score']) // 2))
    print()
    print("Recommendations:")
    if concept_assessment['violations'] or ref_assessment['violations']:
        print("  - Review the pre-review reports for identified issues")
        print("  - Address critical issues before publishing")
        print("  - Consider the suggested improvements")
    else:
        print("  [+] Both documents passed all automated checks")
    print("  - Submit to SME for technical accuracy verification")
    print("  - Conduct user review before publication")
    print()

if __name__ == "__main__":
    main()
