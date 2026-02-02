# Use Case: Data Deduplication Specialists

## Who Needs This

**User Persona:** Data engineers and ETL pipeline builders focused on deduplication and record linkage

**Context:**
- Web scraping (remove duplicate articles, product listings)
- Database cleanup (merge duplicate customer records)
- Document management (find near-duplicate files)
- Log analysis (deduplicate error messages, cluster similar events)
- Scale: 1M to 1B records
- Latency: Batch processing (minutes to hours acceptable)

**Examples:**
- News aggregators (deduplicate articles from multiple sources)
- CRM systems (merge duplicate contact records)
- Legal discovery (find similar documents in litigation datasets)
- Data warehouses (entity resolution across data sources)

## Why They Need Similarity Search

**Problem:** Exact deduplication (MD5 hashing) misses near-duplicates (typos, reformatting, minor edits)

**Solution:**
1. **Text:** Hash documents using MinHash/SimHash → find duplicates via LSH
2. **Structured data:** Embed records into vectors → find similar records via FAISS
3. **Batch process:** Group similar items, merge/deduplicate

**Critical requirements:**
- **Recall:** >95% (missing duplicates = data quality issues)
- **Precision:** >90% (false positives = manual review overhead)
- **Memory efficiency:** Process billion-scale datasets with GB RAM (not TB)
- **Throughput:** Process millions of records per hour

## Requirements Breakdown

### Must-Have
- ✅ High recall (>95%) to catch near-duplicates
- ✅ Memory efficiency (billion-scale on commodity hardware)
- ✅ Batch processing (real-time latency not critical)
- ✅ Precision >90% (minimize false positives)

### Nice-to-Have
- 🟡 Incremental deduplication (process new data without reprocessing entire dataset)
- 🟡 Configurable similarity threshold (e.g., 80% vs 95% similarity)
- 🟡 Distributed processing (Spark/Dask integration)

### Can Compromise
- ⚠️ Query latency (batch jobs run overnight)
- ⚠️ Perfect accuracy (manual review of edge cases acceptable)
- ⚠️ GPU acceleration (CPU-only fine for batch work)

## Library Recommendations by Data Type

### Text Deduplication: datasketch (MinHash + LSH)

**Why datasketch:**
- **Memory efficiency:** 10B documents, 128-byte signature each = **1.2 TB** (vs petabytes for raw text)
- **Speed:** Sub-linear search via LSH (O(1) vs O(N) pairwise comparison)
- **Precision:** 90-95% with tuned parameters
- **Proven:** Used by Common Crawl, web archiving projects

**Algorithm choice:**
```
MinHash (for Jaccard similarity):
- Use case: Document deduplication (compare text as sets of shingles)
- Signature size: k=128 (±8.8% error)
- LSH: b=16 bands, r=8 rows → threshold ≈ 0.55

SimHash (for near-duplicates):
- Use case: Near-duplicate detection (Hamming distance ≤3 bits)
- Signature: 64-bit hash
- Good for: Web page deduplication
```

**Deployment:**
```
1. Extract shingles (3-word sequences: "quick brown fox", "brown fox jumps", ...)
2. Compute MinHash signature (128 hash functions)
3. Insert into LSH index (16 bands)
4. Query each new document → find candidates with J(A,B) > 0.55
5. Exact Jaccard on candidates → filter to J(A,B) > 0.8
6. Merge duplicates
```

**Performance (10M documents):**
- Build time: 2 hours (CPU)
- Memory: 10M × 128 bytes = 1.28 GB
- Recall: 95% (J > 0.8)
- Precision: 98%

### Structured Record Deduplication: FAISS (IVF or HNSW)

**Why FAISS:**
- **Dense embeddings:** Entity embeddings (names, addresses, attributes) → 128-512 dim vectors
- **High recall:** HNSW achieves 99% recall
- **Speed:** GPU-accelerated batch embedding + search

**Use case examples:**
- Customer records (similar names, addresses)
- Product catalogs (similar titles, descriptions)
- Company databases (entity resolution)

**Workflow:**
```
1. Embed records (Sentence-BERT, entity embeddings)
2. Build FAISS index (HNSW for accuracy)
3. For each record, query top-10 similar records
4. If similarity > 0.9, flag as potential duplicate
5. Manual review or auto-merge based on rules
```

**Performance (1M records, 384-dim embeddings):**
- Embedding: 1M records in 10 min (GPU batch)
- Index build: 20 min (HNSW)
- Search: 1M queries in 5 min (GPU, batch size 10K)
- Recall@10: 99%
- Precision: 85% (requires post-filtering)

### Hybrid Approach: Text + Metadata

**Combine datasketch (text) + FAISS (structured):**

```
Stage 1: MinHash LSH (text content) → 100 candidates per record
Stage 2: FAISS (metadata embeddings) → re-rank candidates
Stage 3: Rule-based filtering (exact match on email, phone)
Stage 4: Manual review (similarity 0.8-0.95)
```

**Example:** CRM deduplication
- Text: Company description (MinHash, J > 0.7)
- Metadata: Company name + address embedding (FAISS, cosine > 0.85)
- Rules: Exact match on domain, phone
- **Result:** 97% recall, 92% precision

### Not Recommended: Annoy

**Annoy:**
- ❌ Recall plateaus at 93% (too low for deduplication)
- ❌ No memory compression (not efficient for billion-scale)
- Use FAISS or datasketch instead

## Real-World Example: News Article Deduplication

**Scenario:** Aggregate 10M news articles/day from 1000 sources, deduplicate

**Requirements:**
- Throughput: 10M articles/day = 115 articles/second
- Recall: >95% (don't miss duplicates)
- Precision: >90% (minimize false positives)
- Latency: Batch processing (hourly jobs)

**Solution:**
1. **Preprocessing:** Extract 3-word shingles from article text
2. **Hashing:** MinHash with k=128 hash functions
3. **LSH:** b=20 bands, r=6 rows → threshold ≈ 0.5
4. **Post-filtering:** Exact Jaccard on candidates, threshold 0.75
5. **Deduplication:** Group duplicates, keep earliest published

**Implementation (Apache Spark):**
```
1. Map: article → MinHash signature (parallelized)
2. LSH: Insert into 20 LSH buckets (distributed hash tables)
3. Reduce: For each bucket, compute pairwise Jaccard
4. Filter: Keep pairs with J > 0.75
5. Group: Union-find to cluster duplicates
```

**Results:**
- Processing time: 30 min/day (100-node Spark cluster)
- Memory: 10M × 128 bytes = 1.28 GB (signature storage)
- Duplicates found: 2.5M/day (25% duplication rate)
- Recall: 96% (measured on labeled dataset)
- Precision: 94%
- Cost: $5/day (AWS EMR spot instances)

## Common Pitfalls

### Pitfall 1: Using Exact Hash (MD5) for Near-Duplicates
**Problem:** Misses duplicates with minor differences (whitespace, punctuation)
**Solution:** Use MinHash/SimHash for fuzzy matching

### Pitfall 2: Low Signature Size (k=16)
**Problem:** High error (±25%), misses many duplicates
**Solution:** Use k=128 (±8.8% error) or k=256 (±6.25%)

### Pitfall 3: Pairwise Comparison (O(N²))
**Problem:** 10M articles → 50 trillion comparisons (months to compute)
**Solution:** Use LSH for sub-linear search (O(N) build, O(1) query)

### Pitfall 4: Ignoring False Positives
**Problem:** LSH at threshold 0.5 → 20% false positive rate → manual review overhead
**Solution:** Two-stage filtering (LSH candidates → exact Jaccard → threshold 0.8)

## Validation Checklist

Before deploying deduplication pipeline:
- [ ] Benchmark on labeled dataset (1000+ duplicate pairs)
- [ ] Measure recall and precision (target: 95%+ recall, 90%+ precision)
- [ ] Tune LSH parameters (b, r) for precision/recall trade-off
- [ ] Load test batch processing (ensure throughput meets SLA)
- [ ] Monitor memory usage (ensure signatures fit in available RAM)

## Scaling Path

**1M records:** datasketch MinHash + LSH (single machine)
**10M records:** datasketch + Apache Spark (distributed LSH)
**100M records:** datasketch + Cassandra storage backend (distributed)
**1B+ records:** datasketch + Spark + S3 (signatures stored in S3)

## Alternative: Probabilistic vs Learned Embeddings

### Probabilistic (datasketch)
- **Pros:** Memory-efficient, no training, deterministic
- **Cons:** Fixed similarity metric (Jaccard), approximate

### Learned Embeddings (FAISS + BERT)
- **Pros:** Semantic similarity (e.g., "NYC" ≈ "New York"), high accuracy
- **Cons:** Requires training/finetuning, GPU for embedding, larger memory

**Hybrid:** Use datasketch for first-pass (fast, cheap), FAISS for second-pass (accurate)

## Related Use Cases

- **Plagiarism detection:** Document similarity (MinHash or FAISS with doc embeddings)
- **Record linkage:** Merge records across databases (FAISS with entity embeddings)
- **Log clustering:** Group similar error messages (SimHash or FAISS)
