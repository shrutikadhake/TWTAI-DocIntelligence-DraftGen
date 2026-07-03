# Atlassian MCP Setup Guide

This skill requires **Atlassian MCP** (Model Context Protocol) to access Confluence pages and attachments. Follow these steps to set up the test environment.

## Prerequisites

- Access to a Confluence Cloud or Server workspace
- Atlassian API token (Cloud) or credentials (Server)
- Atlassian MCP configured and running

## Step 1: Configure Atlassian MCP

Ensure your `Claude Code` settings include Atlassian MCP configuration:

```json
{
  "mcpServers": {
    "atlassian": {
      "command": "node",
      "args": ["path/to/atlassian-mcp/index.js"],
      "env": {
        "CONFLUENCE_DOMAIN": "your-org.atlassian.net",
        "CONFLUENCE_USER": "your-email@example.com",
        "CONFLUENCE_TOKEN": "your-api-token"
      }
    }
  }
}
```

## Step 2: Create Sample Confluence Pages

Create the following pages in your Confluence workspace for testing:

### Page 1: Advanced Search PRD

**Space**: DOCS  
**Title**: Advanced Search PRD  
**Page ID**: 11111 (or your actual page ID)  
**URL**: `https://your-org.atlassian.net/wiki/spaces/DOCS/pages/11111/Advanced-Search-PRD`

**Content** (Confluence Markup):
```
h1. Advanced Search with AI-Powered Filters

h2. Overview
The Advanced Search feature enables users to quickly find relevant documents using natural language queries combined with intelligent filtering. The feature leverages machine learning to understand search intent and deliver accurate, contextual results.

h2. Problem Statement
Users currently struggle with traditional keyword-based search. They waste time formulating complex queries and manually filtering results, resulting in frustration and reduced productivity. The current search does not understand context or user intent.

h2. Solution
Implement AI-powered semantic search that understands natural language queries. The system will parse user intent, automatically suggest relevant filters, and rank results based on relevance and user behavior patterns.

h2. Key Features and Benefits

* Natural Language Search - Users can type conversational queries instead of keywords
* Smart Filter Suggestions - System suggests relevant filters based on query content  
* Faceted Results - Results organized by document type, date, author, etc.
* Search History - Users can access previous searches and save favorite searches
* AI Ranking - Results ranked by relevance, popularity, and personalization

h3. Business Benefits
* Reduced search time by 40%
* Improved first-result relevance
* Better user engagement with content
* Reduced support tickets related to search

h2. Target Users
* End users searching for documentation
* Power users needing advanced filtering
* Administrators monitoring search usage

h2. Technical Approach
* Integrate semantic search engine (Elasticsearch with ML plugin)
* Build query parser for intent recognition
* Implement faceted navigation UI component
* Add personalization engine for ranking

h2. Timeline
* Phase 1: Semantic search - 2 weeks
* Phase 2: Smart filters - 2 weeks
* Phase 3: Personalization - 1 week

h2. Success Metrics
* 90% of queries return relevant results in top 3
* Average search time reduced by 35%
* User satisfaction score above 4.5/5

h2. Acceptance Criteria
* Natural language queries correctly interpreted
* Filter suggestions appear within 500ms
* System handles 1000 queries/minute
* Mobile and desktop support
```

---

### Page 2: Advanced Search API Reference

**Space**: API  
**Title**: Advanced Search API Reference  
**Page ID**: 22222 (or your actual page ID)  
**URL**: `https://your-org.atlassian.net/wiki/spaces/API/pages/22222/Advanced-Search-API-Reference`

**Content** (Confluence Markup):
```
h1. Advanced Search API Reference

h2. Overview
This API enables developers to integrate advanced semantic search capabilities into their applications. The API supports natural language queries, intelligent filtering, and personalized result ranking.

h2. Endpoints

h3. POST /api/v2/search
Execute a search query with optional filters and configuration options.

h2. Configuration Options

The following configuration parameters control the behavior of the search service.

h3. Core Configuration
* search_engine - Search backend engine (elasticsearch, opensearch, meilisearch). Default: elasticsearch
* semantic_model - ML model for semantic understanding. Default: multilingual-e5-large
* timeout_ms - Search query timeout in milliseconds. Range: 1000-30000. Default: 5000

h3. Ranking and Filtering
* min_relevance_score - Minimum relevance score (0-1) to include in results. Default: 0.5
* enable_personalization - Enable personalized ranking based on user behavior. Default: true

h3. Caching
* cache_results - Cache popular search results. Default: true
* cache_ttl_seconds - Time-to-live for cached results in seconds. Range: 60-86400. Default: 3600

{info}Note: Attached JSON file (search-api-config.json) contains full schema with all parameters and response structures.{info}
```

**Attachment**: Create and attach the `search-api-config.json` file (see below)

---

### Attachment File: search-api-config.json

Attach this JSON file to Page 2:

```json
{
  "api_name": "Advanced Search API",
  "version": "2.0",
  "description": "API for configuring and executing advanced search queries with semantic understanding",
  "endpoints": {
    "search": {
      "method": "POST",
      "path": "/api/v2/search",
      "description": "Execute a search query with optional filters",
      "parameters": {
        "query": {
          "type": "string",
          "required": true,
          "description": "Search query in natural language. Can include conversational phrases or traditional keywords.",
          "example": "documents about security from last month",
          "max_length": 500
        },
        "filters": {
          "type": "object",
          "required": false,
          "description": "Optional filters to refine results",
          "properties": {
            "document_type": {
              "type": "array",
              "items": {
                "type": "string",
                "enum": ["guide", "api_reference", "tutorial", "faq"]
              },
              "description": "Filter by document type"
            },
            "date_range": {
              "type": "object",
              "description": "Filter by date range",
              "properties": {
                "from": {
                  "type": "string",
                  "format": "date",
                  "description": "Start date (ISO 8601 format)"
                },
                "to": {
                  "type": "string",
                  "format": "date",
                  "description": "End date (ISO 8601 format)"
                }
              }
            },
            "author": {
              "type": "string",
              "description": "Filter by document author name or ID"
            },
            "tags": {
              "type": "array",
              "items": {
                "type": "string"
              },
              "description": "Filter by document tags"
            }
          }
        },
        "limit": {
          "type": "integer",
          "required": false,
          "default": 20,
          "minimum": 1,
          "maximum": 100,
          "description": "Maximum number of results to return"
        },
        "offset": {
          "type": "integer",
          "required": false,
          "default": 0,
          "minimum": 0,
          "description": "Pagination offset for result set"
        },
        "sort": {
          "type": "string",
          "required": false,
          "default": "relevance",
          "enum": ["relevance", "date_desc", "date_asc", "popularity"],
          "description": "Sort order for results"
        },
        "include_suggestions": {
          "type": "boolean",
          "required": false,
          "default": true,
          "description": "Include AI-generated filter suggestions in response"
        }
      }
    }
  },
  "configuration": {
    "search_engine": {
      "type": "string",
      "description": "Search backend engine to use",
      "default": "elasticsearch",
      "enum": ["elasticsearch", "opensearch", "meilisearch"]
    },
    "semantic_model": {
      "type": "string",
      "description": "ML model for semantic understanding",
      "default": "multilingual-e5-large",
      "enum": ["multilingual-e5-large", "all-mpnet-base-v2", "bge-large-en-v1.5"]
    },
    "timeout_ms": {
      "type": "integer",
      "description": "Search query timeout in milliseconds",
      "default": 5000,
      "minimum": 1000,
      "maximum": 30000
    },
    "min_relevance_score": {
      "type": "number",
      "description": "Minimum relevance score (0-1) to include in results",
      "default": 0.5,
      "minimum": 0,
      "maximum": 1
    },
    "enable_personalization": {
      "type": "boolean",
      "description": "Enable personalized ranking based on user behavior",
      "default": true
    },
    "cache_results": {
      "type": "boolean",
      "description": "Cache popular search results",
      "default": true
    },
    "cache_ttl_seconds": {
      "type": "integer",
      "description": "Time-to-live for cached results in seconds",
      "default": 3600,
      "minimum": 60,
      "maximum": 86400
    }
  }
}
```

## Step 3: Get Actual URLs

Once pages are created, note their actual URLs:

1. Update `evals/evals.json` with the actual Confluence page URLs
2. Ensure attachment name matches exactly (e.g., `search-api-config.json`)

## Step 4: Test Atlassian MCP Connection

Run a quick test to ensure Atlassian MCP can access your Confluence:

```bash
# Test MCP connection
atlas confluence get-page --url "https://your-org.atlassian.net/wiki/spaces/DOCS/pages/11111/Advanced-Search-PRD"
```

## Usage in Skill

When running the skill, provide the Confluence page URL:

```
Confluence URL: https://your-org.atlassian.net/wiki/spaces/DOCS/pages/11111/Advanced-Search-PRD
```

The skill will:
1. Use Atlassian MCP to fetch the page content
2. Parse Confluence Markup format
3. Extract any attached JSON files
4. Generate structured documentation
5. Provide pre-review assessment

## Troubleshooting

**Connection Issues**:
- Verify API token has appropriate scopes
- Check MCP server is running: `ps aux | grep atlassian-mcp`
- Review Confluence access permissions

**URL Extraction Issues**:
- Ensure URL follows format: `https://org.atlassian.net/wiki/spaces/SPACE/pages/ID/Page-Name`
- Check page exists and is accessible
- Verify page ID (numbers after `/pages/`)

**Attachment Issues**:
- Verify attachment is JSON format
- Check filename matches exactly
- Ensure attachment is readable by API user

