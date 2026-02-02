# pyahocorasick - Technical Analysis

## Algorithm Foundation

**Core Algorithm:** Aho-Corasick automaton (trie-based multi-pattern matching)

**Data Structure:** Combines two components:
1. **Trie**: Efficient prefix tree for pattern storage
2. **Automaton**: State machine for linear-time matching

## How It Works

1. **Build Phase**: Insert all patterns into trie (one-time cost)
2. **Link Phase**: Construct failure links between trie nodes
3. **Search Phase**: Scan text once, following automaton transitions

## Complexity Analysis

| Operation | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Build automaton | O(Σm) | O(Σm) |
| Search | O(n + z) | O(1) |
| Total | O(Σm + n + z) | O(Σm) |

*where n = text length, m = pattern length, Σm = sum of all pattern lengths, z = matches*

## Performance Characteristics

**Key Insight**: Performance is **independent of pattern count**

- **100 patterns**: O(n) search time
- **10,000 patterns**: Still O(n) search time (same!)
- **Worst-case = Best-case**: Predictable performance

**Comparison:**
- Naive loop: O(n × k × m) where k = pattern count
- Single regex: O(n × k) with potential backtracking
- Aho-Corasick: O(n + z) regardless of pattern count

## API Design

### Minimal Examples

**Basic multi-pattern search:**
```python
import ahocorasick

# Build automaton
A = ahocorasick.Automaton()
A.add_word("apple", "apple")
A.add_word("orange", "orange")
A.make_automaton()

# Search
text = "I have an apple and an orange"
for end_index, value in A.iter(text):
    print(value, "found")
# Output: apple found, orange found
```

**Keyword filtering (10K patterns):**
```python
# Build once
automaton = ahocorasick.Automaton()
for keyword in banned_words:  # 10,000 words
    automaton.add_word(keyword, keyword)
automaton.make_automaton()

# Reuse for many texts - O(n) each time
def check_content(text):
    for end_index, word in automaton.iter(text):
        return False  # Found banned word
    return True  # Clean
```

## Architecture

- **Language**: 52% C, 38% Python
- **Python Support**: 3.9+
- **Platforms**: Linux (64-bit), macOS, Windows
- **License**: BSD-3-Clause (very permissive)

## Feature Matrix

| Feature | Supported | Notes |
|---------|-----------|-------|
| Exact multi-pattern | ✅ | Core strength |
| Approximate matching | ⚠️ | Limited support |
| Case sensitivity | ✅ | Configurable |
| Unicode | ✅ | Full support |
| Pattern count | ✅ | No practical limit |

## Strengths

1. **Scalability**: Performance doesn't degrade with pattern count
2. **Predictability**: O(n) worst-case guaranteed
3. **Memory efficiency**: Trie shares common prefixes
4. **Mature algorithm**: Well-studied, proven correct

## Limitations

1. **Build cost**: Creating automaton has upfront cost
2. **Exact matching focus**: Not designed for fuzzy matching
3. **API complexity**: Automaton pattern requires learning
4. **Overkill for few patterns**: str.find() faster for 1-10 patterns

## When to Choose pyahocorasick

✅ **Use when:**
- Searching for many patterns simultaneously (100+)
- Pattern count is large or variable
- Performance predictability critical
- Reusing automaton across many texts

❌ **Skip when:**
- Single pattern search (→ str.find() or regex)
- Approximate matching needed (→ RapidFuzz)
- Pattern count < 10 (overhead not justified)
- One-time search (build cost dominates)

## Alternative

**ahocorasick_rs** (Rust implementation): Claims 1.5× to 7× faster, but less mature ecosystem.

## References

- [pyahocorasick Documentation](https://pyahocorasick.readthedocs.io/)
- [GitHub - WojciechMula/pyahocorasick](https://github.com/WojciechMula/pyahocorasick)
- [Aho-Corasick Algorithm Paper](https://dl.acm.org/doi/10.1145/360825.360855)
