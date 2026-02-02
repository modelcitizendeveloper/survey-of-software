# snap.py - Technical Analysis

## Architecture

**Core**: Stanford's C++ SNAP library with SWIG Python bindings

### Data Structures

**Optimized for sparse graphs**:
- Compressed adjacency lists
- Designed for billion-edge web/social graphs
- Memory layout optimized for pointer chasing

**Node IDs**: Integer-based (like igraph)
- Efficient for massive graphs
- Less flexible than NetworkX

## Key Algorithms

**Web-scale focus**:
- PageRank: Optimized for billion-node graphs
- Cascades and diffusion: Unique to SNAP
- Connected components: Very fast on huge graphs

**Performance** (100M edge graph):
- PageRank: ~2 minutes
- Connected components: <1 minute
- Community detection (CNM): ~5 minutes

## API

**SWIG-generated bindings**:
```python
import snap
G = snap.TUNGraph.New()
G.AddNode(1)
G.AddNode(2)
G.AddEdge(1, 2)
```

**Not Pythonic**: C++-style API through SWIG
- `TUNGraph` (undirected), `TNGraph` (directed)
- Method names: `AddNode`, `GetNodes` (C++ conventions)

## Strengths

1. **Scalability**: Billion-node graphs
2. **Research provenance**: Stanford, used in published research
3. **BSD license**: Permissive
4. **Datasets**: SNAP dataset collection included
5. **Cascades**: Unique algorithms for diffusion

## Weaknesses

1. **Limited algorithms**: Narrower than NetworkX/igraph
2. **API**: SWIG bindings awkward for Python users
3. **Maintenance**: Slower development than alternatives
4. **Documentation**: C++-centric
5. **Community**: Smaller than NetworkX/igraph

## When Architecture Matters

**Use when**:
- Graph >100M nodes (billion-scale)
- Need Python interface (not C++)
- Core algorithms sufficient
- Research uses SNAP datasets

**Avoid when**:
- Graph <10M nodes (igraph/graph-tool better)
- Need comprehensive algorithms
- Want Pythonic API
- Require active maintenance/community
