# Pattern Matching Algorithms: Domain Explainer

## What is Pattern Matching?

**Pattern matching** is the task of finding occurrences of a pattern (substring) within a larger text. It's one of the most fundamental operations in computer science, powering everything from text editors (Ctrl+F) to bioinformatics (DNA sequence analysis) to intrusion detection systems.

### The Core Problem

**Given**:
- Text: A long string to search within (length n)
- Pattern: A shorter string to find (length m)

**Find**: All positions where the pattern occurs in the text

**Example**:
```
Text:    "AABAACAADAABAABA"
Pattern: "AABA"
Matches at positions: 0, 9, 12
```

## Why Pattern Matching Matters

Pattern matching is ubiquitous in software systems:

- **Text editors**: Find/replace operations (VS Code, Sublime, vim)
- **Search engines**: Query matching in documents
- **Bioinformatics**: DNA/protein sequence alignment
- **Network security**: Intrusion detection (Snort uses Aho-Corasick)
- **Compilers**: Lexical analysis and tokenization
- **Data processing**: Log analysis, ETL pipelines

The difference between a naive O(nm) algorithm and an optimized O(n+m) algorithm can mean:
- Searching a 1GB file in 1 second vs 17 minutes
- Real-time virus scanning vs system slowdown
- Practical genome analysis vs computationally infeasible

## Core Concepts

### 1. Naive vs Optimized Algorithms

**Naive approach** (brute force):
```
For each position i in text:
    Check if pattern matches starting at position i
```
- Time: O(nm) - checks every position, compares up to m characters
- Space: O(1)
- Used in: Simple implementations when patterns are very short

**Optimized approaches**:
All modern algorithms avoid redundant comparisons by using one of three strategies:
1. **Preprocessing the pattern** (KMP, Boyer-Moore, Rabin-Karp)
2. **Preprocessing the text** (suffix trees, suffix arrays)
3. **Parallel matching** (Aho-Corasick for multiple patterns)

### 2. Key Performance Dimensions

**Time complexity**:
- Preprocessing: One-time cost to analyze pattern(s)
- Matching: Cost to scan through text
- Best case, average case, worst case can differ dramatically

**Space complexity**:
- Pattern table size (e.g., KMP: O(m), Boyer-Moore: O(m + σ) where σ = alphabet size)
- Affects cache performance and memory usage

**Practical performance factors**:
- Alphabet size (2 for binary, 4 for DNA, 26 for English, 256 for bytes, 65536 for Unicode)
- Pattern characteristics (repeated substrings, unique characters)
- Text characteristics (random vs structured, matches common vs rare)
- Cache locality and branch prediction

### 3. Single-Pattern vs Multi-Pattern

**Single-pattern algorithms** (KMP, Boyer-Moore, Rabin-Karp):
- Optimized to find one pattern in text
- Must run multiple times for multiple patterns
- Time: O(k × (n + m)) for k patterns (Boyer-Moore can be faster in practice)

**Multi-pattern algorithms** (Aho-Corasick, Commentz-Walter):
- Build combined structure for all patterns
- Scan text once to find all patterns
- Time: O(n + m + z) where m = total pattern length, z = output size
- Critical for: Virus scanners, network IDS, URL blacklists

### 4. Preprocessing vs Streaming

**Preprocessing-based** (most algorithms):
- Require full pattern(s) upfront
- Build lookup tables or automata
- Excellent when pattern is reused (e.g., virus signatures)

**Streaming/online** (naive, some Rabin-Karp variants):
- Can start matching immediately
- Lower overhead for one-time searches
- Better for dynamic patterns

## Core Algorithms

### 1. Knuth-Morris-Pratt (KMP)

**Key insight**: When a mismatch occurs, use information from matched characters to skip positions.

**How it works**:
- Builds a "failure function" table from the pattern
- On mismatch, table tells you how far you can shift the pattern
- Never backtracks in the text (each character examined once)

**Characteristics**:
- Time: O(n + m) guaranteed (optimal)
- Space: O(m) for failure function
- Best for: Theoretical guarantees, worst-case predictability

**Real-world use**: Educational (teaches string algorithm concepts), systems requiring worst-case guarantees

**Example**: Pattern "ABABAC"
```
Failure function: [0, 0, 1, 2, 3, 0]
Meaning: On mismatch at position i, the first f[i] characters already match
```

### 2. Boyer-Moore

**Key insight**: Scan pattern right-to-left; on mismatch, skip multiple positions based on mismatched character.

**How it works**:
- Two heuristics: bad character rule + good suffix rule
- Bad character: If text character not in pattern, skip entire pattern length
- Good suffix: If suffix of pattern matches, shift to align with another occurrence

**Characteristics**:
- Time: O(nm) worst case, but O(n/m) best case (sublinear!)
- Space: O(m + σ) for lookup tables
- Best for: Large alphabets, patterns with unique characters

**Real-world use**: grep, text editors, most practical search tools

**Why it's fast**: For English text, often examines <n/m characters (e.g., searching 1000-char text for 10-char pattern might check only 100 characters)

**Example**: Pattern "EXAMPLE", text contains 'Z'
```
Pattern: EXAMPLE
Text:    ...Z...
         ↑
Skip 7 positions (pattern length) because Z not in pattern
```

### 3. Aho-Corasick

**Key insight**: Build a trie (prefix tree) of all patterns + failure links to efficiently match multiple patterns in one pass.

**How it works**:
- Builds a finite automaton (trie + KMP-style failure links)
- Processes text character by character
- At each state, can match multiple patterns simultaneously

**Characteristics**:
- Time: O(n + m + z) where z = output size (number of matches)
- Space: O(m × σ) in worst case (trie nodes × alphabet size)
- Best for: Multiple patterns (10s to millions), streaming text

**Real-world use**:
- Snort IDS (network intrusion detection)
- ClamAV (antivirus scanner)
- AWS WAF (web application firewall)
- Elasticsearch (multi-pattern search)

**Example**: Patterns ["he", "she", "his", "hers"]
```
Trie with failure links allows finding all 4 patterns in "ushers" in one pass:
- Matches "she" at position 1
- Matches "he" at position 2
- Matches "hers" at position 3
```

### 4. Rabin-Karp

**Key insight**: Use rolling hash to compare pattern with text substrings in O(1).

**How it works**:
- Compute hash of pattern
- Compute hash of first text window
- Roll hash through text (remove left char, add right char)
- On hash match, verify with actual string comparison (handles collisions)

**Characteristics**:
- Time: O(n + m) average, O(nm) worst case (many hash collisions)
- Space: O(1)
- Best for: Multiple pattern search (hash all patterns), substring search with wildcards

**Real-world use**: Plagiarism detection, duplicate file detection (rsync uses related ideas)

**Example**: Pattern "ABC" with simple hash (sum of ASCII values)
```
Hash("ABC") = 65 + 66 + 67 = 198
Hash("XYZ") = 88 + 89 + 90 = 267  → No match, no comparison needed
Hash("CAB") = 67 + 65 + 66 = 198  → Hash matches, compare strings → Not equal
```

**Rolling hash**: Hash("ABC") → Hash("BCD") by subtracting 'A', adding 'D'

## Algorithm Comparison

### Performance Characteristics

| Algorithm | Preprocessing | Matching (avg) | Matching (worst) | Space | Best For |
|-----------|---------------|----------------|------------------|-------|----------|
| Naive | O(1) | O(nm) | O(nm) | O(1) | Very short patterns |
| KMP | O(m) | O(n) | O(n) | O(m) | Worst-case guarantees |
| Boyer-Moore | O(m + σ) | O(n/m) | O(nm) | O(m + σ) | Large alphabets, practical search |
| Aho-Corasick | O(Σm) | O(n + z) | O(n + z) | O(Σm × σ) | Multiple patterns |
| Rabin-Karp | O(m) | O(n + m) | O(nm) | O(1) | Multiple patterns, simple impl |

Where:
- n = text length
- m = pattern length (or total pattern length for multiple patterns)
- σ = alphabet size
- z = number of matches

### Practical Performance (English Text)

**Scenario 1**: Find "pattern" in 1MB file
- Naive: ~17 minutes (examines every position)
- KMP: ~1 second (linear scan, no backtracking)
- Boyer-Moore: ~0.3 seconds (sublinear, skips characters)

**Scenario 2**: Find any of 10,000 virus signatures in 100MB memory dump
- Run Boyer-Moore 10k times: ~50 minutes
- Aho-Corasick (one pass): ~30 seconds

**Scenario 3**: Find "AAAAAAAAB" in "AAAAAAA...AAA" (worst case for Boyer-Moore)
- Boyer-Moore: Degrades to O(nm)
- KMP: Still O(n) - consistent performance

## Trade-offs

### The Performance Triangle

You typically optimize for two of:
1. **Preprocessing speed**: How fast to build structures
2. **Matching speed**: How fast to scan text
3. **Memory usage**: How much space for tables

**Examples**:
- **KMP**: Fast preprocessing, fast matching, low memory ✓✓✓
- **Boyer-Moore**: Moderate preprocessing, very fast matching (avg), low memory ✓✓✓
- **Aho-Corasick**: Slow preprocessing (many patterns), fast matching, high memory ✓✓×
- **Naive**: Instant preprocessing, slow matching, no memory ✓×✓

### Alphabet Size Impact

**Small alphabet** (DNA: A, C, G, T):
- Boyer-Moore bad-character rule less effective (fewer unique characters to skip on)
- KMP often competitive or better
- Specialized algorithms (e.g., agrep with bitwise parallelism) can outperform

**Large alphabet** (Unicode, binary data):
- Boyer-Moore shines (many unique characters → large skips)
- Aho-Corasick trie becomes sparse (memory inefficient)
- Hash-based methods (Rabin-Karp) avoid alphabet-dependent tables

### Pattern Characteristics

**Patterns with repetition** ("AAAAB", "abcabc"):
- Naive and Boyer-Moore can be slow (many partial matches)
- KMP designed exactly for this (failure function handles repetition)

**Patterns with unique characters** ("WXYZ"):
- Boyer-Moore excels (large skips on mismatch)
- KMP has no advantage (failure function trivial)

**Many short patterns**:
- Aho-Corasick ideal (shared prefixes in trie)
- Running BM repeatedly can be faster if patterns share few prefixes

**Few long patterns**:
- Boyer-Moore or KMP each pattern
- Aho-Corasick overhead may not be worth it

## Common Use Cases

### 1. Text Editors (Find/Replace)

**Requirements**:
- Interactive (low latency for small files)
- Incremental (pattern changes frequently)
- Typically case-insensitive, regex support

**Algorithm choice**: Naive or optimized regex engine
- Files usually small enough that O(nm) is fine
- Pattern changes every keystroke (preprocessing overhead not amortized)
- Boyer-Moore used in some editors for large files

**Examples**: VS Code uses Rust regex crate (hybrid approach), Sublime Text uses custom optimized search

### 2. Virus/Malware Scanning

**Requirements**:
- Thousands to millions of signatures
- Scan files/memory once
- Need all matches (not just first)

**Algorithm choice**: Aho-Corasick or variants
- ClamAV: Uses Aho-Corasick with optimizations
- Snort: Aho-Corasick for signature matching
- Modern tools: GPU-accelerated parallel matching

**Why Aho-Corasick wins**: Scanning 1GB file with 100K signatures
- Boyer-Moore × 100K: ~15 hours
- Aho-Corasick: ~30 seconds

### 3. Bioinformatics (DNA Sequence Search)

**Requirements**:
- Very long texts (human genome: 3 billion bases)
- Moderate pattern length (20-1000 bases)
- Approximate matching (allow mismatches, insertions, deletions)
- Small alphabet (A, C, G, T)

**Algorithm choice**: Specialized algorithms (not general string matching)
- BLAST: Uses seed-and-extend with suffix structures
- Bowtie: Uses Burrows-Wheeler Transform (BWT) + FM-index
- BLAT: Uses indexed seeds

**Why not standard algorithms**: Need approximate matching, index-based search faster for very long texts

### 4. Log Analysis

**Requirements**:
- Streaming data (logs arriving continuously)
- Multiple patterns (error signatures, security events)
- Real-time alerting (low latency)

**Algorithm choice**: Aho-Corasick for offline, Rabin-Karp or KMP for streaming
- Splunk: Uses inverted indexes + regex
- grep/ag: Boyer-Moore for single pattern
- LogStash: Grok patterns (regex-based)

**Considerations**: Often want regex support (more powerful than exact matching), so use regex engines rather than pure string matching

### 5. Network Intrusion Detection

**Requirements**:
- Inspect every packet (gigabit+ speeds)
- Thousands of attack signatures
- Deep packet inspection (scan payloads)
- Low false positive rate

**Algorithm choice**: Aho-Corasick with optimizations
- Snort: AC + hyperscan for multi-pattern
- Suricata: Uses hyperscan (Intel's optimized AC)
- Hardware NICs: Implement AC in FPGA/ASIC

**Performance requirement**: Must sustain 10+ Gbps → Software AC + SIMD, or hardware acceleration

## Implementation Considerations

### 1. Unicode and Encoding

**Challenge**: Pattern matching at byte level vs character level

**Byte-level matching**:
- Fast (no decoding overhead)
- Works for ASCII-compatible encodings
- Problem: Multi-byte characters (UTF-8) can cause false matches

**Character-level matching**:
- Semantically correct for Unicode
- Requires decoding text (slower)
- Pattern and text must use same encoding

**Best practice**:
- For ASCII/Latin-1: Byte-level is fine
- For UTF-8/UTF-16: Character-level or use library that handles it

### 2. Case Sensitivity

**Case-sensitive**: Direct matching, fast
**Case-insensitive**:
- Option 1: Convert pattern and text to lowercase (doubles memory, slower)
- Option 2: Use case-folding tables in algorithm (more complex)
- Option 3: Use regex engines with flags

### 3. Regex vs Exact Matching

**Exact string matching** (what these algorithms do):
- Faster (no backtracking, predictable performance)
- Limited expressiveness (fixed strings only)

**Regular expressions** (DFA/NFA-based):
- Much more powerful (wildcards, alternation, quantifiers)
- Slower (backtracking in NFA engines)
- Can have exponential worst case (catastrophic backtracking)

**When to use exact matching**: When patterns are known strings (virus signatures, URLs, keywords)

**When to use regex**: When patterns have structure (email validation, log parsing, wildcards)

## Common Pitfalls

1. **Using naive algorithm for large texts**: O(nm) becomes infeasible quickly
2. **Ignoring alphabet size**: Boyer-Moore bad-character table with Unicode is 65,536 entries
3. **Not considering preprocessing cost**: Building AC trie for 1M patterns takes time and memory
4. **Assuming Boyer-Moore is always fastest**: Worst-case can be slower than KMP
5. **Using wrong algorithm for multiple patterns**: Running single-pattern algorithm k times vs one AC pass
6. **Ignoring cache effects**: Algorithms with better complexity can be slower due to cache misses
7. **Not handling Unicode correctly**: Byte-level matching on UTF-8 can miss or false-match
8. **Forgetting the constant factors**: "O(n)" KMP can be slower than "O(nm)" naive for small patterns

## Best Practices (2025)

### Default Recommendations

**For single pattern search**:
- **General purpose**: Use Boyer-Moore (library implementation)
- **Worst-case guarantees needed**: Use KMP
- **Very short patterns (<5 chars)**: Naive or SIMD-optimized search
- **Text editors/interactive**: Optimized naive or regex engine

**For multiple patterns**:
- **10-100 patterns**: Consider running Boyer-Moore for each (if independent searches)
- **100+ patterns**: Use Aho-Corasick
- **Millions of patterns**: Use compressed AC variants or hyperscan

**For approximate matching**:
- Use specialized algorithms (agrep, Bitap) or regex with edit distance
- Consider Levenshtein automata for fuzzy matching

### Library Recommendations

**C/C++**:
- **strstr()**: Naive, use only for very short patterns
- **memmem()**: Optimized (often Boyer-Moore variant)
- **Boost.StringAlgo**: Various algorithms
- **Hyperscan** (Intel): Highly optimized multi-pattern (Aho-Corasick + DFA optimization)

**Python**:
- **str.find()**: Optimized (often Boyer-Moore-Horspool)
- **re module**: For regex (use when pattern matching not sufficient)
- **ahocorasick** library: For multi-pattern
- **pyre2**: Google RE2 bindings (safer regex)

**Rust**:
- **memchr crate**: Highly optimized single-byte search (uses SIMD)
- **aho-corasick crate**: Multi-pattern search
- **regex crate**: Modern regex engine (DFA/NFA hybrid)

**Go**:
- **strings.Index()**: Optimized (often Rabin-Karp variant)
- **regexp package**: For regex

**Java**:
- **String.indexOf()**: Optimized (often Boyer-Moore variant)
- **Pattern/Matcher**: For regex
- **Aho-Corasick implementations**: Various third-party libraries

### Performance Tips

1. **Benchmark with real data**: Theoretical complexity doesn't always predict real performance
2. **Consider SIMD**: Modern CPUs can search 16-32 bytes in parallel
3. **Profile memory access**: Cache-friendly algorithms can beat theoretically faster ones
4. **Use specialized libraries**: Hyperscan, RE2, Rust regex crate are highly optimized
5. **Precompile patterns**: Amortize preprocessing cost over multiple searches
6. **Consider hardware acceleration**: FPGAs/ASICs for ultra-high throughput (e.g., 100 Gbps networks)

## Key Metrics

**Pattern matching performance metrics**:

1. **Throughput**: MB/s or GB/s of text processed
   - Naive: ~100 MB/s
   - KMP: ~500 MB/s
   - Boyer-Moore: ~1-2 GB/s (average case)
   - SIMD-optimized: ~5-10 GB/s
   - Hardware: ~100+ GB/s

2. **Latency**: Time to first match (interactive search)
   - Affected by: Preprocessing time, text size, match position

3. **Memory footprint**:
   - KMP: ~1 KB for typical patterns
   - Boyer-Moore: ~1-256 KB (depends on alphabet)
   - Aho-Corasick: ~1 MB per 1000 patterns (varies widely)

4. **Preprocessing time**:
   - KMP/BM: Microseconds to milliseconds
   - Aho-Corasick: Seconds for 100K patterns

## Resources

### Essential Reading
- [Knuth-Morris-Pratt paper (1977)](https://doi.org/10.1137/0206024) - Original KMP algorithm
- [Boyer-Moore paper (1977)](https://dl.acm.org/doi/10.1145/359842.359859) - Original BM algorithm
- [Aho-Corasick paper (1975)](https://dl.acm.org/doi/10.1145/360825.360855) - Original AC algorithm
- [Handbook of Exact String Matching](http://www-igm.univ-mlv.fr/~lecroq/string/) - Comprehensive algorithm survey

### Libraries
- **Hyperscan** (Intel): Industrial-strength multi-pattern matching
- **RE2** (Google): Fast, safe regex engine
- **Rust regex**: Fast regex with linear time guarantees
- **Aho-Corasick implementations**: Available in most languages

### Benchmarks
- [Smart String Search](https://github.com/cloudflare/sliceslice-rs) - Benchmark suite
- [Hyperscan benchmarks](https://www.hyperscan.io/performance/) - Multi-pattern performance

## Summary

Pattern matching is a foundational algorithm problem with solutions ranging from simple brute-force to sophisticated multi-pattern matching. The choice of algorithm depends on:

1. **Number of patterns**: Single (BM/KMP) vs many (AC)
2. **Text characteristics**: Size, alphabet, structure
3. **Performance requirements**: Average vs worst-case, throughput vs latency
4. **Reusability**: One-time search vs reuse pattern structures

**Modern recommendations (2025)**:
- **Single pattern**: Boyer-Moore for speed, KMP for guarantees
- **Multiple patterns**: Aho-Corasick (or hyperscan for extreme performance)
- **Regex needed**: Use modern engines (RE2, Rust regex) with linear time guarantees
- **Production systems**: Use specialized libraries, not hand-rolled implementations

The field has matured with highly optimized implementations leveraging SIMD, cache-friendly data structures, and hardware acceleration. For most applications, use a well-tested library rather than implementing from scratch.

## Sources

This domain explainer synthesizes knowledge from:
- Classic papers (KMP 1977, Boyer-Moore 1977, Aho-Corasick 1975)
- Modern textbooks (Introduction to Algorithms, Algorithm Design Manual)
- Production systems (ClamAV, Snort, hyperscan, grep implementations)
- Benchmarks and performance studies (2020-2025)

For detailed algorithm descriptions and implementations, see the S1-S4 discovery documents.
