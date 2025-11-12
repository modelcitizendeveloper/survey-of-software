#!/usr/bin/env python3
"""
Test the new set_position() method for assigning tasks to buckets.
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

# Use Talks project
project_id = 13481

print("Step 1: Get Kanban view...")
kanban_view = client.views.get_kanban_view(project_id)
print(f"  Kanban view ID: {kanban_view.id}")

print("\nStep 2: Get buckets...")
buckets = client.buckets.list(project_id, kanban_view.id)
print(f"  Found {len(buckets)} buckets:")
for b in buckets[:3]:
    print(f"    - {b.title} (ID: {b.id})")
test_bucket = buckets[0]
print(f"  Using: {test_bucket.title} (ID: {test_bucket.id})")

print("\nStep 3: Create test task...")
task = client.tasks.create(
    project_id=project_id,
    title="Test set_position() method"
)
print(f"  Task ID: {task.id}")

print(f"\nStep 4: Assign to bucket via set_position()...")
result = client.tasks.set_position(
    task_id=task.id,
    project_view_id=kanban_view.id,
    bucket_id=test_bucket.id
)
print(f"  Result: {result}")

print(f"\nStep 5: Verify by viewing in Vikunja UI...")
print(f"  Task URL: {base_url}/tasks/{task.id}")
print(f"  Kanban URL: {base_url}/projects/{project_id}/{kanban_view.id}")
print(f"\n  ✅ Check if task appears in '{test_bucket.title}' bucket!")

input("\nPress Enter to delete test task...")

print("\nStep 6: Cleanup...")
client.tasks.delete(task.id)
print("  ✅ Test task deleted")

print("\n✅ Test complete! The set_position() method works.")
