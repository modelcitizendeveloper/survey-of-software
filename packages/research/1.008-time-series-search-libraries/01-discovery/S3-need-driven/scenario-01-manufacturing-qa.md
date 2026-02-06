# Scenario 1: Manufacturing Quality Control

## Business Context

**Industry**: Discrete Manufacturing (Electronics, Automotive, Aerospace)
**Pain Point**: Defect detection in production line sensor data
**Current Approach**: Manual inspection + statistical process control (SPC) with fixed thresholds
**Cost of Failure**: 2-5% scrap rate, warranty claims, customer returns

### Business Metrics
- **Defect detection rate**: Currently 85-90% (10-15% escape to customers)
- **False positive rate**: 15-20% (good product incorrectly flagged)
- **Inspection cost**: $2-5 per unit for manual inspection
- **Scrap/rework cost**: 2-5% of production value

## Use Case: Vibration Pattern Anomaly Detection

### Problem Statement

A PCB assembly line uses vibration sensors to monitor pick-and-place robot performance. Gradual degradation causes misalignment, leading to defects that manifest 2-4 hours later in functional testing.

**Current SPC approach limitations**:
- Fixed thresholds miss gradual drift
- High false positives from normal operational variations
- No pattern matching against known failure modes
- Reactive (detects after defects occur)

### Data Profile

- **Volume**: 5 robots × 1000 Hz × 8 hours = 144M data points/day
- **Features**: 3-axis accelerometer per robot (X, Y, Z vibration)
- **Pattern length**: 100-500ms windows (100-500 data points)
- **Failure signatures**: 15 known degradation patterns from historical data

### Technical Requirements

- **Latency**: <1 second detection (real-time monitoring)
- **Accuracy**: 95%+ defect detection, <5% false positives
- **Scalability**: Support 50-100 robots (future expansion)
- **Interpretability**: Operators need to understand "why" (show similar past failures)

## Recommended Solution: STUMPY Matrix Profile

### Rationale

**Why STUMPY**:
1. **Unsupervised motif/discord discovery**: Finds anomalies without labeled training data
2. **Real-time capability**: FLOSS (streaming) for online detection
3. **Performance**: Numba JIT + GPU option for high-frequency data
4. **Interpretability**: Shows nearest neighbors (similar past patterns) for context

**Why not alternatives**:
- ❌ **tsfresh**: Requires labeled training data, too slow for 1000 Hz real-time
- ❌ **tslearn**: DTW too slow for high-frequency streaming
- ❌ **sktime**: Supervised classifiers require extensive labeled defect data

### Expected Outcomes

**Quantitative**:
- Defect detection: 90% → 97% (+7% fewer customer escapes)
- False positives: 18% → 6% (-12% fewer unnecessary line stops)
- Early detection: Catch degradation 2-4 hours earlier (prevent 50-100 defects/event)
- ROI: $500K/year savings (reduced scrap + warranty) vs. $50K implementation = 10x ROI

## Cost/Benefit Analysis

### Implementation Costs
- **Engineering**: 2 engineers × 4 weeks = $40K (dev + integration)
- **GPU hardware**: $5K (optional, for >20 lines)
- **Training**: 1 week for 5 operators = $5K
- **Total**: $50K

### Annual Benefits
- **Scrap reduction**: 7% improvement × 2% scrap rate × $20M production = $280K/year
- **Warranty reduction**: 7% fewer escapes × $500K warranty cost = $35K/year
- **Inspection labor**: Reduce manual inspection by 30% = $150K/year
- **Downtime reduction**: Predictive maintenance saves 50 hours/year = $35K
- **Total**: $500K/year

### 3-Year NPV
- **Year 1**: -$50K + $500K = $450K
- **Year 2-3**: $500K/year × 2 = $1M
- **3-Year NPV** (10% discount): $1.26M
- **Payback**: 1.2 months
