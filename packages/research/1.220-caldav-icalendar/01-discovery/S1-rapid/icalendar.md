# icalendar

**Package:** [icalendar](https://pypi.org/project/icalendar/)
**GitHub:** [collective/icalendar](https://github.com/collective/icalendar)
**Docs:** https://icalendar.readthedocs.io

## Overview

iCalendar parser/generator for Python. Full RFC 5545 (iCalendar) support.

## Stats

| Metric | Value |
|--------|-------|
| Monthly Downloads | 4.7M |
| Latest Version | 6.3.2 |
| Python Support | 3.8-3.13, PyPy3 |
| License | BSD |

## Dependencies

- python-dateutil
- tzdata
- backports-zoneinfo (Python < 3.9)

## Features

- Parse ICS files/strings
- Generate iCalendar output
- Event, Todo, Journal, FreeBusy, Alarm components
- Recurring events (RRULE via dateutil)
- Timezone support (zoneinfo, pytz, dateutil.tz)

## Example

```python
from icalendar import Calendar, Event
from datetime import datetime

# Create
cal = Calendar()
event = Event()
event.add('summary', 'Meeting')
event.add('dtstart', datetime(2025, 12, 20, 14, 0))
event.add('dtend', datetime(2025, 12, 20, 15, 0))
cal.add_component(event)
ics = cal.to_ical()

# Parse
cal = Calendar.from_ical(ics_string)
for event in cal.walk('VEVENT'):
    print(event.get('summary'))
```

## Notes

- De facto standard for Python iCalendar work
- Very active maintenance
- caldav library depends on this internally
