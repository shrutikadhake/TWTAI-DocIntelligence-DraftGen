#!/usr/bin/env python3
"""
Extract content from a malformed Word document (.doc) file.
Handles ZIP headers that may be offset due to malformed files.
"""

import zipfile
import io
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import json


class WordDocumentExtractor:
    """Extract content from Word documents with malformed ZIP headers."""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.zip_file = None
        self.content = {
            'metadata': {},
            'body': {
                'paragraphs': [],
                'tables': [],
                'lists': [],
                'headings': [],
                'formatted_text': []
            },
            'structure': []
        }

    def find_zip_header(self, data: bytes) -> int:
        """Find the ZIP file magic bytes (PK\x03\x04) in the data."""
        magic_bytes = b'PK\x03\x04'
        offset = data.find(magic_bytes)
        if offset != -1:
            print(f"Found ZIP header at offset: {offset} (0x{offset:x})")
            return offset
        raise ValueError("Could not find ZIP header in file")

    def load_zip(self) -> bool:
        """Load ZIP data, handling malformed headers."""
        try:
            with open(self.file_path, 'rb') as f:
                data = f.read()

            print(f"File size: {len(data)} bytes")

            # Try to open as regular ZIP first
            try:
                self.zip_file = zipfile.ZipFile(self.file_path, 'r')
                print("Successfully opened as standard ZIP")
                return True
            except zipfile.BadZipFile:
                print("Standard ZIP opening failed, searching for ZIP header...")

                # Find the ZIP header offset
                offset = self.find_zip_header(data)

                # Extract ZIP data starting from the header
                zip_data = data[offset:]
                self.zip_file = zipfile.ZipFile(io.BytesIO(zip_data), 'r')
                print("Successfully opened with offset ZIP")
                return True

        except Exception as e:
            print(f"Error loading ZIP: {e}")
            return False

    def extract_metadata(self) -> Dict[str, Any]:
        """Extract metadata from docProps/core.xml."""
        metadata = {}
        try:
            # Try to read core properties
            if 'docProps/core.xml' in self.zip_file.namelist():
                core_xml = self.zip_file.read('docProps/core.xml')
                root = ET.fromstring(core_xml)

                # Define namespaces
                namespaces = {
                    'cp': 'http://schemas.openxmlformats.org/officeDocument/2006/custom-properties',
                    'dc': 'http://purl.org/dc/elements/1.1/',
                    'dcterms': 'http://purl.org/dc/terms/',
                    'dcmitype': 'http://purl.org/dc/dcmitype/',
                    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
                }

                # Extract common metadata fields
                fields = {
                    'title': 'dc:title',
                    'subject': 'dc:subject',
                    'creator': 'dc:creator',
                    'description': 'dc:description',
                    'created': 'dcterms:created',
                    'modified': 'dcterms:modified',
                    'version': 'cp:version'
                }

                for key, xpath in fields.items():
                    elem = root.find(xpath, namespaces)
                    if elem is not None and elem.text:
                        metadata[key] = elem.text

            print(f"Extracted metadata: {metadata}")
            return metadata

        except Exception as e:
            print(f"Error extracting metadata: {e}")
            return metadata

    def extract_text_with_formatting(self, element: ET.Element, namespaces: Dict) -> str:
        """Extract text from an element with formatting information."""
        text = ''
        for child in element:
            if child.tag.endswith('}t'):  # Text element
                if child.text:
                    text += child.text
            elif child.tag.endswith('}tab'):  # Tab element
                text += '\t'
            elif child.tag.endswith('}br'):  # Break element
                text += '\n'
            elif child.tag.endswith('}r'):  # Run element
                text += self.extract_text_with_formatting(child, namespaces)
        return text

    def get_paragraph_style(self, para: ET.Element, namespaces: Dict) -> Optional[str]:
        """Extract style information from a paragraph."""
        pPr = para.find('.//w:pPr', namespaces)
        if pPr is not None:
            pStyle = pPr.find('w:pStyle', namespaces)
            if pStyle is not None:
                return pStyle.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
        return None

    def get_run_properties(self, run: ET.Element, namespaces: Dict) -> Dict[str, bool]:
        """Extract formatting properties from a run."""
        props = {'bold': False, 'italic': False, 'underline': False}
        rPr = run.find('w:rPr', namespaces)
        if rPr is not None:
            if rPr.find('w:b', namespaces) is not None:
                props['bold'] = True
            if rPr.find('w:i', namespaces) is not None:
                props['italic'] = True
            if rPr.find('w:u', namespaces) is not None:
                props['underline'] = True
        return props

    def extract_body_content(self) -> bool:
        """Extract content from word/document.xml."""
        try:
            if 'word/document.xml' not in self.zip_file.namelist():
                print("document.xml not found")
                return False

            doc_xml = self.zip_file.read('word/document.xml')
            root = ET.fromstring(doc_xml)

            # Define namespaces
            namespaces = {
                'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
                'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
                'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
                'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture'
            }

            # Find the body element
            body = root.find('.//w:body', namespaces)
            if body is None:
                print("Body element not found")
                return False

            para_count = 0
            table_count = 0
            heading_count = 0

            # Process body content
            for element in body:
                if element.tag.endswith('}p'):  # Paragraph
                    para_data = self.extract_paragraph(element, namespaces)
                    if para_data['text'].strip():  # Only add non-empty paragraphs
                        self.content['body']['paragraphs'].append(para_data)
                        para_count += 1

                        # Track headings
                        if para_data.get('style') and 'Heading' in para_data['style']:
                            heading_data = {
                                'level': int(para_data['style'].split('Heading')[-1]) if any(c.isdigit() for c in para_data['style']) else 1,
                                'text': para_data['text'],
                                'style': para_data['style']
                            }
                            self.content['body']['headings'].append(heading_data)
                            heading_count += 1

                elif element.tag.endswith('}tbl'):  # Table
                    table_data = self.extract_table(element, namespaces)
                    self.content['body']['tables'].append(table_data)
                    table_count += 1

            print(f"Extracted {para_count} paragraphs, {table_count} tables, {heading_count} headings")
            return True

        except Exception as e:
            print(f"Error extracting body content: {e}")
            import traceback
            traceback.print_exc()
            return False

    def extract_paragraph(self, para: ET.Element, namespaces: Dict) -> Dict[str, Any]:
        """Extract a paragraph and its formatting."""
        para_data = {
            'text': '',
            'style': self.get_paragraph_style(para, namespaces),
            'runs': [],
            'list_level': None
        }

        # Check for list properties
        pPr = para.find('.//w:pPr', namespaces)
        if pPr is not None:
            numPr = pPr.find('w:numPr', namespaces)
            if numPr is not None:
                ilvl = numPr.find('w:ilvl', namespaces)
                if ilvl is not None:
                    para_data['list_level'] = ilvl.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')

        # Extract runs (formatted text segments)
        for run in para.findall('.//w:r', namespaces):
            run_data = self.extract_run(run, namespaces)
            if run_data['text']:
                para_data['runs'].append(run_data)
                para_data['text'] += run_data['text']

        return para_data

    def extract_run(self, run: ET.Element, namespaces: Dict) -> Dict[str, Any]:
        """Extract a run (formatted text segment)."""
        run_data = {
            'text': '',
            'bold': False,
            'italic': False,
            'underline': False,
            'font': None
        }

        # Get formatting
        rPr = run.find('w:rPr', namespaces)
        if rPr is not None:
            if rPr.find('w:b', namespaces) is not None:
                run_data['bold'] = True
            if rPr.find('w:i', namespaces) is not None:
                run_data['italic'] = True
            if rPr.find('w:u', namespaces) is not None:
                run_data['underline'] = True

            rFonts = rPr.find('w:rFonts', namespaces)
            if rFonts is not None:
                run_data['font'] = rFonts.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}ascii')

        # Extract text
        for child in run:
            if child.tag.endswith('}t'):
                if child.text:
                    run_data['text'] += child.text
            elif child.tag.endswith('}tab'):
                run_data['text'] += '\t'
            elif child.tag.endswith('}br'):
                run_data['text'] += '\n'

        return run_data

    def extract_table(self, tbl: ET.Element, namespaces: Dict) -> Dict[str, Any]:
        """Extract a table."""
        table_data = {
            'rows': [],
            'properties': {}
        }

        for row in tbl.findall('.//w:tr', namespaces):
            row_data = {'cells': []}
            for cell in row.findall('w:tc', namespaces):
                cell_text = ''
                for para in cell.findall('w:p', namespaces):
                    para_text = self.extract_text_with_formatting(para, namespaces)
                    if cell_text:
                        cell_text += '\n'
                    cell_text += para_text
                row_data['cells'].append({
                    'content': cell_text,
                    'paragraphs': [{'text': para_text} for para_text in cell_text.split('\n')]
                })
            table_data['rows'].append(row_data)

        return table_data

    def extract(self) -> bool:
        """Main extraction method."""
        print("Starting extraction...")

        if not self.load_zip():
            return False

        # Extract metadata
        self.content['metadata'] = self.extract_metadata()

        # Extract body content
        if not self.extract_body_content():
            return False

        print("Extraction completed successfully")
        return True

    def get_formatted_output(self) -> str:
        """Get a nicely formatted output of the extracted content."""
        output = []
        output.append("=" * 80)
        output.append("EXTRACTED WORD DOCUMENT CONTENT")
        output.append("=" * 80)

        # Metadata section
        output.append("\nMETADATA:")
        output.append("-" * 40)
        if self.content['metadata']:
            for key, value in self.content['metadata'].items():
                output.append(f"  {key}: {value}")
        else:
            output.append("  (no metadata found)")

        # Headings section
        if self.content['body']['headings']:
            output.append("\n\nDOCUMENT STRUCTURE (Headings):")
            output.append("-" * 40)
            for heading in self.content['body']['headings']:
                level = heading.get('level', 1)
                indent = "  " * (level - 1)
                output.append(f"{indent}[H{level}] {heading['text']}")

        # Main content section
        output.append("\n\nDOCUMENT CONTENT:")
        output.append("-" * 40)

        # Process body elements in order
        para_idx = 0
        table_idx = 0

        # We need to reconstruct the order, so let's re-parse
        try:
            with open(self.file_path, 'rb') as f:
                data = f.read()

            offset = self.find_zip_header(data)
            zip_data = data[offset:]
            zip_file = zipfile.ZipFile(io.BytesIO(zip_data), 'r')

            doc_xml = zip_file.read('word/document.xml')
            root = ET.fromstring(doc_xml)

            namespaces = {
                'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
            }

            body = root.find('.//w:body', namespaces)

            for element in body:
                if element.tag.endswith('}p'):
                    if para_idx < len(self.content['body']['paragraphs']):
                        para = self.content['body']['paragraphs'][para_idx]

                        # Format paragraph based on style
                        style = para.get('style', '')
                        text = para['text'].strip()

                        if 'Heading' in style:
                            output.append(f"\n### {text}")
                        elif style == 'List Paragraph' or para.get('list_level') is not None:
                            level = int(para.get('list_level', 0))
                            indent = "  " * level
                            output.append(f"{indent}• {text}")
                        else:
                            if text:
                                output.append(f"\n{text}")

                        # Show formatting details if present
                        if para['runs']:
                            for run in para['runs']:
                                if run['bold'] or run['italic'] or run['underline']:
                                    fmt = []
                                    if run['bold']:
                                        fmt.append('bold')
                                    if run['italic']:
                                        fmt.append('italic')
                                    if run['underline']:
                                        fmt.append('underline')
                                    # Uncomment to show formatting: output.append(f"    [{', '.join(fmt)}]: {run['text']}")

                        para_idx += 1

                elif element.tag.endswith('}tbl'):
                    if table_idx < len(self.content['body']['tables']):
                        table = self.content['body']['tables'][table_idx]
                        output.append("\n[TABLE]")

                        for row_idx, row in enumerate(table['rows']):
                            for cell_idx, cell in enumerate(row['cells']):
                                cell_text = cell['content'].replace('\n', ' | ')
                                if cell_text.strip():
                                    output.append(f"  Row {row_idx + 1}, Col {cell_idx + 1}: {cell_text}")

                        output.append("[/TABLE]\n")
                        table_idx += 1

        except Exception as e:
            print(f"Error formatting output: {e}")

        output.append("\n" + "=" * 80)
        output.append(f"SUMMARY: {len(self.content['body']['paragraphs'])} paragraphs, "
                     f"{len(self.content['body']['tables'])} tables, "
                     f"{len(self.content['body']['headings'])} headings")
        output.append("=" * 80)

        return "\n".join(output)

    def get_json_output(self) -> str:
        """Get JSON formatted output."""
        return json.dumps(self.content, indent=2, default=str)


def main():
    """Main entry point."""
    file_path = r"C:\Users\tamilselvan\OneDrive\Documents\GitHub\TWTAI-DocIntelligence-DraftGen\resources\Product Requirements _and Specifications.doc"

    print(f"Processing: {file_path}\n")

    extractor = WordDocumentExtractor(file_path)

    if extractor.extract():
        # Print formatted output
        formatted = extractor.get_formatted_output()
        print(formatted)

        # Save JSON output
        json_output = extractor.get_json_output()
        output_file = r"C:\Users\tamilselvan\OneDrive\Documents\GitHub\TWTAI-DocIntelligence-DraftGen\extracted_content.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(json_output)
        print(f"\nJSON output saved to: {output_file}")
    else:
        print("Extraction failed")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
