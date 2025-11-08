# Task → Project Lifecycle - Quick Reference

**One-page command reference for complete lifecycle management**

---

## 📍 Environment Setup

```bash
cd /home/ivanadamin && source .venv/bin/activate
cd /home/ivanadmin/spawn-solutions/research/1.131-project-management/02-implementations/tools
```

---

## 🚀 Phase 1: Promotion (Task → Sub-Project)

**When**: "I'm serious about this" - commitment increases

**Templates**: talk | research | product | client | custom

```bash
# Preview
python3 promote_task_to_project.py <task_id> --template talk --dry-run

# Execute
python3 promote_task_to_project.py <task_id> --template talk
```

**Creates**: Sub-project + template tasks + links

---

## ✅ Outcome 1: Success (Event Delivered)

**When**: Successfully completed and delivered

```bash
# With notes
python3 complete_event.py <task_id> --notes "Great audience, lots of questions"

# Custom next-year date
python3 complete_event.py <task_id> --next-year-date 2026-11-15

# Preview
python3 complete_event.py <task_id> --dry-run
```

**Creates**:
- Follow-up tasks (feedback, notes, learnings, sharing)
- Next-year reminder

---

## ❌ Outcome 2: Rejection (They Said No)

**When**: Proposal/pitch rejected

### Path A: Try Again Next Time

```bash
# With retry date
python3 handle_rejection.py <task_id> --response retry --retry-date 2026-11-01

# Default: +1 year
python3 handle_rejection.py <task_id> --response retry
```

**Does**: Archive sub-project + create reminder

### Path B: Don't Pursue

```bash
# Off the list
python3 handle_rejection.py <task_id> --response remove --reason "Topics don't align"
```

**Does**: Delete sub-project + mark "do not pursue"

---

## 🗃️ Outcome 3: Abandonment (Never Mind)

**When**: Decided not to pursue

### Archive Mode (Recommended)

```bash
# Archive with reason
python3 archive_task.py <task_id> --reason "Event cancelled"

# Preview
python3 archive_task.py <task_id> --dry-run
```

**Does**: Archive sub-project + mark DONE

### Delete Mode (Permanent)

```bash
# CAUTION: Cannot be undone!
python3 archive_task.py <task_id> --delete --reason "Duplicate"
```

**Does**: Permanently delete everything

---

## 🎯 Decision Tree

```
Is the idea serious?
├─ NO → Keep as task in Ideas
└─ YES → promote_task_to_project.py
          │
          Work on sub-project...
          │
          What's the outcome?
          ├─ SUCCESS → complete_event.py
          ├─ REJECTED
          │   ├─ Try again → handle_rejection.py --response retry
          │   └─ Bad fit → handle_rejection.py --response remove
          └─ ABANDONED → archive_task.py
```

---

## 📊 Setup Kanban Board

**First time setup** for a project:

```bash
# Create kanban view + buckets
python3 setup_kanban_board_v2.py <project_id> --template talks

# Templates: talks | sprint | gtd | custom
```

---

## 🔍 Common Scenarios

### Scenario 1: New Speaking Opportunity
```bash
# 1. Create task in Ideas bucket manually
# 2. When ready to pitch:
python3 promote_task_to_project.py 216450 --template talk
# 3. Work through sub-project tasks
# 4. After delivery:
python3 complete_event.py 216450 --notes "Went great!"
```

### Scenario 2: Proposal Rejected, Will Try Again
```bash
python3 handle_rejection.py 216450 --response retry --retry-date 2026-11-01
```

### Scenario 3: Bad Venue Fit, Don't Pitch Again
```bash
python3 handle_rejection.py 216450 --response remove --reason "Audience doesn't match"
```

### Scenario 4: Lost Interest in Topic
```bash
python3 archive_task.py 216450 --reason "Priorities shifted to different area"
```

### Scenario 5: Event Cancelled by Organizer
```bash
python3 archive_task.py 216450 --reason "Event cancelled"
```

---

## 🛠️ All Commands at a Glance

| Command | Purpose | Key Options |
|---------|---------|-------------|
| `promote_task_to_project.py` | Promote to sub-project | `--template {talk\|research\|product\|client\|custom}` |
| `complete_event.py` | Success + follow-up | `--notes TEXT --next-year-date DATE` |
| `handle_rejection.py` | Rejection handling | `--response {retry\|remove} --retry-date DATE` |
| `archive_task.py` | Abandonment | `--reason TEXT --delete` |
| `setup_kanban_board_v2.py` | Create kanban board | `--template {talks\|sprint\|gtd\|custom}` |

**All scripts support**: `--dry-run` to preview changes

---

## 📚 Full Documentation

- **Complete Pattern**: `LIFECYCLE_COMPLETE_PATTERN.md`
- **Promotion Pattern**: `PATTERN_TASK_TO_PROJECT_PROMOTION.md`
- **Tools README**: `tools/README.md`
- **SOP Workflow**: `SOP_VIKUNJA_TASK_WORKFLOW.md`

---

## 🔑 Key Principles

1. **Match weight to commitment**: Lightweight task → Heavyweight sub-project only when serious
2. **Structured outcomes**: Every promotion has clear end state (complete/reject/abandon)
3. **Learning capture**: Success creates follow-up tasks to extract lessons
4. **Future planning**: Automatic reminders for retry/next-year pitches
5. **Clean pipeline**: Completed/rejected/abandoned work properly archived

---

## ⚠️ Common Pitfalls

- ❌ **Premature promotion**: Don't create sub-project for every idea
- ❌ **Forgetting follow-up**: Use `complete_event.py` to capture learnings
- ❌ **Cluttered pipeline**: Archive abandoned ideas with `archive_task.py`
- ❌ **Losing opportunities**: Rejected? Use `--response retry` to try again
- ❌ **Pursuing bad fits**: Use `--response remove` to mark "do not pursue"

---

## 💡 Tips

- Always use `--dry-run` first to preview changes
- Document `--reason` for better future context
- Use `--notes` on completion to capture while fresh
- Set specific `--retry-date` based on CFP timeline
- Archive (not delete) to preserve history

---

**Created**: 2025-11-08
**Status**: Production-ready
**Location**: `/home/ivanadmin/spawn-solutions/research/1.131-project-management/02-implementations/tools/`
