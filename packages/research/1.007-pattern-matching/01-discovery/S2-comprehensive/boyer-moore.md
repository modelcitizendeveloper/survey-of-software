# Boyer-Moore Algorithm

## Core Mechanism

**Central insight**: Scan the pattern from right to left; on mismatch, use information about the mismatched character and matched suffix to skip multiple positions.

**Key innovation**: Two independent heuristics (bad character and good suffix) that can skip positions. Take the maximum skip from both heuristics.

**Why right-to-left scanning**: Makes the bad character heuristic highly effective (can skip entire pattern length on mismatch with character not in pattern).

## Data Structures

### 1. Bad Character Table

**Array**: `badChar[c]` for each character c in the alphabet

**Definition**: For each character, stores the rightmost position in the pattern (or -1 if not present)

**Purpose**: On mismatch at position j with character c, shift pattern to align c with its rightmost occurrence

**Example**: Pattern "EXAMPLE"
```
E: 6  (rightmost occurrence at index 6)
X: 1
A: 2
M: 3
P: 4
L: 5
(all other characters): -1
```

**Size**: O(σ) where σ = alphabet size
- DNA: 4 bytes
- ASCII: 256 bytes
- Unicode (full): 65,536 × 4 = 256 KB (often use hash table instead)

### 2. Good Suffix Table

**Array**: `goodSuffix[j]` for each position j in pattern

**Definition**: For position j where mismatch occurred:
- If suffix `pattern[j+1..m-1]` appears earlier in pattern, shift to align them
- Otherwise, shift to align longest prefix that matches a suffix
- Otherwise, shift entire pattern length

**Example**: Pattern "ANPANMAN"
```
Position: 0 1 2 3 4 5 6 7
Pattern:  A N P A N M A N
goodSuffix: [8, 8, 8, 8, 8, 4, 8, 1]
```

**Intuition**:
- At j=5 (mismatch), suffix "AN" appears at position 3-4 → shift 4 positions
- At j=7 (mismatch), suffix "N" appears at position 6 → shift 1 position

**Size**: O(m) where m = pattern length

### Strong Good Suffix Rule

**Refinement**: Only shift to occurrences where the character before the suffix differs from the mismatched character

**Example**: Pattern "ABCXXABC"
- Naive good suffix: "BC" appears at position 1 and 6
- Strong rule: If mismatch at position 4, don't shift to position 1 (same character 'X' would mismatch again)

**Benefit**: Reduces redundant comparisons, improves average case

## Algorithm Phases

### Phase 1: Preprocessing

**Bad Character Table Construction**: O(m + σ)
```
Initialize all badChar[c] = -1
for j = 0 to m-1:
    badChar[pattern[j]] = j
```

**Good Suffix Table Construction**: O(m)
- More complex: requires two passes
- First pass: compute border positions (similar to KMP failure function)
- Second pass: fill goodSuffix[] array

**Total preprocessing**: O(m + σ)

### Phase 2: Matching

**Pseudocode**:
```
shift = 0
while shift <= n - m:
    j = m - 1  // start from rightmost position

    while j >= 0 and pattern[j] == text[shift + j]:
        j = j - 1  // scan right to left

    if j < 0:
        report match at position shift
        shift += goodSuffix[0]  // shift to next possible match
    else:
        // Mismatch at position j
        bcShift = j - badChar[text[shift + j]]
        gsShift = goodSuffix[j]
        shift += max(bcShift, gsShift, 1)  // take maximum shift
```

**Key features**:
- Right-to-left scanning within each alignment
- Both heuristics computed, maximum used
- Can skip multiple positions on mismatch

## Complexity Analysis

### Time Complexity

**Preprocessing**: O(m + σ)
- Bad character: O(m + σ) (initialize array + scan pattern)
- Good suffix: O(m) (two passes over pattern)

**Matching Best Case**: O(n/m) - **SUBLINEAR**

**When**: Character in text doesn't appear in pattern
**Example**: Pattern "NEEDLE", Text "SSSSSSSS..."
- Each mismatch skips m positions
- Check only n/m positions

**This is Boyer-Moore's killer feature**: Only algorithm that's sublinear in the text length

**Matching Average Case**: O(n)

**Analysis**: For random text and pattern, expected comparisons ≈ 2n

**Empirical studies**: Often examines only n/m to n/2 characters in practice

**Matching Worst Case**: O(nm)

**When**: Highly repetitive text/pattern with late mismatches

**Example**: Pattern "AAAAAAB", Text "AAAAAAAA..."
```
Alignment 1: Match AAAAAA, mismatch at last character, shift 1
Alignment 2: Match AAAAAA, mismatch at last character, shift 1
...
O(n) alignments × O(m) comparisons each = O(nm)
```

**Mitigation**: Galil's optimization (don't re-compare matched suffix) → O(n) worst case

### Space Complexity

**O(m + σ)**: Pattern table + bad character table

**Trade-off for large alphabets**:
- Full Unicode (65,536 entries): Use hash table instead of array
- Reduces to O(m + k) where k = number of distinct characters in pattern

## Performance Characteristics

### Why Boyer-Moore Dominates in Practice

**1. Sublinear average case**: Examines fraction of text characters

**2. Large skips**: Bad character rule very effective on large alphabets
- English text: 26+ characters → Often skip 10-20 positions
- Binary data: 256 values → Can skip large chunks

**3. Right-to-left scanning**: Mismatches found quickly
- Most mismatches occur at end of pattern
- No wasted comparisons on early characters

**4. Cache-friendly**: Usually makes large jumps, but pattern is small (cache-resident)

### When Boyer-Moore Struggles

**Small alphabets** (DNA: 4 chars):
- Bad character heuristic less effective
- Frequent matches → More comparisons
- KMP can be competitive

**Short patterns** (< 5 characters):
- Preprocessing overhead not amortized
- Naive algorithm may be faster (simpler code, better branch prediction)

**Highly repetitive text** (logs, structured data):
- Worst-case O(nm) behavior more likely
- Good suffix rule helps but not always enough

## Variants and Optimizations

### Boyer-Moore-Horspool (BMH)

**Simplification**: Uses only bad character rule (ignores good suffix)

**Trade-offs**:
- Simpler implementation (no good suffix table)
- Still O(nm) worst case
- Average case: O(n) (slightly worse constant than full BM)

**Usage**: Most practical implementations (simpler, still very fast)

**Example**: Python's `str.find()`, many stdlib implementations use BMH

### Boyer-Moore-Sunday

**Modification**: On mismatch, look at character *after* current alignment

**Benefit**: Can make larger skips in some cases

**Example**:
```
Text:    ABCDEFGH
Pattern: XYZ

BM:  Shifts based on 'A' (in alignment)
Sunday: Shifts based on 'D' (after alignment)
If 'D' not in pattern, can skip further
```

### Boyer-Moore with Galil's Rule

**Addition**: Track matched suffix, don't re-compare it on next alignment

**Benefit**: Reduces worst-case from O(nm) to O(n)

**Cost**: More bookkeeping, slightly slower average case

**Usage**: Rarely implemented (worst case uncommon in practice)

### Tuned Boyer-Moore

**Combined optimizations**:
- Use BMH for simplicity
- Fallback to naive for very short patterns (< 3 characters)
- Use memchr() for single-character search
- SIMD for scanning (check multiple positions simultaneously)

**Example**: Rust's `memchr` crate uses SIMD BMH

## Implementation Considerations

### Alphabet Size Handling

**Small alphabet** (< 256 characters):
- Use array for bad character table: `badChar[256]`
- Fast O(1) lookup

**Large alphabet** (Unicode):
- Option 1: Hash table (O(1) average lookup)
- Option 2: Sparse array (only store present characters)
- Option 3: Ignore bad character rule (use only good suffix)

### Unicode and Multi-byte Encodings

**Challenge**: Pattern matching at byte level vs character level

**Byte-level BM**:
- Fast (no decoding)
- Works for ASCII, UTF-8 (if pattern and text same encoding)
- Risk: False matches on partial multi-byte sequences

**Character-level BM**:
- Correct for Unicode
- Requires decoding (slower)
- Bad character table size: 65,536 entries or hash table

**Best practice**: UTF-8 byte-level usually works if pattern is also UTF-8

### Case-Insensitive Search

**Approach 1**: Convert text and pattern to lowercase
- Simple but doubles memory usage

**Approach 2**: Modify comparison to use case-folding
- More complex, but no extra memory

**Approach 3**: Build bad character table with lowercase mapping
- Best of both worlds

## Comparison with Other Algorithms

### vs KMP

**BM advantages**:
- Much faster average case (O(n/m) vs O(n))
- Practical choice for most text search

**KMP advantages**:
- Guaranteed O(n) (no worst case slowdown)
- Better for small alphabets
- Streaming-friendly (no backtracking)

### vs Aho-Corasick

**AC advantages**:
- Multiple patterns in one pass
- O(n + m + z) regardless of pattern count

**BM advantages**:
- Single pattern: BM faster (simpler, better constants)
- Can run BM k times faster than AC if k < 10

### vs Rabin-Karp

**BM advantages**:
- No hash collisions to handle
- Deterministic performance
- Generally faster

**RK advantages**:
- Simpler implementation
- Multiple patterns with same hash (somewhat competitive with BM)
- Rolling hash useful for other problems

## Real-World Usage

### Where Boyer-Moore is Used

**grep/ag/ripgrep**: Fast text search tools
- Often BMH or tuned variants
- ripgrep: Hybrid (BM + SIMD)

**Text editors**: Sublime Text, Notepad++
- Interactive search needs fast average case
- Patterns typically have high alphabet diversity

**Databases**: String search in indexes
- MySQL, PostgreSQL internal string search

**Operating systems**: String search in kernels
- glibc `strstr()` uses Two-Way (BM-related)

### Implementation Examples

**glibc memmem()**: Two-Way algorithm (O(n), O(1) space)
- Related to BM, uses critical factorization
- Better worst-case than BM, comparable average case

**Python str.find()**: BMH variant
- Simple, fast for typical use cases

**Rust memchr**: SIMD-optimized BMH
- Uses AVX2/SSE to check multiple positions

## Theoretical Insights

**Optimality**: O(n/m) is optimal for comparison-based search
- Cannot do better without additional structure

**Lower bound**: Any algorithm must examine at least n/m characters in worst case
- BM achieves this bound

**Practical optimality**: BM often fastest despite O(nm) worst case
- Worst case rare in natural text

## Key Takeaways

**Strengths**:
- Sublinear average case O(n/m)
- Very fast for large alphabets
- Simple variants (BMH) easy to implement
- Industry standard for single-pattern search

**Weaknesses**:
- O(nm) worst case (pathological inputs)
- Worse than KMP for small alphabets
- Preprocessing overhead for short patterns
- Complex good suffix rule (often omitted)

**Best for**:
- Large alphabets (English, Unicode, binary)
- Interactive search (text editors)
- General-purpose text search
- When average case matters more than worst case

**Not best for**:
- Small alphabets (DNA: 4 chars → use KMP)
- Multiple patterns (use Aho-Corasick)
- Streaming (text backtracking possible)
- Hard real-time (unpredictable worst case)
