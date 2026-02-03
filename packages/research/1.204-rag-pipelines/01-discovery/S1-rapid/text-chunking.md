# Text Chunking Strategies for RAG

## Overview

Text chunking is the process of breaking documents into smaller, retrievable pieces. This is the single most impactful component of RAG pipelines - **chunking strategy determines approximately 60% of your RAG system's accuracy**, more than the embedding model, reranker, or even the LLM generating final answers.

## Why Chunking Matters

**The fundamental problem**: You can't stuff 100 pages into an LLM prompt.
- Context window limits (even 200k tokens has limits)
- Cost scales with tokens
- Performance degrades with irrelevant context ("needle in haystack")

**The solution**: Break documents into chunks, retrieve only the most relevant chunks.

**The challenge**: Finding the right chunk size and strategy.

## The Chunk Size Trade-off

### Too Small (e.g., 50-100 tokens)
**Problem**: Fragments context
**Example**: Chunk contains "The answer is yes" without the question
**Result**: Precise matching but meaningless retrieval

### Too Large (e.g., 2000+ tokens)
**Problem**: Dilutes similarity
**Example**: Relevant paragraph buried in giant chunk with unrelated content
**Result**: Preserves context but poor ranking (cosine similarity diluted by irrelevant text)

### Sweet Spot (256-1024 tokens)
**Factual Q&A**: 256-512 tokens (precision over context)
**Context-heavy tasks**: 512-1024 tokens (summaries, analysis)
**General baseline**: 512 tokens

## Chunking Strategies Compared

### 1. Fixed-Size Chunking (Baseline Only)

**Approach**: Split every N tokens/characters
**Parameters**: Chunk size (e.g., 512 tokens)

**Pros**:
- Simple, predictable
- Easy to implement

**Cons**:
- Ignores document structure
- May split mid-sentence, mid-paragraph, mid-thought
- No semantic awareness

**Use case**: Baseline comparison only. Don't use in production.

**Example**:
```
Text: "The revenue for Q4 was $5M. This represents...
       [512 tokens later, mid-sentence]
       ...a 20% increase over Q3. Our margins improved..."

Chunk 1: "The revenue for Q4 was $5M. This represents..."
Chunk 2: "...a 20% increase over Q3. Our margins improved..."
```

Problem: Context split awkwardly, "This" in Chunk 2 has no referent.

### 2. RecursiveCharacterTextSplitter (Recommended Baseline)

**Approach**: Tries to split on separators in order: `["\n\n", "\n", " ", ""]`
**Framework**: LangChain (widely adopted)
**Parameters**: Chunk size (512 tokens), chunk overlap (50 tokens)

**How it works**:
1. Try splitting on double newlines (paragraphs)
2. If chunks still too large, split on single newlines (sentences)
3. If still too large, split on spaces (words)
4. Last resort: split on characters

**Pros**:
- Respects natural boundaries (paragraphs > sentences > words)
- Works for 80% of RAG applications
- Widely supported, well-tested
- Easy to configure

**Cons**:
- Not structure-aware (doesn't understand headers, sections)
- Heuristic-based (not semantic understanding)

**Use case**: **Start here**. This is the recommended baseline for 2025.

**Parameters**:
- **Chunk size**: 512 tokens (balance of precision and context)
- **Overlap**: 50 tokens (10% overlap prevents split context)

**Example**:
```
Text: "# Revenue Report\n\nQ4 revenue was $5M.\n\nThis represents a 20% increase.\n\nOur margins improved..."

Chunk 1: "# Revenue Report\n\nQ4 revenue was $5M.\n\nThis represents a 20% increase." (split on \n\n)
Chunk 2: "This represents a 20% increase.\n\nOur margins improved..." (50-token overlap includes "This represents...")
```

Result: Overlap ensures "This" has context even in Chunk 2.

### 3. Structure-Aware Chunking (Often Biggest Improvement)

**Approach**: Split based on document structure (headers, sections)
**Frameworks**: MarkdownHeaderTextSplitter, HTMLHeaderTextSplitter
**Parameters**: Header levels to split on (e.g., # ## ###)

**How it works**:
- Markdown: Split on headers (#, ##, ###)
- HTML: Split on tags (h1, h2, div)
- Preserves hierarchy in metadata

**Pros**:
- **Often the single biggest improvement over fixed-size**
- Preserves semantic units (sections are naturally coherent)
- Maintains context (heading provides topic for content)
- Metadata includes heading hierarchy

**Cons**:
- Only works for structured documents (Markdown, HTML)
- Not applicable to plain text

**Use case**: Documents with clear structure (Markdown READMEs, HTML pages, structured reports).

**Example**:
```markdown
# Refund Policy

Damaged goods can be returned within 30 days.

## Shipping Policy

Delivery takes 5-7 business days.
```

Chunks:
```
Chunk 1: {
  content: "Damaged goods can be returned within 30 days.",
  metadata: {header_1: "Refund Policy"}
}

Chunk 2: {
  content: "Delivery takes 5-7 business days.",
  metadata: {header_1: "Refund Policy", header_2: "Shipping Policy"}
}
```

Query "refund policy for damaged goods" matches Chunk 1 metadata + content.

### 4. Semantic Chunking (2-3% Better Recall)

**Approach**: Group sentences by semantic similarity of embeddings
**Frameworks**: LangChain SemanticChunker
**Parameters**: Breakpoint threshold method (percentile, std dev, IQR)

**How it works**:
1. Embed each sentence
2. Compute similarity between consecutive sentences
3. Split when similarity drops significantly (topic shift)

**Breakpoint methods**:
- **Percentile**: Split when similarity < 95th percentile
- **Standard deviation**: Split when difference > 1 std dev
- **Interquartile range (IQR)**: Split based on IQR of similarities

**Pros**:
- Topic-aware (each chunk = coherent theme)
- Better recall than recursive (2-3% improvement)
- No manual structure needed

**Cons**:
- Computationally expensive (embedding every sentence)
- Variable chunk sizes (can be very large or very small)
- More complex to tune

**Use case**: When thematic coherence matters more than fixed size. Documents without clear structure but with topic shifts.

**Performance**: +2-3% recall vs RecursiveCharacterTextSplitter (research finding).

### 5. Parent-Child (Small-to-Large)

**Approach**: Small chunks for retrieval, large chunks for context
**Frameworks**: LlamaIndex ParentDocumentRetriever

**How it works**:
1. Index small chunks (e.g., 128 tokens) for precise retrieval
2. When retrieving, return parent chunk (e.g., 1024 tokens) for context
3. Best of both: precision of small chunks, context of large chunks

**Pros**:
- Combines precision and context
- Retrieves specific snippets but provides surrounding text
- Ideal for complex Q&A

**Cons**:
- More complex to implement
- Requires maintaining parent-child relationships
- Higher storage (both small and large chunks indexed)

**Use case**: Complex Q&A where you need both precise matching and broad context. Enterprise knowledge bases.

### 6. Page-Level Chunking (Best for Certain Document Types)

**Approach**: One chunk per page
**Parameters**: None (page boundaries define chunks)

**Pros**:
- Simplest approach
- **Highest accuracy in NVIDIA 2024 benchmarks** for financial reports, legal docs
- Preserves natural document organization

**Cons**:
- Only works for paginated documents (PDFs)
- Variable chunk sizes (some pages have more content)
- Not suitable for long pages (> 1024 tokens)

**Use case**: Financial reports, legal documents, research papers that organize information by pages.

**Performance**: Achieved highest accuracy in NVIDIA 2024 chunking study for financial data.

## Chunk Overlap: Preventing Split Context

**The problem**: Important context might span chunk boundaries.

**Example without overlap**:
```
Chunk 1: "...introduced a new pricing model."
Chunk 2: "This model reduces costs by 30%."
```

Query "what does the new pricing model do?" → Chunk 2 matches ("model...costs") but "This model" has no referent.

**Solution**: Overlap chunks by 10-15%

**Example with 50-token overlap**:
```
Chunk 1: "...introduced a new pricing model. This model reduces costs by 30%. Our customers..."
Chunk 2: "This model reduces costs by 30%. Our customers have reported..."
```

Now Chunk 2 includes "new pricing model" context.

**NVIDIA Finding (2024)**: 15% overlap optimal for 1024-token chunks.

**Recommendation**: 50-token overlap for 512-token chunks (~10%).

## Decision Framework

### Start with RecursiveCharacterTextSplitter (80% of cases)
**Parameters**: 512 tokens, 50 overlap
**When**: General-purpose baseline

### Upgrade to Structure-Aware (biggest single improvement)
**Tools**: MarkdownHeaderTextSplitter, HTMLHeaderTextSplitter
**When**: Documents have clear structure (headers, sections)
**Impact**: Often the biggest improvement over fixed-size

### Consider Semantic Chunking (+2-3% recall)
**When**: Thematic coherence critical, willing to pay embedding cost
**Impact**: +2-3% recall vs recursive

### Try Page-Level for Specific Types
**When**: Financial reports, legal docs, research papers (NVIDIA 2024 best accuracy)

### Use Parent-Child for Complex Q&A
**When**: Need both precision and broad context, complex knowledge bases

## Impact on RAG Accuracy

**Research finding**: Chunking strategy determines ~60% of RAG system accuracy.

**Hierarchy of impact** (ranked):
1. **Chunking strategy** (~60%)
2. Retrieval method (hybrid vs dense-only)
3. Document parsing quality
4. Embedding model
5. LLM choice

**Implication**: Optimize chunking BEFORE upgrading embeddings or LLM.

## Common Mistakes

1. **Fixed-size chunking in production**
   - Ignores structure, splits awkwardly
   - Recursive is strictly better for same parameters

2. **No overlap**
   - Context split across chunks
   - Queries matching split content fail

3. **Wrong chunk size**
   - Too small: "yes" without question
   - Too large: diluted similarity
   - Baseline: 512 tokens

4. **Ignoring document structure**
   - Markdown/HTML → use structure-aware splitters
   - Often biggest single improvement

5. **Not evaluating on your data**
   - Different corpora need different strategies
   - Test with real queries on real documents

## The 2025 Baseline

**For most developers starting a RAG project**:

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,        # Tokens (balance of precision/context)
    chunk_overlap=50,      # 10% overlap prevents split context
    length_function=len,   # Or token counter
)

chunks = splitter.split_documents(documents)
```

**If your documents have structure (Markdown)**:

```python
from langchain.text_splitter import MarkdownHeaderTextSplitter

splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[
        ("#", "header_1"),
        ("##", "header_2"),
        ("###", "header_3"),
    ]
)

chunks = splitter.split_text(markdown_text)
```

## Future Trends

**Late 2025 prediction**: Production RAG systems will use agents to select chunking strategies dynamically.

**Example**:
- Financial PDF → Page-level chunking
- Markdown README → Structure-aware chunking
- Plain text blog → Semantic chunking
- LLM agent decides based on document type and query

## Sources

- [Document Chunking for RAG: 9 Strategies Tested (70% Accuracy Boost)](https://langcopilot.com/posts/2025-10-11-document-chunking-for-rag-practical-guide)
- [Chunking Strategies for RAG: A Comprehensive Guide](https://medium.com/@adnanmasood/chunking-strategies-for-retrieval-augmented-generation-rag-a-comprehensive-guide-5522c4ea2a90)
- [Ultimate Guide to Chunking Strategies for RAG (Databricks)](https://community.databricks.com/t5/technical-blog/the-ultimate-guide-to-chunking-strategies-for-rag-applications/ba-p/113089)
- [Chunking Strategies for RAG (Weaviate)](https://weaviate.io/blog/chunking-strategies-for-rag)
- [Best Chunking Strategies for RAG in 2025](https://www.firecrawl.dev/blog/best-chunking-strategies-rag-2025)
- [Finding the Best Chunking Strategy (NVIDIA)](https://developer.nvidia.com/blog/finding-the-best-chunking-strategy-for-accurate-ai-responses/)
- [Why Semantic Boundaries Cut RAG Errors by 60%](https://ragaboutit.com/the-chunking-strategy-shift-why-semantic-boundaries-cut-your-rag-errors-by-60/)
