# FastMCP 2.0 - Library Profile

**Package**: `fastmcp`
**Version**: 2.14.0 (December 2025)
**License**: Apache-2.0
**Maintainer**: Jeremiah Lowin (@jlowin), Prefect
**Repository**: https://github.com/jlowin/fastmcp
**Documentation**: https://gofastmcp.com

---

## Overview

FastMCP is a high-level Python framework for building MCP servers and clients. Originally created independently, FastMCP 1.0 was incorporated into the official MCP SDK in 2024. FastMCP 2.0 is the actively maintained standalone version with enterprise features.

---

## Installation

```bash
pip install fastmcp
# or
uv add fastmcp
```

**Requirements**: Python >= 3.10

---

## Key Statistics

| Metric | Value |
|--------|-------|
| GitHub Stars | 21.2k |
| GitHub Forks | 1.6k |
| Open Issues | 201 |
| PyPI Downloads | High (exact count varies) |
| Last Release | December 11, 2025 |

---

## Core Features

### Tools
Decorated Python functions exposing functionality to LLMs:

```python
from fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def search_database(query: str, limit: int = 10) -> list[dict]:
    """Search the database for matching records."""
    return db.search(query, limit=limit)
```

### Resources
Read-only data sources with templated URIs:

```python
@mcp.resource("config://{section}")
def get_config(section: str) -> str:
    """Get configuration for a section."""
    return config.get(section)
```

### Prompts
Reusable message templates:

```python
@mcp.prompt()
def summarize_prompt(text: str) -> str:
    """Create a summarization prompt."""
    return f"Please summarize the following text:\n\n{text}"
```

### Context
Access to session features within decorated functions:

```python
from fastmcp import Context

@mcp.tool()
async def long_task(ctx: Context) -> str:
    await ctx.report_progress(0.5, "Halfway done")
    return "Complete"
```

---

## Enterprise Features (FastMCP 2.0)

### Authentication
Built-in OAuth providers with zero-configuration setup:
- Google
- GitHub
- Azure
- Auth0
- WorkOS
- Descope
- Discord
- JWT (custom)
- API Keys

### Deployment Options
- Local development via CLI
- FastMCP Cloud (hosted)
- Self-hosted HTTP/SSE

### Advanced Patterns
- Server composition and mounting
- Proxy servers for transport bridging
- OpenAPI integration (`FastMCP.from_openapi()`)
- FastAPI integration (`FastMCP.from_fastapi()`)
- Tool transformation

### Testing
In-memory client for unit testing without network:

```python
from fastmcp import Client

async with Client(mcp) as client:
    result = await client.call_tool("my_tool", {"param": "value"})
```

---

## Transport Support

| Transport | Support | Notes |
|-----------|---------|-------|
| stdio | Full | Default for local |
| Streamable HTTP | Full | Production recommended |
| SSE | Full | Legacy support |
| WebSocket | Via extension | `mcp[ws]` |

---

## Dependency Note

FastMCP depends on Cyclopts for CLI functionality. Cyclopts v4 includes docutils as a transitive dependency with complex licensing. Organizations with strict compliance may need to use Cyclopts v5 alpha or wait for stable release.

---

## Relationship to Official SDK

| Aspect | mcp.server.fastmcp | fastmcp (standalone) |
|--------|--------------------|-----------------------|
| Version | 1.x (in SDK) | 2.x |
| Features | Basic | Full enterprise |
| Auth | Limited | Comprehensive |
| Maintained | By Anthropic | By Prefect |
| Import | `from mcp.server.fastmcp` | `from fastmcp` |

**Recommendation**: Use standalone `fastmcp` for new projects (more features, actively developed).

---

## Strengths

1. **Simplicity**: Minimal boilerplate, decorator-based
2. **Production-ready**: Enterprise auth, deployment tools
3. **Well-documented**: Comprehensive docs at gofastmcp.com
4. **Active community**: 21.2k stars, responsive maintainers
5. **Proven**: Validated in spawn-experiments 1.618

---

## Limitations

1. **Apache-2.0 license**: May require attribution (not MIT like SDK)
2. **Cyclopts dependency**: Licensing complexity for some orgs
3. **Abstraction layer**: Less control than raw SDK
4. **Prefect backing**: Tied to Prefect's business interests

---

## When to Choose FastMCP

- New MCP server projects
- Rapid prototyping
- Production deployments
- Teams wanting Pythonic API
- Enterprise auth requirements

---

## When to Avoid

- Need protocol-level control
- Minimal dependency requirements
- Building MCP tooling/frameworks
- License compliance concerns with Apache-2.0

---

## Example: Complete Server

```python
from fastmcp import FastMCP

mcp = FastMCP("task-manager")
tasks = {}
task_id = 0

@mcp.tool()
def create_task(title: str, priority: str = "medium") -> dict:
    """Create a new task."""
    global task_id
    task_id += 1
    tasks[task_id] = {"id": task_id, "title": title, "priority": priority}
    return tasks[task_id]

@mcp.tool()
def list_tasks(status: str = "all") -> list[dict]:
    """List all tasks."""
    return list(tasks.values())

if __name__ == "__main__":
    mcp.run()
```

---

## Sources

- https://github.com/jlowin/fastmcp
- https://pypi.org/project/fastmcp/
- https://gofastmcp.com
- https://www.prefect.io/fastmcp
