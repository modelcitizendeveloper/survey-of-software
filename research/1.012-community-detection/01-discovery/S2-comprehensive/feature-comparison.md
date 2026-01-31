# Feature Comparison Matrix

## Algorithm Complexity Comparison

| Algorithm | Time | Space | Deterministic | Converges | K Required |
|-----------|------|-------|---------------|-----------|------------|
| Louvain | O(n log n) | O(n+m) | No | Yes | No (auto) |
| Leiden | O(m) per iter | O(n+m) | No | Yes | No (auto) |
| Label Prop | O(m·k) | O(n) | No | Maybe* | No (auto) |
| Spectral | O(n³) | O(n²) | Partial** | Yes | Yes (required) |
| Infomap | O(m log n) | O(n+m) | No | Yes | No (auto) |

\* Asynchronous converges, synchronous may oscillate
\*\* Deterministic with cluster_qr, randomized with k-means

## Quality Guarantees

| Algorithm | Connectedness | Optimality | Resolution Limit |
|-----------|---------------|------------|------------------|
| Louvain | ❌ None | Local (modularity) | Yes (√m) |
| Leiden | ✅ Guaranteed | Subset-optimal* | Yes (√m) |
| Label Prop | ❌ None | None | No |
| Spectral | ✅ Guaranteed | Global (continuous)** | No |
| Infomap | ✅ Guaranteed | Local (map eq) | No |

\* When iterated to convergence
\*\* Approximates normalized cuts in continuous relaxation

## Scalability Comparison

| Algorithm | 1K nodes | 10K nodes | 100K nodes | 1M nodes | 10M nodes |
|-----------|----------|-----------|------------|----------|-----------|
| Louvain | 0.1s | 2s | 45s | 21min | Slow |
| Leiden | 0.05s | 1s | 15s | 8min | 1-2h |
| Label Prop | 0.2s | 3s | 30s | 5min | 1h |
| Spectral | 0.5s | 20s | 8min | Impractical | ❌ |
| Infomap | 0.1s | 1s | 5min | 45min | 8h |

**Performance notes:**
- GPU Leiden: 315x faster than CPU Louvain for large graphs
- GVE-LPA: 1.4B edges/s (custom implementation)
- Spectral: Practical limit ~50K nodes

## Network Type Support

| Algorithm | Directed | Weighted | Temporal | Multiplex | Overlapping |
|-----------|----------|----------|----------|-----------|-------------|
| Louvain | Partial* | ✅ Yes | ❌ No | ❌ No | ❌ No |
| Leiden | Partial* | ✅ Yes | ❌ No | ❌ No | ❌ No |
| Label Prop | Partial* | ✅ Yes | ✅ Yes | ❌ No | ❌ No |
| Spectral | ❌ No | ✅ Yes | ❌ No | ❌ No | ❌ No |
| Infomap | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |

\* Treats directed edges as undirected or uses symmetrized adjacency

## Modularity Scores (Typical)

| Graph Type | Louvain | Leiden | Label Prop | Spectral | Infomap |
|------------|---------|--------|------------|----------|---------|
| Social (Karate) | 0.42 | 0.42 | 0.32 | 0.38 | N/A*** |
| Collaboration | 0.40 | 0.41 | 0.28 | 0.35 | N/A*** |
| Citation | 0.38 | 0.39 | 0.25 | 0.33 | N/A*** |
| Web | 0.35 | 0.36 | 0.22 | Impractical | N/A*** |

**Note:** Leiden typically 0.01-0.02 higher than Louvain
***Infomap uses map equation (codelength), not modularity

## Hyperparameter Sensitivity

| Algorithm | Critical Params | Default Works? | Tuning Effort |
|-----------|-----------------|----------------|---------------|
| Louvain | resolution | ✅ Usually | Low |
| Leiden | resolution, n_iterations | ✅ Usually | Low |
| Label Prop | max_iterations | ⚠️ Sometimes | Medium |
| Spectral | k (num clusters) | ❌ No | High |
| Infomap | teleportation | ✅ Usually | Low |

## API Integration Patterns

| Algorithm | NetworkX Native | igraph Support | scikit-learn | Standalone |
|-----------|-----------------|----------------|--------------|------------|
| Louvain | ✅ 3.x+ | ✅ Via python-louvain | ❌ No | python-louvain |
| Leiden | ❌ No | ✅ leidenalg | ❌ No | leidenalg |
| Label Prop | ✅ Yes | ✅ Yes | ❌ No | NetworKit |
| Spectral | Manual* | Manual* | ✅ Yes | scikit-learn |
| Infomap | ❌ No | ❌ No | ❌ No | infomap |

\* Construct Laplacian manually, use SpectralClustering on adjacency matrix

## Implementation Languages

| Algorithm | Primary Lang | Python Bindings | Performance Notes |
|-----------|--------------|-----------------|-------------------|
| Louvain | Python | Native | Pure Python (NetworkX) or C++ (python-louvain) |
| Leiden | C++ | leidenalg | C++ core, 20x faster than Louvain |
| Label Prop | C++ | NetworKit | C++ kernel, Python frontend |
| Spectral | C/Fortran | scipy/BLAS | Eigensolvers highly optimized |
| Infomap | C++ | infomap | C++ core, command-line or Python API |

**Performance implication:** C++ implementations (Leiden, NetworKit, Infomap) significantly faster than pure Python (NetworkX Louvain, Label Prop)

## Memory Footprint

| Algorithm | 10K nodes, 50K edges | 100K nodes, 500K edges | Notes |
|-----------|---------------------|------------------------|-------|
| Louvain | ~10 MB | ~100 MB | Graph + community labels |
| Leiden | ~12 MB | ~120 MB | +refinement overhead |
| Label Prop | ~8 MB | ~80 MB | Minimal (just labels) |
| Spectral | ~800 MB | Impractical | Dense Laplacian O(n²) |
| Infomap | ~10 MB | ~100 MB | Graph + flow state |

**Spectral note:** Sparse matrices reduce memory, but still O(n²) for eigendecomposition

## Output Format Comparison

| Algorithm | Output Type | Hierarchical | Overlapping | Metadata |
|-----------|-------------|--------------|-------------|----------|
| Louvain | List[Set] or Dict | ✅ Yes (dendrogram) | ❌ No | Modularity |
| Leiden | List[int] (igraph) | ✅ Yes (multi-level) | ❌ No | Quality score |
| Label Prop | Generator[Set] | ❌ No | ❌ No | None |
| Spectral | ndarray (labels) | ❌ No | ❌ No | None |
| Infomap | Tree structure | ✅ Yes (nested) | ✅ Optional | Codelength |

## Use Case Match

| Use Case | Best Algorithm | Why |
|----------|----------------|-----|
| **Quick prototype** | Louvain (NetworkX) | Native, familiar, fast enough |
| **Production** | Leiden | Faster, guarantees, fixes Louvain defects |
| **Billion-edge graph** | Label Prop (NetworKit) | Only algorithm that scales |
| **Directed network** | Infomap | Exploits flow asymmetry |
| **Small graph, known K** | Spectral | Mathematical rigor, deterministic |
| **Research/comparison** | CDlib | 39+ algorithms, evaluation framework |
| **Hierarchical structure** | Infomap or Leiden | Multi-level output |
| **Temporal network** | Infomap or Label Prop | Dynamic support |

## Ecosystem Maturity

| Library | GitHub Stars | Last Update | Documentation | Community |
|---------|--------------|-------------|---------------|-----------|
| NetworkX | 16.5K | Active | Excellent | Large |
| leidenalg | ~300 | Active | Good | Growing |
| python-louvain | ~1K | Maintenance | Minimal | Stable |
| scikit-learn | 67K | Active | Excellent | Huge |
| infomap | ~200 | Active | Good | Specialized |
| NetworKit | ~800 | Active | Good | Academic |
| CDlib | ~405 | Active | Excellent | Research |

**Stability ranking:** scikit-learn > NetworkX > leidenalg > CDlib > infomap > NetworKit > python-louvain
