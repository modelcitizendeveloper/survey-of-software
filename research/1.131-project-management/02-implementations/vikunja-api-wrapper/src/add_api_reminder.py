#!/usr/bin/env python3
"""
Create API Token Renewal Reminder in Vikunja

Creates a one-time setup task to remind you to rotate the Vikunja API token
for security (recommended every 6-12 months).

Usage:
    python add_api_reminder.py

Prerequisites:
    1. Vikunja API token configured in /home/ivanadmin/spawn-solutions/.env
    2. Dependencies installed: uv pip install -r requirements.txt python-dotenv
    3. test_token.py passing (validates token works)
"""
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from vikunja_wrapper import VikunjaClient, VikunjaError


def main():
    """Create API token renewal reminder task"""

    # Load .env from spawn-solutions root (6 levels up from this script)
    env_path = Path(__file__).parent.parent.parent.parent.parent.parent / '.env'

    print("=" * 70)
    print("CREATE API TOKEN RENEWAL REMINDER")
    print("=" * 70)
    print()

    # Check if .env exists
    if not env_path.exists():
        print(f"❌ ERROR: .env file not found at: {env_path}")
        print("\nRun test_token.py first to verify setup")
        return False

    # Load .env
    load_dotenv(env_path)
    token = os.environ.get('VIKUNJA_API_TOKEN')
    base_url = os.environ.get('VIKUNJA_BASE_URL', 'https://app.vikunja.cloud')

    # Validate environment variables
    if not token or token == 'your_vikunja_token_here':
        print("❌ ERROR: VIKUNJA_API_TOKEN not set in .env file")
        return False

    print(f"✅ Using API: {base_url}")
    print(f"✅ Token loaded")
    print()

    # Initialize client
    try:
        client = VikunjaClient(base_url=base_url, token=token)
    except Exception as e:
        print(f"❌ ERROR: Could not initialize client: {e}")
        return False

    # Get all projects
    print("Looking for 'spawn-solutions' project...")
    try:
        projects = client.projects.list()
        print(f"✅ Found {len(projects)} project(s)")

        # Find or create spawn-solutions project
        spawn_project = None
        for project in projects:
            if project.title == "spawn-solutions":
                spawn_project = project
                print(f"✅ Found existing project: spawn-solutions (ID: {spawn_project.id})")
                break

        if not spawn_project:
            print("Creating new project: spawn-solutions...")
            spawn_project = client.projects.create(
                title="spawn-solutions",
                description="Infrastructure, automation, and maintenance tasks"
            )
            print(f"✅ Created project: spawn-solutions (ID: {spawn_project.id})")

    except VikunjaError as e:
        print(f"❌ ERROR: Could not list/create projects: {e}")
        print()
        print("This might be an API endpoint issue.")
        print("Try running integration_tests.py to diagnose the problem.")
        return False

    print()

    # Create Security label
    print("Creating 'Security' label...")
    security_label = None
    try:
        security_label = client.labels.create(
            title="Security",
            hex_color="#FF0000"  # Red
        )
        print(f"✅ Created label: Security (ID: {security_label.id})")
    except VikunjaError as e:
        print(f"⚠️  Could not create label (may already exist): {e}")
        # Try to find existing Security label
        try:
            all_labels = client.labels.list()
            security_label = next((l for l in all_labels if l.title == "Security"), None)
            if security_label:
                print(f"✅ Found existing Security label (ID: {security_label.id})")
        except:
            pass

    print()

    # Create task due in 1 month
    print("Creating 'Renew API token' task...")
    try:
        # Due date: 1 month from today (December 7, 2025)
        due_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")

        # Prepare task data
        task_data = {
            "project_id": spawn_project.id,
            "title": "Renew API token",
            "description": (
                "Security maintenance: Rotate Vikunja API token<br><br>"
                "<strong>Steps:</strong><br><br>"
                "1. Login to https://app.vikunja.cloud/<br>"
                "2. Go to Settings → API Tokens<br>"
                "3. Delete old token<br>"
                "4. Create new token with same permissions<br>"
                "5. Update /home/ivanadmin/spawn-solutions/.env<br>"
                "6. Run test_token.py to verify<br>"
                "7. Reschedule this task for 6-12 months<br><br>"
                "<strong>Recommended frequency:</strong> Every 6-12 months"
            ),
            "due_date": due_date,
            "priority": 0  # Unset (not urgent)
        }

        task = client.tasks.create(**task_data)
        print(f"✅ Created task: 'Renew API token' (ID: {task.id})")
        print(f"   Due date: {due_date}")
        print(f"   Priority: {task.priority}")

        # Attach Security label if available
        if security_label:
            try:
                client.tasks.add_label(task_id=task.id, label_id=security_label.id)
                print(f"✅ Attached Security label to task")
            except Exception as e:
                print(f"⚠️  Could not attach label: {e}")

    except VikunjaError as e:
        print(f"❌ ERROR: Could not create task: {e}")
        print()
        print("This might be an API endpoint issue.")
        print("Try running integration_tests.py to diagnose the problem.")
        return False

    print()
    print("=" * 70)
    print("✅ SETUP COMPLETE!")
    print("=" * 70)
    print()
    print("Created:")
    print(f"  📁 Project: spawn-solutions (ID: {spawn_project.id})")
    if security_label:
        print(f"  🏷️  Label: Security (ID: {security_label.id})")
    print(f"  ✅ Task: Renew API token (ID: {task.id}, due: {due_date})")
    print()
    print("Next steps:")
    print("  - View task in Vikunja: https://app.vikunja.cloud/")
    print("  - Set reminder notifications in Vikunja settings")
    print("  - Use wrapper for other automation (see SETUP_GUIDE.md)")
    print()

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
