# Pattern: Task → Project Promotion

**Status**: Implemented and Tested
**Abstraction Level**: Generic (applies to any commitment-based workflow)
**Created**: 2025-11-08

---

## The Pattern

### Problem Statement

How do you manage work that starts **lightweight** (idea, lead, concept) but can become **heavyweight** (serious commitment, detailed execution)?

**Anti-patterns**:
- ❌ Create full project for every idea → overhead, clutter
- ❌ Keep everything as tasks → lose detail when serious
- ❌ Arbitrary thresholds → inconsistent decisions

**Solution**:
✅ **Promote task to sub-project when commitment increases**

---

## Core Concept

```
┌─────────────┐
│ Main Kanban │  ← Pipeline visibility (one task per opportunity)
│  Project    │
└─────────────┘
      │
      │ Promotion trigger:
      │ "I'm serious about this"
      ↓
┌─────────────┐
│ Sub-Project │  ← Implementation details (granular tasks)
└─────────────┘
```

### The Decision Point

**Keep as task when**:
- Exploring / considering
- Low commitment
- May not happen
- Simple tracking sufficient

**Promote to sub-project when**:
- Committing to do it
- Need detailed planning
- Multiple workstreams
- Worth dedicated focus

---

## Generic Workflow

### Phase 1: Lightweight Task (Pipeline Tracking)

```yaml
# Example: Talks kanban
Main Project: "Talks"
Task: "PyCon 2026 - Topic TBD"
Bucket: "💡 Ideas"
```

**Characteristics**:
- Single task in main kanban
- Minimal detail
- Pipeline position visible
- Easy to abandon (just delete)

---

### Phase 2: Promotion Trigger

**When commitment increases**:
```bash
# Automatic promotion
python3 promote_task_to_project.py <task_id> --template <type>
```

**What happens**:
1. Creates sub-project (child of main project)
2. Generates template tasks in sub-project
3. Links main task → sub-project
4. Keeps main task in kanban for tracking
5. Suggests pipeline stage movement

---

### Phase 3: Dual Tracking

```
Main Kanban (pipeline visibility)
├── Task: "PyCon 2026 - Schema Evolution"
│   Bucket: "📝 Proposal Writing"
│   Links to ↓

Sub-Project (detailed work)
├── Research topic
├── Write abstract
├── Submit to CFP
├── Create slides
└── Deliver talk
```

**Main task** = Where in pipeline
**Sub-project** = How to execute

---

### Phase 4: Completion

```bash
# When work is done
1. Mark main task DONE ✅
2. Archive sub-project
3. Event graduates to "completed work"
```

**Completion criteria** is template-specific:
- Talk: Delivered + follow-up done
- Research: Report published
- Product: Launched + stable
- Client: Delivered + invoiced

---

## Domain Applications

### 1. Speaking / Talks

**Pipeline**: Ideas → Proposal → Accepted → Preparing → Delivered

**Promotion trigger**: "I'm going to pitch this"

**Template tasks**:
- Research and outline
- Write abstract
- Submit CFP
- Create slides
- Build demos
- Rehearse
- Deliver
- Follow-up materials

**Completion**: Talk delivered, materials published

---

### 2. Research / Investigation

**Pipeline**: Topics → Active → Analysis → Published

**Promotion trigger**: "This is worth serious investigation"

**Template tasks**:
- Define research question
- Literature review
- Collect data
- Analyze findings
- Synthesize conclusions
- Write report
- Publish

**Completion**: Report published, findings shared

---

### 3. Product Development

**Pipeline**: Backlog → Planning → Building → Launched

**Promotion trigger**: "We're building this"

**Template tasks**:
- Define requirements
- Design architecture
- Create mockups
- Build core features
- Write tests
- User testing
- Launch
- Post-launch monitoring

**Completion**: Launched, stable, handed off

---

### 4. Client Work

**Pipeline**: Leads → Qualified → Proposal → Active → Complete

**Promotion trigger**: "This lead is qualified"

**Template tasks**:
- Discovery call
- Understand requirements
- Write proposal
- Negotiate contract
- Deliver work
- Review/revisions
- Invoice and close

**Completion**: Work delivered, invoiced, closed

---

## Implementation

### Tools Created

**1. Promotion Script** (`promote_task_to_project.py`)
```bash
# See what will happen
python3 promote_task_to_project.py 216450 --template talk --dry-run

# Execute promotion
python3 promote_task_to_project.py 216450 --template talk
```

**Available templates**:
- `talk` - Speaking engagement
- `research` - Research investigation
- `product` - Product development
- `client` - Client engagement
- `custom` - Basic 3-task project

---

### Adding New Templates

Edit `TASK_TEMPLATES` in `promote_task_to_project.py`:

```python
TASK_TEMPLATES = {
    'my_workflow': {
        'description': 'Workflow description',
        'tasks': [
            {"title": "Task 1", "priority": 5},
            {"title": "Task 2", "priority": 3},
            {"title": "Task 3", "priority": 1},
        ],
        'next_stage': {
            'from': 'Current Stage',
            'to': 'Next Stage'
        }
    },
}
```

---

## Benefits

### 1. **Cognitive Clarity**
- ✅ Simple tracking for ideas
- ✅ Detailed planning for serious work
- ✅ Clear commitment signal

### 2. **Reduces Overhead**
- ✅ Don't create projects for every idea
- ✅ Only create detail when needed
- ✅ Easy to abandon early-stage ideas

### 3. **Pipeline Visibility**
- ✅ Main kanban shows ALL opportunities
- ✅ Sub-projects don't clutter view
- ✅ Clear stage progression

### 4. **Completion Clarity**
- ✅ Main task = Event/Project complete
- ✅ Sub-project = Implementation complete
- ✅ Can archive without losing history

### 5. **Scalability**
- ✅ Works for 5 ideas or 50
- ✅ Sub-projects only for serious work
- ✅ Consistent pattern across domains

---

## Anti-Patterns to Avoid

### ❌ Premature Promotion
```
Don't create sub-project for every idea
→ Wait for commitment signal
```

### ❌ Living in Sub-Projects
```
Don't lose pipeline view
→ Keep main task for tracking
```

### ❌ Never Completing
```
Don't let sub-projects become permanent
→ Mark done, archive when complete
```

### ❌ CRM Creep
```
Don't track relationships
→ Only track deliverable events/projects
```

---

## Example: Talks Workflow

### Scenario 1: Early Idea

```
User: "I should speak at PyCon someday"

Action: Create task in "💡 Ideas"
- Task: "PyCon 202X - Topic TBD"
- No sub-project yet
- May never happen
```

---

### Scenario 2: Getting Serious

```
User: "I'm going to pitch schema evolution to PyCascades"

Action: Promote task to sub-project
$ python3 promote_task_to_project.py 216450 --template talk

Result:
- Main task: "PyCascades 2025 - Schema Evolution"
  → Moved to "📝 Proposal Writing"
- Sub-project created with 8 tasks
  → Research, abstract, submit, slides, demos, etc.
```

---

### Scenario 3: Execution

```
User works through sub-project tasks:
✅ Research topic
✅ Write abstract
✅ Submit to CFP
⏳ Create slides (if accepted)
⏳ Build demos
...
```

Main task moves through pipeline:
- "📝 Proposal Writing" → "✅ Accepted" → "🎯 Preparing"

---

### Scenario 4: Completion

```
Talk delivered!

Actions:
1. Complete final sub-project tasks
2. Mark main task DONE ✅
3. Archive sub-project
4. Main task stays in "🎤 Delivered" as history
```

---

## Abstraction Guidelines

### When Creating New Templates

Ask these questions:

1. **What's the pipeline?**
   - What stages does work move through?
   - What's the kanban structure?

2. **What's the promotion trigger?**
   - When does work become "serious"?
   - What signals commitment?

3. **What are the implementation phases?**
   - What tasks are needed to execute?
   - What's the natural sequence?

4. **What defines completion?**
   - When is main task DONE?
   - When can sub-project be archived?

---

## Vikunja Implementation

### Structure

```
Parent Project (Main Kanban)
├── View: Kanban
│   ├── Bucket: Stage 1
│   ├── Bucket: Stage 2
│   ├── Bucket: Stage 3
│   └── Bucket: Complete
│
└── Sub-Project 1 (Child)
    ├── Task: Implementation 1
    ├── Task: Implementation 2
    └── Task: Implementation 3

└── Sub-Project 2 (Child)
    └── ...
```

### Key Properties

**Main Task**:
- Lives in parent project
- Shows in kanban view
- Links to sub-project via description
- Completion = Event complete

**Sub-Project**:
- Child of parent project (`parent_project_id`)
- Contains detailed tasks
- Can have own kanban if needed
- Archived when main task done

---

## Testing the Pattern

### Test Case 1: New Idea

```bash
# Create lightweight task
Task: "OSCON 2026 - Docker for Data Science"
Bucket: "💡 Ideas"

# Wait for commitment signal...
```

### Test Case 2: Promotion

```bash
# Commitment increases
python3 promote_task_to_project.py <task_id> --template talk

# Verify:
✅ Sub-project created
✅ Template tasks populated
✅ Main task linked
✅ Ready to execute
```

### Test Case 3: Execution

```bash
# Work through sub-project tasks
# Move main task through pipeline
# Track progress in both views
```

### Test Case 4: Completion

```bash
# Mark main task DONE
# Archive sub-project
# Verify history preserved
```

---

## Lifecycle Management

The promotion pattern is complete with lifecycle outcome handlers:

### Success ✅ - `complete_event.py`
**When**: Event/project delivered successfully

**What it does**:
- Marks main task DONE
- Creates 4 follow-up tasks (feedback, notes, learnings, sharing)
- Sets next-year reminder

**Usage**:
```bash
python3 complete_event.py <task_id> --notes "Completion notes"
```

### Rejection ❌ - `handle_rejection.py`
**When**: Proposal/pitch rejected

**Two paths**:
- `--response retry`: Maybe next time (archive, set reminder)
- `--response remove`: Off the list (delete, don't pursue)

**Usage**:
```bash
# Retry next year
python3 handle_rejection.py <task_id> --response retry --retry-date 2026-11-01

# Don't pursue
python3 handle_rejection.py <task_id> --response remove --reason "Bad fit"
```

### Abandonment 🗃️ - `archive_task.py`
**When**: "Never mind" - decided not to pursue

**Usage**:
```bash
python3 archive_task.py <task_id> --reason "Priorities changed"
```

**See**: `LIFECYCLE_COMPLETE_PATTERN.md` for full lifecycle documentation

---

## Future Enhancements

### Potential Additions

1. **Reverse Promotion** (Project → Task)
   - When you realize it's simpler than expected
   - Collapse sub-project back to task

2. **Automatic Stage Movement**
   - Promotion auto-moves main task
   - Based on template's `next_stage`

3. **Progress Rollup**
   - Show sub-project completion % on main task
   - Automatic status updates

4. **Template Marketplace**
   - Community-contributed templates
   - Domain-specific workflows

5. **Analytics Dashboard**
   - Success/rejection rates
   - Time from idea to delivery
   - Follow-up completion tracking

---

## Related Patterns

### Complementary Patterns

**This pattern** (Task → Project):
- Manages commitment escalation
- Lightweight → Heavyweight
- Pipeline + Detail

**Kanban buckets**:
- Manages stage progression
- Visual workflow
- WIP limits

**Task relations**:
- Manages dependencies
- Blocking relationships
- Subtask hierarchies

### Pattern Composition

```
Task → Project Promotion
  ↓
Sub-project with Kanban
  ↓
Tasks with Relations
  ↓
Granular execution
```

---

## References

- **Implementation**: `tools/promote_task_to_project.py`
- **Talks Example**: Project 13481 (Talks)
- **Migration**: `tools/migrate_talks_to_hybrid.py`
- **Kanban Setup**: `tools/setup_kanban_board_v2.py`

---

## Summary

**The Pattern**: Task → Sub-Project when commitment increases

**Key Principle**: Match tool weight to commitment level

**Benefits**:
- ✅ Cognitive clarity
- ✅ Reduced overhead
- ✅ Pipeline visibility
- ✅ Completion clarity
- ✅ Scalable

**Applications**: Any commitment-based workflow (talks, research, products, clients, etc.)

**Abstraction**: Generic, reusable, template-driven

---

**Created**: 2025-11-08
**Status**: Production-ready
**Applies to**: All commitment-based workflows
