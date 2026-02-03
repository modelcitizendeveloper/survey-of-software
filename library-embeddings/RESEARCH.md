# Research Path: Strengthening Library Embeddings

**Goal:** Enhance embeddings quality, validate against baselines, prepare for publication.

---

## Phase 1: Codebase Sampling (2-3 weeks)

**Objective:** Add real-world usage patterns to strengthen embeddings.

### What We Have Now
- **Data source:** Research topics only (75 "sentences")
- **Signal:** Which libraries are studied together (expert curation)
- **Limitation:** Small corpus, research-biased

### What Codebase Adds
- **Data source:** 500-1000 real Python repositories
- **Signal:** Which libraries are imported together in production code
- **Benefit:** Pragmatic co-use patterns, larger corpus

### Implementation

**Sampling strategy (already designed):**
- 500 repos across 10 domains (web, ML, data science, etc.)
- GitHub API: `stars:10..500` (avoids popularity bias)
- Equal representation per domain (no Steinberg distortion)
- AST parsing for imports (not regex)
- Only repos updated 2023-2025 (current practices)

**Deliverables:**
1. GitHub query script (reproducible sampling)
2. AST import parser
3. Extended co-occurrence matrix (research + codebase)
4. Re-trained embeddings (dual signal)
5. Comparison report (old vs new embeddings)

**Effort:** 1 week scripting + 2 hours processing + 1 week analysis

**Output:** Stronger embeddings, richer clusters, better analogies

---

## Phase 2: LibRec Baseline Comparison (1 week)

**Objective:** Quantify improvement over collaborative filtering approach.

### What Is LibRec?

LibRec (2016) used collaborative filtering on GitHub repo dependencies:
- "Repos using X also use Y" → recommend Y
- Binary co-occurrence (uses/doesn't use)
- Evaluated on 50K GitHub repos

### Our Comparison

**Replicate their approach:**
1. Build binary co-occurrence matrix from our data
2. Generate recommendations via collaborative filtering
3. Compare to our nearest neighbors

**Evaluation metrics:**
- Precision@k: Are our top-k similar libraries better than CF's?
- Diversity: Do embeddings suggest more diverse alternatives?
- Analogies: Can CF do vector arithmetic? (No - only we can)

**Expected finding:** Embeddings capture more nuance than binary co-occurrence.

**Deliverables:**
1. LibRec replication script
2. Comparison table (CF vs embeddings)
3. Case studies showing where embeddings excel

**Effort:** 3 days implementation + 2 days analysis

**Output:** Quantitative validation of our approach

---

## Phase 3: Cross-Ecosystem Extension (2-3 weeks)

**Objective:** Prove approach generalizes beyond Python.

### Extend to npm (JavaScript)

**Why npm:**
- Similar package ecosystem structure
- Different community practices (frontend vs backend focus)
- Tests generalizability

**Approach:**
1. Adapt extraction for package.json, npm registry
2. Sample 500 JavaScript repos (same methodology)
3. Train embeddings on npm libraries
4. Compare: Are JS library relationships similar to Python?

**Questions answered:**
- Are library relationships universal or ecosystem-specific?
- Do analogies work across languages? (e.g., express → fastify in JS)
- Which patterns transfer? Which are unique?

### Optional: Add Rust (Cargo)

**Why Rust:**
- Smaller ecosystem (easier to process)
- Different paradigm (systems programming vs application)
- Strong test of generalizability

**Deliverables:**
1. npm embeddings (100d model)
2. Optional: Rust/Cargo embeddings
3. Cross-ecosystem comparison report
4. Universal patterns identified

**Effort:** 1 week per ecosystem

**Output:** Multi-language library embeddings, transferability analysis

---

## Phase 4: Intrinsic Evaluation (1 week)

**Objective:** Measure embedding quality with standard NLP metrics.

### Analogy Accuracy

Build test set of known library relationships:
```
flask : fastapi :: django : ?  (Expected: fastapi or similar async framework)
requests : httpx :: urllib : ?
numpy : cupy :: pandas : ?  (GPU-accelerated versions)
```

**Metric:** % of analogies where expected answer is in top-k

### Cluster Coherence

Manually label libraries by domain:
- Web frameworks: flask, django, fastapi, tornado
- ML libraries: torch, tensorflow, jax, mxnet
- Data viz: matplotlib, plotly, seaborn, bokeh

**Metric:** Silhouette score, intra-cluster distance

### Nearest Neighbor Quality

Manual inspection by domain experts:
- For each library, review top-10 nearest neighbors
- Label: Relevant / Somewhat relevant / Not relevant
- Compute: Precision@10, nDCG

**Deliverables:**
1. Analogy test set (50-100 examples)
2. Domain labels for clustering
3. Quality metrics report

**Effort:** 2 days test set creation + 3 days evaluation

**Output:** Quantitative quality scores

---

## Phase 5: Dimensionality Study (3 days)

**Objective:** Optimize embedding dimensions for downstream tasks.

### Current State
We trained 50d, 100d, 300d models arbitrarily.

### Systematic Evaluation

Test dimensions: 25, 50, 75, 100, 150, 200, 300

**For each:**
- Train embeddings
- Measure analogy accuracy
- Measure cluster coherence
- Note training time

**Find:**
- Minimum dimensions for good analogies
- Diminishing returns point
- Speed/quality tradeoff

**Deliverables:**
1. Dimension sweep results
2. Recommended dimensions for different use cases
3. Performance vs quality curves

**Effort:** 1 day training + 2 days analysis

**Output:** Optimized embeddings for production use

---

## Research Timeline

### 6-Week Plan

| Week | Phase | Output |
|------|-------|--------|
| 1-2 | Codebase sampling | Extended embeddings (research + usage) |
| 3 | LibRec baseline | Quantitative comparison |
| 4 | Intrinsic evaluation | Quality metrics |
| 5 | Cross-ecosystem (npm) | JavaScript embeddings |
| 6 | Dimensionality study | Optimized models |

**Total effort:** ~6 weeks (can parallelize some phases)

### 12-Week Extended Plan

Add:
- Weeks 7-8: Rust/Cargo ecosystem
- Weeks 9-10: User study (see PUBLICATION.md)
- Weeks 11-12: Paper writing

---

## Expected Outcomes

### Stronger Embeddings
- 10x more training data (500-1000 repos vs 75 topics)
- Dual signal (research + usage)
- Better analogies, richer clusters

### Quantitative Validation
- LibRec comparison shows improvement
- Intrinsic metrics (analogy accuracy, cluster coherence)
- Cross-ecosystem proves generalizability

### Production-Ready
- Optimized dimensions
- Reproducible methodology
- Multiple ecosystems supported

### Publication-Ready
- Novel contribution validated
- Baselines compared
- Extensible framework demonstrated

---

## Open Research Questions

### 1. Optimal Signal Weighting

How should we weight research vs codebase signals?
- Research: High quality, low volume, curated
- Codebase: High volume, noisy, real-world

**Approaches to test:**
- Equal weight (50/50)
- Inverse frequency weighting (rare libraries up-weighted)
- Confidence-weighted (research gets higher confidence)

### 2. Temporal Embeddings

Do library relationships change over time?
- Sample repos from 2015, 2017, 2019, 2021, 2023, 2025
- Train separate embeddings per time period
- Track: Which libraries rise/fall? Which relationships shift?

**Use case:** "What was the 2019 equivalent of fastapi?" (Answer: flask)

### 3. Domain-Specific Embeddings

Should we train separate embeddings per domain?
- ML libraries (specialized vocabulary)
- Web libraries (different patterns)
- Data science (distinct ecosystem)

**vs.** Single universal embedding (captures cross-domain relationships)

### 4. Hierarchical Embeddings

Can we capture library-API-function hierarchy?
- Library level (our current work)
- Module level (numpy.linalg, pandas.DataFrame)
- Function level (API2Vec's domain)

**Benefit:** Multi-granularity similarity search

---

## Next Steps

### Immediate (This Week)
1. Start codebase sampling Phase 1
2. Build GitHub query script
3. Pilot on 50 repos to validate pipeline

### Short-term (This Month)
1. Complete 500-repo sample
2. Re-train embeddings (dual signal)
3. Run LibRec comparison

### Long-term (Next Quarter)
1. Extend to npm/Cargo
2. Run user study
3. Write paper draft

---

## Resources Needed

### Compute
- Modest: Single machine, 8GB RAM, 4 cores
- Processing time: ~2 hours for 500 repos
- Storage: ~5GB for repo clones (deleted after extraction)

### Data Access
- GitHub API token (free tier: 5000 req/hour)
- Libraries.io API key (free, already have)
- Optional: BigQuery access for large-scale analysis

### Time
- Agent work: ~40-60 hours total (6-8 weeks)
- Human review: ~10 hours (validate samples, review results)

---

## Success Metrics

**Research quality:**
- ✅ Analogy accuracy >70% (top-5)
- ✅ Cluster coherence >0.7 (silhouette score)
- ✅ LibRec baseline improvement >20%

**Publication readiness:**
- ✅ Novel contribution validated
- ✅ Reproducible methodology documented
- ✅ 2+ ecosystems demonstrated
- ✅ User study shows utility

**Production readiness:**
- ✅ API for library similarity queries
- ✅ Web interface for exploration
- ✅ Integrated into Survey of Software site
