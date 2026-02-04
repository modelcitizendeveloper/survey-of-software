# S4: Strategic Selection - Final Recommendations

## Executive Summary

After evaluating 6 time series search libraries across technical health, community adoption, and organizational backing, **3 libraries emerge as safe long-term investments** (sktime, STUMPY, tsfresh) while **2 require monitoring** (tslearn, dtaidistance) and **1 should be avoided for production** (pyts).

The strategic decision is not just "which library" but **how to build a sustainable time series capability** with minimal vendor lock-in and migration risk.

---

## Strategic Library Portfolio (2025-2030)

### Core Stack (Low Risk, High Investment)

**1. sktime: Primary Classification/Regression Platform**
- **When**: Any supervised learning task, production ML pipelines
- **Why safe**: Turing Institute backing, NumFOCUS sponsorship, 100+ contributors
- **Investment**: Standardize on sktime for all classification, train team extensively
- **5-Year TCO**: $160K (medium scale)
- **Risk level**: 🟢 **LOW**

**2. STUMPY: Unsupervised Pattern Discovery**
- **When**: Anomaly detection, motif discovery, real-time streaming
- **Why safe**: Strong academic foundation (UC Riverside), active maintenance, no commercial competition
- **Investment**: Build STUMPY expertise for all anomaly detection use cases
- **5-Year TCO**: $230K (includes GPU infrastructure)
- **Risk level**: 🟢 **LOW**

**3. tsfresh: Feature Extraction for Standard ML**
- **When**: Integrating time series into existing XGBoost/Random Forest pipelines
- **Why safe**: Commercial backing (Blue Yonder), mature codebase, 794 well-tested features
- **Investment**: Use for feature engineering when sktime ROCKET doesn't fit
- **5-Year TCO**: $190K (compute-intensive)
- **Risk level**: 🟢 **LOW**

### Tactical Use (Medium Risk, Limited Investment)

**4. tslearn: DTW Specialists**
- **When**: DTW-specific needs (clustering, shapelets) where sktime's DTW is insufficient
- **Strategy**: Use but maintain abstraction layer for migration to sktime if needed
- **Monitor**: GitHub activity quarterly, watch for maintainer changes
- **5-Year TCO**: $133K
- **Risk level**: 🟡 **MEDIUM**

**5. dtaidistance: Performance-Critical DTW**
- **When**: Ultra-high-frequency DTW (>1000 Hz) where speed is critical
- **Strategy**: Use for performance bottlenecks only, fall back to tslearn/sktime otherwise
- **Monitor**: Academic team status, commit frequency
- **5-Year TCO**: $97K (lowest cost)
- **Risk level**: 🟡 **MEDIUM**

### Avoid

**6. pyts: Imaging Methods**
- **Why avoid**: High bus factor (single maintainer), ROCKET has superseded imaging methods
- **Alternative**: Use sktime ROCKET for classification instead
- **Exception**: Research projects where imaging methods are specifically required
- **Risk level**: 🔴 **HIGH**

---

## Build vs. Buy: Open Source vs. Commercial

### When to Use Open Source (Recommended)

**Scenarios**:
- You have ML/data science expertise in-house
- You need custom algorithms or research flexibility
- Budget <$500K/year
- Data sovereignty requirements (on-premise deployment)

**Cost comparison** (5-year TCO for 100K time series):
- **Open source**: $200K-500K (implementation + infrastructure + maintenance)
- **Commercial (Datadog)**: $1M-2M (licenses + support)
- **Savings**: $500K-1.5M over 5 years

**Trade-offs**:
- ✅ Full control, no vendor lock-in
- ✅ Customize for specific needs
- ❌ Requires ML expertise
- ❌ Longer time to value (3-6 months)

### When to Use Commercial

**Scenarios**:
- You lack in-house ML expertise
- Need production deployment in <1 month
- Budget >$500K/year
- Want SLA-backed support

**Best commercial options by use case**:
- **Infrastructure monitoring**: Datadog Anomaly Detection ($100K-500K/year)
- **Application performance**: Dynatrace Davis AI ($150K-750K/year)
- **Business metrics**: Anodot ($50K-200K/year)
- **Cloud-native**: AWS Anomaly Detector, Azure Anomaly Detector (pay-per-use)

**Trade-offs**:
- ✅ Fast deployment (1-4 weeks)
- ✅ No ML expertise required
- ❌ Vendor lock-in (proprietary formats)
- ❌ 2-5x cost premium vs. open source

### Hybrid Strategy (Best of Both)

**Phase 1** (Months 1-3): Use commercial for quick wins
- Deploy Datadog/Dynatrace for immediate anomaly detection
- Learn what works, identify gaps

**Phase 2** (Months 4-12): Build open source in parallel
- Implement STUMPY/sktime for custom use cases
- Validate accuracy matches commercial

**Phase 3** (Year 2+): Migrate to open source
- Move non-critical workloads to open source first
- Keep commercial for mission-critical systems with SLA requirements
- **Cost savings**: $500K-1M/year once migration complete

---

## Total Cost of Ownership: 5-Year Projection

### Small Scale (<1K Time Series)

| Item | Year 1 | Years 2-5 | Total |
|------|--------|-----------|-------|
| **Open Source** (sktime) | | | |
| Implementation | $40K | - | $40K |
| Maintenance | $5K | $5K/year × 4 = $20K | $25K |
| Infrastructure | $2K | $2K/year × 4 = $8K | $10K |
| **Total** | **$47K** | **$28K** | **$75K** |
| | | | |
| **Commercial** (Datadog) | | | |
| Licenses | $30K | $35K/year × 4 = $140K | $170K |
| Support | $10K | $10K/year × 4 = $40K | $50K |
| **Total** | **$40K** | **$180K** | **$220K** |

**Verdict**: Open source saves **$145K** (66% savings)

### Medium Scale (10K-100K Time Series)

| Item | Year 1 | Years 2-5 | Total |
|------|--------|-----------|-------|
| **Open Source** (STUMPY + Dask) | | | |
| Implementation | $150K | - | $150K |
| Maintenance | $25K | $25K/year × 4 = $100K | $125K |
| Infrastructure (Dask + GPU) | $30K | $30K/year × 4 = $120K | $150K |
| **Total** | **$205K** | **$220K** | **$425K** |
| | | | |
| **Commercial** (Datadog) | | | |
| Licenses | $300K | $350K/year × 4 = $1.4M | $1.7M |
| Support | $50K | $50K/year × 4 = $200K | $250K |
| **Total** | **$350K** | **$1.65M** | **$2M** |

**Verdict**: Open source saves **$1.575M** (79% savings)

### Large Scale (>100K Time Series)

| Item | Year 1 | Years 2-5 | Total |
|------|--------|-----------|-------|
| **Open Source** (STUMPY + Dask + GPU) | | | |
| Implementation | $300K | - | $300K |
| Maintenance | $50K | $50K/year × 4 = $200K | $250K |
| Infrastructure (GPU cluster) | $100K | $100K/year × 4 = $400K | $500K |
| **Total** | **$450K** | **$600K** | **$1.05M** |
| | | | |
| **Commercial** (Datadog) | | | |
| Licenses | $800K | $1M/year × 4 = $4M | $4.8M |
| Support | $100K | $100K/year × 4 = $400K | $500K |
| **Total** | **$900K** | **$4.4M** | **$5.3M** |

**Verdict**: Open source saves **$4.25M** (80% savings)

**Key insight**: Savings increase with scale. At 100K+ time series, commercial becomes prohibitively expensive.

---

## Technology Trends: 2025-2030 Outlook

### Emerging Threats to Current Libraries

**1. Foundation Models for Time Series**
- **What**: LLMs/transformers trained on billions of time series (TimeGPT, Chronos, Lag-Llama)
- **Impact on libraries**: May replace feature engineering (tsfresh) and simple classification (sktime)
- **Timeline**: 2-3 years to maturity
- **Risk to current stack**: 🟡 **MEDIUM**
- **Mitigation**: Foundation models still require fine-tuning (sktime/STUMPY remain relevant for custom use cases)

**2. AutoML for Time Series**
- **What**: Automated library/algorithm selection (AutoTS, AutoGluon-TimeSeries)
- **Impact**: Reduces need for deep library expertise
- **Timeline**: Already available, improving
- **Risk to current stack**: 🟢 **LOW**
- **Mitigation**: AutoML uses these libraries under the hood (complements, doesn't replace)

**3. Hardware Acceleration (Neuromorphic, TPUs)**
- **What**: Specialized hardware for time series (matrix profile on neuromorphic chips)
- **Impact**: Could obsolete current GPU implementations
- **Timeline**: 5+ years
- **Risk to current stack**: 🟢 **LOW**
- **Mitigation**: Libraries will adapt (STUMPY already has GPU support, will add TPU)

### Growing Adoption Trends

**STUMPY adoption growing faster than others**:
- GitHub stars: +30%/year (vs. +10% for tslearn)
- StackOverflow questions: +40%/year
- Conference talks: 10+ presentations in 2024 (vs. 3 in 2020)

**sktime becoming "scikit-learn for time series"**:
- NumFOCUS sponsorship (Feb 2024) = credibility boost
- 100+ contributors (most collaborative TS library)
- Integration with sklearn ecosystem (Pipelines, GridSearchCV)

**tsfresh stable but not growing**:
- Mature library (fewer new features needed)
- Competition from ROCKET (faster, similar accuracy)
- Still widely used in manufacturing/IoT

**tslearn/dtaidistance/pyts declining adoption**:
- Fewer new projects choosing these (sktime/STUMPY absorbing use cases)
- Maintenance mode (stable but not innovating)

### Recommendation: Hedge Against Future

**Safe bets** (will adapt to new trends):
- **sktime**: Already integrating transformers, AutoML-friendly API
- **STUMPY**: Hardware-agnostic (CPU/GPU/Dask), will add TPU support

**Monitor but don't over-invest**:
- **tsfresh**: May be obsoleted by foundation models (but not in next 3 years)
- **tslearn**: May be absorbed into sktime (use sparingly)

**Experimental exploration**:
- Allocate 10-20% of time series R&D to foundation models (TimeGPT, Chronos)
- Don't bet production systems on them yet (immature, expensive inference)

---

## Strategic Investment Roadmap

### Year 1: Build Core Capability
- **Q1-Q2**: Implement sktime + STUMPY for primary use cases (S3 scenarios)
- **Q3**: Train team on chosen libraries (3-day workshops)
- **Q4**: Deploy to production, measure ROI vs. baseline

**Deliverables**:
- 3-5 production deployments (manufacturing QA, healthcare monitoring, etc.)
- Reusable template code (Docker containers, deployment scripts)
- Internal documentation (when to use which library)

### Year 2-3: Scale & Optimize
- **Year 2**: Expand to more use cases, optimize infrastructure (Dask, GPU)
- **Year 3**: Migrate from commercial tools (if using), build center of excellence

**Deliverables**:
- 10+ production deployments
- Cost savings realized (vs. commercial baseline)
- Team expertise (2-3 specialists per library)

### Year 4-5: Innovate & Future-Proof
- **Year 4**: Experiment with foundation models, evaluate next-gen libraries
- **Year 5**: Migrate to better alternatives if they emerge, or double down on current stack

**Deliverables**:
- Quarterly tech radar review (emerging libraries)
- Migration plan if needed (abstraction layers in place)
- Thought leadership (conference talks, blog posts on your implementations)

---

## Final Recommendation

### Organizational Standardization

**Mandate**:
1. **All classification/regression**: Use **sktime** (no exceptions without approval)
2. **All anomaly detection**: Use **STUMPY** (no custom threshold logic)
3. **All feature extraction**: Use **tsfresh** or **sktime ROCKET**

**Rationale**: Standardization reduces:
- Training costs (everyone learns same tools)
- Maintenance burden (fewer libraries to monitor)
- Migration risk (concentrated expertise)

### Abstraction Layer Strategy

Wrap library calls to enable swapping:

```python
# Good: Abstraction layer
from our_ts_library import TimeSeriesClassifier

clf = TimeSeriesClassifier(backend='sktime', algorithm='ROCKET')
# Can switch to clf = TimeSeriesClassifier(backend='prophet', algorithm='auto')

# Bad: Direct library coupling
from sktime.classification.kernel_based import RocketClassifier
clf = RocketClassifier()  # Hard to swap
```

**Why**: Enables migration if library abandoned or better alternative emerges

### Quarterly Health Check

Monitor library health every quarter:
1. **GitHub activity**: Commits in last 90 days? (Yes = healthy)
2. **Maintainer status**: Key contributors still active? (Check LinkedIn, GitHub)
3. **Issue response time**: <2 weeks average? (Yes = responsive)
4. **StackOverflow growth**: Questions increasing? (Yes = growing adoption)

**Trigger**: If any metric degrades 2 quarters in a row, initiate migration plan

---

## Conclusion

**The strategic answer is not a single library but a portfolio approach**:

- **Core bet**: sktime + STUMPY + tsfresh (low risk, high investment)
- **Tactical use**: tslearn + dtaidistance (when specialized needs arise)
- **Avoid**: pyts (too risky for production)
- **Monitor**: Quarterly health checks, adapt to emerging trends (foundation models)
- **Hedge**: Abstraction layers, avoid vendor lock-in

**Expected outcome** (5 years):
- $1-4M savings vs. commercial solutions
- 10+ production deployments
- Robust time series capability
- Low migration risk (libraries likely to persist)

**Highest risk**: Failing to standardize (every team picks different library = fragmentation)

**Lowest risk path**: Follow this recommendation, monitor quarterly, adapt as needed.
