# Vikunja YAML Files - Ready for Review

**Created**: November 8, 2025
**Status**: All YAML files created, awaiting review before loading into Vikunja
**Total**: 23 projects (17 applications + 5 QRCards sites + 1 consulting service)

---

## Phase 1: Critical & Active (6 projects)

### 1. schema-evolution-automation/vikunja-tasks.yaml
**Description**: SEA CLI tool - Phase 0 complete, Phase 1 ready (Weeks 1-12)
**Key tasks**:
- GTD capture: Review Phase 1 implementation plan
- Decision point: Validate technology stack (7 selections)
- Architecture review: Meta-circular design validation

**Priority**: Critical (in active development)

---

### 2. qrcards/vikunja-tasks.yaml
**Description**: Multi-database creator platform implementation work
**Key tasks**:
- GTD capture: Review ~/qrcards for open items
- Infrastructure: Execute Render migration from PythonAnywhere ($147/year savings)

**Priority**: High (production platform)
**Note**: High-level only (detailed work tracked in ~/qrcards itself)

---

### 3. cookbooks/vikunja-tasks.yaml
**Description**: Research-to-content conversion system
**Key tasks**:
- GTD capture: Review content system
- Strategy: Resolve brand architecture (Taelyen vs MCD vs ivantohelpyou)
- Process: Complete conversion templates (free/invited/subscriber tiers)

**Priority**: High (active content pipeline)

---

### 4. spawn/vikunja-tasks.yaml
**Description**: Platform coordination for spawn-* ecosystem
**Key tasks**:
- GTD capture: Platform-level coordination work only

**Priority**: High (framework foundation)
**Note**: Individual spawn-* projects have their own YAMLs

---

### 5. spawn-analysis/vikunja-tasks.yaml
**Description**: Progressive content delivery for decision reports
**Key tasks**:
- GTD capture: Review content delivery system
- Check ~/spawn-analysis for actual tool status

**Priority**: High (active decision tool)

---

### 6. spawn-solutions/vikunja-tasks.yaml
**Description**: Technology intelligence database
**Key tasks**:
- GTD capture: Review database system
- Database: Create spawn_solutions.db and verify schema (17 tables, 5 views)

**Priority**: High (active research repository)

---

## Phase 2: Infrastructure (2 projects)

### 7. spawn-experiments/vikunja-tasks.yaml
**Description**: Methodology tracking database (Method 1-4 competitions)
**Key tasks**:
- GTD capture: Review database system
- Database: Create spawn_experiments.db and verify schema (11 tables, 6 views)

**Priority**: Medium (infrastructure)

---

### 8. project-management/vikunja-tasks.yaml
**Description**: Vikunja integration suite (wrapper, populate, export)
**Key tasks**:
- GTD capture: Document next steps
- Enhancement: Implement hierarchical project structures
- Enhancement: Expand wrapper API to cover all Vikunja features (100% coverage)

**Priority**: Medium (recently completed, enhancements planned)
**Status**: Core integration ✅ complete (Nov 7-8, 2025)

---

## Phase 3: Backlog (9 projects)

### 9. elevator-project/vikunja-tasks.yaml
**Description**: Elevator scheduling simulation
**Key tasks**:
- **Prepare demo for condo board** (priority 5, due Nov 15)
- GTD capture: Review simulation project

**Priority**: Medium (demo needed soon)

---

### 10. inverse-fractional/vikunja-tasks.yaml
**Description**: CFO consulting + Learning Laboratory
**Key tasks**:
- GTD capture: Review all 7 folders (business model, operations, learning lab, etc.)
- Learning Lab 1.1: Implement Odoo Community (20-40 hours, $5K/year savings)
- Learning Lab 1.2: Build unit economics simulator (Python + Monte Carlo)
- Learning Lab 1.3: Build cash flow forecasting tool (Python, $720/year savings)
- Learning Lab 1.4: Build CFO dashboard with Metabase ($840/year savings)
- **Content: FATE event preparation** (priority 5, due Nov 20)
- Portfolio: Document operational stack publicly

**Priority**: High (active business + learning lab experiments)

---

### 11. spawn-patents/vikunja-tasks.yaml
**Description**: Patent opportunity analysis for QRCards (12-methodology framework)
**Key tasks**:
- **Contact patent lawyer for IP consultation** (priority 5, due Nov 15)
- GTD capture: Review framework and create implementation tasks
- Stage 1: Execute Quadruple Archaeology (MP-001 through MP-004)
- Stage 2: Prior Art Hunter (search existing patents)
- Stage 4: IP Portfolio Optimizer (strategic filing plan)

**Priority**: High (patent lawyer contact urgent)
**Real location**: ~/spawn-patents

---

### 12-17. Investigation Needed (6 projects)
Simple GTD capture YAMLs created for:
- boutique-hotel-recs/vikunja-tasks.yaml
- business-database/vikunja-tasks.yaml
- intelligence-portal/vikunja-tasks.yaml
- org-chart/vikunja-tasks.yaml
- research-lineage-system/vikunja-tasks.yaml
- werise/vikunja-tasks.yaml

**All have**: Single task "GTD Capture: Investigate [project] and document scope"
**Priority**: Low (need investigation)

---

## QRCards Sites (5 projects)

Already created in previous session:
1. qrcards-sites/ivantohelpyou.yaml
2. qrcards-sites/model-citizen-developer.yaml
3. qrcards-sites/convention-city-seattle.yaml
4. qrcards-sites/inverse-fractional.yaml
5. qrcards-sites/taelyen.yaml

**All have**: GTD capture task to review site content in ~/qrcards

---

## Consulting Service (1 project)

Already created in previous session:
- products/decision-analysis.yaml

**Description**: Live consulting service (client calls using spawn-solutions/spawn-analysis)

---

## Summary Statistics

**Total YAML files created**: 23

**By priority**:
- Critical: 1 (schema-evolution-automation)
- High: 10 (qrcards, cookbooks, spawn-*, inverse-fractional, spawn-patents, 5 QRCards sites)
- Medium: 3 (project-management, elevator-project, decision-analysis)
- Low: 6 (investigation needed)
- Unknown: 3 (await investigation)

**Immediate priorities** (due Nov 9-15):
- GTD captures for all projects (due Nov 9-10)
- **Contact patent lawyer** (priority 5, due Nov 15)
- Elevator demo for condo board (priority 5, due Nov 15)
- FATE event prep (priority 5, due Nov 20)

**Sprint-level tasks** (due Nov 15-30):
- SEA architecture review (Nov 11)
- Odoo Community research (inverse-fractional, Nov 15)
- Render migration planning (qrcards, Nov 20)
- spawn-* database creation (Nov 15)

---

## Next Steps

### 1. User Review
User to review all YAML files before loading into Vikunja.

### 2. Loading into Vikunja
Once approved, use populate script:
```bash
cd ~/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-populate-script/src

# Bootstrap labels first (if not already done)
python populate_vikunja.py --verbose ~/spawn-solutions/applications/00-bootstrap-labels.yaml

# Then populate all applications (17 total)
for yaml in ~/spawn-solutions/applications/*/vikunja-tasks.yaml; do
    echo "Loading $yaml..."
    python populate_vikunja.py --verbose "$yaml"
done

# QRCards sites
for yaml in ~/spawn-solutions/applications/qrcards-sites/*.yaml; do
    echo "Loading $yaml..."
    python populate_vikunja.py --verbose "$yaml"
done

# Products
for yaml in ~/spawn-solutions/applications/products/*.yaml; do
    echo "Loading $yaml..."
    python populate_vikunja.py --verbose "$yaml"
done
```

### 3. GTD Capture Workflow
After loading, execute GTD capture tasks for each project:
- Review documentation
- Search for TODO/FIXME comments
- Create detailed task lists
- Set priorities and due dates

---

## File Locations

All YAML files are in:
- `/home/ivanadamin/spawn-solutions/applications/*/vikunja-tasks.yaml`
- `/home/ivanadamin/spawn-solutions/applications/qrcards-sites/*.yaml`
- `/home/ivanadamin/spawn-solutions/applications/products/*.yaml`

Bootstrap labels:
- `/home/ivanadamin/spawn-solutions/applications/00-bootstrap-labels.yaml`

GTD labels template:
- `/home/ivanadamin/spawn-solutions/applications/vikunja-labels.yaml`

---

**Status**: Ready for user review
**Date**: November 8, 2025
