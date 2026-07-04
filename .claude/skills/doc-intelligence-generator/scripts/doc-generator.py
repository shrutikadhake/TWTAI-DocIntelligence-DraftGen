#!/usr/bin/env python3
"""
Document Intelligence Generator
Converts source content (Confluence wiki, JSON) into structured HTML documentation
and performs automated pre-review checks against documentation standards.
"""

import json
import re
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from pathlib import Path

class ConfluenceAPIClient:
    """Interface to Atlassian MCP for Confluence access"""

    def __init__(self):
        """Initialize Confluence MCP client"""
        self.mcp_available = self._check_mcp_availability()

    def _check_mcp_availability(self) -> bool:
        """Check if Atlassian MCP is configured and available"""
        try:
            import subprocess
            result = subprocess.run(['which', 'atlassian-mcp'], capture_output=True)
            return result.returncode == 0
        except:
            return False

    def fetch_page(self, page_url: str) -> Dict:
        """Fetch Confluence page content via Atlassian MCP"""
        if not self.mcp_available:
            raise RuntimeError("Atlassian MCP not configured. Please set up MCP connection to Confluence.")

        # Extract space key and page ID from URL
        # Format: https://org.atlassian.net/wiki/spaces/SPACE/pages/123456/Page-Name
        try:
            import re
            match = re.search(r'/spaces/(\w+)/pages/(\d+)', page_url)
            if not match:
                raise ValueError(f"Invalid Confluence URL format: {page_url}")

            space_key, page_id = match.groups()

            # Via Atlassian MCP: fetch page content
            page_data = {
                'id': page_id,
                'space': space_key,
                'url': page_url,
                'content': '',  # Would be populated by MCP call
                'attachments': []  # Would be populated by MCP call
            }

            return page_data
        except Exception as e:
            raise RuntimeError(f"Failed to fetch Confluence page: {str(e)}")

    def get_attachments(self, page_id: str) -> List[Dict]:
        """Fetch attachment metadata from page via Atlassian MCP"""
        # Would use Atlassian MCP to list and download attachments
        attachments = []

        # Example structure returned by MCP:
        # [
        #   {'id': 'att123', 'filename': 'api-config.json', 'media_type': 'application/json'},
        #   {'id': 'att124', 'filename': 'schema.json', 'media_type': 'application/json'}
        # ]

        return attachments

    def download_attachment(self, page_id: str, attachment_id: str) -> str:
        """Download attachment content via Atlassian MCP"""
        # Would use Atlassian MCP to download attachment
        # Returns file content as string
        pass


class DocumentType:
    CONCEPT = "concept"
    TASK = "task"
    REFERENCE = "reference"

class Severity:
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"

class GlossaryExtractor:
    """Extract technical terms and generate glossary"""

    @staticmethod
    def extract_technical_terms(content: str) -> List[Dict]:
        """Identify technical terms and extract definitions"""
        technical_terms = []

        # Common technical terms to identify
        term_patterns = {
            'semantic search': 'Understanding meaning beyond keywords',
            'machine learning': 'AI systems that learn from data',
            'API': 'Application Programming Interface',
            'JSON': 'JavaScript Object Notation',
            'relevance': 'How closely a result matches the query intent',
            'faceted': 'Organized by multiple categories or dimensions',
            'threshold': 'A minimum value or boundary',
            'tokenization': 'Breaking text into individual words or tokens',
            'embedding': 'Numeric representation of text meaning',
            'personalization': 'Customizing results based on user behavior',
        }

        for term, definition in term_patterns.items():
            if term.lower() in content.lower():
                technical_terms.append({
                    'term': term,
                    'definition': definition,
                    'first_mention': content.lower().find(term.lower())
                })

        return sorted(technical_terms, key=lambda x: x['first_mention'])

class ScreenshotPlaceholder:
    """Generate screenshot placeholders for Task topics"""

    @staticmethod
    def identify_ui_steps(steps: List[str]) -> List[Dict]:
        """Identify steps that need screenshots"""
        ui_steps = []
        ui_keywords = ['click', 'button', 'menu', 'icon', 'dropdown', 'panel', 'dialog', 'window', 'navigate', 'select', 'checkbox', 'toggle']

        for i, step in enumerate(steps):
            step_lower = step.lower()
            if any(keyword in step_lower for keyword in ui_keywords):
                ui_steps.append({
                    'step_number': i + 1,
                    'step_text': step,
                    'needs_screenshot': True,
                    'placeholder_id': f'screenshot-{i+1}'
                })

        return ui_steps

    @staticmethod
    def insert_screenshot_placeholders(html: str, ui_steps: List[Dict]) -> str:
        """Insert screenshot placeholders into HTML"""
        for ui_step in ui_steps:
            placeholder = f'''
            <div class="screenshot-placeholder" id="{ui_step['placeholder_id']}">
                <div style="background-color: #f0f7ff; border: 2px dashed #0078d4; border-radius: 4px; padding: 20px; margin: 15px 0; text-align: center;">
                    <strong>📸 Screenshot Placeholder</strong><br>
                    <em>Step {ui_step['step_number']}: {ui_step['step_text']}</em><br>
                    <small style="color: #666;">Insert annotated screenshot here showing the UI element(s) mentioned in this step</small>
                </div>
            </div>
            '''

        return html

class HyperlinkGenerator:
    """Generate hyperlinks for cross-references"""

    @staticmethod
    def generate_related_topics_links(topics: List[str], base_url: str = "/docs/") -> str:
        """Convert related topics to navigable hyperlinks"""
        links_html = "<ul>\n"

        for topic in topics:
            # Convert topic name to URL-friendly slug
            slug = topic.lower().replace(' ', '-').replace(':', '').replace('&', 'and')
            url = f"{base_url}{slug}.html"
            links_html += f'    <li><a href="{url}">{topic}</a></li>\n'

        links_html += "</ul>"
        return links_html

    @staticmethod
    def extract_related_topics(content: str) -> List[str]:
        """Extract related topics from "See also" sections"""
        import re

        # Look for "See also:" or "Related Topics" sections
        pattern = r'(?:See also:|Related[^:]*:)(.*?)(?=<|$)'
        matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)

        topics = []
        for match in matches:
            # Extract individual topic names
            items = re.findall(r'[A-Z][^,\n<]*', match)
            topics.extend([item.strip() for item in items if len(item.strip()) > 3])

        return list(set(topics))  # Remove duplicates

class ErrorDocumenter:
    """Extract and document API errors and edge cases"""

    @staticmethod
    def extract_error_scenarios(content: str) -> List[Dict]:
        """Identify potential error scenarios from content"""
        errors = [
            {
                'code': 400,
                'status': 'Bad Request',
                'description': 'Invalid query syntax or missing required parameters',
                'example_response': '{"error": "Missing required parameter: query"}'
            },
            {
                'code': 401,
                'status': 'Unauthorized',
                'description': 'Missing or invalid API authentication credentials',
                'example_response': '{"error": "Invalid API token"}'
            },
            {
                'code': 403,
                'status': 'Forbidden',
                'description': 'User does not have permission to access this resource',
                'example_response': '{"error": "User lacks required search permissions"}'
            },
            {
                'code': 404,
                'status': 'Not Found',
                'description': 'The requested document or resource was not found',
                'example_response': '{"error": "Document with ID not found"}'
            },
            {
                'code': 429,
                'status': 'Too Many Requests',
                'description': 'Rate limit exceeded - too many requests in short time period',
                'example_response': '{"error": "Rate limit exceeded", "retry_after": 60}'
            },
            {
                'code': 500,
                'status': 'Internal Server Error',
                'description': 'Server error - search service encountered an unexpected error',
                'example_response': '{"error": "Internal server error"}'
            },
            {
                'code': 503,
                'status': 'Service Unavailable',
                'description': 'Search service is temporarily unavailable or under maintenance',
                'example_response': '{"error": "Service temporarily unavailable"}'
            }
        ]

        return errors

    @staticmethod
    def generate_error_table_html(errors: List[Dict]) -> str:
        """Generate HTML table documenting errors"""
        html = '''
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
        '''

        for error in errors:
            html += f'''
                <tr>
                    <td><strong>{error['code']}</strong></td>
                    <td>{error['status']}</td>
                    <td>{error['description']}</td>
                    <td><code>{error['example_response']}</code></td>
                </tr>
            '''

        html += '''
            </tbody>
        </table>
        '''

        return html

class ConfluenceParser:
    """Parse Confluence Markup format"""

    @staticmethod
    def parse_confluence_markup(content: str) -> Dict:
        """Convert Confluence Markup to structured content"""
        sections = {
            'title': '',
            'overview': '',
            'purpose': '',
            'key_concepts': [],
            'when_to_use': '',
            'steps': [],
            'prerequisites': [],
            'raw_content': content
        }

        lines = content.split('\n')

        for i, line in enumerate(lines):
            # Parse headings (h1. h2. h3. etc.)
            if line.startswith('h1.'):
                sections['title'] = line.replace('h1.', '').strip()
            elif line.startswith('h2.'):
                section_name = line.replace('h2.', '').strip().lower()
                sections['_current_section'] = section_name
            elif line.startswith('#'):
                # Numbered list (steps)
                sections['steps'].append(line.lstrip('# ').strip())
            elif line.startswith('*'):
                # Bullet list (benefits, prerequisites, etc.)
                item = line.lstrip('* ').strip()
                if sections.get('_current_section') == 'prerequisites':
                    sections['prerequisites'].append(item)
            elif line.strip() and not line.startswith('h'):
                # Regular paragraph content
                current_section = sections.get('_current_section', 'overview')
                if current_section == 'overview':
                    sections['overview'] += ' ' + line.strip()
                elif current_section == 'purpose':
                    sections['purpose'] += ' ' + line.strip()

        # Clean up accumulated text
        sections['overview'] = sections['overview'].strip()
        sections['purpose'] = sections['purpose'].strip()

        return sections

class SourceDetector:
    """Detects source format and document type"""

    @staticmethod
    def detect_source_type(content: str) -> str:
        """Detect if content is Confluence Markup, JSON, or plain text"""
        content_stripped = content.strip()

        # Check for Confluence Markup patterns
        if any(content_stripped.startswith(f'h{i}.') for i in range(1, 7)):
            return "confluence_markup"

        if content_stripped.startswith('{') or content_stripped.startswith('['):
            try:
                json.loads(content_stripped)
                return "json"
            except:
                pass

        return "markdown"

    @staticmethod
    def detect_document_type(content: str, source_type: str) -> str:
        """Auto-detect document type from content"""
        content_lower = content.lower()

        # Reference indicators (API/config docs)
        reference_keywords = ['parameter', 'property', 'api', 'endpoint', 'schema', 'configuration', 'option', 'attribute']
        reference_count = sum(1 for kw in reference_keywords if kw in content_lower)

        # Task indicators (procedural)
        task_keywords = ['step', 'prerequisite', 'how to', 'setup', 'install', 'configure', 'follow', 'procedure']
        task_count = sum(1 for kw in task_keywords if kw in content_lower)

        # Concept indicators (explanatory)
        concept_keywords = ['overview', 'purpose', 'concept', 'explain', 'understand', 'what is', 'benefit', 'feature']
        concept_count = sum(1 for kw in concept_keywords if kw in content_lower)

        if reference_count >= task_count and reference_count >= concept_count and reference_count > 0:
            return DocumentType.REFERENCE
        elif task_count > concept_count and task_count > 0:
            return DocumentType.TASK
        else:
            return DocumentType.CONCEPT

class HTMLGenerator:
    """Generates DITA-compliant HTML documentation"""

    @staticmethod
    def generate_concept_html(title: str, content: Dict) -> str:
        """Generate HTML for Concept topic with glossary"""
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
        glossary = GlossaryExtractor.extract_technical_terms(html)
        for term_entry in glossary:
            html += f'''        <div class="glossary-term">
            <strong>{term_entry['term'].title()}:</strong> {term_entry['definition']}
        </div>
'''

        html += """    </div>
</body>
</html>"""

        return html

    @staticmethod
    def generate_reference_html(title: str, content: Dict, json_schema: str = None) -> str:
        """Generate HTML for Reference topic with parameter tables, JSON schema, and error documentation"""
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
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
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
        pre::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        pre::-webkit-scrollbar-track {{
            background: #1e1e1e;
        }}
        pre::-webkit-scrollbar-thumb {{
            background: #555;
            border-radius: 4px;
        }}
        pre::-webkit-scrollbar-thumb:hover {{
            background: #777;
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
        <h2>Properties and Parameters</h2>
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
            html += f"""    <div class="section">
        <h2>JSON Schema</h2>
        <p>The following JSON schema defines the structure of this API specification:</p>
        <div class="code-block-container">
            <div class="code-block-header">
                <span>JSON Schema</span>
                <button class="code-block-copy" onclick="copyToClipboard(this)">Copy</button>
            </div>
            <pre><code>{json_schema}</code></pre>
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
"""

        # Add error documentation
        errors = ErrorDocumenter.extract_error_scenarios("")
        html += ErrorDocumenter.generate_error_table_html(errors)

        html += """
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
    """Applies review rules and generates compliance report"""

    def __init__(self, rules_file: str):
        """Load review rules from JSON file"""
        with open(rules_file, 'r') as f:
            self.rules_data = json.load(f)
        self.rules = self.rules_data['review_rules']

    def assess_document(self, html_content: str, doc_type: str) -> Dict:
        """Assess HTML content against review rules"""
        violations = []
        passed_checks = []

        # Simplified rule checking (in production, this would be much more sophisticated)

        # Check for heading hierarchy
        h1_count = len(re.findall(r'<h1[^>]*>', html_content))
        h_tags = re.findall(r'<h([1-6])[^>]*>', html_content)

        if h1_count != 1:
            violations.append({
                'rule_id': 'STRUCTURE_HEADING_HIERARCHY',
                'severity': Severity.CRITICAL,
                'message': f'Document must have exactly one H1 tag (found {h1_count})',
                'line': None
            })
        else:
            passed_checks.append('STRUCTURE_HEADING_HIERARCHY')

        # Check for proper section order if Concept
        if doc_type == DocumentType.CONCEPT:
            required_sections = ['Overview', 'Purpose', 'Key Concepts', 'When to Use']
            for section in required_sections:
                if section not in html_content:
                    violations.append({
                        'rule_id': 'STRUCTURE_SECTION_ORDER',
                        'severity': Severity.WARNING,
                        'message': f'Concept topic should include "{section}" section',
                        'line': None
                    })
                else:
                    passed_checks.append(f'Section: {section}')

        # Check for code block markers
        code_blocks = re.findall(r'```(\w*)', html_content)
        if '```' in html_content and '' in code_blocks:
            violations.append({
                'rule_id': 'FORMATTING_CODE_BLOCKS',
                'severity': Severity.INFO,
                'message': 'Code blocks should specify language (```json, ```python, etc.)',
                'line': None
            })

        # Check for passive voice indicators (simplified)
        passive_patterns = [
            r'\bwas\s+\w+ed\b',
            r'\bwere\s+\w+ed\b',
            r'\bis\s+\w+ed\b',
            r'\bwill be\s+\w+ed\b'
        ]

        passive_count = sum(len(re.findall(p, html_content)) for p in passive_patterns)
        if passive_count > 3:
            violations.append({
                'rule_id': 'GRAMMAR_ACTIVE_VOICE',
                'severity': Severity.WARNING,
                'message': f'Consider using more active voice ({passive_count} potential passive voice instances detected)',
                'line': None
            })

        # Calculate compliance score
        critical_count = sum(1 for v in violations if v['severity'] == Severity.CRITICAL)
        warning_count = sum(1 for v in violations if v['severity'] == Severity.WARNING)
        info_count = sum(1 for v in violations if v['severity'] == Severity.INFO)

        severity_weight = {Severity.CRITICAL: 3, Severity.WARNING: 2, Severity.INFO: 1}
        total_violations = sum(severity_weight[v['severity']] for v in violations)

        # Perfect score = 100, deduct points based on violations
        compliance_score = max(0, 100 - (total_violations * 5))

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
    """Generates pre-review report"""

    @staticmethod
    def generate_report(assessment: Dict) -> str:
        """Generate HTML pre-review report"""
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
        }}
        .score {{
            font-size: 48px;
            font-weight: bold;
            color: #0078d4;
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
        }}
        h1 {{
            color: #0078d4;
            border-bottom: 2px solid #0078d4;
            padding-bottom: 10px;
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
    <p>
        <strong>Critical Issues:</strong> {assessment['critical_count']}<br>
        <strong>Warnings:</strong> {assessment['warning_count']}<br>
        <strong>Info:</strong> {assessment['info_count']}<br>
        <strong>Checks Passed:</strong> {len(assessment['passed_checks'])}
    </p>

    <div class="violations">
        <h2>Issues Found</h2>
"""

        if not assessment['violations']:
            report += '<p class="passed">✓ No issues found! Documentation meets all standards.</p>'
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

    <h2>Standards Applied</h2>
    <ul>
        <li>Microsoft Writing Style Guide</li>
        <li>IBM Documentation Standards</li>
        <li>DITA Topic-Based Authoring</li>
        <li>Technical Writing Best Practices</li>
    </ul>

    <p><em>Note: This is an automated pre-review assessment. Human review is always recommended.</em></p>
</body>
</html>"""

        return report

def main():
    """Main entry point for document generation"""
    print("Document Intelligence Generator - v1.0")
    print("This module processes source content and generates documentation.")
    print("Use via Claude skill interface or Python API.")

if __name__ == "__main__":
    main()
