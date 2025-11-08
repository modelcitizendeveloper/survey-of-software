# Vikunja Task Workflow - Quick Reference

**One-page guide for task-driven development**

---

## 🚀 Quick Start

### In Any Claude Code Session

```
/vikunja-tasks
```

Claude will automatically:
1. List current tasks
2. Guide you through workflow
3. Remind you to mark tasks complete

---

## 📋 Manual Commands

### List Tasks
```bash
cd ~/spawn-solutions && source ~/.venv/bin/activate
python3 research/1.131-project-management/02-implementations/tools/vikunja_task_list.py
```

### Complete Tasks
```bash
cd ~/spawn-solutions && source ~/.venv/bin/activate
python3 research/1.131-project-management/02-implementations/tools/vikunja_complete_tasks.py <task_id> <task_id>
```

---

## 🔄 The 3-Phase Workflow

```
START → List tasks, note IDs
  ↓
DEVELOP → Implement features
  ↓
END → Mark tasks complete
```

---

## 🎯 Project IDs

- **13456** - Vikunja Integration (main)
- https://app.vikunja.cloud/projects/13456/47891

---

## 💡 Example Session

```bash
# START
python3 .../vikunja_task_list.py
# See: Task #216401 - JWT authentication

# DEVELOP
# (implement the feature)

# END
python3 .../vikunja_complete_tasks.py 216401
# ✅ Task complete!
```

---

## 🔧 Wrapper API (Python)

```python
import sys
sys.path.insert(0, '.../vikunja-api-wrapper/src')
from vikunja_wrapper import VikunjaClient

client = VikunjaClient(
    base_url='https://app.vikunja.cloud',
    token='tk_...'  # from .env
)

# List tasks
tasks = client.tasks.list(project_id=13456)

# Complete task
client.tasks.update(task_id=216401, done=True)

# Create relation
client.task_relations.create(
    task_id=task_a,
    relation_kind="blocking",
    other_task_id=task_b
)

# Create bucket
bucket = client.buckets.create(
    project_id=13456,
    title="In Progress",
    limit=3
)
```

---

## 📚 Full Documentation

| Document | Location |
|----------|----------|
| **SOP** | `SOP_VIKUNJA_TASK_WORKFLOW.md` |
| **Skill** | `~/.claude/skills/vikunja-tasks.md` |
| **Tools** | `tools/README.md` |
| **Implementation** | `IMPLEMENTATION_COMPLETE.md` |

---

## ✅ Checklist

Before starting work:
- [ ] Run `vikunja_task_list.py`
- [ ] Note task IDs

After completing work:
- [ ] Run `vikunja_complete_tasks.py <ids>`
- [ ] Verify in Vikunja UI

---

## 🆘 Troubleshooting

**Token expired?**
```bash
vim ~/spawn-solutions/.env
# Update VIKUNJA_API_TOKEN
```

**Commands fail?**
```bash
cd /home/ivanadamin && source .venv/bin/activate
```

**Skill not working?**
```bash
cat ~/.claude/skills/vikunja-tasks.md
```

---

**Tip**: Just say `/vikunja-tasks` in any session - Claude handles the rest!
