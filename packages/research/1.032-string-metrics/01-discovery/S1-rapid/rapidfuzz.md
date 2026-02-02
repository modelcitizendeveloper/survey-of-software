# rapidfuzz (Python)

**GitHub:** ~3.3K stars | **Ecosystem:** Python | **License:** MIT

## Positioning

Fast C++ implementation of 20+ string metrics with Python bindings. Industry standard for production Python applications requiring high-performance fuzzy matching.

## Key Metrics

- **Performance:** 5-50x faster than pure Python implementations (python-Levenshtein, difflib)
- **Download stats:** ~12M downloads/month on PyPI (Jan 2025)
- **Maintenance:** Active development, releases every 1-2 months
- **Python versions:** 3.8+ supported

## Algorithms Included

- Levenshtein distance (edit distance)
- Jaro-Winkler similarity
- Hamming distance
- Indel distance
- Longest Common Subsequence
- Token-based metrics (token_set_ratio, token_sort_ratio)
- Phonetic algorithms (Soundex, Metaphone)

## Community Signals

**Stack Overflow sentiment:**
- "Use rapidfuzz, not fuzzywuzzy - it's the maintained fork with C++ speed"
- "Rapidfuzz for production, textdistance for prototyping"
- "Replaced difflib with rapidfuzz, 10x speedup on fuzzy search"

**Common use cases:**
- Fuzzy name matching in databases
- Duplicate detection in ETL pipelines
- Search autocomplete with typo tolerance
- Record linkage and data deduplication

## Trade-offs

**Strengths:**
- Production-grade performance (C++ core)
- Drop-in replacement for fuzzywuzzy with better speed
- Comprehensive test coverage
- Cross-platform wheels (no compilation needed)

**Limitations:**
- Python-only (bindings available but ecosystem is Python-first)
- Larger binary size due to C++ compiled extensions
- More complex debugging compared to pure Python alternatives

## Decision Context

**Choose rapidfuzz when:**
- Processing >10K string comparisons per second
- Fuzzy matching is in the hot path
- You need multiple algorithms (Levenshtein + Jaro-Winkler + token-based)

**Skip if:**
- Occasional string comparisons (difflib is good enough)
- Need JavaScript/Rust/Go implementation
- Want minimal dependencies (pure Python preferred)
