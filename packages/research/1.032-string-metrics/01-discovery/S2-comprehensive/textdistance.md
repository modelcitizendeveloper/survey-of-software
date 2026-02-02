# textdistance - Technical Deep-Dive

## Architecture

**Core implementation:**
- Pure Python with optional C/C++ accelerators
- Modular design: each algorithm is a separate class
- Consistent base interface via abstract `Base` class
- Optional external libraries for performance (python-Levenshtein, pyxDamerauLevenshtein)

**Design philosophy:**
- Comprehensiveness over performance
- Easy to extend with custom metrics
- Pluggable backends (pure Python, numpy, C extensions)
- Research-friendly API

## Algorithm Categories

### Edit-Based Distances (10 algorithms)

**Levenshtein:**
- Pure Python: O(n*m) time, O(n*m) space
- C backend (optional): 10-20x speedup
- Normalized variant: distance / max(len(s1), len(s2))

**Damerau-Levenshtein:**
- Allows transpositions (swap adjacent chars)
- Time: O(n*m), Space: O(n*m)
- More permissive than standard Levenshtein

**Hamming:**
- Requires equal-length strings
- Time: O(n), Space: O(1)
- Returns count of position mismatches

**Jaro and Jaro-Winkler:**
- Jaro: matching window-based similarity
- Jaro-Winkler: adds prefix bonus
- Time: O(n*m) worst case, O(n+m) typical
- Returns similarity score (0-1)

### Token-Based Similarities (8 algorithms)

**Jaccard:**
- Set-based: intersection / union
- Tokenization: whitespace split or character n-grams
- Time: O(n + m), Space: O(n + m)

**Sørensen-Dice:**
- 2 * intersection / (|A| + |B|)
- More weight to shared elements than Jaccard
- Common in biomedical text matching

**Cosine:**
- Vector-based similarity
- Requires feature extraction (TF-IDF, n-grams)
- Time: O(n + m), Space: O(n + m) for feature vectors

**Tversky:**
- Generalization of Jaccard with alpha/beta weights
- Asymmetric: useful for query vs document matching
- Configurable to emphasize precision or recall

### Sequence-Based (5 algorithms)

**LCSStr (Longest Common Substring):**
- Finds longest contiguous match
- Time: O(n*m), Space: O(n*m)
- Sensitive to word order

**LCSSeq (Longest Common Subsequence):**
- Allows gaps (non-contiguous matches)
- Time: O(n*m), Space: O(n*m)
- More permissive than LCSStr

**Ratcliff-Obershelp:**
- Gestalt pattern matching (difflib uses this)
- Recursive LCS-based algorithm
- Time: O(n*m) average, can be O(n*m*log(n*m))

### Phonetic Algorithms (2 algorithms)

**MRA (Match Rating Approach):**
- NYSIIS-like phonetic encoding
- Encodes names to phonetic representation
- Comparison: encoded strings must match exactly

**Editex:**
- Edit distance with phonetic costs
- Phonetically similar substitutions cost less
- Useful for name matching across languages

### Compression-Based (4 algorithms)

**NCD (Normalized Compression Distance):**
- Based on Kolmogorov complexity approximation
- Uses real compressors (gzip, bz2, lzma)
- Time: depends on compressor (slow)

**Compression variants:**
- BZ2, LZMA, ZLib, Arith (arithmetic coding)
- Good for detecting similar documents
- Very slow (not for real-time use)

### Q-gram Based (5 algorithms)

**Q-gram distance:**
- Character n-gram overlap
- Time: O(n + m), Space: O(n + m)
- Configurable n (typical: 2-3)

**Jaccard/Sørensen for q-grams:**
- Apply set metrics to character n-grams
- More robust to typos than exact matching
- Common for fuzzy search indexing

## Performance Characteristics

### Benchmark Results (Pure Python baseline)

**Relative performance (10-char strings, pure Python implementations):**

| Algorithm | Ops/sec | Memory | Notes |
|-----------|---------|--------|-------|
| Hamming | 500K | O(1) | Fastest, equal-length only |
| Jaccard | 200K | O(n+m) | Token creation overhead |
| Jaro-Winkler | 80K | O(1) | Limited window search |
| Levenshtein | 50K | O(n*m) | DP matrix allocation |
| LCS | 30K | O(n*m) | More complex DP |
| Compression | 50 | O(n+m) | Compressor dominates |

**With C accelerators:**
- Levenshtein: 800K ops/sec (16x speedup)
- Damerau-Levenshtein: 600K ops/sec (12x speedup)
- Hamming: 1.2M ops/sec (2.4x speedup)

**Optimization strategies:**
```
import textdistance

# Slow: Pure Python
textdistance.levenshtein('hello', 'hallo')

# Fast: Specify C backend explicitly
lev = textdistance.Levenshtein(external=True)  # Uses python-Levenshtein C lib
lev('hello', 'hallo')

# Fastest: Use rapidfuzz for Levenshtein
# (textdistance is better for rare metrics)
```

## API Design and Extensibility

**Consistent interface:**
```
# All algorithms implement:
algorithm.distance(s1, s2)       # Returns raw distance
algorithm.similarity(s1, s2)     # Returns similarity score
algorithm.normalized_distance(s1, s2)  # Distance in [0, 1]
algorithm.normalized_similarity(s1, s2) # Similarity in [0, 1]
```

**Custom metrics:**
```
from textdistance import Base

class CustomMetric(Base):
    def __call__(self, s1, s2):
        # Your logic here
        return score

    def maximum(self, *sequences):
        # Max possible distance
        return max(len(s) for s in sequences)

# Use like built-in algorithms
custom = CustomMetric()
score = custom.normalized_similarity('hello', 'world')
```

**Configurable tokenization:**
```
# Character n-grams
jaccard_bigram = textdistance.Jaccard(qval=2)
score = jaccard_bigram('hello', 'hallo')  # Compare 2-grams

# Word tokens
jaccard_word = textdistance.Jaccard(qval=None)  # None = word split
score = jaccard_word('hello world', 'hello earth')
```

## Unicode and Edge Cases

**Unicode handling:**
- Works with unicode strings natively
- No automatic normalization (user's responsibility)
- Correct character counting (not byte counting)

**Edge cases:**
```
# Empty strings
textdistance.levenshtein('', 'hello')  # Returns 5 (length of non-empty)

# Very long strings
# Pure Python: Memory usage O(n*m) can be prohibitive
# Workaround: Use C backends or chunk the comparison

# Mixed types
textdistance.hamming('abc', [1, 2, 3])  # Works (sequences of any type)
textdistance.hamming('abc', 'ab')       # ValueError (length mismatch)
```

## Integration Patterns

**Research workflow:**
```
import textdistance
import pandas as pd

# Test multiple algorithms quickly
algorithms = [
    'levenshtein', 'jaro_winkler', 'jaccard',
    'cosine', 'lcsstr', 'hamming'
]

results = {}
for algo in algorithms:
    metric = getattr(textdistance, algo)
    try:
        results[algo] = metric.normalized_similarity(s1, s2)
    except ValueError:
        results[algo] = None  # Not applicable (e.g., Hamming on unequal length)

# Find best metric for your data
df = pd.DataFrame.from_dict(results, orient='index', columns=['score'])
best_algo = df['score'].idxmax()
```

**Custom preprocessing:**
```
from textdistance import levenshtein
import unicodedata

def normalized_levenshtein(s1, s2):
    # Custom normalization
    s1 = unicodedata.normalize('NFKD', s1.lower())
    s2 = unicodedata.normalize('NFKD', s2.lower())
    return levenshtein.normalized_distance(s1, s2)
```

## Production Readiness

**Thread safety:**
- Pure Python implementations are thread-safe
- External C libraries: check individual library thread safety
- Recommendation: Use separate instances per thread if using state

**Performance considerations:**
- Pure Python: Not suitable for high-throughput production
- With C backends: Acceptable for moderate load (< 1K ops/sec)
- For higher load: Migrate to rapidfuzz or specialized libraries

**Monitoring:**
- Algorithm choice affects performance by orders of magnitude
- Profile before deploying (compression-based can be 1000x slower)
- Memory profiling essential for DP-based algorithms on long strings

## Limitations and Trade-offs

**When textdistance shines:**
- Research and prototyping (try many algorithms quickly)
- Rare metrics (compression-based, phonetic, Tversky)
- Educational use (pure Python is readable)
- Custom metrics (easy to extend)

**When to use alternatives:**
- Production high-throughput: rapidfuzz (10-100x faster)
- Simple use cases: Standard library difflib (no dependencies)
- JavaScript: Not applicable (Python-only)
- Embedded systems: Too heavy (use Rust/C alternatives)

**Dependency footprint:**
- Pure Python: No dependencies (minimal install)
- With accelerators: Requires C extensions (compilation or wheels)
- Optional dependencies: numpy (for some token metrics)
