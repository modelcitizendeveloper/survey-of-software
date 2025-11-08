# spawn-analysis Prompt Template

Copy this prompt when starting a spawn-analysis session to leverage Vikunja export data.

---

## Recommended Prompt

```
I need help prioritizing my work using evidence-based decision-making.

CONTEXT: Current Portfolio State

I've exported my complete Vikunja project management state with full metadata:

**Export Files**:
- JSON (complete): /home/ivanadmin/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-export-script/src/portfolio-complete.json
- Markdown (summary): /home/ivanadmin/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-export-script/src/portfolio-complete.md

**Portfolio Stats**:
- 41 projects across Foundations, Applications, Talks
- 105 total tasks (69 overdue, 102 pending)
- 17 tasks have source document references with evidence files
- Current velocity: Low (2.9% completion rate)

**Source Documents Available**:
The export includes file paths to evidence for 17 tasks:
- Project definitions: vikunja-tasks.yaml files
- Project folders: Full planning documentation
- Codebases: Where applicable (QRCards, SEA, etc.)

Example source doc structure:
{
  "source_documents": {
    "project_definition": "/home/ivanadmin/spawn-solutions/applications/qrcards/vikunja-tasks.yaml",
    "project_folder": "/home/ivanadmin/spawn-solutions/applications/qrcards/",
    "codebase": "/home/ivanadmin/qrcards/"
  }
}

TASK: Strategic Prioritization

Please help me decide what to prioritize this week by:

1. Reading the portfolio export (JSON or Markdown)
2. Analyzing the current state (overdue tasks, velocity, project health)
3. Following source_documents paths to review evidence for key projects
4. Executing decision cards (Strategist, Capability Auditor, Optimizer, etc.)
5. Providing a recommendation with rationale based on actual evidence

CONSTRAINTS:
- 40 hours available this week
- Need to address overdue tasks
- Want to maintain/build momentum
- Revenue-generating work preferred when feasible

SPECIFIC QUESTIONS:
- What are the highest-impact projects to focus on?
- Which overdue tasks are truly critical vs. can be deprioritized?
- Should I focus on clearing backlogs or starting new work?
- What evidence from source documents supports your recommendation?

Please start by reading portfolio-complete.json and providing your analysis.
```

---

## Alternative: Short Prompt

For quick prioritization sessions:

```
Load my Vikunja portfolio export and help me prioritize this week's work:

File: /home/ivanadmin/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-export-script/src/portfolio-complete.json

Key info:
- 105 tasks, 69 overdue
- 17 tasks have source document paths for evidence
- Need to decide: clear overdue backlog vs. new work

Execute decision cards with evidence from source_documents field.
What should I focus on?
```

---

## Scenario-Specific Prompts

### Scenario 1: Weekly Planning

```
Weekly prioritization using Vikunja export:

Export: portfolio-complete.json (path above)
Current state: 69 overdue tasks, low velocity
Question: What should I prioritize this week to maximize impact?

Use source documents to evaluate:
- inversefractional.com (CFO consulting - revenue?)
- QRCards (platform development - strategic?)
- Talks (PyCascades 2025, NWES 2026 - deadlines?)

Provide top 3 priorities with evidence-based rationale.
```

### Scenario 2: Project Selection

```
Help me choose between competing projects:

Export: portfolio-complete.json
Options with source docs:
1. inversefractional.com - CFO consulting business
2. QRCards - Platform for site building
3. Boutique Hotel Recommendations - QRCards deployment

Read source_documents for each:
- Business model (vikunja-tasks.yaml)
- Current state (project folder README)
- Technical readiness (codebase if available)

Which should I prioritize? Why? Show evidence.
```

### Scenario 3: Capacity Planning

```
Can I take on new work or should I focus on existing?

Export: portfolio-complete.json
Current: 102 pending tasks, 0.0 tasks/week velocity
Question: Do I have capacity for new projects?

Capability Auditor analysis:
- What's realistic given current velocity?
- Which existing work can be deprioritized?
- What evidence suggests I'm overcommitted?

Be honest about capacity constraints.
```

### Scenario 4: Revenue Focus

```
Prioritize revenue-generating work:

Export: portfolio-complete.json
Filter for revenue opportunities using source docs:
- inversefractional.com (CFO consulting)
- Decision Analysis (consulting service)
- QRCards (potential product revenue)

Rank by:
1. Revenue potential (from source docs)
2. Time to revenue
3. Current state/readiness

Provide evidence-based revenue roadmap.
```

---

## What spawn-analysis Can Do With This Data

### Direct Access

**Read the export**:
```python
import json
portfolio = json.load(open('portfolio-complete.json'))
```

**Find tasks with evidence**:
```python
for project in portfolio['projects']:
    for task in project['tasks']:
        if task.get('source_documents'):
            print(f"{task['title']}: {task['source_documents']['project_folder']}")
```

**Follow source document paths**:
```python
import yaml
definition_path = task['source_documents']['project_definition']
with open(definition_path) as f:
    evidence = yaml.safe_load(f)
# Now has full context for decision-making
```

### Decision Card Execution

**The Strategist**:
- Reviews project hierarchy
- Reads source docs for strategic positioning
- Evaluates long-term impact

**Capability Auditor**:
- Checks velocity metrics (0.0 tasks/week = overcommitted)
- Reviews overdue count (69 = capacity issue)
- Reality-checks feasibility

**Optimizer**:
- Analyzes task priority distribution
- Identifies highest-impact work from source docs
- Maximizes portfolio value

**Economizer**:
- Looks for quick wins
- Evaluates effort vs. impact
- Optimizes resource allocation

**Experience-Based**:
- Notes patterns (0% completion = blockers?)
- Identifies what's working vs. stalled
- Suggests based on past patterns

---

## Expected Output from spawn-analysis

Good spawn-analysis response should include:

**1. Evidence Cited**:
```
"After reviewing inversefractional.com/vikunja-tasks.yaml, I see:
- Revenue model: Fractional CFO services
- Current state: Learning lab experiments planned
- Blocker: No recent completions suggest capacity issue
Evidence: /home/ivanadmin/spawn-solutions/applications/inverse-fractional/"
```

**2. Quantitative Analysis**:
```
"Portfolio health metrics:
- 69/105 tasks overdue (66%) = serious backlog
- 0.0 tasks/week velocity = work not moving
- 17 projects with evidence = can make informed decisions"
```

**3. Specific Recommendation**:
```
"RECOMMENDATION: Focus on clearing critical overdue tasks first

Priority 1: [Specific task] - Evidence: [source doc finding]
Priority 2: [Specific task] - Evidence: [source doc finding]
Priority 3: [Specific task] - Evidence: [source doc finding]

DEPRIORITIZE: [Tasks with weak evidence or low impact]"
```

**4. Rationale**:
```
"Why this prioritization:
- Addresses capacity constraint (clear backlog)
- Evidence from source docs shows X is revenue-critical
- Builds momentum before starting new work"
```

---

## Tips for Effective spawn-analysis Sessions

**DO**:
- ✅ Point to specific export file paths
- ✅ Ask for evidence-based decisions
- ✅ Request source document review
- ✅ Provide constraints (time, capacity)
- ✅ Ask "why" - demand rationale

**DON'T**:
- ❌ Ask for decisions without context
- ❌ Ignore the source documents feature
- ❌ Accept recommendations without evidence
- ❌ Skip the velocity/capacity analysis
- ❌ Let spawn-analysis guess your priorities

---

## Files Mentioned in Prompts

**Main Export**:
- `/home/ivanadmin/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-export-script/src/portfolio-complete.json`

**Alternative Export** (same data, readable format):
- `/home/ivanadmin/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-export-script/src/portfolio-complete.md`

**Source Documents** (examples from export):
- `/home/ivanadmin/spawn-solutions/applications/inverse-fractional/vikunja-tasks.yaml`
- `/home/ivanadmin/spawn-solutions/applications/qrcards/vikunja-tasks.yaml`
- `/home/ivanadmin/qrcards/` (codebase)

**Export Script** (to regenerate):
- `/home/ivanadmin/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-export-script/src/export_vikunja.py`

---

## Regenerating Export

If you need fresh data:

```bash
cd /home/ivanadamin && source .venv/bin/activate
cd /home/ivanadmin/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-export-script/src

# Full portfolio
python export_vikunja.py --format json --output portfolio-complete.json

# Specific project (e.g., Applications)
python export_vikunja.py --project-id 13448 --output applications.json
```

---

**Created**: 2025-11-08
**Purpose**: Guide spawn-analysis sessions to leverage Vikunja export with source documents
**Key Feature**: Evidence-based decision-making using real project data
