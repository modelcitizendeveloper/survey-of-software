# vobject

**Package:** [vobject](https://pypi.org/project/vobject/)
**GitHub:** [py-vobject/vobject](https://github.com/py-vobject/vobject)
**Docs:** https://vobject.readthedocs.io

## Overview

Full-featured Python package for parsing and creating iCalendar and vCard files. Originally developed for the Chandler project.

## Stats

| Metric | Value |
|--------|-------|
| Monthly Downloads | 783K |
| Latest Version | 1.x |
| Python Support | 3.8+ (v1.x), 2.7 (v0.9.x) |
| License | Apache-2.0 |

## Dependencies

- python-dateutil
- pytz
- six

## Features

- iCalendar parsing/generation
- vCard 3.0 parsing/generation
- VAVAILABILITY support
- Command line tools: `ics_diff`, `change_tz`

## Example

```python
import vobject

# Create
cal = vobject.iCalendar()
event = cal.add('vevent')
event.add('summary').value = 'Meeting'
event.add('dtstart').value = datetime(2025, 12, 20, 14, 0)
ics = cal.serialize()

# Parse
cal = vobject.readOne(ics_string)
for event in cal.vevent_list:
    print(event.summary.value)
```

## Notes

- Legacy library - predates icalendar
- Main advantage: vCard support
- Lower adoption than icalendar (783K vs 4.7M)
- Less active maintenance
- Use if you need vCard, otherwise prefer icalendar
