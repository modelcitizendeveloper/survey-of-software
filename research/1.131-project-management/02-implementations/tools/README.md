# Vikunja Task Management Tools

Quick scripts for task-driven development workflow (see `../SOP_VIKUNJA_TASK_WORKFLOW.md`)

---

## Quick Start

```bash
# Activate environment
cd /home/ivanadamin && source .venv/bin/activate

# List current tasks
python3 /home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/tools/vikunja_task_list.py

# Complete tasks
python3 /home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/tools/vikunja_complete_tasks.py 216369 216370
```

---

## Scripts

### `vikunja_task_list.py`

List all tasks in a project.

**Usage**:
```bash
python3 vikunja_task_list.py [project_id]
```

**Default project**: 13456 (Vikunja Integration)

**Output**:
```
================================================================================
VIKUNJA TASKS - Project 13456
================================================================================

📋 Found 6 tasks:

⏳ TODO [216368] Feature: Create vikunja-admin script P5
✅ DONE [216369] Feature: Implement task relations
✅ DONE [216370] Feature: Add kanban buckets

================================================================================
Progress: 2/6 completed (33%)
================================================================================
```

---

### `vikunja_complete_tasks.py`

Mark one or more tasks as complete.

**Usage**:
```bash
python3 vikunja_complete_tasks.py <task_id> [task_id ...]
```

**Example**:
```bash
python3 vikunja_complete_tasks.py 216369 216370
```

**Output**:
```
================================================================================
MARKING TASKS AS COMPLETE
================================================================================

✅ Completed [216369]: Feature: Implement task relations
✅ Completed [216370]: Feature: Add kanban buckets

================================================================================
Marked 2 task(s) as complete
================================================================================
```

---

## Task → Project Lifecycle Tools

These scripts implement the complete lifecycle for the task → project promotion pattern (see `../PATTERN_TASK_TO_PROJECT_PROMOTION.md`).

### `promote_task_to_project.py`

Promote a lightweight task to a full sub-project when commitment increases.

**Usage**:
```bash
python3 promote_task_to_project.py <task_id> --template TEMPLATE [--dry-run]
```

**Templates**: talk, research, product, client, custom

**Example**:
```bash
# See what will happen
python3 promote_task_to_project.py 216450 --template talk --dry-run

# Execute promotion
python3 promote_task_to_project.py 216450 --template talk
```

**What it does**:
1. Creates sub-project (child of main project)
2. Generates template tasks in sub-project
3. Links main task → sub-project
4. Keeps main task in kanban for pipeline tracking

---

### `complete_event.py`

Handle successful event completion with follow-up tasks and next-year reminder.

**Usage**:
```bash
python3 complete_event.py <task_id> [--notes TEXT] [--next-year-date DATE]
```

**Example**:
```bash
python3 complete_event.py 216450 --notes "Great audience, lots of questions"
```

**What it does**:
1. Marks main task DONE ✅
2. Creates 4 follow-up tasks in sub-project:
   - Collect feedback and reviews
   - Capture completion notes
   - Process learnings for next time
   - Share materials and follow-up
3. Creates reminder to pitch again next year

---

### `handle_rejection.py`

Handle proposal rejection with two response paths.

**Usage**:
```bash
python3 handle_rejection.py <task_id> --response {retry|remove} [--retry-date DATE]
```

**Response paths**:
- `retry`: Maybe next time (archives sub-project, creates reminder)
- `remove`: Off the list (deletes sub-project, marks done)

**Examples**:
```bash
# Rejected but will try next year
python3 handle_rejection.py 216450 --response retry --retry-date 2026-11-01

# Not a good fit, don't pursue
python3 handle_rejection.py 216450 --response remove --reason "Topics don't align"
```

---

### `archive_task.py`

Handle abandonment ("never mind" scenario).

**Usage**:
```bash
python3 archive_task.py <task_id> [--reason REASON] [--delete]
```

**Examples**:
```bash
# Archive with reason
python3 archive_task.py 216450 --reason "Event cancelled"

# Permanent deletion (use with caution)
python3 archive_task.py 216450 --delete
```

**What it does**:
- Archives sub-project (or deletes if --delete)
- Marks main task DONE with archival note
- Cleanup for ideas/events that won't be pursued

---

## Kanban Board Tools

### `setup_kanban_board_v2.py`

Create kanban view and buckets for a project.

**Usage**:
```bash
python3 setup_kanban_board_v2.py <project_id> --template TEMPLATE
```

**Templates**: talks, sprint, gtd, custom

**Example**:
```bash
python3 setup_kanban_board_v2.py 13481 --template talks
```

**What it does**:
1. Gets or creates kanban view
2. Creates buckets from template
3. Sets WIP limits where appropriate

**Note**: Uses modern Vikunja API (views-based buckets)

---

### `migrate_talks_to_hybrid.py`

Migrate existing sub-projects to hybrid pattern (one-time migration tool).

**Usage**:
```bash
python3 migrate_talks_to_hybrid.py
```

**What it does**:
- Creates main kanban tasks for existing sub-projects
- Links tasks → sub-projects
- Preserves existing work

---

## Configuration

Scripts use hardcoded token from `/home/ivanadamin/spawn-solutions/.env`:

```bash
VIKUNJA_API_TOKEN=tk_b58cb267d291c55985136b9f054a62e0502e803f
VIKUNJA_BASE_URL=https://app.vikunja.cloud
```

**Project IDs**:
- **13456**: Vikunja Integration (default)

---

## Development Workflow

### Start of Session

```bash
# 1. List tasks to see what needs to be done
python3 vikunja_task_list.py

# 2. Note task IDs you'll work on
# Example: Working on tasks 216368, 216371

# 3. Develop...
```

### End of Session

```bash
# Mark completed tasks
python3 vikunja_complete_tasks.py 216368 216371

# Verify
python3 vikunja_task_list.py
```

---

## Integration with Development

### In Code

Reference task IDs in commits:
```
git commit -m "Add user assignment support (#216370)"
```

### In Scripts

```python
# Task 216369: Implement task relations
def create_task_relation(task_id, relation_kind, other_task_id):
    # Implementation...
```

---

## Troubleshooting

### Import Error

```bash
# Ensure you're in the venv
cd /home/ivanadamin && source .venv/bin/activate

# Or install dependencies
pip install requests python-dateutil
```

### Token Expired

Update token in scripts (search for `VIKUNJA_API_TOKEN`).

### Task Not Found

```bash
# Verify task exists
python3 vikunja_task_list.py 13456
```

---

## Future Enhancements

- [ ] Create task from CLI
- [ ] Assign tasks to users
- [ ] Add labels to tasks
- [ ] Set priorities
- [ ] Create task relations
- [ ] Bulk operations
- [ ] Interactive mode (prompt for task IDs)
- [ ] Git integration (parse task IDs from commits)

---

**See Also**: `../SOP_VIKUNJA_TASK_WORKFLOW.md`
