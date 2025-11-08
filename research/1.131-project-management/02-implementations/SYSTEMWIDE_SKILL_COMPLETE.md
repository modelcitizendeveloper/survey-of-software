# Systemwide Claude Skill - COMPLETE ✅

**Date**: 2025-11-08
**Status**: Installed and Active
**Scope**: All Claude Code sessions

---

## What Was Created

### Claude Skill (Systemwide)

**Location**: `~/.claude/skills/vikunja-tasks.md`

**Functionality**:
- Loads Vikunja task workflow into any conversation
- Provides START → DEVELOP → END workflow
- Includes quick commands and API reference
- Guides task-driven development

**Invocation**:
```
/vikunja-tasks
```

Or simply ask:
- "Load the Vikunja tasks skill"
- "Let's follow the task workflow"
- "Show me current tasks"

---

## How It Works

### In Any Claude Code Session

1. **User invokes skill**: `/vikunja-tasks`

2. **Claude loads context**:
   - Task-driven development workflow
   - Quick command reference
   - Vikunja API wrapper usage
   - SOP integration

3. **Claude proactively**:
   - Runs `vikunja_task_list.py` at session start
   - Shows current tasks
   - Asks which tasks to work on
   - Reminds to mark tasks complete at end

4. **Result**: Automatic task tracking in every session

---

## File Structure

```
~/.claude/skills/
└── vikunja-tasks.md          # ← Systemwide skill

/home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/
├── SOP_VIKUNJA_TASK_WORKFLOW.md     # Full SOP
├── SKILL_INSTALLATION.md             # Skill documentation
├── QUICK_REFERENCE.md                # One-page guide
├── SESSION_SUMMARY.md                # This session's work
├── IMPLEMENTATION_COMPLETE.md        # Core implementation
│
├── tools/
│   ├── vikunja_task_list.py         # List tasks
│   ├── vikunja_complete_tasks.py    # Mark complete
│   └── README.md                     # Tool docs
│
├── vikunja-api-wrapper/
│   └── src/
│       ├── vikunja_wrapper.py       # API wrapper
│       ├── test_task_relations.py   # Relations tests
│       ├── test_buckets.py          # Buckets tests
│       └── M4_MUTATION_LOG.md       # M4 documentation
│
└── vikunja-populate-script/
    ├── src/
    │   ├── population.py            # Population logic
    │   ├── validation.py            # Validation
    │   └── SCHEMA.md                # YAML schema
    └── examples/
        ├── sprint-with-dependencies.yaml
        └── project-with-subtasks.yaml
```

---

## Integration Levels

### Level 1: Manual (No Skill)
```bash
# User manually runs commands
python3 tools/vikunja_task_list.py
python3 tools/vikunja_complete_tasks.py 216401
```

### Level 2: SOP Following
```bash
# User follows SOP document
# References: SOP_VIKUNJA_TASK_WORKFLOW.md
```

### Level 3: Skill-Assisted (Active Now!) ✅
```
# User invokes skill
/vikunja-tasks

# Claude automatically:
# - Runs task list
# - Guides workflow
# - Marks tasks complete
```

### Level 4: Fully Automated (Future)
```
# Claude proactively invokes skill
# No user action needed
# Automatic task management
```

---

## Example Session With Skill

### Start

```
You: "Let's work on the authentication feature"

Claude: [Automatically loads vikunja-tasks skill]

I'll check what tasks we have for this work.

[Runs: python3 tools/vikunja_task_list.py]

================================================================================
VIKUNJA TASKS - Project 13456
================================================================================

📋 Found 6 tasks:

⏳ TODO [216401] Feature: Implement JWT authentication P5
⏳ TODO [216402] Feature: Add password reset flow P4
✅ DONE [216369] Feature: Implement task relations
...

================================================================================
Progress: 2/6 completed (33%)
================================================================================

Which task(s) will we work on today?
```

### End

```
You: "Authentication is done, mark it complete"

Claude: I'll mark task 216401 as complete.

[Runs: python3 tools/vikunja_complete_tasks.py 216401]

================================================================================
MARKING TASKS AS COMPLETE
================================================================================

✅ Completed [216401]: Feature: Implement JWT authentication

================================================================================
Marked 1 task(s) as complete
================================================================================

Great! Updated progress: 3/6 completed (50%)

Would you like to see the updated task list?
```

---

## Benefits

### For Users

✅ **Zero Configuration** - Works in any session
✅ **Automatic Workflow** - No need to remember commands
✅ **Consistent Process** - Same workflow everywhere
✅ **Living Documentation** - Tasks always up to date

### For Development

✅ **Dogfooding** - Validate tools immediately
✅ **Continuous Feedback** - Find issues early
✅ **Clear Accountability** - Track all work
✅ **Quality Signal** - If we won't use it, fix it

### For Project Management

✅ **Real-time Progress** - Always know what's done
✅ **Task Tracking** - No work goes unrecorded
✅ **Dependency Management** - Relations tracked
✅ **Team Visibility** - Shared understanding

---

## Testing the Skill

### Quick Test

In a **new** Claude Code session:

```
You: /vikunja-tasks
```

**Expected**:
- Skill loads
- Task list runs
- Current tasks displayed
- Workflow guidance provided

### Verify Installation

```bash
ls -la ~/.claude/skills/vikunja-tasks.md
# Should exist

cat ~/.claude/skills/vikunja-tasks.md | head -10
# Should show skill content
```

---

## Maintenance

### Update Skill

```bash
vim ~/.claude/skills/vikunja-tasks.md
```

Changes take effect immediately in new conversations.

### Add Projects

Edit skill to add new project IDs:

```markdown
## Project IDs

- **13456**: Vikunja Integration
- **13457**: QRCards Project
- **13458**: Another Project
```

### Update Token

When token expires (2026-11-07):

```bash
# 1. Update .env
vim /home/ivanadamin/spawn-solutions/.env

# 2. Update skill if hardcoded
vim ~/.claude/skills/vikunja-tasks.md
```

---

## Evolution Path

### Current (v1.0)
- ✅ Manual skill invocation
- ✅ Guided workflow
- ✅ Task list/complete commands

### Near Future (v1.1)
- [ ] Auto-invoke at session start
- [ ] Git integration (task IDs in commits)
- [ ] Multi-project support

### Long Term (v2.0)
- [ ] Fully automatic task detection
- [ ] Smart task suggestions
- [ ] Cross-project task management
- [ ] Integration with CI/CD

---

## Related Skills

### Existing
- `spawn-analysis.md` - Research workflow

### Potential Future Skills
- `git-workflow.md` - Git best practices
- `testing.md` - Testing workflow
- `deployment.md` - Deployment procedures

### Skill Composition

```
You: "Load vikunja-tasks and spawn-analysis"

Claude: [Loads both skills]
Ready for research with task tracking!
```

---

## Success Metrics

Track over time:

| Metric | Target | Status |
|--------|--------|--------|
| Sessions using skill | >80% | ⏳ TBD |
| Tasks tracked | 100% | ✅ Active |
| Task completion rate | >90% | ⏳ TBD |
| User satisfaction | High | ⏳ TBD |

---

## Documentation Hierarchy

1. **QUICK_REFERENCE.md** ← Start here (one page)
2. **SKILL_INSTALLATION.md** ← How to use skill
3. **SOP_VIKUNJA_TASK_WORKFLOW.md** ← Full workflow
4. **IMPLEMENTATION_COMPLETE.md** ← Technical details
5. **~/.claude/skills/vikunja-tasks.md** ← Skill source

---

## Troubleshooting

### Skill Not Loading

```bash
# Verify file exists
ls ~/.claude/skills/vikunja-tasks.md

# Check permissions
chmod 644 ~/.claude/skills/vikunja-tasks.md
```

### Commands Fail

```bash
# Activate venv
cd /home/ivanadamin && source .venv/bin/activate

# Test command
python3 /home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/tools/vikunja_task_list.py
```

### Token Issues

```bash
# Check token
cat /home/ivanadamin/spawn-solutions/.env | grep VIKUNJA

# Test API
python3 -c "
from vikunja_wrapper import VikunjaClient
client = VikunjaClient(
    base_url='https://app.vikunja.cloud',
    token='tk_...'
)
print(len(client.tasks.list(project_id=13456)))
"
```

---

## Conclusion

The Vikunja task management skill is now **systemwide** and ready for use in all Claude Code sessions.

**Key Achievement**: Task-driven development is now the **default workflow** - not something you have to remember, but something Claude automatically guides you through.

This creates a self-reinforcing loop:
1. Use tools we build
2. Find issues immediately
3. Fix and improve
4. Repeat

**Status**: ✅ Ready for production use
**Next**: Use `/vikunja-tasks` in your next session!

---

**Created**: 2025-11-08
**Version**: 1.0
**Location**: `~/.claude/skills/vikunja-tasks.md`
