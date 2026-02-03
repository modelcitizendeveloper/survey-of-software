# Retrieval Strategies for RAG

## Overview

Retrieval is the stage where your RAG system finds the most relevant chunks for a given query. The quality of retrieval directly determines answer quality - the best LLM in the world can't help if you give it irrelevant context.

**Evolution**:
- **2023 (Naive)**: Dense retrieval only (embed query, find top-k by similarity)
- **2025 (Standard)**: Hybrid retrieval (BM25 + dense) + reranking

**Performance**: Hybrid retrieval + reranking delivers **40-50% precision improvement** vs naive dense-only approach.

## Dense Retrieval (Semantic Search)

### How It Works

1. **Indexing**: Embed all chunks with an embedding model (e.g., text-embedding-3-large)
2. **Query**: Embed the user's question with same model
3. **Search**: Find top-K chunks by cosine similarity (or other distance metric)

**Example**:
```
Query: "How do I return damaged goods?"
Query embedding: [0.23, -0.45, 0.67, ...] (1536 dimensions)

Chunk embeddings:
Chunk 1: [0.21, -0.43, 0.69, ...] → similarity: 0.92
Chunk 2: [0.54, 0.12, -0.33, ...] → similarity: 0.45
Chunk 3: [0.19, -0.48, 0.71, ...] → similarity: 0.89

Return: [Chunk 1, Chunk 3] (top-2)
```

### Strengths

- **Semantic understanding**: Matches meaning, not just words
  - Query "ROI" matches "return on investment"
  - Query "refund" matches "money back guarantee"
- **Handles synonyms and paraphrasing**
- **Language understanding**: "What was Q4 revenue?" matches "fourth quarter sales were $5M"

### Weaknesses

- **Misses exact matches**: Query "Q4 2025" might match "Q3 2024" if semantically similar
- **Poor for specific terms**: Dates, IDs, model numbers, names
- **No keyword matching**: "Product SKU #12345" won't necessarily match "12345" if embedding doesn't capture it

### When Dense-Only Works

- Broad conceptual questions
- Synonyms and paraphrasing common
- Exact terms not critical

### When Dense-Only Fails

- Specific dates, IDs, model numbers
- Legal/compliance (exact wording matters)
- Technical documentation (specific commands, APIs)

## BM25 (Keyword Search)

### How It Works

BM25 (Best Match 25) is a statistical ranking function for keyword matching.

**Algorithm**:
- Counts term frequency (TF) in document
- Adjusts for document length (longer docs aren't penalized)
- Considers inverse document frequency (IDF) - rare terms weighted higher

**Example**:
```
Query: "Q4 2025 revenue"

Chunk 1: "Q4 2025 revenue was $5M. Our Q4 performance..."
  - "Q4": appears 2 times (high TF)
  - "2025": appears 1 time
  - "revenue": appears 1 time
  - BM25 score: 8.7

Chunk 2: "The fourth quarter revenue increased..."
  - "Q4": appears 0 times (no match)
  - "revenue": appears 1 time
  - BM25 score: 1.2

Return: [Chunk 1] (exact match wins)
```

### Strengths

- **Exact term matching**: Catches specific dates, IDs, numbers
- **Fast**: No embedding computation, just text statistics
- **Explainable**: Can see which terms matched
- **No model dependency**: Pure statistical approach

### Weaknesses

- **No semantic understanding**: "ROI" doesn't match "return on investment"
- **Synonyms fail**: "refund" doesn't match "money back"
- **Spelling matters**: Typos break matching

### When BM25 Works

- Exact term matching critical (dates, IDs, names)
- Legal/compliance documentation
- API docs (exact command names)
- Database queries (specific field names)

### When BM25 Fails

- Paraphrased queries
- Synonym-heavy content
- Conceptual questions (no specific keywords)

## Hybrid Search: Best of Both Worlds

### The 2025 Standard Approach

Combine BM25 (keyword) + Dense (semantic) for complementary strengths.

**Pipeline**:
```
1. BM25 Search → Top-100 candidates by keyword matching
2. Dense Search → Top-100 candidates by semantic similarity
3. Reciprocal Rank Fusion (RRF) → Merge both rankings
4. Result: Top-K chunks combining both signals
```

### Reciprocal Rank Fusion (RRF)

**Problem**: How do you combine two different scoring systems (BM25 scores vs cosine similarities)?

**Solution**: RRF uses **rank** instead of raw scores.

**Algorithm**:
```python
RRF_score = sum(1 / (k + rank_i)) for each list where item appears

k = 60 (constant to prevent divide-by-zero)
rank_i = position in list i (1-indexed)
```

**Example**:
```
BM25 ranking:           Dense ranking:
1. Chunk A (score 8.7)  1. Chunk B (similarity 0.92)
2. Chunk B (score 7.2)  2. Chunk A (similarity 0.89)
3. Chunk C (score 5.1)  3. Chunk D (similarity 0.85)

RRF scores:
Chunk A: 1/(60+1) + 1/(60+2) = 0.0164 + 0.0161 = 0.0325
Chunk B: 1/(60+2) + 1/(60+1) = 0.0161 + 0.0164 = 0.0325
Chunk C: 1/(60+3) + 0 = 0.0159
Chunk D: 0 + 1/(60+3) = 0.0159

Final ranking: [Chunk A, Chunk B, Chunk C, Chunk D]
```

Chunks appearing in both lists get boosted.

### Why Hybrid Outperforms

**Query**: "What was Widget A's ROI in Q4 2025?"

**BM25 catches**:
- "Q4 2025" (exact date match)
- "Widget A" (exact product name)

**Dense catches**:
- "ROI" ↔ "return on investment" (semantic)
- "profitability increased" (conceptually related)

**Hybrid**: Combines both → Finds chunk with "Widget A showed 15% return on investment in Q4 2025"

**Performance**: **40-50% precision improvement** vs dense-only or BM25-only.

### Implementation Complexity

**Moderate**. Most vector databases support hybrid search:
- Weaviate: Built-in hybrid search
- Pinecone: Sparse-dense vectors
- Qdrant: Fusion API
- LangChain / LlamaIndex: Built-in hybrid retrievers

## Reranking: The Final Optimization

### The Problem

Hybrid search returns top-K candidates (e.g., top-20), but the ranking might not be perfect. Similarity scores and BM25 scores are crude signals.

**Example**:
```
Top-5 from hybrid search:
1. Chunk A: Mentions "Q4" and "revenue" but different product
2. Chunk B: About Q3 2025 Widget A (wrong quarter)
3. Chunk C: About Q4 2025 Widget A ROI (PERFECT)
4. Chunk D: General revenue discussion
5. Chunk E: Mentions "quarterly performance"
```

Chunk C is buried at #3, but it's the best match.

### How Reranking Works

**Cross-encoder model** scores query-document pairs directly.

**Difference from bi-encoder (dense retrieval)**:
- **Bi-encoder**: Embeds query and doc separately → cosine similarity
- **Cross-encoder**: Takes [query, doc] as input → relevance score

**Cross-encoders are more accurate but slower** (can't pre-compute doc embeddings).

**Pipeline**:
```
1. Hybrid search → Top-20 candidates (fast, broad recall)
2. Cross-encoder → Re-score all 20 candidates (slow, high precision)
3. Return top-5 after reranking (best matches)
```

**Example**:
```
Hybrid search top-5:
1. Chunk A (hybrid score: 0.82)
2. Chunk B (hybrid score: 0.79)
3. Chunk C (hybrid score: 0.76)  ← Actually best
4. Chunk D (hybrid score: 0.73)
5. Chunk E (hybrid score: 0.71)

Cross-encoder rescoring:
Chunk C: 0.94 (most relevant) ← Promoted to #1
Chunk A: 0.71
Chunk B: 0.68
Chunk D: 0.45
Chunk E: 0.39

Final top-5:
1. Chunk C (0.94)
2. Chunk A (0.71)
3. Chunk B (0.68)
4. Chunk D (0.45)
5. Chunk E (0.39)
```

### Reranking Performance

- **Quality improvement**: Up to **48%** better relevance
- **Cost reduction**: **25%** fewer tokens (better context → shorter prompts)
- **User engagement**: Higher satisfaction, fewer re-queries

### Popular Reranking Models

- **Cohere Rerank**: Commercial API, high quality
- **Cross-encoders from Hugging Face**: Open-source (e.g., ms-marco-MiniLM)
- **Anthropic's Claude**: Can be used for reranking (expensive but effective)

## The Complete 2025 RAG Retrieval Pipeline

```
User Query: "What's our refund policy for damaged goods?"

┌──────────────────────────────────────────┐
│ Stage 1: Hybrid Search                   │
├──────────────────────────────────────────┤
│ BM25: Find chunks with "refund",         │
│       "damaged", "goods" → Top-100       │
│                                          │
│ Dense: Embed query, find similar         │
│        chunks → Top-100                  │
│                                          │
│ RRF: Merge rankings → Top-20             │
└──────────────────────────────────────────┘
                ↓
┌──────────────────────────────────────────┐
│ Stage 2: Cross-Encoder Reranking         │
├──────────────────────────────────────────┤
│ For each of top-20:                      │
│   score = cross_encoder([query, chunk])  │
│                                          │
│ Re-sort by cross-encoder scores          │
│ → Top-5 highest scores                   │
└──────────────────────────────────────────┘
                ↓
┌──────────────────────────────────────────┐
│ Stage 3: Metadata Filtering (Optional)   │
├──────────────────────────────────────────┤
│ Apply access control, date ranges        │
│ E.g., "only docs from last 6 months"     │
│      "only docs user has permission for" │
└──────────────────────────────────────────┘
                ↓
┌──────────────────────────────────────────┐
│ Stage 4: LLM Generation                  │
├──────────────────────────────────────────┤
│ Send top-5 chunks to LLM as context      │
│ Generate grounded answer with citations  │
└──────────────────────────────────────────┘
```

**Expected Performance**: 40-50% precision improvement over naive (dense-only, no reranking).

## Metadata Filtering

### The Use Case

Sometimes you need to filter by:
- **Access control**: User can only see certain docs
- **Time range**: "What changed in last 6 months?"
- **Document type**: "Search only in financial reports"
- **Geography**: "Policies for California only"

### How It Works

**Pre-filtering** (recommended):
```python
# Filter before retrieval
results = vector_db.search(
    query_embedding,
    filter={"date": {"$gte": "2025-01-01"}, "access": "public"}
)
```

**Post-filtering** (less efficient):
```python
# Retrieve all, then filter
all_results = vector_db.search(query_embedding, top_k=100)
filtered = [r for r in all_results if r.metadata["access"] == "public"]
```

**Pre-filtering is faster** (database indexes help) but requires good metadata.

### Common Metadata

- **Source**: filename, URL, database table
- **Timestamp**: created_at, updated_at
- **Access control**: department, permission_level, public/private
- **Document type**: pdf, markdown, email, slack
- **Section**: chapter, heading, page_number

## Decision Framework

### Use Dense-Only when:
- Broad conceptual questions
- Exact terms not critical
- Prototyping / baseline

### Use BM25-Only when:
- Exact keyword matching critical
- Legacy systems
- Ultra-low-latency requirements

### Use Hybrid (BM25 + Dense) when:
- Production RAG systems (2025 standard)
- Mix of exact and semantic matching
- Best quality matters

### Add Reranking when:
- Quality is critical
- Cost of better context < cost of reranking
- 48% improvement and 25% token savings worth it

### Add Metadata Filtering when:
- Access control required
- Time-based queries
- Document type filtering
- Compliance requirements

## The 2025 Baseline

**For production RAG**:
```
1. Hybrid Search (BM25 + Dense + RRF)
2. Cross-Encoder Reranking
3. Metadata Filtering (if needed)
```

**Expected improvement**: 40-50% precision vs naive dense-only.

## Common Mistakes

1. **Dense-only in production**
   - Missing exact keyword matches
   - 40-50% worse than hybrid

2. **No reranking**
   - Missing 48% quality improvement
   - Paying for extra tokens (worse context)

3. **BM25-only in 2025**
   - Missing semantic matches
   - Outdated approach

4. **Post-filtering instead of pre-filtering**
   - Slower, less efficient
   - Wastes retrieval on filtered-out docs

5. **Too few candidates for reranking**
   - Reranking top-5 → Limited room for improvement
   - Retrieve top-20, rerank to top-5 → Better

6. **Ignoring metadata**
   - Can't filter by time, access, type
   - Missing valuable signal

## Evaluation Metrics

### Precision@K
**What**: Of top-K results, how many are relevant?
**Example**: Retrieve 5 chunks, 4 are relevant → Precision@5 = 80%

### Recall@K
**What**: Of all relevant chunks, how many are in top-K?
**Example**: 10 relevant chunks exist, 4 in top-5 → Recall@5 = 40%

### Context Relevancy
**What**: Are the retrieved chunks actually relevant to the query?
**Measure**: Human evaluation, LLM-as-judge, or ground-truth dataset

### How to Evaluate

1. **Create test dataset**: Real user queries + ground-truth relevant chunks
2. **Vary one parameter at a time**: Hybrid vs dense, reranking on/off, etc.
3. **Measure precision@K, recall@K**: Track improvement
4. **A/B test in production**: See impact on user satisfaction

## Future Trends

1. **Agentic retrieval**: LLMs dynamically choosing retrieval strategies
2. **Multi-modal retrieval**: Images, tables, charts as first-class citizens
3. **Graph RAG**: Knowledge graphs supplementing vector search
4. **Learned reranking**: Fine-tuned models for domain-specific ranking
5. **Real-time personalization**: Retrieval adapts to user preferences

## Sources

- [Optimizing RAG with Hybrid Search & Reranking](https://superlinked.com/vectorhub/articles/optimizing-rag-with-hybrid-search-reranking)
- [Advanced RAG: From Naive Retrieval to Hybrid Search and Re-ranking](https://dev.to/kuldeep_paul/advanced-rag-from-naive-retrieval-to-hybrid-search-and-re-ranking-4km3)
- [Hybrid Retrieval and Reranking in RAG](https://www.genzeon.com/hybrid-retrieval-deranking-in-rag-recall-precision/)
- [Understanding hybrid search RAG for better AI answers](https://www.meilisearch.com/blog/hybrid-search-rag)
- [Improving RAG Performance: WTF is Hybrid Search?](https://www.fuzzylabs.ai/blog-post/improving-rag-performance-hybrid-search)
- [Ultimate Guide to Choosing the Best Reranking Model in 2025](https://www.zeroentropy.dev/articles/ultimate-guide-to-choosing-the-best-reranking-model-in-2025)
- [Advanced RAG Techniques for High-Performance LLM Applications](https://neo4j.com/blog/genai/advanced-rag-techniques/)
