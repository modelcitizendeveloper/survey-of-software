# Infomap Community Detection

## Overview

Infomap uses information theory to detect communities by minimizing the description length of a random walker's path through the network. Based on the Map Equation framework, it's both theoretically rigorous and highly performant.

**Key Stats:**
- **Ecosystem:** mapequation.org (official), Python API via PyPI
- **Maintenance:** Active (2024 ACM Computing Surveys tutorial published)
- **Performance:** O(m) time complexity, handles millions of nodes in minutes
- **Output:** Hierarchical, multi-level, overlapping communities supported

## When to Use

**Best for:**
- Directed or weighted networks (exploits flow information)
- When network dynamics matter (random walk = information flow)
- Hierarchical community structure discovery
- Academic research with strong theoretical requirements

**Avoid when:**
- Simple undirected, unweighted graphs (Louvain may be faster)
- You need purely local/greedy optimization
- Interpretability is more important than theoretical rigor

## Strengths

1. **Theoretical rigor:** Information-theoretic foundation with strong guarantees
2. **Flexibility:** Handles directed, weighted, temporal, multiplex, and memory networks
3. **Speed:** Classifies millions of nodes in minutes
4. **Hierarchical output:** Multi-level and overlapping communities
5. **Tooling:** Web app (Infomap Online), Python API, pre-compiled binaries

## Limitations

1. **Complexity:** Harder to explain to non-technical stakeholders than Louvain
2. **Hyperparameters:** More tuning options = more decisions
3. **Overkill:** May be unnecessarily complex for simple graphs
4. **Learning curve:** Steeper than modularity-based methods

## Access Methods

1. **Python API:** `pip install infomap` (PyPI)
2. **Web Application:** Infomap Online (browser-based, data stays local)
3. **Binaries:** Pre-compiled for Windows, Ubuntu, macOS
4. **Source:** C++ implementation available

## Ecosystem Maturity

**Production-ready.** Used in academic and industry applications. Well-documented, actively maintained by mapequation.org team.

**Recommendation tier:** **Best for directed/weighted networks**, overkill for simple graphs.

## Sources

- [Infomap - Network community detection](https://www.mapequation.org/infomap/)
- [Community Detection with the Map Equation and Infomap (ACM Computing Surveys)](https://dl.acm.org/doi/10.1145/3779648)
- [arXiv: Community Detection with the Map Equation](https://arxiv.org/abs/2311.04036)
- [MapEquation.org](https://www.mapequation.org/)
- [Community Detection with Louvain and Infomap (Statworx)](https://www.statworx.com/en/content-hub/blog/community-detection-with-louvain-and-infomap)
