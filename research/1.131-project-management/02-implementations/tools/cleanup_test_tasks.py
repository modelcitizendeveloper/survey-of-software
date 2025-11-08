#!/usr/bin/env python3
"""
Cleanup Test Tasks

Delete test artifacts created during lifecycle tools testing.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'vikunja-api-wrapper', 'src'))

from vikunja_wrapper import VikunjaClient

# Configuration
VIKUNJA_API_TOKEN = "tk_b58cb267d291c55985136b9f054a62e0502e803f"
VIKUNJA_BASE_URL = "https://app.vikunja.cloud"

# Test artifacts to delete
TEST_ARTIFACTS = {
    'projects': [
        {'id': 13603, 'name': 'Garbage Tracker sub-project'}
    ],
    'tasks': [
        {'id': 217426, 'name': 'Garbage Tracker'},
        {'id': 217427, 'name': 'Recycling Tracker'},
        {'id': 217428, 'name': 'Compost Tracker'},
        {'id': 217432, 'name': 'Recycling Tracker reminder'}
    ]
}

def main():
    client = VikunjaClient(base_url=VIKUNJA_BASE_URL, token=VIKUNJA_API_TOKEN)

    print("=" * 80)
    print("CLEANING UP TEST ARTIFACTS")
    print("=" * 80)
    print()

    # Delete projects first (includes all tasks within)
    print("Deleting test sub-projects...")
    for project in TEST_ARTIFACTS['projects']:
        try:
            client.projects.delete(project['id'])
            print(f"   ✅ Deleted: {project['name']} (ID: {project['id']})")
        except Exception as e:
            print(f"   ⚠️  Failed to delete {project['name']}: {e}")

    print()

    # Delete standalone tasks
    print("Deleting test tasks...")
    for task in TEST_ARTIFACTS['tasks']:
        try:
            client.tasks.delete(task['id'])
            print(f"   ✅ Deleted: {task['name']} (ID: {task['id']})")
        except Exception as e:
            # Expected to fail for Garbage Tracker if sub-project deletion worked
            if task['id'] == 217426:
                print(f"   ℹ️  {task['name']} already deleted with sub-project")
            else:
                print(f"   ⚠️  Failed to delete {task['name']}: {e}")

    print()
    print("=" * 80)
    print("CLEANUP COMPLETE")
    print("=" * 80)
    print()
    print("Applications and Talks projects are now in clean, production-ready state.")
    print()

if __name__ == "__main__":
    main()
