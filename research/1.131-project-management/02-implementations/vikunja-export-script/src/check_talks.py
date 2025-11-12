#!/usr/bin/env python3
"""Quick script to view Talks project tasks."""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "vikunja-api-wrapper" / "src"))
from vikunja_wrapper import VikunjaClient

# Load token from .env
from dotenv import load_dotenv
load_dotenv('/home/ivanadamin/spawn-solutions/.env')

client = VikunjaClient(
    base_url=os.environ.get('VIKUNJA_BASE_URL'),
    token=os.environ.get('VIKUNJA_API_TOKEN')
)

# Find Talks project
all_projects = client.projects.list()
talks_project = None
for p in all_projects:
    if 'talk' in p.title.lower():
        talks_project = p
        break

if not talks_project:
    print("No Talks project found")
    print("Available projects:", [p.title for p in all_projects[:20]])
    sys.exit(1)

print(f"=== {talks_project.title} (ID: {talks_project.id}) ===\n")

# Get tasks
tasks = client.tasks.list(project_id=talks_project.id)

if not tasks:
    print("No tasks found")
else:
    for task in tasks:
        status = '✓' if task.done else '○'
        print(f"{status} {task.title}")

        if task.description:
            # Clean HTML tags for readability
            import re
            clean_desc = re.sub('<[^<]+?>', '', task.description)
            clean_desc = clean_desc.strip()
            if clean_desc:
                print(f"  {clean_desc[:200]}{'...' if len(clean_desc) > 200 else ''}")

        if task.due_date:
            print(f"  Due: {task.due_date.strftime('%Y-%m-%d')}")

        print()
