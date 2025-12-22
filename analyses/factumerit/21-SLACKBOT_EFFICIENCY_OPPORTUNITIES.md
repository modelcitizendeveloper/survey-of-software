# Factum Erit Slack Bot: Efficiency & Intelligence Opportunities

**Date**: 2025-12-20
**Status**: Exploration
**Context**: Analysis of vikunja-slack-bot capabilities and improvement opportunities

---

## Current Architecture Summary

The Factum Erit bot is a **hybrid MCP server + Slack app** (5,907 lines) that:
- Exposes 58 Vikunja tools to Claude via MCP
- Handles per-user Vikunja tokens (multi-tenant)
- Tracks usage/costs with budget enforcement
- Manages conversation memory (rolling window)
- Generates ICS calendar feeds

### What Makes It "Smart" Today

| Feature | Implementation | Value |
|---------|----------------|-------|
| Per-user tokens | Context variables inject user's Vikunja token | Multi-tenant from single bot |
| Usage tracking | Input/output tokens per user per month | Cost control ($2/day, $20/month limits) |
| Memory | Last N messages from Slack history | Continuity across sessions |
| Model flexibility | Haiku/Sonnet/Opus per user | Cost vs capability tradeoff |
| Tool gating | `SLACK_EXCLUDED_TOOLS` blocks expensive ops | Prevents runaway API calls |
| Timezone | Cached from Slack profile | Accurate date reasoning |

### What Makes It "Dumb" Today

| Limitation | Impact | Difficulty to Fix |
|------------|--------|-------------------|
| No file attachments | Can't process images/PDFs dropped in chat | Medium (need vision API) |
| Admin-provisioned tokens | Users can't self-register tokens | Low (add `/token` command) |
| No audit logging | Can't see what Claude did on user's behalf | Low (add logging) |
| Single system prompt | Same behavior for all users/workspaces | Low (user prefs) |
| No "current project" | Must specify project_id every time | Medium (session state) |
| Limited batch intelligence | Batch ops require exact data structures | Medium (fuzzy matching) |

---

## Efficiency Opportunities

### 1. Leverage Vikunja's Server-Side Filtering

**Current State**: The `search_all()` tool accepts Vikunja filter syntax but it's underutilized.

**Vikunja Filter Syntax** (from UI docs):
```
# Fields: done, priority, percentDone, dueDate, startDate, endDate, doneAt, assignees, labels, project
# Operators: !=, =, >, >=, <, <=, like, in
# Logical: &&, ||, ( )
# Date math: now, now+7d, now-1w
```

**Opportunity**: Add pre-built filter tools that generate efficient server-side queries:

```python
# Instead of fetching all tasks then filtering client-side:
@mcp.tool()
def overdue_tasks(project_id: int = 0) -> dict:
    """Tasks with due date in the past, not done"""
    return search_all(filter="dueDate < now && done = false", project_id=project_id)

@mcp.tool()
def due_this_week(project_id: int = 0) -> dict:
    """Tasks due within the next 7 days"""
    return search_all(filter="dueDate >= now && dueDate <= now+7d && done = false")

@mcp.tool()
def high_priority_open(project_id: int = 0) -> dict:
    """Priority 3+ tasks not yet done"""
    return search_all(filter="priority >= 3 && done = false")

@mcp.tool()
def stale_in_progress(days: int = 14) -> dict:
    """Tasks started but not updated recently"""
    # Note: Vikunja may not support updatedAt filter - verify API
    return search_all(filter=f"percentDone > 0 && percentDone < 100 && done = false")
```

**Benefit**: Reduces API calls, faster responses, lower token usage (smaller result sets).

---

### 2. Self-Service Token Registration

**Current Flow**:
1. User creates Vikunja account via Slack OIDC
2. User generates API token in Vikunja Settings
3. User tells admin the token (insecure!)
4. Admin runs `admin_set_user_token` tool

**Proposed Flow**:
1. User creates Vikunja account via Slack OIDC
2. User generates API token in Vikunja Settings
3. User DMs bot: `/register <token>`
4. Bot validates token (GET /api/v1/user) and stores it

**Implementation**:
```python
@app.command("/register")
async def register_token(ack, command, say):
    await ack()
    token = command["text"].strip()
    user_id = command["user_id"]

    # Validate token against Vikunja
    try:
        resp = requests.get(f"{VIKUNJA_URL}/api/v1/user",
                           headers={"Authorization": f"Bearer {token}"})
        if resp.status_code == 200:
            # Store in config
            _set_user_token(user_id, token)
            await say("Token validated and saved! You're ready to use Factum Erit.")
        else:
            await say("Invalid token. Please check and try again.")
    except Exception as e:
        await say(f"Error validating token: {e}")
```

**Security**: Token sent in DM (not public channel), validated before storage.

---

### 3. Project Context / "Current Project"

**Problem**: Users must specify `project_id` for most operations:
> "Create a task in project 5 called 'Buy groceries'"

**Solution**: Add session-level "current project" that persists:

```python
# User preferences stored in config.yaml
users:
  U12345:
    vikunja_token: xxx
    current_project: 5
    current_project_name: "Home"

@mcp.tool()
def set_current_project(project_id: int) -> dict:
    """Set the default project for subsequent operations"""
    # Validate project exists
    project = _get_project(project_id)
    _set_user_pref("current_project", project_id)
    _set_user_pref("current_project_name", project["title"])
    return {"success": True, "project": project["title"]}

# Then in other tools:
def create_task(project_id: int = 0, title: str = "", ...):
    if project_id == 0:
        project_id = _get_user_pref("current_project")
        if not project_id:
            return {"error": "No project specified and no current project set. Use set_current_project first."}
```

**UX**: "You're now working in 'Home'. Tasks will be created there unless you specify otherwise."

---

### 4. Smart Defaults from Project Config

**Current**: `batch_create_tasks` requires explicit bucket_id, label_ids.

**Enhancement**: Use project config for smart defaults:

```yaml
# In config.yaml
projects:
  5:  # Home project
    default_bucket: "Inbox"
    default_labels: ["personal"]
    auto_labels:
      - pattern: "buy|purchase|order"
        label: "shopping"
      - pattern: "call|email|text"
        label: "communication"
```

**Implementation**:
```python
def create_task(project_id: int, title: str, ...):
    config = _get_project_config(project_id)

    # Apply default bucket if not specified
    if not bucket_id and config.get("default_bucket"):
        bucket_id = _resolve_bucket_id(project_id, config["default_bucket"])

    # Apply auto-labels based on title patterns
    for rule in config.get("auto_labels", []):
        if re.search(rule["pattern"], title, re.IGNORECASE):
            labels.append(rule["label"])
```

---

### 5. Conversation Intelligence

**Current**: Memory is simple rolling window (last N messages).

**Enhancement**: Add conversation summaries for long-term context:

```python
# After N exchanges, summarize and compress
def _maybe_summarize_conversation(user_id: str, messages: list):
    if len(messages) > 20:
        # Use Claude to summarize older messages
        summary = _call_claude_for_summary(messages[:15])
        # Store summary, keep only recent 5 messages
        _set_user_pref("conversation_summary", summary)
        return [{"role": "system", "content": f"Previous conversation summary: {summary}"}] + messages[-5:]
    return messages
```

---

### 6. Proactive Notifications

**Current**: Bot only responds when messaged.

**Enhancement**: Daily digest or alerts:

```python
# Scheduled job (Render cron or background thread)
async def daily_digest():
    for user_id, config in users.items():
        overdue = _get_overdue_tasks(config["vikunja_token"])
        due_today = _get_due_today(config["vikunja_token"])

        if overdue or due_today:
            message = f"Good morning! You have {len(overdue)} overdue tasks and {len(due_today)} due today."
            await slack_client.chat_postMessage(channel=user_id, text=message)
```

**Caution**: Requires careful rate limiting and user opt-in.

---

## Cost Efficiency Improvements

### Current Cost Model
- Haiku: $0.80/$4.00 per 1M input/output tokens
- Sonnet: $3.00/$15.00 per 1M tokens
- Opus: $15.00/$75.00 per 1M tokens

### Optimization Strategies

1. **Tool Result Compression**: Truncate large lists before returning to Claude
2. **Caching**: Already implemented (30s TTL on task lists)
3. **Server-side Filtering**: Reduces payload size dramatically
4. **Model Degradation**: Already implemented (auto-switch to Haiku on budget)
5. **Response Streaming**: Would improve perceived latency (not cost)

---

## Priority Ranking

| Opportunity | Impact | Effort | Priority |
|-------------|--------|--------|----------|
| Server-side filter tools | High (efficiency) | Low | **P0** |
| Self-service token registration | High (UX) | Low | **P0** |
| Current project context | Medium (UX) | Low | **P1** |
| Smart defaults from config | Medium (UX) | Medium | **P1** |
| Conversation summaries | Medium (quality) | Medium | **P2** |
| Proactive notifications | Low (nice-to-have) | High | **P3** |

---

## Next Steps

1. **Validate filter syntax**: Test Vikunja's date math and field support
2. **Prototype `/register`**: Implement token self-service in dev
3. **Design project context UX**: How does user set/clear current project?
4. **Measure current costs**: Get baseline token usage before optimization

---

## Related Files

- Bot source: `/home/ivanadamin/vikunja-slack-bot/src/vikunja_mcp/server.py`
- MCP dev: `/home/ivanadamin/spawn-solutions/development/projects/impl-1131-vikunja/vikunja-mcp/`
- Sync docs: `/home/ivanadamin/vikunja-slack-bot/SYNC.md`
