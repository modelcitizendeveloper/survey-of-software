# 24: User Experience Flow - Tiered Model Architecture

**Date**: 2025-12-22
**Status**: Design
**Context**: Onboarding and capability tiers for Matrix bot

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                      User Message                        │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   Has Vikunja Token?                     │
│                    No → Onboarding                       │
│                    Yes ↓                                 │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              Local Model (Ollama/Mistral)                │
│                                                          │
│   "show tasks due today" → parse → GET /api/v1/tasks    │
│   "add buy milk" → parse → PUT /api/v1/tasks            │
│   "what's overdue" → parse → GET + filter               │
│                                                          │
│   ✓ Command parsing (NLU → API)                         │
│   ✓ Basic summaries                                     │
│   ✓ Simple Q&A about tasks                              │
│   ✗ Deep analysis                                       │
│   ✗ Prioritization advice                               │
│   ✗ Multi-day planning                                  │
└─────────────────────────┬───────────────────────────────┘
                          │
            User asks complex question
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              Has Cloud API Key?                          │
│                                                          │
│   No →  "I can give you a basic answer. For deeper      │
│          analysis, add a Claude or OpenAI key:          │
│          `config apikey sk-...`"                        │
│                                                          │
│   Yes → Route to Claude/GPT                             │
│         ✓ "Analyze my productivity this week"           │
│         ✓ "What should I focus on today?"               │
│         ✓ "Help me plan this project"                   │
└─────────────────────────────────────────────────────────┘
```

---

## Onboarding Flow

### Step 1: First Contact

```
User: hi

Bot: Hi! I'm Factumerit, a task assistant for Vikunja.

     To get started, I need your Vikunja API token.

     Get it from: [your-vikunja-url]/user/settings/api-tokens

     Then send: config vikunja [token]
```

### Step 2: Vikunja Connected

```
User: config vikunja vkt_abc123...

Bot: ✓ Connected to Vikunja!

     Found 3 projects, 27 tasks.

     Try: "what's due today" or "add buy groceries"

     I'm using a local model for basic commands.
     For smarter analysis, you can add a Claude API key later.
```

### Step 3: Basic Usage (Local Model)

```
User: what's due today

Bot: 📋 Due Today (3 tasks):

     1. [ ] Call dentist (Health)
     2. [ ] Review PR #42 (Work)
     3. [ ] Buy groceries (Personal)
```

### Step 4: Complex Request → Upsell

```
User: analyze my productivity this week

Bot: This week you completed 12 tasks and have 8 remaining.

     💡 For deeper analysis (patterns, suggestions, planning),
     add a cloud API key:

     config claude sk-ant-...
     config openai sk-...
```

### Step 5: Full Capability

```
User: config claude sk-ant-abc123...

Bot: ✓ Claude connected. Full analysis available.

User: analyze my productivity this week

Bot: Looking at your week...

     **Patterns:**
     - Most productive Tuesday (7 tasks)
     - Health tasks consistently deferred
     - Work tasks done same-day

     **Suggestions:**
     - Schedule dentist first thing tomorrow
     - Your "Review" tasks average 2 days late

     **This week's focus:**
     1. Clear the 3 overdue Health tasks
     2. PR #42 is blocking #45 and #46
```

---

## Model Selection

### Local Model (Free Tier)

| Model | Size | Use Case |
|-------|------|----------|
| **Mistral 7B** | 4GB | Good balance, fast |
| **Llama 3 8B** | 5GB | Better reasoning |
| **Phi-3 mini** | 2GB | Minimal resources |

**Capabilities:**
- Intent classification ("list", "add", "complete", "query")
- Entity extraction (dates, project names, task titles)
- Simple response generation

**Prompt template:**
```
You are a task bot parser. Convert user messages to actions.

User: "show me what's due this week"
Action: {"intent": "list", "filter": {"due_before": "end_of_week"}}

User: "add call mom to personal"
Action: {"intent": "create", "title": "call mom", "project": "personal"}

User: {user_message}
Action:
```

### Cloud Model (Paid Tier)

| Trigger | Route to Cloud |
|---------|----------------|
| "analyze..." | Yes |
| "prioritize..." | Yes |
| "plan..." | Yes |
| "help me think about..." | Yes |
| "suggest..." | Yes |
| Simple CRUD | No (local) |

---

## Configuration Storage

Per-user config stored in Matrix account data or bot's DB:

```json
{
  "user_id": "@alice:matrix.org",
  "vikunja_url": "https://tasks.example.com",
  "vikunja_token": "vkt_...",
  "llm_provider": "claude",
  "llm_key": "sk-ant-...",
  "preferences": {
    "default_project": "inbox",
    "timezone": "America/New_York"
  }
}
```

---

## Privacy Considerations

| Data | Local Model | Cloud Model |
|------|-------------|-------------|
| Task titles | Processed locally | Sent to API |
| Task content | Processed locally | Sent to API |
| API tokens | Stored encrypted | Never sent |
| Conversation | Ephemeral | Sent for context |

**User messaging:**
```
Bot: Note: When using Claude/OpenAI, your task data is sent
     to their API for analysis. Your tokens stay local.

     Use `config privacy local-only` to disable cloud features.
```

---

## Commands Reference

```
config vikunja [token]     Set Vikunja API token
config claude [key]        Set Claude API key
config openai [key]        Set OpenAI API key
config privacy local-only  Disable cloud LLM
config privacy full        Enable cloud LLM
config status              Show current config
config clear               Remove all stored data
```

---

## Implementation Notes

**Ollama integration:**
```python
import httpx

async def local_parse(message: str) -> dict:
    resp = await httpx.post("http://localhost:11434/api/generate", json={
        "model": "mistral",
        "prompt": f"Parse task command: {message}",
        "stream": False
    })
    return parse_action(resp.json()["response"])
```

**Routing logic:**
```python
CLOUD_TRIGGERS = ["analyze", "prioritize", "plan", "suggest", "help me"]

async def route_message(message: str, user_config: dict) -> str:
    # Always use local for simple commands
    action = await local_parse(message)

    if action["intent"] in ["list", "create", "complete", "delete"]:
        return await execute_vikunja(action, user_config)

    # Complex request
    if any(t in message.lower() for t in CLOUD_TRIGGERS):
        if user_config.get("llm_key"):
            return await cloud_analyze(message, user_config)
        else:
            return UPSELL_MESSAGE

    # Fallback: local model does its best
    return await local_respond(message, user_config)
```

---

## Related

- [21-MATRIX_PLATFORM_RECOMMENDATION.md](21-MATRIX_PLATFORM_RECOMMENDATION.md)
- [22-BOT_SDK_EVALUATION.md](22-BOT_SDK_EVALUATION.md)
