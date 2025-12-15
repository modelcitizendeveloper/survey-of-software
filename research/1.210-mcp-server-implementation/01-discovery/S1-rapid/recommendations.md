# 1.210 MCP Server Implementation - S1 Recommendations

**Research Date**: December 2025
**Category**: 1.2XX AI & LLM Application Frameworks
**Status**: S1 Complete

---

## Executive Summary

For building MCP (Model Context Protocol) servers in Python, **FastMCP 2.0** is the recommended choice for most use cases. It provides the best balance of simplicity, features, and production-readiness while maintaining full protocol compliance.

---

## Library Landscape (December 2025)

| Library | Version | Stars | Use Case | Recommendation |
|---------|---------|-------|----------|----------------|
| **FastMCP** | 2.14.0 | 21.2k | General MCP servers | **Primary choice** |
| **MCP Python SDK** | 1.24.0 | 20.6k | Protocol-level control | When you need low-level access |
| **FastAPI-MCP** | Latest | ~1k | Existing FastAPI apps | Brownfield projects only |
| **Raw JSON-RPC** | N/A | N/A | Learning/embedded | Educational or minimal deps |

---

## Primary Recommendation: FastMCP 2.0

**Install**: `pip install fastmcp` or `uv add fastmcp`

### Why FastMCP

1. **Simplicity**: Decorator-based API requires minimal boilerplate
2. **Production-ready**: Enterprise auth, deployment tools, testing utilities
3. **Active development**: 21.2k stars, frequent updates, Prefect backing
4. **Protocol compliance**: Built on official SDK, full MCP spec support
5. **Proven**: spawn-experiments 1.618 validated it "makes MCP trivial"

### When to Use

- New MCP server projects (greenfield)
- Rapid prototyping
- Production deployments needing auth
- Teams wanting Pythonic API design

### Example

```python
from fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def my_tool(param: str) -> dict:
    """Tool description for LLM."""
    return {"result": param}

if __name__ == "__main__":
    mcp.run()
```

---

## Alternative: Official MCP Python SDK

**Install**: `pip install "mcp[cli]"` or `uv add "mcp[cli]"`

### Why SDK Instead

1. **Protocol-level control**: Direct access to all MCP primitives
2. **Official support**: Maintained by Anthropic
3. **Minimal dependencies**: No FastMCP abstractions
4. **Compliance-critical**: When exact protocol behavior matters

### When to Use

- Need fine-grained protocol control
- Building MCP tooling/frameworks
- Compliance requirements for official implementations
- Debugging protocol-level issues

### Note on Relationship

FastMCP 1.0 was incorporated into the official SDK as `mcp.server.fastmcp`. FastMCP 2.0 is the standalone, feature-rich evolution. Both work, but FastMCP 2.0 has more features.

---

## Brownfield Option: FastAPI-MCP

**Install**: `pip install fastapi-mcp`

### Why FastAPI-MCP

1. **Zero configuration**: Automatically exposes existing endpoints as MCP tools
2. **Preserves auth**: Reuses FastAPI `Depends()` for authorization
3. **ASGI-native**: No HTTP hop, direct integration

### When to Use

- Existing FastAPI application
- Want to expose REST endpoints to LLMs without rewrite
- Need to maintain both REST and MCP interfaces

### Example

```python
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

app = FastAPI()
mcp = FastApiMCP(app)
mcp.mount()  # Available at /mcp
```

### Limitation

Not suitable for new MCP-first projects - use FastMCP instead.

---

## Educational Option: Raw JSON-RPC

### Why Raw Implementation

1. **Learning**: Understand MCP protocol internals
2. **Minimal deps**: No external libraries needed
3. **Embedded**: When SDK overhead is unacceptable

### Key Insight

> "At its core, MCP is just JSON-RPC 2.0 over newline-delimited streams. No magic, no hidden complexity."

### When to Use

- Learning the protocol
- Extremely resource-constrained environments
- Building custom transports
- Protocol debugging

### Caveat

Requires implementing schema validation, message routing, error handling manually. Only recommended for educational purposes or very specific constraints.

---

## Transport Selection

| Transport | Use Case | Latency | Complexity |
|-----------|----------|---------|------------|
| **stdio** | Local subprocess, CLI tools | Lowest | Lowest |
| **Streamable HTTP** | Remote/networked, production | Medium | Medium |
| **SSE** | Legacy (deprecated 2024-11) | Medium | Higher |

### Recommendation

- **Local development**: stdio (default)
- **Production/remote**: Streamable HTTP
- **Legacy systems**: SSE only if required

---

## Decision Matrix

| Scenario | Recommendation |
|----------|----------------|
| New MCP server, any use case | FastMCP 2.0 |
| Existing FastAPI app | FastAPI-MCP |
| Protocol debugging/tooling | MCP Python SDK |
| Learning MCP internals | Raw JSON-RPC |
| Enterprise with auth needs | FastMCP 2.0 (built-in OAuth) |
| Minimal dependencies | MCP Python SDK |

---

## Key Findings from spawn-experiments 1.618

The methodology experiment (1.618-mcp-server) tested building MCP servers using FastMCP:

- **FastMCP makes MCP trivial**: Decorator-based API requires no protocol knowledge
- **Spec-driven less critical**: MCP tool schemas are auto-generated
- **Winner**: M4 (Mutation TDD) at 93/100, but M1 (Immediate) scored 92/100
- **Insight**: Library simplicity neutralized methodology differences

---

## Not Recommended

### pymcp, mcp-framework (Python)
- No significant Python packages found with these names
- TypeScript has MCP-Framework, but Python ecosystem centers on FastMCP + SDK

### Building from scratch (production)
- Unless you have specific constraints, use FastMCP
- Protocol details are non-trivial (handshake, capabilities, schema validation)

---

## Sources

- [FastMCP GitHub](https://github.com/jlowin/fastmcp) (21.2k stars)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) (20.6k stars)
- [FastAPI-MCP GitHub](https://github.com/tadata-org/fastapi_mcp)
- [FastMCP PyPI](https://pypi.org/project/fastmcp/)
- [MCP PyPI](https://pypi.org/project/mcp/)
- [MCP Transports Documentation](https://modelcontextprotocol.io/docs/concepts/transports)
- [Raw STDIO Implementation Guide](https://foojay.io/today/understanding-mcp-through-raw-stdio-communication/)

---

**Next Steps**: S2 will include benchmarks, architecture patterns, and multi-tenant design guidance.
