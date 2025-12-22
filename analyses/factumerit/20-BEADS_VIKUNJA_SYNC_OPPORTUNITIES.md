# Beads + Vikunja Sync: Integration Opportunities

**Date**: 2025-12-20
**Status**: Exploration
**Context**: Two-tier tracking architecture analysis

---

## Current State

### The Two-Tier Model

```
┌─────────────────────────────────────────────────────────────────┐
│ VIKUNJA (Portfolio Layer)                                       │
│ • Client engagements, strategic initiatives                     │
│ • GTD contexts (@Home, @Work, @Errands)                        │
│ • Application backlogs                                          │
│ • Calendar-visible deadlines                                    │
│ • Shared with stakeholders                                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                    external_ref: vikunja:NNNN
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ BEADS (Implementation Layer)                                    │
│ • Fine-grained work units                                       │
│ • Blocking dependencies (bd blocked, bd ready)                  │
│ • Git-native sync (lives in .beads/)                           │
│ • Developer workflow (bd update, bd close)                      │
│ • Research tracking (S1-S4 stages via labels)                   │
└─────────────────────────────────────────────────────────────────┘
```

### Existing Tools

| Tool | Purpose | Status |
|------|---------|--------|
| `bd-vikunja-sync.py` | Sync closed beads → done Vikunja tasks | Created, not deployed |
| `vikunja-mcp` | 58 tools for Claude ↔ Vikunja | Production |
| `vikunja-populate-script` | YAML → Vikunja tasks | Production |
| `vikunja-export-script` | Vikunja → portfolio-state.md | Production |

---

## Gap Analysis

### What Works Well

1. **Beads for implementation tracking**: `bd ready` workflow, blocking deps
2. **Vikunja for portfolio view**: Kanban, calendar, shared access
3. **MCP for Claude integration**: Rich tooling already available
4. **YAML for bulk operations**: populate-script handles complex setups

### What's Missing

1. **Bi-directional sync**: Only beads→Vikunja exists, not reverse
2. **Automatic linking**: Must manually add `external_ref: vikunja:NNNN`
3. **Stage propagation**: Beads labels don't reflect in Vikunja
4. **Query federation**: Can't search across both systems
5. **Conflict resolution**: No handling if both sides change

---

## Integration Opportunities

### 1. Automatic External Ref Linking

**Problem**: Creating linked beads/Vikunja items requires manual ID coordination.

**Solution**: Command that creates in both systems atomically:

```bash
# Creates Vikunja task, then beads issue with external_ref
bd create-linked "Implement elevator simulation" \
  --vikunja-project=5 \
  --vikunja-bucket="Backlog" \
  --labels="tier1,research"

# Result:
# - Vikunja task #123 created
# - Beads issue solutions-abc created with external_ref: vikunja:123
```

**Implementation**:
```python
def create_linked(title, vikunja_project, vikunja_bucket=None, labels=None):
    # 1. Create Vikunja task
    task = vikunja_client.tasks.create(
        project_id=vikunja_project,
        title=title,
        bucket_id=resolve_bucket(vikunja_bucket)
    )

    # 2. Create beads issue with link
    result = subprocess.run([
        "bd", "create", title,
        "--external-ref", f"vikunja:{task['id']}",
        "--labels", ",".join(labels or [])
    ], capture_output=True)

    return {"vikunja_id": task["id"], "beads_id": parse_beads_id(result.stdout)}
```

---

### 2. Stage Label Sync (Beads → Vikunja)

**Problem**: Research stages tracked in beads labels don't appear in Vikunja.

**Current Beads Labels**:
- `s1-pending`, `s1-in-progress`, `s1-complete`
- `s2-pending`, `s2-in-progress`, `s2-complete`
- etc.

**Solution**: Sync stage labels to Vikunja on beads update:

```python
# In bd-vikunja-sync.py
def sync_stage_labels(beads_issue, vikunja_task_id):
    stage_labels = [l for l in beads_issue["labels"] if l.startswith("s")]
    current_stage = get_highest_stage(stage_labels)  # e.g., "S2-in-progress"

    # Map to Vikunja label
    vikunja_label = ensure_label_exists(f"Stage: {current_stage}")

    # Remove old stage labels, add new
    current_labels = vikunja_client.tasks.get(vikunja_task_id)["labels"]
    stage_label_ids = [l["id"] for l in current_labels if l["title"].startswith("Stage:")]
    for lid in stage_label_ids:
        vikunja_client.tasks.remove_label(vikunja_task_id, lid)
    vikunja_client.tasks.add_label(vikunja_task_id, vikunja_label["id"])
```

**Vikunja Display**: Task shows "Stage: S2-in-progress" label, visible in Kanban.

---

### 3. Progress Percentage Sync

**Problem**: Beads tracks blocking deps, but Vikunja shows `percentDone`.

**Solution**: Calculate progress from dependency completion:

```python
def calculate_progress(beads_issue):
    deps = beads_issue.get("dependencies", [])
    if not deps:
        return 0 if beads_issue["status"] == "open" else 100

    completed = sum(1 for d in deps if d["status"] == "closed")
    return int(100 * completed / len(deps))

def sync_progress(beads_issue, vikunja_task_id):
    progress = calculate_progress(beads_issue)
    vikunja_client.tasks.update(vikunja_task_id, percent_done=progress)
```

**Vikunja Display**: Progress bar fills as dependencies close.

---

### 4. Federated Query Tool

**Problem**: Can't search across beads and Vikunja in one query.

**Solution**: MCP tool that queries both and merges results:

```python
@mcp.tool()
def search_everywhere(query: str, include_closed: bool = False) -> dict:
    """Search across beads and Vikunja for matching items"""

    # Search beads
    beads_result = subprocess.run(
        ["bd", "list", "--title-contains", query, "--json"],
        capture_output=True, text=True
    )
    beads_items = json.loads(beads_result.stdout)

    # Search Vikunja
    vikunja_items = search_all(query=query, include_completed=include_closed)

    # Merge and dedupe (linked items appear once)
    merged = merge_results(beads_items, vikunja_items)

    return {
        "total": len(merged),
        "beads_only": [i for i in merged if i["source"] == "beads"],
        "vikunja_only": [i for i in merged if i["source"] == "vikunja"],
        "linked": [i for i in merged if i["source"] == "both"]
    }
```

---

### 5. Vikunja → Beads Reverse Sync

**Problem**: Tasks created in Vikunja UI don't appear in beads.

**Solution**: Webhook or polling to import new Vikunja tasks:

```python
# Polling approach (simpler, no webhook setup)
def poll_vikunja_for_new_tasks(since_timestamp):
    tasks = vikunja_client.tasks.list_all(filter=f"created >= {since_timestamp}")

    for task in tasks:
        # Check if already linked
        existing = find_beads_by_external_ref(f"vikunja:{task['id']}")
        if not existing:
            # Create beads issue
            subprocess.run([
                "bd", "create", task["title"],
                "--external-ref", f"vikunja:{task['id']}",
                "--description", task.get("description", ""),
                "--labels", "imported-from-vikunja"
            ])
```

**Trigger**: Run on session start, or as scheduled job.

---

### 6. Conflict Detection

**Problem**: Both systems might be updated independently.

**Solution**: Last-modified comparison with warning:

```python
def detect_conflicts(beads_issue, vikunja_task):
    beads_updated = parse_datetime(beads_issue["updated_at"])
    vikunja_updated = parse_datetime(vikunja_task["updated"])

    # If both updated since last sync, potential conflict
    last_sync = get_last_sync_time(beads_issue["id"])

    if beads_updated > last_sync and vikunja_updated > last_sync:
        return {
            "conflict": True,
            "beads_changes": diff_since(beads_issue, last_sync),
            "vikunja_changes": diff_since(vikunja_task, last_sync),
            "recommendation": "manual_review"
        }
    return {"conflict": False}
```

---

## Architecture Decision: Sync Direction

### Option A: Beads as Source of Truth
- All work tracked in beads first
- Vikunja reflects beads state (read-only view)
- Simpler, no conflicts
- **Con**: Can't use Vikunja UI to update

### Option B: Vikunja as Source of Truth
- All work tracked in Vikunja first
- Beads pulls from Vikunja
- **Con**: Loses git-native benefits

### Option C: Bi-directional with Beads Priority (Recommended)
- Work can originate in either system
- On conflict, beads wins (developer's local state)
- Vikunja changes flagged for review
- **Pro**: Flexibility with clear resolution rule

---

## Implementation Phases

### Phase 1: Close Loop (Minimum Viable Sync)
- [ ] Deploy `bd-vikunja-sync.py` as beads hook
- [ ] Test: close beads issue → Vikunja task marked done
- [ ] Add stage label sync (S1-S4 → Vikunja labels)

### Phase 2: Enhanced Visibility
- [ ] Progress percentage sync (deps → percentDone)
- [ ] `bd create-linked` command
- [ ] Federated search tool in MCP

### Phase 3: Full Bi-Directional
- [ ] Vikunja polling for new tasks
- [ ] Conflict detection and resolution
- [ ] Webhook integration (if Vikunja supports)

---

## Filter Syntax Opportunities

Given Vikunja's powerful filter syntax, we can create smart views:

### Research Dashboard Filters

```
# All S1-complete research ready for S2
labels like "%s1-complete%" && labels like "%research%" && done = false

# High-priority research blocked on dependencies
priority >= 3 && labels like "%blocked%" && done = false

# Overdue research items
dueDate < now && labels like "%research%" && done = false

# Stale research (not updated in 30 days)
# Note: May need Vikunja API verification for updatedAt filter
```

### Combined Beads+Vikunja Queries

```bash
# Find all research with S1 complete, show both beads and Vikunja status
bd list -l s1-complete -l research --json | \
  jq -r '.[] | select(.external_ref | startswith("vikunja:"))' | \
  while read issue; do
    vikunja_id=$(echo "$issue" | jq -r '.external_ref' | cut -d: -f2)
    vikunja_status=$(curl -s "$VIKUNJA_URL/api/v1/tasks/$vikunja_id" | jq -r '.done')
    echo "$(echo "$issue" | jq -r '.id'): beads=$(echo "$issue" | jq -r '.status'), vikunja_done=$vikunja_status"
  done
```

---

## Related Files

| File | Purpose |
|------|---------|
| `/home/ivanadamin/spawn-solutions/tools/bd-vikunja-sync.py` | Sync implementation |
| `/home/ivanadamin/spawn-solutions/plan/BEADS-VIKUNJA-MIGRATION.md` | Migration plan |
| `/home/ivanadamin/spawn-solutions/analyses/BEADS_DESIGN_PROPOSAL.md` | ID conventions |
| `/home/ivanadamin/spawn-solutions/development/projects/impl-1131-vikunja/` | Vikunja tooling |

---

## Next Steps

1. **Review `bd-vikunja-sync.py`**: Verify it's functional, add to hooks
2. **Test filter syntax**: Validate Vikunja supports needed fields
3. **Prototype `create-linked`**: Build the atomic create command
4. **Define sync schedule**: Hook-triggered vs polling vs manual

---

## Questions to Resolve

1. Does Vikunja filter syntax support `updatedAt` for stale detection?
2. Should linked items use Vikunja task ID or beads ID as primary?
3. How to handle Vikunja project hierarchy in beads (flat structure)?
4. What's the conflict resolution UX in Slack bot context?
