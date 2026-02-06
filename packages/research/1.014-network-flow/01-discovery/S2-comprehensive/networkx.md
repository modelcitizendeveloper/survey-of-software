# NetworkX: Comprehensive Technical Analysis

## Architecture Overview

Pure Python implementation built on standard library data structures (dicts, sets) with optional NumPy/SciPy integration. Graph representation uses nested dictionaries for maximum flexibility at the cost of memory efficiency.

**Core philosophy:** Readability and extensibility over raw performance. Designed for algorithm exploration and teaching.

## Maximum Flow Algorithms

### Preflow-Push (Default)
- **Complexity:** O(V³) worst case, often faster in practice
- **Implementation:** Python adaptation of Goldberg-Tarjan algorithm
- **Best for:** General-purpose max flow, works well on most graph types

### Edmonds-Karp
- **Complexity:** O(VE²) or O(VEU) for integer capacities
- **Implementation:** BFS-based Ford-Fulkerson variant
- **Best for:** Graphs with small capacity values, pedagogical use

### Shortest Augmenting Path
- **Complexity:** O(V²E) for unit capacities
- **Implementation:** Modified BFS with distance labeling
- **Best for:** Unit capacity networks

### Dinitz Algorithm
- **Complexity:** O(V²E) general, O(E√V) for unit capacities
- **Implementation:** Level graph construction with blocking flows
- **Best for:** Bipartite matching, unit capacity networks

## API Patterns

### Basic Max Flow
```python
import networkx as nx

G = nx.DiGraph()
G.add_edge("s", "a", capacity=3.0)
G.add_edge("s", "b", capacity=1.0)
G.add_edge("a", "t", capacity=3.0)
G.add_edge("b", "t", capacity=1.0)

flow_value, flow_dict = nx.maximum_flow(G, "s", "t")
# flow_value: 4.0
# flow_dict: nested dict with flow on each edge
```

### Minimum Cost Flow
```python
# Nodes with demands (negative = supply, positive = demand)
G.add_node("s", demand=-5)
G.add_node("t", demand=5)
G.add_edge("s", "a", capacity=4, weight=2)  # weight = cost per unit
G.add_edge("a", "t", capacity=4, weight=3)

flowDict = nx.min_cost_flow(G)
# Returns flow satisfying all demands with minimum total cost
```

### Custom Algorithm Selection
```python
# Use Edmonds-Karp instead of default preflow-push
flow_value, flow_dict = nx.maximum_flow(
    G, "s", "t",
    flow_func=nx.algorithms.flow.edmonds_karp
)
```

## Performance Characteristics

### Time Complexity Summary
| Graph Size | Algorithm | Runtime (estimate) |
|------------|-----------|-------------------|
| 100 nodes, 500 edges | Preflow-push | <10ms |
| 1K nodes, 5K edges | Preflow-push | 100-500ms |
| 10K nodes, 50K edges | Preflow-push | 10-60s |
| 100K nodes, 500K edges | Any | Not practical |

### Memory Overhead
- **Graph storage:** ~200 bytes/edge (nested dicts + Python object overhead)
- **Flow computation:** O(V+E) additional for residual network
- **Rule of thumb:** 1M edges ≈ 200MB+ memory

### Numerical Stability
**Critical limitation:** Integer-only capacities recommended for min cost flow. Floating-point can cause:
- Infinite loops in capacity scaling algorithm
- Incorrect optimal solutions due to rounding errors
- Workaround: Multiply capacities by large constant, convert to integers

## API Design Philosophy

### Strengths
- **Intuitive graph construction:** Add nodes/edges incrementally
- **Flexible node IDs:** Any hashable type (strings, tuples, integers)
- **Attribute-based configuration:** Edge capacities/costs as attributes
- **Returns both value and flow dict:** Useful for debugging and visualization

### Pain Points
- **Mutable graphs during computation:** Must copy graph if original needed
- **No sparse matrix optimization:** Pure Python dicts don't leverage NumPy/SciPy speed
- **Inconsistent return types:** Some functions return objects, others return tuples

## Integration Patterns

### With NumPy/SciPy
```python
# Convert graph to scipy sparse matrix for external algorithms
adjacency_matrix = nx.to_scipy_sparse_array(G, weight='capacity')

# Convert adjacency matrix back to NetworkX graph
G = nx.from_scipy_sparse_array(adjacency_matrix, create_using=nx.DiGraph)
```

### With Pandas
```python
# Build graph from DataFrame of edges
import pandas as pd
edges_df = pd.DataFrame({
    'source': ['s', 's', 'a'],
    'target': ['a', 'b', 't'],
    'capacity': [3, 1, 3]
})
G = nx.from_pandas_edgelist(edges_df, 'source', 'target',
                             edge_attr='capacity',
                             create_using=nx.DiGraph)
```

## When NetworkX Implementation Shines

1. **Rapid prototyping:** Write/test flow algorithm in <30 minutes
2. **Teaching/learning:** Code readability matches textbook pseudocode
3. **Visualization:** Built-in matplotlib integration for flow diagrams
4. **Heterogeneous workflows:** Easy to combine flow with centrality, clustering, etc.
5. **Irregular graphs:** Flexible node IDs handle non-sequential node names

## When to Migrate Away

1. **Graphs >50K nodes:** Pure Python becomes prohibitively slow
2. **Real-time requirements:** Even small graphs take milliseconds, not microseconds
3. **Repeated computations:** No graph structure caching, recomputes from scratch
4. **Production systems:** No thread safety, no C-level optimization

## Debugging and Introspection

### View Residual Network
```python
R = nx.algorithms.flow.build_residual_network(G, 'capacity')
# Inspect residual capacities after flow computation
```

### Verify Flow Conservation
```python
flow_value, flow_dict = nx.maximum_flow(G, 's', 't')
for node in G.nodes():
    if node not in ['s', 't']:
        inflow = sum(flow_dict[u][node] for u in G.predecessors(node))
        outflow = sum(flow_dict[node][v] for v in G.successors(node))
        assert abs(inflow - outflow) < 1e-6  # Flow conservation
```

## Comparative Positioning

NetworkX is the **reference implementation** for understanding network flow algorithms. Think of it as the "CPython of graph libraries" - not the fastest, but the most readable and widely understood. For production or large-scale research, you'll migrate to OR-Tools (if building products) or graph-tool (if maximizing performance), but you'll prototype in NetworkX first.
