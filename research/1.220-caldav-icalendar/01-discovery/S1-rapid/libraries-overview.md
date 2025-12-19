# 1.220 CalDAV/iCalendar Libraries - S1 Rapid Research

**Date**: December 19, 2025
**Status**: S1 Complete

## Summary

Three main Python libraries cover CalDAV and iCalendar needs. **icalendar** is the dominant choice for parsing/generating iCal files. **caldav** handles server communication. **vobject** is legacy but still maintained.

## Library Comparison

| Library | Purpose | Monthly Downloads | Python | Latest Version |
|---------|---------|-------------------|--------|----------------|
| [icalendar](https://pypi.org/project/icalendar/) | Parse/generate iCal (RFC 5545) | **4.7M** | 3.8-3.13 | 6.3.2 |
| [vobject](https://pypi.org/project/vobject/) | Parse/generate iCal + vCard | 783K | 3.8+ | 1.x |
| [caldav](https://pypi.org/project/caldav/) | CalDAV client (RFC 4791) | 107K | 3.9+ | 2.2.3 |

## Recommendations

### For Vikunja Calendar Integration

**Use: icalendar + caldav**

```python
# icalendar - parse/create events
from icalendar import Calendar, Event

# caldav - communicate with CalDAV servers
import caldav
```

**Don't use vobject** - older API, lower adoption, icalendar is better maintained.

## Library Details

### icalendar (collective/icalendar)

**Strengths:**
- 4.7M downloads/month - de facto standard
- Full RFC 5545 support
- Recurring events via dateutil.rrule
- Active maintenance (v6.3.2, Dec 2025)

**Use for:**
- Parsing ICS files/feeds
- Generating calendar events
- RRULE expansion (recurring events)

**Docs:** https://icalendar.readthedocs.io

### caldav (python-caldav/caldav)

**Strengths:**
- CalDAV protocol client (RFC 4791)
- Works with: Nextcloud, DAViCal, Radicale, Fastmail, iCloud
- v2.2 (Dec 2025): RFC 6764 auto-discovery
- Server compatibility hints for quirky implementations

**Use for:**
- Syncing with CalDAV servers
- CRUD operations on remote calendars
- Two-way sync implementations

**Note:** caldav depends on icalendar internally.

**Docs:** https://caldav.readthedocs.io

### vobject (py-vobject/vobject)

**Status:** Legacy, still maintained

**Use only if:**
- Need vCard support (contacts)
- Maintaining legacy code
- Otherwise prefer icalendar

## Related RFCs

| RFC | Name | Library |
|-----|------|---------|
| RFC 5545 | iCalendar format | icalendar |
| RFC 4791 | CalDAV protocol | caldav |
| RFC 6764 | CalDAV auto-discovery | caldav v2.2+ |
| RFC 6638 | CalDAV scheduling | caldav (in progress) |

## For Vikunja Integration

### ICS Export (Vikunja → Calendar apps)
```python
from icalendar import Calendar, Event
from datetime import datetime

cal = Calendar()
event = Event()
event.add('summary', 'Review Q4 report')
event.add('dtstart', datetime(2025, 12, 20, 14, 0))
event.add('dtend', datetime(2025, 12, 20, 15, 0))
cal.add_component(event)

ics_content = cal.to_ical()
```

### CalDAV Sync (two-way with Nextcloud)
```python
import caldav

# v2.2+ supports auto-discovery
client = caldav.DAVClient(url="nextcloud.example.com", username="user", password="pass")
principal = client.principal()
calendars = principal.calendars()

# Create event
calendar = calendars[0]
calendar.save_event(ics_content)
```

## Server Compatibility Notes

| Server | CalDAV Support | Notes |
|--------|---------------|-------|
| Nextcloud | Full | caldav v2.2 auto-discovery |
| Google Calendar | Read-only* | No external CalDAV write |
| Outlook/Exchange | Via plugin | CalDAV Synchronizer (Windows) |
| Fastmail | Full | Good CalDAV support |
| iCloud | Full | Requires app-specific password |
| Proton Calendar | None | No API/CalDAV |
| Vikunja | Full | Built-in CalDAV support |

*Google accepts CalDAV reads but doesn't allow external CalDAV writes - use Google Calendar API instead.

## Next Steps (S2)

1. Test caldav with Vikunja's CalDAV endpoint
2. Benchmark icalendar parsing performance
3. Test RRULE expansion for recurring events
4. Evaluate sync latency patterns

---

**Sources:**
- https://pypi.org/project/icalendar/
- https://pypi.org/project/caldav/
- https://pypi.org/project/vobject/
- https://caldav.readthedocs.io
- https://icalendar.readthedocs.io
