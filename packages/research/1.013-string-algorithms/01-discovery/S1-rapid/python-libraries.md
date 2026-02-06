# Python String Algorithm Libraries

## Built-in: `re` (Regular Expressions)
- **Standard library**: Ships with Python
- **Capabilities**: Regex pattern matching, search, replace, split
- **Performance**: C-implemented, adequate for most use cases
- **Limitations**: Backtracking engine, not suitable for untrusted input

## `regex` - Enhanced Regular Expressions
- **PyPI**: `regex`
- **Purpose**: Drop-in replacement for `re` with additional features
- **Features**: Unicode support, fuzzy matching, variable-length lookbehinds
- **Performance**: Similar to `re`, optimized for complex patterns
- **Use case**: When `re` is insufficient (e.g., fuzzy matching, Unicode categories)

## `fuzzywuzzy` / `thefuzz` - Fuzzy String Matching
- **PyPI**: `thefuzz` (maintained fork of `fuzzywuzzy`)
- **Purpose**: String similarity and fuzzy matching
- **Algorithm**: Levenshtein distance via `python-Levenshtein`
- **Features**: Ratio, partial ratio, token sort/set ratios
- **Use case**: Name matching, deduplication, search ranking

## `python-Levenshtein` - Edit Distance
- **PyPI**: `python-Levenshtein`
- **Purpose**: Fast C implementation of edit distance algorithms
- **Algorithms**: Levenshtein, Jaro-Winkler, Hamming distance
- **Performance**: Highly optimized, 10-100x faster than pure Python
- **Use case**: Low-level string similarity computations

## `jellyfish` - Phonetic & String Comparison
- **PyPI**: `jellyfish`
- **Purpose**: Phonetic encoding and string comparison
- **Features**: Soundex, Metaphone, NYSIIS, Jaro distance
- **Use case**: Name matching with phonetic similarity

## `aho-corasick` - Multi-pattern Search
- **PyPI**: `pyahocorasick`
- **Purpose**: Efficient multi-pattern string searching
- **Algorithm**: Aho-Corasick automaton
- **Performance**: O(n+m) where n=text length, m=pattern length
- **Use case**: Searching for many patterns simultaneously (e.g., content filtering)
