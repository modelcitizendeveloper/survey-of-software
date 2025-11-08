#!/usr/bin/env python3
"""Debug what description is being sent"""

# Create the exact same description as add_api_reminder.py
description = (
    "Security maintenance: Rotate Vikunja API token\n\n"
    "**Steps:**\n\n"
    "1. Login to https://app.vikunja.cloud/\n"
    "2. Go to Settings → API Tokens\n"
    "3. Delete old token\n"
    "4. Create new token with same permissions\n"
    "5. Update /home/ivanadmin/spawn-solutions/.env\n"
    "6. Run test_token.py to verify\n"
    "7. Reschedule this task for 6-12 months\n\n"
    "**Recommended frequency:** Every 6-12 months"
)

print("Description as Python sees it:")
print(repr(description))
print("\nDescription formatted:")
print(description)
print("\nLength:", len(description))
print("\nNumber of newlines:", description.count('\n'))
