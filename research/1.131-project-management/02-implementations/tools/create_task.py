#!/usr/bin/env python3
"""
Create Vikunja Task

Helper script to create new tasks with proper formatting.
Handles environment variables, date formatting, and API quirks.
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta

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


def parse_date(date_str, is_start=False):
    """
    Parse date string to ISO format with timezone.

    Vikunja requires: YYYY-MM-DDTHH:MM:SSZ (with Z suffix for UTC)
    """
    if not date_str:
        return None

    # If already in ISO format with timezone, return as-is
    if 'T' in date_str and ('Z' in date_str or '+' in date_str):
        return date_str

    # Special handling for relative dates
    if date_str.lower() == 'today':
        dt = datetime.now(timezone.utc)
    elif date_str.lower() == 'tomorrow':
        dt = datetime.now(timezone.utc) + timedelta(days=1)
    elif date_str.lower().startswith('next'):
        # "next sunday", "next monday", etc.
        day_name = date_str.split()[1].lower()
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        if day_name in days:
            target_day = days.index(day_name)
            today = datetime.now(timezone.utc)
            days_ahead = (target_day - today.weekday()) % 7
            if days_ahead == 0:
                days_ahead = 7
            dt = today + timedelta(days=days_ahead)
        else:
            print(f"⚠️  Unknown day: {day_name}")
            return None
    else:
        # Try to parse standard formats
        try:
            # YYYY-MM-DD
            dt = datetime.strptime(date_str, '%Y-%m-%d')
            dt = dt.replace(tzinfo=timezone.utc)
        except ValueError:
            try:
                # MM/DD/YYYY
                dt = datetime.strptime(date_str, '%m/%d/%Y')
                dt = dt.replace(tzinfo=timezone.utc)
            except ValueError:
                print(f"⚠️  Could not parse date: {date_str}")
                print("   Use: YYYY-MM-DD, MM/DD/YYYY, 'today', 'tomorrow', or 'next sunday'")
                return None

    # Set time based on whether it's start or due date
    if is_start:
        dt = dt.replace(hour=9, minute=0, second=0, microsecond=0)  # 9am UTC = 1am PST
    else:
        dt = dt.replace(hour=23, minute=59, second=0, microsecond=0)  # End of day

    return dt.isoformat()


def read_description_from_file(file_path):
    """Read description from file."""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Create new Vikunja task',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:

  # Simple task
  python3 create_task.py --project-id 13426 --title "Review weekly metrics"

  # Task with due date
  python3 create_task.py --project-id 13426 --title "Submit report" --due-date 2025-11-15

  # Recurring task (weekly)
  python3 create_task.py --project-id 13426 --title "Weekly review" \\
    --due-date "next sunday" --repeat-weekly --repeat-from-completion

  # Task with HTML description
  python3 create_task.py --project-id 13426 --title "Research CDN" \\
    --description "<strong>Goal:</strong> Compare Cloudflare vs Fastly"

  # Task from description file
  python3 create_task.py --project-id 13426 --title "FIFA prep" \\
    --description-file prep.html --priority 3

Priority Levels:
  0 = Unset (default)
  1 = Low
  2 = Medium (High in UI)
  3 = High (Urgent in UI)
  4 = Urgent (DO NOW in UI)
  5 = DO NOW (Critical in UI)

Recurrence (in seconds):
  86400 = daily
  604800 = weekly (7 days)
  2592000 = monthly (30 days)

Repeat Mode:
  0 = Repeat from due date (default)
  1 = Repeat from completion (better for habits)
        """
    )

    # Required
    parser.add_argument('--project-id', type=int, required=True,
                        help='Project ID to create task in')
    parser.add_argument('--title', type=str, required=True,
                        help='Task title')

    # Optional fields
    parser.add_argument('--description', type=str,
                        help='Task description (HTML formatted)')
    parser.add_argument('--description-file', type=str,
                        help='Read description from file')
    parser.add_argument('--priority', type=int, choices=[0, 1, 2, 3, 4, 5], default=0,
                        help='Task priority (0-5, default: 0)')
    parser.add_argument('--due-date', type=str,
                        help='Due date (YYYY-MM-DD, "today", "tomorrow", "next sunday")')
    parser.add_argument('--start-date', type=str,
                        help='Start date (same formats as due-date)')

    # Recurrence options
    parser.add_argument('--repeat-after', type=int,
                        help='Repeat interval in seconds (86400=daily, 604800=weekly)')
    parser.add_argument('--repeat-daily', action='store_true',
                        help='Shortcut for --repeat-after 86400')
    parser.add_argument('--repeat-weekly', action='store_true',
                        help='Shortcut for --repeat-after 604800')
    parser.add_argument('--repeat-from-completion', action='store_true',
                        help='Repeat from completion instead of due date')

    # Options
    parser.add_argument('--dry-run', '-d', action='store_true',
                        help='Preview task without creating')

    args = parser.parse_args()

    # Handle description from file
    if args.description_file and args.description:
        print("❌ Error: Cannot specify both --description and --description-file")
        sys.exit(1)

    if args.description_file:
        args.description = read_description_from_file(args.description_file)

    # Handle recurrence shortcuts
    if args.repeat_daily:
        args.repeat_after = 86400
    elif args.repeat_weekly:
        args.repeat_after = 604800

    # Initialize client
    client = VikunjaClient(
        base_url=os.environ.get('VIKUNJA_BASE_URL', 'https://app.vikunja.cloud'),
        token=os.environ['VIKUNJA_API_TOKEN']
    )

    print("=" * 80)
    print("CREATE NEW TASK")
    print("=" * 80)
    print()

    # Build task payload
    task_data = {
        'title': args.title,
        'project_id': args.project_id,
        'priority': args.priority,
    }

    if args.description:
        task_data['description'] = args.description

    if args.due_date:
        due_date_iso = parse_date(args.due_date, is_start=False)
        if due_date_iso:
            task_data['due_date'] = due_date_iso

    if args.start_date:
        start_date_iso = parse_date(args.start_date, is_start=True)
        if start_date_iso:
            task_data['start_date'] = start_date_iso

    if args.repeat_after:
        task_data['repeat_after'] = args.repeat_after
        task_data['repeat_mode'] = 1 if args.repeat_from_completion else 0

    # Show preview
    print(f"Title: {task_data['title']}")
    print(f"Project ID: {task_data['project_id']}")
    print(f"Priority: {task_data['priority']}")

    if 'due_date' in task_data:
        print(f"Due Date: {task_data['due_date']}")
    if 'start_date' in task_data:
        print(f"Start Date: {task_data['start_date']}")
    if 'repeat_after' in task_data:
        interval = task_data['repeat_after']
        if interval == 86400:
            interval_str = "Daily"
        elif interval == 604800:
            interval_str = "Weekly"
        elif interval == 2592000:
            interval_str = "Monthly"
        else:
            interval_str = f"{interval} seconds"
        mode = "from completion" if task_data.get('repeat_mode') == 1 else "from due date"
        print(f"Recurrence: {interval_str} ({mode})")
    if 'description' in task_data:
        desc_preview = task_data['description'][:100] + "..." if len(task_data['description']) > 100 else task_data['description']
        print(f"Description: {desc_preview}")

    print()

    if args.dry_run:
        print("🔍 DRY RUN - Task not created")
    else:
        print("Creating task...")
        try:
            # API endpoint for creating tasks: PUT /api/v1/projects/{id}/tasks
            response = client._request("PUT", f"/api/v1/projects/{args.project_id}/tasks", json=task_data)

            if response:
                print()
                print("✅ Task created successfully")
                print()
                print(f"Task ID: {response['id']}")
                print(f"URL: https://app.vikunja.cloud/tasks/{response['id']}")
        except Exception as e:
            print()
            print(f"❌ Failed to create task: {e}")
            sys.exit(1)

    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
