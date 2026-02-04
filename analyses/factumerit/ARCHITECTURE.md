# Factumerit Platform Architecture

**Version**: 1.0
**Last Updated**: 2025-12-24
**Status**: Production Ready

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [System Overview](#2-system-overview)
3. [Component Architecture](#3-component-architecture)
4. [Connection Architecture](#4-connection-architecture)
5. [Data Flows](#5-data-flows)
6. [Security Model](#6-security-model)
7. [Deployment Architecture](#7-deployment-architecture)
8. [Configuration Reference](#8-configuration-reference)
9. [Operational Runbook](#9-operational-runbook)
10. [Architectural Decisions](#10-architectural-decisions)

---

## 1. Executive Summary

Factumerit is an AI-powered task management platform that bridges chat interfaces (Matrix, Slack) to Vikunja task management via natural language processing.

### Core Value Proposition

> "You're not managing tasks. You're declaring outcomes."

Users interact via chat:
- **Declare**: "I need to call the dentist before Thursday"
- **Inquire**: "What's on my plate this week?"
- **Confirm**: "The dentist appointment is done"

### Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Chat | Matrix (Synapse) | Federated messaging |
| Auth | MAS | OIDC/OAuth2 provider |
| Tasks | Vikunja | Task management backend |
| AI | Claude (Anthropic) | Natural language processing |
| Bot | vikunja-slack-bot | Multi-transport bridge |
| Infra | Render | Cloud hosting |
| Data | PostgreSQL | Shared database |

### Monthly Cost

```
factumerit-matrix    $9.00   (Starter + 3GB disk)
vikunja-slack-bot   $11.50   (Starter + 1GB disk)
vikunja             $11.50   (Starter + 10GB disk)
factumerit-db        $9.00   (Basic 256MB PostgreSQL)
─────────────────────────────
Total               $41.00/mo
```

---

## 2. System Overview

### High-Level Architecture

```
                                    EXTERNAL
    ┌─────────────────────────────────────────────────────────────┐
    │                      Internet                                │
    │   Matrix Federation    Slack API    Claude API    Vikunja   │
    │   (matrix.org, etc)                                  API    │
    └─────────────────────────────────────────────────────────────┘
                │                 │            │            │
                │                 │            │            │
    ════════════╪═════════════════╪════════════╪════════════╪═════
                │                 │            │            │
                ▼                 ▼            ▼            ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                    RENDER PLATFORM                           │
    │                                                              │
    │  ┌──────────────────────┐    ┌──────────────────────────┐   │
    │  │  factumerit-matrix   │    │   vikunja-slack-bot      │   │
    │  │  ┌────────────────┐  │    │                          │   │
    │  │  │     nginx      │  │    │  ┌──────────────────┐    │   │
    │  │  │   (port 10000) │  │    │  │   MCP Server     │    │   │
    │  │  └───────┬────────┘  │    │  │   (FastMCP)      │    │   │
    │  │          │           │    │  └────────┬─────────┘    │   │
    │  │    ┌─────┴─────┐     │    │           │              │   │
    │  │    ▼           ▼     │    │  ┌────────┴─────────┐    │   │
    │  │ ┌──────┐  ┌───────┐  │    │  │ Transport Layer  │    │   │
    │  │ │Synapse│  │  MAS  │  │    │  ├──────┬──────────┤    │   │
    │  │ │:8008  │  │ :8080 │  │    │  │Slack │  Matrix  │    │   │
    │  │ └───┬───┘  └───┬───┘  │    │  │bolt  │  nio     │    │   │
    │  │     │          │      │    │  └──────┴──────────┘    │   │
    │  └─────┼──────────┼──────┘    └──────────────────────────┘   │
    │        │          │                       │                  │
    │        └────┬─────┘                       │                  │
    │             │                             │                  │
    │             ▼                             ▼                  │
    │  ┌─────────────────────────────────────────────────────┐    │
    │  │              factumerit-db (PostgreSQL)              │    │
    │  │  ┌─────────┐  ┌─────────┐  ┌─────────────────────┐  │    │
    │  │  │ matrix  │  │   mas   │  │      vikunja        │  │    │
    │  │  └─────────┘  └─────────┘  └─────────────────────┘  │    │
    │  └─────────────────────────────────────────────────────┘    │
    │                                                              │
    └──────────────────────────────────────────────────────────────┘
```

### Service Endpoints

| Service | Public URL | Internal Port |
|---------|------------|---------------|
| Matrix Homeserver | https://matrix.factumerit.app | 8008 |
| MAS (Auth) | https://matrix.factumerit.app/* | 8080 |
| Element Web | https://matrix.factumerit.app/chat/ | static |
| Vikunja | https://vikunja.factumerit.app | 3456 |
| Bot (MCP/Slack) | https://vikunja-slack-bot.onrender.com | $PORT |

---

## 3. Component Architecture

### 3.1 Synapse (Matrix Homeserver)

**Purpose**: Federated messaging, user accounts, room management

**Key Configuration**:
```yaml
# homeserver.template.yaml
server_name: matrix.factumerit.app
experimental_features:
  msc4108_enabled: true      # QR code login
  msc3861:
    enabled: true            # OIDC delegation to MAS
    issuer: http://localhost:8080/
    client_id: 0000000000000000000SYNAPSE
```

**Responsibilities**:
- Matrix federation with other homeservers
- Message storage and sync
- Room state management
- Delegates authentication to MAS

### 3.2 MAS (Matrix Authentication Service)

**Purpose**: OIDC/OAuth2 provider for Matrix and external apps

**Key Configuration**:
```yaml
# mas.template.yaml
clients:
  - client_id: 0000000000000000000SYNAPSE   # Synapse delegation
  - client_id: 0000000000000000000V1KYNJA   # Vikunja OIDC
  - client_id: 000000000000000000ATHNTK00   # Authentik (optional)

experimental:
  oidc_native_authentication:
    enabled: true  # QR code device sign-in
```

**Custom Patch**: MAS is built from source with email claims fix:
- Returns `email` and `email_verified` in userinfo endpoint
- Required for Vikunja auto-email population

### 3.3 Vikunja (Task Manager)

**Purpose**: Task storage, project management, Kanban boards

**Integration Points**:
- OIDC login via MAS ("Login with Factumerit")
- REST API for bot operations
- CalDAV for calendar sync

### 3.4 vikunja-slack-bot (AI Bot)

**Purpose**: Multi-transport bridge between chat and Vikunja

**Architecture**:
```
┌─────────────────────────────────────────────────────────────┐
│                    vikunja-slack-bot                         │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              MCP Server Core (FastMCP)                  │ │
│  │                                                         │ │
│  │  58 Tools: projects, tasks, labels, kanban, calendar   │ │
│  │  Claude AI: Natural language → tool calls              │ │
│  │  User Config: Per-user tokens, preferences             │ │
│  └────────────────────────────────────────────────────────┘ │
│                            │                                 │
│         ┌──────────────────┼──────────────────┐             │
│         ▼                  ▼                  ▼             │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐       │
│  │   Slack     │   │   Matrix    │   │    MCP      │       │
│  │  Transport  │   │  Transport  │   │  Transport  │       │
│  │             │   │             │   │             │       │
│  │ slack-bolt  │   │ matrix-nio  │   │  SSE/HTTP   │       │
│  │ Events API  │   │ sync loop   │   │  OAuth2     │       │
│  └─────────────┘   └─────────────┘   └─────────────┘       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Transport Comparison**:

| Feature | Slack | Matrix | MCP |
|---------|-------|--------|-----|
| Library | slack-bolt | matrix-nio | FastMCP |
| Auth | OAuth + signing | Password/token | OAuth2 + PKCE |
| Commands | @mention, /slash | !commands, @mention | Tool calls |
| Response | Ephemeral/channel | DM (privacy model) | Structured JSON |

### 3.5 nginx (Reverse Proxy)

**Purpose**: TLS termination, request routing, static file serving

**Routing Rules**:
```nginx
# MAS routes
/.well-known/openid-configuration → MAS :8080
/.well-known/webfinger            → MAS :8080
/oauth2/*                         → MAS :8080
/authorize, /token, /login        → MAS :8080
/register, /account, /logout      → MAS :8080

# Static content
/.well-known/matrix/*             → Static files
/chat/*                           → Element Web
/                                 → Homepage

# Synapse routes (everything else)
/_matrix/*                        → Synapse :8008
/*                                → Synapse :8008
```

### 3.6 PostgreSQL (Database)

**Purpose**: Shared data store for all services

**Database Layout**:
```
factumerit-db (Render PostgreSQL)
├── matrix_jfmr    (Synapse: rooms, events, users)
├── mas            (MAS: sessions, tokens, emails)
└── vikunja        (Tasks, projects, labels)
```

**Why Shared**: ADR-020 - Cost optimization ($9/mo vs $27/mo for separate instances)

---

## 4. Connection Architecture

### 4.1 Connection Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CONNECTION MAP                                │
│                                                                      │
│  ┌──────────┐         MSC3861 OIDC           ┌──────────┐           │
│  │  Synapse │◄──────────────────────────────►│   MAS    │           │
│  │  :8008   │   (delegation, token validate)  │  :8080   │           │
│  └────┬─────┘                                 └────┬─────┘           │
│       │                                            │                 │
│       │ PostgreSQL                                 │ PostgreSQL      │
│       │ (matrix db)                                │ (mas db)        │
│       │                                            │                 │
│       ▼                                            ▼                 │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    PostgreSQL :5432                          │    │
│  └─────────────────────────────────────────────────────────────┘    │
│       ▲                                            ▲                 │
│       │                                            │                 │
│       │ SQLite (local)                            │ OIDC Login      │
│       │                                            │                 │
│  ┌────┴─────┐                                 ┌────┴─────┐          │
│  │  Vikunja │◄────────────────────────────────│   MAS    │          │
│  │  :3456   │         OIDC Authentication      │  :8080   │          │
│  └────┬─────┘                                 └──────────┘          │
│       │                                                              │
│       │ REST API (per-user tokens)                                  │
│       │                                                              │
│       ▼                                                              │
│  ┌──────────────────┐                                               │
│  │ vikunja-slack-bot│──────► Claude API (Anthropic)                 │
│  │                  │──────► Slack API (Events, Web)                │
│  │                  │──────► Matrix (Synapse via matrix-nio)        │
│  └──────────────────┘                                               │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### 4.2 Connection Details

| Connection | Protocol | Auth Method | Port |
|------------|----------|-------------|------|
| nginx → Synapse | HTTP | None (internal) | 8008 |
| nginx → MAS | HTTP | None (internal) | 8080 |
| Synapse ↔ MAS | HTTP | Shared secret + client_secret | 8080 |
| Vikunja → MAS | HTTPS | OIDC (client_id + client_secret) | 443 |
| Bot → Vikunja | HTTPS | Bearer token (per-user) | 443 |
| Bot → Synapse | HTTPS | Password/access_token | 443 |
| Bot → Claude | HTTPS | API key | 443 |
| Bot → Slack | HTTPS | Bot token + signing secret | 443 |
| Services → PostgreSQL | PostgreSQL | Connection string | 5432 |

---

## 5. Data Flows

### 5.1 Matrix Login Flow (OIDC Delegation)

```
┌────────┐     ┌────────┐     ┌────────┐     ┌────────┐
│ Element│     │ nginx  │     │  MAS   │     │Synapse │
│  Web   │     │        │     │        │     │        │
└───┬────┘     └───┬────┘     └───┬────┘     └───┬────┘
    │              │              │              │
    │ 1. GET /login│              │              │
    │─────────────►│              │              │
    │              │──────────────►              │
    │              │  2. Forward to MAS          │
    │              │              │              │
    │◄─────────────────────────────              │
    │  3. Login form              │              │
    │                             │              │
    │ 4. POST credentials         │              │
    │────────────────────────────►│              │
    │                             │              │
    │                             │ 5. Validate  │
    │                             │─────────────►│
    │                             │◄─────────────│
    │                             │ 6. User valid│
    │                             │              │
    │◄────────────────────────────│              │
    │ 7. Access token + redirect  │              │
    │                             │              │
    │ 8. Sync with token          │              │
    │────────────────────────────────────────────►
    │◄────────────────────────────────────────────
    │ 9. Messages, rooms, etc     │              │
```

### 5.2 Vikunja OIDC Login Flow

```
┌────────┐     ┌────────┐     ┌────────┐
│Vikunja │     │  MAS   │     │  User  │
│  Web   │     │        │     │Browser │
└───┬────┘     └───┬────┘     └───┬────┘
    │              │              │
    │              │◄─────────────│ 1. Click "Login with Factumerit"
    │              │              │
    │◄─────────────│              │ 2. Redirect to MAS /authorize
    │              │              │
    │              │◄─────────────│ 3. Enter Matrix credentials
    │              │              │
    │              │──────────────►  4. Consent screen
    │              │◄─────────────│ 5. Grant consent
    │              │              │
    │◄─────────────│              │ 6. Redirect with auth code
    │              │              │
    │──────────────►              │ 7. Exchange code for tokens
    │◄─────────────│              │ 8. Access token + ID token
    │              │              │    (includes email claim)
    │              │              │
    │──────────────────────────────► 9. Logged in, email auto-populated
```

### 5.3 Bot Message Flow (Matrix)

```
┌────────┐     ┌────────┐     ┌────────┐     ┌────────┐     ┌────────┐
│  User  │     │Synapse │     │  Bot   │     │ Claude │     │Vikunja │
│        │     │        │     │        │     │   API  │     │  API   │
└───┬────┘     └───┬────┘     └───┬────┘     └───┬────┘     └───┬────┘
    │              │              │              │              │
    │ 1. "what's overdue?"        │              │              │
    │─────────────►│              │              │              │
    │              │──────────────►              │              │
    │              │ 2. Sync event│              │              │
    │              │              │              │              │
    │              │              │──────────────►              │
    │              │              │ 3. Parse intent             │
    │              │              │◄──────────────              │
    │              │              │ 4. Tool: list_all_tasks     │
    │              │              │              │              │
    │              │              │──────────────────────────────►
    │              │              │ 5. GET /api/v1/tasks?filter=overdue
    │              │              │◄──────────────────────────────
    │              │              │ 6. Task list                │
    │              │              │              │              │
    │              │◄─────────────│              │              │
    │              │ 7. Send DM response         │              │
    │◄─────────────│              │              │              │
    │ 8. "You have 3 overdue..."  │              │              │
```

### 5.4 ECO Mode Flow (No LLM)

```
┌────────┐     ┌────────┐     ┌────────┐     ┌────────┐
│  User  │     │Synapse │     │  Bot   │     │Vikunja │
│        │     │        │     │(parser)│     │  API   │
└───┬────┘     └───┬────┘     └───┬────┘     └───┬────┘
    │              │              │              │
    │ 1. "!oops"   │              │              │
    │─────────────►│              │              │
    │              │──────────────►              │
    │              │ 2. Sync event│              │
    │              │              │              │
    │              │              │ 3. RapidFuzz: "oops" → overdue
    │              │              │    (no Claude call)
    │              │              │              │
    │              │              │──────────────►
    │              │              │ 4. GET overdue tasks
    │              │              │◄──────────────
    │              │              │              │
    │◄─────────────────────────────              │
    │ 5. Response (token saved)   │              │
```

---

## 6. Security Model

### 6.1 Security Layers

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SECURITY LAYERS                              │
│                                                                      │
│  Layer 1: Network Security                                          │
│  ├── TLS everywhere (Render terminates at edge)                     │
│  ├── Private network between Render services                        │
│  └── No direct database access from internet                        │
│                                                                      │
│  Layer 2: Authentication                                            │
│  ├── Matrix identity via MAS (OIDC)                                 │
│  ├── Vikunja OIDC via MAS                                           │
│  ├── Bot password/token for Matrix login                            │
│  └── Per-user Vikunja API tokens                                    │
│                                                                      │
│  Layer 3: Authorization                                             │
│  ├── Admin commands: ADMIN_IDS env var (ACL)                        │
│  ├── Vikunja token scope limits operations                          │
│  └── MAS policy engine (OPA/WASM)                                   │
│                                                                      │
│  Layer 4: Data Protection                                           │
│  ├── E2EE disabled for V1 (bot cannot read encrypted rooms)         │
│  ├── Secrets in Render env vars (not git)                           │
│  └── User tokens in config file (plaintext, 600 perms)              │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 6.2 Authentication Details

| Component | Auth Method | Credential Storage |
|-----------|-------------|-------------------|
| Matrix users | Password via MAS | MAS database (hashed) |
| Vikunja users | OIDC via MAS | Session cookies |
| Bot → Matrix | Password or access_token | Render env var |
| Bot → Vikunja | Per-user API tokens | YAML config file |
| Bot → Claude | API key | Render env var |
| Bot → Slack | Bot token + signing secret | Render env vars |

### 6.3 Admin Protection

**Unified Admin IDs**:
```bash
ADMIN_IDS=U12345ABC,@i2:matrix.factumerit.app
```

**Admin-Only Commands**:
- `admin_set_user_token` - Set Vikunja token for another user
- `admin_list_users` - List all configured users
- `admin_connect_instance` - Connect new Vikunja instance
- `/credits` (Matrix) - Manage user credits

**Implementation**:
```python
def _is_admin(user_id: str) -> bool:
    admin_ids = set(os.environ.get("ADMIN_IDS", "").split(","))
    return user_id in admin_ids
```

### 6.4 E2EE Status

**Decision**: E2EE disabled for V1

**Implementation**: Hardcoded in `matrix_client.py:58`:
```python
config = AsyncClientConfig(encryption_enabled=False)
```

**Rationale**:
- Bot cannot read encrypted rooms without device verification
- Device verification requires manual user action (UX friction)
- Task data is not highly sensitive
- We control the homeserver (trusted infrastructure)

**Risk**: If E2EE accidentally enabled, bot silently fails to respond.

### 6.5 Secrets Management

| Secret | Location | Purpose |
|--------|----------|---------|
| `MATRIX_PASSWORD` | Render env var | Bot Matrix login |
| `ANTHROPIC_API_KEY` | Render env var | Claude API |
| `SLACK_BOT_TOKEN` | Render env var | Slack integration |
| `VIKUNJA_TOKEN` | Render env var | Fallback API token |
| `MAS_*` secrets | Render env var | MAS configuration |
| User tokens | `/data/config/config.yaml` | Per-user Vikunja tokens |

**Never Committed**:
- `.env` files (gitignored)
- API keys, passwords, tokens
- Database connection strings

---

## 7. Deployment Architecture

### 7.1 Render Services

```yaml
# factumerit-matrix (render.yaml)
services:
  - type: web
    name: factumerit-matrix
    runtime: docker
    plan: starter              # $7/mo
    region: oregon
    healthCheckPath: /health
    disk:
      sizeGB: 3                # Media, keys, Element Web
      mountPath: /data

# vikunja-slack-bot (render.yaml)
services:
  - type: web
    name: vikunja-slack-bot
    runtime: python
    plan: starter              # $7/mo
    startCommand: vikunja-mcp --transport sse --port $PORT --matrix
    disk:
      sizeGB: 1                # User configs
      mountPath: /data

# Shared database
databases:
  - name: factumerit-db
    plan: basic-256mb          # $9/mo
```

### 7.2 Container Architecture (factumerit-matrix)

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Docker Container (Render)                         │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │                    supervisord (PID 1)                           ││
│  │                                                                  ││
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          ││
│  │  │    nginx     │  │   synapse    │  │     mas      │          ││
│  │  │  (priority   │  │  (priority   │  │  (priority   │          ││
│  │  │    100)      │  │    200)      │  │    200)      │          ││
│  │  └──────────────┘  └──────────────┘  └──────────────┘          ││
│  │                                                                  ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │                    Persistent Storage (/data)                    ││
│  │                                                                  ││
│  │  /data/synapse/           /data/mas/                            ││
│  │  ├── homeserver.yaml      ├── signing_key.pem                   ││
│  │  ├── signing.key          └── encryption_secret                 ││
│  │  └── media_store/                                               ││
│  │                                                                  ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │                    Static Files (/var/www)                       ││
│  │                                                                  ││
│  │  /var/www/element/        /var/www/static/                      ││
│  │  └── Element Web app      ├── index.html                        ││
│  │                           └── .well-known/matrix/*              ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### 7.3 Build Process

**Dockerfile (3-stage build)**:
1. **Stage 1**: Extract OPA policy from official MAS image
2. **Stage 2**: Build patched MAS from Rust source (~15 min)
3. **Stage 3**: Combine Synapse base + MAS binary + nginx + Element Web

**Build time**: 15-20 min (first), 5-7 min (cached)

### 7.4 Startup Sequence

```bash
# start.sh execution order
1. Generate Synapse signing key (if not exists)
2. Generate MAS signing key (if not exists)
3. Generate MAS encryption secret (if not exists)
4. Parse DATABASE_URL, create 'mas' database if needed
5. Run envsubst on template configs
6. Start supervisord (nginx → synapse + mas)
```

### 7.5 DNS Configuration

```
matrix.factumerit.app    A     <Render IP>
vikunja.factumerit.app   A     <Render IP>
```

**TLS**: Managed by Render (automatic Let's Encrypt)

---

## 8. Configuration Reference

### 8.1 Environment Variables

#### factumerit-matrix

| Variable | Required | Description |
|----------|----------|-------------|
| `DENDRITE_DOMAIN` | Yes | Matrix server hostname |
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `REGISTRATION_SECRET` | Yes | Synapse registration token |
| `MAS_HOMESERVER_SECRET` | Yes | Synapse ↔ MAS shared secret |
| `MAS_SYNAPSE_CLIENT_SECRET` | Yes | OAuth client secret |
| `VIKUNJA_OIDC_SECRET` | Yes | Vikunja OAuth client secret |
| `RESEND_API_KEY` | Yes | Email provider API key |

#### vikunja-slack-bot

| Variable | Required | Description |
|----------|----------|-------------|
| `SLACK_BOT_TOKEN` | Yes | Slack bot OAuth token |
| `SLACK_SIGNING_SECRET` | Yes | Slack signature verification |
| `ANTHROPIC_API_KEY` | Yes | Claude API key |
| `MATRIX_HOMESERVER` | Yes | Matrix homeserver URL |
| `MATRIX_USER` | Yes | Bot Matrix user ID |
| `MATRIX_PASSWORD` | Yes | Bot Matrix password |
| `VIKUNJA_URL` | Yes | Default Vikunja instance |
| `VIKUNJA_TOKEN` | No | Fallback API token |
| `ADMIN_IDS` | Yes | Comma-separated admin IDs |

### 8.2 Config File Structure

**Bot user config** (`/data/config/config.yaml`):
```yaml
users:
  "@i2:matrix.factumerit.app":
    vikunja_token: "tk_xxx"
    welcomed: true
    model: "haiku"
    timezone_override: "America/New_York"

  "U12345ABC":  # Slack user
    vikunja_token: "tk_yyy"
    show_token_usage: true

instances:
  default:
    url: "https://vikunja.factumerit.app"
    token: "tk_admin"
```

---

## 9. Operational Runbook

### 9.1 Health Checks

| Service | Endpoint | Expected |
|---------|----------|----------|
| Matrix | `/health` | 200 OK |
| MAS | `/.well-known/openid-configuration` | JSON |
| Vikunja | `/api/v1/info` | JSON with version |
| Bot | `/health` | 200 OK |

### 9.2 Common Issues

**"No Such Resource" on login**:
- nginx not routing to MAS
- Check: `/.well-known/openid-configuration` returns JSON

**Bot not responding**:
- Check E2EE status (must be disabled)
- Verify MATRIX_PASSWORD is correct
- Check bot sync loop in logs

**Vikunja OIDC fails**:
- Verify client_id and client_secret match MAS config
- Check redirect_uri exact match
- Verify MAS returns email claims

### 9.3 Log Locations

| Service | Log Method |
|---------|------------|
| Synapse | stdout (Render dashboard) |
| MAS | stdout (Render dashboard) |
| nginx | stdout (access + error) |
| Bot | stdout (structured JSON) |

### 9.4 Backup Strategy

| Data | Method | Frequency |
|------|--------|-----------|
| PostgreSQL | Render managed backups | Daily |
| Bot config | Git (no secrets) | On change |
| User tokens | Not backed up (regenerate) | N/A |
| Media files | /data disk (Render) | Included in disk |

---

## 10. Architectural Decisions

### ADR-020: Shared PostgreSQL

**Decision**: Single PostgreSQL instance, separate databases per service

**Rationale**: Cost ($9/mo vs $27/mo for 3 instances)

**Trade-off**: Single point of failure, but acceptable for MVP

### ADR-021: Synapse over Dendrite

**Decision**: Use Synapse (not Dendrite) as Matrix homeserver

**Rationale**: MAS only supports Synapse (requires `/_synapse/mas/*` endpoints)

**Trade-off**: Higher RAM (500MB vs 100MB), but enables OIDC delegation

### ADR-024: Patch MAS for Email Claims

**Decision**: Build MAS from source with email claims fix

**Rationale**: Upstream bug - userinfo endpoint doesn't return email

**Trade-off**: 15-min build time, but saves $25/mo (no Authentik needed)

### E2EE Disabled (V1)

**Decision**: Hardcode `encryption_enabled=False` in bot

**Rationale**: Bot cannot read encrypted rooms without device verification

**Trade-off**: No E2E encryption, but acceptable for task data

---

## Appendix: Quick Reference

### Service URLs

| Service | URL |
|---------|-----|
| Matrix | https://matrix.factumerit.app |
| Element Web | https://matrix.factumerit.app/chat/ |
| Vikunja | https://vikunja.factumerit.app |
| Bot user | @eis:matrix.factumerit.app |

### Bot Commands (Matrix)

| Command | Action |
|---------|--------|
| `!oops` | List overdue tasks (ECO mode) |
| `!now` | List tasks due today |
| `!vik <token>` | Connect Vikunja account |
| Natural language | Parsed by Claude |

### Key Files

| File | Purpose |
|------|---------|
| `factumerit-matrix/Dockerfile` | 3-stage container build |
| `factumerit-matrix/nginx.conf` | Request routing |
| `factumerit-matrix/start.sh` | Startup script |
| `vikunja-slack-bot/src/vikunja_mcp/server.py` | Bot core (8k lines) |
| `vikunja-slack-bot/src/vikunja_mcp/matrix_client.py` | Matrix transport |
