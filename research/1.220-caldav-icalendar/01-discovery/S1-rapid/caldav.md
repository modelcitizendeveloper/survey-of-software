# caldav

**Package:** [caldav](https://pypi.org/project/caldav/)
**GitHub:** [python-caldav/caldav](https://github.com/python-caldav/caldav)
**Docs:** https://caldav.readthedocs.io

## Overview

CalDAV (RFC 4791) client library for Python. Communicates with calendar servers.

## Stats

| Metric | Value |
|--------|-------|
| Monthly Downloads | 107K |
| Latest Version | 2.2.3 |
| Python Support | 3.9+ |
| License | GPL-3.0 or Apache-2.0 |

## Dependencies

- icalendar
- lxml
- niquests (HTTP client)
- dnspython

## Features

- CalDAV protocol (RFC 4791)
- Auto-discovery (RFC 6764) - v2.2+
- CRUD operations on remote calendars
- Server compatibility hints for quirky implementations
- Scheduling support (RFC 6638) - in progress

## Supported Servers

| Server | Status | Notes |
|--------|--------|-------|
| Nextcloud | Full | v2.2 auto-discovery |
| DAViCal | Full | |
| Radicale | Full | |
| Fastmail | Full | |
| iCloud | Full | App-specific password |
| Zimbra | Full | |
| Vikunja | Full | Built-in CalDAV |

## Example

```python
import caldav

# Connect (v2.2+ auto-discovery)
client = caldav.DAVClient(
    url="nextcloud.example.com",
    username="user",
    password="pass"
)
principal = client.principal()
calendars = principal.calendars()

# List events
for calendar in calendars:
    events = calendar.events()
    for event in events:
        print(event.data)

# Create event
calendar.save_event(ics_content)

# Search
events = calendar.date_search(
    start=datetime(2025, 12, 1),
    end=datetime(2025, 12, 31)
)
```

## Notes

- Handles server quirks with compatibility hints
- Depends on icalendar for ICS parsing
- v2.2 (Dec 2025) major improvement for auto-discovery
