# Knuth-Morris-Pratt (KMP) Algorithm

## Core Mechanism

**Central insight**: When a mismatch occurs, use information from the matched portion to skip positions that cannot possibly match.

**Key innovation**: The "failure function" (also called "prefix function" or "partial match table") precomputes how much of the pattern overlaps with itself, enabling smart skipping without backtracking in the text.

## Data Structures

### Failure Function

**Array**: `fail[0..m-1]` where m = pattern length

**Definition**: `fail[i]` = length of longest proper prefix of `pattern[0..i]` that is also a suffix

**Example**: Pattern "ABABAC"
```
Index:    0  1  2  3  4  5
Pattern:  A  B  A  B  A  C
fail[]:   0  0  1  2  3  0
```

**Interpretation**:
- `fail[4] = 3`: The first 3 characters "ABA" appear again at end of "ABABA"
- On mismatch at position 5, can skip to position 3 (reuse "ABA" match)

### Construction Algorithm

**Time**: O(m)
**Space**: O(m)

**Pseudocode logic**:
1. Initialize fail[0] = 0 (no proper prefix for single character)
2. For each position i from 1 to m-1:
   - Try to extend the longest matching prefix
   - If can't extend, follow failure links to find next best match
   - Record length in fail[i]

**Key property**: fail[] values are non-decreasing in expectation, making construction linear time

## Matching Algorithm

### Execution Flow

**Input**: Text T (length n), Pattern P (length m), failure function fail[]

**Output**: All positions where P occurs in T

**Pseudocode logic**:
```
j = 0  // position in pattern
for i = 0 to n-1:  // scan text left-to-right
    while j > 0 and T[i] != P[j]:
        j = fail[j-1]  // follow failure link
    if T[i] == P[j]:
        j = j + 1
    if j == m:
        report match at position i-m+1
        j = fail[j-1]  // continue searching
```

**Key properties**:
- Text pointer i never backtracks (always advances)
- Pattern pointer j can reset via failure links
- Each text character examined at most once

### Example Execution

**Text**: "ABABABAC"
**Pattern**: "ABABAC"
**fail[]**: [0, 0, 1, 2, 3, 0]

```
Step 1: T[0]=A, P[0]=A → match, j=1
Step 2: T[1]=B, P[1]=B → match, j=2
Step 3: T[2]=A, P[2]=A → match, j=3
Step 4: T[3]=B, P[3]=B → match, j=4
Step 5: T[4]=A, P[4]=A → match, j=5
Step 6: T[5]=B, P[5]=C → MISMATCH
        j = fail[4] = 3  (reuse "ABA" match)
        T[5]=B, P[3]=B → match, j=4
Step 7: T[6]=A, P[4]=A → match, j=5
Step 8: T[7]=C, P[5]=C → match, j=6 → MATCH at position 2
```

**Key observation**: At step 6, instead of starting over, KMP reuses the fact that "ABA" at T[3..5] matches P[0..2]

## Complexity Analysis

### Time Complexity

**Preprocessing**: O(m)
- Constructs failure function in linear time
- Each position processed once, with amortized constant work

**Matching**: O(n)
- Text pointer i makes n iterations (one per character)
- Pattern pointer j can decrease (via fail[]), but total decrease is bounded by total increase
- Amortized O(1) work per text character

**Total**: O(n + m) - optimal for pattern matching

### Space Complexity

**O(m)**: Only stores failure function array

**Memory access pattern**:
- Sequential access to text (excellent cache locality)
- Random access to fail[] (small array, usually cache-resident)
- Pattern access bounded by fail[] jumps

## Performance Characteristics

### Best Case: O(n/m)

**When**: Pattern has no self-overlap, text doesn't match pattern at all

**Example**: Pattern "ABCD", Text "EEEEEEEE"
- Can skip forward quickly after first mismatch

**Rare in practice**: KMP doesn't achieve sublinear like Boyer-Moore

### Average Case: O(n)

**Typical behavior**: ~1.5n to 2n character comparisons

**Analysis**: Most real-world patterns have some repetition but not extreme

### Worst Case: O(n + m)

**When**: Highly repetitive text and pattern

**Example**: Pattern "AAAAAAB", Text "AAAAAAA..."
- Many characters match before final mismatch
- But still linear (no backtracking in text)

**Key advantage over naive**: Naive would be O(nm) here, KMP stays O(n)

## Implementation Considerations

### Optimization Techniques

**1. Failure function refinement**:
- Standard fail[]: Computes longest prefix-suffix
- Optimized fail[]: Skip positions that would immediately fail again
- Example: Pattern "AAAAB", standard fail[] = [0,1,2,3,0]
  - At fail[3]=3, would check A vs B again (known to fail)
  - Optimized: follow chain until different character or 0

**2. Loop unrolling**:
- Unroll inner while loop for common cases (0, 1, 2 jumps)
- Reduces branch mispredictions

**3. SIMD preprocessing**:
- Can vectorize failure function construction for long patterns
- Marginal benefit (preprocessing is already O(m))

### Edge Cases

**Empty pattern**: Return all positions (or error, depending on spec)

**Pattern longer than text**: No matches (preprocessing still runs)

**Single-character pattern**: Degenerates to linear scan (fail[0]=0, no jumps)

**Unicode**: Works on any sequence; treat as array of code units or code points

## Comparison with Other Algorithms

### vs Naive (O(nm))

**KMP advantages**:
- Guaranteed O(n) vs O(nm)
- No text backtracking (better for streaming)

**Naive advantages**:
- Simpler code (no preprocessing)
- Better constant factors for short patterns (m < 5)
- Better branch prediction (simpler control flow)

### vs Boyer-Moore

**KMP advantages**:
- Predictable performance (no worst-case O(nm))
- Smaller space (O(m) vs O(m + σ))
- Better for small alphabets (DNA: 4 characters)

**BM advantages**:
- Much faster average case (O(n/m) vs O(n))
- Better for large alphabets (English, Unicode)
- More practical for most use cases

### vs Aho-Corasick

**AC is KMP generalization**:
- KMP is single-pattern, AC is multi-pattern
- Both use failure links to avoid backtracking
- AC builds trie instead of linear array

**When to use which**:
- Single pattern → KMP
- Multiple patterns → AC

## Real-World Usage

### Where KMP is Used

**Educational**: Standard algorithm in CS courses (CLRS, Sedgewick)
- Teaches prefix-suffix structure
- Demonstrates amortized analysis

**Specialized systems**:
- Real-time systems (predictable latency)
- Hardware implementations (simple, regular structure)
- DNA sequence matching (small alphabet, long patterns)

### Where KMP is NOT Used

**General text search**: Boyer-Moore variants are faster

**Production systems**: Libraries use BM or hybrid algorithms

**Text editors**: Usually naive or optimized naive (patterns short, interactive)

## Theoretical Significance

**Optimal linear time**: First algorithm to prove O(n+m) is achievable

**Amortization technique**: Classic example of amortized analysis (potential method)

**Automaton perspective**: KMP builds DFA for pattern, processes text in one pass

**Online algorithm**: Can process text as a stream (no need to buffer)

## Extensions and Variants

### KMP with wildcards
- Modify failure function to handle "don't care" characters
- Still O(n+m) time

### Multiple pattern KMP
- Build failure function for concatenated patterns
- Superseded by Aho-Corasick (more efficient)

### Two-Way algorithm
- Combines KMP with reverse KMP
- Better practical performance (used in glibc memmem())
- O(n+m) time, O(1) space

## Key Takeaways

**Strengths**:
- Optimal O(n+m) time complexity
- No backtracking in text (streaming-friendly)
- Predictable worst-case performance
- Small memory footprint O(m)

**Weaknesses**:
- Slower than Boyer-Moore in practice (average case)
- Preprocessing overhead for short patterns
- Doesn't achieve sublinear time

**Best for**:
- Small alphabets (DNA, binary)
- Streaming text (can't buffer)
- Hard real-time systems (predictable)
- Teaching/learning (classic algorithm)

**Not best for**:
- Interactive search (BM faster)
- Large alphabets (BM better)
- Multiple patterns (use AC)
