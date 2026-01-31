# Annoy: Technical Deep-Dive

## Architecture Overview

Annoy (Approximate Nearest Neighbors Oh Yeah) uses **random projection trees** to partition high-dimensional space for efficient approximate search.

**Core innovation:** Memory-mapped file-based indexes enable multi-process sharing without RAM duplication.

## Algorithm: Random Projection Trees

### Tree Construction

**Recursive partitioning:**
1. Select two random points from current dataset
2. Compute hyperplane equidistant to these points
3. Split dataset: left child (closer to point A), right child (closer to point B)
4. Recurse until leaf node ≤ M points (M = configurable)

**Mathematical foundation:** Random hyperplanes preserve angular distances with high probability (Johnson-Lindenstrauss lemma)

**Complexity:**
- Build: O(N × D × n_trees × log(N))
- Memory: O(N × D × n_trees)

### Why Multiple Trees (Forest)?

**Problem:** Single tree may make poor splits (e.g., random points both in one cluster)

**Solution:** Build T trees (T = 10-100 typical)
- Each tree creates different partitions
- Query combines candidates from all trees
- More trees → better recall, slower query

**Trade-off:** 10 trees → ~90% recall, 100 trees → ~98% recall

### Query Algorithm

1. **Traverse each tree:** Follow split hyperplanes to leaf node
2. **Collect candidates:** Union of all leaf nodes reached (T × M points)
3. **Distance computation:** Compute exact distances to all candidates
4. **Return top-K:** Sort by distance, return K nearest

**Complexity:** O(T × log(N) + T × M × D)
- Tree traversal: T × log(N)
- Distance computation: T × M × D (M = leaf size, typically 5-100)

## Memory-Mapped Architecture

**mmap design:**
- Index stored as binary file on disk
- OS loads pages into RAM on access
- Multiple processes share same physical memory pages

**Advantages:**
- Shared memory across processes (e.g., web server workers)
- Lazy loading (only accessed pages loaded)
- OS manages eviction (LRU)

**Disadvantages:**
- Slower than in-RAM (page faults on cold data)
- Not suitable for random access patterns (thrashing)

## Distance Metrics

Annoy supports:
- **Angular (default):** Cosine similarity via dot product
- **Euclidean:** L2 distance
- **Manhattan:** L1 distance
- **Hamming:** For binary vectors

**Note:** Metric must be chosen at build time (not queryable across metrics)

## Performance Characteristics

### Time Complexity

| Phase | Complexity | Typical Time |
|-------|------------|--------------|
| Build (T trees) | O(N × D × T × log(N)) | 1-10 min for 1M vectors |
| Query | O(T × log(N) + T × M × D) | 0.1-1 ms |
| Load index | O(1) (mmap) | Instant |

### Memory Complexity

- **RAM (hot data):** ~N × D × 4 bytes (same as raw vectors)
- **Disk (full index):** ~N × D × T × 4 bytes
- **Typical:** 10 trees → 10x disk footprint vs raw vectors

### Scaling Behavior

| Dataset Size | Build Time | Query Time | Recall (50 trees) |
|--------------|------------|------------|-------------------|
| 10K | 1 sec | 0.01 ms | 98% |
| 100K | 10 sec | 0.05 ms | 96% |
| 1M | 2 min | 0.15 ms | 93% |
| 10M | 30 min | 0.5 ms | 88% |

**Observation:** Recall degrades gracefully with scale; add more trees to compensate

## Tuning Parameters

### n_trees (T)
- **Range:** 10-100 typical
- **Effect:** More trees → higher recall, slower query, larger disk
- **Rule of thumb:** T = 10 for quick prototypes, T = 50-100 for production

### search_k
- **Definition:** Number of nodes to inspect during search
- **Default:** search_k = n_trees × n (n = number of results)
- **Effect:** Higher search_k → better recall, slower query
- **Range:** 100 to 10000 typical

### Leaf size (M)
- **Default:** Adaptive (Annoy auto-tunes)
- **Effect:** Smaller leaves → deeper trees, more accurate, slower build

## Benchmark Results (ann-benchmarks, 2024)

**Dataset:** 1M vectors, 128-dim, angular distance

| n_trees | search_k | QPS | Recall@10 |
|---------|----------|-----|-----------|
| 10 | 100 | 120 | 78% |
| 50 | 500 | 53 | 93.5% |
| 100 | 1000 | 28 | 97% |

**Observations:**
- Sweet spot: 50 trees, ~90% recall, 50+ QPS
- Annoy trades query speed for simplicity (vs FAISS HNSW: 6000 QPS at 99% recall)

## Comparison: Trees vs Graphs (Annoy vs HNSW)

### Annoy (Tree-based)
- **Structure:** Binary trees with random splits
- **Build:** Faster (simple recursive split)
- **Query:** Slower (must traverse multiple trees)
- **Recall:** Good (~90-95% with 50 trees)

### HNSW (Graph-based)
- **Structure:** Multi-layer graph with greedy search
- **Build:** Slower (compute M nearest neighbors per node)
- **Query:** Faster (single graph traversal)
- **Recall:** Excellent (~99% with M=32)

**Trade-off:** Annoy = simplicity + fast build, HNSW = accuracy + fast query

## Production Use Cases

### Spotify Music Recommendation
- **Dataset:** Millions of tracks, 100-300 dim embeddings
- **Why Annoy:** Fast build, shared memory across workers, good-enough recall

### Content Recommendation (Medium Scale)
- **Dataset:** <10M items, 256-768 dim embeddings
- **Why Annoy:** Simple API, no GPU needed, disk-backed indexes

### Prototyping
- **Why Annoy:** 5-minute setup, iterate quickly, graduate to FAISS when scale demands

## Limitations

### No Incremental Updates
- **Problem:** Adding vectors requires full rebuild
- **Workaround:** Rebuild periodically (e.g., nightly batch)
- **When this breaks:** Real-time index updates (use FAISS or Milvus)

### Accuracy Ceiling
- **Problem:** Recall plateaus at ~95-97% even with 100+ trees
- **Why:** Random splits don't adapt to data distribution (unlike k-means in IVF)
- **When this breaks:** High-recall applications (medical, legal retrieval)

### Single-Algorithm Design
- **Problem:** No compression (PQ), no GPU support
- **When this breaks:** Billion-scale datasets, memory constraints

## When Annoy Excels

- **Small-to-medium datasets (<10M vectors)**
- **Shared-memory environments (web servers, multi-process)**
- **Fast prototyping (minimal configuration)**
- **Disk-backed indexes (RAM constraints)**

## When to Graduate to FAISS

- Dataset grows >10M vectors
- Need >95% recall
- GPU available
- Memory constraints (need PQ compression)

---

**Sources:**
- [Annoy Random Projection Trees (Lyst Engineering)](https://making.lyst.com/2015/07/10/ann/)
- [Tree-based vs Graph-based Indices (Milvus AI)](https://milvus.io/ai-quick-reference/what-data-structures-or-algorithmic-strategies-allow-annoy-to-quickly-find-neighbors-eg-multiple-random-projection-trees-and-how-do-these-contribute-to-its-query-performance)
- [Random Projection Trees Revisited (Academic Paper)](https://www.cse.iitk.ac.in/users/purushot/papers/rptree.pdf)
