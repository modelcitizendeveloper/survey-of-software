# SuperMemo2 (SM-2 Algorithm)

**PyPI Package**: `supermemo2`
**GitHub**: alankan886/SuperMemo2
**Algorithm**: SM-2 (1987, classic)

## Popularity Metrics

- **Downloads**: 361/month (PyPI)
- **GitHub Stars**: 120
- **Maintenance**: Stable (last commit June 2024, 64 total commits)
- **Latest Release**: v3.0.1 (June 2024)
- **Python Requirement**: Not specified (likely 3.x)

## Quick Assessment

**Pros**:
- ✅ **Simple algorithm** (E-Factor, interval, repetition count)
- ✅ **Battle-tested** (used since 1987, proven effective)
- ✅ **Easy to understand** (5 quality ratings, simple math)
- ✅ **Lightweight** (minimal dependencies: attrs)
- ✅ **Clean API** (rewritten v3.0 removed class complexity)

**Cons**:
- ⚠️ **Lower popularity** (20× fewer downloads than FSRS)
- ⚠️ **Less active maintenance** (6 months since last update)
- ⚠️ **Older algorithm** (37 years old, surpassed by modern research)
- ⚠️ **Smaller community** (fewer resources, examples)

## Installation

```bash
pip install supermemo2
```

## Basic Usage Pattern

```python
from supermemo2 import SMTwo

# Initialize with quality rating (0-5)
review = SMTwo.first_review(4)  # quality = 4

# Next review
review = SMTwo(review.easiness, review.interval, review.repetitions).review(4)
```

## Confidence for Personal Language Learning

**MEDIUM** - Works but lower popularity suggests FSRS is preferred by community.

## Sources
- [supermemo2 PyPI](https://pypi.org/project/supermemo2/)
- [SuperMemo2 GitHub](https://github.com/alankan886/SuperMemo2)
