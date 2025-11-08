#!/usr/bin/env python3
"""Test different endpoint combinations to find what works"""
import os
import sys
from pathlib import Path
import requests

from dotenv import load_dotenv

# Load .env
env_path = Path(__file__).parent.parent.parent.parent.parent.parent / '.env'
load_dotenv(env_path)

token = os.environ.get('VIKUNJA_API_TOKEN')
base_url = os.environ.get('VIKUNJA_BASE_URL', 'https://app.vikunja.cloud')

headers = {"Authorization": f"Bearer {token}"}

# Test creating a project/list with different endpoints
endpoints_to_try = [
    ("POST", "/api/v1/lists"),
    ("PUT", "/api/v1/lists"),
    ("POST", "/api/v1/projects"),
    ("PUT", "/api/v1/projects"),
]

data = {"title": "Test-Endpoint-Discovery"}

print("Testing different endpoints for creating a project/list:")
print("=" * 70)

for method, endpoint in endpoints_to_try:
    print(f"\nTrying: {method} {endpoint}")
    try:
        url = f"{base_url}{endpoint}"
        if method == "POST":
            response = requests.post(url, headers=headers, json=data)
        else:
            response = requests.put(url, headers=headers, json=data)

        print(f"  Status: {response.status_code}")
        if response.status_code in [200, 201]:
            print(f"  ✅ SUCCESS! This endpoint works!")
            print(f"  Response: {response.json()}")
        else:
            print(f"  ❌ Failed: {response.text[:100]}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

print("\n" + "=" * 70)
