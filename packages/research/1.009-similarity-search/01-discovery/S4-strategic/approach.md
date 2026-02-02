# S4 Strategic Selection: Similarity Search Libraries

## Methodology

Think beyond immediate technical fit—evaluate long-term viability, ecosystem health, and organizational alignment. Make decisions that remain sound 2-5 years from now.

## Research Approach

1. **Ecosystem maturity:** Community size, adoption, longevity
2. **Maintenance trajectory:** Release cadence, bug fixes, active development
3. **Vendor stability:** Corporate backing, open governance, roadmap
4. **Team expertise:** Learning curve, hiring pool, knowledge transfer
5. **Integration ecosystem:** Cloud services, vector DBs, tool compatibility
6. **Migration paths:** Ability to switch libraries if needs change

## Key Strategic Questions

- **Will this library exist in 5 years?** (Vendor stability, community health)
- **Can we hire for this?** (Talent availability, learning curve)
- **What's the total cost of ownership?** (Not just infrastructure, but eng time)
- **Is there an exit path?** (Avoid vendor lock-in)
- **Does this align with our org culture?** (Self-hosted vs managed, OSS vs proprietary)

## Libraries Analyzed

1. **FAISS** - Meta's production-grade library
2. **Annoy** - Spotify's lightweight solution
3. **ScaNN** - Google Research's SOTA library
4. **datasketch** - Community-maintained probabilistic library

## What S4 Discovers That S1/S2/S3 Miss

- **S1:** FAISS is faster (technical benchmark)
- **S2:** FAISS uses PQ compression (how it works)
- **S3:** RAG systems use FAISS (who and why)
- **S4:** Meta maintains FAISS actively, huge community, hiring is easy, but switching costs high

**Example:** ScaNN has best accuracy (S1), uses anisotropic quantization (S2), fits research use cases (S3), but **S4 reveals:** Google Cloud lock-in risk, smaller community, harder to hire, monorepo deployment complexity.

## Time Investment

- Per-library viability analysis: ~15 min
- Strategic recommendation: ~15 min
- **Total: ~75 minutes**

## Decision Framework

### Short-term (<1 year): S1-S3 dominate
- Pick fastest/cheapest/easiest for MVP

### Medium-term (1-3 years): S4 matters
- Community support, bug fixes, hiring

### Long-term (3-5 years): S4 critical
- Vendor stability, ecosystem evolution, migration costs

**Trade-off:** Sometimes the "best" library (S1/S2) isn't the "strategic" choice (S4)
