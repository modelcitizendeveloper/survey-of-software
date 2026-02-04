# 25: Factumerit Architecture

**Date**: 2025-12-22
**Status**: Design

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                           MATRIX FEDERATION                          │
│                                                                       │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐        │
│   │ matrix.org   │     │ element.io   │     │ other servers│        │
│   │   users      │     │   users      │     │   users      │        │
│   └──────┬───────┘     └──────┬───────┘     └──────┬───────┘        │
│          │                    │                    │                 │
│          └────────────────────┼────────────────────┘                 │
│                               │                                      │
│                               ▼                                      │
│                    ┌─────────────────────┐                          │
│                    │  Dendrite Server    │                          │
│                    │  matrix.factumerit  │                          │
│                    │     .app            │                          │
│                    └──────────┬──────────┘                          │
│                               │                                      │
└───────────────────────────────┼──────────────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────────────┐
│                         RENDER INFRASTRUCTURE                          │
│                                                                        │
│  ┌────────────────────────────────────────────────────────────────┐   │
│  │                     Factumerit Bot Service                      │   │
│  │                                                                 │   │
│  │  ┌─────────────┐   ┌─────────────┐   ┌─────────────────────┐  │   │
│  │  │ Matrix      │   │ Message     │   │ Vikunja             │  │   │
│  │  │ Client      │──▶│ Router      │──▶│ Adapter             │  │   │
│  │  │ (nio)       │   │             │   │                     │  │   │
│  │  └─────────────┘   └──────┬──────┘   └──────────┬──────────┘  │   │
│  │                           │                      │             │   │
│  │                           ▼                      │             │   │
│  │                    ┌─────────────┐               │             │   │
│  │                    │ Local LLM   │               │             │   │
│  │                    │ (Ollama)    │               │             │   │
│  │                    └──────┬──────┘               │             │   │
│  │                           │                      │             │   │
│  │                           ▼                      │             │   │
│  │                    ┌─────────────┐               │             │   │
│  │                    │ Cloud LLM   │               │             │   │
│  │                    │ (optional)  │               │             │   │
│  │                    └─────────────┘               │             │   │
│  │                                                  │             │   │
│  └──────────────────────────────────────────────────┼─────────────┘   │
│                                                     │                  │
│  ┌─────────────────┐         ┌─────────────────────┼───────────────┐  │
│  │   PostgreSQL    │◀────────│     User Config DB   │               │  │
│  │                 │         │   - matrix_id        │               │  │
│  │  - bot state    │         │   - vikunjae[]       │               │  │
│  │  - user config  │         │   - llm_keys         │               │  │
│  │  - nonces       │         │   - preferences      │               │  │
│  └─────────────────┘         └─────────────────────┬───────────────┘  │
│                                                     │                  │
│  ┌─────────────────┐                               │                  │
│  │ Provisioning    │                               │                  │
│  │ Web Service     │                               │                  │
│  │ (FastAPI)       │                               │                  │
│  └────────┬────────┘                               │                  │
│           │                                        │                  │
└───────────┼────────────────────────────────────────┼──────────────────┘
            │                                        │
            ▼                                        ▼
┌─────────────────────┐              ┌─────────────────────────────────┐
│ Hosted Vikunja      │              │      User's Vikunjae            │
│ vikunja.factumerit  │              │                                 │
│ .app                │              │  • vikunja.factumerit.app       │
│                     │              │  • app.vikunja.cloud            │
│ (for one-click      │              │  • self-hosted instances        │
│  provisioning)      │              │                                 │
└─────────────────────┘              └─────────────────────────────────┘
```

---

## Components

### 1. Dendrite (Matrix Homeserver)

**Purpose**: Hosts the bot's Matrix identity, federates with other servers

**Details**:
- Lightweight Go-based Matrix server
- Bot account: `@bot:matrix.factumerit.app`
- Handles federation with matrix.org, element.io, etc.
- Users DM the bot from any Matrix server

**Resources**:
- RAM: ~256MB
- Storage: Minimal (bot doesn't store messages long-term)
- Domain: `matrix.factumerit.app`

### 2. Factumerit Bot Service

**Purpose**: Core bot logic - message handling, LLM routing, Vikunja integration

**Components**:

| Component | Role |
|-----------|------|
| Matrix Client (nio) | Connect to Dendrite, receive/send messages |
| Message Router | Parse intent, route to handler |
| Local LLM (Ollama) | Parse natural language → API calls |
| Cloud LLM (optional) | Deep analysis, planning (BYOK) |
| Vikunja Adapter | Translate actions to Vikunja API calls |
| User Config | Load/store per-user vikunjae and preferences |

**Resources**:
- RAM: ~512MB (bot) + ~4GB (Ollama with Mistral 7B)
- CPU: Moderate (LLM inference)

### 3. PostgreSQL

**Purpose**: Persistent storage for bot state and user configuration

**Tables**:
```sql
-- User configuration
CREATE TABLE users (
    matrix_id TEXT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Vikunja connections
CREATE TABLE vikunjae (
    id SERIAL PRIMARY KEY,
    matrix_id TEXT REFERENCES users(matrix_id),
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    token TEXT NOT NULL,  -- encrypted
    is_hosted BOOLEAN DEFAULT FALSE,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(matrix_id, name)
);

-- LLM API keys (BYOK)
CREATE TABLE llm_keys (
    matrix_id TEXT PRIMARY KEY REFERENCES users(matrix_id),
    provider TEXT,  -- 'claude', 'openai'
    api_key TEXT,   -- encrypted
    updated_at TIMESTAMP DEFAULT NOW()
);

-- One-time provisioning nonces
CREATE TABLE nonces (
    matrix_id TEXT NOT NULL,
    nonce TEXT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    PRIMARY KEY(matrix_id, nonce)
);
```

### 4. Provisioning Web Service

**Purpose**: One-click account creation for new users

**Endpoints**:
```
GET  /setup?mid=...&nonce=...   One-click provisioning
GET  /health                     Health check
```

**Flow**:
1. Validate nonce
2. Create Vikunja user on hosted instance
3. Generate API token
4. Store vikunja connection for matrix_id
5. Redirect to success page

### 5. Hosted Vikunja (Optional - Phase 2)

**Purpose**: Vikunja instance for one-click provisioning

**Details**:
- Existing: `vikunja.factumerit.app`
- Admin API access for user/token creation
- Default projects created per user

---

## Data Flow

### BYOV Flow (Side Door)

```
User (any Matrix server)
    │
    │ DM: "config add https://my.vikunja.io vkt_abc"
    ▼
Dendrite (federation)
    │
    ▼
Bot receives message
    │
    ├─▶ Parse: config command
    │
    ├─▶ Validate: ping Vikunja API
    │
    ├─▶ Store: vikunjae table
    │
    └─▶ Reply: "✓ Connected, found X tasks"
```

### Task Query Flow

```
User: "what's due today"
    │
    ▼
Bot receives message
    │
    ├─▶ Load user config (vikunjae, default)
    │
    ├─▶ Local LLM: parse intent
    │   └─▶ {"intent": "list", "filter": "due_today"}
    │
    ├─▶ Vikunja Adapter: GET /api/v1/tasks?filter=...
    │
    ├─▶ Format response
    │
    └─▶ Reply: "📋 Due Today: ..."
```

### Cloud LLM Flow (BYOK)

```
User: "analyze my productivity this week"
    │
    ▼
Bot receives message
    │
    ├─▶ Detect: complex query (trigger word: "analyze")
    │
    ├─▶ Check: user has LLM key?
    │   │
    │   ├─▶ No: "For analysis, add API key: config claude sk-..."
    │   │
    │   └─▶ Yes: continue
    │
    ├─▶ Fetch: all tasks from user's vikunjae
    │
    ├─▶ Cloud LLM: analyze with context
    │
    └─▶ Reply: "Looking at your week..."
```

---

## Security Considerations

See [26-SECURITY.md](26-SECURITY.md)

---

## Related

- [21-MATRIX_PLATFORM_RECOMMENDATION.md](21-MATRIX_PLATFORM_RECOMMENDATION.md)
- [24-USER_EXPERIENCE_FLOW.md](24-USER_EXPERIENCE_FLOW.md)
- [26-SECURITY.md](26-SECURITY.md)
- [27-RENDER_DEPLOYMENT.md](27-RENDER_DEPLOYMENT.md)
