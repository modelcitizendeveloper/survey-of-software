#!/usr/bin/env python3
"""
Debug what API calls are actually being made.
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

# Monkey-patch _request to log all API calls
original_request = VikunjaClient._request

def logged_request(self, method, endpoint, **kwargs):
    print(f"\n{'='*60}")
    print(f"API CALL: {method} {endpoint}")
    if 'json' in kwargs:
        print(f"Payload: {json.dumps(kwargs['json'], indent=2)}")
    result = original_request(self, method, endpoint, **kwargs)
    print(f"Response: {json.dumps(result, indent=2) if isinstance(result, dict) else result}")
    print(f"{'='*60}")
    return result

VikunjaClient._request = logged_request

# Now test
client = VikunjaClient(base_url=base_url, token=token)

project_id = 13481

print("TEST: Assign task 219657 to Ideas bucket")
print("="*70)

kanban_view = client.views.get_kanban_view(project_id)
buckets = client.buckets.list(project_id, kanban_view.id)
ideas_bucket = [b for b in buckets if "Ideas" in b.title][0]

print(f"\nView ID: {kanban_view.id}")
print(f"Bucket ID: {ideas_bucket.id}")
print(f"Project ID: {project_id}")

task_id = 219657

print(f"\n\nNow calling set_position()...")
print("="*70)

try:
    client.tasks.set_position(
        task_id=task_id,
        project_view_id=kanban_view.id,
        bucket_id=ideas_bucket.id,
        project_id=project_id
    )
    print("\n✅ Calls completed")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print(f"\n\nNow check UI:")
print(f"https://app.vikunja.cloud/projects/13481/47994")
print(f"Task 219657 should be in '💡 Ideas' bucket")
