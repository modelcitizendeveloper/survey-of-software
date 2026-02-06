# igraph - Comprehensive Technical Analysis

## Architecture Overview

**Language**: C core with Python/R/Mathematica interfaces
**Graph Representation**: C structs with adjacency lists
**Performance Strategy**: Tight C loops, minimal Python overhead

### Core Design

**C Backend**: Pure C implementation (~150K lines of C code)
**Python Bindings**: C API bindings using Python/C API
**Cross-Language**: Same C core for Python, R, Mathematica

```python
g = igraph.Graph(directed=True)
# C igraph_t struct wrapped in Python
```

## Algorithm Implementations

### Shortest Paths (shortest_paths, get_shortest_paths)

**Note**: No dedicated A* implementation

**Dijkstra Support**:
```python
# Single-source shortest paths
paths = g.get_shortest_paths(
    v=source,
    to=target,
    weights="weight",  # Edge attribute name
    mode="out"  # Direction for directed graphs
)

# All-pairs shortest paths matrix
distances = g.shortest_paths(
    source=None,  # None = all vertices
    target=None,
    weights="weight"
)
```

**C Implementation**:
- Uses Dijkstra with binary heap
- Bidirectional search for single source-target queries
- Matrix operations for all-pairs
- BLAS integration for dense graphs

**Performance** (10K nodes):

| Operation | Time (μs) | vs NetworkX |
|-----------|-----------|-------------|
| Single path | ~150 | 80x faster |
| All-pairs | ~350,000 | 71x faster |

### BFS/DFS (bfs, dfs)

**BFS API**:
```python
# BFS with callback
def callback(parent, vertex, parent_idx, distance):
    print(f"Visit {vertex} from {parent}, distance {distance}")

g.bfs(
    vid=source,
    mode="out",
    advanced=True  # Enables callback
)

# Simple BFS (returns visited order)
order = g.bfs(vid=source)[0]
```

**DFS API**:
```python
# DFS traversal order
order = g.dfs(vid=source, mode="out")[0]

# DFS with in/out timestamps (advanced)
result = g.dfs(vid=source, mode="out", advanced=True)
```

**C Implementation**:
- Stack-based DFS (no recursion)
- Deque-based BFS
- Callback system for custom processing
- Visited bitset for space efficiency

## Graph Representation

### Internal C Structure

```c
// Simplified igraph_t structure
typedef struct igraph_t {
    igraph_vector_int_t *from;  // Edge source vertices
    igraph_vector_int_t *to;    // Edge target vertices
    igraph_bool_t directed;
    // Adjacency cache built on demand
} igraph_t;
```

**Edge List Representation**:
- Edges stored as parallel arrays (from[], to[])
- Adjacency lists built on demand (cached)
- Space-efficient for sparse graphs
- Sequential edge access patterns

### Attribute System

**Vertex/Edge Attributes**:
```python
# Add attributes during creation
g = igraph.Graph(n=5)
g.vs["name"] = ["A", "B", "C", "D", "E"]
g.vs["x"] = [0, 1, 2, 3, 4]
g.es["weight"] = [1.0, 2.0, 3.0, ...]

# Access attributes
print(g.vs[0]["name"])  # "A"
weights = g.es["weight"]
```

**Storage**:
- Attributes stored in Python dicts (not in C)
- Overhead for attribute access vs pure C
- Trade-off: Flexibility vs performance

## Performance Characteristics

### Memory Layout

**Graph Storage** (10K nodes, 50K edges):
- Edge arrays: ~400 KB (2 * int32 per edge)
- Adjacency cache: ~600 KB (when built)
- Attributes: Python dict overhead (~2 MB for typical attributes)

**vs C-only libs**: Small overhead from Python attribute storage
**vs NetworkX**: 5-10x less memory

### Algorithm Performance

**Why igraph is fast**:
1. **C loops**: No Python interpretation in inner loops
2. **Cache locality**: Contiguous arrays, sequential access
3. **BLAS integration**: Matrix operations use optimized BLAS
4. **Minimal overhead**: Thin Python wrapper over C

**Limitation**: Python GIL not released (single-threaded)

## API Design

### Graph Construction

```python
# Edge list
g = igraph.Graph([(0, 1), (1, 2), (2, 3)])

# Adjacency matrix
import numpy as np
adj = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
g = igraph.Graph.Adjacency(adj.tolist())

# Famous graphs
g = igraph.Graph.Erdos_Renyi(n=1000, p=0.01)
g = igraph.Graph.Barabasi(n=1000, m=2)
```

### Vertex Sequences and Edge Sequences

**Powerful Selection API**:
```python
# Select vertices by attribute
high_degree = g.vs.select(_degree_gt=10)

# Select edges by attribute
heavy_edges = g.es.select(weight_gt=5.0)

# Method chaining
important = g.vs.select(_degree_gt=10).select(name_in=["A", "B", "C"])
```

**Implementation**: Lazy evaluation, efficient C filtering

### Shortest Path Variants

```python
# Get path as vertex sequence
path = g.get_shortest_paths(source, target)[0]

# Get path as edge sequence
path_edges = g.get_shortest_paths(source, target, output="epath")[0]

# Get distance matrix only
dist_matrix = g.shortest_paths(weights="weight")
```

## Integration with Data Science Stack

### NumPy/Pandas
```python
# Export to NumPy adjacency matrix
adj = np.array(g.get_adjacency().data)

# Edge list to Pandas DataFrame
import pandas as pd
edges = [(e.source, e.target, e["weight"]) for e in g.es]
df = pd.DataFrame(edges, columns=["source", "target", "weight"])
```

### R Integration
```python
# Python igraph ↔ R igraph (via rpy2)
# Useful for cross-language workflows
# Same C backend, compatible formats
```

## Cross-Platform Support

**Platforms**:
- **Linux**: First-class support, easiest installation
- **macOS**: Good support via Homebrew/Conda
- **Windows**: Good support, pre-built wheels available

**Installation**:
```bash
pip install python-igraph  # Works on all platforms
conda install -c conda-forge python-igraph  # Recommended
```

**Dependencies**: Minimal (C library + Python), no Boost/C++ compiler needed

## Strengths in Detail

1. **Ease of Installation**: `pip install` works reliably
2. **Cross-Platform**: Excellent Windows support
3. **Performance**: 50-80x faster than NetworkX
4. **R Compatibility**: Same library in Python and R
5. **API Simplicity**: More intuitive than graph-tool
6. **Community**: Large academic user base

## Weaknesses in Detail

1. **No A\***: Major limitation for pathfinding applications
2. **GPL License**: May limit commercial use (though less restrictive than LGPL)
3. **Attribute Overhead**: Python dict attributes slower than native C
4. **Algorithm Coverage**: Fewer algorithms than NetworkX
5. **Documentation**: Good but less comprehensive than NetworkX

## Workarounds for Missing A*

**Option 1**: Weighted BFS approximation (inadmissible heuristic)
**Option 2**: Use NetworkX for A*, igraph for other operations
**Option 3**: Implement A* using igraph BFS + custom logic

**Example** (manual A*-like search):
```python
import heapq

def astar_workaround(g, source, target, heuristic_func):
    # Manual A* implementation using igraph primitives
    frontier = [(0, source, [source])]
    visited = set()

    while frontier:
        cost, node, path = heapq.heappop(frontier)

        if node == target:
            return path

        if node in visited:
            continue
        visited.add(node)

        for neighbor in g.neighbors(node, mode="out"):
            if neighbor not in visited:
                new_cost = cost + g.es[g.get_eid(node, neighbor)]["weight"]
                heuristic = heuristic_func(neighbor, target)
                priority = new_cost + heuristic
                heapq.heappush(frontier, (priority, neighbor, path + [neighbor]))

    return None
```

**Limitation**: Slower than native C implementation, loses igraph's speed advantage

## When to Deep-Dive into igraph

- **Medium-large graphs**: 10K-1M nodes
- **Good performance needed**: NetworkX too slow, graph-tool too complex
- **Cross-platform**: Need Windows support
- **R integration**: Work across Python/R
- **A* not required**: Dijkstra sufficient
- **Commercial use**: GPL acceptable

## Migration from NetworkX

**Similarities**:
- Graph construction similar
- Many function names overlap
- Attribute system familiar

**Differences**:
- Vertex/edge sequences (igraph) vs arbitrary IDs (NetworkX)
- Different shortest path function names
- Callback-based traversals
- No A* (must adapt algorithm)

**Migration Effort**: Moderate (few days for medium projects)
