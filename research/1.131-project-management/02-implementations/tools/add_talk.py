#!/usr/bin/env python3
"""
Add Talk Opportunity to Vikunja

Simplified wrapper for adding speaking opportunities to the Talks project.
Automatically assigns to "💡 Ideas" bucket and calculates proposal deadline.
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

TALKS_PROJECT_ID = 13481
IDEAS_BUCKET_NAME = "Ideas"


def parse_event_date(date_str):
    """Parse event date to datetime object."""
    if not date_str:
        return None

    try:
        return datetime.strptime(date_str, '%Y-%m-%d').replace(tzinfo=timezone.utc)
    except ValueError:
        try:
            return datetime.strptime(date_str, '%m/%d/%Y').replace(tzinfo=timezone.utc)
        except ValueError:
            print(f"⚠️  Could not parse date: {date_str}")
            print("   Use: YYYY-MM-DD or MM/DD/YYYY")
            return None


def calculate_proposal_deadline(event_date, months_before=3):
    """Calculate proposal deadline (default: 3 months before event)."""
    if not event_date:
        return None

    # Subtract months
    deadline = event_date - timedelta(days=months_before * 30)
    # Set to end of day
    deadline = deadline.replace(hour=23, minute=59, second=0, microsecond=0)
    return deadline


def build_html_description(event_date=None, location=None, focus=None,
                           organizer=None, contact=None, url=None,
                           speakers=None, notes=None):
    """Build HTML description from talk details."""
    html_parts = []

    # Event details section
    details = []
    if event_date:
        details.append(f"<li><strong>Date:</strong> {event_date.strftime('%B %d, %Y')}</li>")
    if location:
        details.append(f"<li><strong>Location:</strong> {location}</li>")
    if focus:
        details.append(f"<li><strong>Focus:</strong> {focus}</li>")
    if organizer:
        details.append(f"<li><strong>Organizer:</strong> {organizer}</li>")

    if details:
        html_parts.append("<h3>📅 Event Details</h3>")
        html_parts.append("<ul>")
        html_parts.extend(details)
        html_parts.append("</ul>")

    # Speaker lineup
    if speakers:
        html_parts.append("\n<h3>🎤 Speaker Lineup</h3>")
        html_parts.append(f"<p>{speakers}</p>")

    # Additional notes
    if notes:
        html_parts.append("\n<h3>📝 Notes</h3>")
        html_parts.append(f"<p>{notes}</p>")

    # Next steps (always include)
    html_parts.append("\n<h3>✅ Next Steps</h3>")
    html_parts.append("<ol>")
    html_parts.append("<li>Research event and audience fit</li>")
    html_parts.append("<li>Draft talk proposal angles</li>")
    html_parts.append("<li>Contact organizer for details (deadline, speaker benefits)</li>")
    html_parts.append("<li>Decide: pursue or decline</li>")
    html_parts.append("</ol>")

    # Contact info
    if contact or url:
        html_parts.append("\n<h3>🔗 Contact</h3>")
        if contact:
            html_parts.append(f"<p>Contact: {contact}</p>")
        if url:
            html_parts.append(f"<p>Website: <a href=\"{url}\">{url}</a></p>")

    return "\n".join(html_parts)


def main():
    parser = argparse.ArgumentParser(
        description='Add speaking opportunity to Talks project',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:

  # Simple talk with auto-calculated proposal deadline
  python3 add_talk.py --title "PyCon 2026" \\
    --event-date 2026-05-15 --location "Pittsburgh, PA"

  # Talk with custom deadline
  python3 add_talk.py --title "inControl Summit" \\
    --event-date 2026-06-02 --location "Düsseldorf, Germany" \\
    --proposal-deadline 2026-03-01

  # Talk with full details
  python3 add_talk.py --title "PyData Seattle" \\
    --event-date 2026-04-20 --location "Seattle, WA" \\
    --focus "Data science and ML" \\
    --organizer "NumFOCUS" \\
    --contact "pydata@example.com" \\
    --url "https://pydata.org/seattle2026"

  # Skip bucket assignment
  python3 add_talk.py --title "Local meetup" --no-bucket

Notes:
  - Automatically assigns to "💡 Ideas" bucket
  - Calculates proposal deadline as 3 months before event (if not specified)
  - Always adds task to Talks project (ID: 13481)
        """
    )

    # Required
    parser.add_argument('--title', type=str, required=True,
                        help='Talk/event title')

    # Event details
    parser.add_argument('--event-date', type=str,
                        help='Event date (YYYY-MM-DD or MM/DD/YYYY)')
    parser.add_argument('--location', type=str,
                        help='Event location')
    parser.add_argument('--focus', type=str,
                        help='Event focus/theme')
    parser.add_argument('--organizer', type=str,
                        help='Event organizer')
    parser.add_argument('--contact', type=str,
                        help='Contact email or name')
    parser.add_argument('--url', type=str,
                        help='Event website URL')
    parser.add_argument('--speakers', type=str,
                        help='Other speakers/lineup')
    parser.add_argument('--notes', type=str,
                        help='Additional notes')

    # Deadline
    parser.add_argument('--proposal-deadline', type=str,
                        help='Proposal deadline (YYYY-MM-DD). If not set, auto-calculated as 3 months before event.')
    parser.add_argument('--months-before', type=int, default=3,
                        help='Months before event for auto-calculated deadline (default: 3)')

    # Options
    parser.add_argument('--no-bucket', action='store_true',
                        help='Skip bucket assignment')
    parser.add_argument('--priority', type=int, choices=[0, 1, 2, 3, 4, 5], default=0,
                        help='Task priority (0-5, default: 0)')
    parser.add_argument('--dry-run', '-d', action='store_true',
                        help='Preview task without creating')

    args = parser.parse_args()

    # Parse event date
    event_date = parse_event_date(args.event_date) if args.event_date else None

    # Calculate/parse proposal deadline
    if args.proposal_deadline:
        due_date = parse_event_date(args.proposal_deadline)
    elif event_date:
        due_date = calculate_proposal_deadline(event_date, args.months_before)
    else:
        # No event date and no explicit deadline - use far future
        due_date = datetime(2026, 12, 31, 23, 59, 0, tzinfo=timezone.utc)
        print("⚠️  No event date or deadline specified, using 2026-12-31")

    # Build description
    description = build_html_description(
        event_date=event_date,
        location=args.location,
        focus=args.focus,
        organizer=args.organizer,
        contact=args.contact,
        url=args.url,
        speakers=args.speakers,
        notes=args.notes
    )

    # Initialize client
    client = VikunjaClient(
        base_url=os.environ.get('VIKUNJA_BASE_URL', 'https://app.vikunja.cloud'),
        token=os.environ['VIKUNJA_API_TOKEN']
    )

    print("=" * 80)
    print("ADD TALK OPPORTUNITY")
    print("=" * 80)
    print()
    print(f"Title: {args.title}")
    print(f"Project: Talks (ID: {TALKS_PROJECT_ID})")
    if event_date:
        print(f"Event Date: {event_date.strftime('%Y-%m-%d')}")
    print(f"Proposal Deadline: {due_date.strftime('%Y-%m-%d')}")
    if args.location:
        print(f"Location: {args.location}")
    print(f"Priority: {args.priority}")
    if not args.no_bucket:
        print(f"Bucket: {IDEAS_BUCKET_NAME}")
    print()

    if args.dry_run:
        print("🔍 DRY RUN - Task not created")
        print()
        print("Description preview:")
        print(description[:300] + "..." if len(description) > 300 else description)
    else:
        print("Creating task...")
        try:
            # Create task
            task_data = {
                'title': args.title,
                'project_id': TALKS_PROJECT_ID,
                'description': description,
                'due_date': due_date.isoformat(),
                'priority': args.priority
            }

            response = client._request("PUT", f"/api/v1/projects/{TALKS_PROJECT_ID}/tasks", json=task_data)
            task_id = response['id']

            print()
            print("✅ Task created successfully")
            print()
            print(f"Task ID: {task_id}")
            print(f"URL: https://app.vikunja.cloud/tasks/{task_id}")

            # Assign to bucket
            if not args.no_bucket:
                print()
                print(f"Assigning to '{IDEAS_BUCKET_NAME}' bucket...")
                try:
                    kanban_view = client.views.get_kanban_view(TALKS_PROJECT_ID)
                    buckets = client.buckets.list(TALKS_PROJECT_ID, kanban_view.id)

                    ideas_bucket = None
                    for b in buckets:
                        if IDEAS_BUCKET_NAME.lower() in b.title.lower():
                            ideas_bucket = b
                            break

                    if ideas_bucket:
                        client.tasks.set_position(
                            task_id=task_id,
                            project_view_id=kanban_view.id,
                            bucket_id=ideas_bucket.id,
                            project_id=TALKS_PROJECT_ID
                        )
                        print(f"✅ Assigned to bucket: {ideas_bucket.title}")
                    else:
                        print(f"⚠️  '{IDEAS_BUCKET_NAME}' bucket not found")

                except Exception as e:
                    print(f"⚠️  Failed to assign bucket: {e}")

        except Exception as e:
            print()
            print(f"❌ Failed to create task: {e}")
            sys.exit(1)

    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
