# Spectral Clustering Community Detection

## Overview

Spectral clustering uses linear algebra and graph theory, performing eigenvalue decomposition on the graph Laplacian to find communities. It's mathematically elegant but computationally expensive.

**Key Stats:**
- **Ecosystem:** scikit-learn (67K+ GitHub stars), SciPy ecosystem
- **Maintenance:** Active, stable API (scikit-learn 1.8.0)
- **Performance:** O(n³) time complexity (eigendecomposition bottleneck)
- **Output:** Non-overlapping communities, fixed number of clusters

## When to Use

**Best for:**
- Small to medium graphs (<10K nodes)
- When you know the exact number of communities in advance
- Academic research requiring mathematical rigor
- Integration with existing scikit-learn ML pipelines

**Avoid when:**
- Graph has >50K nodes (prohibitively slow)
- Number of communities is unknown
- You need hierarchical community structure
- Speed is a constraint

## Strengths

1. **Theoretical foundation:** Strong mathematical guarantees, well-understood
2. **Quality:** Finds globally optimal normalized cuts
3. **Ecosystem:** Seamless integration with scikit-learn workflows
4. **Stability:** Deterministic with consistent hyperparameters

## Limitations

1. **Speed:** Cubic time complexity makes it impractical for large graphs
2. **K must be known:** Requires specifying number of communities upfront
3. **Scalability:** Only viable for small graphs
4. **Memory:** High memory requirements for eigendecomposition

## Algorithm Details

**Recent improvements (scikit-learn 1.8.0):**
- **cluster_qr method:** Extracts clusters directly from eigenvectors, no tuning, may outperform k-means
- **LOBPCG with multigrid:** Accelerated eigenvalue computation

**Normalization methods:** Arithmetic mean is most common for community detection

## Ecosystem Maturity

**Mature but niche.** Well-maintained within scikit-learn, but rarely used for large-scale community detection due to speed constraints.

**Recommendation tier:** **Only for small graphs with known K**, otherwise use Louvain/Leiden.

## Sources

- [scikit-learn 1.8.0 SpectralClustering Documentation](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.SpectralClustering.html)
- [Spectral Clustering Wikipedia](https://en.wikipedia.org/wiki/Spectral_clustering)
- [GitHub: communities library](https://github.com/shobrook/communities)
- [Kaggle: Spectral Clustering Detailed Explanation](https://www.kaggle.com/code/vipulgandhi/spectral-clustering-detailed-explanation)
