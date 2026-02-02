# S1 Rapid Discovery: Similarity Search Libraries

## Methodology

Speed-focused reconnaissance of the similarity search landscape. Target: decide on a library in 15 minutes.

## Research Approach

1. **Ecosystem scan**: Identify dominant players through GitHub stars, PyPI downloads, Stack Overflow mentions
2. **Quick categorization**: Dense vectors (FAISS, Annoy, ScaNN) vs probabilistic hashing (LSH, MinHash, SimHash)
3. **Performance indicators**: Benchmark results, scale testimonials, production usage
4. **Decision factors**: Speed, memory, accuracy trade-offs at a glance

## Libraries Surveyed

### Dense Vector Search
- **FAISS** (Meta) - GPU-accelerated, billion-scale
- **Annoy** (Spotify) - Memory-efficient, disk-backed
- **ScaNN** (Google) - Accuracy-optimized

### Probabilistic Hashing
- **datasketch** - LSH, MinHash, SimHash for set similarity

## Key Trade-offs

- **FAISS**: Maximum throughput vs setup complexity
- **Annoy**: Simplicity vs feature limitations
- **ScaNN**: Accuracy vs resource requirements
- **datasketch**: Memory efficiency vs approximate results

## Time Investment

- Library overview: ~3 min per library
- Recommendation: ~3 min
- **Total: ~15 minutes**
