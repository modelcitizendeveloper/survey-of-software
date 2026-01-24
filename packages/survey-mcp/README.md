# survey-mcp

MCP server exposing [research.modelcitizendeveloper.com](https://research.modelcitizendeveloper.com) surveys as MCP resources.

## Overview

survey-mcp provides programmatic access to the Survey of Software research site's 169+ library surveys through the Model Context Protocol (MCP). It exposes curated research from the 4PS methodology (Rapid, Comprehensive, Need-Driven, Strategic) as resources that can be consumed by Claude Desktop, spawn-analysis, and other MCP clients.

## Architecture

```
┌──────────────────────────────────────────┐
│ research.modelcitizendeveloper.com       │
│ - 169 survey slots                       │
│ - 4PS analysis per survey                │
└────────────────┬─────────────────────────┘
                 │
                 ↓ (cached HTTP)
┌──────────────────────────────────────────┐
│ survey-mcp MCP Server                    │
│ - MCP Resources: survey://<category>/... │
│ - MCP Tools: search, index               │
│ - Local cache (diskcache)                │
└────────────────┬─────────────────────────┘
                 │
                 ↓ (MCP protocol)
┌──────────────────────────────────────────┐
│ MCP Clients                              │
│ - spawn-analysis (decision frameworks)   │
│ - Claude Desktop (direct queries)        │
│ - Other MCPs (SMCP integration)          │
└──────────────────────────────────────────┘
```

## MCP Resources

Access survey data via resource URIs:

```python
# Full survey (all 4PS passes)
survey://1.001-009

# Specific passes
survey://1.001-009/s1-rapid         # Quick comparison
survey://1.001-009/s2-comprehensive # Feature matrix
survey://1.001-009/s3-need-driven   # Use case scenarios
survey://1.001-009/s4-strategic     # Maturity analysis
```

## MCP Tools

### search_surveys(query: str) → list

Find surveys matching a query string.

```python
search_surveys("testing frameworks")
# → ["1.XXX - Python Testing", "1.YYY - JavaScript Testing", ...]
```

### get_survey_index() → dict

Get complete index of all 169 survey slots with completion status.

```python
get_survey_index()
# → {
#     "categories": [...],
#     "surveys": {
#       "1.001-009": {"title": "Sorting & Searching", "complete": 5/9},
#       ...
#     }
#   }
```

## Installation

### For Claude Desktop (WSL)

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "survey": {
      "type": "stdio",
      "command": "wsl",
      "args": ["/home/ivanadamin/gt/research/crew/ivan/packages/survey-mcp/run-mcp.sh"],
      "env": {}
    }
  }
}
```

### For Development

```bash
cd packages/survey-mcp
uv sync
uv run survey-mcp
```

## Integration with spawn-analysis

spawn-analysis can use survey data as context for decision-making:

```python
# In spawn-analysis-mcp
conduct_analysis(
    question="Which Python testing framework?",
    context=mcp.resource("survey://1.XXX/s2-comprehensive"),
    analysts=["optimizer", "capability-auditor", "strategist"]
)
```

## Caching

survey-mcp uses `diskcache` to cache HTTP requests to the research site:
- Cache location: `~/.cache/survey-mcp/`
- TTL: 24 hours (surveys don't change frequently)
- Manual refresh: Delete cache directory

## SMCP Integration (Future)

When SMCP is available, survey-mcp can register with Paulina for service discovery:

```python
# Auto-discovery by other MCPs
survey_server = paulina.discover("survey-data")
context = survey_server.get_resource("1.001-009")
```

## License

Same as parent research project.
