# Label Propagation: Technical Deep-Dive

## Algorithm Structure

Label propagation uses a simple consensus mechanism: nodes adopt the most common label among their neighbors.

### Basic Algorithm

1. **Initialization:** Each node assigned unique label
2. **Propagation:** For each node *i* (in some order):
   - Count label frequencies among neighbors *N(i)*
   - Adopt most frequent label (ties broken randomly)
3. **Termination:** Stop when labels stabilize or max iterations reached

**Pseudocode:**
```
initialize: label[i] = i for all nodes
while not converged:
    for node i in order:
        label[i] = most_common_label(neighbors(i))
```

## Update Strategy Variants

### Asynchronous (LPA-Classic)
- **Order:** Nodes updated sequentially in random order
- **Convergence:** Guaranteed (each update uses latest neighbor labels)
- **Performance:** Sequential bottleneck, hard to parallelize
- **Stability:** Better, labels converge to fixed point

### Synchronous (LPA-Sync)
- **Order:** All nodes updated simultaneously
- **Convergence:** NOT guaranteed (may oscillate)
- **Performance:** Fully parallelizable
- **Stability:** Worse, can oscillate indefinitely on bipartite graphs

**Oscillation example (bipartite graph):**
```
Iteration 0: A={1,2}, B={3,4}
Iteration 1: All nodes see 50/50 split → flip
Iteration 2: Back to Iteration 0 state
Result: Period-2 oscillation, never converges
```

### Semi-Synchronous (SLPA, LALPA)
- **Order:** Certain node sets updated synchronously, others asynchronously
- **Convergence:** Provably converges to stable labeling
- **Performance:** Parallelizable with guarantees
- **Adoption:** LALPA (2025) uses node importance measures for ordered updates

## Complexity Analysis

**Time:**
- Per iteration: O(m) where m = number of edges
- Iterations: Unknown theoretically, typically O(log n) to O(n)
- Total: O(m · k) where k = iterations

**Space:** O(n) for label array

**Practical performance:**
- **Basic LPA:** 700x faster than naive implementations
- **GVE-LPA:** 1.4 billion edges/s throughput
- **FLPA (queue-based):** Near-linear scaling

## Convergence Properties

**Termination guarantee:**
- **Asynchronous:** Always terminates at local maximum
- **Synchronous:** May never converge (oscillate)
- **Semi-synchronous:** Provably converges

**Convergence criterion:**
All labels are "maximal": no node can improve by changing label.

**Typical iterations:**
- Sparse graphs: 5-10 iterations
- Dense graphs: 10-50 iterations
- Poorly structured: May not converge (set max_iterations limit)

## Stability and Determinism

**Problem:** LPA is highly non-deterministic
- Random initialization → different results
- Node ordering → different results
- Tie-breaking → different results

**Impact:**
- Modularity variance: ±0.05 across runs
- Community assignment variance: 20-30% nodes change communities

**Mitigations:**
1. **Multiple runs + consensus:** Run 100+ times, keep consensus partition
2. **Ordering strategies:** Use degree-based or betweenness-based ordering (LALPA)
3. **Hybrid approaches:** LPA for initial guess, refine with Louvain

## Quality Metrics

**Modularity:** Typically 0.05-0.1 lower than Louvain/Leiden

**Why lower quality?**
- Greedy local decisions, no global optimization
- Early convergence to local maximum
- High sensitivity to initialization

**When acceptable:**
- Rough clustering for visualization
- Preprocessing for refinement
- Speed critical, approximate quality sufficient

## Advanced Variants

### MILPA (Multi-level Iterative LPA)
- **Innovation:** Multi-level coarsening + refinement
- **Performance:** Best NMI scores in recent benchmarks
- **Complexity:** Higher than basic LPA

### LALPA (Label Acceptance-based LPA, 2025)
- **Innovation:** Node importance measures for ordered updates
- **Stability:** More stable than random ordering
- **Convergence:** Faster, fewer oscillations

### GVE-LPA (Graph Value Estimation LPA)
- **Innovation:** Parallel implementation with value estimation
- **Performance:** 1.4B edges/s (vs competitors at ~0.1B edges/s)
- **Scalability:** Handles billions of edges

## API Patterns

### NetworkX
```python
import networkx as nx
from networkx.algorithms.community import label_propagation_communities

G = nx.karate_club_graph()
communities = label_propagation_communities(G)
# Returns: generator of sets of nodes

# Control iterations
communities_list = list(label_propagation_communities(G))
```

### NetworKit (fast C++ implementation)
```python
import networkit as nk

# Convert from NetworkX
G_nk = nk.nxadapter.nx2nk(G)

# Run LPA
lp = nk.community.PLP(G_nk)
lp.run()
communities = lp.getPartition()
```

## When Label Propagation Excels

**Best scenarios:**
1. **Billion-edge graphs:** Only algorithm that scales
2. **Streaming graphs:** Online updates possible
3. **Approximation acceptable:** Speed >> quality
4. **Quick visualization:** Rough clustering for layout

**Avoid when:**
- Results must be deterministic
- High modularity required
- Unclear community structure (slow convergence)

## Performance Benchmarks

| Implementation | Nodes | Edges | Time | Modularity |
|----------------|-------|-------|------|------------|
| NetworkX LPA   | 1K    | 10K   | 0.2s | 0.32       |
| NetworkX LPA   | 10K   | 100K  | 3s   | 0.28       |
| NetworKit LPA  | 100K  | 1M    | 5s   | 0.30       |
| NetworKit LPA  | 1M    | 10M   | 45s  | 0.27       |
| GVE-LPA        | 10M   | 100M  | 90s  | 0.25       |

**Note:** Modularity consistently lower than Louvain (~0.40) but 10-50x faster.

## Sources

- [A semi-synchronous label propagation algorithm](https://www.nature.com/articles/srep45836)
- [Community detection via semi-synchronous label propagation](https://arxiv.org/abs/1103.4550)
- [Label propagation algorithm: A semi-synchronous approach](https://www.researchgate.net/publication/264817879_Label_propagation_algorithm_A_semi-synchronous_approach)
- [Large network community detection by fast label propagation](https://www.nature.com/articles/s41598-023-29610-z)
- [Label Acceptance based label propagation (2025)](https://www.sciencedirect.com/science/article/abs/pii/S030645732500514X)
