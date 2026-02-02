# FAISS (Meta)

**GitHub:** ~38.9K stars | **Ecosystem:** C++/Python | **License:** MIT
**Latest Release:** v1.13.2 (Dec 2025)

## Positioning

Meta's production-grade library for billion-scale dense vector similarity search. Industry standard for large-scale retrieval systems (RAG, recommendation engines, search).

## Key Metrics

- **Scale:** Proven at 1.5 trillion 144-dim vectors (Meta internal systems)
- **Performance:** 8.5x faster than previous state-of-the-art on billion-scale datasets
- **GPU support:** CUDA acceleration for throughput-critical applications
- **Languages:** C++ core with Python/Julia bindings

## Algorithms Included

- **IVF (Inverted File Index)** - Partitioning-based search
- **PQ (Product Quantization)** - Memory compression
- **HNSW** - Graph-based approximate search
- **Flat/Exact** - Brute-force baseline
- **Hybrid combinations** - IVF+PQ, IVF+HNSW for scale/accuracy trade-offs

## Community Signals

**Stack Overflow sentiment:**
- "FAISS is the gold standard for production vector search"
- "Use FAISS for RAG systems - handles millions of embeddings easily"
- "GPU support makes FAISS 100x faster on large datasets"

**Production usage:**
- Meta (1.5T vectors, recommendation/search systems)
- Widely adopted for LLM retrieval-augmented generation (RAG)
- Vector database backends (Milvus, Weaviate use FAISS)

## Benchmarks (2025)

- **ann-benchmarks:** Top performer for recall@10 on high-dimensional data
- **Queries/sec:** ~10K QPS at 95% recall (GPU, 1M vectors, 768-dim)
- **Memory:** PQ compression achieves 32x reduction vs raw vectors

## Trade-offs

**Strengths:**
- Production-proven at extreme scale (1B+ vectors)
- GPU acceleration for maximum throughput
- Comprehensive algorithm suite (exact, approximate, compressed)
- Active development by Meta AI Research

**Limitations:**
- Steep learning curve (many index types, parameter tuning required)
- GPU memory constraints for ultra-high-dimensional data
- Build time can be hours for billion-scale indexes

## Decision Context

**Choose FAISS when:**
- Processing >1M vectors or need GPU acceleration
- Building RAG systems, recommendation engines, semantic search
- Need production-grade reliability and scale

**Skip if:**
- Dataset <10K vectors (simpler tools suffice)
- No time for parameter tuning (Annoy is simpler)
- Need real-time index updates (FAISS optimizes for batch builds)
