# Feature Comparison Matrix

## Algorithm Complexity

| Library | Index Build | Query | Memory per Vector |
|---------|-------------|-------|-------------------|
| **FAISS Flat** | O(1) | O(N × D) | D × 4 bytes |
| **FAISS IVF** | O(N × D × iter) | O(K × M × D) | D × 4 bytes + centroids |
| **FAISS PQ** | O(N × D + train) | O(N × M) | M bytes + codebooks |
| **FAISS HNSW** | O(N × M × log N) | O(log N × M × D) | D × 4 + M × log N × 4 |
| **Annoy** | O(N × D × T × log N) | O(T × log N + T × M × D) | D × 4 × T |
| **ScaNN** | O(N × D × iter) | O(K × M × D_c) | 8-16 bytes + centroids |
| **MinHash** | O(\|S\| × k) | O(k) | k × 4 bytes |
| **LSH** | O(N × k) | O(b + \|cand\|) | k × 4 bytes per item |

**Legend:**
- N = dataset size, D = dimensions, K = clusters/partitions, M = points per partition/neighbors
- T = trees (Annoy), k = hash functions (MinHash), b = bands (LSH)

---

## Distance Metrics

| Library | Euclidean (L2) | Cosine | Inner Product | Jaccard | Hamming |
|---------|----------------|--------|---------------|---------|---------|
| **FAISS** | ✅ Primary | ✅ Via normalization | ✅ Native (MIPS) | ❌ | ❌ |
| **Annoy** | ✅ | ✅ (angular) | ✅ | ❌ | ✅ |
| **ScaNN** | ✅ | ✅ | ✅ Primary (anisotropic) | ❌ | ❌ |
| **datasketch** | ❌ | ❌ (SimHash approx) | ❌ | ✅ Native (MinHash) | ✅ (SimHash) |

**Key takeaway:** Dense vector libraries (FAISS/Annoy/ScaNN) optimize for continuous spaces; datasketch optimizes for discrete sets

---

## Quantization & Compression

| Library | Technique | Compression Ratio | Accuracy Impact |
|---------|-----------|-------------------|-----------------|
| **FAISS PQ** | Product Quantization (isotropic) | 32-384x | 2-5% recall loss |
| **FAISS SQ** | Scalar Quantization | 4x (FP32→INT8) | <1% recall loss |
| **ScaNN** | Anisotropic Quantization | 16-32x | <1% recall loss (MIPS) |
| **Annoy** | None (full precision) | 1x | N/A |
| **MinHash** | Signature hashing | 100-1000x | ±5-10% error |
| **LSH** | Locality-sensitive hashing | 100-1000x | 5-15% recall loss |

**Best compression:** MinHash/LSH (but only for set similarity, not dense vectors)
**Best accuracy/compression:** ScaNN anisotropic (for inner-product metric)

---

## GPU Support

| Library | CPU | GPU | Multi-GPU | Notes |
|---------|-----|-----|-----------|-------|
| **FAISS** | ✅ | ✅ CUDA | ✅ | Best GPU support (100x speedup on batch queries) |
| **Annoy** | ✅ | ❌ | ❌ | CPU-only |
| **ScaNN** | ✅ | ⚠️ Limited (CuPy) | ❌ | Experimental GPU support |
| **datasketch** | ✅ | ⚠️ MinHash only (CuPy) | ❌ | v1.8+ has GPU batch updates |

**Winner:** FAISS (mature, production-grade GPU acceleration)

---

## Index Update Strategies

| Library | Incremental Add | Incremental Delete | Rebuild Required |
|---------|-----------------|--------------------| -----------------|
| **FAISS IVF** | ⚠️ Slow (re-assign) | ❌ | ✅ Periodic |
| **FAISS HNSW** | ✅ Add-only | ❌ | ✅ For deletes |
| **Annoy** | ❌ | ❌ | ✅ Every update |
| **ScaNN** | ⚠️ Slow | ❌ | ✅ Periodic |
| **LSH** | ✅ (with overhead) | ✅ (v1.8+) | ⚠️ Threshold changes |

**Most static:** Annoy (full rebuild always)
**Most dynamic:** FAISS HNSW (add-only efficient)
**None support fast deletes** (rebuild or tombstone required)

---

## Scale & Performance (Benchmarks)

### Dataset: 1M vectors, 768-dim (BERT embeddings)

| Library | Index Type | Build Time | QPS | Recall@10 | Memory |
|---------|------------|------------|-----|-----------|--------|
| **FAISS** | Flat | instant | 120 | 100% | 3 GB |
| **FAISS** | IVF1000 | 5 min | 8500 | 95% | 3 GB |
| **FAISS** | PQ8x8 | 10 min | 12000 | 93% | 100 MB |
| **FAISS** | HNSW32 | 30 min | 6000 | 99% | 4.5 GB |
| **FAISS** | IVFPQ | 15 min | 15000 | 94% | 150 MB |
| **Annoy** | 50 trees | 2 min | 53 | 93.5% | 300 MB |
| **ScaNN** | Default | 20 min | 2400 | 98.5% | 200 MB |

### Dataset: 10M documents (text, set similarity)

| Library | Method | Build Time | Duplicates Found | Precision |
|---------|--------|------------|------------------|-----------|
| **datasketch** | MinHash LSH | 2 hours | 95% of exact | 98% |
| **Exact Jaccard** | Pairwise | 3 days | 100% | 100% |

**Speed champion:** FAISS PQ (12K QPS at 93% recall)
**Accuracy champion:** FAISS HNSW (99% recall at 6K QPS)
**Memory champion:** datasketch (for set similarity tasks)

---

## Deployment & Ecosystem

| Library | Cloud Services | Vector DBs Using It | Community Size | Docs Quality |
|---------|----------------|---------------------|----------------|--------------|
| **FAISS** | AWS/GCP integrations | Milvus, Weaviate, Vespa | ⭐⭐⭐⭐⭐ (38.9K stars) | ⭐⭐⭐⭐⭐ Excellent |
| **Annoy** | None native | Some custom | ⭐⭐⭐⭐ (14.1K stars) | ⭐⭐⭐⭐ Good |
| **ScaNN** | Vertex AI, AlloyDB | None (standalone) | ⭐⭐⭐ (part of 37K repo) | ⭐⭐⭐ Moderate |
| **datasketch** | None | Custom dedup pipelines | ⭐⭐⭐ (2.9K stars) | ⭐⭐⭐⭐ Good |

**Production ecosystem:** FAISS (widely adopted, battle-tested)
**Cloud-native:** ScaNN (Vertex AI integration)
**Simplest:** Annoy (no dependencies, easy deploy)

---

## Language Bindings

| Library | Python | C++ | Java | Go | Rust | JavaScript |
|---------|--------|-----|------|----|----|------------|
| **FAISS** | ✅ | ✅ | ⚠️ Community | ❌ | ❌ | ❌ |
| **Annoy** | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ |
| **ScaNN** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **datasketch** | ✅ (pure) | ❌ | ❌ | ❌ | ❌ | ❌ |

**Most polyglot:** Annoy (5 languages)
**Python-first:** datasketch (pure Python)
**C++ core:** FAISS, Annoy, ScaNN (with Python bindings)

---

## License

| Library | License | Commercial Use | Attribution Required |
|---------|---------|----------------|----------------------|
| **FAISS** | MIT | ✅ | ❌ |
| **Annoy** | Apache-2.0 | ✅ | ❌ |
| **ScaNN** | Apache-2.0 | ✅ | ❌ |
| **datasketch** | MIT | ✅ | ❌ |

**All libraries:** Permissive, commercial-friendly

---

## Decision Matrix

### Choose FAISS if:
- ✅ Dataset >1M vectors
- ✅ GPU available
- ✅ Need flexible speed/accuracy/memory trade-offs (PQ, HNSW, IVF)
- ✅ Production maturity matters

### Choose Annoy if:
- ✅ Dataset <10M vectors
- ✅ Simplicity > optimization
- ✅ Memory-mapped indexes (multi-process sharing)
- ✅ Fast prototyping

### Choose ScaNN if:
- ✅ Accuracy critical (>98% recall)
- ✅ Inner-product metric (MIPS)
- ✅ Google Cloud (Vertex AI integration)
- ✅ Research/experimentation

### Choose datasketch if:
- ✅ Set similarity (Jaccard, documents, user behavior)
- ✅ Memory constraints (billion-scale with GB RAM)
- ✅ Text deduplication
- ✅ Can tolerate ~5% error
