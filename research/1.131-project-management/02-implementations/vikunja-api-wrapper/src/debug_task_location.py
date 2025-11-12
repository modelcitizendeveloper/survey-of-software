#!/usr/bin/env python3
"""
Debug where tasks actually are in the Vikunja UI.
Check if set_position() is working by querying bucket contents.
"""

import os
import sys
from dotenv import load_dotenv
from vikunja_wrapper import VikunjaClient

load_dotenv()

base_url = os.getenv("VIKUNJA_BASE_URL", "https://app.vikunja.cloud")
token = os.getenv("VIKUNJA_API_TOKEN")

if not token:
    print("Error: VIKUNJA_API_TOKEN not set")
    sys.exit(1)

client = VikunjaClient(base_url=base_url, token=token)

# Check task 219653 mentioned in bug report
task_ids_to_check = [219653, 219642, 219643, 219644]
project_id = 13481

print("=" * 70)
print("DEBUGGING TASK LOCATIONS")
print("=" * 70)

# Get Kanban view
print("\nStep 1: Get Kanban view...")
kanban_view = client.views.get_kanban_view(project_id)
print(f"  Kanban view ID: {kanban_view.id}")

# Get all buckets
print("\nStep 2: Get all buckets in Kanban view...")
buckets = client.buckets.list(project_id, kanban_view.id)
print(f"  Found {len(buckets)} buckets:")
for b in buckets:
    print(f"    - {b.title} (ID: {b.id})")

# Find "💡 Ideas" bucket
ideas_bucket = None
for b in buckets:
    if "Ideas" in b.title or b.title == "💡 Ideas":
        ideas_bucket = b
        break

if not ideas_bucket:
    print("\n❌ ERROR: Could not find '💡 Ideas' bucket!")
    sys.exit(1)

print(f"\n  Target bucket: {ideas_bucket.title} (ID: {ideas_bucket.id})")

# Check each task
print("\n" + "=" * 70)
print("CHECKING TASKS")
print("=" * 70)

for task_id in task_ids_to_check:
    print(f"\nTask ID: {task_id}")
    try:
        # Get task details
        task = client.tasks.get(task_id)
        print(f"  Title: {task.title}")
        print(f"  Project ID: {task.project_id}")
        print(f"  bucket_id field: {task.bucket_id}")

        # Try to get task position via API
        try:
            # This endpoint might not exist, but let's try
            position_response = client._request("GET", f"/api/v1/tasks/{task_id}/positions")
            print(f"  Position info: {position_response}")
        except Exception as e:
            if "404" not in str(e):
                print(f"  Position query error: {e}")

    except Exception as e:
        print(f"  ❌ Error fetching task: {e}")

# Check what tasks are IN the Ideas bucket
print("\n" + "=" * 70)
print(f"TASKS IN '💡 Ideas' BUCKET")
print("=" * 70)

# Try to get tasks from the bucket via different endpoints
print(f"\nAttempt 1: GET bucket tasks directly...")
try:
    # Try getting tasks in bucket
    bucket_tasks = client._request(
        "GET",
        f"/api/v1/projects/{project_id}/views/{kanban_view.id}/buckets/{ideas_bucket.id}/tasks"
    )
    print(f"  Found {len(bucket_tasks)} tasks:")
    for t in bucket_tasks:
        print(f"    - [{t.get('id')}] {t.get('title', 'No title')[:50]}")

    # Check if our test tasks are in this list
    task_ids_in_bucket = {t.get('id') for t in bucket_tasks}
    print(f"\n  Test tasks in Ideas bucket:")
    for tid in task_ids_to_check:
        status = "✅ YES" if tid in task_ids_in_bucket else "❌ NO"
        print(f"    Task {tid}: {status}")

except Exception as e:
    print(f"  ❌ Error: {e}")
    print(f"  Endpoint might not exist or parameters wrong")

# Alternative: Get ALL tasks and try to determine their bucket
print(f"\nAttempt 2: Get all project tasks and check positions...")
try:
    all_tasks = client.tasks.list(project_id)
    print(f"  Total tasks in project: {len(all_tasks)}")

    test_tasks = [t for t in all_tasks if t.id in task_ids_to_check]
    print(f"  Found {len(test_tasks)}/{len(task_ids_to_check)} test tasks in project")

    for t in test_tasks:
        print(f"    - [{t.id}] {t.title[:50]} - bucket_id: {t.bucket_id}")

except Exception as e:
    print(f"  ❌ Error: {e}")

print("\n" + "=" * 70)
print("RECOMMENDATION")
print("=" * 70)

print("""
If test tasks are NOT in the Ideas bucket, the set_position() method is not
working as expected. Possible reasons:

1. The endpoint accepts the request but doesn't persist the bucket assignment
2. The parameters are correct but there's an additional step required
3. The Vikunja API has another breaking change we haven't discovered
4. There's a permissions issue with the API token

Next steps:
- Try creating a NEW task and immediately checking if it's in the bucket
- Try calling set_position() with different parameters
- Check Vikunja API documentation or source code directly
""")
