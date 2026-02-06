# Infomap: Technical Deep-Dive

## Algorithm Structure

Infomap minimizes the **map equation**, which measures the description length of a random walker's path using a hierarchical codebook.

### Information-Theoretic Foundation

**Core idea:** Communities = regions where random walker stays longer

**Map equation:** Measures per-step average code length *L(M)* for partition *M*:
```
L(M) = q_⊙ H(Q) + Σ_i p_⊙^i H(P^i)

where:
- q_⊙: rate of switching between modules
- H(Q): entropy of module-level codebook
- p_⊙^i: rate of using module i's codebook
- H(P^i): entropy of module i's internal codebook
```

**Intuition:** Better partition = shorter description = less information needed to describe walker's path

### Random Walk Dynamics

**Transition probability:**
```
P(i → j) = w_ij / w_i
where w_ij = edge weight, w_i = total outgoing weight from i
```

**Ergodic flow:** Steady-state probability *π_i* (PageRank-like)

**Module flow:** Random walker tends to stay within dense regions (modules)

## Three-Phase Algorithm

### Phase 1: Greedy Node Movement

1. **Initialize:** Each node in singleton community
2. **Random sequential order:** For each node *i*:
   - Try moving to each neighbor's module
   - Calculate ΔL (change in map equation)
   - Move to module with largest decrease in *L* (if ΔL < 0)
3. **Iterate:** Until no improvement

### Phase 2: Coarsening

1. **Create meta-network:** Modules become super-nodes
2. **Meta-edges:** Aggregate flow between modules
3. **Self-loops:** Flow within modules

### Phase 3: Recursive Optimization

1. **Apply Phase 1** to meta-network
2. **Repeat** until convergence (no improvement)

**Hierarchical output:** Multi-level module structure

## Complexity Analysis

**Time:**
- Per iteration: O(m) (scan edges)
- Iterations: O(log n) typically
- **Total: O(m log n)** empirical

**Space:** O(n + m) for graph + O(n) for partition

**Practical performance:** Millions of nodes in minutes (C++ implementation)

**Scaling:** Linear with edges (empirically), handles large networks efficiently

## Quality Function: Map Equation Details

**Module-level codebook (Q):**
- One codeword for each module
- Used when random walker exits module
- Entropy: *H(Q) = -Σ q_i log(q_i)*

**Module-internal codebook (P^i):**
- Codewords for nodes within module *i*
- Plus exit codeword (leaving module)
- Entropy: *H(P^i) = -Σ p_j log(p_j) - p_exit log(p_exit)*

**Optimization goal:** Minimize *L(M)* = find modules where walker rarely exits

### Why Map Equation Works

**Short description ↔ Good modules:**
- Frequent switches between modules → long module codebook → high *L*
- Infrequent switches (strong modules) → short codebook → low *L*

**Directedness advantage:** Exploits asymmetric flow patterns (unlike modularity)

## Network Types Supported

### Directed Networks
- **Native support:** Uses directed transition probabilities
- **Flow information:** Exploits asymmetric pathways
- **Example:** Citation networks (papers → papers)

### Weighted Networks
- **Edge weights:** Incorporated in transition probabilities
- **Strength-based:** Uses weighted degree in flow calculations

### Temporal Networks
- **Time-varying:** Edges with timestamps
- **Dynamic flow:** Random walk respects temporal order

### Multiplex Networks
- **Multiple layers:** Different edge types (e.g., social + biological)
- **Inter-layer transitions:** Flow between layers

### Memory Networks (Higher-Order)
- **Second-order:** Remember previous step (node pairs)
- **k-order:** Remember k previous steps
- **Pathways:** Detect flow patterns, not just dense regions

## Hyperparameters

### Teleportation probability (α)
- Default: α = 0.15 (PageRank standard)
- Higher α → more global exploration
- Lower α → more local structure

### Number of trials
- Multiple random initializations
- Keep partition with minimum *L*
- Default: 10 trials

### Hierarchical depth
- Two-level vs multi-level
- Multi-level reveals nested structure

### Markov time
- Scale parameter for flow dynamics
- Default: 1 (standard random walk)

## API Patterns

### Python (infomap package)
```python
import infomap

# Create Infomap object
im = infomap.Infomap("--two-level --directed")

# Add edges
for u, v in G.edges():
    im.add_link(u, v)

# Run algorithm
im.run()

# Extract communities
communities = {}
for node in im.tree:
    if node.is_leaf:
        communities[node.node_id] = node.module_id
```

### NetworkX integration (via CDlib)
```python
from cdlib import algorithms

communities = algorithms.infomap(G)
# Returns NodeClustering object
```

### Command-line interface
```bash
# Input: Pajek format
./Infomap network.net output/

# Options
./Infomap --two-level --directed --num-trials 100 network.net output/
```

## Advanced Features

### Overlapping Communities
- **Node splitting:** Assign node to multiple modules with flow allocation
- **Flow-based:** Overlap based on actual flow distribution

### Significance Testing
- **Null model:** Random graph with same degree distribution
- **p-values:** Statistical significance of modules

### Visualization
- **Alluvial diagrams:** Hierarchical flow visualization
- **Map generator:** Interactive web-based visualization

## Performance Benchmarks

| Network | Nodes | Edges | Time | Modules | Codelength |
|---------|-------|-------|------|---------|------------|
| Karate  | 34    | 78    | <0.1s| 2-4     | 3.45 bits  |
| Dolphins| 62    | 159   | 0.1s | 4-5     | 4.32 bits  |
| Email   | 1K    | 25K   | 1s   | 15-20   | 6.2 bits   |
| Web     | 1M    | 5M    | 5min | 5000    | 11.8 bits  |
| Large   | 10M   | 50M   | 45min| 50000   | 15.2 bits  |

**Codelength:** Lower = better partition

## When Infomap Excels

**Best scenarios:**
1. **Directed networks:** Citation, web graphs, metabolic networks
2. **Weighted flows:** Transportation, communication networks
3. **Hierarchical structure:** Nested communities important
4. **Higher-order patterns:** Pathways matter (use memory networks)

**Avoid when:**
- Simple undirected graphs (Leiden simpler/faster)
- Explainability critical (modularity easier to explain)
- Quick prototype (Louvain faster to implement)

## Comparison to Modularity Methods

**Infomap advantages:**
- Directed network support
- Information-theoretic foundation (no resolution limit)
- Multi-scale hierarchy
- Flow-based (dynamics-aware)

**Modularity advantages:**
- Simpler to explain
- Faster for simple undirected graphs
- More widespread adoption

## Sources

- [Infomap - Network community detection](https://www.mapequation.org/infomap/)
- [Community Detection with the Map Equation and Infomap (ACM Computing Surveys)](https://dl.acm.org/doi/10.1145/3779648)
- [arXiv: Community Detection with the Map Equation](https://arxiv.org/abs/2311.04036)
- [Identifying flow modules in ecological networks](https://besjournals.onlinelibrary.wiley.com/doi/full/10.1111/2041-210X.13569)
- [Infomap Python Module Documentation](https://mapequation.github.io/infomap/python/infomap.html)
