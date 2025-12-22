# 28: MVP Scope

**Date**: 2025-12-22
**Status**: Design

---

## MVP Definition

**Goal**: Feature parity with Slack bot on Matrix platform.

**MVP includes**:
- One-click provisioning (hosted vikunja account)
- BYOV (bring your own vikunja)
- Full task CRUD via 58 MCP tools
- Multi-vikunjae support
- Permanent bot identity (`@bot:factumerit.app`)

**Not MVP** (future):
- Local LLM (Ollama)
- Cloud LLM (BYOK)
- Templates/Interview features

---

## MVP Features

### In Scope (Parity with Slack bot)

| Feature | Description | Priority |
|---------|-------------|----------|
| **Dendrite** | Self-hosted Matrix server | P0 |
| **One-click provisioning** | New user → hosted vikunja in one click | P0 |
| **BYOV** | Connect existing vikunja | P0 |
| **58 MCP tools** | Full task/project/label CRUD | P0 |
| **Multi-vikunjae** | Connect multiple instances | P0 |
| **Permission testing** | `config test` | P0 |
| **Instance switching** | `switch_instance`, `list_instances` | P0 |

### Out of Scope (Future)

| Feature | Phase |
|---------|-------|
| Local LLM (Ollama) | 2 |
| Cloud LLM (BYOK) | 2 |
| Templates | 3 |
| Interview feature | 3 |

---

## Technical Stack (MVP)

| Component | Choice | Reason |
|-----------|--------|--------|
| Codebase | vikunja-slack-bot | Reuse 58 MCP tools, multi-instance |
| Matrix client | matrix-nio | Python, async, E2EE ready |
| Matrix server | Dendrite (self-hosted) | Permanent identity `@bot:factumerit.app` |
| Parser | Regex (MVP) | Simple, no LLM overhead |
| Hosting | Existing + Dendrite | +$9/mo for Dendrite |

**LLM Strategy (TBD - not MVP)**:

| Option | Pros | Cons |
|--------|------|------|
| No LLM (regex) | Simple, fast, $0 | Limited NLU |
| Ollama on Render | Private, no API cost | RAM expensive ($25+/mo) |
| Cloud LLM (BYOK) | Smart, user pays | Privacy, dependency |
| Hybrid | Best of both | Complexity |

Decision deferred. MVP uses regex parser. LLM can be added later.

---

## MVP Architecture

```
┌──────────────────┐
│   Dendrite       │  (NEW Render service $9/mo)
│   matrix.        │
│   factumerit.app │
│                  │
│  Bot account:    │
│  @bot:factumerit │
│  .app            │
└────────┬─────────┘
         │
         ▼
┌───────────────────────────────────────────────────┐
│ vikunja-slack-bot (existing Render service)       │
│                                                    │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  │
│  │ Slack Bot  │  │ Matrix Bot │  │ MCP Server │  │
│  │ (existing) │  │ (NEW)      │  │ (existing) │  │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  │
│        │               │               │          │
│        └───────────────┼───────────────┘          │
│                        ▼                          │
│              ┌─────────────────┐                  │
│              │ vikunja-mcp     │                  │
│              │ (58 tools)      │                  │
│              │ multi-instance  │                  │
│              └─────────────────┘                  │
│                        │                          │
│              ┌─────────▼─────────┐                │
│              │ ~/.vikunja-mcp/   │                │
│              │ config.yaml       │                │
│              │ (instances)       │                │
│              └───────────────────┘                │
└───────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────┐
│            User's Vikunjae                │
│                                           │
│  • vikunja.factumerit.app (personal)     │
│  • app.vikunja.cloud (business)          │
└───────────────────────────────────────────┘
```

---

## User Stories (MVP)

### US1: Connect Vikunja
```
As a user with an existing Vikunja
I want to connect it to the bot
So I can manage tasks via chat

Given I DM the bot
When I say "config add https://vikunja.factumerit.app vkt_abc123"
Then the bot stores my connection
And confirms with task count
```

### US2: List Today's Tasks
```
As a connected user
I want to see what's due today
So I know what to focus on

Given I have tasks due today
When I say "what's due today"
Then the bot shows my tasks with checkboxes
```

### US3: Add Task
```
As a connected user
I want to quickly add a task
So I don't forget it

Given I'm connected
When I say "add buy groceries"
Then the bot creates the task
And confirms it was added
```

### US4: Complete Task
```
As a connected user
I want to mark a task done
So I can track progress

Given I have a task #42
When I say "done 42"
Then the bot marks it complete
And confirms
```

---

## Acceptance Criteria

### Must Have (MVP = Slack parity)
- [ ] Dendrite running at `matrix.factumerit.app`
- [ ] Federation works (matrix.org users can DM bot)
- [ ] Bot responds to DMs as `@bot:factumerit.app`
- [ ] One-click provisioning creates hosted vikunja
- [ ] BYOV connects to user's vikunja
- [ ] All 58 MCP tools accessible via Matrix
- [ ] Multi-vikunjae support (switch_instance, list_instances)
- [ ] Permission testing (`config test`)

### Won't Have (Future)
- Local LLM (Ollama)
- Cloud LLM (BYOK)
- Templates
- Interview feature

---

## File Structure

**Add to existing `~/vikunja-slack-bot/src/vikunja_mcp/`:**

```
vikunja_mcp/
├── __init__.py
├── server.py              # Existing: MCP + Slack (58 tools)
├── matrix_client.py       # NEW: matrix-nio wrapper
├── matrix_handlers.py     # NEW: Message → tool routing
└── matrix_parser.py       # NEW: Regex command parser

# Reuse from existing:
# - Multi-instance config (~/.vikunja-mcp/config.yaml)
# - All 58 Vikunja tools
# - OAuth callback for one-click
```

**Dependencies to add to pyproject.toml:**
```toml
dependencies = [
    # ... existing ...
    "matrix-nio[e2e]>=0.21",
]
```

---

## Implementation Order

### Phase 1: Dendrite
1. **Deploy Dendrite** - New Render service, `matrix.factumerit.app`
2. **Configure federation** - DNS, .well-known, TLS
3. **Create bot account** - `@bot:factumerit.app`
4. **Test federation** - Verify matrix.org users can see the server

### Phase 2: Matrix Bot
5. **Add matrix-nio** - `uv add matrix-nio[e2e]`
6. **Matrix client wrapper** - Connect to Dendrite, receive DMs
7. **Wire to existing tools** - Reuse vikunja-mcp 58 tools
8. **Message handlers** - Route Matrix messages to tools
9. **Test BYOV** - Connect your existing vikunjae

### Phase 3: One-Click Provisioning
10. **Provisioning endpoint** - Adapt existing OAuth callback for Matrix
11. **Onboarding flow** - DM → link → hosted vikunja created
12. **Test end-to-end** - New user gets working vikunja via Matrix

### Phase 4: Deploy & Announce
13. **Deploy to Render** - Push bot update
14. **Test from Element** - Full flow as external user
15. **Announce in Vikunja Matrix room** - Distribution channel

---

## Testing Strategy

### Local Testing
- Use matrix.org account for bot
- Your existing vikunjae for testing

### Test Cases
```python
def test_parse_due_today():
    assert parse("what's due today") == {"intent": "list", "filter": "due_today"}
    assert parse("show tasks due today") == {"intent": "list", "filter": "due_today"}
    assert parse("whats due") == {"intent": "list", "filter": "due_today"}

def test_parse_add():
    assert parse("add buy groceries") == {"intent": "create", "title": "buy groceries"}

def test_parse_done():
    assert parse("done 42") == {"intent": "complete", "id": "42"}
```

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Bot responds to DM | < 2 seconds |
| Config add works | First try |
| List tasks works | Shows correct tasks |
| Add task works | Appears in Vikunja web UI |
| Uptime | 99% (Render SLA) |

---

## Related

- [24-USER_EXPERIENCE_FLOW.md](24-USER_EXPERIENCE_FLOW.md)
- [25-ARCHITECTURE.md](25-ARCHITECTURE.md)
- [27-RENDER_DEPLOYMENT.md](27-RENDER_DEPLOYMENT.md)
