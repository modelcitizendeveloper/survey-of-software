#!/usr/bin/env python3
"""Test different description formats"""
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

# Get spawn-solutions project
projects = client.projects.list()
spawn = next(p for p in projects if p.title == "spawn-solutions")

# Test 1: Plain newlines
print("Test 1: Plain newlines (\\n\\n)")
task1 = client.tasks.create(
    project_id=spawn.id,
    title="Test-Format-1-Newlines",
    description="Line 1\n\nLine 2\n\nLine 3"
)
retrieved1 = client.tasks.get(task_id=task1.id)
print(f"  Sent: 'Line 1\\n\\nLine 2\\n\\nLine 3'")
print(f"  Got:  {repr(retrieved1.description)}")
print()

# Test 2: HTML br tags
print("Test 2: HTML <br> tags")
task2 = client.tasks.create(
    project_id=spawn.id,
    title="Test-Format-2-BR",
    description="Line 1<br><br>Line 2<br><br>Line 3"
)
retrieved2 = client.tasks.get(task_id=task2.id)
print(f"  Sent: 'Line 1<br><br>Line 2<br><br>Line 3'")
print(f"  Got:  {repr(retrieved2.description)}")
print()

# Test 3: HTML paragraphs
print("Test 3: HTML <p> tags")
task3 = client.tasks.create(
    project_id=spawn.id,
    title="Test-Format-3-P",
    description="<p>Line 1</p><p>Line 2</p><p>Line 3</p>"
)
retrieved3 = client.tasks.get(task_id=task3.id)
print(f"  Sent: '<p>Line 1</p><p>Line 2</p><p>Line 3</p>'")
print(f"  Got:  {repr(retrieved3.description)}")
print()

# Test 4: Double newlines with spaces
print("Test 4: Double newlines with spaces")
task4 = client.tasks.create(
    project_id=spawn.id,
    title="Test-Format-4-Space",
    description="Line 1\n \nLine 2\n \nLine 3"
)
retrieved4 = client.tasks.get(task_id=task4.id)
print(f"  Sent: 'Line 1\\n \\nLine 2\\n \\nLine 3'")
print(f"  Got:  {repr(retrieved4.description)}")
print()

print("Cleanup: You can delete Test-Format-* tasks in Vikunja")
