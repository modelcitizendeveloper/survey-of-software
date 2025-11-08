#!/usr/bin/env python3
"""Verify the final task has the Security label"""
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

# Get task 216275
task = client.tasks.get(task_id=216275)

print(f"Task: {task.title}")
print(f"ID: {task.id}")
print(f"Due: {task.due_date}")
print(f"Priority: {task.priority}")
print(f"Labels: {task.labels}")
print()

if task.labels and len(task.labels) > 0:
    print(f"✅ SUCCESS! Task has {len(task.labels)} label(s):")
    for label in task.labels:
        print(f"  - {label.get('title')} (ID: {label.get('id')}, color: {label.get('hex_color')})")
else:
    print("❌ No labels found on task")
