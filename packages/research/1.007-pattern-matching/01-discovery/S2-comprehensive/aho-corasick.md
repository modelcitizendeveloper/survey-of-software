# Aho-Corasick Algorithm

## Core Mechanism

**Central insight**: Build a single finite automaton (trie + failure links) that can match all patterns simultaneously in one pass through the text.

**Key innovation**: Combines:
1. **Trie** (prefix tree) to share common prefixes among patterns
2. **KMP-style failure links** to avoid backtracking on mismatch
3. **Output links** to report all matches at current position

**Result**: O(n + m + z) time where z = number of matches (output size)

## Data Structures

### 1. Trie (Prefix Tree)

**Structure**: Tree where each edge represents a character, root-to-leaf paths spell patterns

**Example**: Patterns ["he", "she", "his", "hers"]
```
        (root)
        /    \
       h      s
      / \      \
     e   i      h
          \      \
           s      e
                   \
                    r
                     \
                      s
```

**Properties**:
- Root represents empty string
- Each node can have up to σ children (σ = alphabet size)
- Leaf nodes (and some internal nodes) mark pattern endings

**Space**: O(m × σ) worst case, where m = total length of all patterns
- Worst case: No shared prefixes (m nodes × σ pointers)
- Best case: O(m) when all patterns share prefix

### 2. Failure Links (Suffix Links)

**Purpose**: When no matching child exists, follow failure link to longest proper suffix that's in the trie

**Analogy**: Like KMP's failure function, but for trie nodes instead of pattern positions

**Example**: Patterns ["she", "he", "hers"]
```
Node spelling "she" has failure link to node "he"
Node spelling "he" has failure link to root
Node spelling "her" has failure link to root (no suffix "er" in trie)
```

**Construction**: BFS traversal, similar to KMP failure function
```
For each node at depth d:
    Find longest suffix that's also a prefix in trie
    Set failure link to that node
    Inherit output links from failure link target
```

**Space**: O(m) - one link per trie node

### 3. Output Links

**Purpose**: Report all patterns that end at current node (including those found via failure links)

**Example**: Node spelling "she"
- Direct match: "she"
- Via failure link to "he": "he"
- Output list: ["she", "he"]

**Optimization**: Chain output links instead of storing full lists
- Node "she" → output "she", link to node "he"
- Node "he" → output "he", link to root
- Follow chain to report all matches

**Space**: O(m) - one link per trie node

## Algorithm Phases

### Phase 1: Build Trie

**Time**: O(m) where m = total pattern length

**Pseudocode**:
```
root = new TrieNode()
for each pattern p:
    node = root
    for each character c in p:
        if node.children[c] doesn't exist:
            node.children[c] = new TrieNode()
        node = node.children[c]
    node.isEndOfPattern = true
    node.patternId = id of p
```

**Result**: Trie with all patterns inserted, no failure links yet

### Phase 2: Build Failure Links (BFS)

**Time**: O(m × σ) worst case, O(m) typical

**Pseudocode**:
```
queue = empty
for each child of root:
    child.failureLink = root
    queue.enqueue(child)

while queue not empty:
    node = queue.dequeue()
    for each child of node:
        walk = node.failureLink
        while walk != null and walk.children[c] doesn't exist:
            walk = walk.failureLink
        if walk != null:
            child.failureLink = walk.children[c]
        else:
            child.failureLink = root
        queue.enqueue(child)
```

**Key**: Each node's failure link computed once, BFS ensures dependencies satisfied

### Phase 3: Matching

**Time**: O(n + z) where n = text length, z = output size

**Pseudocode**:
```
node = root
for each character c in text:
    while node != root and node.children[c] doesn't exist:
        node = node.failureLink  // follow failure link

    if node.children[c] exists:
        node = node.children[c]

    if node.isEndOfPattern:
        report match(es) at this position
        follow output links to report all matches
```

**Key properties**:
- Text scanned once, left to right
- Failure links prevent backtracking in text
- Each character examined O(1) times (amortized)

### Example Execution

**Patterns**: ["he", "she", "his", "hers"]
**Text**: "ushers"

```
Position 0 (u): No match, stay at root
Position 1 (s): Transition to 's' node
Position 2 (h): Transition to 'h' (child of 's')
Position 3 (e): Transition to 'e' (child of 'h')
    → Match "she" (direct)
    → Follow output link to "he", match "he"
Position 4 (r): No 'r' child, follow failure link
    → End up at 'h' node
    → Transition to 'r' (child of 'h')
Position 5 (s): Transition to 's' (child of 'r')
    → Match "hers"
```

**Matches found**: "she" at position 1, "he" at position 2, "hers" at position 3

## Complexity Analysis

### Time Complexity

**Preprocessing**: O(m × σ) worst case, O(m) typical
- Trie construction: O(m)
- Failure link construction: O(m) amortized (each node visited once, failure links followed ≤ m times total)

**Matching**: O(n + z)
- Text scanning: O(n) - each character examined once
- Output reporting: O(z) - proportional to matches found

**Total**: O(m + n + z) - **linear in input + output**

**Key insight**: Running time independent of number of patterns (after preprocessing)

### Space Complexity

**Trie nodes**: O(m) nodes in worst case (no shared prefixes)

**Trie edges**: O(m × σ) worst case
- Each node can have σ children (alphabet size)
- Dense representation: Array of size σ per node → O(m × σ)
- Sparse representation: Hash table per node → O(m + edges)

**Failure/output links**: O(m) - one per node

**Total**:
- Dense: O(m × σ) - problematic for large alphabets (Unicode: 65K)
- Sparse: O(m) - typical for most practical use cases

### Amortized Analysis

**Why O(n) matching is not obvious**:
- Inner while loop follows failure links
- Could seem like O(n × m) total

**Amortization argument**:
- Each failure link decreases depth in trie
- Depth can increase by at most 1 per character (single edge traversal)
- Total depth increase: ≤ n
- Total depth decrease (via failure links): ≤ n
- Therefore, total failure link traversals: O(n)

## Performance Characteristics

### When Aho-Corasick Excels

**Many patterns** (100-1,000,000):
- Single pass finds all patterns
- Running single-pattern BM k times: O(k × n) → Infeasible for large k
- AC: O(n + z) regardless of k

**Shared prefixes**:
- Patterns like ["test", "testing", "tester", "tests"]
- Trie shares prefix "test", saves space and time

**Streaming text**:
- Processes text online (character by character)
- No buffering needed
- Natural fit for network packets, logs

### When Aho-Corasick Struggles

**Few patterns** (< 10):
- Preprocessing overhead not amortized
- Running BM 5-10 times may be faster
- Trie construction more complex than BM tables

**Large alphabets with sparse trie**:
- Unicode (65,536 characters): Dense representation infeasible
- Must use sparse (hash table) representation
- Slower lookups than array indexing

**Long patterns with little overlap**:
- Patterns: ["XABC", "YDEF", "ZFGH"] (no shared prefixes)
- Trie doesn't save space
- BM's sublinear average case might win

## Variants and Optimizations

### Space Optimizations

**Compressed trie** (radix tree):
- Merge single-child chains into one edge
- Example: "test" → "testing" becomes single edge labeled "ing"
- Reduces nodes but complicates lookup

**Double-array trie**:
- Compact representation using two arrays
- O(m) space with fast array lookups
- Complex construction algorithm

**Hash table children**:
- Replace array[σ] with hash table
- Saves space for large alphabets
- Slightly slower lookup (hash vs array index)

### Performance Optimizations

**SIMD-parallel transition**:
- Check multiple characters in parallel
- Hyperscan uses this extensively

**Minimized DFA**:
- Convert NFA (trie + failure links) to equivalent DFA
- Larger but faster (no failure link traversals)
- Trade space for speed

**Hybrid approaches**:
- Use AC for patterns with shared prefixes
- Use separate BM for patterns with unique prefixes
- Best of both worlds

### Commentz-Walter Algorithm

**Combination**: Aho-Corasick + Boyer-Moore ideas

**Approach**:
- Build AC trie for reversed patterns
- Scan text right-to-left like BM
- Use bad character rule to skip

**Benefit**: Can achieve sublinear performance O(n/m) for multiple patterns

**Complexity**: More complex implementation, used in specialized tools

## Implementation Considerations

### Alphabet Size

**Small alphabet** (DNA: 4, ASCII: 128):
- Use array for children: fast O(1) lookup
- Space manageable: 128 × 8 bytes = 1 KB per node

**Large alphabet** (Unicode: 65,536):
- Must use hash table or sparse representation
- Or restrict to subset (e.g., only handle ASCII portion)

### Memory Layout

**Cache-friendly layout**:
- Pack frequently-accessed fields together
- Align structures to cache line boundaries
- Prefetch next nodes during traversal

**Example**: Hyperscan uses compressed structures optimized for x86 cache

### Unicode Handling

**Code unit vs code point**:
- UTF-8: Match on bytes (code units) - simple, fast
- UTF-16/32: Match on code points - correct for Unicode properties

**Normalization**:
- Unicode has multiple representations (é = e + ´ or single codepoint)
- Normalize patterns and text for consistent matching

### Case Sensitivity

**Case-insensitive matching**:
- Option 1: Lowercase all patterns and text
- Option 2: Expand trie with both cases ('a' and 'A' children)
- Option 3: Custom comparison during traversal

**Trade-offs**: Space (option 2 doubles nodes) vs time (option 3 slower comparisons)

## Real-World Usage

### Security Applications

**ClamAV (antivirus)**:
- Millions of virus signatures
- AC automaton with optimizations
- Must scan file once for all signatures

**Snort/Suricata (IDS)**:
- Network packet inspection
- Thousands of attack signatures
- Hyperscan (optimized AC) for multi-gigabit speeds

**Web Application Firewalls**:
- AWS WAF, Cloudflare: Block malicious patterns
- SQL injection signatures, XSS patterns
- AC for fast multi-pattern matching

### Text Processing

**Keyword extraction**:
- Find multiple keywords in documents
- NLP preprocessing pipelines
- Python flashtext library (optimized AC variant)

**Log analysis**:
- Grep for multiple error patterns
- Elasticsearch: Multiple search terms
- Stream processing (Kafka consumers)

### Bioinformatics

**Motif finding**:
- Search DNA/protein sequences for known motifs
- Multiple patterns (binding sites, domains)
- AC often faster than BLAST for exact matching

## Comparison with Other Algorithms

### vs Running Boyer-Moore k Times

**AC advantages**:
- O(n + z) regardless of k (BM: O(k × n))
- When k > 10, AC usually faster
- Single pass over text (better cache locality)

**BM advantages**:
- Simpler implementation
- When k < 10, BM often competitive
- Sublinear average case (AC is always linear)

**Break-even point**: ~5-20 patterns depending on implementation

### vs KMP on Each Pattern

**AC is strictly better**:
- Same O(n + m) complexity
- But shared prefixes make AC faster
- AC specifically designed for multi-pattern

### vs Rabin-Karp Multiple Pattern

**AC advantages**:
- No hash collisions to handle
- Deterministic performance
- Generally faster

**RK advantages**:
- Simpler to implement
- Can handle wildcards more easily
- Lower space usage

### vs Suffix Trees/Arrays

**Suffix structures advantages**:
- Preprocess text once, search many patterns
- O(m + occ) per pattern search

**AC advantages**:
- Preprocess patterns, scan text once
- Better when patterns fixed, text changes

**Use cases differ**:
- AC: Fixed patterns, streaming text (IDS, logs)
- Suffix trees: Fixed text, varying patterns (genome databases)

## Theoretical Insights

**Optimality**: O(n + m + z) is optimal for reporting all matches
- Must read text: O(n)
- Must read patterns: O(m)
- Must output matches: O(z)

**Automaton view**: AC builds a DFA that recognizes all patterns
- States = trie nodes
- Failure links = ε-transitions
- Can be minimized like any DFA

**Failure link structure**: Forms a tree (failure tree)
- Root of failure tree = root of trie
- Each node points to ancestor (proper suffix)

## Extensions

### AC with wildcards**:
- Extend trie to handle "don't care" characters
- Multiple transitions from same node

### Approximate AC**:
- Allow k mismatches
- Exponentially increases automaton size
- Practical for small k

### AC with constraints**:
- Example: Match patterns only at word boundaries
- Augment automaton with additional state

## Key Takeaways

**Strengths**:
- Optimal O(n + m + z) for multi-pattern
- Single pass through text
- Scales to millions of patterns
- Industry standard for security (IDS, antivirus)

**Weaknesses**:
- Preprocessing overhead for few patterns
- Large space usage for sparse patterns
- Always linear (no sublinear like BM)
- Complex implementation

**Best for**:
- Many patterns (10+, scales to millions)
- Security applications (IDS, malware scanning)
- Keyword extraction, log analysis
- Streaming data (online processing)

**Not best for**:
- Single pattern (use BM or KMP)
- Few patterns (< 10): BM may be faster
- Extremely large alphabets with sparse patterns
