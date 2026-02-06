# S1 Recommendation: Network Flow Libraries

## Quick Decision Matrix

| Library | Best For | Performance Tier | Ease of Use | License |
|---------|----------|------------------|-------------|---------|
| **NetworkX** | Prototyping, research, <100K nodes | ⭐ Slowest | ⭐⭐⭐ Easiest | BSD (permissive) |
| **igraph** | R users, mid-scale (100K-1M nodes) | ⭐⭐ Fast | ⭐⭐ Moderate | GPL-2.0 |
| **OR-Tools** | Production logistics, optimization | ⭐⭐⭐ Very Fast | ⭐ Complex | Apache 2.0 |
| **graph-tool** | Research, >1M nodes, max performance | ⭐⭐⭐⭐ Fastest | ⭐ Difficult | LGPL-3.0 |

## Primary Recommendation by Use Case

### "I need to prototype a supply chain model for a presentation next week"
→ **NetworkX**
Clean API, excellent docs, fast development velocity. Performance won't matter for demo data.

### "I'm building a production routing system for a logistics company"
→ **OR-Tools**
Battle-tested at Google scale. Worth the learning curve for performance and reliability.

### "I'm analyzing Twitter follower graphs with 10M users"
→ **graph-tool**
Only library that will handle this scale without choking. Be prepared to debug installation.

### "I'm a statistician who primarily works in R"
→ **igraph**
Dual Python/R API means you learn once, use everywhere. Strong academic community.

## The Performance-Complexity Trade-off

```
Ease of Use  ←→  Raw Performance
NetworkX ← igraph ← OR-Tools ← graph-tool
```

**Key insight:** Most projects start with NetworkX, then migrate to OR-Tools (if building products) or graph-tool (if doing research) when performance becomes critical. igraph sits in the middle for R users or those wanting better-than-NetworkX speed without extreme complexity.

## Red Flags

**Don't use NetworkX if:**
- Processing >100K nodes repeatedly in production
- Flow computations must complete in <100ms
- Building commercial logistics software

**Don't use OR-Tools if:**
- Just exploring graph properties (centrality, clustering, visualization)
- Team has no operations research background
- Problem is simple enough for NetworkX

**Don't use graph-tool if:**
- Graph size <100K nodes (overkill)
- Installation/deployment complexity is a blocker
- Need operations research features (assignment, scheduling)

**Don't use igraph if:**
- Pure Python preferred (NetworkX is cleaner)
- Already invested in NetworkX ecosystem
- GPL license problematic for your project

## Strategic Guidance

1. **Start with NetworkX** for prototyping (always)
2. **Benchmark with real data** before committing to migration
3. **Consider OR-Tools** if building products (Apache license, Google support)
4. **Consider graph-tool** if doing research (LGPL license, academic focus)
5. **Consider igraph** if R is part of your workflow

**The 90% rule:** NetworkX solves 90% of network flow problems people actually encounter. Only move to specialized tools when you've proven NetworkX won't work.
