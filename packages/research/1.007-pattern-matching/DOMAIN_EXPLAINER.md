# Pattern Matching Algorithms

## Overview

Pattern matching is the problem of finding occurrences of a pattern (substring) within a text. While naive approaches check every position (O(nm) complexity), sophisticated algorithms achieve better performance through preprocessing and clever skipping strategies.

## Key Algorithms

### 1. Knuth-Morris-Pratt (KMP)

**Invented:** 1977 by Donald Knuth, James H. Morris, and Vaughan Pratt

**Key Insight:** When a mismatch occurs, use information from the pattern itself to skip comparisons we know will fail.

**How it works:**
- Preprocessing: Build a "failure function" that tells us where to resume matching after a mismatch
- Searching: Never backtrack in the text, only adjust the pattern position
- Complexity: O(n+m) where n=text length, m=pattern length

**Best for:** Patterns with internal repetition, streaming data where you can't backtrack

### 2. Boyer-Moore

**Invented:** 1977 by Robert S. Boyer and J Strother Moore

**Key Insight:** Search right-to-left in the pattern, use character information to skip large sections of text.

**How it works:**
- Bad character rule: Skip ahead based on rightmost occurrence of mismatched character
- Good suffix rule: Skip based on matching suffix patterns
- Scans pattern from right to left
- Complexity: O(n/m) best case, O(nm) worst case

**Best for:** Long patterns in natural language text, patterns without much repetition

### 3. Aho-Corasick

**Invented:** 1975 by Alfred V. Aho and Margaret J. Corasick

**Key Insight:** Build a finite automaton that can match multiple patterns simultaneously in a single pass.

**How it works:**
- Build a trie of all patterns
- Add failure links for efficient transitions on mismatch
- Process text once, finding all pattern matches
- Complexity: O(n+m+z) where z=number of matches

**Best for:** Searching for many patterns at once (virus scanning, keyword detection, content filtering)

### 4. Rabin-Karp

**Invented:** 1987 by Michael O. Rabin and Richard M. Karp

**Key Insight:** Use rolling hash to quickly compare pattern with text substrings.

**How it works:**
- Compute hash of pattern
- Use rolling hash to efficiently compute hash of each text substring
- Only do character comparison when hashes match
- Complexity: O(n+m) average, O(nm) worst case

**Best for:** Multiple pattern matching, plagiarism detection, finding repeated substrings

## Modern Implementations

### Python

**Standard Library:**
```python
# str.find() uses optimized C implementation
text.find(pattern)  # Returns index or -1

# re module for regex patterns
import re
re.search(pattern, text)
```

**pyahocorasick:**
```python
import ahocorasick

A = ahocorasick.Automaton()
A.add_word("pattern1", ("pattern1", 1))
A.add_word("pattern2", ("pattern2", 2))
A.make_automaton()

for end_index, (pattern, count) in A.iter(text):
    print(f"Found {pattern} at position {end_index - len(pattern) + 1}")
```

### Rust

**aho-corasick crate:**
```rust
use aho_corasick::AhoCorasick;

let patterns = &["apple", "maple", "Snapple"];
let haystack = "Nobody likes maple in their apple flavored Snapple.";

let ac = AhoCorasick::new(patterns);
for mat in ac.find_iter(haystack) {
    println!("Pattern '{}' found at: {}", patterns[mat.pattern()], mat.start());
}
```

**memchr crate:**
Fast byte search using SIMD when available:
```rust
use memchr::memmem;

let finder = memmem::Finder::new("pattern");
for pos in finder.find_iter(haystack) {
    println!("Found at: {}", pos);
}
```

### C/C++

**Standard Library:**
```cpp
// strstr() - naive implementation
char* strstr(const char* haystack, const char* needle);

// std::string::find() - typically Boyer-Moore variant
std::string text = "...";
size_t pos = text.find("pattern");
```

**Specialized Libraries:**
- `libdivsufsort` - Suffix array construction for advanced matching
- `pcre2` - Perl-Compatible Regular Expressions with optimized matching

### Go

**Standard Library:**
```go
import "strings"

// Uses Rabin-Karp for small patterns, otherwise a variant of Boyer-Moore
index := strings.Index(text, pattern)

// Multiple patterns
replacer := strings.NewReplacer("old1", "new1", "old2", "new2")
result := replacer.Replace(text)
```

## Performance Comparison

| Algorithm | Preprocessing | Search (best) | Search (worst) | Space |
|-----------|--------------|---------------|----------------|-------|
| Naive | O(1) | O(n) | O(nm) | O(1) |
| KMP | O(m) | O(n) | O(n+m) | O(m) |
| Boyer-Moore | O(m+σ)* | O(n/m) | O(nm) | O(m+σ) |
| Aho-Corasick | O(Σm) | O(n+z) | O(n+Σm+z) | O(Σm) |
| Rabin-Karp | O(m) | O(n+m) | O(nm) | O(1) |

*σ = alphabet size, Σm = sum of pattern lengths, z = number of matches

## Use Case Decision Tree

**Single pattern, text streaming (can't backtrack)?**
→ KMP

**Single pattern, large text, long pattern, natural language?**
→ Boyer-Moore

**Multiple patterns (10+), scan once?**
→ Aho-Corasick

**Need simplicity, patterns change frequently?**
→ Rabin-Karp

**General purpose, modern languages?**
→ Use standard library (often hybrid algorithms)

## Real-World Applications

1. **Text Editors:** Find/replace functionality (Boyer-Moore variants)
2. **Intrusion Detection Systems:** Snort uses Aho-Corasick for signature matching
3. **Antivirus Software:** Multiple pattern matching for virus signatures
4. **Bioinformatics:** DNA sequence searching
5. **Log Analysis:** Searching for error patterns across logs
6. **Content Filtering:** Blocking banned words/phrases
7. **Plagiarism Detection:** Finding copied text (Rabin-Karp)

## Modern Optimizations

### SIMD Acceleration

Modern CPUs can compare 16-32 bytes simultaneously:
- Intel's `pcmpestri` instruction for string operations
- Rust's `memchr` uses SIMD for single-byte search
- Can achieve 10-20x speedup for certain patterns

### Hybrid Algorithms

Many modern implementations combine strategies:
- Python's `str.find()`: Two-way algorithm (Crochemore-Perrin)
- glibc's `strstr()`: Two-way algorithm
- Go's `strings.Index()`: Rabin-Karp for small, Boyer-Moore variant for large

### Suffix Arrays / Trees

For repeated searches on the same text:
- Build suffix array once: O(n log n)
- Search in O(m log n)
- Used in bioinformatics, data compression

## Benchmarks

Typical performance on 1MB text, 10-character pattern:

| Implementation | Time | Speed |
|----------------|------|-------|
| Python str.find() | 0.5 ms | ~2 GB/s |
| pyahocorasick (single) | 2.1 ms | ~500 MB/s |
| Rust memchr | 0.15 ms | ~6.7 GB/s |
| Rust aho-corasick (100 patterns) | 3.5 ms | ~300 MB/s |
| Go strings.Index | 0.8 ms | ~1.25 GB/s |

*Benchmarks approximate, vary by pattern characteristics*

## Limitations & Edge Cases

1. **Small patterns (<5 chars):** Naive search often fastest due to simplicity
2. **Many patterns on short text:** Overhead of Aho-Corasick may not pay off
3. **Unicode:** Character boundaries complicate byte-level algorithms
4. **Regex features:** Need full regex engine (e.g., PCRE) for complex patterns

## Further Reading

- Original papers (all freely available):
  - Knuth, Morris, Pratt (1977): "Fast Pattern Matching in Strings"
  - Boyer, Moore (1977): "A Fast String Searching Algorithm"
  - Aho, Corasick (1975): "Efficient String Matching: An Aid to Bibliographic Search"
- "Flexible Pattern Matching in Strings" by Gonzalo Navarro, Mathieu Raffinot
- stringzilla library (recent, SIMD-optimized string operations)
