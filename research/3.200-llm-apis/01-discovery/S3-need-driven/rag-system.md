# RAG System (Knowledge Base): LLM API Provider Selection

**Experiment**: 3.200 LLM APIs
**Stage**: S3 - Need-Driven Analysis
**Use Case**: RAG-Powered Knowledge Base
**Date**: November 5, 2025

---

## 1. Scenario Profile

### Use Case Description
A Retrieval-Augmented Generation (RAG) system for an enterprise knowledge base, enabling employees to ask questions and receive accurate answers grounded in internal documentation, policies, procedures, and historical records. The system combines semantic search (embeddings), result reranking, and LLM generation to provide contextual, citation-backed responses.

### Volume Characteristics
- **Queries per day**: 1,000 employee queries
- **Monthly queries**: 30,000 (1,000 × 30 days)
- **Embeddings**:
  - Initial indexing: 100M tokens (one-time)
  - Monthly updates: 10M tokens (new/updated docs)
- **Reranking**: 30,000 searches/month (1 per query)
- **LLM generation**:
  - 5M tokens/month (2.5M input context, 2.5M output answers)
- **Growth rate**: 25% YoY (employee growth + knowledge base expansion)
- **Query patterns**: Business hours (9 AM - 6 PM), peaks during onboarding weeks

### Quality Requirements
- **Embeddings**: Best-in-class semantic search (Cohere Embed v3 MTEB leader)
- **Reranking**: High precision (Cohere Rerank v3 industry standard)
- **Generation**: Mid-range acceptable (75-85% MMLU sufficient for fact retrieval)
- **Citation accuracy**: Must cite source documents accurately
- **Error tolerance**: Medium (wrong answer frustrates users but not catastrophic)
- **Hallucination risk**: High concern (must ground answers in retrieved docs only)

### Context Requirements
- **System prompt**: 500-1,000 tokens (answer format, citation guidelines)
- **Retrieved context**: 5,000-10,000 tokens (top 5-10 documents)
- **User query**: 50-200 tokens
- **Total context**: Medium-Large (5K-10K tokens per request)
- **Context stability**: High (system prompt stable, retrieved docs semi-stable)

### Latency Requirements
- **Target**: Interactive (<2 seconds total response time)
- **Embedding latency**: <100ms (for query embedding)
- **Reranking latency**: <200ms (rank top 100 results)
- **LLM generation TTFT**: <500ms
- **Total pipeline**: <2s (embedding → search → rerank → generate)
- **User expectation**: Search-like responsiveness

### Budget Constraints
- **Tier**: Moderate ($5,000-$50,000/month)
- **Year 1 target**: <$10,000/month
- **Year 3 target**: <$20,000/month (with 25% YoY growth)
- **Cost per query**: Target <$0.50
- **Sensitivity**: Medium (productivity tool, ROI from time saved finding answers)

### Compliance Requirements
- **Level**: SOC 2 preferred (internal company data)
- **Data retention**: 0-day preferred (protect proprietary knowledge)
- **Privacy**: Never train on customer data (confidential company information)
- **Geographic**: US-based, no specific data residency requirements
- **Certifications**: SOC 2 preferred for enterprise deployment

---

## 2. Requirements Matrix

| Requirement | Priority | Threshold | Impact on Selection |
|-------------|----------|-----------|---------------------|
| **Embedding Quality** | Critical | MTEB top-10 | Cohere Embed v3 (leader), OpenAI text-embedding-3 (runner-up) |
| **Reranking Capability** | Critical | NDCG@10 >0.7 | Cohere Rerank v3 (best), Voyage Rerank (alternative) |
| **Generation Quality** | Medium | >75% MMLU | Many options: Gemini Flash, Claude Haiku, GPT-3.5 |
| **Cost** | High | <$0.50/query | Reranking dominates (90% of cost); optimize reranking first |
| **Latency** | High | <2s total | Fast embeddings (<100ms) + fast generation (<500ms TTFT) |
| **Citation Accuracy** | Critical | >95% correct sources | All frontier models capable; test in evaluation |
| **Data Retention** | High | 0-day preferred | Cohere, Anthropic, Google Vertex (opt-in) |

### Derived Requirements
1. **Complete RAG stack critical**: Need embeddings + reranking + generation → Cohere offers all three
2. **Reranking cost dominates**: $2/1K searches × 30K searches = $60/month (56-90% of total RAG cost)
3. **Embedding quality non-negotiable**: Poor embeddings → irrelevant search results → LLM can't help
4. **Generation is smallest cost**: Only 10-44% of total RAG cost → Not primary optimization target
5. **Latency budget tight**: 2s total = 100ms embedding + 200ms rerank + 500ms TTFT + 1200ms generation

---

## 3. Provider Shortlist (Decision Tree)

### Step 1: Filter by RAG Stack Completeness
**Required**: Embeddings + Reranking + Generation (or can mix providers)

| Provider | Embeddings | Reranking | Generation | Complete Stack? |
|----------|-----------|-----------|------------|----------------|
| Cohere | Embed v3 (MTEB #1) | Rerank v3 (best) | Command R+ | Yes (complete) |
| OpenAI | text-embedding-3 (#2) | No | GPT-4o, GPT-3.5 | Partial (no rerank) |
| Google | text-embedding-004 | No (in development) | Gemini Pro, Flash | Partial (no rerank) |
| Anthropic | No | No | Claude Sonnet | Partial (gen only) |
| Voyage | voyage-2 | voyage-rerank-1 | No | Partial (no gen) |

**Result**: Only Cohere offers complete stack; others require mixing providers

### Step 2: Evaluate Hybrid Stacks
**Option 1: Cohere Complete Stack**
- Embeddings: Cohere Embed v3 ($0.10/M)
- Reranking: Cohere Rerank v3 ($2/1K searches)
- Generation: Cohere Command R+ ($3/$15 per M)

**Option 2: OpenAI Embeddings + Cohere Rerank + OpenAI Generation**
- Embeddings: OpenAI text-embedding-3 ($0.13/M)
- Reranking: Cohere Rerank v3 ($2/1K searches)
- Generation: OpenAI GPT-4o ($5/$15 per M)

**Option 3: Google Embeddings (free) + Cohere Rerank + Google Generation**
- Embeddings: Google text-embedding-004 (free tier)
- Reranking: Cohere Rerank v3 ($2/1K searches)
- Generation: Google Gemini Flash ($0.075/$0.30 per M)

**Option 4: Cohere Embed + Cohere Rerank + Anthropic Generation (cached)**
- Embeddings: Cohere Embed v3 ($0.10/M)
- Reranking: Cohere Rerank v3 ($2/1K searches)
- Generation: Anthropic Claude Sonnet cached ($0.30/$15 per M for cached)

### Step 3: Cost Comparison (Year 1)

**Assumptions**:
- Embeddings: 120M tokens Year 1 (100M initial + 10M monthly × 12)
- Reranking: 30,000 searches/month × 12 = 360,000 searches/year
- Generation: 30M input, 30M output/year

| Stack | Embeddings | Reranking | Generation | Year 1 Total |
|-------|-----------|-----------|------------|--------------|
| **Cohere Complete** | $12 | $720 | $540 | **$1,272** |
| **OpenAI + Cohere + OpenAI** | $15.60 | $720 | $600 | **$1,335.60** |
| **Google + Cohere + Google** | $0 | $720 | $78.75 | **$798.75** |
| **Cohere + Cohere + Claude** | $12 | $720 | $126.90 | **$858.90** |

### Step 4: Rank by Cost-Quality Score

Quality score: (Embedding MTEB + Reranking NDCG + Generation MMLU) / 3
Cost score: Year 1 total cost

Composite: Quality / Cost

| Stack | Embedding | Reranking | Generation | Avg Quality | Year 1 Cost | Quality/Cost | Rank |
|-------|-----------|-----------|------------|-------------|-------------|--------------|------|
| **Google + Cohere + Google** | 90 | 95 | 78.9 | 87.97 | $798.75 | **0.110** | 1 |
| **Cohere + Cohere + Claude** | 100 | 95 | 88.7 | 94.57 | $858.90 | **0.110** | 2 |
| **Cohere Complete** | 100 | 95 | 75.0 | 90.0 | $1,272 | **0.071** | 3 |
| **OpenAI + Cohere + OpenAI** | 95 | 95 | 88.0 | 92.67 | $1,335.60 | **0.069** | 4 |

### Final Shortlist (Top 3)
1. **Google Embeddings + Cohere Rerank + Gemini Flash**: Cheapest ($798.75), excellent quality
2. **Cohere Embed + Cohere Rerank + Claude Sonnet (cached)**: Best quality (94.57), moderate cost
3. **Cohere Complete Stack**: Single-vendor simplicity, best-in-class embeddings

---

## 4. Recommended Provider(s)

### Primary Choice: Cohere Complete Stack (Embed v3 + Rerank v3 + Command R+)

**Rationale**:
- **Single-vendor simplicity**: No multi-provider integration complexity
- **Best embeddings**: Cohere Embed v3 tops MTEB leaderboard (semantic search leader)
- **Best reranking**: Cohere Rerank v3 industry standard (NDCG@10 >0.85)
- **Optimized RAG pipeline**: All components trained to work together
- **Good generation**: Command R+ 75% MMLU (sufficient for fact retrieval)
- **Built for RAG**: Cohere's entire product focused on enterprise search/RAG
- **99.9% uptime**: Strong reliability
- **SOC 2 certified**: Enterprise compliance
- **Dedicated support**: Enterprise tier includes RAG optimization consulting

**Monthly Cost (Year 1)**:
- Embeddings: $1/month (initial spike, then $0.83/month ongoing)
- Reranking: $60/month
- Generation: $45/month
- **Total**: $106/month ($1,272/year)

**3-Year TCO**: $3,758.25

**Cost per query**: $0.0424 (Year 1)

**Trade-off**: 13-point MMLU gap vs. Claude/GPT-4o (75% vs. 88%), but sufficient for fact retrieval

### Runner-Up: Google Embeddings (free) + Cohere Rerank + Gemini Flash

**Rationale**:
- **Cheapest**: $798.75 Year 1 (37% cheaper than Cohere complete)
- **Free embeddings**: Google text-embedding-004 free tier eliminates largest one-time cost
- **Best reranking**: Cohere Rerank v3 (same as primary choice)
- **Excellent generation**: Gemini Flash 78.9% MMLU (better than Cohere Command R+ 75%)
- **Fast generation**: 400ms TTFT
- **99.9% uptime + SLA**: Best reliability

**Monthly Cost (Year 1)**: $66.56/month ($799/year)
**3-Year TCO**: $2,555.77

**Trade-off**: Multi-provider complexity (3 vendors vs. 1), integration overhead

### Premium Option: Cohere Embed + Cohere Rerank + Anthropic Claude Sonnet (cached)

**Rationale**:
- **Best generation quality**: Claude Sonnet 88.7% MMLU (highest)
- **Excellent explanations**: Best at synthesizing retrieved docs into coherent answers
- **Prompt caching ROI**: System prompt + retrieved docs semi-stable → 80% cache hit rate
  - Reduces generation cost 70%: $540 → $126.90/year
- **200K context**: Fits many retrieved docs (5-10K tokens) comfortably
- **Citation quality**: Excellent at citing specific sources

**Monthly Cost (Year 1)**: $71.58/month ($859/year)
**3-Year TCO**: $2,586.48

**Trade-off**: Multi-provider complexity (2 vendors), slightly more expensive than Google hybrid

### Budget Option: Google Free Tier Complete

**Rationale**:
- **Zero embeddings cost**: Google text-embedding-004 free tier
- **Skip reranking**: Use embeddings only (semantic search without reranking)
- **Cheapest generation**: Gemini Flash
- **Free tier limits**: 1,500 requests/day embeddings (sufficient for 1,000 queries/day)

**Monthly Cost (Year 1)**: $6.56/month ($79/year) - generation only
**3-Year TCO**: $237.21

**Trade-off**: No reranking → 20-30% lower search precision → more irrelevant results

---

## 5. Architecture Pattern

### Recommended: Cohere Complete RAG Stack

```
User Query: "What is our return policy for enterprise customers?"
    ↓
┌──────────────────────────────────────────────┐
│ Step 1: Query Embedding                      │
│ Cohere Embed v3                              │
│ - Input: "What is our return policy..."     │
│ - Output: 1024-dim vector                    │
│ - Latency: <50ms                             │
│ - Cost: $0.10 per 1M tokens (negligible)     │
└──────────────────────────────────────────────┘
    ↓
┌──────────────────────────────────────────────┐
│ Step 2: Vector Search (External)            │
│ Pinecone / Weaviate / Qdrant                 │
│ - Input: Query vector                        │
│ - Output: Top 100 candidate documents       │
│ - Latency: <100ms                            │
│ - Cost: $70/month (vector DB hosting)       │
└──────────────────────────────────────────────┘
    ↓
┌──────────────────────────────────────────────┐
│ Step 3: Reranking                            │
│ Cohere Rerank v3                             │
│ - Input: Query + 100 candidates              │
│ - Output: Top 5 documents (scored)           │
│ - Latency: <200ms                            │
│ - Cost: $2 per 1K searches ($60/month)       │
└──────────────────────────────────────────────┘
    ↓
┌──────────────────────────────────────────────┐
│ Step 4: Context Assembly                    │
│ - Combine top 5 docs (~5-10K tokens)        │
│ - Add metadata (doc title, last updated)    │
│ - Truncate if exceeds context limit         │
└──────────────────────────────────────────────┘
    ↓
┌──────────────────────────────────────────────┐
│ Step 5: Answer Generation                    │
│ Cohere Command R+                            │
│ - Input: Query + Context (5-10K tokens)     │
│ - Output: Answer with citations (200 tokens) │
│ - Latency: <1s                               │
│ - Cost: $3/$15 per M tokens ($45/month)      │
└──────────────────────────────────────────────┘
    ↓
Response: "For enterprise customers, our return policy allows
returns within 90 days of purchase... [Citation: Enterprise
Sales Policy v2.3, Section 4.2]"
```

**Total Latency**: 50ms (embed) + 100ms (search) + 200ms (rerank) + 1000ms (generate) = **1.35s**

**Total Cost per Query**: $0.0424 (Year 1 average)

**Why Cohere Complete?**
1. **Single-vendor simplicity**: One API, one billing, one support contract
2. **Optimized integration**: Components trained to work together (embed → rerank → generate)
3. **Best embeddings + reranking**: Industry-leading semantic search quality
4. **RAG-specific features**: Grounded generation (cite sources), connectors (Google Drive, Confluence)
5. **Enterprise support**: Dedicated RAG optimization consulting

### Alternative 1: Google Hybrid (Cost-Optimized)

**When to use**: Budget-constrained, free embeddings tier sufficient

```
User Query
    ↓
Google text-embedding-004 (FREE)
    ↓
Vector Search (Pinecone/Weaviate)
    ↓
Cohere Rerank v3 ($2/1K)
    ↓
Google Gemini Flash ($0.075/$0.30 per M)
    ↓
Response with Citations
```

**Pros**:
- **37% cheaper**: $799/year vs. $1,272 (Cohere complete)
- **Better generation**: Gemini Flash 78.9% MMLU vs. Command R+ 75%
- **Free embeddings**: Zero cost for embedding step

**Cons**:
- **Multi-provider complexity**: 3 vendors (Google, Cohere, Pinecone)
- **Integration overhead**: Manage 3 API keys, 3 billing systems
- **No optimization**: Components not trained together

**Cost**: $2,555.77 (3-year TCO)

### Alternative 2: Claude Premium (Quality-Focused)

**When to use**: Quality paramount, budget less constrained

```
User Query
    ↓
Cohere Embed v3 ($0.10/M)
    ↓
Vector Search
    ↓
Cohere Rerank v3 ($2/1K)
    ↓
Anthropic Claude Sonnet (cached) ($0.30/$15 per M)
    ↓
High-Quality Response with Citations
```

**Pros**:
- **Best generation**: Claude Sonnet 88.7% MMLU (13 points better than Command R+)
- **Excellent citations**: Best at attributing facts to specific sources
- **Prompt caching**: 70% cost reduction on generation (system prompt + context cached)

**Cons**:
- **Multi-provider**: 2 vendors (Cohere, Anthropic)
- **Slightly more expensive**: $859/year vs. $799 (Google hybrid)

**Cost**: $2,586.48 (3-year TCO)

---

## 6. Implementation Guide

### API Setup (Cohere Complete Stack Primary Recommendation)

#### Step 1: Create Cohere Account & Get API Keys (15 minutes)
```bash
# Visit: https://dashboard.cohere.com/
# Sign up with business email
# Navigate to API Keys section
# Generate production API keys (separate keys for embed, rerank, generate)
# Store in secure secrets manager
```

#### Step 2: Install SDKs (5 minutes)
```bash
# Python
pip install cohere pinecone-client  # Cohere + vector DB

# JavaScript/TypeScript
npm install cohere-ai @pinecone-database/pinecone
```

#### Step 3: Set Up Vector Database (2 hours)
```python
import pinecone
from pinecone import ServerlessSpec

# Initialize Pinecone
pinecone.init(api_key="your-pinecone-api-key")

# Create index for Cohere Embed v3 (1024 dimensions)
index_name = "company-knowledge-base"

if index_name not in pinecone.list_indexes():
    pinecone.create_index(
        name=index_name,
        dimension=1024,  # Cohere Embed v3 dimension
        metric="cosine",  # Cosine similarity for semantic search
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

index = pinecone.Index(index_name)
```

#### Step 4: Embed and Index Documents (4-6 hours)
```python
import cohere
import os
from pathlib import Path

co = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))

def load_documents(docs_dir):
    """Load all documents from directory"""
    documents = []
    for filepath in Path(docs_dir).rglob("*.txt"):
        with open(filepath, 'r') as f:
            documents.append({
                "id": str(filepath),
                "text": f.read(),
                "metadata": {
                    "source": filepath.name,
                    "last_updated": filepath.stat().st_mtime
                }
            })
    return documents

def embed_and_index(documents, batch_size=96):
    """Embed documents and index in Pinecone"""

    # Cohere Embed API has batch limit of 96
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        texts = [doc["text"] for doc in batch]

        # Generate embeddings
        response = co.embed(
            texts=texts,
            model="embed-english-v3.0",  # Cohere Embed v3
            input_type="search_document"  # Optimize for indexing
        )

        # Prepare vectors for Pinecone
        vectors = []
        for j, doc in enumerate(batch):
            vectors.append({
                "id": doc["id"],
                "values": response.embeddings[j],
                "metadata": {
                    "text": doc["text"][:1000],  # Store preview (Pinecone metadata limit)
                    "source": doc["metadata"]["source"]
                }
            })

        # Upsert to Pinecone
        index.upsert(vectors=vectors)

        print(f"Indexed {i + len(batch)}/{len(documents)} documents")

# Usage
documents = load_documents("./company-docs")
embed_and_index(documents)
print(f"Indexed {len(documents)} documents")
```

#### Step 5: Implement RAG Query Pipeline (3-4 hours)
```python
class RAGPipeline:
    def __init__(self, cohere_api_key, pinecone_index_name):
        self.co = cohere.Client(api_key=cohere_api_key)
        self.index = pinecone.Index(pinecone_index_name)

    def query(self, question, top_k=5):
        """
        Execute full RAG pipeline

        Args:
            question: User's question
            top_k: Number of documents to retrieve

        Returns:
            dict with answer, sources, and metadata
        """

        # Step 1: Embed query
        query_embedding = self.co.embed(
            texts=[question],
            model="embed-english-v3.0",
            input_type="search_query"  # Optimize for search
        ).embeddings[0]

        # Step 2: Vector search (retrieve top 100 candidates)
        search_results = self.index.query(
            vector=query_embedding,
            top_k=100,
            include_metadata=True
        )

        # Extract candidates
        candidates = [
            {
                "text": match.metadata["text"],
                "source": match.metadata["source"],
                "score": match.score
            }
            for match in search_results.matches
        ]

        # Step 3: Rerank to get top K
        rerank_response = self.co.rerank(
            query=question,
            documents=[c["text"] for c in candidates],
            model="rerank-english-v3.0",
            top_n=top_k
        )

        # Get top documents after reranking
        top_docs = [candidates[result.index] for result in rerank_response.results]

        # Step 4: Assemble context
        context = "\n\n---\n\n".join([
            f"Source: {doc['source']}\n{doc['text']}"
            for doc in top_docs
        ])

        # Step 5: Generate answer with Cohere
        generation_response = self.co.chat(
            message=question,
            documents=[{"text": doc["text"], "id": doc["source"]} for doc in top_docs],
            model="command-r-plus",
            temperature=0.3,  # Lower temp for factual responses
            prompt_truncation="AUTO"  # Truncate if context too long
        )

        # Extract citations
        citations = []
        if generation_response.citations:
            for citation in generation_response.citations:
                citations.append({
                    "source": citation.document_ids[0],
                    "text": citation.text
                })

        return {
            "answer": generation_response.text,
            "sources": [doc["source"] for doc in top_docs],
            "citations": citations,
            "latency": {
                "total": "calculated externally"
            }
        }

# Usage
pipeline = RAGPipeline(
    cohere_api_key=os.getenv("COHERE_API_KEY"),
    pinecone_index_name="company-knowledge-base"
)

result = pipeline.query("What is our return policy for enterprise customers?")

print("Answer:", result["answer"])
print("\nSources:")
for source in result["sources"]:
    print(f"  - {source}")
print("\nCitations:")
for citation in result["citations"]:
    print(f"  [{citation['source']}]: {citation['text']}")
```

### Prompt Engineering (RAG-Specific)

#### System Prompt for Grounded Generation
```python
SYSTEM_PROMPT = """You are a helpful assistant answering questions about company policies and procedures.

IMPORTANT RULES:
1. ONLY use information from the provided context documents
2. If the answer is not in the context, say "I don't have information about that in the knowledge base"
3. ALWAYS cite your sources using [Source: document_name]
4. If multiple sources provide conflicting information, mention the conflict
5. Be concise but complete - aim for 2-3 paragraph answers
6. Use bullet points for lists or step-by-step instructions

ANSWER FORMAT:
[Direct answer to the question]

[Supporting details with citations]

Sources:
- [List all sources used]
"""
```

#### Citation Enforcement
```python
def generate_with_citations(question, context_docs):
    """Generate answer with enforced citation"""

    # Format documents with IDs
    documents = [
        {
            "id": f"doc_{i}",
            "text": f"[Source: {doc['source']}]\n{doc['text']}"
        }
        for i, doc in enumerate(context_docs)
    ]

    response = co.chat(
        message=f"""{SYSTEM_PROMPT}

Question: {question}

Context Documents:
{documents}

Provide a complete answer with citations.""",
        documents=documents,
        model="command-r-plus",
        temperature=0.3,
        citation_quality="accurate"  # Cohere-specific parameter
    )

    return response
```

### Quality Assurance

#### Evaluation Metrics
```python
def evaluate_rag_quality(test_questions):
    """Evaluate RAG system on test questions"""

    metrics = {
        "retrieval_accuracy": [],  # % of relevant docs in top K
        "answer_accuracy": [],  # Human rating 1-5
        "citation_accuracy": [],  # % of citations pointing to correct docs
        "latency": []
    }

    for q in test_questions:
        result = pipeline.query(q["question"])

        # Retrieval accuracy
        relevant_docs = set(q["expected_sources"])
        retrieved_docs = set(result["sources"])
        retrieval_acc = len(relevant_docs & retrieved_docs) / len(relevant_docs)
        metrics["retrieval_accuracy"].append(retrieval_acc)

        # Citation accuracy (automated check)
        citation_acc = verify_citations(result["answer"], result["citations"])
        metrics["citation_accuracy"].append(citation_acc)

        # Latency
        metrics["latency"].append(result["latency"]["total"])

    # Print summary
    print(f"Retrieval Accuracy: {np.mean(metrics['retrieval_accuracy']):.1%}")
    print(f"Citation Accuracy: {np.mean(metrics['citation_accuracy']):.1%}")
    print(f"Avg Latency: {np.mean(metrics['latency']):.2f}s")

    return metrics
```

---

## 7. Cost Breakdown (3-Year TCO)

### Recommended Stack: Cohere Complete (Embed v3 + Rerank v3 + Command R+)

#### Volume Projections (25% YoY Growth)
| Year | Monthly Queries | Annual Queries | Annual Embeddings | Annual Reranks | LLM Input | LLM Output |
|------|----------------|----------------|-------------------|----------------|-----------|------------|
| Year 1 | 30,000 | 360,000 | 220M (100M initial + 120M updates) | 360K | 30M | 30M |
| Year 2 | 37,500 | 450,000 | 150M (updates only) | 450K | 37.5M | 37.5M |
| Year 3 | 46,875 | 562,500 | 187.5M (updates only) | 562.5K | 46.875M | 46.875M |
| **3-Year Total** | - | **1,372,500** | **557.5M** | **1,372.5K** | **114.375M** | **114.375M** |

#### Cost Calculations

**Embeddings (Cohere Embed v3: $0.10/M)**:
- Year 1: 220M × $0.10/M = $22
- Year 2: 150M × $0.10/M = $15
- Year 3: 187.5M × $0.10/M = $18.75
- **Subtotal (3-year)**: $55.75

**Reranking (Cohere Rerank v3: $2.00/1K searches)**:
- Year 1: 360K × $2/1K = $720
- Year 2: 450K × $2/1K = $900
- Year 3: 562.5K × $2/1K = $1,125
- **Subtotal (3-year)**: $2,745

**Generation (Cohere Command R+: $3/$15 per M)**:
- Year 1: (30M × $3/M) + (30M × $15/M) = $90 + $450 = $540
- Year 2: (37.5M × $3/M) + (37.5M × $15/M) = $675
- Year 3: (46.875M × $3/M) + (46.875M × $15/M) = $843.75
- **Subtotal (3-year)**: $2,058.75

**Total 3-Year TCO**: $4,859.50
- **Average monthly cost**: $135.54
- **Cost per query**: $0.0354 (3-year average)

**Cost Breakdown by Component**:
- Embeddings: 1.1% of total cost
- Reranking: **56.5% of total cost** ← Dominates
- Generation: 42.4% of total cost

### Cost Comparison: Alternative Stacks

| Stack | Embeddings | Reranking | Generation | Year 1 | Year 2 | Year 3 | 3-Year Total |
|-------|-----------|-----------|------------|--------|--------|--------|--------------|
| **Google + Cohere + Google** | $0 | $720 | $78.75 | **$798.75** | $998.44 | $1,248.05 | **$3,045.23** |
| **Cohere + Cohere + Claude** | $22 | $720 | $126.90 | **$868.90** | $1,078.13 | $1,347.66 | **$3,294.69** |
| **Cohere Complete** | $22 | $720 | $540 | **$1,282** | $1,590 | $1,987.50 | **$4,859.50** |
| **OpenAI + Cohere + OpenAI** | $28.60 | $720 | $600 | **$1,348.60** | $1,669.50 | $2,086.88 | **$5,104.98** |

### Reranking Cost Dominance Analysis

**Reranking as % of Total Cost**:
| Stack | Reranking Cost (3-year) | Total Cost (3-year) | Reranking % |
|-------|------------------------|---------------------|-------------|
| Google + Cohere + Google | $2,745 | $3,045 | **90.1%** |
| Cohere + Cohere + Claude | $2,745 | $3,295 | **83.3%** |
| Cohere Complete | $2,745 | $4,860 | **56.5%** |
| OpenAI + Cohere + OpenAI | $2,745 | $5,105 | **53.8%** |

**Key Insight**: Reranking dominates cost in all stacks (54-90%). Optimizing reranking is critical.

### Savings Opportunities

#### 1. Reduce Reranking Frequency (Aggressive Optimization)
- **Current**: Rerank 100 candidates for every query
- **Potential**: Rerank only if initial search confidence <0.8 (50% of queries)
  - Reranking volume: 360K → 180K searches/year
  - **Savings**: $360/year (50% reduction) = **$1,080 over 3 years**

**Trade-off**: 5-10% lower precision on 50% of queries (acceptable if initial search good)

#### 2. Reduce Reranking Candidates (Cost vs. Quality)
- **Current**: Rerank top 100 candidates → top 5
- **Potential**: Rerank top 20 candidates → top 5 (80% cost reduction)
  - Cohere charges per candidate reranked
  - **Savings**: Depends on Cohere's per-candidate pricing (not public)

**How**: Set `top_n` parameter in rerank API

#### 3. Use Cheaper Generation Model
- **Current**: Cohere Command R+ ($3/$15 per M)
- **Potential**: Gemini Flash ($0.075/$0.30 per M) = 95% cheaper on output
  - Generation cost: $540/year → $78.75/year
  - **Savings**: $461.25/year = **$1,384 over 3 years**

**Implementation**: Hybrid stack (Cohere embed/rerank + Gemini Flash generation)

#### 4. Cache Retrieved Context (Anthropic)
- **Current**: No caching
- **Potential**: Use Claude with prompt caching for generation step
  - Retrieved context (5-10K tokens) semi-stable across similar queries
  - 70% cost reduction on cached portion
  - **Savings**: $284/year = **$852 over 3 years**

### Hidden Costs (Infrastructure)

| Cost Component | Estimate | Notes |
|---------------|----------|-------|
| **Vector database** (Pinecone) | $70-300/month | 100M vectors × $0.001-0.003 per 1K vectors |
| **Embeddings storage** | $20-50/month | S3 for document storage |
| **Monitoring/observability** | $50-200/month | Datadog, CloudWatch for latency tracking |
| **Development time** | 120-160 hours | Initial implementation ($18K-24K at $150/hour) |
| **Ongoing maintenance** | 20 hours/month | Knowledge base updates, prompt tuning ($3K/month) |

**Total hidden costs (Year 1)**: $24K (one-time) + $36K (ongoing) = **$60K**

**Important**: Infrastructure costs (vector DB, maintenance) exceed API costs. Budget accordingly.

---

## 8. Migration Path (From ElasticSearch / Algolia Keyword Search)

### Assumption: Currently Using ElasticSearch for Knowledge Base
Many enterprises use keyword search (ElasticSearch, Algolia) for internal knowledge bases.

**Current Limitations**:
- Keyword matching only (no semantic understanding)
- Synonyms require manual configuration
- No answer generation (returns docs, user must read)

**Recommended Target**: Cohere Complete RAG Stack

**Improvement**: Semantic search + reranking + answer generation = 10× better user experience

### Migration Steps

#### Phase 1: Evaluation (Week 1-2, 24 hours)

**Step 1: Create Cohere account, get API keys** (2 hours)

**Step 2: Side-by-side quality testing** (12 hours)
- Select 50 diverse employee queries from search logs
- Run through both ElasticSearch (keyword) and Cohere RAG (semantic)
- Human evaluation: Rate relevance 1-5 stars for top 5 results
- Measure: Precision@5, NDCG@5, answer quality

**Step 3: Cost modeling** (4 hours)
- Analyze query volume from ElasticSearch logs
- Estimate tokens for embeddings (document corpus size)
- Model 3-year TCO with 25% YoY growth
- Compare to ElasticSearch hosting costs ($500-2K/month)

**Step 4: Latency testing** (4 hours)
- Measure end-to-end latency for RAG pipeline
- Compare to ElasticSearch (<100ms keyword search)
- Determine if 1.5-2s acceptable for semantic search + answer

**Step 5: Go/No-Go Decision** (2 hours)
- Quality improvement validated? (Target: +30% precision vs. keyword search)
- Latency acceptable? (1.5-2s vs. 100ms)
- Cost acceptable? ($1,272/year RAG vs. $6K-24K/year ElasticSearch cluster)

#### Phase 2: Implementation (Week 3-4, 32 hours)

**Step 1: Set up vector database** (8 hours)
- Choose Pinecone, Weaviate, or Qdrant
- Create index with Cohere Embed v3 dimensions (1024)
- Configure metadata fields (source, last_updated, etc.)

**Step 2: Migrate documents** (12 hours)
```python
# Export from ElasticSearch
from elasticsearch import Elasticsearch

es = Elasticsearch(["http://localhost:9200"])
docs = []

# Scroll through all docs
for hit in es.search(index="knowledge-base", scroll="5m", size=1000):
    docs.append({
        "id": hit["_id"],
        "text": hit["_source"]["content"],
        "metadata": hit["_source"]["metadata"]
    })

# Embed and index in Pinecone (see Implementation Guide Section 6)
embed_and_index(docs)
```

**Step 3: Implement RAG pipeline** (8 hours)
- See Implementation Guide Section 6 for full code
- Integrate Cohere embed → Pinecone search → Cohere rerank → Cohere generate

**Step 4: Testing** (4 hours)
- Run full test suite (50 queries)
- Validate answer quality, citation accuracy
- Load testing (1,000 concurrent queries)

#### Phase 3: Staged Rollout (Week 5-6, 16 hours)

**Step 1: Internal beta (10% of employees)** (Week 5)
- Deploy RAG system to 10% of employees
- Monitor usage, collect feedback
- Compare query satisfaction vs. ElasticSearch

**Step 2: Expand to 50%** (Week 6)
- If beta successful, expand to 50% of employees
- A/B test: 50% use RAG, 50% use ElasticSearch
- Measure: Query success rate, time to answer, user satisfaction

**Step 3: Full migration (100%)** (Week 6)
- If A/B test successful, migrate all users to RAG
- Keep ElasticSearch running for 30-day fallback period
- Decommission ElasticSearch after 30 days

#### Phase 4: Optimization (Week 7-8, 12 hours)

**Step 1: Optimize retrieval** (6 hours)
- Analyze low-precision queries (where top 5 docs not relevant)
- Tune reranking parameters (top_n, relevance threshold)
- Update document metadata for better filtering

**Step 2: Optimize generation** (4 hours)
- Analyze low-quality answers (user thumbs-down)
- Refine system prompt for better citations
- A/B test different generation models (Command R+ vs. Gemini Flash)

**Step 3: Cost optimization** (2 hours)
- Analyze per-query costs (embeddings, reranking, generation)
- Implement reranking optimization (skip if confidence high)
- Test cheaper generation model for simple queries

### Migration Effort Summary

| Phase | Duration | Effort | Key Activities |
|-------|----------|--------|----------------|
| **Phase 1: Evaluation** | 2 weeks | 24 hours | Side-by-side testing, cost modeling, latency testing |
| **Phase 2: Implementation** | 2 weeks | 32 hours | Vector DB setup, document migration, RAG pipeline |
| **Phase 3: Rollout** | 2 weeks | 16 hours | Beta (10%) → 50% → 100% staged migration |
| **Phase 4: Optimization** | 2 weeks | 12 hours | Retrieval tuning, generation optimization, cost tuning |
| **Total** | **8 weeks** | **84 hours** | $12,600 at $150/hour fully-loaded cost |

---

## 9. Risks & Mitigations

### Risk 1: Reranking Cost Explosion

**Severity**: Critical (5/5)

**Description**: Reranking dominates cost (56-90% of total). Volume growth or misuse can cause budget overruns.

**Impact**:
- 25% YoY query growth → reranking cost grows linearly
- If queries increase 100% (vs. planned 25%), reranking cost doubles
- Budget overrun: $2,745 (3-year planned) → $5,490 (if 100% growth)

**Mitigation**:
1. **Monthly cost monitoring**: Track reranking spend separately, alert if >10% variance
2. **Optimize reranking frequency**: Only rerank if initial search confidence <0.8 (50% savings)
3. **Reduce candidates**: Rerank top 20 (not 100) candidates → lower per-query cost
4. **Rate limiting**: Cap queries per user per day (prevent abuse)
5. **Caching**: Cache reranking results for duplicate queries (5-10% of queries are duplicates)

**Residual Risk**: Medium (3/5) - Monitoring + optimization mitigate but growth unpredictable

---

### Risk 2: Hallucinations (Answers Not Grounded in Docs)

**Severity**: High (4/5)

**Description**: LLM generates plausible-sounding answers not supported by retrieved documents.

**Impact**:
- Employees receive incorrect information (policy violations, wrong procedures)
- Damages trust in knowledge base system
- Legal/compliance risk if incorrect answers lead to violations

**Mitigation**:
1. **Grounded generation mode**: Use Cohere's `citation_quality="accurate"` parameter
2. **Citation enforcement**: Require citations for all facts, reject answers without citations
3. **Retrieved-only rule**: System prompt: "ONLY use information from provided documents"
4. **Human verification**: For critical queries (HR, legal, compliance), flag for human review
5. **Confidence scores**: Show LLM confidence, warn users on low-confidence answers

**Residual Risk**: Low (2/5) - Citation enforcement + grounded generation catch most hallucinations

---

### Risk 3: Poor Retrieval Quality (Irrelevant Docs)

**Severity**: High (4/5)

**Description**: Embedding/reranking returns irrelevant documents, LLM cannot generate good answer.

**Impact**:
- Precision@5 <50% → most retrieved docs not relevant
- LLM forced to synthesize from poor context → wrong or vague answers
- User frustration, abandons knowledge base

**Mitigation**:
1. **Embedding quality**: Use Cohere Embed v3 (MTEB leader) not weaker embeddings
2. **Reranking required**: Never skip reranking step (30% precision improvement)
3. **Document quality**: Clean, well-structured, up-to-date documents in knowledge base
4. **Metadata filtering**: Filter by doc type, department, date before semantic search
5. **Evaluation**: Monthly precision@5 testing on 100 random queries (target >70%)

**Residual Risk**: Low (2/5) - Cohere best-in-class embeddings + reranking mitigate

---

### Risk 4: Latency Regression (>2s Response Time)

**Severity**: Medium (3/5)

**Description**: RAG pipeline exceeds 2s latency target, users perceive as slow.

**Impact**:
- Poor user experience (frustration, abandonment)
- Lower adoption (users revert to keyword search or asking colleagues)
- Productivity loss (time wasted waiting)

**Mitigation**:
1. **Optimize each step**: Embedding <50ms, search <100ms, rerank <200ms, generate <1s
2. **Caching**: Cache query embeddings for popular queries (10% of queries account for 50% of volume)
3. **Parallel processing**: Run embedding + initial search in parallel where possible
4. **Index optimization**: Use Pinecone/Weaviate HNSW index for <100ms search
5. **Streaming**: Stream LLM generation (show partial answer as it generates)

**Residual Risk**: Low (2/5) - Optimization + streaming maintain <2s user experience

---

### Risk 5: Vendor Lock-In (Cohere-Specific)

**Severity**: Medium (3/5)

**Description**: Cohere-specific APIs (rerank v3, embed v3) create dependency.

**Impact**:
- Migration to another provider requires re-implementing embedding/reranking
- Embeddings incompatible (1024-dim Cohere vs. 1536-dim OpenAI)
- Reranking no direct equivalent (would need to rebuild or use Voyage Rerank)

**Mitigation**:
1. **Abstraction layer**: Provider-agnostic interface for embed/rerank/generate
2. **Multi-provider testing**: Quarterly test OpenAI embeddings + Voyage rerank
3. **Embeddings portability**: Store both Cohere and OpenAI embeddings (redundant but enables switching)
4. **Hybrid stack contingency**: Google embeddings (free) + Gemini Flash (cheap) as backup
5. **Contract terms**: Negotiate data export clause (can export embeddings if switching)

**Residual Risk**: Medium (3/5) - Abstraction layer reduces but doesn't eliminate lock-in

---

## 10. Success Metrics

### Cost Targets

| Metric | Target | Measurement | Alert Threshold |
|--------|--------|-------------|-----------------|
| **Monthly Spend (Year 1)** | <$500 | Actual API spend (embed + rerank + generate) | >$600 (20% over) |
| **Cost per Query** | <$0.05 | Total spend / queries | >$0.07 (40% over) |
| **Reranking Cost %** | <70% of total | Reranking spend / total spend | >80% (reranking dominance) |
| **3-Year TCO** | <$10,000 | Projected based on actual growth | On track vs. budget |

**How to Track**:
- Daily cost dashboard (Cohere Console for embed/rerank/generate)
- Weekly cost breakdown by component (embeddings, reranking, generation)
- Monthly review with IT leadership

---

### Quality Targets

| Metric | Target | Measurement | Alert Threshold |
|--------|--------|-------------|-----------------|
| **Precision@5** | >70% | % of top 5 retrieved docs relevant to query | <60% |
| **NDCG@5** | >0.75 | Normalized Discounted Cumulative Gain (ranking quality) | <0.65 |
| **Answer Accuracy** | >85% | Human rating 1-5 stars, % rated ≥4 | <75% |
| **Citation Accuracy** | >95% | % of citations pointing to correct source docs | <90% |
| **User Satisfaction** | >4.0/5.0 | Post-query rating: "Was this helpful?" | <3.5/5.0 |

**How to Track**:
- Weekly retrieval evaluation: 20 random queries, measure precision@5
- Monthly answer quality audit: 50 queries rated by experts
- Automated citation verification: Check all citations point to retrieved docs
- User feedback: Thumbs up/down + optional comment after each query

---

### Performance Targets

| Metric | Target | Measurement | Alert Threshold |
|--------|--------|-------------|-----------------|
| **Total Latency** | <2s | End-to-end (query → answer) | >3s |
| **Embedding Latency** | <50ms | Query embedding generation | >100ms |
| **Search Latency** | <100ms | Vector search in Pinecone | >200ms |
| **Reranking Latency** | <200ms | Cohere rerank API call | >500ms |
| **Generation TTFT** | <500ms | Time to first token from LLM | >1s |

**How to Track**:
- Measure latency for each pipeline step in application code
- Log all latencies to monitoring system (Datadog/CloudWatch)
- Daily latency dashboard with P50, P95, P99
- Alert if P95 >3s for >5 minutes

---

### Adoption Targets

| Metric | Target | Measurement | Alert Threshold |
|--------|--------|-------------|-----------------|
| **Daily Active Users** | >60% of employees | Users making ≥1 query/day | <40% (low adoption) |
| **Queries per User per Day** | >2 | Average queries per active user | <1 (underutilization) |
| **Query Success Rate** | >80% | % of queries resulting in thumbs-up or follow-up query | <70% |
| **Time to Answer** | <3 min | Time from query to finding answer (vs. 10-15 min manual search) | >5 min (not saving time) |

**How to Track**:
- User analytics: Daily active users, queries per user
- Success signals: Thumbs up, follow-up query (indicates found answer)
- Time savings survey: Monthly survey asking time saved per day

---

### Example Success Dashboard (Month 1)

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| **Monthly Spend** | <$500 | $428 | ✅ 14% under budget |
| **Cost per Query** | <$0.05 | $0.0424 | ✅ 15% under target |
| **Precision@5** | >70% | 74% | ✅ Exceeding target |
| **Answer Accuracy** | >85% | 87% | ✅ Exceeding target |
| **Citation Accuracy** | >95% | 96% | ✅ On target |
| **Total Latency (P95)** | <2s | 1.8s | ✅ On target |
| **User Satisfaction** | >4.0/5.0 | 4.3/5.0 | ✅ Exceeding target |
| **Daily Active Users** | >60% | 58% | ⚠️ Slightly below (adoption campaign needed) |

**Interpretation**: Most metrics green in Month 1. Quality and latency targets met. Adoption slightly low (58% vs. 60% target) - launch awareness campaign.

---

## Conclusion

### Recommended Implementation Summary

**Primary Provider**: Cohere Complete Stack (Embed v3 + Rerank v3 + Command R+)
**Alternative**: Google Embeddings (free) + Cohere Rerank + Gemini Flash (cost-optimized)
**Architecture**: Full RAG pipeline (embed → search → rerank → generate)

**Key Decision Factors**:
1. **Single-vendor simplicity**: Cohere offers complete RAG stack (embed, rerank, generate)
2. **Best embeddings**: Cohere Embed v3 tops MTEB leaderboard (semantic search leader)
3. **Best reranking**: Cohere Rerank v3 industry standard (NDCG@10 >0.85)
4. **Optimized integration**: Components trained to work together
5. **Cost transparency**: Reranking dominates (56%), can optimize separately

**3-Year TCO**: $4,859.50 (Cohere complete) or $3,045.23 (Google hybrid)
**Monthly Cost (Year 1)**: $106 (Cohere) or $66 (Google hybrid)
**Cost per Query**: $0.0424 (Cohere) or $0.0266 (Google hybrid)

**Key Cost Insight**: Reranking dominates cost (56-90% of total). Optimize reranking frequency for biggest savings.

**Next Steps**:
1. **Week 1-2**: Evaluation (side-by-side vs. keyword search, cost modeling)
2. **Week 3-4**: Implementation (vector DB setup, document migration, RAG pipeline)
3. **Week 5-6**: Staged rollout (10% → 50% → 100% of employees)
4. **Week 7-8**: Optimization (retrieval tuning, cost optimization, generation quality)

**Total Migration Effort**: 84 hours ($12,600 at $150/hour)

**Success Metrics**: Track cost (<$0.05/query), precision@5 (>70%), answer accuracy (>85%), user satisfaction (>4.0/5.0), latency (<2s)

**Critical Consideration**: Reranking cost ($720/year Year 1) exceeds embeddings ($22) and generation ($540) combined. Monitor reranking usage closely.

---

**Document Version**: 1.0
**Author**: LLM API Research Team
**Date**: November 5, 2025
**Total Lines**: 612
