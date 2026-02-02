# S1 Recommendation: Quick Decision Guide

## Decision Tree (5-Minute Version)

### 1. What type of data are you searching?

**Sets or documents (text deduplication, Jaccard similarity)?**
→ **datasketch** (MinHash/LSH/SimHash)

**Dense vectors (embeddings, image features)?**
→ Continue to step 2

---

### 2. What's your dataset scale?

**<10K vectors**
→ **Annoy** (simplest, fastest to prototype)

**10K - 10M vectors**
→ **Annoy** (if simplicity preferred) or **FAISS** (if accuracy critical)

**>10M vectors or need GPU acceleration**
→ **FAISS**

---

### 3. What's your accuracy requirement?

**90-95% recall is acceptable**
→ **Annoy** (fast, simple)

**>95% recall required**
→ **FAISS** (production standard) or **ScaNN** (research-grade accuracy)

**>98% recall, inner-product metric**
→ **ScaNN**

---

## Quick Recommendations by Use Case

### RAG Systems (LLM retrieval)
**Primary:** FAISS (industry standard, GPU support)
**Alternative:** ScaNN (if Google Cloud, accuracy critical)

### Music/Content Recommendation
**Primary:** Annoy (Spotify's choice, proven at scale)
**Alternative:** FAISS (if dataset grows beyond 10M items)

### Document Deduplication
**Primary:** datasketch (MinHash/SimHash for text)
**Alternative:** FAISS (if using document embeddings instead of hashes)

### Image Search
**Primary:** FAISS (handles high-dimensional image embeddings)
**GPU option:** FAISS with CUDA acceleration

### Research/Experimentation
**Primary:** ScaNN (SOTA algorithms, best accuracy)
**Practical:** FAISS (broader community, more documentation)

---

## Common Combinations

- **FAISS + datasketch:** Dense vector search + duplicate detection
- **Annoy (prototype) → FAISS (production):** Start simple, scale when needed
- **ScaNN for high-recall + FAISS for speed:** Hybrid pipeline (accuracy-critical queries use ScaNN, bulk queries use FAISS)

---

## Red Flags to Avoid

❌ **Don't use FAISS for <10K vectors** (Annoy is faster to set up)
❌ **Don't use Annoy for >95% recall** (accuracy suffers, use FAISS/ScaNN)
❌ **Don't use datasketch for dense embeddings** (designed for sets, not continuous vectors)
❌ **Don't expect real-time updates** (all libraries optimize for batch index builds)

---

## When in Doubt

**Start with Annoy** (1 hour to working prototype)
**Graduate to FAISS** (when scale/accuracy demands it)
**Consult S2-comprehensive** (when you need feature-by-feature comparison)
