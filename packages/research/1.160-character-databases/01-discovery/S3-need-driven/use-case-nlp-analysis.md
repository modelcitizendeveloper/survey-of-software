# Use Case: CJK Text Analysis & NLP

## Context

**Application:** Sentiment analysis, entity extraction, semantic search for Chinese text

**User scenario:**
- Analyze 10M Chinese social media posts
- Extract: sentiment, entities (people, places), topics
- Requires: word segmentation, semantic understanding, cross-variant handling

**NLP requirements:**
- Character properties (pronunciation for phonetic models)
- Semantic relationships (disambiguate polysemous characters)
- Structural analysis (compound character understanding)
- Cross-variant normalization (treat 学 ≈ 學 as same)

## Requirements

### Must-Have (P0)

- **[P0-1] Character properties:** Pronunciation, radical, stroke count
- **[P0-2] Variant normalization:** Unified representation (学 → 學)
- **[P0-3] Fast batch processing:** >10K chars/sec

### Nice-to-Have (P1)

- **[P1-1] Semantic features:** Embeddings based on character structure + meaning
- **[P1-2] Component analysis:** Semantic radical extraction (氵 in 江 = water)

### Constraints

- **Throughput:** 10M posts/day = 200M characters/day
- **Latency:** Batch processing OK (not real-time)
- **Accuracy:** Preprocessing quality critical for downstream models

## Database Fit Analysis

| Database | P0-1 (Properties) | P0-2 (Variants) | P0-3 (Speed) | P1-1 (Semantics) | Fit Score |
|----------|------------------|----------------|-------------|-----------------|-----------|
| **Unihan** | ✅ | ✅ (Basic) | ✅ (11K/sec) | ❌ | 75% |
| **CHISE** | ✅ | ✅ | ❌ (122/sec) | ✅ | 60% |
| **IDS** | ⚠️ | ❌ | ✅ (Fast) | ⚠️ | 50% |
| **CJKVI** | ❌ | ✅ | ✅ | ❌ | 60% |

## Recommended Stack

**Optimal:** Unihan + CJKVI (preprocessing) + CHISE (offline enrichment)

**Rationale:**
- Unihan + CJKVI for fast preprocessing (<1ms/char)
- CHISE for semantic feature extraction (offline, one-time)
- Pattern: Fast path (99% of chars) + slow path (1% rare semantic lookups)

**Architecture:**
1. **Preprocessing layer:** Unihan + CJKVI (normalize variants, extract properties)
   - Throughput: 11K chars/sec (meets 10M posts/day requirement)
2. **Feature enrichment:** CHISE-derived semantic embeddings (offline, pre-computed)
   - Build once, use in all downstream models

**Real-World:** Baidu NLP, Tencent AI
- Baidu: Unihan + custom word embeddings (character structure features)
- Tencent: Variant normalization (CJKVI-like) + semantic models
- Performance: >100K chars/sec (optimized, cached)

**Must include:** Unihan + CJKVI (preprocessing)
**Optional:** CHISE (offline semantic enrichment, not runtime)

## Confidence: 80%** - Two-tier approach (fast preprocessing + offline enrichment) balances performance vs richness
