# Use Case: Text Processing Application Developers

## Who Needs This

**Persona:** Application developers building text-heavy features, NLP engineers, data cleaning tool creators

**Context:**
- Building fuzzy search features (find similar strings despite typos)
- Deduplication systems (find near-duplicate records)
- Spell checkers, autocorrect, text suggestion systems
- Data cleaning tools (match dirty data to canonical forms)
- Document similarity scoring

**Scale:**
- 1000s-millions of string comparisons
- Real-time or batch processing
- Variable string lengths (10 chars to 10k chars)
- Performance critical (user-facing features)

**Constraints:**
- Speed is critical (real-time features need <10ms per comparison)
- Similarity scoring required (not just "same or different")
- Fuzzy matching (tolerate typos, variants, abbreviations)
- Multiple metrics (Levenshtein, Jaro-Winkler, etc. for different use cases)

## Why They Need It

**Problem:** Exact string matching (`s1 == s2`) fails for real-world text:
- Typos: "recieve" vs "receive"
- Variants: "color" vs "colour"
- Abbreviations: "Dr." vs "Doctor"
- Noise: "  hello  " vs "hello"
- Near-duplicates: "John Smith" vs "Jon Smith"

**Use cases:**
1. **Fuzzy search:** User types "Shakespear", find "Shakespeare"
2. **Deduplication:** Find duplicate customer records despite typos
3. **Spell check:** Find closest dictionary word to misspelling
4. **Data cleaning:** Match messy input to clean database entries
5. **Similarity scoring:** Rank documents by similarity to query

**Requirements:**
- **MUST**: Similarity scoring (quantify how close strings are)
- **MUST**: Very fast (10-100x faster than pure Python)
- **MUST**: Multiple metrics (Levenshtein, Jaro-Winkler, etc.)
- **SHOULD**: Edit operations (for autocorrect: what to change)
- **SHOULD**: Handle Unicode (international text)

**Anti-Requirements:**
- Not for full diff with context (use difflib for code review)
- Not for structured data (use DeepDiff for JSON)
- Not for git integration (use GitPython)

## Library Fit Analysis

### Recommended Solution

→ **python-Levenshtein** (primary) + **difflib.get_close_matches** (secondary)

**python-Levenshtein:**
- ✅ Very fast (C extension, 10-100x faster than pure Python)
- ✅ Multiple metrics (Levenshtein, Jaro-Winkler, Hamming, Damerau)
- ✅ Edit operations (returns actual edit sequence)
- ✅ Low memory (no LCS computation, just distance)
- ✅ Battle-tested (10M downloads/month)

**difflib.get_close_matches:**
- ✅ Stdlib (no dependencies)
- ✅ Good for simple fuzzy matching
- ✅ Returns top N matches from candidates
- ⚠️ Slower than python-Levenshtein (pure Python)
- ⚠️ One metric only (SequenceMatcher ratio)

### Decision Matrix

| Use Case | Primary | Secondary | Rationale |
|----------|---------|-----------|-----------|
| Fuzzy search (real-time) | python-Levenshtein | - | Speed critical |
| Spell checker | python-Levenshtein | difflib | Fast C ext wins |
| Deduplication (batch) | python-Levenshtein | difflib | Either works, C faster |
| Simple matching (low volume) | difflib | - | Stdlib sufficient |
| International text | python-Levenshtein | - | Better Unicode support |

### Metric Selection Guide

**Levenshtein distance:**
- Best for: General-purpose similarity
- Measures: Minimum edits (insert, delete, substitute)
- Use when: Default choice for most cases

**Jaro-Winkler:**
- Best for: Short strings, especially names
- Measures: Character similarity with prefix bonus
- Use when: Matching person names, identifiers

**Hamming distance:**
- Best for: Fixed-length strings
- Measures: Position-by-position differences
- Use when: Comparing fixed-format codes, hashes

**Damerau-Levenshtein:**
- Best for: Typo tolerance
- Measures: Levenshtein + transpositions ("teh" → "the")
- Use when: Autocorrect, spell checking

### Anti-Patterns

**❌ DON'T use difflib for high-volume fuzzy matching:**
- 10-100x slower than python-Levenshtein
- Pure Python (no C optimization)

**❌ DON'T use DeepDiff/jsondiff:**
- Wrong domain (structured data, not text similarity)

**❌ DON'T use GitPython/tree-sitter:**
- Massive overkill for simple string similarity

### Decision Factors

**Choose python-Levenshtein when:**
- Speed critical (real-time features, high-volume batch)
- Need multiple metrics (try different algorithms)
- Want edit operations (for autocorrect features)
- Performance matters more than dependencies

**Choose difflib.get_close_matches when:**
- Simple fuzzy matching (low-volume)
- Want zero dependencies (stdlib only)
- Speed is acceptable (pure Python OK)

**Use both when:**
- Prototype with difflib (fast to try)
- Profile and benchmark
- Upgrade to python-Levenshtein if too slow

## Validation Criteria

**You picked the right library if:**
- ✅ Fast enough for your use case (<10ms per comparison for real-time)
- ✅ Finds similar strings (handles typos, variants)
- ✅ Similarity scores make sense (closer strings → higher scores)
- ✅ Handles your data (Unicode, long strings, etc.)

**Red flags (wrong choice):**
- ❌ Too slow (users notice lag in fuzzy search)
- ❌ Missing obvious matches (threshold too strict)
- ❌ Too many false positives (threshold too loose)
- ❌ Crashes on Unicode (encoding issues)

## Common Patterns

**Pattern: Spell checker**
```
# Find closest dictionary word to misspelling
def correct_spelling(word, dictionary):
    # Use Levenshtein distance to find closest matches
    distances = [(w, Levenshtein.distance(word, w)) for w in dictionary]
    distances.sort(key=lambda x: x[1])
    return distances[0][0]  # Closest match
```

**Pattern: Deduplication**
```
# Find near-duplicate records
def find_duplicates(records, threshold=0.9):
    duplicates = []
    for i, r1 in enumerate(records):
        for r2 in records[i+1:]:
            ratio = Levenshtein.ratio(r1, r2)
            if ratio > threshold:
                duplicates.append((r1, r2, ratio))
    return duplicates
```

**Pattern: Fuzzy search with ranking**
```
# Return top N closest matches
def fuzzy_search(query, candidates, n=5):
    scores = [(c, Levenshtein.ratio(query, c)) for c in candidates]
    scores.sort(key=lambda x: x[1], reverse=True)
    return [c for c, score in scores[:n]]
```

**Pattern: Hybrid approach (stdlib → C extension)**
```
# Start with difflib for simplicity
matches = difflib.get_close_matches(query, candidates)

# If too slow (profiling shows), upgrade:
# import Levenshtein
# matches = fuzzy_search_levenshtein(query, candidates)
```

## Real-World Example

**Scenario:** Building autocomplete for a search box (10k product names)

**Requirements:**
- User types "ipone", suggest "iPhone" and similar
- <10ms latency (real-time feature)
- Tolerate typos, missing characters
- Return top 5 matches

**Solution:** python-Levenshtein with Jaro-Winkler
1. User types query
2. Compute Jaro-Winkler distance to all 10k products (C ext is fast)
3. Sort by score (descending)
4. Return top 5

**Why python-Levenshtein:** Speed critical (10k comparisons per keystroke), C extension fast enough

**Why Jaro-Winkler:** Prefix-sensitive (user typing "ipho" should match "iPhone"), better than Levenshtein for short prefix matching

**Why not difflib:** Too slow (pure Python can't handle 10k comparisons in <10ms)

**Optimization:** Pre-filter with BK-tree or similar (reduce comparisons), then use Levenshtein for ranking
