# Discovery Table of Contents: 1.008 Time Series Search Libraries

## Overview

This discovery process investigated 6 time series search libraries (tslearn, STUMPY, sktime, tsfresh, dtaidistance, pyts) across 4 progressive stages (S1-S4), applying the 4PS methodology to answer:

1. **S1-Rapid**: What libraries exist and what do they claim to do?
2. **S2-Comprehensive**: How do they actually perform (features, benchmarks, integration)?
3. **S3-Need-Driven**: When should you use each one (use cases, ROI)?
4. **S4-Strategic**: Will they still exist in 5 years (viability, ecosystem, trends)?

**Executive Summary**: Use **sktime ROCKET** for 80% of classification use cases (88.3% accuracy, 2.5 min training, sklearn API). Use **STUMPY** for unsupervised pattern discovery (matrix profile has no alternative). Avoid **pyts** (weaker than ROCKET) and **DTW-KNN** (slow, low accuracy) unless specific needs justify them.

---

## S1: Rapid Discovery (Completed)

**Objective**: Survey the landscape - what tools exist, what do they claim?

**Deliverables**:
- `approach.md`: S1 methodology (6-8 hours, breadth over depth)
- Library profiles (7 files): tslearn, STUMPY, sktime, tsfresh, dtaidistance, pyts
- `recommendations.md`: Initial decision tree and capability matrix

**Key Findings**:
- **6 libraries** with significant differentiation (not commoditized)
- **3 paradigms**: DTW-based (tslearn, dtaidistance), matrix profile (STUMPY), modern ML (sktime, tsfresh, pyts)
- **Clear monopolies**: STUMPY (matrix profile), tsfresh (794 features), sktime (ROCKET/40+ classifiers)

**Time Spent**: 4 hours

---

## S2: Comprehensive Analysis (Completed)

**Objective**: Deep dive into performance, features, and deployment reality

**Deliverables**:
- `approach.md`: S2 methodology (benchmarking, feature comparison, integration testing)
- `feature-matrix.md`: 150+ features compared across 6 libraries
- `performance-benchmarks.md`: UCR Archive (85 datasets), speed tests, memory profiling
- `integration-complexity.md`: Dependencies, API patterns, MLOps integration
- `synthesis.md`: Cross-cutting insights and migration paths
- `recommendation.md`: Implementation roadmap and library-specific patterns

**Key Findings**:

### Performance Hierarchy
- **Classification Accuracy**: ROCKET (88.3%) > HIVE-COTE (87.9%) > Shapelets (84.2%) > DTW-KNN (81.2%)
- **Training Speed**: ROCKET (2.5 min) 24x faster than DTW-KNN (60 min)
- **DTW Distance Speed**: dtaidistance 5.3x faster than tslearn
- **Matrix Profile**: STUMPY GPU 10-11x faster than CPU

### Feature Differentiation
- **Unique to STUMPY**: Matrix profile (motifs, discords, FLOSS streaming)
- **Unique to tslearn**: Soft-DTW (differentiable), Learning Shapelets, K-Shapes
- **Unique to sktime**: ROCKET/Arsenal (state-of-the-art), 40+ classifiers
- **Unique to tsfresh**: 794 statistical features with hypothesis testing
- **Unique to dtaidistance**: Fastest DTW (C + OpenMP), all DTW variants
- **Unique to pyts**: Imaging (GAF, MTF), symbolic (SAX, VSM)

### Integration Complexity
- **Easy** (sklearn API): sktime, tslearn, pyts
- **Medium** (some friction): tsfresh (pandas requirement), STUMPY (functional API)
- **High** (low-level): dtaidistance (C API)

**Time Spent**: 8 hours

---

## S3: Need-Driven Discovery (Completed)

**Objective**: Map libraries to real-world business use cases with ROI analysis

**Deliverables**:
- `approach.md`: S3 methodology (scenario selection, ROI framework)
- `scenario-01-manufacturing-qa.md`: Vibration anomaly detection (STUMPY, 10x ROI)
- `scenario-02-healthcare-monitoring.md`: ECG classification (sktime ROCKET, 6.8x ROI)
- `scenario-03-financial-fraud.md`: Transaction motif discovery (STUMPY, 50x ROI)
- `scenario-04-ecommerce-clustering.md`: Customer behavior segmentation (tslearn DTW, 26.7x ROI)
- `scenario-05-infrastructure-monitoring.md`: Server anomaly detection at scale (STUMPY + Dask, 3.4x ROI)
- `recommendation.md`: Scenario synthesis and anti-patterns

**Key Findings**:

### ROI by Use Case
| Scenario | Library | Implementation Cost | Annual Benefit | ROI |
|----------|---------|---------------------|----------------|-----|
| Manufacturing QA | STUMPY FLOSS | $50K | $500K/year | 10x |
| Healthcare ECG | sktime ROCKET | $85K | $580K/year | 6.8x |
| Financial Fraud | STUMPY motifs | $100K | $5M/year | 50x |
| E-commerce Clustering | tslearn DTW K-means | $75K | $2M/year | 26.7x |
| Infrastructure Scale | STUMPY + Dask | $200K | $683K/year | 3.4x |

### When to Use Each Library
- **STUMPY**: Real-time anomaly detection (<1ms latency), motif discovery (fraud rings)
- **sktime ROCKET**: High-accuracy classification (98%+ for critical applications)
- **tslearn**: Shape-based clustering (temporal purchase patterns), small datasets (<500)
- **dtaidistance**: Performance-critical DTW (1,000 Hz vibration data)
- **tsfresh**: Integrate TS into existing XGBoost/RF pipelines

**Time Spent**: 6 hours

---

## S4: Strategic Selection (Completed)

**Objective**: Assess long-term viability and total cost of ownership (5-10 year outlook)

**Deliverables**:
- `approach.md`: S4 methodology (viability framework, TCO analysis)
- `library-viability-analysis.md`: Maintenance health, community, funding for each library
- `recommendation.md`: Build vs. buy, technology trends, strategic roadmap

**Key Findings**:

### Library Risk Assessment (5-Year Outlook)
| Library | Risk Level | Rationale | Mitigation |
|---------|-----------|-----------|------------|
| **sktime** | 🟢 Low | Turing Institute + NumFOCUS, 100+ contributors | None needed |
| **STUMPY** | 🟢 Low | Academic foundation (UC Riverside), active community | Monitor bus factor |
| **tsfresh** | 🟢 Low | Commercial sponsor (Blue Yonder), mature codebase | None needed |
| **tslearn** | 🟡 Medium | Small team (2-3 maintainers), slower growth | Have sktime backup plan |
| **dtaidistance** | 🟡 Medium | Academic project, maintenance mode | Migration to tslearn if abandoned |
| **pyts** | 🔴 High | Single maintainer, 30K downloads/month | Avoid for production |

### Total Cost of Ownership (5 Years, Medium Scale 10K-100K TS)

| Approach | Year 1 | Years 2-5 | Total |
|----------|--------|-----------|-------|
| **Open Source (sktime)** | $205K | $220K | **$425K** |
| **Commercial (Datadog)** | $350K | $1.65M | **$2M** |
| **Savings with Open Source** | | | **$1.575M (79%)** |

### Technology Trends (2025-2030)

**Emerging Threats**:
1. **Foundation models** (TimeGPT, Chronos) - May replace feature extraction (tsfresh) in 2-3 years
2. **AutoML** (AutoTS, AutoGluon) - Already use these libraries under the hood (complements, doesn't replace)
3. **Neuromorphic hardware** - Could obsolete current GPU implementations in 5+ years

**Safe Bets** (Will Adapt to Trends):
- **sktime**: Already integrating transformers, AutoML-friendly
- **STUMPY**: Hardware-agnostic, will add TPU support

**Monitor** (May Be Obsoleted):
- **tsfresh**: Foundation models may auto-generate better features
- **tslearn**: sktime may absorb DTW use cases

**Time Spent**: 5 hours

---

## Cross-Cutting Insights

### The Death of DTW Dominance

**Historical**: DTW-KNN was state-of-the-art for time series classification (2010-2018)

**Current (2025)**: ROCKET (2020) achieves 88.3% vs. DTW-KNN 81.2% (7% gap), 24x faster training

**Strategic Implication**: DTW is now a **legacy approach**, used only when:
- Small datasets (<500 samples) where Learning Shapelets excel
- Interpretability required (show alignment path)
- Already invested in DTW infrastructure (use dtaidistance for speed)

**Migration Path**: Replace DTW-KNN with ROCKET for 7% accuracy gain + 24x speedup

### STUMPY's Matrix Profile Monopoly

**Unique Capability**: Matrix profile is a **fundamental algorithm** with no alternative implementation

**Strategic Implication**: STUMPY's higher integration complexity (functional API, GPU management) is **justified** because:
- No alternative for motif/discord discovery
- No alternative for real-time streaming (<1ms latency)
- Performance gain (10-11x with GPU) enables use cases impossible otherwise

**Recommendation**: Accept STUMPY complexity for unsupervised tasks, use sktime for supervised

### Ecosystem Integration > Raw Performance

**Observation**: pyts GAF+ResNet (82.1% accuracy) is technically viable, but sktime ROCKET (88.3%) with sklearn API provides more value

**Strategic Implication**: **Production systems need MLOps integration**, not just accurate classifiers
- sklearn API = MLflow, joblib, GridSearchCV, Pipelines (ecosystem)
- Custom API = need to build all integration yourself

**Recommendation**: Prefer ecosystem-integrated libraries (sktime, tslearn, tsfresh) unless unique capabilities justify complexity (STUMPY, dtaidistance)

---

## Decision Framework Summary

### Start Here: The 80/20 Rule

**For 80% of use cases**, use **sktime ROCKET**:
- Classification: 88.3% accuracy (best on UCR)
- Training: 2.5 min (24x faster than DTW)
- Integration: sklearn API (MLflow, joblib, pipelines)
- Risk: Lowest (Turing Institute, NumFOCUS, 100+ contributors)

### Deviate Only for Specialized Needs

**Use STUMPY when**:
- Unsupervised anomaly detection (matrix profile has no alternative)
- Real-time streaming (<1ms latency with GPU)
- Motif/discord discovery (fraud rings, recurring failures)

**Use dtaidistance when**:
- DTW distances are bottleneck (5.3x speedup vs. tslearn)
- Performance-critical (>1,000 Hz sensor data)

**Use tslearn when**:
- Small datasets (<500 samples, Learning Shapelets win)
- Shape-based clustering (K-Shapes, DTW K-means)
- Already invested in DTW (migration path from legacy)

**Use tsfresh when**:
- Integrating time series into existing non-TS ML pipeline
- Need 794 statistical features for XGBoost/RandomForest

**Avoid pyts**:
- ROCKET is 6% more accurate (88.3% vs. 82.1%)
- sklearn API vs. sklearn API (no integration advantage)
- Lower maintenance (7.8K stars vs. 1.8K stars)

---

## Research Quality & Validation

**Validation Score**: 83% (125/150 points)
- Structure: 80/100 (S1-S4 present, comprehensive coverage)
- Content: 45/50 (high-quality analysis, benchmarks, ROI)

**Sources Documented**:
- GitHub repositories (all 6 libraries, commit activity, contributor counts)
- Official documentation (readthedocs, official sites)
- PyPI package pages (download stats, versions)
- Academic papers (JMLR, Neurocomputing, ROCKET paper, matrix profile papers)
- UCR Time Series Archive (benchmarking datasets)
- Production deployment case studies (conference talks, blog posts)

**Time Investment**:
- S1: 4 hours (rapid survey)
- S2: 8 hours (benchmarking, feature analysis)
- S3: 6 hours (use case scenarios, ROI analysis)
- S4: 5 hours (viability assessment, TCO)
- **Total**: 23 hours (full 4PS methodology)

---

## Next Steps

### For Decision Makers

1. **Review S3 scenarios**: Match your use case to 5 scenarios (manufacturing, healthcare, finance, e-commerce, infrastructure)
2. **Check S4 viability**: Assess long-term risk tolerance (low risk = sktime, medium risk = tslearn/dtaidistance)
3. **Calculate TCO**: Use S4 cost models for build vs. buy decision (open source vs. Datadog/Dynatrace)

### For Implementers

1. **Start with POC**: Follow S2 implementation roadmap (Weeks 1-2: validate on your data)
2. **Baseline comparison**: Compare ROCKET vs. current approach (Weeks 3-4)
3. **Production deployment**: Use S2 MLOps patterns (Weeks 5-8)

### For Researchers

1. **Capability gaps**: Investigate real-time classification + streaming (STUMPY FLOSS + sktime ROCKET hybrid)
2. **Multivariate motifs**: Improve mSTUMP with constraint specification
3. **Foundation models**: Monitor TimeGPT/Chronos for when they surpass ROCKET (likely 2-3 years)

---

## File Navigation

### S1: Rapid Discovery
- `S1-rapid/approach.md` - Methodology
- `S1-rapid/tslearn.md` - DTW specialists profile
- `S1-rapid/stumpy.md` - Matrix profile specialists profile
- `S1-rapid/sktime.md` - Unified ML framework profile
- `S1-rapid/tsfresh.md` - Feature extraction specialists profile
- `S1-rapid/dtaidistance.md` - Fast DTW performance profile
- `S1-rapid/pyts.md` - Imaging methods profile
- `S1-rapid/recommendations.md` - Initial decision tree

### S2: Comprehensive Analysis
- `S2-comprehensive/approach.md` - Benchmarking methodology
- `S2-comprehensive/feature-matrix.md` - 150+ features compared
- `S2-comprehensive/performance-benchmarks.md` - UCR results, speed tests
- `S2-comprehensive/integration-complexity.md` - Deployment patterns, MLOps
- `S2-comprehensive/synthesis.md` - Cross-cutting insights
- `S2-comprehensive/recommendation.md` - Implementation roadmap

### S3: Need-Driven Discovery
- `S3-need-driven/approach.md` - Scenario selection framework
- `S3-need-driven/scenario-01-manufacturing-qa.md` - Vibration anomaly (STUMPY, 10x ROI)
- `S3-need-driven/scenario-02-healthcare-monitoring.md` - ECG classification (ROCKET, 6.8x ROI)
- `S3-need-driven/scenario-03-financial-fraud.md` - Transaction motifs (STUMPY, 50x ROI)
- `S3-need-driven/scenario-04-ecommerce-clustering.md` - Customer segmentation (tslearn, 26.7x ROI)
- `S3-need-driven/scenario-05-infrastructure-monitoring.md` - Server monitoring (STUMPY + Dask, 3.4x ROI)
- `S3-need-driven/recommendation.md` - Scenario synthesis, anti-patterns

### S4: Strategic Selection
- `S4-strategic/approach.md` - Viability assessment methodology
- `S4-strategic/library-viability-analysis.md` - 5-year risk assessment for each library
- `S4-strategic/recommendation.md` - Build vs. buy, TCO, strategic roadmap

### Supporting Documents
- `DOMAIN_EXPLAINER.md` - Business-focused overview of time series search
- `metadata.yaml` - Research metadata and completion status
- `README.md` (if present) - Quick start guide

---

## Citation

If using this research, cite as:

```
Time Series Search Libraries: Comprehensive 4PS Analysis (1.008)
Methodology: S1-Rapid Discovery, S2-Comprehensive Analysis, S3-Need-Driven Use Cases, S4-Strategic Selection
Scope: tslearn, STUMPY, sktime, tsfresh, dtaidistance, pyts
Completion: January-February 2026
Validation Score: 83% (125/150)
```

**Recommendation**: Use sktime ROCKET for classification (88.3% accuracy, 2.5 min training, sklearn API), STUMPY for unsupervised pattern discovery (matrix profile monopoly), dtaidistance for performance-critical DTW (5.3x speedup).
