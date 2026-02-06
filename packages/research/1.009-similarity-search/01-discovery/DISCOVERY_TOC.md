# Discovery Table of Contents: Similarity Search Libraries

**Research Status:** Complete (S1-S4)
**Last Updated:** 2026-01-30

---

## Quick Navigation

- **New to similarity search?** Start with [DOMAIN_EXPLAINER.md](../DOMAIN_EXPLAINER.md)
- **Need a library in 15 minutes?** Read [S1-rapid](#s1-rapid-discovery)
- **Planning architecture?** See [S2-comprehensive](#s2-comprehensive-analysis)
- **Know your use case?** Check [S3-need-driven](#s3-need-driven-discovery)
- **Making long-term decisions?** Review [S4-strategic](#s4-strategic-selection)

---

## S1-rapid Discovery

**Time investment:** ~15 minutes | **Goal:** Pick a library quickly

### Overview
- [approach.md](S1-rapid/approach.md) - Methodology and decision framework

### Library Comparisons
- [faiss.md](S1-rapid/faiss.md) - Meta's production-grade library (38.9K stars)
- [annoy.md](S1-rapid/annoy.md) - Spotify's lightweight solution (14.1K stars)
- [scann.md](S1-rapid/scann.md) - Google's SOTA accuracy library
- [datasketch.md](S1-rapid/datasketch.md) - LSH/MinHash for set similarity (2.9K stars)

### Decision Guide
- [recommendation.md](S1-rapid/recommendation.md) - Quick decision tree and red flags

**Key takeaway:** FAISS for production, Annoy for prototypes, datasketch for deduplication

---

## S2-comprehensive Analysis

**Time investment:** ~90 minutes | **Goal:** Understand how they work

### Overview
- [approach.md](S2-comprehensive/approach.md) - Deep-dive methodology

### Technical Analysis
- [faiss.md](S2-comprehensive/faiss.md) - IVF, PQ, HNSW algorithms explained
- [annoy.md](S2-comprehensive/annoy.md) - Random projection trees deep-dive
- [scann.md](S2-comprehensive/scann.md) - Anisotropic vector quantization
- [datasketch.md](S2-comprehensive/datasketch.md) - MinHash, LSH, SimHash theory

### Comparison & Selection
- [feature-comparison.md](S2-comprehensive/feature-comparison.md) - Algorithm complexity, performance benchmarks
- [recommendation.md](S2-comprehensive/recommendation.md) - Architecture-grade selection guide

**Key takeaway:** FAISS IVF+PQ for memory optimization, HNSW for accuracy, ScaNN for inner-product

---

## S3-need-driven Discovery

**Time investment:** ~55 minutes | **Goal:** Match library to your use case

### Overview
- [approach.md](S3-need-driven/approach.md) - Use-case-driven methodology

### Use Case Guides
- [use-case-rag-systems.md](S3-need-driven/use-case-rag-systems.md) - LLM retrieval-augmented generation
- [use-case-ecommerce-search.md](S3-need-driven/use-case-ecommerce-search.md) - Product search, visual similarity
- [use-case-data-deduplication.md](S3-need-driven/use-case-data-deduplication.md) - Near-duplicate detection, record linkage
- [use-case-content-recommendation.md](S3-need-driven/use-case-content-recommendation.md) - Music, video, news recommendations
- [use-case-research-scientists.md](S3-need-driven/use-case-research-scientists.md) - Academic/industrial research, benchmarking

### Decision Matrix
- [recommendation.md](S3-need-driven/recommendation.md) - Use-case-specific recommendations

**Key takeaway:** RAG → FAISS, E-commerce → FAISS IVF+PQ, Dedup → datasketch, Recs → Annoy, Research → FAISS+ScaNN

---

## S4-strategic Selection

**Time investment:** ~75 minutes | **Goal:** Long-term viability assessment

### Overview
- [approach.md](S4-strategic/approach.md) - Strategic decision framework

### Viability Analysis
- [faiss-viability.md](S4-strategic/faiss-viability.md) - ⭐⭐⭐⭐⭐ Meta backing, massive community, 5-10+ year horizon
- [annoy-viability.md](S4-strategic/annoy-viability.md) - ⭐⭐⭐ Stable but maintenance mode, 1-3 year horizon
- [scann-viability.md](S4-strategic/scann-viability.md) - ⭐⭐⭐ Google Cloud lock-in, 3-5 year horizon
- [datasketch-viability.md](S4-strategic/datasketch-viability.md) - ⭐⭐⭐⭐ Best for deduplication niche, 3-5 year horizon

### Strategic Guidance
- [recommendation.md](S4-strategic/recommendation.md) - Long-term decision framework, TCO, migration paths

**Key takeaway:** FAISS is safest long-term bet, Annoy for prototyping, ScaNN if Google Cloud committed

---

## Cross-Cutting Themes

### Performance Benchmarks

| Library | QPS (1M vectors) | Recall@10 | Memory (1M, 768-dim) |
|---------|------------------|-----------|----------------------|
| FAISS Flat | 120 | 100% | 3 GB |
| FAISS IVF | 8,500 | 95% | 3 GB |
| FAISS PQ | 12,000 | 93% | 100 MB |
| FAISS HNSW | 6,000 | 99% | 4.5 GB |
| Annoy (50 trees) | 53 | 93.5% | 300 MB |
| ScaNN | 2,400 | 98.5% | 200 MB |

### Quick Decision Matrix

| Use Case | Primary Choice | Alternative | Why |
|----------|---------------|-------------|-----|
| RAG Systems | FAISS | ScaNN | Industry standard, GPU support |
| E-Commerce | FAISS IVF+PQ | Annoy | Memory-efficient, CPU-friendly |
| Deduplication | datasketch | FAISS | Billion-scale, set similarity |
| Recommendations | Annoy | FAISS | Spotify's proven choice |
| Research | FAISS + ScaNN | - | SOTA baselines |

### Cost Estimates (5-Year TCO, 10M vectors)

| Deployment | Infrastructure | Engineering | Total |
|------------|----------------|-------------|-------|
| FAISS self-hosted (CPU) | $50K | $84K | $134K |
| Annoy self-hosted | $13K | $24K | $37K |
| ScaNN (Vertex AI) | $120K | $10K | $130K |
| datasketch (batch) | $2K | $38K | $40K |

---

## How to Use This Research

### Scenario 1: "I need to ship in 2 weeks"
1. Read S1-rapid (15 min)
2. Choose Annoy (simplest)
3. Prototype and iterate

### Scenario 2: "I'm architecting a new system"
1. Read S1-rapid (15 min)
2. Read S2-comprehensive (90 min)
3. Read relevant S3 use case (10 min)
4. Choose FAISS (production-grade)

### Scenario 3: "I'm planning for 3-5 years"
1. Read S1-rapid (15 min)
2. Read S4-strategic (75 min)
3. Consider FAISS + vector DB abstraction (Milvus, Weaviate)

### Scenario 4: "I'm benchmarking for research"
1. Read S2-comprehensive (90 min)
2. Read use-case-research-scientists (10 min)
3. Use FAISS + ScaNN as baselines

---

## Related Research

### Within This Category
- **String metrics** (1.032) - Character-level similarity (Levenshtein, Jaro-Winkler)
- **Embedding models** - Generate vectors for similarity search (BERT, CLIP)

### Complementary Topics
- **Vector databases** - Abstraction layers over FAISS/Annoy (Milvus, Weaviate)
- **RAG frameworks** - LLM systems using similarity search (LangChain, LlamaIndex)
- **Deduplication pipelines** - ETL workflows using MinHash/LSH

---

## Research Methodology

All four passes (S1-S4) were completed following the 4PS framework:

- **S1-rapid:** Ecosystem scan, benchmark analysis, quick comparison
- **S2-comprehensive:** Algorithm deep-dive, performance profiling, feature matrices
- **S3-need-driven:** Use case analysis, requirements mapping, validation checklists
- **S4-strategic:** Vendor stability, community health, TCO calculations, migration paths

**Quality confidence:**
- S1: 70-80% (speed-optimized)
- S2: 80-90% (depth-optimized)
- S3: 75-85% (context-specific)
- S4: 60-70% (forward-looking)

**Accuracy window:** Research conducted Jan 2026. Expect ~50% accuracy after 12 months due to library evolution.

---

## Feedback & Updates

Found an error or have an update? This is a living document.

**Last major update:** 2026-01-30 (Initial research completion)
