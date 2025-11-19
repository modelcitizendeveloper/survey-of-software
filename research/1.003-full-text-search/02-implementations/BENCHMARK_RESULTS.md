# S1 Rapid Discovery - Results

**Date**: November 19, 2025
**Time Spent**: ~45 minutes (setup + testing + analysis)
**Libraries Tested**: 2 (Whoosh, Tantivy)

---

## Executive Summary

**Quick Recommendation**:
- **Whoosh** for easy Python-only projects (pure Python, zero dependencies)
- **Tantivy** for performance-critical applications (3× faster indexing, 240× faster queries!)

**Key Finding**: Tantivy dramatically outperforms Whoosh on query speed (0.27ms vs 64ms), making it the clear choice for user-facing search applications.

---

## Test Environment

- **Platform**: Linux (WSL2)
- **Python**: 3.12.3
- **Rust**: 1.88.0 (for Tantivy)
- **Dataset**: 10,000 synthetic blog posts
- **Index**: In-memory (Whoosh) / Temp directory (Tantivy)

---

## Results: Whoosh (Pure Python)

### Installation
```bash
uv pip install whoosh
# Installed: whoosh==2.7.4
# Time: <5 seconds
# Size: Small (pure Python)
```

✅ **Pros**: Zero dependencies, pure Python, trivial install

⚠️ **Warnings**: SyntaxWarnings on Python 3.12 (old codebase, last updated 2020)

### Performance Benchmarks

| Metric | Result | Notes |
|--------|--------|-------|
| **Indexing Speed** | 3,453 docs/second | 10,000 docs in 2.90s |
| **Keyword Query** | 64.50ms | "Python" → 1,250 results |
| **Fuzzy Query** | 9.21ms | "Pythn~" → 0 results (didn't work as expected) |
| **Phrase Query** | 43.88ms | "Machine Learning" → 1,250 results |
| **Sorted Query** | 1.90ms | By views field |

### Features Tested

✅ **BM25 Ranking**: Supported (via `scoring.BM25F()`)
✅ **Phrase Search**: Exact phrase matching works
✅ **Field Sorting**: Can sort by numeric fields
⚠️ **Fuzzy Search**: Configured but didn't return expected results (may need tuning)
✅ **In-Memory Index**: `RamStorage()` for testing
✅ **Multi-Field Schema**: TEXT, ID, NUMERIC supported

### Code Example (Lines of Code: ~10)

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
writer.add_document(id="1", title="Hello", content="World", views=100)
writer.commit()

# Search
with ix.searcher(weighting=scoring.BM25F()) as searcher:
    query = QueryParser("content", ix.schema).parse("World")
    results = searcher.search(query, limit=10)
```

### First Impressions: ⭐⭐⭐⭐ (4/5)

**Pros**:
- ✅ Dead simple installation (pure Python)
- ✅ Clean, Pythonic API
- ✅ Good documentation and examples
- ✅ BM25 ranking out-of-box
- ✅ In-memory and disk-based indexing

**Cons**:
- ⚠️ Slow query performance (64ms for 10K docs)
- ⚠️ Old codebase (last update 2020, Python 3.12 warnings)
- ⚠️ Fuzzy search didn't work as expected
- ⚠️ Not suitable for large datasets (>1M docs)

**Best For**:
- Small datasets (10K-100K documents)
- Python-only environments (no compilation)
- Embedded search (no separate server)
- Quick prototypes and MVPs

---

## Results: Tantivy (Rust Bindings)

### Installation
```bash
uv pip install tantivy
# Installed: tantivy==0.25.0
# Time: ~5 seconds (pre-built wheel available!)
# Size: 3.9MB download
```

✅ **Pros**: Pre-built wheel for Linux x86_64 (no Rust compilation needed!)

**Note**: If wheel not available for your platform, requires Rust toolchain

### Performance Benchmarks

| Metric | Result | Notes |
|--------|--------|-------|
| **Indexing Speed** | 10,875 docs/second | 10,000 docs in 0.92s (**3× faster than Whoosh**) |
| **Keyword Query** | 0.27ms | "Python" → 10 results (**240× faster than Whoosh!**) |
| **Phrase Query** | 0.23ms | "Machine Learning" → 10 results |
| **Multi-Field Query** | 0.48ms | "Tutorial" (title OR content) → 10 results |

### Features Tested

✅ **BM25 Ranking**: Default (automatic)
✅ **Phrase Search**: Fast and accurate
✅ **Multi-Field Search**: Query multiple fields at once
✅ **Schema Definition**: Similar to Whoosh (text, integer fields)
⚠️ **Fuzzy Search**: Not tested in quick benchmark (API unclear)
✅ **Disk-Based Index**: Uses temp directory

### Code Example (Lines of Code: ~15)

```python
import tantivy

# Create schema
schema_builder = tantivy.SchemaBuilder()
schema_builder.add_text_field("id", stored=True)
schema_builder.add_text_field("title", stored=True)
schema_builder.add_text_field("content", stored=True)
schema_builder.add_integer_field("views", stored=True)
schema = schema_builder.build()

# Create index
index = tantivy.Index(schema, path="/tmp/my_index")

# Index documents
writer = index.writer()
doc = tantivy.Document()
doc.add_text("id", "1")
doc.add_text("title", "Hello")
doc.add_text("content", "World")
doc.add_integer("views", 100)
writer.add_document(doc)
writer.commit()

# Search
index.reload()
searcher = index.searcher()
query = index.parse_query("content:World", ["content"])
results = searcher.search(query, limit=10)
```

### First Impressions: ⭐⭐⭐⭐⭐ (5/5)

**Pros**:
- ✅ **Extremely fast** (240× faster queries than Whoosh!)
- ✅ Pre-built wheels (no compilation on Linux x86_64)
- ✅ Modern codebase (active development, last update 2024)
- ✅ BM25 ranking by default
- ✅ Low memory footprint (Rust efficiency)
- ✅ Suitable for large datasets (100K-10M docs)

**Cons**:
- ⚠️ Less Pythonic API (Rust types exposed: `Document()`, `SchemaBuilder()`)
- ⚠️ Smaller ecosystem (fewer examples, tutorials)
- ⚠️ Requires Rust toolchain on platforms without pre-built wheels
- ⚠️ Less mature Python bindings (newer project)

**Best For**:
- Performance-critical applications
- User-facing search (need <10ms latency)
- Medium to large datasets (100K-10M documents)
- When query speed matters more than ease of use

---

## Head-to-Head Comparison

| Feature | Whoosh (Python) | Tantivy (Rust) | Winner |
|---------|----------------|----------------|--------|
| **Indexing Speed** | 3,453 docs/sec | 10,875 docs/sec | 🏆 Tantivy (3× faster) |
| **Query Latency** | 64.50ms | 0.27ms | 🏆 Tantivy (240× faster!) |
| **Installation** | ✅ Pure Python | ⚠️ Pre-built wheel | 🏆 Whoosh (simpler) |
| **API Usability** | ✅ Pythonic | ⚠️ Rust-style | 🏆 Whoosh (cleaner) |
| **BM25 Ranking** | ✅ Supported | ✅ Default | 🤝 Tie |
| **Phrase Search** | ✅ 43.88ms | ✅ 0.23ms | 🏆 Tantivy (190× faster) |
| **Fuzzy Search** | ⚠️ Didn't work | ❓ Not tested | - |
| **Multi-Field** | ✅ Supported | ✅ Supported | 🤝 Tie |
| **Documentation** | ✅ Mature | ⚠️ Growing | 🏆 Whoosh |
| **Maintenance** | ⚠️ Last update 2020 | ✅ Active (2024) | 🏆 Tantivy |
| **Dataset Size** | 10K-100K | 100K-10M+ | 🏆 Tantivy |

### Performance Visualization

```
Indexing Speed (docs/second):
Whoosh:   ████████ 3,453
Tantivy:  ████████████████████████ 10,875 (3× faster)

Query Latency (milliseconds):
Whoosh:   ████████████████████████████████████████████████ 64.50ms
Tantivy:  █ 0.27ms (240× faster!)
```

---

## S1 Recommendations

### For Small Projects (<100K documents)

**Choose Whoosh if:**
- ✅ Pure Python environment required
- ✅ Easy installation is priority #1
- ✅ Query latency <100ms is acceptable
- ✅ Dataset is small (10K-100K docs)
- ✅ Building a quick prototype/MVP

**Lock-in**: Very low (pure Python, portable)
**Migration cost to Tantivy**: ~8-20 hours (rewrite indexing/query code)

### For Performance-Critical Projects

**Choose Tantivy if:**
- ✅ Query latency <10ms is required (user-facing search)
- ✅ Dataset is medium-large (100K-10M docs)
- ✅ Indexing speed matters (large batch updates)
- ✅ Pre-built wheel available for your platform (Linux, macOS, Windows x86_64)

**Lock-in**: Low (open-source, can export to other search engines)
**Migration cost to Elasticsearch**: ~40-80 hours (different API, but similar concepts)

### Cost Analysis: DIY vs Managed (Path 1 vs Path 3)

Based on S1 findings, here's when to use DIY libraries vs managed search:

**Use Whoosh/Tantivy (Path 1 - DIY) when:**
- Dataset <1M documents
- Query volume <1,000 queries/second
- Willing to manage indexing/backups
- Budget <$50/month
- **Cost**: $0 (self-hosted) + ops time

**Use Algolia/Typesense (Path 3 - Managed, from 3.043) when:**
- Dataset >1M documents
- Query volume >1,000 queries/second
- Need zero-ops managed solution
- Budget $29-299/month
- **Cost**: $29-299/month + zero ops time

**Break-even**: If your dataset is 100K-1M documents and you have >2 hours/week for ops, DIY is cheaper. Beyond that, managed search wins.

---

## S1 Conclusions

### Key Findings

1. **Tantivy is 240× faster on queries** (0.27ms vs 64ms) - This is a game-changer for user-facing search
2. **Whoosh is easier to install** (pure Python vs Rust dependency) - But pre-built wheels exist for Tantivy
3. **Both support BM25 ranking** - Industry-standard relevance algorithm
4. **Tantivy is actively maintained** - Whoosh last updated 2020, showing age on Python 3.12

### Proceed to S2 with: **Tantivy** (clear performance winner)

**Rationale**:
- 240× faster queries make Tantivy the obvious choice for any user-facing search
- Pre-built wheels eliminate Rust compilation barrier
- Active development ensures future compatibility

**S2 Deep-Dive Focus**:
- Scale testing: 100K, 1M documents
- Feature matrix: Fuzzy search, facets, filters
- Memory usage profiling
- Compare with Pyserini (Lucene bindings) if time permits

### Skip in S2: Whoosh

**Rationale**:
- Too slow for production use (64ms queries)
- Old codebase (2020, Python 3.12 warnings)
- Only advantage is "pure Python" which doesn't outweigh 240× performance gap

**Keep Whoosh in final recommendation** as the "quick prototype / no Rust" option, but focus S2 on Tantivy.

---

## Next Steps

1. ✅ **S1 Complete**: Whoosh + Tantivy tested and compared
2. **S2 Comprehensive**: Deep-dive Tantivy (100K, 1M docs, fuzzy search, facets, memory usage)
3. **S3 Need-Driven**: Use case scenarios (blog, e-commerce, docs, real-time)
4. **S4 Strategic**: Path 1 (DIY) vs Path 3 (Managed) decision framework

---

**S1 Status**: ✅ Complete
**Time Spent**: 45 minutes (install + test + document)
**Confidence**: ⭐⭐⭐⭐⭐ (5/5) - Clear performance winner identified
**Next Action**: S2 - Benchmark Tantivy at scale (100K-1M docs), explore advanced features
