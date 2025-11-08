#!/usr/bin/env python3
"""
Setup Kanban Board for Vikunja Project

Creates standard kanban buckets for a project.

Usage:
    python3 setup_kanban_board.py <project_id> [--template TEMPLATE]

Templates:
    - talks: Speaking pipeline (Idea → Proposal → Accepted → Prep → Done)
    - sprint: Sprint workflow (Backlog → In Progress → Review → Done)
    - gtd: GTD workflow (Inbox → Next → Waiting → Someday → Done)
    - custom: Basic 3-column (Todo → Doing → Done)

Example:
    python3 setup_kanban_board.py 13481 --template talks
"""

import sys
import os
import argparse

# Add wrapper to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'vikunja-api-wrapper', 'src'))

from vikunja_wrapper import VikunjaClient

# Configuration
VIKUNJA_API_TOKEN = "tk_b58cb267d291c55985136b9f054a62e0502e803f"
VIKUNJA_BASE_URL = "https://app.vikunja.cloud"

# Kanban Templates
TEMPLATES = {
    'talks': [
        {"name": "💡 Ideas", "position": 0, "limit": 0},
        {"name": "📝 Proposal Writing", "position": 1, "limit": 3},
        {"name": "✅ Accepted", "position": 2, "limit": 0},
        {"name": "🎯 Preparing", "position": 3, "limit": 2},
        {"name": "🎤 Delivered", "position": 4, "limit": 0},
    ],
    'sprint': [
        {"name": "📋 Backlog", "position": 0, "limit": 0},
        {"name": "🏃 In Progress", "position": 1, "limit": 3},
        {"name": "👀 Code Review", "position": 2, "limit": 2},
        {"name": "✅ Done", "position": 3, "limit": 0},
    ],
    'gtd': [
        {"name": "📥 Inbox", "position": 0, "limit": 0},
        {"name": "⏭️ Next Actions", "position": 1, "limit": 5},
        {"name": "⏸️ Waiting For", "position": 2, "limit": 0},
        {"name": "🔮 Someday/Maybe", "position": 3, "limit": 0},
        {"name": "✅ Done", "position": 4, "limit": 0},
    ],
    'custom': [
        {"name": "📝 Todo", "position": 0, "limit": 0},
        {"name": "🏃 Doing", "position": 1, "limit": 3},
        {"name": "✅ Done", "position": 2, "limit": 0},
    ],
}


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

    client = VikunjaClient(base_url=VIKUNJA_BASE_URL, token=VIKUNJA_API_TOKEN)

    # Get project details
    try:
        project = client.projects.get(project_id)
    except Exception as e:
        print(f"❌ Failed to get project {project_id}: {e}")
        return False

    print("=" * 80)
    print(f"SETTING UP KANBAN BOARD")
    print("=" * 80)
    print(f"\nProject: {project.title} (ID: {project_id})")
    print(f"Template: {template}")
    print()

    # Get existing buckets
    try:
        existing_buckets = client.buckets.list(project_id=project_id)
        print(f"Existing buckets: {len(existing_buckets)}")
        for bucket in existing_buckets:
            print(f"  - {bucket.title} (position {bucket.position})")
        print()
    except Exception as e:
        existing_buckets = []

    # Create buckets from template
    buckets = TEMPLATES[template]
    created_count = 0
    skipped_count = 0

    print("Creating buckets:")
    print()

    for bucket_def in buckets:
        bucket_name = bucket_def["name"]

        # Check if bucket already exists
        existing = next((b for b in existing_buckets if b.title == bucket_name), None)

        if existing:
            print(f"⏭️  Skipped: {bucket_name} (already exists)")
            skipped_count += 1
        else:
            try:
                bucket = client.buckets.create(
                    project_id=project_id,
                    title=bucket_name,
                    position=bucket_def["position"],
                    limit=bucket_def["limit"]
                )
                limit_str = f", WIP limit: {bucket.limit}" if bucket.limit > 0 else ""
                print(f"✅ Created: {bucket.title} (position {bucket.position}{limit_str})")
                created_count += 1
            except Exception as e:
                print(f"❌ Failed to create '{bucket_name}': {e}")

    print()
    print("=" * 80)
    print(f"SUMMARY")
    print("=" * 80)
    print(f"Buckets created: {created_count}")
    print(f"Buckets skipped: {skipped_count}")
    print()

    if created_count > 0:
        print("🎉 Kanban board setup complete!")
        print(f"\nView project: https://app.vikunja.cloud/projects/{project_id}")
    else:
        print("ℹ️  No new buckets created (all already exist)")

    print("=" * 80)

    return True


def main():
    parser = argparse.ArgumentParser(
        description='Setup Kanban board for Vikunja project',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Templates:
  talks     Speaking pipeline (Idea → Proposal → Accepted → Prep → Done)
  sprint    Sprint workflow (Backlog → In Progress → Review → Done)
  gtd       GTD workflow (Inbox → Next → Waiting → Someday → Done)
  custom    Basic 3-column (Todo → Doing → Done)

Examples:
  python3 setup_kanban_board.py 13481 --template talks
  python3 setup_kanban_board.py 13456 --template sprint
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
