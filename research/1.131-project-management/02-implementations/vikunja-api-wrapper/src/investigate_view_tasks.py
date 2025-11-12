#!/usr/bin/env python3
"""
Investigate why tasks aren't appearing in view task lists.
"""

import os
import sys
import json
from dotenv import load_dotenv
from vikunja_wrapper import VikunjaClient

load_dotenv()

base_url = os.getenv("VIKUNJA_BASE_URL", "https://app.vikunja.cloud")
token = os.getenv("VIKUNJA_API_TOKEN")

if not token:
    print("Error: VIKUNJA_API_TOKEN not set")
    sys.exit(1)

client = VikunjaClient(base_url=base_url, token=token)

project_id = 13481

print("=" * 70)
print("INVESTIGATING VIEW TASKS VS PROJECT TASKS")
print("=" * 70)

# Get Kanban view
kanban_view = client.views.get_kanban_view(project_id)
print(f"\nKanban view ID: {kanban_view.id}")

# Get tasks from project directly
print(f"\n1. Tasks from project endpoint:")
print(f"   GET /api/v1/projects/{project_id}/tasks")
project_tasks = client.tasks.list(project_id)
print(f"   Found: {len(project_tasks)} tasks")
for t in project_tasks[:5]:
    print(f"     - [{t.id}] {t.title[:40]}")
if len(project_tasks) > 5:
    print(f"     ... and {len(project_tasks) - 5} more")

# Get tasks from view endpoint
print(f"\n2. Tasks from view endpoint:")
print(f"   GET /api/v1/projects/{project_id}/views/{kanban_view.id}/tasks")
try:
    view_tasks = client._request("GET", f"/api/v1/projects/{project_id}/views/{kanban_view.id}/tasks")
    print(f"   Found: {len(view_tasks)} tasks")
    for t in view_tasks[:5]:
        print(f"     - [{t['id']}] {t['title'][:40]}")
    if len(view_tasks) > 5:
        print(f"     ... and {len(view_tasks) - 5} more")

    # Compare
    project_task_ids = {t.id for t in project_tasks}
    view_task_ids = {t['id'] for t in view_tasks}

    print(f"\n3. Comparison:")
    print(f"   Tasks in PROJECT but NOT in VIEW: {len(project_task_ids - view_task_ids)}")
    missing_from_view = project_task_ids - view_task_ids
    if missing_from_view:
        print(f"   IDs: {sorted(list(missing_from_view))}")
        print(f"\n   Details of missing tasks:")
        for tid in sorted(list(missing_from_view))[:10]:
            task = [t for t in project_tasks if t.id == tid][0]
            print(f"     - [{tid}] {task.title[:50]}")
            print(f"       bucket_id: {task.bucket_id}, priority: {task.priority}, done: {task.done}")

    print(f"\n   Tasks in VIEW but NOT in PROJECT: {len(view_task_ids - project_task_ids)}")

except Exception as e:
    print(f"   ❌ Error: {e}")

# Check if there's a filter on the view
print(f"\n4. Check view configuration:")
try:
    view_details = client._request("GET", f"/api/v1/projects/{project_id}/views/{kanban_view.id}")
    print(f"   View details keys: {list(view_details.keys())}")
    if 'filter' in view_details:
        print(f"   Filter: {json.dumps(view_details['filter'], indent=2)}")
    if 'bucket_configuration_mode' in view_details:
        print(f"   Bucket config mode: {view_details['bucket_configuration_mode']}")
    if 'default_bucket_id' in view_details:
        print(f"   Default bucket ID: {view_details['default_bucket_id']}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 70)
print("HYPOTHESIS")
print("=" * 70)

print("""
If tasks are missing from the view, possible reasons:

1. **View has a filter** - Only tasks matching certain criteria appear
2. **Tasks need to be explicitly added to views** - Not automatic
3. **Tasks must have a position set** - Our set_position() call might be failing silently
4. **Bucket assignment is required** - Tasks without buckets don't show in Kanban
5. **View caching** - API returns cached data

The fact that set_position() succeeds but the task doesn't appear in the
view suggests that either:
- The position endpoint doesn't actually add tasks to views
- There's an additional API call needed
- The view filters out tasks without certain properties
""")
