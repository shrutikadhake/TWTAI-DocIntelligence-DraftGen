#!/usr/bin/env python3
"""
AI Draft Generator - Microsoft Word to HTML5 Converter
Converts .doc/.docx Product Requirements and Specifications documents to HTML5

Usage:
    python convert_docx_to_html5.py <input_file> <output_file>

Example:
    python convert_docx_to_html5.py "resources/Product Requirements.doc" "output/Product Requirements.html"
"""

import sys
import os
import re
from pathlib import Path
from datetime import datetime

try:
    from docx import Document
    from docx.oxml import parse_xml
    from docx.table import Table
except ImportError:
    try:
        import docx
    except ImportError:
        print("ERROR: python-docx is required. Install with: pip install python-docx")
        sys.exit(1)

try:
    from doc2docx import convert
except ImportError:
    convert = None

class WordToHTML5Converter:
    """Convert Microsoft Word documents to HTML5"""

    def __init__(self, input_file):
        self.input_file = input_file
        self.doc = None
        self.html_content = []
        self.heading_stack = []
        self.in_list = False
        self.current_list_type = None
        self.metadata = {
            'title': 'Product Requirements and Specifications',
            'author': 'Unknown',
            'version': '1.0',
            'date': datetime.now().strftime('%Y-%m-%d')
        }

    def load_document(self):
        """Load the Word document"""
        input_path = Path(self.input_file)

        if not input_path.exists():
            raise FileNotFoundError(f"File not found: {self.input_file}")

        # Handle .doc files by converting to .docx first
        if input_path.suffix.lower() == '.doc':
            if convert is None:
                print(f"Converting .doc file to .docx format...")
                try:
                    # Try using LibreOffice/UNO if available
                    self._convert_doc_to_docx(str(input_path))
                except Exception as e:
                    print(f"Warning: Could not convert .doc file: {e}")
                    # Try to read directly if possible
                    return self._load_doc_file(str(input_path))
            else:
                temp_docx = input_path.with_suffix('.docx')
                convert(str(input_path), str(temp_docx))
                input_path = temp_docx

        try:
            self.doc = Document(str(input_path))
        except Exception as e:
            print(f"Error loading document: {e}")
            raise

        return self.doc

    def _load_doc_file(self, filepath):
        """Attempt to extract text from .doc file"""
        try:
            from docx import Document
            # Try to load directly
            return Document(filepath)
        except:
            # Fallback: extract what we can
            print("Warning: Limited support for .doc format. Some formatting may be lost.")
            return None

    def _convert_doc_to_docx(self, doc_path):
        """Convert .doc to .docx using available tools"""
        try:
            # Try using python-docx if it supports the format
            self.doc = Document(doc_path)
        except:
            # Try converting using command line tools if available
            try:
                import subprocess
                docx_path = doc_path.replace('.doc', '.docx')
                # Try using LibreOffice
                subprocess.run(['libreoffice', '--headless', '--convert-to', 'docx', doc_path],
                             check=False, capture_output=True)
                if os.path.exists(docx_path):
                    self.doc = Document(docx_path)
            except:
                raise Exception("Cannot convert .doc file. Please convert to .docx manually.")

    def extract_metadata(self):
        """Extract document metadata"""
        try:
            props = self.doc.core_properties
            if props.title:
                self.metadata['title'] = props.title
            if props.author:
                self.metadata['author'] = props.author
            if props.created:
                self.metadata['date'] = props.created.strftime('%Y-%m-%d')
        except:
            pass

    def get_heading_level(self, paragraph):
        """Determine heading level from paragraph style"""
        style = paragraph.style.name
        if 'Heading' in style:
            # Extract number from "Heading 1", "Heading 2", etc.
            match = re.search(r'Heading (\d)', style)
            if match:
                return int(match.group(1))
        return None

    def is_special_paragraph(self, text):
        """Check if paragraph is a special element (Note, Warning, Caution, Tip)"""
        special_types = {
            r'^Note:': 'note',
            r'^Warning:': 'warning',
            r'^Caution:': 'caution',
            r'^Tip:': 'tip'
        }
        for pattern, type_name in special_types.items():
            if re.match(pattern, text.strip()):
                return type_name, re.sub(pattern + r'\s*', '', text.strip())
        return None, text

    def format_text(self, run):
        """Format text with HTML tags based on Word formatting"""
        text = run.text
        if not text:
            return ""

        html = text

        # Apply formatting
        if run.bold:
            html = f"<strong>{html}</strong>"
        if run.italic:
            html = f"<em>{html}</em>"
        if run.underline:
            html = f"<u>{html}</u>"
        if run.font.strike:
            html = f"<del>{html}</del>"

        return html

    def paragraph_to_html(self, paragraph):
        """Convert paragraph to HTML"""
        text = paragraph.text.strip()
        if not text:
            return ""

        # Check for heading
        heading_level = self.get_heading_level(paragraph)
        if heading_level:
            # Create anchor ID from heading text
            anchor_id = re.sub(r'[^\w\s-]', '', text.lower()).replace(' ', '-')
            return f'<h{heading_level} id="{anchor_id}">{text}</h{heading_level}>'

        # Check for special paragraphs (Note, Warning, etc.)
        special_type, special_text = self.is_special_paragraph(text)
        if special_type:
            return f'<section class="{special_type}"><strong>{special_type.capitalize()}:</strong> {special_text}</section>'

        # Regular paragraph
        formatted_text = ""
        for run in paragraph.runs:
            formatted_text += self.format_text(run)

        if formatted_text:
            return f"<p>{formatted_text}</p>"
        return ""

    def table_to_html(self, table):
        """Convert table to HTML"""
        html = '<table>\n'

        # Check if first row should be header
        html += '<thead>\n<tr>\n'
        for cell in table.rows[0].cells:
            html += f'<th>{cell.text}</th>\n'
        html += '</tr>\n</thead>\n'

        # Add body rows
        if len(table.rows) > 1:
            html += '<tbody>\n'
            for row in table.rows[1:]:
                html += '<tr>\n'
                for cell in row.cells:
                    html += f'<td>{cell.text}</td>\n'
                html += '</tr>\n'
            html += '</tbody>\n'

        html += '</table>\n'
        return html

    def list_to_html(self, paragraphs, start_idx):
        """Convert list items to HTML"""
        if not paragraphs:
            return "", start_idx

        first_para = paragraphs[start_idx]

        # Determine list type from paragraph style
        list_type = 'ul'  # default to unordered
        if 'List Number' in first_para.style.name:
            list_type = 'ol'

        html = f'<{list_type}>\n'
        idx = start_idx

        while idx < len(paragraphs):
            para = paragraphs[idx]

            # Check if this is still a list item
            if 'List' not in para.style.name and para.text.strip() and not para.text.strip().startswith(('•', '-', '*', '1.', '2.', '3.')):
                break

            text = para.text.strip()
            if text:
                # Remove list markers if present
                text = re.sub(r'^[•\-*]?\s*', '', text)
                text = re.sub(r'^\d+\.\s*', '', text)
                html += f'<li>{text}</li>\n'

            idx += 1

        html += f'</{list_type}>\n'
        return html, idx - 1

    def convert(self):
        """Convert document to HTML5"""
        if not self.doc:
            self.load_document()

        self.extract_metadata()

        # Process all paragraphs and tables
        idx = 0
        while idx < len(self.doc.paragraphs):
            para = self.doc.paragraphs[idx]

            # Check for list items
            if 'List' in para.style.name or para.text.strip().startswith(('•', '-', '*')):
                html, new_idx = self.list_to_html(self.doc.paragraphs, idx)
                self.html_content.append(html)
                idx = new_idx + 1
            else:
                html = self.paragraph_to_html(para)
                if html:
                    self.html_content.append(html)
                idx += 1

        # Process tables
        for table in self.doc.tables:
            self.html_content.append(self.table_to_html(table))

        return '\n'.join(self.html_content)

    def generate_html5(self):
        """Generate complete HTML5 document"""
        body_content = self.convert()

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.metadata['title']}</title>
    <meta name="author" content="{self.metadata['author']}">
    <meta name="description" content="Product Requirements and Specifications Document">
    <meta name="version" content="{self.metadata['version']}">
    <meta name="date" content="{self.metadata['date']}">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        header {{
            border-bottom: 2px solid #333;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        main {{
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #222;
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        h1 {{
            font-size: 2.5em;
            border-bottom: 3px solid #007bff;
            padding-bottom: 10px;
        }}
        h2 {{
            font-size: 2em;
            color: #0056b3;
        }}
        h3 {{
            font-size: 1.5em;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        table th, table td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        table thead {{
            background-color: #f8f9fa;
            font-weight: bold;
        }}
        table tbody tr:nth-child(odd) {{
            background-color: #f9f9f9;
        }}
        ul, ol {{
            margin: 15px 0;
            padding-left: 30px;
        }}
        li {{
            margin: 8px 0;
        }}
        section.note {{
            border-left: 4px solid #17a2b8;
            padding: 15px;
            background-color: #d1ecf1;
            margin: 20px 0;
            border-radius: 4px;
        }}
        section.warning {{
            border-left: 4px solid #ffc107;
            padding: 15px;
            background-color: #fff3cd;
            margin: 20px 0;
            border-radius: 4px;
        }}
        section.caution {{
            border-left: 4px solid #dc3545;
            padding: 15px;
            background-color: #f8d7da;
            margin: 20px 0;
            border-radius: 4px;
        }}
        section.tip {{
            border-left: 4px solid #28a745;
            padding: 15px;
            background-color: #d4edda;
            margin: 20px 0;
            border-radius: 4px;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
            margin: 15px 0;
        }}
        footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <header>
        <h1>{self.metadata['title']}</h1>
        <p><strong>Author:</strong> {self.metadata['author']}</p>
        <p><strong>Version:</strong> {self.metadata['version']}</p>
        <p><strong>Date:</strong> {self.metadata['date']}</p>
    </header>

    <main>
{body_content}
    </main>

    <footer>
        <p>Generated from Microsoft Word document on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>This document was automatically converted to HTML5 using the AI Draft Generator skill.</p>
    </footer>
</body>
</html>"""

        return html

    def save(self, output_file):
        """Save HTML5 document to file"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        html_content = self.generate_html5()

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✓ Successfully converted document")
        print(f"  Input:  {self.input_file}")
        print(f"  Output: {output_path.absolute()}")
        print(f"  Size:   {len(html_content)} bytes")


def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        print("Usage: python convert_docx_to_html5.py <input_file> <output_file>")
        print("\nExample:")
        print("  python convert_docx_to_html5.py 'resources/Product Requirements.doc' 'output/Product Requirements.html'")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        converter = WordToHTML5Converter(input_file)
        converter.load_document()
        converter.save(output_file)
        print("\n✓ Conversion complete!")
        sys.exit(0)
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
