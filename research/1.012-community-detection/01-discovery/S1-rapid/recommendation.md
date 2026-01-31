# S1 Recommendation: Rapid Decision Guide

## Quick Decision Matrix

| Use Case | Recommendation | Why |
|----------|---------------|-----|
| **Prototype quickly** | Louvain (NetworkX) | Fast, familiar, good enough |
| **Production deployment** | Leiden (leidenalg) | Fixes Louvain's defects, faster |
| **Billion-edge graphs** | Label Propagation (NetworKit) | Only algorithm that scales this far |
| **Directed/weighted networks** | Infomap | Exploits flow information |
| **Small graphs, known K** | Spectral Clustering (scikit-learn) | Mathematically elegant |
| **Don't know which to pick** | CDlib | Compare 39+ algorithms systematically |

## The 80/20 Rule

**For 80% of use cases, use Leiden.** It's faster than Louvain, produces better partitions, and guarantees well-connected communities.

**Why not Louvain?** Louvain may produce disconnected communities (up to 16% in some graphs). Leiden fixes this defect while being 20x faster on large networks.

## Decision Tree

```
START
  ↓
Graph size?
  ├─ <10K nodes → Spectral Clustering (if K known) or Leiden
  ├─ 10K-500K nodes → Leiden (first choice) or Louvain (prototype)
  └─ >500K nodes → Label Propagation or GPU-accelerated Leiden
       ↓
Quality vs Speed?
  ├─ Quality matters → Leiden or Infomap
  └─ Speed critical → Label Propagation
       ↓
Network type?
  ├─ Directed/weighted → Infomap
  └─ Undirected/unweighted → Leiden
       ↓
Still unsure? → CDlib (benchmark all)
```

## Implementation Path

### Phase 1: Prototype (Day 1)
```python
import networkx as nx
from networkx.algorithms.community import louvain_communities

G = nx.karate_club_graph()
communities = louvain_communities(G)
# 5 minutes to working prototype
```

### Phase 2: Validate (Week 1)
```python
# Compare Louvain vs Leiden
import cdlib
from cdlib import algorithms

louvain_result = algorithms.louvain(G)
leiden_result = algorithms.leiden(G)
# Evaluate: Which produces better modularity?
```

### Phase 3: Production (Month 1)
```python
# Use best algorithm directly
from leidenalg import find_partition
import igraph as ig

# Convert and optimize
G_igraph = ig.Graph.from_networkx(G)
partition = find_partition(G_igraph, leidenalg.ModularityVertexPartition)
```

## Red Flags

**Avoid Louvain if:**
- Communities must be well-connected (use Leiden)
- Iterative refinement is required (disconnection risk compounds)

**Avoid Label Propagation if:**
- Results must be deterministic (extremely non-deterministic)
- Modularity scores matter (lower than Louvain/Leiden)

**Avoid Spectral Clustering if:**
- Graph has >50K nodes (too slow)
- Number of communities is unknown

**Avoid Infomap if:**
- Simple undirected graphs (Leiden is simpler and faster)
- Stakeholders need simple explanations (modularity is easier to explain)

## The Contrarian Take

**Don't start with cdlib.** Its value is in *comparison*, not first-pass implementation. Start with a single algorithm (Leiden), validate it works, *then* use cdlib to benchmark alternatives.

**Why?** Debugging "why doesn't this work?" is easier with one library than 39. CDlib's power is comparative analysis, not initial development.

## Sources

This recommendation synthesizes findings from:
- [From Louvain to Leiden: guaranteeing well-connected communities](https://www.nature.com/articles/s41598-019-41695-z)
- [NVIDIA: GPU-Powered Leiden](https://developer.nvidia.com/blog/how-to-accelerate-community-detection-in-python-using-gpu-powered-leiden/)
- [Performance Evaluation of Python Libraries (2024)](https://www.researchgate.net/publication/382750317_Performance_Evaluation_of_Python_Libraries_for_Community_Detection_on_Large_Social_Network_Graphs)
- [CDlib: a python library to extract, compare and evaluate communities](https://link.springer.com/article/10.1007/s41109-019-0165-9)
