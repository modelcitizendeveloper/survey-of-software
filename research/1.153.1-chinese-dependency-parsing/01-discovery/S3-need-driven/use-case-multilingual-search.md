# Use Case: Multilingual Search Engines and Information Retrieval

## Who Needs This

**User Persona**: Search engineers and ML engineers at companies building cross-lingual search, document retrieval, or question-answering systems that include Chinese content.

**Organization Context**:
- Search engine companies (Bing, DuckDuckGo, etc.)
- Enterprise search platforms (Elasticsearch, Algolia)
- Knowledge management systems (corporate intranets)
- Academic/legal research databases

**Technical Background**:
- Software engineers (search indexing, query processing)
- ML engineers (ranking models, semantic search)
- Information retrieval experience (BM25, vector search, reranking)

**Scale**: Indexing millions of documents across 10-50 languages including Chinese

## Why They Need Dependency Parsing

### Primary Goals

**Query Understanding**:
- Parse user queries to understand intent
- Example: "谁发明了电脑" (Who invented the computer) → extract subject-verb-object structure
- Rewrite queries for better matching ("谁" → person entity, "发明" → invented relationship)

**Document Structure Analysis**:
- Index documents at syntactic level (not just bag-of-words)
- Identify key phrases and their grammatical roles
- Weight terms by syntactic importance (subjects/verbs > adjectives/adverbs)

**Cross-Lingual Matching**:
- Align queries and documents across languages using dependency structure
- Example: English query "computer inventor" → Chinese "电脑 的 发明者" (same syntactic pattern)
- Improve translation-based search (syntactic features help MT)

**Question Answering**:
- Extract answers from Chinese documents
- Map question structure to document structures
- Example: "什么时候" (when) questions → extract temporal expressions via dependency relations

### Success Criteria

- **Relevance**: Improved search quality (MRR, NDCG metrics)
- **Multilingual**: Consistent experience across Chinese, English, Japanese, etc.
- **Scalability**: Index millions of documents in reasonable time
- **Latency**: Query-time parsing <50ms (for real-time search)
- **Maintainability**: Single codebase for all languages (not language-specific hacks)

## Requirements and Constraints

### Technical Requirements

**Must-have**:
- Multilingual support (Chinese + English + others)
- Consistent output format (same dependency schema across languages)
- Fast inference (query-time parsing must not slow search)
- Batch processing (index millions of documents offline)

**Nice-to-have**:
- Semantic relations (for knowledge graph construction)
- Custom model training (domain-specific search, e.g., legal)
- Integration with search engines (Elasticsearch, Solr plugins)

### Resource Constraints

**Compute**:
- Offline indexing: GPU clusters available (batch processing)
- Online query: CPU-only (latency-critical, cost-sensitive)
- Cloud infrastructure (AWS, GCP)

**Budget**:
- Open-source required (per-API costs prohibitive at scale)
- Infrastructure budget available (can run GPU for indexing)

**Skills**:
- Search engineering (not NLP experts)
- Need simple APIs (integrate with existing search stack)
- Prefer standard formats (easy to index in Elasticsearch)

## Library Recommendation

### Primary Choice: **Stanza**

**Why Stanza**:

1. **Multilingual consistency**: 80+ languages with same API
   - Chinese, English, Japanese, Korean, etc. (all major search languages)
   - UD output format (identical schema across languages)
   - Simplifies cross-lingual search (same features for all languages)

2. **UD-native**: Standard output for IR systems
   - CoNLL-U format (easy to parse and index)
   - 17 universal POS tags (consistent across languages)
   - 48 universal dependencies (cross-lingual alignment)

3. **Two-phase processing fits IR workflows**:
   - **Offline indexing**: Use GPU, batch process all documents
     - Extract dependency features (subjects, objects, modifiers)
     - Index syntactic structures in Elasticsearch
   - **Online query**: Use CPU, parse queries in real-time
     - Fast transition-based parsing (<50ms per query)
     - Extract query intent (entity types, relation types)

4. **Clean API**: Easy integration with search pipelines
   - Python (dominant in ML/search engineering)
   - JSON output (standard for Elasticsearch)
   - Batch processing support (index thousands of docs/minute)

**Implementation Pattern**:

```
Offline Indexing (GPU cluster):
Documents → Stanza (batch parsing) → Extract features:
  - Subject-verb-object triples
  - Named entities with roles (nsubj, obj)
  - Key phrases (compound nouns, verb phrases)
→ Index in Elasticsearch with syntactic metadata

Online Query Processing (CPU servers):
User Query → Stanza (single query parsing) → Extract query structure:
  - Entity types (person, location, organization)
  - Relation types (invention, location, temporal)
  - Query rewriting (expand with synonyms based on POS)
→ Enhanced query → Elasticsearch → Rerank with syntactic features
```

**Elasticsearch Integration**:
- Custom ingest pipeline (call Stanza during indexing)
- Store dependency features in document metadata
- Use syntactic features in ranking (BM25F with field boosts)
- Query rewriting based on POS/dependency patterns

### Alternative: **HanLP (for semantic search with Chinese focus)**

**When to choose HanLP instead**:

**Semantic search priority**:
- Building knowledge graphs from Chinese documents
- Semantic similarity matching (not just keyword matching)
- Semantic dependency parsing (DAG) for complex relations

**Chinese language emphasis**:
- 70%+ of content is Chinese (vs multilingual mix)
- Chinese-specific features critical (measure words, aspectual markers)
- Can deploy separate parsers per language (not unified)

**Advanced NLP pipeline**:
- Need sentiment, NER, classification (beyond just parsing)
- MTL efficiency (multiple tasks in one pass)

**Trade-offs**:
- Heavier models (500MB-2GB vs Stanza 300MB)
- Less consistent across languages (Chinese-optimized, others less so)
- More complex API (more options, steeper learning curve)

### Why Not LTP

**Reasons to avoid**:

1. **Chinese-only**: Cannot handle multilingual search
   - Need separate tools for English, Japanese, etc.
   - Inconsistent output formats (LTP for Chinese, X for English)
   - More code complexity (language-specific routing)

2. **MTL constraint**: Indexing doesn't need all six tasks
   - Only need parsing, not segmentation/POS/NER/SRL/SDP
   - Paying compute cost for unused tasks
   - Single-task parser (Stanza) more efficient for IR

**Exception**: If search is Chinese-only (rare for modern systems).

### Why Not CoreNLP

**Reasons to avoid**:
- Pre-neural (lower accuracy hurts relevance)
- Slow (cubic time graph-based parsing slows indexing)
- Java (Python dominates search ML pipelines)
- Only 8 languages (insufficient for global search)

## Risk Factors and Mitigations

### Risk: Query-Time Latency

**Problem**: Parsing adds 20-50ms to query latency, slowing search.
- User-perceivable delay (aim for <100ms total)
- Competitive disadvantage vs non-parsed search

**Mitigation**:
- Cache parsed queries (frequent queries → precomputed structures)
- Async parsing (parse in background, use bag-of-words initially, rerank with syntax later)
- Feature flags (only parse for complex queries, skip simple keywords)
- Model optimization (distillation, quantization for faster CPU inference)

### Risk: Index Bloat

**Problem**: Storing dependency features increases index size.
- Each document has POS tags, dependency arcs, syntactic metadata
- 2-5x index size increase (storage costs, slower retrieval)

**Mitigation**:
- Selective indexing (only index key syntactic features, not full parse trees)
- Compression (delta encoding for frequent POS patterns)
- Tiered storage (full parse in cold storage, summary in hot index)
- ROI analysis (measure relevance gain vs storage cost)

### Risk: Domain Mismatch

**Problem**: Stanza trained on news/Wikipedia, but indexing legal/medical/patent documents.
- Lower parsing accuracy → worse relevance
- Domain-specific terminology mishandled

**Mitigation**:
- Fine-tune Stanza on domain corpus (1K-10K annotated documents)
- Terminology injection (add domain lexicons to POS tagger)
- Hybrid approach (syntax + BM25, syntax weight lower on domain mismatch)
- A/B test (measure relevance gain per domain)

### Risk: Multilingual Quality Variance

**Problem**: Stanza accuracy varies across languages.
- High accuracy on English, Chinese, Spanish (high-resource)
- Lower accuracy on low-resource languages (Amharic, etc.)
- Inconsistent search quality across languages

**Mitigation**:
- Language-specific thresholds (use syntax only for high-confidence parses)
- Fallback to bag-of-words (if parsing quality low, ignore syntactic features)
- Cross-lingual transfer (train on high-resource, apply to low-resource)
- Monitor per-language relevance (identify underperforming languages)

## Expected Outcomes

**Timeline**: 4-8 months for production deployment
- Month 1-2: Prototype (Stanza + Elasticsearch on sample corpus, measure relevance)
- Month 3-4: Offline indexing (GPU cluster, batch process full corpus)
- Month 5-6: Online query (integrate Stanza into query pipeline, measure latency)
- Month 7-8: Optimization (caching, model distillation, A/B testing)

**Deliverables**:
- Syntactic indexing pipeline (Stanza + Elasticsearch integration)
- Query understanding (entity/relation extraction from queries)
- Relevance metrics (MRR, NDCG improvement vs baseline)
- Latency dashboard (query parsing time, total query time)

**Business Impact**:
- Improved relevance (5-15% MRR/NDCG gain typical for syntactic features)
- Better cross-lingual search (consistent features across languages)
- Smarter query understanding (handle complex natural language queries)

**Cost Estimate**:
- Development: 2-3 engineers × 4-8 months
- Indexing infrastructure: $2K-10K/month (GPU cluster for offline)
- Query infrastructure: $500-2K/month (CPU servers, low latency)
- Ongoing: 1 engineer (monitoring, fine-tuning)

## Summary

**For multilingual search engines, Stanza is the clear choice** due to 80+ language support, UD consistency, and efficient two-phase processing (GPU indexing, CPU queries). HanLP is an alternative for Chinese-focused semantic search. LTP and CoreNLP don't fit multilingual IR requirements.

**Key success factors**:
- Two-phase design (offline GPU indexing, online CPU queries)
- Cache parsed queries (reduce latency for frequent searches)
- A/B test (measure relevance gain vs baseline)
- Monitor per-language quality (ensure consistent experience)
- Domain adaptation (fine-tune on search corpus if needed)
