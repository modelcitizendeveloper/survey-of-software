#!/usr/bin/env python3
"""Delete specific task"""
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

# Delete task 216270
task_id = 216270
print(f"Deleting task {task_id}...")
client.tasks.delete(task_id=task_id)
print(f"✅ Deleted task {task_id}")
