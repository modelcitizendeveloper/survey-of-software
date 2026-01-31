# Annoy (Spotify)

**GitHub:** ~14.1K stars | **Ecosystem:** C++/Python | **License:** Apache-2.0
**Latest Release:** v1.17.2 (Apr 2023)

## Positioning

Lightweight library for approximate nearest neighbors, optimized for memory efficiency and disk-backed indexes. Built at Spotify for music recommendations.

## Key Metrics

- **Memory efficiency:** mmap-based indexes shared across processes
- **Simplicity:** ~5 parameters vs FAISS's dozens
- **Build speed:** Fast index creation for <10M vectors
- **Languages:** C++ core with Python/Lua/Go/Rust bindings

## Algorithm

**Random Projection Trees:**
- Recursively splits data space using hyperplanes
- Builds a forest of binary search trees
- Combines results from multiple trees for accuracy

**Trade-off:** Simplicity and speed vs advanced optimization techniques

## Community Signals

**Stack Overflow sentiment:**
- "Annoy is the go-to for simple, fast nearest neighbor search"
- "Use Annoy if you don't need GPU and want minimal config"
- "Great for prototyping - index builds are quick, API is intuitive"

**Production usage:**
- Spotify (music recommendation, playlist generation)
- Content recommendation systems (when dataset fits in memory)
- Small-to-medium vector databases

## Benchmarks (2024)

- **ann-benchmarks:** 53 QPS at 93.5% precision (angular metric, 1M vectors)
- **Query time:** ~0.00015 seconds average
- **Memory:** 0.24 MB index for compressed datasets

## Trade-offs

**Strengths:**
- Extremely simple API (build, query, save, load)
- Fast for small-to-medium datasets (<10M vectors)
- Memory-mapped indexes enable multi-process sharing
- Minimal dependencies, easy to deploy

**Limitations:**
- No GPU support
- Single algorithm (no PQ, HNSW, etc.)
- Static indexes (rebuild required for updates)
- Less accurate than FAISS/ScaNN on high-recall tasks

## Decision Context

**Choose Annoy when:**
- Dataset <10M vectors, RAM-friendly scale
- Simplicity is priority (5-minute setup)
- Need disk-backed indexes for memory sharing
- Prototyping or MVP development

**Skip if:**
- Need >95% recall (FAISS/ScaNN are more accurate)
- Dataset >10M vectors (FAISS scales better)
- Need real-time updates (Annoy requires rebuild)
- GPU acceleration is available and desired
