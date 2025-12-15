# 2.074 MCP Protocol - Implementation Landscape

**Research Date**: December 2025
**Category**: 2.0XX Open Standards & Portability Layer

---

## Overview

MCP has multiple implementations across languages and platforms. This document catalogs the ecosystem for portability assessment.

---

## Official SDKs

### Python SDK
- **Package**: `mcp`
- **Version**: 1.24.0 (Dec 2025)
- **Maintainer**: Anthropic
- **License**: MIT
- **Features**: Full protocol, all transports, OAuth 2.1
- **Repository**: https://github.com/modelcontextprotocol/python-sdk

### TypeScript SDK
- **Package**: `@modelcontextprotocol/sdk`
- **Maintainer**: Anthropic
- **License**: MIT
- **Features**: Full protocol, all transports
- **Repository**: https://github.com/modelcontextprotocol/typescript-sdk

---

## Third-Party SDKs

### Python

| Library | Stars | Focus | Maintainer |
|---------|-------|-------|------------|
| **FastMCP** | 21.2k | High-level framework | Prefect |
| **FastAPI-MCP** | ~1k | FastAPI integration | Tadata Inc |

### Other Languages

| Language | Library | Status |
|----------|---------|--------|
| Go | Community SDKs | Emerging |
| Java | Quarkus MCP SDK | Production |
| Rust | Community SDKs | Emerging |
| C# | Community SDKs | Emerging |

---

## MCP Clients

### Major Clients (December 2025)

| Client | Company | Platform | Notes |
|--------|---------|----------|-------|
| **Claude Desktop** | Anthropic | Desktop app | Original client |
| **Claude.ai** | Anthropic | Web | Browser-based |
| **ChatGPT Desktop** | OpenAI | Desktop app | Since Mar 2025 |
| **Gemini** | Google | Web/API | Since Apr 2025 |
| **VS Code** | Microsoft | IDE | Since May 2025 |
| **Cursor** | Cursor | IDE | Developer-focused |
| **Microsoft Copilot** | Microsoft | Various | Windows integration |

### Client Compatibility

All clients implement the same MCP specification:
- Any MCP server works with any MCP client
- No server changes needed when switching clients
- Protocol-level compatibility guaranteed

---

## Managed MCP Infrastructure

### Google Cloud
- Managed MCP servers for Maps, BigQuery, Compute Engine, Kubernetes Engine
- "Agent-ready by design"
- Launched Dec 2025

### AWS
- MCP servers for Lambda, ECS, EKS, Fargate
- Bedrock MCP integration
- Enterprise deployment support

### FastMCP Cloud
- Hosted MCP server deployment
- By Prefect
- Managed auth, scaling

---

## Server Ecosystem

### Ecosystem Size (December 2025)

| Metric | Count |
|--------|-------|
| Active public servers | 10,000+ |
| Registered servers | 5,800+ |
| Monthly SDK downloads | 97M+ |
| MCP clients | 300+ |

### Server Categories

| Category | Examples |
|----------|----------|
| **Database** | PostgreSQL, MongoDB, Supabase |
| **Cloud** | AWS, GCP, Azure services |
| **Productivity** | Notion, Slack, GitHub |
| **Search** | Brave Search, Tavily |
| **Development** | Git, Docker, CI/CD |
| **Custom** | Internal APIs, proprietary systems |

---

## Transport Implementations

### stdio
- **Support**: All SDKs
- **Use case**: Local subprocess
- **Complexity**: Lowest
- **Performance**: Best for local

### Streamable HTTP
- **Support**: All SDKs (since 2025-03)
- **Use case**: Remote/networked
- **Complexity**: Medium
- **Performance**: Production-ready

### SSE (Legacy)
- **Support**: Deprecated since 2024-11
- **Use case**: Legacy only
- **Complexity**: Higher
- **Performance**: Suboptimal

### WebSocket
- **Support**: Extension (`mcp[ws]`)
- **Use case**: Real-time bidirectional
- **Complexity**: Higher
- **Performance**: Good for streaming

---

## Auth Implementations

### OAuth 2.1 (Standard)
- Built into spec since 2025-03-26
- RFC 9728 compliance
- Resource indicators (RFC 8707)

### FastMCP Enterprise Auth
- Google, GitHub, Azure, Auth0, WorkOS
- Zero-configuration OAuth providers
- Additional to spec

### Custom Auth
- API keys
- JWT tokens
- Custom schemes (not spec-compliant)

---

## Compatibility Matrix

| SDK | stdio | HTTP | SSE | OAuth | Structured Output |
|-----|-------|------|-----|-------|-------------------|
| Python SDK 1.24 | ✓ | ✓ | ✓ | ✓ | ✓ |
| FastMCP 2.14 | ✓ | ✓ | ✓ | ✓+ | ✓ |
| TypeScript SDK | ✓ | ✓ | ✓ | ✓ | ✓ |
| FastAPI-MCP | - | ✓ | - | ✓ | ✓ |

---

## Migration Paths

### From Custom Integration

```
Custom LLM Integration
         │
         ▼ (20-80 hours)
   MCP Server (FastMCP)
         │
         ▼ (0 hours)
   Works with all MCP clients
```

### From REST API

```
FastAPI REST API
         │
         ▼ (2-8 hours)
   FastAPI-MCP or FastMCP.from_fastapi()
         │
         ▼ (0 hours)
   Dual REST + MCP support
```

### Between SDKs

```
FastMCP Server
         │
         ▼ (1-2 hours, import changes)
   MCP SDK Server
         │
         ▼ (0 hours)
   Same clients work
```

---

## Interoperability Evidence

### Cross-Vendor Testing

| Server SDK | Client | Status |
|------------|--------|--------|
| Python SDK | Claude Desktop | ✓ Works |
| Python SDK | ChatGPT Desktop | ✓ Works |
| FastMCP | Claude Desktop | ✓ Works |
| FastMCP | VS Code | ✓ Works |
| TypeScript SDK | Claude Desktop | ✓ Works |

### Protocol Compliance

All major implementations pass MCP protocol test suites:
- Tool registration
- Resource access
- Prompt handling
- Transport negotiation
- Auth flows (2025-03+)

---

## Sources

- [MCP GitHub Organization](https://github.com/modelcontextprotocol)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- [Google Managed MCP](https://techcrunch.com/2025/12/10/google-is-going-all-in-on-mcp-servers-agent-ready-by-design/)
- [AWS MCP Servers](https://aws.amazon.com/blogs/compute/)
- [One Year of MCP](https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/)
