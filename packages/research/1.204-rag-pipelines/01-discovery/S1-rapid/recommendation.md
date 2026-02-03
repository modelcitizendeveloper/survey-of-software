# RAG Pipeline Decision Framework & Recommendations

## Quick Decision Tree

```
Starting a new RAG project?
│
├─ Simple text PDFs, standard Q&A?
│  └─ Use: PyPDFLoader + RecursiveCharacterTextSplitter (512, 50 overlap) + Hybrid retrieval
│
├─ Complex PDFs with tables?
│  └─ Use: LlamaParse + LlamaIndex + Hybrid retrieval + Reranking
│
├─ Markdown/HTML documents?
│  └─ Use: MarkdownHeaderTextSplitter + Hybrid retrieval
│
├─ Mixed sources (PDFs, web, databases)?
│  └─ Use: LlamaIndex (160+ connectors) + Hybrid retrieval + Reranking
│
└─ Need RAG + multi-agent workflows?
   └─ Use: LlamaIndex (retrieval) + LangChain (orchestration)
```

## The 2025 Baseline RAG Pipeline

If starting today, this is the recommended baseline for production:

### Document Loading
- **Simple PDFs**: PyPDFLoader (fast, lightweight)
- **Complex PDFs**: LlamaParse (~6s processing, 10/10 accuracy)
- **Multiple formats**: LlamaIndex data connectors (160+ types)

### Text Chunking
- **No clear structure**: RecursiveCharacterTextSplitter (512 tokens, 50 overlap)
- **Markdown/HTML**: MarkdownHeaderTextSplitter
- **Financial/legal**: Page-level chunking (NVIDIA 2024 best accuracy)

### Retrieval
- **Baseline**: Hybrid search (BM25 + dense + RRF)
- **Production**: Hybrid + cross-encoder reranking
- **Enterprise**: Hybrid + reranking + metadata filtering

### Framework
- **RAG-focused**: LlamaIndex (35% better retrieval)
- **Broader orchestration**: LangChain
- **Both needs**: LlamaIndex (retrieval) + LangChain (agents)

### Expected Performance
- **40-50% precision improvement** vs naive (dense-only, fixed-size chunks)
- **+2-3% additional boost** from semantic chunking
- **Up to 48% quality improvement** from reranking
- **25% token cost reduction** from better context

## Decision Framework by Use Case

### Document Q&A System

**Scenario**: Users ask questions about your documentation (e.g., "How do I reset my password?")

**Recommended Stack**:
```
- Document loading: LlamaIndex SimpleDirectoryReader (handles multiple formats)
- Chunking: RecursiveCharacterTextSplitter (512 tokens, 50 overlap)
  - If Markdown/HTML: MarkdownHeaderTextSplitter
- Retrieval: Hybrid search (BM25 + dense)
- Reranking: Cross-encoder (improves by 48%)
- Framework: LlamaIndex (RAG-specialized)
```

**Why**:
- Multiple document formats → LlamaIndex connectors
- Structured docs (READMEs) → Structure-aware chunking wins
- Exact command names + concepts → Hybrid search essential
- Quality matters → Reranking worth the cost

**Expected Accuracy**: 40-50% better than naive dense-only

### Customer Support Knowledge Base

**Scenario**: AI assistant answering customer questions using internal knowledge base

**Recommended Stack**:
```
- Document loading: LlamaIndex (Slack, Zendesk, Confluence connectors)
- Chunking: RecursiveCharacterTextSplitter (512, 50) or Semantic chunking
- Retrieval: Hybrid + reranking + metadata filtering (permissions)
- Framework: LlamaIndex (retrieval) + LangChain (multi-turn conversation)
```

**Why**:
- Multiple sources (Slack, tickets, docs) → LlamaIndex connectors
- Conversational queries → Semantic chunking helps
- User permissions matter → Metadata filtering essential
- Multi-turn dialogue → LangChain conversation chains
- Quality critical → Reranking (48% improvement)

**Additional considerations**:
- Access control: Filter by user permissions
- Recency: Weight recent tickets higher
- Escalation: Hand off to human when uncertain

### Financial Document Analysis

**Scenario**: Answering questions about financial reports, earnings calls, SEC filings

**Recommended Stack**:
```
- Document loading: LlamaParse (table preservation critical)
- Chunking: Page-level (NVIDIA 2024 best for financial docs)
- Retrieval: Hybrid + reranking
- Framework: LlamaIndex
```

**Why**:
- Complex tables → LlamaParse essential (PyPDF breaks retrieval)
- Organized by page → Page-level chunking best (NVIDIA finding)
- Specific dates/numbers → Hybrid (BM25 catches "Q4 2025")
- Accuracy critical → Reranking mandatory
- Citations required → LlamaIndex citation mapping

**Compliance**:
- Metadata filtering for regulatory requirements
- Audit trail for all retrievals
- Citation to source documents

### Legal Document Search

**Scenario**: Searching case law, contracts, regulations

**Recommended Stack**:
```
- Document loading: LlamaParse (preserves structure)
- Chunking: Structure-aware (section headers) OR Page-level
- Retrieval: Hybrid (exact terms critical) + reranking
- Metadata: Case number, jurisdiction, date, court
```

**Why**:
- Exact wording matters → Hybrid with strong BM25 weight
- Structure important → Section-aware chunking
- Citations mandatory → LlamaIndex fine-grained mapping
- Compliance → Audit trail required

### Research Paper Database

**Scenario**: Q&A over academic papers, literature review assistance

**Recommended Stack**:
```
- Document loading: LlamaParse (equations, figures, tables)
- Chunking: Page-level OR semantic chunking
- Retrieval: Hybrid + reranking
- Framework: LlamaIndex
```

**Why**:
- Complex PDFs (equations, figures) → LlamaParse
- Topic coherence → Semantic chunking
- Specific citations (author names, years) → Hybrid (BM25)
- Cross-references → Graph RAG (advanced)

**Advanced**:
- Citation graph traversal
- Author disambiguation
- Multi-modal (figures, charts)

### Enterprise Knowledge Management

**Scenario**: Unified search across all company knowledge (SharePoint, Confluence, Slack, Google Drive)

**Recommended Stack**:
```
- Document loading: LlamaIndex (160+ connectors, enterprise integrations)
- Chunking: Adaptive (structure-aware where available, recursive elsewhere)
- Retrieval: Hybrid + reranking + metadata filtering
- Framework: LlamaIndex (retrieval) + LangChain (workflows)
```

**Why**:
- Diverse sources → LlamaIndex enterprise connectors
- Mixed formats → Adaptive chunking strategy
- Permissions → Metadata filtering critical
- Usage patterns → Analytics and monitoring

**Enterprise considerations**:
- SSO integration
- Data residency requirements
- Incremental updates (not full re-index)
- Cost management (embedding budget)

## Decision Framework by Constraints

### By Budget

#### Low Budget / Prototyping
```
- Loading: PyPDF, TextLoader (free)
- Chunking: RecursiveCharacterTextSplitter
- Retrieval: Dense-only (skip reranking)
- Embeddings: text-embedding-3-small (cheap)
- Vector DB: Chroma (local, free)
- Framework: LangChain (largest community, most free tutorials)
```

**Trade-off**: ~40% worse retrieval than production baseline, but $0 infrastructure cost.

#### Production (Quality Matters)
```
- Loading: LlamaParse ($$ but worth it for quality)
- Chunking: Structure-aware + semantic
- Retrieval: Hybrid + reranking
- Embeddings: text-embedding-3-large or domain-specific
- Vector DB: Pinecone, Weaviate (managed)
- Framework: LlamaIndex (35% better retrieval)
```

**Trade-off**: Higher cost but 40-50% better quality, 25% token savings from better context.

### By Team Expertise

#### Beginner
**Start with**: LangChain + RecursiveCharacterTextSplitter + dense retrieval
**Why**: Most tutorials, largest community, simpler concepts
**Upgrade path**: Add hybrid search, then reranking, then switch to LlamaIndex if RAG-focused

#### Intermediate
**Start with**: LlamaIndex + hybrid retrieval
**Why**: Better defaults for RAG, worth the learning curve
**Upgrade path**: Add reranking, semantic chunking, advanced retrieval modes

#### Advanced
**Start with**: Best tool for each component
**Why**: Can navigate complexity, optimize each stage
**Options**: Custom chunking, graph RAG, multi-modal, agentic retrieval

### By Data Characteristics

#### Highly Structured (Markdown, HTML, XML)
```
- Chunking: Structure-aware (MarkdownHeaderTextSplitter)
- Impact: Often the single biggest improvement
- Why: Preserves hierarchy, semantic units
```

#### Unstructured (Plain text, transcripts)
```
- Chunking: Semantic chunking (topic coherence)
- Impact: +2-3% recall vs recursive
- Why: No structure to leverage
```

#### Tables and Charts (Financial, scientific)
```
- Loading: LlamaParse (critical for table preservation)
- Chunking: Page-level (NVIDIA 2024 best)
- Impact: Broken tables = broken retrieval
```

#### Mixed (Enterprise corpus)
```
- Loading: LlamaIndex (160+ connectors)
- Chunking: Adaptive per document type
- Retrieval: Hybrid (handles variety)
```

## Common Patterns and Anti-Patterns

### ✅ Good Patterns

**Start simple, iterate**:
1. Baseline: RecursiveCharacterTextSplitter + dense retrieval
2. Add hybrid search (+40-50% precision)
3. Add reranking (+48% quality)
4. Add semantic chunking (+2-3% recall)

**Match tool to complexity**:
- Simple docs → Simple tools (PyPDF, recursive splitter)
- Complex docs → Sophisticated tools (LlamaParse, structure-aware)

**Evaluate on your data**:
- Create test queries from real users
- Measure precision@5, recall@5
- A/B test in production

### ❌ Anti-Patterns

**Premature optimization**:
- Using semantic chunking before trying recursive
- Fine-tuning embeddings before testing hybrid search
- Start simple, upgrade based on metrics

**Ignoring hierarchy of impact**:
- Chunking (~60% of accuracy) → Optimize first
- Retrieval (hybrid vs dense) → Second
- Embedding model → Later

**One-size-fits-all**:
- PyPDF for everything (breaks on tables)
- Fixed-size for everything (ignores structure)
- Dense-only for everything (misses exact matches)

**No evaluation**:
- Assuming it works
- Not measuring precision/recall
- No A/B testing

## Incremental Upgrade Path

### Level 1: MVP (Functional but not optimal)
```
- PyPDF + RecursiveCharacterTextSplitter + Dense retrieval
- Expected: Functional, ~40% worse than production baseline
- Cost: Minimal
- Time: 1 day implementation
```

### Level 2: Production Baseline (Recommended start)
```
- Add: Hybrid search (BM25 + dense + RRF)
- Improvement: +40-50% precision
- Cost: Minimal (BM25 is cheap)
- Time: +1 day implementation
```

### Level 3: High Quality
```
- Add: Reranking (cross-encoder)
- Improvement: +48% quality, -25% token cost
- Cost: Reranking API costs
- Time: +1 day implementation
```

### Level 4: Optimal
```
- Add: Structure-aware chunking where applicable
- Add: Semantic chunking for unstructured
- Add: LlamaParse for complex PDFs
- Improvement: Additional 5-10% quality
- Cost: Higher (LlamaParse API, semantic chunking embeddings)
- Time: +2-3 days implementation
```

### Level 5: Advanced
```
- Add: Graph RAG (knowledge graph augmentation)
- Add: Multi-modal (images, tables as first-class)
- Add: Agentic retrieval (dynamic strategy selection)
- Improvement: Domain-specific, varies
- Cost: Significant development time
- Time: +1-2 weeks
```

## The "Start Here" Recommendation

**For most developers starting a RAG project in 2025**:

### Phase 1: Baseline (Day 1)
```python
# Document Loading
from llama_index import SimpleDirectoryReader
documents = SimpleDirectoryReader('docs/').load_data()

# Chunking
from langchain.text_splitter import RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
chunks = splitter.split_documents(documents)

# Hybrid Retrieval (BM25 + Dense)
from llama_index import VectorStoreIndex
index = VectorStoreIndex.from_documents(chunks)
retriever = index.as_retriever(
    similarity_top_k=20,    # Retrieve more for reranking
    mode="hybrid"            # BM25 + dense
)
```

### Phase 2: Add Reranking (Day 2)
```python
# Rerank top-20 to top-5
from llama_index.postprocessor import CohereRerank
reranker = CohereRerank(top_n=5)
query_engine = index.as_query_engine(
    similarity_top_k=20,
    node_postprocessors=[reranker]
)
```

### Phase 3: Optimize Chunking (Day 3-4)
```python
# If documents have structure
from langchain.text_splitter import MarkdownHeaderTextSplitter
md_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[("#", "h1"), ("##", "h2"), ("###", "h3")]
)

# If complex PDFs with tables
from llama_parse import LlamaParse
parser = LlamaParse(result_type="markdown")
documents = parser.load_data("complex.pdf")
```

**Expected Results**:
- Phase 1: Functional RAG (40-50% better than naive)
- Phase 2: High-quality RAG (+48% from reranking)
- Phase 3: Optimized RAG (additional 5-10%)

**Total time**: 3-4 days to production-ready RAG pipeline

## When to Stop Optimizing

**Stop when**:
- Retrieval precision@5 > 80% on test set
- User satisfaction > 90%
- Cost per query acceptable
- Marginal gains < effort cost

**Don't chase**:
- 100% precision (impossible with RAG)
- Every advanced technique (agentic retrieval, graph RAG, multi-modal)
- State-of-art papers (production needs differ from research)

**Focus on**:
- User experience (are they finding answers?)
- Cost efficiency (tokens, API calls, infrastructure)
- Maintainability (can you update the system?)

## Summary: The Decision Matrix

| Use Case | Loading | Chunking | Retrieval | Framework |
|----------|---------|----------|-----------|-----------|
| **Simple Q&A** | PyPDF | Recursive (512, 50) | Hybrid | LangChain |
| **Complex PDFs** | LlamaParse | Page-level | Hybrid + Rerank | LlamaIndex |
| **Structured docs** | Any | MarkdownHeaderTextSplitter | Hybrid | Either |
| **Enterprise** | LlamaIndex | Adaptive | Hybrid + Rerank + Filter | Both |
| **Financial/Legal** | LlamaParse | Page-level | Hybrid + Rerank | LlamaIndex |
| **Research papers** | LlamaParse | Semantic | Hybrid + Rerank | LlamaIndex |

## Key Takeaways

1. **Start with the baseline**: RecursiveCharacterTextSplitter (512, 50) + Hybrid retrieval
2. **Biggest wins first**: Structure-aware chunking (if applicable) → Hybrid search → Reranking
3. **Hierarchy of impact**: Chunking (~60%) > Retrieval > Parsing > Embeddings > LLM
4. **Evaluate on your data**: Test queries, measure precision/recall, iterate
5. **Match tool to complexity**: Simple docs → simple tools, complex docs → sophisticated tools
6. **Production baseline (2025)**: Hybrid + reranking = 40-50% improvement
7. **Don't chase perfection**: 80% precision often good enough, focus on user experience

## Resources

All sources and links from individual research documents:
- Document Loading: See `/01-discovery/S1-rapid/document-loading.md`
- Text Chunking: See `/01-discovery/S1-rapid/text-chunking.md`
- Retrieval Strategies: See `/01-discovery/S1-rapid/retrieval-strategies.md`
- Framework Comparison: See `/01-discovery/S1-rapid/framework-comparison.md`
