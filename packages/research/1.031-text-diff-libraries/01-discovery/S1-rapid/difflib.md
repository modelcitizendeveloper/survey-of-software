# difflib

## Overview
- **Package**: Python standard library (built-in, no installation needed)
- **Status**: Active (maintained with Python releases)
- **Popularity**: Universal (ships with Python, no download metrics)
- **First choice**: Yes, try this first for basic needs

## Algorithm
- **Core**: SequenceMatcher using Ratcliff/Obershelp pattern recognition
- **Similarity**: Similar to Myers diff but not identical (different heuristics)
- **Complexity**: O(n*m) worst case, typically much faster with optimizations
- **Not optimal**: Doesn't guarantee minimal edit distance

## Best For
- **Quick prototyping**: Already installed, no dependencies
- **Basic diffing**: Text files, simple comparisons
- **Testing**: Comparing expected vs actual outputs in unit tests
- **HTML output**: Built-in side-by-side HTML diff viewer
- **Learning**: Simple API, good for understanding diff concepts

## Trade-offs

**Strengths:**
- Zero dependencies (stdlib)
- Cross-platform (wherever Python runs)
- Simple API for common cases
- HTML diff output built-in
- Fuzzy matching with `get_close_matches()`

**Limitations:**
- No patience or histogram diff (inferior for code with moved blocks)
- Pure Python (slower than C-extension libraries)
- Struggles with large files (>1MB)
- No patch application (can generate diff, can't apply it)
- No three-way merge support

## Ecosystem Fit
- **Dependencies**: None (stdlib)
- **Platform**: All (Windows, macOS, Linux)
- **Python**: 2.7+ and 3.x
- **Maintenance**: Stable, evolves with Python
- **Risk**: Very low (won't disappear)

## Quick Verdict
**Start here unless you have specific needs.** If difflib is too slow, lacks features you need, or produces poor diffs for your use case, then consider alternatives. For 80% of cases, this is sufficient.
