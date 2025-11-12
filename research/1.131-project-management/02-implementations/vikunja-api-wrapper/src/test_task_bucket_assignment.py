#!/usr/bin/env python3
"""
Test task bucket assignment via create + update approach.
"""

import os
import sys
from dotenv import load_dotenv
from vikunja_wrapper import VikunjaClient

load_dotenv()

def test_bucket_assignment():
    """Test if we can assign a bucket to a task via update after creation."""

    base_url = os.getenv("VIKUNJA_BASE_URL", "https://app.vikunja.cloud")
    token = os.getenv("VIKUNJA_API_TOKEN")

    if not token:
        print("Error: VIKUNJA_API_TOKEN not set")
        sys.exit(1)

    client = VikunjaClient(base_url=base_url, token=token)

    # Use Talks project (13481) which has buckets configured
    project_id = 13481

    # Get Kanban view
    print("Getting Kanban view...")
    kanban_view = client.views.get_kanban_view(project_id)
    print(f"  Kanban view ID: {kanban_view.id}")

    # Get buckets
    print("\nGetting buckets...")
    buckets = client.buckets.list(project_id, kanban_view.id)
    print(f"  Found {len(buckets)} buckets:")
    for b in buckets:
        print(f"    - {b.title} (ID: {b.id})")

    if not buckets:
        print("\nError: No buckets found in project")
        sys.exit(1)

    # Use first bucket for test
    test_bucket = buckets[0]
    print(f"\nWill assign to bucket: {test_bucket.title} (ID: {test_bucket.id})")

    # Test 1: Create task WITH bucket_id
    print("\n=== Test 1: Create with bucket_id ===")
    task1 = client.tasks.create(
        project_id=project_id,
        title="Test Bucket Assignment (Create with bucket)",
        description="Testing if create can assign bucket",
        bucket_id=test_bucket.id
    )
    print(f"  Task created: ID {task1.id}")
    print(f"  Returned bucket_id: {task1.bucket_id}")

    # Verify by fetching
    fetched1 = client.tasks.get(task1.id)
    print(f"  Fetched bucket_id: {fetched1.bucket_id}")
    success1 = (fetched1.bucket_id == test_bucket.id)
    print(f"  Result: {'✅ SUCCESS' if success1 else '❌ FAILED'}")

    # Test 2: Create task WITHOUT bucket, then update
    print("\n=== Test 2: Create without bucket, update after ===")
    task2 = client.tasks.create(
        project_id=project_id,
        title="Test Bucket Assignment (Update after)",
        description="Testing if update can assign bucket"
    )
    print(f"  Task created: ID {task2.id}")
    print(f"  Initial bucket_id: {task2.bucket_id}")

    # Update task to assign bucket
    print(f"  Updating to assign bucket {test_bucket.id}...")
    updated_task = client.tasks.update(task2.id, bucket_id=test_bucket.id)
    print(f"  Update returned bucket_id: {updated_task.bucket_id}")

    # Verify by fetching
    fetched2 = client.tasks.get(task2.id)
    print(f"  Fetched bucket_id: {fetched2.bucket_id}")
    success2 = (fetched2.bucket_id == test_bucket.id)
    print(f"  Result: {'✅ SUCCESS' if success2 else '❌ FAILED'}")

    # Cleanup
    print(f"\n=== Cleanup ===")
    print(f"  Deleting test task 1 (ID: {task1.id})...")
    client.tasks.delete(task1.id)
    print(f"  Deleting test task 2 (ID: {task2.id})...")
    client.tasks.delete(task2.id)

    # Result
    print(f"\n=== Summary ===")
    if success1:
        print(f"✅ Method 1 (Create with bucket_id): SUCCESS")
        print(f"   Recommendation: Use bucket_id parameter in create() method")
    else:
        print(f"❌ Method 1 (Create with bucket_id): FAILED")

    if success2:
        print(f"✅ Method 2 (Update after create): SUCCESS")
        print(f"   Can use as fallback if create doesn't support bucket_id")
    else:
        print(f"❌ Method 2 (Update after create): FAILED")

    return success1 or success2

if __name__ == "__main__":
    try:
        success = test_bucket_assignment()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
