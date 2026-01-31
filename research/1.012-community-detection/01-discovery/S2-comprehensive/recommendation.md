# S2 Recommendation: Technical Decision Guide

## Primary Recommendation: Start with Leiden

**For 90% of use cases, use Leiden.** Here's why:

1. **Fixes Louvain's critical defect:** Guarantees well-connected communities (0% disconnected vs 16% for Louvain)
2. **Faster despite extra phase:** 20x faster on large graphs (39M nodes)
3. **Better quality:** Higher modularity, subset-optimal when iterated
4. **Production-ready:** C++ implementation (leidenalg), stable API

**Exception:** If you're prototyping in pure NetworkX and can't add dependencies, use NetworkX Louvain temporarily, then migrate to Leiden before production.

## Decision Framework

### Step 1: Graph Size Filter

```
Graph size?
├─ <10K nodes → Any algorithm works, choose by features
├─ 10K-500K nodes → Leiden or Louvain
├─ 500K-10M nodes → Leiden or Label Propagation
└─ >10M nodes → Label Propagation (NetworKit) or GPU Leiden
```

### Step 2: Network Type Filter

**Directed graph with meaningful flow patterns?**
→ Use Infomap (exploits directedness)

**Temporal/evolving graph?**
→ Label Propagation (supports online updates) or Infomap

**Multiplex or higher-order?**
→ Infomap (only algorithm with native support)

**Simple undirected/weighted?**
→ Leiden (simplicity + performance)

### Step 3: Requirements Filter

**Know exact number of communities (K)?**
→ Spectral Clustering (if K known and graph <50K nodes)

**Need hierarchical structure?**
→ Leiden (multi-level) or Infomap (nested modules)

**Overlapping communities required?**
→ Infomap (flow-based overlap) or use CDlib for specialized algorithms

**Deterministic results critical?**
→ Spectral (cluster_qr method) - but limited to small graphs

## Algorithm Selection Matrix

| Constraint | Algorithm | Reason |
|------------|-----------|--------|
| **Graph >1M nodes** | Label Prop (NetworKit) | Only algorithm that scales |
| **Directed network** | Infomap | Exploits asymmetric flow |
| **Known K, graph <50K** | Spectral | Mathematical rigor |
| **Production deployment** | Leiden | Quality guarantees + speed |
| **Quick prototype** | Louvain (NetworkX) | Minimal friction |
| **Research/benchmarking** | CDlib | 39+ algorithms in one API |
| **Temporal network** | Infomap or Label Prop | Dynamic support |

## When to Use Each Algorithm

### Louvain: Prototype Phase

**Use when:**
- Exploring new dataset
- Quick visualization needed
- Working in NetworkX ecosystem (no extra dependencies)

**Migrate to Leiden when:**
- Moving to production
- Quality matters (avoid disconnected communities)
- Performance critical (Leiden faster anyway)

**Code transition:**
```python
# Prototype with Louvain
from networkx.algorithms.community import louvain_communities
communities = louvain_communities(G)

# Production with Leiden
from cdlib import algorithms
communities = algorithms.leiden(G)
```

### Leiden: Production Standard

**Use when:**
- Deploying to production
- Quality guarantees required
- Graph size: 1K-10M nodes
- Network type: undirected or symmetrized

**Implementation:**
```python
import leidenalg
import igraph as ig

G_ig = ig.Graph.from_networkx(G)
partition = leidenalg.find_partition(
    G_ig,
    leidenalg.ModularityVertexPartition,
    n_iterations=2,
    seed=42
)
```

### Label Propagation: Extreme Scale

**Use when:**
- Graph >10M nodes
- Speed >> quality
- Approximate clustering acceptable
- Real-time or streaming analysis

**Implementation (NetworKit):**
```python
import networkit as nk

G_nk = nk.nxadapter.nx2nk(G)
lp = nk.community.PLP(G_nk)
lp.run()
communities = lp.getPartition()
```

### Spectral: Small Graphs, Known K

**Use when:**
- Graph <10K nodes
- Know exact number of communities
- Theoretical rigor required
- Integration with scikit-learn ML pipeline

**Implementation:**
```python
from sklearn.cluster import SpectralClustering
import networkx as nx

A = nx.adjacency_matrix(G).todense()
sc = SpectralClustering(
    n_clusters=3,
    affinity='precomputed',
    assign_labels='cluster_qr',  # Deterministic
    random_state=42
)
labels = sc.fit_predict(A)
```

### Infomap: Directed/Complex Networks

**Use when:**
- Directed graph with meaningful flow
- Weighted network with flow dynamics
- Temporal or multiplex networks
- Hierarchical structure important

**Implementation:**
```python
import infomap

im = infomap.Infomap("--two-level --directed")
for u, v in G.edges():
    im.add_link(u, v)
im.run()

communities = {node.node_id: node.module_id
               for node in im.tree if node.is_leaf}
```

### CDlib: Research and Comparison

**Use when:**
- Don't know which algorithm to use
- Comparing multiple methods systematically
- Research requiring comprehensive baseline
- Evaluating novel network against standards

**Implementation:**
```python
from cdlib import algorithms, evaluation

# Try multiple algorithms
results = {}
for name, algo in [('louvain', algorithms.louvain),
                    ('leiden', algorithms.leiden),
                    ('infomap', algorithms.infomap)]:
    comm = algo(G)
    mod = evaluation.newman_girvan_modularity(G, comm).score
    results[name] = (comm, mod)

# Pick best by modularity
best = max(results.items(), key=lambda x: x[1][1])
```

## Hyperparameter Tuning Guide

### Leiden Resolution Parameter

**Default: 1.0** (standard modularity)

**Tune when:**
- Communities too large (increase resolution, e.g., 1.5)
- Communities too small (decrease resolution, e.g., 0.5)

**Method:**
```python
for res in [0.5, 1.0, 1.5, 2.0]:
    partition = leidenalg.find_partition(
        G_ig, leidenalg.ModularityVertexPartition,
        resolution_parameter=res
    )
    print(f"Resolution {res}: {len(partition)} communities")
```

### Label Propagation Max Iterations

**Default: varies** (NetworkX: no max, NetworKit: 1000)

**Tune when:**
- Non-convergence (set max_iter=50)
- Need faster approximate result (max_iter=10)

### Spectral Number of Clusters (K)

**Required parameter.** No default.

**Selection method: Eigengap**
```python
import numpy as np
from scipy.sparse.linalg import eigsh

L = nx.normalized_laplacian_matrix(G)
eigenvalues, _ = eigsh(L, k=10, which='SM')

# Look for largest gap
gaps = np.diff(eigenvalues)
k = np.argmax(gaps) + 1
print(f"Suggested K: {k}")
```

## Performance Optimization Strategies

### For Leiden (leidenalg)

**1. Reduce iterations if quality sufficient:**
```python
partition = leidenalg.find_partition(
    G_ig, leidenalg.ModularityVertexPartition,
    n_iterations=1  # Default: 2, try 1 for speed
)
```

**2. Use GPU for >1M nodes:**
```python
# cuGraph (NVIDIA GPUs)
import cugraph
communities = cugraph.leiden(G_cudf)
```

### For Label Propagation

**1. Use C++ implementation (NetworKit):**
- 10-100x faster than NetworkX pure Python

**2. Reduce iterations:**
```python
lp = nk.community.PLP(G_nk, maxIterations=10)  # Default: 1000
```

### For Spectral

**1. Use LOBPCG for sparse graphs:**
```python
sc = SpectralClustering(
    n_clusters=k,
    eigen_solver='lobpcg',  # Faster for sparse graphs
    affinity='precomputed'
)
```

**2. Don't use spectral for >50K nodes:**
- Switch to modularity-based methods

## Common Pitfalls and Solutions

### Pitfall 1: Using Louvain in Production

**Problem:** Disconnected communities (up to 16%)
**Solution:** Switch to Leiden (trivial API change via CDlib)

```python
# Before (risky)
from networkx.algorithms.community import louvain_communities
communities = louvain_communities(G)

# After (safe)
from cdlib import algorithms
communities = algorithms.leiden(G)
```

### Pitfall 2: Expecting Determinism from Modularity Methods

**Problem:** Louvain/Leiden give different results on each run
**Solution:**
- Set random seed (partial determinism)
- Or use Spectral (fully deterministic with cluster_qr)

```python
# Partial determinism (same seed = same result)
communities = algorithms.leiden(G, seed=42)

# Full determinism (same graph = same result)
sc = SpectralClustering(n_clusters=k, assign_labels='cluster_qr')
```

### Pitfall 3: Spectral on Large Graphs

**Problem:** O(n³) complexity → 10min for 10K nodes, hours for 50K
**Solution:** Don't use spectral for >10K nodes. Use Leiden instead.

### Pitfall 4: Label Propagation Quality Assumptions

**Problem:** Expecting modularity comparable to Louvain/Leiden
**Solution:** Accept 0.05-0.1 lower modularity as cost of speed, or refine with Louvain

```python
# Two-stage: LPA for initial guess, Louvain to refine
lpa_comm = label_propagation_communities(G)
# Convert to partition, refine with Louvain
```

### Pitfall 5: Infomap on Simple Undirected Graphs

**Problem:** Overcomplicated for task, harder to explain than modularity
**Solution:** Use Leiden unless directedness/flow is meaningful

## Validation Checklist

Before deploying community detection in production:

- [ ] **Connectedness:** Verify all communities are connected subgraphs
- [ ] **Size distribution:** Check for trivial solutions (1 giant community)
- [ ] **Modularity:** Benchmark against baseline (random, single community)
- [ ] **Stability:** Run multiple times, check variance
- [ ] **Domain validation:** Show sample communities to domain experts
- [ ] **Edge cases:** Test on graphs with known structure (e.g., stochastic block model)

**Validation code:**
```python
import networkx as nx

for community in communities:
    subgraph = G.subgraph(community)
    assert nx.is_connected(subgraph), f"Community {community} disconnected!"
```

## Migration Path: Prototype → Production

**Week 1: Prototype**
```python
# NetworkX Louvain (pure Python, no dependencies)
from networkx.algorithms.community import louvain_communities
communities = louvain_communities(G)
```

**Week 2: Validate**
```python
# Compare with Leiden via CDlib
from cdlib import algorithms, evaluation

louvain = algorithms.louvain(G)
leiden = algorithms.leiden(G)

print("Louvain modularity:", evaluation.newman_girvan_modularity(G, louvain).score)
print("Leiden modularity:", evaluation.newman_girvan_modularity(G, leiden).score)
```

**Week 3: Production**
```python
# Direct leidenalg (C++, optimized)
import leidenalg
import igraph as ig

G_ig = ig.Graph.from_networkx(G)
partition = leidenalg.find_partition(
    G_ig, leidenalg.ModularityVertexPartition,
    n_iterations=2, seed=42
)
```

## Sources

This recommendation synthesizes findings from all S2 technical analyses:
- [From Louvain to Leiden](https://www.nature.com/articles/s41598-019-41695-z)
- [Performance Evaluation of Python Libraries (2024)](https://www.researchgate.net/publication/382750317_Performance_Evaluation_of_Python_Libraries_for_Community_Detection_on_Large_Social_Network_Graphs)
- [Community Detection with the Map Equation](https://dl.acm.org/doi/10.1145/3779648)
- [Label propagation: A semi-synchronous approach](https://www.nature.com/articles/srep45836)
- [Spectral clustering tutorial (Luxburg)](https://people.csail.mit.edu/dsontag/courses/ml14/notes/Luxburg07_tutorial_spectral_clustering.pdf)
