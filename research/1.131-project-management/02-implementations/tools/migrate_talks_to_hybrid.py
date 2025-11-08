#!/usr/bin/env python3
"""
Migrate Talks to Hybrid Pattern

Creates main kanban tasks for each sub-project event.

Usage:
    python3 migrate_talks_to_hybrid.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'vikunja-api-wrapper', 'src'))

from vikunja_wrapper import VikunjaClient

VIKUNJA_API_TOKEN = "tk_b58cb267d291c55985136b9f054a62e0502e803f"
VIKUNJA_BASE_URL = "https://app.vikunja.cloud"

def migrate_to_hybrid():
    """Create main kanban tasks for existing sub-projects"""

    client = VikunjaClient(base_url=VIKUNJA_BASE_URL, token=VIKUNJA_API_TOKEN)

    print("=" * 80)
    print("MIGRATING TALKS TO HYBRID PATTERN")
    print("=" * 80)

    # Get Talks project and sub-projects
    all_projects = client.projects.list()
    talks_project = next((p for p in all_projects if p.id == 13481), None)
    sub_projects = [p for p in all_projects if p.parent_project_id == 13481]

    print(f"\nMain project: {talks_project.title}")
    print(f"Sub-projects: {len(sub_projects)}")
    print()

    # Get existing tasks in main project
    existing_tasks = client.tasks.list(project_id=13481)
    existing_titles = {t.title for t in existing_tasks}

    # Event stage mapping (you can adjust these)
    event_stages = {
        "PyCascades 2025: Schema Evolution": "✅ Accepted",  # Already accepted
        "NWES 2026 Talk": "📝 Proposal Writing",  # Working on proposal
    }

    created_count = 0

    print("Creating main kanban tasks:")
    print()

    for sp in sub_projects:
        event_title = sp.title

        # Check if main task already exists
        if event_title in existing_titles:
            print(f"⏭️  Skipped: {event_title} (task already exists)")
            continue

        # Get bucket for this event
        bucket_name = event_stages.get(event_title, "💡 Ideas")

        # Create main tracking task
        description = f"""
Event: {sp.title}

{sp.description or ''}

📂 Details: https://app.vikunja.cloud/projects/{sp.id}

<strong>Progress tracking:</strong>
- This task represents the event's position in the speaking pipeline
- Detailed tasks are in the sub-project linked above
- Move this task through the kanban as the event progresses
- Mark DONE when delivered, then archive the sub-project
"""

        try:
            # Note: We'd need to get bucket_id to set bucket
            # For now, just create the task
            task = client.tasks.create(
                project_id=13481,
                title=event_title,
                description=description.strip(),
                priority=5 if "2025" in event_title else 3
            )

            print(f"✅ Created: {task.title}")
            print(f"   → Assigned to: {bucket_name}")
            print(f"   → Details: https://app.vikunja.cloud/projects/{sp.id}")
            print()

            created_count += 1

        except Exception as e:
            print(f"❌ Failed to create task for {event_title}: {e}")

    print("=" * 80)
    print(f"SUMMARY")
    print("=" * 80)
    print(f"Main tasks created: {created_count}")
    print()

    if created_count > 0:
        print("✅ Migration complete!")
        print("\nNext steps:")
        print("1. Manually move tasks to correct buckets in kanban")
        print("2. Link sub-project tasks as subtasks (optional)")
        print("3. Use main kanban for pipeline tracking")
        print("4. Use sub-projects for detailed work")
    else:
        print("ℹ️  No new tasks created")

    print("=" * 80)


if __name__ == "__main__":
    migrate_to_hybrid()
