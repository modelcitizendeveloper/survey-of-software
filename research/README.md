# Spawn Solutions Research System

**Purpose**: Centralized research tracking system for algorithm libraries (1.XXX), open standards (2.XXX), and managed services (3.XXX).

---

## Quick Start: Next Research

To find what research should be done next:

```bash
# View priority queue (ordered by importance)
cat research/RESEARCH-PRIORITIES.yaml

# View completed research count
cat research/COMPLETED-RESEARCH.yaml | grep "total_completed:"

# View all planned research
cat research/PLANNED-RESEARCH.yaml | grep "total_planned:"
```

**The top item in `RESEARCH-PRIORITIES.yaml` is always the next research to start.**

---

## Research Tracking Files

### 1. `COMPLETED-RESEARCH.yaml`
**Purpose**: Canonical record of all completed research experiments

**Format**:
```yaml
repository: spawn-solutions
total_completed: 70
research:
  - code: '1.002'
    title: fuzzy search
    description: Research on fuzzy search
    path: research/1.002-fuzzy-search
```

**Usage**:
- Updated AFTER experiment completion
- Source of truth for completion status
- Referenced by roadmaps for completion counts

### 2. `RESEARCH-PRIORITIES.yaml`
**Purpose**: Priority queue for next research (ordered by importance)

**Format**:
```yaml
queue:
  - code: '3.131'
    title: Team Task Management
    tier: 3
    status: not_started
    estimated_hours: 10-12
    rationale: HIGH - Team tier competitive analysis
    value: Collaboration features, permission models, per-seat pricing
```

**Usage**:
- **Consulted FIRST** when starting new research
- Top item = highest priority
- Updated as priorities shift
- Estimated hours guide time commitment

**When to update**:
- New trigger discovered (e.g., CFO forum post → 3.007 FP&A added to top)
- Application needs shift priorities
- Research completes → remove from queue, add to COMPLETED-RESEARCH.yaml

### 3. `PLANNED-RESEARCH.yaml`
**Purpose**: Comprehensive catalog of ALL planned research (157 items)

**Format**:
```yaml
repository: spawn-solutions
total_planned: 157
planned_research:
  - code: '1.001'
    title: Advanced sorting libraries
    tier: 'Tier 1: Algorithms & Libraries'
    roadmap: 1.001-099-ALGORITHM_ROADMAP.md
```

**Usage**:
- Reference list of all potential research
- NOT prioritized (see RESEARCH-PRIORITIES.yaml for priority order)
- Generated FROM roadmaps (plan/1.001-099-ALGORITHM_ROADMAP.md, etc.)
- Used to ensure roadmap coverage

---

## Research Workflow

### Starting New Research

1. **Check priority queue**:
   ```bash
   head -20 research/RESEARCH-PRIORITIES.yaml
   ```

2. **Validate top priority is still relevant**:
   - Has a new trigger emerged (forum post, product need)?
   - If yes, update RESEARCH-PRIORITIES.yaml to reorder

3. **Create experiment directory**:
   ```bash
   mkdir -p research/X.XXX-experiment-name/
   ```

4. **Follow MPSE methodology**:
   - S1: Rapid discovery (provider profiles)
   - S2: Comprehensive (feature matrix, pricing, integrations)
   - S3: Need-driven (5 generic business scenarios)
   - S4: Strategic (frameworks, vendor viability, 5-year outlook)

5. **Create metadata.yaml**:
   - See `research/3.007-fpa-platforms/metadata.yaml` as reference
   - Track completion status, deliverables, findings

### Completing Research

1. **Update completion status** in `metadata.yaml`:
   ```yaml
   experiment:
     status: "complete"
     completed: "2025-11-12"
   ```

2. **Add to COMPLETED-RESEARCH.yaml**:
   ```yaml
   - code: 'X.XXX'
     title: experiment name
     description: Brief description
     path: research/X.XXX-experiment-name
   ```

3. **Increment total_completed count**:
   ```yaml
   total_completed: 71  # was 70
   ```

4. **Remove from RESEARCH-PRIORITIES.yaml** (if present)

5. **Update roadmap** (plan/X.001-099-*_ROADMAP.md):
   - Change status from ❌ to ✅
   - Update completion date
   - Update completion count in roadmap summary

### Adding New Research to Queue

**When new research need identified**:

1. **Determine tier**: 1.XXX (library), 2.XXX (standard), 3.XXX (service)

2. **Check if already in PLANNED-RESEARCH.yaml**:
   ```bash
   grep -i "keyword" research/PLANNED-RESEARCH.yaml
   ```

3. **Add to RESEARCH-PRIORITIES.yaml** (ordered by priority):
   ```yaml
   - code: 'X.XXX'
     title: Experiment Name
     tier: X
     status: not_started
     estimated_hours: 8-10
     rationale: Why this is important NOW
     value: What we'll learn
   ```

4. **Add to roadmap** if not present:
   - Edit `plan/X.001-099-*_ROADMAP.md`
   - Add experiment with ❌ status
   - Increment total experiment count

5. **Add to PLANNED-RESEARCH.yaml** if not present

---

## Roadmap Integration

### Roadmap Files Reference These YAMLs

**Tier 1 (Algorithms)**: `plan/1.001-099-ALGORITHM_ROADMAP.md`
- Completion count: 30 complete (check COMPLETED-RESEARCH.yaml for 1.XXX codes)
- Priority experiments: Listed in roadmap, cross-check with RESEARCH-PRIORITIES.yaml

**Tier 2 (Open Standards)**: `plan/2.001-099-OPEN_STANDARDS_ROADMAP.md`
- Completion count: 8 complete (target achieved)
- Priority experiments: All 8 priority standards complete

**Tier 3 (Managed Services)**: `plan/3.001-099-MANAGED_SERVICES_ROADMAP.md`
- Completion count: 19 complete (check COMPLETED-RESEARCH.yaml for 3.XXX codes)
- Priority experiments: Check RESEARCH-PRIORITIES.yaml for current queue

### When Roadmap Says "Next Steps"

**Ignore generic "Next Steps" sections in roadmaps.**

**Instead, consult**:
1. `research/RESEARCH-PRIORITIES.yaml` (priority order)
2. Application needs (e.g., `/applications/project-management/` may drive priorities)
3. Recent triggers (forum posts, product decisions, market analysis)

**Roadmap "Next Steps" are historical snapshots, not current priorities.**

---

## Research Statistics (as of Nov 12, 2025)

**Completed**: 70 experiments
- Tier 1 (1.XXX): 30 experiments
- Tier 2 (2.XXX): 8 experiments
- Tier 3 (3.XXX): 32 experiments

**Planned**: 157 total research items across all tiers

**In Progress**:
- 3.502 ERP Platforms
- 3.503 HRIS/HCM
- 3.031 Object Storage (substantial progress)
- 3.064 Metadata Management (S1 complete)

**Priority Queue**: 8 items in RESEARCH-PRIORITIES.yaml (ordered by urgency)

---

## File Maintenance

### Who Updates These Files?

**COMPLETED-RESEARCH.yaml**:
- Updated by: Researcher (on experiment completion)
- Frequency: After each experiment completes
- Validation: Count matches roadmap completion marks (✅)

**RESEARCH-PRIORITIES.yaml**:
- Updated by: Product/research lead (as priorities shift)
- Frequency: Weekly or when triggers emerge
- Validation: Top item should always be "what's next"

**PLANNED-RESEARCH.yaml**:
- Updated by: Roadmap maintainer (when roadmaps change)
- Frequency: When new categories added to roadmaps
- Validation: Count should match sum of all roadmap items

### Audit Process

**Monthly audit** (recommended):

1. **Verify counts**:
   ```bash
   # Count completed directories
   find research -name "metadata.yaml" -type f | wc -l

   # Compare to COMPLETED-RESEARCH.yaml total_completed
   grep "total_completed:" research/COMPLETED-RESEARCH.yaml
   ```

2. **Cross-check roadmap completion marks**:
   - Count ✅ marks in each roadmap
   - Should match COMPLETED-RESEARCH.yaml count for that tier

3. **Validate priority queue**:
   - Is top item still highest priority?
   - Have new triggers emerged?
   - Reorder if needed

4. **Update planned count**:
   - Count all items in roadmaps (✅ + ❌)
   - Update PLANNED-RESEARCH.yaml total_planned

---

## Examples

### Example 1: Starting Next Research

**User says**: "next research"

**Response**:
1. Read `research/RESEARCH-PRIORITIES.yaml`
2. Identify top item: `3.131 Team Task Management`
3. Confirm: "Starting 3.131 Team Task Management (Asana, ClickUp, Linear analysis). Estimated 10-12 hours."
4. Create `research/3.131-team-task-management/` directory
5. Begin S1 rapid discovery

### Example 2: Completing Research

**After finishing 3.131**:

1. Update `research/3.131-team-task-management/metadata.yaml`:
   ```yaml
   status: "complete"
   completed: "2025-11-15"
   ```

2. Add to `research/COMPLETED-RESEARCH.yaml`:
   ```yaml
   - code: '3.131'
     title: team task management
     description: Research on team task management
     path: research/3.131-team-task-management
   ```

3. Update count: `total_completed: 71`

4. Remove from `research/RESEARCH-PRIORITIES.yaml`

5. Update `plan/3.001-099-MANAGED_SERVICES_ROADMAP.md`:
   - Change 3.131 status from ❌ to ✅
   - Update completion count: 19 → 20

### Example 3: New Trigger Discovered

**CFO forum post mentions "FP&A + HRIS integration critical"**:

1. Research trigger validates: 3.503 HRIS/HCM is prerequisite for 3.007 FP&A

2. Add to top of `research/RESEARCH-PRIORITIES.yaml`:
   ```yaml
   - code: '3.503'
     title: HRIS/HCM Platforms
     tier: 3
     status: not_started
     estimated_hours: 8-10
     rationale: CRITICAL - FP&A platforms require HRIS integration
     value: Rippling, Gusto, Workday analysis for FP&A selection
   ```

3. Reorder queue (3.503 now highest priority)

4. Next "next research" command starts 3.503

---

## Related Documentation

**Roadmaps**:
- `plan/1.001-099-ALGORITHM_ROADMAP.md` - Tier 1 algorithms & libraries
- `plan/2.001-099-OPEN_STANDARDS_ROADMAP.md` - Tier 2 open standards
- `plan/3.001-099-MANAGED_SERVICES_ROADMAP.md` - Tier 3 managed services

**Methodology**:
- `plan/MPSE_METHODOLOGY.md` (if exists) - S1-S4 research process
- Individual `metadata.yaml` files - Experiment tracking

**Applications**:
- `/applications/{app}/` - Application-specific research needs
- May drive priorities in RESEARCH-PRIORITIES.yaml

---

**Last Updated**: 2025-11-12
**Maintained By**: Research lead
**Authority**: Canonical source for "next research" decisions
