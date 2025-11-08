#!/usr/bin/env python3
"""
Handle Rejection (They Said No)

Handle proposal/pitch rejection with two response paths.

Pattern:
  Rejected proposal → Choose response:
  - "Maybe next time": Archive with reminder to try again
  - "Off the list": Permanent removal, don't pitch again

Usage:
    python3 handle_rejection.py <task_id> --response {retry|remove} [--retry-date DATE]

Responses:
    retry:  Maybe next time - keep for future opportunities
    remove: Off the list - don't pursue this venue/opportunity again

Example:
    python3 handle_rejection.py 216450 --response retry --retry-date 2026-11-01
    python3 handle_rejection.py 216450 --response remove --reason "Not a good fit"
"""

import sys
import os
import argparse
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'vikunja-api-wrapper', 'src'))

from vikunja_wrapper import VikunjaClient

# Configuration
VIKUNJA_API_TOKEN = "tk_b58cb267d291c55985136b9f054a62e0502e803f"
VIKUNJA_BASE_URL = "https://app.vikunja.cloud"


def handle_rejection(task_id: int, response: str, retry_date: str = None, reason: str = None, dry_run: bool = False):
    """
    Handle proposal rejection.

    Args:
        task_id: ID of rejected task
        response: 'retry' (maybe next time) or 'remove' (off the list)
        retry_date: For retry - when to pitch again (YYYY-MM-DD)
        reason: Optional reason for rejection/removal
        dry_run: If True, show plan without executing
    """

    if response not in ['retry', 'remove']:
        print(f"❌ Invalid response: {response}")
        print("Must be 'retry' or 'remove'")
        return False

    client = VikunjaClient(base_url=VIKUNJA_BASE_URL, token=VIKUNJA_API_TOKEN)

    print("=" * 80)
    print("HANDLING REJECTION")
    print("=" * 80)

    # Get the task
    try:
        task = client.tasks.get(task_id)
    except Exception as e:
        print(f"❌ Failed to get task {task_id}: {e}")
        return False

    print(f"\nRejected proposal:")
    print(f"  ID: {task.id}")
    print(f"  Title: {task.title}")
    print(f"  Project: {task.project_id}")
    print()

    # Look for linked sub-project
    import re
    subproject_id = None
    if task.description:
        match = re.search(r'https://app\.vikunja\.cloud/projects/(\d+)', task.description)
        if match:
            subproject_id = int(match.group(1))

    if subproject_id:
        try:
            subproject = client.projects.get(subproject_id)
            print(f"Linked sub-project: {subproject.title} (ID: {subproject.id})")
            print()
        except Exception as e:
            print(f"⚠️  Could not fetch sub-project {subproject_id}: {e}")
            subproject = None
    else:
        subproject = None

    # Get parent project to find buckets
    try:
        parent_project = client.projects.get(task.project_id)
        print(f"Parent project: {parent_project.title} (ID: {parent_project.id})")
    except Exception as e:
        print(f"❌ Failed to get parent project: {e}")
        return False

    # Plan the response
    print()
    print("=" * 80)
    print("RESPONSE PLAN")
    print("=" * 80)
    print()

    if response == 'retry':
        print("📅 RETRY STRATEGY - Maybe next time")
        print()
        print("Will do:")
        print("  1. Archive sub-project (preserve work done)")
        print("  2. Update main task with rejection note")
        print("  3. Move to 'Ideas' or appropriate bucket")
        if retry_date:
            print(f"  4. Create reminder task for {retry_date}")
        else:
            # Default: try again next year
            next_year = datetime.now() + timedelta(days=365)
            retry_date = next_year.strftime('%Y-%m-%d')
            print(f"  4. Create reminder task for {retry_date} (1 year)")
        print()
        print("💡 Keeps opportunity alive for future attempts")

    else:  # remove
        print("🚫 REMOVE STRATEGY - Off the list")
        print()
        print("Will do:")
        print("  1. Delete sub-project and all tasks")
        print("  2. Mark main task DONE with removal note")
        if reason:
            print(f"  3. Document reason: {reason}")
        print()
        print("⚠️  Signals not to pursue this venue/opportunity again")

    print()

    if dry_run:
        print("=" * 80)
        print("DRY RUN - No changes made")
        print("=" * 80)
        print("\nTo execute, run without --dry-run flag")
        return True

    # Execute response
    print("=" * 80)
    print("EXECUTING RESPONSE")
    print("=" * 80)
    print()

    try:
        if response == 'retry':
            # RETRY PATH - Maybe next time

            # 1. Archive sub-project (preserve work)
            if subproject:
                print("1. Archiving sub-project (preserving proposal work)...")
                client.projects.update(
                    project_id=subproject.id,
                    is_archived=True
                )
                print(f"   ✅ Archived: {subproject.title}")
                print()

            # 2. Update main task with rejection note
            print("2. Updating main task with rejection note...")

            rejection_note = f"""
{task.description or ''}

<br><br>
<strong>❌ REJECTED</strong><br>
Date: {datetime.now().strftime('%Y-%m-%d')}<br>
Response: Try again next time<br>
Next attempt: {retry_date}<br>
{"Reason: " + reason if reason else ""}
{"<br>Sub-project archived: " + subproject.title if subproject else ""}
""".strip()

            client.tasks.update(
                task_id=task.id,
                description=rejection_note
            )
            print(f"   ✅ Updated task with rejection note")
            print()

            # 3. Create reminder task
            print(f"3. Creating reminder task for {retry_date}...")

            # Parse retry date
            try:
                reminder_date = datetime.strptime(retry_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
            except ValueError:
                print(f"   ⚠️  Invalid date format: {retry_date}, skipping reminder")
                reminder_task = None
            else:
                reminder_title = f"Consider re-pitching: {task.title}"
                reminder_description = f"""
Time to consider pitching this again!

Previous attempt: {datetime.now().strftime('%Y-%m-%d')}
{"Previous rejection reason: " + reason if reason else ""}

Original task: https://app.vikunja.cloud/tasks/{task.id}
{"Previous work: https://app.vikunja.cloud/projects/" + str(subproject.id) if subproject else ""}

Review and decide:
- [ ] Review previous submission/pitch
- [ ] Check if anything changed
- [ ] Decide whether to pitch again
""".strip()

                reminder_task = client.tasks.create(
                    project_id=task.project_id,
                    title=reminder_title,
                    description=reminder_description,
                    due_date=reminder_date.isoformat(),
                    priority=3
                )
                print(f"   ✅ Created reminder: {reminder_task.title}")
                print(f"   📅 Due: {retry_date}")
                print()

            print("=" * 80)
            print("RETRY RESPONSE COMPLETE")
            print("=" * 80)
            print()
            print("✅ Actions taken:")
            print(f"   Rejection documented on: {task.title}")
            if subproject:
                print(f"   Archived sub-project: {subproject.title}")
            if reminder_task:
                print(f"   Reminder created for: {retry_date}")
            print()
            print("💡 Next steps:")
            print("   1. Move main task to 'Ideas' or appropriate bucket")
            print("   2. Wait for reminder to consider re-pitching")
            print()
            print("🔗 Links:")
            print(f"   Task: https://app.vikunja.cloud/tasks/{task.id}")
            if subproject:
                print(f"   Archived work: https://app.vikunja.cloud/projects/{subproject.id}")
            if reminder_task:
                print(f"   Reminder: https://app.vikunja.cloud/tasks/{reminder_task.id}")

        else:  # remove
            # REMOVE PATH - Off the list

            # 1. Delete sub-project
            if subproject:
                print("1. Deleting sub-project and all tasks...")
                client.projects.delete(subproject.id)
                print(f"   ✅ Deleted: {subproject.title}")
                print()

            # 2. Mark main task DONE with removal note
            print("2. Marking task as DONE with removal note...")

            removal_note = f"""
{task.description or ''}

<br><br>
<strong>🚫 REMOVED - DO NOT PURSUE</strong><br>
Date: {datetime.now().strftime('%Y-%m-%d')}<br>
Response: Off the list<br>
{"Reason: " + reason if reason else "Not a good fit"}<br>
{"Sub-project deleted: " + subproject.title if subproject else ""}

<br>
<strong>Note:</strong> This venue/opportunity has been marked as not worth pursuing again.
""".strip()

            client.tasks.update(
                task_id=task.id,
                description=removal_note,
                done=True
            )
            print(f"   ✅ Marked as DONE with removal note")
            print()

            print("=" * 80)
            print("REMOVE RESPONSE COMPLETE")
            print("=" * 80)
            print()
            print("✅ Actions taken:")
            print(f"   Task marked DONE: {task.title}")
            if subproject:
                print(f"   Deleted sub-project: {subproject.title}")
            print(f"   Reason: {reason or 'Not a good fit'}")
            print()
            print("🚫 This venue/opportunity is now marked as 'do not pursue'")
            print()
            print("🔗 Link:")
            print(f"   Task: https://app.vikunja.cloud/tasks/{task.id}")

        print()
        print("=" * 80)

        return True

    except Exception as e:
        print(f"\n❌ Response handling failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Handle proposal/pitch rejection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Two Response Paths:

1. RETRY (Maybe next time)
   - Archives sub-project (preserves work)
   - Creates reminder to try again
   - Keeps opportunity alive
   - Use when: rejection was due to timing, topic fit, or other changeable factors

2. REMOVE (Off the list)
   - Deletes sub-project
   - Marks task as DONE with "do not pursue" note
   - Removes from pipeline
   - Use when: venue isn't a good fit, won't accept your topics, or shouldn't pursue

Examples:
  # Rejected but will try again next year
  python3 handle_rejection.py 216450 --response retry --retry-date 2026-11-01

  # Rejected, not a good fit, don't pursue
  python3 handle_rejection.py 216450 --response remove --reason "Topics don't align"

  # See what will happen
  python3 handle_rejection.py 216450 --response retry --dry-run
        """
    )
    parser.add_argument('task_id', type=int, help='ID of rejected task')
    parser.add_argument('--response', '-r', required=True,
                        choices=['retry', 'remove'],
                        help='Response: retry (maybe next time) or remove (off the list)')
    parser.add_argument('--retry-date', help='For retry: when to pitch again (YYYY-MM-DD, default: +1 year)')
    parser.add_argument('--reason', help='Optional reason for rejection/removal')
    parser.add_argument('--dry-run', '-d', action='store_true',
                        help='Show plan without executing')

    args = parser.parse_args()

    # Validate retry-date if provided
    if args.response == 'retry' and args.retry_date:
        try:
            datetime.strptime(args.retry_date, '%Y-%m-%d')
        except ValueError:
            print(f"❌ Invalid date format: {args.retry_date}")
            print("Use YYYY-MM-DD format")
            sys.exit(1)

    success = handle_rejection(args.task_id, args.response, args.retry_date, args.reason, args.dry_run)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
