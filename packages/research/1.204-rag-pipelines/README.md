# 1.204: RAG Pipelines

## Overview

**Category**: 1.200-209 AI & LLM Application Frameworks (Tier 1 - you run the code)
**Research Question**: How should developers build RAG (Retrieval-Augmented Generation) pipelines? What are the best practices for document loading, chunking, and retrieval in 2025?
**Status**: S1 Rapid Discovery completed
**Generic Use Cases**: Developers building document Q&A systems, teams implementing knowledge bases, enterprises deploying AI assistants over private data

## What This Research Covers

This research explores the three critical stages of RAG pipelines: document loading (getting data into the system), text chunking (breaking documents into retrievable pieces), and retrieval (finding relevant context for questions). These are the foundational components that determine RAG system accuracy.

**In Scope**:
- Document loading tools and strategies (PyPDF, Unstructured, LlamaParse)
- Text chunking approaches (fixed-size, recursive, semantic, structure-aware)
- Retrieval strategies (hybrid search, BM25, dense retrieval, reranking)
- Framework comparison for RAG (LangChain vs LlamaIndex)
- Performance benchmarks and best practices

**Out of Scope**:
- LLM orchestration frameworks (covered in 1.200)
- Vector databases (covered in 1.203)
- LLM evaluation (covered in 1.205)
- Specific client implementations (generic research only)

## Quick Start: What Should I Use?

**For most developers**: Start with RecursiveCharacterTextSplitter (512 tokens, 50 overlap) + Hybrid retrieval (BM25 + dense + reranking)

**For simple PDFs**: PyPDFLoader (fast, lightweight)
**For complex PDFs with tables**: LlamaParse (6s processing, best accuracy)
**For RAG-specialized framework**: LlamaIndex (35% better retrieval than general frameworks)
**For hybrid retrieval**: BM25 + dense embeddings + cross-encoder reranking (40-50% precision improvement)
**For document structure**: MarkdownHeaderTextSplitter or structure-aware chunking (often the biggest single improvement)

See `/01-discovery/S1-rapid/recommendation.md` for detailed decision framework.

## Key Findings (S1 Rapid Discovery)

### The RAG Pipeline Hierarchy of Impact

Research shows that component quality determines overall RAG accuracy in this order:

1. **Chunking strategy** (~60% of accuracy) - Not the embedding model, not the reranker, not the LLM
2. **Retrieval quality** (hybrid > dense-only by 40-50%)
3. **Document parsing** (garbage in = garbage out)
4. **Embedding model** (surprisingly less critical)
5. **LLM choice** (any modern LLM works if retrieval is good)

**Implication**: Spend time optimizing chunking and retrieval before upgrading your LLM or embeddings.

### Document Loading: 2025 State

**Top Tools**:

| Tool | Best For | Speed | Accuracy | Key Limitation |
|------|----------|-------|----------|----------------|
| **LlamaParse** | Complex PDFs with tables | ~6s per doc | 10/10 (highest rated) | Cloud-only, requires API |
| **PyPDF** | Simple text-based PDFs | Fast | Good for basic docs | Loses table structure |
| **Unstructured** | Complex layouts, OCR | Moderate | Declining (2025 reports) | Recent quality issues |
| **Docling** | Open-source alternative | Moderate | Good | Lacks form/handwriting support |
| **Reducto** | High-precision parsing | Moderate | 20% higher than average | Commercial |

**Key Finding (2025)**: LlamaParse dominates complex PDF parsing. PyPDF is fine for simple docs. Unstructured quality has declined recently. If you're still using PyPDF/PyMuPDF for complex documents, your RAG pipeline may be broken at the data layer.

**Document ingestion frameworks**:
- **LlamaIndex**: Best-in-class data ingestion with 160+ data connectors via LlamaHub
- **LangChain**: Flexible, customizable document loaders for specific logic

### Text Chunking: Strategies and Performance

**Recommended Starting Point (2025)**:
Always start with **RecursiveCharacterTextSplitter** (512 tokens, 50 overlap). This respects semantic boundaries (paragraphs → sentences → words) and works for 80% of RAG applications.

**Chunking Strategies Compared**:

| Strategy | When to Use | Performance vs Baseline | Complexity |
|----------|-------------|------------------------|------------|
| **Fixed-size** | Baseline only | Baseline (0%) | Simple |
| **RecursiveCharacterTextSplitter** | General-purpose start | Good baseline | Easy |
| **Structure-aware** (Markdown/HTML) | Documents with clear structure | Often biggest single improvement | Easy |
| **Semantic chunking** | Thematically coherent chunks needed | +2-3% recall vs recursive | Moderate |
| **Parent-child (Small-to-Large)** | Complex Q&A needing context | Best for deep questions | Complex |
| **Page-level** | Financial reports, legal docs | Best accuracy (NVIDIA 2024) | Very simple |

**Chunk Size Guidelines**:
- **256-512 tokens**: Fact-focused retrieval (Q&A, lookup)
- **512-1024 tokens**: Context-heavy tasks (summaries, analysis)
- **15% overlap**: NVIDIA found this optimal for 1024-token chunks
- **Smaller chunks**: Better precision, fragments context
- **Larger chunks**: Preserve meaning, dilute similarity scores

**Critical Finding**: Chunking strategy determines ~60% of RAG accuracy. The biggest and easiest improvement is switching from fixed-size to structure-aware splitting (MarkdownHeaderTextSplitter) if your content has clear structure.

**2025 Trend**: Late 2025 prediction is that production RAG systems will use agents to select chunking strategies dynamically based on document type and query.

### Retrieval: Hybrid is Standard in 2025

**Evolution**:
- **2023 (Naive)**: Dense retrieval only (embed query, find top-k by cosine similarity)
- **2025 (Standard)**: Hybrid retrieval + reranking

**The 2025 Standard Pipeline**:
```
1. BM25 (keyword search) → Catch exact term matches (dates, names, IDs)
2. Dense retrieval (embeddings) → Catch semantic matches
3. Reciprocal Rank Fusion (RRF) → Combine both rankings
4. Cross-encoder reranking → Optimize top candidates
5. Metadata filtering → Apply access control, date ranges
```

**Performance**:
- Hybrid retrieval: **40-50% precision improvement** vs dense-only
- Reranking: **Up to 48% quality improvement**, **25% token cost reduction**
- Combined: Hybrid + reranking delivers best-in-class retrieval

**Why BM25 + Dense Together**:
- **BM25**: Purely statistical keyword matching (fast, exact matches)
- **Dense**: Semantic understanding via embeddings (meaning, not just words)
- **Example**: Query "ROI for Q4 2025"
  - BM25 catches "Q4 2025" exact match (dense might miss specific quarter)
  - Dense catches "return on investment" as semantic match for "ROI"
  - Together: Best of both worlds

**Reranking**: After hybrid retrieval returns top-20 candidates, a cross-encoder model re-scores them for final top-5 selection. This is computationally expensive but dramatically improves relevance.

### Framework Comparison: LangChain vs LlamaIndex for RAG

| Dimension | LlamaIndex | LangChain |
|-----------|-----------|-----------|
| **RAG Specialization** | Purpose-built for RAG | General-purpose orchestration |
| **Document Ingestion** | Best-in-class (160+ connectors) | Flexible, customizable |
| **Retrieval Accuracy** | 35% boost (2025 benchmarks) | Good |
| **Retrieval Speed** | 40% faster in specific tests | Good |
| **Chunking Tools** | Sophisticated NodeParsers | RecursiveCharacterTextSplitter |
| **Best For** | Document-heavy RAG systems | Multi-step LLM workflows |
| **Learning Curve** | RAG-focused | Broader scope |

**Complementary Usage**: Many production teams use **LlamaIndex for ingestion & retrieval** + **LangChain for orchestration & agents**. LlamaIndex returns the most relevant docs, LangChain organizes the multi-step flow.

**Recommendation**:
- Pure RAG use case → **LlamaIndex** (specialized tooling, better performance)
- RAG + multi-agent workflows → **LangChain** (broader capabilities)
- RAG + orchestration needs → **Both** (use each for its strength)

### Production Best Practices (2025)

**The Practical Three-Stage Pipeline** (achieves 40-50% improvement over baseline):
1. **Hybrid retrieval** on semantic chunks (BM25 + dense search with RRF)
2. **Cross-encoder reranking** to identify most relevant chunks
3. **Metadata filtering** for compliance/access control

**Evaluation Metrics** (measure continuously):
- **Context relevancy**: Are retrieved chunks actually relevant?
- **Precision@K**: How many of top-K results are relevant?
- **Recall@K**: What % of all relevant docs are in top-K?
- **Test systematically**: Create evaluation datasets, vary one parameter at a time

**Common Mistakes to Avoid**:
1. **Using dense-only retrieval** (hybrid improves by 40-50%)
2. **Ignoring document structure** (structure-aware chunking often biggest win)
3. **Wrong chunk size** (too small = fragments, too large = dilutes)
4. **No overlap** (context split across chunks)
5. **No reranking** (missing 48% quality improvement)
6. **Poor document parsing** (LlamaParse vs PyPDF matters for complex docs)

## Research Deliverables

### S1 Rapid Discovery (Completed)

**Component Profiles**:
- `/01-discovery/S1-rapid/document-loading.md` - Parsing tools comparison (LlamaParse, PyPDF, Unstructured)
- `/01-discovery/S1-rapid/text-chunking.md` - Chunking strategies and performance
- `/01-discovery/S1-rapid/retrieval-strategies.md` - Hybrid search, BM25, dense, reranking

**Framework Comparison**:
- `/01-discovery/S1-rapid/framework-comparison.md` - LangChain vs LlamaIndex for RAG

**Recommendations**:
- `/01-discovery/S1-rapid/recommendation.md` - Decision framework for building RAG pipelines

**Domain Understanding**:
- `DOMAIN_EXPLAINER.md` - What are RAG pipelines and why they matter

## Key Questions Answered

1. **Which document loader?** LlamaParse for complex PDFs, PyPDF for simple docs, LlamaIndex for breadth (160+ connectors)
2. **Which chunking strategy?** RecursiveCharacterTextSplitter (512 tokens, 50 overlap) for 80% of cases; structure-aware for documents with headers
3. **Which retrieval approach?** Hybrid (BM25 + dense + RRF + reranking) is 2025 standard (40-50% better than dense-only)
4. **Chunk size?** 256-512 for factual Q&A, 512-1024 for context-heavy tasks
5. **LangChain or LlamaIndex?** LlamaIndex for RAG specialization (35% better), LangChain for broader workflows
6. **What matters most?** Chunking strategy (~60% of accuracy), then retrieval quality, then parsing
7. **When to use RAG?** Private documents, frequently changing knowledge, citation requirements, data too large for context window

## Cross-References

- **1.200** (LLM Orchestration Frameworks): RAG pipelines run INSIDE these frameworks
- **1.203** (Vector Databases): RAG retrieval USES vector databases (Pinecone, Chroma, etc.)
- **1.205** (LLM Evaluation): Measuring RAG quality with metrics like precision@K, recall@K
- **3.200** (LLM APIs): RAG augments prompts to THESE APIs (OpenAI, Anthropic, etc.)

## Market Trends (2025)

1. **Hybrid Retrieval Standard**: BM25 + dense + reranking now table stakes for production
2. **LlamaParse Dominance**: Clear leader for complex PDF parsing in 2025
3. **Semantic Chunking Emerging**: 2-3% better recall, growing adoption
4. **Agentic RAG**: LLMs dynamically selecting chunking strategies (late 2025 prediction)
5. **Graph RAG**: Knowledge graphs supplementing vector search for complex reasoning
6. **Multi-modal RAG**: Images, tables, charts as first-class citizens
7. **Fine-tuned Embeddings**: Domain-specific embedding models for better retrieval
8. **Evaluation Tooling**: Continuous monitoring of retrieval quality becoming standard

## Repository Structure

```
1.204-rag-pipelines/
├── README.md (this file)
├── DOMAIN_EXPLAINER.md (what are RAG pipelines, why they matter)
├── metadata.yaml (experiment tracking)
└── 01-discovery/
    └── S1-rapid/
        ├── document-loading.md (parsing tools comparison)
        ├── text-chunking.md (chunking strategies)
        ├── retrieval-strategies.md (hybrid search, reranking)
        ├── framework-comparison.md (LangChain vs LlamaIndex)
        └── recommendation.md (decision framework)
```

## Next Steps (Potential S2-S4)

### S2 Comprehensive (If Needed)
- Hands-on benchmarking of chunking strategies on real documents
- Performance testing of hybrid retrieval configurations
- Cost analysis (embedding costs, reranking costs, storage)
- Evaluation framework implementation (precision@K, recall@K)

### S3 Need-Driven (If Specific Client Need)
- Deep dive into domain-specific RAG (legal, medical, financial)
- Production deployment architecture with monitoring
- Custom embedding model fine-tuning for client data
- Multi-modal RAG implementation (images, tables)

### S4 Strategic (If Build Decision)
- Reference RAG pipeline implementation (production-ready)
- Evaluation and monitoring framework
- Cost optimization guide
- Team training materials

## Recommendations Summary

### By Use Case:
- **Simple document Q&A**: RecursiveCharacterTextSplitter + Hybrid retrieval
- **Complex PDFs (tables)**: LlamaParse + LlamaIndex
- **Structured documents (Markdown/HTML)**: MarkdownHeaderTextSplitter
- **Enterprise knowledge base**: LlamaIndex + hybrid search + reranking + metadata filtering
- **Multi-agent system with RAG**: LlamaIndex (retrieval) + LangChain (orchestration)

### By Document Type:
- **Simple text PDFs**: PyPDFLoader + RecursiveCharacterTextSplitter
- **Complex PDFs with tables**: LlamaParse + semantic chunking
- **Markdown/HTML**: Structure-aware splitters (MarkdownHeaderTextSplitter)
- **Financial reports/legal docs**: Page-level chunking (NVIDIA 2024 best accuracy)
- **Mixed content**: Unstructured + semantic chunking

### By Performance Requirements:
- **Baseline (fast start)**: RecursiveCharacterTextSplitter (512 tokens) + dense retrieval
- **Production (best quality)**: Structure-aware chunking + hybrid retrieval + reranking
- **Maximum accuracy**: Semantic chunking + hybrid search + cross-encoder reranking + metadata filtering

### By Team Expertise:
- **Beginner**: LangChain with RecursiveCharacterTextSplitter + dense retrieval (simplest)
- **Intermediate**: LlamaIndex with hybrid retrieval (best RAG-specific tooling)
- **Advanced**: Custom pipeline with dynamic chunking + graph RAG + multi-modal

## The 2025 Baseline RAG Pipeline

If starting a new RAG project today, this is the recommended baseline:

**Document Loading**:
- Simple PDFs → PyPDFLoader
- Complex PDFs → LlamaParse
- Multiple formats → LlamaIndex connectors

**Chunking**:
- No clear structure → RecursiveCharacterTextSplitter (512 tokens, 50 overlap)
- Markdown/HTML → MarkdownHeaderTextSplitter
- Financial/legal → Page-level chunking

**Retrieval**:
- BM25 + dense embeddings → Hybrid search with RRF
- Cross-encoder reranking → Top-K optimization
- Metadata filtering → Compliance/access control

**Framework**:
- RAG-focused → LlamaIndex (35% better retrieval)
- Broader orchestration → LangChain
- Both needs → Use both (LlamaIndex for retrieval, LangChain for agents)

**Evaluation**:
- Measure precision@K, recall@K, context relevancy
- Create test datasets from real user queries
- Vary one parameter at a time

**Expected Performance**:
- 40-50% precision improvement over naive (dense-only, fixed-size chunks)
- 2-3% additional boost from semantic chunking
- Up to 48% quality improvement from reranking

## Resources

### Document Parsing:
- LlamaParse: https://www.llamaindex.ai/llamaparse
- Unstructured: https://unstructured.io/
- PyPDF: https://pypdf.readthedocs.io/

### Frameworks:
- LlamaIndex: https://www.llamaindex.ai/
- LangChain: https://www.langchain.com/
- LlamaHub (connectors): https://llamahub.ai/

### Research & Benchmarks:
- NVIDIA Chunking Study (2024): https://developer.nvidia.com/blog/finding-the-best-chunking-strategy-for-accurate-ai-responses/
- Weaviate Chunking Guide: https://weaviate.io/blog/chunking-strategies-for-rag
- Pinecone Chunking Strategies: https://www.pinecone.io/learn/chunking-strategies/

### Retrieval & Reranking:
- Superlinked (Hybrid Search): https://superlinked.com/vectorhub/articles/optimizing-rag-with-hybrid-search-reranking
- LangChain Text Splitters: https://docs.langchain.com/oss/python/integrations/splitters

## Research Methodology

**S1 Rapid Discovery** conducted via:
- Web search for current state (2025-2026 sources)
- Performance benchmark analysis (NVIDIA, industry reports)
- Framework documentation review (LangChain, LlamaIndex)
- Production case study research
- Tool comparison analysis (LlamaParse, PyPDF, Unstructured)

**Time Investment**: ~90 minutes (within S1 60-90 minute target)
**Sources**: Official documentation, technical blogs, benchmarks, research papers
**Currency**: All data from 2024-2026 unless noted

## Conclusion

RAG pipelines transform LLMs from "smart but limited" to "smart and grounded in your data." The pipeline quality determines system accuracy through three critical stages:

1. **Document loading** - Use LlamaParse for complex PDFs, PyPDF for simple docs
2. **Chunking** - Strategy determines ~60% of accuracy; start with RecursiveCharacterTextSplitter, upgrade to structure-aware for biggest wins
3. **Retrieval** - Hybrid (BM25 + dense + reranking) outperforms naive dense-only by 40-50%

The 2025 standard is clear: hybrid retrieval with reranking is table stakes, LlamaParse dominates complex parsing, and chunking strategy matters more than most developers realize (60% of accuracy).

For most developers, the winning combination is:
- **LlamaIndex** for RAG-specialized ingestion and retrieval (35% better than general frameworks)
- **RecursiveCharacterTextSplitter** (512 tokens, 50 overlap) or structure-aware chunking
- **Hybrid retrieval** (BM25 + dense + RRF + reranking) for 40-50% precision improvement

Get the pipeline right, and RAG delivers accurate, cited answers from your knowledge. Get it wrong, and you've built an expensive hallucination machine that's broken at the data layer.

---

**Last Updated**: 2026-01-18 (S1 Rapid Discovery)
**Maintained By**: spawn-solutions research team
**MPSE Version**: v3.0
