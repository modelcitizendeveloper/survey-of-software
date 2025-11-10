#!/usr/bin/env python3
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "vikunja-api-wrapper" / "src"))
from vikunja_wrapper import VikunjaClient

client = VikunjaClient(base_url='https://app.vikunja.cloud', token='tk_b58cb267d291c55985136b9f054a62e0502e803f')

# Get direct tasks in Applications main project
tasks = client.tasks.list(project_id=13448)
print(f"Applications main project (13448): {len(tasks) if tasks else 0} tasks")

# Find a child project with tasks to test export
all_projects = client.projects.list()
children = [p for p in all_projects if hasattr(p, 'parent_project_id') and p.parent_project_id == 13448]

print(f"\nChild projects with tasks:")
for child in children:
    tasks = client.tasks.list(project_id=child.id)
    task_count = len(tasks) if tasks else 0
    if task_count > 0:
        print(f"  {child.title} (ID: {child.id}): {task_count} tasks")
