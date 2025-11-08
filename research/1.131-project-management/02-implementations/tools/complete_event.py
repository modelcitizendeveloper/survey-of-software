#!/usr/bin/env python3
"""
Complete Event (Successfully Delivered)

Handle successful event completion with follow-up tasks and next-year reminder.

Pattern:
  Event delivered → Create closure tasks:
  - Collect feedback
  - Capture notes
  - Process learnings
  - Set reminder for next year

Usage:
    python3 complete_event.py <task_id> [--next-year-date DATE] [--notes TEXT]

Options:
    --next-year-date: When to pitch again (default: +1 year from today)
    --notes: Initial completion notes
    --skip-followup: Don't create follow-up tasks
    --skip-reminder: Don't create next-year reminder

Example:
    python3 complete_event.py 216450 --notes "Great audience, lots of questions"
    python3 complete_event.py 216450 --next-year-date 2026-11-01
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

# Follow-up tasks template
FOLLOWUP_TASKS = [
    {
        "title": "Collect feedback and reviews",
        "description": """
Gather feedback from the event:

- [ ] Check event platform for ratings/reviews
- [ ] Review comments on social media
- [ ] Collect direct feedback from attendees
- [ ] Note organizer feedback
- [ ] Save screenshots/evidence

Document everything in the completion notes task.
        """.strip(),
        "priority": 5
    },
    {
        "title": "Capture completion notes",
        "description": """
Document the event experience:

What went well:
-

What could be improved:
-

Key takeaways:
-

Interesting questions/interactions:
-

Would do this event again? (Yes/No/Maybe)

Rating (1-5):
        """.strip(),
        "priority": 5
    },
    {
        "title": "Process learnings for next time",
        "description": """
Extract lessons learned:

- [ ] Update talk/demo materials based on feedback
- [ ] Identify topics that resonated
- [ ] Note timing adjustments needed
- [ ] Update proposal template with learnings
- [ ] Archive final materials to reference folder

Add insights to the completion notes task.
        """.strip(),
        "priority": 3
    },
    {
        "title": "Share materials and follow-up",
        "description": """
Post-event sharing:

- [ ] Upload slides to sharing platform
- [ ] Publish demo code/examples
- [ ] Share recording (if available)
- [ ] Post thank-you on social media
- [ ] Connect with interesting contacts
- [ ] Send follow-up emails if promised

Update main project with links to published materials.
        """.strip(),
        "priority": 2
    }
]


def complete_event(task_id: int, next_year_date: str = None, notes: str = None,
                   skip_followup: bool = False, skip_reminder: bool = False, dry_run: bool = False):
    """
    Complete an event and create follow-up tasks.

    Args:
        task_id: ID of completed event task
        next_year_date: When to pitch again (YYYY-MM-DD)
        notes: Initial completion notes
        skip_followup: Don't create follow-up tasks
        skip_reminder: Don't create next-year reminder
        dry_run: If True, show plan without executing
    """

    client = VikunjaClient(base_url=VIKUNJA_BASE_URL, token=VIKUNJA_API_TOKEN)

    print("=" * 80)
    print("COMPLETING EVENT")
    print("=" * 80)

    # Get the task
    try:
        task = client.tasks.get(task_id)
    except Exception as e:
        print(f"❌ Failed to get task {task_id}: {e}")
        return False

    print(f"\nCompleted event:")
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
        print("ℹ️  No linked sub-project found")
        print()
        subproject = None

    # Get parent project
    try:
        parent_project = client.projects.get(task.project_id)
        print(f"Parent project: {parent_project.title} (ID: {parent_project.id})")
    except Exception as e:
        print(f"❌ Failed to get parent project: {e}")
        return False

    # Calculate next year date
    if not next_year_date:
        next_year = datetime.now() + timedelta(days=365)
        next_year_date = next_year.strftime('%Y-%m-%d')

    # Plan the completion
    print()
    print("=" * 80)
    print("COMPLETION PLAN")
    print("=" * 80)
    print()

    print("Will do:")
    print("  1. Mark main task as DONE ✅")

    if not skip_followup and subproject:
        print(f"  2. Create {len(FOLLOWUP_TASKS)} follow-up tasks in sub-project:")
        for i, ft in enumerate(FOLLOWUP_TASKS, 1):
            print(f"     {i}. {ft['title']}")

    if not skip_reminder:
        print(f"  3. Create reminder to pitch again on {next_year_date}")

    if notes:
        print(f"  4. Add initial notes to completion")

    if subproject:
        print(f"  5. Keep sub-project active for follow-up work")
        print(f"     (Archive manually after all follow-up complete)")

    print()

    if dry_run:
        print("=" * 80)
        print("DRY RUN - No changes made")
        print("=" * 80)
        print("\nTo execute, run without --dry-run flag")
        return True

    # Execute completion
    print("=" * 80)
    print("EXECUTING COMPLETION")
    print("=" * 80)
    print()

    try:
        # 1. Update main task with completion note
        print("1. Marking main task as DONE...")

        completion_note = f"""
{task.description or ''}

<br><br>
<strong>✅ COMPLETED</strong><br>
Date: {datetime.now().strftime('%Y-%m-%d')}<br>
{"Initial notes: " + notes if notes else ""}
{f"<br>Sub-project: https://app.vikunja.cloud/projects/{subproject.id} (follow-up tasks added)" if subproject and not skip_followup else ""}

<br><br>
<em>Remember to complete follow-up tasks and archive sub-project when done!</em>
""".strip()

        client.tasks.update(
            task_id=task.id,
            description=completion_note,
            done=True
        )
        print(f"   ✅ Marked as DONE: {task.title}")
        print()

        # 2. Create follow-up tasks in sub-project
        created_followup = []
        if not skip_followup and subproject:
            print(f"2. Creating {len(FOLLOWUP_TASKS)} follow-up tasks in sub-project...")

            for ft in FOLLOWUP_TASKS:
                try:
                    followup_task = client.tasks.create(
                        project_id=subproject.id,
                        title=ft['title'],
                        description=ft['description'],
                        priority=ft['priority']
                    )
                    print(f"   ✅ {followup_task.title}")
                    created_followup.append(followup_task)
                except Exception as e:
                    print(f"   ⚠️  Failed to create '{ft['title']}': {e}")

            print()

        # 3. Create next-year reminder
        reminder_task = None
        if not skip_reminder:
            step_num = 3 if (skip_followup or not subproject) else 3
            print(f"{step_num}. Creating reminder for next year...")

            try:
                reminder_date = datetime.strptime(next_year_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
            except ValueError:
                print(f"   ⚠️  Invalid date format: {next_year_date}, skipping reminder")
            else:
                # Extract event name from title (remove year if present)
                event_name = re.sub(r'\d{4}', '', task.title).strip()
                event_name = re.sub(r'\s+', ' ', event_name)  # Clean up spaces

                reminder_title = f"Pitch to {event_name} again?"
                reminder_description = f"""
Time to consider pitching to this event again!

Previous event: {task.title}
Completed: {datetime.now().strftime('%Y-%m-%d')}

Links:
- Main task: https://app.vikunja.cloud/tasks/{task.id}
{"- Previous work: https://app.vikunja.cloud/projects/" + str(subproject.id) if subproject else ""}

Review and decide:
- [ ] Check CFP timeline
- [ ] Review previous talk/feedback
- [ ] Decide on topic (same or new?)
- [ ] Update materials if needed
- [ ] Submit proposal

If interested, promote to sub-project with: python3 promote_task_to_project.py <task_id> --template talk
""".strip()

                reminder_task = client.tasks.create(
                    project_id=task.project_id,
                    title=reminder_title,
                    description=reminder_description,
                    due_date=reminder_date.isoformat(),
                    priority=3
                )
                print(f"   ✅ Created: {reminder_task.title}")
                print(f"   📅 Due: {next_year_date}")
                print()

        # Summary
        print("=" * 80)
        print("EVENT COMPLETION RECORDED")
        print("=" * 80)
        print()
        print("✅ Actions taken:")
        print(f"   Main task marked DONE: {task.title}")

        if created_followup:
            print(f"   Follow-up tasks created: {len(created_followup)}")

        if reminder_task:
            print(f"   Next-year reminder created for: {next_year_date}")

        print()
        print("📋 Next steps:")
        if created_followup:
            print("   1. Complete follow-up tasks:")
            for ft in created_followup:
                print(f"      - {ft.title}")
        print(f"   2. Archive sub-project when all follow-up complete")
        if reminder_task:
            print(f"   3. Wait for reminder ({next_year_date}) to consider pitching again")

        print()
        print("🔗 Links:")
        print(f"   Completed task: https://app.vikunja.cloud/tasks/{task.id}")
        if subproject:
            print(f"   Sub-project: https://app.vikunja.cloud/projects/{subproject.id}")
        if reminder_task:
            print(f"   Next-year reminder: https://app.vikunja.cloud/tasks/{reminder_task.id}")

        print()
        print("=" * 80)

        return True

    except Exception as e:
        print(f"\n❌ Completion failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Complete event with follow-up tasks and next-year reminder',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
What This Does:

1. Marks main task as DONE ✅
2. Creates follow-up tasks in sub-project:
   - Collect feedback and reviews
   - Capture completion notes
   - Process learnings for next time
   - Share materials and follow-up
3. Creates reminder to pitch again next year
4. Keeps sub-project active for follow-up work

Workflow:
1. Deliver event
2. Run this script
3. Complete follow-up tasks
4. Archive sub-project when done
5. Wait for next-year reminder

Examples:
  # Complete event with notes
  python3 complete_event.py 216450 --notes "Great turnout, lots of interest in demos"

  # Specify custom next-year date
  python3 complete_event.py 216450 --next-year-date 2026-11-15

  # Skip follow-up tasks (just mark done and create reminder)
  python3 complete_event.py 216450 --skip-followup

  # See what will happen
  python3 complete_event.py 216450 --dry-run
        """
    )
    parser.add_argument('task_id', type=int, help='ID of completed event task')
    parser.add_argument('--next-year-date', help='When to pitch again (YYYY-MM-DD, default: +1 year)')
    parser.add_argument('--notes', '-n', help='Initial completion notes')
    parser.add_argument('--skip-followup', action='store_true',
                        help="Don't create follow-up tasks")
    parser.add_argument('--skip-reminder', action='store_true',
                        help="Don't create next-year reminder")
    parser.add_argument('--dry-run', '-d', action='store_true',
                        help='Show plan without executing')

    args = parser.parse_args()

    # Validate next-year-date if provided
    if args.next_year_date:
        try:
            datetime.strptime(args.next_year_date, '%Y-%m-%d')
        except ValueError:
            print(f"❌ Invalid date format: {args.next_year_date}")
            print("Use YYYY-MM-DD format")
            sys.exit(1)

    success = complete_event(
        args.task_id,
        args.next_year_date,
        args.notes,
        args.skip_followup,
        args.skip_reminder,
        args.dry_run
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
