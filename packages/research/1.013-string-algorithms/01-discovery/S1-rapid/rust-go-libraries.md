# Rust & Go String Algorithm Libraries

## Rust Libraries

### `regex` - Regular Expressions
- **crates.io**: `regex`
- **Purpose**: Fast, safe regex engine
- **Features**: DFA-based (no backtracking), Unicode support, linear time guarantees
- **Performance**: Compiled regex, thread-safe
- **Use case**: Production regex with DoS protection

### `aho-corasick` - Multi-pattern Search
- **crates.io**: `aho-corasick`
- **Purpose**: Fast multi-pattern string searching
- **Performance**: Highly optimized, used by ripgrep
- **Use case**: Content scanning, log analysis, pattern filtering

### `strsim` - String Similarity
- **crates.io**: `strsim`
- **Purpose**: String distance metrics
- **Algorithms**: Hamming, Levenshtein, Jaro, Jaro-Winkler, Damerau-Levenshtein
- **Use case**: Fuzzy matching, spell checking

### `pest` - PEG Parser
- **crates.io**: `pest`
- **Purpose**: Parsing Expression Grammar (PEG) parser
- **Features**: Elegant grammar syntax, compile-time code generation
- **Use case**: Building parsers for DSLs, configuration languages

### `glob` - Glob Pattern Matching
- **crates.io**: `glob`
- **Purpose**: File path glob pattern matching
- **Features**: Standard glob syntax, iterator-based API
- **Use case**: File selection, pattern-based filtering

## Go Libraries

### `regexp` - Regular Expressions
- **Standard library**: `regexp`
- **Purpose**: RE2-based regex engine
- **Features**: Guaranteed linear time, no backtracking
- **Limitation**: Less feature-rich than PCRE/Perl regex
- **Use case**: Safe regex for untrusted input

### `strings` - String Manipulation
- **Standard library**: `strings`
- **Purpose**: Core string operations
- **Features**: Contains, Index, Split, Join, Replace, Trim
- **Performance**: Optimized for common operations
- **Use case**: Basic string processing

### `github.com/lithammer/fuzzysearch` - Fuzzy Search
- **Package**: `fuzzysearch`
- **Purpose**: Fuzzy string searching
- **Algorithm**: Levenshtein-based
- **Use case**: Fuzzy matching, search suggestions

### `github.com/texttheater/golang-levenshtein` - Edit Distance
- **Package**: `levenshtein`
- **Purpose**: Levenshtein distance calculation
- **Options**: Standard and Damerau-Levenshtein variants
- **Use case**: String similarity, spell checking

### `github.com/gobwas/glob` - Glob Matching
- **Package**: `glob`
- **Purpose**: Fast glob pattern matching
- **Performance**: Optimized for performance, minimal allocations
- **Use case**: Path matching, filtering
