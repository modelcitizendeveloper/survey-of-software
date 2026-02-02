# igraph - Technical Analysis

## Architecture

**Core design**: C library with language bindings (Python, R, Mathematica)

### Data Structures

**Graph representation**: Compressed sparse format
- Edges stored as flat integer arrays
- Node/edge attributes in separate vectors
- Memory-contiguous layout (cache-friendly)

**Memory efficiency**:
- ~16 bytes per edge (10-15x more efficient than NetworkX)
- Attributes stored separately from structure
- Integer-based node indexing (0 to n-1)

### Implementation

**C core**:
- Hand-optimized algorithms
- No Python overhead in hot loops
- Direct memory management

**Python bindings**:
- Thin wrapper around C functions
- Minimal conversion overhead
- Some Pythonic convenience layers

## Algorithm Implementations

### Centrality

**Betweenness**: Brandes' algorithm with C optimization
- Performance: ~12 seconds for 100K nodes (vs 600s for NetworkX)
- Parallel version available (experimental)

**PageRank**: Power iteration with sparse matrix ops
- BLAS/LAPACK acceleration where available
- Converges faster than NetworkX (optimized termination)

### Community Detection

**Louvain**: Multi-level modularity optimization
- Fast implementation: ~5 seconds for 1M edges
- Built-in (not third-party like NetworkX)

**Infomap**: Information-theoretic method
- State-of-the-art for many networks
- Not available in NetworkX

**Label propagation**: Synchronous and asynchronous variants
- 10-20x faster than NetworkX

### API Design

**Integer node IDs**:
```python
g = igraph.Graph(n=100)  # Nodes are 0-99
g.add_edges([(0, 1), (1, 2)])
```

**Attribute access**:
```python
g.vs["name"] = ["Alice", "Bob", "Charlie"]
g.es["weight"] = [1.5, 2.0, 3.5]
```

**Algorithm invocation**:
```python
result = g.betweenness()  # Method on graph object
communities = g.community_multilevel()  # Built-in Louvain
```

## Performance

**Benchmarks** (1M node Barabási-Albert, 5M edges):
- Betweenness: ~5 minutes (vs ~50 hours for NetworkX)
- PageRank: 30 seconds (vs 10 minutes)
- Louvain: 15 seconds (not in core NetworkX)

**Scalability**: Comfortable up to ~10M nodes on workstation

## Strengths

1. **Performance**: 10-50x faster than NetworkX
2. **Memory**: 10-15x more efficient
3. **Comprehensive algorithms**: Louvain, Infomap, VF2 isomorphism
4. **Production-ready**: Stable, maintained, cross-platform
5. **Multi-language**: Same algorithms in Python, R

## Weaknesses

1. **GPL license**: Viral, commercial restrictions
2. **API ergonomics**: Less Pythonic (integer nodes, method-heavy)
3. **Learning curve**: Steeper than NetworkX
4. **Installation**: Binary wheels, but occasional platform issues
5. **Flexibility**: Less flexible than NetworkX's dict-based model

## When Architecture Matters

**Use when**:
- Graph >10K nodes and NetworkX too slow
- Need Louvain, Infomap, or other advanced algorithms
- Production deployment (GPL acceptable)
- Cross-language workflows (Python + R)

**Avoid when**:
- GPL license conflicts with proprietary use
- Prefer Pythonic API ergonomics
- Graph <10K nodes (NetworkX easier, performance gap negligible)
