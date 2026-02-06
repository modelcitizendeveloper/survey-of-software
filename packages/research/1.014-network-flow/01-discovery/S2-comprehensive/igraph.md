# igraph: Comprehensive Technical Analysis

## Architecture Overview

C library core with idiomatic Python (and R) bindings. Built on Boost Graph Library algorithms but wraps them in more accessible API. Balances performance with usability.

**Core philosophy:** Fast enough for most research, simple enough for rapid development. Academic network science focus.

## Maximum Flow Algorithms

### Primary Implementation
- **Algorithm:** Push-relabel (via Boost Graph Library)
- **Complexity:** O(V²√E) for bipartite graphs, O(V³) general case
- **Implementation:** C core, minimal Python overhead

**Key characteristic:** Single `maxflow()` method handles all cases, automatically selects appropriate variant based on graph structure.

## API Patterns

### Basic Max Flow
```python
import igraph as ig

# Create directed graph
g = ig.Graph(
    6,  # Number of vertices
    [(0, 1), (0, 2), (1, 3), (2, 3), (2, 4), (3, 5), (4, 5)],
    directed=True
)

# Assign edge capacities
g.es["capacity"] = [7, 8, 1, 2, 3, 4, 5]

# Compute max flow
flow = g.maxflow(source=0, target=5, capacity="capacity")

print(f"Max flow value: {flow.value}")  # Total flow
print(f"Edge flows: {flow.flow}")       # Flow on each edge
print(f"Min cut: {flow.cut}")           # Edges in minimum cut
print(f"Partition: {flow.partition}")   # Source-side nodes in cut
```

### Flow Object Structure
```python
# flow is a Flow object with attributes:
flow.value       # float: maximum flow value
flow.flow        # list: flow on each edge (same order as g.es)
flow.cut         # list of edge IDs in minimum cut
flow.partition   # list of 0/1 indicating partition membership
```

### Alternative: Explicit Edge List
```python
# Use edge IDs instead of edge attribute name
capacities = g.es["capacity"]
flow = g.maxflow(0, 5, capacity=capacities)
```

## Performance Characteristics

### Time Complexity Summary
| Graph Size | Runtime (estimate) |
|------------|--------------------|
| 100 nodes, 500 edges | <5ms |
| 1K nodes, 5K edges | 20-100ms |
| 10K nodes, 50K edges | 500ms-5s |
| 100K nodes, 1M edges | 1-10 minutes |

**5-20x faster than NetworkX**, **2-5x slower than graph-tool**.

### Memory Overhead
- **Graph storage:** ~100 bytes/edge (C structs + Python wrappers)
- **Flow computation:** O(E) for residual network
- **Rule of thumb:** 1M edges ≈ 100MB memory

### Numerical Handling
- **Floating-point capacities supported** (unlike OR-Tools SimpleMinCostFlow)
- **Precision:** Double-precision floats (IEEE 754)
- **No overflow protection:** Large integer capacities may lose precision

## API Design Philosophy

### Strengths
- **Single method interface:** `maxflow()` does everything
- **Rich return object:** Value, flow, cut, partition all in one result
- **Pythonic containers:** Edge/vertex sequences with attribute access
- **Flexible node IDs:** Integer-indexed (0 to N-1) but can use names via attributes

### Pain Points
- **Integer vertex IDs required:** No arbitrary hashable types like NetworkX
- **Graph mutability:** Must recompute flow if graph changes (no incremental updates)
- **Limited min cost flow:** No built-in min cost flow solver (max flow only)
- **R-influenced API:** Some methods named for R conventions, not Python idioms

## Integration Patterns

### With NumPy
```python
import numpy as np

# Create graph from adjacency matrix
adj_matrix = np.array([[0, 7, 8, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 2, 3, 0],
                        [0, 0, 0, 0, 0, 4],
                        [0, 0, 0, 0, 0, 5],
                        [0, 0, 0, 0, 0, 0]])

g = ig.Graph.Weighted_Adjacency(adj_matrix.tolist(), mode="directed", attr="capacity")
```

### With NetworkX (Migration Pattern)
```python
import networkx as nx

# Prototype in NetworkX
G_nx = nx.DiGraph()
# ... build graph ...

# Convert to igraph for better performance
G_ig = ig.Graph.from_networkx(G_nx)

# Run flow computation
flow = G_ig.maxflow(source_name, target_name, capacity="capacity")
```

### With R (Cross-Language Workflow)
```r
# R code using same igraph library
library(igraph)
g <- graph_from_edgelist(edges, directed=TRUE)
E(g)$capacity <- capacities
flow <- max_flow(g, source=1, target=6)
```

## Specialized Use Cases

### Bipartite Matching
```python
# Create bipartite graph
g = ig.Graph.Bipartite([0,0,0,1,1,1],  # Type indicators
                        [(0,3), (0,4), (1,3), (1,5), (2,4), (2,5)])

# Max matching via max flow
matching = g.maximum_bipartite_matching()
# Returns Matching object with matched pairs
```

### Min Cut Visualization
```python
import matplotlib.pyplot as plt

flow = g.maxflow(source, target, capacity="capacity")

# Color edges in min cut
edge_colors = ["red" if e in flow.cut else "black"
               for e in range(g.ecount())]

ig.plot(g, edge_color=edge_colors,
        vertex_label=range(g.vcount()),
        layout=g.layout_circle())
plt.show()
```

## When igraph Implementation Shines

1. **R users who occasionally need Python:** Single library across both languages
2. **Medium-scale graphs:** 10K-100K nodes, need better than NetworkX speed
3. **Community detection workflows:** Flow + clustering + centrality in one library
4. **Academic publications:** Mature, well-cited library (15+ years)
5. **Cross-platform reproducibility:** Identical results across Windows/Mac/Linux

## When to Use Alternatives

1. **Min cost flow required:** igraph lacks this, use NetworkX or OR-Tools
2. **Pure Python preferred:** NetworkX has simpler installation
3. **Extreme performance needed:** graph-tool is 2-5x faster
4. **Operations research problems:** OR-Tools has constraint programming integration
5. **GPL license incompatible:** Use NetworkX (BSD) or OR-Tools (Apache)

## Debugging and Validation

### Verify Flow Conservation
```python
flow = g.maxflow(source, target, capacity="capacity")

for v in range(g.vcount()):
    if v in [source, target]:
        continue
    inflow = sum(flow.flow[e] for e in g.incident(v, mode="in"))
    outflow = sum(flow.flow[e] for e in g.incident(v, mode="out"))
    assert abs(inflow - outflow) < 1e-9, f"Flow not conserved at node {v}"
```

### Visualize Min Cut
```python
# Partition vertices into source/sink sides
partition = flow.partition
source_side = [i for i in range(g.vcount()) if partition[i] == 0]
sink_side = [i for i in range(g.vcount()) if partition[i] == 1]

print(f"Source side: {source_side}")
print(f"Sink side: {sink_side}")
print(f"Cut edges: {flow.cut}")
```

## Comparative Positioning

igraph is the **balanced implementation** for network flow. Think of it as the "SQLite of graph libraries" - fast enough for most uses, simple enough to deploy anywhere, works the same in Python and R. Not the fastest (that's graph-tool), not the simplest (that's NetworkX), but the best middle ground for multi-language research workflows.
