# tslearn: Machine Learning Toolkit for Time Series

## Overview

**tslearn** is a comprehensive machine learning toolkit specifically designed for time series analysis in Python. It provides implementations of Dynamic Time Warping (DTW), shapelet discovery, time series clustering, and classification algorithms. The library is built to work seamlessly with the scikit-learn ecosystem.

**Current Version**: 0.8.0.dev0 (latest development), 0.7.0 (stable)

**Primary Maintainer**: Romain Tavenard and the tslearn team

**Repository**: https://github.com/tslearn-team/tslearn

## Core Features

### Dynamic Time Warping (DTW)
- **Standard DTW**: Classic DTW implementation for time series similarity
- **DTW Barycenter Averaging**: Compute average of multiple time series
- **DTW Variants**: Includes soft-DTW, DTW with global constraints (Sakoe-Chiba band, Itakura parallelogram)
- **DTW-based clustering**: K-means clustering using DTW as the distance metric
- **Fast implementation**: Optimized C/Cython backend for performance

### Shapelet Discovery
- **Learning Shapelets**: Implementation of "Learning Time-series Shapelets" algorithm
- **Shapelet-based classification**: Use discriminative subsequences for classification
- **Configurable parameters**: `n_shapelets_per_size` dictionary controls shapelet lengths and counts
- **Visualization support**: Tools for aligning and visualizing discovered shapelets with time series

### Time Series Classification
- **K-Nearest Neighbors with DTW**: KNN classifier using DTW distance
- **Shapelet-based classifiers**: Classification using learned shapelets
- **Support Vector Classifiers**: Time series SVC with various kernels
- **Integration**: Works with scikit-learn pipelines and cross-validation

### Clustering
- **TimeSeriesKMeans**: K-means with DTW, soft-DTW, or Euclidean distance
- **Kernel K-Means**: Clustering using kernel methods
- **Silhouette analysis**: Quality metrics for clustering

### Transformations
- **Piecewise Aggregate Approximation (PAA)**: Dimensionality reduction
- **Symbolic Aggregate approXimation (SAX)**: Time series to symbolic representation
- **1d-SAX**: One-dimensional SAX variant

## Performance Characteristics

**Computational Complexity**:
- DTW: O(n*m) where n, m are time series lengths (can be reduced with constraints)
- Shapelet learning: Varies by dataset size and shapelet configuration
- Clustering: Iterative, depends on number of series, length, and convergence

**Scalability**:
- Handles datasets with thousands of time series
- C/Cython backend provides significant speedup
- Memory usage scales with dataset size and algorithm choice

**Speed Notes**:
- Pure Python implementations available for transparency
- Optimized implementations for production use
- GPU acceleration not natively supported (CPU-bound)

## Ecosystem Integration

**Dependencies**:
- Core: NumPy, SciPy, scikit-learn, numba
- Shapelet learning: Keras 3+ (requires dedicated backend: TensorFlow, PyTorch, or JAX)
- Optional: joblib (parallelization), h5py (model persistence)

**Installation**:
```bash
pip install tslearn
# For shapelet features:
pip install tslearn[all_features]
```

**Compatibility**:
- Python 3.7+
- Works with pandas DataFrames (via conversion)
- Integrates with scikit-learn pipelines
- Supports joblib for parallel processing

## Community and Maintenance

**GitHub Statistics** (as of 2026-01):
- Stars: ~2.8k
- Contributors: 40+
- Latest commit: January 2026 (active development)
- Issues: ~50 open, ~400 closed

**Documentation Quality**:
- Comprehensive user guide with tutorials
- API reference documentation
- Gallery of examples covering all major features
- Academic paper citations for algorithms

**Maintenance Status**: ✅ Actively maintained
- Regular releases and updates
- Responsive to issues and pull requests
- Active development branch (0.8.0.dev0)

## Primary Use Cases

### Time Series Classification
- **Scenario**: Classify physiological signals (ECG, EEG)
- **Approach**: Use shapelet-based classifiers or KNN with DTW
- **Benefit**: Captures temporal patterns that traditional ML misses

### Pattern Similarity Search
- **Scenario**: Find similar motion patterns in sensor data
- **Approach**: DTW distance calculation between query and database
- **Benefit**: Handles temporal shifts and speed variations

### Time Series Clustering
- **Scenario**: Group customers by purchasing behavior over time
- **Approach**: K-means with DTW distance
- **Benefit**: Identifies similar behavioral patterns despite timing differences

### Anomaly Detection via Shapelets
- **Scenario**: Detect unusual patterns in manufacturing sensor data
- **Approach**: Learn normal shapelets, flag series without them
- **Benefit**: Discovers discriminative subsequences automatically

### Medical Signal Analysis
- **Scenario**: Classify heart arrhythmias from ECG recordings
- **Approach**: Shapelet-based classification with learned features
- **Benefit**: Interpretable features (specific waveform shapes)

## Strengths

1. **Comprehensive toolkit**: DTW + shapelets + clustering + classification in one package
2. **Scikit-learn compatibility**: Familiar API, works with existing pipelines
3. **Strong academic foundation**: Implements peer-reviewed algorithms
4. **Good documentation**: Tutorials, examples, user guide
5. **Active maintenance**: Regular updates and bug fixes
6. **Flexible DTW**: Multiple variants and constraints
7. **Interpretable features**: Shapelets provide explainability

## Limitations

1. **Shapelet dependency**: Requires Keras 3+ backend (TensorFlow/PyTorch/JAX)
2. **No GPU acceleration**: Primarily CPU-bound computations
3. **Learning curve**: Requires understanding of time series concepts
4. **Memory intensive**: Large datasets can be memory-hungry
5. **Slower than specialized libraries**: DTW is faster in dtaidistance, matrix profiles faster in STUMPY
6. **Limited real-time support**: Not optimized for streaming data

## Comparison to Alternatives

**vs. stumpy (Matrix Profile)**:
- tslearn: Better for classification tasks, shapelet discovery
- stumpy: Better for motif discovery, anomaly detection, pattern matching

**vs. sktime**:
- tslearn: More focused on DTW and distance-based methods
- sktime: Broader toolkit, more forecasting-oriented, more classifiers

**vs. dtaidistance**:
- tslearn: Full ML toolkit (classification, clustering)
- dtaidistance: Specialized for fast DTW distance calculations

**vs. tsfresh**:
- tslearn: Distance-based features (DTW, shapelets)
- tsfresh: Statistical features (800+ automatic extractions)

## Decision Criteria

**Choose tslearn when**:
- Need DTW-based clustering or classification
- Want to discover discriminative shapelets
- Require scikit-learn integration
- Need interpretable time series features
- Working with moderate-sized datasets (<10k series)

**Avoid tslearn when**:
- Only need ultra-fast DTW distances (use dtaidistance)
- Primarily forecasting (use statsmodels, Prophet, or sktime)
- Need GPU acceleration for large-scale processing
- Require real-time/streaming analysis
- Prefer statistical features over distance-based (use tsfresh)

## Getting Started Example

```python
from tslearn.clustering import TimeSeriesKMeans
from tslearn.datasets import CachedDatasets
import numpy as np

# Load sample dataset
X_train, y_train, X_test, y_test = CachedDatasets().load_dataset("Trace")

# Cluster time series using DTW
km = TimeSeriesKMeans(n_clusters=4, metric="dtw", random_state=0)
labels = km.fit_predict(X_train)

# Shapelet-based classification
from tslearn.shapelets import LearningShapelets
from tslearn.preprocessing import TimeSeriesScalerMeanVariance

# Normalize data
scaler = TimeSeriesScalerMeanVariance()
X_train_scaled = scaler.fit_transform(X_train)

# Learn shapelets
shp_clf = LearningShapelets(
    n_shapelets_per_size={10: 5, 20: 5},  # 5 shapelets each of length 10 and 20
    max_iter=100,
    verbose=1
)
shp_clf.fit(X_train_scaled, y_train)
predictions = shp_clf.predict(X_test)
```

## Sources

- [tslearn GitHub Repository](https://github.com/tslearn-team/tslearn) - Accessed 2026-01-30
- [tslearn Documentation v0.8.0.dev0](https://tslearn.readthedocs.io/en/latest/) - Latest development version, Accessed 2026-01-30
- [tslearn Documentation v0.7.0](https://tslearn.readthedocs.io/en/stable/) - Stable release, Accessed 2026-01-30
- [DTW User Guide](https://github.com/tslearn-team/tslearn/blob/main/docs/user_guide/dtw.rst) - Accessed 2026-01-30
- [Shapelets User Guide](https://tslearn.readthedocs.io/en/latest/user_guide/shapelets.html) - Accessed 2026-01-30
- [Example Gallery](https://tslearn.readthedocs.io/en/stable/auto_examples/index.html) - Accessed 2026-01-30
- [Shapelet Alignment Example](https://tslearn.readthedocs.io/en/stable/auto_examples/classification/plot_shapelet_locations.html) - Accessed 2026-01-30
