# pyts: Time Series Classification via Imaging and Transformations

## Overview

**pyts** is a Python package specifically designed for time series classification that focuses on transformation-based approaches. Its unique strength is converting time series into images (Recurrence Plots, Gramian Angular Fields, Markov Transition Fields) and using image-based or symbolic representations for classification. It provides state-of-the-art transformation algorithms in an accessible, scikit-learn-compatible API.

**Current Version**: 0.13.0

**Primary Maintainer**: Johann Faouzi (with Hicham Janati)

**Repository**: https://github.com/johannfaouzi/pyts

## Core Features

### Imaging Time Series
- **Recurrence Plot (RP)**: Visualizes recurrences in time series as binary matrices
- **Gramian Angular Field (GAF)**:
  - **GASF** (Summation): Cosine of sum of angles (temporal correlations)
  - **GADF** (Difference): Sine of difference of angles
- **Markov Transition Field (MTF)**: Encodes transition probabilities as images
- **Process**: Rescale series → polar coordinates → compute angular transformations

### Transformation Algorithms
- **Bag of Patterns (BOP)**: Discretize, create SAX words, count patterns
- **BOSS (Bag of SFA Symbols)**: Symbolic Fourier Approximation with bag-of-words
- **WEASEL**: Word ExtrAction for time SEries cLassification
- **Shapelet Transform**: Extract discriminative subsequences
- **ROCKET**: Random Convolutional Kernel Transform (fast, accurate)

### Classification Algorithms
- **KNeighborsClassifier**: KNN with various time series distances (DTW, BOSS, etc.)
- **SAXVSM**: SAX + Vector Space Model classifier
- **BOSSVS**: BOSS + Vector Space Model
- **TimeSeriesForest**: Ensemble of decision trees on time series intervals
- **LearningShapelets**: Learn discriminative shapelets

### Feature Extraction
- **Symbolic representations**: SAX (Symbolic Aggregate approXimation), 1d-SAX
- **Dimensionality reduction**: PAA (Piecewise Aggregate Approximation), DFT (Discrete Fourier Transform)
- **Bag-of-words features**: Extract counts of symbolic patterns

## Performance Characteristics

**Computational Complexity**:
- Imaging (GAF, MTF, RP): O(n²) where n is series length
- BOSS/WEASEL: O(nm) where m is alphabet size
- ROCKET: O(nk) where k is number of kernels (very fast)

**Scalability**:
- Handles 100s-1000s of time series efficiently
- Imaging methods can be memory-intensive for long series (O(n²) image size)
- ROCKET is particularly scalable (linear complexity)

**Speed**:
- **ROCKET**: Very fast (~seconds for 1000 series)
- **Imaging methods**: Moderate (minutes for 1000 series)
- **BOSS/WEASEL**: Moderate to fast
- **DTW-based**: Slower for large datasets

## Ecosystem Integration

**Dependencies**:
- Core: NumPy, SciPy, scikit-learn, joblib, numba
- Optional: matplotlib (visualization)

**Installation**:
```bash
pip install pyts
```

**Compatibility**:
- Python 3.6+
- Scikit-learn API (fit/predict/transform)
- Works with NumPy arrays
- Integrates with sklearn pipelines

## Community and Maintenance

**GitHub Statistics** (as of 2026-01):
- Stars: ~1.7k
- Contributors: 10+
- Academic project (PhD research output)

**Documentation Quality**:
- Comprehensive user guide
- Gallery of examples for all modules
- API reference
- Published in JMLR (2020)

**Maintenance Status**: ⚠️ Moderately maintained
- Less frequent updates than tslearn/sktime
- Community contributions active
- Stable codebase (v0.13.0)

**Academic Foundation**:
- **Publication**: "pyts: A Python Package for Time Series Classification" (JMLR 2020)
- Implements algorithms from peer-reviewed research
- Based on PhD work by Johann Faouzi

## Primary Use Cases

### Image-Based Deep Learning Classification
- **Scenario**: Use CNNs for time series classification
- **Approach**: Convert series to GAF images → train CNN (ResNet, VGG)
- **Benefit**: Leverage pre-trained image models for time series

### Symbolic Pattern Recognition
- **Scenario**: Classify physiological signals with recurring symbolic patterns
- **Approach**: BOSS or WEASEL transformation + classifier
- **Benefit**: Captures symbolic structure, robust to noise

### Recurrence Analysis
- **Scenario**: Identify periodic or chaotic behavior in time series
- **Approach**: Compute Recurrence Plot, analyze visual patterns
- **Benefit**: Interpretable visualization of temporal structure

### Fast Transformation-Based Classification
- **Scenario**: Classify large dataset with limited compute
- **Approach**: ROCKET transformation + Ridge classifier
- **Benefit**: State-of-the-art accuracy with low computational cost

### Bag-of-Patterns Classification
- **Scenario**: Text-like classification (count pattern occurrences)
- **Approach**: Bag of Patterns or BOSS → Count Vectorizer → Naive Bayes
- **Benefit**: Simple, interpretable, effective for many domains

## Strengths

1. **Unique imaging methods**: Only library with comprehensive imaging algorithms (GAF, MTF, RP)
2. **Transformation focus**: Rich set of transformation algorithms
3. **Scikit-learn API**: Familiar, easy to use
4. **Academic rigor**: Peer-reviewed algorithms, JMLR publication
5. **Interpretability**: Image representations are visually interpretable
6. **Lightweight**: Minimal dependencies, easy to install
7. **ROCKET support**: Includes state-of-the-art ROCKET algorithm

## Limitations

1. **Classification only**: No forecasting, clustering, or regression
2. **Less comprehensive**: Fewer classifiers than sktime
3. **Maintenance pace**: Slower updates compared to sktime/tslearn
4. **Memory for imaging**: O(n²) images can be large for long series
5. **No GPU support**: CPU-only implementations
6. **Smaller community**: Less active than sktime/tslearn
7. **Limited documentation examples**: Fewer real-world case studies

## Comparison to Alternatives

**vs. sktime**:
- pyts: Specialized in imaging and transformations, simpler API
- sktime: More comprehensive (40+ classifiers), better maintained

**vs. tslearn**:
- pyts: Imaging methods (GAF, MTF), symbolic representations
- tslearn: DTW, shapelets, clustering focus

**vs. tsfresh**:
- pyts: Transformation-based features (imaging, symbolic)
- tsfresh: Statistical features (800+ automatic extractions)

**vs. STUMPY**:
- pyts: Supervised classification with transformations
- STUMPY: Unsupervised motif/discord discovery

## Decision Criteria

**Choose pyts when**:
- Need to convert time series to images for deep learning (CNNs)
- Want symbolic representations (SAX, BOSS, WEASEL)
- Require interpretable image-based features
- Need ROCKET for fast, accurate classification
- Prefer simple, focused library over comprehensive toolkit
- Value JMLR-published, academically rigorous implementations

**Avoid pyts when**:
- Need forecasting or regression (not supported)
- Require comprehensive classifier collection (use sktime)
- Want active development and frequent updates
- Need clustering or unsupervised methods (use tslearn or STUMPY)
- Working with very long time series (imaging is O(n²) memory)
- Prefer DTW-based methods (use tslearn or dtaidistance)

## Getting Started Example

```python
import numpy as np
from pyts.image import GramianAngularField, RecurrencePlot, MarkovTransitionField
from pyts.classification import BOSSVS, KNeighborsClassifier
from pyts.transformation import ROCKET
from sklearn.ensemble import RidgeClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Generate sample data
np.random.seed(42)
X = np.random.randn(100, 50)  # 100 time series, length 50
y = np.random.choice([0, 1, 2], size=100)  # 3 classes
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 1. Gramian Angular Field imaging
gasf = GramianAngularField(image_size=24, method='summation')
X_gasf = gasf.fit_transform(X_train)
print(f"GASF images shape: {X_gasf.shape}")  # (n_samples, 24, 24)

# Visualize first time series as GASF image
import matplotlib.pyplot as plt
plt.imshow(X_gasf[0], cmap='rainbow', origin='lower')
plt.title('Gramian Angular Summation Field')
plt.colorbar()
# plt.show()

# 2. BOSS Classification
boss = BOSSVS(word_size=4, n_bins=4, window_size=10, drop_sum=True)
boss.fit(X_train, y_train)
y_pred_boss = boss.predict(X_test)
print(f"BOSS Accuracy: {accuracy_score(y_test, y_pred_boss):.3f}")

# 3. ROCKET transformation + Ridge classifier
rocket = ROCKET(n_kernels=10000, random_state=42)
X_rocket_train = rocket.fit_transform(X_train)
X_rocket_test = rocket.transform(X_test)

clf = RidgeClassifierCV(alphas=np.logspace(-3, 3, 10))
clf.fit(X_rocket_train, y_train)
y_pred_rocket = clf.predict(X_rocket_test)
print(f"ROCKET Accuracy: {accuracy_score(y_test, y_pred_rocket):.3f}")

# 4. Recurrence Plot
rp = RecurrencePlot(threshold='point', percentage=20)
X_rp = rp.fit_transform(X_train)
print(f"Recurrence Plot shape: {X_rp.shape}")

# 5. Symbolic representation (SAX)
from pyts.approximation import SymbolicAggregateApproximation
sax = SymbolicAggregateApproximation(n_bins=4, strategy='uniform')
X_sax = sax.fit_transform(X_train)
print(f"SAX representation (first series): {X_sax[0]}")

# 6. KNN with DTW
knn_dtw = KNeighborsClassifier(n_neighbors=5, metric='dtw')
knn_dtw.fit(X_train, y_train)
y_pred_knn = knn_dtw.predict(X_test)
print(f"KNN-DTW Accuracy: {accuracy_score(y_test, y_pred_knn):.3f}")
```

## Sources

- [pyts GitHub Repository](https://github.com/johannfaouzi/pyts) - Accessed 2026-01-30
- [pyts Documentation](https://pyts.readthedocs.io/en/stable/) - Accessed 2026-01-30
- [Introduction Documentation](https://pyts.readthedocs.io/en/stable/introduction.html) - Accessed 2026-01-30
- [Imaging Time Series Module](https://pyts.readthedocs.io/en/stable/modules/image.html) - Accessed 2026-01-30
- [Transformation Module](https://pyts.readthedocs.io/en/latest/modules/transformation.html) - Accessed 2026-01-30
- [pyts PyPI](https://pypi.org/project/pyts/) - Accessed 2026-01-30
- [JMLR Paper (2020)](https://www.jmlr.org/papers/volume21/19-763/19-763.pdf) - "pyts: A Python Package for Time Series Classification", Accessed 2026-01-30
- [ResearchGate Publication](https://www.researchgate.net/publication/342582089_pyts_A_Python_Package_for_Time_Series_Classification) - Accessed 2026-01-30
- [ACM Digital Library](https://dl.acm.org/doi/10.5555/3455716.3455762) - JMLR Volume 21, Accessed 2026-01-30
