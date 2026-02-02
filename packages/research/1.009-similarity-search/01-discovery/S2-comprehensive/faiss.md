# FAISS: Technical Deep-Dive

## Architecture Overview

FAISS combines multiple indexing strategies into a composable framework:
- **Flat indexes** - Exact search baseline
- **IVF (Inverted File)** - Partitioning-based approximate search
- **PQ (Product Quantization)** - Vector compression
- **HNSW (Hierarchical Navigable Small World)** - Graph-based search
- **Composite indexes** - IVF+PQ, IVF+HNSW for multi-objective optimization

## Core Algorithms

### 1. Inverted File Index (IVF)

**Concept:** Cluster-based partitioning to reduce search space

**How it works:**
1. **Clustering phase:** K-means creates N centroids (e.g., N=1000 for 1M vectors)
2. **Assignment:** Each vector assigned to nearest centroid
3. **Query:** Search only K closest clusters (e.g., K=10), not entire dataset

**Complexity:**
- Build: O(N × D × iterations) for k-means
- Query: O(K × M × D) where K=clusters searched, M=avg points per cluster

**Trade-off:** 10-100x speedup at cost of ~5% recall loss

### 2. Product Quantization (PQ)

**Concept:** Compress vectors by quantizing subspaces independently

**How it works:**
1. Split D-dimensional vector into M subvectors (e.g., 768-dim → 8 subvectors of 96-dim)
2. Learn K centroids per subspace (e.g., K=256 → 8 bits per subspace)
3. Represent each vector as M × 8-bit codes (instead of M × 32-bit floats)

**Memory reduction:**
- Original: 768 floats × 4 bytes = 3072 bytes
- PQ (M=8, K=256): 8 codes × 1 byte = 8 bytes
- **Compression ratio: 384x** (practical: ~32x after codebooks)

**Accuracy:** 98.4% memory reduction with minimal recall degradation

### 3. HNSW (Hierarchical Navigable Small World)

**Concept:** Multi-layer graph where greedy search converges to nearest neighbors

**Structure:**
- Layer 0: All vectors
- Layer L: Sparse subset (exponentially decreasing density)
- Edges: Connect each node to M nearest neighbors per layer

**Query algorithm:**
1. Start at top layer, jump to nearest neighbor
2. Descend layers, refining search
3. At layer 0, greedily traverse to k-NN

**Trade-off:** Best accuracy (~99% recall) at cost of higher memory (graph storage)

### 4. Composite Indexes: IVF+PQ+HNSW

**IVFPQ:** Combines partitioning + compression
- IVF reduces search space
- PQ compresses vectors within partitions
- **Result:** 92x faster than flat search, 15x smaller than HNSW

**IVF+HNSW:** HNSW as coarse quantizer
- HNSW finds top-K clusters (faster than k-means scan)
- IVF+PQ searches within those clusters
- **Result:** Best of both worlds—graph speed + compression

## GPU Acceleration

**GPU advantages:**
- Parallel distance computation (10K+ vectors simultaneously)
- Batch processing of queries
- **Speedup:** 100x vs CPU for large batches

**GPU limitations:**
- Memory constraints (e.g., A100 has 80GB VRAM)
- Transfer overhead for small query batches
- Less effective for ultra-high-dimensional vectors (>2048-dim)

## Performance Characteristics

### Time Complexity

| Index Type | Build | Query |
|------------|-------|-------|
| Flat | O(1) | O(N × D) |
| IVF | O(N × D × k-means-iter) | O(K × M × D) |
| HNSW | O(N × M × log(N)) | O(log(N) × M × D) |
| IVFPQ | O(N × D + PQ-train) | O(K × M × D/subvec-factor) |

### Memory Complexity

| Index Type | Memory per Vector |
|------------|-------------------|
| Flat | D × 4 bytes |
| IVF | D × 4 bytes + centroids |
| PQ | M × 1 byte + codebooks |
| HNSW | D × 4 bytes + M × log(N) × 4 bytes (edges) |

## Tuning Parameters

### IVF
- `nlist`: Number of clusters (√N to N/100 typical)
- `nprobe`: Clusters to search (1-100, higher = more accurate/slower)

### PQ
- `M`: Subvectors (8, 16, 32 common; must divide D)
- `nbits`: Bits per code (8 typical, 4-12 range)

### HNSW
- `M`: Neighbors per node (16-64 typical)
- `efConstruction`: Build-time search depth (40-500)
- `efSearch`: Query-time search depth (16-512)

## Benchmark Results (ann-benchmarks, 2025)

**Dataset:** 1M vectors, 768-dim (BERT embeddings)

| Index | QPS | Recall@10 | Memory | Build Time |
|-------|-----|-----------|--------|------------|
| Flat | 120 | 100% | 3 GB | instant |
| IVF1000 | 8500 | 95% | 3 GB | 5 min |
| PQ8x8 | 12000 | 93% | 100 MB | 10 min |
| HNSW32 | 6000 | 99% | 4.5 GB | 30 min |
| IVFPQ | 15000 | 94% | 150 MB | 15 min |

**GPU (A100):**
- Flat: 12000 QPS (100x speedup)
- IVF: 85000 QPS (10x speedup)

## Production Deployment Patterns

### Pattern 1: Hybrid Exact/Approximate
```
Query → IVFPQ (fast, approximate) → Flat re-rank top-100 (exact)
```
**Use case:** High-recall applications (medical, legal retrieval)

### Pattern 2: Tiered Search
```
Small dataset (<1M): HNSW
Large dataset (>10M): IVFPQ with periodic HNSW coarse quantizer refresh
```

### Pattern 3: GPU Batch Processing
```
Collect queries → Batch search on GPU → Stream results
```
**Optimal:** 1000+ queries/batch for 100x GPU speedup

## When FAISS Excels

- **Billion-scale datasets:** IVF+PQ handles 1B+ vectors
- **GPU availability:** 100x speedup on batch queries
- **Flexible requirements:** Composable indexes for speed/accuracy/memory trade-offs
- **Production maturity:** Battle-tested at Meta, widely adopted

## Limitations

- **Learning curve:** Index selection requires understanding of IVF/PQ/HNSW
- **Build time:** Hours for billion-scale indexes (not real-time)
- **Static indexes:** Updates require rebuild (no efficient incremental updates)
- **Parameter tuning:** Optimal nlist/nprobe/M varies by dataset

## Related Work

- **Milvus/Weaviate:** Vector databases built on FAISS backend
- **Vertex AI Vector Search:** Google Cloud service (uses ScaNN)
- **Pinecone:** Managed vector DB (proprietary, FAISS-inspired)

---

**Sources:**
- [FAISS Product Quantization (Pinecone)](https://www.pinecone.io/learn/series/faiss/product-quantization/)
- [IVF+PQ+HNSW for Billion-scale Search](https://towardsdatascience.com/ivfpq-hnsw-for-billion-scale-similarity-search-89ff2f89d90e/)
- [FAISS indexes documentation](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes)
