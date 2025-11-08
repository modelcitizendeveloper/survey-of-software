# Complete Lifecycle Pattern: Task → Project → Outcome

**Status**: Implemented and Tested
**Created**: 2025-11-08
**Abstraction Level**: Generic (applies to any commitment-based workflow)

---

## Overview

This document describes the **complete lifecycle** for managing work that starts lightweight but can become heavyweight, from initial idea through final outcome.

**Full Pattern**:
```
Idea (task)
  ↓
Commitment increases → PROMOTE to sub-project
  ↓
Work on sub-project tasks
  ↓
Outcome → COMPLETE | REJECT | ABANDON
  ↓
Archive and learn
```

---

## Phase 1: Lightweight Tracking (Task)

**Tool**: Kanban task in main project

**When to use**:
- Exploring / considering
- Low commitment
- May not happen
- Simple tracking sufficient

**Example**:
```yaml
Project: Talks
Task: "PyCon 2026 - Topic TBD"
Bucket: "💡 Ideas"
```

**Characteristics**:
- Single task in kanban
- Minimal detail
- Easy to abandon (just delete)
- Pipeline position visible

---

## Phase 2: Promotion (Commitment Increases)

**Tool**: `promote_task_to_project.py`

**Trigger**: "I'm serious about this"

**When to promote**:
- Committing to do it
- Need detailed planning
- Multiple workstreams
- Worth dedicated focus

**How to promote**:
```bash
# See plan
python3 promote_task_to_project.py 216450 --template talk --dry-run

# Execute
python3 promote_task_to_project.py 216450 --template talk
```

**What happens**:
1. Creates sub-project (child of main project)
2. Generates template tasks in sub-project
3. Links main task → sub-project
4. Main task stays in kanban for tracking
5. Suggests moving to next pipeline stage

**Templates available**:
- `talk`: Speaking engagement (8 tasks)
- `research`: Research investigation (7 tasks)
- `product`: Product development (8 tasks)
- `client`: Client engagement (7 tasks)
- `custom`: Basic project (3 tasks)

**Result**:
```
Main Kanban (pipeline tracking)
├── Task: "PyCon 2026 - Schema Evolution"
│   Bucket: "📝 Proposal Writing"
│   Links to ↓

Sub-Project (detailed work)
├── Research topic and outline
├── Write abstract and proposal
├── Submit to CFP
├── Create slide deck
├── Build demos/examples
├── Rehearse presentation
├── Deliver talk
└── Create follow-up materials
```

---

## Phase 3: Execution

**Work in sub-project**:
- Complete template tasks
- Move main task through pipeline stages
- Track progress in kanban

**Pipeline stages** (talks example):
```
💡 Ideas
  ↓
📝 Proposal Writing  ← After promotion
  ↓
✅ Accepted          ← After acceptance
  ↓
🎯 Preparing         ← Building slides/demos
  ↓
🎤 Delivered         ← After delivery
```

**Main task** = Where in pipeline
**Sub-project** = How to execute

---

## Phase 4: Outcome

Three possible outcomes:

### Outcome A: Success ✅

**Tool**: `complete_event.py`

**When**: Event delivered successfully

**Usage**:
```bash
python3 complete_event.py 216450 --notes "Great audience, lots of questions"
```

**What happens**:
1. Marks main task DONE ✅
2. Creates 4 follow-up tasks in sub-project:
   - **Collect feedback and reviews**
     - Event platform ratings/reviews
     - Social media comments
     - Direct attendee feedback
     - Organizer feedback
   - **Capture completion notes**
     - What went well
     - What could be improved
     - Key takeaways
     - Interesting questions/interactions
     - Rating (1-5)
   - **Process learnings for next time**
     - Update materials based on feedback
     - Identify topics that resonated
     - Note timing adjustments
     - Update proposal template
   - **Share materials and follow-up**
     - Upload slides
     - Publish demo code
     - Share recording
     - Post thank-you
     - Connect with contacts

3. Creates next-year reminder (default: +1 year)

**Next steps**:
1. Complete follow-up tasks
2. Archive sub-project when follow-up done
3. Wait for next-year reminder

---

### Outcome B: Rejection ❌

**Tool**: `handle_rejection.py`

**When**: Proposal rejected / they said no

**Two response paths**:

#### Path 1: Retry (Maybe Next Time)

**Usage**:
```bash
python3 handle_rejection.py 216450 --response retry --retry-date 2026-11-01
```

**When to use**:
- Timing was wrong
- Topic didn't fit this year
- Competition was strong
- May work next time

**What happens**:
1. Archives sub-project (preserves work)
2. Updates main task with rejection note
3. Creates reminder to try again (with date)
4. Keeps opportunity alive

**Characteristics**:
- ✅ Work preserved for next attempt
- ✅ Automatic reminder to re-pitch
- ✅ Pipeline stays clean
- ✅ Future opportunity maintained

#### Path 2: Remove (Off the List)

**Usage**:
```bash
python3 handle_rejection.py 216450 --response remove --reason "Topics don't align"
```

**When to use**:
- Not a good venue fit
- Won't accept your topics
- Bad experience with organizers
- Should not pursue again

**What happens**:
1. Deletes sub-project and all tasks
2. Marks main task DONE with "do not pursue" note
3. Documents reason
4. Removed from pipeline

**Characteristics**:
- ✅ Clean removal
- ✅ Clear "do not pursue" signal
- ✅ Reason documented
- ✅ No reminder created

---

### Outcome C: Abandonment 🗃️

**Tool**: `archive_task.py`

**When**: "Never mind" - decided not to pursue

**Usage**:
```bash
# Archive with reason (recommended)
python3 archive_task.py 216450 --reason "Event cancelled"

# Permanent deletion (use with caution)
python3 archive_task.py 216450 --delete
```

**When to use**:
- Event cancelled by organizer
- No longer interested
- Priorities changed
- Opportunity passed
- Cleanup needed

**What happens** (archive mode):
1. Archives sub-project
2. Marks main task DONE with archival note
3. Documents reason
4. Cleanup complete

**What happens** (delete mode):
1. Permanently deletes sub-project
2. Permanently deletes main task
3. Complete removal
4. ⚠️ Cannot be undone

**Characteristics**:
- ✅ Clean pipeline
- ✅ Reason preserved (archive mode)
- ✅ History maintained (archive mode)
- ⚠️ Permanent (delete mode)

---

## Complete Lifecycle Flowchart

```
┌─────────────────┐
│  New Idea       │
│  (Lightweight)  │
└────────┬────────┘
         │
         │ "I'm interested"
         ↓
┌─────────────────┐
│  Task in Kanban │
│  "💡 Ideas"     │
└────────┬────────┘
         │
         ├─→ "Never mind" ───────→ ARCHIVE_TASK ──→ 🗃️ Archived
         │
         │ "I'm serious about this"
         ↓
┌─────────────────┐
│  PROMOTE        │ ← promote_task_to_project.py
│  to Sub-Project │
└────────┬────────┘
         │
         │ Creates:
         │ - Sub-project
         │ - Template tasks
         │ - Links
         ↓
┌─────────────────┐
│  Work on Tasks  │
│  Track Progress │
└────────┬────────┘
         │
         │ Move through pipeline:
         │ Ideas → Proposal → Accepted → Preparing → Delivered
         │
         ├─→ "Never mind" ───────→ ARCHIVE_TASK ──→ 🗃️ Archived
         │
         │ Submit/Pitch
         ↓
┌─────────────────┐
│  Outcome        │
└────────┬────────┘
         │
         ├─→ ACCEPTED ──→ Continue work
         │                     │
         │                     ↓
         │              ┌─────────────────┐
         │              │  Deliver Event  │
         │              └────────┬────────┘
         │                       │
         │                       ↓
         │              ┌─────────────────┐
         │              │  COMPLETE_EVENT │ ← complete_event.py
         │              └────────┬────────┘
         │                       │
         │                       ├─→ Create follow-up tasks
         │                       ├─→ Mark main task DONE ✅
         │                       ├─→ Create next-year reminder
         │                       └─→ Keep sub-project for follow-up
         │                           │
         │                           ↓
         │                    Complete follow-up → Archive
         │
         └─→ REJECTED ──┬─→ "Maybe next time" ──→ HANDLE_REJECTION (retry)
                        │                           ├─→ Archive sub-project
                        │                           ├─→ Create reminder
                        │                           └─→ Try again next year
                        │
                        └─→ "Off the list" ────→ HANDLE_REJECTION (remove)
                                                    ├─→ Delete sub-project
                                                    └─→ Mark DONE (do not pursue)
```

---

## Tools Summary

| Tool | Purpose | When | Main Actions |
|------|---------|------|--------------|
| **promote_task_to_project.py** | Promote task → sub-project | Commitment increases | Create sub-project, template tasks, links |
| **complete_event.py** | Handle success | Event delivered | Mark DONE, create follow-up tasks, set reminder |
| **handle_rejection.py** (retry) | Handle rejection, maybe later | "Try again next time" | Archive sub-project, create reminder |
| **handle_rejection.py** (remove) | Handle rejection, final | "Off the list" | Delete sub-project, mark do-not-pursue |
| **archive_task.py** | Handle abandonment | "Never mind" | Archive/delete, clean up pipeline |

---

## Domain Examples

### Speaking / Talks

**Lifecycle**:
```
Idea → Promotion (CFP opens) → Submit → Rejected/Accepted
  ↓
If Accepted: Prepare → Deliver → Complete (follow-up + reminder)
If Rejected: Retry (next year) or Remove (bad fit)
If Never Mind: Archive (not interested / cancelled)
```

**Complete flow**:
1. Create task: "PyCon 2026 - Topic TBD" in Ideas
2. Commit: `promote_task_to_project.py --template talk`
3. Work through: Research → Abstract → Submit
4. Outcome:
   - ✅ Accepted → Slides → Deliver → `complete_event.py`
   - ❌ Rejected (retry) → `handle_rejection.py --response retry`
   - ❌ Rejected (final) → `handle_rejection.py --response remove`
   - 🗃️ Lost interest → `archive_task.py`

---

### Research / Investigation

**Lifecycle**:
```
Topic → Promotion (worth deep dive) → Investigate → Publish/Abandon
  ↓
If Published: Complete (document learnings)
If Not Worth It: Archive
```

**Complete flow**:
1. Create task: "Investigate GraphQL federation" in Topics
2. Commit: `promote_task_to_project.py --template research`
3. Work through: Define question → Literature review → Analyze
4. Outcome:
   - ✅ Published → `complete_event.py` (creates "share findings" tasks)
   - 🗃️ Not worth it → `archive_task.py --reason "Already solved"`

---

### Product Development

**Lifecycle**:
```
Backlog → Promotion (building this) → Build → Launch/Cancel
  ↓
If Launched: Complete (post-launch monitoring)
If Cancelled: Archive
```

**Complete flow**:
1. Create task: "Build user dashboard" in Backlog
2. Commit: `promote_task_to_project.py --template product`
3. Work through: Requirements → Design → Build → Test
4. Outcome:
   - ✅ Launched → `complete_event.py` (creates monitoring tasks)
   - 🗃️ Deprioritized → `archive_task.py --reason "Replaced by v2 approach"`

---

### Client Work

**Lifecycle**:
```
Lead → Promotion (qualified) → Proposal → Won/Lost
  ↓
If Won: Deliver → Invoice → Complete
If Lost: Retry (maybe next time) or Remove (bad fit)
```

**Complete flow**:
1. Create task: "ACME Corp - CRM migration" in Leads
2. Qualify: `promote_task_to_project.py --template client`
3. Work through: Discovery → Proposal → Negotiate
4. Outcome:
   - ✅ Won → Deliver → Invoice → `complete_event.py`
   - ❌ Lost (timing) → `handle_rejection.py --response retry`
   - ❌ Lost (bad fit) → `handle_rejection.py --response remove`
   - 🗃️ Unqualified → `archive_task.py --reason "Budget too small"`

---

## Benefits of Complete Lifecycle

### 1. Cognitive Clarity
- ✅ Clear decision points
- ✅ Explicit commitment signals
- ✅ Structured outcomes
- ✅ Consistent handling

### 2. Knowledge Capture
- ✅ Follow-up tasks ensure learning
- ✅ Feedback systematically collected
- ✅ Notes captured while fresh
- ✅ Patterns emerge over time

### 3. Future Planning
- ✅ Automatic reminders for retry
- ✅ "Do not pursue" signals respected
- ✅ Next-year pitches don't get forgotten
- ✅ Historical context preserved

### 4. Clean Pipeline
- ✅ Completed work archived
- ✅ Rejected opportunities handled
- ✅ Abandoned ideas cleaned up
- ✅ Active work visible

### 5. Scalability
- ✅ Works for 5 events or 50
- ✅ Template-driven (add domains easily)
- ✅ Automated where possible
- ✅ Consistent across domains

---

## Anti-Patterns to Avoid

### ❌ Never Closing the Loop
**Problem**: Event delivered but no follow-up, feedback lost
**Solution**: Use `complete_event.py` to create structured follow-up

### ❌ Forgetting to Re-Pitch
**Problem**: Rejected proposal, never try again despite good fit
**Solution**: Use `handle_rejection.py --response retry` with date

### ❌ Cluttered Pipeline
**Problem**: Old ideas still visible, can't see active work
**Solution**: Use `archive_task.py` to clean up abandoned ideas

### ❌ Pursuing Bad Fits
**Problem**: Keep pitching to venues that don't want your topics
**Solution**: Use `handle_rejection.py --response remove` to mark "do not pursue"

### ❌ Premature Deletion
**Problem**: Delete work that could be reused
**Solution**: Use archive mode instead of delete (preserve history)

---

## Script Reference

### Quick Command Guide

```bash
# 1. Promote task to sub-project
python3 promote_task_to_project.py <task_id> --template {talk|research|product|client|custom}

# 2a. Complete successfully
python3 complete_event.py <task_id> --notes "Event notes"

# 2b. Rejected - try again
python3 handle_rejection.py <task_id> --response retry --retry-date YYYY-MM-DD

# 2c. Rejected - don't pursue
python3 handle_rejection.py <task_id> --response remove --reason "Why"

# 2d. Abandoned
python3 archive_task.py <task_id> --reason "Why"

# All scripts support --dry-run to preview changes
```

### Location

All scripts in:
```
/home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/tools/
```

### Environment

```bash
cd /home/ivanadamin && source .venv/bin/activate
```

---

## Future Enhancements

### Potential Additions

1. **Analytics Dashboard**
   - Success/rejection rates by venue
   - Time from idea to delivery
   - Follow-up completion rates
   - Pitch-again reminder adherence

2. **Automatic Stage Movement**
   - Promotion auto-moves task to next stage
   - Completion auto-moves to "Delivered"
   - Rejection auto-moves to "Ideas" (retry) or "Done" (remove)

3. **Template Marketplace**
   - Community-contributed templates
   - Domain-specific workflows
   - Best practices sharing

4. **Rollup Progress**
   - Show sub-project completion % on main task
   - Automatic status updates
   - Blocked/at-risk detection

5. **Reverse Promotion**
   - Project → Task when simpler than expected
   - Collapse sub-project back to task

---

## Related Patterns

### Complementary Patterns

- **Kanban buckets**: Manages stage progression
- **Task relations**: Manages dependencies within sub-projects
- **Labels**: Categorizes across projects (GTD contexts, etc.)
- **Due dates**: Time-based tracking for deadlines
- **Assignments**: Delegates work in collaborative environments

### Pattern Composition

```
Task → Project Promotion (this pattern)
  ↓
Sub-project with Kanban buckets
  ↓
Tasks with Relations (blocking, subtasks)
  ↓
Granular execution
  ↓
Outcome handling (complete/reject/abandon)
  ↓
Learning capture → Next iteration
```

---

## Summary

**The Complete Pattern**: Task → Promote → Execute → Outcome → Learn

**Key Principles**:
1. Match tool weight to commitment level
2. Structured outcomes (complete/reject/abandon)
3. Systematic learning capture
4. Future planning built-in
5. Clean pipeline maintained

**Benefits**:
- ✅ Cognitive clarity throughout lifecycle
- ✅ Knowledge systematically captured
- ✅ Future opportunities managed
- ✅ Clean and scalable
- ✅ Consistent across domains

**Applications**: Any commitment-based workflow where work starts lightweight but can become heavyweight

**Abstraction**: Generic, reusable, template-driven lifecycle management

---

**Created**: 2025-11-08
**Status**: Production-ready
**Applies to**: All commitment-based workflows
**Scripts**: 5 lifecycle management tools
**Templates**: 5 domain templates (talk, research, product, client, custom)
