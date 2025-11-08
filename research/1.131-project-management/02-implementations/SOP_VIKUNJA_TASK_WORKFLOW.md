# SOP: Vikunja Task-Driven Development Workflow

**Version**: 1.0
**Created**: 2025-11-08
**Status**: Active SOP

---

## Purpose

Establish a standard operating procedure where all development efforts **begin and end with Vikunja task management**. This creates a self-reinforcing feedback loop where we dogfood our own project management tools.

---

## Benefits

1. **Immediate Validation** - Test our tools on real work
2. **Continuous Feedback** - Identify integration issues early
3. **Living Documentation** - Tasks reflect actual work done
4. **Progress Tracking** - Real-time visibility into development
5. **Quality Signal** - If we won't use it, why should others?
6. **Accountability** - Clear record of completed work

---

## Workflow

### Phase 1: START - Task Retrieval

**Before starting any development work:**

```bash
# Activate environment
cd /home/ivanadamin && source .venv/bin/activate

# Retrieve current tasks
python3 /home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/tools/vikunja_task_list.py

# Or use the wrapper directly
cd /home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-api-wrapper/src
python3 -c "
from vikunja_wrapper import VikunjaClient
import os

client = VikunjaClient(
    base_url='https://app.vikunja.cloud',
    token='tk_b58cb267d291c55985136b9f054a62e0502e803f'
)

PROJECT_ID = 13456  # Vikunja Integration project
tasks = client.tasks.list(project_id=PROJECT_ID)

print(f'\n📋 Found {len(tasks)} tasks:\n')
for task in tasks:
    status = '✅' if task.done else '⏳'
    priority = f'P{task.priority}' if task.priority > 0 else ''
    print(f'{status} [{task.id}] {task.title} {priority}')
"
```

**Actions**:
1. Review tasks assigned to current work
2. Identify which task(s) you'll be working on
3. Note task IDs for completion later
4. Check for dependencies or blockers

---

### Phase 2: DEVELOP - Implementation

**During development:**

1. Keep task IDs visible (in notes, comments, commit messages)
2. Reference task IDs in code comments where relevant
3. Use task descriptions as acceptance criteria
4. Update task status if needed (set priority, add comments)

**Example commit message**:
```
Add TaskRelationsManager to wrapper API (#216369)

Implements full task relation support (subtask, blocking, related, etc.)
as specified in Vikunja task 216369.

- Created TaskRelationsManager with create/delete/list methods
- Added 13 comprehensive tests with real API validation
- Updated YAML schema with blocked_by and subtask_of fields
```

---

### Phase 3: END - Task Completion

**After completing development work:**

```bash
# Mark tasks as complete
cd /home/ivanadamin && source .venv/bin/activate

# Using wrapper API
python3 -c "
from vikunja_wrapper import VikunjaClient

client = VikunjaClient(
    base_url='https://app.vikunja.cloud',
    token='tk_b58cb267d291c55985136b9f054a62e0502e803f'
)

# Tasks completed in this session
completed_tasks = [
    216369,  # Task relations
    216370,  # Kanban buckets
]

for task_id in completed_tasks:
    task = client.tasks.update(task_id=task_id, done=True)
    print(f'✅ Completed: {task.title}')
"
```

**Verification**:
```bash
# Verify tasks are marked done
# Check project: https://app.vikunja.cloud/projects/13456/47891
```

---

## Project Structure

### Vikunja Projects

- **Project ID: 13456** - "Vikunja Integration"
  - View: https://app.vikunja.cloud/projects/13456/47891
  - Purpose: Tasks related to Vikunja wrapper development
  - Labels: Backend, Frontend, Testing, Documentation

---

## Task Creation Guidelines

### When Creating Tasks

Use the populate script to create structured tasks:

```yaml
project:
  title: "Vikunja Integration"

tasks:
  - title: "Feature: Add X to wrapper"
    description: |
      <strong>Goal:</strong> Brief description<br><br>
      <strong>Scope:</strong><br>
      - Deliverable 1<br>
      - Deliverable 2<br>
      - Deliverable 3<br><br>
      <strong>Acceptance Criteria:</strong><br>
      - [ ] Tests passing<br>
      - [ ] Documentation updated<br>
      - [ ] Examples created
    priority: 5
    labels:
      - "Backend"
```

### Task Naming Convention

- **Feature**: New functionality (e.g., "Feature: Add task relations")
- **Enhancement**: Improve existing feature (e.g., "Enhancement: Expand API coverage")
- **Bug**: Fix broken functionality (e.g., "Bug: Task update fails for bucket_id")
- **Refactor**: Code improvement without new features (e.g., "Refactor: Simplify parsing logic")
- **Documentation**: Docs only (e.g., "Documentation: Add quickstart guide")
- **Testing**: Tests only (e.g., "Testing: Add mutation tests for relations")

---

## Tools

### Quick Scripts

**1. List Tasks** (`tools/vikunja_task_list.py`):
```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/ivanadmin/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-api-wrapper/src')
from vikunja_wrapper import VikunjaClient

client = VikunjaClient(
    base_url='https://app.vikunja.cloud',
    token='tk_b58cb267d291c55985136b9f054a62e0502e803f'
)

tasks = client.tasks.list(project_id=13456)
print(f"\n📋 {len(tasks)} tasks:\n")
for task in tasks:
    status = '✅' if task.done else '⏳'
    print(f"{status} [{task.id}] {task.title}")
```

**2. Complete Tasks** (`tools/vikunja_complete_tasks.py`):
```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/ivanadmin/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-api-wrapper/src')
from vikunja_wrapper import VikunjaClient

client = VikunjaClient(
    base_url='https://app.vikunja.cloud',
    token='tk_b58cb267d291c55985136b9f054a62e0502e803f'
)

task_ids = [int(x) for x in sys.argv[1:]]
for task_id in task_ids:
    task = client.tasks.update(task_id=task_id, done=True)
    print(f"✅ {task.title}")
```

Usage: `python3 vikunja_complete_tasks.py 216369 216370`

---

## Example Session

### Complete Development Session

```bash
# 1. START - Retrieve tasks
cd /home/ivanadamin && source .venv/bin/activate
python3 tools/vikunja_task_list.py

# Output:
# 📋 6 tasks:
# ⏳ [216369] Feature: Implement task relations P5
# ⏳ [216370] Feature: Add kanban buckets P5
# ...

# 2. DEVELOP - Work on tasks 216369, 216370
# (Implementation happens here)

# 3. END - Mark complete
python3 tools/vikunja_complete_tasks.py 216369 216370

# Output:
# ✅ Feature: Implement task relations in Vikunja wrapper and populate script
# ✅ Feature: Add kanban buckets and task assignments to populate script
```

---

## Integration with Git

### Pre-commit Hook (Optional)

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Remind to update Vikunja tasks after commit

echo ""
echo "📋 Remember to mark Vikunja tasks as complete:"
echo "   python3 tools/vikunja_complete_tasks.py <task_id>"
echo ""
```

### Post-session Checklist

After each development session:

- [ ] All implemented features have corresponding tasks
- [ ] Completed tasks are marked as done in Vikunja
- [ ] New work identified is added as tasks
- [ ] Dependencies/blockers are documented
- [ ] Next session tasks are prioritized

---

## Configuration

### Environment Variables

```bash
# .env file (already exists at /home/ivanadamin/spawn-solutions/.env)
VIKUNJA_API_TOKEN=tk_b58cb267d291c55985136b9f054a62e0502e803f
VIKUNJA_BASE_URL=https://app.vikunja.cloud
```

### Project IDs

- **13456**: Vikunja Integration (main development project)

---

## Success Metrics

Track these over time:

1. **Task Completion Rate** - % of tasks marked done after implementation
2. **Task Accuracy** - Do completed tasks match actual work done?
3. **Discovery Rate** - New tasks identified during development
4. **Workflow Efficiency** - Time spent on task management vs. development

**Target**: 100% of development work tracked in Vikunja tasks

---

## Troubleshooting

### Token Expired

```bash
# Get new token from Vikunja UI
# Update .env file
vim /home/ivanadamin/spawn-solutions/.env
```

### Task Not Found

```bash
# Verify project ID
python3 -c "
from vikunja_wrapper import VikunjaClient
client = VikunjaClient(...)
projects = client.projects.list()
for p in projects:
    print(f'{p.id}: {p.title}')
"
```

### API Rate Limits

- Current limit: Unknown (test and document)
- Mitigation: Cache task list, batch updates

---

## Evolution

This SOP should evolve as we learn:

1. **Feedback Loop** - Update based on actual usage
2. **Tool Improvements** - Build better scripts as needs arise
3. **Integration Depth** - Deeper git/IDE integration over time
4. **Automation** - Automate routine task management

---

## References

- **Vikunja Project**: https://app.vikunja.cloud/projects/13456/47891
- **Wrapper Docs**: `vikunja-api-wrapper/src/README.md`
- **Populate Script**: `vikunja-populate-script/src/populate_vikunja.py`
- **Environment Config**: `/home/ivanadamin/spawn-solutions/.env`

---

**Last Updated**: 2025-11-08 (Initial SOP creation)
**Next Review**: After 10 development sessions
