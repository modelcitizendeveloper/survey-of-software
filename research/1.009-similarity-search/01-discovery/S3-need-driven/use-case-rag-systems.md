# Use Case: RAG System Builders

## Who Needs This

**User Persona:** LLM application developers building retrieval-augmented generation (RAG) systems

**Context:**
- Embedding documents/code/knowledge bases into vector databases
- Querying for top-K most relevant chunks to augment LLM prompts
- Scale: 10K to 100M+ document chunks
- Latency target: <100ms for real-time chat, <1s for batch processing

**Examples:**
- AI chatbots answering questions from internal documentation
- Code assistants retrieving relevant functions/classes
- Customer support systems finding similar past tickets
- Legal research tools querying case law databases

## Why They Need Similarity Search

**Problem:** LLMs have limited context windows (8K-128K tokens). Can't fit entire knowledge base in prompt.

**Solution:**
1. Embed documents/chunks into vectors (e.g., BERT, OpenAI embeddings)
2. Index vectors in similarity search library
3. At query time, retrieve top-K most similar chunks
4. Inject retrieved chunks into LLM prompt

**Critical requirements:**
- **Recall:** High recall (>95%) to avoid missing relevant documents
- **Latency:** Sub-100ms for interactive chat
- **Scale:** 1M+ chunks for enterprise knowledge bases
- **Accuracy metric:** Cosine similarity (most embeddings use normalized vectors)

## Requirements Breakdown

### Must-Have
- ✅ Cosine similarity or inner-product search
- ✅ Handle 100-2048 dimensional embeddings (typical range)
- ✅ Scale to 1M+ vectors
- ✅ <100ms query latency (p95)
- ✅ >95% recall@10 (missing relevant docs breaks RAG)

### Nice-to-Have
- 🟡 GPU acceleration (batch embedding + search)
- 🟡 Incremental updates (add new documents without full rebuild)
- 🟡 Metadata filtering (e.g., "search only docs from 2024")
- 🟡 Hybrid search (vector + keyword BM25)

### Can Compromise
- ⚠️ Memory footprint (cloud GPUs have 24-80 GB VRAM)
- ⚠️ Build time (offline indexing acceptable)
- ⚠️ Exact search (95-99% recall sufficient)

## Library Recommendations

### Primary: FAISS (IVF or HNSW)

**Why FAISS:**
- Industry standard for RAG (used by LangChain, LlamaIndex, Haystack)
- GPU acceleration: Embed + search in single pipeline
- Proven at scale: Meta uses FAISS for 1.5T vectors
- Flexible accuracy/speed: IVF (fast) or HNSW (accurate)

**Index configuration:**
```
Option 1 (Speed): IndexIVFFlat
- nlist=1000 (for 1M vectors)
- nprobe=10-50
- QPS: 8000+, Recall: 95%

Option 2 (Accuracy): IndexHNSWFlat
- M=32, efConstruction=200, efSearch=100
- QPS: 6000, Recall: 99%

Option 3 (Memory): IndexIVFPQ
- nlist=1000, m=8, nbits=8
- Memory: 30 GB → 1 GB (32x compression)
- QPS: 15000, Recall: 94%
```

**Deployment pattern:**
- Vector DB wrappers: Milvus, Weaviate, Qdrant (FAISS backend)
- Self-hosted: FAISS + Redis/PostgreSQL for metadata

### Alternative: ScaNN (for Google Cloud)

**Why ScaNN:**
- Vertex AI Vector Search (managed service)
- Higher accuracy than FAISS for inner-product (98%+ recall)
- Auto-scaling, HA built-in

**When to choose:**
- Already on Google Cloud
- Need managed solution (no ops overhead)
- Budget for cloud service (~$200/month for 1M vectors)

**When NOT to choose:**
- Self-hosted deployment (FAISS easier)
- Multi-cloud or on-prem (vendor lock-in)

### Not Recommended: Annoy, datasketch

**Annoy:**
- ❌ Recall plateaus at ~93% (too low for RAG)
- ❌ No GPU support (FAISS 100x faster on batch)

**datasketch:**
- ❌ Designed for set similarity (Jaccard), not dense vectors
- ❌ No support for embeddings

## Real-World Example: Enterprise Chatbot

**Scenario:** Company with 50K internal documents, 2M chunks after splitting

**Requirements:**
- Latency: <50ms (interactive chat)
- Accuracy: >98% recall (critical for compliance questions)
- Updates: Daily (new docs added nightly)

**Solution:**
1. **Embedding:** OpenAI text-embedding-3 (1536-dim)
2. **Index:** FAISS HNSW (M=32, efSearch=200)
3. **Hardware:** 1x NVIDIA A10G (24 GB VRAM)
4. **Memory:** 2M × 1536 × 4 bytes = 12 GB (fits in VRAM)
5. **Update strategy:** Rebuild index nightly (takes 20 min)

**Results:**
- Query latency: 8ms (p50), 25ms (p95)
- Recall@10: 99.2%
- Cost: $1.50/hour GPU × 730 hours/month = $1095/month

**Cost optimization:** Use FAISS IVFPQ → 1.5 GB index → CPU-only (NVIDIA T4, $0.35/hour = $255/month)

## Common Pitfalls

### Pitfall 1: Using Default Flat Index
**Problem:** Flat index = O(N) search, too slow for >10K vectors
**Solution:** Use IVF or HNSW from the start

### Pitfall 2: Ignoring Recall Metrics
**Problem:** Fast but inaccurate index misses relevant docs → LLM hallucinates
**Solution:** Benchmark recall on held-out queries, target >95%

### Pitfall 3: Storing Embeddings Separately from Metadata
**Problem:** N+1 query problem (fetch IDs from FAISS, then fetch metadata from DB)
**Solution:** Use vector DB (Milvus, Weaviate) with metadata co-location

### Pitfall 4: Not Normalizing Vectors
**Problem:** Using inner-product without normalization → biased by vector magnitude
**Solution:** L2-normalize embeddings → cosine similarity

## Validation Checklist

Before deploying RAG with similarity search:
- [ ] Benchmark recall@10 on 1000+ real queries (target >95%)
- [ ] Measure p95 latency under load (target <100ms)
- [ ] Test with embedding updates (ensure index rebuild is automated)
- [ ] Verify GPU memory fits index (or use PQ compression)
- [ ] A/B test LLM answer quality (vector search vs keyword search)

## Related Use Cases

- **Code search:** Similar to RAG, but code embeddings (CodeBERT, GraphCodeBERT)
- **Semantic search:** User queries → relevant documents (no LLM, just retrieval)
- **Question-answering:** FAQ matching, support ticket routing
