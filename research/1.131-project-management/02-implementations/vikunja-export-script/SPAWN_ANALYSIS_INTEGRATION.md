# spawn-analysis Integration Guide

**How to use Vikunja portfolio state in spawn-analysis decision cards**

---

## Quick Integration

### Step 1: Export Portfolio State

```bash
cd ~/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-export-script/src
python export_vikunja.py --output portfolio-state.md
```

### Step 2: Use in spawn-analysis Decision

Navigate to `~/spawn-analysis/` and create a decision with portfolio context:

```bash
cd ~/spawn-analysis/
# Use Task tool or direct card execution
```

**Decision prompt template**:

```markdown
# Portfolio State Context

<paste content from portfolio-state.md>

---

# Decision Question

What should I prioritize this week?

**Available Time**: 40 hours
**Constraints**: None specific
**Goal**: Maximize portfolio value while maintaining project momentum

**Current Considerations**:
- SEA has good velocity (2.3 tasks/week) but 2 overdue tasks
- qrcards has 3 overdue bugs (low velocity 0.5 tasks/week)
- cookbooks has 0 velocity (12 pending tasks, possible blocker)

Execute the following decision cards:
1. The Strategist (long-term positioning)
2. Capability Auditor (reality-check feasibility)
3. Optimizer (maximize portfolio value)
4. Economizer (resource efficiency)
5. Experience-Based (past patterns)
6. Synthesizer (integrate perspectives)

Provide recommendation with rationale.
```

---

## Decision Card Prompts

### Cards That Use Portfolio Data

#### 1. The Strategist

**What it looks for**:
- Project momentum (velocity trends)
- Strategic positioning (which projects unlock future value)
- Competitive advantage (time-to-market considerations)

**Example interpretation**:
```
Portfolio shows:
- SEA: 2.3 tasks/week velocity = strong momentum, continue to capitalize
- qrcards: 0.5 tasks/week = low momentum but overdue = risk
- cookbooks: 0.0 tasks/week = stalled, investigate blockers first

Strategic recommendation: Fix qrcards overdue (risk mitigation),
continue SEA momentum, unblock cookbooks before committing time.
```

#### 2. Capability Auditor

**What it looks for**:
- Current workload (pending task counts)
- Historical velocity (can you actually do this?)
- Overdue accumulation (capacity mismatch signal)

**Example interpretation**:
```
Portfolio shows:
- Total pending: 27 tasks across 3 projects
- Average velocity: ~3 tasks/week total
- Overdue: 5 tasks (capacity exceeded recently)

Reality check: You have 40 hours this week
- At 3 tasks/week, can complete ~3 tasks
- 5 overdue suggests recent overcapacity
- Recommendation: Focus on 2-3 HIGH-value tasks, not 5+
```

#### 3. Optimizer

**What it looks for**:
- Which projects have highest ROI
- Where is effort most effective (velocity as proxy)
- Compounding value (what unlocks other work)

**Example interpretation**:
```
Portfolio optimization:
- SEA: 60% complete, 2.3 velocity = finish Week 2-3 high ROI
- qrcards: 25% complete, 0.5 velocity = fix overdue bugs prevents debt
- cookbooks: 0% complete, 0.0 velocity = low confidence until unblocked

Optimal allocation:
1. qrcards overdue (2 hours) - prevent escalation
2. SEA Week 2 (30 hours) - maintain momentum
3. cookbooks investigation (4 hours) - understand blocker
4. Buffer (4 hours) - unexpected issues
```

#### 4. Economizer

**What it looks for**:
- Minimum viable effort
- Where is waste occurring (0 velocity = possible waste)
- Most efficient path

**Example interpretation**:
```
Efficiency analysis:
- SEA: 2.3 tasks/week = efficient, continue
- qrcards: 0.5 tasks/week = investigate inefficiency
- cookbooks: 0.0 velocity = STOP adding tasks until unblocked

Economizer constraint:
"Do NOT add more cookbooks tasks until you complete at least 1.
0 velocity = adding tasks = waste."
```

#### 5. Experience-Based

**What it looks for**:
- Past patterns (what happened last time velocity was 0?)
- Historical success factors
- Recognizable failure modes

**Example interpretation**:
```
Pattern recognition:
- 0 velocity = usually blocked by external dependency or unclear requirements
- Overdue accumulation = usually overcommitted capacity
- High velocity = usually clear requirements + unblocked execution

Past lesson: Last time qrcards had overdue bugs, they escalated to
user complaints. Fix overdue first before new features.

Past lesson: Last time project had 0 velocity for 2+ weeks, it was
because requirements were unclear. Investigate cookbooks blocker.
```

---

## Example spawn-analysis Output

**Input**: Portfolio state showing SEA (good velocity), qrcards (overdue), cookbooks (stalled)

**Cards Executed**: Strategist, Capability Auditor, Optimizer, Economizer, Experience-Based, Synthesizer

**Output**:

```markdown
# Decision: Weekly Prioritization (2025-11-07)

## Recommendation

**Priority 1**: Fix qrcards overdue bugs (3 tasks, ~6 hours)
**Priority 2**: Continue SEA Week 2 (maintain 2.3 velocity, ~25 hours)
**Priority 3**: Investigate cookbooks blocker (1 hour diagnostic)
**Buffer**: 8 hours for unexpected issues

## Rationale

### The Strategist
qrcards overdue = customer-facing risk. SEA momentum is good (2.3 tasks/week),
continue to compound progress. cookbooks 0 velocity suggests blocker -
investigate before committing more time.

### Capability Auditor
5 overdue tasks = recent overcapacity. You can realistically complete 3 tasks
this week at current velocity. Don't overcommit again.

### Optimizer
Maximum portfolio value = fix qrcards debt (prevents escalation), continue
SEA (60% complete, finish strong), investigate cookbooks (unblock or deprioritize).

### Economizer
Most efficient: Fix qrcards fast (known issues), leverage SEA momentum
(2.3 velocity = efficient), STOP adding cookbooks tasks until 1 completes.

### Experience-Based
Past pattern: 0 velocity = blocker (requirements or dependency). Last qrcards
overdue escalated to user complaints. Fix overdue first.

### Synthesis
Clear priority: qrcards overdue (risk + fast), SEA continuation (momentum),
cookbooks investigation (understand blocker). Total: ~32 hours, 8 hour buffer.
```

---

## Portfolio State Indicators

### Velocity Interpretation

| Velocity | Interpretation | Recommended Action |
|----------|---------------|-------------------|
| **>2.0 tasks/week** | High momentum | Continue, don't disrupt |
| **1.0-2.0 tasks/week** | Steady progress | Maintain or accelerate |
| **0.5-1.0 tasks/week** | Slow progress | Investigate friction |
| **0.0 tasks/week** | Stalled | Find blocker BEFORE adding tasks |
| **Declining trend** | Losing momentum | Refocus or deprioritize |

### Overdue Interpretation

| Overdue Count | Interpretation | Recommended Action |
|--------------|---------------|-------------------|
| **0 overdue** | Capacity match | Continue current pace |
| **1-2 overdue** | Minor slip | Address quickly |
| **3-5 overdue** | Overcapacity | Reduce commitments |
| **>5 overdue** | Systemic problem | Stop adding, clear backlog |

### Completion Rate Interpretation

| Completion % | Interpretation | Recommended Action |
|-------------|---------------|-------------------|
| **>70%** | Nearing completion | Push to finish |
| **40-70%** | Mid-progress | Maintain momentum |
| **10-40%** | Early stages | Reassess scope/timeline |
| **<10%** | Just started | Validate approach early |

---

## Weekly Prioritization Workflow

### Monday Morning Routine

```bash
# 1. Export portfolio state
cd ~/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-export-script/src
python export_vikunja.py --output ~/spawn-analysis/portfolio-state.md

# 2. Navigate to spawn-analysis
cd ~/spawn-analysis/

# 3. Create decision (use Task tool or direct execution)
# Prompt: "Given portfolio-state.md, what should I prioritize this week?"

# 4. Execute 5-7 decision cards:
#    - The Strategist
#    - Capability Auditor
#    - Optimizer
#    - Economizer
#    - Experience-Based
#    - Synthesizer

# 5. Review recommendation

# 6. Update Vikunja based on decision
# Mark deprioritized tasks, adjust due dates, etc.
```

---

## Advanced: Trend Analysis

**Track velocity over time** to see project health trends:

```bash
# Weekly exports
mkdir -p ~/spawn-analysis/portfolio-history
python export_vikunja.py --format json --output ~/spawn-analysis/portfolio-history/$(date +%Y-%m-%d).json

# Compare week-over-week (manual or scripted)
# - Is SEA velocity increasing or decreasing?
# - Are overdue tasks accumulating?
# - Which projects are consistently 0 velocity?
```

**Use in spawn-analysis**:
```
Context: Portfolio velocity trends (last 4 weeks)

SEA: 1.8 → 2.1 → 2.3 → 2.5 (INCREASING) ✅
qrcards: 1.2 → 0.8 → 0.5 → 0.5 (DECLINING) ⚠️
cookbooks: 0.0 → 0.0 → 0.0 → 0.0 (STALLED) ❌

Question: Should I continue current allocation or reallocate?
```

---

## Integration with spawn-plans

**Bidirectional flow**:

```
spawn-plans (Tactical Detailer) → YAML → populate_vikunja.py → Vikunja
                                                                  ↓
                                                            (work happens)
                                                                  ↓
export_vikunja.py → portfolio-state.md → spawn-analysis → Priority decision
                                                                  ↓
                                                    (Update Vikunja priorities)
                                                                  ↓
                                              spawn-plans (next planning round)
```

**Example**:
1. **Week 0**: spawn-plans creates SEA Week 1-3 tasks → Vikunja
2. **Week 1**: Work on SEA, velocity = 2.3 tasks/week
3. **Week 2**: export_vikunja.py shows 60% Week 1 done
4. **Week 2**: spawn-analysis: "Continue SEA Week 2"
5. **Week 3**: export_vikunja.py shows overdue accumulating
6. **Week 3**: spawn-analysis: "Slow down, address overdue"
7. **Week 4**: spawn-plans Round 2: Adjust timeline based on actual velocity

---

## spawn-analysis Card Enhancements

**Potential new cards** that would benefit from portfolio data:

### The Portfolio Manager (Proposed)

**Philosophy**: Optimize across competing initiatives using portfolio theory

**Uses from portfolio export**:
- Velocity as proxy for ROI
- Overdue as proxy for risk
- Label distribution as proxy for diversification

**Example output**:
```
Portfolio optimization:
- 60% allocation to SEA (high velocity, momentum)
- 30% allocation to qrcards (overdue risk mitigation)
- 10% allocation to cookbooks (exploratory, capped until unblocked)

Rationale: Maintain momentum on winners (SEA), manage risk (qrcards),
limit exposure to stalled projects (cookbooks).
```

**When to play**: Multiple active projects, resource allocation decisions

---

## Troubleshooting

### Empty Portfolio Export

**Symptom**: Script runs but shows 0 projects

**Causes**:
1. API token invalid/expired
2. No projects in Vikunja yet
3. Permission issues

**Fix**:
```bash
# Test API connection
cd ~/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-api-wrapper/src
python test_token.py

# Create test project
python -c "from vikunja_wrapper import VikunjaClient; ..."
```

### Velocity Always 0

**Symptom**: All projects show 0.0 tasks/week

**Causes**:
1. No tasks marked done in last 4 weeks
2. Tasks marked done but missing `done_at` timestamp
3. Clock skew (server vs local time)

**Fix**: Mark some tasks as done in Vikunja, wait for sync

### spawn-analysis Can't Interpret Output

**Symptom**: Decision cards confused by portfolio data

**Causes**:
1. Too much detail (information overload)
2. Not enough context (cards need rationale)
3. Ambiguous metrics

**Fix**: Edit portfolio-state.md to highlight key issues:
```markdown
# Simplified for Decision

**Key Issue**: qrcards has 3 overdue bugs (customer-facing)
**Key Opportunity**: SEA has 2.3 velocity (momentum)
**Key Blocker**: cookbooks 0 velocity for 4 weeks

Question: What should I prioritize?
```

---

## Next Steps

1. **Test integration**: Export portfolio, feed to spawn-analysis
2. **Validate cards**: Do they produce useful recommendations?
3. **Iterate format**: Adjust export format based on card needs
4. **Automate workflow**: Script Monday morning routine
5. **Track effectiveness**: Do recommendations improve outcomes?

---

**Status**: Ready for integration testing
**Date**: 2025-11-07
**Next**: Export real portfolio → test with spawn-analysis cards
