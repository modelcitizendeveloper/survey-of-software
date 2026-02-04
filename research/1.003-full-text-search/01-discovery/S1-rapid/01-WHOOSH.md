# Whoosh - Pure Python Search Library

**Type**: Pure Python full-text search library
**GitHub**: https://github.com/mchaput/whoosh
**License**: BSD
**Origin**: Created by Matt Chaput (2007)
**Maintenance**: Last updated 2020 (community fork: whoosh-community for revival)

---

## Overview

Whoosh is a **fast, featureful full-text indexing and searching library** implemented in pure Python. It's designed to be easy to install and use without any compilation dependencies.

**Key Philosophy**: Pure Python portability and simplicity over maximum performance.

---

## Architecture

```
Python Application
    ↓
Whoosh (Pure Python)
    ↓
RAM Storage or Disk Storage
```

**Dependency**: Zero - Pure Python

---

## Key Features

### Core Search
- **BM25F ranking** (industry-standard algorithm)
- **Boolean queries** (AND, OR, NOT)
- **Phrase search** (exact matching)
- **Fuzzy search** (typo tolerance with ~ operator)
- **Wildcard queries** (prefix, suffix patterns)
- **Field boosting** (weight fields differently)

### Index Options
- **In-memory indexes** (RamStorage for testing/prototyping)
- **Disk-based indexes** (persistent storage)
- **Incremental updates** (add/delete documents without full reindex)

### Advanced Features
- **Field sorting** (sort results by custom fields)
- **Numeric/date ranges** (filter by ranges)
- **Highlighting** (show matching snippets)
- **Query parsing** (convert user queries to search queries)
- **Spelling suggestions** (did-you-mean functionality)

---

## Strengths

### 1. Pure Python (Zero Dependencies)
- No C/C++/Rust/Java compilation
- Works anywhere Python runs
- Easy deployment (pip install)
- No platform-specific binaries

### 2. Good Developer Experience
- Clean, Pythonic API
- Well-documented (extensive tutorials)
- Easy to understand and customize
- Good examples and community resources

### 3. Flexible Storage
- In-memory for testing (RamStorage)
- Disk-based for production
- Custom storage backends possible

### 4. Feature-Complete for Basic Search
- BM25F ranking (same as Elasticsearch)
- All standard query types
- Sorting, filtering, highlighting
- Suitable for 10K-1M documents

### 5. BSD License
- Commercial-friendly
- Permissive open-source

---

## Weaknesses

### 1. Aging Codebase
- Last updated 2020 (5 years old)
- Shows Python 3.12 deprecation warnings
- Community fork exists but uncertain future
- May have compatibility issues with future Python versions

### 2. Performance Limitations
- Pure Python is inherently slower than compiled languages
- Query latency: 20-100ms (depends on dataset size)
- Indexing: 3,000-10,000 docs/sec
- Not suitable for <10ms latency requirements

### 3. Single-Process Only
- No built-in distributed search
- Can't scale horizontally
- Single-threaded indexing

### 4. Limited Scale
- Suitable for 10K-1M documents
- Beyond 1M docs, performance degrades
- Better alternatives exist for large datasets

---

## Use Cases

### ✅ Good Fit

**1. Small to Medium Datasets (10K-1M documents)**
- Blog search (thousands of posts)
- Product catalogs (tens of thousands of items)
- Internal documentation
- Archive search

**2. Python-Only Environments**
- When avoiding compilation dependencies
- Shared hosting without custom binaries
- Pure Python deployment pipelines

**3. Embedded Search**
- Desktop applications
- Command-line tools
- Scripts with search capabilities
- No separate search server needed

**4. Prototypes and MVPs**
- Quick proof-of-concepts
- Iterate fast without infrastructure
- Easy to set up and tear down

**5. Educational Use**
- Learning search engine concepts
- Pure Python makes internals accessible
- Good for understanding IR fundamentals

### ❌ Not a Good Fit

**1. High-Performance Requirements**
- User-facing search needing <10ms latency
- High query volume (>1000 QPS)
- Real-time search applications

**2. Large Datasets (>1M documents)**
- Performance degrades significantly
- Better alternatives: Xapian, Elasticsearch, managed services

**3. Distributed Search**
- No built-in clustering
- Can't scale horizontally
- Need Elasticsearch/OpenSearch for distribution

**4. Long-Term Production (Uncertainty)**
- Aging codebase (2020)
- Uncertain maintenance future
- May need migration later

---

## Performance Expectations

Based on benchmarks with 10,000 documents:

| Metric | Performance |
|--------|-------------|
| **Indexing** | 3,453 docs/sec |
| **Keyword Query** | 64.50ms |
| **Phrase Query** | 43.88ms |
| **Fuzzy Query** | 9.21ms |
| **Sorted Query** | 1.90ms |
| **Memory** | ~50-100MB for 10K docs (in-memory) |

**Scale**: Suitable for 10K-1M documents. Beyond 1M, consider alternatives.

---

## Installation Complexity

```bash
# Simple installation
pip install whoosh

# Or with uv
uv pip install whoosh
```

**Complexity**: Very easy (pure Python)
**First-time setup**: <1 minute
**Binary dependencies**: None

---

## Code Example (~10 lines)

```python
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, NUMERIC
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.filedb.filestore import RamStorage

# Create schema
schema = Schema(
    id=ID(stored=True),
    title=TEXT(stored=True),
    content=TEXT(stored=True),
    views=NUMERIC(stored=True, sortable=True)
)

# Create in-memory index
storage = RamStorage()
ix = storage.create_index(schema)

# Index documents
writer = ix.writer()
writer.add_document(
    id="1",
    title="Sample Title",
    content="Sample content text",
    views=100
)
writer.commit()

# Search with BM25F ranking
with ix.searcher(weighting=scoring.BM25F()) as searcher:
    query = QueryParser("content", ix.schema).parse("sample")
    results = searcher.search(query, limit=10)

    for hit in results:
        print(f"{hit['title']}: {hit.score}")
```

**API Complexity**: Low (very Pythonic)

---

## Comparison to Other Libraries

| Feature | Whoosh | Tantivy | lunr.py | Xapian |
|---------|--------|---------|---------|--------|
| **Dependencies** | Zero | Rust | Zero | C++ |
| **Installation** | pip | pip (wheel) | pip | apt |
| **Speed (10K docs)** | 64ms | 0.27ms | ~50ms | ~10ms |
| **Ranking** | BM25F | BM25 | TF-IDF | Probabilistic |
| **Index Storage** | RAM or disk | Disk | RAM only | Disk |
| **Scale** | 10K-1M | 1M-10M | 1K-10K | 10M-100M |
| **Maintenance** | 2020 | Active | 2023 | Active |
| **License** | BSD | MIT | MIT | GPL |

---

## Decision Framework

**Choose Whoosh if:**
- ✅ Pure Python environment required (no compilation)
- ✅ Dataset 10K-1M documents
- ✅ Query latency <100ms is acceptable
- ✅ Easy deployment/portability is priority
- ✅ Quick prototype or embedded search
- ✅ Educational use (learning search concepts)

**Choose Tantivy instead if:**
- ❌ Performance critical (<10ms latency needed)
- ❌ Dataset >1M documents
- ❌ High query volume (>1000 QPS)
- ❌ Production use with long-term support concerns

**Choose lunr.py instead if:**
- ❌ Dataset <10K documents
- ❌ In-memory only is fine
- ❌ Need JavaScript interop (Lunr.js compatibility)

**Choose Xapian instead if:**
- ❌ Dataset >1M documents
- ❌ Need facets, spelling correction built-in
- ❌ GPL license acceptable

---

## Lock-in Assessment

**Lock-in Score**: 10/100 (Very Low)

**Why very low lock-in?**
- Standard BM25F algorithm (portable concept)
- Pure Python (easy to read and rewrite)
- Simple API (straightforward migration)
- BSD license (can fork if needed)

**Migration paths:**
- To Tantivy: Similar API, ~8-16 hours rewrite
- To lunr.py: Very similar, ~4-8 hours
- To Elasticsearch: API rewrite, ~20-40 hours
- To managed services: Similar effort

**Minimal risk** due to simplicity and standard algorithms.

---

## Related Research

**Tier 1 (Libraries)**:
- **1.002**: Fuzzy Search - Whoosh has built-in fuzzy search with ~ operator
- **1.033**: NLP Libraries - Can use spaCy for advanced tokenization before Whoosh indexing

**Tier 3 (Managed Services)**:
- **3.043**: Search Services - When Whoosh can't scale, migrate to Algolia/Typesense

---

## References

- **GitHub**: https://github.com/mchaput/whoosh
- **Docs**: https://whoosh.readthedocs.io/
- **PyPI**: https://pypi.org/project/Whoosh/
- **Community fork**: https://github.com/Sygil-Dev/whoosh-reloaded (revival effort)

---

## S1 Assessment

**Rating**: ⭐⭐⭐⭐ (4/5)

**Pros**:
- ✅ Pure Python (zero dependencies)
- ✅ Easy installation and use
- ✅ BM25F ranking (industry standard)
- ✅ Feature-complete for basic search
- ✅ Good documentation

**Cons**:
- ⚠️ Aging codebase (2020, Python 3.12 warnings)
- ⚠️ Slower performance (64ms queries vs <1ms alternatives)
- ⚠️ Limited scale (1M document ceiling)
- ⚠️ Uncertain maintenance future

**Best For**:
- Python-only environments
- Prototypes and MVPs
- Small to medium datasets (10K-1M docs)
- Embedded search (no separate server)
- Educational use

**Trade-off**: Simplicity and portability vs performance. Choose Whoosh when pure Python deployment is more valuable than query speed.
