#!/usr/bin/env python3
"""
Document Intelligence Generator - Advanced Search PRD Processing
Converts the Advanced Search PRD into structured HTML documentation
"""

import json
import sys
import importlib.util
from pathlib import Path
from datetime import datetime

# Load doc_generator module directly
doc_gen_path = Path(__file__).parent / "scripts" / "doc-generator.py"
spec = importlib.util.spec_from_file_location("doc_generator", doc_gen_path)
doc_generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(doc_generator)

# Import classes
ConfluenceParser = doc_generator.ConfluenceParser
SourceDetector = doc_generator.SourceDetector
DocumentType = doc_generator.DocumentType
HTMLGenerator = doc_generator.HTMLGenerator
ReviewEngine = doc_generator.ReviewEngine
ReportGenerator = doc_generator.ReportGenerator
GlossaryExtractor = doc_generator.GlossaryExtractor
ErrorDocumenter = doc_generator.ErrorDocumenter

# Confluence markdown content from PRD
confluence_content = """# Overview

The Advanced Search feature enables users to quickly find relevant documents using natural language queries combined with intelligent filtering. The feature leverages machine learning to understand search intent and deliver accurate, contextual results.

# Problem Statement

Users currently struggle with traditional keyword-based search. They waste time formulating complex queries and manually filtering results, resulting in frustration and reduced productivity. The current search does not understand context or user intent.

# Solution

Implement AI-powered semantic search that understands natural language queries. The system will parse user intent, automatically suggest relevant filters, and rank results based on relevance and user behavior patterns.

# Key Features and Benefits

* Natural Language Search - Users can type conversational queries instead of keywords

* Smart Filter Suggestions - System suggests relevant filters based on query content

* Faceted Results - Results organized by document type, date, author, etc.

* Search History - Users can access previous searches and save favorite searches

* AI Ranking - Results ranked by relevance, popularity, and personalization

# Business Benefits

* Reduced search time by 40%

* Improved first-result relevance

* Better user engagement with content

* Reduced support tickets related to search

# Target Users

* End users searching for documentation

* Power users needing advanced filtering

* Administrators monitoring search usage

# Technical Approach

* Integrate semantic search engine (Elasticsearch with ML plugin)

* Build query parser for intent recognition

* Implement faceted navigation UI component

* Add personalization engine for ranking

# Timeline

* Phase 1: Semantic search - 2 weeks

* Phase 2: Smart filters - 2 weeks

* Phase 3: Personalization - 1 week

# Success Metrics

* 90% of queries return relevant results in top 3

* Average search time reduced by 35%

* User satisfaction score above 4.5/5

# Acceptance Criteria

* Natural language queries correctly interpreted

* Filter suggestions appear within 500ms

* System handles 1000 queries/minute

* Mobile and desktop support"""

def generate_concept_output(content: str, output_dir: Path):
    """Generate Concept topic documentation"""

    # Parse Confluence markdown
    parsed = ConfluenceParser.parse_confluence_markup(content)

    # Extract title from first heading
    title = "Advanced Search with AI-Powered Filters"

    # Prepare content structure
    concept_content = {
        'title': title,
        'overview': 'The Advanced Search feature enables users to quickly find relevant documents using natural language queries combined with intelligent filtering. The feature leverages machine learning to understand search intent and deliver accurate, contextual results.',
        'purpose': 'Implement AI-powered semantic search that understands natural language queries and automatically suggests relevant filters based on query content.',
        'key_concepts': [
            {'term': 'Natural Language Search', 'description': 'Users can type conversational queries instead of keywords'},
            {'term': 'Semantic Search', 'description': 'Understanding meaning beyond keywords in user queries'},
            {'term': 'Smart Filter Suggestions', 'description': 'System suggests relevant filters based on query content'},
            {'term': 'Faceted Results', 'description': 'Results organized by document type, date, author, and other dimensions'},
            {'term': 'Personalization', 'description': 'Customizing results based on user behavior and preferences'},
        ],
        'when_to_use': 'Use this feature when your users need to find documents quickly without having to formulate complex queries. Ideal for documentation, knowledge bases, and content repositories where context and intent matter.',
        'raw_content': content
    }

    # Generate HTML
    html_output = HTMLGenerator.generate_concept_html(title, concept_content)

    # Save HTML
    concept_file = output_dir / "advanced-search-concept.html"
    with open(concept_file, 'w', encoding='utf-8') as f:
        f.write(html_output)
    print(f"[OK] Concept topic saved: {concept_file}")

    return html_output, concept_file

def generate_reference_output(content: str, output_dir: Path):
    """Generate Reference topic for API and technical specifications"""

    title = "Advanced Search API Reference"

    # Create parameter definitions from the PRD
    reference_content = {
        'title': title,
        'overview': 'The Advanced Search API provides semantic search capabilities with AI-powered filtering and intelligent ranking. This reference documents the API endpoints, parameters, and response formats.',
        'parameters': [
            {
                'name': 'query',
                'type': 'string',
                'required': True,
                'default': None,
                'description': 'Natural language search query (e.g., "recent documents about authentication")'
            },
            {
                'name': 'filters',
                'type': 'array[filter]',
                'required': False,
                'default': '[]',
                'description': 'Array of faceted filters (document_type, date_range, author, etc.)'
            },
            {
                'name': 'limit',
                'type': 'integer',
                'required': False,
                'default': '10',
                'description': 'Maximum number of results to return (1-100)'
            },
            {
                'name': 'offset',
                'type': 'integer',
                'required': False,
                'default': '0',
                'description': 'Number of results to skip for pagination'
            },
            {
                'name': 'sort_by',
                'type': 'enum: relevance|recency|popularity',
                'required': False,
                'default': 'relevance',
                'description': 'Sorting method for results'
            },
            {
                'name': 'personalize',
                'type': 'boolean',
                'required': False,
                'default': 'true',
                'description': 'Enable personalization ranking based on user behavior'
            },
            {
                'name': 'timeout_ms',
                'type': 'integer',
                'required': False,
                'default': '500',
                'description': 'Maximum time in milliseconds to wait for results'
            }
        ]
    }

    # Sample JSON schema
    json_schema = """{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "Natural language search query",
      "example": "authentication setup"
    },
    "filters": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "type": {"type": "string", "enum": ["document_type", "date_range", "author"]},
          "value": {"type": "string"}
        }
      }
    },
    "limit": {"type": "integer", "minimum": 1, "maximum": 100},
    "offset": {"type": "integer", "minimum": 0},
    "sort_by": {"type": "string", "enum": ["relevance", "recency", "popularity"]}
  },
  "required": ["query"]
}"""

    # Generate HTML with JSON schema
    html_output = HTMLGenerator.generate_reference_html(title, reference_content, json_schema)

    # Save HTML
    reference_file = output_dir / "advanced-search-reference.html"
    with open(reference_file, 'w', encoding='utf-8') as f:
        f.write(html_output)
    print(f"[OK] Reference topic saved: {reference_file}")

    return html_output, reference_file

def main():
    """Main entry point"""
    skill_dir = Path(__file__).parent
    output_dir = skill_dir / "outputs"
    output_dir.mkdir(exist_ok=True)

    # Load review rules
    rules_file = skill_dir / "references" / "review-rules.json"
    review_engine = ReviewEngine(str(rules_file))

    print("\n" + "="*70)
    print("DOCUMENT INTELLIGENCE GENERATOR")
    print("Processing: Advanced Search with AI-Powered Filters PRD")
    print("="*70)

    # Generate Concept Topic
    print("\n[1/4] Generating Concept Topic...")
    concept_html, concept_file = generate_concept_output(confluence_content, output_dir)
    concept_assessment = review_engine.assess_document(concept_html, DocumentType.CONCEPT)
    concept_report = ReportGenerator.generate_report(concept_assessment)

    concept_report_file = output_dir / "advanced-search-concept-report.html"
    with open(concept_report_file, 'w', encoding='utf-8') as f:
        f.write(concept_report)
    print(f"[OK] Concept report saved: {concept_report_file}")
    print(f"  Compliance Score: {concept_assessment['compliance_score']}%")

    # Generate Reference Topic
    print("\n[2/4] Generating Reference Topic...")
    reference_html, reference_file = generate_reference_output(confluence_content, output_dir)
    reference_assessment = review_engine.assess_document(reference_html, DocumentType.REFERENCE)
    reference_report = ReportGenerator.generate_report(reference_assessment)

    reference_report_file = output_dir / "advanced-search-reference-report.html"
    with open(reference_report_file, 'w', encoding='utf-8') as f:
        f.write(reference_report)
    print(f"[OK] Reference report saved: {reference_report_file}")
    print(f"  Compliance Score: {reference_assessment['compliance_score']}%")

    # Generate Summary Report
    print("\n[3/4] Generating Summary Report...")
    summary = {
        'project': 'Advanced Search with AI-Powered Filters',
        'generated': datetime.now().isoformat(),
        'documents': [
            {
                'type': 'Concept',
                'file': str(concept_file),
                'report': str(concept_report_file),
                'compliance_score': concept_assessment['compliance_score'],
                'issues': {
                    'critical': concept_assessment['critical_count'],
                    'warning': concept_assessment['warning_count'],
                    'info': concept_assessment['info_count']
                }
            },
            {
                'type': 'Reference',
                'file': str(reference_file),
                'report': str(reference_report_file),
                'compliance_score': reference_assessment['compliance_score'],
                'issues': {
                    'critical': reference_assessment['critical_count'],
                    'warning': reference_assessment['warning_count'],
                    'info': reference_assessment['info_count']
                }
            }
        ],
        'overall_score': (concept_assessment['compliance_score'] + reference_assessment['compliance_score']) / 2
    }

    summary_file = output_dir / "generation-summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    print(f"[OK] Summary saved: {summary_file}")

    # Print Summary
    print("\n[4/4] Summary")
    print("="*70)
    print(f"Project: {summary['project']}")
    print(f"Overall Compliance Score: {summary['overall_score']:.1f}%")
    print("\nDocuments Generated:")
    for doc in summary['documents']:
        print(f"\n  {doc['type']} Topic:")
        print(f"    - File: {Path(doc['file']).name}")
        print(f"    - Report: {Path(doc['report']).name}")
        print(f"    - Compliance: {doc['compliance_score']}%")
        print(f"    - Issues: {doc['issues']['critical']} critical, {doc['issues']['warning']} warnings, {doc['issues']['info']} info")

    print("\n" + "="*70)
    print("[OK] Document generation complete!")
    print("="*70 + "\n")

    return summary

if __name__ == "__main__":
    main()
