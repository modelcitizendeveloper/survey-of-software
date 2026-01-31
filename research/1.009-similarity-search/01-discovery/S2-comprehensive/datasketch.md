# datasketch: Technical Deep-Dive

## Architecture Overview

datasketch implements **probabilistic data structures** for similarity search using hashing-based algorithms:

- **MinHash** - Jaccard similarity estimation
- **LSH (Locality-Sensitive Hashing)** - Sub-linear similarity search
- **SimHash** - Near-duplicate detection
- **LSH Forest** - Dynamic LSH with adjustable precision
- **HyperLogLog** - Cardinality estimation (not similarity search)

**Core principle:** Trade exact results for massive speed/memory gains via probabilistic approximation

## MinHash: Jaccard Similarity Estimation

### Mathematical Foundation

**Jaccard similarity:**
```
J(A, B) = |A ∩ B| / |A ∪ B|
```
Range: 0 (disjoint) to 1 (identical)

**MinHash property:**
```
P(h_min(A) = h_min(B)) = J(A, B)
```
Where h_min(S) = element with minimum hash value in set S

**Key insight:** Probability of hash collision equals Jaccard similarity

### Algorithm

**Signature generation (k hash functions):**
```
For each hash function h_i (i = 1 to k):
    sig[i] = min(h_i(element) for element in set)
```

**Similarity estimation:**
```
J(A, B) ≈ (# of matching signature values) / k
```

**Error bound:**
- Standard error: ε = 1 / √k
- k=128 → ε ≈ 8.8%
- k=1024 → ε ≈ 3.1%

**Complexity:**
- Signature generation: O(|S| × k)
- Similarity estimation: O(k)
- **Memory per set:** k × 4 bytes (vs potentially gigabytes for raw set)

### Performance Characteristics

**Dataset:** 1M documents, avg 1000 words each

| k (signature size) | Memory per doc | Error | Build time |
|--------------------|----------------|-------|------------|
| 64 | 256 bytes | ±12.5% | 0.1s |
| 128 | 512 bytes | ±8.8% | 0.2s |
| 256 | 1 KB | ±6.25% | 0.4s |

**Compared to exact Jaccard:**
- Exact: 1000 words × 20 bytes avg = 20 KB per doc
- MinHash (k=128): 512 bytes = **39x memory reduction**

## LSH: Sub-Linear Similarity Search

### The Sub-Linear Search Problem

**Naive search:** Compare query to all N items → O(N)

**LSH solution:** Hash similar items to same buckets → O(1) lookup

### LSH Theory: Hash Families

**Locality-sensitive property:**
```
If d(A, B) ≤ r (similar), then P(h(A) = h(B)) ≥ p1 (high)
If d(A, B) ≥ cr (dissimilar), then P(h(A) = h(B)) ≤ p2 (low)
```
Where p1 > p2, c > 1

**For MinHash:**
- Distance metric: 1 - J(A, B)
- p1 = J(A, B) for similar pairs
- p2 = J(A, B) for dissimilar pairs

### LSH Index Structure

**Band-and-row technique:**
1. Divide MinHash signature (k values) into b bands of r rows each (k = b × r)
2. Hash each band independently into buckets
3. Items are candidates if they match in ≥1 band

**Amplification effect:**
- Single hash: P(collision) = J^r (low for single band)
- Multiple bands: P(collision) = 1 - (1 - J^r)^b (amplified)

**Example:** k=128, b=16 bands, r=8 rows
- Similar pair (J=0.8): P(collision) ≈ 99%
- Dissimilar pair (J=0.3): P(collision) ≈ 0.01%

### Query Process

1. Compute MinHash signature for query
2. Hash each band → get candidate buckets
3. Retrieve all items in those buckets
4. (Optional) Re-compute exact Jaccard for candidates

**Complexity:**
- Query time: O(b + |candidates|)
- **Expected candidates:** ~10-100 (vs N=millions)

### Tuning Parameters

**b (bands) and r (rows):**
- More bands (b↑, r↓) → find more similar pairs, more false positives
- Fewer bands (b↓, r↑) → stricter threshold, fewer false positives

**Threshold (t):**
- LSH detects pairs with J(A, B) ≥ t
- Optimal: t ≈ (1/b)^(1/r)
- Example: b=20, r=5 → t ≈ 0.55

### Performance Benchmarks

**Dataset:** 10M documents, deduplication task

| Method | Time | Recall | Precision |
|--------|------|--------|-----------|
| Exact (pairwise) | 3 days | 100% | 100% |
| LSH (b=20, r=6) | 2 hours | 95% | 98% |
| LSH (b=10, r=10) | 1 hour | 85% | 99.5% |

**Speedup:** 36x faster with 95% recall

## SimHash: Near-Duplicate Detection

### Algorithm

**Concept:** Locality-sensitive hash where similar documents produce similar hashes (Hamming distance)

**Signature generation:**
1. Extract features (e.g., shingles: "quick brown", "brown fox", ...)
2. Hash each feature to 64-bit integer
3. For each bit position:
   - If feature hash has bit=1, increment counter
   - If feature hash has bit=0, decrement counter
4. Final SimHash: bit=1 if counter>0, else bit=0

**Result:** 64-bit fingerprint where similar docs have low Hamming distance

### Similarity Detection

**Hamming distance:** Count of differing bits

**Thresholds:**
- ≤3 bits different → near-duplicates (~95% similarity)
- ≤6 bits different → similar (~85% similarity)

**Query:** Find all docs with Hamming distance ≤ k
- Use LSH on bit vectors (banding technique)
- Or exhaustive search (fast: 64-bit XOR + popcount)

### Performance

**Dataset:** 100M web pages

| k (Hamming threshold) | Duplicates found | False positives |
|-----------------------|------------------|-----------------|
| 3 | 5M | 0.1% |
| 6 | 12M | 1.5% |
| 10 | 25M | 5% |

**Google's use case:** Web page deduplication (original SimHash paper, 2007)

## datasketch Implementation

### Available Algorithms

1. **MinHash** - Jaccard similarity, variable k
2. **MinHashLSH** - LSH index for MinHash signatures
3. **MinHashLSHForest** - Dynamic LSH (adjustable threshold)
4. **Lean MinHash** - Memory-optimized (no seed storage)
5. **Weighted MinHash** - Jaccard with element weights
6. **HyperLogLog** - Cardinality estimation (not similarity)
7. **SimHash** - Locality-sensitive hash for text

### Recent Features (v1.8+, 2025)

**CuPy GPU backend:**
- GPU-accelerated MinHash.update_batch()
- Speedup: ~10x for large batches
- Still CPU-only for LSH index

**Cassandra storage backend:**
- Distributed LSH index
- Horizontal scaling for billion-scale datasets

**Deletion support (v1.8):**
- MinHashLSHDeletionSession for bulk key removal
- Previously required full rebuild

## When to Use Probabilistic Hashing vs Dense Vectors

### Use datasketch (MinHash/LSH/SimHash) for:
- **Set similarity:** Documents, user behavior, shopping carts
- **Sparse data:** Text (shingles), categorical features
- **Memory constraints:** Billion-scale with GB RAM (not TB)
- **Deduplication:** Primary use case

### Use FAISS/Annoy/ScaNN for:
- **Dense embeddings:** BERT, image features, audio
- **High-dimensional continuous vectors:** 128-2048 dims
- **High recall:** >98% (LSH plateaus at ~95%)
- **Euclidean/cosine on embeddings:** Optimized for continuous spaces

### Hybrid Approach
```
Stage 1: LSH → find 100 candidates (fast, approximate)
Stage 2: FAISS → re-rank with dense embeddings (accurate)
```

## Limitations

### 1. Approximate Results
- No guarantee of finding all similar pairs
- Recall typically 85-95% (vs 100% exact)

### 2. Static Thresholds
- LSH optimized for single similarity threshold
- Changing threshold requires rebuild

### 3. Set/Text Only
- Designed for Jaccard similarity (sets)
- Not suitable for continuous vector spaces

### 4. No Incremental Updates (LSH)
- Adding items requires partial rebuild
- Batch updates preferred

## When datasketch Excels

- **Text deduplication at scale:** Web crawling, news articles
- **Collaborative filtering:** User-item sets (recommenders)
- **Record linkage:** Database deduplication
- **Memory-constrained environments:** Mobile, edge devices

## Production Patterns

### Pattern 1: Two-Stage Retrieval
```
LSH (1M docs → 100 candidates) → Exact Jaccard (100 → top-10)
```

### Pattern 2: Distributed LSH (Cassandra backend)
```
Billion-scale index → horizontal scaling → sub-second queries
```

### Pattern 3: Hybrid Vector+Set
```
Dense embeddings (FAISS) + Set features (MinHash LSH) → Ensemble ranking
```

---

**Sources:**
- [MinHash Mathematics (Wikipedia)](https://en.wikipedia.org/wiki/MinHash)
- [MinHash - Fast Jaccard Similarity](https://arpitbhayani.me/blogs/jaccard-minhash/)
- [LSH Theory (Pinecone)](https://www.pinecone.io/learn/series/faiss/locality-sensitive-hashing/)
- [LSH with PyImageSearch (Jan 2025)](https://pyimagesearch.com/2025/01/27/approximate-nearest-neighbor-with-locality-sensitive-hashing-lsh/)
- [datasketch documentation](http://ekzhu.com/datasketch/)
