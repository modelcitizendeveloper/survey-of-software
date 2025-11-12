#!/usr/bin/env python3
"""
Create a task, call set_position(), and examine the actual API response.
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
print("TESTING set_position() WITH DETAILED LOGGING")
print("=" * 70)

# Get Kanban view and bucket
print("\nStep 1: Setup...")
kanban_view = client.views.get_kanban_view(project_id)
buckets = client.buckets.list(project_id, kanban_view.id)
ideas_bucket = [b for b in buckets if "Ideas" in b.title][0]

print(f"  Kanban view ID: {kanban_view.id}")
print(f"  Ideas bucket ID: {ideas_bucket.id}")

# Create a test task
print("\nStep 2: Create test task...")
task = client.tasks.create(
    project_id=project_id,
    title="Debug Test - Position Assignment"
)
print(f"  Created task ID: {task.id}")
print(f"  Task bucket_id (initial): {task.bucket_id}")

# Call set_position and capture the response
print(f"\nStep 3: Call set_position()...")
print(f"  Parameters:")
print(f"    task_id: {task.id}")
print(f"    project_view_id: {kanban_view.id}")
print(f"    bucket_id: {ideas_bucket.id}")

try:
    response = client.tasks.set_position(
        task_id=task.id,
        project_view_id=kanban_view.id,
        bucket_id=ideas_bucket.id
    )
    print(f"\n  ✅ API call succeeded!")
    print(f"  Response: {json.dumps(response, indent=2)}")
except Exception as e:
    print(f"\n  ❌ API call failed: {e}")
    sys.exit(1)

# Fetch the task again to see if anything changed
print(f"\nStep 4: Fetch task again to verify...")
fetched_task = client.tasks.get(task.id)
print(f"  Task bucket_id (after set_position): {fetched_task.bucket_id}")

# Check via direct API call to see raw response
print(f"\nStep 5: Raw API call to get task...")
raw_task = client._request("GET", f"/api/v1/tasks/{task.id}")
print(f"  Raw task response keys: {list(raw_task.keys())}")
print(f"  Raw task bucket_id: {raw_task.get('bucket_id')}")

# Check if there's a positions field or similar
if 'positions' in raw_task:
    print(f"  Raw task positions: {raw_task['positions']}")
if 'kanban_position' in raw_task:
    print(f"  Raw task kanban_position: {raw_task['kanban_position']}")

# Try to list tasks via view endpoint
print(f"\nStep 6: Try to get tasks via view endpoint...")
try:
    view_tasks = client._request("GET", f"/api/v1/projects/{project_id}/views/{kanban_view.id}/tasks")
    print(f"  Found {len(view_tasks)} tasks in view")

    # Find our task
    our_task_in_view = [t for t in view_tasks if t['id'] == task.id]
    if our_task_in_view:
        print(f"  ✅ Our task found in view!")
        print(f"  View task data: {json.dumps(our_task_in_view[0], indent=2)}")
    else:
        print(f"  ❌ Our task NOT found in view tasks list")
except Exception as e:
    print(f"  Error: {e}")

print("\n" + "=" * 70)
print("CLEANUP")
print("=" * 70)

input("\nPress Enter to delete test task (or Ctrl+C to keep for manual inspection)...")

client.tasks.delete(task.id)
print(f"✅ Test task {task.id} deleted")

print("\n" + "=" * 70)
print("CONCLUSION")
print("=" * 70)

if fetched_task.bucket_id == 0:
    print("""
❌ CONFIRMED: set_position() does NOT set bucket_id on the task

The API call succeeds, returns a response, but the task's bucket_id
remains 0. This means either:

1. bucket_id is deprecated and we need to query positions differently
2. The position endpoint is for a different purpose (ordering within a view)
3. We're missing a required step or parameter
4. The Vikunja API documentation is outdated/incorrect

NEXT STEP: Need to find how to ACTUALLY query which bucket a task is in,
since bucket_id field is not reliable.
    """)
else:
    print(f"✅ bucket_id was set to: {fetched_task.bucket_id}")
