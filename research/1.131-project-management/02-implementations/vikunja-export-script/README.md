# Vikunja Portfolio Export Script

**Export current Vikunja portfolio state for spawn-analysis decision input**

Part of 1.131 Project Management research - completes the OODA loop by making execution state observable for strategic prioritization.

---

## Purpose

**OODA Loop Integration**: Vikunja → spawn-analysis

This script exports your current Vikunja portfolio state (projects, tasks, velocity) into a format that spawn-analysis decision cards can interpret. This enables data-driven prioritization based on actual execution reality, not assumptions.

---

## Quick Start

### Basic Usage

```bash
# Navigate to script directory
cd research/1.131-project-management/02-implementations/vikunja-export-script/src

# Export for spawn-analysis (console output)
python export_vikunja.py

# Save to file
python export_vikunja.py --output portfolio-state.md

# JSON format
python export_vikunja.py --format json --output portfolio.json
```

---

## Output Formats

### 1. spawn-analysis Format (Default)

**Optimized for decision cards** - provides context that cards like The Strategist, Capability Auditor, and Optimizer need:

```markdown
# Current Portfolio State

**Exported**: 2025-11-07T20:00:00

## Portfolio Summary

- **Active Projects**: 3
- **Total Tasks**: 45
- **Completed**: 18 (40.0%)
- **Pending**: 27
- **Overdue**: 5

## Active Projects

### Schema Evolution Automation - Phase 1

*12-week implementation plan for stateless orchestrator CLI tool*

**Tasks**: 15 total, 9 done, 6 pending
⚠️  **2 overdue**
📅 3 due this week

**Velocity**: 2.3 tasks/week (last 4 weeks)
**Completion Rate**: 60.0%

**Top Labels**: Week 1 (5), Foundation (4), Development (3)

### qrcards Maintenance

**Tasks**: 8 total, 2 done, 6 pending
⚠️  **3 overdue**

**Velocity**: 0.5 tasks/week (last 4 weeks)
**Completion Rate**: 25.0%

### Cookbooks Publishing

**Tasks**: 12 total, 0 done, 12 pending
📅 5 due this week

**Velocity**: 0.0 tasks/week (last 4 weeks)
**Completion Rate**: 0.0%

## Context for Decision Cards

**Question**: What should I prioritize this week?

**Considerations**:
- **2 projects have overdue tasks**
- **1 project has 0 velocity** (no recent completions)
- **2 projects are actively progressing**
- **1 project has >10 pending tasks**
```

### 2. JSON Format

**Machine-readable** - for programmatic processing or custom formatting:

```json
{
  "exported_at": "2025-11-07T20:00:00",
  "projects": [
    {
      "id": 123,
      "title": "Schema Evolution Automation - Phase 1",
      "tasks": {
        "total": 15,
        "done": 9,
        "pending": 6,
        "overdue": 2
      },
      "velocity": {
        "tasks_per_week": 2.3,
        "completion_rate": 60.0
      }
    }
  ],
  "summary": {
    "total_projects": 3,
    "total_tasks": 45,
    "total_overdue": 5
  }
}
```

---

## Integration with spawn-analysis

### Workflow

```
1. Export portfolio state:
   $ python export_vikunja.py --output portfolio-state.md

2. Feed to spawn-analysis decision:
   "Given current portfolio state (see portfolio-state.md),
   what should I prioritize this week?"

3. spawn-analysis cards process:
   - The Strategist: Evaluates long-term impact
   - Capability Auditor: Reality-checks what's feasible
   - Optimizer: Maximizes portfolio value
   - Economizer: Considers resource efficiency

4. Decision output:
   "Recommendation: Focus on qrcards overdue tasks first (3 overdue),
   then SEA Week 2 (momentum is good at 2.3 tasks/week).
   Deprioritize cookbooks (0 velocity suggests blockers)."
```

### Example spawn-analysis Prompt

```
# Context: Portfolio State

<paste output from export_vikunja.py>

# Decision Question

Given the portfolio state above, what should I prioritize this week?

**Constraints**:
- 40 hours available
- Want to maintain momentum on active projects
- Revenue-generating work preferred when possible

**Options**:
1. Continue SEA Week 2 (good velocity, on track)
2. Fix qrcards overdue bugs (3 overdue tasks)
3. Start cookbooks publishing (revenue opportunity, 0 progress)
4. Research new experiments (backlog items)

Execute decision cards and provide recommendation with rationale.
```

### Decision Cards Interpretation

**How cards use portfolio data**:

| Card | What it looks for | Example interpretation |
|------|------------------|----------------------|
| **The Strategist** | Long-term positioning | "SEA momentum = good investment, continue" |
| **Capability Auditor** | Feasibility given velocity | "qrcards 0.5 tasks/week = can fix 2-3 bugs" |
| **Optimizer** | Maximum portfolio value | "Fix qrcards overdue first (risk mitigation)" |
| **Economizer** | Efficiency | "SEA has 2.3 velocity, highest ROI" |
| **Experience-Based** | Past patterns | "Cookbooks 0 velocity = likely blockers" |

---

## Features

### Metrics Calculated

**Per Project**:
- Task counts (total, done, pending)
- Due date tracking (overdue, this week, next week)
- Priority distribution
- Label distribution
- Velocity (tasks/week over last 4 weeks)
- Completion rate

**Portfolio-wide**:
- Total projects
- Total tasks across all projects
- Aggregate overdue count
- Project health indicators

### Health Indicators

**Automatically highlighted**:
- ⚠️  **Overdue tasks** (attention needed)
- 📅 **Due this week** (urgency indicator)
- **0 velocity** (stalled projects = possible blockers)
- **>10 pending** (high workload projects)

---

## CLI Options

```
usage: export_vikunja.py [-h] [--format {json,markdown,spawn-analysis}]
                         [--output OUTPUT] [--spawn-analysis]

options:
  --format {json,markdown,spawn-analysis}
                        Output format (default: spawn-analysis)
  --output OUTPUT       Output file path (default: stdout)
  --spawn-analysis      Format for spawn-analysis decision cards
```

---

## Use Cases

### 1. Weekly Prioritization

```bash
# Monday morning routine
python export_vikunja.py --output portfolio.md

# Feed to spawn-analysis
# "What should I prioritize this week?"
```

### 2. Project Health Check

```bash
# Check which projects are stalled
python export_vikunja.py --format json | jq '.projects[] | select(.velocity.tasks_per_week == 0)'
```

### 3. Capacity Planning

```bash
# Export current state before spawn-plans
python export_vikunja.py --output current-capacity.md

# Use in spawn-plans Capacity Auditor methodology
# "Given current workload, can we add new project?"
```

### 4. Retrospectives

```bash
# Export state weekly
python export_vikunja.py --output "retrospectives/week-$(date +%Y-%m-%d).md"

# Compare velocity week-over-week
# Identify patterns in stalled projects
```

---

## Integration with OODA Loop

```
┌─────────────────────────────────────────────────────────────┐
│                    OBSERVE (Vikunja State)                  │
│  python export_vikunja.py → portfolio-state.md              │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│         ORIENT (spawn-analysis: SHOULD I do this?)          │
│  Decision cards process portfolio state                     │
│  Output: "Fix qrcards overdue tasks" (strategic direction)  │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│      DECIDE (spawn-solutions: WHAT tools to use?)           │
│  "Which debugging approach?" → Use existing tools           │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                   ACT (Build + Track)                       │
│  spawn-experiments: Fix bugs (Method 1)                     │
│  spawn-plans: Mark tasks done in Vikunja                    │
└────────────────────────┬────────────────────────────────────┘
                         ↓
                  (Loop back: Export new state)
```

**Key Innovation**: Execution reality (velocity, overdue tasks) feeds back into next strategic decision, preventing planning delusions.

---

## Requirements

- Python 3.8+
- Vikunja API token configured (see [vikunja-api-wrapper/QUICK_START.md](../vikunja-api-wrapper/QUICK_START.md))
- `.env` file at repo root with `VIKUNJA_API_TOKEN`

---

## Related Tools

**Same implementation series (1.131)**:
- [vikunja-api-wrapper](../vikunja-api-wrapper/) - Python API client
- [vikunja-populate-script](../vikunja-populate-script/) - YAML → Vikunja task creation
- **vikunja-export-script** (this tool) - Vikunja → spawn-analysis state export

**Integration points**:
- **spawn-analysis** (`~/spawn-analysis/`) - Consumes exported portfolio state
- **spawn-plans** (`~/spawn-plans/`) - Creates tasks via populate script
- **Vikunja** - Source of truth for execution state

---

## Development

**Methodology**: Method 1 (Direct Implementation)
- Straightforward data extraction and formatting
- No complex validation (read-only)
- Clear transformation logic

**Future Enhancements**:
- [ ] Trend analysis (velocity over time)
- [ ] Burndown chart data export
- [ ] Blocked tasks detection (no progress in N weeks)
- [ ] Team capacity calculation (if multi-user)
- [ ] Custom metrics (time estimates vs actuals)

---

**Hardware Store Model**: Generic tool for portfolio observation. Adapt output format to your decision framework needs.
