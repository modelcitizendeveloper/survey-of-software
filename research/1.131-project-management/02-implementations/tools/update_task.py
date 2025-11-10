#!/usr/bin/env python3
"""
Generic Task Update Tool

Update Vikunja tasks with properly formatted HTML descriptions.
Supports updating title, description, priority, due date, start date, and other fields.
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime

# Setup path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'vikunja-api-wrapper', 'src'))
from vikunja_wrapper import VikunjaClient

# Load environment
env_file = Path.home() / "spawn-solutions/.env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value


def parse_date(date_str):
    """Parse date string to ISO format."""
    if not date_str:
        return None

    # If already in ISO format, return as-is
    if 'T' in date_str and 'Z' in date_str:
        return date_str

    # Try to parse common formats
    try:
        # YYYY-MM-DD
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%Y-%m-%dT23:59:59Z')
    except ValueError:
        pass

    try:
        # MM/DD/YYYY
        dt = datetime.strptime(date_str, '%m/%d/%Y')
        return dt.strftime('%Y-%m-%dT23:59:59Z')
    except ValueError:
        pass

    print(f"⚠️  Could not parse date: {date_str}")
    print("   Use format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ")
    return None


def read_description_from_file(file_path):
    """Read description from file."""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Update Vikunja task fields',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:

  # Update task description (inline)
  python3 update_task.py --task-id 123 --description "<strong>New description</strong>"

  # Update description from file
  python3 update_task.py --task-id 123 --description-file task_desc.html

  # Update title and priority
  python3 update_task.py --task-id 123 --title "New title" --priority 3

  # Update due date
  python3 update_task.py --task-id 123 --due-date 2025-12-31

  # Update start date
  python3 update_task.py --task-id 123 --start-date 2025-11-11

  # Update multiple fields at once
  python3 update_task.py --task-id 123 \\
    --title "Updated title" \\
    --priority 2 \\
    --due-date 2025-12-15 \\
    --description "<strong>HTML description</strong>"

  # Preview changes without applying
  python3 update_task.py --task-id 123 --title "Test" --dry-run

HTML Formatting Tips:
  - Use <strong> for bold, <em> for italic
  - Use <ul><li>...</li></ul> for unordered lists
  - Use <ol><li>...</li></ol> for ordered lists
  - Use <code>...</code> for file paths/code
  - Use <hr> for horizontal rules
  - Use <br> for line breaks

Priority Levels:
  0 = Unset
  1 = Low
  2 = Medium
  3 = High
  4 = Urgent
  5 = DO NOW
        """
    )

    # Required
    parser.add_argument('--task-id', type=int, required=True,
                        help='Task ID to update')

    # Optional fields
    parser.add_argument('--title', type=str,
                        help='New task title')
    parser.add_argument('--description', type=str,
                        help='New task description (HTML formatted)')
    parser.add_argument('--description-file', type=str,
                        help='Read description from file')
    parser.add_argument('--priority', type=int, choices=[0, 1, 2, 3, 4, 5],
                        help='Task priority (0-5)')
    parser.add_argument('--due-date', type=str,
                        help='Due date (YYYY-MM-DD or ISO format)')
    parser.add_argument('--start-date', type=str,
                        help='Start date (YYYY-MM-DD or ISO format)')

    # Options
    parser.add_argument('--dry-run', '-d', action='store_true',
                        help='Preview changes without applying')
    parser.add_argument('--show-current', action='store_true',
                        help='Show current task details before updating')

    args = parser.parse_args()

    # Validate that at least one field is being updated
    if not any([args.title, args.description, args.description_file,
                args.priority is not None, args.due_date, args.start_date]):
        print("❌ Error: Must specify at least one field to update")
        print("   Use --title, --description, --priority, --due-date, or --start-date")
        sys.exit(1)

    # Handle description from file
    if args.description_file and args.description:
        print("❌ Error: Cannot specify both --description and --description-file")
        sys.exit(1)

    if args.description_file:
        args.description = read_description_from_file(args.description_file)

    # Initialize client
    client = VikunjaClient(
        base_url=os.environ['VIKUNJA_BASE_URL'],
        token=os.environ['VIKUNJA_API_TOKEN']
    )

    print("=" * 80)
    print("TASK UPDATE TOOL")
    print("=" * 80)
    print()

    # Get current task
    try:
        task = client.tasks.get(args.task_id)
    except Exception as e:
        print(f"❌ Failed to get task {args.task_id}: {e}")
        sys.exit(1)

    print(f"Task ID: {args.task_id}")
    print(f"Current Title: {task.title}")
    print()

    if args.show_current:
        print("=" * 80)
        print("CURRENT TASK DETAILS")
        print("=" * 80)
        print(f"Title: {task.title}")
        print(f"Priority: {task.priority}")
        print(f"Due Date: {task.due_date}")
        print(f"Start Date: {task.start_date}")
        print(f"Description:")
        print(task.description if task.description else "(empty)")
        print()
        print("=" * 80)
        print()

    # Build update payload
    updates = {}

    if args.title:
        updates['title'] = args.title
        print(f"✏️  Title: {task.title} → {args.title}")

    if args.priority is not None:
        priority_names = {0: 'Unset', 1: 'Low', 2: 'Medium', 3: 'High', 4: 'Urgent', 5: 'DO NOW'}
        old_priority = priority_names.get(task.priority, task.priority)
        new_priority = priority_names.get(args.priority, args.priority)
        updates['priority'] = args.priority
        print(f"🔢 Priority: {old_priority} → {new_priority}")

    if args.due_date:
        due_date_iso = parse_date(args.due_date)
        if due_date_iso:
            updates['due_date'] = due_date_iso
            print(f"📅 Due Date: {task.due_date} → {due_date_iso}")

    if args.start_date:
        start_date_iso = parse_date(args.start_date)
        if start_date_iso:
            updates['start_date'] = start_date_iso
            print(f"🏁 Start Date: {task.start_date} → {start_date_iso}")

    if args.description:
        updates['description'] = args.description
        desc_preview = args.description[:100] + "..." if len(args.description) > 100 else args.description
        print(f"📝 Description: Updating ({len(args.description)} chars)")
        print(f"   Preview: {desc_preview}")

    print()

    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
        print()
        print("Would update with:")
        for key, value in updates.items():
            if key == 'description':
                print(f"  {key}: ({len(value)} chars)")
            else:
                print(f"  {key}: {value}")
    else:
        print("Applying updates...")
        try:
            # Use _request() directly since tasks.update() doesn't support all fields
            client._request("POST", f"/api/v1/tasks/{args.task_id}", json=updates)
            print()
            print("✅ Task updated successfully")
            print()
            print(f"View at: https://app.vikunja.cloud/tasks/{args.task_id}")
        except Exception as e:
            print()
            print(f"❌ Failed to update task: {e}")
            sys.exit(1)

    print()
    print("=" * 80)
    print("COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
