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

Bot: Hi! I'm Factumerit, your task assistant.

     Get started in one click:
     → factumerit.com/setup?mid=@user:matrix.org&nonce=abc123

     (Already have Vikunja? Say "config add")
```

### Easy Path: One-Click Provisioning

```
User: [clicks link]

Browser: factumerit.com/setup
         ┌────────────────────────────────────┐
         │  Welcome, @user:matrix.org!        │
         │                                     │
         │  Creating your Vikunja account...  │
         │  ✓ Account created                 │
         │  ✓ Default projects set up         │
         │  ✓ Connected to bot                │
         │                                     │
         │  Go back to Matrix and try:        │
         │  "add buy groceries"               │
         └────────────────────────────────────┘

User: [back in Matrix] what's due today

Bot: 📋 You're all set! No tasks yet.

     Try: "add buy groceries" or "add call mom tomorrow"
```

### Side Door: BYOV (Bring Your Own Vikunja)

```
User: config add

Bot: To connect your Vikunja:

     1. Create an API token at:
        [your-vikunja]/user/settings/api-tokens

     2. Recommended scopes:
        ✓ tasks:read, tasks:write
        ✓ projects:read
        ✓ labels:read, labels:write

     3. Then: config add [url] [token]

User: config add https://tasks.mycompany.com vkt_abc123

Bot: ✓ Connected to tasks.mycompany.com

     Found 3 projects, 27 tasks.
     Your data stays on your server.

     To verify token permissions: config test
```

### Permission Testing (Explicit)

```
User: config test

Bot: Testing permissions on tasks.mycompany.com...

     Creating test task... ✓
     Reading tasks... ✓
     Updating task... ✓
     Deleting test task... ✓

     ✓ Full read/write access confirmed.
```

Read-only token:

```
User: config test

Bot: Testing permissions on tasks.mycompany.com...

     Reading tasks... ✓
     Creating test task... ✗ (403 Forbidden)

     This token is read-only. I can show your tasks
     but can't add or modify them.

     For full features, add these scopes to your token:
     • tasks:write
     • projects:write
```

---

## Multiple Vikunjae

The bot supports connecting to **multiple vikunjae** (Vikunja backends):

```
User: config add https://work.vikunja.io vkt_work123 --name work
User: config add https://home.vikunja.io vkt_home456 --name home

Bot: ✓ You have 2 vikunjae:
     • work → work.vikunja.io (15 tasks)
     • home → home.vikunja.io (8 tasks)

User: what's due today

Bot: 📋 Due Today:

     **work** (2 tasks):
     1. [ ] Review PR #42
     2. [ ] Team standup

     **home** (1 task):
     1. [ ] Buy groceries

User: add fix bug to work

Bot: ✓ Added "fix bug" to work
```

### Vikunja Commands

```
config add [url] [token]           Add a vikunja
config add [url] [token] --name X  Add with alias
config test                        Test token permissions (explicit)
config remove [name]               Remove vikunja
config list                        Show all vikunjae
config default [name]              Set default vikunja
```

---

## Provisioning Implementation

### One-Click Flow

```python
# Bot generates unique provisioning link
async def handle_new_user(room, event):
    matrix_id = event.sender

    # Check existing vikunjae
    vikunjae = await db.get_vikunjae(matrix_id)
    if vikunjae:
        return await show_welcome_back(room, vikunjae)

    # Generate one-time nonce
    nonce = secrets.token_urlsafe(32)
    await db.store_nonce(matrix_id, nonce, expires=timedelta(hours=1))

    link = f"https://factumerit.com/setup?mid={quote(matrix_id)}&nonce={nonce}"

    await self.send(room, ONBOARDING_MESSAGE.format(link=link))
```

### Provisioning Endpoint

```python
@app.get("/setup")
async def setup(mid: str, nonce: str):
    # Verify nonce
    if not await db.verify_nonce(mid, nonce):
        raise HTTPException(400, "Link expired or invalid")

    # Create Vikunja user on hosted instance
    username = sanitize_username(mid)  # @alice:matrix.org → alice_matrix_org

    user = await vikunja_admin.create_user(
        username=username,
        email=f"{username}@users.factumerit.com"
    )

    # Create default projects
    await vikunja_admin.create_project(user.id, "Inbox")
    await vikunja_admin.create_project(user.id, "Personal")
    await vikunja_admin.create_project(user.id, "Work")

    # Generate API token
    token = await vikunja_admin.create_token(user.id, name="Factumerit Bot")

    # Store vikunja
    await db.add_vikunja(
        matrix_id=mid,
        url="https://vikunja.factumerit.com",
        token=token,
        name="default",
        is_hosted=True
    )

    # Invalidate nonce
    await db.delete_nonce(mid, nonce)

    return templates.TemplateResponse("success.html", {"matrix_id": mid})
```

### User Storage

```json
{
  "matrix_id": "@alice:matrix.org",
  "vikunjae": [
    {
      "name": "default",
      "url": "https://vikunja.factumerit.com",
      "token": "vkt_...",
      "is_hosted": true,
      "created": "2025-12-22"
    },
    {
      "name": "work",
      "url": "https://tasks.company.com",
      "token": "vkt_...",
      "is_hosted": false,
      "created": "2025-12-22"
    }
  ],
  "default_vikunja": "default",
  "llm_provider": null,
  "llm_key": null
}
```

---

## Hosted vs BYOT Comparison

| Aspect | Hosted (Quick Start) | BYOT (Bring Your Own) |
|--------|---------------------|----------------------|
| Setup | One click | Manual token |
| Data location | Factumerit servers | Your servers |
| Backup | Factumerit manages | You manage |
| Cost | Free tier / paid | Your Vikunja cost |
| Privacy | Shared infra | Full control |
| Features | All | All |

---

## Step 2: Basic Usage (After Connection)

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
