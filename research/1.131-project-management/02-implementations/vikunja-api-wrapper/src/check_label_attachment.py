#!/usr/bin/env python3
"""Check which label format actually attached the label"""
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

# Check the test tasks
task_ids = [216271, 216272, 216273]
task_names = [
    "Test-Label-Format-2-Objects",
    "Test-Label-Format-3-Full",
    "Test-Label-Format-4-LabelIDs"
]

for task_id, name in zip(task_ids, task_names):
    try:
        task = client.tasks.get(task_id=task_id)
        labels = task.labels if hasattr(task, 'labels') else []
        print(f"{name}:")
        print(f"  ID: {task.id}")
        print(f"  Labels: {labels}")
        print(f"  Has Security label: {'Yes' if labels else 'No'}")
        print()
    except Exception as e:
        print(f"{name}: Error - {e}\n")
