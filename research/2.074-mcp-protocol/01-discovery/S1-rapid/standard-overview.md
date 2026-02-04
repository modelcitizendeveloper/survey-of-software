# 2.074 MCP Protocol - Standard Overview

**Research Date**: December 2025
**Category**: 2.0XX Open Standards & Portability Layer
**Status**: S1 Complete

---

## Executive Summary

**MCP (Model Context Protocol)** has achieved the maturity of a true open standard. In December 2025, Anthropic donated MCP to the Linux Foundation's Agentic AI Foundation (AAIF), joining OpenAI, Google, Microsoft, AWS, and others in governance. With 97+ million monthly SDK downloads and adoption by all major AI platforms, MCP meets 2.xxx criteria for an open standard.

**Verdict**: MCP qualifies as a 2.xxx Open Standard despite its young age (1 year).

---

## Standard Identity

| Attribute | Value |
|-----------|-------|
| **Name** | Model Context Protocol (MCP) |
| **Purpose** | Standardize LLM-to-tool/data integration |
| **Governing Body** | Agentic AI Foundation (Linux Foundation) |
| **Original Creator** | Anthropic |
| **License** | MIT (specification), Apache-2.0 (SDKs vary) |
| **First Release** | November 2024 |
| **Current Version** | 2025-11-25 |
| **Protocol Type** | JSON-RPC 2.0 based |

---

## Governance Structure

### Pre-December 2025
- Anthropic-controlled with community input
- SEP (Specification Enhancement Proposal) process
- Open-source development on GitHub

### Post-December 2025 (Current)
- **Agentic AI Foundation (AAIF)** under Linux Foundation
- **Co-founders**: Anthropic, Block, OpenAI
- **Supporters**: Google, Microsoft, AWS, Cloudflare, Bloomberg

### Governance Model
> "The AAIF Governing Board will make decisions regarding strategic investments, budget allocation, member recruitment, and approval of new projects, while individual projects, such as MCP, maintain full autonomy over their technical direction and day-to-day operations."

**Key Point**: Technical decisions remain with maintainers; strategic decisions with AAIF board.

---

## Maturity Assessment

### 2.xxx Criteria Evaluation

| Criterion | Required | MCP Status | Assessment |
|-----------|----------|------------|------------|
| Vendor-neutral governance | Yes | Linux Foundation (Dec 2025) | **PASS** |
| Multiple implementations | 5+ | 10,000+ servers, major SDKs | **PASS** |
| Production maturity | Graduated/stable | 4 spec versions, enterprise use | **PASS** |
| True portability | Config switch | Protocol-level, any client | **PASS** |
| Industry adoption | 100+ companies | Google, OpenAI, Microsoft, AWS | **PASS** |

### Version History

| Version | Date | Key Changes |
|---------|------|-------------|
| 2024-11-05 | Nov 2024 | Initial release |
| 2025-03-26 | Mar 2025 | OAuth 2.1, Streamable HTTP, Tool annotations |
| 2025-06-18 | Jun 2025 | Structured outputs, RFC 8707, Server interactions |
| 2025-11-25 | Nov 2025 | Tasks abstraction, community features |

### Adoption Metrics (December 2025)

- **97+ million** monthly SDK downloads
- **10,000+** active public servers
- **5,800+** registered MCP servers
- **300+** MCP clients

---

## Major Adopters

| Company | Adoption Date | Products |
|---------|---------------|----------|
| **Anthropic** | Nov 2024 | Claude Desktop, Claude.ai |
| **OpenAI** | Mar 2025 | ChatGPT Desktop, Agents SDK, Responses API |
| **Google** | Apr 2025 | Gemini, Agent Development Kit, managed MCP servers |
| **Microsoft** | May 2025 | VS Code 1.101, Windows integration, Copilot |
| **AWS** | 2025 | Lambda, ECS, EKS, Fargate, Bedrock |
| **Cursor** | 2025 | IDE integration |
| **Block** | 2025 | goose framework |

---

## What MCP Standardizes

### Core Primitives

1. **Tools**: Functions an LLM can invoke (like POST endpoints)
2. **Resources**: Read-only data access (like GET endpoints)
3. **Prompts**: Reusable message templates
4. **Context**: Session state and capabilities

### Transports

| Transport | Status | Use Case |
|-----------|--------|----------|
| stdio | Standard | Local subprocess communication |
| Streamable HTTP | Standard (2025-03) | Remote/networked production |
| SSE | Deprecated (2024-11) | Legacy support |
| WebSocket | Extension | Real-time bidirectional |

### Protocol Details

- **Message Format**: JSON-RPC 2.0
- **Authentication**: OAuth 2.1 (since 2025-03-26)
- **Content Types**: Text, Images, Audio (since 2025-03)
- **Structured Output**: Pydantic/TypedDict (since 2025-06)

---

## What MCP Does NOT Standardize

| Aspect | Status | Notes |
|--------|--------|-------|
| Agent-to-agent communication | Not covered | Use A2A protocol |
| Multi-agent orchestration | Not covered | Framework-specific |
| Model selection | Not covered | Client decision |
| Training/fine-tuning | Not covered | Out of scope |
| Pricing/billing | Not covered | Provider-specific |

---

## Related Protocols

### A2A (Agent-to-Agent Protocol)
- **Creator**: Google (April 2025)
- **Purpose**: Agent-to-agent communication (horizontal)
- **Relationship**: Complementary to MCP (vertical)

### ACP (Agent Communication Protocol)
- **Creator**: IBM (BeeAI framework)
- **Purpose**: Inter-framework agent communication

### Comparison

| Protocol | Focus | Creator | Status |
|----------|-------|---------|--------|
| **MCP** | Agent-to-tool | Anthropic → AAIF | Production |
| **A2A** | Agent-to-agent | Google | Production |
| **ACP** | Framework-to-framework | IBM | Emerging |

**Key Insight**: MCP and A2A are complementary, not competing.

---

## Lock-in Analysis

### Lock-in Risk: **LOW**

| Factor | Assessment |
|--------|------------|
| **Specification** | Open, MIT licensed |
| **Governance** | Vendor-neutral (Linux Foundation) |
| **Implementations** | Multiple SDKs (Python, TypeScript, etc.) |
| **Clients** | Any MCP-compatible client works |
| **Migration** | Protocol-level portability |

### Switching Costs

| Scenario | Effort | Notes |
|----------|--------|-------|
| Switch MCP SDK | ~1-2 hours | Config/import changes only |
| Switch MCP client | ~0 hours | Server unchanged |
| Move server to new host | ~1-4 hours | Deployment config only |
| Migrate from custom → MCP | 20-80 hours | Depends on complexity |

### What Could Cause Lock-in

1. **Vendor-specific extensions**: Using non-standard features
2. **Proprietary auth**: Custom auth beyond OAuth 2.1
3. **Client-specific features**: Relying on Claude-only capabilities

### Mitigation

- Stick to core MCP primitives
- Use standard OAuth 2.1 auth
- Test with multiple clients

---

## Portability Test

**Can you switch implementations via config only?**

| Switch | Config Only? | Time |
|--------|--------------|------|
| FastMCP → MCP SDK | Mostly (import changes) | 1-2 hours |
| Claude Desktop → ChatGPT | Yes (client config) | <1 hour |
| stdio → HTTP transport | Yes (run config) | <1 hour |
| Self-hosted → Cloud | Depends on auth | 2-4 hours |

**Conclusion**: MCP passes the 2.xxx portability test.

---

## Sources

- [MCP joins the Agentic AI Foundation](https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/)
- [Linux Foundation AAIF Announcement](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)
- [Anthropic Donation Announcement](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)
- [MCP Specification Changelog](https://modelcontextprotocol.io/specification/2025-03-26/changelog)
- [MCP Wikipedia](https://en.wikipedia.org/wiki/Model_Context_Protocol)
- [GitHub Blog: MCP joins Linux Foundation](https://github.blog/open-source/maintainers/mcp-joins-the-linux-foundation-what-this-means-for-developers-building-the-next-era-of-ai-tools-and-agents/)
- [One Year of MCP](https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/)
