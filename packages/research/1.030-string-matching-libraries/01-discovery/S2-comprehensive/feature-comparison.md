# Feature Comparison Matrix

## Fuzzy/Approximate Matching Libraries

| Feature | RapidFuzz | Jellyfish | difflib (stdlib) |
|---------|-----------|-----------|------------------|
| **Edit Distance** | ✅ Levenshtein, Hamming, Damerau | ✅ Levenshtein, Damerau | ✅ SequenceMatcher |
| **Similarity Scores** | ✅ Jaro, Jaro-Winkler, LCS | ✅ Jaro, Jaro-Winkler | ✅ ratio, quick_ratio |
| **Token-Based** | ✅ Sort, Set, Partial | ❌ | ❌ |
| **Phonetic Encoding** | ❌ | ✅ Soundex, Metaphone, NYSIIS | ❌ |
| **Speed (pairs/sec)** | ~1,800 | Slower | ~1,000 |
| **Memory Usage** | 20-200 MB | Higher with long strings | Moderate |
| **Implementation** | C++ | C + Python | Pure Python |
| **License** | MIT | MIT | PSF (stdlib) |
| **Python Version** | 3.10+ | 3.x | Included |

## Exact Matching Libraries

| Feature | pyahocorasick | Standard str methods |
|---------|---------------|---------------------|
| **Multi-Pattern** | ✅ Thousands | ❌ One at a time |
| **Time Complexity** | O(n + z) | O(n × k × m) |
| **Build Phase** | ✅ Required | ❌ None |
| **Memory** | O(Σm) trie | O(1) |
| **Use Case** | Many patterns | Few patterns |
| **Learning Curve** | Moderate | Minimal |

## Regex Libraries

| Feature | re (stdlib) | regex | google-re2 |
|---------|-------------|-------|------------|
| **Engine Type** | Backtracking | Backtracking | DFA |
| **Time Complexity** | O(2^n) worst | O(2^n) worst | O(n) guaranteed |
| **Backreferences** | ✅ | ✅ | ❌ |
| **Lookahead/Lookbehind** | ✅ (fixed) | ✅ (variable) | ❌ |
| **Set Operations** | ❌ | ✅ | ❌ |
| **Possessive Quantifiers** | ❌ | ✅ | ✅ (implicit) |
| **Unicode Support** | Older | 17.0.0 | Older |
| **GIL Release** | ❌ | ✅ | ❌ |
| **DoS Resistance** | ❌ | ❌ | ✅ |
| **License** | PSF | Apache 2.0 | BSD-3 |
| **Dependency** | Stdlib | PyPI | PyPI + C++ |

## Performance Summary

### Speed Rankings (Fastest to Slowest)

**Fuzzy Matching:**
1. RapidFuzz (~1,800 pairs/sec)
2. Jellyfish (good for short strings)
3. difflib (~1,000 pairs/sec)

**Multi-Pattern Exact:**
1. pyahocorasick (O(n) regardless of pattern count)
2. Multiple str.find() calls (O(n × k))

**Regex:**
1. RE2 (linear time guaranteed, but compilation overhead)
2. re/regex (similar, re sometimes faster for simple patterns)

### Memory Rankings (Most Efficient to Least)

1. re, str methods (minimal)
2. google-re2 (DFA can vary)
3. pyahocorasick (trie structure)
4. Jellyfish (higher with long strings)
5. RapidFuzz (20-200 MB range)

## Algorithm Complexity Comparison

| Library | Build/Compile | Match/Search | Space |
|---------|---------------|--------------|-------|
| **RapidFuzz** | O(1) | O(nm) optimized | O(min(n,m)) |
| **Jellyfish** | O(1) | O(nm) | O(nm) |
| **pyahocorasick** | O(Σm) | O(n + z) | O(Σm) |
| **re/regex** | O(m) | O(2^n) worst | O(m) |
| **google-re2** | O(m²) | O(n) | O(m) to O(2^m) |

## License Comparison

| License | Libraries | Commercial Use | Attribution Required |
|---------|-----------|----------------|---------------------|
| **MIT** | RapidFuzz, Jellyfish | ✅ | Minimal |
| **BSD-3** | pyahocorasick, google-re2 | ✅ | Yes |
| **Apache 2.0** | regex | ✅ | Yes |
| **PSF** | re, difflib | ✅ | N/A (stdlib) |

All libraries listed are permissive for commercial use.

## Platform Support Matrix

| Library | Linux | macOS | Windows | ARM |
|---------|-------|-------|---------|-----|
| RapidFuzz | ✅ | ✅ | ✅ | ✅ |
| Jellyfish | ✅ | ✅ | ✅ | ⚠️ |
| pyahocorasick | ✅ | ✅ | ✅ | ⚠️ |
| regex | ✅ | ✅ | ✅ | ✅ |
| google-re2 | ✅ | ✅ | ✅ | ⚠️ |
| re, difflib | ✅ | ✅ | ✅ | ✅ |

✅ = Full support, ⚠️ = Limited/manual build required

## Key Insights

1. **RapidFuzz dominates fuzzy matching** across speed, features, and production usage
2. **Jellyfish owns phonetic** - the only library with Soundex/Metaphone
3. **pyahocorasick is unbeatable** for multi-pattern exact matching (>100 patterns)
4. **regex library is safer bet** than re for new projects (more features, better Unicode)
5. **RE2 trades features for guarantees** - use when security/predictability matters

## Decision Factors by Priority

### Speed Priority:
- Fuzzy: **RapidFuzz**
- Multi-pattern: **pyahocorasick**
- Regex: **re** (simple) or **RE2** (complex)

### Feature Priority:
- Fuzzy: **RapidFuzz** (most metrics)
- Phonetic: **Jellyfish** (only option)
- Regex: **regex library** (most features)

### Security Priority:
- Regex: **google-re2** (DoS-resistant)
- Fuzzy: All safe (no DoS risk)
- Multi-pattern: **pyahocorasick** (predictable)

### Zero-Dependency Priority:
- Fuzzy: **difflib** (stdlib)
- Regex: **re** (stdlib)
- Exact: **str methods** (built-in)
