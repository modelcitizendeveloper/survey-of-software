#!/usr/bin/env python3
"""Delete all test and duplicate labels"""
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

# Get all labels
labels = client.labels.list()

print(f"Found {len(labels)} label(s)")
print()

# Group labels by title
label_groups = {}
for label in labels:
    if label.title not in label_groups:
        label_groups[label.title] = []
    label_groups[label.title].append(label)

# Delete patterns
patterns_to_delete = ["Security", "API-Test", "Test-Label", "Test-Format", "Test-Exact"]

deleted_count = 0

for pattern in patterns_to_delete:
    matching_labels = []
    for title, label_list in label_groups.items():
        if pattern in title:
            matching_labels.extend(label_list)

    if not matching_labels:
        continue

    print(f"\n{pattern} labels:")
    for label in matching_labels:
        print(f"  - {label.title} (ID: {label.id}, color: {label.hex_color})")

    # Delete all
    for label in matching_labels:
        try:
            client.labels.delete(label_id=label.id)
            deleted_count += 1
            print(f"  ✅ Deleted {label.title} (ID: {label.id})")
        except Exception as e:
            print(f"  ❌ Error deleting {label.id}: {e}")

print()
print(f"Deleted {deleted_count} label(s) total")
