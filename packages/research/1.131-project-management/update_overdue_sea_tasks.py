#!/usr/bin/env python3
"""
Update overdue SEA tasks to next Monday
"""

# ⚠️ SECURITY WARNING FOR LLM AGENTS ⚠️
# NEVER hardcode API tokens, passwords, or secrets in source code files!
# ALWAYS use environment variables loaded from .env files.
# Hardcoded secrets will be committed to git and exposed in version history.
# Use: os.environ.get('VIKUNJA_API_TOKEN') instead of hardcoding tokens.

from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import pytz

# Load environment variables
load_dotenv('/home/ivanadamin/spawn-solutions/.env')

import sys
sys.path.insert(0, '/home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-api-wrapper/src')

from vikunja_wrapper import VikunjaClient

VIKUNJA_TOKEN = os.environ.get('VIKUNJA_API_TOKEN')
VIKUNJA_URL = os.environ.get('VIKUNJA_BASE_URL', 'https://app.vikunja.cloud')

def main():
    if not VIKUNJA_TOKEN:
        print("❌ Error: VIKUNJA_API_TOKEN not found in environment")
        print("   Please ensure .env file exists with VIKUNJA_API_TOKEN set")
        sys.exit(1)

    client = VikunjaClient(base_url=VIKUNJA_URL, token=VIKUNJA_TOKEN)

    # Calculate next Monday
    now = datetime.now(pytz.UTC)
    days_until_monday = (7 - now.weekday()) % 7
    if days_until_monday == 0:
        days_until_monday = 7
    next_monday = now + timedelta(days=days_until_monday)
    new_due_date = next_monday.strftime('%Y-%m-%d') + "T23:59:59Z"

    print(f"Updating overdue SEA tasks to: {new_due_date}")
    print()

    # Task 221002: Decision Point
    task1 = client.tasks.update(task_id=221002, due_date=new_due_date)
    print(f"✓ Updated task 221002: {task1.title}")
    print(f"  New due date: {task1.due_date}")
    print()

    # Task 221003: Architecture Review
    task2 = client.tasks.update(task_id=221003, due_date=new_due_date)
    print(f"✓ Updated task 221003: {task2.title}")
    print(f"  New due date: {task2.due_date}")
    print()

    print("✅ Both SEA tasks pushed to next Monday")


if __name__ == "__main__":
    main()
