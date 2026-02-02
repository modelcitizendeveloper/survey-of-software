# S2 Technical Recommendation

## Performance-First Decision Tree

```
High throughput needed (>10K ops/sec)?
├─ YES → C++/Rust implementations
│  ├─ Python: rapidfuzz (C++ core, 400K ops/sec)
│  ├─ Rust: strsim (native performance, memory safe)
│  └─ Java: Apache Commons + JIT optimization
│
└─ NO → Pure-language implementations acceptable
   ├─ Python: textdistance (readable, flexible)
   ├─ JavaScript: string-similarity (lightweight)
   └─ Consider trade-off: dev speed vs runtime speed
```

## Algorithm Selection by Use Case

### Fuzzy Name Matching
**Recommended:** Jaro-Winkler
- Designed for personal names
- Prefix bonus helps with common prefixes
- Normalized score (0-1) is intuitive

**Implementation:**
- Python production: `rapidfuzz.jaro_winkler_similarity()`
- Research: `textdistance.jaro_winkler()`
- JavaScript: Use external library (string-similarity doesn't have it)

### Typo Tolerance in Search
**Recommended:** Levenshtein with threshold
- Single typos = distance 1-2
- Threshold optimization for speed
- Well-understood behavior

**Implementation:**
```python
from rapidfuzz import fuzz

# Autocomplete with typo tolerance
def fuzzy_autocomplete(query, candidates, max_distance=2):
    return [
        c for c in candidates
        if fuzz.distance(query, c, score_cutoff=max_distance) <= max_distance
    ]
```

### Duplicate Detection
**Recommended:** Token-based metrics (token_set_ratio, Jaccard)
- Robust to word reordering
- Handles partial matches
- Less sensitive to minor variations

**Example:**
```python
from rapidfuzz import fuzz

# Duplicate detection with token-based matching
def is_duplicate(s1, s2, threshold=85):
    return fuzz.token_set_ratio(s1, s2) >= threshold
```

### Document Similarity
**Recommended:** Cosine similarity on TF-IDF vectors
- Better for long texts
- Captures semantic similarity
- Standard in IR

**Implementation:**
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# For long documents
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(documents)
similarity_matrix = cosine_similarity(vectors)
```

### Genomic/Bioinformatics
**Recommended:** Specialized edit distance with custom costs
- Nucleotide/amino acid specific costs
- Gap penalties
- Banded alignment for long sequences

**Consider:** Dedicated libraries (BioPython) over general string metrics

## Optimization Strategies

### Threshold-Based Early Termination

**Scenario:** Filtering candidates where distance must be < k

```python
from rapidfuzz import fuzz

# Slow: Compute all distances
distances = [fuzz.distance(query, c) for c in candidates]
matches = [c for c, d in zip(candidates, distances) if d < 5]

# Fast: Early termination
matches = [
    c for c in candidates
    if fuzz.distance(query, c, score_cutoff=4) < 5
]
# ~3-5x speedup when threshold filters most candidates
```

### Preprocessing and Caching

**Scenario:** Comparing one string against many candidates

```python
from rapidfuzz import process

# Inefficient: Linear scan every time
for query in queries:
    results = [compare(query, c) for c in candidates]

# Efficient: Use process.extract() with preprocessing
from rapidfuzz import process, fuzz

# Candidates are preprocessed once
results = process.extract(
    query,
    candidates,
    scorer=fuzz.ratio,
    limit=10
)
```

### Parallel Processing

**When:** Batch comparisons, multi-core available

```python
from rapidfuzz import process, fuzz
from concurrent.futures import ProcessPoolExecutor

# Single-threaded
results = [process.extractOne(q, candidates) for q in queries]

# Multi-process (scales to core count)
with ProcessPoolExecutor() as executor:
    results = list(executor.map(
        lambda q: process.extractOne(q, candidates, scorer=fuzz.WRatio),
        queries
    ))
```

**Speedup:** ~4x on 8-core CPU for independent comparisons

### Indexing for Large Datasets

**Problem:** O(n) scan over 1M+ candidates

**Solution:** BK-tree or similar metric indexing

```python
# Concept: Index candidates in BK-tree for sub-linear search
# Not built into rapidfuzz, use pybktree

from pybktree import BKTree
from rapidfuzz import fuzz

# Build index (one-time cost)
tree = BKTree(fuzz.distance, candidates)

# Query with distance threshold
matches = tree.find(query, max_distance=2)
# Typically 10-100x faster than linear scan
```

## Unicode Normalization Patterns

**Problem:** "café" vs "café" (composed vs decomposed)

**Solution:** Normalize before comparison

```python
import unicodedata
from rapidfuzz import fuzz

def normalized_similarity(s1, s2, form='NFKD'):
    s1_norm = unicodedata.normalize(form, s1.lower())
    s2_norm = unicodedata.normalize(form, s2.lower())
    return fuzz.ratio(s1_norm, s2_norm)
```

**Forms:**
- **NFC:** Composed characters (default for most text)
- **NFD:** Decomposed (useful for accent-insensitive matching)
- **NFKC/NFKD:** Compatibility forms (normalize ligatures, stylistic variants)

## Performance Profiling Template

```python
import time
from rapidfuzz import fuzz

# Benchmark template
def benchmark(scorer, pairs, iterations=1000):
    start = time.perf_counter()
    for _ in range(iterations):
        for s1, s2 in pairs:
            _ = scorer(s1, s2)
    elapsed = time.perf_counter() - start
    ops_per_sec = (iterations * len(pairs)) / elapsed
    return ops_per_sec

# Test different algorithms
results = {
    'levenshtein': benchmark(fuzz.distance, test_pairs),
    'jaro_winkler': benchmark(fuzz.jaro_winkler_similarity, test_pairs),
    'token_set': benchmark(fuzz.token_set_ratio, test_pairs),
}

print(f"Levenshtein: {results['levenshtein']:,.0f} ops/sec")
```

## Memory Profiling

```python
import tracemalloc
from rapidfuzz import fuzz

# Memory usage pattern
def profile_memory(scorer, s1, s2):
    tracemalloc.start()

    # Baseline
    baseline = tracemalloc.get_traced_memory()[0]

    # Run comparison
    _ = scorer(s1, s2)

    # Peak usage
    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()

    return (peak - baseline) / 1024  # KB

# Test with different string lengths
for length in [10, 100, 1000, 10000]:
    s = "a" * length
    mem_kb = profile_memory(fuzz.distance, s, s)
    print(f"Length {length}: {mem_kb:.1f} KB")
```

## Integration Best Practices

### Django ORM Pattern

```python
# Anti-pattern: Load all records, compare in Python
all_names = Person.objects.values_list('name', flat=True)
matches = [n for n in all_names if fuzz.ratio(query, n) > 80]

# Better: Pre-filter with DB, fuzzy-match smaller set
candidates = Person.objects.filter(
    name__istartswith=query[:2]  # Trigram/prefix index
).values_list('name', flat=True)[:1000]  # Limit candidates

matches = [n for n in candidates if fuzz.ratio(query, n) > 80]
```

### FastAPI Caching Pattern

```python
from fastapi import FastAPI
from functools import lru_cache
from rapidfuzz import process, fuzz

app = FastAPI()

@lru_cache(maxsize=1)
def get_candidates():
    # Load candidates once, cache in memory
    return load_products_from_db()

@app.get("/search/{query}")
def search(query: str, limit: int = 10):
    candidates = get_candidates()
    results = process.extract(
        query,
        candidates,
        scorer=fuzz.WRatio,
        limit=limit
    )
    return [{"name": r[0], "score": r[1]} for r in results]
```

### React Client Pattern

```javascript
import stringSimilarity from 'string-similarity';

// Debounced autocomplete
function useAutocomplete(query, items, debounceMs = 300) {
  const [matches, setMatches] = useState([]);

  useEffect(() => {
    const timer = setTimeout(() => {
      if (query.length < 2) {
        setMatches([]);
        return;
      }

      const scored = items.map(item => ({
        item,
        score: stringSimilarity.compareTwoStrings(query, item)
      }));

      const filtered = scored
        .filter(x => x.score > 0.3)
        .sort((a, b) => b.score - a.score)
        .slice(0, 10);

      setMatches(filtered);
    }, debounceMs);

    return () => clearTimeout(timer);
  }, [query, items]);

  return matches;
}
```

## When to Build Custom Implementations

**Consider custom implementation if:**
- Existing libraries don't support your language/platform
- Need domain-specific edit costs (bioinformatics, chemistry)
- Performance requirements exceed available libraries
- License constraints (all major libraries are MIT/Apache)

**Algorithm complexity to expect:**
- Levenshtein: ~50-100 lines for naive O(n*m)
- Jaro-Winkler: ~80-120 lines
- Optimizations (SIMD, banded DP): 500+ lines, high bug risk

**Recommendation:** Use existing libraries unless strong justification for custom implementation.
