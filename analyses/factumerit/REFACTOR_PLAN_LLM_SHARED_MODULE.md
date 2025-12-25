# LLM Integration Refactor: Shared Module Architecture

**Date**: 2025-12-25  
**Epic**: solutions-ndw6  
**Goal**: Single source of truth for LLM logic - no copypasta between Slack/Matrix/MCP  
**Status**: Planned (8 subtasks created)

---

## Problem Statement

**Current State**: 
- ✅ Slack bot has full LLM integration (_slack_chat_with_claude)
- ✅ Matrix bot has ECO mode (quick commands)
- ❌ Matrix bot lacks LLM integration (returns raw JSON for natural language)
- ❌ Code duplication risk if we copy-paste Slack implementation

**User Request**: "i like option 2. we now have the matrix-specific code working. we need to maintained shared codebase for mcp, slack, matrix. no copypasta"

---

## Architecture: Option 2 (Clean Refactor)

### New Module: `llm_integration.py`

**Location**: `src/vikunja_mcp/llm_integration.py`

**Purpose**: Transport-agnostic LLM interaction, usage tracking, cost control

**Core Functions**:
```python
# Main LLM interaction
def chat_with_claude(
    user_message: str,
    user_id: str,
    conversation_history: list[dict],
    tools: list[dict],
    system_prompt_additions: str = ""
) -> dict:
    """
    Returns:
        {
            "response": str,           # Raw text response
            "input_tokens": int,
            "output_tokens": int,
            "cost": float,
            "using_own_key": bool,
            "warning": str | None,     # Budget warnings
            "model": str               # Model used
        }
    """

# Usage tracking
def check_usage_limits(user_id: str) -> dict
def update_user_usage(user_id: str, input_tokens: int, output_tokens: int) -> dict
def get_user_credits_info(user_id: str) -> dict

# API key management (BYOK)
def get_user_anthropic_api_key(user_id: str) -> str | None
def set_user_anthropic_api_key(user_id: str, api_key: str) -> dict
def validate_anthropic_api_key(api_key: str) -> tuple[bool, str]
```

---

## Implementation Plan

### Phase 1: Extract to Shared Module

**Subtasks**:
1. ✅ **solutions-ndw6.1**: Create `llm_integration.py` module
2. ✅ **solutions-ndw6.2**: Extract usage tracking functions
3. ✅ **solutions-ndw6.3**: Extract API key management
4. ✅ **solutions-ndw6.4**: Create transport-agnostic `chat_with_claude()`

**Key Principle**: No Slack or Matrix specific code in shared module
- ❌ No `_fetch_slack_history()` 
- ❌ No `_md_to_slack_mrkdwn()`
- ❌ No Matrix room history fetching
- ✅ Just pure LLM interaction + usage tracking

---

### Phase 2: Refactor Slack to Use Shared Module

**Subtask**: solutions-ndw6.5

**Before** (server.py):
```python
def _slack_chat_with_claude(user_message, user_id, client, channel):
    # 150 lines of LLM + usage tracking + formatting
    ...
```

**After** (server.py):
```python
def _slack_chat_with_claude(user_message, user_id, client, channel):
    # Slack-specific: Fetch conversation history
    history = _fetch_slack_history(client, channel, user_id)
    
    # Shared: LLM interaction
    from .llm_integration import chat_with_claude
    result = chat_with_claude(
        user_message=user_message,
        user_id=user_id,
        conversation_history=history,
        tools=SLACK_TOOLS,
        system_prompt_additions=_get_user_timezone_prompt(user_id)
    )
    
    # Slack-specific: Format response
    response = result["response"]
    if result.get("warning"):
        response += f"\n\n{result['warning']}"
    
    return _md_to_slack_mrkdwn(response)
```

**Testing**: All Slack commands must still work (DM, channel, natural language)

---

### Phase 3: Implement Matrix LLM Integration

**Subtask**: solutions-ndw6.6

**New Function** (matrix_client.py):
```python
async def _matrix_chat_with_claude(user_message, user_id, room_id):
    # Matrix-specific: Fetch room history
    history = await self._fetch_room_history(room_id, limit=20)
    
    # Shared: LLM interaction (same code as Slack!)
    from .llm_integration import chat_with_claude
    result = chat_with_claude(
        user_message=user_message,
        user_id=user_id,
        conversation_history=history,
        tools=MATRIX_TOOLS,  # Same as SLACK_TOOLS
        system_prompt_additions=""
    )
    
    # Matrix-specific: Format response (markdown already works)
    response = result["response"]
    if result.get("warning"):
        response += f"\n\n{result['warning']}"
    
    return response
```

**Wire Up** (matrix_client.py):
```python
# In message handler
if result.get("needs_llm"):
    response = await self._matrix_chat_with_claude(
        message, 
        event.sender, 
        room.room_id
    )
    await self._send_message(room.room_id, response)
```

---

### Phase 4: Add Matrix Cost Control

**Subtask**: solutions-ndw6.7

**New Commands**:
- `!credits` - Show remaining budget
- `!apikey <key>` - Set own API key (BYOK)
- `!apikey status` - Check if key is set
- `!apikey remove` - Remove key

**Admin Commands** (already exist in Slack):
- `!credits @user:domain.com +5` - Add credits (admin only)

**Testing**: 
- ✅ Matrix user gets $1 free credit
- ✅ Warning at 80% usage
- ✅ Hard block at 100% usage
- ✅ BYOK bypasses limits

---

### Phase 5: Integration Testing

**Subtask**: solutions-ndw6.8

**Test Matrix**:
| Transport | Test Case | Expected |
|-----------|-----------|----------|
| Slack DM | "show my tasks" | Task list |
| Slack channel | "@bot show my tasks" | Task list |
| Matrix DM | "show my tasks" | Task list |
| Matrix room | "show my tasks" | Task list |
| Slack | Usage tracking | Tokens counted |
| Matrix | Usage tracking | Tokens counted |
| Slack | Budget limit | Blocked at $1 |
| Matrix | Budget limit | Blocked at $1 |
| Slack | BYOK | Uses own key |
| Matrix | BYOK | Uses own key |

**Update Tests**: `tests/integration/test_matrix_bot.py`
- Currently: Natural language test expects fallback or `[]`
- After: Natural language test expects actual task list

---

## Benefits of This Approach

### ✅ Single Source of Truth
- LLM logic in one place
- Bug fixes apply to all transports
- Feature additions benefit everyone

### ✅ Maintainability
- Changes to usage tracking: edit one file
- Changes to Claude API: edit one file
- No risk of Slack/Matrix diverging

### ✅ Testability
- Can test `chat_with_claude()` in isolation
- Mock conversation history easily
- No transport-specific dependencies

### ✅ Extensibility
- Future transports (Discord, Telegram) just call shared module
- MCP can use same usage tracking
- Easy to add new features (streaming, caching, etc.)

---

## Migration Strategy

### Step 1: Create Shared Module (No Breaking Changes)
- Create `llm_integration.py`
- Extract functions from `server.py`
- Keep old functions in `server.py` (deprecated but working)

### Step 2: Refactor Slack (Test Thoroughly)
- Update `_slack_chat_with_claude()` to use shared module
- Run all Slack tests
- Deploy to production
- Monitor for issues

### Step 3: Implement Matrix (New Feature)
- Add `_matrix_chat_with_claude()`
- Wire up to `needs_llm=True` path
- Run all Matrix tests
- Deploy to production

### Step 4: Cleanup (Optional)
- Remove deprecated functions from `server.py`
- Update documentation
- Add architecture diagram

---

## Risk Mitigation

### Risk: Breaking Slack Bot
**Mitigation**: 
- Keep old `_slack_chat_with_claude()` until new version tested
- Deploy to staging first
- Run full integration test suite
- Monitor error rates after deploy

### Risk: User ID Format Differences
**Mitigation**:
- Slack: `U12345ABC` (alphanumeric)
- Matrix: `@user:domain.com` (email-like)
- Shared module treats user_id as opaque string
- Config storage already handles both formats

### Risk: Conversation History Format Differences
**Mitigation**:
- Shared module expects standard format: `[{"role": "user", "content": "..."}]`
- Slack adapter converts from Slack API format
- Matrix adapter converts from Matrix API format
- Both produce same structure for shared module

---

## Success Criteria

### Phase 1-2 Complete When:
- ✅ Slack bot still works (all tests pass)
- ✅ No code duplication in LLM logic
- ✅ `llm_integration.py` has no transport-specific code

### Phase 3-4 Complete When:
- ✅ Matrix bot handles natural language queries
- ✅ "show my tasks" returns task list (not raw JSON)
- ✅ Usage tracking works for Matrix users
- ✅ Budget limits enforced for Matrix users

### Phase 5 Complete When:
- ✅ All integration tests pass
- ✅ Both Slack and Matrix use same LLM code
- ✅ solutions-27l2 closed (natural language works)
- ✅ solutions-ndw6 closed (refactor complete)

---

## Timeline Estimate

| Phase | Effort | Dependencies |
|-------|--------|--------------|
| 1. Extract to shared module | 4-6 hours | None |
| 2. Refactor Slack | 2-3 hours | Phase 1 |
| 3. Implement Matrix LLM | 3-4 hours | Phase 2 |
| 4. Add Matrix cost control | 2-3 hours | Phase 3 |
| 5. Integration testing | 2-3 hours | Phase 4 |
| **TOTAL** | **13-19 hours** | |

**Calendar Time**: 2-3 days (with testing and deployment)

---

## Next Steps

1. **Start with solutions-ndw6.1**: Create `llm_integration.py` skeleton
2. **Extract functions incrementally**: One function at a time, test after each
3. **Keep Slack working**: Don't break production while refactoring
4. **Add Matrix LLM**: Once shared module stable
5. **Test thoroughly**: Both transports, all features

---

**Status**: Ready to start implementation  
**Blocker**: None  
**Owner**: TBD

