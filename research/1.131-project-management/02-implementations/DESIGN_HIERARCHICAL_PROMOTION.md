# Design Note: Task Promotion in Hierarchical Structures

**Date**: 2025-11-08
**Context**: Testing lifecycle tools on Applications project
**Issue**: Where should promoted tasks be created in multi-level hierarchies?

---

## The Problem

When promoting a task using `promote_task_to_project.py`, the script creates a sub-project as a child of the **main project** where the task lives.

**Example**:
```
Applications (main project)
  └── Task: "Garbage Tracker" (lightweight idea)
       ↓ promote_task_to_project.py
  └── Sub-project: Garbage Tracker (created as direct child of Applications)
```

**Issue**: In hierarchical structures with categories, the sub-project should be created under the **appropriate category**, not the main parent.

**Desired outcome**:
```
Applications
  └── Labs
      └── Q (applied technology)
          └── Garbage Tracker (sub-project belongs here)
```

---

## The Decision

**Current implementation (v1)**:
- Promotion creates sub-project as **direct child of task's project**
- Works perfectly for **flat structures** (e.g., Talks project)
- Requires **manual move** for hierarchical structures

**Design choice**: Keep current behavior, manual move for now

**Rationale**:
1. **Simplicity**: Automatic category detection is complex
2. **Flexibility**: User knows best which category
3. **Low frequency**: Promotion happens occasionally, not constantly
4. **Easy fix**: Moving projects is one API call
5. **Works well for primary use case**: Talks (flat structure)

---

## Workarounds

### Option 1: Manual Move (Current)
After promotion, move sub-project to correct category:

```python
# Move Garbage Tracker (13603) to Labs/Q (13592)
data = {'title': 'Garbage Tracker', 'parent_project_id': 13592}
requests.post('https://app.vikunja.cloud/api/v1/projects/13603',
              headers=headers, json=data)
```

### Option 2: Promote from Category Task (Recommended)
Instead of promoting tasks in Applications main project, create tasks **within categories** and promote from there:

```
Applications
  └── Labs
      └── Q
          └── Task: "Garbage Tracker" (create task here)
               ↓ promote_task_to_project.py
          └── Sub-project: Garbage Tracker (created as sibling)
```

**Benefits**:
- ✅ Promotes to correct location automatically
- ✅ No manual move needed
- ✅ Clearer organization

**Drawback**:
- Tasks not visible in Applications main kanban (only in category)

### Option 3: Future Enhancement
Add `--parent` parameter to promotion script:

```bash
python3 promote_task_to_project.py 217426 --template custom --parent 13592
```

This would:
- Create sub-project under specified parent
- Keep main task where it is
- Link task → sub-project

---

## Recommended Pattern for Applications

**For hierarchical structures like Applications**:

1. **Create tracking tasks in main kanban** (for pipeline visibility)
2. **When promoting, specify category manually** or move after promotion
3. **Alternative**: Maintain dual structure
   - Main kanban tasks = high-level tracking (no sub-projects)
   - Category tasks = detailed work (can be promoted)

**Example workflow**:

```
Applications Main Kanban:
  💡 Backlog
    └── "Garbage Tracker" (tracking task, links to sub-project)

Labs/Q:
  └── Garbage Tracker (sub-project)
      ├── Plan the work
      ├── Do the work
      └── Review and complete
```

---

## Current Practice

**For Applications project**:
1. Create task in main project for kanban visibility
2. Promote task (creates sub-project as direct child)
3. **Manually move sub-project to appropriate category** (Products/Sites/Labs/etc.)
4. Main task remains in kanban, linked to sub-project

**For Talks project** (flat structure):
1. Create task in main project
2. Promote task (creates sub-project as child - correct location)
3. No move needed ✅

---

## Future Considerations

If promotion becomes frequent in hierarchical structures, consider:

1. **Interactive mode**: Prompt for category during promotion
2. **Smart detection**: Infer category from task labels/keywords
3. **Template-category mapping**:
   - `--template product` → auto-create under Products
   - `--template site` → auto-create under Sites
4. **Two-step promotion**:
   - Step 1: Promote (creates under main)
   - Step 2: Auto-detect and suggest move

---

## Related Patterns

- **Talks**: Flat structure, promotion works perfectly as-is
- **Applications**: Hierarchical, requires manual categorization
- **Future projects**: May need category-aware promotion

---

## Summary

**Design decision**: Keep promotion simple, manual categorization for hierarchical structures

**Rationale**: Low frequency, high flexibility, works for primary use case

**Workaround**: Manual move (one API call) or promote from category tasks

**Future**: Add `--parent` parameter if promotion becomes frequent

---

**Status**: Documented
**Applies to**: Hierarchical project structures (Applications, future complex projects)
**Alternative**: Flat structures (Talks) work perfectly with current implementation
