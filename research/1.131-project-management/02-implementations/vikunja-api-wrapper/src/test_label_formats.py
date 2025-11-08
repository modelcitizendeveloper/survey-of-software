#!/usr/bin/env python3
"""Test different label formats for task creation"""
import os
import sys
from pathlib import Path
import requests

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

# Get Security label
labels = client.labels.list()
security = next((l for l in labels if l.title == "Security"), None)

if not security:
    print("No Security label found - creating one")
    security = client.labels.create(title="Security", hex_color="#FF0000")

print(f"Security label: ID={security.id}, title={security.title}")
print()

# Test different formats directly with requests
headers = {"Authorization": f"Bearer {token}"}

# Format 1: Array of label IDs
print("Test 1: Array of label IDs [6524]")
response = requests.put(
    f"{base_url}/api/v1/projects/{spawn.id}/tasks",
    headers=headers,
    json={
        "title": "Test-Label-Format-1-IDs",
        "labels": [security.id]
    }
)
print(f"  Status: {response.status_code}")
print(f"  Response: {response.text[:200]}")
print()

# Format 2: Array of label objects with just ID
print("Test 2: Array of objects with ID [{{'id': 6524}}]")
response = requests.put(
    f"{base_url}/api/v1/projects/{spawn.id}/tasks",
    headers=headers,
    json={
        "title": "Test-Label-Format-2-Objects",
        "labels": [{"id": security.id}]
    }
)
print(f"  Status: {response.status_code}")
print(f"  Response: {response.text[:200]}")
print()

# Format 3: Array of full label objects
print("Test 3: Full label objects")
response = requests.put(
    f"{base_url}/api/v1/projects/{spawn.id}/tasks",
    headers=headers,
    json={
        "title": "Test-Label-Format-3-Full",
        "labels": [{
            "id": security.id,
            "title": security.title,
            "hex_color": security.hex_color
        }]
    }
)
print(f"  Status: {response.status_code}")
print(f"  Response: {response.text[:200]}")
print()

# Format 4: label_ids field
print("Test 4: label_ids field")
response = requests.put(
    f"{base_url}/api/v1/projects/{spawn.id}/tasks",
    headers=headers,
    json={
        "title": "Test-Label-Format-4-LabelIDs",
        "label_ids": [security.id]
    }
)
print(f"  Status: {response.status_code}")
print(f"  Response: {response.text[:200]}")
