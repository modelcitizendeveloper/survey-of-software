#!/usr/bin/env python3
"""
Mark Vikunja tasks as complete

Usage:
    python3 vikunja_complete_tasks.py <task_id> [task_id ...]

Example:
    python3 vikunja_complete_tasks.py 216369 216370
"""
import sys
import os

# Add wrapper to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'vikunja-api-wrapper', 'src'))

from vikunja_wrapper import VikunjaClient

# Configuration
VIKUNJA_API_TOKEN = "tk_b58cb267d291c55985136b9f054a62e0502e803f"
VIKUNJA_BASE_URL = "https://app.vikunja.cloud"

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 vikunja_complete_tasks.py <task_id> [task_id ...]")
        print("\nExample:")
        print("  python3 vikunja_complete_tasks.py 216369 216370")
        sys.exit(1)

    task_ids = [int(x) for x in sys.argv[1:]]

    client = VikunjaClient(base_url=VIKUNJA_BASE_URL, token=VIKUNJA_API_TOKEN)

    print("=" * 80)
    print("MARKING TASKS AS COMPLETE")
    print("=" * 80)

    for task_id in task_ids:
        try:
            # Get current task
            task = client.tasks.get(task_id)

            if task.done:
                print(f"\n⚠️  Task {task_id} already completed: {task.title}")
                continue

            # Mark as done
            updated = client.tasks.update(task_id=task_id, done=True)

            print(f"\n✅ Completed [{task_id}]: {task.title}")

        except Exception as e:
            print(f"\n❌ Error completing task {task_id}: {e}")

    print("\n" + "=" * 80)
    print(f"Marked {len(task_ids)} task(s) as complete")
    print("=" * 80)

if __name__ == "__main__":
    main()
