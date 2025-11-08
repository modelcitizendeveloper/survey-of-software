#!/usr/bin/env python3
"""
Archive Task and Sub-Project (Abandonment)

Handle the "never mind" scenario - when you decide not to pursue an idea or event.

Pattern:
  Task with sub-project → Archive both when:
  - Idea no longer relevant
  - Opportunity passed
  - Decision to not pursue
  - Cleanup needed

Usage:
    python3 archive_task.py <task_id> [--reason REASON] [--delete]

Options:
    --reason: Optional reason for abandonment
    --delete: Permanently delete instead of archive (use with caution)
    --dry-run: Show what will happen without executing

Example:
    python3 archive_task.py 216450 --reason "Event cancelled"
    python3 archive_task.py 216450 --delete --dry-run
"""

import sys
import os
import argparse
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'vikunja-api-wrapper', 'src'))

from vikunja_wrapper import VikunjaClient

# Configuration
VIKUNJA_API_TOKEN = "tk_b58cb267d291c55985136b9f054a62e0502e803f"
VIKUNJA_BASE_URL = "https://app.vikunja.cloud"


def archive_task(task_id: int, reason: str = None, delete: bool = False, dry_run: bool = False):
    """
    Archive a task and its associated sub-project.

    Args:
        task_id: ID of task to archive
        reason: Optional reason for abandonment
        delete: If True, permanently delete instead of archive
        dry_run: If True, show plan without executing
    """

    client = VikunjaClient(base_url=VIKUNJA_BASE_URL, token=VIKUNJA_API_TOKEN)

    print("=" * 80)
    print("ARCHIVING TASK" + (" (DELETE MODE)" if delete else ""))
    print("=" * 80)

    # Get the task
    try:
        task = client.tasks.get(task_id)
    except Exception as e:
        print(f"❌ Failed to get task {task_id}: {e}")
        return False

    print(f"\nTask to archive:")
    print(f"  ID: {task.id}")
    print(f"  Title: {task.title}")
    print(f"  Project: {task.project_id}")
    print(f"  Description: {task.description[:100] if task.description else '(none)'}...")
    print()

    # Look for linked sub-project in description
    # Pattern: https://app.vikunja.cloud/projects/{project_id}
    import re
    subproject_id = None
    if task.description:
        match = re.search(r'https://app\.vikunja\.cloud/projects/(\d+)', task.description)
        if match:
            subproject_id = int(match.group(1))

    if subproject_id:
        try:
            subproject = client.projects.get(subproject_id)
            print(f"Found linked sub-project:")
            print(f"  ID: {subproject.id}")
            print(f"  Title: {subproject.title}")
            print(f"  Tasks: (will be counted)")
            print()

            # Get tasks in sub-project
            subproject_tasks = client.tasks.list(project_id=subproject_id)
            print(f"  Sub-project contains {len(subproject_tasks)} tasks")
            print()
        except Exception as e:
            print(f"⚠️  Could not fetch sub-project {subproject_id}: {e}")
            subproject = None
            subproject_tasks = []
    else:
        print("ℹ️  No linked sub-project found")
        print()
        subproject = None
        subproject_tasks = []

    # Plan the archival
    print("=" * 80)
    print("ARCHIVAL PLAN")
    print("=" * 80)
    print()

    if delete:
        print("⚠️  DELETE MODE - This is permanent!")
        print()
        print("Will permanently delete:")
        print(f"  - Main task: {task.title}")
        if subproject:
            print(f"  - Sub-project: {subproject.title}")
            print(f"  - {len(subproject_tasks)} sub-project tasks")
        print()
        print("⚠️  This cannot be undone!")
    else:
        print("Will mark as done and add archival note:")
        print(f"  - Main task: {task.title} → DONE ✅")
        if subproject:
            print(f"  - Sub-project: {subproject.title} → Archive")
        if reason:
            print(f"  - Reason: {reason}")
        print()

    if dry_run:
        print("=" * 80)
        print("DRY RUN - No changes made")
        print("=" * 80)
        print("\nTo execute, run without --dry-run flag")
        return True

    # Execute archival
    print("=" * 80)
    print("EXECUTING ARCHIVAL")
    print("=" * 80)
    print()

    try:
        if delete:
            # DELETE MODE - Permanent removal

            # 1. Delete sub-project (this also deletes all tasks within)
            if subproject:
                print(f"1. Deleting sub-project and its {len(subproject_tasks)} tasks...")
                client.projects.delete(subproject.id)
                print(f"   ✅ Deleted sub-project: {subproject.title}")
                print()

            # 2. Delete main task
            print("2. Deleting main task...")
            client.tasks.delete(task.id)
            print(f"   ✅ Deleted task: {task.title}")
            print()

            print("=" * 80)
            print("DELETION COMPLETE")
            print("=" * 80)
            print()
            print("✅ Permanently deleted:")
            print(f"   Main task: {task.title}")
            if subproject:
                print(f"   Sub-project: {subproject.title}")
                print(f"   Tasks: {len(subproject_tasks)}")
            print()

        else:
            # ARCHIVE MODE - Mark done with notes

            # 1. Archive sub-project if exists
            if subproject:
                print("1. Archiving sub-project...")
                client.projects.update(
                    project_id=subproject.id,
                    is_archived=True
                )
                print(f"   ✅ Archived: {subproject.title}")
                print()

            # 2. Update main task with archival note
            print("2. Updating main task...")

            archive_note = f"""
{task.description or ''}

<br><br>
<strong>🗃️ ARCHIVED</strong><br>
Date: {datetime.now().strftime('%Y-%m-%d')}<br>
Reason: {reason or 'Not pursuing'}<br>
{"Sub-project archived: " + subproject.title if subproject else "No sub-project"}
""".strip()

            client.tasks.update(
                task_id=task.id,
                description=archive_note,
                done=True
            )
            print(f"   ✅ Marked as DONE with archival note")
            print()

            print("=" * 80)
            print("ARCHIVAL COMPLETE")
            print("=" * 80)
            print()
            print("✅ Archived:")
            print(f"   Main task: {task.title} (marked DONE)")
            if subproject:
                print(f"   Sub-project: {subproject.title} (archived)")
            if reason:
                print(f"   Reason: {reason}")
            print()
            print("🔗 Links:")
            print(f"   Task: https://app.vikunja.cloud/tasks/{task.id}")
            if subproject:
                print(f"   Sub-project: https://app.vikunja.cloud/projects/{subproject.id}")
            print()

        print("=" * 80)

        return True

    except Exception as e:
        print(f"\n❌ Archival failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Archive task and sub-project (abandonment)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Pattern:
  When you decide "never mind" on an idea or event:
  1. Task marked DONE with archival note (or deleted)
  2. Sub-project archived (or deleted)
  3. Pipeline cleared

Use Cases:
  - Event cancelled by organizer
  - No longer interested in topic
  - Opportunity passed
  - Priorities changed
  - Cleanup needed

Examples:
  # Archive with reason (recommended)
  python3 archive_task.py 216450 --reason "Event cancelled"

  # See what will happen
  python3 archive_task.py 216450 --dry-run

  # Permanent deletion (use with caution)
  python3 archive_task.py 216450 --delete --reason "Duplicate entry"
        """
    )
    parser.add_argument('task_id', type=int, help='ID of task to archive')
    parser.add_argument('--reason', '-r', help='Reason for archival')
    parser.add_argument('--delete', action='store_true',
                        help='Permanently delete instead of archive (CAUTION)')
    parser.add_argument('--dry-run', '-d', action='store_true',
                        help='Show plan without executing')

    args = parser.parse_args()

    # Confirm deletion if requested
    if args.delete and not args.dry_run:
        print("\n⚠️  WARNING: You are about to PERMANENTLY DELETE this task and sub-project!")
        print("This action cannot be undone.\n")
        confirm = input("Type 'DELETE' to confirm: ")
        if confirm != "DELETE":
            print("❌ Deletion cancelled")
            sys.exit(1)

    success = archive_task(args.task_id, args.reason, args.delete, args.dry_run)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
