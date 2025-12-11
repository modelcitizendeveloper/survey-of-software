# Vector Databases: Domain Explainer

## What Are Vector Databases?

Vector databases are specialized database systems designed to store, index, and query high-dimensional vectors (embeddings). Unlike traditional databases that search for exact matches or ranges, vector databases find items that are **semantically similar** to a query.

### The Core Problem They Solve

Traditional databases excel at structured queries:
- "Find all users where `age > 25`"
- "Get products where `category = 'electronics'`"

But they fail at semantic queries:
- "Find documents similar to this one"
- "What products are related to 'comfortable summer shoes'?"
- "Which images look like this photo?"

Vector databases solve this by representing data as numerical vectors in high-dimensional space, where **similar items cluster together**.

## Key Concepts

### 1. Embeddings

Embeddings are numerical representations of data (text, images, audio) as vectors of floating-point numbers. They're created by machine learning models (like OpenAI's `text-embedding-3-small` or Sentence Transformers).

```python
# Example: Text to embedding
text = "The quick brown fox"
embedding = model.encode(text)  # Returns: [0.023, -0.156, 0.892, ...]
# Typical dimensions: 384, 768, 1536, 3072
```

**Why embeddings matter**: Two semantically similar texts will have vectors that are "close" in vector space, even if they share no common words.

### 2. Distance Metrics

Vector databases measure similarity using distance functions:

| Metric | Formula | Best For |
|--------|---------|----------|
| **Cosine** | 1 - cos(θ) | Text similarity (normalized vectors) |
| **Euclidean (L2)** | √Σ(a-b)² | Image embeddings, general purpose |
| **Dot Product** | Σ(a×b) | When magnitude matters (recommendations) |
| **Hamming** | Count of different bits | Binary vectors |

**Most common**: Cosine similarity for text, L2 for images.

### 3. Indexing Algorithms

Brute-force search (comparing every vector) is too slow at scale. Vector databases use **Approximate Nearest Neighbor (ANN)** algorithms:

| Algorithm | How It Works | Trade-offs |
|-----------|--------------|------------|
| **HNSW** | Multi-layer graph navigation | Best recall, higher memory |
| **IVF** | Clusters + inverted index | Faster build, lower recall |
| **Flat** | Brute force (exact) | 100% recall, slow at scale |
| **SCANN** | Learned quantization | Google's approach, good balance |
| **DiskANN** | SSD-optimized HNSW | Large datasets, lower memory |

**HNSW (Hierarchical Navigable Small World)** is the most popular choice in 2024-2025 for its excellent speed-recall tradeoff.

### 4. Approximate vs Exact Search

- **Exact (kNN)**: Guaranteed to find the true k nearest neighbors. O(n) complexity.
- **Approximate (ANN)**: Finds "good enough" neighbors much faster. Typically 95-99% recall.

Most production systems use ANN because the slight recall loss is acceptable for 100-1000x speed improvement.

## How They Differ from Traditional Databases

| Aspect | Traditional DB | Vector Database |
|--------|---------------|-----------------|
| Query type | Exact match, ranges | Similarity search |
| Data model | Tables, documents | Vectors + metadata |
| Index type | B-tree, hash | HNSW, IVF, etc. |
| Primary operation | SELECT WHERE | k-NN search |
| Result guarantee | Exact | Approximate (usually) |

## Use Cases

### 1. Semantic Search
Search by meaning, not just keywords.
```
Query: "affordable lightweight laptop for students"
Finds: "Budget Chromebook for college" (no keyword overlap!)
```

### 2. RAG (Retrieval Augmented Generation)
The dominant pattern for production LLM applications:
1. Chunk documents → generate embeddings → store in vector DB
2. User asks question → embed question → find relevant chunks
3. Pass chunks to LLM as context → generate answer

**Why RAG matters**: Reduces hallucinations, enables domain-specific knowledge, keeps data fresh.

### 3. Recommendation Systems
- "Users who liked X also liked Y"
- Product recommendations based on browsing history
- Content recommendations (Netflix, Spotify style)

### 4. Image/Multimodal Search
- "Find images similar to this one"
- CLIP embeddings enable text-to-image search
- Visual product search (Pinterest, Google Lens)

### 5. Anomaly Detection
Normal data clusters together; anomalies are far from any cluster.

### 6. Deduplication
Find near-duplicate documents, images, or records.

## The 2024-2025 Landscape

### Market Growth
- **$2.2B** market size in 2024
- **$10.6B** projected by 2032
- **21.9% CAGR**

### Categories of Solutions

1. **Purpose-Built Vector Databases**
   - Pinecone, Qdrant, Weaviate, Milvus, ChromaDB
   - Optimized specifically for vector operations

2. **Database Extensions**
   - pgvector (PostgreSQL), MongoDB Atlas Vector Search
   - Add vectors to existing databases

3. **Vector Libraries** (not databases)
   - FAISS (Facebook), Annoy (Spotify), ScaNN (Google)
   - In-memory only, no persistence/CRUD

### Key Trends

1. **RAG is Standard**: Most LLM applications use vector databases for retrieval
2. **Hybrid Search**: Combining vector similarity with keyword (BM25) search
3. **GraphRAG**: Emerging pattern combining vectors with knowledge graphs
4. **GPU Acceleration**: Milvus 2.4+ supports NVIDIA CAGRA for faster indexing
5. **Consolidation**: Traditional databases adding vector features

## Selection Criteria

### When to Use pgvector (PostgreSQL Extension)
- You already use PostgreSQL
- Under 100 million vectors
- Want single database for everything
- Team knows SQL

### When to Use a Dedicated Vector Database
- Vector search is your primary workload
- Need specialized features (hybrid search, filtering)
- Scale beyond 100 million vectors
- Need managed cloud service

### When to Use ChromaDB
- Rapid prototyping
- Learning/experimentation
- Embedded in application
- Under 1 million vectors

### Decision Matrix

| Criteria | ChromaDB | pgvector | Qdrant | Weaviate | Milvus | Pinecone |
|----------|----------|----------|--------|----------|--------|----------|
| Setup ease | ★★★★★ | ★★★★ | ★★★★ | ★★★ | ★★ | ★★★★★ |
| Scale | ★★ | ★★★ | ★★★★ | ★★★★ | ★★★★★ | ★★★★ |
| Performance | ★★★ | ★★★ | ★★★★★ | ★★★★ | ★★★★★ | ★★★★ |
| Features | ★★★ | ★★★ | ★★★★ | ★★★★★ | ★★★★★ | ★★★★ |
| Self-host | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★ | ★★★★ | ✗ |
| Managed | ★★★ | ★★★★ | ★★★★ | ★★★★ | ★★★★ | ★★★★★ |

## Common Misconceptions

### "Vector databases replace traditional databases"
**False**: They complement each other. Use vector DBs for similarity search, traditional DBs for structured data. Many applications use both.

### "More dimensions = better embeddings"
**Not always**: 1536 dimensions (OpenAI) often works as well as 3072 for most tasks. Higher dimensions increase storage and compute costs.

### "I need a vector database for my LLM app"
**Maybe not**: For small datasets (<10K documents), in-memory solutions like FAISS or even brute-force search may suffice.

### "All vector databases are the same"
**False**: Significant differences in:
- Performance characteristics
- Filtering capabilities
- Hybrid search support
- Deployment options
- Pricing models

## Getting Started

### Simplest Path (Python + ChromaDB)
```python
import chromadb

# Create client (in-memory)
client = chromadb.Client()

# Create collection
collection = client.create_collection("my_collection")

# Add documents (auto-embeds with default model)
collection.add(
    documents=["Doc about AI", "Doc about databases"],
    ids=["doc1", "doc2"]
)

# Query
results = collection.query(
    query_texts=["artificial intelligence"],
    n_results=2
)
```

### Production Path
1. **Prototype**: ChromaDB in-memory
2. **Validate**: ChromaDB persistent or pgvector
3. **Scale**: Qdrant, Weaviate, or Milvus (self-hosted or cloud)
4. **Enterprise**: Pinecone, Zilliz Cloud, or Weaviate Cloud

## Resources

### Official Documentation
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Pinecone Docs](https://docs.pinecone.io/)
- [Qdrant Docs](https://qdrant.tech/documentation/)
- [Weaviate Docs](https://weaviate.io/developers/weaviate)
- [Milvus Docs](https://milvus.io/docs)
- [pgvector GitHub](https://github.com/pgvector/pgvector)

### Learning Resources
- [LangChain Vector Store Guide](https://python.langchain.com/docs/modules/data_connection/vectorstores/)
- [LlamaIndex Vector Store Guide](https://docs.llamaindex.ai/en/stable/module_guides/storing/vector_stores/)

### Benchmarks
- [ANN Benchmarks](https://ann-benchmarks.com/)
- [Qdrant Benchmarks](https://qdrant.tech/benchmarks/)
- [VectorDBBench (Zilliz)](https://github.com/zilliztech/VectorDBBench)

---

**Last Updated**: 2025-12-11
**Related Research**: 1.200 (LLM Orchestration), 3.200 (LLM APIs), 3.040 (Databases)
