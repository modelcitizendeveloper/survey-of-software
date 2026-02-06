# S2: Integration Complexity & Deployment Patterns

## Dependency Analysis

### Core Dependencies Comparison

| Library | Core Deps | Optional Deps | Total Install Size | Python Versions |
|---------|-----------|---------------|-------------------|-----------------|
| **dtaidistance** | numpy | cython (build only) | 45 MB | 3.7-3.12 |
| **STUMPY** | numpy, scipy, numba | cupy (GPU), dask | 125 MB | 3.8-3.12 |
| **pyts** | numpy, scipy, scikit-learn, joblib | tensorflow (GAF+CNN) | 150 MB | 3.7-3.10 |
| **tslearn** | numpy, scipy, scikit-learn | tensorflow, keras | 280 MB | 3.7-3.12 |
| **tsfresh** | pandas, scikit-learn, statsmodels, patsy | dask, tqdm | 310 MB | 3.7-3.11 |
| **sktime** | numpy, scipy, pandas, scikit-learn | 40+ optional packages | 450 MB | 3.8-3.12 |

**Key Findings**:
- **dtaidistance lightest** (45 MB, minimal dependencies)
- **sktime heaviest** (450 MB, largest ecosystem)
- **pyts lagging Python support** (no 3.11/3.12 yet)
- **Optional dependencies matter**: GPU (cupy), distributed (dask), deep learning (tensorflow)

### Dependency Conflict Analysis

**Common Conflict Points**:

1. **NumPy version**:
   - dtaidistance: requires >=1.20 (C compilation compatibility)
   - STUMPY: requires >=1.17 (numba compatibility)
   - sktime: requires >=1.21 (array API changes)
   - **Resolution**: Use NumPy >=1.21 (all compatible)

2. **scikit-learn version**:
   - tslearn: tightly coupled to sklearn API (requires >=0.23)
   - sktime: extensive sklearn integration (requires >=1.0)
   - tsfresh: feature selection depends on sklearn (requires >=0.22)
   - **Resolution**: Use sklearn >=1.0 (backward compatible)

3. **Numba version** (STUMPY only):
   - Requires numba >=0.50 for JIT compilation
   - Numba has llvmlite dependency (can conflict with other JIT libraries)
   - **Gotcha**: Numba not compatible with PyPy (CPython only)

4. **Pandas version** (tsfresh, sktime):
   - tsfresh expects DataFrame inputs (requires pandas >=0.22)
   - sktime supports both numpy and pandas (optional)
   - **Gotcha**: Pandas 2.0 introduced breaking changes (check library versions)

**Dependency Hell Scenarios**:

```python
# Scenario 1: GPU conflicts
# STUMPY (cupy) + pyts (tensorflow) can conflict on CUDA versions
# STUMPY cupy-cuda11x vs. tensorflow-gpu cuda12x
# Resolution: Use CPU-only versions or match CUDA versions

# Scenario 2: Dask version conflicts
# STUMPY (dask >=2.0) + tsfresh (dask >=2021.1.0) usually compatible
# But dask-ml or dask-cuda can introduce conflicts
# Resolution: Pin dask version explicitly

# Scenario 3: Cython build failures
# dtaidistance, tslearn require C compiler for installation
# macOS: need Xcode, Linux: need gcc, Windows: need Visual Studio
# Resolution: Use pre-built wheels (conda-forge or PyPI)
```

---

## API Learning Curve

### API Complexity Matrix

| Library | API Style | Lines of Code (Typical Use) | Learning Curve | Documentation Quality |
|---------|-----------|----------------------------|----------------|---------------------|
| **STUMPY** | NumPy functions | 5-10 lines | Medium | ⭐⭐⭐⭐⭐ Excellent |
| **dtaidistance** | Low-level C API | 3-5 lines | High (advanced) | ⭐⭐⭐ Good |
| **sktime** | sklearn API | 8-15 lines | Low (familiar) | ⭐⭐⭐⭐⭐ Excellent |
| **tslearn** | sklearn API | 8-12 lines | Low (familiar) | ⭐⭐⭐⭐ Good |
| **tsfresh** | Pandas dataframes | 10-20 lines | Medium | ⭐⭐⭐⭐ Good |
| **pyts** | sklearn API | 8-15 lines | Low (familiar) | ⭐⭐⭐ Fair |

### Hello World: Classification Task

**STUMPY** (Anomaly Detection - No Supervised Equivalent):
```python
import stumpy
import numpy as np

data = np.random.randn(10000)
m = 100  # window size
mp = stumpy.stump(data, m)  # matrix profile
discord_idx = np.argmax(mp[:, 0])  # most anomalous pattern

# 3 lines of core logic
```

**sktime** (ROCKET Classifier):
```python
from sktime.classification.kernel_based import RocketClassifier
from sktime.datasets import load_arrow_head

X_train, y_train = load_arrow_head(split="train", return_X_y=True)
X_test, y_test = load_arrow_head(split="test", return_X_y=True)

clf = RocketClassifier()
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)

# 3 lines of core logic (familiar sklearn pattern)
```

**tslearn** (DTW K-Means Clustering):
```python
from tslearn.clustering import TimeSeriesKMeans
from tslearn.datasets import CachedDatasets

X = CachedDatasets().load_dataset("Trace")[0]  # load data
km = TimeSeriesKMeans(n_clusters=3, metric="dtw", max_iter=10)
labels = km.fit_predict(X)

# 2 lines of core logic
```

**tsfresh** (Feature Extraction):
```python
from tsfresh import extract_features
from tsfresh.utilities.dataframe_functions import impute
import pandas as pd

df = pd.read_csv("timeseries.csv")  # columns: id, time, value
features = extract_features(df, column_id='id', column_sort='time')
features_clean = impute(features)  # handle NaN from failed feature extraction

# 2 lines of core logic, but pandas setup overhead
```

**dtaidistance** (DTW Distance):
```python
from dtaidistance import dtw
import numpy as np

s1 = np.array([0, 0, 1, 2, 1, 0, 1, 0, 0])
s2 = np.array([0, 1, 2, 0, 0, 0, 0, 0, 0])
distance = dtw.distance(s1, s2)

# 1 line of core logic (but need to know DTW parameters)
```

**pyts** (GAF Imaging):
```python
from pyts.image import GramianAngularField
import numpy as np

X = np.random.randn(10, 48)  # 10 time series, length 48
gaf = GramianAngularField(image_size=24, method='summation')
X_gaf = gaf.fit_transform(X)  # (10, 24, 24) images

# 2 lines of core logic
```

**Learning Curve Ranking** (Easiest to Hardest):
1. **tslearn/sktime** (sklearn API = instant familiarity)
2. **pyts** (sklearn API but imaging concepts need learning)
3. **STUMPY** (NumPy-style but matrix profile concepts new)
4. **tsfresh** (pandas overhead + feature selection complexity)
5. **dtaidistance** (low-level API, need DTW parameter expertise)

---

## Production Deployment Patterns

### Containerization: Docker Best Practices

**dtaidistance** (Lightweight):
```dockerfile
FROM python:3.10-slim
RUN apt-get update && apt-get install -y gcc
RUN pip install dtaidistance
# Image size: 450 MB
```

**STUMPY** (CPU):
```dockerfile
FROM python:3.10-slim
RUN pip install stumpy dask distributed
# Image size: 850 MB
```

**STUMPY** (GPU):
```dockerfile
FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04
RUN pip install stumpy cupy-cuda11x
# Image size: 3.2 GB (CUDA overhead)
```

**sktime** (Full Stack):
```dockerfile
FROM python:3.10
RUN pip install sktime[all_extras]
# Image size: 2.1 GB (includes 40+ optional packages)
```

**Production Optimization**:
```dockerfile
# Multi-stage build for minimal final image
FROM python:3.10 as builder
WORKDIR /install
RUN pip install --prefix=/install stumpy

FROM python:3.10-slim
COPY --from=builder /install /usr/local
# Reduced image: 850 MB → 520 MB
```

### Cloud Platform Deployment

**AWS SageMaker**:
- **Best**: sktime (sklearn API works out-of-box with SageMaker SDK)
- **Good**: tsfresh (pandas → CSV → SageMaker training job)
- **Manual**: STUMPY (need custom inference container)

**Azure ML**:
- **Best**: sktime (registered as MLflow model)
- **Good**: tslearn (sklearn API compatible with Azure AutoML)
- **Manual**: dtaidistance (low-level API, need wrapper)

**Google Vertex AI**:
- **Best**: sktime (Vertex AI Pipelines support sklearn)
- **Good**: tsfresh (can use Dataflow for distributed feature extraction)
- **Manual**: STUMPY GPU (need custom Vertex AI training job with GPU)

**Serverless (AWS Lambda, Cloud Functions)**:
- **Viable**: dtaidistance (45 MB fits in Lambda)
- **Marginal**: STUMPY (125 MB fits but tight)
- **Infeasible**: sktime (450 MB exceeds 250 MB deployment package limit)

### Real-Time Serving Patterns

**Pattern 1: REST API (Flask/FastAPI)**

```python
# sktime ROCKET (easiest deployment)
from fastapi import FastAPI
from sktime.classification.kernel_based import RocketClassifier
import joblib

app = FastAPI()
model = joblib.load("rocket_model.pkl")  # load once at startup

@app.post("/predict")
async def predict(data: list):
    prediction = model.predict([data])  # 0.12ms latency
    return {"class": int(prediction[0])}

# Latency: 0.12ms inference + 2ms network overhead = 2.12ms
# Throughput: 470 req/sec (single instance)
```

**Pattern 2: Streaming (Kafka + STUMPY FLOSS)**

```python
# STUMPY streaming anomaly detection
from kafka import KafkaConsumer, KafkaProducer
import stumpy
import numpy as np

consumer = KafkaConsumer('sensor-data')
producer = KafkaProducer('anomaly-alerts')

historic_data = np.load("baseline.npy")  # 1 week normal operation
stream_mp = stumpy.floss(
    stream=consumer,
    m=100,
    historic=historic_data,
    egress=True
)

for distance, pattern in stream_mp:
    if distance > threshold:
        producer.send('anomaly-alerts', pattern)

# Latency: 0.15ms (GPU) per data point
# Throughput: 6,667 Hz (real-time for 1,000 Hz sensor)
```

**Pattern 3: Batch (Spark + tsfresh)**

```python
# tsfresh distributed feature extraction
from pyspark.sql import SparkSession
from tsfresh import extract_features
from tsfresh.utilities.distribution import DistributorBaseClass

spark = SparkSession.builder.appName("TSFresh").getOrCreate()
df_spark = spark.read.parquet("timeseries_data.parquet")

# tsfresh with PySpark distributor
features = extract_features(
    df_spark.toPandas(),
    column_id='id',
    column_sort='time',
    distributor=SparkDistributor(spark_context=spark.sparkContext)
)

# Throughput: 1M time series in 2.5 hours (100-node Spark cluster)
```

---

## MLOps Integration

### Model Versioning & Registry

| Library | MLflow Support | Weights & Biases | Custom Serialization |
|---------|---------------|------------------|---------------------|
| **sktime** | ✅ Native (sklearn API) | ✅ Yes | joblib |
| **tslearn** | ✅ Native (sklearn API) | ✅ Yes | joblib |
| **pyts** | ✅ Native (sklearn API) | ✅ Yes | joblib |
| **tsfresh** | ⚠️ Features only | ⚠️ Custom wrapper | pickle |
| **STUMPY** | ❌ No (stateless functions) | ❌ N/A | Save matrix profile (numpy) |
| **dtaidistance** | ❌ No (distance function) | ❌ N/A | N/A (stateless) |

**Best Practice: Model Versioning**

```python
# sktime + MLflow (automatic versioning)
import mlflow
from sktime.classification.kernel_based import RocketClassifier

with mlflow.start_run():
    clf = RocketClassifier()
    clf.fit(X_train, y_train)

    mlflow.sklearn.log_model(clf, "rocket_model")  # auto-versioned
    mlflow.log_metric("accuracy", clf.score(X_test, y_test))

# Retrieval
model = mlflow.sklearn.load_model("runs:/<run_id>/rocket_model")
```

### Experiment Tracking

**sktime + Weights & Biases**:
```python
import wandb
from sktime.classification.kernel_based import RocketClassifier

wandb.init(project="time-series-clf")
clf = RocketClassifier()
clf.fit(X_train, y_train)

wandb.log({"accuracy": clf.score(X_test, y_test)})
wandb.log({"training_time": training_time})
```

**STUMPY + Custom Logging**:
```python
# STUMPY has no model (stateless), log matrix profile statistics
import stumpy
import wandb

wandb.init(project="anomaly-detection")
mp = stumpy.stump(data, m=100)

wandb.log({
    "motifs_found": len(stumpy.motifs(data, mp, max_motifs=10)),
    "discord_distance": np.max(mp[:, 0]),
    "computation_time": time_taken
})
```

### A/B Testing Infrastructure

**Scenario**: Compare ROCKET vs. DTW-KNN in production

```python
# Feature flag-based A/B testing
import random
from sktime.classification.kernel_based import RocketClassifier
from tslearn.neighbors import KNeighborsTimeSeriesClassifier

def classify(data, user_id):
    # 50/50 split based on user_id hash
    if hash(user_id) % 2 == 0:
        model = rocket_model  # Variant A
        variant = "rocket"
    else:
        model = knn_dtw_model  # Variant B
        variant = "knn_dtw"

    prediction = model.predict([data])

    # Log for analysis
    metrics_logger.log({
        "user_id": user_id,
        "variant": variant,
        "prediction": prediction,
        "latency": latency_ms
    })

    return prediction
```

---

## Integration Gotchas & Solutions

### Gotcha 1: Input Shape Mismatch

**Problem**: Different libraries expect different input shapes

```python
# sktime expects (n_samples, n_features, n_timepoints) for multivariate
X_sktime = np.random.randn(100, 3, 200)  # 100 samples, 3-dim, length 200

# tslearn expects (n_samples, n_timepoints, n_features)
X_tslearn = np.random.randn(100, 200, 3)  # same data, transposed

# STUMPY expects 1D or 2D (n_timepoints, n_dims)
X_stumpy = np.random.randn(200, 3)  # single sample, multi-dimensional
```

**Solution**: Use explicit transposes and document shape conventions

```python
def to_sktime_format(X):
    """Convert (n_samples, n_timepoints, n_features) → (n_samples, n_features, n_timepoints)"""
    return np.transpose(X, (0, 2, 1))

def to_tslearn_format(X):
    """Convert (n_samples, n_features, n_timepoints) → (n_samples, n_timepoints, n_features)"""
    return np.transpose(X, (0, 2, 1))
```

### Gotcha 2: Missing Value Handling

**Different libraries handle NaN differently**:

- **sktime**: Some classifiers support NaN, others fail
- **tslearn**: Fills NaN with 0 or interpolates (silent behavior)
- **tsfresh**: Generates NaN features (need impute())
- **STUMPY**: Fails on NaN (need explicit handling)

**Solution**: Explicit NaN handling upfront

```python
from sklearn.impute import SimpleImputer

def preprocess_for_library(X, library="sktime"):
    if library == "stumpy":
        # STUMPY requires no NaN
        imputer = SimpleImputer(strategy='mean')
        X_clean = imputer.fit_transform(X.reshape(-1, 1)).reshape(X.shape)
    elif library == "tsfresh":
        # tsfresh generates NaN features, handle post-extraction
        X_clean = X  # handle after extract_features
    else:
        # sklearn API libraries (sktime, tslearn, pyts)
        X_clean = X  # most handle internally

    return X_clean
```

### Gotcha 3: GPU Memory Management (STUMPY)

**Problem**: STUMPY GPU runs out of VRAM on large datasets

```python
import stumpy

# This fails on 16GB GPU for 10M points
mp = stumpy.gpu_stump(data, m=100)  # OOM error
```

**Solution**: Use Dask for distributed or batch processing

```python
import stumpy
import dask.array as da

# Dask version automatically batches
data_dask = da.from_array(data, chunks=1000000)  # 1M point chunks
mp = stumpy.stumped(data_dask, m=100, normalize=True)  # distributed
```

### Gotcha 4: Thread Safety (Numba JIT)

**Problem**: STUMPY uses Numba JIT (not thread-safe during compilation)

```python
# This causes race conditions
from concurrent.futures import ThreadPoolExecutor
import stumpy

def process(data):
    return stumpy.stump(data, m=100)  # JIT compiles on first call

with ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(process, datasets)  # RACE CONDITION
```

**Solution**: Warm up Numba before parallel execution

```python
import stumpy
import numpy as np

# Warm-up: trigger JIT compilation with dummy data
dummy = np.random.randn(1000)
stumpy.stump(dummy, m=10)  # compile once

# Now safe to parallelize
with ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(process, datasets)  # OK
```

### Gotcha 5: sklearn Pipeline Compatibility

**Problem**: Not all libraries support sklearn's Pipeline API

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# This works (sklearn API)
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', RocketClassifier())  # sktime
])

# This fails (STUMPY is not a transformer/estimator)
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('mp', stumpy.stump)  # ERROR: not sklearn API
])
```

**Solution**: Wrap non-sklearn libraries in custom transformers

```python
from sklearn.base import BaseEstimator, TransformerMixin

class STUMPYTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, m=100):
        self.m = m

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        mp = stumpy.stump(X, m=self.m)
        return mp[:, 0].reshape(-1, 1)  # return discord distances

# Now works in Pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('stumpy', STUMPYTransformer(m=100)),
    ('clf', RandomForestClassifier())
])
```

---

## Integration Complexity Summary

### Easy Integration (Minimal Friction)

**sktime, tslearn, pyts**:
- ✅ sklearn API (drop-in replacement)
- ✅ joblib serialization (model persistence)
- ✅ Pipeline support (preprocessing chains)
- ✅ MLflow/W&B compatible

**Use when**: Standard ML workflow, need MLOps integration

### Medium Integration (Some Friction)

**tsfresh**:
- ⚠️ Pandas DataFrame requirement (conversion overhead)
- ⚠️ Feature extraction separate from classification (two-step process)
- ⚠️ NaN features require imputation
- ✅ Can use with any sklearn classifier

**Use when**: Feature extraction for standard classifiers, batch processing

### Complex Integration (High Friction)

**STUMPY**:
- ❌ Not sklearn API (functional, not OO)
- ❌ No model persistence (stateless functions)
- ⚠️ Numba JIT warm-up needed for parallel
- ⚠️ GPU memory management required

**Use when**: Unsupervised pattern discovery, real-time streaming (unique capabilities justify complexity)

**dtaidistance**:
- ❌ Low-level C API (need to wrap)
- ❌ Returns distance matrix only (no classifier)
- ⚠️ Build dependency (requires C compiler)
- ✅ Minimal Python dependencies

**Use when**: Performance-critical DTW, minimal overhead required

### Recommended Integration Stack

**Greenfield Project** (New system):
1. **Default**: sktime (best ecosystem, MLOps support)
2. **Alternative**: tslearn (if DTW-focused, slightly lighter)

**Existing ML Pipeline** (sklearn already):
1. **Classification**: Add sktime (seamless integration)
2. **Feature extraction**: Add tsfresh (works with existing classifiers)

**Specialized Needs**:
1. **Real-time anomaly detection**: STUMPY (no alternative, worth complexity)
2. **Performance-critical DTW**: dtaidistance (30-300x speedup justifies C dependency)

**Avoid Mixing**:
- Don't use STUMPY + sktime (different paradigms, conversion overhead)
- Don't use dtaidistance + tslearn DTW (redundant, just use dtaidistance)
- Don't use tsfresh + ROCKET (both do feature extraction, pick one)
