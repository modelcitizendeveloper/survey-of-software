# Matrix Bot Instance Management Redesign

**Date**: 2025-12-28  
**Status**: Planning  
**Context**: Fix instance selection logic for Matrix bot to match Slack bot and MCP server patterns

---

## Current State Analysis

### How Slack Bot Works (Multi-Instance)

**Instance Storage**: YAML config `instances` section
```yaml
instances:
  personal:
    url: https://vikunja.factumerit.app
    token: tk_xxx
  business:
    url: https://app.vikunja.cloud
    token: tk_yyy
```

**User Preferences**: YAML config `users` section
```yaml
users:
  U12345:  # Slack user ID
    vikunja_token: tk_xxx  # Legacy single-instance
    current_project: 5
```

**Command Behavior**:
- Slash commands (`/maybe`, `/now`, `/week`) → Query **ALL instances** in parallel
- Shows `[instance]` tags when multiple instances configured
- No per-user instance selection - always queries all

**Key Functions**:
- `_get_instances()` - Returns all configured instances
- `_fetch_all_pages_from_all_instances()` - Queries all instances
- `_format_tasks_for_slack()` - Adds instance tags

---

### How MCP Server Works (Single-Instance with Switching)

**Instance Storage**: YAML config `instances` section (same as Slack)

**Current Instance**: YAML config `current_instance` field
```yaml
current_instance: personal
```

**User Context**: Per-user instance selection
```yaml
users:
  '@i2:matrix.factumerit.app':
    active_instance: personal  # User's current instance
```

**Command Behavior**:
- Tools use `_get_current_instance()` to determine which instance
- `switch_instance(name)` changes current instance
- All subsequent commands use the switched instance

**Key Functions**:
- `_get_current_instance()` - Returns current instance name
- `_set_current_instance(name)` - Switches instance
- `_get_instance_config(name)` - Gets URL + token for instance

---

### How Matrix Bot Currently Works (BROKEN)

**Token Storage**: PostgreSQL `user_tokens` table
```sql
user_id | vikunja_instance | encrypted_token
@i2:... | personal         | <encrypted>
@i2:... | business         | <encrypted>
@i2:... | default          | <encrypted>
```

**Instance Selection**: YAML config `users` section
```yaml
users:
  '@i2:matrix.factumerit.app':
    active_instance: ???  # NOT SET
```

**Current Behavior**:
1. `_get_user_vikunja_token(user_id)` hardcoded to `instance="default"`
2. `_get_user_instance(user_id)` reads from YAML `users.{user_id}.active_instance`
3. No user entry in YAML → returns `None`
4. Commands fail because no instance configured

**The Problem**:
- Tokens in PostgreSQL with instance names (`personal`, `business`)
- No user entry in YAML config
- `_get_user_vikunja_token()` always queries `instance="default"`
- User has no `default` instance token, only `personal` and `business`

---

## Design Decision: Which Pattern Should Matrix Bot Follow?

### Option A: Follow Slack Bot (Multi-Instance, Query All)

**Pros**:
- Consistent with Slack bot behavior
- Users see all tasks from all instances
- No need to switch instances

**Cons**:
- More complex for users with many instances
- Higher API usage (queries all instances)
- Doesn't match MCP server pattern

### Option B: Follow MCP Server (Single-Instance with Switching)

**Pros**:
- Consistent with MCP server behavior
- Users can focus on one instance at a time
- Lower API usage
- Matches user's mental model (working in one context)

**Cons**:
- Users must manually switch instances
- Need to add `!switch` command to Matrix bot

### Option C: Hybrid (Default Instance + Query All Option)

**Pros**:
- Best of both worlds
- `!maybe`, `!now` → Query active instance only
- `!maybe --all`, `!now --all` → Query all instances
- Users can switch default instance

**Cons**:
- More complex implementation
- Need to teach users about `--all` flag

---

## Recommended Approach: Option B (MCP Server Pattern)

**Rationale**:
1. Matrix bot is primarily for personal use (1-on-1 DM)
2. Users likely have 1-2 instances (personal + work)
3. Switching context is natural ("I'm working on personal tasks now")
4. Matches MCP server behavior (consistency)
5. Simpler implementation

---

## Implementation Plan

### Phase 1: Fix Token Retrieval

**Current Code** (`server.py` line ~977):
```python
token = get_user_token(
    user_id=user_id,
    purpose="get_user_token",
    instance="default",  # ← HARDCODED
    caller="server._get_user_vikunja_token"
)
```

**Fixed Code**:
```python
# Get user's active instance
instance = _get_user_instance(user_id) or "default"

token = get_user_token(
    user_id=user_id,
    purpose="get_user_token",
    instance=instance,  # ← Use user's active instance
    caller="server._get_user_vikunja_token"
)
```

### Phase 2: Welcome Back Message

When user sends first message after having tokens:
```python
async def handle_first_message(user_id):
    # Query PostgreSQL for user's instances
    instances = get_user_instances(user_id)  # ['personal', 'business']
    
    if not instances:
        return show_onboarding_message()
    
    # User has instances - show welcome back
    active = _get_user_instance(user_id) or instances[0]
    
    message = f"""
👋 Welcome back! You have {len(instances)} Vikunja instance(s) connected:

"""
    for inst in instances:
        marker = "✓" if inst == active else " "
        message += f"[{marker}] {inst}\n"
    
    message += f"""

**Active instance**: {active}

**Commands**:
- `!maybe`, `!now`, `!week` - Search active instance
- `!switch <instance>` - Change active instance
- `!instances` - List all instances
- `!help` - Show all commands
"""
    
    return message
```

### Phase 3: Add Matrix Commands

**New Commands**:
1. `!switch <instance>` - Change active instance
2. `!instances` - List all connected instances
3. `!vik <url> <token>` - Connect new instance (existing, but needs instance name)

**Updated `!vik` Command**:
```python
# Current: !vik <token> or !vik <url> <token>
# New: !vik <instance_name> <url> <token>

# Examples:
!vik personal https://vikunja.factumerit.app tk_xxx
!vik work https://app.vikunja.cloud tk_yyy

# Backward compatible:
!vik tk_xxx  # Assumes instance="default", url=VIKUNJA_URL env var
```

### Phase 4: PostgreSQL Helper Functions

**New Functions in `token_broker.py`**:
```python
def get_user_instances(user_id: str) -> list[str]:
    """Get list of instance names for a user."""
    query = """
        SELECT DISTINCT vikunja_instance
        FROM user_tokens
        WHERE user_id = %s AND revoked = FALSE
        ORDER BY vikunja_instance
    """
    # Returns ['business', 'default', 'personal']

def get_instance_info(user_id: str, instance: str) -> dict:
    """Get instance details (URL, token, access count, etc.)."""
    # Query user_tokens + instance config
    # Returns {url, last_accessed, access_count, expires_at}
```

---

## Migration Strategy

### Step 1: Add User Entries to YAML Config

For existing users with tokens in PostgreSQL:
```python
# Migration script
def migrate_user_instances():
    users = get_all_users_from_postgres()

    for user_id in users:
        instances = get_user_instances(user_id)

        if instances:
            # Set first instance as active
            _set_user_instance(user_id, instances[0])

            print(f"Set {user_id} active_instance to {instances[0]}")
```

### Step 2: Update `_get_user_vikunja_token()`

Change hardcoded `instance="default"` to use `_get_user_instance(user_id)`.

### Step 3: Add Welcome Back Logic

Detect returning users and show instance summary.

### Step 4: Add `!switch` and `!instances` Commands

Implement Matrix command handlers.

---

## Testing Plan

### Test Case 1: User with Multiple Instances

**Setup**:
- User `@i2` has tokens for `personal` and `business`
- Active instance: `personal`

**Test**:
1. Send `!test` → Should show "Connected to personal instance"
2. Send `!maybe` → Should query personal instance only
3. Send `!switch business` → Should switch to business
4. Send `!maybe` → Should query business instance only
5. Send `!instances` → Should list both instances with `business` marked active

### Test Case 2: New User Onboarding

**Setup**:
- User `@alice` has no tokens

**Test**:
1. Send `!vik` → Should show onboarding instructions
2. Send `!vik personal https://vikunja.factumerit.app tk_xxx` → Should save token
3. Send `!test` → Should show "Connected to personal instance"
4. Send `!maybe` → Should query personal instance

### Test Case 3: User with Only Default Instance

**Setup**:
- User `@bob` has token for `default` instance only

**Test**:
1. Send `!test` → Should show "Connected to default instance"
2. Send `!maybe` → Should query default instance
3. Send `!instances` → Should show only default instance

---

## Summary

**Current Problem**:
- Matrix bot hardcoded to query `instance="default"`
- Users have tokens for `personal`, `business` instances
- No user entry in YAML config → `_get_user_instance()` returns `None`
- Commands fail silently

**Solution**:
1. Fix `_get_user_vikunja_token()` to use `_get_user_instance(user_id)`
2. Add welcome back message showing all instances
3. Add `!switch` and `!instances` commands
4. Migrate existing users to have `active_instance` set

**Next Steps**:
1. Review this plan with user
2. Implement Phase 1 (fix token retrieval)
3. Test with `@i2` user
4. Implement Phase 2 (welcome back message)
5. Implement Phase 3 (new commands)

