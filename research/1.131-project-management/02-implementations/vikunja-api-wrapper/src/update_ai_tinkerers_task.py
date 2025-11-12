#!/usr/bin/env python3
"""
Update AI Tinkerers task with upcoming events from seattle.aitinkerers.org
"""
import os
import sys
from vikunja_wrapper import VikunjaClient

def create_events_html() -> str:
    """Generate HTML description with upcoming AI Tinkerers events."""

    html = """<h2>Upcoming AI Tinkerers - Seattle Events</h2>

<h3>🎯 Frontier Builds Demo Night: Experiments at the Edge of AI</h3>
<ul>
  <li><strong>Date:</strong> Wednesday, November 12th, 2025</li>
  <li><strong>Time:</strong> 6:00 PM - 9:00 PM</li>
  <li><strong>Status:</strong> 160+ registered</li>
  <li><strong>RSVP:</strong> <a href="https://seattle.aitinkerers.org/p/frontier-builds-demo-night-experiments-at-the-edge-of-ai">Register Here</a></li>
</ul>

<h3>🛠️ AI Tinkerers Seattle Meetup: Dev Tools Track</h3>
<ul>
  <li><strong>Date:</strong> Monday, December 8th, 2025</li>
  <li><strong>Time:</strong> 6:00 PM - 9:00 PM</li>
  <li><strong>Status:</strong> 179+ registered</li>
  <li><strong>RSVP:</strong> <a href="https://seattle.aitinkerers.org/p/ai-tinkerers-seattle-meetup-dev-tools-track-december-8-2025">Register Here</a></li>
</ul>

<hr>

<h3>📍 Resources</h3>
<ul>
  <li><strong>Seattle Chapter:</strong> <a href="https://seattle.aitinkerers.org/">seattle.aitinkerers.org</a></li>
  <li><strong>All Events:</strong> <a href="https://aitinkerers.org/events">aitinkerers.org/events</a></li>
  <li><strong>Global Network:</strong> 187 chapters worldwide</li>
  <li><strong>Jobs Board:</strong> <a href="https://seattle.aitinkerers.org/jobs">seattle.aitinkerers.org/jobs</a></li>
</ul>

<p><em>Last updated: November 10, 2025</em></p>"""

    return html


def main():
    """Update the AI Tinkerers task with event information."""

    # Get credentials from environment
    base_url = os.getenv("VIKUNJA_BASE_URL", "https://app.vikunja.cloud")
    token = os.getenv("VIKUNJA_TOKEN")

    if not token:
        print("Error: VIKUNJA_TOKEN environment variable not set")
        print("Please set it with: export VIKUNJA_TOKEN='your-token'")
        sys.exit(1)

    # Initialize client
    client = VikunjaClient(base_url=base_url, token=token)

    # Task ID from the user
    task_id = 217401

    # Generate HTML description
    html_description = create_events_html()

    print(f"Updating task {task_id} with AI Tinkerers events...")
    print(f"\nGenerated HTML ({len(html_description)} characters):")
    print("-" * 60)
    print(html_description)
    print("-" * 60)

    # Update the task
    try:
        updated_task = client.tasks.update(
            task_id=task_id,
            description=html_description
        )
        print(f"\n✅ Successfully updated task: {updated_task.title}")
        print(f"   Task ID: {updated_task.id}")
        print(f"   View at: {base_url}/tasks/{task_id}")
    except Exception as e:
        print(f"\n❌ Error updating task: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
