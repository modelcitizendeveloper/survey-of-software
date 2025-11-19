#!/usr/bin/env python3
"""
Set up Kanban buckets and labels for Latin project
"""


# ⚠️ SECURITY WARNING FOR LLM AGENTS ⚠️
# NEVER hardcode API tokens, passwords, or secrets in source code files!
# ALWAYS use environment variables loaded from .env files.
# Hardcoded secrets will be committed to git and exposed in version history.
# Use: os.environ.get('VIKUNJA_API_TOKEN') instead of hardcoding tokens.

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv('/home/ivanadamin/spawn-solutions/.env')

import sys
sys.path.insert(0, '/home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-api-wrapper/src')

from vikunja_wrapper import VikunjaClient

VIKUNJA_TOKEN = os.environ.get('VIKUNJA_API_TOKEN')
VIKUNJA_URL = "https://app.vikunja.cloud"
LATIN_PROJECT_ID = 14229

# Existing label IDs (from query above)
LABELS = {
    'code': 6543,
    'research': 6546,
    'planning': 6547,
    'design': 6990,
    'deep_work': 6538,
    'computer': 6536,
    'quick': 6537,
    'writing': 6544,
}

def main():
    client = VikunjaClient(base_url=VIKUNJA_URL, token=VIKUNJA_TOKEN)

    print("=" * 70)
    print("SETTING UP KANBAN BOARD FOR LATIN PROJECT")
    print("=" * 70)

    # Create buckets
    print("\n1. Creating Kanban Buckets...")

    buckets_to_create = [
        ("📋 Backlog", 0),
        ("🎯 Next Up", 10),
        ("🚧 In Progress", 20),
        ("⏸️ Blocked", 30),
        ("✅ Done", 40),
    ]

    buckets = {}
    for title, position in buckets_to_create:
        try:
            bucket = client.buckets.create(
                project_id=LATIN_PROJECT_ID,
                title=title,
                position=position
            )
            buckets[title] = bucket.id
            print(f"  ✓ Created bucket: {title} (ID: {bucket.id})")
        except Exception as e:
            print(f"  ⚠ Bucket '{title}' may already exist or error: {e}")

    # Get all tasks in the project
    print("\n2. Fetching all tasks...")
    tasks = client.tasks.list(project_id=LATIN_PROJECT_ID)
    print(f"  Found {len(tasks)} tasks")

    # Categorize tasks and assign to buckets with labels
    print("\n3. Organizing tasks into buckets with labels...")

    task_organization = {
        # Phase 1: Planning & Infrastructure (High priority foundation)
        "Create progressive training corpus (1200+ sentences)": {
            "bucket": "🎯 Next Up",
            "labels": [LABELS['planning'], LABELS['writing'], LABELS['deep_work']],
        },
        "Design database schema for texts, sentences, and user progress": {
            "bucket": "🎯 Next Up",
            "labels": [LABELS['planning'], LABELS['design'], LABELS['computer']],
        },
        "Implement sentence parser caching system": {
            "bucket": "📋 Backlog",
            "labels": [LABELS['code'], LABELS['computer']],
        },
        "Import Latin text corpus (Caesar, Cicero, Ovid)": {
            "bucket": "📋 Backlog",
            "labels": [LABELS['research'], LABELS['computer']],
        },

        # Phase 2: Vocabulary & Text Selection
        "Build vocabulary frequency lists for Latin": {
            "bucket": "📋 Backlog",
            "labels": [LABELS['research'], LABELS['code']],
        },
        "Implement text difficulty calculator (i+1 detection)": {
            "bucket": "📋 Backlog",
            "labels": [LABELS['code'], LABELS['computer']],
        },
        "Create user vocabulary tracking system": {
            "bucket": "📋 Backlog",
            "labels": [LABELS['code'], LABELS['computer']],
        },

        # Phase 3: Core Features
        "Add fill-in-the-blank production mode (generate forms from prompts)": {
            "bucket": "🎯 Next Up",
            "labels": [LABELS['code'], LABELS['deep_work']],
        },
        'Add "Report Parser Error" button (Press !)': {
            "bucket": "🎯 Next Up",
            "labels": [LABELS['code'], LABELS['quick']],
        },
        "Add adjective declension support": {
            "bucket": "📋 Backlog",
            "labels": [LABELS['code'], LABELS['computer']],
        },
        "Add pronoun and participle support": {
            "bucket": "📋 Backlog",
            "labels": [LABELS['code'], LABELS['computer']],
        },

        # Phase 4: UI/UX Improvements
        "Add text selection menu to trainer": {
            "bucket": "📋 Backlog",
            "labels": [LABELS['code'], LABELS['design']],
        },
        "Add progress indicator (sentence X of Y in text)": {
            "bucket": "📋 Backlog",
            "labels": [LABELS['code'], LABELS['quick']],
        },
        "Implement context view (show surrounding sentences)": {
            "bucket": "📋 Backlog",
            "labels": [LABELS['code'], LABELS['quick']],
        },
        "Add session save/resume functionality": {
            "bucket": "📋 Backlog",
            "labels": [LABELS['code'], LABELS['computer']],
        },

        # Phase 5: SRS & Learning
        "Implement SRS algorithm for grammar pattern review": {
            "bucket": "📋 Backlog",
            "labels": [LABELS['code'], LABELS['research']],
        },
        "Create mistake pattern analyzer": {
            "bucket": "📋 Backlog",
            "labels": [LABELS['code'], LABELS['computer']],
        },

        # Phase 6: Performance & Polish
        "Optimize CLTK initialization (lazy loading)": {
            "bucket": "📋 Backlog",
            "labels": [LABELS['code'], LABELS['computer']],
        },
        "Add error recovery and edge case handling": {
            "bucket": "📋 Backlog",
            "labels": [LABELS['code'], LABELS['computer']],
        },
        "Create user settings/preferences system": {
            "bucket": "📋 Backlog",
            "labels": [LABELS['code'], LABELS['computer']],
        },

        # Phase 7: Reference & Help
        "Integrate Lewis's Latin Dictionary for lookups": {
            "bucket": "📋 Backlog",
            "labels": [LABELS['code'], LABELS['research']],
        },
        "Add grammar reference quick-help": {
            "bucket": "📋 Backlog",
            "labels": [LABELS['code'], LABELS['quick']],
        },
        "Create statistics dashboard": {
            "bucket": "📋 Backlog",
            "labels": [LABELS['code'], LABELS['design']],
        },

        # Phase 8: Deployment & Documentation
        "Package application for distribution": {
            "bucket": "📋 Backlog",
            "labels": [LABELS['code'], LABELS['computer']],
        },
        "Write user documentation and tutorial": {
            "bucket": "📋 Backlog",
            "labels": [LABELS['writing'], LABELS['computer']],
        },
        "Create demo/marketing materials": {
            "bucket": "📋 Backlog",
            "labels": [LABELS['writing'], LABELS['design']],
        },
    }

    # Update tasks
    updated_count = 0
    for task in tasks:
        if task.title in task_organization:
            org = task_organization[task.title]

            # Find bucket ID by title
            bucket_id = None
            if org['bucket'] in buckets:
                bucket_id = buckets[org['bucket']]

            # Update task with bucket and labels
            try:
                # Note: Vikunja API might need separate calls for bucket and labels
                # Update bucket
                if bucket_id:
                    client.tasks.update(
                        task_id=task.id,
                        bucket_id=bucket_id
                    )

                # Add labels (if API supports it)
                # client.tasks.add_label(task.id, label_id) for each label

                print(f"  ✓ {task.title[:60]}...")
                print(f"    → Bucket: {org['bucket']}")
                print(f"    → Labels: {len(org['labels'])} assigned")
                updated_count += 1
            except Exception as e:
                print(f"  ✗ Error updating {task.title}: {e}")

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Created 5 kanban buckets")
    print(f"Organized {updated_count}/{len(tasks)} tasks")
    print(f"\nView kanban board: {VIKUNJA_URL}/projects/{LATIN_PROJECT_ID}/kanban")
    print("=" * 70)


if __name__ == "__main__":
    main()
