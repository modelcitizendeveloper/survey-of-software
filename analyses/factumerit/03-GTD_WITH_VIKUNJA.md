# Getting Things Done (GTD) with Vikunja Integration

**How to apply GTD methodology using Vikunja + spawn-tools**

---

## GTD Overview

**The 5 Steps**:
1. **Capture** - Collect everything that has your attention
2. **Clarify** - Process what each item means and what to do about it
3. **Organize** - Put items where they belong
4. **Reflect** - Review your system regularly
5. **Engage** - Do the work

**Our implementation**: GTD + OODA loop + spawn-tools

---

## GTD Step 1: CAPTURE

**Goal**: Get everything out of your head and into a trusted system

### Tools to Use

**Vikunja UI** (Real-time capture):
- Quick add tasks to Inbox project
- Mobile app for on-the-go capture
- Browser extension for web captures

**vikunja-populate-script** (Batch capture):
- Code scanning: `grep -r "TODO\|FIXME\|HACK" applications/`
- README/ROADMAP files
- Meeting notes, emails, mental notes
- Create YAML with all items, populate in batch

### Capture Workflow

```bash
# 1. Scan codebase for open items
cd ~/spawn-solutions/applications/<app-name>
grep -r "TODO" . > capture-todos.txt
grep -r "FIXME" . > capture-fixmes.txt
grep -r "HACK" . > capture-hacks.txt

# 2. Review documentation
ls -la README* ROADMAP* STATUS* TODO*

# 3. Brain dump - write down everything you're thinking about
# Create vikunja-tasks.yaml with ONE task per item
# Don't organize yet - just capture!

# 4. Populate Vikunja
python populate_vikunja.py applications/<app-name>/vikunja-tasks.yaml
```

**Capture checklist**:
- [ ] Code TODOs/FIXMEs
- [ ] README action items
- [ ] Email action items
- [ ] Meeting notes
- [ ] "Wouldn't it be nice if..." ideas
- [ ] Bugs discovered
- [ ] Things bothering you
- [ ] Commitments made to others

**Rule**: Capture first, organize later. Don't filter during capture.

---

## GTD Step 2: CLARIFY

**Goal**: Process each item - is it actionable? What's the next action?

### Tools to Use

**Vikunja UI** (Interactive clarification):
- Review each task in Inbox
- Add details to task description
- Set priority (0=normal, 5=urgent)
- Add labels for context

**spawn-analysis** (Strategic clarification):
- For big decisions: "Should I even do this?"
- Run decision cards before committing to large projects
- Export portfolio, analyze with Strategist/Economizer

### Clarification Workflow

```bash
# Open Vikunja Inbox project
# For each captured item, ask:

# 1. Is it actionable?
#    - YES → Clarify next action
#    - NO → Delete or move to "Someday/Maybe" label

# 2. What's the next physical action?
#    - Be specific: "Call John" not "Think about calling John"
#    - Update task title to be action-oriented

# 3. Is this a project (>1 action)?
#    - YES → Create new Vikunja project, break into subtasks
#    - NO → Keep as single task

# 4. How long will it take?
#    - <2 min → Do it now (Don't add to Vikunja)
#    - 2min - 4hr → "Quick Win" or "Small" label
#    - 1-2 days → "Medium" label
#    - 3+ days → "Large" label, probably a project

# 5. Strategic decision needed?
cd ~/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-export-script/src
python export_vikunja.py --output ~/spawn-analysis/portfolio.md
# Run spawn-analysis: "Should I prioritize this item?"
```

**Clarification labels to add**:
- **Type**: Bug / Feature / Refactor / Documentation / Research / Infrastructure
- **Effort**: Quick Win (<2hr) / Small (2-4hr) / Medium (1-2 days) / Large (3+ days)
- **Priority**: Critical / High Priority / Low Priority
- **Phase**: Planning / Development / Testing / Deployment / Maintenance

**Questions to ask**:
1. What does "done" look like for this?
2. What's blocking me from starting?
3. Do I have the resources/tools needed?
4. Is this my responsibility or should I delegate?

---

## GTD Step 3: ORGANIZE

**Goal**: Put items in the right places with the right context

### GTD Categories → Vikunja Structure

| GTD Category | Vikunja Implementation |
|--------------|------------------------|
| **Projects** | Vikunja Projects (one per GTD project) |
| **Next Actions** | Tasks with "Ready" label, no dependencies |
| **Waiting For** | Tasks with "Waiting" label |
| **Someday/Maybe** | Tasks with "Low Priority" label, no due date |
| **Reference** | Project descriptions, task descriptions with docs |
| **Calendar** | Tasks with due_date set |

### Organization Workflow

```bash
# 1. Create projects for multi-step items
# Use vikunja-populate-script for batch creation:

cat > applications/<app-name>/vikunja-tasks.yaml <<'EOF'
project:
  title: "Application Name - Feature X"
  description: "Specific feature/epic description"

labels:
  # Copy from applications/vikunja-labels.yaml

tasks:
  - title: "Step 1: Research approach"
    labels: ["Research", "Ready", "Small"]
    due_date: "2025-11-10"

  - title: "Step 2: Design implementation"
    labels: ["Planning", "Waiting", "Medium"]
    # No due date yet - waiting on Step 1

  - title: "Step 3: Build feature"
    labels: ["Development", "Blocked", "Large"]
    # Blocked until Step 2 complete
EOF

python populate_vikunja.py applications/<app-name>/vikunja-tasks.yaml

# 2. Organize existing tasks by labels
# Use Vikunja UI to:
# - Add "Ready" to tasks you can start now
# - Add "Blocked" to tasks waiting on something
# - Add "Waiting" to tasks waiting on others
# - Set due dates for time-sensitive items
# - Add effort labels (Quick Win / Small / Medium / Large)

# 3. Create contexts with labels
# Examples:
# - "Quick Win" - when you have 30 min
# - "Research" - when you're in learning mode
# - "Documentation" - when you're in writing mode
# - "Bug" - when you're in debugging mode
```

**Organization rules**:
1. **One project per Vikunja project** - don't mix unrelated work
2. **Tasks are atomic** - one clear outcome per task
3. **Labels show context** - when/where/how to do this
4. **Due dates are sacred** - only set if truly deadline-driven
5. **Ready means Ready** - no blockers, can start immediately

---

## GTD Step 4: REFLECT

**Goal**: Review your system regularly to stay on top of everything

### Weekly Review (Every Monday)

```bash
# 1. OBSERVE - Export portfolio state
cd ~/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-export-script/src
python export_vikunja.py --output ~/spawn-analysis/weekly-review.md

# Review shows:
# - Velocity: Are you completing tasks?
# - Overdue: What slipped?
# - Completion rate: Are projects progressing?
# - Stalled projects: 0 velocity = needs attention

# 2. ORIENT - Analyze with spawn-analysis
cd ~/spawn-analysis
# Run decision cards:
# - The Strategist: Long-term positioning
# - Capability Auditor: Capacity reality check
# - Optimizer: ROI analysis
# - Economizer: Efficiency check
# - Experience-Based: Pattern recognition

# Question: "What should I prioritize this week?"
# Get recommendation based on actual data

# 3. DECIDE - Update priorities
# Based on spawn-analysis recommendation:
# - Adjust task due dates
# - Reprioritize projects
# - Archive completed projects
# - Add new tasks discovered during week

# 4. ACT - Plan next week
# Use spawn-plans if starting new initiative:
cd ~/spawn-plans
# Run planning methodologies → Tactical Detailer → YAML
python populate_vikunja.py new-week-tasks.yaml
```

### Weekly Review Checklist

**Every Monday morning** (60-90 minutes):

**Process**:
- [ ] Collect loose items (emails, notes, new TODOs)
- [ ] Empty Inbox project (clarify & organize all items)
- [ ] Review "Waiting" tasks (follow up or remove label)
- [ ] Review "Blocked" tasks (still blocked or can unblock?)

**Analyze**:
- [ ] Export portfolio state
- [ ] Run spawn-analysis weekly prioritization
- [ ] Review velocity trends (improving or declining?)
- [ ] Identify stalled projects (0 velocity for 2+ weeks)

**Plan**:
- [ ] Set 3-5 Most Important Tasks for the week
- [ ] Adjust due dates based on reality
- [ ] Archive completed projects
- [ ] Update project descriptions with learnings

**Commit**:
- [ ] Create calendar blocks for focused work
- [ ] Decline/delegate tasks that don't align with priorities
- [ ] Share commitments with stakeholders

---

## GTD Step 5: ENGAGE

**Goal**: Do the work with confidence

### Daily Engagement Workflow

```bash
# Morning (15 min)
# 1. Check today's tasks
# Open Vikunja → Filter: Due today
# Review 3-5 Most Important Tasks

# 2. Quick win check
# Filter: "Quick Win" label, "Ready" status
# Do 1-2 quick wins to build momentum

# 3. Set intention
# Which "Ready" tasks align with today's energy/context?

# During day
# - Work in Vikunja UI
# - Mark tasks "In Progress" when starting
# - Mark tasks done when complete
# - Add new tasks as they arise (capture!)
# - Update task notes with blockers/learnings

# End of day (10 min)
# 1. Update task status
#    - "In Progress" → "Blocked" if stuck
#    - "In Progress" → "Waiting" if need input
#    - "In Progress" → Done if complete

# 2. Quick capture
#    - Any open loops from today?
#    - Commitments made that need tasks?

# 3. Preview tomorrow
#    - What's due tomorrow?
#    - What "Ready" tasks could I start?
```

### Engagement Contexts (Labels)

**When you have...**:
- **15-30 min** → Filter: "Quick Win"
- **Deep focus time** → Filter: "Development" OR "Research", "Large"
- **Low energy** → Filter: "Documentation" OR "Small"
- **Waiting on build** → Filter: "Quick Win", "Bug"
- **Admin time** → Filter: "Infrastructure", "Planning"

**By phase**:
- **Starting project** → Filter: "Planning", "Research"
- **Building** → Filter: "Development", "In Progress"
- **Finishing** → Filter: "Testing", "Documentation"
- **Maintaining** → Filter: "Bug", "Maintenance"

---

## GTD + OODA Integration

**How they work together**:

| GTD Step | OODA Phase | Tools | Frequency |
|----------|------------|-------|-----------|
| **Capture** | OBSERVE | vikunja-export, manual entry | Continuous |
| **Clarify** | ORIENT | spawn-analysis | Daily (small), Weekly (strategic) |
| **Organize** | DECIDE | spawn-solutions, vikunja-populate | Weekly |
| **Reflect** | ORIENT | vikunja-export + spawn-analysis | Weekly |
| **Engage** | ACT | Vikunja UI, spawn-plans | Daily |

**The loop**:
```
CAPTURE (throughout week)
   ↓
REFLECT (Monday: export portfolio)
   ↓
ORIENT (Monday: spawn-analysis prioritization)
   ↓
ORGANIZE (Monday: update Vikunja based on analysis)
   ↓
DECIDE (As needed: spawn-solutions for tool selection)
   ↓
PLAN (As needed: spawn-plans for new initiatives)
   ↓
ENGAGE (Daily: work in Vikunja)
   ↓
CAPTURE (results, new items, blockers)
   ↓
[loop back to REFLECT]
```

---

## Common GTD Challenges & Solutions

### Challenge 1: "Too many projects"

**Solution**: Use spawn-analysis Economizer card
```bash
# Export portfolio
python export_vikunja.py --output portfolio.md

# Run spawn-analysis: "Which projects should I stop?"
# Economizer will identify:
# - 0 velocity projects (not progressing)
# - High effort, low ROI projects
# - Projects past point of diminishing returns

# Archive or delete low-value projects
```

### Challenge 2: "Can't keep up with capture"

**Solution**: Batch capture weekly
```bash
# Friday afternoon: scan for open items
cd ~/spawn-solutions
find . -name "*.py" -o -name "*.md" | xargs grep -l "TODO\|FIXME" > weekly-capture.txt

# Create YAML from findings
# Populate on Monday morning during Weekly Review
```

### Challenge 3: "Overdue tasks piling up"

**Solution**: Use spawn-analysis Capability Auditor
```bash
# Export shows overdue accumulation
python export_vikunja.py

# Capability Auditor reality check:
# "Can I actually do all 3 projects this week?"
# "Historical velocity = 3 tasks/week, but I committed to 10"

# Recommendation: Reduce commitments to match capacity
```

### Challenge 4: "Don't know what to work on"

**Solution**: Labels + filters
```bash
# In Vikunja:
# 1. Filter: "Ready" status (no blockers)
# 2. Filter: "High Priority" (strategic importance)
# 3. Filter: Effort label matching available time
#    - Have 30 min? → "Quick Win"
#    - Have 3 hours? → "Small" or "Medium"
# 4. Sort by due_date (earliest first)

# Top item = what to work on next
```

### Challenge 5: "Projects stalling"

**Solution**: Weekly velocity review
```bash
# Export portfolio every Monday
python export_vikunja.py

# Look for:
# - 0 velocity for 2+ weeks = investigate blocker
# - Declining velocity = scope too large or motivation issue
# - No tasks marked "Ready" = planning problem

# Actions:
# - 0 velocity + blocker = escalate or deprioritize
# - Declining velocity = reduce scope
# - No "Ready" tasks = run spawn-plans Tactical Detailer
```

---

## GTD Best Practices with Vikunja

**DO**:
- ✅ Capture immediately (don't trust memory)
- ✅ Weekly Review every Monday (non-negotiable)
- ✅ Keep Inbox empty (process everything)
- ✅ Use "Ready" label liberally (can start now = Ready)
- ✅ Set due dates ONLY for real deadlines
- ✅ Archive completed projects (keep portfolio clean)
- ✅ Use spawn-analysis for big decisions
- ✅ Trust the system (don't keep mental lists)

**DON'T**:
- ❌ Skip Weekly Review (system breaks down)
- ❌ Set fake due dates (undermines trust)
- ❌ Leave items in Inbox >1 week
- ❌ Create tasks without next action clarity
- ❌ Ignore velocity data (reality > wishful thinking)
- ❌ Commit to new projects without Capability Auditor check
- ❌ Mix personal and work in same project
- ❌ Use Vikunja as archive (move done projects out)

---

## Example: GTD Capture for Schema Evolution Automation

```bash
# Step 1: CAPTURE
cd ~/spawn-solutions/applications/schema-evolution-automation
grep -r "TODO" . > todos.txt
# Found: 12 TODO comments

# Step 2: CLARIFY (for each TODO)
# - TODO: Implement rollback functionality
#   → Actionable? Yes
#   → Next action: Research rollback patterns in Alembic/Flyway
#   → Project? Yes (multi-step)
#   → Effort: Large
#   → Labels: Feature, Research, Large

# Step 3: ORGANIZE
cat > applications/schema-evolution-automation/vikunja-tasks.yaml <<'EOF'
project:
  title: "SEA - Rollback Feature"
  description: "Add rollback capability to schema evolution orchestrator"

labels:
  # Copy from applications/vikunja-labels.yaml
  - title: "Feature"
    hex_color: "9b59b6"
  - title: "Research"
    hex_color: "34495e"
  - title: "Large"
    hex_color: "e74c3c"
  - title: "Ready"
    hex_color: "2ecc71"

tasks:
  - title: "Research rollback patterns in Alembic"
    description: "Study how Alembic handles rollback, document patterns"
    due_date: "2025-11-10"
    priority: 0
    labels: ["Research", "Ready", "Small"]

  - title: "Research rollback patterns in Flyway"
    description: "Study how Flyway handles rollback, document patterns"
    due_date: "2025-11-10"
    priority: 0
    labels: ["Research", "Ready", "Small"]

  - title: "Design SEA rollback interface"
    description: "Based on research, design CLI interface for rollback"
    labels: ["Feature", "Planning", "Medium"]
    # No due date - waiting on research tasks
EOF

python populate_vikunja.py applications/schema-evolution-automation/vikunja-tasks.yaml

# Step 4: REFLECT (Weekly Review)
python export_vikunja.py --output weekly-review.md
# Shows: SEA velocity = 0 (new project), 2 tasks Ready

# Step 5: ENGAGE (Daily work)
# Monday: Do first research task (Alembic)
# Tuesday: Do second research task (Flyway)
# Wednesday: Design rollback interface
# Update Vikunja as you go
```

---

## Quick Reference Card

**Daily**:
- Morning: Check due today, do 1-2 quick wins
- During: Work in Vikunja, mark progress
- Evening: Update status, capture new items

**Weekly (Monday)**:
- Export portfolio (`python export_vikunja.py`)
- Run spawn-analysis prioritization
- Empty Inbox (clarify & organize)
- Set 3-5 Most Important Tasks for week
- Update due dates based on reality

**As Needed**:
- New project: Run spawn-plans → populate YAML
- Big decision: Run spawn-analysis decision cards
- Tool selection: Use spawn-solutions S1-S4
- Feeling overwhelmed: Capability Auditor reality check

---

**Status**: Production ready (Nov 7, 2025)
**Integration**: GTD + OODA + Vikunja + spawn-tools
**Result**: Trusted system for getting things done with data-driven prioritization
