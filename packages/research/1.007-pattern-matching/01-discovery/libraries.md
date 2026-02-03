# Pattern Matching Libraries - Detailed Comparison

## Python Libraries

### 1. Built-in str Methods

**Package:** Python Standard Library
**Algorithm:** Two-way algorithm (Crochemore-Perrin)
**License:** PSF License

```python
text.find(pattern)      # Returns index or -1
text.index(pattern)     # Returns index or raises ValueError
text.count(pattern)     # Count occurrences
text.replace(old, new)  # Replace all occurrences
```

**Pros:**
- No dependencies
- Very fast for single patterns
- Memory efficient

**Cons:**
- Single pattern only
- No regex support
- Limited to exact matches

**GitHub:** Part of CPython
**PyPI Downloads:** N/A (built-in)

---

### 2. pyahocorasick

**Package:** pyahocorasick
**Algorithm:** Aho-Corasick automaton
**License:** BSD-3-Clause
**GitHub:** ~900 stars

```python
import ahocorasick

A = ahocorasick.Automaton()
for idx, key in enumerate(['apple', 'banana', 'orange']):
    A.add_word(key, (idx, key))
A.make_automaton()

for end_index, (idx, key) in A.iter(text):
    start = end_index - len(key) + 1
    print(f"Found '{key}' at position {start}")
```

**Pros:**
- Extremely fast for multiple patterns
- C implementation (fast)
- Supports case-insensitive matching
- Memory efficient automaton

**Cons:**
- Must rebuild automaton when patterns change
- No regex support
- Preprocessing overhead for small pattern sets

**PyPI Downloads:** ~400K/month
**Use Cases:** Keyword extraction, content filtering, log analysis

---

### 3. regex Module

**Package:** regex (PyPI) or re (stdlib)
**Algorithm:** Backtracking with optimizations
**License:** PSF License (re), Apache 2.0 (regex)

```python
import re

# Standard library
pattern = re.compile(r'pattern')
matches = pattern.finditer(text)

# regex module (more features)
import regex
pattern = regex.compile(r'(?r)pattern', regex.IGNORECASE)
```

**Pros:**
- Full regex support
- Named groups, lookahead, lookbehind
- Unicode support
- `regex` module adds features missing from `re`

**Cons:**
- Slower than specialized algorithms
- Can have exponential time complexity
- Memory overhead

**PyPI Downloads (regex):** ~25M/month
**Use Cases:** Complex pattern matching, validation, parsing

---

## Rust Libraries

### 1. aho-corasick

**Crate:** aho-corasick
**Algorithm:** Aho-Corasick with DFA optimization
**License:** MIT/Apache-2.0
**GitHub:** ~900 stars
**Crates.io:** ~50M downloads

```rust
use aho_corasick::AhoCorasick;

let patterns = &["apple", "maple", "Snapple"];
let ac = AhoCorasick::new(patterns)?;

for mat in ac.find_iter(haystack) {
    println!("Pattern {} at {}", mat.pattern(), mat.start());
}
```

**Pros:**
- Extremely fast
- Zero-copy searching
- Optional DFA construction for speed
- Streaming support

**Cons:**
- Memory usage scales with pattern set
- No regex support

**Used by:** ripgrep, the silver searcher (ag)

---

### 2. memchr

**Crate:** memchr
**Algorithm:** SIMD-accelerated byte search
**License:** MIT/Apache-2.0
**GitHub:** Part of rust-lang/memchr
**Crates.io:** ~200M downloads

```rust
use memchr::{memchr, memmem};

// Single byte search
if let Some(pos) = memchr(b'a', haystack) {
    println!("Found 'a' at {}", pos);
}

// Substring search
let finder = memmem::Finder::new(b"pattern");
for pos in finder.find_iter(haystack) {
    println!("Found at {}", pos);
}
```

**Pros:**
- Insanely fast (SIMD)
- Zero dependencies
- Used everywhere in Rust ecosystem
- Falls back to optimized scalar code

**Cons:**
- Byte-oriented (not Unicode-aware)
- Single pattern at a time

**Used by:** Almost every Rust string library

---

### 3. regex (Rust)

**Crate:** regex
**Algorithm:** Finite automaton (Thompson NFA)
**License:** MIT/Apache-2.0
**GitHub:** ~3.3K stars
**Crates.io:** ~150M downloads

```rust
use regex::Regex;

let re = Regex::new(r"\d{4}-\d{2}-\d{2}").unwrap();
for mat in re.find_iter(text) {
    println!("Date: {}", mat.as_str());
}
```

**Pros:**
- Guaranteed linear time (no catastrophic backtracking)
- Unicode support
- Very well optimized
- Compile-time regex with `regex_macros`

**Cons:**
- More limited than PCRE (no backreferences, no lookaround)
- Compilation overhead

**Used by:** ripgrep, fd, countless Rust projects

---

## C/C++ Libraries

### 1. std::string::find()

**Library:** C++ Standard Library
**Algorithm:** Implementation-defined (often Boyer-Moore variant)
**License:** Part of compiler

```cpp
#include <string>

std::string text = "...";
size_t pos = text.find("pattern");
if (pos != std::string::npos) {
    std::cout << "Found at " << pos << std::endl;
}
```

**Pros:**
- No dependencies
- Well-optimized in modern stdlib implementations
- Familiar API

**Cons:**
- Implementation-defined behavior
- Single pattern only

---

### 2. strstr() / memmem()

**Library:** C Standard Library / GNU libc
**Algorithm:** Two-way algorithm (glibc), varies by implementation
**License:** Part of libc

```c
#include <string.h>

char *result = strstr(haystack, needle);
void *result = memmem(haystack, haystack_len, needle, needle_len);
```

**Pros:**
- Universally available
- glibc version is highly optimized

**Cons:**
- Varies by platform
- Null-terminated strings only (strstr)

---

### 3. libdivsufsort + suffix array libraries

**Library:** libdivsufsort
**Algorithm:** Induced sorting for suffix array construction
**License:** MIT
**GitHub:** ~400 stars

```c
#include <divsufsort.h>

// Build suffix array
saidx_t *SA = malloc(n * sizeof(saidx_t));
divsufsort((const unsigned char *)text, SA, n);

// Use for pattern matching
```

**Pros:**
- Very fast suffix array construction
- Enables O(m log n) pattern search
- Useful for repeated searches

**Cons:**
- Preprocessing overhead
- More complex API
- Not for simple one-time searches

---

## Go Libraries

### 1. strings Package

**Package:** strings (stdlib)
**Algorithm:** Rabin-Karp (short patterns), Boyer-Moore variant (long)
**License:** BSD-3-Clause

```go
import "strings"

idx := strings.Index(haystack, needle)
count := strings.Count(haystack, needle)
contains := strings.Contains(haystack, needle)
```

**Pros:**
- Built-in, no dependencies
- Automatically chooses algorithm
- Fast and simple

**Cons:**
- Single pattern only
- No regex in strings package

---

### 2. regexp Package

**Package:** regexp (stdlib)
**Algorithm:** RE2 (guaranteed linear time)
**License:** BSD-3-Clause

```go
import "regexp"

re := regexp.MustCompile(`\d{3}-\d{4}`)
matches := re.FindAllString(text, -1)
```

**Pros:**
- Linear time guarantee (like Rust regex)
- Safe from ReDoS attacks
- Good performance

**Cons:**
- More limited than PCRE
- No backreferences

---

## Performance Summary

### Single Pattern Search (1MB text, 10-char pattern)

| Library | Language | Time | Throughput |
|---------|----------|------|------------|
| memchr | Rust | 0.15 ms | ~6.7 GB/s |
| str.find() | Python | 0.5 ms | ~2 GB/s |
| std::string::find() | C++ | 0.3 ms | ~3.3 GB/s |
| strings.Index | Go | 0.8 ms | ~1.25 GB/s |

### Multiple Pattern Search (100 patterns, 1MB text)

| Library | Language | Time | Throughput |
|---------|----------|------|------------|
| aho-corasick | Rust | 3.5 ms | ~300 MB/s |
| pyahocorasick | Python | 4.0 ms | ~250 MB/s |
| regex (union) | Rust | 8.0 ms | ~125 MB/s |

*Benchmarks approximate, vary by CPU and pattern characteristics*

## Recommendation Matrix

| Use Case | Language | Recommended Library |
|----------|----------|-------------------|
| Single pattern, Python | Python | Built-in str.find() |
| Multiple patterns, Python | Python | pyahocorasick |
| Complex patterns, Python | Python | re or regex module |
| Any pattern matching, Rust | Rust | aho-corasick + memchr |
| Regex in Rust | Rust | regex crate |
| System programming | C/C++ | glibc strstr/memmem |
| Single pattern, Go | Go | strings.Index |
| Regex in Go | Go | regexp package |

## Emerging Libraries

### stringzilla
- Ultra-fast string operations using SIMD
- Python and C++ bindings
- Claims 10x faster than standard implementations
- Still relatively new (2023+)

### hyperscan (Intel)
- Multiple regex matching with DFA
- Extremely fast but complex
- Used in high-performance networking (Suricata IDS)
- Commercial-grade library
