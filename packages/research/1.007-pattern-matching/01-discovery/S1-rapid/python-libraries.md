# Python Pattern Matching Libraries

## Built-in Functions

### str.find() / str.index()
- **Maturity**: Python standard library (universal)
- **Performance**: ~500 MB/s to 2 GB/s (CPython uses optimized C)
- **Algorithms**: Boyer-Moore-Horspool variant in CPython
- **Ease**: Trivial (one method call)
- **Best for**: Single-pattern search in pure Python

### re module (Regex)
- **Maturity**: Python standard library
- **Performance**: ~50-200 MB/s (slower than pure string matching)
- **Algorithms**: Backtracking NFA for regex
- **Ease**: Simple API, powerful patterns
- **Best for**: Pattern matching with wildcards/structure
- **Warning**: Can have catastrophic backtracking on complex patterns

## pyahocorasick

- **Maturity**: 936 GitHub stars, actively maintained
- **Performance**: ~500 MB/s to 2 GB/s (C extension)
- **Algorithms**: Aho-Corasick automaton
- **Ease**: Simple API, Pythonic
- **Best for**: Multi-pattern matching (100+ patterns)
- **Production use**: Log analysis, security scanning

## regex (PyPI package)

- **Maturity**: 363 stars, alternative to stdlib re
- **Performance**: Similar to stdlib re
- **Algorithms**: Enhanced regex with more features
- **Ease**: Drop-in replacement for re
- **Best for**: Advanced regex features (fuzzy matching, Unicode)

## pyre2 (RE2 Python bindings)

- **Maturity**: Google RE2 with Python bindings
- **Performance**: ~100-500 MB/s
- **Algorithms**: Linear-time regex (DFA-based)
- **Ease**: Similar to re module
- **Best for**: Regex with guaranteed performance (no catastrophic backtracking)

## flashtext

- **Maturity**: 5.6K GitHub stars
- **Performance**: Claims 10-100x faster than regex for keyword matching
- **Algorithms**: Aho-Corasick variant (Trie-based)
- **Ease**: Very simple API
- **Best for**: Large-scale keyword replacement (NLP preprocessing)
- **Note**: Optimized for exact word matching, not general substrings

## mrab-regex

- **Maturity**: Part of regex package
- **Performance**: Comparable to stdlib re
- **Algorithms**: Enhanced backtracking with optimizations
- **Ease**: Extended re syntax
- **Best for**: Complex regex patterns requiring features not in stdlib
