#!/usr/bin/env python3
"""
Vikunja Upcoming Digest - Show tasks starting or due soon

Filters by start_date and due_date (addresses Vikunja UI limitation that only shows due_date)

Usage:
    # Tasks starting or due in next 7 days
    python upcoming_digest.py --days 7

    # Next 14 days with descriptions
    python upcoming_digest.py --days 14 --show-description

    # Just today
    python upcoming_digest.py --days 0
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime, timedelta, timezone
from collections import defaultdict

# Setup path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'vikunja-api-wrapper', 'src'))
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


def parse_vikunja_date(date_obj):
    """Parse Vikunja date object to datetime."""
    if not date_obj:
        return None

    # If already a datetime object
    if isinstance(date_obj, datetime):
        # Check for zero date (0001-01-01) which means "not set"
        if date_obj.year == 1:
            return None
        return date_obj

    # If string, parse it
    if isinstance(date_obj, str):
        try:
            dt = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
            # Check for zero date
            if dt.year == 1:
                return None
            return dt
        except:
            return None

    return None


def get_project_hierarchy(client, project_id, all_projects):
    """Get full project hierarchy path."""
    hierarchy = []
    current_id = project_id

    # Build project lookup
    project_lookup = {p.id: p for p in all_projects}

    # Walk up the hierarchy
    max_depth = 10  # Prevent infinite loops
    depth = 0
    while current_id and current_id != 0 and depth < max_depth:
        project = project_lookup.get(current_id)
        if not project:
            break
        hierarchy.insert(0, project.title)
        current_id = project.parent_project_id
        depth += 1

    return " > ".join(hierarchy) if hierarchy else "Unknown"


def format_date(date_obj):
    """Format date for display."""
    if not date_obj:
        return "None"

    dt = parse_vikunja_date(date_obj)
    if not dt:
        return "None"

    # Format as "Nov 11" or "Nov 11, 2026" if not current year
    now = datetime.now(timezone.utc)
    date_str = dt.strftime("%b %d")

    if dt.year != now.year:
        date_str += f", {dt.year}"

    return date_str


def get_task_attr(task, attr, default=None):
    """Get attribute from task (dict or object)."""
    if isinstance(task, dict):
        return task.get(attr, default)
    else:
        return getattr(task, attr, default)


def format_priority(priority):
    """Format priority for display."""
    priority_map = {
        0: "·",  # Unset
        1: "Low",
        2: "Med",
        3: "High",
        4: "Urgent",
        5: "DO NOW"
    }
    return priority_map.get(priority, str(priority))


def get_labels_string(task):
    """Get labels as comma-separated string."""
    labels = task.get('labels', []) if isinstance(task, dict) else getattr(task, 'labels', [])
    if not labels:
        return ""
    # Labels can be dicts or strings
    label_names = []
    for label in labels:
        if isinstance(label, dict):
            label_names.append(label.get('title', str(label)))
        else:
            label_names.append(str(label))
    return ", ".join(label_names)


def is_upcoming(task, days_ahead):
    """Check if task is starting or due within days_ahead."""
    now = datetime.now(timezone.utc)
    cutoff = now + timedelta(days=days_ahead + 1)  # +1 to include the last day

    # Get start_date and due_date from dict or object
    if isinstance(task, dict):
        start_date_raw = task.get('start_date')
        due_date_raw = task.get('due_date')
    else:
        start_date_raw = getattr(task, 'start_date', None)
        due_date_raw = getattr(task, 'due_date', None)

    # Check start_date
    start_date = parse_vikunja_date(start_date_raw)
    if start_date and now <= start_date <= cutoff:
        return True, 'starting', start_date

    # Check due_date
    due_date = parse_vikunja_date(due_date_raw)
    if due_date and now <= due_date <= cutoff:
        return True, 'due', due_date

    return False, None, None


def is_overdue(task):
    """Check if task is overdue."""
    if isinstance(task, dict):
        due_date_raw = task.get('due_date')
    else:
        due_date_raw = getattr(task, 'due_date', None)

    if not due_date_raw:
        return False

    due_date = parse_vikunja_date(due_date_raw)
    if not due_date:
        return False

    now = datetime.now(timezone.utc)
    return due_date < now


def main():
    parser = argparse.ArgumentParser(
        description='Show tasks starting or due soon',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Next 7 days
  python upcoming_digest.py --days 7

  # Next 14 days with descriptions
  python upcoming_digest.py --days 14 --show-description

  # Just today
  python upcoming_digest.py --days 0

  # Include high priority tasks regardless of dates
  python upcoming_digest.py --days 7 --include-priority
        """
    )

    parser.add_argument('--days', type=int, default=7,
                        help='Days ahead to look (default: 7)')
    parser.add_argument('--show-description', action='store_true',
                        help='Include task descriptions')
    parser.add_argument('--include-priority', action='store_true',
                        help='Include high priority (4-5) tasks regardless of dates')
    parser.add_argument('--include-done', action='store_true',
                        help='Include completed tasks (default: exclude)')

    args = parser.parse_args()

    # Initialize client
    client = VikunjaClient(
        base_url=os.environ['VIKUNJA_BASE_URL'],
        token=os.environ['VIKUNJA_API_TOKEN']
    )

    print("=" * 80)
    print(f"UPCOMING DIGEST - Next {args.days} Day{'s' if args.days != 1 else ''}")
    print("=" * 80)
    print()

    # Get all projects for hierarchy lookup
    all_projects = client.projects.list()

    # Get all tasks via direct API (to get start_date field)
    all_tasks = []
    for project in all_projects:
        try:
            # Use direct API to get all fields including start_date
            response = client._request("GET", f"/api/v1/projects/{project.id}/tasks")
            if response:
                all_tasks.extend(response)
        except Exception as e:
            print(f"Warning: Failed to get tasks for project {project.id}: {e}", file=sys.stderr)

    print(f"Scanning {len(all_tasks)} tasks...")
    print()

    # Categorize tasks
    starting_tasks = []
    due_tasks = []
    overdue_tasks = []
    priority_tasks = []

    for task in all_tasks:
        # Skip done tasks unless requested
        done = get_task_attr(task, 'done', False)
        if done and not args.include_done:
            continue

        # Check if overdue
        if is_overdue(task):
            overdue_tasks.append(task)
            continue

        # Check if upcoming
        is_upcoming_task, reason, date = is_upcoming(task, args.days)
        if is_upcoming_task:
            if reason == 'starting':
                starting_tasks.append((task, date))
            elif reason == 'due':
                due_tasks.append((task, date))

        # Check priority
        priority = get_task_attr(task, 'priority', 0)
        if args.include_priority and priority >= 4:
            priority_tasks.append(task)

    # Sort by date
    starting_tasks.sort(key=lambda x: x[1])
    due_tasks.sort(key=lambda x: x[1])
    overdue_tasks.sort(key=lambda x: parse_vikunja_date(get_task_attr(x, 'due_date')))
    priority_tasks.sort(key=lambda x: get_task_attr(x, 'priority', 0), reverse=True)

    # Display results
    total_shown = 0

    # Overdue
    if overdue_tasks:
        print("🔴 OVERDUE")
        print("-" * 80)
        for task in overdue_tasks:
            project_id = get_task_attr(task, 'project_id')
            project_path = get_project_hierarchy(client, project_id, all_projects)
            priority = format_priority(get_task_attr(task, 'priority', 0))
            due = format_date(get_task_attr(task, 'due_date'))
            labels = get_labels_string(task)
            title = get_task_attr(task, 'title', 'Untitled')
            task_id = get_task_attr(task, 'id')
            description = get_task_attr(task, 'description')

            print(f"[{priority}] {title}")
            print(f"    Project: {project_path}")
            print(f"    Due: {due}")
            if labels:
                print(f"    Labels: {labels}")
            print(f"    URL: https://app.vikunja.cloud/tasks/{task_id}")

            if args.show_description and description:
                print(f"    Description: {description[:200]}...")

            print()
            total_shown += 1
        print()

    # Starting Soon
    if starting_tasks:
        print("🟢 STARTING SOON")
        print("-" * 80)
        for task, start_date in starting_tasks:
            project_path = get_project_hierarchy(client, get_task_attr(task, "project_id"), all_projects)
            priority = format_priority(get_task_attr(task, "priority", 0))
            start = format_date(start_date)
            due = format_date(get_task_attr(task, "due_date"))
            labels = get_labels_string(task)

            print(f"[{priority}] {get_task_attr(task, "title", "Untitled")}")
            print(f"    Project: {project_path}")
            print(f"    Start: {start} | Due: {due}")
            if labels:
                print(f"    Labels: {labels}")
            print(f"    URL: https://app.vikunja.cloud/tasks/{get_task_attr(task, "id")}")

            if args.show_description and get_task_attr(task, "description"):
                print(f"    Description: {get_task_attr(task, "description")[:200]}...")

            print()
            total_shown += 1
        print()

    # Due Soon
    if due_tasks:
        print("🟡 DUE SOON")
        print("-" * 80)
        for task, due_date in due_tasks:
            project_path = get_project_hierarchy(client, get_task_attr(task, "project_id"), all_projects)
            priority = format_priority(get_task_attr(task, "priority", 0))
            due = format_date(due_date)
            labels = get_labels_string(task)

            print(f"[{priority}] {get_task_attr(task, "title", "Untitled")}")
            print(f"    Project: {project_path}")
            print(f"    Due: {due}")
            if labels:
                print(f"    Labels: {labels}")
            print(f"    URL: https://app.vikunja.cloud/tasks/{get_task_attr(task, "id")}")

            if args.show_description and get_task_attr(task, "description"):
                print(f"    Description: {get_task_attr(task, "description")[:200]}...")

            print()
            total_shown += 1
        print()

    # High Priority (if requested)
    if args.include_priority and priority_tasks:
        print("⚡ HIGH PRIORITY")
        print("-" * 80)
        for task in priority_tasks:
            # Skip if already shown in other categories
            if task in overdue_tasks or task in [t for t, _ in starting_tasks] or task in [t for t, _ in due_tasks]:
                continue

            project_path = get_project_hierarchy(client, get_task_attr(task, "project_id"), all_projects)
            priority = format_priority(get_task_attr(task, "priority", 0))
            start = format_date(get_task_attr(task, "start_date")) if hasattr(task, 'start_date') else "None"
            due = format_date(get_task_attr(task, "due_date"))
            labels = get_labels_string(task)

            print(f"[{priority}] {get_task_attr(task, "title", "Untitled")}")
            print(f"    Project: {project_path}")
            print(f"    Start: {start} | Due: {due}")
            if labels:
                print(f"    Labels: {labels}")
            print(f"    URL: https://app.vikunja.cloud/tasks/{get_task_attr(task, "id")}")

            if args.show_description and get_task_attr(task, "description"):
                print(f"    Description: {get_task_attr(task, "description")[:200]}...")

            print()
            total_shown += 1
        print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Overdue: {len(overdue_tasks)}")
    print(f"Starting soon: {len(starting_tasks)}")
    print(f"Due soon: {len(due_tasks)}")
    if args.include_priority:
        print(f"High priority: {len([t for t in priority_tasks if t not in overdue_tasks and t not in [x for x, _ in starting_tasks] and t not in [x for x, _ in due_tasks]])}")
    print(f"Total shown: {total_shown}")
    print()

    if total_shown == 0:
        print("✨ Nothing upcoming - you're all clear!")
        print()


if __name__ == "__main__":
    main()
