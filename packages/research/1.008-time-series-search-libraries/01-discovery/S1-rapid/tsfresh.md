# tsfresh: Automatic Time Series Feature Extraction

## Overview

**tsfresh** (Time Series Feature extraction based on scalable hypothesis tests) is a Python package that automatically extracts hundreds of features from time series data and performs statistical feature selection. While not a search/similarity library like DTW tools, it's essential for time series classification as it generates features that can be used with standard ML classifiers.

**Current Version**: 0.21.1 (actively developed)

**Primary Maintainer**: Blue Yonder (now part of JDA Software)

**Repository**: https://github.com/blue-yonder/tsfresh

## Core Features

### Automatic Feature Extraction
- **794+ features**: Automatically extracts 794 time series features by default (expandable to 1200+)
- **63 characterization methods**: Statistical, signal processing, and nonlinear dynamics features
- **Feature categories**:
  - Statistical: mean, median, variance, skewness, kurtosis, quantiles
  - Spectral: FFT coefficients, autocorrelation, partial autocorrelation
  - Complexity: approximate entropy, sample entropy, Lempel-Ziv complexity
  - Patterns: Friedrich coefficients, AR model parameters
  - Time-domain: number of peaks, last location of maximum, time reversal asymmetry

### Feature Selection
- **Hypothesis testing**: Automatically tests each feature's relevance to the target variable
- **FDR control**: False Discovery Rate adjustment (Benjamini-Yekutieli procedure)
- **Configurable p-values**: Filter features by statistical significance
- **Scalable**: Uses parallelization for large datasets

### Integration Features
- **Pandas DataFrame support**: Seamless integration with pandas
- **scikit-learn compatible**: Extracted features work with any sklearn classifier
- **Dask integration**: Distributed processing for large-scale datasets
- **Time series with metadata**: Handle complex data structures (multiple series, IDs, timestamps)

## Performance Characteristics

**Computational Complexity**:
- Feature extraction: O(n*m*f) where n=series count, m=series length, f=feature count
- Scales linearly with number of series
- Feature selection: Additional O(f) per feature for hypothesis tests

**Scalability**:
- **Small datasets (<1000 series)**: Runs in minutes
- **Medium datasets (1000-10k series)**: Use multiprocessing (n_jobs=-1)
- **Large datasets (>10k series)**: Use Dask for distribution
- Memory usage: ~10-50MB per 1000 series (depends on feature count)

**Speed Benchmarks**:
- 100 time series (length 1000): ~30 seconds (8 cores)
- 1000 time series: ~5 minutes (8 cores)
- 10,000 time series: ~1 hour (distributed Dask cluster)

## Ecosystem Integration

**Dependencies**:
- Core: NumPy, Pandas, scikit-learn, statsmodels, scipy
- Optional: Dask (distributed), joblib (parallelization)
- Compatible with: Any scikit-learn classifier/regressor

**Installation**:
```bash
pip install tsfresh
# With Dask for large-scale:
pip install tsfresh[dask]
```

**Compatibility**:
- Python 3.7+
- Works with pandas DataFrames and Series
- Outputs feature matrix compatible with sklearn
- Integrates with ML pipelines

## Community and Maintenance

**GitHub Statistics** (as of 2026-01):
- Stars: ~8.3k
- Contributors: 90+
- Active maintenance by Blue Yonder/JDA
- Production use in enterprise settings

**Documentation Quality**:
- Comprehensive documentation with tutorials
- Quick start guide
- Feature calculation details
- API reference

**Maintenance Status**: ✅ Actively maintained
- Regular updates and bug fixes
- Used in production at Blue Yonder
- Community-driven feature requests

**Academic Foundation**:
- Published in Neurocomputing (2018): "Time Series FeatuRe Extraction on basis of Scalable Hypothesis tests (tsfresh – A Python package)"
- Cited in 1000+ research papers

## Primary Use Cases

### Time Series Classification Preprocessing
- **Scenario**: Classify sensor data (accelerometer, ECG) into activity types
- **Approach**: Extract 794 features → select relevant ones → train sklearn classifier
- **Benefit**: Automatic feature engineering replaces manual domain expertise

### Anomaly Detection Feature Generation
- **Scenario**: Detect fraudulent transactions in temporal patterns
- **Approach**: Extract features from time series, use Random Forest for classification
- **Benefit**: Captures complex temporal patterns as numeric features

### Medical Signal Analysis
- **Scenario**: Classify heart arrhythmias from ECG time series
- **Approach**: tsfresh extraction → feature selection → SVM classifier
- **Benefit**: Statistical features capture signal characteristics automatically

### IoT Sensor Classification
- **Scenario**: Predict equipment failure from sensor readings
- **Approach**: Rolling window extraction → feature matrix → XGBoost classifier
- **Benefit**: Handles multiple sensors and time windows systematically

### Customer Behavior Prediction
- **Scenario**: Predict churn from usage time series
- **Approach**: Extract features per customer → select predictive features → logistic regression
- **Benefit**: Transforms temporal behavior into predictive features

## Strengths

1. **Automatic feature engineering**: No manual feature design required
2. **Comprehensive feature set**: 794+ features cover most temporal patterns
3. **Statistical rigor**: Hypothesis testing ensures feature relevance
4. **Scalable**: Dask integration for large datasets
5. **Production-proven**: Used in enterprise environments
6. **sklearn integration**: Works seamlessly with existing ML workflows
7. **Well-documented**: Clear examples and API reference
8. **Feature interpretability**: Features have clear statistical meaning

## Limitations

1. **Not a search library**: Doesn't do DTW, shapelets, or similarity search directly
2. **Computationally expensive**: Extracting 794 features per series is slow
3. **Feature explosion**: Many features can lead to overfitting without selection
4. **Requires preprocessing**: Needs clean, structured time series data
5. **Memory intensive**: Large feature matrices for big datasets
6. **No real-time support**: Batch processing only
7. **Fixed feature set**: Limited ability to add custom domain-specific features

## Comparison to Alternatives

**vs. tslearn (Shapelets)**:
- tsfresh: Statistical features for any classifier
- tslearn: Distance-based features (DTW, shapelets) for classification

**vs. sktime**:
- tsfresh: Feature extraction only (use with sklearn)
- sktime: End-to-end framework (features + classifiers)

**vs. Catch22**:
- tsfresh: 794+ features, comprehensive
- Catch22: 22 canonical features, faster, less redundant

**vs. pyts (Transformations)**:
- tsfresh: Statistical feature extraction
- pyts: Imaging and dictionary-based transformations

## Decision Criteria

**Choose tsfresh when**:
- Need automatic feature engineering for time series classification
- Want to avoid manual feature design
- Have sufficient computational resources (multi-core CPU)
- Working with structured, labeled time series data
- Plan to use standard ML classifiers (Random Forest, XGBoost, SVM)
- Need interpretable features with statistical meaning
- Dataset size: 100-100,000 time series

**Avoid tsfresh when**:
- Need DTW or similarity-based search (use tslearn, dtaidistance)
- Require real-time/streaming feature extraction
- Have very large datasets (>1M series) without Dask cluster
- Only need a few hand-crafted features (overhead not worth it)
- Working with very short time series (<10 points)
- Need end-to-end classification (use sktime instead)

## Getting Started Example

```python
from tsfresh import extract_features, select_features
from tsfresh.utilities.dataframe_functions import impute
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

# Sample data: DataFrame with columns [id, time, value]
# id: time series identifier, time: timestamp, value: measurement
df = pd.DataFrame({
    'id': [1,1,1,2,2,2,3,3,3],
    'time': [0,1,2,0,1,2,0,1,2],
    'value': [0.1, 0.5, 0.3, 0.8, 0.9, 0.7, 0.2, 0.3, 0.1]
})
y = pd.Series([0, 1, 0], index=[1, 2, 3])  # Labels for each time series

# Extract features (794 default features per time series)
features = extract_features(
    df,
    column_id='id',
    column_sort='time',
    n_jobs=4  # Use 4 CPU cores
)

# Impute missing values (some features may be NaN)
features_imputed = impute(features)

# Select relevant features using hypothesis tests
features_selected = select_features(features_imputed, y)
print(f"Selected {len(features_selected.columns)} features out of {len(features.columns)}")

# Train classifier with selected features
X_train, X_test, y_train, y_test = train_test_split(
    features_selected, y, test_size=0.3, random_state=42
)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")

# Or use extract_relevant_features (one-step extraction + selection)
from tsfresh import extract_relevant_features
features_filtered = extract_relevant_features(
    df, y,
    column_id='id',
    column_sort='time'
)
```

## Sources

- [tsfresh GitHub Repository](https://github.com/blue-yonder/tsfresh) - Accessed 2026-01-30
- [tsfresh Documentation](https://tsfresh.readthedocs.io/en/latest/) - Accessed 2026-01-30
- [Quick Start Guide](https://tsfresh.readthedocs.io/en/latest/text/quick_start.html) - Accessed 2026-01-30
- [tsfresh PyPI](https://pypi.org/project/tsfresh/) - Accessed 2026-01-30
- [Neurocomputing Paper (2018)](https://www.sciencedirect.com/science/article/pii/S0925231218304843) - "Time Series FeatuRe Extraction on basis of Scalable Hypothesis tests", Accessed 2026-01-30
- [GeeksforGeeks Tutorial (July 2025)](https://www.geeksforgeeks.org/data-analysis/advanced-feature-extraction-and-selection-from-time-series-data-using-tsfresh-in-python/) - Accessed 2026-01-30
- [ResearchGate Publication](https://www.researchgate.net/publication/324948288_Time_Series_FeatuRe_Extraction_on_basis_of_Scalable_Hypothesis_tests_tsfresh_-_A_Python_package) - Accessed 2026-01-30
- [Semantic Scholar](https://www.semanticscholar.org/paper/Time-Series-FeatuRe-Extraction-on-basis-of-Scalable-Christ-Braun/82f472fb8e5f7db675f7b75000047b637b2facc7) - Accessed 2026-01-30
