# Quick Start: Vikunja Project Management for Other Repos

**Date**: November 8, 2025
**Audience**: AI agents working in other repositories (qrcards, spawn-experiments, etc.)
**Purpose**: Get started with Vikunja project management without reading 20+ docs

---

## TL;DR - The Essentials

1. **All projects organize into 3-tier hierarchy by work context**:
   - 🔵 **Foundations** (ID: 13447) - Capability development (spawn-* ecosystem, research)
   - 🟢 **Applications** (ID: 13448) - Capability application (products, tools)
   - 🔴 **Clients** (ID: 13449) - Customer-facing work (consulting, sites)

2. **To add a new project to Vikunja**:
   - Create `vikunja-tasks.yaml` in your repo
   - Run the populate script
   - Complete your GTD capture task

3. **All tools live in spawn-solutions**:
   - API Wrapper: `~/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-api-wrapper/`
   - Populate Script: `~/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-populate-script/`

---

## Step 1: Understand the Hierarchy

**Question**: Which parent project does your work belong under?

```
🔵 FOUNDATIONS (ID: 13447)
   Purpose: Building capabilities - research, infrastructure, methodology
   Examples: spawn-solutions, spawn-experiments, spawn-analysis, spawn-patents

🟢 APPLICATIONS (ID: 13448)
   Purpose: Applying capabilities - products, tools, internal systems
   Examples: qrcards, schema-evolution-automation, elevator-project

🔴 CLIENTS (ID: 13449)
   Purpose: Customer-facing - consulting, client sites, deliverables
   Examples: decision-analysis, ivantohelpyou, model-citizen-developer
```

**Rule**: Pick the parent that matches your **work context**, not your tech stack.

---

## Step 2: Create Your YAML File

Create `vikunja-tasks.yaml` in your repo root (or wherever makes sense):

```yaml
# Example: ~/qrcards/vikunja-tasks.yaml

project:
  title: "QRCards"
  description: "QR code-based content delivery platform"
  parent_project_id: 13448  # Applications - capability application
  hex_color: "#9b59b6"      # Optional: purple for content systems

tasks:
  - title: "GTD Capture: Review QRCards architecture and open items"
    description: |
      <strong>Goal:</strong> Capture all open items for QRCards<br><br>
      <strong>Steps:</strong><br>
      - Review current architecture<br>
      - List pending features<br>
      - Document known bugs<br>
      - Identify tech debt<br><br>
      <strong>Deliverables:</strong><br>
      - Complete task list in Vikunja
    due_date: "2025-11-09"
    priority: 0
```

**Key fields**:
- `parent_project_id`: 13447 (Foundations), 13448 (Applications), or 13449 (Clients)
- `hex_color`: Optional, any valid hex color (with or without #)
- First task should be a GTD capture task

---

## Step 3: Populate Into Vikunja

```bash
# From anywhere, run:
cd ~/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-populate-script/src

# Activate venv (if not already active)
source ~/.venv/bin/activate

# Populate your project
python populate_vikunja.py --verbose /path/to/your/vikunja-tasks.yaml

# Example for qrcards:
python populate_vikunja.py --verbose ~/qrcards/vikunja-tasks.yaml
```

**Expected output**:
```
✅ Created project: QRCards (ID: 13XXX)
✅ Created task: GTD Capture: Review QRCards architecture... (ID: XXXXX)
```

---

## Step 4: Complete GTD Capture

Your project now exists in Vikunja with one task: the GTD capture task.

**What is GTD Capture?**
- Review all current work in your repo
- Break down into actionable tasks
- Add all tasks to Vikunja (either via YAML + re-populate, or via Vikunja UI)
- Result: Complete view of all work for this project

**After GTD Capture**, your project transforms from:
```
QRCards
└── GTD Capture: Review QRCards architecture...
```

To:
```
QRCards
├── ✅ GTD Capture: Review QRCards architecture... (DONE)
├── Implement JWT authentication
├── Add PostgreSQL support
├── Fix QR code generation bug
├── Write API documentation
└── Deploy to production
```

---

## Environment Setup

The populate script needs environment variables. They're already configured in `~/spawn-solutions/.env`:

```bash
VIKUNJA_BASE_URL=https://app.vikunja.cloud
VIKUNJA_API_TOKEN=tk_...
```

**No action needed** - the script auto-detects this .env file.

---

## YAML Schema Reference

```yaml
project:
  title: "Project Name"                    # Required
  description: "What this project does"    # Optional
  parent_project_id: 13447|13448|13449    # Optional (defaults to top-level)
  hex_color: "#rrggbb"                     # Optional (any hex color)

tasks:
  - title: "Task title"                    # Required
    description: |                         # Optional (supports HTML)
      <strong>Bold text</strong><br>
      - Bullet points
    due_date: "YYYY-MM-DD"                 # Optional
    priority: 0|1|2|3|4|5                  # Optional (0=none, 5=urgent)
    labels: ["label1", "label2"]           # Optional

labels:                                    # Optional section
  - title: "bug"
    hex_color: "#e74c3c"
```

**Full schema**: See `~/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-populate-script/SCHEMA.md`

---

## Common Use Cases

### Use Case 1: New Application Project

```bash
# 1. Create YAML in your repo
cat > ~/my-new-app/vikunja-tasks.yaml << 'EOF'
project:
  title: "My New App"
  description: "Description of what it does"
  parent_project_id: 13448  # Applications

tasks:
  - title: "GTD Capture: Review My New App requirements"
    description: "Document all open items"
    due_date: "2025-11-10"
    priority: 0
EOF

# 2. Populate
cd ~/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-populate-script/src
python populate_vikunja.py ~/my-new-app/vikunja-tasks.yaml

# 3. Complete GTD capture in Vikunja UI or add more tasks to YAML
```

### Use Case 2: Client Project (QRCards Site)

```yaml
# ~/qrcards/content/client-name/vikunja-tasks.yaml
project:
  title: "client-name"
  description: "Client website via QRCards"
  parent_project_id: 13449  # Clients
  hex_color: "#e74c3c"      # Red for clients
```

### Use Case 3: Research Experiment (Foundations)

```yaml
# ~/spawn-solutions/research/1.XXX-topic/vikunja-tasks.yaml
project:
  title: "1.XXX Topic Research"
  description: "Discovery and implementation"
  parent_project_id: 13447  # Foundations
  hex_color: "#3498db"      # Blue for foundations
```

---

## Updating Existing Projects

If you need to add more tasks after initial population:

**Option 1: Edit YAML + Re-populate** (recommended for bulk changes)
```bash
# Edit your vikunja-tasks.yaml to add tasks
# Then re-run populate script
python populate_vikunja.py ~/your-repo/vikunja-tasks.yaml
# The script is idempotent - won't duplicate existing tasks
```

**Option 2: Use Vikunja UI** (recommended for quick adds)
- Go to https://app.vikunja.cloud
- Navigate to your project
- Add tasks directly

**Option 3: Use API Wrapper** (for programmatic access)
```python
# ~/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-api-wrapper/
from vikunja_wrapper import VikunjaClient

client = VikunjaClient(
    base_url="https://app.vikunja.cloud",
    token=os.environ["VIKUNJA_API_TOKEN"]
)

# Add task to existing project
task = client.tasks.create(
    project_id=13454,  # Your project ID
    title="New task",
    description="Task details"
)
```

---

## Troubleshooting

### Error: "VIKUNJA_API_TOKEN not found"
**Fix**: The .env file should be at `~/spawn-solutions/.env`. Check it exists and contains the token.

### Error: "Module not found: vikunja_wrapper"
**Fix**: Make sure you're using the venv that has all dependencies:
```bash
source ~/.venv/bin/activate
cd ~/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-populate-script/src
```

### Error: "Invalid parent_project_id"
**Fix**: Use one of the three valid parent IDs:
- 13447 (Foundations)
- 13448 (Applications)
- 13449 (Clients)

### Tasks are duplicating when I re-populate
**Issue**: The script matches tasks by title. If you change the title, it creates a new task.
**Fix**: Keep task titles consistent, or delete old tasks in Vikunja UI before re-populating.

---

## Current Hierarchy State (as of Nov 8, 2025)

```
🔵 Foundations/ (4 projects)
   ├── spawn
   ├── spawn-analysis
   ├── spawn-experiments
   └── spawn-solutions

🟢 Applications/ (12 projects)
   ├── Boutique Hotel Recommendations
   ├── Business Database
   ├── Cookbooks Content System
   ├── Elevator Project
   ├── Intelligence Portal
   ├── inverse-fractional
   ├── Org Chart
   ├── Project Management - Vikunja
   ├── QRCards
   ├── Research Lineage System
   ├── Schema Evolution Automation (SEA)
   └── WeRise

🔴 Clients/ (6 projects)
   ├── convention-city-seattle
   ├── decision-analysis
   ├── inverse-fractional (site)
   ├── ivantohelpyou
   ├── model-citizen-developer
   └── taelyen
```

**Total**: 22 child projects + 3 parent projects = 25 projects in Vikunja

---

## For More Details

**Full Documentation** (in spawn-solutions):
- API Wrapper: `research/1.131-project-management/02-implementations/vikunja-api-wrapper/README.md`
- Populate Script: `research/1.131-project-management/02-implementations/vikunja-populate-script/README.md`
- YAML Schema: `research/1.131-project-management/02-implementations/vikunja-populate-script/SCHEMA.md`
- Implementation Summary: `applications/HIERARCHY_IMPLEMENTATION_SUMMARY.md`

**Vikunja Web UI**: https://app.vikunja.cloud

---

## Quick Reference Card

```bash
# The one command you need:
cd ~/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-populate-script/src
python populate_vikunja.py --verbose /path/to/your/vikunja-tasks.yaml

# Parent IDs:
13447 = Foundations (blue)
13448 = Applications (green)
13449 = Clients (red)

# YAML template:
project:
  title: "Name"
  parent_project_id: 13447|13448|13449
tasks:
  - title: "GTD Capture: ..."
```

---

**Status**: 22 projects populated and organized by work context ✅
**Next**: Complete GTD capture tasks to fully populate each project's work items
