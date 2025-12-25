# Critical Path: Matrix LLM Integration

**Epic**: solutions-ndw6  
**Goal**: Matrix bot responds to natural language (achieve Slack parity)  
**Blocker for**: solutions-27l2 (Matrix natural language returns raw JSON)

---

## 🎯 Critical Path (Minimum Viable)

### Must-Have for Natural Language to Work

```
solutions-ndw6.1 → ndw6.2 → ndw6.3 → ndw6.4
```

**Sequential dependencies**:

1. **solutions-ndw6.1** - Create MATRIX_TOOLS list (30 min)
   - Generate from TOOL_REGISTRY
   - Needed by: ndw6.3 (passed to Claude API)

2. **solutions-ndw6.2** - Create _matrix_execute_tool() dispatcher (45 min)
   - Dispatch tool calls to TOOL_REGISTRY
   - Needed by: ndw6.3 (executes tools during LLM loop)

3. **solutions-ndw6.3** - Create _matrix_chat_with_claude() function (2-3 hours)
   - Core LLM integration (BYOK, usage limits, Claude API, tool loop)
   - Needed by: ndw6.4 (called from matrix_client.py)

4. **solutions-ndw6.4** - Wire to matrix_client.py (30 min)
   - Replace needs_llm fallback with actual LLM call
   - **UNBLOCKS**: Matrix natural language works!

**Critical path total**: 4-5 hours

---

## 🔧 Nice-to-Have (Can Be Done Later)

### Parallel/Post-MVP Tasks

**solutions-ndw6.5** - Add conversation history (1-2 hours)
- **Can start**: After ndw6.3 exists (add to _matrix_chat_with_claude)
- **Dependency**: None (enhances ndw6.3 but not required for basic LLM)
- **Impact**: Better context for multi-turn conversations

**solutions-ndw6.6** - Add !credits and !apikey commands (1-2 hours)
- **Can start**: Anytime (independent of LLM integration)
- **Dependency**: None (uses existing functions from server.py)
- **Impact**: Users can manage API keys and check usage

**solutions-ndw6.7** - Test Matrix LLM integration (1-2 hours)
- **Can start**: After ndw6.4 complete
- **Dependency**: ndw6.1-4 (tests the critical path)
- **Impact**: Validation and confidence

**solutions-ndw6.8** - Verify Slack still works (1 hour)
- **Can start**: Anytime (regression testing)
- **Dependency**: None (tests existing Slack code)
- **Impact**: Ensure no regressions

---

## 📊 Dependency Graph

```
ndw6.1 (MATRIX_TOOLS)
  ↓
ndw6.2 (_matrix_execute_tool)
  ↓
ndw6.3 (_matrix_chat_with_claude) ← ndw6.5 (history) can enhance this
  ↓
ndw6.4 (wire to matrix_client.py)
  ↓
ndw6.7 (test Matrix)

ndw6.6 (!credits, !apikey) ← Independent, can do anytime
ndw6.8 (test Slack) ← Independent, can do anytime
```

---

## ⚡ Fast-Track Strategy

### Option 1: MVP First (4-5 hours)
```
1. Do ndw6.1-4 sequentially (critical path)
2. Test manually (send natural language message)
3. Ship it! ✅ Matrix natural language works
4. Do ndw6.5-8 later (enhancements + testing)
```

**Pros**: Unblocks solutions-27l2 fastest  
**Cons**: No conversation memory, no cost control commands yet

---

### Option 2: Full Feature (6-8 hours)
```
1. Do ndw6.1-4 sequentially (critical path)
2. Add ndw6.5 (conversation history)
3. Add ndw6.6 (!credits, !apikey) in parallel
4. Test with ndw6.7-8
```

**Pros**: Complete feature parity with Slack  
**Cons**: Takes 2 hours longer

---

### Option 3: Parallel Work (4-6 hours with 2 people)
```
Person A (critical path):
├── ndw6.1 → ndw6.2 → ndw6.3 → ndw6.4

Person B (enhancements):
├── ndw6.6 (!credits, !apikey)
└── ndw6.8 (test Slack)

Then together:
├── ndw6.5 (add history to ndw6.3)
└── ndw6.7 (test Matrix)
```

**Pros**: Fastest overall (4-6 hours)  
**Cons**: Requires coordination

---

## 🚦 Recommended: Option 1 (MVP First)

**Why**:
- ✅ Fastest path to unblock solutions-27l2
- ✅ Can test immediately after ndw6.4
- ✅ Low risk (minimal changes)
- ✅ Can add enhancements incrementally

**Sequence**:
1. **Now**: ndw6.1 (30 min) - Create MATRIX_TOOLS
2. **Next**: ndw6.2 (45 min) - Create dispatcher
3. **Then**: ndw6.3 (2-3 hours) - Create _matrix_chat_with_claude
4. **Finally**: ndw6.4 (30 min) - Wire to matrix_client.py
5. **Test**: Send "show my tasks" in Matrix DM
6. **Ship**: ✅ Matrix natural language works!
7. **Later**: Add ndw6.5-8 (enhancements + proper testing)

**Total time to working natural language**: 4-5 hours

---

## 🎯 Success Criteria (MVP)

**After ndw6.1-4 complete**:
- ✅ Matrix bot responds to "show my tasks"
- ✅ Tool calls work (creates tasks, lists projects, etc.)
- ✅ Usage tracking increments
- ✅ Budget limits enforced (if user hits $1 limit)
- ✅ BYOK works (if user sets API key)

**What's missing** (can add later):
- ⏳ Conversation memory (ndw6.5)
- ⏳ !credits command (ndw6.6)
- ⏳ !apikey command (ndw6.6)
- ⏳ Comprehensive tests (ndw6.7-8)

---

## 📝 Critical Path Summary

**Minimum to unblock Matrix natural language**: ndw6.1 → ndw6.2 → ndw6.3 → ndw6.4

**Time**: 4-5 hours

**Next step**: Start with solutions-ndw6.1 (Create MATRIX_TOOLS list)

**Blocker removed**: solutions-27l2 can be closed after ndw6.4 complete

