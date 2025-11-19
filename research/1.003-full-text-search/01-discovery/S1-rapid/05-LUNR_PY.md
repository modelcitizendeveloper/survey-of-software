# lunr.py - Lightweight Python Search

**Type**: Pure Python search library (port of Lunr.js)
**GitHub**: https://github.com/yeraydiazdiaz/lunr.py
**License**: MIT
**Origin**: Python port of Lunr.js (JavaScript library)
**Maintenance**: Active (last update 2023)

---

## Overview

Lunr.py is a **simple full-text search solution** for situations where deploying a full-scale solution like Elasticsearch isn't possible, viable, or you're simply prototyping.

**Key Philosophy**: Lightweight, in-memory search for prototypes and small datasets.

**Trade-off**: Lunr keeps the inverted index in **memory** and requires you to recreate or read the index at the start of your application.

---

## Architecture

```
Python Application
    ↓
lunr.py (Pure Python)
    ↓
In-Memory Index
```

**Dependency**: Zero - Pure Python

---

## Key Features

### Core Search
- **TF-IDF ranking** (classic information retrieval)
- **Boolean queries** (AND, OR, NOT)
- **Field boosting** (weight title higher than body)
- **Stemming** (English by default)
- **Multi-field search**

### Language Support
- **English** (built-in)
- **16+ languages** via optional NLTK integration
  - Install with: `pip install lunr[languages]`
  - Includes: French, German, Spanish, Italian, Portuguese, Russian, Arabic, Chinese, Japanese, etc.

### Interoperability
- **Compatible with Lunr.js indexes** (can share indexes between Python and JavaScript)
- Useful for static site generators (build index in Python, search in browser JavaScript)

---

## Strengths

### 1. Pure Python (Zero Dependencies)
- No C/C++/Rust/Java required
- Works anywhere Python runs
- Easy deployment (pip install lunr)

### 2. Lightweight and Simple
- ~1000 lines of Python code
- Easy to understand and customize
- Minimal memory footprint (for small indexes)

### 3. Interoperability with Lunr.js
- Build index in Python, use in JavaScript
- Great for static site generators (MkDocs, Pelican, etc.)
- Share indexes across languages

### 4. Good for Prototyping
- Quick to set up
- No external services
- Iterate fast

### 5. MIT License
- Commercial-friendly
- No GPL restrictions

---

## Weaknesses

### 1. In-Memory Indexes Only
- Must load entire index into RAM at startup
- Not suitable for large datasets (>100K documents)
- No disk-based persistence (must rebuild or deserialize)

### 2. Slower Than Compiled Alternatives
- Pure Python performance
- Likely similar speed to Whoosh (both pure Python)
- Much slower than Tantivy, Xapian, Pyserini

### 3. Limited Scalability
- Designed for small datasets (1K-10K documents)
- Memory grows linearly with dataset size
- No incremental updates (rebuild full index)

### 4. Basic Features Only
- No faceted search
- No spelling correction
- No advanced ranking (just TF-IDF, not BM25)
- No geospatial search

### 5. Smaller Ecosystem
- Fewer tutorials than Whoosh
- Less battle-tested
- Smaller community

---

## Use Cases

### ✅ Good Fit

**1. Static Site Search**
- MkDocs documentation
- Jekyll/Hugo blogs
- Pelican static sites
- **Use case**: Build index at compile time, search in browser

**2. Quick Prototypes**
- MVP search functionality
- Demo applications
- Internal tools

**3. Small Datasets (1K-10K documents)**
- Blog search (hundreds of posts)
- Small product catalogs
- Internal documentation

**4. Embedded Applications**
- Desktop apps with search
- Command-line tools
- Scripts with search capabilities

**5. Cross-Platform Compatibility**
- When JavaScript interop is needed
- Share indexes between Python backend and JS frontend

### ❌ Not a Good Fit

**1. Large Datasets (>10K documents)**
- Memory constraints
- Slow indexing
- Better alternatives exist

**2. Production High-Traffic Search**
- Not optimized for speed
- Tantivy/Xapian better choices

**3. Feature-Rich Requirements**
- No facets, spelling correction, advanced features
- Use Xapian or managed services instead

**4. Real-Time Updates**
- Must rebuild entire index
- No incremental updates

---

## Performance Expectations

Expected (not benchmarked, based on pure Python):

| Metric | Expected Performance |
|--------|---------------------|
| **Indexing** | 1,000-5,000 docs/sec (similar to Whoosh) |
| **Query latency** | 50-200ms (depends on index size in memory) |
| **Memory** | 10-100MB for 10K documents (entire index in RAM) |
| **Scale** | 1K-10K documents (max ~50K before memory issues) |

**Note**: Being pure Python, performance likely similar to Whoosh but possibly slower due to simpler implementation.

---

## Installation Complexity

```bash
# Basic installation
pip install lunr

# With multi-language support (requires NLTK)
pip install lunr[languages]
```

**Complexity**: Very easy (pure Python pip install)
**First-time setup**: <1 minute

---

## Code Example (~10 lines)

```python
from lunr import lunr

# Documents
documents = [
    {
        'id': '1',
        'title': 'Python Tutorial',
        'body': 'Learn Python programming fundamentals'
    },
    {
        'id': '2',
        'title': 'JavaScript Guide',
        'body': 'Master JavaScript for web development'
    }
]

# Build index (specify which fields to index and search)
idx = lunr(
    ref='id',
    fields=('title', 'body'),
    documents=documents
)

# Search
results = idx.search('Python')

for result in results:
    print(f"{result['ref']}: {result['score']}")
```

**API Complexity**: Low (very Pythonic, simple)

---

## Comparison to Other Libraries

| Feature | lunr.py | Whoosh | Tantivy | Xapian |
|---------|---------|--------|---------|--------|
| **Dependencies** | Zero | Zero | Rust | C++ |
| **Installation** | pip | pip | pip | apt |
| **Speed** | Slow | Slow | Very fast | Fast |
| **Scale** | 1K-10K | 10K-1M | 1M-10M | 10M-100M |
| **Ranking** | TF-IDF | BM25 | BM25 | Probabilistic |
| **Index Storage** | RAM only | RAM or disk | Disk | Disk |
| **Interop** | ✅ Lunr.js | ❌ | ❌ | ❌ |
| **Multi-language** | ✅ 16+ | ✅ | ⚠️ | ✅ 30+ |
| **License** | MIT | BSD | MIT | GPL |

---

## Decision Framework

**Choose lunr.py if:**
- ✅ Dataset <10K documents
- ✅ Quick prototype or MVP
- ✅ Pure Python required (no dependencies)
- ✅ Static site search (interop with Lunr.js)
- ✅ Simplicity more important than performance
- ✅ MIT license desired

**Choose Whoosh instead if:**
- ❌ Need disk-based indexes (not just in-memory)
- ❌ Want BM25 ranking (not TF-IDF)
- ❌ Dataset 10K-1M documents
- ❌ Need more features (fuzzy search, sorting by fields)

**Choose Tantivy instead if:**
- ❌ Performance is critical
- ❌ Dataset >10K documents
- ❌ User-facing search (<10ms latency required)

**Choose Xapian instead if:**
- ❌ Dataset >100K documents
- ❌ Need facets, spelling correction
- ❌ GPL license acceptable

---

## Lock-in Assessment

**Lock-in Score**: 15/100 (Very Low)

**Why very low lock-in?**
- Simple API (easy to rewrite)
- Standard IR concepts (TF-IDF)
- Pure Python (no binary dependencies)
- MIT license (fork/modify if needed)

**Migration paths:**
- To Whoosh: Similar API, ~4-8 hours rewrite
- To Tantivy: Different API, ~8-16 hours
- To Elasticsearch: API rewrite, ~20-40 hours

**Minimal switching cost** due to simplicity.

---

## lunr.py vs Whoosh: Direct Comparison

Both are **pure Python** search libraries. Key differences:

| Aspect | lunr.py | Whoosh |
|--------|---------|--------|
| **Philosophy** | Minimalist, prototyping | Full-featured |
| **Ranking** | TF-IDF | BM25 |
| **Index Storage** | RAM only | RAM or disk |
| **Scale** | 1K-10K docs | 10K-1M docs |
| **Features** | Basic | Rich (fuzzy, sorting, etc.) |
| **Maintenance** | Active (2023) | Older (2020) |
| **Interop** | ✅ Lunr.js | ❌ None |
| **Lines of Code** | ~1,000 | ~10,000 |

**Recommendation**:
- Use **lunr.py** for static sites, prototypes, <10K docs, need Lunr.js interop
- Use **Whoosh** for more features, disk indexes, 10K-1M docs

---

## Related Research

**Tier 1 (Libraries)**:
- **1.002**: Fuzzy Search - lunr.py does not have fuzzy search, would need RapidFuzz
- **1.033**: NLP Libraries - Could use spaCy for tokenization before lunr.py indexing

**Tier 3 (Managed Services)**:
- **3.043**: Search Services - Algolia/Typesense for when lunr.py can't scale

---

## References

- **GitHub**: https://github.com/yeraydiazdiaz/lunr.py
- **Docs**: https://lunr.readthedocs.io/
- **PyPI**: https://pypi.org/project/lunr/
- **Lunr.js** (original): https://lunrjs.com/

---

## S1 Assessment

**Rating**: ⭐⭐⭐ (3/5)

**Pros**:
- ✅ Pure Python, zero dependencies
- ✅ Very simple API
- ✅ Interop with Lunr.js (static sites)
- ✅ MIT license
- ✅ Quick to prototype

**Cons**:
- ⚠️ In-memory only (RAM constraint)
- ⚠️ Limited scale (<10K docs)
- ⚠️ Basic features (no facets, spelling)
- ⚠️ TF-IDF (not BM25)
- ⚠️ Likely slow (pure Python)

**Best For**:
- Static site search (MkDocs, blogs)
- Quick prototypes and MVPs
- Small datasets (1K-10K documents)
- When JavaScript interop needed

**Worth Testing?**: ⚠️ Maybe - if static site use case or need to compare pure Python options (lunr.py vs Whoosh). Otherwise, skip in favor of Whoosh/Tantivy.
