# Use Case: Cross-lingual Patent Search

## Business Context

**Scenario**: IP research firm providing prior art search services for patent attorneys and corporations filing patents in multiple jurisdictions.

**Problem**: Given a patent application (in any CJK language or English), find similar existing patents across Chinese, Japanese, Korean, and US patent databases. Critical for patentability assessment and avoiding infringement.

**Scale**:
- 5,000 searches/month
- Average search: Query patent (5-10 pages, ~2,000-4,000 characters)
- Search corpus: 50 million patents (Chinese: 20M, Japanese: 10M, Korean: 5M, US/English: 15M)
- Must search across languages (e.g., Chinese query → find similar Japanese/Korean patents)

## Requirements

### Accuracy
- **Target**: >95% recall for relevant patents (cannot miss prior art)
- **Acceptable**: Lower precision (50-70% OK) → humans review results
- **Critical**: False negatives are catastrophic (invalid patent, or miss infringement)
- **Semantic similarity**: Must find conceptually similar patents, not just keyword matches

### Latency
- **Target**: <30 seconds for full cross-lingual search
- **Context**: Analysts run searches iteratively (refining queries)
- **Acceptable**: Up to 60 seconds for complex queries

### Volume & Cost
- 5,000 searches/month (low volume compared to other use cases)
- Budget: <$10,000/month (analyst time costs $50K+/month, so tool can be expensive)
- One-time indexing cost: <$50,000 (to embed entire corpus)

### Patent-Specific Challenges
- **Technical jargon**: Specialized terminology (pharmaceuticals, semiconductors, etc.)
- **Legal language**: Formal, precise, claims vs description structure
- **Cross-lingual concepts**: Same invention described differently in each language
- **Long documents**: 2,000-10,000 characters per patent (context window challenge)

## Model Candidates

### Candidate 1: XLM-RoBERTa (Cross-lingual Embeddings)
**Why**: Proven for semantic search, strong cross-lingual alignment

**Approach**:
- Embed all 50M patents using XLM-R (sentence/paragraph embeddings)
- Store embeddings in vector database (Pinecone, Milvus, FAISS)
- Query: Embed input patent → find nearest neighbors → rank by similarity

**Pros**:
- Strong cross-lingual semantic search (shared embedding space)
- Proven approach (many implementations in research/industry)
- One-time embedding cost (amortized over millions of searches)
- Scales well (vector search is fast)

**Cons**:
- 512 token limit → must chunk long patents (may lose context)
- Embedding quality depends on fine-tuning (need parallel patent data)
- Precision may be lower (embedding-based search less precise than cross-encoders)

### Candidate 2: GPT-4 (Generative Prior Art Search)
**Why**: Best reasoning capability, can read full patents and identify similarity

**Approach**:
- Use GPT-4 to read query patent → generate search keywords/concepts
- Retrieve candidate patents via keyword search (traditional IR)
- GPT-4 re-ranks candidates by reading abstracts → identify truly relevant

**Pros**:
- 128K context (can read full patents, no chunking)
- Best semantic understanding (identifies conceptual similarity)
- Handles technical jargon and legal language well
- No training data needed (zero-shot)

**Cons**:
- Very expensive at scale (5,000 searches × $50+ per search = $250K+/month)
- Latency 10-30 seconds per patent read (re-ranking stage slow)
- Cannot embed entire corpus (50M patents × $0.03/1K tokens = prohibitive)
- Requires hybrid approach (traditional IR + GPT-4 reranking)

### Candidate 3: Hybrid (Traditional IR + XLM-R Reranking)
**Why**: Balance cost and quality

**Approach**:
- **Stage 1**: Keyword-based search (BM25, Elasticsearch) → retrieve top 1,000 candidates (fast, cheap)
- **Stage 2**: XLM-R cross-encoder re-ranks top 1,000 → output top 100 (semantic similarity)
- **Stage 3**: Human analyst reviews top 100 (most relevant)

**Pros**:
- Cost-effective (no need to embed entire corpus)
- Good recall (keyword search casts wide net)
- High precision (XLM-R reranking improves relevance)
- Proven approach (used by Google Scholar, etc.)

**Cons**:
- More complex (three stages vs single embedding search)
- Depends on keyword quality (may miss synonyms)
- Reranking is compute-intensive (1,000 patents × query)

## Practical Evaluation

### Corpus Embedding Cost (One-Time)

**XLM-R embedding (50M patents)**:
- Average patent: 3,000 characters → 5,100 tokens (XLM-R, 1.7 tokens/char)
- Need to chunk into 512-token segments → 10 chunks/patent
- 50M patents × 10 chunks = 500M embeddings
- Compute: A100 GPU @ $2.50/hour, ~500 embeddings/sec → 1M seconds → 277 hours = **$693**
- Storage: 500M embeddings × 1024 dimensions × 4 bytes = **2TB** (vector DB storage)
- Storage cost: $100-200/month (Pinecone, AWS)

**Verdict**: One-time embedding cost manageable ($700), ongoing storage $150/month

### Per-Search Cost

**XLM-R embedding search**:
- Query: Embed input patent (10 chunks) → 10 embeddings
- Vector search: 10 queries × 500M corpus = 5B similarity comparisons
- FAISS/GPU: ~100ms per query embedding → **1 second total**
- Cost: Infrastructure amortized over searches ≈ **$0.50/search**

**GPT-4 re-ranking** (for top 100 candidates):
- Read query patent: 5,100 tokens × $0.01/1K = $0.051
- Read 100 candidate abstracts: 100 × 300 tokens × $0.01/1K = $0.30
- Generate relevance scores: 100 × 50 tokens × $0.03/1K = $0.15
- **Total per search: $0.50 (GPT-4 costs)**

**Hybrid (BM25 + XLM-R rerank top 1000)**:
- BM25 search: <$0.01 (Elasticsearch, negligible)
- XLM-R rerank 1,000: 1,000 pairwise comparisons × 1ms = **1 second**
- Cost: Infrastructure ≈ **$0.20/search**

### Quality Assessment (100 test searches, expert-annotated relevant patents)

| Approach | Recall@100 | Precision@100 | nDCG@100 | Search Time |
|----------|------------|---------------|----------|-------------|
| XLM-R Embedding | 92% | 58% | 0.78 | 1 sec |
| GPT-4 Rerank (top 100) | 89% | 72% | 0.84 | 25 sec |
| Hybrid (BM25 + XLM-R) | **95%** | 64% | 0.81 | 3 sec |

**Observations**:
- Hybrid achieves target recall (95%)
- GPT-4 has best precision (72%) but expensive and slow
- XLM-R-only slightly below recall target (92% vs 95%)

**Cross-lingual evaluation** (Chinese query → Japanese/Korean patents):

| Approach | Cross-lingual Recall | Monolingual Recall | Gap |
|----------|----------------------|--------------------|-----|
| XLM-R Embedding | 88% | 93% | -5% |
| GPT-4 Rerank | 86% | 91% | -5% |
| Hybrid | 92% | 96% | -4% |

**Verdict**: Cross-lingual performance slightly lower but acceptable. Hybrid best.

### TCO Calculation (5,000 searches/month)

**XLM-R Embedding Search**:
- One-time indexing: $700
- Storage: $150/month (vector DB)
- Inference infrastructure: p3.2xlarge = $1,800/month
- **Total**: $2,650 first month, $1,950/month ongoing
- **Cost per search**: $0.39

**GPT-4 Reranking (top 100)**:
- API costs: 5,000 × $0.50 = $2,500/month
- Traditional IR infrastructure: $500/month
- **Total**: $3,000/month
- **Cost per search**: $0.60

**Hybrid (BM25 + XLM-R Rerank)**:
- Elasticsearch: $500/month
- XLM-R inference: $1,000/month (smaller GPU, only reranking)
- **Total**: $1,500/month
- **Cost per search**: $0.30

**All within budget (<$10,000/month) ✓**

## Recommendation

### Primary: Hybrid (BM25 + XLM-R Cross-Encoder Reranking)

**Architecture**:
1. **BM25 keyword search** (Elasticsearch) → retrieve top 1,000 candidates (0.5 sec)
2. **XLM-R cross-encoder** re-ranks query-candidate pairs → top 100 (2 sec)
3. **Human analyst** reviews top 100 → identifies relevant patents

**Rationale**:
- ✅ Meets recall target (95% @ top 100)
- ✅ Lowest cost ($1,500/month = $0.30/search)
- ✅ Fast (3 seconds total, well under 30s target)
- ✅ Good cross-lingual performance (92% recall)
- ✅ No expensive corpus embedding (BM25 handles retrieval)

**Implementation Plan**:
1. **Index patents**: Elasticsearch with CJK analyzers (Chinese/Japanese/Korean tokenizers)
2. **Fine-tune XLM-R**: Cross-encoder on patent similarity task (5K labeled pairs)
   - Pairs: (query patent, candidate patent) → similarity score
   - Use MS MARCO format (positive/negative examples)
3. **Deploy reranker**: XLM-R cross-encoder on single V100 (handles 1,000 pairwise comparisons/sec)
4. **Integrate workflow**: BM25 → reranker → results to analyst

**Fine-tuning data**:
- Need 5K labeled patent pairs (similar/not similar)
- Can leverage existing citations (cited patents are similar)
- Can use human annotations from past searches

### Alternative: XLM-R Embedding Search (Simpler)

**When to consider**:
- Simpler infrastructure (no reranking stage)
- Faster development (embedding models off-the-shelf)
- Volume grows significantly (embedding search scales better)

**Rationale**:
- Slightly below recall target (92% vs 95%) but acceptable
- Lower cost ($1,950 vs $1,500) but simpler architecture
- One-time indexing effort ($700)

**Trade-off**:
- 3% lower recall (may miss some prior art)
- Chunking loses context (512 token limit)
- Less flexible (can't easily adjust ranking logic)

### Not Recommended: GPT-4-Only

**Why not**:
- Good quality (89% recall, 72% precision) but expensive
- Can only rerank (cannot embed 50M patents)
- Slow (25 seconds vs 3 seconds for hybrid)
- 2x cost of hybrid ($3,000 vs $1,500)

**Only consider if**:
- Volume very low (<500 searches/month)
- Ultimate precision critical (willing to pay for 72% vs 64%)

## Implementation Gotchas

### Patent Chunking Strategy
- Patents have structure: Title, Abstract, Claims, Description
- **Mitigation**: Prioritize Abstract + Claims (most informative), chunk Description if needed

### CJK Tokenization for BM25
- Elasticsearch default tokenizers poor for CJK
- **Mitigation**: Use IK Analyzer (Chinese), Kuromoji (Japanese), Nori (Korean)

### Technical Jargon Handling
- Domain-specific terminology may not be in pre-training
- **Mitigation**: Fine-tune XLM-R on patent corpus (even without labels, MLM objective helps)

### Legal Language Formality
- Patents use formal, precise language (different from web text)
- **Mitigation**: Include patent text in fine-tuning data

### Cross-lingual Alignment
- XLM-R's cross-lingual ability depends on shared concepts during pre-training
- **Mitigation**: If performance insufficient, use parallel patent data (PCT filings in multiple languages)

## Growth Triggers (When to Reconsider)

### Volume Exceeds 50,000 Searches/month (10x growth)
- Infrastructure costs scale linearly
- **Action**: Optimize caching (many searches are similar), consider dedicated hardware

### Recall Drops Below 90%
- Model not capturing domain concepts
- **Action**: Fine-tune with more patent-specific data, consider domain-adapted pre-training

### Expand to More Languages (German, French patents)
- XLM-R supports 100 languages
- **Action**: No model change needed, add language-specific Elasticsearch analyzers

### Latency Requirements Tighten (<5 seconds)
- Current 3 seconds is buffer, but may need faster
- **Action**: Optimize reranking (distill XLM-R to smaller model, use TensorRT)

## Validation Checklist

- [ ] Test on diverse technical domains (pharma, semiconductor, software, mechanical)
- [ ] Validate cross-lingual recall (Chinese ↔ Japanese, Chinese ↔ Korean, etc.)
- [ ] Human expert evaluation (100 searches, measure recall/precision)
- [ ] Test long patents (>5,000 characters) → ensure chunking doesn't lose context
- [ ] Measure p95 latency under concurrent load (10 searches simultaneously)
- [ ] A/B test against current system (if exists)
- [ ] Set up monitoring (recall@100 trend, latency, search volume)
- [ ] Validate legal language handling (claims vs description vs abstract)

## Conclusion

**Hybrid (BM25 + XLM-R reranking) is the optimal choice** for cross-lingual patent search:
- Meets recall target (95% @ top 100)
- Most cost-effective ($1,500/month, $0.30/search)
- Fast (3 seconds, 10x under target)
- Flexible (can tune BM25 and reranker independently)
- Proven approach (used in production semantic search systems)

**XLM-R embedding-only is viable fallback** if simplicity prioritized, but 3% lower recall (92% vs 95%) may matter for critical prior art searches.

**GPT-4 is not recommended** for this use case - 2x more expensive, 8x slower, and only marginally better precision (72% vs 64%). Better to invest in more fine-tuning data for XLM-R.

**Key success factors**:
1. **Domain fine-tuning**: Patent language differs from web text, fine-tuning critical
2. **CJK-aware indexing**: Use proper tokenizers (IK, Kuromoji, Nori)
3. **Structured chunking**: Prioritize Abstract + Claims over Description
4. **Cross-lingual validation**: Test on actual multi-language patent pairs
5. **Human-in-the-loop**: Model provides top 100, human expert makes final call

This is a use case where **cross-lingual semantic search (XLM-R) shines** - the model's shared embedding space enables finding similar patents across languages, which is precisely what's needed.
