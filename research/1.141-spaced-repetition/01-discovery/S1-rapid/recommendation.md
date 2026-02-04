# S1 Rapid Discovery - Recommendation

**Time Spent**: ~70 minutes
**Confidence Level**: HIGH

## Clear Winner: FSRS (Free Spaced Repetition Scheduler)

**Package**: `fsrs` on PyPI
**Install**: `pip install fsrs`

## Why FSRS?

### Overwhelming Popularity Signal
- **7,324 downloads/month** vs 361 (supermemo2) vs 156 (anki-sm-2)
- **20-47× more popular** than alternatives
- **355 GitHub stars** (largest community)

### Active Maintenance
- Latest release: v6.3.0 (October 2025)
- 118 commits, automated testing
- Regular updates through 2025

### Modern, Evidence-Based Algorithm
- Based on DSR model (Difficulty, Stability, Retrievability)
- Published 2022 with academic backing
- **Adopted by Anki as official algorithm** (v23.10+)

### Strong Ecosystem
- Maintained by Open Spaced Repetition organization
- Same org that maintains anki-sm-2 (they built FSRS to replace SM-2)
- Well-documented with optimizer for parameters

## When to Consider Alternatives

### Use **supermemo2** if:
- ❌ You need Python <3.10 support (FSRS requires 3.10+)
- ❌ You want absolute simplicity (SM-2 is simpler to understand)
- ❌ You're implementing for historical/research purposes

**Verdict**: Not recommended. Lower popularity + older algorithm.

### Use **anki-sm-2** if:
- ❌ You need exact Anki pre-2023 compatibility
- ❌ You're maintaining legacy Anki integration

**Verdict**: Not recommended. Same org now recommends FSRS.

## Default Recommendation for 90% of Learners

**Use FSRS.**

- Popularity signal is decisive (47× more than next option)
- Anki's official adoption validates effectiveness
- Active maintenance ensures long-term viability
- Modern algorithm with research backing

## Implementation Path

```python
# Install
pip install fsrs

# Basic usage
from fsrs import FSRS, Card, Rating

f = FSRS()
card = Card()
scheduling_cards = f.repeat(card, now)

# After review
card = scheduling_cards[Rating.Good].card
```

## Confidence Assessment

**HIGH (9/10)** - Multiple strong signals converge:
- ✅ Popularity (20-47× leader)
- ✅ Anki adoption (industry validation)
- ✅ Active maintenance (2025 releases)
- ✅ Modern algorithm (research-backed)
- ✅ Community support (Open Spaced Repetition org)

Only risk: FSRS is newer (2022) vs SM-2 (1987), but Anki's adoption mitigates this.

## Sources

- [FSRS PyPI Stats](https://pypistats.org/packages/fsrs) - 7,324 downloads/month
- [py-fsrs GitHub](https://github.com/open-spaced-repetition/py-fsrs) - 355 stars
- [supermemo2 PyPI](https://pypi.org/project/supermemo2/) - 361 downloads/month
- [SuperMemo2 GitHub](https://github.com/alankan886/SuperMemo2) - 120 stars
- [anki-sm-2 PyPI](https://pypi.org/project/anki-sm-2/) - 156 downloads/month
- [Anki Algorithm FAQs](https://faqs.ankiweb.net/what-spaced-repetition-algorithm.html) - Official Anki docs confirming FSRS adoption
- [Open Spaced Repetition](https://github.com/open-spaced-repetition) - Maintainer organization
