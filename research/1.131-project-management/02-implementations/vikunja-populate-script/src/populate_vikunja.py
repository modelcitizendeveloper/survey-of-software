#!/usr/bin/env python3
"""
Vikunja Population Script

Populate Vikunja with projects, labels, and tasks from YAML/JSON files.

Usage:
    python populate_vikunja.py input.yaml
    python populate_vikunja.py --dry-run input.yaml
    python populate_vikunja.py --verbose input.json
"""

import argparse
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

from parsing import parse_input, ParsingError
from validation import validate_schema, ValidationError
from population import populate_vikunja, PopulationError


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Populate Vikunja with projects, labels, and tasks from YAML/JSON",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Populate from YAML file
  python populate_vikunja.py tasks.yaml

  # Validate without creating (dry run)
  python populate_vikunja.py --dry-run tasks.yaml

  # Verbose output
  python populate_vikunja.py --verbose tasks.json

Input file format:
  See SCHEMA.md for full documentation.
  Supports .yaml, .yml, and .json files.
        """
    )

    parser.add_argument(
        "input_file",
        type=Path,
        help="Path to YAML or JSON input file"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate schema without creating resources (no API calls)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output (show all API calls)"
    )

    parser.add_argument(
        "--preserve-api-order",
        action="store_true",
        help="Preserve Vikunja API order (tasks added to top). By default, tasks are reversed to match YAML order."
    )

    parser.add_argument(
        "--allow-root-project",
        action="store_true",
        help="Allow creating root-level projects (bypasses parent project requirement). Use for automation/testing only."
    )

    args = parser.parse_args()

    # Load environment variables
    env_path = Path(__file__).parent.parent.parent.parent.parent.parent / '.env'
    if not env_path.exists():
        print(f"❌ Error: .env file not found at: {env_path}")
        print("   See ../vikunja-api-wrapper/QUICK_START.md for setup instructions")
        sys.exit(1)

    load_dotenv(env_path)

    # Check environment variables
    api_token = os.environ.get("VIKUNJA_API_TOKEN")
    base_url = os.environ.get("VIKUNJA_BASE_URL", "https://app.vikunja.cloud")

    if not api_token:
        print("❌ Error: VIKUNJA_API_TOKEN not found in .env file")
        sys.exit(1)

    # Step 1: Parse input file
    if args.verbose:
        print(f"📄 Parsing input file: {args.input_file}")

    try:
        schema = parse_input(args.input_file)
    except ParsingError as e:
        print(f"❌ Parsing Error: {e}")
        sys.exit(1)

    if args.verbose:
        print(f"✅ Parsed successfully")
        print(f"   Project: {schema['project']['title']}")
        print(f"   Labels: {len(schema.get('labels', []))}")
        print(f"   Tasks: {len(schema.get('tasks', []))}")

    # Step 2: Validate schema
    if args.verbose:
        print(f"\n🔍 Validating schema...")

    try:
        validate_schema(schema, allow_root_project=args.allow_root_project)
    except ValidationError as e:
        print(f"❌ Validation Error: {e}")
        sys.exit(1)

    if args.verbose:
        print(f"✅ Schema is valid")

    # Dry run mode - stop here
    if args.dry_run:
        print(f"\n✅ DRY RUN - Schema is valid, no resources created")
        print(f"\nSummary:")
        print(f"  Project: {schema['project']['title']}")

        labels = schema.get('labels', [])
        if labels:
            print(f"  Labels ({len(labels)}):")
            for label in labels:
                print(f"    - {label['title']}")

        tasks = schema.get('tasks', [])
        if tasks:
            print(f"  Tasks ({len(tasks)}):")
            for task in tasks:
                task_labels = task.get('labels', [])
                labels_str = f" [{', '.join(task_labels)}]" if task_labels else ""
                print(f"    - {task['title']}{labels_str}")

        sys.exit(0)

    # Step 3: Initialize Vikunja client
    if args.verbose:
        print(f"\n🔌 Connecting to Vikunja API: {base_url}")

    try:
        # Import only when needed (avoid missing dependencies in dry-run mode)
        sys.path.insert(0, str(Path(__file__).parent.parent.parent / "vikunja-api-wrapper" / "src"))
        from vikunja_wrapper import VikunjaClient

        client = VikunjaClient(base_url=base_url, token=api_token)
    except Exception as e:
        print(f"❌ Failed to connect to Vikunja API: {e}")
        sys.exit(1)

    # Step 4: Populate Vikunja
    if args.verbose:
        print(f"\n🚀 Creating resources in Vikunja...")

    try:
        result = populate_vikunja(client, schema, dry_run=False, preserve_api_order=args.preserve_api_order)
    except PopulationError as e:
        print(f"❌ Population Error: {e}")
        sys.exit(1)

    # Success!
    print(f"\n✅ Successfully populated Vikunja!")
    print(f"\nCreated:")
    print(f"  📁 Project: {result['project'].title} (ID: {result['project'].id})")

    if result['labels']:
        print(f"  🏷️  Labels ({len(result['labels'])}):")
        for label in result['labels']:
            print(f"     - {label.title} (ID: {label.id})")

    if result['tasks']:
        print(f"  ✅ Tasks ({len(result['tasks'])}):")
        for task in result['tasks']:
            print(f"     - {task.title} (ID: {task.id})")

    print(f"\n🌐 View in Vikunja: {base_url}/projects/{result['project'].id}")


if __name__ == "__main__":
    main()
