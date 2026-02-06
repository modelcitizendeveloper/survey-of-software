# graph-tool - Technical Analysis

## Architecture

**Core**: Boost Graph Library (C++) with Python bindings

### Data Structures

**Property maps**: Boost's generic property system
- Edges/nodes stored in Boost containers
- Attributes as typed property maps
- Extremely compact memory layout (~8 bytes/edge)

**Template metaprogramming**: C++ templates for type specialization
- Compile-time optimization
- Zero-overhead abstractions

## Key Algorithms

**Stochastic Block Models (SBM)**:
- Bayesian inference for community structure
- Hierarchical and nested variants
- State-of-the-art, not available elsewhere

**Parallel algorithms**: OpenMP throughout
- Betweenness, PageRank, shortest paths parallelized
- Near-linear speedup on multi-core

**Performance** (10M node graph, 16 cores):
- Betweenness: ~2 minutes (vs hours for igraph)
- SBM community detection: ~10 minutes (unique capability)

## API

```python
from graph_tool.all import Graph
g = Graph(directed=False)
v1 = g.add_vertex()
e = g.add_edge(v1, v2)

# Property maps for attributes
vprop = g.new_vertex_property("string")
g.vp.name = vprop  # Register property
```

**Learning curve**: Steeper (Boost concepts, property maps)

## Strengths

1. **Fastest**: 100-1000x faster than NetworkX
2. **Memory**: Most efficient (~8 bytes/edge)
3. **Advanced algorithms**: SBM, statistical inference
4. **Parallel**: OpenMP support throughout
5. **Scalability**: 100M+ node graphs

## Weaknesses

1. **Installation**: Conda-only, complex dependencies
2. **API complexity**: Boost property maps confusing
3. **LGPL license**: More restrictive than BSD/MIT
4. **Documentation**: Assumes CS background
5. **Smaller community**: Fewer resources for help

## When Architecture Matters

**Use when**:
- Graph >1M nodes and performance critical
- Need SBM or advanced community detection
- Have multi-core hardware
- Can invest in learning curve

**Avoid when**:
- Graph <100K nodes (overkill)
- Quick prototyping (installation friction)
- Need easy API (NetworkX/igraph easier)
- LGPL conflicts with deployment
