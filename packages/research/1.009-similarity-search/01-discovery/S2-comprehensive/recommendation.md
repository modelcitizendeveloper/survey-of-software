# S2 Recommendation: Architecture-Grade Selection

## Technical Decision Framework

After comprehensive analysis, choose based on these technical requirements:

---

## 1. Algorithm Selection by Metric & Data Type

### Dense Vectors (Embeddings, Image Features)

**Euclidean Distance (L2):**
- **Primary:** FAISS (IVF, PQ optimized for L2)
- **Simple:** Annoy (angular approximates normalized L2)

**Inner Product / Cosine Similarity:**
- **Accuracy-critical:** ScaNN (anisotropic quantization for MIPS)
- **Production-grade:** FAISS (HNSW or IVF with normalized vectors)
- **Simple:** Annoy (angular distance native support)

### Discrete Sets / Text (Jaccard, Hamming)

**Set Similarity (Jaccard):**
- **Primary:** datasketch MinHash + LSH
- **Exact (small scale):** Direct Jaccard computation

**Near-Duplicate Detection:**
- **Text:** datasketch SimHash
- **Embeddings:** FAISS with very low threshold

---

## 2. Scale-Driven Selection

### <10K vectors
**Recommendation:** Annoy or even exact search (Flat)
- Build time: seconds
- Query time: sub-millisecond
- Complexity not justified for FAISS/ScaNN

### 10K - 1M vectors
**Recommendation:** Annoy (simple) or FAISS IVF (optimized)
- Annoy: 2-min build, 50+ QPS
- FAISS IVF: 5-min build, 8K+ QPS

### 1M - 100M vectors
**Recommendation:** FAISS (IVF+PQ or HNSW)
- IVF+PQ: Best QPS/memory trade-off (15K QPS, 150 MB)
- HNSW: Best accuracy (99% recall, 6K QPS)

### >100M vectors
**Recommendation:** FAISS IVF+PQ with GPU
- GPU acceleration: 100x speedup on batch queries
- PQ compression: Fit 100M+ vectors in RAM

### Billion-scale (sets/text)
**Recommendation:** datasketch MinHash LSH
- Memory: KB per item vs GB for dense vectors
- Speed: Sub-linear search with LSH

---

## 3. Accuracy Requirements

### 90-95% Recall
**Recommendation:** Annoy (50 trees) or FAISS IVF
- Fast query times (50-8000 QPS)
- Moderate memory footprint

### 95-98% Recall
**Recommendation:** FAISS IVF+PQ or HNSW
- IVF: Tune nprobe higher (50-100)
- HNSW: M=32, efSearch=100-200

### >98% Recall
**Recommendation:** ScaNN or FAISS HNSW
- ScaNN: Anisotropic quantization (best for MIPS)
- FAISS HNSW: M=64, efSearch=500+

### 100% Recall (Exact Search)
**Recommendation:** FAISS Flat + GPU
- No approximation, brute force
- GPU: 100x speedup (12K QPS for 1M vectors)

---

## 4. Memory Constraints

### No Memory Limit
**Recommendation:** FAISS HNSW (best accuracy)
- Memory: ~4.5 GB per 1M vectors (768-dim)

### Moderate Constraint (10x compression needed)
**Recommendation:** FAISS PQ or ScaNN
- FAISS PQ: 32x compression, 93% recall
- ScaNN: 16-32x compression, 98% recall

### Severe Constraint (100x+ compression)
**Recommendation:** datasketch MinHash
- 100-1000x reduction for set similarity
- Probabilistic (±5-10% error)

### Disk-Backed (Multi-Process Sharing)
**Recommendation:** Annoy
- Memory-mapped indexes
- OS manages paging (LRU)

---

## 5. GPU Availability

### GPU Available (CUDA)
**Recommendation:** FAISS with GPU
- Flat: 100x speedup
- IVF: 10x speedup
- Batch queries: 1000+ queries for max efficiency

### No GPU
**Recommendation:**
- **Fast:** Annoy (CPU-optimized)
- **Accurate:** FAISS HNSW (CPU)
- **Memory-efficient:** FAISS PQ (CPU)

---

## 6. Update Patterns

### Static Dataset (Rebuild Acceptable)
**Any library works:** FAISS, Annoy, ScaNN, datasketch
- Build once, query many

### Frequent Additions (Daily/Hourly)
**Recommendation:** FAISS HNSW (add-only efficient)
- Rebuild when accuracy degrades (~weekly)

### Real-Time Updates
**Recommendation:** None (all libraries struggle)
- **Workaround:** Dual-index (hot + cold), merge periodically
- **Alternative:** Milvus (built on FAISS with update support)

### Deletions Required
**Recommendation:** FAISS with tombstones + periodic compaction
- Mark deleted, rebuild when tombstones >10%

---

## 7. Deployment Environment

### Cloud-Native (Google Cloud)
**Recommendation:** ScaNN via Vertex AI Vector Search
- Managed service, auto-scaling
- ~$200/month for 1M vectors

### Cloud-Agnostic (AWS/GCP/Azure)
**Recommendation:** FAISS in Docker
- Self-hosted, full control
- Widely documented, proven at scale

### On-Premise / Edge
**Recommendation:** Annoy or datasketch
- Minimal dependencies (Annoy: C++, datasketch: Python)
- Small binary size

### Multi-Process (Web Server)
**Recommendation:** Annoy
- Memory-mapped indexes shared across workers
- No RAM duplication

---

## 8. Development Speed vs Optimization

### Prototype in 1 Hour
**Recommendation:** Annoy
- 5 parameters, intuitive API
- pip install, 10 lines of code

### Production in 1 Day
**Recommendation:** FAISS IVF
- Well-documented, production examples
- Tune nlist/nprobe for speed/accuracy

### Research / Experimentation
**Recommendation:** ScaNN or FAISS
- ScaNN: SOTA algorithms (anisotropic quantization)
- FAISS: Composable indexes (IVF+PQ+HNSW)

---

## 9. Common Architecture Patterns

### Pattern 1: Two-Stage Retrieval (Hybrid)
```
Stage 1: FAISS PQ (100K→1000 candidates, fast)
Stage 2: FAISS Flat (1000→10 exact, re-rank)
```
**Use case:** High-recall RAG systems

### Pattern 2: GPU Batch Processing
```
Collect 1000+ queries → FAISS GPU (batch) → Stream results
```
**Use case:** Offline analytics, recommendation generation

### Pattern 3: Tiered Search
```
Hot data (recent): HNSW (fast, accurate)
Cold data (archive): IVF+PQ (compressed)
```
**Use case:** Search engines, log analytics

### Pattern 4: Hybrid Vector + Set
```
Dense vectors (FAISS) + Set features (MinHash) → Ensemble
```
**Use case:** E-commerce (image similarity + attribute matching)

---

## 10. Migration Paths

### Start: Annoy (Prototype)
**Graduate to:** FAISS (Scale)
- **Trigger:** Dataset >10M or recall <95%

### Start: FAISS CPU
**Graduate to:** FAISS GPU
- **Trigger:** GPU available, batch query workload

### Start: FAISS IVF
**Graduate to:** FAISS IVFPQ
- **Trigger:** Memory constraints (10x+ compression needed)

### Start: Exact Search
**Graduate to:** Annoy/FAISS
- **Trigger:** Dataset >100K, query time >100ms

---

## Key Takeaways by Workload

| Workload | Primary Choice | Alternative | Why |
|----------|---------------|-------------|-----|
| **RAG Systems** | FAISS | ScaNN (accuracy) | Industry standard, GPU support |
| **Image Search** | FAISS HNSW | FAISS GPU Flat | High-dim embeddings, accuracy matters |
| **Music Recommendation** | Annoy | FAISS | Spotify's proven choice |
| **Document Dedup** | datasketch | FAISS (if embeddings) | Set similarity, memory-efficient |
| **E-commerce Search** | FAISS IVF+PQ | Milvus (if updates) | Balance speed/memory/accuracy |
| **Research** | ScaNN | FAISS | SOTA algorithms, cutting-edge |

---

## Red Flags

❌ **Don't use FAISS for <10K vectors** → Annoy is simpler
❌ **Don't use Annoy for >98% recall** → FAISS HNSW or ScaNN
❌ **Don't use datasketch for dense vectors** → FAISS optimized for embeddings
❌ **Don't expect real-time updates** → All libraries batch-oriented
❌ **Don't use ScaNN without Google Cloud** → Deployment complexity vs FAISS

---

## Final Recommendation

**For most production use cases: Start with FAISS**
- Mature ecosystem, widely adopted
- GPU support, flexible indexes (IVF/PQ/HNSW)
- Proven at billion-scale (Meta internal use)

**Exception: Use Annoy for prototypes, datasketch for set similarity**

Consult S3-need-driven and S4-strategic for use-case-specific and long-term considerations.
