# sktime: Unified Framework for Time Series Machine Learning

## Overview

**sktime** is a unified framework for machine learning with time series in Python. While it's comprehensive across forecasting, classification, regression, clustering, and transformations, this profile focuses on its time series classification and clustering capabilities relevant to pattern search and similarity analysis.

**Current Version**: 0.20.0+ (actively developed)

**Primary Maintainer**: sktime community (originally from Alan Turing Institute)

**Repository**: https://github.com/sktime/sktime

## Core Features (Search/Classification Focus)

### Time Series Classification
- **Interval-based**: TimeSeriesForestClassifier, CanonicalIntervalForest
- **Dictionary-based**: BOSS (Bag of SFA Symbols), ContractableBOSS, WEASEL
- **Distance-based**: KNeighborsTimeSeriesClassifier (supports multiple metrics including DTW)
- **Shapelet-based**: ShapeletTransformClassifier
- **Deep learning**: CNN, ResNet, InceptionTime classifiers
- **Hybrid**: HIVE-COTE (Hierarchical Vote Collective of Transformation-based Ensembles)
- **Rocket**: ROCKET, MiniRocket, MultiRocket (random convolutional kernels)

### Time Series Clustering
- **Partition-based**: K-Means, K-Medoids with time series metrics
- **Hierarchical**: Agglomerative clustering with DTW, Euclidean, or custom distances
- **Kernel-based**: Kernel K-Means for time series
- **Distance metrics**: DTW, MSM (Move-Split-Merge), LCSS, ERP, TWE

### Distance Metrics
- **Elastic distances**: DTW (Dynamic Time Warping), WDTW (Weighted DTW)
- **Edit distances**: ERP (Edit Distance on Real Sequences), LCSS (Longest Common Subsequence)
- **Lockstep**: Euclidean, Manhattan
- **Shape-based**: Shape DTW
- **All metrics**: Accessible via `sktime.distances` module

### Transformations
- **Feature extraction**: Catch22, TSFresh integration
- **Shapelets**: ShapeletTransform for extracting discriminative subsequences
- **Rocket**: Random convolutional kernel transform
- **Dictionary methods**: SFA (Symbolic Fourier Approximation), SAX
- **Interval features**: Summary statistics over intervals

## Performance Characteristics

**Computational Complexity**:
- Varies by algorithm: O(n log n) for forest methods, O(n²m²) for DTW-based
- ROCKET variants are particularly fast: O(nm) where n=series count, m=length

**Scalability**:
- Handles 100s-1000s of time series efficiently
- Some algorithms (ROCKET, forests) scale better than distance-based methods
- No built-in GPU support (CPU-bound)

**Speed Benchmarks** (relative):
- ROCKET: Very fast (10-100x faster than DTW-based methods)
- Forest-based: Fast (good for large datasets)
- DTW-KNN: Moderate to slow (depends on dataset size)
- Shapelet Transform: Slow for large datasets

## Ecosystem Integration

**Dependencies**:
- Core: NumPy, Pandas, scikit-learn
- Optional: numba (acceleration), tslearn (DTW), catch22 (features), tsfresh (features)
- Deep learning: TensorFlow/Keras (for DL classifiers)

**Installation**:
```bash
pip install sktime
# With all optional dependencies:
pip install sktime[all_extras]
# Just deep learning:
pip install sktime[dl]
```

**Compatibility**:
- Python 3.10, 3.11, 3.12, 3.13 (64-bit only)
- macOS, Linux, Windows 8.1+
- Pandas DataFrame input supported
- Fully compatible with scikit-learn API (fit/predict/transform)

## Community and Maintenance

**GitHub Statistics** (as of 2026-01):
- Stars: ~7.5k
- Contributors: 350+
- Very active development
- Part of scikit-learn ecosystem

**Documentation Quality**:
- Comprehensive tutorials and examples
- API reference for all estimators
- User guide covering all modules
- Classification and clustering notebooks

**Maintenance Status**: ✅ Actively maintained
- Monthly releases
- Large contributor base
- Community-driven development
- Originally from Alan Turing Institute research

**Academic Foundation**:
- Published in JMLR 2019: "sktime: A Unified Interface for Machine Learning with Time Series"
- Implements state-of-the-art algorithms from literature

## Primary Use Cases

### Multi-Class Time Series Classification
- **Scenario**: Classify sensor readings into activity types (walking, running, sitting)
- **Approach**: ROCKET or HIVE-COTE for state-of-the-art accuracy
- **Benefit**: Scikit-learn API makes it easy to integrate into existing pipelines

### Customer Behavior Clustering
- **Scenario**: Group customers by purchase pattern similarity
- **Approach**: K-Means with DTW distance
- **Benefit**: Finds similar temporal patterns despite timing variations

### Shapelet-Based Feature Discovery
- **Scenario**: Find discriminative patterns in medical signals
- **Approach**: ShapeletTransform + standard classifier
- **Benefit**: Interpretable features for downstream analysis

### Benchmark Comparisons
- **Scenario**: Evaluate multiple classification algorithms
- **Approach**: Use sktime's unified API to test 20+ classifiers easily
- **Benefit**: Consistent interface simplifies experimentation

### Pipeline Construction
- **Scenario**: Build end-to-end time series ML workflow
- **Approach**: Combine transformers (e.g., Rocket) + classifiers + CV
- **Benefit**: Seamless integration with scikit-learn tools

## Strengths

1. **Unified API**: Scikit-learn-style interface for all time series tasks
2. **Comprehensive**: 40+ classifiers, 10+ distance metrics, many transformers
3. **State-of-the-art algorithms**: ROCKET, HIVE-COTE, BOSS, etc.
4. **Excellent documentation**: Tutorials, examples, API reference
5. **Active community**: Large contributor base, regular updates
6. **Pipeline support**: Works with scikit-learn pipelines, GridSearchCV
7. **Modular design**: Mix and match components easily
8. **Benchmarking-friendly**: Easy to compare multiple approaches

## Limitations

1. **No GPU acceleration**: CPU-only implementations
2. **Memory intensive**: Some classifiers (e.g., DTW-KNN) scale poorly with data size
3. **Slower than specialized libraries**: DTW slower than dtaidistance, matrix profile not as fast as STUMPY
4. **No streaming support**: Batch processing only
5. **Learning curve**: Many options can be overwhelming
6. **Dependency bloat**: Full installation is large (many optional deps)

## Comparison to Alternatives

**vs. tslearn**:
- sktime: Broader toolkit, more classifiers, better pipeline integration
- tslearn: More focused on DTW/shapelets, has clustering with DTW

**vs. STUMPY**:
- sktime: Supervised classification, many algorithms
- STUMPY: Unsupervised motif/discord discovery, matrix profiles

**vs. tsfresh**:
- sktime: Full ML workflow (features + models)
- tsfresh: Specialized for automatic feature extraction only

**vs. pyts**:
- sktime: More classifiers, better maintained, scikit-learn API
- pyts: Imaging techniques, simpler for beginners

## Decision Criteria

**Choose sktime when**:
- Need scikit-learn API compatibility
- Want to benchmark multiple classification algorithms
- Building ML pipelines with transformers + classifiers
- Require state-of-the-art accuracy (ROCKET, HIVE-COTE)
- Need both classification and clustering in one library
- Value comprehensive documentation and community support

**Avoid sktime when**:
- Only need ultra-fast DTW (use dtaidistance)
- Require unsupervised pattern discovery (use STUMPY)
- Need GPU acceleration for deep learning
- Working with streaming/real-time data
- Want simple, minimal dependencies

## Getting Started Example

```python
from sktime.datasets import load_arrow_head
from sktime.classification.interval_based import TimeSeriesForestClassifier
from sktime.classification.kernel_based import RocketClassifier
from sktime.classification.distance_based import KNeighborsTimeSeriesClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load dataset
X, y = load_arrow_head(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# ROCKET classifier (fast and accurate)
rocket = RocketClassifier(num_kernels=10000)
rocket.fit(X_train, y_train)
y_pred = rocket.predict(X_test)
print(f"ROCKET Accuracy: {accuracy_score(y_test, y_pred):.3f}")

# DTW-based KNN classifier
knn_dtw = KNeighborsTimeSeriesClassifier(distance="dtw", n_neighbors=5)
knn_dtw.fit(X_train, y_train)
y_pred_knn = knn_dtw.predict(X_test)
print(f"DTW-KNN Accuracy: {accuracy_score(y_test, y_pred_knn):.3f}")

# Time series clustering
from sktime.clustering.k_means import TimeSeriesKMeans
kmeans = TimeSeriesKMeans(n_clusters=3, metric="dtw", random_state=42)
labels = kmeans.fit_predict(X_train)
print(f"Cluster assignments: {labels[:10]}")

# Pipeline with shapelet transform
from sktime.transformations.panel.shapelet_transform import RandomShapeletTransform
from sklearn.linear_model import RidgeClassifierCV
from sklearn.pipeline import make_pipeline

shapelet_clf = make_pipeline(
    RandomShapeletTransform(n_shapelet_samples=100, max_shapelets=10),
    RidgeClassifierCV()
)
shapelet_clf.fit(X_train, y_train)
y_pred_shapelet = shapelet_clf.predict(X_test)
print(f"Shapelet Accuracy: {accuracy_score(y_test, y_pred_shapelet):.3f}")
```

## Sources

- [sktime GitHub Repository](https://github.com/sktime/sktime) - Accessed 2026-01-30
- [sktime Documentation](https://www.sktime.net/en/stable/) - Accessed 2026-01-30
- [Time Series Classification](https://www.sktime.net/en/stable/examples/02_classification.html) - Accessed 2026-01-30
- [Time Series Clustering API](https://www.sktime.net/en/stable/api_reference/clustering.html) - Accessed 2026-01-30
- [Classification API Reference](https://www.sktime.net/en/latest/api_reference/classification.html) - Accessed 2026-01-30
- [sktime PyPI](https://pypi.org/project/sktime/) - Accessed 2026-01-30
- [JMLR Paper: sktime (2019)](https://ar5iv.labs.arxiv.org/html/1909.07872) - arXiv:1909.07872, Accessed 2026-01-30
- [sktime LinkedIn](https://www.linkedin.com/company/scikit-time) - Accessed 2026-01-30
