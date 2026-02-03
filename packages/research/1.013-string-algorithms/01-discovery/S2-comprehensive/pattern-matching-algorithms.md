# Pattern Matching Algorithms - Deep Dive

## Single Pattern Search

### Naive Algorithm
- **Time**: O(n·m) where n=text length, m=pattern length
- **Space**: O(1)
- **Best for**: Very short patterns, simple implementations
- **Limitation**: Worst case on repetitive text/patterns

### Knuth-Morris-Pratt (KMP)
- **Time**: O(n+m) preprocessing + search
- **Space**: O(m) for failure function table
- **Key insight**: Avoid re-examining text characters by pre-computing pattern overlaps
- **Best for**: Streaming text, single-pass requirements
- **Implementation**: Python `str.find()` uses variant for large patterns

### Boyer-Moore
- **Time**: O(n/m) best case, O(n·m) worst case
- **Space**: O(m + σ) where σ=alphabet size
- **Key insight**: Search from right-to-left, skip ahead on mismatches
- **Best for**: Large alphabets (English text), longer patterns
- **Real-world**: Grep, text editors use BM variants

### Rabin-Karp
- **Time**: O(n+m) average, O(n·m) worst case with collisions
- **Space**: O(1)
- **Key insight**: Rolling hash for constant-time comparison
- **Best for**: Multiple pattern search, plagiarism detection
- **Caution**: Hash collision handling critical for correctness

## Multi-Pattern Search

### Aho-Corasick
- **Time**: O(n + m + z) where z=number of matches
- **Space**: O(m·σ) for automaton
- **Key insight**: Finite automaton with failure links
- **Best for**: Large pattern sets (thousands), content filtering
- **Real-world**: Antivirus scanning, log analysis, search engines

### Suffix Trees/Arrays
- **Time**: O(n) build, O(m) search per pattern
- **Space**: O(n) for text
- **Key insight**: All suffixes in trie structure
- **Best for**: Many searches on same text, substring problems
- **Limitation**: High memory overhead, complex construction

### Tries (Prefix Trees)
- **Time**: O(m) per pattern operation
- **Space**: O(total pattern length)
- **Key insight**: Shared prefixes save space and time
- **Best for**: Autocomplete, dictionary lookups, IP routing
- **Variants**: Compressed tries (Patricia trees), double-array tries

## Approximate Matching (Fuzzy Search)

### Levenshtein Distance (Edit Distance)
- **Time**: O(n·m) dynamic programming
- **Space**: O(min(n,m)) with optimization
- **Operations**: Insert, delete, substitute (all cost 1)
- **Best for**: Spell checking, fuzzy search
- **Variants**: Damerau-Levenshtein (adds transposition)

### Bitap Algorithm
- **Time**: O(n) with pattern-dependent constant
- **Space**: O(σ) for bit masks
- **Key insight**: Bit-parallel simulation of NFA
- **Best for**: Short patterns (≤ word size), k-mismatch search
- **Real-world**: Used by fuse.js, agrep

### Jaro-Winkler Distance
- **Time**: O(n·m) worst case, often faster in practice
- **Application**: Name matching, record linkage
- **Key insight**: Weights matching prefix higher
- **Best for**: Short strings with typos at end (names, addresses)

## Regular Expression Engines

### Backtracking NFA
- **Examples**: Python `re`, Java `java.util.regex`, PCRE
- **Time**: Exponential worst case O(2^n)
- **Features**: Backreferences, lookahead, full Perl features
- **Risk**: ReDoS (Regular Expression Denial of Service)
- **Best for**: Trusted input, complex patterns

### DFA-based (Linear Time)
- **Examples**: Rust `regex`, Go `regexp` (RE2), Russ Cox's RE2
- **Time**: O(n) guaranteed
- **Features**: No backreferences, limited lookahead
- **Safety**: DoS-resistant
- **Best for**: Untrusted input, high-throughput systems

### Hybrid Approaches
- **Examples**: Hyperscan, Vectorscan
- **Technique**: SIMD-accelerated multi-pattern matching
- **Performance**: Gigabits/second throughput
- **Best for**: Network intrusion detection, packet inspection

## Performance Comparison

| Algorithm | Best Case | Avg Case | Worst Case | Space | Use Case |
|-----------|-----------|----------|------------|-------|----------|
| Naive | O(n) | O(n·m) | O(n·m) | O(1) | Education |
| KMP | O(n) | O(n) | O(n) | O(m) | Streaming |
| Boyer-Moore | O(n/m) | O(n) | O(n·m) | O(m+σ) | Large alphabet |
| Rabin-Karp | O(n) | O(n+m) | O(n·m) | O(1) | Multi-pattern |
| Aho-Corasick | O(n+m+z) | O(n+m+z) | O(n+m+z) | O(m·σ) | Many patterns |
| Levenshtein | O(n·m) | O(n·m) | O(n·m) | O(n·m) | Fuzzy match |

## Choosing the Right Algorithm

**Single exact match on large text**: Boyer-Moore or built-in string search

**Multiple patterns**: Aho-Corasick for static patterns, trie for dynamic

**Fuzzy matching**: Levenshtein for accuracy, Bitap for speed on short patterns

**Regex with untrusted input**: RE2/Rust regex for safety

**Regex with complex features**: PCRE/Python re with timeout limits

**Maximum performance**: SIMD-accelerated engines (Hyperscan) for specialized use
