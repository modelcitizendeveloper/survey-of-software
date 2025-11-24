# FSRS (Free Spaced Repetition Scheduler)

**PyPI Package**: `fsrs`
**GitHub**: open-spaced-repetition/py-fsrs
**Algorithm**: FSRS (2022, modern open-source)

## Popularity Metrics

- **Downloads**: 7,324/month (PyPI)
- **GitHub Stars**: 355
- **Maintenance**: Active (118 commits, automated testing)
- **Latest Release**: v6.3.0 (October 2025)
- **Python Requirement**: >=3.10

## Quick Assessment

**Pros**:
- ✅ **Most popular** by far (20× more downloads than alternatives)
- ✅ **Active maintenance** (regular releases through 2025)
- ✅ **Modern algorithm** (based on academic research, 2022)
- ✅ **Backed by Open Spaced Repetition community**
- ✅ **Adopted by Anki** (as of Anki 23.10, FSRS is official option)
- ✅ **Well-documented** with optimizer for parameters
- ✅ **Evidence-based** (DSR model: difficulty, stability, retrievability)

**Cons**:
- ⚠️ More complex (21 model weight parameters)
- ⚠️ Requires Python 3.10+ (not 3.9)
- ⚠️ Newer algorithm (less battle-tested than SM-2)

## Installation

```bash
pip install fsrs
```

## Basic Usage Pattern

```python
from fsrs import FSRS, Card, Rating

# Initialize scheduler
f = FSRS()

# Create new card
card = Card()

# Schedule first review
scheduling_cards = f.repeat(card, now)

# User rates card (Again, Hard, Good, Easy)
card = scheduling_cards[Rating.Good].card
```

## Confidence for Personal Language Learning

**HIGH** - Clear popularity leader, active maintenance, modern algorithm with academic backing.

## Sources
- [FSRS PyPI](https://pypi.org/project/fsrs/)
- [py-fsrs GitHub](https://github.com/open-spaced-repetition/py-fsrs)
- [Open Spaced Repetition](https://github.com/open-spaced-repetition)
