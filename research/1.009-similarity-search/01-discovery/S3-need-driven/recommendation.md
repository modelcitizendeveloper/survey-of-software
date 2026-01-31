# S3 Recommendation: Use-Case-Driven Selection

## Decision Matrix by User Persona

| Who You Are | Primary Need | Recommended Library | Why |
|-------------|--------------|---------------------|-----|
| **RAG System Builder** | Semantic search for LLM context | FAISS (IVF/HNSW) | Industry standard, GPU support, >95% recall |
| **E-commerce Engineer** | Visual search, product recommendations | FAISS IVF+PQ | Memory-efficient (32x compression), fits on CPU |
| **Data Deduplication Specialist** | Near-duplicate detection | datasketch (MinHash/LSH) | Billion-scale with GB RAM, 95% recall |
| **Content Recommender** | Music/video "more like this" | Annoy | Spotify's choice, simple, memory-mapped |
| **Research Scientist** | Benchmarking, prototyping | FAISS + ScaNN | SOTA baselines, ann-benchmarks compatible |

---

## Quick Decision Tree

### Step 1: What type of data?

**Text/Documents (sets, shingles)?**
→ **datasketch** (MinHash for Jaccard, SimHash for near-duplicates)

**Dense vectors (embeddings)?**
→ Continue to Step 2

---

### Step 2: What's your scale?

**<1M vectors**
→ **Annoy** (simple, fast to prototype)

**1M - 10M vectors**
→ **FAISS IVF** (speed) or **FAISS HNSW** (accuracy)

**>10M vectors**
→ **FAISS IVF+PQ** (memory compression)

---

### Step 3: What's your accuracy requirement?

**85-95% recall**
→ **Annoy** or **FAISS IVF**

**>95% recall**
→ **FAISS HNSW** or **ScaNN**

---

### Step 4: What's your deployment environment?

**Google Cloud**
→ **ScaNN** (Vertex AI Vector Search)

**Self-hosted / Multi-cloud**
→ **FAISS** (proven, widely adopted)

**Memory-constrained**
→ **datasketch** (for sets) or **FAISS PQ** (for vectors)

---

## Use-Case-Specific Recommendations

### RAG Systems

**Best choice:** FAISS (IVF or HNSW)

**Configuration:**
- **Speed-optimized:** IVFPQ (15K QPS, 94% recall, 1 GB for 1M vectors)
- **Accuracy-optimized:** HNSW (6K QPS, 99% recall, 4.5 GB for 1M vectors)

**Deployment:**
- Vector DB: Milvus, Weaviate (FAISS backend)
- Self-hosted: FAISS + Redis/PostgreSQL for metadata

**Critical success factors:**
- Recall >95% (missing docs → LLM hallucinates)
- Latency <100ms (interactive chat)
- GPU acceleration (batch embedding + search)

---

### E-Commerce Search

**Best choice:** FAISS IVF+PQ

**Why:**
- Memory: 10M products × 512 dims × 4 bytes = 20 GB → 625 MB (32x compression)
- Cost: Fits on CPU server ($0.38/hour vs $1.50/hour GPU)
- Speed: 15K QPS at 94% recall

**Alternative:** Annoy (if catalog <1M)

**Critical success factors:**
- <50ms latency (real-time product pages)
- 90%+ recall (balance speed/relevance)
- Incremental updates (new products hourly)

---

### Data Deduplication

**Best choice:** datasketch (MinHash + LSH)

**Why:**
- Memory: 10B documents, 128-byte signature = 1.2 TB (vs petabytes for raw text)
- Speed: Sub-linear LSH search (O(1) vs O(N²) pairwise)
- Precision: 90-95% with tuned parameters

**Alternative:** FAISS (if using document embeddings, not text hashes)

**Critical success factors:**
- Recall >95% (missing duplicates = data quality issues)
- Precision >90% (false positives = manual review overhead)
- Batch processing (overnight jobs acceptable)

---

### Content Recommendation

**Best choice:** Annoy

**Why:**
- Proven: Spotify's music recommendations
- Simple: 5-min setup, production-ready
- Memory-mapped: Share index across web workers

**Alternative:** FAISS IVF+PQ (if catalog >10M or need >95% recall)

**Critical success factors:**
- <100ms latency (real-time homepage)
- 85-95% recall (diversity matters more than perfect accuracy)
- Hybrid with collaborative filtering (content + user preferences)

---

### Research & Benchmarking

**Best choice:** FAISS + ScaNN

**Why:**
- FAISS: SOTA baseline (IVF+PQ, HNSW), widely cited
- ScaNN: Cutting-edge (anisotropic quantization, SOAR)
- ann-benchmarks compatible (reproducible comparisons)

**Critical success factors:**
- Compare against SOTA baselines
- Use standard datasets (SIFT1M, glove-100-angular)
- Report recall@K, QPS, memory, build time
- Publish code + results (reproducibility)

---

## Common Patterns Across Use Cases

### Pattern 1: Two-Stage Retrieval
```
Stage 1: Fast approximate search (FAISS PQ, Annoy, LSH) → 1000 candidates
Stage 2: Exact re-ranking → top-10 results
```

**Use cases:** RAG (high recall), e-commerce (business rules), deduplication (exact Jaccard)

---

### Pattern 2: Hybrid Vector + Metadata
```
Vector search (FAISS/Annoy) → 500 candidates
Filter by metadata (price, category, in-stock) → 100 candidates
Re-rank by hybrid score (similarity × popularity × recency) → top-20
```

**Use cases:** E-commerce, content recommendation

---

### Pattern 3: Batch Processing
```
1. Collect items overnight (new products, articles)
2. Batch embed (GPU)
3. Rebuild index (FAISS/Annoy)
4. Blue-green deploy (swap old index with new)
```

**Use cases:** E-commerce (daily updates), news aggregation, deduplication

---

### Pattern 4: Multi-Modal Ensemble
```
Index 1: Image embeddings (FAISS)
Index 2: Text embeddings (FAISS)
Index 3: Metadata (Annoy)
→ Combine scores → top-K
```

**Use cases:** E-commerce (visual + text), content recommendation (audio + lyrics)

---

## Anti-Patterns to Avoid

### ❌ Using Exact Search for >10K Vectors
**Problem:** O(N) query time too slow
**Solution:** Use approximate search (IVF, HNSW, Annoy)

### ❌ Using FAISS for <10K Vectors
**Problem:** Overkill, Annoy is simpler
**Solution:** Start with Annoy, graduate to FAISS when scale demands

### ❌ Ignoring Recall Metrics
**Problem:** Fast but inaccurate → poor user experience
**Solution:** Benchmark recall on real queries, A/B test impact on engagement

### ❌ Using datasketch for Dense Vectors
**Problem:** Designed for sets (Jaccard), not embeddings
**Solution:** Use FAISS/Annoy for embeddings

### ❌ Real-Time Index Updates
**Problem:** All libraries batch-oriented (rebuild required)
**Solution:** Dual-index pattern (hot + cold), merge periodically

---

## Key Takeaways

1. **RAG Systems → FAISS** (industry standard, GPU support)
2. **E-Commerce → FAISS IVF+PQ** (memory-efficient, CPU-friendly)
3. **Deduplication → datasketch** (billion-scale, memory-efficient)
4. **Content Recs → Annoy** (Spotify's proven choice)
5. **Research → FAISS + ScaNN** (SOTA baselines)

**When in doubt:** Start with **Annoy** (prototype) → Graduate to **FAISS** (production)

---

## Next Steps

- **S4-Strategic:** Long-term considerations (maintenance, ecosystem, vendor stability)
- **DOMAIN_EXPLAINER:** Understand similarity search fundamentals (if new to the field)
