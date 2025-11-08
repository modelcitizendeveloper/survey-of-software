#!/usr/bin/env python3
"""Check raw API response for task with label"""
import os
from pathlib import Path
import requests
import json

from dotenv import load_dotenv

# Load .env
env_path = Path(__file__).parent.parent.parent.parent.parent.parent / '.env'
load_dotenv(env_path)

token = os.environ.get('VIKUNJA_API_TOKEN')
base_url = os.environ.get('VIKUNJA_BASE_URL', 'https://app.vikunja.cloud')

headers = {"Authorization": f"Bearer {token}"}

# Check task 216273 (label_ids format)
task_id = 216273

response = requests.get(
    f"{base_url}/api/v1/tasks/{task_id}",
    headers=headers
)

print(f"Task {task_id} raw response:")
print(json.dumps(response.json(), indent=2))
