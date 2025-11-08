#!/usr/bin/env python3
"""
List tasks from Vikunja project

Usage:
    python3 vikunja_task_list.py [project_id]

Default project_id: 13456 (Vikunja Integration)
"""
import sys
import os

# Add wrapper to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'vikunja-api-wrapper', 'src'))

from vikunja_wrapper import VikunjaClient

# Configuration
VIKUNJA_API_TOKEN = "tk_b58cb267d291c55985136b9f054a62e0502e803f"
VIKUNJA_BASE_URL = "https://app.vikunja.cloud"
DEFAULT_PROJECT_ID = 13456

def main():
    project_id = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PROJECT_ID

    client = VikunjaClient(base_url=VIKUNJA_BASE_URL, token=VIKUNJA_API_TOKEN)

    print("=" * 80)
    print(f"VIKUNJA TASKS - Project {project_id}")
    print("=" * 80)

    tasks = client.tasks.list(project_id=project_id)

    if not tasks:
        print("\n📭 No tasks found")
        return

    print(f"\n📋 Found {len(tasks)} tasks:\n")

    # Sort by priority (desc) then by done status
    tasks_sorted = sorted(tasks, key=lambda t: (-t.priority, t.done))

    for task in tasks_sorted:
        status = "✅ DONE" if task.done else "⏳ TODO"
        priority_str = f"P{task.priority}" if task.priority > 0 else ""
        bucket_str = f"[Bucket {task.bucket_id}]" if task.bucket_id > 0 else ""

        print(f"{status} [{task.id}] {task.title} {priority_str} {bucket_str}")

    # Summary
    completed = sum(1 for t in tasks if t.done)
    print("\n" + "=" * 80)
    print(f"Progress: {completed}/{len(tasks)} completed ({completed*100//len(tasks)}%)")
    print("=" * 80)

if __name__ == "__main__":
    main()
