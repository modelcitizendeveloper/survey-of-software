# Color Support & Project Migration - Implementation Complete

**Date**: November 8, 2025
**Status**: Both features implemented with TDD ✅

---

## ✅ Features Implemented

### 1. hex_color Support

**Added to wrapper**: Projects now support colors!

```python
# Create project with color
project = client.projects.create(
    title="Foundations",
    hex_color="#3498db"  # Blue
)

# Update project color
project = client.projects.update(
    project_id=123,
    hex_color="#2ecc71"  # Green
)
```

**Implementation**:
- ✅ Added `hex_color` field to `Project` model (optional, defaults to None)
- ✅ Added `hex_color` parameter to `create()` method
- ✅ Added `hex_color` parameter to `update()` method
- ✅ Updated `_parse_project()` to parse `hex_color` from API
- ✅ **4 tests written first**, all passing

---

### 2. move_project() Method

**Added to wrapper**: Migrate existing projects into hierarchy!

```python
# Move existing project under a parent
client.projects.move_project(
    project_id=5,           # Project to move
    new_parent_id=13448     # Applications parent
)

# Move project to top-level
client.projects.move_project(
    project_id=5,
    new_parent_id=0  # 0 = top-level
)
```

**Use case**: Migrate existing Vikunja projects into your new hierarchy without recreating them.

**Implementation**:
- ✅ Added `move_project(project_id, new_parent_id)` method to `ProjectsManager`
- ✅ Convenience wrapper around `update()` with `parent_project_id`
- ✅ Clear error handling for invalid parents
- ✅ **3 tests written first**, all passing

---

## 🧪 Testing Summary

**TDD Approach - All tests written first**:

```bash
# Red phase (tests fail) → Green phase (implementation) → All tests pass ✅
```

**New tests**:
- ✅ 4 tests for `hex_color` support
- ✅ 3 tests for `move_project()` method
- ✅ **Total: 7 new tests, all passing**

**Existing tests**:
- ✅ 21 hierarchy tests still pass
- ✅ 23 wrapper tests still pass
- ✅ **Total: 44 tests, all passing**

Run tests:
```bash
cd research/1.131-project-management/02-implementations/vikunja-api-wrapper/src

# New features only
pytest test_project_hierarchy.py::TestProjectColors -v
pytest test_project_hierarchy.py::TestMoveProject -v

# All tests
pytest test_project_hierarchy.py test_vikunja_wrapper.py -v
```

---

## 🎨 Parent Projects Updated with Colors

**Updated in Vikunja** (Nov 8, 2025):

| Project | ID | Color | Visual |
|---------|-----|--------|--------|
| **Foundations** | 13447 | `#3498db` | 🔵 Blue - infrastructure |
| **Applications** | 13448 | `#2ecc71` | 🟢 Green - growth |
| **Clients** | 13449 | `#e74c3c` | 🔴 Red - revenue |

**YAML files updated**:
- `applications/00-parents/01-foundations.yaml` ✅
- `applications/00-parents/02-applications.yaml` ✅
- `applications/00-parents/03-clients.yaml` ✅

---

## 🔄 Migration Script

**File**: `vikunja-api-wrapper/src/migrate_to_hierarchy.py`

### Usage

**Dry-run** (preview changes):
```bash
cd research/1.131-project-management/02-implementations/vikunja-api-wrapper/src
python migrate_to_hierarchy.py --dry-run
```

**Execute migration**:
```bash
python migrate_to_hierarchy.py
```

### What it does

- Fetches all projects from Vikunja
- Moves projects to their designated parent according to mapping
- Skips projects already under correct parent
- Reports not-found projects (not yet populated)

### Current Migration Status

**Dry-run results** (Nov 8, 2025):

```
Total in migration map: 23
  ✅ Found in Vikunja: 7
  ✅ Already correct:  0
  📦 Would migrate:    7
  ❌ Not found:        16
```

**7 existing projects found**:
1. spawn-solutions (would move to Foundations)
2. inverse-fractional (would move to Applications)
3. decision-analysis (would move to Clients)
4. ivantohelpyou (would move to Clients)
5. model-citizen-developer (would move to Clients)
6. convention-city-seattle (would move to Clients)
7. taelyen (would move to Clients)

**16 projects not found** (not yet populated in Vikunja):
- spawn, spawn-experiments, spawn-analysis, spawn-patents (Foundations)
- qrcards, SEA, project-management, cookbooks, elevator-project, + 6 backlog (Applications)
- inverse-fractional-site (Clients)

---

## 📝 Migration Mapping

```python
# Foundations (ID: 13447) - 5 children
"spawn": 13447,
"spawn-experiments": 13447,
"spawn-solutions": 13447,
"spawn-analysis": 13447,
"spawn-patents": 13447,

# Applications (ID: 13448) - 12 children
"qrcards": 13448,
"schema-evolution-automation": 13448,
"inverse-fractional": 13448,
"project-management": 13448,
"cookbooks": 13448,
"elevator-project": 13448,
"boutique-hotel-recs": 13448,
"business-database": 13448,
"intelligence-portal": 13448,
"org-chart": 13448,
"research-lineage-system": 13448,
"werise": 13448,

# Clients (ID: 13449) - 6 children
"decision-analysis": 13449,
"ivantohelpyou": 13449,
"model-citizen-developer": 13449,
"convention-city-seattle": 13449,
"inverse-fractional-site": 13449,
"taelyen": 13449,
```

---

## 🚀 Next Steps

### Option A: Migrate Existing 7 Projects

```bash
# Execute migration for existing projects
cd research/1.131-project-management/02-implementations/vikunja-api-wrapper/src
python migrate_to_hierarchy.py
```

### Option B: Populate Remaining 16 Projects with Hierarchy

**Update YAMLs** with `parent_project_id`:

```yaml
# Example: applications/qrcards/vikunja-tasks.yaml
project:
  title: "qrcards"
  description: "..."
  parent_project_id: 13448  # Applications
  hex_color: "#3498db"      # Optional color
```

**Then populate**:
```bash
cd research/1.131-project-management/02-implementations/vikunja-populate-script/src

for yaml in ~/spawn-solutions/applications/*/vikunja-tasks.yaml; do
    python populate_vikunja.py --verbose "$yaml"
done
```

### Option C: Both (Recommended)

1. **Migrate existing 7 projects** → establishes hierarchy for populated projects
2. **Update remaining 16 YAMLs** → adds `parent_project_id` field
3. **Populate remaining projects** → creates them already nested

---

## 🎯 Usage Examples

### Create Project with Color & Hierarchy

```python
from vikunja_wrapper import VikunjaClient
import os

client = VikunjaClient(
    base_url="https://app.vikunja.cloud",
    token=os.getenv('VIKUNJA_API_TOKEN')
)

# Create child project under Applications with color
project = client.projects.create(
    title="My New App",
    description="Awesome new tool",
    hex_color="#9b59b6",      # Purple
    parent_project_id=13448   # Applications parent
)

print(f"Created project {project.id} under Applications with purple color")
```

### Migrate Existing Project

```python
# Move existing top-level project under Foundations
project = client.projects.move_project(
    project_id=12345,
    new_parent_id=13447  # Foundations
)

print(f"Moved {project.title} to Foundations")
```

### Update Project Color

```python
# Change project color
project = client.projects.update(
    project_id=12345,
    title="Updated Title",  # Must include title
    hex_color="#e67e22"     # Orange
)
```

**⚠️ Note**: Vikunja API requires `title` in update requests, so always include it:

```python
# Get current project first
project = client.projects.get(12345)

# Update with title preserved
updated = client.projects.update(
    12345,
    title=project.title,  # Preserve existing title
    hex_color="#new-color"
)
```

---

## 📚 Files Modified/Created

**Wrapper implementation**:
- ✅ `vikunja_wrapper.py` - Added `hex_color` to Project model, create/update methods, move_project()
- ✅ `test_project_hierarchy.py` - Added TestProjectColors + TestMoveProject (7 tests)

**Parent projects**:
- ✅ `applications/00-parents/01-foundations.yaml` - Added hex_color
- ✅ `applications/00-parents/02-applications.yaml` - Added hex_color
- ✅ `applications/00-parents/03-clients.yaml` - Added hex_color

**Migration**:
- ✅ `vikunja-api-wrapper/src/migrate_to_hierarchy.py` - Migration script

**Documentation**:
- ✅ `COLOR_AND_MIGRATION_SUMMARY.md` - This file

---

## ✅ Completion Summary

**hex_color support**:
- ✅ Tests written first (4 tests)
- ✅ Implementation complete
- ✅ All tests passing
- ✅ Parent projects updated in Vikunja

**move_project() method**:
- ✅ Tests written first (3 tests)
- ✅ Implementation complete
- ✅ All tests passing
- ✅ Migration script created

**Total tests**: 44 passing (21 hierarchy + 23 wrapper)

**Status**: Ready for migration ✅

---

**Date**: November 8, 2025
**Next action**: Run `python migrate_to_hierarchy.py` (without --dry-run) to migrate existing 7 projects
