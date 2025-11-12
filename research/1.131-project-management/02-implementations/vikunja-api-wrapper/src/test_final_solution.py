#!/usr/bin/env python3
"""
Test the FINAL solution with the corrected set_position() method.
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
print("TESTING FINAL SOLUTION")
print("=" * 70)

# Get Kanban view and bucket
print("\nSetup...")
kanban_view = client.views.get_kanban_view(project_id)
buckets = client.buckets.list(project_id, kanban_view.id)
ideas_bucket = [b for b in buckets if "Ideas" in b.title][0]

print(f"  Kanban view: {kanban_view.id}")
print(f"  Ideas bucket: '{ideas_bucket.title}' (ID: {ideas_bucket.id})")

# Test with task 219644 (Rust Programming Language)
test_task_id = 219644

print(f"\nTest task: {test_task_id}")

# Call the updated set_position() method
print(f"\nCalling set_position() with correct parameters...")
print(f"  This will make TWO API calls:")
print(f"    1. Set bucket (with max_permission, bucket_id, project_id)")
print(f"    2. Set position (with max_permission)")

try:
    response = client.tasks.set_position(
        task_id=test_task_id,
        project_view_id=kanban_view.id,
        bucket_id=ideas_bucket.id,
        project_id=project_id
    )
    print(f"\n✅ Success! Response: {response}")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print(f"\n{'=' * 70}")
print("VERIFICATION")
print(f"{'=' * 70}")

print(f"\n✅ API calls completed successfully!")
print(f"\nNow verify in Vikunja UI:")
print(f"  1. Open: https://app.vikunja.cloud/projects/13481/47994")
print(f"  2. Look for: 'Rust Programming Language' (task {test_task_id})")
print(f"  3. Expected: Should be in '💡 Ideas' bucket")
print(f"\nIs it there? ", end="")

# Wait for user confirmation
answer = input().strip().lower()

if answer in ['y', 'yes']:
    print(f"\n🎉 SUCCESS! The fix works!")
    print(f"\nThe solution required:")
    print(f"  1. Including 'max_permission': null in the payload")
    print(f"  2. Making TWO API calls (bucket assignment, then position)")
    print(f"  3. Including project_id in the bucket assignment call")
elif answer in ['n', 'no']:
    print(f"\n❌ Still not working. Need more investigation.")
    print(f"Can you check the Network tab for what API calls were made?")
else:
    print(f"\nPlease check the UI and let me know if it worked.")
