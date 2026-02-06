# Scenario 2: Healthcare Patient Monitoring

## Business Context

**Industry**: Healthcare (Hospital ICU, Remote Patient Monitoring)
**Pain Point**: ECG arrhythmia classification and real-time alerting
**Current Approach**: Rule-based algorithms + manual review by nursing staff
**Cost of Failure**: Missed cardiac events, false alarms causing alert fatigue

### Business Metrics
- **Arrhythmia detection sensitivity**: 92% (8% missed events)
- **False alarm rate**: 85-95% (overwhelming nursing staff)
- **Nurse review time**: 4-6 hours/shift on false alarms
- **Missed event cost**: $50K-500K per adverse outcome + liability

## Use Case: ECG Pattern Classification

### Problem Statement

ICU monitors generate 300+ alerts per patient per day. 90% are false positives. Nurses spend significant time investigating alarms instead of patient care. Need ML classification to distinguish true arrhythmias from noise/movement artifacts.

### Data Profile

- **Volume**: 50 patients × 500 Hz × 24 hours = 2.16B data points/day
- **Classes**: Normal sinus, AF, VT, VF, PVC, artifact (6 classes)
- **Training data**: MIT-BIH Arrhythmia Database (48 patients, 110K labeled beats)
- **Deployment**: Real-time classification (<1 second latency)

## Recommended Solution: sktime with ROCKET Classifier

### Rationale

**Why sktime + ROCKET**:
1. **State-of-the-art accuracy**: 98%+ on UCR ECG datasets
2. **Fast training**: 100x faster than DTW-based methods
3. **No hyperparameter tuning**: Minimal configuration
4. **Interpretable**: Can extract most important features for clinician review

**Why not alternatives**:
- ❌ **STUMPY**: Unsupervised (needs labeled data for safety-critical classification)
- ❌ **tslearn (DTW shapelets)**: Slower, not significantly more accurate than ROCKET
- ❌ **tsfresh**: 794 features cause overfitting on small medical datasets

### Architecture

```python
from sktime.classification.kernel_based import RocketClassifier
from sktime.datasets import load_ECG200
import numpy as np

# Train on MIT-BIH database
X_train, y_train = load_mit_bih_data()  # (110000, 180) - 180 samples per beat
rocket = RocketClassifier(num_kernels=10000)
rocket.fit(X_train, y_train)

# Real-time: Classify each detected heartbeat
ecg_stream = PatientMonitor(patient_id=123)
for heartbeat in ecg_stream.detect_beats():
    beat_segment = heartbeat.get_window(length=180)  # 360ms window

    prediction = rocket.predict([beat_segment])[0]
    confidence = rocket.predict_proba([beat_segment])[0]

    if prediction in ['VF', 'VT'] and confidence.max() > 0.85:
        # Critical arrhythmia with high confidence
        alert_care_team(priority='CRITICAL', pattern=beat_segment)
    elif prediction == 'artifact' or confidence.max() < 0.7:
        # Likely false alarm, suppress
        log_suppressed_alert(reason='low_confidence')
```

### Expected Outcomes

**Quantitative**:
- Arrhythmia detection sensitivity: 92% → 98% (+6% fewer missed events)
- False alarm reduction: 90% false positive rate → 15% (83% reduction)
- Nurse alarm review time: 4-6 hours/shift → 30 minutes (-88%)
- Cost savings: $300K/year (reduced nursing time + fewer adverse events)

**Qualitative**:
- Reduced alert fatigue (nurses trust alarms)
- Faster response to true arrhythmias
- Auditability (can review classifier decision for each alert)

## Alternative Approaches

### Alternative 1: tslearn Shapelets (If Interpretability Critical)

**When to use**: If clinicians need to see "which part of the waveform" caused the classification

```python
from tslearn.shapelets import LearningShapelets

# Train shapelet-based classifier
clf = LearningShapelets(n_shapelets_per_size={30: 5, 50: 5}, max_iter=500)
clf.fit(X_train, y_train)

# For each prediction, show which shapelet matched
shapelet_match = clf.shapelets_as_time_series_
# Clinician can see: "Classified as VT because this 30ms pattern matched"
```

**Trade-offs**:
- ✅ Highly interpretable (shows exact waveform patterns used)
- ✅ Good accuracy (95-97%)
- ❌ Slower training (hours vs. minutes)
- ❌ Requires shapelet length tuning

### Alternative 2: tsfresh + XGBoost (If Custom Features Needed)

**When to use**: If domain experts have specific QRS/QT interval features to include

```python
from tsfresh import extract_features, select_features
from xgboost import XGBClassifier

# Extract 794 statistical features
features = extract_features(ecg_df, column_id='beat_id', column_sort='time')

# Add custom clinical features
features['QT_interval'] = calculate_qt_interval(ecg_df)
features['heart_rate_variability'] = calculate_hrv(ecg_df)

# Train XGBoost
clf = XGBClassifier()
clf.fit(features, y_train)
```

**Trade-offs**:
- ✅ Can integrate custom clinical features
- ✅ Feature importance for interpretability
- ❌ Slower real-time inference (feature extraction bottleneck)
- ❌ Risk of overfitting with 800+ features on small dataset

## Cost/Benefit Analysis

### Implementation Costs
- **Engineering**: 2 ML engineers × 6 weeks = $60K
- **Clinical validation**: 2 cardiologists × 40 hours = $20K
- **Compute**: CPU sufficient, $5K (on-premise server)
- **FDA clearance** (if selling to other hospitals): $100K-500K (out of scope for internal deployment)
- **Total**: $85K (internal use)

### Annual Benefits (per 50-bed ICU)
- **Nursing labor**: 3 hours/day × 10 nurses × $50/hour × 365 days = $550K/year
- **Adverse event reduction**: 6% fewer missed events × 5 events/year × $100K average = $30K/year
- **Total**: $580K/year

### ROI
- **Year 1**: -$85K + $580K = $495K
- **Payback**: 1.7 months
- **3-Year NPV**: $1.4M

## Success Metrics

### Clinical Validation (Months 1-3)
- Retrospective testing on MIT-BIH: Target 98%+ sensitivity, 95%+ specificity
- Prospective testing on 10 patients: Cardiologist review of all alerts
- Inter-rater reliability: Compare classifier to 2 independent cardiologists

### Deployment Metrics (Months 4-6)
- False alarm rate: Target <20% (vs. 90% baseline)
- Time-to-alert: <2 seconds from arrhythmia onset
- Nursing feedback survey: "Do you trust these alerts?" >4/5 average

## Implementation Gotchas

### Gotcha 1: Imbalanced Classes
**Problem**: VF/VT are rare (0.1% of beats), model predicts "normal" for everything
**Solution**: Use class weights in ROCKET, or SMOTE oversampling for minority classes

### Gotcha 2: Patient-Specific Variations
**Problem**: Baseline ECG varies by patient (pacemakers, bundle branch blocks)
**Solution**: Fine-tune model per patient after 1 hour of data, or use patient demographics as features

### Gotcha 3: Lead Placement Artifacts
**Problem**: Poor lead placement causes waveform distortions that confuse classifier
**Solution**: Train on "artifact" class, include signal quality index (SQI) check before classification

### Gotcha 4: Regulatory Compliance
**Problem**: Medical device regulation requires extensive validation
**Solution**: Deploy as "clinical decision support" (CDS) not "diagnostic device" to avoid FDA clearance for internal use

## Production Deployment Checklist

- [ ] **Integration**: HL7/FHIR feed from patient monitors → preprocessing → sktime → alert system
- [ ] **Latency**: <2 second end-to-end (monitor → alert)
- [ ] **Audit trail**: Log all classifications + confidence scores (for liability)
- [ ] **Failover**: Automatic fallback to rule-based alarms if ML service fails
- [ ] **Dashboards**: Real-time view of all patient statuses, alert history
- [ ] **Model monitoring**: Daily check of prediction distribution (detect data drift)
- [ ] **Clinical review**: Weekly chart review by cardiologist (catch any misses)
- [ ] **Retraining**: Quarterly retraining on new labeled data

## References

- sktime ROCKET: Dempster et al. (2020) - "ROCKET: Exceptionally fast and accurate time series classification using random convolutional kernels"
- ECG classification benchmarks: UCR Time Series Archive, MIT-BIH Arrhythmia Database
- Clinical deployment: Ribeiro et al. (2020) - "Automatic diagnosis of the 12-lead ECG using a deep neural network"
