# CDlib - Technical Analysis

## Architecture

**Core**: Pure Python wrapper orchestrating community detection algorithms

### Design Pattern

**Adapter/Facade**:
- Unified interface to algorithms from multiple libraries
- Delegates to NetworkX, igraph, or graph-tool backends
- Minimal own implementation (coordination layer)

**Backend agnostic**:
```python
from cdlib import algorithms
# Uses NetworkX backend
communities = algorithms.louvain(nx_graph)

# Uses igraph backend (faster)
communities = algorithms.louvain(ig_graph)
```

## Algorithm Coverage

**40+ algorithms** across categories:

**Non-overlapping**: Louvain, Leiden, label propagation, Infomap, SBM
**Overlapping**: DEMON, SLPA, CONGO (nodes in multiple communities)
**Hierarchical**: Hierarchical link clustering, divisive methods
**Attribute-aware**: Combine structure + node features
**Temporal**: Dynamic community detection (evolving graphs)

## API Design

**Consistent interface**:
```python
from cdlib import algorithms, evaluation

# Detection
communities = algorithms.leiden(graph)

# Evaluation
mod = evaluation.modularity(graph, communities)
nmi = evaluation.normalized_mutual_information(communities1, communities2)

# Visualization
from cdlib import viz
viz.plot_network_clusters(graph, communities)
```

**Result object**:
- `communities.communities`: List of sets (node IDs)
- `communities.to_node_community_map()`: Node → communities
- Rich metadata and methods

## Performance

**Depends on backend**:
- NetworkX backend: Slow (pure Python)
- igraph backend: Fast (C library)
- graph-tool backend: Fastest (C++ + OpenMP)

**Overhead**: Minimal (<5% over direct library use)

## Evaluation Framework

**20+ quality metrics**:
- Modularity, coverage, performance
- Internal/external validation
- Statistical significance tests

**Comparison tools**:
- Side-by-side algorithm comparison
- Consensus clustering across methods
- Parameter sensitivity analysis

## Strengths

1. **Comprehensive**: 40+ algorithms, one interface
2. **Evaluation**: Built-in quality metrics
3. **Backend flexibility**: Choose speed vs ease
4. **Overlapping**: Unique algorithms not elsewhere
5. **Research-friendly**: Reproducible, standard metrics

## Weaknesses

1. **Not standalone**: Requires backend library
2. **Installation**: Complexity of all backends
3. **Documentation**: Algorithm selection guidance limited
4. **Performance**: Adds small overhead
5. **Scope**: Only community detection

## When Architecture Matters

**Use when**:
- Community detection is primary focus
- Need to compare multiple algorithms
- Require overlapping communities
- Want systematic evaluation

**Avoid when**:
- Only need one algorithm (use backend directly)
- General graph analysis (not specialized)
- Minimal dependencies preferred
- Real-time / streaming detection
