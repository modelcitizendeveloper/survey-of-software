# Source Documents for spawn-analysis

**Date**: 2025-11-08
**Purpose**: Add source document references to Vikunja tasks so spawn-analysis agents can find evidence when making decisions

---

## Problem Statement

When exporting Vikunja tasks to spawn-analysis, agents need access to source documents to make informed decisions.

**Example**: An agent deciding whether to focus on "inverse-fractional for CFO" or "QRCards for hotels" needs to review:
- Project definitions (YAML files)
- Planning documents (README, business model, etc.)
- Codebase (if applicable)

Without explicit paths, agents can't find this evidence.

---

## Solution: Source Document References

Add standardized "Source Documents for Analysis" sections to task descriptions.

**Format**:
```html
---
<strong>📂 Source Documents for Analysis:</strong><br>
<ul>
<li>Project definition: <code>/home/ivanadmin/spawn-solutions/applications/{folder}/vikunja-tasks.yaml</code></li>
<li>Project folder: <code>/home/ivanadmin/spawn-solutions/applications/{folder}/</code></li>
<li>Codebase: <code>{codebase_path}</code></li> <!-- if applicable -->
</ul>
```

---

## Implementation

### 1. Examples (Step 1)

**Script**: `tools/show_source_doc_examples.py`

Shows what updates would look like for 3 example tasks:
- inversefractional.com (site)
- QRCards (product with codebase)
- Boutique Hotel Recommendations (product without codebase)

**Usage**:
```bash
python3 show_source_doc_examples.py
```

---

### 2. Bulk Update (Step 2)

**Script**: `tools/add_source_documents.py`

Bulk updates all Applications project tracking tasks with source document references.

**Features**:
- Pattern matching: Maps task titles to folder names
- Smart mapping: Knows which projects have codebases
- Dry-run mode: Preview changes before applying
- Skip logic: Won't duplicate if already has source docs

**Mappings** (17 tasks updated):

| Task Title | Folder | Codebase |
|------------|--------|----------|
| inversefractional.com | inverse-fractional | - |
| conventioncityseattle.com | convention-city-seattle | - |
| ivantohelpyou.com | ivantohelpyou | - |
| modelcitizendeveloper.com | model-citizen-developer | - |
| taelyen.com | taelyen | - |
| mztape.com | mztape | - |
| QRCards | qrcards | /home/ivanadmin/qrcards/ |
| Business Database | business-database | - |
| Boutique Hotel Recommendations | boutique-hotel-recs | - |
| Decision Analysis | products/decision-analysis | - |
| SEA | schema-evolution-automation | /home/ivanadmin/spawn-experiments/tools/schema-evolution-framework/ |
| Elevator Project | elevator-project | - |
| IF Learning Lab | inverse-fractional/05-learning-lab | - |
| Project Management - Vikunja | project-management | /home/ivanadmin/spawn-solutions/research/1.131-project-management/ |
| Research Lineage System | research-lineage-system | - |
| Cookbooks Content System | cookbooks | - |
| Intelligence Portal | intelligence-portal | - |

**Usage**:
```bash
# Preview changes
python3 add_source_documents.py --dry-run

# Apply updates
python3 add_source_documents.py

# Force update even if exists
python3 add_source_documents.py --force
```

**Results**:
- ✅ Updated: 17 tasks
- ⏭️  Skipped: 5 tasks (no folder mapping)
- ❌ Failed: 0

---

### 3. Promotion Template (Step 3)

**Script**: `tools/promote_task_to_project.py` (updated)

Added optional parameters to automatically include source documents when promoting tasks.

**New Parameters**:
- `--source-folder`: Relative path in applications/ (e.g., "qrcards")
- `--codebase`: Absolute path to codebase (e.g., "/home/ivanadmin/qrcards/")

**Examples**:
```bash
# Product with codebase
python3 promote_task_to_project.py 216450 --template product \
    --source-folder qrcards --codebase /home/ivanadmin/qrcards/

# Site (no codebase)
python3 promote_task_to_project.py 216451 --template custom \
    --source-folder inverse-fractional

# Without source docs (backward compatible)
python3 promote_task_to_project.py 216450 --template talk
```

**How It Works**:
1. Promote task to sub-project (existing behavior)
2. If `--source-folder` provided, append source documents section to main task
3. Main task now has both sub-project link AND source documents

---

## Usage for spawn-analysis

When exporting Vikunja tasks to spawn-analysis:

**Before**:
```
Task: "inversefractional.com vs. QRCards - which to prioritize?"
Agent: "I need more information about these projects to decide"
```

**After**:
```
Task: "inversefractional.com vs. QRCards - which to prioritize?"

Source Documents:
- inversefractional.com:
  - Project folder: /home/ivanadmin/spawn-solutions/applications/inverse-fractional/
  - Definition: vikunja-tasks.yaml

- QRCards:
  - Project folder: /home/ivanadmin/spawn-solutions/applications/qrcards/
  - Definition: vikunja-tasks.yaml
  - Codebase: /home/ivanadmin/qrcards/

Agent: *reads business models, current state, priorities*
Agent: "Based on evidence, recommend QRCards because [specific reasons from docs]"
```

---

## Files Created/Modified

**New Files**:
- `tools/show_source_doc_examples.py` - Example viewer
- `tools/add_source_documents.py` - Bulk update script
- `SOURCE_DOCUMENTS_IMPLEMENTATION.md` - This documentation

**Modified Files**:
- `tools/promote_task_to_project.py` - Added --source-folder and --codebase parameters

**Helper Files**:
- `tools/get_task.py` - Utility to inspect task details
- `tools/get_project_tasks.py` - Utility to list all tasks in a project

---

## Maintenance

**Adding new projects**:

When creating new application projects, either:

1. **Use promotion script with source docs**:
   ```bash
   python3 promote_task_to_project.py <task_id> --template product \
       --source-folder new-project --codebase /path/to/code/
   ```

2. **Run bulk update**:
   - Add mapping to `add_source_documents.py` TASK_MAPPINGS
   - Run: `python3 add_source_documents.py`

3. **Manual update**:
   - Edit task description in Vikunja UI
   - Add source documents section using format above

---

## Statistics

**Current Coverage**:
- Applications project: 22 tasks total
- Source documents added: 17 tasks (77%)
- Remaining: 5 tasks (GTD tasks + projects without folders)

**Task Types**:
- Sites (QRCards-hosted): 6 tasks
- Products: 3 tasks
- Services: 1 task
- Labs: 3 tasks
- Meta: 2 tasks
- Content: 2 tasks

**Codebases tracked**: 3
- QRCards: /home/ivanadmin/qrcards/
- SEA: /home/ivanadmin/spawn-experiments/tools/schema-evolution-framework/
- Project Management: /home/ivanadmin/spawn-solutions/research/1.131-project-management/

---

## Future Enhancements

**Potential improvements**:

1. **Auto-detection**: Scan applications/ folder to find new projects automatically
2. **Validation**: Check that referenced paths exist before updating
3. **Export integration**: Dedicated export script that includes source documents in JSON
4. **Talks project**: Extend pattern to Talks project (link to talk materials)
5. **Rich metadata**: Add project status, timeline, budget from YAML files

---

## Related Documentation

- `LIFECYCLE_QUICK_REFERENCE.md` - Task lifecycle commands
- `DESIGN_HIERARCHICAL_PROMOTION.md` - Promotion in hierarchical structures
- `tools/README.md` - All lifecycle tools documentation

---

**Status**: Implemented ✅
**Coverage**: 17/22 tasks (77%)
**Next**: Export to spawn-analysis and test agent decision-making
