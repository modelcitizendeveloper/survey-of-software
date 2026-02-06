# ChromaDB

**Repository:** github.com/chroma-core/chroma
**Downloads/Month:** ~500,000 (PyPI)
**GitHub Stars:** 23,000+
**Last Updated:** 2025-12 (active development)

## Quick Assessment
- **Popularity**: High (top 3 in vector database space)
- **Maintenance**: Active (weekly releases, responsive maintainers)
- **Documentation**: Excellent (clear quickstart, extensive examples)

## Pros
- **Simplest API**: Only 4 functions (add, query, update, delete) - fastest learning curve
- **Flexible deployment**: In-memory, persistent local, client-server, or managed cloud
- **Auto-embedding**: Built-in embedding generation (can use OpenAI, Sentence Transformers, or custom)
- **Framework integration**: First-class support in LangChain and LlamaIndex
- **Open source**: Apache 2.0 license, no vendor lock-in

## Cons
- **Scale limits**: Not designed for billions of vectors (practical limit ~10M)
- **Fewer production features**: Limited compared to Qdrant or Weaviate (no multi-tenancy, basic RBAC)
- **Performance**: Good but not best-in-class (Qdrant faster on large datasets)
- **Relatively new**: Only since 2022 (less battle-tested than competitors)

## Quick Take
ChromaDB is the fastest way to add semantic search to an LLM application. If you're prototyping a RAG system or building an MVP, start here. The 4-function API means you'll be querying embeddings within 5 minutes of `pip install chromadb`.
