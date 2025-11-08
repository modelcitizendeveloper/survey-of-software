#!/usr/bin/env python3
"""
End-to-End Integration Tests for Vikunja API Wrapper

Tests CRUD operations for all three main resources:
- Projects (Lists)
- Tasks
- Labels

Usage:
    python integration_tests.py

Prerequisites:
    1. Vikunja API token configured in /home/ivanadmin/spawn-solutions/.env
    2. Dependencies installed: uv pip install -r requirements.txt python-dotenv
"""
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from vikunja_wrapper import VikunjaClient, VikunjaError

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


class IntegrationTestRunner:
    """Runs integration tests against Vikunja API"""

    def __init__(self, client):
        self.client = client
        self.passed = 0
        self.failed = 0
        self.test_resources = {
            'projects': [],
            'tasks': [],
            'labels': []
        }

    def test(self, name, func):
        """Run a single test"""
        try:
            print(f"\n{BLUE}▶{RESET} Testing: {name}")
            result = func()
            self.passed += 1
            print(f"{GREEN}✅ PASS{RESET}: {name}")
            return result
        except Exception as e:
            self.failed += 1
            print(f"{RED}❌ FAIL{RESET}: {name}")
            print(f"{RED}   Error: {e}{RESET}")
            import traceback
            traceback.print_exc()
            return None

    def cleanup(self):
        """Clean up test resources"""
        print(f"\n{YELLOW}🧹 Cleaning up test resources...{RESET}")

        # Note: Delete methods not implemented in wrapper yet
        # Cleanup will need to be done manually for now
        print(f"{YELLOW}   Note: Delete methods not in wrapper - clean up manually{RESET}")
        print(f"   Test labels created: {len(self.test_resources['labels'])}")
        print(f"   Test tasks created: {len(self.test_resources['tasks'])}")
        print(f"   Test projects created: {len(self.test_resources['projects'])}")

    def summary(self):
        """Print test summary"""
        total = self.passed + self.failed
        print("\n" + "=" * 70)
        print("INTEGRATION TEST SUMMARY")
        print("=" * 70)
        print(f"Total tests: {total}")
        print(f"{GREEN}Passed: {self.passed}{RESET}")
        print(f"{RED}Failed: {self.failed}{RESET}")

        if self.failed == 0:
            print(f"\n{GREEN}✅ ALL TESTS PASSED!{RESET}")
            return True
        else:
            print(f"\n{RED}❌ SOME TESTS FAILED{RESET}")
            return False


def main():
    """Run integration tests"""

    # Load .env from spawn-solutions root
    env_path = Path(__file__).parent.parent.parent.parent.parent.parent / '.env'

    print("=" * 70)
    print("VIKUNJA API WRAPPER - INTEGRATION TESTS")
    print("=" * 70)

    # Check if .env exists
    if not env_path.exists():
        print(f"{RED}❌ ERROR: .env file not found at: {env_path}{RESET}")
        print("\nRun test_token.py first to verify setup")
        return False

    # Load .env
    load_dotenv(env_path)
    token = os.environ.get('VIKUNJA_API_TOKEN')
    base_url = os.environ.get('VIKUNJA_BASE_URL', 'https://app.vikunja.cloud')

    if not token or token == 'your_vikunja_token_here':
        print(f"{RED}❌ ERROR: VIKUNJA_API_TOKEN not set{RESET}")
        return False

    print(f"{GREEN}✅{RESET} Using API: {base_url}")
    print(f"{GREEN}✅{RESET} Token loaded: {token[:30]}...")

    # Initialize client
    client = VikunjaClient(base_url=base_url, token=token)
    runner = IntegrationTestRunner(client)

    # ========================================================================
    # LABELS CRUD TESTS
    # ========================================================================
    print("\n" + "=" * 70)
    print("LABELS - CRUD TESTS")
    print("=" * 70)

    # Test: Create Label
    test_label = runner.test(
        "Labels - Create",
        lambda: client.labels.create(
            title="Test-Label-Integration",
            hex_color="#FF5733"
        )
    )
    if test_label:
        runner.test_resources['labels'].append(test_label.id)
        print(f"   Created label ID: {test_label.id}")

    # Test: List Labels
    labels = runner.test(
        "Labels - List",
        lambda: client.labels.list()
    )
    if labels:
        print(f"   Found {len(labels)} label(s)")

    # Test: Get Label (not implemented in wrapper yet)
    if test_label and hasattr(client.labels, 'get'):
        label_detail = runner.test(
            "Labels - Get by ID",
            lambda: client.labels.get(label_id=test_label.id)
        )
        if label_detail:
            print(f"   Retrieved label: {label_detail.title}")
    else:
        print(f"\n{YELLOW}⚠️  SKIP: Labels - Get by ID (method not implemented){RESET}")

    # Test: Update Label
    if test_label:
        updated_label = runner.test(
            "Labels - Update",
            lambda: client.labels.update(
                label_id=test_label.id,
                title="Test-Label-Updated",
                hex_color="#00FF00"
            )
        )
        if updated_label:
            print(f"   Updated label title: {updated_label.title}")

    # ========================================================================
    # PROJECTS CRUD TESTS
    # ========================================================================
    print("\n" + "=" * 70)
    print("PROJECTS - CRUD TESTS")
    print("=" * 70)

    # Test: Create Project
    test_project = runner.test(
        "Projects - Create",
        lambda: client.projects.create(
            title="Test-Project-Integration",
            description="Integration test project"
        )
    )
    if test_project:
        runner.test_resources['projects'].append(test_project.id)
        print(f"   Created project ID: {test_project.id}")

    # Test: List Projects
    projects = runner.test(
        "Projects - List",
        lambda: client.projects.list()
    )
    if projects:
        print(f"   Found {len(projects)} project(s)")

    # Test: Get Project
    if test_project:
        project_detail = runner.test(
            "Projects - Get by ID",
            lambda: client.projects.get(project_id=test_project.id)
        )
        if project_detail:
            print(f"   Retrieved project: {project_detail.title}")

    # Test: Update Project
    if test_project:
        updated_project = runner.test(
            "Projects - Update",
            lambda: client.projects.update(
                project_id=test_project.id,
                title="Test-Project-Updated",
                description="Updated description"
            )
        )
        if updated_project:
            print(f"   Updated project title: {updated_project.title}")

    # ========================================================================
    # TASKS CRUD TESTS
    # ========================================================================
    print("\n" + "=" * 70)
    print("TASKS - CRUD TESTS")
    print("=" * 70)

    # Test: Create Task (requires a project)
    if test_project:
        due_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
        test_task = runner.test(
            "Tasks - Create",
            lambda: client.tasks.create(
                project_id=test_project.id,
                title="Test-Task-Integration",
                description="Integration test task",
                due_date=due_date,
                priority=5
            )
        )
        if test_task:
            runner.test_resources['tasks'].append(test_task.id)
            print(f"   Created task ID: {test_task.id}")
    else:
        print(f"{YELLOW}⚠️  SKIP: Tasks - Create (no test project){RESET}")
        test_task = None

    # Test: List Tasks (all) - Not supported, requires project_id
    print(f"\n{YELLOW}⚠️  SKIP: Tasks - List All (requires project_id parameter){RESET}")

    # Test: List Tasks (by project)
    if test_project:
        project_tasks = runner.test(
            "Tasks - List by Project",
            lambda: client.tasks.list(project_id=test_project.id)
        )
        if project_tasks:
            print(f"   Found {len(project_tasks)} task(s) in project {test_project.id}")

    # Test: Get Task
    if test_task:
        task_detail = runner.test(
            "Tasks - Get by ID",
            lambda: client.tasks.get(task_id=test_task.id)
        )
        if task_detail:
            print(f"   Retrieved task: {task_detail.title}")

    # Test: Update Task
    if test_task:
        updated_task = runner.test(
            "Tasks - Update",
            lambda: client.tasks.update(
                task_id=test_task.id,
                title="Test-Task-Updated",
                done=True,
                priority=8
            )
        )
        if updated_task:
            print(f"   Updated task title: {updated_task.title}, done: {updated_task.done}")

    # ========================================================================
    # CLEANUP & SUMMARY
    # ========================================================================
    runner.cleanup()
    success = runner.summary()

    print("\n" + "=" * 70)
    if success:
        print("Next steps:")
        print("- Clean up test resources manually in Vikunja")
        print("- Use wrapper for real automation (SEA, cookbooks, qrcards)")
        print("- See SETUP_GUIDE.md for examples")
    else:
        print("Troubleshooting:")
        print("- Check API token permissions")
        print("- Review error messages above")
        print("- Check Vikunja API documentation for endpoint changes")
    print("=" * 70)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
