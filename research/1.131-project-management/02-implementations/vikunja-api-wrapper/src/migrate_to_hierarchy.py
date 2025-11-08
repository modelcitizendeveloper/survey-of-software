#!/usr/bin/env python3
"""
Migrate existing Vikunja projects into hierarchy.

This script moves existing top-level projects under their appropriate parent
projects according to the organizational structure.

Usage:
    python migrate_to_hierarchy.py --dry-run  # Preview changes
    python migrate_to_hierarchy.py            # Execute migration
"""

import os
import sys
from dotenv import load_dotenv
from vikunja_wrapper import VikunjaClient, NotFoundError

# Load environment
load_dotenv('/home/ivanadamin/spawn-solutions/.env')

# Parent project IDs (created Nov 8, 2025)
FOUNDATIONS_ID = 13447  # Blue - capability development
APPLICATIONS_ID = 13448  # Green - capability application
CLIENTS_ID = 13449  # Red - customer-facing work

# Migration mapping: project title → parent ID
MIGRATION_MAP = {
    # Foundations (5 children)
    "spawn": FOUNDATIONS_ID,
    "spawn-experiments": FOUNDATIONS_ID,
    "spawn-solutions": FOUNDATIONS_ID,
    "spawn-analysis": FOUNDATIONS_ID,
    "spawn-patents": FOUNDATIONS_ID,

    # Applications (12 children)
    "qrcards": APPLICATIONS_ID,
    "schema-evolution-automation": APPLICATIONS_ID,
    "inverse-fractional": APPLICATIONS_ID,
    "project-management": APPLICATIONS_ID,
    "cookbooks": APPLICATIONS_ID,
    "elevator-project": APPLICATIONS_ID,
    "boutique-hotel-recs": APPLICATIONS_ID,
    "business-database": APPLICATIONS_ID,
    "intelligence-portal": APPLICATIONS_ID,
    "org-chart": APPLICATIONS_ID,
    "research-lineage-system": APPLICATIONS_ID,
    "werise": APPLICATIONS_ID,

    # Clients (6 children)
    "decision-analysis": CLIENTS_ID,
    "ivantohelpyou": CLIENTS_ID,
    "model-citizen-developer": CLIENTS_ID,
    "convention-city-seattle": CLIENTS_ID,
    "inverse-fractional-site": CLIENTS_ID,
    "taelyen": CLIENTS_ID,
}


def main():
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print("🔍 DRY RUN MODE - No changes will be made\n")
    else:
        print("🚀 MIGRATION MODE - Projects will be moved\n")

    # Initialize client
    client = VikunjaClient(
        base_url="https://app.vikunja.cloud",
        token=os.getenv('VIKUNJA_API_TOKEN')
    )

    # Get all projects
    print("📋 Fetching all projects from Vikunja...\n")
    all_projects = client.projects.list()

    # Build map of title → project for quick lookup
    projects_by_title = {p.title: p for p in all_projects}

    # Track statistics
    stats = {
        "total_to_migrate": len(MIGRATION_MAP),
        "found": 0,
        "already_correct": 0,
        "migrated": 0,
        "not_found": 0,
    }

    print(f"Total projects in Vikunja: {len(all_projects)}")
    print(f"Projects to migrate: {stats['total_to_migrate']}\n")
    print("=" * 80)

    # Process each project in migration map
    for title, target_parent_id in sorted(MIGRATION_MAP.items()):
        # Find parent name for display
        parent_name = {
            FOUNDATIONS_ID: "Foundations",
            APPLICATIONS_ID: "Applications",
            CLIENTS_ID: "Clients",
        }.get(target_parent_id, f"Unknown ({target_parent_id})")

        # Check if project exists
        if title not in projects_by_title:
            print(f"❌ NOT FOUND: '{title}'")
            stats["not_found"] += 1
            continue

        project = projects_by_title[title]
        stats["found"] += 1

        # Check current parent
        if project.parent_project_id == target_parent_id:
            print(f"✅ ALREADY CORRECT: '{title}' → {parent_name} (ID: {project.id})")
            stats["already_correct"] += 1
            continue

        # Show current state
        current_parent = "Top-level" if project.parent_project_id == 0 else f"Parent ID {project.parent_project_id}"
        print(f"📦 MIGRATE: '{title}' (ID: {project.id})")
        print(f"   From: {current_parent}")
        print(f"   To:   {parent_name} (ID: {target_parent_id})")

        if not dry_run:
            try:
                # Execute migration (must include title due to Vikunja API requirement)
                updated = client.projects.update(
                    project.id,
                    title=project.title,  # Preserve existing title
                    parent_project_id=target_parent_id
                )
                print(f"   ✅ SUCCESS - Now under {parent_name}")
                stats["migrated"] += 1
            except NotFoundError as e:
                print(f"   ❌ ERROR: {e}")
            except Exception as e:
                print(f"   ❌ UNEXPECTED ERROR: {e}")
        else:
            print(f"   🔍 WOULD MOVE (dry-run)")
            stats["migrated"] += 1  # Count as would-be migrated

        print()

    # Print summary
    print("=" * 80)
    print("\n📊 MIGRATION SUMMARY\n")
    print(f"Total in migration map: {stats['total_to_migrate']}")
    print(f"  ✅ Found in Vikunja: {stats['found']}")
    print(f"  ✅ Already correct:  {stats['already_correct']}")

    if dry_run:
        print(f"  📦 Would migrate:    {stats['migrated']}")
    else:
        print(f"  ✅ Migrated:         {stats['migrated']}")

    print(f"  ❌ Not found:        {stats['not_found']}")

    if stats["not_found"] > 0:
        print("\n⚠️  Some projects were not found. They may not exist yet or have different titles.")

    if dry_run:
        print("\n🔍 This was a DRY RUN - no changes were made.")
        print("   Run without --dry-run to execute the migration.")
    else:
        print("\n✅ Migration complete!")
        print("   View hierarchy: https://app.vikunja.cloud")

    print()


if __name__ == "__main__":
    main()
