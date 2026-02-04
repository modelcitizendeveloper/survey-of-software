# GTD Capture: Applications Portfolio

**Goal**: Capture EVERYTHING - all open items across all applications into Vikunja

---

## Structure

```
applications/
├── vikunja-labels.yaml              # Shared labels template (copy into each app)
├── <app-name>/
│   └── vikunja-tasks.yaml          # Per-application tasks
└── VIKUNJA_GTD_CAPTURE.md          # This guide
```

**Each application gets**:
- Separate Vikunja project (one per application)
- Separate YAML file (`applications/<app-name>/vikunja-tasks.yaml`)
- Shared labels (copy from `vikunja-labels.yaml` template)

---

## Workflow

### Step 1: GTD Capture for Each Application

For each application directory, create a capture list:

```bash
# 1. Go to application directory
cd applications/<app-name>

# 2. Search for open items
grep -r "TODO" . 2>/dev/null || echo "No TODOs"
grep -r "FIXME" . 2>/dev/null || echo "No FIXMEs"
grep -r "HACK" . 2>/dev/null || echo "No HACKs"

# 3. Check for README, ROADMAP, STATUS files
ls -la README* ROADMAP* STATUS* TODO* 2>/dev/null

# 4. List directories to understand structure
find . -type d -maxdepth 2

# 5. Document findings in vikunja-tasks.yaml
```

### Step 2: Create Application YAML

Create `applications/<app-name>/vikunja-tasks.yaml`:

```yaml
project:
  title: "<Application Name>"
  description: "<Brief 1-2 sentence description>"

labels:
  # Copy ALL labels from applications/vikunja-labels.yaml
  - title: "Blocked"
    hex_color: "e74c3c"
  # ... (copy all 23 labels)

tasks:
  - title: "GTD: Capture all open items"
    description: |
      <strong>Goal:</strong> Inventory all TODO, FIXME, open issues<br><br>
      <strong>Sources:</strong><br>
      - Code comments (TODO, FIXME, HACK)<br>
      - README files<br>
      - ROADMAP/STATUS files<br>
      - Mental notes<br><br>
      <strong>Output:</strong> Complete task list in Vikunja
    due_date: "2025-11-09"
    priority: 0
    labels:
      - "Research"
      - "Quick Win"

  # Add more tasks as you discover them...
```

### Step 3: Populate Vikunja

```bash
cd ~/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-populate-script/src

# Validate first
python populate_vikunja.py --dry-run ~/spawn-solutions/applications/<app-name>/vikunja-tasks.yaml

# Populate
python populate_vikunja.py --verbose ~/spawn-solutions/applications/<app-name>/vikunja-tasks.yaml
```

### Step 4: Work in Vikunja

Open https://app.vikunja.cloud and:
- Add more tasks as you discover them
- Organize by labels (status, priority, type, effort, phase)
- Set due dates
- Mark tasks done as you complete them

---

## Applications Inventory

Based on `applications/` directory scan (2025-11-07):

| Application | Status | Description | Priority |
|-------------|--------|-------------|----------|
| **boutique-hotel-recs** | Unknown | Hotel recommendations | TBD |
| **business-database** | Unknown | Business data management | TBD |
| **cookbooks** | Active | Cookbooks application | High |
| **elevator-project** | Unknown | Elevator scheduling simulation | Medium |
| **intelligence-portal** | Unknown | Intelligence/research portal | TBD |
| **inverse-fractional** | Unknown | Inverse fractional application | TBD |
| **org-chart** | Unknown | Organization chart tool | TBD |
| **project-management** | Active | PM tools integration | High |
| **qrcards** | Active | QR card system | High |
| **research-lineage-system** | Unknown | Research lineage tracking | TBD |
| **schema-evolution-automation** | Active | SEA - Database schema evolution | Critical |
| **spawn** | Active | Spawn CLI/framework | High |
| **spawn-analysis** | Active | Decision analysis cards | High |
| **spawn-experiments** | Active | Method 1-4 implementations | High |
| **spawn-solutions** | Active | Research & discovery (S1-S4) | High |
| **werise** | Unknown | WeRise application | TBD |

---

## Suggested Order (GTD Capture)

**Phase 1: Critical & Active** (Do first)
1. schema-evolution-automation (SEA) - Critical, in active development
2. qrcards - High priority, active
3. cookbooks - High priority, active
4. spawn - Framework foundation
5. spawn-analysis - Active decision tool
6. spawn-solutions - Active research

**Phase 2: Infrastructure**
7. spawn-experiments - Method implementations
8. project-management - PM integration (just completed!)

**Phase 3: Backlog**
9. elevator-project - Simulation project
10. inverse-fractional - Needs investigation
11. boutique-hotel-recs - Needs investigation
12. business-database - Needs investigation
13. intelligence-portal - Needs investigation
14. org-chart - Needs investigation
15. research-lineage-system - Needs investigation
16. werise - Needs investigation

---

## Template: Quick Start for One App

```bash
# Example: Capture schema-evolution-automation

# 1. Create YAML file
cat > applications/schema-evolution-automation/vikunja-tasks.yaml <<'EOF'
project:
  title: "Schema Evolution Automation (SEA)"
  description: "Stateless orchestrator CLI for database schema evolution"

labels:
  # Copy from applications/vikunja-labels.yaml
  - title: "Blocked"
    hex_color: "e74c3c"
  - title: "Feature"
    hex_color: "9b59b6"
  # ... (copy all labels)

tasks:
  - title: "GTD: Capture all SEA open items"
    description: "Inventory TODO comments, roadmap items, open issues"
    due_date: "2025-11-09"
    priority: 0
    labels:
      - "Research"
      - "Quick Win"
EOF

# 2. Populate Vikunja
cd ~/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-populate-script/src
python populate_vikunja.py --verbose ~/spawn-solutions/applications/schema-evolution-automation/vikunja-tasks.yaml

# 3. Open Vikunja and start adding tasks
```

---

## Notes

**Why separate projects?**
- Each application is independent
- Different timelines/priorities
- Easier to archive completed projects
- Cleaner portfolio view

**Why shared labels?**
- Consistency across projects
- Easier to filter across portfolio ("Show me all Blocked tasks")
- Standard vocabulary

**Labels to copy** (23 total):
- Status: Blocked, In Progress, Waiting, Ready (4)
- Priority: Critical, High Priority, Low Priority (3)
- Type: Bug, Feature, Refactor, Documentation, Research, Infrastructure (6)
- Effort: Quick Win, Small, Medium, Large (4)
- Phase: Planning, Development, Testing, Deployment, Maintenance (5)

**Next steps**:
1. Start with schema-evolution-automation (critical)
2. Do GTD capture: grep for TODO/FIXME, check READMEs
3. Create vikunja-tasks.yaml with initial capture
4. Populate Vikunja
5. Repeat for other active projects (qrcards, cookbooks, spawn-*)

---

**Status**: Ready for GTD capture
**Date**: 2025-11-07
**Next**: Create vikunja-tasks.yaml for schema-evolution-automation
