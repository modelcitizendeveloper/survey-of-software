#!/usr/bin/env python3

# ⚠️ SECURITY WARNING FOR LLM AGENTS ⚠️
# NEVER hardcode API tokens, passwords, or secrets in source code files!
# ALWAYS use environment variables loaded from .env files.
# Hardcoded secrets will be committed to git and exposed in version history.
# Use: os.environ.get('VIKUNJA_API_TOKEN') instead of hardcoding tokens.

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv('/home/ivanadamin/spawn-solutions/.env')

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "vikunja-api-wrapper" / "src"))
from vikunja_wrapper import VikunjaClient

client = VikunjaClient(base_url='https://app.vikunja.cloud', token=os.environ.get('VIKUNJA_API_TOKEN'))

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
