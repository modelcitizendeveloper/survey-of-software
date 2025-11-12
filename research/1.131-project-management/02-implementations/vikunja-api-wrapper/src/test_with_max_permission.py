#!/usr/bin/env python3
"""
Test set_position() with max_permission parameter that the UI uses.
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

project_id = 13481

print("=" * 70)
print("TESTING WITH max_permission PARAMETER")
print("=" * 70)

# Get Kanban view and bucket
kanban_view = client.views.get_kanban_view(project_id)
buckets = client.buckets.list(project_id, kanban_view.id)
ideas_bucket = [b for b in buckets if "Ideas" in b.title][0]

print(f"\nSetup:")
print(f"  Kanban view: {kanban_view.id}")
print(f"  Ideas bucket: {ideas_bucket.id}")

# Test with existing task 219653 (Go Programming Language)
test_task_id = 219653

print(f"\nTest task: {test_task_id}")

# Call with max_permission=None (exactly like UI)
print(f"\nCalling set_position() with max_permission=None...")
payload = {
    "max_permission": None,
    "position": 0,
    "project_view_id": kanban_view.id,
    "task_id": test_task_id,
    "bucket_id": ideas_bucket.id  # Adding bucket_id too
}

print(f"Payload: {payload}")

try:
    response = client._request(
        "POST",
        f"/api/v1/tasks/{test_task_id}/position",
        json=payload
    )
    print(f"\n✅ API Response: {response}")
except Exception as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)

# Verify
task = client.tasks.get(test_task_id)
print(f"\nTask bucket_id after: {task.bucket_id}")

print(f"\n{'=' * 70}")
print("NOW CHECK VIKUNJA UI")
print(f"{'=' * 70}")
print(f"\nOpen: https://app.vikunja.cloud/projects/13481/47994")
print(f"Look for: NWES 2026 Talk (task {test_task_id})")
print(f"Expected: Should be in '💡 Ideas' bucket")
print(f"\nIs it there? (y/n): ", end="")
