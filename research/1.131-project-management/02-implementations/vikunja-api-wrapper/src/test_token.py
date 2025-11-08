#!/usr/bin/env python3
"""
Test Vikunja API token from .env file

This script verifies your Vikunja API token is properly configured
and has the correct permissions.

Usage:
    python test_token.py

Prerequisites:
    1. Created API token in Vikunja Cloud (see SETUP_GUIDE.md Step 1)
    2. Added token to /home/ivanadamin/spawn-solutions/.env (see SETUP_GUIDE.md Step 2)
    3. Installed dependencies: pip install -r requirements.txt python-dotenv
"""
import os
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from vikunja_wrapper import VikunjaClient, VikunjaError

def main():
    """Test Vikunja API token configuration"""

    # Load .env from spawn-solutions root (6 levels up from this script)
    # Path structure: spawn-solutions/research/1.131.../02-implementations/vikunja-api-wrapper/method-4-adaptive-tdd/test_token.py
    env_path = Path(__file__).parent.parent.parent.parent.parent.parent / '.env'

    print("=" * 70)
    print("Vikunja API Token Test")
    print("=" * 70)
    print()

    # Check if .env exists
    if not env_path.exists():
        print(f"❌ ERROR: .env file not found at: {env_path}")
        print()
        print("Setup Instructions:")
        print("1. Copy template: cp .env.template .env")
        print("2. Follow SETUP_GUIDE.md to create API token")
        print("3. Add token to .env file")
        print()
        return False

    # Load .env
    load_dotenv(env_path)
    print(f"✅ Found .env file: {env_path}")

    # Get credentials from environment
    token = os.environ.get('VIKUNJA_API_TOKEN')
    base_url = os.environ.get('VIKUNJA_BASE_URL', 'https://app.vikunja.cloud')

    # Validate environment variables
    if not token or token == 'your_vikunja_token_here':
        print()
        print("❌ ERROR: VIKUNJA_API_TOKEN not set in .env file")
        print()
        print("Setup Instructions:")
        print("1. Open .env file: nano .env")
        print("2. Replace 'your_vikunja_token_here' with actual token")
        print("3. Save and try again")
        print()
        print("To get token:")
        print("- Login to https://app.vikunja.cloud/")
        print("- Go to Settings → API Tokens")
        print("- Create new token with Projects, Tasks, Labels permissions")
        print("- Copy token and paste in .env")
        print()
        return False

    print(f"✅ VIKUNJA_API_TOKEN loaded")
    print(f"✅ Base URL: {base_url}")
    print(f"✅ Token preview: {token[:30]}...")
    print()

    # Test API connection
    print("Testing API connection...")
    print("-" * 70)

    try:
        client = VikunjaClient(base_url=base_url, token=token)

        # List projects
        projects = client.projects.list()
        print(f"✅ SUCCESS! Connected to Vikunja API")
        print(f"✅ Found {len(projects)} project(s)")
        print()

        if projects:
            print("Your Projects:")
            for project in projects:
                task_count = len(client.tasks.list(project_id=project.id))
                print(f"  📁 {project.title}")
                print(f"     ID: {project.id}")
                print(f"     Tasks: {task_count}")
                if project.description:
                    print(f"     Description: {project.description}")
                print()
        else:
            print("No projects yet. Create your first project:")
            print()
            print("  from vikunja_wrapper import VikunjaClient")
            print(f"  client = VikunjaClient('{base_url}', 'your-token')")
            print("  project = client.projects.create(title='My First Project')")
            print()

        # Test permissions by trying to create a test label
        print("Testing permissions (will create test label)...")
        try:
            test_label = client.labels.create(
                title="API-Test-Label",
                hex_color="#00FF00"
            )
            print(f"✅ Create permission: OK (created label ID: {test_label.id})")
            print(f"✅ Test label created (you can delete manually if needed)")
        except Exception as e:
            print(f"⚠️  Warning: Could not create test label: {e}")
            print("   Check token has 'Labels: Create' permission")

        print()
        print("=" * 70)
        print("✅ API TOKEN IS WORKING CORRECTLY!")
        print("=" * 70)
        print()
        print("Next Steps:")
        print("- Use wrapper in SEA automation (see SETUP_GUIDE.md Step 4.2)")
        print("- Use wrapper in cookbooks automation (see SETUP_GUIDE.md Step 4.3)")
        print("- Create your own automation scripts")
        print()

        return True

    except VikunjaError as e:
        print()
        print(f"❌ API Error: {e}")
        print()
        print("Troubleshooting:")
        print("1. Verify token has correct permissions:")
        print("   - Projects: Read, Create, Update, Delete")
        print("   - Tasks: Read, Create, Update, Delete")
        print("   - Labels: Read, Create, Update")
        print()
        print("2. Check token hasn't expired:")
        print("   - Go to Settings → API Tokens in Vikunja Cloud")
        print("   - Verify token is active")
        print()
        print("3. Ensure base_url is correct:")
        print(f"   - Current: {base_url}")
        print("   - Should be: https://app.vikunja.cloud (for Cloud)")
        print()
        return False

    except Exception as e:
        print()
        print(f"❌ Unexpected error: {type(e).__name__}: {e}")
        print()
        print("This might be a network issue or bug in the wrapper.")
        print("Please check your internet connection and try again.")
        print()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
