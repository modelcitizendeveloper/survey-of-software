# dtaidistance: Fast DTW Distance Calculations

## Overview

**dtaidistance** is a specialized Python library focused exclusively on computing Dynamic Time Warping (DTW) distances quickly and efficiently. It provides both pure Python and highly optimized C implementations, making it the fastest DTW library available for Python. Unlike comprehensive toolkits (tslearn, sktime), dtaidistance does one thing extremely well: calculate DTW distances.

**Current Version**: 2.3.9

**Primary Maintainer**: Wannes Meert (KU Leuven DTAI Research Group)

**Repository**: https://github.com/wannesm/dtaidistance

## Core Features

### Dynamic Time Warping Distance
- **Standard DTW**: Classic DTW distance between two time series
- **Weighted DTW**: Penalize warping with custom weight functions
- **Constrained DTW**: Sakoe-Chiba band (window parameter) for faster computation
- **Pruneddtw**: Automatically sets max_dist to Euclidean distance for speedup
- **Warping paths**: Extract the alignment path between series
- **Best path**: Find optimal warping path

### Distance Matrix Computation
- **All-pairs distances**: Compute NxN distance matrix efficiently
- **Parallel computation**: Multi-threaded distance matrix calculation
- **Memory-efficient**: Avoids unnecessary data copies
- **Block processing**: Process large matrices in chunks

### Performance Optimizations
- **Pure Python implementation**: Available for compatibility/debugging
- **C implementation**: 30-300x faster than pure Python
- **Cython dependency only**: Minimal dependencies for C version
- **NumPy/Pandas compatible**: Works with standard data structures
- **64-bit optimization**: Uses ssize_t for larger data structures on 64-bit systems

## Performance Characteristics

**Computational Complexity**:
- Unconstrained DTW: O(nm) where n, m are series lengths
- With Sakoe-Chiba band (window w): O(nw) - linear in series length
- Distance matrix: O(k²nm) for k series

**Scalability**:
- **Single pair**: Sub-millisecond for series <1000 points (C version)
- **Distance matrix**: Efficiently handles 100s-1000s of series
- **Parallel processing**: Near-linear speedup with multiple cores
- Memory: O(nm) for DTW, O(k²) for distance matrix

**Speed Benchmarks** (C implementation):
- 2 series (length 1000): ~0.1ms
- 100x100 distance matrix (length 1000): ~5 seconds (single core)
- 1000x1000 distance matrix: ~10 minutes (8 cores with parallelization)
- **30-300x faster** than pure Python implementations

## Ecosystem Integration

**Dependencies**:
- **Minimal**: Cython (for C implementation), NumPy (optional but recommended)
- **Optional**: None (extremely lightweight)
- **Compatible**: Pandas, scikit-learn, tslearn

**Installation**:
```bash
pip install dtaidistance
# Or with C acceleration (pre-compiled wheels available):
pip install dtaidistance[numpy]
```

**Compatibility**:
- Python 3.7+
- Works with NumPy arrays, Pandas Series, Python lists
- No additional dependencies for core functionality
- Cross-platform: Windows, macOS, Linux

## Community and Maintenance

**GitHub Statistics** (as of 2026-01):
- Stars: ~1.1k
- Contributors: 15+
- Active development by DTAI Research Group (KU Leuven)
- Used as backend for other libraries

**Documentation Quality**:
- Comprehensive DTW tutorial
- API reference
- Performance optimization guide
- Examples for common use cases

**Maintenance Status**: ✅ Actively maintained
- Regular updates and bug fixes
- Responsive to issues
- Production-grade quality
- Used in academic research

**Academic Foundation**:
- Developed by DTAI (Declaratieve Talen en Artificiële Intelligentie) Research Group
- Based on established DTW algorithms
- Used in time series research publications

## Primary Use Cases

### Fast DTW Distance Matrix
- **Scenario**: Compute all-pairs DTW distances for 1000 time series
- **Approach**: Use `distance_matrix_fast()` with parallelization
- **Benefit**: 30-300x faster than pure Python, near-linear scaling with cores

### Time Series Clustering Preprocessing
- **Scenario**: Cluster time series using hierarchical clustering with DTW
- **Approach**: Compute DTW distance matrix → scipy.cluster.hierarchy.linkage
- **Benefit**: Fast DTW computation enables clustering large datasets

### K-Nearest Neighbors with DTW
- **Scenario**: Find k most similar time series to a query
- **Approach**: Compute DTW from query to all candidates, sort, take top-k
- **Benefit**: Constrained DTW (window) provides major speedup

### Time Series Search
- **Scenario**: Search database for series similar to a query pattern
- **Approach**: Use PrunedDTW to quickly filter out dissimilar candidates
- **Benefit**: Automatic pruning based on Euclidean lower bound

### Warping Path Visualization
- **Scenario**: Understand how two time series align under DTW
- **Approach**: Use `warping_paths()` to extract alignment, visualize
- **Benefit**: Debugging and interpretability for DTW-based methods

## Strengths

1. **Extreme speed**: 30-300x faster than pure Python DTW implementations
2. **Minimal dependencies**: Only requires Cython for C version
3. **Specialized focus**: Does DTW extremely well (not bloated)
4. **Parallel support**: Built-in multi-threading for distance matrices
5. **Memory-efficient**: Careful memory management, no unnecessary copies
6. **64-bit optimized**: Handles large data structures efficiently
7. **Production-ready**: Stable, well-tested, used in research
8. **Multiple variants**: Standard, weighted, constrained, pruned DTW

## Limitations

1. **DTW only**: No shapelets, matrix profiles, or other similarity methods
2. **No ML models**: Just distance computation (not a classification library)
3. **No visualization**: Provides data, not plots (use matplotlib separately)
4. **No GPU support**: CPU-bound implementation
5. **Limited high-level API**: Lower-level than tslearn/sktime (fewer conveniences)
6. **Manual integration**: Must combine with sklearn/scipy for clustering/classification

## Comparison to Alternatives

**vs. tslearn (DTW)**:
- dtaidistance: 10-50x faster for pure DTW distance calculations
- tslearn: Broader toolkit (DTW + clustering + classification + shapelets)

**vs. sktime (DTW distances)**:
- dtaidistance: Faster, more DTW variants, optimized C code
- sktime: More distance metrics beyond DTW, full ML framework

**vs. STUMPY (Matrix Profile)**:
- dtaidistance: Pairwise DTW distances
- STUMPY: All-pairs similarity (matrix profile), motif/discord discovery

**vs. fastdtw library**:
- dtaidistance: More accurate (exact DTW), better maintained
- fastdtw: Approximate DTW (O(n) complexity but less accurate)

## Decision Criteria

**Choose dtaidistance when**:
- Need the fastest possible DTW distance calculations
- Computing large distance matrices (100+ time series)
- Building DTW-based clustering or KNN from scratch
- Require minimal dependencies (embedded systems, containers)
- Performance is critical (production systems with tight latency)
- Want fine-grained control over DTW parameters (window, weights)
- Need exact DTW (not approximations)

**Avoid dtaidistance when**:
- Need a complete ML toolkit (use tslearn or sktime instead)
- Require similarity methods beyond DTW (matrix profile → STUMPY)
- Want high-level APIs and less coding (sktime abstracts more)
- Need GPU acceleration for massive datasets
- Prefer approximate DTW for speed (fastdtw might be better)

## Getting Started Example

```python
import numpy as np
from dtaidistance import dtw, dtw_ndim
from dtaidistance.dtw import distance_matrix_fast, warping_paths

# Two time series
series1 = np.array([0, 1, 2, 3, 4, 3, 2, 1, 0])
series2 = np.array([0, 0, 1, 2, 3, 4, 3, 2, 1])

# Compute DTW distance
dist = dtw.distance(series1, series2)
print(f"DTW distance: {dist:.3f}")

# Compute DTW with Sakoe-Chiba band (window constraint)
dist_constrained = dtw.distance(series1, series2, window=2)
print(f"Constrained DTW distance: {dist_constrained:.3f}")

# Get warping path (alignment)
path = dtw.warping_path(series1, series2)
print(f"Warping path: {path}")

# Compute distance matrix for multiple series (fast C implementation)
series = np.array([
    [0, 1, 2, 3, 4],
    [0, 0, 1, 2, 3],
    [4, 3, 2, 1, 0],
    [0, 1, 1, 2, 2]
])

# All-pairs distance matrix (parallelized)
dist_matrix = distance_matrix_fast(series, use_c=True, parallel=True)
print(f"Distance matrix shape: {dist_matrix.shape}")
print(dist_matrix)

# Multidimensional time series (e.g., x, y, z accelerometer)
series_3d = np.array([
    [[0, 1], [1, 2], [2, 3]],  # Series 1: (x, y) coordinates
    [[0, 0], [1, 1], [2, 2]]   # Series 2: (x, y) coordinates
])
dist_3d = dtw_ndim.distance(series_3d[0], series_3d[1])
print(f"Multidimensional DTW distance: {dist_3d:.3f}")

# Use with scikit-learn KNN
from sklearn.neighbors import NearestNeighbors

# Pre-compute DTW distance matrix
X_train = series
dist_matrix_train = distance_matrix_fast(X_train, use_c=True)

# Use as precomputed metric in KNN
knn = NearestNeighbors(n_neighbors=2, metric='precomputed')
knn.fit(dist_matrix_train)

# Find nearest neighbors
query = np.array([[0, 1, 2, 2, 3]])
query_dists = np.array([dtw.distance(query[0], x) for x in X_train]).reshape(1, -1)
distances, indices = knn.kneighbors(query_dists)
print(f"Nearest neighbors: {indices}, distances: {distances}")
```

## Sources

- [dtaidistance GitHub Repository](https://github.com/wannesm/dtaidistance) - Accessed 2026-01-30
- [dtaidistance Documentation](https://dtaidistance.readthedocs.io/en/latest/) - Accessed 2026-01-30
- [Dynamic Time Warping Documentation](https://dtaidistance.readthedocs.io/en/latest/usage/dtw.html) - Accessed 2026-01-30
- [dtw Module API](https://dtaidistance.readthedocs.io/en/latest/modules/dtw.html) - Accessed 2026-01-30
- [dtaidistance PyPI](https://pypi.org/project/dtaidistance/) - Accessed 2026-01-30
- [Snyk dtw.distance Documentation](https://snyk.io/advisor/python/dtaidistance/functions/dtaidistance.dtw.distance) - Accessed 2026-01-30
- [Snyk dtw.warping_paths Documentation](https://snyk.io/advisor/python/dtaidistance/functions/dtaidistance.dtw.warping_paths) - Accessed 2026-01-30
