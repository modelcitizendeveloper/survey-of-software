# Louvain Community Detection

## Overview

Louvain is the most widely-used modularity-based community detection algorithm. It's fast, produces high-quality results, and has become the de facto standard for moderate-sized graphs.

**Key Stats:**
- **Ecosystem:** NetworkX (16.5K GitHub stars), python-louvain (~1K stars)
- **Maintenance:** Active (NetworkX native implementation as of 3.x)
- **Performance:** O(n log n) time complexity
- **Output:** Non-overlapping, hierarchical communities

## When to Use

**Best for:**
- Networks with 1K-500K nodes
- Quick exploratory analysis
- When modularity optimization is the goal
- Standard NetworkX workflows

**Avoid when:**
- You need guaranteed well-connected communities (use Leiden instead)
- Networks have >1M nodes (consider GPU-accelerated Leiden)
- You require overlapping communities

## Strengths

1. **Speed:** Fast convergence on most graphs
2. **Quality:** High modularity scores in practice
3. **Integration:** Native NetworkX support, minimal dependencies
4. **Adoption:** Widely understood, easy to explain to stakeholders

## Limitations

1. **Disconnected communities:** May produce poorly connected or even disconnected communities (up to 16% in some graphs)
2. **Resolution limit:** Struggles with very small or very large communities
3. **Non-deterministic:** Random initialization means results vary between runs
4. **Superseded:** Leiden algorithm addresses Louvain's major defects

## Ecosystem Maturity

**Production-ready.** Used in major production systems worldwide. Well-documented, stable API.

**Recommendation tier:** **First choice for prototyping**, but validate with Leiden for production.

## Sources

- [NetworkX 3.6.1 Documentation - louvain_communities](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.community.louvain.louvain_communities.html)
- [python-louvain GitHub](https://github.com/taynaud/python-louvain)
- [From Louvain to Leiden: guaranteeing well-connected communities](https://www.nature.com/articles/s41598-019-41695-z)
- [NVIDIA Technical Blog: GPU-Powered Leiden](https://developer.nvidia.com/blog/how-to-accelerate-community-detection-in-python-using-gpu-powered-leiden/)
