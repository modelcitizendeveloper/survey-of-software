# Library Embeddings CLI

Discover Python library relationships through word embeddings. Find similar libraries, perform vector arithmetic analogies, and explore ecosystem clusters.

## Installation

```bash
pip install library-embeddings
```

## Quick Start

```bash
# Find libraries similar to pandas
lib-emb similar pandas

# What's the async version of Flask?
lib-emb analogy flask asyncio --sub threading
# → fastapi (0.987)

# Show ML ecosystem cluster
lib-emb cluster torch

# Search for libraries
lib-emb search "data"

# Get model info
lib-emb info
```

## Commands

### `similar` - Find Similar Libraries

Find libraries that are functionally related based on co-occurrence patterns.

```bash
lib-emb similar pandas --top 10
```

**Output:**
```
                  Libraries Similar to pandas
┌────────┬─────────────────┬────────────┬─────────────────────┐
│ Rank   │ Library         │ Similarity │ Bar                 │
├────────┼─────────────────┼────────────┼─────────────────────┤
│ 1.     │ scipy           │ 0.996      │ ███████████████████ │
│ 2.     │ networkx        │ 0.996      │ ███████████████████ │
│ 3.     │ matplotlib      │ 0.995      │ ███████████████████ │
└────────┴─────────────────┴────────────┴─────────────────────┘
```

### `analogy` - Library Vector Arithmetic

Perform vector arithmetic to discover library relationships:

```bash
lib-emb analogy flask asyncio --sub threading
```

This finds: "What library is to async what Flask is to threading?"

**More examples:**
```bash
# GPU version of NumPy?
lib-emb analogy numpy --add gpu --sub cpu

# Modern alternative to requests?
lib-emb analogy requests --add async

# What goes with pandas for data science?
lib-emb analogy pandas sklearn --top 5
```

**Output:**
```
    Library Analogy: flask + asyncio - threading
┌────────┬───────────────────┬────────────┐
│ Rank   │ Result            │ Similarity │
├────────┼───────────────────┼────────────┤
│ 1.     │ pydantic          │ 0.990      │
│ 2.     │ prometheus_client │ 0.988      │
│ 3.     │ fastapi           │ 0.987      │
└────────┴───────────────────┴────────────┘

✓ Best match: pydantic (similarity: 0.990)
```

### `cluster` - Ecosystem Analysis

Show what libraries typically cluster together:

```bash
lib-emb cluster torch --top 15
```

**Output:**
```
╔══════════════════════════════════════════════════════════════╗
║ torch Ecosystem Cluster                                      ║
║                                                              ║
║ Cluster size: 15 libraries                                   ║
║ Avg similarity: 0.997                                        ║
╚══════════════════════════════════════════════════════════════╝

  Library                 Similarity
 ────────────────────────────────────
  transformers            0.997
  datasets                0.997
  onnxruntime             0.997
  sentence_transformers   0.997
  fastapi                 0.997
  ...
```

### `search` - Fuzzy Search

Find libraries by name substring:

```bash
lib-emb search "data"
```

**Output:**
```
           Search Results for 'data'
┌─────────────────┬─────────┐
│ Library         │ Match   │
├─────────────────┼─────────┤
│ datasets        │ Contains│
│ dataclasses     │ Contains│
└─────────────────┴─────────┘
```

### `info` - Model Information

Show embeddings model metadata:

```bash
lib-emb info
```

### `explain` - Detailed Library Info

Get detailed explanation for a specific library:

```bash
lib-emb explain pandas
```

## Use Cases

### 1. Library Discovery

**Problem:** "I know what I need functionally, but not what it's called."

**Solution:** Use analogies to discover:

```bash
# Async version of Flask?
lib-emb analogy flask asyncio --sub threading
→ fastapi

# GPU version of NumPy?
lib-emb analogy numpy cupy --sub cpu
→ cupy (if in vocabulary)

# What's like pandas but for large datasets?
lib-emb similar pandas --top 20 | grep -i "dask\|vaex\|polars"
```

### 2. Ecosystem Exploration

**Problem:** "I'm adopting PyTorch. What else do ML teams typically use?"

**Solution:** Explore clusters:

```bash
lib-emb cluster torch --top 20
```

Shows: transformers, datasets, onnxruntime, sentence-transformers, etc.

### 3. Competitive Advantage

**Problem:** "Everyone uses the same popular libraries. How do I find alternatives?"

**Strategy:** Look for high similarity but low mainstream adoption:

```bash
# Find pandas alternatives
lib-emb similar pandas --top 50
# Review results: polars, vaex, dask (alternatives, not complements)
```

### 4. Tech Stack Validation

**Problem:** "Do these libraries work well together?"

**Solution:** Check if they cluster:

```bash
# Check if fastapi + celery + boto3 are commonly paired
lib-emb cluster fastapi --top 20
# If celery and boto3 appear → validated pairing
```

## How It Works

**Training data:**
- 432 Python libraries extracted from [Survey of Software](https://research.modelcitizendeveloper.com)
- Co-occurrence patterns from expert-curated research topics
- Word2Vec embeddings (100 dimensions)

**What similarity means:**
- High similarity = libraries often discussed together
- Reflects **functional co-use**, not technical dependencies
- Complements (not replaces) dependency graphs

**Validation:**
- Pearson correlation with Libraries.io: r=0.060
- Low correlation is good → captures different dimension
- Embeddings: "used together", Dependencies: "needs to work"

## Vocabulary

Currently covers **97 Python libraries** including:

- **ML/AI:** torch, transformers, datasets, onnxruntime, sentence-transformers
- **Data Science:** pandas, scipy, networkx, matplotlib, plotly
- **Web:** flask, fastapi, django, pydantic, celery
- **Infrastructure:** boto3, redis, prometheus_client, airflow
- **NLP:** jieba, pkuseg, ltp, cjklib

See full list: `lib-emb info`

## Limitations

- **Python-only:** Currently trained on Python libraries
- **Vocabulary:** 97 libraries (subset of 432 extracted)
- **Temporal:** Embeddings reflect 2023-2025 usage patterns
- **Coverage:** Best for popular libraries, gaps in niche domains

## Roadmap

- [ ] Expand vocabulary to 500+ libraries
- [ ] Add npm/Cargo ecosystem support
- [ ] Temporal embeddings (track evolution over time)
- [ ] Domain-specific models (ML, web, data science)
- [ ] Web interface for exploration

## Development

```bash
# Clone repository
git clone https://github.com/modelcitizendeveloper/survey-of-software
cd survey-of-software/library-embeddings/cli

# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/
ruff check src/
```

## Citation

If you use this in research:

```bibtex
@software{library_embeddings_2026,
  title = {Library Embeddings: Discovering Python Library Relationships},
  author = {Survey of Software},
  year = {2026},
  url = {https://research.modelcitizendeveloper.com},
  note = {PyPI: library-embeddings}
}
```

## License

MIT License - see LICENSE file for details.

## Learn More

- **Website:** https://research.modelcitizendeveloper.com
- **Research:** [Library Embeddings Methodology](https://research.modelcitizendeveloper.com/library-embeddings)
- **Repository:** https://github.com/modelcitizendeveloper/survey-of-software

---

**Built with:** Word2Vec, Gensim, Click, Rich

**Maintained by:** [Survey of Software](https://research.modelcitizendeveloper.com)
