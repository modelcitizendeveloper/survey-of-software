# Use Case: Academic Researchers (Information Retrieval)

## Who Needs This

**Persona**: PhD students, postdocs, or faculty conducting research in information retrieval (IR), natural language processing (NLP), or search-related fields.

**Context**:
- Publishing papers at ACL, SIGIR, EMNLP, WSDM conferences
- Need reproducible experiments on standard datasets (MS MARCO, TREC, etc.)
- Working with large corpora: 1M-100M documents
- Comparing retrieval algorithms: BM25, BM25+, neural retrieval, hybrid approaches
- Using Python for experiments (Jupyter notebooks, research scripts)

**Team size**: Individual researchers or 2-5 person research groups

**Budget**: Academic/research grants, university computing clusters

---

## Why They Need Full-Text Search Libraries

**Primary problem**: Reproducible information retrieval experiments require stable, well-documented libraries with standard IR methods.

**Research workflow**:
1. Load standard dataset (MS MARCO, BEIR, TREC)
2. Build search index with specific algorithm (BM25, BM25+)
3. Run evaluation queries, measure metrics (MAP, NDCG, MRR)
4. Compare against baselines from published papers
5. Write paper with reproducible results

**Why NOT build from scratch**:
- **Reproducibility crisis** - If you implement BM25 yourself, how do reviewers know it's correct?
- **Baseline comparisons** - Need to match published baseline scores exactly
- **Time constraints** - PhD is 4-5 years; can't spend 6 months building IR infrastructure
- **Community standards** - Papers must compare against established implementations

---

## Their Requirements

### Reproducibility Requirements (CRITICAL)
- **Standard algorithms** - BM25 must match Lucene/Anserini implementation
- **Documented parameters** - k1, b values must be explicit
- **Version control** - Results must reproduce with same library version
- **Baseline scores** - Library must report known scores on standard datasets

### Scale Requirements
- **Datasets**: 1M-100M documents (MS MARCO: 8.8M, TREC: varies)
- **Query volume**: Batch evaluation (not real-time), 1K-10K test queries
- **Index size**: 10GB-1TB (depending on corpus)

### Feature Requirements
1. **BM25 variants** - BM25, BM25+, BM25F
2. **Hybrid search** - Combine keyword (BM25) + neural retrieval (dense vectors)
3. **Standard datasets** - Pre-built indexes for MS MARCO, BEIR, TREC
4. **Evaluation metrics** - MAP, NDCG@k, MRR, Recall@k built-in
5. **Query expansion** - RM3, PRF for advanced retrieval

### Infrastructure Constraints
- **University clusters** - May have GPU access, large memory nodes
- **Notebook-friendly** - Work in Jupyter for experiments
- **Docker support** - Reproducible environments

---

## Library Selection Criteria (From S1)

### Top Priority: Academic Credibility

**Decision rule**: Library must be **cited in published papers** with reproducible baselines.

### Evaluation Against S1 Libraries

| Library | Fits? | Why / Why Not |
|---------|-------|---------------|
| **Pyserini** | ✅ Perfect | Built by academic IR group (Waterloo), 100+ citations, BM25 baselines for all standard datasets, hybrid search support |
| **Xapian** | ⚠️ Maybe | Mature, but less common in academic IR papers, no standard dataset integrations |
| **Tantivy** | ❌ No | Industry-focused, not cited in academic papers, no IR evaluation tools |
| **Whoosh** | ❌ No | Educational use only, not suitable for research-grade experiments |
| **lunr.py** | ❌ No | Static sites only, not for research |

### Recommended Choice
**Primary**: **Pyserini**
- Built by University of Waterloo IR group (Jimmy Lin's lab)
- Cited in 100+ research papers (Google Scholar)
- Pre-built indexes for MS MARCO, BEIR, TREC (just download and run)
- Lucene-backed (industry-standard BM25 implementation)
- Hybrid search (BM25 + dense retrieval)
- Evaluation metrics built-in

**No competitive alternative** from S1 libraries for academic IR research.

---

## When to Consider Managed Services

**Generally NOT applicable** for academic research:

### Why Managed Services DON'T Fit
- **Reproducibility** - Algolia's algorithm is proprietary, can't publish "We used Algolia BM25"
- **Baselines** - No published baseline scores for Algolia on MS MARCO
- **Cost** - $200-500/month ongoing cost not suitable for research budgets (one-time grant ≠ recurring subscription)
- **Control** - Can't tweak algorithm parameters for experiments

### Exception: Industry Research Labs
- Google Research, Microsoft Research, Meta AI
- Use internal search systems for experiments
- Publish with proprietary baselines (less reproducible, but accepted from tier-1 labs)

---

## Real-World Examples

**Who uses Pyserini?**:
- **University research groups**: Waterloo, CMU, UMass, Edinburgh
- **PhD students**: IR dissertation research
- **Reproducibility studies**: "Can we reproduce Paper X's results?"

**Conferences where Pyserini is cited**:
- **SIGIR** (Information Retrieval)
- **EMNLP, ACL** (NLP conferences with IR tracks)
- **WSDM** (Web Search and Data Mining)
- **TREC** (Text Retrieval Conference)

**Published datasets with Pyserini baselines**:
- **MS MARCO** - 8.8M passages, BM25 baseline: MRR@10 = 0.184
- **BEIR** - 18 datasets, BM25 baselines for all
- **TREC-COVID** - COVID-19 literature search

---

## Academic Workflow Example (Context Only)

For understanding WHY Pyserini is essential (not HOW to use it):

**Typical research project**:
1. **Hypothesis**: "Combining BM25 with BERT re-ranking improves retrieval on medical queries"
2. **Baseline**: Pyserini BM25 on TREC-COVID (published score: NDCG@10 = 0.656)
3. **Experiment**: Run Pyserini BM25, re-rank top 100 with BERT
4. **Evaluation**: New NDCG@10 = 0.712 (+8.5% improvement)
5. **Paper**: "We improve upon Pyserini's BM25 baseline (Lin et al. 2021) by 8.5%"

**Key insight**: Research builds on published baselines. Pyserini provides those baselines.

---

## Success Metrics

How researchers know Pyserini (or any library) is suitable:

✅ **Good fit indicators**:
- Can reproduce published baseline scores exactly (±0.01 on metrics)
- Index builds complete in reasonable time (<24 hours)
- Evaluation metrics match paper's reported values
- Library is actively maintained (bugs fixed, new datasets added)
- Cited in >10 papers at top conferences

⚠️ **Warning signs to reconsider**:
- Can't reproduce baseline scores (implementation bug?)
- Library version changes break results (reproducibility nightmare)
- No community support (abandoned project = risky to build on)

---

## JVM Requirement Trade-off

Pyserini requires Java 21+ (JVM overhead).

**Why researchers accept this**:
- **Academic clusters have Java** - Not a barrier in university environments
- **Docker mitigates issues** - Reproducible environments with fixed Java version
- **Performance matters less** - Batch evaluation (not real-time), can wait hours for results
- **Lucene is standard** - Built on same engine as Elasticsearch, Solr (industry standard)

**Contrast with product developers** (from use-case-product-developers.md):
- Product devs avoid JVM (deployment complexity)
- Researchers embrace JVM (reproducibility via Docker + cluster availability)

---

## Validation Against S1 Findings

S1 noted:
- **Pyserini** = academic quality, hybrid search, billions of docs, JVM required
- **Rating**: ⭐⭐⭐⭐ (4/5) - "Best for: Academic research, large-scale"

**S3 validation**: Academic researchers are Pyserini's INTENDED audience:
- Need reproducibility (✅ Pyserini = cited baselines)
- Large scale (✅ Handles MS MARCO 8.8M passages)
- Hybrid search (✅ BM25 + neural retrieval)
- JVM acceptable (✅ University clusters support it)

**Alignment**: Pyserini was built BY academics FOR academics. Perfect fit.

**Gap identified**: For non-academic use cases (product development, static sites), Pyserini is overkill. S1's recommendation to use Tantivy or lunr.py for those use cases is validated by S3 persona analysis.
