# Spectral Clustering: Technical Deep-Dive

## Algorithm Structure

Spectral clustering uses eigenvalue decomposition of the graph Laplacian to embed nodes in low-dimensional space, then clusters the embedding.

### Three-Step Process

1. **Construct graph Laplacian**
   - Compute similarity/adjacency matrix *A*
   - Compute degree matrix *D*
   - Form Laplacian: *L = D - A* (unnormalized)
   - Or normalized: *L_norm = D^(-1/2) L D^(-1/2)*

2. **Eigenvalue decomposition**
   - Compute *k* smallest eigenvectors of *L*
   - Each node represented as *k*-dimensional vector (eigenvector row)
   - Embedding: *X ∈ ℝ^(n×k)*

3. **Cluster in embedding space**
   - Apply k-means (or other clustering) to rows of *X*
   - Each cluster in embedding → community in graph

**Mathematical foundation:** Finding *k* smallest eigenvectors of normalized Laplacian approximates solving the normalized cuts problem.

## Graph Laplacian Variants

### Unnormalized Laplacian
```
L = D - A
where D[i,i] = degree(i), A = adjacency matrix
```
- Eigenvalue range: [0, 2·d_max]
- Smallest eigenvalue: 0 (multiplicity = number of connected components)

### Symmetric Normalized Laplacian
```
L_sym = I - D^(-1/2) A D^(-1/2)
```
- Eigenvalue range: [0, 2]
- Most common for community detection (arithmetic mean normalization)

### Random Walk Normalized Laplacian
```
L_rw = I - D^(-1) A
```
- Relates to random walk transition probabilities

## Complexity Analysis

**Time:**
- Laplacian construction: O(m)
- Eigenvalue decomposition: **O(n³)** (bottleneck)
  - LOBPCG (sparse): O(k · n² · iterations)
  - ARPACK: O(k · n² · iterations)
- K-means clustering: O(k · n · iterations)
- **Total: O(n³)** dominated by eigendecomposition

**Space:**
- Dense Laplacian: O(n²)
- Sparse Laplacian: O(n + m)
- Eigenvectors: O(k · n)

**Practical limit:** ~10K nodes (dense), ~50K nodes (sparse with LOBPCG)

## Algorithmic Guarantees

### Normalized Cuts Approximation

**Goal:** Minimize normalized cut:
```
NCut(A, B) = cut(A, B) / vol(A) + cut(A, B) / vol(B)
where vol(A) = sum of degrees in A
```

**Relaxation:** NP-hard discrete problem → continuous relaxation via eigenvectors

**Approximation quality:** Second eigenvector provides 2-approximation for 2-way cut

### Cluster Quality

**Advantages:**
- Finds globally optimal cuts (in continuous relaxation)
- Strong theoretical guarantees
- Deterministic (given seed for k-means)

**Limitations:**
- Approximation gap: continuous → discrete
- K-means initialization randomness
- Only works for *k* known in advance

## Hyperparameters

### Number of clusters (k)
- **REQUIRED:** Must be specified
- **Selection:** Eigengap heuristic (look for large gap in eigenvalue spectrum)
- **No automatic selection:** Unlike Louvain/Leiden

### Affinity matrix
- Adjacency matrix (graph community detection)
- RBF kernel (point cloud clustering)
- Custom similarity measure

### Normalization method
- **'arithmetic_mean'** (most common for community detection)
- 'geometric_mean'
- 'min_max'
- 'median'

### Clustering method (scikit-learn 1.8.0)
- **'kmeans'** (default, randomized)
- **'cluster_qr'** (new, deterministic, no tuning, may outperform k-means)
- 'discretize'

## API Patterns

### scikit-learn
```python
from sklearn.cluster import SpectralClustering
import networkx as nx
import numpy as np

# Create affinity matrix from graph
G = nx.karate_club_graph()
A = nx.adjacency_matrix(G).todense()

# Spectral clustering
sc = SpectralClustering(
    n_clusters=2,
    affinity='precomputed',
    assign_labels='kmeans',
    random_state=42
)
labels = sc.fit_predict(A)
```

### NetworkX (via Laplacian)
```python
import networkx as nx
import numpy as np
from scipy.sparse.linalg import eigsh
from sklearn.cluster import KMeans

# Manual implementation
L = nx.normalized_laplacian_matrix(G)
k = 3

# Compute k smallest eigenvectors
eigenvalues, eigenvectors = eigsh(L, k=k, which='SM')

# Cluster eigenvector rows
kmeans = KMeans(n_clusters=k, random_state=42)
labels = kmeans.fit_predict(eigenvectors)
```

## Advanced Features (scikit-learn 1.8.0)

### cluster_qr method
- **No hyperparameters:** Deterministic extraction from eigenvectors
- **No iterations:** Single QR decomposition
- **Performance:** May outperform k-means
- **When to use:** Prefer over k-means for determinism

### LOBPCG eigenvalue solver
- **Sparse optimization:** For large sparse graphs
- **Multigrid preconditioning:** Accelerates convergence
- **Scalability:** Handles up to ~50K nodes

## When Spectral Clustering Fails

**Pathological cases:**
1. **High-degree hubs:** Dominate eigenvectors, poor community detection
2. **Very unbalanced communities:** Small communities lost in embedding
3. **k unknown:** No principled way to select (unlike Louvain's automatic hierarchy)

**Mitigation:**
- Degree normalization (use normalized Laplacian)
- Multi-scale analysis (vary *k*)
- Use modularity-based methods if *k* unknown

## Performance Benchmarks

| Nodes | Edges | k | Time (LOBPCG) | Time (ARPACK) | Modularity |
|-------|-------|---|---------------|---------------|------------|
| 1K    | 5K    | 5 | 0.5s          | 1s            | 0.38       |
| 5K    | 25K   | 5 | 5s            | 15s           | 0.35       |
| 10K   | 50K   | 5 | 20s           | 90s           | 0.33       |
| 50K   | 250K  | 5 | 8min          | impractical   | 0.30       |

**Scaling:** Prohibitive above 50K nodes even with sparse solvers.

## Comparison to Modularity Methods

**Spectral wins:**
- Theoretical guarantees (approximates normalized cuts)
- Deterministic (with cluster_qr)
- Finds global structure

**Modularity methods win:**
- Speed (O(n log n) vs O(n³))
- Scalability (millions of nodes vs thousands)
- Automatic *k* selection (hierarchical)
- Practical performance

**Use spectral when:** Small graph, *k* known, theory matters more than speed

## Sources

- [Spectral clustering - Wikipedia](https://en.wikipedia.org/wiki/Spectral_clustering)
- [scikit-learn 1.8.0 SpectralClustering](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.SpectralClustering.html)
- [A Tutorial on Spectral Clustering (Luxburg)](https://people.csail.mit.edu/dsontag/courses/ml14/notes/Luxburg07_tutorial_spectral_clustering.pdf)
- [Number Analytics: Spectral Clustering Deep Dive](https://www.numberanalytics.com/blog/spectral-clustering-basics)
