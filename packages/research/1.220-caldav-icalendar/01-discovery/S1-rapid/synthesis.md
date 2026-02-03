# 1.220 CalDAV/iCalendar Libraries - S1 Synthesis

**Date**: December 19, 2025

## Summary

Three Python libraries cover calendar file formats and protocols.

| Library | Purpose | Downloads/mo | Status |
|---------|---------|--------------|--------|
| icalendar | RFC 5545 parsing/generation | 4.7M | Active, recommended |
| caldav | RFC 4791 CalDAV client | 107K | Active, v2.2 Dec 2025 |
| vobject | iCal + vCard parsing | 783K | Legacy, maintained |

## When to Use What

**icalendar** - Default choice for iCalendar work
- Parse/generate ICS files
- Recurring events (RRULE)
- Highest adoption, best maintained

**caldav** - When syncing with CalDAV servers
- Depends on icalendar internally
- v2.2 adds RFC 6764 auto-discovery
- Works with Nextcloud, Radicale, Fastmail, iCloud

**vobject** - Only if vCard needed
- Lower adoption
- Less active
- Main differentiator: vCard support

## Server Compatibility (caldav)

| Server | CalDAV Support |
|--------|---------------|
| Nextcloud | Full |
| Radicale | Full |
| Fastmail | Full |
| iCloud | Full (app-specific password) |
| Vikunja | Full |
| Google Calendar | Read-only (no external writes) |
| Proton Calendar | None |

## Key RFCs

- RFC 5545: iCalendar format (icalendar)
- RFC 4791: CalDAV protocol (caldav)
- RFC 6764: CalDAV auto-discovery (caldav v2.2+)
- RFC 6638: CalDAV scheduling (caldav, in progress)

## See Also

- [icalendar.md](icalendar.md) - Library profile
- [caldav.md](caldav.md) - Library profile
- [vobject.md](vobject.md) - Library profile
