# datasketch (LSH, MinHash, SimHash)

**GitHub:** ~2.9K stars | **Ecosystem:** Python | **License:** MIT
**Latest Release:** v1.9.0 (Jan 2026)

## Positioning

Python library for probabilistic similarity search using hashing algorithms. Optimal for set similarity, document deduplication, and memory-constrained environments.

## Key Metrics

- **Memory efficiency:** Orders of magnitude smaller than dense vectors
- **Speed:** Sub-linear search via LSH (Locality-Sensitive Hashing)
- **Algorithms:** MinHash, SimHash, LSH, LSH Forest, HyperLogLog, HNSW
- **Recent addition:** Optional CuPy GPU backend for MinHash (v1.8+)

## Algorithms Included

### MinHash
- **Use case:** Jaccard similarity for sets (document similarity, deduplication)
- **Precision:** Probabilistic estimate with tunable accuracy
- **Memory:** Fixed-size signature regardless of set size

### SimHash
- **Use case:** Near-duplicate detection (text, documents)
- **Method:** Locality-sensitive hash where similar docs produce similar hashes
- **Application:** Google-style web page deduplication

### LSH (Locality-Sensitive Hashing)
- **Use case:** Sub-linear similarity search in high-dimensional spaces
- **Trade-off:** Approximate results for massive speed gains

## Community Signals

**Stack Overflow sentiment:**
- "datasketch is the standard Python library for MinHash/LSH"
- "Use MinHash for document deduplication - handles millions of docs"
- "SimHash is perfect for near-duplicate detection at scale"

**Use cases:**
- Web crawling (duplicate detection)
- Recommendation systems (collaborative filtering)
- Data deduplication (ETL pipelines)
- Text clustering (news articles, social media)

## Trade-offs

**Strengths:**
- Probabilistic algorithms handle billion-scale datasets
- Constant-size signatures (memory efficiency)
- Pure Python (easy to install, no C++ dependencies)
- Cassandra backend support for distributed LSH

**Limitations:**
- Approximate results (not exact search)
- Only for set/text similarity (not general dense vectors)
- Less accurate than FAISS for high-recall dense vector search
- CPU-only by default (GPU support limited to MinHash batch updates)

## When to Use vs Dense Vector Libraries

**datasketch (LSH/MinHash/SimHash):**
- Set similarity (documents, user behavior)
- Text deduplication
- Memory-constrained environments
- Billion-scale approximate search

**FAISS/Annoy/ScaNN (Dense vectors):**
- Embedding similarity (LLMs, image features)
- High-dimensional continuous vectors
- When accuracy >95% is required

## Decision Context

**Choose datasketch when:**
- Comparing sets or documents (Jaccard similarity)
- Need memory efficiency at billion-scale
- Deduplication is the primary task
- Can tolerate approximate results (90-95% accuracy)

**Skip if:**
- Working with dense embeddings (use FAISS instead)
- Need exact nearest neighbors (LSH is approximate)
- GPU acceleration is critical (limited GPU support)
- Real-time updates required (LSH rebuild can be costly)
