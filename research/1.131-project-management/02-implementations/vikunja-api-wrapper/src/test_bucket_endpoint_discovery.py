#!/usr/bin/env python3
"""
Discover the correct endpoint for assigning tasks to buckets.

Based on Vikunja 0.24.0 changelog, bucket_id in task update no longer works.
There's a new dedicated endpoint. Let's find it by testing patterns.
"""

import os
import sys
from dotenv import load_dotenv
from vikunja_wrapper import VikunjaClient

load_dotenv()

def test_endpoint_patterns():
    """Test different endpoint patterns to find the correct one."""

    base_url = os.getenv("VIKUNJA_BASE_URL", "https://app.vikunja.cloud")
    token = os.getenv("VIKUNJA_API_TOKEN")

    if not token:
        print("Error: VIKUNJA_API_TOKEN not set")
        sys.exit(1)

    client = VikunjaClient(base_url=base_url, token=token)

    # Use Talks project (13481)
    project_id = 13481

    # Get Kanban view and buckets
    print("Setup: Getting Kanban view and buckets...")
    kanban_view = client.views.get_kanban_view(project_id)
    buckets = client.buckets.list(project_id, kanban_view.id)
    test_bucket = buckets[0]

    print(f"  View ID: {kanban_view.id}")
    print(f"  Bucket: {test_bucket.title} (ID: {test_bucket.id})")

    # Create a test task
    print("\nCreating test task...")
    task = client.tasks.create(
        project_id=project_id,
        title="Test Bucket Endpoint Discovery"
    )
    print(f"  Task ID: {task.id}")

    # Try different endpoint patterns
    patterns = [
        # Pattern 1: POST to tasks with position INCLUDING project_id
        {
            "method": "POST",
            "url": f"/api/v1/tasks/{task.id}/position",
            "data": {"project_id": project_id, "project_view_id": kanban_view.id, "bucket_id": test_bucket.id, "position": 0}
        },
        # Pattern 1b: Same but with view_id instead of project_view_id
        {
            "method": "POST",
            "url": f"/api/v1/tasks/{task.id}/position",
            "data": {"project_id": project_id, "view_id": kanban_view.id, "bucket_id": test_bucket.id, "position": 0}
        },
        # Pattern 1c: Minimal version
        {
            "method": "POST",
            "url": f"/api/v1/tasks/{task.id}/position",
            "data": {"project_view_id": kanban_view.id, "bucket_id": test_bucket.id}
        },
        # Pattern 2: POST to tasks with bucket endpoint
        {
            "method": "POST",
            "url": f"/api/v1/tasks/{task.id}/buckets/{test_bucket.id}",
            "data": {"view_id": kanban_view.id}
        },
        # Pattern 3: PUT to tasks position
        {
            "method": "PUT",
            "url": f"/api/v1/tasks/{task.id}/position",
            "data": {"bucket_id": test_bucket.id, "view_id": kanban_view.id}
        },
        # Pattern 4: PATCH task position
        {
            "method": "PATCH",
            "url": f"/api/v1/tasks/{task.id}/position",
            "data": {"bucket_id": test_bucket.id, "view_id": kanban_view.id}
        },
        # Pattern 5: POST to buckets with task
        {
            "method": "POST",
            "url": f"/api/v1/buckets/{test_bucket.id}/tasks/{task.id}",
            "data": {"view_id": kanban_view.id}
        },
        # Pattern 6: Direct bucket assignment via POST to task in bucket
        {
            "method": "POST",
            "url": f"/api/v1/projects/{project_id}/views/{kanban_view.id}/buckets/{test_bucket.id}/tasks/{task.id}",
            "data": {}
        },
        # Pattern 7: POST task bucket assignment
        {
            "method": "POST",
            "url": f"/api/v1/projects/{project_id}/tasks/{task.id}/bucket",
            "data": {"bucket_id": test_bucket.id, "view_id": kanban_view.id}
        },
    ]

    print("\n=== Testing Endpoint Patterns ===\n")

    for i, pattern in enumerate(patterns, 1):
        print(f"Pattern {i}: {pattern['method']} {pattern['url']}")
        try:
            response = client._request(
                pattern["method"],
                pattern["url"],
                json=pattern["data"] if pattern["data"] else None
            )
            print(f"  ✅ SUCCESS! Status: 200")
            print(f"  Response: {response}")
            print(f"  Data sent: {pattern['data']}")

            # Verify bucket assignment
            fetched = client.tasks.get(task.id)
            print(f"  Task bucket_id after fetch: {fetched.bucket_id}")

            if fetched.bucket_id == test_bucket.id:
                print(f"  🎉 VERIFIED! Bucket assignment worked!")
                return pattern
            else:
                print(f"  ⚠️  Endpoint succeeded but bucket_id not set (expected: {test_bucket.id}, got: {fetched.bucket_id})")

        except Exception as e:
            error_str = str(e)
            if "404" in error_str or "Not Found" in error_str:
                print(f"  ❌ 404 Not Found")
            elif "405" in error_str or "Method Not Allowed" in error_str:
                print(f"  ❌ 405 Method Not Allowed")
            else:
                print(f"  ❌ Error: {error_str[:100]}")

        print()

    # Cleanup
    print("Cleanup: Deleting test task...")
    client.tasks.delete(task.id)

    print("\n❌ None of the tested patterns worked")
    return None

if __name__ == "__main__":
    try:
        result = test_endpoint_patterns()
        if result:
            print(f"\n✅ Found working endpoint:")
            print(f"   Method: {result['method']}")
            print(f"   URL: {result['url']}")
            print(f"   Data: {result['data']}")
        sys.exit(0 if result else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
