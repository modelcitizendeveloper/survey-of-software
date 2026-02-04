# Louvain Algorithm: Technical Deep-Dive

## Algorithm Structure

Louvain operates in two alternating phases until no modularity improvement is possible:

### Phase 1: Local Node Movement

1. **Initialization:** Each node assigned to its own community
2. **Iteration:** For each node *i* in random order:
   - Calculate modularity gain ΔQ for moving *i* to each neighbor's community *j*
   - Move *i* to the community yielding maximum positive ΔQ (or stay if all ΔQ ≤ 0)
3. **Termination:** Repeat until no further moves improve modularity

**Modularity gain formula:**
```
ΔQ = [Σin + ki,in / 2m - (Σtot + ki)² / 4m²] - [Σin / 2m - Σtot² / 4m² - (ki / 2m)²]
```
Where:
- Σin = sum of weights inside community C
- Σtot = sum of weights incident to nodes in C
- ki = weighted degree of node i
- ki,in = sum of weights from i to nodes in C
- m = total edge weight in graph

### Phase 2: Network Aggregation

1. **Community contraction:** Create meta-graph where each community becomes a node
2. **Weight aggregation:**
   - Inter-community edges → meta-edges with summed weights
   - Intra-community edges → self-loops on meta-nodes
3. **Recursion:** Apply Phase 1 to meta-graph

**Termination:** Algorithm stops when:
- No modularity gain achieved (ΔQ < threshold, typically 1e-7)
- Maximum hierarchy depth reached (default: unlimited)

## Complexity Analysis

**Time:** O(n log n) empirical, though exact worst-case unknown
- Phase 1: O(m) per pass, typically few passes
- Phase 2: O(m) graph reconstruction
- Hierarchy depth: O(log n) typically

**Space:** O(n + m) for graph + O(n) for community assignments

**Practical performance:** Scales to 500K nodes on commodity hardware (single-threaded)

## The Disconnected Communities Problem

**Critical defect:** Louvain does not guarantee community connectivity.

**Why it happens:**
1. Modularity only considers edge density, not path connectivity
2. Local moves can create "bridge nodes" connecting otherwise disconnected subgraphs
3. Phase 2 aggregation can merge disconnected components if modularity improves

**Empirical frequency:** Up to 16% of communities disconnected, 25% badly connected

**Example pathology:**
```
Community A: nodes {1,2,3} fully connected, plus isolated node 4
Modularity may be higher with node 4 in A than elsewhere
Result: "Community A" is technically disconnected
```

## Hyperparameter Sensitivity

**Resolution parameter (γ):**
- Controls community size preference
- γ < 1: Favors larger communities
- γ > 1: Favors smaller communities
- Default: γ = 1 (standard modularity)

**Random seed:**
- Node ordering affects results (non-deterministic)
- Multiple runs recommended, consensus partitioning

**Convergence threshold:**
- Lower threshold → more iterations, slightly better Q
- Typical: 1e-7 (good tradeoff)

## API Patterns

### NetworkX (native)
```python
import networkx as nx
from networkx.algorithms.community import louvain_communities

G = nx.karate_club_graph()
communities = louvain_communities(G, seed=42, resolution=1.0)
# Returns: list of sets of nodes
```

### python-louvain (standalone)
```python
import community as community_louvain  # python-louvain
import networkx as nx

G = nx.karate_club_graph()
partition = community_louvain.best_partition(G)
# Returns: dict {node: community_id}
```

## When Louvain Fails

**Disconnection risk scenarios:**
1. Sparse graphs with bridge nodes
2. Iterative refinement (risk compounds)
3. Networks with natural bottleneck structure

**Mitigation:**
- Post-process: Split disconnected communities
- Use Leiden instead (fixes defect)
- Validate: Check `nx.is_connected(G.subgraph(community))`

## Performance Benchmarks

| Graph Size | Nodes | Edges | Time (NetworkX) | Modularity |
|------------|-------|-------|-----------------|------------|
| Small      | 1K    | 10K   | 0.1s            | 0.42       |
| Medium     | 10K   | 100K  | 2s              | 0.38       |
| Large      | 100K  | 1M    | 45s             | 0.35       |
| Very Large | 1M    | 10M   | 21min           | 0.32       |

**Note:** Performance degrades dramatically above 500K nodes. Consider GPU-accelerated Leiden for >1M nodes.

## Strengths vs Limitations

**Strengths:**
- Fast convergence on most graphs
- High modularity scores
- Simple to explain and implement
- Widely adopted (battle-tested)

**Limitations:**
- No connectivity guarantees
- Non-deterministic results
- Resolution limit (can't detect communities smaller than √m)
- Superseded by Leiden

## Sources

- [Louvain method - Wikipedia](https://en.wikipedia.org/wiki/Louvain_method)
- [NetworkX 3.6.1 louvain_communities](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.community.louvain.louvain_communities.html)
- [Demystifying Louvain's Algorithm and Its implementation in GPU (Medium)](https://medium.com/walmartglobaltech/demystifying-louvains-algorithm-and-its-implementation-in-gpu-9a07cdd3b010)
- [From Louvain to Leiden](https://www.nature.com/articles/s41598-019-41695-z)
