# 28: MVP Scope

**Date**: 2025-12-22
**Status**: Design

---

## MVP Definition

**Goal**: Bot responds to DMs, connects to user's Vikunja, does basic task CRUD.

**Not Goal**: One-click provisioning, LLM parsing, multi-vikunjae, cloud LLM.

---

## MVP Features

### In Scope

| Feature | Commands | Priority |
|---------|----------|----------|
| **Connect vikunja** | `config add [url] [token]` | P0 |
| **List tasks** | `what's due today`, `show tasks` | P0 |
| **Add task** | `add [title]` | P0 |
| **Complete task** | `done [id]` | P0 |
| **Test permissions** | `config test` | P1 |
| **Show config** | `config list` | P1 |
| **Remove vikunja** | `config remove` | P1 |
| **Help** | `help` | P1 |

### Out of Scope (Later Phases)

| Feature | Phase |
|---------|-------|
| One-click provisioning | 2 |
| Own Dendrite | 2 |
| Local LLM (Ollama) | 3 |
| Multi-vikunjae | 3 |
| Cloud LLM (BYOK) | 3 |
| Templates/Interview | 4 |

---

## Technical Stack (MVP)

| Component | Choice | Reason |
|-----------|--------|--------|
| Matrix client | matrix-nio | Python, async, E2EE ready |
| Matrix server | matrix.org | Free, no deploy needed |
| Parser | Regex | Simple, no LLM overhead |
| Database | PostgreSQL (Render free) | Familiar, cheap |
| Hosting | Render Background Worker | $7/mo |

---

## MVP Architecture

```
┌──────────────────┐
│   matrix.org     │  (use existing, no deploy)
│                  │
│  Bot account:    │
│  @factumerit:    │
│   matrix.org     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐     ┌──────────────────┐
│ factumerit-bot   │────▶│ PostgreSQL       │
│ (Render Worker)  │     │ (Render free)    │
│                  │     │                  │
│ - matrix-nio     │     │ - users          │
│ - regex parser   │     │ - vikunjae       │
│ - httpx          │     │                  │
└────────┬─────────┘     └──────────────────┘
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

### Must Have (MVP)
- [ ] Bot responds to DMs on matrix.org
- [ ] `config add` connects to Vikunja, stores encrypted token
- [ ] `what's due today` lists tasks
- [ ] `add [title]` creates task
- [ ] `done [id]` completes task
- [ ] Bot handles errors gracefully (invalid token, network issues)

### Should Have (MVP+)
- [ ] `config test` probes permissions
- [ ] `config list` shows connection
- [ ] `config remove` deletes connection
- [ ] `help` shows available commands

### Won't Have (MVP)
- Own Dendrite
- Natural language parsing (LLM)
- Multiple vikunjae per user
- One-click provisioning
- Cloud LLM analysis

---

## File Structure

```
factumerit/
├── bot/
│   ├── __init__.py
│   ├── __main__.py          # Entry point
│   ├── client.py             # Matrix client wrapper
│   ├── handlers.py           # Message handlers
│   └── parser.py             # Regex command parser
├── vikunja/
│   ├── __init__.py
│   ├── client.py             # Vikunja API client
│   └── models.py             # Task, Project models
├── db/
│   ├── __init__.py
│   ├── connection.py         # asyncpg connection
│   ├── users.py              # User CRUD
│   └── vikunjae.py           # Vikunja connection CRUD
├── config.py                 # Settings from env
└── security.py               # Token encryption
```

---

## Implementation Order

1. **Project setup** - Poetry, structure, config
2. **Database** - Schema, connection, basic CRUD
3. **Vikunja client** - API wrapper, list/add/complete
4. **Matrix client** - Connect, receive messages
5. **Parser** - Regex command matching
6. **Handlers** - Wire parser → vikunja actions
7. **Config commands** - add, test, list, remove
8. **Error handling** - Graceful failures
9. **Deploy** - Render, test live

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
