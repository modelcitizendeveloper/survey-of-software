# ScaNN: Technical Deep-Dive

## Architecture Overview

ScaNN (Scalable Nearest Neighbors) is Google Research's vector similarity search library optimized for **Maximum Inner Product Search (MIPS)** using **anisotropic vector quantization**.

**Key innovation:** Score-aware quantization that prioritizes accuracy for high-similarity pairs over low-similarity pairs.

## Core Algorithm: Anisotropic Vector Quantization

### Traditional Quantization (Isotropic)

**Goal:** Minimize distance between original vector x and quantized vector x̃

**Loss function:** L = ||x - x̃||²

**Problem:** Treats all error directions equally, but nearest-neighbor search cares most about high-scoring vectors

### Anisotropic Quantization (ScaNN)

**Goal:** Minimize error for vectors with high inner products to query

**Key insight:** For MIPS, parallel error (along query direction) matters more than orthogonal error

**Loss function (simplified):**
```
L = α × (parallel error)² + β × (orthogonal error)²
where α > β (penalize parallel error more)
```

**Effect:** Quantization "stretches" to preserve high inner products, tolerates error on low-scoring vectors

### Mathematical Formulation

Given query q and database vector x:

1. **Decompose residual:** r = x - x̃ into parallel (r∥) and orthogonal (r⊥) components relative to q
2. **Anisotropic penalty:**
   ```
   Error = ||r∥||² + λ × ||r⊥||²  (λ < 1)
   ```
3. **Result:** Minimizes error for vectors with high q·x

**Why this works for top-K search:**
- Top-K results have large inner products with query
- Anisotropic loss focuses accuracy on these high-scoring vectors
- Low-scoring vectors can have higher error (they won't be in top-K anyway)

## SOAR Algorithm (2025)

**SOAR (Scaling Optimization for Anisotropic Retrieval):** Recent enhancement to ScaNN

**Innovation:** Introduces effective redundancy to reduce query latency

**Mechanism:**
- Duplicates partitions with overlapping coverage
- Query searches fewer partitions but with higher confidence
- Reduces false negatives from partition boundaries

**Performance:** 2x QPS improvement at same accuracy (Google benchmark, Dec 2025)

## Index Structure

ScaNN uses a two-level hierarchy:

### 1. Coarse Quantization (Partitioning)
- K-means or learned partitioning to create clusters
- Similar to FAISS IVF but with anisotropic-aware centroids

### 2. Fine Quantization (Within-partition)
- Anisotropic vector quantization for compression
- Score-aware loss minimizes error for top-K candidates

### Query Process
1. Find top-K partitions (coarse quantization)
2. Search within partitions using compressed vectors (fine quantization)
3. Re-rank top candidates with original vectors (optional)

## Performance Characteristics

### Time Complexity

| Phase | Complexity | Notes |
|-------|------------|-------|
| Build | O(N × D × iterations) | K-means + quantization training |
| Query | O(K × M × D_compressed) | K=partitions, M=avg points/partition |

### Memory Complexity

- **Quantized vectors:** N × M × 1 byte (M = subvectors)
- **Centroids:** K × D × 4 bytes
- **Total:** ~8-16 bytes per vector (vs 768 × 4 = 3072 for raw embeddings)

### Benchmark Results (ann-benchmarks, 2025)

**Dataset:** glove-100-angular (1.2M vectors, 100-dim)

| Library | QPS | Recall@10 |
|---------|-----|-----------|
| ScaNN | 2400 | 98.5% |
| FAISS (HNSW) | 1200 | 98.0% |
| Annoy | 650 | 95.0% |

**Observation:** ScaNN achieves 2x QPS at higher accuracy than next-best competitor

**Gene embedding study (2025):**
- ScaNN query latency: 1.83s
- FAISS slightly faster but ScaNN more accurate
- ScaNN better for in-domain queries, FAISS for out-of-domain

## Tuning Parameters

### Partitions (num_leaves)
- **Effect:** More partitions → faster query, lower recall
- **Typical:** 1000-10000 for million-scale datasets
- **Rule of thumb:** num_leaves = √N to N/100

### Search leaves (num_leaves_to_search)
- **Effect:** More leaves → higher recall, slower query
- **Typical:** 5-50
- **Trade-off:** Similar to FAISS nprobe

### Quantization dimensions (num_quantized_dims)
- **Effect:** More dims → better accuracy, larger index
- **Typical:** 8-16 (for 768-dim vectors: 48-96 subvector dims)

### Anisotropic weight (quantization_weight)
- **Effect:** Higher weight → more anisotropic (favor high-scoring vectors)
- **Default:** Library auto-tunes based on data distribution

## Comparison: ScaNN vs FAISS PQ

### ScaNN Anisotropic Quantization
- **Optimizes for:** Top-K accuracy (MIPS objective)
- **Loss function:** Score-aware (penalizes high-scoring errors more)
- **Best for:** Inner-product search (dot product similarity)

### FAISS Product Quantization
- **Optimizes for:** Average reconstruction error
- **Loss function:** Isotropic (all errors weighted equally)
- **Best for:** Euclidean distance, general-purpose compression

**When ScaNN wins:**
- Inner-product metric (e.g., cosine similarity, MIPS)
- High-recall requirements (>98%)
- Query distribution matches training data

**When FAISS wins:**
- Euclidean distance metric
- GPU acceleration needed
- More mature ecosystem (broader community)

## Production Deployment

### Google Cloud Integration

**Vertex AI Vector Search:**
- Managed ScaNN service
- Auto-scaling, high availability
- ~$200/month for 1M vectors (2025 pricing)

**AlloyDB ScaNN Index:**
- PostgreSQL with ScaNN indexes
- SQL-queryable vector search
- Hybrid queries (vector + relational filters)

### Self-Hosted Considerations

**Installation complexity:**
- Part of google-research monorepo (not standalone package)
- Requires Bazel build system
- Python package available but less documented than FAISS

**Operational overhead:**
- Less mature than FAISS for self-hosting
- Fewer pre-built Docker images, tutorials
- Community smaller than FAISS

## When ScaNN Excels

- **Accuracy-critical applications:** Medical, legal, high-stakes retrieval
- **Inner-product metric:** Cosine similarity, MIPS
- **Google Cloud deployment:** Native Vertex AI integration
- **Research:** SOTA algorithms, cutting-edge techniques

## Limitations

- **Ecosystem maturity:** Smaller community, fewer tutorials than FAISS
- **Installation:** Monorepo complexity vs standalone FAISS package
- **GPU support:** Less mature than FAISS
- **Euclidean distance:** FAISS optimizes better for L2 metric

## Recent Developments (2025-2026)

**SOAR algorithm (Dec 2025):**
- 2x query throughput improvement
- Redundancy-based optimization
- Winner of Big-ANN 2023 benchmark

**CuPy GPU support (2025):**
- GPU acceleration for batch queries
- Still less optimized than FAISS CUDA

---

**Sources:**
- [Announcing ScaNN (Google Research Blog)](https://research.google/blog/announcing-scann-efficient-vector-similarity-search/)
- [Anisotropic Vector Quantization (ICML 2020)](https://arxiv.org/abs/1908.10396)
- [SOAR Algorithm (Google Research, Dec 2025)](https://research.google/blog/soar-new-algorithms-for-even-faster-vector-search-with-scann/)
- [ScaNN Technical Overview (Zilliz)](https://zilliz.com/learn/what-is-scann-scalable-nearest-neighbors-google)
