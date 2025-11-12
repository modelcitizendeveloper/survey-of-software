#!/usr/bin/env python3
"""
Test manually moving a task between buckets using the Vikunja UI workflow.
Try to replicate what the UI does when you drag-and-drop.
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
print("MANUALLY INSPECT VIKUNJA UI NETWORK TRAFFIC")
print("=" * 70)

print("""
INSTRUCTIONS:

1. Open Vikunja in browser: https://app.vikunja.cloud/projects/13481/kanban
2. Open browser DevTools -> Network tab
3. Filter for "Fetch/XHR" requests
4. Create a new task in the default bucket
5. Drag it to the "💡 Ideas" bucket
6. Observe what API call is made

Expected to see something like:
  POST /api/v1/tasks/{id}/position
  or
  PUT /api/v1/tasks/{id}/bucket
  or
  POST /api/v1/projects/{id}/views/{view_id}/buckets/{bucket_id}/tasks

Let's test what our existing tasks look like and try different approaches.
""")

# Get setup
kanban_view = client.views.get_kanban_view(project_id)
buckets = client.buckets.list(project_id, kanban_view.id)

ideas_bucket = [b for b in buckets if "Ideas" in b.title][0]
todo_bucket = [b for b in buckets if b.title == "To-Do"][0]

print(f"\nSetup:")
print(f"  Kanban view: {kanban_view.id}")
print(f"  💡 Ideas bucket: {ideas_bucket.id}")
print(f"  To-Do bucket (default): {todo_bucket.id}")

# Use one of the test tasks
test_task_id = 219653  # "Go Programming Language"

print(f"\nUsing test task: {test_task_id}")

# Try different parameter combinations for set_position
test_cases = [
    {
        "name": "With project_id in data",
        "data": {
            "project_id": project_id,
            "project_view_id": kanban_view.id,
            "bucket_id": ideas_bucket.id,
            "position": 0
        }
    },
    {
        "name": "With position as float",
        "data": {
            "project_view_id": kanban_view.id,
            "bucket_id": ideas_bucket.id,
            "position": 0.0
        }
    },
    {
        "name": "Without position",
        "data": {
            "project_view_id": kanban_view.id,
            "bucket_id": ideas_bucket.id
        }
    },
    {
        "name": "With relative_to parameter",
        "data": {
            "project_view_id": kanban_view.id,
            "bucket_id": ideas_bucket.id,
            "position": 0,
            "relative_to": None
        }
    },
]

print(f"\n{'=' * 70}")
print(f"TESTING DIFFERENT PARAMETER COMBINATIONS")
print(f"{'=' * 70}")

for i, test_case in enumerate(test_cases, 1):
    print(f"\nTest {i}: {test_case['name']}")
    print(f"  Data: {json.dumps(test_case['data'], indent=4)}")

    try:
        response = client._request(
            "POST",
            f"/api/v1/tasks/{test_task_id}/position",
            json=test_case['data']
        )
        print(f"  ✅ Response: {json.dumps(response, indent=4)}")

        # Check task immediately
        task = client.tasks.get(test_task_id)
        print(f"  Task bucket_id after: {task.bucket_id}")

    except Exception as e:
        print(f"  ❌ Error: {e}")

    print()

print(f"\n{'=' * 70}")
print(f"FINAL CHECK")
print(f"{'=' * 70}")

task = client.tasks.get(test_task_id)
print(f"Task {test_task_id} final bucket_id: {task.bucket_id}")

print(f"\nNow check in Vikunja UI:")
print(f"  https://app.vikunja.cloud/projects/13481/kanban")
print(f"  Look for task: {task.title}")
print(f"  Is it in '💡 Ideas' bucket? _______")
