# ScaNN (Google)

**GitHub:** Part of google-research (~37.1K stars repo-wide) | **Ecosystem:** C++/Python | **License:** Apache-2.0
**Latest Major Update:** SOAR algorithm (Dec 2025)

## Positioning

Google's state-of-the-art library for maximum-accuracy similarity search. Optimized for inner-product metrics and research-grade precision.

## Key Metrics

- **Performance:** 2x QPS of competitors at equivalent accuracy (2025 benchmarks)
- **Accuracy focus:** Best-in-class for high-recall scenarios (>98% recall)
- **Integration:** Available in Vertex AI Vector Search, AlloyDB
- **Languages:** C++ core with Python/TensorFlow APIs

## Key Innovation

**Anisotropic Vector Quantization:**
- Directional quantization aligned with data distribution
- Trades off low-similarity accuracy for high-similarity precision
- Superior to isotropic approaches (PQ) for top-K retrieval

**SOAR (2025):** Redundancy-based efficiency improvements

## Community Signals

**Research citations:**
- "ScaNN achieves SOTA on ann-benchmarks for inner-product search"
- "Use ScaNN when accuracy is non-negotiable (e.g., medical retrieval)"

**Production usage:**
- Google Cloud (Vertex AI Vector Search)
- AlloyDB (ScaNN indexes for PostgreSQL)
- Research labs prioritizing accuracy over simplicity

## Benchmarks (2025)

- **Gene embedding study:** 1.83s query latency, FAISS slightly faster but ScaNN more accurate
- **ann-benchmarks:** Top accuracy scores for inner-product metrics
- **Accuracy:** 98%+ recall achievable with tuned parameters

## Trade-offs

**Strengths:**
- Best accuracy for inner-product similarity
- Advanced quantization techniques
- Backed by Google Research (cutting-edge algorithms)
- Cloud integration (Vertex AI, AlloyDB)

**Limitations:**
- Part of monorepo (not standalone package, harder to install)
- Steeper learning curve than Annoy
- Less documentation than FAISS
- GPU support not as mature as FAISS

## Decision Context

**Choose ScaNN when:**
- Accuracy is critical (medical, legal, high-stakes retrieval)
- Inner-product metric is primary use case
- Using Google Cloud (native Vertex AI integration)
- Research/experimentation with SOTA algorithms

**Skip if:**
- Need simplicity (Annoy) or GPU speed (FAISS)
- Deployment complexity is a concern (monorepo setup)
- Dataset <1M vectors (overhead not justified)
- Euclidean distance preferred (FAISS optimizes for this better)
