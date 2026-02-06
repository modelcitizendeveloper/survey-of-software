# S3 Need-Driven Discovery: Similarity Search Libraries

## Methodology

Start with WHO needs this and WHY, then match requirements to libraries. Reverse the typical tech-first approach—begin with user personas and their pain points.

## Research Approach

1. **Identify personas:** Who searches for similar items/documents?
2. **Extract requirements:** What matters most to each persona? (Speed, accuracy, scale, cost)
3. **Map to libraries:** Which library best fits each use case?
4. **Validate trade-offs:** What compromises are acceptable?

## Use Cases Covered

1. **RAG System Builders** - LLM developers building retrieval-augmented generation
2. **E-commerce Search Engineers** - Product search, visual similarity
3. **Data Deduplication Specialists** - ETL pipelines, record linkage
4. **Content Recommendation Systems** - Music, video, news personalization
5. **Research Data Scientists** - Academic/industrial similarity research

## Key Questions Per Use Case

- **Who** are they? (Role, context, constraints)
- **Why** do they need similarity search? (Problem being solved)
- **What** are their requirements? (Scale, latency, accuracy, budget)
- **Which** library fits best? (Primary + alternative recommendations)

## What S3 Discovers That S1/S2 Miss

- **S1:** Tells you WHAT libraries exist (features, benchmarks)
- **S2:** Tells you HOW they work (algorithms, architecture)
- **S3:** Tells you WHO needs each library and WHY (context-specific guidance)

**Example:** S2 says "FAISS PQ achieves 32x compression." S3 says "E-commerce engineers use FAISS PQ because 10M products × 768 dims = 30 GB RAM without compression, but only 1 GB with PQ—fits on a single server."

## Time Investment

- Per use case: ~10 min
- Recommendation synthesis: ~5 min
- **Total: ~55 minutes**
