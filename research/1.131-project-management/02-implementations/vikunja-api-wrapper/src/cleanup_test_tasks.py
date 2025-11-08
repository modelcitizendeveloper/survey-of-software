#!/usr/bin/env python3
"""Delete all test tasks"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from vikunja_wrapper import VikunjaClient

# Load .env
env_path = Path(__file__).parent.parent.parent.parent.parent.parent / '.env'
load_dotenv(env_path)

token = os.environ.get('VIKUNJA_API_TOKEN')
base_url = os.environ.get('VIKUNJA_BASE_URL', 'https://app.vikunja.cloud')

client = VikunjaClient(base_url=base_url, token=token)

# Get spawn-solutions project
projects = client.projects.list()
spawn = next((p for p in projects if p.title == "spawn-solutions"), None)

if not spawn:
    print("No spawn-solutions project found")
    sys.exit(0)

# Get all tasks in the project
tasks = client.tasks.list(project_id=spawn.id)

print(f"Found {len(tasks)} tasks in spawn-solutions project")
print()

# Delete tasks matching our test patterns
patterns_to_delete = [
    "Renew API token",
    "Test-Format-",
    "Test-Exact-",
]

deleted_count = 0
for task in tasks:
    should_delete = any(pattern in task.title for pattern in patterns_to_delete)

    if should_delete:
        print(f"Deleting: {task.title} (ID: {task.id})")
        try:
            client.tasks.delete(task_id=task.id)
            deleted_count += 1
            print(f"  ✅ Deleted")
        except Exception as e:
            print(f"  ❌ Error: {e}")

print()
print(f"Deleted {deleted_count} task(s)")
