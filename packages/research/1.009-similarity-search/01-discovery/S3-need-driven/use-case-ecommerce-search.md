# Use Case: E-Commerce Search Engineers

## Who Needs This

**User Persona:** Engineers building product search and recommendation systems for e-commerce platforms

**Context:**
- Visual search ("find similar products to this image")
- Recommendation ("customers who bought this also liked...")
- Duplicate product detection (consolidate vendor catalogs)
- Scale: 100K to 100M products
- Latency target: <50ms for real-time search

**Examples:**
- Fashion retailers (visual similarity: "find dresses like this")
- Marketplaces (aggregate similar listings from multiple sellers)
- Cross-sell engines (recommend complementary products)
- Inventory deduplication (merge identical products)

## Why They Need Similarity Search

**Problem:** Text-based search misses visual similarity and semantic relationships

**Solution:**
1. Embed product images/text into vectors (ResNet, CLIP, BERT)
2. Index vectors for fast similarity search
3. Query: "Find top-20 products similar to [this image/product]"
4. Display results in search/recommendation widgets

**Critical requirements:**
- **Latency:** <50ms (real-time user experience)
- **Scale:** 1M-100M products
- **Accuracy:** 90%+ recall (missing products = lost sales)
- **Memory:** Fit on commodity hardware (cost constraints)

## Requirements Breakdown

### Must-Have
- ✅ Support 128-2048 dim embeddings (vision models: 512-2048, text: 384-768)
- ✅ <50ms latency (p95)
- ✅ Scale to 10M+ products
- ✅ Memory efficiency (host on CPU servers, not GPU)
- ✅ 90%+ recall (balance speed/accuracy for commercial use)

### Nice-to-Have
- 🟡 Incremental updates (add new products hourly)
- 🟡 Metadata filtering (price range, category, brand)
- 🟡 Hybrid scoring (visual similarity × price × ratings)
- 🟡 Multi-modal search (image + text)

### Can Compromise
- ⚠️ Perfect accuracy (90-95% recall acceptable for recommendations)
- ⚠️ GPU acceleration (not cost-effective for 24/7 serving)
- ⚠️ Build time (offline indexing during low-traffic hours)

## Library Recommendations

### Primary: FAISS IVF+PQ (Memory-Optimized)

**Why FAISS IVF+PQ:**
- **Memory compression:** 10M products × 512 dims × 4 bytes = 20 GB → **625 MB** (32x compression)
- **Cost:** Fits on single m5.2xlarge AWS instance (32 GB RAM, $0.38/hour)
- **Speed:** 15K QPS at 94% recall
- **Proven:** Used by Pinterest, Alibaba for product search

**Index configuration:**
```
IndexIVFPQ
- nlist = 4000 (for 10M products)
- nprobe = 50-100
- m = 8 subvectors (512 dims ÷ 64 = 8)
- nbits = 8 (256 centroids per subvector)

Memory: 10M × 8 bytes = 80 MB (vectors) + 545 MB (codebooks/centroids) = 625 MB
QPS: 15000 (CPU), 50000 (GPU)
Recall@20: 93-95%
```

**Deployment:**
- Multi-replica serving (3-5 replicas behind load balancer)
- Hot reload on index update (blue-green deployment)

### Alternative 1: Annoy (For Small Catalogs)

**Why Annoy:**
- **Simplicity:** 5-parameter API, fast prototyping
- **Memory-mapped:** Share index across web server workers
- **Speed:** 50+ QPS, sub-ms latency

**When to choose:**
- Catalog <1M products
- Fast iteration (prototype → MVP → production)
- Memory-sharing critical (multi-process web servers)

**When NOT to choose:**
- Catalog >10M (FAISS scales better)
- Need >95% recall (Annoy plateaus at 93%)

### Alternative 2: ScaNN (For Google Cloud)

**Why ScaNN:**
- Vertex AI Vector Search (managed, auto-scaling)
- Higher accuracy (98%+ recall)
- No ops overhead (index management, backups, HA)

**Cost analysis (10M products):**
- Vertex AI: ~$2000/month (managed)
- Self-hosted FAISS: ~$275/month (3× m5.2xlarge instances)

**Trade-off:** Pay 7x more for managed service, zero ops burden

### Not Recommended: datasketch

**datasketch:**
- ❌ Designed for set similarity (Jaccard), not dense vectors
- ❌ Use only for duplicate detection (text/shingles), not visual search

## Real-World Example: Fashion Retailer

**Scenario:** 5M clothing items, visual similarity search

**Requirements:**
- Latency: <30ms (mobile app)
- Accuracy: >92% recall (show 20 similar items)
- Cost: <$500/month (startup constraints)
- Updates: New items added hourly

**Solution:**
1. **Embedding:** CLIP ViT-B/32 (512-dim image embeddings)
2. **Index:** FAISS IVFPQ (nlist=3000, nprobe=75, m=8, nbits=8)
3. **Hardware:** 2× m5.xlarge (16 GB RAM each, $0.19/hour)
4. **Memory:** 5M × 8 bytes = 40 MB + 300 MB codebooks = **340 MB per replica**
5. **Update strategy:** Rebuild index every 6 hours, blue-green deploy

**Results:**
- Query latency: 12ms (p50), 28ms (p95)
- Recall@20: 93.5%
- Cost: 2 instances × $0.19/hour × 730 hours = **$277/month**
- Conversion lift: +18% (from visual similarity recommendations)

## Common Pitfalls

### Pitfall 1: Not Compressing High-Dimensional Embeddings
**Problem:** 10M × 2048 dims × 4 bytes = 80 GB RAM (requires expensive GPU instance)
**Solution:** Use PQ compression → 2.5 GB (32x reduction)

### Pitfall 2: Ignoring Incremental Updates
**Problem:** Full rebuild takes 30 min → can't add new products in real-time
**Solution:** Dual-index pattern (hot index + cold index, merge hourly)

### Pitfall 3: Serving on GPU for 24/7 Traffic
**Problem:** GPU instances expensive ($1.50-$3/hour) for always-on serving
**Solution:** Use GPU for embedding generation, CPU+PQ for search

### Pitfall 4: Not A/B Testing Recall Impact on Revenue
**Problem:** Optimizing for QPS without measuring business impact
**Solution:** A/B test different recall levels (90% vs 95%), measure conversion rate

## Hybrid Search Pattern

**Combine vector similarity with business logic:**

```
1. Vector search (FAISS) → 1000 candidates (fast, approximate)
2. Filter by business rules:
   - In stock (exclude out-of-stock)
   - Price range (user preferences)
   - Margin (prioritize high-margin products)
3. Re-rank top 100 by hybrid score:
   - Score = 0.7 × visual_similarity + 0.2 × rating + 0.1 × recency
4. Return top 20
```

**Implementation:**
- Store metadata in Redis/Elasticsearch
- FAISS returns IDs → batch lookup metadata → apply filters

## Validation Checklist

Before deploying e-commerce search:
- [ ] Benchmark recall@20 on 1000+ real product queries (target >90%)
- [ ] Measure p95 latency under 10K QPS load (target <50ms)
- [ ] A/B test conversion rate (visual search vs text search)
- [ ] Load test index rebuild process (ensure <5 min downtime)
- [ ] Monitor memory usage (ensure index fits in available RAM)

## Scaling Path

**10K products:** Annoy (prototype)
**100K products:** Annoy or FAISS IVF
**1M products:** FAISS IVF+PQ (CPU)
**10M products:** FAISS IVF+PQ (multi-replica)
**100M products:** FAISS IVF+PQ (sharded across 10+ servers) or Milvus/Weaviate

## Related Use Cases

- **Duplicate detection:** datasketch SimHash for text, FAISS for image duplicates
- **Content-based filtering:** Recommend items similar to user's past purchases
- **Visual search apps:** Pinterest Lens, Google Lens (FAISS or ScaNN backend)
