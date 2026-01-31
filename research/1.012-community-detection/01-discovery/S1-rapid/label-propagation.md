# Label Propagation Community Detection

## Overview

Label propagation is one of the fastest community detection algorithms, using a simple consensus-based approach where nodes adopt the most common label among their neighbors.

**Key Stats:**
- **Ecosystem:** NetworkX, NetworKit (C++ with Python bindings), igraph
- **Maintenance:** Active across multiple implementations
- **Performance:** Near-linear time O(m) where m = edges
- **Output:** Non-overlapping communities

## When to Use

**Best for:**
- Very large graphs (millions of nodes)
- When speed is critical and perfect accuracy is secondary
- Real-time or streaming graph analysis
- Initial rough clustering before refinement

**Avoid when:**
- You need deterministic results (highly non-deterministic)
- Network has unclear community structure (slow convergence)
- Quality metrics (modularity) must be maximized

## Strengths

1. **Extreme speed:** 700x faster than basic implementations, 1.4B edges/s (GVE-LPA)
2. **Scalability:** Handles billions of edges efficiently
3. **Simplicity:** Easy to understand and implement
4. **Flexibility:** Works on directed, weighted, and temporal networks

## Limitations

1. **Instability:** Highly sensitive to node ordering and random initialization
2. **Quality:** Lower modularity scores compared to Louvain/Leiden
3. **Convergence:** May oscillate indefinitely without convergence guarantees
4. **Trivial solutions:** Can collapse entire network into one community

## Algorithm Variants

**Recent improvements:**
- **LALPA (2025):** Node importance measures for stable, ordered updates
- **MILPA:** Best NMI performance in recent benchmarks
- **GVE-LPA:** Parallel implementation, outperforms FLPA by 1.4B edges/s

## Ecosystem Maturity

**Production-ready with caveats.** Fast enough for production at scale, but requires careful parameter tuning and result validation.

**Recommendation tier:** **Best for speed-critical large-scale analysis**, not for high-quality partitioning.

## Sources

- [Large network community detection by fast label propagation](https://www.nature.com/articles/s41598-023-29610-z)
- [Hypermode: Top Community Detection Algorithms Compared](https://hypermode.com/blog/community-detection-algorithms)
- [GVE-LPA: Fast Label Propagation Algorithm](https://arxiv.org/html/2312.08140v5)
- [Label Acceptance based label propagation algorithm](https://www.sciencedirect.com/science/article/abs/pii/S030645732500514X)
