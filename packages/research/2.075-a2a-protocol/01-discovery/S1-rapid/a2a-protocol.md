# 2.075: A2A (Agent2Agent Protocol) - S1 Rapid Research

**Date**: December 18, 2025
**Status**: S1 Complete
**Governance**: Linux Foundation (A2A Project), initiated by Google
**Spec Version**: 0.3 (as of Dec 2025)

---

## Executive Summary

A2A is an open protocol for **agent-to-agent communication**, enabling AI agents from different vendors to discover each other, negotiate interactions, and collaborate on tasks. It complements MCP (which handles agent↔tool integration) by providing **horizontal integration** between autonomous agents.

---

## Protocol Overview

### What A2A Standardizes

| Capability | Description |
|------------|-------------|
| **Agent Discovery** | Agent Cards (JSON metadata) at `/.well-known/agent.json` |
| **Task Management** | Stateful tasks with lifecycle (submitted → working → completed) |
| **Message Exchange** | Multi-turn conversations with role-based messages |
| **Artifact Delivery** | Structured output (text, files, data) from completed tasks |
| **Authentication** | API Key, OAuth2, OIDC, mTLS support |

### Protocol Foundation

- **Transport**: HTTP(S) with TLS 1.3+
- **Payload**: JSON-RPC 2.0
- **Streaming**: Server-Sent Events (SSE)
- **Push**: Webhook notifications
- **Bindings**: JSON-RPC, gRPC, REST

---

## Core Concepts

### Agent Cards

Digital business cards describing agent capabilities:

```json
{
  "name": "Currency Converter Agent",
  "description": "Converts between currencies using live rates",
  "url": "https://currency-agent.example.com",
  "version": "1.0.0",
  "capabilities": {
    "streaming": true,
    "pushNotifications": true
  },
  "skills": [
    {
      "id": "convert-currency",
      "name": "Convert Currency",
      "description": "Convert amount between two currencies"
    }
  ],
  "authentication": {
    "schemes": ["apiKey", "oauth2"]
  }
}
```

**Discovery**: Agents publish at `/.well-known/agent.json`

### Tasks

Stateful work units with defined lifecycle:

```
SUBMITTED → WORKING → COMPLETED
                   ↘ FAILED
                   ↘ CANCELLED
                   ↘ INPUT_REQUIRED (awaiting user input)
                   ↘ AUTH_REQUIRED (needs authentication)
```

### Messages and Parts

Messages contain **Parts** (modality-independent content):

| Part Type | Use Case |
|-----------|----------|
| `TextPart` | Plain text content |
| `FilePart` | Files (inline Base64 or URI) |
| `DataPart` | Structured JSON (forms, parameters) |

### Artifacts

Deliverables from completed tasks (distinct from conversational messages):

```json
{
  "id": "artifact-123",
  "name": "Conversion Result",
  "parts": [
    {"type": "data", "data": {"from": "USD", "to": "EUR", "result": 0.92}}
  ]
}
```

---

## JSON-RPC Methods (11 Operations)

| Method | Purpose |
|--------|---------|
| `message/send` | Send message, get Task or Message response |
| `message/stream` | Streaming message with incremental updates |
| `tasks/get` | Get task state and artifacts |
| `tasks/list` | Query tasks with filtering |
| `tasks/cancel` | Cancel a task |
| `tasks/subscribe` | Stream updates for existing task |
| `tasks/pushNotification/set` | Register webhook |
| `tasks/pushNotification/get` | Get webhook config |
| `tasks/pushNotification/list` | List all webhooks for task |
| `tasks/pushNotification/delete` | Remove webhook |
| `agent/authenticatedExtendedCard` | Get detailed card post-auth |

---

## Python SDK

### Installation

```bash
pip install a2a-sdk
# or with extras
pip install "a2a-sdk[http-server,grpc,telemetry,sql]"
```

### Creating an A2A Server

```python
from a2a.server import A2AServer
from a2a.server.agent_execution import AgentExecutor
from a2a.types import AgentCard, Skill

class MyAgentExecutor(AgentExecutor):
    async def execute(self, context, event_queue):
        # Process incoming message
        message = context.message

        # Do work...
        result = await self.process(message)

        # Send response
        await event_queue.enqueue_event(
            agent_message(result)
        )

    async def cancel(self, context, event_queue):
        # Handle cancellation
        pass

# Define agent card
agent_card = AgentCard(
    name="My Agent",
    description="Does useful things",
    skills=[
        Skill(id="do-thing", name="Do Thing", description="Does the thing")
    ]
)

# Start server
server = A2AServer(
    agent_card=agent_card,
    executor=MyAgentExecutor()
)
server.run(port=8000)
```

### Creating an A2A Client

```python
from a2a.client import A2AClient

async def call_agent():
    client = A2AClient(base_url="https://agent.example.com")

    # Discover agent
    card = await client.get_agent_card()
    print(f"Agent: {card.name}, Skills: {card.skills}")

    # Send message
    response = await client.send_message(
        message="Convert 100 USD to EUR"
    )

    # Handle task if returned
    if response.task:
        task = await client.get_task(response.task.id)
        print(f"Status: {task.status.state}")
        print(f"Artifacts: {task.artifacts}")
```

---

## A2A vs MCP: Complementary Roles

| Aspect | MCP | A2A |
|--------|-----|-----|
| **Purpose** | Agent↔Tool integration | Agent↔Agent collaboration |
| **Abstraction** | Vertical (model to resources) | Horizontal (peer agents) |
| **Communication** | Function calls | Multi-turn conversations |
| **State** | Stateless operations | Stateful tasks |
| **Discovery** | MCP server config | Agent Cards at well-known URL |
| **Typical Use** | Database queries, API calls | Delegation, coordination |

### When to Use Each

```
┌─────────────────────────────────────────────────────────────┐
│                     Agent Application                        │
│                                                              │
│   ┌─────────────┐         A2A          ┌─────────────┐      │
│   │   Agent A   │◄────────────────────►│   Agent B   │      │
│   └──────┬──────┘                      └──────┬──────┘      │
│          │ MCP                                │ MCP         │
│          ▼                                    ▼             │
│   ┌─────────────┐                      ┌─────────────┐      │
│   │   Tools     │                      │   Tools     │      │
│   │ (Database,  │                      │ (APIs,      │      │
│   │  APIs, etc) │                      │  Services)  │      │
│   └─────────────┘                      └─────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

**Official guidance**: "Use MCP for tools and A2A for agents"
- Tools = primitives with structured I/O and well-known behavior
- Agents = autonomous applications that reason and interact

---

## Adoption & Ecosystem

### Support (as of Dec 2025)

- **150+ organizations** including all hyperscalers
- **SDKs**: Python, Go, JavaScript, Java, .NET
- **GitHub**: 21.1k stars, 449 commits
- **Governance**: Linux Foundation (June 2025)

### Major Adopters

- Google (creator)
- Atlassian, Box, Cohere, Intuit, LangChain
- MongoDB, PayPal, Salesforce, SAP, ServiceNow
- Accenture, BCG, Deloitte, KPMG, McKinsey, PwC

---

## Use Cases

### 1. Task Delegation

A customer service agent delegates billing inquiries to a specialized billing agent.

### 2. Multi-Agent Coordination

A travel agent coordinates with flight, hotel, and activity agents to plan a trip.

### 3. Enterprise Integration

Different departments' AI agents collaborate across organizational boundaries.

### 4. Tool + Agent Hybrid

Agent uses MCP to access its tools (databases, APIs) and A2A to collaborate with other agents.

---

## Security Considerations

- **TLS 1.3+** required for all communication
- **Authentication schemes**: API Key, HTTP Auth, OAuth2, OIDC, mTLS
- **Agent Cards** declare supported auth schemes
- **Extended Agent Cards** available post-authentication with enhanced capabilities
- Treat external agents as potentially untrusted entities

---

## Comparison with Other Protocols

| Protocol | Focus | Governance | Maturity |
|----------|-------|------------|----------|
| **MCP** | Agent↔Tool | Linux Foundation (AAIF) | Production |
| **A2A** | Agent↔Agent | Linux Foundation | Production (v0.3) |
| **ACP** | Message infrastructure | Linux Foundation | Emerging |
| **ANP** | Decentralized networks | Cisco | Early |

---

## Sources

- [A2A Protocol Specification](https://a2a-protocol.org/latest/specification/)
- [A2A Key Concepts](https://a2a-protocol.org/latest/topics/key-concepts/)
- [A2A and MCP Comparison](https://a2a-protocol.org/latest/topics/a2a-and-mcp/)
- [A2A Python SDK](https://github.com/a2aproject/a2a-python)
- [A2A GitHub Repository](https://github.com/a2aproject/A2A)
- [Google Developers Blog - A2A Announcement](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
- [Linux Foundation A2A Launch](https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents)
