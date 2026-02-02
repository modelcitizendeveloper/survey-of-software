# graph-tool

## Overview

High-performance graph library with C++ core and Python bindings. Designed for scientific computing and large-scale network analysis. The fastest general-purpose graph library in the Python ecosystem.

## Ecosystem Stats

- **GitHub Stars**: ~700
- **Conda Downloads**: ~200K total (not on PyPI)
- **First Release**: 2006
- **Maintenance**: Active (maintained by Tiago Peixoto)
- **License**: LGPL-3.0

## Core Strengths

**Extreme performance**:
- Boost Graph Library (C++) core
- OpenMP parallel processing support
- ~100-1000x faster than NetworkX for many operations
- Handles graphs with billions of edges
- SIMD vectorization where applicable

**Advanced algorithms**:
- State-of-the-art community detection (stochastic block models)
- Bayesian inference for network structure
- Graph drawing with force-directed layouts
- Motif finding, percolation, epidemic models
- All standard centrality/shortest path algorithms

**Scalability**:
- Designed for massive graphs (10M+ nodes)
- Efficient memory layout using Boost property maps
- Out-of-core processing possible for huge graphs
- Parallel algorithms utilize multiple cores

## Performance Characteristics

**Speed**: Fastest
- Centrality on 1M node graph: seconds (vs minutes for NetworkX)
- Community detection (SBM): handles 10M+ node graphs
- Parallel algorithms: near-linear speedup on multi-core systems
- Practical for billion-edge graphs with sufficient RAM

**Memory**: Most efficient
- Compact graph representation
- ~50% less memory than igraph for same graph
- Supports memory-mapped graphs for out-of-core analysis

**Benchmarks** (approximate, 1M node random graph):
- Betweenness centrality: 100x faster than NetworkX
- PageRank: 200x faster than NetworkX
- Community detection: 50-500x faster (algorithm-dependent)

## Limitations

**Installation complexity**:
- Not on PyPI (Conda-only or compile from source)
- Requires Boost, CGAL, Cairo dependencies
- Platform-specific build issues common
- Conda recommended, but adds environment management overhead

**Steep learning curve**:
- API more complex than NetworkX/igraph
- Requires understanding property maps (Boost concept)
- Documentation assumes graph theory/CS background
- Fewer tutorials and Stack Overflow answers

**LGPL license concerns**:
- Less permissive than BSD/MIT
- Dynamic linking required for proprietary use
- More restrictive than NetworkX (BSD) or snap.py (BSD)

**Smaller ecosystem**:
- Fewer users than NetworkX/igraph
- Less community support
- Harder to find help with specific problems

## Best For

- **Large-scale scientific research**: 1M-100M+ node graphs
- **Computationally intensive analysis**: Speed is critical
- **Advanced community detection**: Stochastic block models, hierarchical inference
- **Performance-critical production**: Can justify installation complexity
- **Parallel processing**: Multi-core servers available

## Avoid For

- **Beginners**: Too steep a learning curve
- **Quick prototyping**: Installation friction slows exploration
- **Small graphs (<10K nodes)**: NetworkX is easier, speed difference negligible
- **Production with strict licensing**: LGPL may complicate proprietary deployment
- **PyPI-only environments**: Conda or source builds required

## Ecosystem Position

**The performance champion**:
- Fastest general-purpose graph library in Python
- Go-to for graphs too large for igraph
- Research-focused: cutting-edge algorithms

**Trade-off**:
- Maximum speed and scale
- Minimum ease of use and accessibility
- Installation and learning curve friction

**When to reach for graph-tool**:
- NetworkX is too slow (>10K nodes, performance-critical)
- igraph is too slow (>1M nodes, or need parallel processing)
- Need state-of-the-art community detection (SBM)
- Have time to invest in learning the API
