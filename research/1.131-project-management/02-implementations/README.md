# Vikunja Integration Suite

**Three tools to close the OODA loop: Plan → Track → Measure → Decide**

---

## Overview

This suite integrates Vikunja project management with the spawn ecosystem to enable data-driven strategic prioritization based on actual execution reality.

```
┌─────────────────────────────────────────────────────────────────┐
│                         OODA LOOP CLOSED                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  OBSERVE         vikunja-export-script                          │
│  (Measure)       └─→ portfolio-state.md                        │
│                  Current reality: velocity, overdue, completion │
│                                                                 │
│  ↓                                                              │
│                                                                 │
│  ORIENT          spawn-analysis decision cards                  │
│  (Analysis)      └─→ "Should I prioritize this project?"       │
│                  Strategist, Optimizer, Economizer analysis     │
│                                                                 │
│  ↓                                                              │
│                                                                 │
│  DECIDE          spawn-solutions                                │
│  (Solution)      └─→ Which tools/services/libraries to use     │
│                  S1-S4 discovery: platform selection            │
│                                                                 │
│  ↓                                                              │
│                                                                 │
│  ACT             spawn-plans + vikunja-populate + execution     │
│  (Plan)          └─→ Tactical Detailer → YAML → Vikunja        │
│                  Create plan, populate tasks, execute & track   │
│                                                                 │
│  ↓ (loop back to OBSERVE to measure execution results)         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## The Three Tools

### 1. **vikunja-api-wrapper** - Foundation API Client

**What**: Python client for Vikunja Cloud API
**When**: When you need programmatic access to Vikunja
**Where**: Used by both populate and export scripts

**Direct use cases**:
- Custom automation scripts
- One-off bulk operations
- Testing API integration

**You probably don't need this directly** - use populate/export scripts instead.

**See**: `vikunja-api-wrapper/README.md`

---

### 2. **vikunja-populate-script** - Plan → Vikunja

**What**: Creates Vikunja projects, labels, and tasks from YAML/JSON
**When**: After completing strategic planning with spawn-plans
**Where**: In the spawn-plans workflow, Stage 5 (Tactical Detailer)

#### When to Use

**✅ Use populate script when**:
- You've completed spawn-plans Tactical Detailer (Stage 5)
- You have a `vikunja-tasks.yaml` file ready
- You want to automatically create tasks in Vikunja from a plan
- Starting a new project sprint/phase

**❌ Don't use populate script when**:
- Adding individual tasks manually (use Vikunja UI)
- Tasks already exist in Vikunja
- Making small adjustments to existing plan

#### Workflow Integration

```bash
# 1. Complete strategic planning in spawn-plans
cd ~/spawn-plans
# Run Stages 1-4 methodologies, then Tactical Detailer (Stage 5)
# Output: plans/my-project/01-initial-round/13-tactical-detailer/vikunja-tasks.yaml

# 2. Validate YAML (dry run)
cd ~/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-populate-script/src
python populate_vikunja.py --dry-run ~/spawn-plans/plans/my-project/.../vikunja-tasks.yaml

# 3. Populate Vikunja
python populate_vikunja.py --verbose ~/spawn-plans/plans/my-project/.../vikunja-tasks.yaml
# ✅ Created project, labels, tasks
# 🌐 View in Vikunja: https://app.vikunja.cloud/projects/12345

# 4. Work in Vikunja
# Mark tasks done, track progress, adjust priorities
```

**YAML Format** (required by Tactical Detailer):
```yaml
project:
  title: "Project Name - Phase 1"
  description: "Brief description"

labels:
  - title: "Week 1"
    hex_color: "ff6b6b"

tasks:
  - title: "Task title"
    description: |
      <strong>Goal:</strong> What this accomplishes<br><br>
      <strong>Steps:</strong><br>
      - Step 1<br>
      - Step 2
    due_date: "2025-11-15"  # YYYY-MM-DD format
    priority: 0  # 0=normal, 5=urgent
    labels:
      - "Week 1"
```

**See**: `vikunja-populate-script/README.md`, `vikunja-populate-script/src/SCHEMA.md`

---

### 3. **vikunja-export-script** - Vikunja → spawn-analysis

**What**: Exports Vikunja portfolio state for strategic decision-making
**When**: Weekly prioritization or when you need to make portfolio decisions
**Where**: Feeds into spawn-analysis decision cards (ORIENT phase)

#### When to Use

**✅ Use export script when**:
- Planning your weekly priorities
- Making portfolio allocation decisions
- Reviewing project health/velocity
- Preparing for strategic planning rounds
- Need data for spawn-analysis decision cards

**❌ Don't use export script when**:
- Just checking task status (use Vikunja UI)
- Working on a single project (no portfolio view needed)
- Making operational decisions (not strategic)

#### Workflow Integration

```bash
# 1. Export portfolio state (weekly routine)
cd ~/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-export-script/src
python export_vikunja.py --output ~/spawn-analysis/portfolio-state.md

# 2. Use in spawn-analysis for prioritization
cd ~/spawn-analysis
# Decision prompt: "Given portfolio-state.md, what should I prioritize this week?"
# Execute decision cards: Strategist, Capability Auditor, Optimizer, Economizer, etc.

# 3. Get recommendation with rationale
# Example output:
#   Priority 1: Fix qrcards overdue (3 tasks, risk mitigation)
#   Priority 2: Continue SEA Week 2 (maintain 2.3 velocity)
#   Priority 3: Investigate cookbooks blocker (0 velocity)

# 4. Update Vikunja based on decision
# Adjust priorities, due dates, deprioritize stalled projects
```

**Output Formats**:
- `--format spawn-analysis` (default) - Markdown for decision cards
- `--format json` - Structured data for custom analysis
- `--output <file>` - Save to file instead of stdout

**Portfolio Metrics Calculated**:
- **Velocity**: tasks/week completed (last 4 weeks)
- **Overdue**: tasks past due date
- **Completion Rate**: % of tasks done
- **Labels**: distribution of work types
- **Due dates**: this week, next week, overdue

**See**: `vikunja-export-script/README.md`, `vikunja-export-script/SPAWN_ANALYSIS_INTEGRATION.md`

---

## Complete Usage Example

### Scenario: Starting a new 12-week project

**Week 0: Planning**
```bash
# 1. Strategic planning in spawn-plans
cd ~/spawn-plans
# Run 12 planning methodologies, output to Tactical Detailer
# Result: plans/sea/01-initial-round/13-tactical-detailer/vikunja-tasks.yaml

# 2. Populate Vikunja with Week 1-3 tasks
cd ~/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-populate-script/src
python populate_vikunja.py ~/spawn-plans/plans/sea/.../vikunja-tasks.yaml
# ✅ Created 3 labels (Week 1, Week 2, Week 3), 15 tasks
```

**Week 1-3: Execution**
```bash
# Work in Vikunja: mark tasks done, track progress
# Example: Completed 7/15 tasks, velocity = 2.3 tasks/week
```

**Week 4: Prioritization**
```bash
# 1. Export portfolio state
cd ~/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-export-script/src
python export_vikunja.py --output ~/spawn-analysis/portfolio-state.md

# Portfolio shows:
# - SEA: 2.3 velocity, 60% complete, on track
# - qrcards: 0.5 velocity, 3 overdue bugs
# - cookbooks: 0.0 velocity, stalled

# 2. Strategic decision with spawn-analysis
cd ~/spawn-analysis
# "Given portfolio-state.md, what should I prioritize this week?"
# Cards recommend: Fix qrcards overdue (risk), continue SEA (momentum),
#                  investigate cookbooks blocker

# 3. Adjust Vikunja priorities based on decision
```

**Week 5: Next Planning Round**
```bash
# 1. Update spawn-plans with actual velocity data
cd ~/spawn-plans
# Run Tactical Detailer Round 2 with realistic estimates
# Result: Adjusted timeline based on 2.3 velocity

# 2. Populate Vikunja with updated Week 4-6 tasks
cd ~/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-populate-script/src
python populate_vikunja.py ~/spawn-plans/plans/sea/.../vikunja-tasks.yaml
```

**Continuous improvement**: Each iteration uses actual execution data to improve planning accuracy.

---

## Decision Matrix: Which Tool When?

| Scenario | Tool | Command |
|----------|------|---------|
| **Just finished strategic planning** | populate | `python populate_vikunja.py plan.yaml` |
| **Need weekly priorities** | export | `python export_vikunja.py --output state.md` |
| **Want to validate plan before creating** | populate | `python populate_vikunja.py --dry-run plan.yaml` |
| **Making portfolio decisions** | export | `python export_vikunja.py` (→ spawn-analysis) |
| **Starting new sprint/phase** | populate | `python populate_vikunja.py sprint-2.yaml` |
| **Reviewing velocity trends** | export | `python export_vikunja.py --format json` |
| **One-off API operations** | wrapper | Use Python API directly |
| **Adding single task** | None | Use Vikunja UI |

---

## Integration with spawn Ecosystem

### spawn-plans Integration

**Tactical Detailer (Stage 5)** now outputs TWO files:
1. `output.md` - Strategic documentation (execution procedures, checklists, schedules)
2. `vikunja-tasks.yaml` - Task tracking (for populate script)

**Flow**:
```
Stages 1-4 → Strategic Synthesizer → final-plan.md
                                          ↓
                              Tactical Detailer (Stage 5)
                                          ↓
                              ┌───────────┴───────────┐
                              ↓                       ↓
                         output.md            vikunja-tasks.yaml
                    (documentation)           (task tracking)
                                                      ↓
                                            populate_vikunja.py
                                                      ↓
                                              Vikunja Cloud
```

**See**: `~/spawn-plans/VIKUNJA_INTEGRATION.md`

### spawn-analysis Integration

**Export script provides context** for these decision cards:
- **The Strategist**: Uses velocity trends for momentum analysis
- **Capability Auditor**: Uses overdue counts for capacity reality-check
- **Optimizer**: Uses completion rates for ROI calculations
- **Economizer**: Uses velocity for efficiency analysis
- **Experience-Based**: Uses historical patterns from past velocity

**Flow**:
```
Vikunja (execution reality)
          ↓
export_vikunja.py → portfolio-state.md
          ↓
spawn-analysis decision cards
          ↓
"What should I prioritize?" → Recommendation
          ↓
Update Vikunja priorities → Next planning round
```

**See**: `vikunja-export-script/SPAWN_ANALYSIS_INTEGRATION.md`

### spawn-solutions Integration

**This research (1.131)** provides the tools:
- S1-S4 discovery completed Nov 7, 2025
- Vikunja Cloud selected (€40/year managed service)
- Three implementations: wrapper (Method 4), populate (Method 4), export (Method 1)

**Research artifacts**:
- `01-discovery/` - Platform evaluation (S1-S4)
- `02-implementations/` - Working integrations (this directory)

---

## Quick Start Checklist

### First-time Setup

- [ ] Vikunja API token configured in `~/.env` (or spawn-solutions root `.env`)
  ```bash
  VIKUNJA_API_TOKEN=your_token_here
  VIKUNJA_BASE_URL=https://app.vikunja.cloud
  ```
- [ ] Python dependencies installed (use `uv`)
  ```bash
  cd vikunja-api-wrapper/src
  uv pip install -r requirements.txt --python venv/bin/python
  uv pip install pyyaml python-dotenv --python venv/bin/python
  ```

### Weekly Workflow

**Monday morning (Planning)**:
- [ ] Export portfolio state
  ```bash
  python export_vikunja.py --output ~/spawn-analysis/portfolio-state.md
  ```
- [ ] Run spawn-analysis decision cards
- [ ] Get weekly priorities recommendation
- [ ] Adjust Vikunja task priorities

**During week (Execution)**:
- [ ] Work in Vikunja UI (mark tasks done, track progress)

**Friday afternoon (Review)**:
- [ ] Export portfolio to check velocity
- [ ] Identify blockers (0 velocity projects)

**Every 2-4 weeks (Strategic planning)**:
- [ ] Run spawn-plans with updated velocity data
- [ ] Generate new `vikunja-tasks.yaml` from Tactical Detailer
- [ ] Populate next sprint/phase tasks
  ```bash
  python populate_vikunja.py --verbose new-sprint.yaml
  ```

---

## Troubleshooting

### "API token not found"
**Issue**: `.env` file missing or wrong location
**Fix**: Ensure `.env` in spawn-solutions root with `VIKUNJA_API_TOKEN=...`

### "Module not found: dateutil"
**Issue**: Dependencies not installed
**Fix**:
```bash
cd vikunja-api-wrapper/src
uv pip install -r requirements.txt --python venv/bin/python
```

### "Invalid YAML syntax"
**Issue**: YAML formatting error
**Fix**: Use `--dry-run` to validate:
```bash
python populate_vikunja.py --dry-run tasks.yaml
```

### "Label 'X' not found"
**Issue**: Task references non-existent label
**Fix**: Define all labels in `labels:` section before tasks reference them

### "Validation error: parsing time"
**Issue**: Date format incorrect (populate script auto-converts now)
**Fix**: Use `YYYY-MM-DD` format, script converts to ISO datetime automatically

### Test data not cleaned up
**Issue**: Test projects/labels still in Vikunja
**Fix**: Tests should leave no trace - always delete test projects after testing

---

## Performance & Limits

**Vikunja Cloud rate limits**:
- Unknown exact limits (2025-11-07: hit limits during development)
- Recommendation: Use `--dry-run` for validation before creating resources
- Batch operations carefully (don't create 100 projects at once)

**Export script performance**:
- Fetches all projects and tasks (1 API call per project)
- ~1 second for 10 projects with 100 tasks total
- Minimal API usage (read-only)

**Populate script performance**:
- Creates project (1 call) + labels (1 per label) + tasks (1 per task) + label attachments (1 per task-label pair)
- Example: 1 project + 3 labels + 10 tasks with 2 labels each = 1 + 3 + 10 + 20 = 34 API calls
- Use `--dry-run` first to avoid wasted API calls

---

## Next Steps

1. **Test with real project**: Use Tactical Detailer on existing spawn-plans output
2. **Weekly routine**: Set up Monday morning portfolio export + spawn-analysis workflow
3. **Iterate planning**: Use actual velocity data in next planning round
4. **Track trends**: Export portfolio weekly, observe velocity patterns over time
5. **Refine cards**: Adjust spawn-analysis decision cards based on portfolio metrics

---

**Status**: Production ready (Nov 7, 2025)
**Research**: 1.131 Project Management Platforms
**Integration**: spawn-plans (ACT), spawn-analysis (ORIENT), spawn-solutions (DECIDE)
**OODA Loop**: ✅ Closed
