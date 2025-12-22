# 27: Render Deployment Plan

**Date**: 2025-12-22
**Status**: Design

---

## Current Render Services

| Service | Type | Cost | Purpose |
|---------|------|------|---------|
| vikunja.factumerit.app | Web Service | $9/mo | Hosted Vikunja |
| Slack bot + MCP | Web Service | $9/mo | vikunja-mcp (58 tools), Slack bot |

**Total current**: $18/mo

**Key assets**:
- `~/vikunja-slack-bot/` - vikunja-mcp (58 tools), multi-instance, Slack bot
- `~/vikunja-factumerit/` - Vikunja deployment with one-click connect page

---

## Target Architecture on Render

**Production architecture** (permanent bot identity from day one):

```
┌──────────────────────────────────────────────────────────────────┐
│                      RENDER DASHBOARD                             │
│                                                                   │
│  ┌──────────────────┐                                            │
│  │ Dendrite         │  (NEW $9/mo)                               │
│  │ matrix.factumerit│                                            │
│  │ .app             │                                            │
│  │                  │                                            │
│  │ Bot account:     │                                            │
│  │ @bot:factumerit  │                                            │
│  │ .app             │                                            │
│  └────────┬─────────┘                                            │
│           │                                                       │
│           ▼                                                       │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ vikunja-mcp (existing $9/mo)                                │ │
│  │                                                              │ │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐            │ │
│  │  │ Slack Bot  │  │ Matrix Bot │  │ MCP Server │            │ │
│  │  │ (existing) │  │ (NEW)      │  │ (existing) │            │ │
│  │  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘            │ │
│  │        │               │               │                    │ │
│  │        └───────────────┼───────────────┘                    │ │
│  │                        ▼                                    │ │
│  │              ┌─────────────────┐                            │ │
│  │              │ vikunja-mcp     │                            │ │
│  │              │ (58 tools)      │                            │ │
│  │              │ multi-instance  │                            │ │
│  │              └─────────────────┘                            │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌─────────────────────┐                                         │
│  │ vikunja.factumerit  │  (existing $9/mo)                       │
│  │ .app                │                                         │
│  └─────────────────────┘                                         │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘

Total: $27/mo (+$9 for Dendrite)
```

**Why Dendrite from day one**:
- Permanent bot identity: `@bot:factumerit.app`
- No migration later (users don't have to re-add bot)
- Custom domain for branding
- Built to last

---

## Service Configurations

### 1. factumerit-dendrite

**Type**: Web Service
**Runtime**: Docker
**Cost**: $9/mo (Starter)

**Dockerfile**:
```dockerfile
FROM matrixdotorg/dendrite-monolith:latest

COPY dendrite.yaml /etc/dendrite/dendrite.yaml

EXPOSE 8008 8448

CMD ["--config", "/etc/dendrite/dendrite.yaml"]
```

**Environment Variables**:
```
DENDRITE_DOMAIN=matrix.factumerit.app
```

**dendrite.yaml** (key parts):
```yaml
global:
  server_name: matrix.factumerit.app
  private_key: /data/matrix_key.pem
  database:
    connection_string: ${DATABASE_URL}

federation_api:
  external_api:
    listen: http://0.0.0.0:8448

client_api:
  external_api:
    listen: http://0.0.0.0:8008
```

**Custom Domain**: `matrix.factumerit.app`

**Health Check**: `GET /health`

### 2. factumerit-bot

**Type**: Background Worker (no public port)
**Runtime**: Docker
**Cost**: $9/mo (Starter) - may need upgrade for Ollama

**Dockerfile**:
```dockerfile
FROM python:3.11-slim

# Install Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Pull model at build time
RUN ollama pull mistral

CMD ["python", "-m", "factumerit.bot"]
```

**Requirements**:
```
matrix-nio[e2e]>=0.21
httpx>=0.25
asyncpg>=0.29
cryptography>=41
pydantic>=2
```

**Environment Variables**:
```
DATABASE_URL=<from Render PostgreSQL>
MATRIX_HOMESERVER=https://matrix.factumerit.app
MATRIX_USER_ID=@bot:matrix.factumerit.app
MATRIX_PASSWORD=<secret>
FACTUMERIT_ENCRYPTION_KEY=<secret>
OLLAMA_HOST=http://localhost:11434
```

**Resource Considerations**:
- Mistral 7B needs ~4GB RAM
- May need to upgrade from Starter ($9) to Standard ($25) or Pro ($85)
- Alternative: Use smaller model (Phi-3 mini, ~2GB)

### 3. PostgreSQL

**Type**: PostgreSQL
**Plan**: Free (90-day) → Starter ($9/mo)

**Connection**: Auto-injected as `DATABASE_URL`

**Initial Schema**: See [25-ARCHITECTURE.md](25-ARCHITECTURE.md)

---

## MVP Deployment (No Ollama)

For faster MVP, skip local LLM initially:

```
┌─────────────────────┐  ┌─────────────────────┐
│ factumerit-dendrite │  │ factumerit-bot      │
│ Web Service $9      │  │ Background Worker $9│
│                     │  │                     │
│                     │  │ Simple regex parser │
│                     │  │ (no LLM)            │
└─────────┬───────────┘  └──────────┬──────────┘
          │                         │
          └────────────┬────────────┘
                       ▼
          ┌─────────────────────────┐
          │ PostgreSQL (free)       │
          └─────────────────────────┘

Total: $18/mo + existing Vikunja ($9) = $27/mo
```

**MVP Parser** (no LLM):
```python
import re

PATTERNS = [
    (r"^(what'?s|show|list).*due.*today", {"intent": "list", "filter": "due_today"}),
    (r"^(what'?s|show|list).*overdue", {"intent": "list", "filter": "overdue"}),
    (r"^(what'?s|show|list).*(task|todo)", {"intent": "list", "filter": "all"}),
    (r"^add\s+(.+)", {"intent": "create", "title": 1}),
    (r"^done\s+(\d+)", {"intent": "complete", "id": 1}),
    (r"^config\s+add", {"intent": "config_add"}),
    (r"^config\s+test", {"intent": "config_test"}),
    (r"^config\s+list", {"intent": "config_list"}),
]

def parse_message(text: str) -> dict | None:
    text = text.lower().strip()
    for pattern, action in PATTERNS:
        if match := re.match(pattern, text):
            result = action.copy()
            for k, v in result.items():
                if isinstance(v, int):
                    result[k] = match.group(v)
            return result
    return None
```

---

## Deployment Steps

### Phase 1: Dendrite + Bot

1. **Deploy Dendrite** as Web Service on Render
   - Configure DNS for `matrix.factumerit.app`
   - Set up federation (.well-known or SRV)
   - Create bot account `@bot:factumerit.app`
2. **Add matrix-nio** to vikunja-slack-bot
   - Connect to Dendrite
   - Implement message handlers
   - Wire to existing vikunja-mcp tools
3. **Test BYOV flow** with your vikunjae
4. **Test federation** from Element (matrix.org users can DM bot)

### Phase 2: Local LLM (Future)

1. **Upgrade bot service** to handle Ollama memory
2. **Add Ollama** to Dockerfile
3. **Implement LLM routing**
4. **Test natural language parsing**

### Phase 3: One-Click Provisioning (Future)

1. **Add provisioning endpoints** to bot
2. **Configure Vikunja admin API** access
3. **Test one-click flow**
4. **Announce in Vikunja Matrix room**

---

## Cost Projection

| Phase | Services | Monthly Cost |
|-------|----------|--------------|
| Current | Vikunja + Slack/MCP | **$18** |
| + Dendrite | Matrix homeserver | **$27** (+$9) |
| + Ollama (future) | RAM upgrade for LLM | **$36+** (TBD) |

**Breakdown**:
- Vikunja: $9/mo (existing)
- Slack/MCP + Matrix bot: $9/mo (existing, add matrix-nio)
- Dendrite: $9/mo (new)

**Total at launch**: $27/mo

---

## Render Blueprint (render.yaml)

```yaml
services:
  - type: worker
    name: factumerit-bot
    env: docker
    plan: starter
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: factumerit-db
          property: connectionString
      - key: MATRIX_HOMESERVER
        value: https://matrix.org  # Phase 1
      - key: MATRIX_USER_ID
        sync: false
      - key: MATRIX_PASSWORD
        sync: false
      - key: FACTUMERIT_ENCRYPTION_KEY
        sync: false

  # Phase 2: Uncomment for own Dendrite
  # - type: web
  #   name: factumerit-dendrite
  #   env: docker
  #   plan: starter
  #   customDomains:
  #     - matrix.factumerit.app

databases:
  - name: factumerit-db
    plan: free  # 90-day, then starter
```

---

## Related

- [25-ARCHITECTURE.md](25-ARCHITECTURE.md)
- [26-SECURITY.md](26-SECURITY.md)
- [28-MVP_SCOPE.md](28-MVP_SCOPE.md)
