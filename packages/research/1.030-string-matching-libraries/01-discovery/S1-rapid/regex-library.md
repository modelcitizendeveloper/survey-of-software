# regex (Enhanced Regex Library)

**Repository:** github.com/mrabarnett/mrab-regex
**Downloads/Month:** 159,745,909 (PyPI)
**Downloads/Week:** 29,874,675
**Downloads/Day:** 4,607,279
**Latest Release:** January 14, 2026
**License:** Apache 2.0

## Quick Assessment

- **Popularity:** Very High (160M+ monthly downloads)
- **Maintenance:** Active (January 2026 release)
- **Documentation:** Good (PyPI and GitHub docs)
- **Production Adoption:** Very High (de facto re module replacement)

## Pros

- **Drop-in replacement**: Backwards-compatible with standard re module
- **Enhanced features**: Named lists, set operations, possessive quantifiers
- **Unicode support**: Full Unicode 17.0.0 support
- **GIL release**: Threads can run concurrently during matching
- **Mature**: Proven in production at scale (160M monthly downloads)
- **More powerful**: Supports features not in standard re module

## Cons

- **Extra dependency**: Not in standard library (requires installation)
- **Slightly different**: Some edge cases behave differently than re
- **Learning curve**: Additional features require learning new syntax
- **Performance trade-off**: Sometimes slightly slower than re for simple patterns

## Quick Take

regex is the enhanced version of Python's re module. Install it when you need advanced regex features (named lists, better Unicode, set operations) or when re module's limitations frustrate you. Backed by 160M monthly downloads proving production readiness. Best choice when you've outgrown standard re but don't need RE2's linear-time guarantees.

## Data Sources

- [regex · PyPI](https://pypi.org/project/regex/)
- [PyPI Download Stats](https://pypistats.org/packages/regex)
- [GitHub - mrabarnett/mrab-regex](https://github.com/mrabarnett/mrab-regex)
