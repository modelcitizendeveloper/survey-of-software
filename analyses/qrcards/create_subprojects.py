#!/usr/bin/env python3
"""
Create QRCards subprojects in Vikunja
Bypasses populate script bugs by using API wrapper directly
"""

import sys
sys.path.insert(0, '/home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-api-wrapper/src')
from vikunja_wrapper import VikunjaClient
from dotenv import load_dotenv
import os

load_dotenv('/home/ivanadamin/spawn-solutions/.env')

client = VikunjaClient(
    base_url=os.environ.get('VIKUNJA_BASE_URL', 'https://app.vikunja.cloud'),
    token=os.environ.get('VIKUNJA_API_TOKEN')
)

print("Creating subprojects under Infrastructure (14214)...\n")

# 1. Create Python API Integration subproject
print("1. Creating Python API Integration subproject...")
python_api_project = client.projects.create(
    title="Python API Integration",
    description="Enable Python execution capabilities for QRCards platform - Flask API + Jupyter integration patterns",
    hex_color="3498db",  # Blue
    parent_project_id=14214
)
print(f"   ✅ Created: {python_api_project.title} (ID: {python_api_project.id})")
print(f"   🌐 URL: https://app.vikunja.cloud/projects/{python_api_project.id}")

# 2. Create Render Migration subproject
print("\n2. Creating Render Migration subproject...")
render_project = client.projects.create(
    title="Render Migration",
    description="Migrate QRCards hosting from PythonAnywhere to Render.com - 7 customer subdomains, 101 SQLite databases",
    hex_color="e67e22",  # Orange
    parent_project_id=14214
)
print(f"   ✅ Created: {render_project.title} (ID: {render_project.id})")
print(f"   🌐 URL: https://app.vikunja.cloud/projects/{render_project.id}")

print("\n✅ Subprojects created successfully!")
print("\nNext steps:")
print("1. Manually add tasks to each subproject via Vikunja UI")
print("2. Or use populate script after debugging the label issue")
print(f"3. Clean up old Infrastructure (14214) tasks")
