# MCP Python SDK - Library Profile

**Package**: `mcp`
**Version**: 1.24.0 (December 2025)
**License**: MIT
**Maintainer**: Anthropic (dsp, jspahrsummers)
**Repository**: https://github.com/modelcontextprotocol/python-sdk
**Documentation**: https://modelcontextprotocol.github.io/python-sdk/

---

## Overview

The official Python SDK for Model Context Protocol, maintained by Anthropic. It implements the full MCP specification including clients, servers, transports, and protocol messages. This is the reference implementation that other libraries build upon.

---

## Installation

```bash
pip install "mcp[cli]"
# or
uv add "mcp[cli]"
```

**Requirements**: Python >= 3.10

### Optional Extensions

| Extra | Purpose |
|-------|---------|
| `cli` | Command-line interface tools |
| `rich` | Enhanced terminal output |
| `ws` | WebSocket transport support |

---

## Key Statistics

| Metric | Value |
|--------|-------|
| GitHub Stars | 20.6k |
| GitHub Forks | 2.9k |
| Open Issues | 241 |
| License | MIT |
| Last Release | December 12, 2025 |

---

## Core Capabilities

### Server Building

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server

server = Server("my-server")

@server.list_tools()
async def list_tools():
    return [
        {"name": "my_tool", "description": "Does something", "inputSchema": {...}}
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "my_tool":
        return {"content": [{"type": "text", "text": "Result"}]}

async with stdio_server() as (read, write):
    await server.run(read, write, server.create_initialization_options())
```

### Client Building

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="python",
    args=["my_server.py"]
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        tools = await session.list_tools()
```

### FastMCP Integration (Built-in)

The SDK includes `mcp.server.fastmcp` (FastMCP 1.x):

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("server")

@mcp.tool()
def my_tool(param: str) -> str:
    """Tool description."""
    return f"Result: {param}"
```

---

## Transport Support

| Transport | Class | Use Case |
|-----------|-------|----------|
| stdio | `stdio_server()` | Local subprocess |
| Streamable HTTP | `streamable_http_server()` | Remote/networked |
| SSE | `sse_server()` | Legacy (deprecated) |
| WebSocket | `websocket_server()` | Real-time bidirectional |

---

## Protocol Features

### Resources
Read-only data exposure:

```python
@server.list_resources()
async def list_resources():
    return [{"uri": "file:///path", "name": "My File"}]

@server.read_resource()
async def read_resource(uri: str):
    return {"contents": [{"uri": uri, "text": "Content"}]}
```

### Tools
Executable functions:

```python
@server.list_tools()
async def list_tools():
    return [{
        "name": "search",
        "description": "Search database",
        "inputSchema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"]
        }
    }]
```

### Prompts
Reusable templates:

```python
@server.list_prompts()
async def list_prompts():
    return [{"name": "summarize", "description": "Summarization prompt"}]

@server.get_prompt()
async def get_prompt(name: str, arguments: dict):
    return {"messages": [{"role": "user", "content": {"type": "text", "text": "..."}}]}
```

### Structured Output
Type-safe responses (spec revision 2025-06-18):

```python
from pydantic import BaseModel

class SearchResult(BaseModel):
    items: list[str]
    total: int

@mcp.tool()
def search(query: str) -> SearchResult:
    return SearchResult(items=["a", "b"], total=2)
```

---

## Authentication

OAuth 2.1 resource server implementation (`mcp.server.auth`):
- RFC 9728 compliance (Protected Resource Metadata)
- AS discovery
- Token validation
- Scope enforcement

---

## Relationship to FastMCP

| Component | Source | Notes |
|-----------|--------|-------|
| `mcp.server.fastmcp` | FastMCP 1.x | Incorporated into SDK |
| `fastmcp` (pip) | FastMCP 2.x | Standalone, more features |

The SDK's `mcp.server.fastmcp` is FastMCP 1.0, suitable for basic use. For production with enterprise features, use standalone `fastmcp` (2.x).

---

## Strengths

1. **Official**: Reference implementation by Anthropic
2. **MIT License**: Maximum permissiveness
3. **Complete**: Full protocol implementation
4. **Low-level control**: Direct access to all primitives
5. **Minimal**: Fewer abstractions, smaller footprint

---

## Limitations

1. **More verbose**: Requires more boilerplate than FastMCP 2.0
2. **Basic auth**: OAuth support less comprehensive than FastMCP 2.0
3. **Less documentation**: Compared to FastMCP's gofastmcp.com
4. **Steeper learning curve**: Protocol concepts exposed directly

---

## When to Choose MCP SDK

- Need protocol-level control
- Building MCP tooling/frameworks
- Compliance requires official implementation
- Minimal dependency footprint
- MIT license requirement

---

## When to Avoid

- Rapid prototyping (use FastMCP 2.0)
- Enterprise auth needs (FastMCP 2.0 is better)
- Teams unfamiliar with MCP protocol details
- Production deployment with auth requirements

---

## Industry Adoption

MCP has been adopted by major players:
- **OpenAI**: ChatGPT desktop, Agents SDK, Responses API (March 2025)
- **Microsoft**: Native Windows integration (May 2025)
- **Linux Foundation**: MCP donated to Agentic AI Foundation (December 2025)

---

## Sources

- https://github.com/modelcontextprotocol/python-sdk
- https://pypi.org/project/mcp/
- https://modelcontextprotocol.io
- https://modelcontextprotocol.github.io/python-sdk/
