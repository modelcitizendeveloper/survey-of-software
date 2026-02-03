# Qdrant

**Repository:** github.com/qdrant/qdrant
**Downloads/Month:** ~100,000 (PyPI client), Docker pulls in millions
**GitHub Stars:** 22,000+
**Last Updated:** 2025-12 (very active development)

## Quick Assessment
- **Popularity**: High (fastest-growing vector database in 2024-2025)
- **Maintenance**: Very Active (multiple releases per month, responsive team)
- **Documentation**: Good (comprehensive docs, examples, deployment guides)

## Pros
- **Performance**: Best-in-class (Rust-based, sub-10ms p50 latency at scale)
- **Rich filtering**: Complex metadata queries without performance degradation
- **Quantization**: 97% RAM reduction via scalar/product quantization
- **Deployment options**: Self-hosted Docker, Kubernetes, or managed Qdrant Cloud
- **Hybrid search**: BM42 keyword search + vector similarity in one query

## Cons
- **Operational overhead**: Self-hosting requires DevOps expertise (unless using managed cloud)
- **Ecosystem maturity**: Smaller plugin/integration ecosystem than Weaviate
- **Learning curve**: More configuration options than ChromaDB (steeper initial setup)
- **Relatively new**: Production-ready since ~2021, less enterprise case studies than Pinecone

## Quick Take
Qdrant is the performance leader for production vector search. If you need high throughput, complex filtering, or want to optimize costs via quantization, Qdrant delivers. It's the best self-hosted option for teams with DevOps capacity who want performance without vendor lock-in.
