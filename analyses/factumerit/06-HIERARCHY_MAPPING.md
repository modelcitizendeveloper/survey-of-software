# Vikunja Project Hierarchy Mapping

**Created**: November 8, 2025
**Parent Projects Created**: ✅ Complete

---

## Parent Projects (Created)

| Parent Project | Vikunja ID | Description |
|---------------|------------|-------------|
| **Foundations** | 13447 | Capability development - spawn-* ecosystem |
| **Applications** | 13448 | Capability application - tools and platforms |
| **Clients** | 13449 | Customer-facing work - consulting and sites |

---

## Foundations/ (Parent ID: 13447)

**Capability development projects** - 5 children

| Project | YAML File | Status |
|---------|-----------|--------|
| spawn | `spawn/vikunja-tasks.yaml` | ⏸️ Add parent_project_id: 13447 |
| spawn-experiments | `spawn-experiments/vikunja-tasks.yaml` | ⏸️ Add parent_project_id: 13447 |
| spawn-solutions | `spawn-solutions/vikunja-tasks.yaml` | ⏸️ Add parent_project_id: 13447 |
| spawn-analysis | `spawn-analysis/vikunja-tasks.yaml` | ⏸️ Add parent_project_id: 13447 |
| spawn-patents | `spawn-patents/vikunja-tasks.yaml` | ✅ EXAMPLE UPDATED |

---

## Applications/ (Parent ID: 13448)

**Capability application projects** - 12 children

| Project | YAML File | Status |
|---------|-----------|--------|
| qrcards | `qrcards/vikunja-tasks.yaml` | ⏸️ Add parent_project_id: 13448 |
| schema-evolution-automation | `schema-evolution-automation/vikunja-tasks.yaml` | ⏸️ Add parent_project_id: 13448 |
| inverse-fractional | `inverse-fractional/vikunja-tasks.yaml` | ⏸️ Add parent_project_id: 13448 |
| project-management | `project-management/vikunja-tasks.yaml` | ⏸️ Add parent_project_id: 13448 |
| cookbooks | `cookbooks/vikunja-tasks.yaml` | ⏸️ Add parent_project_id: 13448 |
| elevator-project | `elevator-project/vikunja-tasks.yaml` | ⏸️ Add parent_project_id: 13448 |
| boutique-hotel-recs | `boutique-hotel-recs/vikunja-tasks.yaml` | ⏸️ Add parent_project_id: 13448 |
| business-database | `business-database/vikunja-tasks.yaml` | ⏸️ Add parent_project_id: 13448 |
| intelligence-portal | `intelligence-portal/vikunja-tasks.yaml` | ⏸️ Add parent_project_id: 13448 |
| org-chart | `org-chart/vikunja-tasks.yaml` | ⏸️ Add parent_project_id: 13448 |
| research-lineage-system | `research-lineage-system/vikunja-tasks.yaml` | ⏸️ Add parent_project_id: 13448 |
| werise | `werise/vikunja-tasks.yaml` | ⏸️ Add parent_project_id: 13448 |

---

## Clients/ (Parent ID: 13449)

**Customer-facing projects** - 6 children

| Project | YAML File | Status |
|---------|-----------|--------|
| decision-analysis (service) | `products/decision-analysis.yaml` | ⏸️ Add parent_project_id: 13449 |
| ivantohelpyou (site) | `qrcards-sites/ivantohelpyou.yaml` | ⏸️ Add parent_project_id: 13449 |
| model-citizen-developer (site) | `qrcards-sites/model-citizen-developer.yaml` | ⏸️ Add parent_project_id: 13449 |
| convention-city-seattle (site) | `qrcards-sites/convention-city-seattle.yaml` | ⏸️ Add parent_project_id: 13449 |
| inverse-fractional (site) | `qrcards-sites/inverse-fractional.yaml` | ⏸️ Add parent_project_id: 13449 |
| taelyen (site) | `qrcards-sites/taelyen.yaml` | ⏸️ Add parent_project_id: 13449 |

---

## How to Update YAML Files

**Add one line to the `project:` section:**

```yaml
project:
  title: "Your Project Title"
  description: "Your description"
  parent_project_id: 13447  # ← Add this line (use appropriate parent ID)
```

**Example** (spawn-patents):

```yaml
project:
  title: "spawn-patents"
  description: "Patent opportunity analysis for QRCards - IP discovery and strategic portfolio planning"
  parent_project_id: 13447  # Foundations
```

---

## Batch Update Script

To update all YAMLs at once:

```bash
# Foundations (ID: 13447)
for project in spawn spawn-experiments spawn-solutions spawn-analysis spawn-patents; do
    # Add parent_project_id to project section
    # (manual edit or sed/awk script)
done

# Applications (ID: 13448)
for project in qrcards schema-evolution-automation inverse-fractional project-management \
               cookbooks elevator-project boutique-hotel-recs business-database \
               intelligence-portal org-chart research-lineage-system werise; do
    # Add parent_project_id to project section
done

# Clients (ID: 13449)
# products/decision-analysis.yaml
# qrcards-sites/*.yaml (5 files)
```

---

## Verification After Population

1. Check Vikunja UI - parent projects should show child count
2. Navigate to Foundations → see 5 children
3. Navigate to Applications → see 12 children
4. Navigate to Clients → see 6 children

---

## Summary

- **Total parent projects**: 3 (all created ✅)
- **Total children to link**: 23
- **Next step**: Update 23 YAML files with parent_project_id
- **Then**: Re-populate or update existing projects with hierarchy

**Example YAML updated**: `spawn-patents/vikunja-tasks.yaml` ✅
