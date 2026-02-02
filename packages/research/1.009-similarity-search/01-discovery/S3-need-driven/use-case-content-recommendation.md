# Use Case: Content Recommendation Systems

## Who Needs This

**User Persona:** ML engineers building recommendation systems for media platforms

**Context:**
- Music streaming (playlist generation, "more like this")
- Video platforms (recommended videos, similar content)
- News aggregators (personalized feed)
- Podcast apps (discover similar shows)
- Scale: 1M to 100M items, 10M to 1B users
- Latency target: <100ms for real-time recommendations

**Examples:**
- Spotify's "Discover Weekly" (find similar songs to user's listening history)
- YouTube's "Recommended Videos" (suggest videos based on watch history)
- Netflix's "Because You Watched" (movie/show similarity)
- Reddit's "Similar Posts" (content-based recommendations)

## Why They Need Similarity Search

**Problem:** Collaborative filtering (user-item matrix) struggles with cold-start (new items) and sparsity

**Solution:**
1. **Content-based filtering:** Embed items (songs, videos, articles) into vectors
2. **Similarity search:** For each user interaction, find K similar items
3. **Personalized ranking:** Re-rank by user preferences, popularity, recency

**Critical requirements:**
- **Latency:** <100ms (real-time homepage recommendations)
- **Recall:** 85-95% (missing relevant items OK if top-K is good)
- **Scale:** 10M+ items, billions of user-item interactions
- **Memory efficiency:** Fit on commodity servers (CPU or small GPU)

## Requirements Breakdown

### Must-Have
- ✅ <100ms latency (p95)
- ✅ Scale to 10M+ items
- ✅ Support 64-512 dim embeddings (audio, video, text features)
- ✅ Memory-efficient (CPU servers, not expensive GPUs)
- ✅ 85%+ recall (balance speed/diversity)

### Nice-to-Have
- 🟡 Incremental updates (add new songs/videos hourly)
- 🟡 Multi-modal search (audio + lyrics, video + title)
- 🟡 Diversity-aware ranking (avoid filter bubbles)
- 🟡 A/B testing framework (experiment with similarity thresholds)

### Can Compromise
- ⚠️ Perfect accuracy (90% recall OK if top-10 recommendations are good)
- ⚠️ Real-time index updates (daily rebuild acceptable)
- ⚠️ Exact search (approximate is faster, users won't notice)

## Library Recommendations

### Primary: Annoy (For Spotify-Scale Music Recommendation)

**Why Annoy:**
- **Proven:** Built by Spotify for music recommendations
- **Speed:** 50+ QPS, sub-ms latency
- **Memory-mapped:** Share index across web server workers (no RAM duplication)
- **Simplicity:** 5-min setup, production-ready

**Index configuration:**
```
AnnoyIndex(f=128, metric='angular')
- n_trees = 50 (good recall/speed balance)
- search_k = 500 (10× n_trees × K)

Dataset: 10M songs, 128-dim audio embeddings
Memory: 10M × 128 × 4 bytes × 50 trees = 25 GB (disk), ~5 GB (hot RAM)
QPS: 60 (CPU), 200+ (SSD-backed)
Recall@10: 92%
```

**Deployment pattern:**
```
1. Offline: Train audio embedding model (e.g., MusicNN, OpenL3)
2. Batch: Embed all songs → build Annoy index (nightly)
3. Serving: Load index via mmap, share across workers
4. Query: User played song X → find 100 similar songs → re-rank by popularity/recency
```

**Why Annoy over FAISS for music:**
- Simpler (no parameter tuning)
- Memory-mapped (multi-process sharing)
- Spotify's proven choice (scaled to 100M+ tracks)

### Alternative: FAISS (For Larger Catalogs or Higher Recall)

**Why FAISS:**
- Scales to 100M+ items
- Higher recall (99% with HNSW)
- GPU acceleration for batch recommendations

**When to choose FAISS:**
- Catalog >10M items
- Need >95% recall (high-stakes recommendations)
- Batch processing (generate recs for all users overnight)

**Index configuration (10M videos, 512-dim):**
```
IndexIVFPQ (memory-optimized)
- nlist = 4000
- nprobe = 50
- m = 8, nbits = 8

Memory: 10M × 8 bytes = 80 MB (vs 20 GB uncompressed)
QPS: 15000 (CPU), 50000 (GPU)
Recall@10: 94%
```

### Not Recommended: ScaNN, datasketch

**ScaNN:**
- ⚠️ Overkill for <100M items (Annoy/FAISS simpler)
- ⚠️ Deployment complexity (Google Cloud or monorepo build)

**datasketch:**
- ❌ Designed for set similarity (Jaccard), not dense vectors
- Use only if collaborative filtering (user-item sets, not embeddings)

## Real-World Example: Video Recommendation Platform

**Scenario:** 5M videos, 50M users, recommend "similar videos"

**Requirements:**
- Latency: <50ms (mobile app)
- Recall: 90%+ (show 20 related videos)
- Updates: New videos uploaded hourly
- Cost: <$1000/month (startup budget)

**Solution:**
1. **Embedding:** Video2Vec (512-dim from video frames + audio + title)
2. **Index:** FAISS IVFPQ (nlist=3000, nprobe=75, m=8)
3. **Hardware:** 3× m5.xlarge (16 GB RAM each, $0.19/hour)
4. **Memory:** 5M × 8 bytes = 40 MB + 250 MB codebooks = **290 MB per replica**
5. **Update strategy:** Rebuild index every 6 hours, blue-green deploy

**Results:**
- Query latency: 8ms (p50), 35ms (p95)
- Recall@20: 91%
- Cost: 3 instances × $0.19/hour × 730 hours = **$416/month**
- Engagement lift: +23% (from related videos)

**Optimization:** Use Annoy instead → 5 GB index (no compression), 60 QPS, 92% recall, same latency

## Content-Based vs Collaborative Filtering

### Content-Based (Similarity Search)
**Pros:**
- No cold-start (works for new items immediately)
- Explainable ("Similar to X because...")
- No user data needed (privacy-friendly)

**Cons:**
- Filter bubble (recommendations too similar)
- Misses user preferences (ignores watch history)

### Collaborative Filtering (Matrix Factorization)
**Pros:**
- Captures user preferences ("users like you also liked...")
- Discovers unexpected connections

**Cons:**
- Cold-start problem (new items have no interactions)
- Sparsity (most user-item pairs unobserved)

### Hybrid Approach (Best Practice)

```
1. Collaborative filtering → top-500 candidates (user preferences)
2. Content similarity (FAISS/Annoy) → expand to 1000 candidates (similar items)
3. Ensemble ranking:
   - Score = 0.5 × collab_score + 0.3 × content_score + 0.2 × popularity
4. Diversity filter (ensure variety, not all similar items)
5. Return top-20
```

## Common Pitfalls

### Pitfall 1: Recommending Only Similar Items (Filter Bubble)
**Problem:** User gets stuck in narrow content niche
**Solution:** Inject diversity (MMR, DPP algorithms) or hybrid collaborative filtering

### Pitfall 2: Ignoring Temporal Dynamics
**Problem:** Recommend old, stale content
**Solution:** Blend similarity with recency score (e.g., 0.7 × similarity + 0.3 × log(days_since_publish))

### Pitfall 3: Not A/B Testing Recall Impact on Engagement
**Problem:** Optimizing for recall without measuring clicks/watch-time
**Solution:** A/B test different recall levels, measure user engagement

### Pitfall 4: Using Single Embedding Space for Multi-Modal Content
**Problem:** Mixing audio, visual, text embeddings → poor similarity
**Solution:** Learn joint embedding space (CLIP-style contrastive learning) or use separate indexes + ensemble

## Validation Checklist

Before deploying recommendation system:
- [ ] Benchmark recall@20 on 1000+ user sessions (target >90%)
- [ ] Measure p95 latency under 10K QPS load (target <100ms)
- [ ] A/B test click-through rate (content similarity vs random)
- [ ] Measure diversity (ensure top-20 aren't all from same artist/genre)
- [ ] Monitor cold-start coverage (% of new items recommended within 24h)

## Scaling Path

**100K items:** Annoy (50 trees)
**1M items:** Annoy (100 trees) or FAISS IVF
**10M items:** FAISS IVF+PQ (CPU) or Annoy (SSD-backed)
**100M items:** FAISS IVF+PQ (multi-replica) or Milvus/Weaviate

## Advanced: Multi-Modal Recommendations

**Scenario:** Recommend podcasts based on audio + transcript + metadata

**Solution:**
```
1. Separate embeddings:
   - Audio: Wav2Vec2 (768-dim)
   - Transcript: BERT (384-dim)
   - Metadata: Category + tags (128-dim)

2. Three indexes:
   - FAISS (audio embeddings)
   - FAISS (text embeddings)
   - Annoy (metadata embeddings)

3. Ensemble:
   - Query all 3 indexes → 100 candidates each
   - Combine scores: 0.5 × audio + 0.3 × text + 0.2 × metadata
   - Return top-20
```

**Cost:** 3× indexes, 3× queries, but better relevance (measured via A/B test)

## Related Use Cases

- **Playlist generation:** Seed song → find similar songs → order by flow
- **Cold-start recommendations:** New user → use content similarity (no history yet)
- **Explore vs exploit:** Balance similar items (exploit) with diverse items (explore)
