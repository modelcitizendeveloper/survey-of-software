# 29: Matrix Protocol Explainer

**Date**: 2025-12-22
**Purpose**: Reference document for Matrix concepts relevant to Factumerit

---

## Overview

**Matrix** is an open protocol for decentralized, real-time communication. Think of it like email: anyone can run their own server, and servers talk to each other.

```
┌─────────────────────────────────────────────────────────────────┐
│                     THE MATRIX NETWORK                          │
│                                                                  │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐        │
│  │ matrix.org   │   │ element.io   │   │ company.com  │        │
│  │ (server)     │◄─►│ (server)     │◄─►│ (server)     │        │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘        │
│         │                  │                  │                 │
│         ▼                  ▼                  ▼                 │
│  @alice:matrix.org  @bob:element.io  @carol:company.com        │
│                                                                  │
│  All three can chat, despite being on different servers         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Terms

### Matrix

**What**: Open standard protocol for real-time communication.

**Analogy**: Like SMTP is to email, Matrix is to chat.

**Features**:
- Decentralized (no single company controls it)
- Federated (servers interconnect)
- End-to-end encrypted (E2EE)
- Open spec (anyone can implement)

**Not**: Matrix is not an app or a company. It's a protocol.

---

### Homeserver

**What**: A server that implements the Matrix protocol. Where your account lives.

**Analogy**: Like your email provider (Gmail, Outlook, self-hosted).

**Examples**:
- matrix.org (free, public, run by Matrix Foundation)
- element.io (run by Element, the company)
- Your own server (self-hosted)

**Your identity**: `@username:homeserver.com`
- `@factumerit:matrix.org` = account on matrix.org
- `@bot:factumerit.app` = account on your own server

---

### Federation

**What**: Servers talking to each other so users on different servers can communicate.

**How it works**:
```
Alice (@alice:server-a.com) sends message to Bob (@bob:server-b.com)

1. Alice's client → Server A
2. Server A looks up Server B via DNS
3. Server A → Server B (server-to-server API)
4. Server B → Bob's client
```

**Why it matters for Factumerit**:
- Bot on matrix.org can receive DMs from users on ANY Matrix server
- Bot on factumerit.app can receive DMs from matrix.org users
- Zero friction - users don't need to join your server

**Requirements for federation**:
- Public domain with DNS
- Valid TLS certificate
- Correct `.well-known` or SRV records
- Port 8448 accessible (server-to-server)

---

### Rooms

**What**: Where conversations happen. Like Slack channels.

**Types**:
- **Public room**: Anyone can join, discoverable
- **Private room**: Invite-only
- **DM (Direct Message)**: Private room with just two users
- **Space**: Collection of rooms (like Slack workspace)

**For Factumerit bot**:
- Users DM the bot (private 1:1 room)
- Bot could also join public rooms and respond to mentions

---

## Server Implementations

### Synapse

**What**: The original, reference Matrix server implementation.

| Aspect | Detail |
|--------|--------|
| Language | Python |
| Maturity | Production-ready, most features |
| Resources | Heavy (1-4GB RAM typical) |
| Use case | Large deployments, full feature set |

**Pros**:
- Most complete implementation
- Best tested
- All features work

**Cons**:
- Resource hungry
- Python = slower
- Complex configuration

**Verdict**: Overkill for a bot.

---

### Dendrite

**What**: Second-generation Matrix server, designed to be lighter.

| Aspect | Detail |
|--------|--------|
| Language | Go |
| Maturity | Production-ready (as of 2023) |
| Resources | Light (256MB-512MB RAM) |
| Use case | Small deployments, bots, self-hosting |

**Pros**:
- Single binary (easy deploy)
- Low resource usage
- Fast (Go)
- Good for Render/Docker

**Cons**:
- Some edge-case features missing
- Smaller community
- Less battle-tested at scale

**Verdict**: Best choice for Factumerit self-hosting.

---

### Conduit

**What**: Experimental Matrix server in Rust.

| Aspect | Detail |
|--------|--------|
| Language | Rust |
| Maturity | Beta/experimental |
| Resources | Very light (~50MB RAM) |
| Use case | Hobbyists, extreme resource constraints |

**Pros**:
- Extremely lightweight
- Single binary
- Fast

**Cons**:
- Not production-ready
- Missing features
- Small team

**Verdict**: Too experimental for production.

---

### Comparison

| Server | RAM | Language | Maturity | Best For |
|--------|-----|----------|----------|----------|
| Synapse | 1-4GB | Python | Stable | Large orgs |
| Dendrite | 256MB | Go | Stable | Bots, small teams |
| Conduit | 50MB | Rust | Beta | Experiments |

---

## End-to-End Encryption (E2EE)

### How It Works

Matrix uses **Megolm** (group encryption) and **Olm** (1:1 encryption).

```
Alice's device                           Bob's device
     │                                        │
     ▼                                        ▼
┌─────────────┐                        ┌─────────────┐
│ Private key │                        │ Private key │
│ (never leaves)                       │ (never leaves)
└─────────────┘                        └─────────────┘
     │                                        │
     ▼                                        ▼
┌─────────────┐    key exchange        ┌─────────────┐
│ Public key  │◄─────────────────────►│ Public key  │
└─────────────┘                        └─────────────┘
     │                                        │
     ▼                                        ▼
┌─────────────┐                        ┌─────────────┐
│ Shared      │                        │ Shared      │
│ session key │ (both derive same key) │ session key │
└─────────────┘                        └─────────────┘
     │                                        │
     ▼                                        ▼
  Encrypt ──────► ciphertext ──────► Decrypt
```

**Server never sees plaintext**. Only metadata (who, when, room).

---

### Device Verification

**Problem**: How do you know you're talking to the real Bob, not an impersonator?

**Solution**: Device verification - cryptographically confirm device identity.

**Methods**:
1. **Emoji verification**: Both users see same emoji sequence
2. **QR code**: Scan QR code in person
3. **Cross-signing**: Trust one device, it vouches for others

**For Bots**:

Bots have a choice:

| Approach | Security | Complexity | UX |
|----------|----------|------------|-----|
| **Unverified** | Lower | Simple | Users see warning |
| **Verified** | Higher | Complex | Users must verify once |

**Recommendation for Factumerit**: Start unverified. Task data isn't highly sensitive. Add verification later if users request.

**Unverified bot behavior**:
- Bot responds to all DMs
- Users see "This session is not verified" warning
- Messages still encrypted in transit

---

## Deployment

### Option 1: Use matrix.org (MVP)

**Setup**:
1. Create account at https://app.element.io
2. Get access token from settings
3. Bot connects to matrix.org homeserver

**Pros**:
- Zero infrastructure
- Free
- Instant

**Cons**:
- No custom domain (@bot:matrix.org)
- Dependent on matrix.org uptime
- Rate limits possible

**Good for**: MVP, testing

---

### Option 2: Self-host Dendrite

**Setup**:
```yaml
# docker-compose.yml
version: '3'
services:
  dendrite:
    image: matrixdotorg/dendrite-monolith:latest
    volumes:
      - ./config:/etc/dendrite
      - ./data:/var/dendrite
    ports:
      - "8008:8008"   # Client API
      - "8448:8448"   # Federation API
```

**DNS Requirements**:
```
# Option A: .well-known (recommended)
# Host at: https://factumerit.app/.well-known/matrix/server
{"m.server": "matrix.factumerit.app:443"}

# Option B: SRV record
_matrix._tcp.factumerit.app. 3600 IN SRV 10 0 443 matrix.factumerit.app.
```

**TLS**: Required. Use Let's Encrypt.

**Render Deployment**:
```yaml
# render.yaml
services:
  - type: web
    name: dendrite
    env: docker
    plan: starter  # $9/mo
    dockerfilePath: ./Dockerfile.dendrite
    customDomains:
      - matrix.factumerit.app
```

**Pros**:
- Custom domain (@bot:factumerit.app)
- Full control
- No rate limits

**Cons**:
- $9/mo
- Ops burden
- Federation config complexity

**Good for**: Production, custom branding

---

## Clients and SDKs

### Element

**What**: The main Matrix client app (like Slack app).

- Web: https://app.element.io
- Desktop: Electron app
- Mobile: iOS/Android

**Relationship to Matrix**: Element (company) employs most Matrix core developers. Element (app) is the flagship client.

---

### matrix-nio (Python)

**What**: Async Python SDK for Matrix. Our choice for Factumerit.

```python
from nio import AsyncClient, RoomMessageText

client = AsyncClient("https://matrix.org", "@bot:matrix.org")

async def message_callback(room, event):
    print(f"Message: {event.body}")
    await client.room_send(
        room.room_id,
        "m.room.message",
        {"msgtype": "m.text", "body": "Hello!"}
    )

client.add_event_callback(message_callback, RoomMessageText)
await client.login("password")
await client.sync_forever()
```

**Features**:
- Async/await native
- E2EE support
- Well-documented
- Active maintenance

---

### matrix-bot-sdk (TypeScript)

**What**: Official TypeScript SDK for bots.

**Use if**: You prefer TypeScript or have JS codebase.

---

## Glossary

| Term | Meaning |
|------|---------|
| **Homeserver** | Server that hosts Matrix accounts |
| **Federation** | Servers talking to each other |
| **Room** | Where messages happen (like channel) |
| **Space** | Collection of rooms (like workspace) |
| **Event** | Anything in Matrix (message, reaction, etc.) |
| **State event** | Room config (name, members, power levels) |
| **Timeline** | Ordered list of events in a room |
| **DAG** | Directed Acyclic Graph (how events are ordered) |
| **E2EE** | End-to-end encryption |
| **Megolm** | Group encryption protocol |
| **Olm** | 1:1 encryption protocol |
| **Cross-signing** | Device verification via trusted device |
| **Power levels** | Permissions within a room (0-100) |

---

## Factumerit Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| MVP server | matrix.org | Zero deploy, test bot logic |
| Production server | Dendrite | Light, Go, easy on Render |
| SDK | matrix-nio | Python, matches existing codebase |
| E2EE verification | Unverified (initially) | Simplicity, low-sensitivity data |
| Bot identity | @factumerit:matrix.org → @bot:factumerit.app | MVP → Production |

---

## Related

- [21-MATRIX_PLATFORM_RECOMMENDATION.md](21-MATRIX_PLATFORM_RECOMMENDATION.md)
- [25-ARCHITECTURE.md](25-ARCHITECTURE.md)
- [28-MVP_SCOPE.md](28-MVP_SCOPE.md)
