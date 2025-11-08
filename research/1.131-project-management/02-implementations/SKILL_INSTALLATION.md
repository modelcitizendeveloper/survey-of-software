# Claude Skill: Vikunja Task Management

**Status**: ✅ Installed Systemwide
**Location**: `~/.claude/skills/vikunja-tasks.md`
**Created**: 2025-11-08

---

## What is This?

A **Claude Code skill** that loads the Vikunja task workflow into any conversation. When invoked, it provides:

- Task-driven development workflow
- Quick commands for task management
- Vikunja API wrapper reference
- SOP integration

---

## How to Use

### In Any Claude Code Session

Simply type:

```
/vikunja-tasks
```

Or ask Claude to invoke it:

```
"Load the Vikunja tasks skill"
"Let's follow the task workflow"
"Show me the task management process"
```

### What Happens

Claude will:
1. Load the task workflow context
2. Proactively run `vikunja_task_list.py` at session start
3. Guide you through task-driven development
4. Remind you to mark tasks complete at session end

---

## Skill Behavior

### Automatic Actions

When the skill is active, Claude will:

**At START of session**:
- Run task list command
- Show current tasks
- Ask which tasks you're working on

**During DEVELOP**:
- Reference task IDs in commits
- Use task descriptions as acceptance criteria
- Keep task IDs visible

**At END of session**:
- Ask which tasks were completed
- Run completion script
- Verify tasks marked done
- Show updated progress

---

## Example Usage

### Starting a Session

```
You: "Let's work on the authentication feature"

Claude: I'll check what tasks we have for this work.
[Loads vikunja-tasks skill]
[Runs vikunja_task_list.py]

Found these relevant tasks:
⏳ [216401] Feature: Implement JWT authentication
⏳ [216402] Feature: Add password reset flow

Which task(s) will we work on today?
```

### Ending a Session

```
You: "We're done with authentication, mark it complete"

Claude: I'll mark task 216401 as complete.
[Runs vikunja_complete_tasks.py 216401]

✅ Completed [216401]: Feature: Implement JWT authentication

Updated progress: 3/6 completed (50%)
```

---

## Commands Available

The skill provides access to:

### List Tasks
```bash
cd /home/ivanadamin && source .venv/bin/activate
python3 /home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/tools/vikunja_task_list.py
```

### Complete Tasks
```bash
cd /home/ivanadamin && source .venv/bin/activate
python3 /home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/tools/vikunja_complete_tasks.py <task_id>
```

### Wrapper API
Direct access to VikunjaClient for complex operations.

---

## Configuration

### Skill Location
`~/.claude/skills/vikunja-tasks.md`

### Dependencies
- Python venv: `/home/ivanadamin/.venv`
- Wrapper: `/home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-api-wrapper`
- Tools: `/home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/tools`
- Token: `/home/ivanadamin/spawn-solutions/.env`

### Default Project
**13456** - Vikunja Integration

---

## Benefits

### Systemwide Availability
- Works in **any** Claude Code session
- No need to remember commands
- Consistent workflow across projects

### Automatic Workflow
- Proactive task retrieval
- Guided development process
- Automated completion tracking

### Dogfooding
- Validates our own tools
- Continuous improvement feedback
- Living documentation

---

## Updating the Skill

To modify the skill:

```bash
vim ~/.claude/skills/vikunja-tasks.md
```

Changes take effect immediately in new conversations.

---

## Testing the Skill

### Manual Test

In a new Claude Code session:

```
You: /vikunja-tasks

Claude: [Loads skill context]
I'll help you with task-driven development using Vikunja.

Let me check current tasks...
[Runs vikunja_task_list.py]

Found 6 tasks in project 13456:
⏳ [216368] Feature: Create vikunja-admin script P5
✅ [216369] Feature: Implement task relations
✅ [216370] Feature: Add kanban buckets
...

Which task(s) are you working on?
```

### Verify Behavior

The skill should:
- ✅ Load without errors
- ✅ Run task list command
- ✅ Display current tasks
- ✅ Ask which tasks to work on
- ✅ Provide workflow guidance

---

## Integration with Other Skills

This skill complements:
- `spawn-analysis.md` - Research analysis workflow
- Future skills for git, testing, etc.

Can be combined in sessions:

```
You: "Load spawn-analysis and vikunja-tasks"

Claude: [Loads both skills]
Ready for research with task tracking!
```

---

## Maintenance

### Check Skill Status
```bash
cat ~/.claude/skills/vikunja-tasks.md | head -20
```

### Update Token (When Expired)
```bash
# 1. Get new token from Vikunja UI
# 2. Update .env
vim /home/ivanadamin/spawn-solutions/.env

# 3. Update skill if token is hardcoded
vim ~/.claude/skills/vikunja-tasks.md
```

### Add New Projects
Edit skill to add project IDs:
```markdown
## Project IDs

- **13456**: Vikunja Integration
- **13457**: New Project Name
```

---

## Troubleshooting

### Skill Not Found

```bash
# Verify location
ls -la ~/.claude/skills/vikunja-tasks.md

# Re-create if missing
cp /home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/SKILL_INSTALLATION.md ~/.claude/skills/vikunja-tasks.md
```

### Commands Fail

```bash
# Check venv
cd /home/ivanadamin && source .venv/bin/activate
python3 --version

# Check tools
ls /home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/tools/
```

### Token Issues

```bash
# Verify token
cat /home/ivanadamin/spawn-solutions/.env | grep VIKUNJA_API_TOKEN

# Test token
cd /home/ivanadamin && source .venv/bin/activate
python3 /home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/tools/vikunja_task_list.py
```

---

## Related Documentation

- **Full SOP**: `/home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/SOP_VIKUNJA_TASK_WORKFLOW.md`
- **Tools README**: `/home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/tools/README.md`
- **Implementation**: `/home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/IMPLEMENTATION_COMPLETE.md`

---

## Evolution

This skill should evolve based on usage:

- Add new commands as tools are built
- Update workflow based on feedback
- Integrate with git/CI/CD as needed
- Add project-specific adaptations

---

**Created**: 2025-11-08
**Version**: 1.0
**Status**: Active and ready for use in all Claude Code sessions
