# Use Case: Academic Research Assistant

## Scenario

**Organization:** University research lab (computational biology)
**Problem:** Researchers spend weeks reading papers to understand state-of-the-art, identify methods, find citations
**Goal:** Build AI research assistant to query 10K+ papers, answer complex questions requiring synthesis across multiple documents

## Requirements

### Must-Have Features

✅ **Multi-document queries** - "What methods do papers A, B, C use for protein folding?"
✅ **Citation tracking** - Every claim must cite source paper
✅ **Complex query decomposition** - Break "Compare X vs Y across 5 papers" into sub-questions
✅ **Accuracy over speed** - Hallucinations unacceptable (publication-grade answers)
✅ **PDF parsing** - Handle complex academic PDFs (tables, figures, equations, references)

### Nice-to-Have Features

⚪ **Knowledge graph** - Entity-relationship extraction (methods, authors, findings)
⚪ **Comparative analysis** - Side-by-side comparison of papers
⚪ **Timeline queries** - "How has X evolved from 2015-2025?"
⚪ **Export citations** - Generate BibTeX for papers cited in answer

### Constraints

📊 **Scale:** 10,000-50,000 papers (growing continuously)
💰 **Budget:** Moderate (academic grant funding, prefer cost-effective)
⏱️ **Latency:** 10-30 seconds acceptable (complex queries take time)
🔒 **Accuracy:** **Critical** - Wrong answers waste weeks of research time
🛠️ **Team:** 1 PhD student + 1 research engineer

### Success Criteria

- 90%+ accuracy for factual questions
- Proper citation for every claim
- Save researchers 20+ hours/week on literature review
- Complex query handling (multi-part questions)

---

## Framework Evaluation

### LangChain - Fit Analysis

**Must-Haves:**
- ⚠️ **Multi-document queries**: Possible via custom chains, not optimized
- ✅ **Citation tracking**: `RetrievalQAWithSourcesChain` returns sources
- ✅ **Query decomposition**: Can implement via LangGraph or custom chain
- ✅ **Accuracy**: Can improve with careful prompting and retrieval
- ⚠️ **PDF parsing**: Basic (PyPDF2), struggles with tables/figures

**Nice-to-Haves:**
- ⚪ **Knowledge graph**: Can integrate with Neo4j, but custom implementation
- ⚪ **Comparative analysis**: Custom chain required
- ⚪ **Timeline queries**: Custom implementation
- ⚪ **Export citations**: Custom parsing of sources

**Constraints:**
- 💰 **Budget**: 2.4k tokens/query × complex queries = moderate cost (acceptable for research)
- ⏱️ **Latency**: 10ms overhead negligible when query takes 10-30 sec
- 🔒 **Accuracy**: Depends on retrieval quality and prompt engineering
- 🛠️ **Team**: Large community helps PhD student/engineer

**Fit Score:** 72/100

**Strengths:**
- Ecosystem has academic Q&A examples
- LangGraph enables complex multi-step queries
- Large community for troubleshooting

**Weaknesses:**
- Not optimized for multi-document synthesis
- Basic PDF parsing (poor for academic papers)
- Query decomposition requires custom work

**Implementation Complexity:** Medium-High (50-80 LOC for multi-document reasoning, custom decomposition)

---

### LlamaIndex - Fit Analysis

**Must-Haves:**
- ✅✅ **Multi-document queries**: **Sub-Question Query Engine** purpose-built for this
- ✅ **Citation tracking**: Returns source documents with responses
- ✅✅ **Query decomposition**: **Built-in sub-question decomposition**
- ✅ **Accuracy**: RAG-optimized retrieval improves precision
- ✅✅ **PDF parsing**: **LlamaParse (enterprise)** handles tables, figures, equations

**Nice-to-Haves:**
- ✅ **Knowledge graph**: **Knowledge Graph Index** built-in
- ✅ **Comparative analysis**: Sub-question engine supports comparative queries naturally
- ⚪ **Timeline queries**: Can implement via metadata filtering
- ⚪ **Export citations**: Custom parsing

**Constraints:**
- 💰 **Budget**: 1.6k tokens/query + LlamaParse cost → Moderate (LlamaParse adds cost but acceptable)
- ⏱️ **Latency**: 6ms overhead negligible for 10-30 sec queries
- 🔒 **Accuracy**: Best RAG retrieval performance (20-30% faster, more precise)
- 🛠️ **Team**: Good documentation for academic use cases

**Fit Score:** 88/100

**Strengths:**
- **Sub-Question Query Engine**: Perfect for "compare X vs Y" queries
- **Knowledge Graph Index**: Entity-relationship queries supported
- **LlamaParse**: Best PDF parsing for complex academic papers
- **RAG-optimized**: Data-centric design fits research perfectly

**Weaknesses:**
- Smaller community for academic RAG (but growing)
- LlamaParse adds cost (though mitigated by lower token usage)

**Implementation Complexity:** Low-Medium (30-40 LOC with built-in sub-question engine and knowledge graph)

---

### Haystack - Fit Analysis

**Must-Haves:**
- ⚠️ **Multi-document queries**: Possible via custom pipeline, not optimized
- ✅ **Citation tracking**: Pipeline returns sources
- ⚠️ **Query decomposition**: Custom pipeline branching required
- ✅ **Accuracy**: Can achieve with hybrid search (dense + sparse)
- ⚠️ **PDF parsing**: Basic converters, struggles with complex layouts

**Nice-to-Haves:**
- ⚪ **Knowledge graph**: Custom integration with graph databases
- ⚪ **Comparative analysis**: Custom pipeline
- ⚪ **Timeline queries**: Metadata filtering supported
- ⚪ **Export citations**: Custom

**Constraints:**
- 💰 **Budget**: 1.57k tokens/query → Best cost (though not critical for research use case)
- ⏱️ **Latency**: 5.9ms overhead negligible
- 🔒 **Accuracy**: Hybrid search helps precision
- 🛠️ **Team**: Smaller community, steeper learning for academic use case

**Fit Score:** 70/100

**Strengths:**
- Best cost and latency (though not primary concerns here)
- Hybrid search good for academic precision
- Production-ready if scaling to departmental use

**Weaknesses:**
- No built-in multi-document or query decomposition
- Basic PDF parsing (critical gap for academic papers)
- Requires significant custom work for complex queries

**Implementation Complexity:** High (80-100 LOC for multi-document reasoning, decomposition, custom PDF parsing)

---

## Comparison Matrix

| Requirement | LangChain | LlamaIndex | Haystack |
|-------------|-----------|------------|----------|
| **Multi-document queries** | ⚠️ Custom | ✅✅ Sub-Question | ⚠️ Custom |
| **Query decomposition** | ⚠️ LangGraph | ✅✅ Built-in | ⚠️ Custom |
| **PDF parsing (complex)** | ⚠️ Basic | ✅✅ LlamaParse | ⚠️ Basic |
| **Knowledge graph** | ⚪ Custom | ✅✅ Built-in | ⚪ Custom |
| **Citation tracking** | ✅ | ✅ | ✅ |
| **Accuracy** | ✅ | ✅✅ Best retrieval | ✅ Hybrid search |
| **Cost** | $2.40/query | $1.60/query + LlamaParse | $1.57/query |
| **Implementation (LOC)** | 50-80 | **30-40** | 80-100 |
| **Fit Score** | 72/100 | **88/100** | 70/100 |

---

## Recommendation

### Primary: **LlamaIndex**

**Fit: 88/100**

**Rationale:**

For academic research assistance, **LlamaIndex is purpose-built**:

1. **Sub-Question Query Engine** = killer feature for research
   - "Compare protein folding methods in AlphaFold vs RoseTTAFold" → automatically decomposes into:
     - Sub-Q1: "What protein folding methods does AlphaFold use?"
     - Sub-Q2: "What methods does RoseTTAFold use?"
     - Synthesis: Compare results
   - **Built-in**, not custom development

2. **LlamaParse** = Best PDF parsing for academic papers
   - Handles tables, figures, equations, multi-column layouts
   - Critical for computational biology papers (lots of data tables)
   - Competitors use basic PyPDF2 (fails on complex layouts)

3. **Knowledge Graph Index** = Natural fit for academic queries
   - Extract entities (methods, proteins, authors)
   - Relationship queries: "Which papers use X method for Y problem?"
   - Semantic + structured retrieval

4. **RAG-optimized performance**
   - 20-30% faster queries than LangChain
   - More precise retrieval = fewer hallucinations

5. **Lowest implementation complexity**
   - 30-40 LOC vs 50-80 (LangChain) or 80-100 (Haystack)
   - PhD student can implement without deep ML engineering

**Cost Consideration:**
- Base: $1.60/query (33% cheaper than LangChain)
- LlamaParse adds ~$0.50/document during indexing (one-time)
- Total: Still cheaper than LangChain at query time

**ROI:**
- **Time saved**: 20 hours/week × $50/hr PhD time = $1,000/week = $52K/year
- **System cost**: $5-10K/year (including LlamaParse)
- **Payback**: < 1 week

**Trade-off Accepted:** None significant. LlamaIndex wins on features, cost, and implementation ease for this use case.

---

## Alternative: **LangChain** (if already in ecosystem)

**Fit: 72/100**

If lab already uses LangChain for other projects:

- Can implement multi-document via LangGraph (more work)
- Large community for troubleshooting
- Adequate for research needs (not optimal)

**Trade-off:** More engineering time, higher cost, worse PDF parsing.

---

## Not Recommended: **Haystack** (for this use case)

**Fit: 70/100**

Haystack's strengths (production, cost) don't matter for research:

- Academic use case doesn't need K8s deployment
- Latency already acceptable (10-30 sec)
- Cost savings ($1.57 vs $1.60) negligible
- Missing features (no query decomposition, basic PDF parsing) are critical gaps

---

## Implementation Estimate

### LlamaIndex (Recommended)

**MVP (Basic Multi-Doc Q&A):** 2-3 days
- PDF ingestion with LlamaParse: 0.5 days
- Vector index setup: 0.5 days
- Sub-question query engine: 0.5 days
- Testing: 1 day

**Advanced Features:** +1-2 weeks
- Knowledge graph index: 3-4 days
- Comparative analysis refinement: 2-3 days
- Citation export: 2 days

**Total:** 2-3 weeks to full-featured research assistant

### Cost Breakdown (Annual)

**Assumptions:** 100 queries/day, 20 work days/month, 10K papers indexed

- **LlamaParse (one-time indexing):** ~$5,000 (10K papers × $0.50/paper)
- **Query API costs:** $1.60 × 100 queries/day × 20 days/month × 12 months = **$38,400/year**
- **Hosting (vector DB):** $1,200-2,400/year
- **Development:** $10,000 (2-3 weeks × PhD student + engineer)
- **Maintenance:** $3,000/year

**Total Year 1:** ~$58,000
**Total Year 2+:** ~$43,000/year (no re-indexing, no development)

**ROI:**
- Researchers save 20 hours/week × $50/hr = $1,000/week = **$52,000/year**
- **Payback: ~1 year** (Year 2+ has positive ROI)

---

## Key Insight

For complex, multi-document queries requiring decomposition and synthesis, **specialized RAG features matter more than general-purpose orchestration**.

LlamaIndex's sub-question query engine and LlamaParse are **architectural advantages** that LangChain and Haystack can't match without substantial custom development.

**S3 validates S2's insight**: "LlamaIndex wins for RAG-specialized use cases."

**S3 contradicts S1**: Popularity doesn't predict fit for specialized academic needs. LangChain's 124K stars don't help with query decomposition.

---

## Publication Note

If this research leads to publications, LlamaIndex's citation tracking ensures every claim in the paper can be traced back to source documents—critical for academic integrity.
