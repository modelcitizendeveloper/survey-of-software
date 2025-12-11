# Vector Database Comparison Matrix

## Overview Comparison

| Feature | ChromaDB | Pinecone | Qdrant | Weaviate | Milvus | pgvector |
|---------|----------|----------|--------|----------|--------|----------|
| **License** | Apache 2.0 | Proprietary | Apache 2.0 | BSD 3-Clause | Apache 2.0 | PostgreSQL |
| **GitHub Stars** | ~23k | N/A (cloud) | ~22k | ~12k | ~35k+ | ~13k |
| **Primary Lang** | Python | Cloud (clients) | Rust | Go | Go/C++ | C (ext) |
| **First Release** | 2022 | 2021 | 2021 | 2019 | 2019 | 2021 |
| **CNCF Status** | - | - | - | - | Graduated | - |

## Deployment Options

| Mode | ChromaDB | Pinecone | Qdrant | Weaviate | Milvus | pgvector |
|------|----------|----------|--------|----------|--------|----------|
| **In-Memory** | ✅ | ❌ | ❌ | ❌ | ✅ (Lite) | ❌ |
| **Embedded/Local** | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Docker** | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Kubernetes** | ❌ | ❌ | ✅ | ✅ | ✅ | ✅* |
| **Managed Cloud** | ✅ (new) | ✅ | ✅ | ✅ | ✅ (Zilliz) | ✅** |
| **Self-Hosted** | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |

*Via PostgreSQL operators
**Via Supabase, Neon, RDS, etc.

## Feature Comparison

| Feature | ChromaDB | Pinecone | Qdrant | Weaviate | Milvus | pgvector |
|---------|----------|----------|--------|----------|--------|----------|
| **HNSW Index** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **IVF Index** | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ |
| **GPU Acceleration** | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Hybrid Search** | ❌ | ✅ | ✅ | ✅ (best) | ✅ | ❌* |
| **Metadata Filtering** | ✅ | ✅ | ✅ (best) | ✅ | ✅ | ✅ |
| **Multi-Tenancy** | Basic | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Replication** | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Sharding** | ❌ | ✅ | ✅ | ✅ | ✅ | ✅*** |
| **GraphQL API** | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| **gRPC API** | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ |
| **Built-in Embeddings** | ✅ | ✅** | ❌ | ✅ | ❌ | ❌ |
| **Quantization** | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ (0.7+) |

*Requires separate full-text search
**Via Pinecone Inference
***Via PostgreSQL sharding solutions

## Distance Metrics

| Metric | ChromaDB | Pinecone | Qdrant | Weaviate | Milvus | pgvector |
|--------|----------|----------|--------|----------|--------|----------|
| **Cosine** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Euclidean (L2)** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Dot Product** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **L1 (Manhattan)** | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ (0.7+) |
| **Hamming** | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ (0.7+) |
| **Jaccard** | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ (0.7+) |

## Client Libraries

| Language | ChromaDB | Pinecone | Qdrant | Weaviate | Milvus | pgvector |
|----------|----------|----------|--------|----------|--------|----------|
| **Python** | ✅ Official | ✅ Official | ✅ Official | ✅ Official | ✅ Official | ✅ Any PG |
| **JavaScript** | ✅ Official | ✅ Official | ✅ Official | ✅ Official | ✅ Official | ✅ Any PG |
| **Go** | ✅ Community | ✅ Official | ✅ Official | ✅ Official | ✅ Official | ✅ Any PG |
| **Java** | ❌ | ✅ Official | ✅ Official | ✅ Official | ✅ Official | ✅ Any PG |
| **Rust** | ❌ | ❌ | ✅ Native | ❌ | ❌ | ✅ Any PG |
| **.NET** | ❌ | ❌ | ✅ Community | ✅ Community | ❌ | ✅ Any PG |
| **REST API** | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |

## Performance Characteristics

| Metric | ChromaDB | Pinecone | Qdrant | Weaviate | Milvus | pgvector |
|--------|----------|----------|--------|----------|--------|----------|
| **Query Latency (1M)** | ~20ms | 10-100ms | <10ms | <10ms | Varies* | Varies |
| **RPS Leader** | ❌ | ❌ | ✅ | ❌ | ✅ (GPU) | ❌ |
| **Indexing Speed** | Moderate | Fast | Fast | Moderate | Fastest (GPU) | Moderate |
| **Memory Efficiency** | High | N/A | High (quant) | Moderate | Moderate | High (quant) |

*Depends on index type and GPU usage

## Scalability

| Scale | ChromaDB | Pinecone | Qdrant | Weaviate | Milvus | pgvector |
|-------|----------|----------|--------|----------|--------|----------|
| **<100K vectors** | ✅✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅ | ✅✅✅ |
| **100K-1M** | ✅✅ | ✅✅✅ | ✅✅✅ | ✅✅✅ | ✅✅ | ✅✅✅ |
| **1M-10M** | ✅ | ✅✅✅ | ✅✅✅ | ✅✅✅ | ✅✅✅ | ✅✅ |
| **10M-100M** | ❌ | ✅✅✅ | ✅✅✅ | ✅✅ | ✅✅✅ | ✅ |
| **100M-1B** | ❌ | ✅✅ | ✅✅ | ✅ | ✅✅✅ | ❌ |
| **1B+** | ❌ | ✅ | ✅ | ❌ | ✅✅✅ | ❌ |

Legend: ✅✅✅ Excellent, ✅✅ Good, ✅ Possible, ❌ Not recommended

## Pricing Comparison

| Aspect | ChromaDB | Pinecone | Qdrant | Weaviate | Milvus | pgvector |
|--------|----------|----------|--------|----------|--------|----------|
| **Self-Hosted** | Free | N/A | Free | Free | Free | Free |
| **Free Tier** | Yes | 100K vec | 1GB forever | 14-day trial | Zilliz trial | Via services |
| **Entry Price** | Cloud TBD | $50/mo min | Pay-as-you-go | $25/mo | Zilliz pricing | $0* |
| **Enterprise** | TBD | $500/mo+ | Custom | Custom | Custom | $0* |

*PostgreSQL infrastructure costs apply

## Framework Integrations

| Framework | ChromaDB | Pinecone | Qdrant | Weaviate | Milvus | pgvector |
|-----------|----------|----------|--------|----------|--------|----------|
| **LangChain** | ✅ First-class | ✅ First-class | ✅ First-class | ✅ First-class | ✅ First-class | ✅ First-class |
| **LlamaIndex** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Haystack** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Semantic Kernel** | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Spring AI** | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |

## Enterprise Features

| Feature | ChromaDB | Pinecone | Qdrant | Weaviate | Milvus | pgvector |
|---------|----------|----------|--------|----------|--------|----------|
| **SOC 2** | ❌ | ✅ | Cloud | Cloud | Zilliz | Via provider |
| **HIPAA** | ❌ | ✅ | Cloud | Cloud | Zilliz | Via provider |
| **GDPR** | ❌ | ✅ | ✅ | ✅ | ✅ | Via provider |
| **RBAC** | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ (PG native) |
| **SSO** | ❌ | Enterprise | Cloud | Cloud | Zilliz | Via provider |
| **SLA** | ❌ | Enterprise | Cloud | Cloud | Zilliz | Via provider |
| **PrivateLink** | ❌ | ✅ | Cloud | Cloud | Zilliz | Via provider |

## Learning Curve & Documentation

| Aspect | ChromaDB | Pinecone | Qdrant | Weaviate | Milvus | pgvector |
|--------|----------|----------|--------|----------|--------|----------|
| **Setup Time** | 5 min | 10 min | 15 min | 20-30 min | 15-60 min | 5-15 min |
| **Learning Curve** | Easy | Easy | Moderate | Moderate-Steep | Steep | Easy* |
| **Documentation** | Good | Excellent | Excellent | Comprehensive | Comprehensive | Good |
| **Tutorials** | Many | Many | Growing | Growing | Many | Many |
| **Community Size** | Large | Large | Growing | Growing | Largest | Large |

*If familiar with PostgreSQL

## Use Case Fit

| Use Case | Best Choice | Second Choice |
|----------|-------------|---------------|
| **Rapid Prototyping** | ChromaDB | pgvector |
| **Zero-Ops Production** | Pinecone | Weaviate Cloud |
| **Complex Filtering** | Qdrant | Milvus |
| **Hybrid Search** | Weaviate | Qdrant |
| **Massive Scale (1B+)** | Milvus | Qdrant |
| **GPU Workloads** | Milvus | - |
| **Existing PostgreSQL** | pgvector | - |
| **GraphQL API** | Weaviate | - |
| **Rust Ecosystem** | Qdrant | - |
| **Multi-Language Support** | pgvector | Milvus |
| **Budget Constrained** | pgvector | ChromaDB |
| **Enterprise Compliance** | Pinecone | Weaviate Cloud |

## Risk Factors

| Risk | ChromaDB | Pinecone | Qdrant | Weaviate | Milvus | pgvector |
|------|----------|----------|--------|----------|--------|----------|
| **Vendor Lock-in** | Low | High | Low | Low | Low | None |
| **Funding/Viability** | VC-backed | Uncertain* | VC-backed | VC-backed | CNCF + Zilliz | Community |
| **Migration Difficulty** | Easy | Hard | Moderate | Moderate | Moderate | Easy** |
| **Technology Risk** | Maturing | Mature | Mature | Mature | Mature | Mature |

*Recent leadership changes, acquisition rumors
**Standard PostgreSQL data

## Summary by Scenario

### "I'm building a prototype"
→ **ChromaDB** (simplest) or **pgvector** (if using PostgreSQL)

### "I need production with zero infrastructure work"
→ **Pinecone** (but watch costs and lock-in)

### "I need the best filtering performance"
→ **Qdrant** (Rust-based, benchmark leader)

### "I need hybrid vector + keyword search"
→ **Weaviate** (native BM25 + vectors)

### "I need billion-scale with GPU"
→ **Milvus** (CNCF graduate, GPU CAGRA)

### "I already use PostgreSQL"
→ **pgvector** (no new infrastructure)

---

**Sources**: Research compiled from official documentation, GitHub repositories, benchmark publications, and industry analyses (December 2025).
