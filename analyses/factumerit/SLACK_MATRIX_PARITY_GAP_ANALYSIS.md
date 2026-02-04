# Slack vs Matrix Bot: Feature Parity Gap Analysis

**Date**: 2025-12-25  
**Context**: Matrix bot is production-ready, but lacks LLM integration that Slack bot has  
**Status**: Gap identified, path to parity defined

---

## Executive Summary

**Current State**: Matrix bot has **ECO mode parity** (all quick commands work), but **lacks LLM integration** for natural language queries.

**Gap**: Slack bot has full Claude integration with usage tracking, cost control, and budget limits. Matrix bot returns raw JSON `[]` for natural language queries.

**Impact**: Matrix users can't use natural language like "show my tasks due today" - they must use exact commands like `!now`.

---

## Feature Comparison Matrix

| Feature | Slack Bot | Matrix Bot | Gap |
|---------|-----------|------------|-----|
| **ECO Mode Commands** | ✅ | ✅ | None |
| Quick filters (!oops, !now, !fire) | ✅ | ✅ | None |
| Connection commands (!vik, !viki) | ✅ | ✅ | None |
| Room/channel binding | ✅ | ✅ | None |
| Stats command | ✅ | ✅ | None |
| Help command | ✅ | ✅ | None |
| **Natural Language** | ✅ | ❌ | **CRITICAL** |
| Claude API integration | ✅ | ❌ | **CRITICAL** |
| "show my tasks" parsing | ✅ | ❌ | **CRITICAL** |
| "create task X" | ✅ | ❌ | **CRITICAL** |
| "mark X as done" | ✅ | ❌ | **CRITICAL** |
| **Cost Control** | ✅ | ❌ | **HIGH** |
| Per-user token tracking | ✅ | ❌ | **HIGH** |
| Daily budget limits ($2/day) | ✅ | ❌ | **HIGH** |
| Monthly budget limits ($20/mo) | ✅ | ❌ | **HIGH** |
| Lifetime budget ($1 free) | ✅ | ❌ | **HIGH** |
| Usage warnings (80% threshold) | ✅ | ❌ | **HIGH** |
| Model degradation (Sonnet→Haiku) | ✅ | ❌ | **HIGH** |
| BYOK (bring your own key) | ✅ | ❌ | **MEDIUM** |
| **Advanced Features** | | | |
| Conversation memory | ✅ | ❌ | **MEDIUM** |
| Usage stats footer | ✅ | ❌ | **LOW** |
| Share button (privacy) | ✅ | N/A | Not applicable |
| Slash commands | ✅ | N/A | Different UX |
| Admin commands | ✅ | ✅ | Partial (credits only) |

---

## Critical Gap: LLM Integration

### What Slack Bot Has

**File**: `src/vikunja_mcp/server.py:7847-7989`

```python
def _slack_chat_with_claude(user_message: str, user_id: str = None, ...):
    """Send message to Claude and handle tool calls for Slack bot."""
    
    # 1. Check for user's own API key (BYOK)
    # 2. Check usage limits (lifetime budget)
    # 3. Get conversation history from Slack
    # 4. Build system prompt with timezone
    # 5. Call Claude API with tools
    # 6. Track token usage (input/output)
    # 7. Update cumulative usage
    # 8. Format response with usage stats
    # 9. Add limit warnings if approaching budget
```

**Features**:
- ✅ Per-user API key support (BYOK)
- ✅ Lifetime budget tracking ($1 default)
- ✅ Token usage tracking (input/output)
- ✅ Model selection (Haiku/Sonnet/Opus)
- ✅ Conversation memory (last N messages)
- ✅ System prompt with timezone
- ✅ Tool call handling (58 MCP tools)
- ✅ Usage stats in footer
- ✅ Budget warnings (80% threshold)
- ✅ Hard limit enforcement (block when exhausted)

### What Matrix Bot Has

**File**: `src/vikunja_mcp/matrix_client.py:171-181`

```python
elif result.get("needs_llm"):
    # LLM fallback not implemented yet - send helpful message
    fallback = (
        "I'm not sure how to help with that yet.\n\n"
        "Try these quick commands:\n"
        "• `!help` - See all commands\n"
        "• `!oops` - Overdue tasks\n"
        "• `!now` - Due today\n"
        "• `!fire` - Urgent tasks"
    )
```

**Status**: ❌ **NO LLM INTEGRATION**

---

## Path to Parity

### Phase 1: Basic LLM Integration (P0)

**Goal**: Matrix users can use natural language like Slack users

**Tasks**:
1. Create `_matrix_chat_with_claude()` function (mirror Slack implementation)
2. Wire up `needs_llm=True` path in matrix_client.py
3. Call Claude API with Matrix user context
4. Return formatted response to Matrix room
5. Handle tool calls (reuse existing 58 MCP tools)

**Estimated Effort**: 4-6 hours  
**Bead**: solutions-27l2 (already exists, P2)

**Acceptance Criteria**:
- ✅ "show my tasks" returns task list (not raw JSON)
- ✅ "create task X" creates task
- ✅ "mark X as done" completes task
- ✅ Natural language queries work in DMs and rooms

---

### Phase 2: Cost Control (P1)

**Goal**: Prevent runaway costs, track usage per Matrix user

**Tasks**:
1. Implement per-user token tracking (Matrix user IDs)
2. Add lifetime budget limits ($1 default)
3. Add usage warnings (80% threshold)
4. Block API calls when budget exhausted
5. Add `/credits` command for Matrix admins

**Estimated Effort**: 3-4 hours  
**New Bead**: Create "Matrix: Add cost control and usage tracking"

**Acceptance Criteria**:
- ✅ Each Matrix user has $1 free credit
- ✅ Token usage tracked per user
- ✅ Warning at 80% usage
- ✅ Hard block at 100% usage
- ✅ Admin can add credits via `!credits @user:domain.com +5`

---

### Phase 3: Advanced Features (P2)

**Goal**: Feature parity with Slack bot

**Tasks**:
1. Add conversation memory (last N messages from room history)
2. Add BYOK support (user can set own API key)
3. Add model selection (Haiku/Sonnet/Opus per user)
4. Add usage stats footer (optional, toggle with `!usage on/off`)
5. Add timezone detection (from Matrix profile or manual set)

**Estimated Effort**: 6-8 hours  
**New Beads**: Create separate beads for each feature

**Acceptance Criteria**:
- ✅ Bot remembers context from previous messages
- ✅ Users can set own API key: `!apikey sk-ant-...`
- ✅ Users can choose model: `!model haiku`
- ✅ Usage stats shown in footer (if enabled)
- ✅ Timezone-aware date parsing

---

## Implementation Strategy

### Option 1: Copy-Paste Slack Implementation (Fast)

**Pros**:
- ✅ Fastest path to parity (1-2 days)
- ✅ Proven code (already working in Slack)
- ✅ Minimal risk

**Cons**:
- ❌ Code duplication
- ❌ Harder to maintain (changes need to be made twice)

**Recommendation**: Use this for Phase 1 (get it working fast)

---

### Option 2: Refactor to Shared LLM Module (Clean)

**Pros**:
- ✅ DRY (don't repeat yourself)
- ✅ Single source of truth for LLM logic
- ✅ Easier to maintain

**Cons**:
- ❌ Slower (need to refactor Slack code too)
- ❌ Risk of breaking Slack bot

**Recommendation**: Do this after Phase 1 works (refactor when stable)

---

### Option 3: Hybrid (Pragmatic)

**Approach**:
1. Copy-paste for Phase 1 (get it working)
2. Refactor in Phase 2 (extract shared module)
3. Both Slack and Matrix use shared `_chat_with_claude()` function

**Pros**:
- ✅ Fast initial delivery
- ✅ Clean long-term architecture
- ✅ Can test refactor without breaking production

**Cons**:
- ❌ Requires two passes (initial + refactor)

**Recommendation**: ✅ **USE THIS APPROACH**

---

## Estimated Timeline

| Phase | Effort | Priority | Blocker |
|-------|--------|----------|---------|
| Phase 1: Basic LLM | 4-6 hours | P0 | None |
| Phase 2: Cost Control | 3-4 hours | P1 | Phase 1 |
| Phase 3: Advanced | 6-8 hours | P2 | Phase 2 |
| Refactor to shared module | 4-6 hours | P2 | Phase 1 |
| **TOTAL** | **17-24 hours** | | |

**Calendar Time**: 2-3 days (with testing)

---

## Current Status

### What's Blocking Parity?

**Technical**: Nothing - code exists in Slack bot, just needs to be ported

**Organizational**: Prioritization - was this intentionally deferred or overlooked?

**Evidence**: 
- solutions-27l2 exists (P2) - "Matrix: Fix natural language response formatting"
- Description mentions "returns raw JSON []"
- This is the LLM integration gap

**Recommendation**: Upgrade solutions-27l2 to P0 or P1, expand scope to full LLM integration

---

## Risk Assessment

### If We Don't Fix This

**User Impact**:
- ❌ Matrix users have worse UX than Slack users
- ❌ Can't use natural language (must memorize commands)
- ❌ Limits adoption ("why doesn't it understand me?")

**Business Impact**:
- ❌ Can't claim "feature parity" in marketing
- ❌ Matrix bot feels like "beta" compared to Slack
- ❌ Harder to migrate Slack users to Matrix

**Technical Debt**:
- ❌ Two different UX patterns (confusing)
- ❌ Harder to maintain (different code paths)

---

## Recommendation

### Immediate Action (This Week)

1. **Upgrade solutions-27l2 to P1**
2. **Expand scope**: "Matrix: Add LLM integration with cost control"
3. **Allocate 1-2 days** for Phase 1 + Phase 2
4. **Test thoroughly** before announcing Matrix bot publicly

### Success Criteria

Matrix bot should be able to handle:
- ✅ "show my tasks due today" → returns task list
- ✅ "create task buy milk" → creates task
- ✅ "mark buy milk as done" → completes task
- ✅ Usage tracking per user
- ✅ Budget limits enforced

---

## Conclusion

**Current State**: Matrix bot is production-ready for **ECO mode** (quick commands), but lacks **LLM integration** for natural language.

**Gap**: ~17-24 hours of work to achieve full parity with Slack bot.

**Recommendation**: Prioritize Phase 1 (basic LLM) and Phase 2 (cost control) before public announcement.

**Timeline**: 2-3 days to full parity.

---

**Next Step**: Review this analysis, decide on priority, and create implementation plan.

