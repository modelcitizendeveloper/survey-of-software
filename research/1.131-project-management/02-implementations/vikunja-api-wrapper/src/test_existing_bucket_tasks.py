#!/usr/bin/env python3
"""
Check if existing tasks in buckets have bucket_id set.
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

# Use Talks project which has tasks in buckets
project_id = 13481

print("Getting all tasks in Talks project...")
tasks = client.tasks.list(project_id)
print(f"Found {len(tasks)} tasks\n")

# Check bucket_id values
bucket_ids = {}
for task in tasks:
    bid = task.bucket_id
    if bid not in bucket_ids:
        bucket_ids[bid] = []
    bucket_ids[bid].append(task.title[:50])

print("Tasks grouped by bucket_id:")
for bid, task_titles in sorted(bucket_ids.items()):
    print(f"\nbucket_id={bid}: {len(task_titles)} tasks")
    for title in task_titles[:3]:
        print(f"  - {title}")
    if len(task_titles) > 3:
        print(f"  ... and {len(task_titles) - 3} more")

print("\n" + "="*60)
if all(bid == 0 for bid in bucket_ids.keys()):
    print("❌ ALL tasks have bucket_id=0")
    print("This confirms bucket_id is NO LONGER stored on tasks!")
    print("\nHypothesis: Buckets are now a VIEW-LEVEL concept,")
    print("not a task property. Tasks are positioned in buckets")
    print("via the position endpoint, but don't store bucket_id.")
else:
    print("✅ Some tasks have non-zero bucket_id")
    print("Tasks DO store bucket_id")
