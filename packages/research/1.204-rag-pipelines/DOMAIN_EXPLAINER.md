# What Are RAG Pipelines?

## The Fundamental Problem

Large Language Models (LLMs) have remarkable general knowledge but face critical limitations:

1. **Knowledge cutoff**: Training data ends at a specific date (e.g., GPT-4 trained through April 2023)
2. **No private data**: Can't access your company's documents, databases, or internal knowledge
3. **Hallucination**: May confidently generate plausible-sounding but incorrect information
4. **Static knowledge**: Can't update without expensive retraining

**Example**: Ask an LLM "What's in our Q4 2025 financial report?" → It has no idea. It wasn't trained on your data.

## The RAG Solution

**RAG (Retrieval-Augmented Generation)** solves this by combining three steps:

```
1. RETRIEVE relevant documents from your knowledge base
2. AUGMENT the LLM prompt with retrieved context
3. GENERATE an answer grounded in your actual data
```

Instead of asking the LLM to know everything, you:
- Store your documents in a searchable format
- Retrieve the most relevant pieces when a question is asked
- Give the LLM those pieces as context
- Let the LLM answer based on provided evidence, not memorized training data

**Result**: Accurate, cited answers from your own data without retraining the model.

## The RAG Pipeline: Three Critical Stages

### Stage 1: Document Loading

**Goal**: Get your data into the system

Your knowledge exists in various formats: PDFs, Word docs, databases, web pages, Slack messages, emails. Document loaders extract text and structure from these sources.

**Key challenge**: Preserving structure matters. A financial table in a PDF needs to maintain its rows/columns. A heading hierarchy in a document affects meaning.

**Common tools**:
- **PyPDF**: Simple, fast, good for basic text-based PDFs
- **Unstructured**: Intelligent parsing for complex layouts, OCR support
- **LlamaParse**: Specialized service for complex PDFs with tables (6s processing, high accuracy)
- **Docling**: Open-source alternative to LlamaParse

**Example**: Loading a 100-page technical manual:
- PyPDF extracts text but loses table structure → Poor retrieval
- LlamaParse preserves tables as markdown → Accurate retrieval

### Stage 2: Text Chunking

**Goal**: Break documents into retrievable pieces

**The problem**: You can't stuff 100 pages into an LLM prompt (context limits, cost, performance). You need to find the most relevant *sections*.

**The trade-off**:
- **Too small** (e.g., 50 tokens): Precise matching but fragments context ("The answer is yes" without knowing the question)
- **Too large** (e.g., 2000 tokens): Preserves context but dilutes similarity (matching an irrelevant paragraph in a giant chunk)

**Common strategies**:

1. **Fixed-size chunking** (256-512 tokens)
   - Simple, predictable
   - Ignores document structure (may split mid-sentence)
   - Baseline approach

2. **RecursiveCharacterTextSplitter** (LangChain default)
   - Tries to split on paragraphs, then sentences, then words
   - Respects natural boundaries
   - 80% of RAG applications start here

3. **Semantic chunking**
   - Groups sentences by topic using embeddings
   - Each chunk = coherent theme
   - 2-3% better recall than recursive splitter

4. **Document-structure aware**
   - Markdown: Split on headers (# ## ###)
   - HTML: Split on tags
   - Preserves hierarchy
   - Often the biggest single improvement

**Best practice (2025)**: Start with RecursiveCharacterTextSplitter (512 tokens, 50 overlap). If your content has clear structure (Markdown, HTML), switch to structure-aware splitting. Research shows chunking strategy determines ~60% of RAG accuracy.

**Chunk overlap**: Including 10-15% overlap between chunks prevents important context from being split across boundaries.

### Stage 3: Retrieval

**Goal**: Find the most relevant chunks for a given question

**The evolution**:

**Naive (2023)**: Embed question, embed chunks, find top-k by cosine similarity
- Fast, simple
- Misses exact keyword matches
- No understanding of query intent

**Hybrid (2025 standard)**:
```
1. BM25 (keyword search) → Find exact term matches
2. Dense retrieval (embeddings) → Find semantic matches
3. Reciprocal Rank Fusion → Combine both rankings
4. Reranking model → Optimize final ordering
5. Metadata filtering → Apply access control, date ranges
```

**Performance**: Hybrid retrieval + reranking delivers **40-50% precision improvement** over naive dense-only retrieval.

**Why hybrid matters**:
- Question: "What's the ROI for Q4 2025?"
- BM25 catches "Q4 2025" exact match (dense might miss the specific quarter)
- Dense catches "return on investment" as semantic match for "ROI"
- Together: Best of both worlds

**Reranking**: After retrieving top-20 candidates with hybrid search, a cross-encoder reranking model re-scores them for final top-5 selection. Research shows this improves quality by up to **48%** and reduces token usage by **25%**.

## The Complete Pipeline Flow

```
User Question: "What's our refund policy for damaged goods?"

┌─────────────────────────────────────────────────────────────┐
│ 1. DOCUMENT LOADING (Offline, one-time per document)       │
├─────────────────────────────────────────────────────────────┤
│   PDF: policies.pdf                                          │
│   → LlamaParse extracts text + tables as markdown           │
│   → Result: Structured markdown document                     │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. CHUNKING (Offline, one-time per document)               │
├─────────────────────────────────────────────────────────────┤
│   Markdown → MarkdownHeaderTextSplitter                      │
│   → Chunk 1: "# Refund Policy\n\nDamaged goods..."          │
│   → Chunk 2: "## Shipping Policy\n\nDelivery times..."       │
│   → Chunk 3: "## Warranty\n\nAll products come with..."     │
│   (Each chunk = 256-512 tokens with metadata)               │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. INDEXING (Offline, one-time per document)               │
├─────────────────────────────────────────────────────────────┤
│   For each chunk:                                            │
│   → Generate embedding vector (1536 dimensions)              │
│   → Store in vector database (Pinecone, Chroma, etc.)       │
│   → Index for BM25 keyword search                           │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. RETRIEVAL (Real-time, per user query)                   │
├─────────────────────────────────────────────────────────────┤
│   Query: "refund policy for damaged goods"                   │
│   → BM25: Find chunks with "refund", "damaged", "goods"     │
│   → Dense: Embed query, find semantically similar chunks    │
│   → Fusion: Combine rankings (RRF algorithm)                │
│   → Rerank: Cross-encoder scores top 20 → select top 5      │
│   → Result: [Chunk 1 (score: 0.92), Chunk 15 (0.87), ...]   │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. GENERATION (Real-time, per user query)                  │
├─────────────────────────────────────────────────────────────┤
│   LLM Prompt:                                                │
│   "Based on the following context, answer the question:      │
│                                                              │
│   Context 1: [Chunk 1 text]                                 │
│   Context 2: [Chunk 15 text]                                │
│   ...                                                        │
│                                                              │
│   Question: What's our refund policy for damaged goods?     │
│                                                              │
│   Answer:"                                                   │
│   → LLM generates grounded answer with citations            │
└─────────────────────────────────────────────────────────────┘
```

## Common Misconceptions

### "RAG means using LangChain"
No. RAG is a pattern. LangChain is one framework that implements it. You can build RAG with LlamaIndex, Haystack, raw code, or any tool.

### "Bigger chunks are always better"
No. Bigger chunks preserve context but dilute similarity scores. Smaller chunks improve precision but fragment meaning. Optimal size depends on your use case: 256-512 for factual Q&A, 512-1024 for context-heavy tasks.

### "Vector search is enough"
Not in 2025. Hybrid search (BM25 + dense) outperforms either alone by 40-50%. Exact keyword matching matters (dates, names, specific terms).

### "Just throw everything into the context window"
Claude 3.7 has 200k token context, but:
- Cost scales with tokens ($$$)
- Performance degrades with irrelevant context ("needle in haystack")
- Retrieval focuses the LLM on what matters

### "Chunking doesn't matter that much"
Research shows chunking strategy determines ~60% of RAG accuracy—more than embedding model, reranker, or even the LLM generating the final answer.

## When to Use RAG

### Use RAG when:
- Answering questions from your private documents
- Knowledge changes frequently (product specs, policies, news)
- Citing sources matters (legal, medical, enterprise)
- Data is too large for one context window
- Fine-tuning is too expensive or slow

### Don't use RAG when:
- Question answerable from LLM's training data
- No external knowledge needed
- Real-time data from APIs (use function calling instead)
- Single document fits in context window

## The 2025 State of RAG Pipelines

**What's working**:
- Hybrid retrieval (BM25 + dense + reranking) is standard
- LlamaParse dominates complex PDF parsing
- LlamaIndex specializes in RAG with 35% better retrieval accuracy
- Semantic chunking outperforms fixed-size by 2-3% recall
- 51% of organizations run agents in production (often RAG-powered)

**What's evolving**:
- Agentic retrieval: LLMs decide chunking strategy dynamically
- Graph RAG: Knowledge graphs supplement vector search
- Multi-modal RAG: Images, tables, charts as first-class citizens
- Fine-tuned embeddings: Domain-specific embedding models

**What's painful**:
- Evaluation is hard (how do you know it's working?)
- Document parsing quality varies wildly by tool
- Chunking strategy is trial-and-error
- Production cost scales with document volume

## Key Takeaway

RAG pipelines transform LLMs from "smart but limited" to "smart and grounded in your data." The pipeline has three critical stages—loading, chunking, retrieval—and each determines overall system quality. In 2025, hybrid retrieval with reranking is standard, LlamaParse leads complex parsing, and chunking strategy matters more than most developers realize.

**The hierarchy of impact**:
1. Chunking strategy (~60% of accuracy)
2. Retrieval quality (hybrid > dense-only by 40-50%)
3. Document parsing (garbage in = garbage out)
4. Embedding model (surprisingly less critical than above)
5. LLM choice (any modern LLM works if retrieval is good)

Get the pipeline right, and RAG delivers accurate, cited answers from your knowledge. Get it wrong, and you've built an expensive hallucination machine.
