# Rabin-Karp Algorithm

## Core Mechanism

**Central insight**: Use rolling hash function to quickly compare pattern hash with text window hashes, verify matches with string comparison.

**Key innovation**: Hash function can be "rolled" in O(1) time (remove left character, add right character) allowing efficient sliding window computation.

**Why it works**: Hash comparison is O(1), only need full string comparison when hashes match (rare for good hash function).

## Data Structures

### Rolling Hash Function

**Polynomial hash** (most common):
```
hash("ABC") = (A × b² + B × b¹ + C × b⁰) mod q
```

Where:
- b = base (typically 256 for byte strings, 31 for text)
- q = large prime modulus (e.g., 10⁹+7, or 2⁶⁴-1)

**Example**: hash("CAT") with b=256, q=997
```
hash = (67×256² + 65×256 + 84) mod 997
     = (4,390,912 + 16,640 + 84) mod 997
     = 4,407,636 mod 997
     = 681
```

**Properties**:
- Deterministic: Same string → same hash
- Uniform distribution (for good choice of b and q)
- Efficient to compute

### Rolling Property

**Remove leftmost character**:
```
old_hash = (A × b² + B × b¹ + C × b⁰) mod q

Remove A: multiply by b⁻¹, gives (B × b¹ + C × b⁰) mod q
```

**Add rightmost character**:
```
new_hash = (B × b² + C × b¹ + D × b⁰) mod q
```

**Combined formula**:
```
new_hash = (b × (old_hash - A × b^(m-1)) + D) mod q
```

**Time**: O(1) - just arithmetic operations

**Key advantage**: Don't recompute hash from scratch for each window

## Algorithm Phases

### Phase 1: Preprocessing

**Compute pattern hash**: O(m)
```
hash_p = 0
for i = 0 to m-1:
    hash_p = (hash_p × b + pattern[i]) mod q
```

**Precompute b^(m-1) mod q**: O(log m) or O(m)
```
h = b^(m-1) mod q  // Used for rolling hash
```

**Total preprocessing**: O(m)

### Phase 2: Matching

**Time**: O(n) average case, O(nm) worst case

**Pseudocode**:
```
hash_t = 0
// Compute hash of first window
for i = 0 to m-1:
    hash_t = (hash_t × b + text[i]) mod q

for s = 0 to n-m:  // slide window
    if hash_p == hash_t:
        // Hash match - verify with string comparison
        if pattern == text[s..s+m-1]:
            report match at position s

    if s < n-m:  // roll hash to next window
        hash_t = (b × (hash_t - text[s] × h) + text[s+m]) mod q
        // Handle negative hash (modulo arithmetic)
        if hash_t < 0:
            hash_t += q
```

**Key steps**:
1. Compute initial window hash
2. For each position:
   - Compare hashes (O(1))
   - On match, verify strings (O(m))
   - Roll hash to next window (O(1))

### Example Execution

**Pattern**: "CAT" (m=3)
**Text**: "SCATTER" (n=7)
**Hash parameters**: b=256, q=997

**Preprocessing**:
```
hash_p = hash("CAT") = 681
h = 256² mod 997 = 929  // for rolling
```

**Matching**:
```
Window "SCA": hash = 123 ≠ 681 → skip
Roll to "CAT": hash = 681 == 681 → verify → MATCH
Roll to "ATT": hash = 456 ≠ 681 → skip
...
```

**Comparisons**:
- Hash comparisons: 5 (one per window)
- String comparisons: 1 (only for hash match at "CAT")
- Total: Much less than naive O(nm)

## Complexity Analysis

### Time Complexity

**Preprocessing**: O(m)
- Compute pattern hash: O(m)
- Compute h = b^(m-1): O(m) or O(log m)

**Matching Best/Average Case**: O(n + m)
- Roll hash n-m+1 times: O(n)
- String comparisons: O(k × m) where k = spurious hits
- For good hash function, k is constant (very few collisions)
- Total: O(n + m)

**Matching Worst Case**: O(nm)
- When: Many hash collisions (all windows match hash)
- Every window requires string comparison: O(m)
- n-m+1 windows: O(nm)

**Example worst case**: Pattern "AAA", Text "AAAAAAA..."
- If hash collides frequently, degrades to naive

### Space Complexity

**O(1)**: Only stores a few hash values and constants
- hash_p, hash_t, h, b, q: O(1)
- No auxiliary arrays or tables

**Advantage over KMP/BM**: Minimal memory footprint

### Hash Collision Analysis

**Probability of collision**:
- For random strings, P(hash(S₁) = hash(S₂)) ≈ 1/q
- With q = 10⁹, collision probability ≈ 10⁻⁹
- For text of length n, expected spurious hits ≈ n/q

**Expected running time**:
```
E[comparisons] = n × (1/q) × m + k
               ≈ O(n + m) for large q
```

**Choosing q**:
- Larger q → fewer collisions, but risk of overflow
- Common choices: 10⁹+7 (32-bit), 10⁹+9, 2³¹-1
- For 64-bit: Can use q ≈ 2⁶¹ (avoid overflow)

## Performance Characteristics

### When Rabin-Karp Excels

**Multiple patterns with same length**:
- Compute hash for each pattern: O(km)
- Store in hash table: O(k)
- Single pass through text: O(n)
- Check if window hash in table: O(1) expected
- **Total**: O(n + km) - much faster than k × O(n)

**Example**: Search for 1000 10-character patterns
- RK: O(n + 10,000) ≈ O(n)
- BM × 1000: O(1000n) worst case
- AC: O(n + 10,000) but more complex

**2D pattern matching**:
- Extend rolling hash to 2D (images, grids)
- Roll hash horizontally and vertically
- Useful for image matching, texture detection

**Plagiarism detection**:
- Search document for chunks matching other documents
- Rabin fingerprinting (related technique)
- Used in tools like MOSS, Turnitin

### When Rabin-Karp Struggles

**Poor hash function**:
- Many collisions → O(nm) behavior
- Critical to choose good b and q

**Variable-length patterns**:
- Must recompute b^(m-1) for each pattern length
- Less efficient than AC for mixed-length patterns

**Single pattern search**:
- BM is faster (sublinear average case)
- RK is linear at best

**Very long patterns**:
- String comparison on hash match takes O(m) time
- If pattern very long (m = 10,000), slow

## Implementation Considerations

### Choosing Hash Parameters

**Base b**:
- For bytes: b = 256 (natural)
- For text: b = 31 or 37 (prime, avoids patterns)
- For alphabet size σ: b ≈ σ

**Modulus q**:
- Large prime (e.g., 10⁹+7, 10⁹+9, 2³¹-1)
- Trade-off: Larger q → fewer collisions, but need bigger integers
- 64-bit systems: Can use q ≈ 2⁶¹ and detect overflow

**Avoiding overflow**:
```
// Careful modular arithmetic
hash = ((hash × b) % q + text[i]) % q
```

Or use 128-bit integers for intermediate results

### Handling Negative Values

**Issue**: In rolling hash, `old_hash - leftChar × h` can be negative

**Solution**: Add q if negative
```
hash = (b × (hash - text[s] × h) + text[s+m]) mod q
if hash < 0:
    hash += q
```

### Multiple Pattern Matching

**Approach**:
1. Compute hash for all patterns: O(km)
2. Store hashes in hash table (or set)
3. Roll through text, check if hash in table

**Pseudocode**:
```
pattern_hashes = set()
for each pattern:
    pattern_hashes.add(hash(pattern))

hash_t = hash(text[0..m-1])
for s = 0 to n-m:
    if hash_t in pattern_hashes:
        // Verify which pattern(s) match
        for each pattern with this hash:
            if pattern == text[s..s+m-1]:
                report match
    roll hash to next window
```

**Complexity**: O(n + km) average, O(nmk) worst case

### Unicode and Encoding

**Byte-level hashing**:
- Hash raw bytes (UTF-8, UTF-16)
- Fast, but assumes same encoding

**Character-level hashing**:
- Hash Unicode code points
- Correct for mixed encodings
- Slower (decoding overhead)

### Case-Insensitive Matching

**Approach 1**: Lowercase before hashing
- Convert pattern and text to lowercase
- Simple but requires extra memory

**Approach 2**: Use case-folded hash
- Map 'A'→'a', 'B'→'b' in hash computation
- No extra memory

## Variants and Extensions

### Rabin Fingerprinting (rsync)

**Application**: Detect similar blocks in files (rsync, deduplication)

**Approach**:
- Compute rolling hash over all windows
- Store hash → position mapping
- Identify common blocks across files

**Use case**: Efficient file synchronization

### Multiple Hash Functions (Bloom Filter)

**Idea**: Use k different hash functions
- Reduces false positive rate
- Similar to Bloom filter

**Trade-off**: k × more computation, but deterministic matching

### 2D Rabin-Karp

**Application**: Find pattern in 2D grid (images, matrices)

**Approach**:
1. Roll hash horizontally for each row
2. Roll hash vertically across rows
3. Check if 2D hash matches pattern

**Complexity**: O(nm) for text size n×n and pattern m×m

**Use case**: Image matching, texture detection

## Comparison with Other Algorithms

### vs Naive

**RK advantages**:
- O(n + m) average vs O(nm)
- Much faster in practice

**Naive advantages**:
- Simpler (no hash computation)
- Better for very short patterns (m < 3)

### vs KMP

**KMP advantages**:
- Guaranteed O(n + m) (no worst case)
- No hash collisions to handle
- Deterministic performance

**RK advantages**:
- Simpler implementation
- O(1) space vs O(m) for failure function
- Easier to adapt for multiple patterns

### vs Boyer-Moore

**BM advantages**:
- Sublinear average case O(n/m)
- Much faster for single pattern

**RK advantages**:
- Simpler implementation
- Better for multiple patterns (same length)
- O(1) space

### vs Aho-Corasick

**AC advantages**:
- Handles variable-length patterns efficiently
- No hash collisions
- Deterministic O(n + m + z)

**RK advantages**:
- Much simpler implementation
- Lower memory usage
- Competitive for few patterns

## Real-World Usage

### Where Rabin-Karp is Used

**Plagiarism detection** (MOSS, Turnitin):
- Rabin fingerprinting for chunking documents
- Detect similar passages efficiently

**rsync (file synchronization)**:
- Rolling hash to find common blocks
- Minimize data transfer

**Database engines** (some implementations):
- Simple string search in indexes
- Low memory overhead

**Education**:
- Teaching hashing, rolling hash concept
- Simpler than KMP/BM for students

### Where Rabin-Karp is NOT Used

**General text search**: BM is faster
**Production IDS**: AC or Hyperscan (deterministic, no collisions)
**Text editors**: Usually BM or naive (interactive, patterns short)

## Theoretical Insights

**Monte Carlo vs Las Vegas**:
- **Monte Carlo RK**: Don't verify string match (accept hash match)
  - Faster: O(n + m) guaranteed
  - Probabilistic: Small chance of false positive
- **Las Vegas RK**: Always verify string match (standard)
  - Correct: No false positives
  - Probabilistic: O(nm) worst case unlikely

**Rolling hash as fingerprint**:
- Weak hash (small q): Fast but many collisions
- Strong hash (large q, cryptographic): Slow but rare collisions
- Trade-off: Speed vs collision rate

**Connection to Bloom filters**:
- Multiple hash functions reduce false positive rate
- RK with k hashes approaches Bloom filter behavior

## Key Takeaways

**Strengths**:
- Simple implementation (easier than KMP/BM)
- O(1) space (minimal memory)
- Good for multiple patterns (same length)
- Extensible (2D, rsync, fingerprinting)

**Weaknesses**:
- O(nm) worst case (hash collisions)
- Slower than BM for single pattern
- Requires careful hash function choice
- Not deterministic (probabilistic correctness)

**Best for**:
- Multiple patterns (same length)
- 2D pattern matching (images)
- Plagiarism detection, fingerprinting
- Teaching hashing concepts
- Low memory environments

**Not best for**:
- Single pattern (use BM)
- Variable-length patterns (use AC)
- Hard real-time (unpredictable due to collisions)
- Production IDS (AC/Hyperscan more reliable)

## Implementation Example (Pseudocode)

```python
def rabin_karp(text, pattern, b=256, q=1000000007):
    n, m = len(text), len(pattern)
    if m > n:
        return []

    # Preprocessing
    hash_p = 0  # pattern hash
    hash_t = 0  # text window hash
    h = 1       # b^(m-1) mod q

    # Compute h = b^(m-1) mod q
    for i in range(m-1):
        h = (h * b) % q

    # Compute initial hashes
    for i in range(m):
        hash_p = (hash_p * b + ord(pattern[i])) % q
        hash_t = (hash_t * b + ord(text[i])) % q

    matches = []

    # Matching
    for s in range(n - m + 1):
        if hash_p == hash_t:
            # Verify match
            if text[s:s+m] == pattern:
                matches.append(s)

        # Roll hash
        if s < n - m:
            hash_t = (b * (hash_t - ord(text[s]) * h) + ord(text[s+m])) % q
            if hash_t < 0:
                hash_t += q

    return matches
```
