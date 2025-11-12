#!/usr/bin/env python3
"""
Test with EXACT payload that the UI sends (without bucket_id).
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
kanban_view_id = 47994

print("=" * 70)
print("TESTING WITH EXACT UI PAYLOAD (NO bucket_id)")
print("=" * 70)

# Test with task 219642 (Flask Framework)
test_task_id = 219642

print(f"\nTest task: {test_task_id}")
print(f"View: {kanban_view_id}")

# EXACT payload from UI (when dragging task 217393)
# UI sent: {"max_permission":null,"position":0,"project_view_id":47994,"task_id":217393}
# Notice: NO bucket_id!

payload = {
    "max_permission": None,
    "position": 0,
    "project_view_id": kanban_view_id,
    "task_id": test_task_id
}

print(f"\nPayload (exact match to UI): {payload}")
print(f"Note: NO bucket_id in payload!")

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

print(f"\n{'=' * 70}")
print("QUESTION")
print(f"{'=' * 70}")

print(f"""
The UI doesn't send bucket_id in the position payload!

This means the bucket must have been set BEFORE calling position endpoint.

Question: When you dragged task 217393 in the UI:
1. Where was it BEFORE the drag?
2. Where did you drag it TO?

Maybe the position endpoint is ONLY for ordering within a bucket,
and there's a SEPARATE API call for changing buckets?

Or maybe the bucket is determined by WHERE you drop the task
(the drop zone determines bucket, then position is set)?

Please check DevTools Network tab - were there TWO API calls?
1. One to change the bucket
2. One to set the position
""")
