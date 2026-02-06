# 1.006 Graph Search Libraries - Discovery Table of Contents

## S1: Rapid Discovery (WHAT libraries exist?)

**Goal**: Quick comparison for decision-making

- [Approach](S1-rapid/approach.md) - Research methodology
- [NetworkX](S1-rapid/networkx.md) - Pure Python, comprehensive, easy to use
- [rustworkx](S1-rapid/rustworkx.md) - Rust-based, high performance, Apache-2.0
- [graph-tool](S1-rapid/graph-tool.md) - C++ academic powerhouse, installation complex
- [igraph](S1-rapid/igraph.md) - C cross-platform library, good balance
- [scipy.csgraph](S1-rapid/scipy-csgraph.md) - SciPy sparse matrix approach, lightweight
- [Recommendation](S1-rapid/recommendation.md) - **Decision matrix and top picks**

**TLDR**: Use NetworkX (easy), upgrade to rustworkx (fast + permissive license) if needed

## S2: Comprehensive Discovery (HOW do they work?)

**Goal**: Technical deep-dive for understanding implementation

- [Approach](S2-comprehensive/approach.md) - Analysis methodology
- [NetworkX](S2-comprehensive/networkx.md) - Pure Python architecture, algorithm implementations
- [rustworkx](S2-comprehensive/rustworkx.md) - Rust + PyO3, petgraph-based, performance analysis
- [graph-tool](S2-comprehensive/graph-tool.md) - C++ + Boost, property maps, template optimization
- [igraph](S2-comprehensive/igraph.md) - C core, Python bindings, cross-language design
- [scipy.csgraph](S2-comprehensive/scipy-csgraph.md) - Sparse matrix representation, BLAS integration
- [Feature Comparison](S2-comprehensive/feature-comparison.md) - **Side-by-side comparison tables**
- [Recommendation](S2-comprehensive/recommendation.md) - **Technical decision guidance**

**TLDR**: NetworkX (readable), rustworkx (fast Rust), graph-tool (fastest C++), igraph (balanced C), scipy.csgraph (NumPy stack)

## S3: Need-Driven Discovery (WHO needs this + WHY?)

**Goal**: Understand real-world use cases and user needs

- [Approach](S3-need-driven/approach.md) - Persona identification methodology
- [Game Developers](S3-need-driven/use-case-game-developers.md) - NPC pathfinding, level validation
- [Robotics Engineers](S3-need-driven/use-case-robotics-engineers.md) - Robot motion planning, ROS integration
- [Data Scientists](S3-need-driven/use-case-data-scientists.md) - Network analysis, centrality, community detection
- [Logistics Optimization](S3-need-driven/use-case-logistics-optimization.md) - Route optimization, VRP, supply chain
- [Recommendation](S3-need-driven/recommendation.md) - **WHO should use WHAT and WHY**

**TLDR**: Python for data science (production), prototyping for game dev/robotics (C++ for production)

## S4: Strategic Discovery (WHICH to choose long-term?)

**Goal**: Long-term viability, ecosystem fit, strategic trade-offs

- [Approach](S4-strategic/approach.md) - Strategic evaluation methodology
- [Recommendation](S4-strategic/recommendation.md) - **10-year outlook, migration paths, ecosystem fit**

**TLDR**: NetworkX (safest bet), rustworkx (commercial + performance), igraph (cross-platform)

## Summary Recommendations

### By Use Case

| Use Case | Library | Rationale |
|----------|---------|-----------|
| **Learning/Prototyping** | NetworkX | Easiest, most Pythonic |
| **Data Science (Small)** | NetworkX | Comprehensive, well-integrated |
| **Data Science (Large)** | igraph | Performance + ease of use |
| **Commercial Products** | rustworkx | Apache-2.0 + performance |
| **Maximum Performance** | graph-tool | Fastest (if Linux acceptable) |
| **SciPy Stack** | scipy.csgraph | No extra dependency, fast |
| **Game Dev Tools** | NetworkX | A* support, easy for designers |
| **Robotics Research** | NetworkX | ROS integration, prototyping |
| **Logistics APIs** | rustworkx | Performance + commercial license |

### Quick Decision Tree

```
Do you need A*?
├─ YES
│  ├─ Performance critical? → rustworkx
│  └─ Ease of use priority? → NetworkX
│
└─ NO (Dijkstra sufficient)
   ├─ Already using SciPy? → scipy.csgraph
   ├─ Maximum performance? → graph-tool (Linux) or rustworkx
   └─ Balanced needs? → igraph or NetworkX
```

### Performance Comparison (10K nodes)

| Library | A* | Dijkstra | Install | License |
|---------|-----|----------|---------|---------|
| **NetworkX** | 15ms | 12ms | ⭐⭐⭐⭐⭐ | BSD-3 |
| **rustworkx** | 105μs | 125μs | ⭐⭐⭐⭐ | Apache-2.0 |
| **graph-tool** | 95μs | 110μs | ⭐⭐ | LGPL-3.0 |
| **igraph** | N/A | 150μs | ⭐⭐⭐⭐ | GPL-2.0 |
| **scipy.csgraph** | N/A | 140μs | ⭐⭐⭐⭐⭐* | BSD-3 |

*Already installed with SciPy

## Additional Resources

- [DOMAIN_EXPLAINER.md](../DOMAIN_EXPLAINER.md) - High-level overview with universal analogies
- [metadata.yaml](../metadata.yaml) - Research metadata, sources, status
