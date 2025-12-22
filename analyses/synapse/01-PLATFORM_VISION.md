# 01: Matrix as Multi-Project Platform

**Date**: 2025-12-22
**Status**: Exploration
**Updated**: Pivoted from Dendrite to Synapse (ADR-021)

---

## Vision

One self-hosted Synapse instance (`matrix.factumerit.app`) becomes a unified conversational gateway to multiple projects and capabilities.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    matrix.factumerit.app                             │
│                    (self-hosted Synapse + MAS)                       │
│                                                                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │
│  │ @tasks:     │ │ @research:  │ │ @qrcards:   │ │ @intel:     │   │
│  │ factumerit  │ │ factumerit  │ │ factumerit  │ │ factumerit  │   │
│  │ .app        │ │ .app        │ │ .app        │ │ .app        │   │
│  │             │ │             │ │             │ │             │   │
│  │ Vikunja     │ │ spawn-      │ │ QR Cards    │ │ Intelligence│   │
│  │ task mgmt   │ │ solutions   │ │ generator   │ │ portal      │   │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘   │
│                                                                      │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                    │
│  │ @analysis:  │ │ @bizdb:     │ │ @assistant: │                    │
│  │ factumerit  │ │ factumerit  │ │ factumerit  │                    │
│  │ .app        │ │ .app        │ │ .app        │                    │
│  │             │ │             │ │             │                    │
│  │ spawn-      │ │ business    │ │ general     │                    │
│  │ analysis    │ │ database    │ │ LLM         │                    │
│  └─────────────┘ └─────────────┘ └─────────────┘                    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
                              │
                    Federation│
                              ▼
              ┌───────────────────────────┐
              │  Any Matrix user can DM   │
              │  any bot from any server  │
              │                           │
              │  @user:matrix.org         │
              │  @user:element.io         │
              │  @user:company.com        │
              └───────────────────────────┘
```

---

## Project Candidates

| Bot Identity | Project | Capability | Status |
|--------------|---------|------------|--------|
| `@tasks:factumerit.app` | vikunja-mcp | Task management (58 MCP tools) | MVP in progress |
| `@research:factumerit.app` | spawn-solutions | Query research library, find prior art | Future |
| `@analysis:factumerit.app` | spawn-analysis | Business analysis, market research | Future |
| `@qrcards:factumerit.app` | qrcards | Generate QR cards, manage templates | Future |
| `@intel:factumerit.app` | intelligence portal | News aggregation, trend analysis | Future |
| `@bizdb:factumerit.app` | business-database | Company/contact lookup, CRM | Future |
| `@assistant:factumerit.app` | General LLM | Catch-all assistant, routing | Future |

---

## Architecture Options

### Option A: One Bot, Multiple Capabilities

Single bot (`@assistant:factumerit.app`) routes to all backends based on intent.

```
User: "add task buy groceries"     → vikunja-mcp
User: "what research do we have on fuzzy search" → spawn-solutions
User: "generate QR for https://..." → qrcards
```

**Pros**: Simple UX, one contact point
**Cons**: Complex routing, context confusion

### Option B: Multiple Specialized Bots

Each project gets its own bot identity.

```
DM @tasks:factumerit.app   → task operations
DM @research:factumerit.app → research queries
DM @qrcards:factumerit.app  → QR generation
```

**Pros**: Clear separation, focused context
**Cons**: Users must know which bot to use

### Option C: Hybrid

- `@assistant:` as entry point, can hand off to specialists
- Direct DM to specialists for power users
- Specialists can summon each other in threads

**Pros**: Best of both worlds
**Cons**: Most complex to build

---

## Shared Infrastructure

All bots share:

| Component | Description |
|-----------|-------------|
| Synapse + MAS | Matrix homeserver + OIDC auth |
| Authentication | Matrix identity = access control |
| E2EE | End-to-end encryption for all DMs |
| Federation | Reachable from any Matrix server |
| Audit logging | Centralized activity logs |
| Rate limiting | Per-user, per-bot limits |

---

## Cost Model

| Component | Cost | Supports |
|-----------|------|----------|
| Synapse + MAS | $7-25/mo | Unlimited bots, users, rooms (RAM dependent) |
| Bot services | $7/mo each | One service per bot (or combined) |
| PostgreSQL | $7/mo | Shared database |

**Minimum viable**: $21/mo (Synapse Starter + 1 combined bot service + PostgreSQL)
**If RAM upgrade needed**: +$18/mo for Standard plan

---

## Implementation Strategy

### Phase 1: Foundation (current)
- Deploy Synapse + MAS
- Launch `@tasks:factumerit.app` (Vikunja MVP)
- Enable "Login with Matrix" for Vikunja
- Prove the model works

### Phase 2: Research Access
- Add `@research:factumerit.app`
- Query spawn-solutions research library
- "What do we know about X?"
- Find prior art before starting new research

### Phase 3: Analysis & Intelligence
- Add `@analysis:factumerit.app`
- Add `@intel:factumerit.app`
- Business analysis on demand

### Phase 4: Unified Assistant
- Add `@assistant:factumerit.app`
- Intent routing to specialists
- Cross-project queries

---

## Questions to Explore

1. **Authentication**: How do bots authenticate users across projects?
   - Matrix identity sufficient?
   - Need per-project permissions?

2. **Data sharing**: Can bots share context?
   - "Create task from this research finding"
   - "Add this company to CRM and create follow-up task"

3. **Rooms vs DMs**:
   - Should there be project rooms? (`#research:factumerit.app`)
   - Or just DM-based interaction?

4. **Public vs Private**:
   - Which bots are public (anyone can DM)?
   - Which require invitation/authorization?

---

## Related

- [02-SYNAPSE_CAPABILITIES.md](./02-SYNAPSE_CAPABILITIES.md) - Capabilities unlocked by Synapse
- [analyses/factumerit/](../factumerit/) - Vikunja/task management analysis
- ADR-019: Matrix Platform Pivot
- ADR-021: Synapse over Dendrite
- `solutions-b847`: Deploy Matrix on Render
