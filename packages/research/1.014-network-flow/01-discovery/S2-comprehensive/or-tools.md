# OR-Tools: Comprehensive Technical Analysis

## Architecture Overview

Multi-layered C++ optimization suite with thin language bindings (Python, Java, C#). Network flow solvers are specialized components within broader constraint programming and linear optimization framework.

**Core philosophy:** Production-grade performance and correctness. Designed for real-world operations research problems at Google scale.

## Maximum Flow Algorithms

### SimpleMaxFlow
- **Implementation:** C++ optimized preflow-push variant
- **Complexity:** O(V²E) worst case, sub-quadratic in practice
- **Best for:** Standard max flow problems without additional constraints

**Key characteristic:** Solves only max flow, not integrated with other OR features. Use for straightforward capacity planning.

## Minimum Cost Flow Algorithms

### SimpleMinCostFlow
- **Implementation:** Network simplex algorithm with C++ optimization
- **Complexity:** Polynomial but depends on problem structure
- **Best for:** Supply/demand satisfaction with cost minimization

### Cost Scaling Algorithm
- **Implementation:** Successive approximation with cost scaling
- **Complexity:** O(E log(V) · (E + V log V))
- **Best for:** Large-scale problems with integer costs

**Distinguishing feature:** Handles supply/demand constraints natively, unlike pure max flow solvers.

## API Patterns

### Basic Min Cost Flow (Python)
```python
from ortools.graph.python import min_cost_flow
import numpy as np

# Instantiate solver
smcf = min_cost_flow.SimpleMinCostFlow()

# Define network as parallel arrays (efficient bulk insertion)
start_nodes = np.array([0, 0, 1, 1, 2])
end_nodes = np.array([1, 2, 2, 3, 3])
capacities = np.array([15, 8, 20, 4, 15])
unit_costs = np.array([4, 4, 2, 2, 1])

# Add all arcs at once (C++ level optimization)
all_arcs = smcf.add_arcs_with_capacity_and_unit_cost(
    start_nodes, end_nodes, capacities, unit_costs
)

# Set supplies (negative = source, positive = sink, 0 = transshipment)
supplies = [20, 0, 0, -20]  # Node 0 supplies 20, Node 3 demands 20
smcf.set_nodes_supplies(np.arange(len(supplies)), supplies)

# Solve
status = smcf.solve()
if status == smcf.OPTIMAL:
    print(f"Min cost: {smcf.optimal_cost()}")
    flows = smcf.flows(all_arcs)  # Flow values on each arc
```

### Max Flow with Min Cost (Python)
```python
# Solve max flow, break ties by minimum cost
status = smcf.solve_max_flow_with_min_cost()
```

### Accessing Solution Details
```python
# Iterate through solution
for arc in all_arcs:
    if smcf.flow(arc) > 0:
        print(f"{smcf.tail(arc)} -> {smcf.head(arc)}: "
              f"flow={smcf.flow(arc)}/{smcf.capacity(arc)}, "
              f"cost={smcf.unit_cost(arc)}")
```

## Performance Characteristics

### Time Complexity Summary
| Graph Size | Algorithm | Runtime (estimate) |
|------------|-----------|-------------------|
| 100 nodes, 500 edges | SimpleMinCostFlow | <1ms |
| 1K nodes, 5K edges | SimpleMinCostFlow | 5-20ms |
| 10K nodes, 50K edges | SimpleMinCostFlow | 50-200ms |
| 100K nodes, 1M edges | SimpleMinCostFlow | 1-10s |

**10-100x faster than NetworkX** due to C++ optimization and specialized algorithms.

### Memory Overhead
- **Graph storage:** ~50-100 bytes/edge (C++ structs, not Python dicts)
- **Solver state:** O(V+E) for residual network + solver-specific structures
- **Rule of thumb:** 1M edges ≈ 50-100MB memory

### Numerical Handling
- **Integer costs required** for SimpleMinCostFlow
- **Floating-point costs** supported in advanced solvers (with caveats)
- **Overflow protection:** Uses 64-bit integers, checks for overflow

## API Design Philosophy

### Strengths
- **Bulk operations:** Add arcs via NumPy arrays (minimize Python/C++ boundary crossings)
- **Clear status codes:** OPTIMAL, INFEASIBLE, UNBALANCED, etc.
- **Efficient queries:** Direct arc access via integer IDs, not dictionary lookups
- **Multi-language consistency:** Same API patterns across Python, Java, C#

### Pain Points
- **Verbosity:** More boilerplate than NetworkX (explicit node/arc management)
- **Node IDs must be integers:** 0 to N-1, no arbitrary hashable types
- **Graph is immutable during solve:** Cannot modify arcs after solver instantiation
- **Debugging difficulty:** C++ errors surface as cryptic Python exceptions

## Integration Patterns

### With NumPy (Recommended)
```python
# Efficiently load large graphs from matrices
adjacency = np.array([...])  # Adjacency matrix with costs
sources, targets = np.where(adjacency > 0)
costs = adjacency[sources, targets]
capacities = np.ones_like(costs) * 1000  # Assume high capacity

smcf.add_arcs_with_capacity_and_unit_cost(sources, targets, capacities, costs)
```

### With NetworkX (Migration Pattern)
```python
import networkx as nx

# Prototype in NetworkX
G = nx.DiGraph()
# ... build graph ...

# Convert to OR-Tools for production
smcf = min_cost_flow.SimpleMinCostFlow()
node_map = {n: i for i, n in enumerate(G.nodes())}  # Map names to integers

for u, v, data in G.edges(data=True):
    smcf.add_arc_with_capacity_and_unit_cost(
        node_map[u], node_map[v],
        data.get('capacity', 1000),
        int(data.get('weight', 1))
    )
```

## Advanced Features

### Assignment Problems
OR-Tools specializes in assignment problems (matching workers to tasks):
```python
# Each worker can do each task, minimize total cost
# Automatically formulated as min cost flow internally
from ortools.graph.python import linear_sum_assignment

assignment = linear_sum_assignment.SimpleLinearSumAssignment()
assignment.add_arc_with_cost(worker=0, task=0, cost=90)
# ... add all worker-task pairs ...
assignment.solve()
```

### Constraint Programming Integration
Combine flow with other constraints (CP-SAT solver):
```python
from ortools.sat.python import cp_model

model = cp_model.CpModel()
# Define flow variables with additional constraints
# (e.g., "flow on arc A must equal flow on arc B")
```

## When OR-Tools Implementation Shines

1. **Production logistics:** Warehouse networks, supply chains, transportation
2. **Assignment problems:** Task allocation, resource scheduling
3. **Large-scale graphs:** >10K nodes, need sub-second latency
4. **Multi-language deployment:** Python backend, Java microservices, C# desktop
5. **Constraint programming:** Flow + additional business rules

## When to Use Alternatives

1. **Pure research:** NetworkX has better documentation for learning
2. **Ad-hoc exploration:** Flexible node IDs, easier visualization
3. **Small graphs:** <1K nodes, OR-Tools setup overhead not worth it
4. **Non-optimization focus:** Need centrality, clustering, graph properties

## Debugging and Validation

### Check Solution Status
```python
if status == smcf.OPTIMAL:
    print("Optimal solution found")
elif status == smcf.INFEASIBLE:
    print("No feasible flow (supply/demand mismatch)")
elif status == smcf.UNBALANCED:
    print("Total supply != total demand")
```

### Verify Supply/Demand Balance
```python
total_supply = sum(s for s in supplies if s < 0)
total_demand = sum(s for s in supplies if s > 0)
assert abs(total_supply + total_demand) < 1e-6
```

## Comparative Positioning

OR-Tools is the **production implementation** for network flow. Think of it as the "Postgres of graph optimization" - engineered for reliability, performance, and scale. You pay the API complexity tax upfront, but gain 10-100x performance and Google-scale battle-testing. Prototype in NetworkX, deploy with OR-Tools.
