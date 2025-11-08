#!/usr/bin/env python3
"""Test adding label via task update"""
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

# Get Security label
response = requests.get(f"{base_url}/api/v1/labels", headers=headers)
labels = response.json()
security = next((l for l in labels if l['title'] == "Security"), None)

if not security:
    print("No Security label found")
    exit(1)

print(f"Security label ID: {security['id']}")
print()

# Create a test task
print("Creating test task...")
response = requests.put(
    f"{base_url}/api/v1/projects/13431/tasks",
    headers=headers,
    json={"title": "Test-Label-Via-Update"}
)
task = response.json()
task_id = task['id']
print(f"Created task {task_id}")
print()

# Try updating with labels field
print("Test 1: Update with labels field (array of objects)")
response = requests.post(
    f"{base_url}/api/v1/tasks/{task_id}",
    headers=headers,
    json={"labels": [{"id": security['id']}]}
)
print(f"  Status: {response.status_code}")
if response.status_code == 200:
    task_updated = response.json()
    print(f"  Labels: {task_updated.get('labels')}")
else:
    print(f"  Error: {response.text[:200]}")
print()

# Check final state
response = requests.get(f"{base_url}/api/v1/tasks/{task_id}", headers=headers)
final_task = response.json()
print(f"Final task labels: {final_task.get('labels')}")
