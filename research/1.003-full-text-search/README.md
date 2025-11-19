# 1.003: Full-text Search Libraries Discovery

**Research Code**: 1.003
**Title**: Full-text Search Libraries
**Category**: Sorting & Searching Algorithms (Tier 1)
**Status**: In Progress
**Started**: 2025-11-19

## Research Question

**"What is the optimal self-hosted full-text search library for Python applications, and when should you use a DIY approach vs managed search services?"**

## Scope

Evaluate **Python full-text search libraries** (Tier 1 - self-operated) as the DIY baseline for managed search services (3.043 already complete):

### In Scope
- **Pure Python libraries**: Whoosh (pure Python, no dependencies)
- **Rust bindings**: Tantivy-py (high performance, Rust backend)
- **Client libraries**: MeiliSearch Python client, Elasticsearch Python client
- **Use cases**: Small to medium datasets (<10M documents), self-hosted search
- **Performance**: Indexing speed, query latency, memory usage
- **Features**: Ranking algorithms, filters, facets, fuzzy search

### Out of Scope
- Managed search services (covered in 3.043 Search Services - Algolia, Typesense, Meilisearch Cloud)
- Elasticsearch/OpenSearch deployment (covered in 3.043, focus on Python client here)
- Database full-text search (PostgreSQL FTS, SQLite FTS5 - different category)
- Vector search / semantic search (separate experiment)

## Strategic Context: Path 1 vs Path 3

This research provides the **Path 1 (Self-Operated)** baseline for the search capability decision:

**Path 1 (DIY - This Experiment)**:
- Whoosh, Tantivy-py libraries in your Python app
- Cost: $0 (runs in-process or self-hosted)
- Control: Full control, customize ranking
- Ops: You manage indexing, scaling, backups

**Path 3 (Managed - 3.043 Complete)**:
- Algolia, Typesense, Meilisearch Cloud
- Cost: $29-299/month
- Control: Limited customization
- Ops: Vendor manages everything

**Decision Point**: When is Path 1 sufficient vs when do you need Path 3?

## Candidate Libraries

### Primary Candidates (Python-focused)

**1. Whoosh** (Pure Python)
- **GitHub**: https://github.com/mchaput/whoosh
- **License**: BSD
- **Approach**: Pure Python, no dependencies, embeddable
- **Strengths**: Easy integration, no C dependencies, portable
- **Weaknesses**: Slower than Rust/C++ options

**2. Tantivy-py** (Rust Bindings)
- **GitHub**: https://github.com/quickwit-oss/tantivy-py
- **License**: MIT
- **Approach**: Python bindings to Tantivy (Rust search engine)
- **Strengths**: Very fast (Rust performance), modern ranking
- **Weaknesses**: Rust dependency, less Python-native

**3. Pyserini** (Lucene/Anserini Bindings)
- **GitHub**: https://github.com/castorini/pyserini
- **License**: Apache 2.0
- **Approach**: Python bindings to Anserini (Java/Lucene)
- **Strengths**: Academic research quality, BM25, neural ranking
- **Weaknesses**: JVM dependency, heavier

### Client Libraries (For Self-Hosted Servers)

**4. MeiliSearch Python Client**
- **Approach**: HTTP client to MeiliSearch server (self-hosted)
- **GitHub**: https://github.com/meilisearch/meilisearch-python
- **Note**: Self-hosted MeiliSearch (Rust binary) + Python client

**5. Elasticsearch Python Client**
- **Approach**: HTTP client to Elasticsearch server (self-hosted)
- **GitHub**: https://github.com/elastic/elasticsearch-py
- **Note**: Self-hosted Elasticsearch (Java) + Python client

## Use Case: DIY Search for Python Applications

**Context**: Building a Python web application (Django/FastAPI) that needs full-text search

**Requirements**:
- Index 10K-1M documents (blog posts, products, documentation)
- Query latency <100ms (interactive search)
- Fuzzy search, filters, facets (price ranges, categories)
- Easy integration into Python codebase
- Self-hosted (no managed service costs)
- Minimal ops burden (no dedicated search cluster)

**Success Criteria**:
- Index 100K documents in <10 minutes
- Query 100K documents in <50ms (p95)
- <500MB RAM for 100K documents
- <10 lines of Python code to integrate
- Portable (works on Linux, macOS, Windows)

## Discovery Methodology

Following MPSE Tier 1 framework:

### S1: Rapid Discovery (Target: 1.5-2 hours)
**Focus**: Quick install, basic benchmarks, ease of use
- Install Whoosh, Tantivy-py, Pyserini
- Index 10K sample documents (benchmark)
- Run basic queries (keyword, fuzzy, filters)
- Measure: indexing time, query latency, memory usage
- Document first impressions (API usability)

### S2: Comprehensive Discovery (Target: 2-3 hours)
**Focus**: Deep feature comparison, performance at scale
- **Feature matrix**: BM25 ranking, facets, filters, fuzzy search, phrase search
- **Performance benchmarks**: 100K documents, 1M documents
- **Scaling**: Single-threaded vs multi-threaded indexing
- **Memory**: RAM usage at 10K, 100K, 1M documents
- **Query types**: Keyword, prefix, wildcard, fuzzy, phrase, Boolean

### S3: Need-Driven Discovery (Target: 1.5-2 hours)
**Focus**: Use case scenarios matching Path 1 vs Path 3 decision
- **Scenario 1**: Blog search (10K posts, low traffic) - Whoosh sufficient?
- **Scenario 2**: E-commerce search (100K products, facets) - Tantivy-py needed?
- **Scenario 3**: Documentation search (1M pages) - Self-hosted Meilisearch better?
- **Scenario 4**: Real-time indexing (user-generated content) - Performance critical?

### S4: Strategic Discovery (Target: 1-1.5 hours)
**Focus**: Path 1 vs Path 3 decision framework
- **When to use Path 1 (DIY)**: Dataset size, query volume, budget thresholds
- **When to use Path 3 (Managed)**: Scale, ops burden, time-to-market
- **Migration path**: Start DIY, move to managed (export/import data)
- **Long-term costs**: Self-hosting ops vs managed service fees

**Total estimated time**: 6-8 hours (reduced from 7-9 due to 3.043 context)

## Deliverables

1. **S1-S4 Discovery Documents**: Library comparison and benchmarks
2. **Performance Benchmarks**: Indexing speed, query latency, memory usage
3. **Feature Matrix**: BM25, facets, filters, fuzzy search comparison
4. **Path 1 vs Path 3 Decision Framework**: When to DIY vs when to buy
5. **Code Examples**: Integration patterns for Django/FastAPI
6. **Recommendation**: Primary library choice with rationale

## Related Research

**Tier 1 (Libraries)**:
- **1.002**: Fuzzy Search (RapidFuzz, FuzzyWuzzy) - Complements full-text search
- **1.003**: Full-text Search (this experiment) ← YOU ARE HERE
- **1.033**: NLP Libraries (spaCy, Transformers) - Advanced text processing

**Tier 3 (Managed Services)**:
- **3.043**: Search Services (Algolia, Typesense, Meilisearch) ← ALREADY COMPLETE
  - This experiment provides Path 1 (DIY) baseline for 3.043's Path 3 (managed) analysis

**Strategic Integration**:
- 1.003 findings inform "when to self-host vs when to use 3.043 managed services"
- Cost/performance trade-off: DIY ($0 + ops time) vs Managed ($29-299/mo + zero ops)

## Success Metrics

### Performance Targets
- **Indexing**: >10K docs/minute (Whoosh), >50K docs/minute (Tantivy-py)
- **Query latency**: <50ms p95 for 100K documents
- **Memory**: <500MB for 100K documents
- **Relevance**: BM25 ranking (industry standard)

### Developer Experience
- **Installation**: <5 minutes (pip install)
- **Integration**: <10 lines of code to add search
- **Documentation**: Sufficient examples, API reference

### Path 1 Viability
- Can handle 10K-1M documents (beyond = managed service)
- Query volume <1000 QPS (beyond = dedicated cluster)
- Ops burden <2 hours/week (maintenance, backups)

## Next Steps

1. **S1 Rapid Discovery** (TODAY):
   - Install Whoosh, Tantivy-py
   - Benchmark indexing 10K documents
   - Basic query tests (keyword, fuzzy)
   - Document in `01-discovery/S1-rapid/`

2. **S2 Comprehensive** (Tomorrow):
   - Feature matrix (BM25, facets, filters)
   - Performance at 100K, 1M documents
   - Memory profiling

3. **S3-S4** (Day 3-4):
   - Use case scenarios
   - Path 1 vs Path 3 decision framework
   - Final synthesis and recommendation

## Research Log

- **2025-11-19**: Project initialized, directory structure created
- Next: S1 Rapid Discovery - Install and benchmark Whoosh, Tantivy-py

---

**Status**: ⬜ S1 Pending | ⬜ S2 Pending | ⬜ S3 Pending | ⬜ S4 Pending
**Next Action**: S1 - Install libraries, run benchmarks, test integration
