#!/usr/bin/env python3
"""
Add Source Documents to Applications Tasks

Bulk update all Applications project tracking tasks to include source document
references for spawn-analysis agents.
"""

import sys
import os
import argparse
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'vikunja-api-wrapper', 'src'))

from vikunja_wrapper import VikunjaClient

# Configuration
VIKUNJA_API_TOKEN = "tk_b58cb267d291c55985136b9f054a62e0502e803f"
VIKUNJA_BASE_URL = "https://app.vikunja.cloud"

# Mapping of task title patterns to folder names and codebases
# Format: (pattern, folder_name, codebase_path or None)
TASK_MAPPINGS = [
    # Sites (QRCards-hosted)
    (r'inversefractional\.com', 'inverse-fractional', None),
    (r'conventioncityseattle\.com', 'convention-city-seattle', None),
    (r'ivantohelpyou\.com', 'ivantohelpyou', None),
    (r'modelcitizendeveloper\.com', 'model-citizen-developer', None),
    (r'taelyen\.com', 'taelyen', None),
    (r'mztape\.com', 'mztape', None),

    # Products
    (r'QRCards', 'qrcards', '/home/ivanadmin/qrcards/'),
    (r'Business Database', 'business-database', None),
    (r'Boutique Hotel Recommendations', 'boutique-hotel-recs', None),

    # Services
    (r'Decision Analysis', 'products/decision-analysis', None),  # Under Products category

    # Labs
    (r'SEA|Schema Evolution', 'schema-evolution-automation', '/home/ivanadmin/spawn-experiments/tools/schema-evolution-framework/'),
    (r'Elevator Project', 'elevator-project', None),
    (r'IF Learning Lab', 'inverse-fractional/05-learning-lab', None),

    # Meta
    (r'Project Management.*Vikunja', 'project-management', '/home/ivanadmin/spawn-solutions/research/1.131-project-management/'),
    (r'Research Lineage', 'research-lineage-system', None),

    # Content
    (r'Cookbooks', 'cookbooks', None),
    (r'Intelligence Portal', 'intelligence-portal', None),

    # Spawn ecosystem
    (r'spawn-analysis', 'spawn-analysis', '/home/ivanadmin/spawn-analysis/'),
    (r'spawn-experiments', 'spawn-experiments', '/home/ivanadmin/spawn-experiments/'),
    (r'spawn-solutions', 'spawn-solutions', '/home/ivanadmin/spawn-solutions/'),
]


def find_mapping(task_title):
    """Find the folder and codebase mapping for a task title."""
    for pattern, folder, codebase in TASK_MAPPINGS:
        if re.search(pattern, task_title, re.IGNORECASE):
            return folder, codebase
    return None, None


def has_source_documents(description):
    """Check if description already has source documents section."""
    if not description:
        return False
    return 'Source Documents for Analysis' in description or '📂 Source Documents' in description


def create_source_docs_section(folder, codebase):
    """Create the source documents HTML section."""
    section = """
---
<strong>📂 Source Documents for Analysis:</strong><br>
<ul>
<li>Project definition: <code>/home/ivanadmin/spawn-solutions/applications/{folder}/vikunja-tasks.yaml</code></li>
<li>Project folder: <code>/home/ivanadmin/spawn-solutions/applications/{folder}/</code></li>
""".format(folder=folder)

    if codebase:
        section += f"<li>Codebase: <code>{codebase}</code></li>\n"

    section += "</ul>"

    return section.strip()


def update_task_with_sources(client, task, dry_run=False):
    """Update a single task with source documents."""

    # Find mapping for this task
    folder, codebase = find_mapping(task.title)

    if not folder:
        print(f"⚠️  No mapping found for: {task.title}")
        return False

    # Check if already has source documents
    if has_source_documents(task.description):
        print(f"⏭️  Already has sources: {task.title}")
        return False

    # Build new description
    source_section = create_source_docs_section(folder, codebase)

    if task.description:
        new_description = task.description + "\n\n" + source_section
    else:
        new_description = source_section

    print(f"📝 Updating: {task.title}")
    print(f"   Folder: {folder}")
    if codebase:
        print(f"   Codebase: {codebase}")

    if dry_run:
        print("   [DRY RUN - no changes made]")
        return True

    # Update task
    try:
        client.tasks.update(
            task_id=task.id,
            description=new_description
        )
        print(f"   ✅ Updated task {task.id}")
        return True
    except Exception as e:
        print(f"   ❌ Failed to update: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Add source document references to Applications tasks',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
What This Does:

Adds source document references to all Applications project tracking tasks
so that spawn-analysis agents can find evidence to make informed decisions.

Each task gets a "Source Documents for Analysis" section with:
- Project definition YAML path
- Project folder path
- Codebase path (if applicable)

Examples:
  # Preview changes
  python3 add_source_documents.py --dry-run

  # Update all tasks
  python3 add_source_documents.py

  # Update specific project
  python3 add_source_documents.py --project 13448

  # Force update even if sources exist
  python3 add_source_documents.py --force
        """
    )
    parser.add_argument('--project', type=int, default=13448,
                        help='Project ID (default: 13448 Applications)')
    parser.add_argument('--dry-run', '-d', action='store_true',
                        help='Show what would be updated without making changes')
    parser.add_argument('--force', '-f', action='store_true',
                        help='Update even if source documents already exist')

    args = parser.parse_args()

    client = VikunjaClient(base_url=VIKUNJA_BASE_URL, token=VIKUNJA_API_TOKEN)

    print("=" * 80)
    print("ADDING SOURCE DOCUMENTS TO APPLICATIONS TASKS")
    print("=" * 80)
    print()

    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
        print()

    # Get all tasks in project
    try:
        tasks = client.tasks.list(project_id=args.project)
    except Exception as e:
        print(f"❌ Failed to get tasks from project {args.project}: {e}")
        sys.exit(1)

    print(f"Found {len(tasks)} tasks in project {args.project}")
    print()

    # Update each task
    updated = 0
    skipped = 0
    failed = 0

    for task in tasks:
        # Skip done tasks
        if task.done:
            print(f"⏭️  Skipping done task: {task.title}")
            skipped += 1
            continue

        # Skip if already has sources (unless --force)
        if not args.force and has_source_documents(task.description):
            print(f"⏭️  Already has sources: {task.title}")
            skipped += 1
            continue

        print()
        success = update_task_with_sources(client, task, args.dry_run)
        if success:
            updated += 1
        else:
            failed += 1

    # Summary
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✅ Updated: {updated}")
    print(f"⏭️  Skipped: {skipped}")
    print(f"❌ Failed: {failed}")
    print()

    if args.dry_run:
        print("Run without --dry-run to apply changes")
    else:
        print("Source documents added to Applications tasks!")


if __name__ == "__main__":
    main()
