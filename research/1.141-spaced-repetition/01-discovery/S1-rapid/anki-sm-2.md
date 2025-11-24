# Anki SM-2 (Anki's SM-2 Variant)

**PyPI Package**: `anki-sm-2`
**GitHub**: open-spaced-repetition/anki-sm-2
**Algorithm**: Anki's SM-2 variant (pre-2023)

## Popularity Metrics

- **Downloads**: 156/month (PyPI)
- **GitHub Stars**: (part of open-spaced-repetition org)
- **Maintenance**: Active (released October 2024)
- **Latest Release**: v0.2.0 (October 31, 2024)
- **Python Requirement**: >=3.10
- **License**: GNU AGPL v3

## Quick Assessment

**Pros**:
- ✅ **Anki-compatible** (matches Anki's original algorithm)
- ✅ **Recent release** (October 2024)
- ✅ **Open Spaced Repetition org** (same maintainers as FSRS)
- ✅ **Clean implementation** (Scheduler + Card + ReviewLog objects)

**Cons**:
- ⚠️ **Lowest popularity** (47× fewer downloads than FSRS)
- ⚠️ **Legacy algorithm** (Anki moved to FSRS as default in v23.10)
- ⚠️ **AGPL license** (more restrictive than MIT)
- ⚠️ **Unclear positioning** (why not use FSRS from same org?)

## Installation

```bash
pip install anki-sm-2
```

## Basic Usage Pattern

```python
from anki_sm_2 import Scheduler, Card, Rating

# Initialize scheduler
scheduler = Scheduler()

# Create card
card = Card()

# Review card
scheduling_cards = scheduler.review_card(card, Rating.Good)
card = scheduling_cards[Rating.Good].card
```

## Confidence for Personal Language Learning

**LOW** - Same organization now recommends FSRS (their newer, better algorithm).

## Notes

Maintained by same organization that created FSRS. The fact they built FSRS suggests SM-2 is being phased out. Anki itself moved to FSRS as default in 2023.

## Sources
- [anki-sm-2 PyPI](https://pypi.org/project/anki-sm-2/)
- [anki-sm-2 GitHub](https://github.com/open-spaced-repetition/anki-sm-2)
- [Anki FAQs - What Algorithm](https://faqs.ankiweb.net/what-spaced-repetition-algorithm.html)
