# NetworKit - Technical Analysis

## Architecture

**Core**: C++ with OpenMP parallelization, Cython Python bindings

### Parallelization Strategy

**OpenMP throughout**:
- Shared-memory parallelism
- Thread-level parallelization
- Near-linear speedup up to ~16 cores

**Thread-safe algorithms**:
- Parallel betweenness, PageRank, community detection
- Work-stealing for load balancing

## Key Algorithms

**Parallel Louvain (PLM)**:
- Multi-threaded community detection
- 8x speedup on 8 cores vs single-threaded

**Approximation algorithms**:
- Approximate betweenness (Riondato-Kornaropoulos)
- Sample-based algorithms for massive graphs
- Trade accuracy for speed (configurable)

**Performance** (10M node graph, 16 cores):
- Betweenness: ~1 minute (vs ~10 minutes single-threaded)
- PageRank: ~5 seconds
- PLM: ~20 seconds

## API

```python
import networkit as nk
G = nk.Graph(n=100)
G.addEdge(0, 1)
bc = nk.centrality.Betweenness(G)
bc.run()
scores = bc.scores()
```

**OOP style**: Algorithm objects with `run()` method
- Allows configuration before execution
- Can query intermediate state

## Strengths

1. **Parallel performance**: 5-25x speedup with cores
2. **Algorithmic engineering**: Optimized implementations
3. **Approximation**: Fast estimates for huge graphs
4. **MIT license**: Most permissive
5. **Active development**: Well-maintained

## Weaknesses

1. **Requires multi-core**: Single-core = no advantage
2. **Memory overhead**: Parallel = more memory
3. **OpenMP dependency**: Platform issues (especially macOS)
4. **Narrower algorithms**: vs NetworkX/igraph
5. **Learning curve**: OOP API different from NetworkX

## When Architecture Matters

**Use when**:
- Have 16+ core server
- Graph size 10M-1B edges
- Can leverage parallelism
- Performance critical (batch jobs)

**Avoid when**:
- Single-core / laptop
- Graph <1M nodes (overhead not worth it)
- Need comprehensive algorithms
- Want simplicity over speed
