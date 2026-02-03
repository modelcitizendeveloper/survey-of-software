# S1: Rapid Discovery Approach

## Methodology

**Philosophy:** "Popular libraries exist for a reason"

**Time Budget:** 10 minutes

## Discovery Process

### 1. Initial Landscape Scan
- Searched GitHub for "vector database" + "RAG" + "embeddings"
- Checked PyPI download stats for embedding/vector libraries
- Reviewed HackerNews and Reddit r/MachineLearning discussions (2024-2025)
- Scanned awesome-lists: awesome-vector-search, awesome-production-ml

### 2. Selection Criteria
- **Popularity**: GitHub stars + package downloads
- **Recent activity**: Commits in last 6 months
- **Active maintenance**: Issue resolution speed, release frequency
- **Clear documentation**: Quickstart availability, examples

### 3. Libraries Identified

From initial scan, four libraries emerged as dominant in the RAG/LLM application space:

1. **ChromaDB** (~23k stars, Python/JS) - Most discussed for prototyping
2. **Pinecone** (Managed service) - Most mentioned in production contexts
3. **Qdrant** (~22k stars, Rust) - Rising fast in performance discussions
4. **Weaviate** (~12k stars, Go) - Strong in hybrid search use cases

### 4. Quick Validation

For each library, validated:
- ✅ Works with LangChain and LlamaIndex (table stakes for LLM apps)
- ✅ Active development (commits within last month)
- ✅ Production users (verified through case studies, blog posts)
- ✅ Clear onboarding docs (can get started in <30 minutes)

## Discovery Tools Used

- **GitHub Search**: Repository discovery, star counts, activity
- **Package Registries**: PyPI (Python), npm (JavaScript) download stats
- **Community**: Stack Overflow mentions, Reddit discussions, HN "Show HN" posts
- **Integration Lists**: LangChain docs, LlamaIndex docs

## Why These Four?

**ChromaDB**: Highest signal-to-noise ratio for "easiest to get started" (4-function API)
**Pinecone**: Dominant in "zero-ops managed" space (despite vendor lock-in concerns)
**Qdrant**: Best performance-to-features ratio in self-hosted category
**Weaviate**: Unique strength in hybrid search (vector + BM25)

## Excluded from S1

- **Milvus**: Too enterprise-focused for rapid discovery (complex setup)
- **pgvector**: PostgreSQL extension, different category (augments existing DB)
- **FAISS**: Library not database (no persistence layer)
- **Elasticsearch/OpenSearch**: General-purpose search with vector add-on (different use case)

## Key Findings (S1 Rapid)

1. **Market maturity**: Vector databases moved from "bleeding edge" (2022) to "mainstream" (2025)
2. **RAG standardization**: All four integrate seamlessly with LangChain/LlamaIndex
3. **Deployment split**: Clear divide between managed (Pinecone) and self-hosted (others)
4. **Performance focus**: Community discussions shifted from "does it work?" to "how fast is it?" (Qdrant wins most benchmarks)

## Recommendation Preview

**For rapid prototyping**: ChromaDB (fastest time-to-first-query)
**For production deployments**: Qdrant (best performance + self-hosted) or Pinecone (zero-ops managed)
**For hybrid search**: Weaviate (best BM25 + vector integration)

See individual library profiles and final recommendation for detailed analysis.
