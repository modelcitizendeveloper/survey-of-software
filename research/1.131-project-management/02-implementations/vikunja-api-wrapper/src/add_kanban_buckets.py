#!/usr/bin/env python3
"""
Add Kanban buckets to an existing Vikunja project.

This script finds the Kanban view for a project and creates standard workflow buckets.
Useful for setting up projects that were created without buckets.

Usage:
    python add_kanban_buckets.py <project_id> [--buckets-file buckets.yaml]

Environment variables (from .env):
    VIKUNJA_BASE_URL - Vikunja instance URL (default: https://app.vikunja.cloud)
    VIKUNJA_API_TOKEN - API authentication token (required)

Example:
    # Add default buckets to project 13792
    python add_kanban_buckets.py 13792

    # Add custom buckets from YAML file
    python add_kanban_buckets.py 13792 --buckets-file custom-buckets.yaml
"""

import argparse
import os
import sys
from typing import List, Dict, Any
import yaml
from dotenv import load_dotenv
from vikunja_wrapper import VikunjaClient


# Default bucket configurations for common workflows
DEFAULT_BUCKETS = {
    "payables": [
        {"title": "Decision Queue", "position": 1, "limit": 0},
        {"title": "Approved - Timing Payment", "position": 2, "limit": 0},
        {"title": "Paid", "position": 3, "limit": 0},
    ],
    "standard": [
        {"title": "Backlog", "position": 1, "limit": 0},
        {"title": "To Do", "position": 2, "limit": 5},
        {"title": "In Progress", "position": 3, "limit": 3},
        {"title": "Done", "position": 4, "limit": 0},
    ],
}


def load_buckets_config(file_path: str = None, preset: str = None) -> List[Dict[str, Any]]:
    """
    Load bucket configuration from file or preset.

    Args:
        file_path: Path to YAML file with bucket configurations
        preset: Name of preset configuration ("payables", "standard")

    Returns:
        List of bucket configurations
    """
    if file_path:
        with open(file_path, 'r') as f:
            config = yaml.safe_load(f)
            return config.get("buckets", [])

    if preset and preset in DEFAULT_BUCKETS:
        return DEFAULT_BUCKETS[preset]

    return DEFAULT_BUCKETS["standard"]


def add_buckets_to_project(
    client: VikunjaClient,
    project_id: int,
    buckets_config: List[Dict[str, Any]],
    skip_existing: bool = True
) -> List:
    """
    Add buckets to a project's Kanban view.

    Args:
        client: VikunjaClient instance
        project_id: ID of the project
        buckets_config: List of bucket configurations
        skip_existing: If True, skip buckets that already exist (default: True)

    Returns:
        List of created bucket objects
    """
    # Get the Kanban view for this project
    print(f"Looking up Kanban view for project {project_id}...")
    try:
        kanban_view = client.views.get_kanban_view(project_id)
        print(f"Found Kanban view (ID: {kanban_view.id})")
    except Exception as e:
        print(f"Error: Could not find Kanban view for project {project_id}")
        print(f"Details: {e}")
        sys.exit(1)

    # Get existing buckets if skip_existing is True
    existing_buckets = []
    if skip_existing:
        try:
            existing_buckets = client.buckets.list(project_id, kanban_view.id)
            existing_titles = {b.title for b in existing_buckets}
            print(f"Found {len(existing_buckets)} existing buckets: {existing_titles}")
        except Exception as e:
            print(f"Warning: Could not list existing buckets: {e}")
            existing_titles = set()
    else:
        existing_titles = set()

    # Create buckets
    created_buckets = []
    for config in buckets_config:
        title = config["title"]

        # Skip if bucket already exists
        if skip_existing and title in existing_titles:
            print(f"  Skipping '{title}' (already exists)")
            continue

        try:
            print(f"  Creating bucket '{title}'...")
            bucket = client.buckets.create(
                project_id=project_id,
                view_id=kanban_view.id,
                title=title,
                position=config.get("position", 0),
                limit=config.get("limit", 0)
            )
            created_buckets.append(bucket)
            print(f"    ✓ Created (ID: {bucket.id}, Position: {bucket.position}, Limit: {bucket.limit})")
        except Exception as e:
            print(f"    ✗ Error creating bucket '{title}': {e}")

    return created_buckets


def main():
    parser = argparse.ArgumentParser(
        description="Add Kanban buckets to an existing Vikunja project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add default standard buckets (Backlog, To Do, In Progress, Done)
  %(prog)s 13792

  # Add payables workflow buckets (Decision Queue, Approved - Timing Payment, Paid)
  %(prog)s 13792 --preset payables

  # Add custom buckets from YAML file
  %(prog)s 13792 --buckets-file custom-buckets.yaml

  # Force recreate all buckets (even if they exist)
  %(prog)s 13792 --no-skip-existing

Presets:
  standard - Backlog, To Do, In Progress, Done (default)
  payables - Decision Queue, Approved - Timing Payment, Paid
        """
    )
    parser.add_argument("project_id", type=int, help="ID of the project")
    parser.add_argument(
        "--buckets-file",
        help="Path to YAML file with bucket configurations"
    )
    parser.add_argument(
        "--preset",
        choices=["standard", "payables"],
        default="standard",
        help="Use a preset bucket configuration (default: standard)"
    )
    parser.add_argument(
        "--no-skip-existing",
        action="store_true",
        help="Create buckets even if they already exist (may cause duplicates)"
    )

    args = parser.parse_args()

    # Load environment variables
    load_dotenv()

    base_url = os.getenv("VIKUNJA_BASE_URL", "https://app.vikunja.cloud")
    token = os.getenv("VIKUNJA_API_TOKEN")

    if not token:
        print("Error: VIKUNJA_API_TOKEN environment variable not set")
        print("Please set it in your .env file or environment")
        sys.exit(1)

    # Create client
    print(f"Connecting to Vikunja at {base_url}...")
    client = VikunjaClient(base_url=base_url, token=token)

    # Verify project exists
    try:
        project = client.projects.get(args.project_id)
        print(f"Project found: '{project.title}' (ID: {project.id})")
    except Exception as e:
        print(f"Error: Could not find project {args.project_id}")
        print(f"Details: {e}")
        sys.exit(1)

    # Load bucket configuration
    buckets_config = load_buckets_config(args.buckets_file, args.preset)
    print(f"\nWill create {len(buckets_config)} buckets:")
    for config in buckets_config:
        print(f"  - {config['title']} (position: {config.get('position', 0)}, limit: {config.get('limit', 0)})")

    # Add buckets
    print("\nCreating buckets...")
    created = add_buckets_to_project(
        client,
        args.project_id,
        buckets_config,
        skip_existing=not args.no_skip_existing
    )

    print(f"\n✓ Done! Created {len(created)} buckets for project '{project.title}'")


if __name__ == "__main__":
    main()
