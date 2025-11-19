# Xapian - C++ Search Engine with Python Bindings

**Type**: C++ search engine library with Python bindings
**Website**: https://xapian.org/
**License**: GPL v2+ (may be issue for commercial/proprietary software)
**Origin**: 1999 (25+ years, very mature)
**Maintenance**: Active (2024)

---

## Overview

Xapian is an **open-source search engine library** written in C++ with bindings for many languages including Python. It's been battle-tested for over 25 years and proven to scale to **hundreds of millions of documents**.

**Key Philosophy**: Mature, proven, scalable search for serious applications.

---

## Architecture

```
Python Application
    ↓
Python Bindings (xapian-bindings)
    ↓
Xapian Core (C++)
    ↓
Disk/Memory
```

**Dependency**: Requires C++ library (system package)

---

## Key Features

### Core Search
- **Probabilistic ranking** (similar to BM25)
- **Boolean queries** (AND, OR, NOT, phrase)
- **Wildcards** and prefix search
- **Stemming** (30+ languages)
- **Spelling correction** built-in

### Advanced Features
- **Faceted search** (category counts, filters)
- **Geospatial search** (lat/lon queries)
- **Synonyms** (built-in synonym support)
- **Range queries** (dates, numbers)
- **Replication** (master-slave for scaling)

### Scalability
- **Proven to 100M+ documents**
- Incremental updates (add/delete without full reindex)
- Multi-database queries (federated search)

---

## Strengths

### 1. Battle-Tested Maturity (25 Years)
- Used in production by major sites
- Debian package search (millions of packages)
- Many large-scale deployments

### 2. Proven Scalability
- **Hundreds of millions of documents** in production
- Efficient incremental updates
- Replication support for high-availability

### 3. Feature-Rich Out-of-Box
- Spelling correction
- Faceted search
- Synonyms
- Stemming for 30+ languages

### 4. Low Memory Footprint
- C++ efficiency
- Disk-based indexes (don't need full index in RAM)
- Can handle large indexes on modest hardware

### 5. Active Community
- 25+ years of development
- Well-documented
- Production-proven

---

## Weaknesses

### 1. GPL License (May Be Problematic)
- GPL v2+ requires derivative works to be GPL
- If embedding Xapian in proprietary software, may need commercial license
- Check with legal if using commercially

### 2. C++ Dependency
- Requires system packages (not just `pip install`)
- May need to compile on some platforms
- More complex deployment than pure Python

### 3. Less Modern API
- Older API design (C++ style exposed)
- Not as "Pythonic" as Whoosh
- Steeper learning curve

### 4. Less Popular in Python Ecosystem
- Fewer Python tutorials/examples
- Smaller Python community
- Most documentation is C++ focused

---

## Use Cases

### ✅ Good Fit

**1. Large-Scale Applications (10M-100M+ documents)**
- Proven at this scale in production
- Efficient disk-based indexes
- Replication for HA

**2. Feature-Rich Search Requirements**
- Need spelling correction out-of-box
- Faceted search (e-commerce, archives)
- Synonym support
- Multi-language stemming

**3. Long-Term Production Use**
- 25 years of stability
- Active maintenance
- Won't disappear tomorrow

**4. Resource-Constrained Environments**
- Low memory footprint
- Efficient C++ implementation
- Disk-based (don't need index in RAM)

**5. Open-Source Projects**
- GPL license is fine for OSS
- No licensing concerns

### ❌ Not a Good Fit

**1. Proprietary/Commercial Software**
- GPL license may require commercial license
- Legal complexity

**2. Quick Prototypes**
- Steeper learning curve
- More complex installation
- Whoosh/Tantivy faster to start

**3. Pure Python Environments**
- Requires C++ library
- System dependencies
- Not portable via pip alone

**4. Small Datasets (<100K documents)**
- Feature overkill
- Simpler solutions (Whoosh) sufficient

---

## Performance Expectations

Based on Xapian benchmarks and production deployments:

| Metric | Expected Performance |
|--------|---------------------|
| **Indexing** | 5,000-20,000 docs/sec (depends on document size) |
| **Query latency** | 10-100ms (depends on index size, complexity) |
| **Memory** | 50-500MB (index mostly on disk) |
| **Scale** | Proven to 100M+ documents |

**Note**: Performance comparable to Lucene, but with lower memory requirements due to disk-based indexes.

---

## Installation Complexity

```bash
# Linux (Debian/Ubuntu)
sudo apt-get install python3-xapian

# macOS (via Homebrew)
brew install xapian
brew install xapian-bindings --with-python

# Then use in Python (already installed, no pip needed)
import xapian
```

**Complexity**: Medium (system packages, not pip)
**First-time setup**: 5-15 minutes (depends on platform)

**Note**: Not available via `pip install xapian` - requires system packages.

---

## Code Example (Estimated ~15 lines)

```python
import xapian

# Create database
db = xapian.WritableDatabase('index_path', xapian.DB_CREATE_OR_OPEN)

# Index document
doc = xapian.Document()
doc.set_data('Sample document text')
doc.add_term('sample')
doc.add_term('document')
db.add_document(doc)

# Commit
db.commit()

# Search
db = xapian.Database('index_path')
enquire = xapian.Enquire(db)
query = xapian.Query('sample')
enquire.set_query(query)
matches = enquire.get_mset(0, 10)

for match in matches:
    print(f'{match.docid}: {match.percent}%')
```

**API Complexity**: Medium (C++ style, not very Pythonic)

---

## Comparison to Other Libraries

| Feature | Xapian | Tantivy | Whoosh | Pyserini |
|---------|--------|---------|--------|----------|
| **Backend** | C++ | Rust | Python | Java |
| **Speed** | Fast | Very fast | Slower | Fast |
| **Installation** | Medium (apt) | Easy (pip) | Easy (pip) | Medium (JVM) |
| **Scale** | 100M+ | 10M | 1M | Billions |
| **Maturity** | 25 years | 5 years | 10 years | 5 years |
| **License** | GPL v2+ | MIT | BSD | Apache 2.0 |
| **Memory** | Low | Low | Medium | High |
| **Facets** | ✅ Built-in | ❌ | ❌ | ✅ |
| **Spelling** | ✅ Built-in | ❌ | ⚠️ Basic | ✅ |

---

## Decision Framework

**Choose Xapian if:**
- ✅ Large-scale deployment (10M-100M+ documents)
- ✅ Need faceted search, spelling correction out-of-box
- ✅ GPL license is acceptable (open-source project)
- ✅ Want 25 years of proven stability
- ✅ Low memory footprint required
- ✅ Multi-language stemming needed (30+ languages)

**Choose Tantivy instead if:**
- ❌ Want easier installation (pip vs apt)
- ❌ Need MIT license (not GPL)
- ❌ Want more modern API
- ❌ Dataset <10M documents

**Choose Whoosh instead if:**
- ❌ Pure Python required
- ❌ Quick prototype
- ❌ Dataset <1M documents

**Choose Pyserini instead if:**
- ❌ Academic research focus
- ❌ Need hybrid search (keyword + neural)
- ❌ Want migration path to Elasticsearch

---

## Lock-in Assessment

**Lock-in Score**: 40/100 (Low-Medium)

**Why moderate lock-in?**
- Xapian-specific API (not standard like Lucene)
- Custom index format (not portable to other engines)
- Would need rewrite to migrate

**But mitigated by:**
- Standard IR concepts (BM25, inverted index)
- Open-source (can always export data)
- Active project (won't be abandoned)

**Migration paths:**
- To Elasticsearch/Tantivy: Rewrite indexing/search code, export/reimport data
- To managed services: Similar effort
- **Effort**: 40-80 hours for medium-sized application

---

## Notable Deployments

**Known users of Xapian**:
- Debian package search (millions of packages)
- Many university library systems
- Archive.org search (historical)
- Various government document archives

**Proven at scale** in production for decades.

---

## Related Research

**Tier 1 (Libraries)**:
- **1.002**: Fuzzy Search - Xapian has built-in fuzzy matching
- **1.033**: NLP Libraries - Can use spaCy for entity extraction + Xapian for search

**Tier 3 (Managed Services)**:
- **3.043**: Search Services - If GPL license is an issue, managed services are alternative

---

## References

- **Website**: https://xapian.org/
- **Docs**: https://getting-started-with-xapian.readthedocs.io/
- **GitHub Mirror**: https://github.com/xapian/xapian

---

## S1 Assessment

**Rating**: ⭐⭐⭐⭐ (4/5)

**Pros**:
- ✅ 25 years of proven stability
- ✅ Scales to 100M+ documents
- ✅ Feature-rich (facets, spelling, synonyms)
- ✅ Low memory footprint
- ✅ Active development

**Cons**:
- ⚠️ GPL license (may block commercial use)
- ⚠️ System package installation (not pip)
- ⚠️ Less Pythonic API
- ⚠️ Smaller Python community

**Best For**:
- Large-scale open-source projects
- Long-term production deployments
- Feature-rich search (facets, spelling, multi-language)
- Resource-constrained environments (low memory)
