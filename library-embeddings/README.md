# Library Embeddings: Python Library Vector Space

**Beyond the Saul Steinberg view:** Mapping the library landscape without popularity bias.

## Project Overview

Word2Vec-style embeddings for Python libraries, capturing functional relationships and ecosystem clusters. Enables library analogies (`flask - threading + asyncio = fastapi`), similarity search, and alternative discovery.

**Status:** Proof-of-concept complete, validated, ready for production enhancement or publication.

---

## Quick Start

### Extract Library Metadata
```bash
cd scripts
uv run python extract_libraries_strict.py
```

### Train Embeddings
```bash
uv run python train_embeddings.py
```

### Explore Results
```bash
uv run python explore_embeddings.py
```

---

## Project Structure

```
library-embeddings/
├── scripts/           # Data extraction & training pipeline
│   ├── extract_libraries_strict.py     # Parse research + markdown
│   ├── build_similarity_matrix.py      # Co-occurrence matrices
│   ├── train_embeddings.py             # Word2Vec training
│   ├── explore_embeddings.py           # Analogies & clusters
│   └── validate_against_librariesio.py # External validation
├── data/              # Extracted library metadata
│   └── library-metadata-clean.json     # 432 libraries, 92 topics
├── validation/        # Validation results & models
│   ├── embeddings/                     # Trained models (50d/100d/300d)
│   ├── similarity_matrices/            # Co-occurrence data
│   └── librariesio_validation_results.json
├── docs/              # Research documentation
│   ├── library-embeddings-codebase-sampling.md
│   └── library-embeddings-prior-art.md
└── README.md          # This file
```

---

## Current State

### What We Have

**Data:**
- 432 Python libraries extracted from Survey of Software
- 92 research topics as training "sentences"
- 4,705 library co-occurrence pairs

**Models:**
- 97 libraries learned (min_count=2 filter)
- 50d, 100d, 300d embeddings trained
- Gensim Word2Vec format + NumPy arrays

**Validation:**
- Libraries.io dependency overlap: r=0.060 (complementary, not redundant)
- Embeddings capture functional similarity, not implementation dependencies

**Clusters Discovered:**
- ML: torch, transformers, datasets, onnxruntime
- Data Science: pandas, scipy, matplotlib, networkx
- Web: fastapi, pydantic, celery, boto3

**Working Analogies:**
- `flask - threading + asyncio → fastapi` (0.987)
- `requests - threading + asyncio → fastapi, pydantic` (0.99)

---

## Three Paths Forward

See detailed documentation:
1. [**Research Path**](RESEARCH.md) - Strengthen embeddings, compare to baselines, publish
2. [**Publication Path**](PUBLICATION.md) - MSR/ICSE paper, 6 weeks to submission
3. [**Practice Path**](PRACTICE.md) - Ship tools for library discovery, competitive advantage

---

## Key Findings

### 1. Embeddings Complement Dependency Graphs

**Dependency graphs answer:** "What does this library need to work?"
- numpy: 0 dependencies (foundational)
- transformers: 350 dependencies (complex)

**Our embeddings answer:** "What is this library used with?"
- numpy: Everywhere (consumed, not consuming)
- transformers: Clusters with torch, datasets

**Validation:** Pearson r=0.060 - proves we capture different dimension.

### 2. Prior Art Gap

**Existing work:**
- Code embeddings (code2vec, CodeBERT) - token/AST level
- API embeddings (API2Vec) - method level
- Dependency analysis (Libraries.io) - network graphs
- Library recommendations (LibRec 2016) - collaborative filtering

**Our contribution:**
- Library-level granularity (between code and networks)
- Dual signal (research curation + usage data)
- Exploratory (not prescriptive)
- Methodologically transparent

### 3. Practical Applications

**For developers:**
- Find async alternatives (sync → async library transitions)
- Discover ecosystem clusters (what works together)
- Identify competitive combinations (uncommon but valid pairings)

**For researchers:**
- Novel approach to software ecosystem analysis
- Reproducible methodology (4PS + sampling documented)
- Extensible to other ecosystems (npm, Cargo, Maven)

---

## Dependencies

```bash
uv pip install gensim numpy pyyaml requests
```

## License

Part of [Survey of Software](https://research.modelcitizendeveloper.com) - methodology published under CC BY-SA 4.0, code under MIT.

---

## Citation

If you use this work:

```
Library Embeddings: Mapping Python Library Relationships
Survey of Software, 2026
https://research.modelcitizendeveloper.com
```

Academic paper in preparation (see PUBLICATION.md).
