#!/usr/bin/env python3
"""Try different label attachment endpoints"""
import os
from pathlib import Path
import requests

from dotenv import load_dotenv

# Load .env
env_path = Path(__file__).parent.parent.parent.parent.parent.parent / '.env'
load_dotenv(env_path)

token = os.environ.get('VIKUNJA_API_TOKEN')
base_url = os.environ.get('VIKUNJA_BASE_URL', 'https://app.vikunja.cloud')

headers = {"Authorization": f"Bearer {token}"}

task_id = 216274  # Test task from previous script
label_id = 6524   # Security label

# Try different endpoints
endpoints_to_try = [
    ("PUT", f"/api/v1/tasks/{task_id}/labels"),
    ("PUT", f"/api/v1/tasks/{task_id}/labels/{label_id}"),
    ("POST", f"/api/v1/tasks/{task_id}/labels"),
    ("POST", f"/api/v1/tasks/{task_id}/labels/{label_id}"),
    ("PUT", f"/api/v1/labels/{label_id}/tasks/{task_id}"),
]

print("Testing label attachment endpoints:")
print("=" * 70)

for method, endpoint in endpoints_to_try:
    print(f"\n{method} {endpoint}")

    if method == "PUT":
        response = requests.put(f"{base_url}{endpoint}", headers=headers, json={"label_id": label_id})
    else:
        response = requests.post(f"{base_url}{endpoint}", headers=headers, json={"label_id": label_id})

    print(f"  Status: {response.status_code}")
    if response.status_code in [200, 201]:
        print(f"  ✅ SUCCESS!")
        print(f"  Response: {response.text[:150]}")

        # Check if label is now attached
        check = requests.get(f"{base_url}/api/v1/tasks/{task_id}", headers=headers)
        task = check.json()
        print(f"  Task labels after: {task.get('labels')}")
        break
    else:
        print(f"  ❌ {response.text[:100]}")
