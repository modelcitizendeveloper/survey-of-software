# S1 Rapid Discovery: Recommendations and Synthesis

## Quick Reference Comparison

| Library | Primary Focus | Best For | Speed | Complexity | Maintenance |
|---------|--------------|----------|-------|------------|-------------|
| **tslearn** | DTW + Shapelets + ML | DTW clustering, shapelet classification | Moderate | Medium | ✅ Active |
| **STUMPY** | Matrix Profile | Motif/discord discovery, anomaly detection | Very Fast | Low | ✅ Active |
| **sktime** | Unified ML Framework | Classification benchmarking, pipelines | Varies | Medium-High | ✅ Very Active |
| **tsfresh** | Feature Extraction | Automatic feature engineering | Slow | Low | ✅ Active |
| **dtaidistance** | Fast DTW | DTW distance matrices, speed-critical apps | Extremely Fast | Low | ✅ Active |
| **pyts** | Imaging + Transformations | Image-based classification, symbolic methods | Moderate | Low-Medium | ⚠️ Moderate |

## Capability Matrix

| Capability | tslearn | STUMPY | sktime | tsfresh | dtaidistance | pyts |
|------------|---------|--------|--------|---------|--------------|------|
| **DTW Distance** | ✅ Good | ❌ No | ✅ Good | ❌ No | ✅ Excellent | ✅ Basic |
| **Shapelet Discovery** | ✅ Yes | ❌ No | ✅ Yes | ❌ No | ❌ No | ✅ Yes |
| **Matrix Profile** | ❌ No | ✅ Excellent | ❌ No | ❌ No | ❌ No | ❌ No |
| **Classification** | ✅ Good | ❌ No | ✅ Excellent | ⚠️ Features only | ❌ No | ✅ Good |
| **Clustering** | ✅ Yes | ❌ No | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Feature Extraction** | ⚠️ Basic | ❌ No | ⚠️ Via plugins | ✅ Excellent | ❌ No | ✅ Good |
| **Imaging Methods** | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No | ✅ Yes |
| **GPU Support** | ❌ No | ✅ Yes (CUDA) | ❌ No | ❌ No | ❌ No | ❌ No |
| **Streaming/Real-time** | ❌ No | ✅ Yes (FLOSS) | ❌ No | ❌ No | ❌ No | ❌ No |
| **Scikit-learn API** | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes |

## Decision Tree

```
Need time series search/similarity?
│
├─ Supervised classification task?
│  ├─ Yes → Need many classifiers for benchmarking?
│  │  ├─ Yes → **sktime** (40+ classifiers, unified API)
│  │  └─ No → Need specific method?
│  │     ├─ DTW-based → **tslearn** (DTW + shapelets + clustering)
│  │     ├─ Image-based (CNN) → **pyts** (GAF, MTF, RP imaging)
│  │     ├─ Feature-based (Random Forest, XGBoost) → **tsfresh** (794+ features)
│  │     └─ Fast and accurate → **sktime** with ROCKET
│  │
│  └─ No (unsupervised pattern discovery)
│     ├─ Find recurring patterns (motifs)? → **STUMPY** (matrix profile)
│     ├─ Find anomalies (discords)? → **STUMPY** (matrix profile)
│     ├─ Cluster by similarity?
│     │  ├─ With DTW distance → **tslearn** (TimeSeriesKMeans)
│     │  └─ Multiple distance options → **sktime** (clustering module)
│     └─ Detect regime changes? → **STUMPY** (FLUSS segmentation)
│
├─ Only need DTW distances (no ML)?
│  ├─ Performance critical (speed matters)? → **dtaidistance** (30-300x faster)
│  ├─ Part of larger ML toolkit → **tslearn** (DTW + more)
│  └─ Simple integration → **dtaidistance** (minimal dependencies)
│
└─ Extract features for any classifier?
   ├─ Statistical features (800+) → **tsfresh** (automatic extraction)
   ├─ Shapelet features → **tslearn** (LearningShapelets)
   ├─ ROCKET features (fast) → **sktime** (ROCKET transform)
   └─ Image features (for CNN) → **pyts** (GAF, MTF imaging)
```

## Use Case Recommendations

### Medical Signal Classification (ECG, EEG)
**Recommended**: **tslearn** (shapelets) or **sktime** (ROCKET)
- **Rationale**: Shapelets provide interpretable features, ROCKET provides accuracy
- **Alternative**: tsfresh for statistical feature extraction

### IoT Anomaly Detection
**Recommended**: **STUMPY** (matrix profile for discords)
- **Rationale**: Unsupervised, no training needed, scales well
- **Alternative**: tsfresh + Isolation Forest for feature-based anomaly detection

### Customer Behavior Clustering
**Recommended**: **tslearn** (TimeSeriesKMeans with DTW)
- **Rationale**: DTW handles timing variations in behavior patterns
- **Alternative**: sktime for more clustering algorithm options

### Activity Recognition (Accelerometer Data)
**Recommended**: **sktime** (ROCKET + Ridge Classifier)
- **Rationale**: Fast, state-of-the-art accuracy for multivariate time series
- **Alternative**: tsfresh for feature extraction + Random Forest

### Financial Pattern Matching
**Recommended**: **STUMPY** (motif discovery, AB-joins)
- **Rationale**: Find recurring price patterns, regime changes
- **Alternative**: dtaidistance for fast similarity search across historical data

### Predictive Maintenance
**Recommended**: **tsfresh** (feature extraction) + **XGBoost**
- **Rationale**: 794 features capture degradation signals, XGBoost handles importance
- **Alternative**: STUMPY for unsupervised anomaly detection

## Performance Comparison

### Speed (Relative to Pure Python)
1. **dtaidistance**: 30-300x faster (C implementation, specialized for DTW)
2. **STUMPY**: 10-100x faster (Numba JIT, GPU option)
3. **sktime ROCKET**: 10-100x faster than DTW-based methods
4. **tslearn**: 5-20x faster (Cython backend for core algorithms)
5. **pyts**: Similar to pure Python (some Numba acceleration)
6. **tsfresh**: Slow for extraction (parallelizable), but one-time cost

### Memory Usage (for 1000 series, length 1000)
- **dtaidistance**: ~100MB (distance matrix only)
- **STUMPY**: ~50MB (matrix profile is compact)
- **tslearn**: ~200MB (depends on algorithm)
- **sktime**: ~100-500MB (varies by classifier)
- **tsfresh**: ~500MB-2GB (794 features per series)
- **pyts**: ~500MB-1GB (imaging methods are O(n²))

### Scalability (Max Dataset Size)
- **STUMPY**: Millions-billions with Dask/GPU
- **dtaidistance**: 10,000s with parallelization
- **sktime**: 1,000s-10,000s (depends on classifier)
- **tslearn**: 1,000s-10,000s (DTW is O(n²m²))
- **tsfresh**: 10,000s-100,000s with Dask
- **pyts**: 1,000s (imaging memory limits)

## Library Pairing Strategies

### Combine for Enhanced Capabilities

**DTW Clustering + Feature Extraction**:
```python
# Use dtaidistance for fast DTW distance matrix
from dtaidistance import dtw
dist_matrix = dtw.distance_matrix_fast(X, use_c=True, parallel=True)

# Use scipy for clustering
from scipy.cluster.hierarchy import linkage, fcluster
Z = linkage(dist_matrix, method='average')
clusters = fcluster(Z, t=3, criterion='maxclust')
```

**Motif Discovery + Classification**:
```python
# Step 1: Use STUMPY to find motifs
import stumpy
mp = stumpy.stump(data, m=100)
motifs = stumpy.motifs(data, mp[:, 0], max_motifs=5)

# Step 2: Extract motif occurrences as features
# Step 3: Use sktime or tslearn for classification with motif features
```

**Feature Extraction + Ensemble**:
```python
# Extract tsfresh features
from tsfresh import extract_features
features = extract_features(df, column_id='id', column_sort='time')

# Extract ROCKET features (via sktime)
from sktime.transformations.panel.rocket import Rocket
rocket = Rocket()
rocket_features = rocket.fit_transform(X)

# Concatenate and train ensemble
combined_features = np.hstack([features, rocket_features])
# ... train classifier ...
```

## Common Pitfalls and Solutions

### Pitfall 1: Using Wrong Library for Task
**Problem**: Using tsfresh for similarity search, or STUMPY for classification
**Solution**: Match library to task (see decision tree above)

### Pitfall 2: DTW on Large Datasets Without Constraints
**Problem**: O(n²m²) complexity causes hour-long waits
**Solution**:
- Use Sakoe-Chiba band (window constraint) with dtaidistance
- Consider STUMPY (matrix profile) for all-pairs similarity instead
- Use ROCKET for classification (avoids DTW entirely)

### Pitfall 3: Not Normalizing Time Series
**Problem**: Distance metrics fail with different scales
**Solution**: Z-normalize before DTW/matrix profile (most libraries have built-in)

### Pitfall 4: Overfitting with tsfresh Features
**Problem**: 794 features on small dataset causes overfitting
**Solution**: Use tsfresh's built-in feature selection (hypothesis tests)

### Pitfall 5: Choosing Wrong Window Size (STUMPY, Shapelets)
**Problem**: Too small misses patterns, too large loses resolution
**Solution**:
- Domain knowledge (e.g., heartbeat duration for ECG)
- Pan-matrix profile (STUMPY) to explore multiple scales
- Cross-validation over window sizes

## Next Steps: S2 Comprehensive Discovery

Based on S1 findings, S2 should focus on:

1. **Feature-by-feature comparison**: Detailed comparison tables for DTW variants, shapelet methods, matrix profile algorithms

2. **Performance benchmarking**: Quantitative speed/accuracy benchmarks on standardized datasets (UCR Time Series Archive)

3. **Integration complexity**: Effort required to integrate each library (dependencies, API learning curve, debugging)

4. **Production readiness**: Deployment considerations (Docker, cloud, versioning, breaking changes)

5. **Deep dives**:
   - tslearn: DTW variants (soft-DTW, global constraints) and shapelet parameter tuning
   - STUMPY: Matrix profile variants (STUMPED, GPU-STUMP, FLOSS) and scalability limits
   - sktime: Comprehensive classifier benchmarking on UCR datasets
   - tsfresh: Feature selection strategies and computational optimization
   - dtaidistance: Performance optimization techniques and parallelization

6. **Hybrid approaches**: Combining libraries for enhanced capabilities (see pairing strategies above)

## Summary

**For most users starting with time series search/classification**:
1. **Start with sktime** if you want a comprehensive toolkit and don't mind some complexity
2. **Use tslearn** if DTW and shapelets are your primary interest
3. **Use STUMPY** if you need unsupervised pattern discovery
4. **Use dtaidistance** if you only need fast DTW distances
5. **Use tsfresh** if you have standard ML classifiers and need automatic features
6. **Use pyts** if you want to experiment with imaging methods or have CNNs

**The "best" library depends entirely on your use case** - there's significant differentiation in the ecosystem, and choosing the right tool for the job is critical for success.
