# Task Granularity for AI-Assisted Development

**Key insight**: With AI-generated code, bottleneck is NOT coding speed—it's strategic decisions, integration, and validation.

---

## Task Size Principles

### ❌ Too Granular (Pre-AI era)
```yaml
tasks:
  - title: "Create main.py"
  - title: "Write parse_config() function"
  - title: "Add error handling to validator"
  - title: "Create test_validator.py"
  - title: "Write docstrings"
```
**Problem**:
- AI can generate 10 files in same time as 1
- Context switching overhead > coding time
- Loses strategic view
- Creates noise in velocity metrics

### ✅ Right Granularity (AI era)
```yaml
tasks:
  - title: "Sprint 1: Foundation & Core Structure"
    description: |
      <strong>Goal:</strong> Runnable CLI with basic orchestration<br><br>
      <strong>Deliverables:</strong><br>
      - Project structure (src/, tests/, docs/)<br>
      - CLI entry point with argument parsing<br>
      - Core orchestrator skeleton<br>
      - CI/CD pipeline<br>
      - Test harness setup<br><br>
      <strong>Definition of Done:</strong><br>
      - `sea --help` works<br>
      - Tests run in CI<br>
      - README has quick start<br><br>
      <strong>Estimated time:</strong> 1 week (10-15 hours)
    due_date: "2025-11-15"
    labels: ["Next Action", "@DeepWork", "Code"]
```

---

## Granularity Guidelines

### Rule of Thumb: **1 task = 1 sprint/week/phase**

| Task Duration | When to Use | Example |
|--------------|-------------|---------|
| **1-2 weeks** | Ideal for sprints | "Sprint 1: Foundation", "Week 2: Pattern Library" |
| **3-5 days** | Ideal for phases | "Phase 1: Data Model", "Phase 2: API Integration" |
| **1-2 days** | Minimum size | "Spike: Research rollback patterns" |
| **< 1 day** | Too small | ❌ Don't create tasks for individual files/functions |

### Task Types & Expected Size

**Development tasks** (1-2 weeks):
- "Sprint 1: Core Orchestrator"
- "Week 3: Template System Implementation"
- "Phase 2: Database Integration"

**Research tasks** (2-5 days):
- "Research: Compare Alembic vs Flyway rollback patterns"
- "Spike: Evaluate YAML vs TOML for config"
- "Investigation: Root cause of migration failures"

**Integration tasks** (3-5 days):
- "Integrate Vikunja API with spawn-plans"
- "Connect export script to spawn-analysis pipeline"

**Bug fixes** (1-3 days):
- "Fix: Schema validation failing on complex patterns"
- "Resolve: CI pipeline timeout issues"

**Documentation** (1-2 days):
- "Document: API reference for pattern library"
- "Write: Quick start guide for new users"

---

## What Goes in Task Description

**Include** (Strategic/Integration):
```yaml
description: |
  <strong>Goal:</strong> What outcome are we achieving?<br><br>

  <strong>Context:</strong><br>
  - Why this matters strategically<br>
  - Dependencies on other work<br>
  - Decisions that need making<br><br>

  <strong>Deliverables:</strong><br>
  - Working feature X<br>
  - Test coverage >80%<br>
  - Documentation updated<br><br>

  <strong>Key Decisions:</strong><br>
  - Which library to use? (spawn-solutions research)<br>
  - Architecture pattern? (review spawn-plans)<br><br>

  <strong>Integration Points:</strong><br>
  - Must work with existing Y<br>
  - API contract with Z<br><br>

  <strong>Definition of Done:</strong><br>
  - Acceptance criteria (specific, testable)<br>
  - CI passing<br>
  - Deployed to staging<br><br>

  <strong>Estimated time:</strong> X hours/days
```

**Don't Include** (Implementation Details):
```yaml
# ❌ Don't specify:
# - Exact function names
# - File structure details
# - Line-by-line pseudocode
# - Implementation approach (let AI suggest)

# These are AI's job, not yours
```

---

## AI-Era Task Decomposition

### Old Way (Pre-AI)
```
Project: Add Rollback Feature
├── Research Alembic (2 days)
├── Research Flyway (2 days)
├── Design CLI interface (1 day)
├── Create rollback.py (1 day)
├── Write rollback_manager.py (1 day)
├── Add error handling (0.5 days)
├── Write tests (1 day)
├── Write docs (0.5 days)
└── Integration testing (1 day)
= 10 tasks, 10 days
```

### New Way (AI-Era)
```
Project: Add Rollback Feature
├── Sprint 1: Research & Design (3-5 days)
│   Goal: Understand rollback patterns, design approach
│   Deliverables: Design doc, API contract, decision on approach
│
├── Sprint 2: Core Implementation (5-7 days)
│   Goal: Working rollback functionality
│   Deliverables: CLI works, tests pass, docs updated
│
└── Sprint 3: Integration & Polish (2-3 days)
    Goal: Production-ready
    Deliverables: Integrated with orchestrator, edge cases handled, deployed
= 3 tasks, 10-15 days
```

**Why better**:
- Strategic focus (What to build, not how)
- Reduces context switching
- AI handles implementation details
- Clear deliverables per sprint
- Easier to track velocity (3 sprints vs 10 micro-tasks)

---

## Mapping to spawn-plans Tactical Detailer

**Tactical Detailer already outputs sprint-level tasks**:

```yaml
# Good Tactical Detailer output (Week-level)
tasks:
  - title: "Week 1: Project Foundation"
    description: |
      <strong>Goal:</strong> Development environment ready<br>
      <strong>Tasks:</strong> Git, Python structure, pytest, CI/CD<br>
      <strong>Deliverables:</strong> sea/ package, CI passing<br>
      <strong>Estimated time:</strong> 10-15 hours
    due_date: "2025-11-14"
    labels: ["Next Action", "@DeepWork"]

  - title: "Week 2: Pattern & Template Structure"
    description: |
      <strong>Goal:</strong> Pattern library functional<br>
      <strong>Tasks:</strong> YAML patterns, Jinja templates, 1 complete pattern<br>
      <strong>Deliverables:</strong> Pattern lib, template lib<br>
      <strong>Estimated time:</strong> 12-15 hours
    due_date: "2025-11-21"
    labels: ["Next Action", "@DeepWork"]
```

**Don't break down further** unless:
- Week-long task is truly blocked and you need smaller chunk to unblock
- You discover task is actually 2 separate initiatives
- Strategic pivot requires re-scoping

---

## GTD Capture at Right Granularity

### Capture Pass 1: Scan for Projects (Not Tasks)
```bash
# Looking for TODO comments:
cd applications/schema-evolution-automation
grep -r "TODO" .

# Found:
# TODO: Implement rollback
# TODO: Add migration validation
# TODO: Support multi-DB backends
# TODO: Improve error messages
# TODO: Add progress bars
# TODO: Write API docs
```

### Capture Pass 2: Group into Sprints
```yaml
# ❌ Don't create 6 separate tasks from 6 TODOs

# ✅ Group into 2-3 sprint-level tasks:
tasks:
  - title: "Sprint: Rollback & Validation Features"
    description: |
      Implement rollback + migration validation<br>
      (Addresses: TODO rollback, TODO validation)
    labels: ["Next Action", "@DeepWork"]

  - title: "Sprint: Multi-DB & Error Handling"
    description: |
      Support multiple backends + better error UX<br>
      (Addresses: TODO multi-DB, TODO error messages, TODO progress bars)
    labels: ["Someday/Maybe", "@DeepWork"]

  - title: "Documentation Sprint"
    description: |
      API docs, guides, examples<br>
      (Addresses: TODO API docs)
    labels: ["Waiting For", "Writing"]
```

---

## Velocity Metrics at Sprint Level

**Why sprint-level tasks improve metrics**:

### File-Level Tracking (Bad)
```
Week 1: Completed 47 tasks
Week 2: Completed 12 tasks
Week 3: Completed 65 tasks

Velocity: Meaningless (tasks vary wildly in size)
```

### Sprint-Level Tracking (Good)
```
Week 1: Completed 1 sprint (Foundation)
Week 2: Completed 0.5 sprints (Pattern Library - in progress)
Week 3: Completed 1 sprint (Core Orchestrator)

Velocity: ~1 sprint/week, consistent and predictable
```

**spawn-analysis can actually use this**:
- "Project A: 2.5 sprints/month velocity"
- "Project B: 0.5 sprints/month velocity → investigate blocker"

---

## When to Break Down Further

**Situations where smaller tasks make sense**:

### 1. **Blocked Sprint - Need Quick Win**
```yaml
# Original (blocked):
- title: "Sprint 2: Pattern Library Implementation"
  labels: ["Blocked"]  # Waiting on design decisions

# Break into immediate action:
- title: "Spike: Test 3 YAML parsing libraries"
  labels: ["Next Action", "@Quick"]  # Can do this now

# Rest stays blocked:
- title: "Sprint 2: Pattern Library (pending spike results)"
  labels: ["Blocked"]
```

### 2. **Research Before Build**
```yaml
# Don't combine research + build in one sprint:

# ✅ Separate:
- title: "Research: Rollback pattern options"
  labels: ["Next Action", "Research"]

- title: "Sprint: Implement rollback (after research)"
  labels: ["Waiting For", "Code"]
```

### 3. **Multi-Phase Epic**
```yaml
# Epic: "Add Multi-Database Support"
# Don't make 1 task, make 3 sprints:

- title: "Sprint 1: PostgreSQL + MySQL Support"
  labels: ["Next Action"]

- title: "Sprint 2: SQLite + SQL Server Support"
  labels: ["Someday/Maybe"]

- title: "Sprint 3: NoSQL Support (MongoDB, DynamoDB)"
  labels: ["Someday/Maybe"]
```

---

## Examples by Application Type

### Schema Evolution Automation (CLI Tool)
```yaml
# Good granularity:
- "Sprint: Core Orchestrator (CLI + basic flow)"
- "Sprint: Pattern Library System"
- "Sprint: Migration Execution Engine"
- "Sprint: Rollback Capability"
- "Documentation Sprint"
```

### Cookbooks (Web App)
```yaml
# Good granularity:
- "Sprint: Recipe CRUD API"
- "Sprint: Search & Filter UI"
- "Sprint: User Authentication"
- "Sprint: Recipe Collections Feature"
- "Performance Sprint (caching, optimization)"
```

### QRCards (System Integration)
```yaml
# Good granularity:
- "Sprint: DAP Processor Modernization"
- "Sprint: Database Schema Migration"
- "Sprint: API Layer Refactor"
- "Integration Sprint: Connect new components"
```

### spawn-analysis (Decision Tool)
```yaml
# Good granularity:
- "Sprint: Add 3 new decision cards"
- "Sprint: Portfolio export integration"
- "Sprint: Improve card synthesis logic"
```

---

## Template: Sprint-Level Task

```yaml
tasks:
  - title: "Sprint [N]: [Outcome/Feature Name]"
    description: |
      <strong>Goal:</strong> [One sentence - what we're achieving]<br><br>

      <strong>Why Now:</strong> [Strategic context]<br><br>

      <strong>Scope:</strong><br>
      - [Major component 1]<br>
      - [Major component 2]<br>
      - [Major component 3]<br><br>

      <strong>Out of Scope:</strong><br>
      - [What we're explicitly NOT doing]<br><br>

      <strong>Key Decisions Needed:</strong><br>
      - [Decision 1] → Check spawn-solutions research<br>
      - [Decision 2] → Run spawn-analysis if strategic<br><br>

      <strong>Integration Points:</strong><br>
      - [What this connects to]<br><br>

      <strong>Deliverables:</strong><br>
      - [ ] Working feature X<br>
      - [ ] Tests >80% coverage<br>
      - [ ] Docs updated<br>
      - [ ] CI passing<br>
      - [ ] Deployed to staging<br><br>

      <strong>Estimated time:</strong> [1-2 weeks / 10-20 hours]

    due_date: "2025-11-[DD]"
    priority: 0
    labels:
      - "Next Action"
      - "@DeepWork"
      - "Code"
```

---

## Quick Reference

**Task size decision tree**:
```
Can AI generate most of the code?
├─ YES → Sprint-level task (1-2 weeks)
└─ NO → Is it research/decision-making?
    ├─ YES → Research task (2-5 days)
    └─ NO → Is it integration work?
        ├─ YES → Integration task (3-5 days)
        └─ NO → Bug/doc task (1-2 days)

Never go smaller than 1 day of work.
```

**Labels by task size**:
- **1-2 weeks**: Sprint tasks → `@DeepWork` (need sustained focus)
- **3-5 days**: Phase tasks → `@Computer` (need dedicated time)
- **1-2 days**: Research/bugs → `@Quick` if truly <4 hours, else `@Computer`

**GTD + AI**:
- Capture: Look for PROJECTS (multi-sprint outcomes), not individual TODOs
- Clarify: Group related work into sprints
- Organize: Sprint tasks in Vikunja, AI handles files/functions
- Engage: Work at sprint level, let AI handle implementation

---

**Status**: Production guidance
**Date**: 2025-11-07
**Applies to**: All applications/ projects with AI-assisted development
**Result**: Higher-level tasks, better velocity tracking, less noise, more strategic focus
