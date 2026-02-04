# Use Case: RAG / Document Q&A System

## Executive Summary

**Best Framework**: LlamaIndex (specialized) or Haystack (production + RAG)

**Time to Production**: 3-6 weeks for MVP, 10-16 weeks for production-grade

**Key Requirements**:
- Document ingestion at scale (PDFs, docs, web)
- Intelligent chunking strategies
- High-quality embeddings and indexing
- Advanced retrieval (hybrid search, reranking)
- Citation and source attribution
- Handling 1000+ documents

## Framework Comparison for RAG

| Framework | RAG Suitability | Key Strengths | Limitations |
|-----------|----------------|---------------|-------------|
| **LlamaIndex** | Excellent (5/5) | **35% better retrieval**, best document parsing, RAG-specialized | Not ideal for non-RAG use cases |
| **Haystack** | Excellent (4/5) | Best production readiness, hybrid search, Fortune 500 adoption | More complex setup |
| **LangChain** | Good (3/5) | General-purpose, easy to start | Not specialized for RAG, higher token usage |
| **Semantic Kernel** | Fair (2/5) | Good for simple RAG in Azure | Limited advanced retrieval |
| **DSPy** | Fair (2/5) | Can optimize retrieval prompts | Not focused on RAG workflows |

**Winner**: **LlamaIndex** for best accuracy, **Haystack** for production + performance

## LlamaIndex vs LangChain for RAG: The Deep Dive

### Retrieval Accuracy
- **LlamaIndex**: 35% boost in retrieval accuracy (2025)
- **LangChain**: Baseline RAG support, adequate for most cases
- **Verdict**: LlamaIndex wins significantly

### Document Parsing
- **LlamaIndex**: LlamaParse (best-in-class) - skew detection, complex PDFs
- **LangChain**: Basic document loaders
- **Verdict**: LlamaIndex wins

### Retrieval Strategies
- **LlamaIndex**: Advanced (CRAG, HyDE, Self-RAG, RAPTOR, hybrid)
- **LangChain**: Standard (vector similarity, MMR)
- **Verdict**: LlamaIndex wins

### Ecosystem
- **LlamaIndex**: RAG-focused integrations, LlamaCloud
- **LangChain**: Broader ecosystem (agents, tools, memory)
- **Verdict**: Depends on needs

### Learning Curve
- **LlamaIndex**: Moderate (RAG concepts required)
- **LangChain**: Easier for beginners
- **Verdict**: LangChain wins for getting started

## Document Ingestion Pipeline

### Supported Document Types

```python
# LlamaIndex comprehensive document loaders
from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import PDFReader, DocxReader

# Load multiple document types
documents = SimpleDirectoryReader(
    input_dir="./data",
    file_extractor={
        ".pdf": PDFReader(),
        ".docx": DocxReader(),
        ".txt": None,  # default text reader
    },
    recursive=True,
    required_exts=[".pdf", ".docx", ".txt"]
).load_data()

# LlamaParse for complex PDFs (premium)
from llama_parse import LlamaParse

parser = LlamaParse(
    api_key="your-api-key",
    result_type="markdown",  # or "text"
    verbose=True
)

documents = parser.load_data("./complex_document.pdf")
```

### Web Scraping Integration
```python
from llama_index.readers.web import SimpleWebPageReader

# Scrape documentation sites
urls = [
    "https://docs.example.com/guide",
    "https://docs.example.com/api",
]

documents = SimpleWebPageReader(html_to_text=True).load_data(urls)
```

### Enterprise Data Sources
```python
# SharePoint integration
from llama_index.readers.microsoft_sharepoint import SharePointReader

sharepoint = SharePointReader(
    client_id="your-client-id",
    client_secret="your-secret",
    tenant_id="your-tenant"
)

documents = sharepoint.load_data(document_library="Documents")

# Google Drive integration
from llama_index.readers.google import GoogleDriveReader

gdrive = GoogleDriveReader()
documents = gdrive.load_data(folder_id="your-folder-id")
```

### Batch Processing Large Datasets
```python
import os
from pathlib import Path
from tqdm import tqdm

def ingest_large_corpus(data_dir: str, batch_size: int = 100):
    """Process large document corpus in batches"""
    files = list(Path(data_dir).rglob("*.pdf"))

    for i in tqdm(range(0, len(files), batch_size)):
        batch_files = files[i:i+batch_size]

        # Process batch
        documents = SimpleDirectoryReader(
            input_files=[str(f) for f in batch_files]
        ).load_data()

        # Index batch
        nodes = node_parser.get_nodes_from_documents(documents)
        index.insert_nodes(nodes)

        # Optional: Clear memory
        del documents, nodes

# Process 10,000 documents
ingest_large_corpus("./large_corpus", batch_size=100)
```

## Chunking Strategies

### 1. Fixed-Size Chunking (Simple)
```python
from llama_index.core.node_parser import SimpleNodeParser

node_parser = SimpleNodeParser.from_defaults(
    chunk_size=1024,        # tokens
    chunk_overlap=200,      # overlap between chunks
)

nodes = node_parser.get_nodes_from_documents(documents)
```

### 2. Sentence-Based Chunking (Better)
```python
from llama_index.core.node_parser import SentenceSplitter

node_parser = SentenceSplitter(
    chunk_size=1024,
    chunk_overlap=200,
    separator=" ",
    paragraph_separator="\n\n",
)

nodes = node_parser.get_nodes_from_documents(documents)
```

### 3. Semantic Chunking (Best)
```python
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding

embed_model = OpenAIEmbedding()

node_parser = SemanticSplitterNodeParser(
    buffer_size=1,          # chunks combined if semantically similar
    breakpoint_percentile_threshold=95,  # similarity threshold
    embed_model=embed_model,
)

nodes = node_parser.get_nodes_from_documents(documents)
```

### 4. Hierarchical Chunking (Advanced)
```python
from llama_index.core.node_parser import HierarchicalNodeParser

# Create parent-child relationships
node_parser = HierarchicalNodeParser.from_defaults(
    chunk_sizes=[2048, 512, 128],  # parent -> child sizes
)

nodes = node_parser.get_nodes_from_documents(documents)
# Enables querying at multiple granularities
```

### Chunking Strategy Selection

| Document Type | Recommended Strategy | Chunk Size | Overlap |
|--------------|---------------------|------------|---------|
| **Technical docs** | Semantic | 1024 | 200 |
| **Legal documents** | Sentence-based | 512 | 100 |
| **Books/long-form** | Hierarchical | 2048→512 | 150 |
| **Short articles** | Fixed-size | 512 | 50 |
| **Code documentation** | Semantic | 1024 | 200 |
| **Chat logs** | Sentence-based | 256 | 50 |

### Chunk Size Impact
```python
# Smaller chunks (256-512 tokens)
# Pros: More precise retrieval, better for specific questions
# Cons: May lose context, need more chunks for broad questions
# Use for: Technical Q&A, specific fact lookup

# Medium chunks (512-1024 tokens)
# Pros: Good balance of precision and context
# Cons: Default recommendation
# Use for: Most RAG applications

# Large chunks (1024-2048 tokens)
# Pros: Better context retention, fewer retrievals needed
# Cons: May include irrelevant information, higher cost
# Use for: Summarization, conceptual questions
```

## Embedding and Indexing

### Embedding Model Selection

```python
# OpenAI (best quality, expensive)
from llama_index.embeddings.openai import OpenAIEmbedding
embed_model = OpenAIEmbedding(
    model="text-embedding-3-large",  # 3072 dimensions
    dimensions=1024,  # can reduce for cost
)

# OpenAI Small (good quality, cheaper)
embed_model = OpenAIEmbedding(
    model="text-embedding-3-small",  # 1536 dimensions
)

# Cohere (high quality, competitive pricing)
from llama_index.embeddings.cohere import CohereEmbedding
embed_model = CohereEmbedding(
    api_key="your-api-key",
    model_name="embed-english-v3.0",
)

# Local/Open-source (free, slower)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-large-en-v1.5"
)
```

### Embedding Cost Comparison

| Provider | Model | Dimensions | Cost/1M tokens | Quality |
|----------|-------|------------|----------------|---------|
| OpenAI | text-embedding-3-large | 3072 | $0.13 | Best |
| OpenAI | text-embedding-3-small | 1536 | $0.02 | Excellent |
| Cohere | embed-english-v3.0 | 1024 | $0.10 | Excellent |
| Local | bge-large-en-v1.5 | 1024 | $0 (compute) | Very Good |

### Vector Store Options

```python
# Pinecone (serverless, easy)
from llama_index.vector_stores.pinecone import PineconeVectorStore
import pinecone

pc = pinecone.Pinecone(api_key="your-api-key")
index = pc.Index("quickstart")

vector_store = PineconeVectorStore(pinecone_index=index)

# Qdrant (self-hosted, open-source)
from llama_index.vector_stores.qdrant import QdrantVectorStore
import qdrant_client

client = qdrant_client.QdrantClient(url="http://localhost:6333")
vector_store = QdrantVectorStore(client=client, collection_name="documents")

# Chroma (local, for development)
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

chroma_client = chromadb.PersistentClient(path="./chroma_db")
vector_store = ChromaVectorStore(chroma_collection=chroma_client.get_or_create_collection("docs"))

# Weaviate (production, scalable)
from llama_index.vector_stores.weaviate import WeaviateVectorStore
import weaviate

client = weaviate.Client("http://localhost:8080")
vector_store = WeaviateVectorStore(weaviate_client=client)
```

### Vector Store Comparison

| Vector DB | Best For | Cost | Scaling | Self-Hosted |
|-----------|----------|------|---------|-------------|
| **Pinecone** | Quick start, serverless | $70+/mo | Auto | No |
| **Qdrant** | Production, control | Free + infra | Manual | Yes |
| **Weaviate** | Enterprise, features | Free + infra | Kubernetes | Yes |
| **Chroma** | Development, prototyping | Free | Local only | Yes |
| **Milvus** | Large-scale, performance | Free + infra | Excellent | Yes |

### Creating the Index

```python
from llama_index.core import VectorStoreIndex, StorageContext

# Create storage context
storage_context = StorageContext.from_defaults(
    vector_store=vector_store
)

# Create index from documents
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    embed_model=embed_model,
    show_progress=True,
)

# Or create from nodes (after chunking)
index = VectorStoreIndex(
    nodes,
    storage_context=storage_context,
    embed_model=embed_model,
)
```

## Retrieval Techniques

### 1. Basic Vector Similarity (Baseline)
```python
# Simple similarity search
query_engine = index.as_query_engine(
    similarity_top_k=5,  # retrieve top 5 chunks
)

response = query_engine.query("What are the main features?")
```

### 2. Hybrid Search (Better)
Combine dense (semantic) and sparse (keyword) retrieval:

```python
# Using Haystack for hybrid search
from haystack import Pipeline
from haystack.components.retrievers import InMemoryBM25Retriever, InMemoryEmbeddingRetriever
from haystack.components.joiners import DocumentJoiner

# Create pipeline
pipeline = Pipeline()

# Add both retrievers
pipeline.add_component("bm25_retriever", InMemoryBM25Retriever(document_store))
pipeline.add_component("embedding_retriever", InMemoryEmbeddingRetriever(document_store))
pipeline.add_component("joiner", DocumentJoiner())

# Connect components
pipeline.connect("bm25_retriever", "joiner")
pipeline.connect("embedding_retriever", "joiner")

# Run hybrid search
result = pipeline.run({
    "bm25_retriever": {"query": "LLM frameworks"},
    "embedding_retriever": {"query": "LLM frameworks"},
})
```

### 3. Reranking (Best for Precision)
```python
from llama_index.postprocessor.cohere_rerank import CohereRerank

# Add reranking step
reranker = CohereRerank(
    api_key="your-api-key",
    top_n=3,  # return top 3 after reranking
)

query_engine = index.as_query_engine(
    similarity_top_k=10,      # retrieve 10 candidates
    node_postprocessors=[reranker],  # rerank to top 3
)

response = query_engine.query("Complex technical question")
```

### 4. HyDE (Hypothetical Document Embeddings)
```python
from llama_index.indices.query.query_transform import HyDEQueryTransform

# Generate hypothetical answer, use for retrieval
hyde = HyDEQueryTransform(include_original=True)

query_engine = index.as_query_engine(
    query_transform=hyde,
)

# Better for abstract or conceptual queries
response = query_engine.query("What are the benefits of microservices?")
```

### 5. CRAG (Corrective RAG)
```python
# LlamaIndex CRAG implementation
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import LLMRerank

retriever = index.as_retriever(similarity_top_k=10)

# Corrective reranking
reranker = LLMRerank(
    choice_batch_size=5,
    top_n=3,
)

query_engine = RetrieverQueryEngine(
    retriever=retriever,
    node_postprocessors=[reranker],
)
```

### 6. Multi-Query Retrieval
```python
# Generate multiple query variations
from llama_index.core.indices.query.query_transform import MultiQueryTransform

multi_query = MultiQueryTransform(num_queries=3)

query_engine = index.as_query_engine(
    query_transform=multi_query,
)

# Retrieves using 3 different query phrasings
response = query_engine.query("How to optimize database performance?")
```

### Retrieval Strategy Selection

| Query Type | Best Strategy | Why |
|-----------|---------------|-----|
| **Specific fact lookup** | Vector similarity | Fast, direct |
| **Keyword-heavy** | Hybrid search | Combines semantic + keywords |
| **Complex questions** | Reranking + HyDE | Higher precision |
| **Ambiguous queries** | Multi-query | Multiple perspectives |
| **Need high precision** | CRAG or reranking | Filters irrelevant results |
| **Conceptual questions** | HyDE | Better semantic matching |

## Citation and Source Attribution

### Basic Source Tracking
```python
response = query_engine.query("What are the key features?")

# Access source documents
for node in response.source_nodes:
    print(f"Score: {node.score}")
    print(f"Text: {node.text}")
    print(f"Metadata: {node.metadata}")
    print(f"File: {node.metadata.get('file_name')}")
    print(f"Page: {node.metadata.get('page_label')}")
    print("---")
```

### Custom Citation Formatting
```python
def format_response_with_citations(response):
    """Format response with inline citations"""
    answer = response.response

    citations = []
    for i, node in enumerate(response.source_nodes, 1):
        file_name = node.metadata.get('file_name', 'Unknown')
        page = node.metadata.get('page_label', 'N/A')
        citations.append(f"[{i}] {file_name}, page {page}")

    # Add citations to answer
    cited_answer = f"{answer}\n\nSources:\n" + "\n".join(citations)
    return cited_answer

result = format_response_with_citations(response)
```

### Advanced Citation with Confidence Scores
```python
def create_citation_report(response, confidence_threshold=0.7):
    """Create detailed citation report with confidence scores"""
    report = {
        "answer": response.response,
        "high_confidence_sources": [],
        "low_confidence_sources": [],
    }

    for node in response.source_nodes:
        citation = {
            "score": node.score,
            "file": node.metadata.get('file_name'),
            "page": node.metadata.get('page_label'),
            "text_snippet": node.text[:200] + "...",
        }

        if node.score >= confidence_threshold:
            report["high_confidence_sources"].append(citation)
        else:
            report["low_confidence_sources"].append(citation)

    return report
```

## Handling Large Document Corpora (1000+ docs)

### Indexing Strategy for Scale

```python
# Use index persistence
from llama_index.core import load_index_from_storage, StorageContext

# First time: create and save
index = VectorStoreIndex.from_documents(documents, show_progress=True)
index.storage_context.persist(persist_dir="./storage")

# Subsequent runs: load from disk
storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)
```

### Incremental Indexing
```python
def add_documents_to_existing_index(new_documents, index_path="./storage"):
    """Add new documents without re-indexing everything"""
    # Load existing index
    storage_context = StorageContext.from_defaults(persist_dir=index_path)
    index = load_index_from_storage(storage_context)

    # Add new documents
    for doc in new_documents:
        index.insert(doc)

    # Persist updated index
    index.storage_context.persist(persist_dir=index_path)

# Add 100 new documents to existing 10,000
add_documents_to_existing_index(new_docs)
```

### Hierarchical Retrieval for Scale
```python
from llama_index.core import DocumentSummaryIndex

# Create summary index (faster for large corpora)
summary_index = DocumentSummaryIndex.from_documents(
    documents,
    embed_model=embed_model,
    show_progress=True,
)

# Two-stage retrieval: summary first, then detail
query_engine = summary_index.as_query_engine(
    response_mode="tree_summarize",
    use_async=True,
)
```

### Namespace/Filtering for Multi-Tenant
```python
# Store documents with tenant metadata
for doc in documents:
    doc.metadata["tenant_id"] = "company_abc"
    doc.metadata["category"] = "technical_docs"

# Query with filters
from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter

filters = MetadataFilters(
    filters=[
        ExactMatchFilter(key="tenant_id", value="company_abc"),
        ExactMatchFilter(key="category", value="technical_docs"),
    ]
)

query_engine = index.as_query_engine(
    filters=filters,
    similarity_top_k=5,
)
```

### Performance Optimization for 10K+ Documents

```python
# Use batched querying
async def batch_query(queries: list[str], batch_size: int = 10):
    """Process queries in batches for efficiency"""
    results = []

    for i in range(0, len(queries), batch_size):
        batch = queries[i:i+batch_size]

        # Parallel processing
        batch_results = await asyncio.gather(*[
            query_engine.aquery(q) for q in batch
        ])

        results.extend(batch_results)

    return results

# Process 1000 queries efficiently
queries = ["Query 1", "Query 2", ...]  # 1000 queries
results = await batch_query(queries)
```

## Example RAG Architecture

### Simple RAG (MVP)
```python
# Complete LlamaIndex RAG system
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# 1. Load documents
documents = SimpleDirectoryReader("./data").load_data()

# 2. Create index
index = VectorStoreIndex.from_documents(
    documents,
    embed_model=OpenAIEmbedding(),
)

# 3. Create query engine
query_engine = index.as_query_engine(
    llm=OpenAI(model="gpt-4"),
    similarity_top_k=5,
)

# 4. Query
response = query_engine.query("What are the main points?")
print(response)

# Time to build: 1-2 days
# Cost: $50-100/month (small dataset)
```

### Production RAG (with Reranking)
```python
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.postprocessor.cohere_rerank import CohereRerank
from llama_index.embeddings.openai import OpenAIEmbedding
import pinecone

# 1. Setup vector store
pc = pinecone.Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
pinecone_index = pc.Index("production-rag")
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

# 2. Create storage context
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# 3. Load or create index
try:
    index = load_index_from_storage(storage_context)
except:
    documents = load_documents_from_sources()
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=OpenAIEmbedding(model="text-embedding-3-large"),
        show_progress=True,
    )

# 4. Create query engine with reranking
reranker = CohereRerank(api_key=os.getenv("COHERE_API_KEY"), top_n=3)

query_engine = index.as_query_engine(
    similarity_top_k=10,
    node_postprocessors=[reranker],
    response_mode="compact",
)

# 5. Query with citations
response = query_engine.query("Complex question")
answer_with_citations = format_response_with_citations(response)

# Time to build: 4-6 weeks
# Cost: $200-500/month (medium dataset)
```

### Enterprise RAG (Hybrid + Evaluation)
```
Architecture:
┌────────────────┐
│   API Gateway  │
└────────┬───────┘
         │
┌────────▼───────────────┐
│   FastAPI Service      │
│  - Rate limiting       │
│  - Caching (Redis)     │
└────────┬───────────────┘
         │
┌────────▼───────────────┐
│  Haystack Pipeline     │
│  - BM25 Retriever      │
│  - Embedding Retriever │
│  - Hybrid Joiner       │
│  - Reranker            │
│  - PromptBuilder       │
└────────┬───────────────┘
         │
┌────────▼───────┬─────────────┐
│   Weaviate     │  PostgreSQL │
│  (vectors)     │  (metadata) │
└────────────────┴─────────────┘

Monitoring:
- Prometheus + Grafana
- Custom metrics (latency, accuracy, cost)
- LangSmith or Langfuse for tracing

Time to build: 10-16 weeks
Cost: $1000-3000/month (large dataset, high traffic)
```

## Cost Optimization

### Embedding Costs for Large Corpora
```python
# Example: 10,000 documents, avg 5 pages, 500 tokens/page
total_tokens = 10000 * 5 * 500  # = 25M tokens

# Cost comparison
openai_large_cost = (25 / 1) * 0.13      # = $3.25
openai_small_cost = (25 / 1) * 0.02      # = $0.50
cohere_cost = (25 / 1) * 0.10             # = $2.50
local_cost = 0  # + compute costs

# One-time embedding cost: $0.50-$3.25
```

### Query Costs
```python
# Per query cost
retrieval_cost = 0  # Vector search is cheap
reranking_cost = 0.002  # Cohere rerank: ~$0.002/query
llm_cost = 0.015        # GPT-4: ~500 tokens @ $0.03/1K

total_per_query = 0.017  # ~$0.02 per query

# For 10K queries/month
monthly_cost = 10000 * 0.017  # = $170
```

### Optimization Strategies
1. **Cache frequent queries**: Save 60-80% on repeat questions
2. **Use smaller embedding models**: 10x cost reduction (small vs large)
3. **Batch embedding**: Process documents in batches
4. **Selective reranking**: Only rerank when needed (complex queries)
5. **Use GPT-4o-mini**: 60% cheaper than GPT-4 for simple RAG

## Common Pitfalls

1. **Poor chunking**: Too large (loses precision) or too small (loses context)
2. **Wrong embedding model**: Using task-specific models for general search
3. **No reranking**: Precision suffers for complex queries
4. **Ignoring metadata**: Filters can dramatically improve relevance
5. **No evaluation**: Can't measure if retrieval quality improves
6. **Over-retrieving**: Retrieving 50 chunks when 5 would do (cost & latency)
7. **No caching**: Repeated queries are expensive

## Best Practices

1. **Start with LlamaIndex for RAG specialization**
2. **Use semantic chunking for better quality**
3. **Implement reranking for high-value queries**
4. **Always track source attribution**
5. **Build evaluation dataset (50-100 Q&A pairs)**
6. **Monitor retrieval metrics** (precision@k, recall@k, MRR)
7. **Cache common queries** (Redis with 1-hour TTL)
8. **Use hybrid search for keyword-heavy domains**
9. **Implement incremental indexing for updates**
10. **Test with production-like document volumes**

## Summary

**For RAG applications, choose:**
- **LlamaIndex** if accuracy is paramount (35% better retrieval)
- **Haystack** if production performance + RAG both critical
- **LangChain** only if RAG is one of many features

**Time to production: 3-16 weeks depending on scale**
**Cost: $100-3000/month depending on corpus size and query volume**

**Critical success factors**:
1. Quality chunking strategy
2. Appropriate embedding model
3. Reranking for precision
4. Source attribution
5. Evaluation metrics
