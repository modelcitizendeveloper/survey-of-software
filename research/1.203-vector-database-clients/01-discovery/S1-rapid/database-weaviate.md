# Weaviate Database Profile

## Overview

**Name**: Weaviate
**Developer**: Weaviate B.V. (Netherlands)
**First Release**: 2019
**Primary Language**: Go
**License**: BSD 3-Clause
**GitHub Stars**: ~12,000 (December 2025)
**Website**: https://weaviate.io/

Weaviate is an open-source, cloud-native vector database that excels at **hybrid search** - combining vector similarity with keyword (BM25) search in a single query. It's built in Go for speed and offers a unique GraphQL API alongside REST and gRPC.

## Core Capabilities

### Vector Storage & Search
- HNSW indexing with configurable parameters
- Dense vector similarity search
- Multiple distance metrics: Cosine, L2, Dot Product
- 10-NN search in single-digit milliseconds over millions of items

### Hybrid Search (Standout Feature)
Weaviate's killer feature is native hybrid search:
```graphql
{
  Get {
    Article(
      hybrid: {query: "machine learning", alpha: 0.5}
    ) {
      title
      content
    }
  }
}
```
- Combines BM25 keyword search with vector similarity
- Adjustable `alpha` parameter (0 = keyword only, 1 = vector only)
- Single query, combined ranking

### GraphQL API
Unique GraphQL interface:
- Connects data via cross-references (knowledge graph style)
- Eliminates over-fetching
- Three main operations: Get, Explore, Aggregate
- Powerful for complex data relationships

### Modules System
Modular architecture for extensibility:
- **Vectorizers**: OpenAI, Cohere, HuggingFace, local models
- **Generative**: Built-in RAG capabilities
- **Rerankers**: Improve result relevance
- **Readers**: Various data formats

## Programming Languages

### Official Clients
- **Python**: `pip install weaviate-client`
- **JavaScript/TypeScript**: `npm install weaviate-ts-client`
- **Go**: Official Go client (Builder pattern)
- **Java**: Official Java client
- **.NET**: Community maintained

### APIs
- **GraphQL**: Primary query interface
- **REST**: CRUD operations, DB management
- **gRPC**: High-performance operations

## Deployment Modes

### 1. Docker (Development)
```bash
docker run -p 8080:8080 semitechnologies/weaviate
```

### 2. Docker Compose
Production-ready with modules:
```yaml
services:
  weaviate:
    image: semitechnologies/weaviate
    environment:
      - ENABLE_MODULES=text2vec-openai,generative-openai
```

### 3. Kubernetes (Helm)
Enterprise deployment with:
- Horizontal scaling
- Replication
- Multi-tenancy

### 4. Weaviate Cloud Services (WCS)
Managed offering:
- 14-day free trial
- $25/month starting price
- Fully managed operations

## Learning Curve & Documentation

### Learning Curve
**Moderate to Steep** - More concepts than simpler alternatives:
- GraphQL familiarity helpful
- Module system requires understanding
- Schema design considerations
- Worth it for hybrid search capabilities

### Documentation Quality
- **Official Docs**: https://weaviate.io/developers/weaviate (comprehensive)
- **Tutorials**: DataCamp, official guides
- **API Reference**: GraphQL schema, REST endpoints
- **Contributor Guide**: Module architecture docs

### Time to First Query
~20-30 minutes including GraphQL basics

## Community & Ecosystem

### GitHub Activity
- ~12,000 stars
- Over 1 million Docker pulls per month
- Active development

### Framework Integrations
- **LangChain**: First-class support
- **LlamaIndex**: Native integration
- **Haystack**: Supported
- **Spring AI**: Java ecosystem

### Module Ecosystem
Pre-built modules for:
- OpenAI, Cohere, HuggingFace embeddings
- Image vectorization
- Multi-modal search
- Generative AI (built-in RAG)

## Performance Characteristics

### Latency
- 10-NN search in **single-digit milliseconds** over millions of items
- Hybrid search adds minimal overhead
- GraphQL parsing is efficient

### Scalability
- Horizontal scaling via sharding
- Replication for availability
- Tested at tens of millions of vectors

### Resource Considerations
- Higher memory usage than some alternatives at very large scale
- Below 50 million vectors, runs efficiently
- Resource needs increase significantly above 100M vectors

## Best Use Cases

### 1. Hybrid Search Applications
When you need both semantic AND keyword search:
- "Find articles about 'neural networks' that mention 'transformer'"
- Combines meaning-based and exact-match

### 2. Knowledge Graphs
When data has relationships:
- Cross-references between objects
- Graph-style traversals
- Entity relationship modeling

### 3. GraphQL-First Teams
Teams already using GraphQL:
- Consistent API patterns
- Single query for complex data
- Familiar tooling

### 4. Built-in RAG
Generative search without external orchestration:
```graphql
{
  Get {
    Article(nearText: {concepts: ["AI"]}) {
      title
      _additional {
        generate(prompt: "Summarize: {content}") {
          singleResult
        }
      }
    }
  }
}
```

### 5. Multi-Modal Search
Image + text search with vectorizer modules.

## Limitations

### 1. Memory at Scale
Higher memory consumption than alternatives:
- Noticeable above 50M vectors
- Plan for resource scaling

### 2. Learning Curve
Steeper than ChromaDB or Pinecone:
- GraphQL concepts
- Module configuration
- Schema design

### 3. GraphQL Requirement
Not everyone wants GraphQL:
- REST/gRPC available but GraphQL is primary
- Team must learn GraphQL patterns

### 4. Cloud Pricing
$25/month after 14-day trial:
- No permanent free tier (unlike Qdrant)
- Can add up for experiments

### 5. Performance vs Qdrant
Benchmark comparisons show:
- Qdrant leads in raw QPS
- Weaviate trades some speed for features

## Production Readiness

### Enterprise Features
- Multi-tenancy (built-in)
- Replication
- RBAC authorization
- Backups and recovery

### Adoption
- Production deployments at scale
- Enterprise customers
- Active support community

### Compliance
- SOC 2 (Cloud)
- GDPR ready
- Enterprise security features

## Code Examples

### Basic Usage (Python)
```python
import weaviate
from weaviate.classes.config import Configure, Property, DataType

# Connect
client = weaviate.connect_to_local()

# Create collection
collection = client.collections.create(
    name="Article",
    vectorizer_config=Configure.Vectorizer.text2vec_openai(),
    properties=[
        Property(name="title", data_type=DataType.TEXT),
        Property(name="content", data_type=DataType.TEXT),
        Property(name="category", data_type=DataType.TEXT)
    ]
)

# Insert data
collection.data.insert({
    "title": "Introduction to Machine Learning",
    "content": "Machine learning is a subset of AI...",
    "category": "tech"
})

# Vector search
results = collection.query.near_text(
    query="artificial intelligence",
    limit=5
)
```

### Hybrid Search
```python
# Combine vector and keyword search
results = collection.query.hybrid(
    query="machine learning transformers",
    alpha=0.5,  # Balance between vector (1) and keyword (0)
    limit=10
)
```

### GraphQL Query
```graphql
{
  Get {
    Article(
      nearText: {concepts: ["artificial intelligence"]}
      where: {
        path: ["category"]
        operator: Equal
        valueText: "tech"
      }
      limit: 5
    ) {
      title
      content
      _additional {
        distance
      }
    }
  }
}
```

### With LangChain
```python
from langchain_weaviate import WeaviateVectorStore
from langchain_openai import OpenAIEmbeddings

vectorstore = WeaviateVectorStore.from_documents(
    documents,
    OpenAIEmbeddings(),
    client=client,
    index_name="Article"
)

# Hybrid search
results = vectorstore.similarity_search(
    "query text",
    k=4,
    search_type="hybrid",
    alpha=0.5
)
```

## When to Choose Weaviate

### Choose Weaviate When:
- Hybrid search is critical (vector + BM25)
- Building knowledge graphs with relationships
- Team prefers GraphQL
- Need built-in RAG capabilities
- Want module ecosystem (vectorizers, generative)
- Multi-modal search (image + text)

### Avoid Weaviate When:
- Raw performance is priority (use Qdrant)
- Simplest setup needed (use ChromaDB)
- Very large scale 100M+ (memory concerns)
- Team dislikes GraphQL
- Budget-constrained experiments (no free cloud tier)

## Summary

Weaviate is the **hybrid search leader** with the best native support for combining vector similarity with keyword (BM25) search. Its GraphQL API and modules ecosystem make it powerful for knowledge graph applications. The trade-off is higher complexity and memory usage compared to simpler alternatives. Ideal for teams that need sophisticated search combining semantic understanding with traditional keyword matching.

---

**Sources**:
- [Weaviate GitHub](https://github.com/weaviate/weaviate)
- [Weaviate Documentation](https://weaviate.io/developers/weaviate)
- [Weaviate Tutorial - DataCamp](https://www.datacamp.com/tutorial/weaviate-tutorial)
- [Go Client Documentation](https://weaviate.io/developers/weaviate/client-libraries/go)
