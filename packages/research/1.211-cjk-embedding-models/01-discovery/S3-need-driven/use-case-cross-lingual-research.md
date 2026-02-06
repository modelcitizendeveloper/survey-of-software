# Use Case 3: Cross-Lingual Research Discovery

## Business Context

**Industry**: Academic databases, patent search, research platforms
**Application**: Query in one language, retrieve relevant documents in other languages
**Scale**: 1K-10K searches/day, 1M+ documents
**Languages**: Chinese (Simp+Trad), Japanese, Korean, English
**Quality Over Speed**: Latency < 2s acceptable, relevance critical

## Technical Requirements

- **Cross-lingual retrieval**: Primary requirement (zh→en, ja→zh, ko→en, etc.)
- **Traditional Chinese support**: Important (Taiwan academic institutions)
- **Quality**: Critical (research productivity depends on relevance)
- **Multi-field search**: Title, abstract, full text, citations

## Model Evaluation

**Winner: LaBSE**

| Model | Cross-Lingual (Tatoeba zh-en) | Trad. Chinese | Zero-Shot Transfer |
|-------|------------------------------|---------------|-------------------|
| LaBSE | **95.2** | Good | Excellent |
| multilingual-e5-base | 89.3 | Fair | Very Good |
| M3E-base | N/A (no multilingual) | Fair | N/A |

**Rationale**: LaBSE purpose-built for translation-pair retrieval. 6-point advantage on cross-lingual benchmarks justifies choice despite being older (2020) model.

## Deployment Architecture

```
[Search Query (any language)] → [LaBSE Embeddings]
                                        ↓
                            [Qdrant Vector DB]
                            - 1M research papers
                            - 768-dim embeddings
                            - Metadata: language, year, citations
                                        ↓
                            [Top-50 Results]
                                        ↓
                            [Re-ranking: Cross-Encoder]
                            (cross-encoder/mmarco-mMiniLMv2-L12-H384-v1)
                                        ↓
                            [Top-10 Results + Translations]
```

## TCO Analysis (5K Searches/Day, 1M Documents)

**Embedding Service** (Self-hosted):
- CPU-based (no GPU needed for research use case - not latency-critical)
- 2x c6i.4xlarge (16 vCPU, 32GB RAM) = $0.68/hour × 2 × 720h = **$979/month**

**Vector Database** (Qdrant Cloud):
- 1M vectors × 768-dim = ~3GB = 1 cluster = **$95/month**

**Document Re-embedding** (quarterly updates):
- 1M docs × 4 times/year = 4M embeddings/year
- Cost: negligible (batch processing overnight)

**Total**: **$1,074/month** ($0.007 per search)

**Value Proposition**: Researchers find 20-30% more relevant papers (cross-lingual discovery). Difficult to quantify ROI but high qualitative value.

## Implementation

**Phase 1** (2 weeks): Deploy LaBSE, embed 100K sample papers, prototype search
**Phase 2** (4 weeks): Embed full 1M corpus, set up Qdrant cluster, deploy to production
**Phase 3** (ongoing): Fine-tune on user click data, add cross-encoder re-ranking

## Recommendation

**Model**: LaBSE (cross-lingual specialist)
**Alternative**: multilingual-e5-large (if budget allows, newer model)
**TCO**: $1,074/month
**Key Benefit**: Best-in-class cross-lingual retrieval (6 pts better than alternatives)
