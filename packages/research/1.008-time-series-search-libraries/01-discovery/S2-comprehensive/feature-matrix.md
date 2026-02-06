# S2: Feature-by-Feature Comparison Matrix

## Core Capabilities Comparison

### Distance Metrics & Similarity Measures

| Feature | tslearn | STUMPY | sktime | tsfresh | dtaidistance | pyts |
|---------|---------|--------|--------|---------|--------------|------|
| **Euclidean Distance** | ✅ Yes | ✅ Yes | ✅ Yes | N/A | ❌ No | ✅ Yes |
| **DTW (Basic)** | ✅ Excellent | ❌ No | ✅ Good | N/A | ✅ Excellent | ✅ Basic |
| **DTW with Constraints** | ✅ Sakoe-Chiba, Itakura | ❌ No | ✅ Sakoe-Chiba | N/A | ✅ All variants | ❌ No |
| **Soft-DTW (Differentiable)** | ✅ Yes | ❌ No | ❌ No | N/A | ❌ No | ❌ No |
| **Fast DTW (Approximation)** | ✅ Yes | ❌ No | ❌ No | N/A | ✅ Yes | ❌ No |
| **Matrix Profile** | ❌ No | ✅ Excellent | ❌ No | N/A | ❌ No | ❌ No |
| **Longest Common Subsequence** | ❌ No | ❌ No | ❌ No | N/A | ❌ No | ❌ No |

**Key Findings**:
- **dtaidistance**: Most comprehensive DTW implementation (all variants, constraints)
- **tslearn**: Unique soft-DTW for gradient-based optimization
- **STUMPY**: Only library with matrix profile (critical for motif/discord discovery)
- **sktime**: Good DTW support but fewer variants than specialists

---

## Pattern Discovery Methods

| Method | tslearn | STUMPY | sktime | tsfresh | dtaidistance | pyts |
|--------|---------|--------|--------|---------|--------------|------|
| **Motif Discovery** | ❌ No | ✅ Excellent | ❌ No | ❌ No | ❌ No | ❌ No |
| **Discord Detection** | ❌ No | ✅ Excellent | ❌ No | ❌ No | ❌ No | ❌ No |
| **Shapelet Discovery** | ✅ LearningShapelets | ❌ No | ✅ Multiple | ❌ No | ❌ No | ✅ Yes |
| **Regime Change Detection** | ❌ No | ✅ FLUSS | ❌ No | ❌ No | ❌ No | ❌ No |
| **Semantic Segmentation** | ❌ No | ✅ FLOSS | ❌ No | ❌ No | ❌ No | ❌ No |

**Key Findings**:
- **STUMPY**: Dominates unsupervised pattern discovery (motifs, discords, regime changes)
- **tslearn/sktime**: Shapelet discovery for supervised tasks
- **Gap**: No library does longest common subsequence (LCS) well

---

## Classification Algorithms

### DTW-Based Classifiers

| Classifier | tslearn | STUMPY | sktime | tsfresh | dtaidistance | pyts |
|------------|---------|--------|--------|---------|--------------|------|
| **KNN-DTW** | ✅ Yes | ❌ No | ✅ Yes | N/A | Distance only | ✅ Yes |
| **DTW Barycentric Averaging** | ✅ Yes | ❌ No | ❌ No | N/A | ❌ No | ❌ No |
| **Shapelet Transform** | ✅ Yes | ❌ No | ✅ Yes | N/A | ❌ No | ✅ Yes |
| **Learning Shapelets** | ✅ Yes | ❌ No | ❌ No | N/A | ❌ No | ❌ No |

### Modern Classifiers (Non-DTW)

| Classifier | tslearn | STUMPY | sktime | tsfresh | dtaidistance | pyts |
|------------|---------|--------|--------|---------|--------------|------|
| **ROCKET** | ❌ No | ❌ No | ✅ Yes | N/A | ❌ No | ❌ No |
| **Arsenal** | ❌ No | ❌ No | ✅ Yes | N/A | ❌ No | ❌ No |
| **HIVE-COTE** | ❌ No | ❌ No | ✅ Yes | N/A | ❌ No | ❌ No |
| **TSForest** | ❌ No | ❌ No | ✅ Yes | N/A | ❌ No | ❌ No |
| **InceptionTime** | ❌ No | ❌ No | ✅ Yes | N/A | ❌ No | ❌ No |

**Key Findings**:
- **sktime**: Widest classifier selection (40+ algorithms)
- **tslearn**: Best DTW-specific classifiers (soft-DTW, learning shapelets)
- **ROCKET (sktime)**: Best accuracy/speed trade-off (state-of-the-art)
- **tsfresh**: Generates features, not classifiers (pair with XGBoost/RF)

---

## Feature Extraction Capabilities

| Feature Type | tslearn | STUMPY | sktime | tsfresh | dtaidistance | pyts |
|--------------|---------|--------|--------|---------|--------------|------|
| **Statistical (794+ features)** | ❌ No | ❌ No | Via plugins | ✅ Excellent | ❌ No | ⚠️ Basic |
| **Shapelet Features** | ✅ Yes | ❌ No | ✅ Yes | ❌ No | ❌ No | ✅ Yes |
| **ROCKET Features** | ❌ No | ❌ No | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Imaging (GAF, MTF, RP)** | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No | ✅ Excellent |
| **Symbolic (SAX, VSM)** | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No | ✅ Yes |
| **Wavelet Transform** | ❌ No | ❌ No | ⚠️ Limited | ✅ Yes | ❌ No | ✅ Yes |

**Key Findings**:
- **tsfresh**: Most comprehensive statistical features (794 built-in + custom)
- **pyts**: Only library with imaging methods (GAF/MTF for CNNs)
- **sktime ROCKET**: Best learned features (10,000 random kernels)
- **Feature selection**: tsfresh has built-in selection, others require manual

---

## Clustering Capabilities

| Algorithm | tslearn | STUMPY | sktime | tsfresh | dtaidistance | pyts |
|-----------|---------|--------|--------|---------|--------------|------|
| **K-Means (Euclidean)** | ✅ Yes | ❌ No | ✅ Yes | N/A | ❌ No | ❌ No |
| **K-Means (DTW)** | ✅ Excellent | ❌ No | ✅ Good | N/A | Distance only | ❌ No |
| **K-Shapes** | ✅ Yes | ❌ No | ✅ Yes | N/A | ❌ No | ❌ No |
| **Hierarchical (DTW)** | ✅ Yes | ❌ No | ✅ Yes | N/A | Distance matrix | ❌ No |
| **DBSCAN (DTW)** | ❌ No | ❌ No | ✅ Yes | N/A | Distance matrix | ❌ No |

**Key Findings**:
- **tslearn**: Most mature clustering (K-Shapes algorithm unique)
- **sktime**: More clustering algorithms but tslearn has better DTW integration
- **dtaidistance**: Provides distance matrix, use with scipy.cluster
- **STUMPY**: No clustering (use for motif discovery, then cluster motifs)

---

## Scalability & Performance Features

### Parallelization Support

| Feature | tslearn | STUMPY | sktime | tsfresh | dtaidistance | pyts |
|---------|---------|--------|--------|---------|--------------|------|
| **Multi-core (CPU)** | ⚠️ Limited | ✅ Excellent (Numba) | ⚠️ Varies | ✅ Dask | ✅ OpenMP | ❌ No |
| **GPU Support** | ❌ No | ✅ CUDA (cupy) | ❌ No | ❌ No | ❌ No | ❌ No |
| **Distributed (Dask)** | ❌ No | ✅ Yes | ⚠️ Experimental | ✅ Yes | ❌ No | ❌ No |
| **Streaming/Online** | ❌ No | ✅ FLOSS | ❌ No | ❌ No | ❌ No | ❌ No |

### Performance Optimizations

| Optimization | tslearn | STUMPY | sktime | tsfresh | dtaidistance | pyts |
|--------------|---------|--------|--------|---------|--------------|------|
| **Cython Backend** | ✅ Yes | ❌ No | ⚠️ Some | ❌ No | ✅ Yes | ❌ No |
| **Numba JIT** | ❌ No | ✅ Excellent | ⚠️ Some | ❌ No | ❌ No | ⚠️ Some |
| **C/C++ Core** | ❌ No | ❌ No | ❌ No | ❌ No | ✅ Yes | ❌ No |
| **Approximate Methods** | ✅ FastDTW | ✅ SCRIMP++ | ❌ No | ❌ No | ✅ Yes | ❌ No |

**Key Findings**:
- **STUMPY**: Best scalability (CPU/GPU/Dask) for matrix profile
- **dtaidistance**: Fastest DTW (C implementation + OpenMP)
- **tsfresh**: Dask support critical for large-scale feature extraction
- **tslearn**: Good Cython performance but no GPU/distributed

---

## Production-Ready Features

| Feature | tslearn | STUMPY | sktime | tsfresh | dtaidistance | pyts |
|---------|---------|--------|--------|---------|--------------|------|
| **scikit-learn API** | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes |
| **Pipeline Support** | ✅ Yes | ❌ No | ✅ Excellent | ✅ Yes | ❌ No | ✅ Yes |
| **Model Persistence** | ✅ joblib | ❌ Manual | ✅ joblib | ✅ joblib | ❌ Manual | ✅ joblib |
| **Incremental Learning** | ❌ No | ✅ FLOSS | ❌ No | ❌ No | ❌ No | ❌ No |
| **Cross-Validation** | ✅ sklearn | ❌ Manual | ✅ sklearn + custom | ✅ sklearn | ❌ Manual | ✅ sklearn |

**Key Findings**:
- **sktime**: Best pipeline integration (TimeSeriesForestClassifier → GridSearchCV)
- **scikit-learn API**: Makes tslearn/tsfresh/pyts easy to integrate
- **STUMPY**: Not ML-focused (low-level pattern discovery functions)
- **dtaidistance**: Provides building blocks, not full ML workflow

---

## Advanced Features

### DTW Variants & Constraints

| Variant | tslearn | STUMPY | sktime | tsfresh | dtaidistance | pyts |
|---------|---------|--------|--------|---------|--------------|------|
| **Sakoe-Chiba Band** | ✅ Yes | ❌ No | ✅ Yes | N/A | ✅ Yes | ❌ No |
| **Itakura Parallelogram** | ✅ Yes | ❌ No | ❌ No | N/A | ✅ Yes | ❌ No |
| **Multi-dimensional DTW** | ✅ Yes | ✅ mSTUMP | ❌ No | N/A | ✅ Yes | ❌ No |
| **Derivative DTW** | ❌ No | ❌ No | ❌ No | N/A | ✅ Yes | ❌ No |
| **Weighted DTW** | ❌ No | ❌ No | ❌ No | N/A | ✅ Yes | ❌ No |

### Matrix Profile Variants

| Variant | tslearn | STUMPY | sktime | tsfresh | dtaidistance | pyts |
|---------|---------|--------|--------|---------|--------------|------|
| **Self-join (STUMP)** | N/A | ✅ Yes | N/A | N/A | N/A | N/A |
| **AB-join (MASS)** | N/A | ✅ Yes | N/A | N/A | N/A | N/A |
| **Multi-dimensional (mSTUMP)** | N/A | ✅ Yes | N/A | N/A | N/A | N/A |
| **Streaming (FLOSS)** | N/A | ✅ Yes | N/A | N/A | N/A | N/A |
| **Distributed (STUMPED)** | N/A | ✅ Yes | N/A | N/A | N/A | N/A |
| **GPU (GPU-STUMP)** | N/A | ✅ Yes | N/A | N/A | N/A | N/A |
| **Approximate (SCRIMP++)** | N/A | ✅ Yes | N/A | N/A | N/A | N/A |

**Key Findings**:
- **dtaidistance**: Most DTW variants (derivative, weighted, all constraints)
- **STUMPY**: Matrix profile monopoly (no other library implements it)
- **tslearn**: Soft-DTW unique (differentiable for neural network integration)

---

## Summary: Library Differentiation

### Unique Capabilities (No Alternative)

**STUMPY**:
- Matrix profile (motifs, discords, regime changes)
- FLOSS streaming for real-time pattern discovery
- GPU acceleration for matrix profile

**tslearn**:
- Soft-DTW (differentiable DTW for gradient-based optimization)
- Learning Shapelets (end-to-end shapelet learning)
- K-Shapes clustering

**sktime**:
- ROCKET/Arsenal (state-of-the-art classification)
- 40+ classifiers in unified API
- Best pipeline/GridSearchCV integration

**tsfresh**:
- 794 statistical features with automatic selection
- Hypothesis testing for feature relevance

**dtaidistance**:
- Fastest DTW implementation (C + OpenMP)
- All DTW variants (derivative, weighted, all constraints)

**pyts**:
- Imaging methods (GAF, MTF, RP) for CNNs
- Symbolic representations (SAX, VSM)

### Overlapping Capabilities (Multiple Libraries)

**DTW Classification**: tslearn (best), sktime (good), pyts (basic)
**Shapelet Discovery**: sktime (multiple methods), tslearn (learning), pyts (basic)
**K-Means Clustering**: tslearn (best DTW integration), sktime (more algorithms)

### Capability Gaps (No Good Solution)

- **Longest Common Subsequence** (LCS) matching
- **Real-time classification** (only STUMPY has streaming, but no classifiers)
- **Causal pattern discovery** (find X → Y temporal patterns)
- **Multivariate motif discovery** with constraints (mSTUMP exists but limited)

## Recommendation Matrix by Need

| Need | Primary Choice | Alternative | Why |
|------|---------------|-------------|-----|
| **Fastest DTW distances** | dtaidistance | tslearn | 30-300x speedup over Python |
| **DTW classification** | tslearn | sktime | Soft-DTW, learning shapelets |
| **Modern classification** | sktime | - | ROCKET is state-of-the-art |
| **Unsupervised anomaly detection** | STUMPY | - | Matrix profile has no alternative |
| **Feature extraction** | tsfresh | sktime ROCKET | 794 features vs. 10K kernels |
| **Clustering** | tslearn | sktime | K-Shapes is unique |
| **Real-time streaming** | STUMPY | - | FLOSS has no alternative |
| **GPU acceleration** | STUMPY | - | Only library with CUDA support |
| **Production ML pipelines** | sktime | tsfresh | Best sklearn integration |
| **Imaging for CNNs** | pyts | - | GAF/MTF unique to pyts |
