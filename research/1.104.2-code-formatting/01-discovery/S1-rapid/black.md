# Black - The Uncompromising Python Code Formatter

**Ecosystem:** Python
**Category:** Code Formatter
**Repository:** https://github.com/psf/black
**PyPI:** https://pypi.org/project/black/

## Popularity Metrics (Dec 2025)

- **GitHub Stars:** 38,000+ (estimated from ecosystem position)
- **Weekly Downloads:** High volume (exact stats not retrieved)
- **Current Version:** 25.1.0
- **Notable Users:** pytest, Django, pandas, SQLAlchemy, Poetry, pytest, tox
- **Organizations:** Dropbox, Mozilla, Quora, Tesla, Lyft

## Key Differentiator

Black is "the uncompromising Python code formatter" - it makes all formatting decisions for you with zero configuration. By ceding control over formatting details, teams gain consistency, speed, and freedom from style debates.

## Features

- Zero configuration by default (opinionated)
- Deterministic formatting (same code = same output)
- Black-compatible format has become an ecosystem standard
- PEP 8 compliant output
- Python 3.13 officially supported (Python 3.8 no longer supported)
- Fast formatting with mypyc-compiled wheels

## Performance

Black is reasonably fast for most projects but not as fast as Rust-based alternatives. Performance is adequate for pre-commit hooks on small-to-medium codebases.

## 2025 Stable Style

The 2025 release introduced the new stable style, stabilizing various formatting changes that had been in preview. Black continues active development with regular releases.

## Quick Verdict

**Status:** Mature, widely adopted standard
**Best for:** Teams wanting zero-configuration consistency and maximum ecosystem compatibility
**Consideration:** Ruff format offers 30x faster formatting with >99.9% Black compatibility

Black remains the gold standard for Python formatting, but Ruff's Black-compatible formatter is becoming the performance-focused alternative. Black's "uncompromising" philosophy has successfully eliminated formatting debates across the Python ecosystem.

**Recommendation:** Safe default choice. Consider Ruff if speed matters or you want unified linting/formatting.
