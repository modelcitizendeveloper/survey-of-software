#!/usr/bin/env python3
"""Test the exact description from add_api_reminder"""
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
spawn = next(p for p in projects if p.title == "spawn-solutions")

# Create the EXACT same description
description = (
    "Security maintenance: Rotate Vikunja API token\n\n"
    "**Steps:**\n\n"
    "1. Login to https://app.vikunja.cloud/\n"
    "2. Go to Settings → API Tokens\n"
    "3. Delete old token\n"
    "4. Create new token with same permissions\n"
    "5. Update /home/ivanadmin/spawn-solutions/.env\n"
    "6. Run test_token.py to verify\n"
    "7. Reschedule this task for 6-12 months\n\n"
    "**Recommended frequency:** Every 6-12 months"
)

print("Creating test task with reminder description...")
print(f"Description length: {len(description)}")
print(f"Newlines: {description.count(chr(10))}")

task = client.tasks.create(
    project_id=spawn.id,
    title="Test-Exact-Reminder-Description",
    description=description,
    priority=0
)

print(f"Created task ID: {task.id}")

# Retrieve it immediately
retrieved = client.tasks.get(task_id=task.id)

print("\nRetrieved description:")
print(repr(retrieved.description))
print(f"\nLength: {len(retrieved.description) if retrieved.description else 0}")
print(f"Newlines: {retrieved.description.count(chr(10)) if retrieved.description else 0}")
print("\nFormatted:")
print(retrieved.description)
