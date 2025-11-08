#!/usr/bin/env python3
"""Check how task description is stored in Vikunja"""
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

# Get the task we just created
task = client.tasks.get(task_id=216270)

print("Task title:", task.title)
print("\nDescription (raw):")
print(repr(task.description))
print("\nDescription (formatted):")
print(task.description)
print("\nDescription length:", len(task.description) if task.description else 0)
