# Task Assignment: Matrix LLM Integration (Claude Code)

**Date**: 2025-12-25
**Epic**: solutions-ndw6 - Matrix LLM Integration
**Purpose**: Extend existing MCP/Slack shared architecture to Matrix

---

## 🎯 Key Discovery: NO REFACTOR NEEDED!

**Initial assumption**: Need to extract LLM code from Slack into shared module
**Reality**: Architecture is ALREADY SHARED via `TOOL_REGISTRY` pattern

### Existing Shared Architecture

```
TOOL_REGISTRY (lines 5228-5900)
├── All _impl functions (create_task, list_tasks, etc.)
├── Used by MCP: @mcp.tool() decorators call _impl functions
└── Used by Slack: _slack_execute_tool() dispatches to TOOL_REGISTRY[name]["impl"]

SLACK_TOOLS (line 7071)
├── Generated from TOOL_REGISTRY
├── Passed to Claude API
└── Executed via _slack_execute_tool()

_slack_chat_with_claude() (line 7847)
├── Handles BYOK, usage limits, conversation memory
├── Calls Claude API with SLACK_TOOLS
└── Executes tools via _slack_execute_tool()
```

**Matrix just needs to follow the same pattern!**

---

## Task Assignments

### 🟢 All Claude Code Tasks (9 tasks)

**Why all Claude Code?**
- ✅ No refactoring needed - just extend existing pattern
- ✅ Clear reference implementation (Slack)
- ✅ Straightforward copy-adapt-test workflow
- ✅ Low risk - not touching production Slack code

#### solutions-ndw6 (Parent Epic)
**Label**: `claude-code`
**Task**: Coordinate Matrix LLM integration

#### solutions-ndw6.1 - Create MATRIX_TOOLS list
**Label**: `claude-code`
**Task**: Copy SLACK_TOOLS pattern, generate from TOOL_REGISTRY
**Complexity**: Low - simple list comprehension

#### solutions-ndw6.2 - Create _matrix_execute_tool() dispatcher
**Label**: `claude-code`
**Task**: Copy _slack_execute_tool() pattern, adapt for Matrix user IDs
**Complexity**: Low - straightforward dispatcher function

#### solutions-ndw6.3 - Create _matrix_chat_with_claude() function
**Label**: `claude-code`
**Task**: Copy _slack_chat_with_claude() pattern (~150 lines), replace Slack-specific parts
**Complexity**: Medium - largest function, but clear reference

#### solutions-ndw6.4 - Wire to matrix_client.py
**Label**: `claude-code`
**Task**: Replace needs_llm fallback with actual LLM call
**Complexity**: Low - simple integration

#### solutions-ndw6.5 - Add Matrix conversation history
**Label**: `claude-code`
**Task**: Copy _fetch_slack_history() pattern, use matrix-nio API
**Complexity**: Low - straightforward API call

#### solutions-ndw6.6 - Add !credits and !apikey commands
**Label**: `claude-code`
**Task**: Add 2 new Matrix commands following existing pattern
**Complexity**: Low - reuse existing functions

#### solutions-ndw6.7 - Test Matrix LLM integration
**Label**: `claude-code`
**Task**: End-to-end testing of Matrix natural language
**Complexity**: Low - testing and validation

#### solutions-ndw6.8 - Verify Slack still works
**Label**: `claude-code`
**Task**: Regression testing
**Complexity**: Low - run existing tests

---

## Workflow Sequence

### Phase 1: Create Matrix Infrastructure (2-3 hours)
```
Claude Code creates Matrix equivalents:
├── solutions-ndw6.1: MATRIX_TOOLS list (copy SLACK_TOOLS pattern)
├── solutions-ndw6.2: _matrix_execute_tool() dispatcher (copy _slack_execute_tool)
└── solutions-ndw6.3: _matrix_chat_with_claude() function (copy _slack_chat_with_claude)
```

**Output**: Matrix has same LLM infrastructure as Slack

---

### Phase 2: Integrate with Matrix Bot (1-2 hours)
```
Claude Code wires everything up:
├── solutions-ndw6.4: Wire to matrix_client.py (replace needs_llm fallback)
└── solutions-ndw6.5: Add conversation history fetching (copy _fetch_slack_history)
```

**Output**: Matrix bot responds to natural language

---

### Phase 3: Add Cost Control Commands (1-2 hours)
```
Claude Code adds Matrix commands:
└── solutions-ndw6.6: !credits and !apikey commands
    ├── Reuse _get_user_anthropic_api_key()
    ├── Reuse _set_user_anthropic_api_key()
    └── Reuse _get_user_credits_info()
```

**Output**: Matrix users can manage API keys and check usage

---

### Phase 4: Test Everything (2-3 hours)
```
Claude Code validates:
├── solutions-ndw6.7: Test Matrix LLM integration
│   ├── Natural language queries
│   ├── Tool execution
│   ├── Usage tracking
│   ├── Budget limits
│   └── BYOK
└── solutions-ndw6.8: Verify Slack still works (regression testing)
```

**Output**: All integration tests pass, both transports working

**Total**: 6-10 hours (all Claude Code)

---

## 🎯 Key Insight: Architecture Already Shared

### TOOL_REGISTRY Pattern (Lines 5228-5900)

**Single source of truth for all Vikunja operations**:
```python
TOOL_REGISTRY = {
    "create_task": {
        "description": "Create a new task",
        "input_schema": {...},
        "impl": _create_task_impl  # ← Shared implementation
    },
    # ... 58 tools total
}
```

**MCP uses it** (via `@mcp.tool()` decorators):
```python
@mcp.tool()
def create_task(...):
    return _create_task_impl(...)  # ← Calls shared impl
```

**Slack uses it** (via dispatcher):
```python
def _slack_execute_tool(name, args, user_id):
    if name not in TOOL_REGISTRY:
        return json.dumps({"error": f"Unknown tool: {name}"})
    return TOOL_REGISTRY[name]["impl"](**args)  # ← Calls shared impl
```

**Matrix just needs to follow the same pattern!**

---

## Why All Claude Code?

### No Refactoring Required

**Initial assumption**: Need to extract LLM code from Slack
**Reality**: Just need to copy Slack patterns for Matrix

**What Matrix needs**:
1. `MATRIX_TOOLS` list (copy `SLACK_TOOLS` pattern)
2. `_matrix_execute_tool()` dispatcher (copy `_slack_execute_tool`)
3. `_matrix_chat_with_claude()` function (copy `_slack_chat_with_claude`)
4. Wire to `matrix_client.py` (replace fallback message)
5. Add conversation history (copy `_fetch_slack_history`)
6. Add !credits and !apikey commands (reuse existing functions)

**All straightforward copy-adapt work** - perfect for Claude Code!

---

## Success Metrics

**When complete**:
- ✅ Matrix bot responds to natural language
- ✅ Tool calls work (via TOOL_REGISTRY)
- ✅ Usage tracking works for Matrix users
- ✅ Budget limits enforced ($1 free, 80% warning, 100% block)
- ✅ BYOK works (users can set own API key)
- ✅ Conversation memory works
- ✅ Slack bot still works (no regressions)
- ✅ All integration tests pass

---

## Timeline

| Phase | Tasks | Estimated |
|-------|-------|-----------|
| 1: Infrastructure | ndw6.1-3 | 2-3 hours |
| 2: Integration | ndw6.4-5 | 1-2 hours |
| 3: Commands | ndw6.6 | 1-2 hours |
| 4: Testing | ndw6.7-8 | 2-3 hours |
| **Total** | **8 tasks** | **6-10 hours** |

**All Claude Code** - no Augment needed!

---

## 🚀 Ready to Start

**All beads tagged**: 9 Claude Code tasks

**Next step**: `solutions-ndw6.1` - Create MATRIX_TOOLS list

**Blocked issue**: `solutions-27l2` (Matrix natural language) will be unblocked when complete

**Estimated completion**: 1-2 days

---

**Status**: Ready for Claude Code implementation

