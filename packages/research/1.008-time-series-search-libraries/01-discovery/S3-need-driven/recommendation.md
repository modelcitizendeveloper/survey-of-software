# S3: Need-Driven Discovery - Recommendations

## Executive Summary

Based on analysis of 5 real-world scenarios across manufacturing, healthcare, finance, e-commerce, and infrastructure, time series search libraries deliver **10-50x ROI** when matched to the correct use case. The key differentiator is not "which library is best" but **"which library fits your search pattern and scale requirements."**

## Decision Framework by Use Case

### Pattern Matching & Search

| Use Case | Data Scale | Recommended Library | Key Rationale | ROI |
|----------|-----------|-------------------|---------------|-----|
| **Unsupervised anomaly detection** | <10K series | **STUMPY** | Matrix profile for discords, no training needed | 10x |
| **Unsupervised anomaly detection** | >10K series | **STUMPY + Dask** | Scales to millions with parallel computation | 3.4x |
| **Supervised classification** | Any | **sktime (ROCKET)** | State-of-the-art accuracy, fast training | 6.8x |
| **Interpretable classification** | <5K series | **tslearn (shapelets)** | Shows which waveform patterns matter | 5x |
| **Customer segmentation** | <100K customers | **tslearn (DTW K-means)** | Shape-based clustering, handles timing variations | 26.7x |
| **Motif discovery (fraud rings)** | 1M+ sequences | **STUMPY (motifs/AB-joins)** | Finds repeated patterns across accounts | 55x |
| **Real-time streaming** | High-frequency | **STUMPY (FLOSS)** | Incremental matrix profile updates | 10x |

### When to Use Each Library

**STUMPY (Unsupervised Pattern Discovery)**:
- ✅ **Anomaly detection** without labeled data
- ✅ **Motif discovery** (find recurring patterns)
- ✅ **Real-time streaming** (FLOSS)
- ✅ **Large scale** (GPU + Dask support)
- ❌ Supervised classification (use sktime instead)

**sktime (Supervised Classification & Pipelines)**:
- ✅ **Classification tasks** with labeled data
- ✅ **Benchmarking** multiple classifiers
- ✅ **Production ML pipelines** (scikit-learn API)
- ❌ Unsupervised motif discovery (use STUMPY instead)
- ❌ Only need DTW distance (use dtaidistance - 30x faster)

**tslearn (DTW-Based Methods & Clustering)**:
- ✅ **Clustering** by shape similarity
- ✅ **Interpretable shapelets** (show which patterns matter)
- ✅ **DTW with constraints** (Sakoe-Chiba, Itakura)
- ❌ Large-scale classification (sktime ROCKET is faster)
- ❌ Real-time streaming (use STUMPY FLOSS instead)

**tsfresh (Feature Extraction for Standard ML)**:
- ✅ **Feature engineering** for non-specialist classifiers (XGBoost, Random Forest)
- ✅ **Statistical features** (794 built-in)
- ✅ **Feature selection** (hypothesis tests)
- ❌ Real-time classification (too slow for high-frequency)
- ❌ Time series-native tasks (DTW, matrix profile better fit)

**dtaidistance (Fast DTW-Only)**:
- ✅ **Performance-critical** DTW distance matrices
- ✅ **Minimal dependencies** (C implementation)
- ✅ **Exact DTW** needed (not approximate)
- ❌ Classification (provides distance only, not classifier)
- ❌ Feature extraction (use tsfresh)

**pyts (Imaging & Symbolic Methods)**:
- ✅ **Imaging methods** for CNN classification (GAF, MTF)
- ✅ **Symbolic representations** (SAX, VSM)
- ✅ **Research/experimentation** with novel methods
- ❌ Production deployment (lower maintenance, less active than sktime/STUMPY)
- ❌ Standard classification (sktime ROCKET is more accurate)

## Scenario-Specific Recommendations

### Scenario 1: Manufacturing Quality Control
**Problem**: Real-time anomaly detection in high-frequency sensor data (1000 Hz vibration)
**Recommended**: **STUMPY (FLOSS streaming)**
**ROI**: $500K/year benefit, $50K cost = **10x ROI**

**Implementation**:
1. Offline: Build 1-2 week baseline matrix profile
2. Online: FLOSS streaming with 250ms window
3. Alert: Distance >3σ triggers operator notification with similar past failures

**Why not others**: tsfresh too slow for 1000 Hz real-time, tslearn DTW can't handle streaming

---

### Scenario 2: Healthcare ECG Classification
**Problem**: Arrhythmia classification with 98%+ accuracy requirement
**Recommended**: **sktime (ROCKET)**
**ROI**: $580K/year benefit, $85K cost = **6.8x ROI**

**Implementation**:
1. Train on MIT-BIH database (110K labeled beats)
2. Deploy real-time ROCKET classifier (<1 second latency)
3. Alert on VF/VT with >85% confidence

**Alternative**: tslearn shapelets if clinicians need to see "which waveform pattern" caused classification

---

### Scenario 3: Financial Fraud Detection
**Problem**: Discover novel fraud patterns (motifs) across millions of accounts
**Recommended**: **STUMPY (motif discovery + AB-joins)**
**ROI**: $5M/year benefit, $100K cost = **50x ROI**

**Implementation**:
1. Convert transaction sequences to time series (amount over time)
2. Find recurring patterns with STUMPY motifs
3. Flag accounts with same pattern (fraud rings)
4. AB-joins to find coordinated fraud across accounts

**Why not others**: tsfresh doesn't find cross-account motifs, tslearn doesn't scale to millions

---

### Scenario 4: E-commerce Customer Clustering
**Problem**: Segment customers by temporal purchase behavior (not just totals)
**Recommended**: **tslearn (TimeSeriesKMeans with DTW)**
**ROI**: $2M/year revenue increase, $75K cost = **26.7x ROI**

**Implementation**:
1. Create 90-day purchase time series per customer
2. Normalize to focus on pattern (not magnitude)
3. DTW K-means clustering into 8 segments
4. Personalize offers by segment (loyal vs. sale hunters vs. churn risk)

**Why not others**: Standard K-means ignores timing patterns, STUMPY doesn't create interpretable segments

---

### Scenario 5: Infrastructure Monitoring at Scale
**Problem**: Anomaly detection across 10K servers, 500K metrics/minute
**Recommended**: **STUMPY + Dask** (parallelized)
**ROI**: $683K/year savings, $200K cost = **3.4x ROI**

**Implementation**:
1. Daily: Dask-parallelized baseline computation (10K matrix profiles)
2. Online: FLOSS streaming on 10 worker nodes
3. Alert: Dedupe correlated alerts (same root cause)

**Alternative**: Prophet + Isolation Forest if you prefer statistical forecasting

---

## Common Anti-Patterns to Avoid

### Anti-Pattern 1: Using Supervised Methods Without Labels
**Problem**: "We want to detect anomalies but have no labeled failure data"
**Wrong choice**: sktime, tslearn shapelets, tsfresh (all need labels)
**Right choice**: **STUMPY** (unsupervised discord discovery)

### Anti-Pattern 2: Using Slow Libraries for Real-Time
**Problem**: "We need <1 second classification on 1000 Hz data"
**Wrong choice**: tsfresh (feature extraction too slow)
**Right choice**: **sktime ROCKET** or **STUMPY FLOSS**

### Anti-Pattern 3: Using DTW Without Constraints on Large Datasets
**Problem**: "DTW clustering takes 10 hours on 10K time series"
**Wrong choice**: Unconstrained DTW (O(n²m²) complexity)
**Right choice**: **dtaidistance with Sakoe-Chiba band** or **sktime ROCKET** (avoids DTW entirely)

### Anti-Pattern 4: Using Time Series Classification for Forecasting
**Problem**: "We want to predict future revenue"
**Wrong choice**: These libraries (they search/classify, not forecast)
**Right choice**: **1.073 Time Series Forecasting libraries** (Prophet, ARIMA, neural forecasting)

### Anti-Pattern 5: Overfitting with tsfresh on Small Datasets
**Problem**: "We have 100 samples and 794 tsfresh features"
**Wrong choice**: Use all features (massive overfitting)
**Right choice**: **tsfresh feature selection** (hypothesis tests reduce to 10-50 features)

## Combining Libraries for Enhanced Capabilities

### Pattern 1: STUMPY + sktime (Discovery + Classification)
```python
# Step 1: Use STUMPY to find interesting patterns (motifs)
import stumpy
mp = stumpy.stump(data, m=100)
motifs = stumpy.motifs(data, mp, max_motifs=10)

# Step 2: Extract motif occurrences as features
motif_features = extract_motif_features(data, motifs)

# Step 3: Use sktime to classify with motif features
from sktime.classification.kernel_based import RocketClassifier
clf = RocketClassifier()
clf.fit(motif_features, labels)
```

### Pattern 2: tsfresh + ROCKET (Statistical + Transform Features)
```python
# Extract 794 statistical features
from tsfresh import extract_features
stat_features = extract_features(df, column_id='id', column_sort='time')

# Extract 10,000 ROCKET transform features
from sktime.transformations.panel.rocket import Rocket
rocket_features = Rocket().fit_transform(X)

# Combine and train ensemble
combined = np.hstack([stat_features, rocket_features])
```

### Pattern 3: dtaidistance + Custom Logic (Fast DTW + Rules)
```python
# Use dtaidistance for fast distance matrix
from dtaidistance import dtw
dist_matrix = dtw.distance_matrix_fast(X, use_c=True, parallel=True)

# Apply custom business logic
for i, distances in enumerate(dist_matrix):
    nearest_neighbor_dist = distances.min()
    if nearest_neighbor_dist < similarity_threshold:
        # Similar to known good pattern
        classify_as_normal(i)
    else:
        # Novel pattern = potential anomaly
        flag_for_review(i)
```

## Deployment Considerations

### Small Scale (<1K time series)
**Recommended stack**: Single library (tslearn or STUMPY)
**Infrastructure**: Single CPU server
**Cost**: $5K-10K (implementation only, no special hardware)

### Medium Scale (1K-100K time series)
**Recommended stack**: sktime or STUMPY with parallelization
**Infrastructure**: Multi-core server or small cluster (4-8 nodes)
**Cost**: $50K-100K (implementation + basic cloud infrastructure)

### Large Scale (>100K time series)
**Recommended stack**: STUMPY + Dask + GPU
**Infrastructure**: Dask cluster (20+ nodes), GPU nodes for baseline computation
**Cost**: $200K-500K (significant engineering + infrastructure)

## Success Criteria by Industry

### Manufacturing
- **Defect detection rate**: 95%+ (vs. 85-90% baseline)
- **False positive rate**: <5% (vs. 15-20% baseline)
- **Early warning**: Detect degradation 2-4 hours before failure
- **ROI timeline**: 3-6 months payback

### Healthcare
- **Sensitivity/Specificity**: 98%+/95%+ on clinical validation
- **Alert reduction**: 80%+ fewer false alarms
- **Regulatory**: FDA clearance if selling externally (internal use = CDS exemption)
- **ROI timeline**: 6-12 months (includes clinical validation)

### Finance
- **Fraud detection rate**: 85%+ (vs. 60% baseline)
- **False positive reduction**: 95% → <35%
- **Novel pattern discovery**: 10+ new schemes per quarter
- **ROI timeline**: 1-3 months

### E-commerce
- **Conversion lift**: +15-25% from personalized offers
- **Churn reduction**: -20%+ in at-risk segments
- **Segment stability**: 80%+ customers stay in same segment month-to-month
- **ROI timeline**: 3-6 months

### Infrastructure/DevOps
- **Alert volume reduction**: 99%+ (10K → <100 alerts/day)
- **Alert precision**: 80%+ (alerts lead to action)
- **MTTD (Mean Time to Detection)**: <1 minute
- **ROI timeline**: 6-12 months (infrastructure investment)

## Next Steps: Integration with S4 Strategic Analysis

S3 demonstrated **when and how** to deploy time series search for specific business needs. S4 will address:

1. **Long-term viability**: Which libraries will still exist in 5 years? Maintenance risk?
2. **Vendor ecosystem**: Commercial support, consulting, training availability
3. **Competitive landscape**: How do these compare to commercial offerings (Datadog, Splunk)?
4. **Technology trends**: What's replacing these libraries? (LLM-based anomaly detection, foundation models?)
5. **Total cost of ownership**: Hidden costs (GPU, engineering time, maintenance)

## Summary

**The "best" library is context-dependent:**
- **Unsupervised anomaly detection** → STUMPY
- **Supervised classification** → sktime (ROCKET)
- **Shape-based clustering** → tslearn (DTW K-means)
- **Fast DTW-only** → dtaidistance
- **Feature extraction for standard ML** → tsfresh

**All 5 scenarios showed 3-55x ROI** when the right library was matched to the use case. The failure mode is not "choosing the wrong library" but "forcing a library into the wrong use case."
