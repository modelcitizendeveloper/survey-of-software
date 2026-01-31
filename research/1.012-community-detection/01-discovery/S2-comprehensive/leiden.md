# Leiden Algorithm: Technical Deep-Dive

## Algorithm Structure

Leiden extends Louvain with a critical **refinement phase** that guarantees well-connected communities.

### Three-Phase Iteration

1. **Local Move Phase** (similar to Louvain Phase 1)
   - Each node moves to neighboring community maximizing quality function
   - Uses modularity (or CPM, Significance, etc.)

2. **Refinement Phase** (NEW - fixes Louvain's defect)
   - Split communities into well-connected subcommunities
   - Ensure each node is sufficiently connected to its refined community
   - Merges subcommunities only if they maintain connectivity

3. **Aggregation Phase** (similar to Louvain Phase 2)
   - Create meta-graph from **refined** partition (not original partition)
   - Recursively apply algorithm

**Key innovation:** Aggregating refined partition (not coarse partition) prevents disconnected communities from forming.

## Refinement Phase Details

### Algorithm

1. **Initialize:** Each node in singleton community (within its original community)
2. **Merge condition:** Node *i* merges with subcommunity *S* if:
   - Both *i* and *S* are well-connected to the original community *C*
   - Merging improves quality function
3. **Well-connectedness test:**
   - Subset *R* ⊂ *C* is well-connected if removing *R* doesn't disconnect remaining nodes
   - Efficiently checked via degree ratios

### Example

```
Original Louvain community: {1,2,3,4,5,6}
Graph: 1-2-3  4-5-6  (disconnected components)

Louvain: Keeps as one community (modularity optimized)
Leiden refinement: Splits into {1,2,3} and {4,5,6}
Result: Two well-connected communities
```

## Complexity Analysis

**Time:** O(m) per iteration, faster than Louvain in practice
- Local move: O(m)
- Refinement: O(m) (linear scan)
- Aggregation: O(m)
- Fewer iterations due to better moves

**Space:** O(n + m)

**Performance advantage:** 20x faster than Louvain on large networks (Web UK 2005: 39M nodes)

**Why faster despite extra phase?**
- Better quality moves → fewer iterations
- Avoids pathological cases that slow Louvain
- More efficient C++ implementation (leidenalg)

## Quality Guarantees

### 1. Connected Communities
**Guarantee:** All communities are guaranteed to be connected.

**Proof sketch:** Refinement phase explicitly checks connectivity and splits disconnected components.

### 2. Subset Optimality (when iterated)
**Guarantee:** Converges to partition where all subsets of all communities are locally optimally assigned.

**Meaning:** No subset of nodes can improve quality by moving together to another community.

### 3. No Disconnected Components
**Empirical:** 0% disconnected communities (vs 16% for Louvain)

## Hyperparameters

### Resolution parameter (γ)
Same as Louvain, controls community size.

### Quality function
- **Modularity** (default): Standard community detection
- **CPM** (Constant Potts Model): Resolution-limit-free
- **Significance:** Statistical approach
- **Surprise:** Information-theoretic

### n_iterations
Number of times to refine partition (default: 2)
- More iterations → better quality, more time
- Typically 2-3 sufficient

## API Patterns

### leidenalg (recommended)
```python
import leidenalg
import igraph as ig

# Convert NetworkX to igraph
G_ig = ig.Graph.from_networkx(G)

# Find partition
partition = leidenalg.find_partition(
    G_ig,
    leidenalg.ModularityVertexPartition,
    n_iterations=2,
    seed=42
)

# Access communities
communities = partition.membership  # List of community IDs
modularity = partition.quality()
```

### CDlib wrapper
```python
from cdlib import algorithms

communities = algorithms.leiden(G, resolution=1.0)
```

## Performance Benchmarks

| Graph Size | Nodes | Edges | Leiden Time | Louvain Time | Speedup |
|------------|-------|-------|-------------|--------------|---------|
| Small      | 1K    | 10K   | 0.05s       | 0.1s         | 2x      |
| Medium     | 10K   | 100K  | 1s          | 2s           | 2x      |
| Large      | 100K  | 1M    | 15s         | 45s          | 3x      |
| Very Large | 1M    | 10M   | 8min        | 21min        | 2.6x    |
| Huge       | 39M   | 783M  | 42min       | 14h          | 20x     |

**Note:** Speedup increases with graph size. Leiden handles pathological graphs where Louvain struggles.

## When to Use Leiden

**Use Leiden instead of Louvain when:**
- Production deployment (guaranteed quality)
- Iterative refinement required
- Community connectivity matters
- Large graphs (>100K nodes) - faster anyway

**Use Louvain instead when:**
- Quick prototype/exploration
- Pedagogical explanations (simpler algorithm)
- Legacy codebase compatibility

## Advanced Features

### Hierarchical communities
```python
partition_hierarchy = leidenalg.find_partition(
    G_ig,
    leidenalg.ModularityVertexPartition,
    n_iterations=-1  # Iterate until convergence
)
```

### Custom quality functions
```python
# Constant Potts Model (resolution-limit-free)
partition = leidenalg.find_partition(
    G_ig,
    leidenalg.CPMVertexPartition,
    resolution_parameter=0.5
)
```

## Implementation Note

Leiden is implemented in C++ (leidenalg) with Python bindings, not pure Python like NetworkX Louvain. This contributes to its speed advantage.

## Sources

- [From Louvain to Leiden: guaranteeing well-connected communities](https://www.nature.com/articles/s41598-019-41695-z)
- [Leiden algorithm - Wikipedia](https://en.wikipedia.org/wiki/Leiden_algorithm)
- [leidenalg Documentation](https://leidenalg.readthedocs.io/en/stable/reference.html)
- [From Louvain to Leiden (PDF)](https://www.traag.net/wp/wp-content/papercite-data/pdf/traag_leiden_algo_2018.pdf)
