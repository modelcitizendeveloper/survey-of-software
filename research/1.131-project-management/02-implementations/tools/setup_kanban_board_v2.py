#!/usr/bin/env python3
"""
Setup Kanban Board for Vikunja Project (Modern API)

Creates kanban view and buckets for a project using current Vikunja API.

Usage:
    python3 setup_kanban_board_v2.py <project_id> [--template TEMPLATE]

Templates:
    - talks: Speaking pipeline (Idea → Proposal → Accepted → Prep → Done)
    - sprint: Sprint workflow (Backlog → In Progress → Review → Done)
    - gtd: GTD workflow (Inbox → Next → Waiting → Someday → Done)
    - custom: Basic 3-column (Todo → Doing → Done)

Example:
    python3 setup_kanban_board_v2.py 13481 --template talks
"""

import sys
import os
import argparse
import requests
import json

# Configuration
VIKUNJA_API_TOKEN = "tk_b58cb267d291c55985136b9f054a62e0502e803f"
VIKUNJA_BASE_URL = "https://app.vikunja.cloud"

# Kanban Templates
TEMPLATES = {
    'talks': [
        {"title": "💡 Ideas", "position": 0, "limit": 0},
        {"title": "📝 Proposal Writing", "position": 1, "limit": 3},
        {"title": "✅ Accepted", "position": 2, "limit": 0},
        {"title": "🎯 Preparing", "position": 3, "limit": 2},
        {"title": "🎤 Delivered", "position": 4, "limit": 0},
    ],
    'sprint': [
        {"title": "📋 Backlog", "position": 0, "limit": 0},
        {"title": "🏃 In Progress", "position": 1, "limit": 3},
        {"title": "👀 Code Review", "position": 2, "limit": 2},
        {"title": "✅ Done", "position": 3, "limit": 0},
    ],
    'gtd': [
        {"title": "📥 Inbox", "position": 0, "limit": 0},
        {"title": "⏭️ Next Actions", "position": 1, "limit": 5},
        {"title": "⏸️ Waiting For", "position": 2, "limit": 0},
        {"title": "🔮 Someday/Maybe", "position": 3, "limit": 0},
        {"title": "✅ Done", "position": 4, "limit": 0},
    ],
    'custom': [
        {"title": "📝 Todo", "position": 0, "limit": 0},
        {"title": "🏃 Doing", "position": 1, "limit": 3},
        {"title": "✅ Done", "position": 2, "limit": 0},
    ],
}


def api_request(method: str, path: str, data=None):
    """Make API request to Vikunja"""
    url = f"{VIKUNJA_BASE_URL}{path}"
    headers = {
        'Authorization': f'Bearer {VIKUNJA_API_TOKEN}',
        'Content-Type': 'application/json'
    }

    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, headers=headers, json=data)
    elif method == 'PUT':
        response = requests.put(url, headers=headers, json=data)
    elif method == 'DELETE':
        response = requests.delete(url, headers=headers)
    else:
        raise ValueError(f"Unsupported method: {method}")

    if response.status_code >= 400:
        raise Exception(f"API error {response.status_code}: {response.text}")

    if method != 'DELETE':
        return response.json()
    return None


def get_or_create_kanban_view(project_id: int):
    """Get existing kanban view or create one"""
    # Get project
    project = api_request('GET', f'/api/v1/projects/{project_id}')

    # Check if kanban view exists
    views = project.get('views', [])
    kanban_view = next((v for v in views if v.get('view_kind') == 'kanban'), None)

    if kanban_view:
        print(f"✅ Found existing Kanban view: {kanban_view['title']} (ID: {kanban_view['id']})")
        return kanban_view

    # Create kanban view
    print("📋 Creating Kanban view...")
    view_data = {
        "title": "Kanban",
        "project_id": project_id,
        "view_kind": "kanban",
        "bucket_configuration_mode": "manual",
        "position": 400
    }

    kanban_view = api_request('PUT', f'/api/v1/projects/{project_id}/views', data=view_data)
    print(f"✅ Created Kanban view (ID: {kanban_view['id']})")

    return kanban_view


def setup_kanban_board(project_id: int, template: str = 'custom'):
    """
    Setup kanban board with buckets for a project.

    Args:
        project_id: Vikunja project ID
        template: Template name (talks, sprint, gtd, custom)
    """
    if template not in TEMPLATES:
        print(f"❌ Unknown template: {template}")
        print(f"Available templates: {', '.join(TEMPLATES.keys())}")
        return False

    print("=" * 80)
    print(f"SETTING UP KANBAN BOARD")
    print("=" * 80)

    try:
        # Get project details
        project = api_request('GET', f'/api/v1/projects/{project_id}')
        print(f"\nProject: {project['title']} (ID: {project_id})")
        print(f"Template: {template}")
        print()

        # Get or create kanban view
        kanban_view = get_or_create_kanban_view(project_id)
        view_id = kanban_view['id']

        # Get existing buckets
        try:
            existing_buckets = api_request('GET', f'/api/v1/projects/{project_id}/views/{view_id}/buckets')
            print(f"\nExisting buckets: {len(existing_buckets)}")
            for bucket in existing_buckets:
                print(f"  - {bucket['title']} (position {bucket['position']})")
            print()
        except Exception as e:
            existing_buckets = []
            print(f"\nNo existing buckets")
            print()

        # Create buckets from template
        buckets = TEMPLATES[template]
        created_count = 0
        skipped_count = 0

        print("Creating buckets:")
        print()

        for bucket_def in buckets:
            bucket_title = bucket_def["title"]

            # Check if bucket already exists
            existing = next((b for b in existing_buckets if b['title'] == bucket_title), None)

            if existing:
                print(f"⏭️  Skipped: {bucket_title} (already exists)")
                skipped_count += 1
            else:
                try:
                    bucket_data = {
                        "title": bucket_title,
                        "position": bucket_def["position"],
                        "limit": bucket_def["limit"]
                    }

                    bucket = api_request(
                        'PUT',
                        f'/api/v1/projects/{project_id}/views/{view_id}/buckets',
                        data=bucket_data
                    )

                    limit_str = f", WIP limit: {bucket['limit']}" if bucket['limit'] > 0 else ""
                    print(f"✅ Created: {bucket['title']} (position {bucket['position']}{limit_str})")
                    created_count += 1
                except Exception as e:
                    print(f"❌ Failed to create '{bucket_title}': {e}")

        print()
        print("=" * 80)
        print(f"SUMMARY")
        print("=" * 80)
        print(f"Buckets created: {created_count}")
        print(f"Buckets skipped: {skipped_count}")
        print()

        if created_count > 0:
            print("🎉 Kanban board setup complete!")
            print(f"\nView board: https://app.vikunja.cloud/projects/{project_id}/{view_id}")
        else:
            print("ℹ️  No new buckets created (all already exist)")

        print("=" * 80)

        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Setup Kanban board for Vikunja project (Modern API)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Templates:
  talks     Speaking pipeline (Idea → Proposal → Accepted → Prep → Done)
  sprint    Sprint workflow (Backlog → In Progress → Review → Done)
  gtd       GTD workflow (Inbox → Next → Waiting → Someday → Done)
  custom    Basic 3-column (Todo → Doing → Done)

Examples:
  python3 setup_kanban_board_v2.py 13481 --template talks
  python3 setup_kanban_board_v2.py 13456 --template sprint
        """
    )
    parser.add_argument('project_id', type=int, help='Vikunja project ID')
    parser.add_argument('--template', '-t', default='custom',
                        choices=list(TEMPLATES.keys()),
                        help='Kanban template to use (default: custom)')

    args = parser.parse_args()

    success = setup_kanban_board(args.project_id, args.template)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
