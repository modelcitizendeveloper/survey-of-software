# Scenario 5: Infrastructure Monitoring at Scale

## Business Context

**Industry**: SaaS, Cloud Infrastructure, DevOps
**Pain Point**: Real-time anomaly detection in server/application metrics
**Current Approach**: Static thresholds + rule-based alerts
**Cost**: Alert fatigue (10K+ alerts/day, 98% false positives), missed outages

## Use Case: Real-Time Anomaly Detection for 10K+ Servers

### Problem Statement

Microservices architecture with 10,000+ containers generates millions of metrics per minute (CPU, memory, latency, error rates). Static thresholds create noise (false alarms during load spikes) or miss real issues (gradual degradation).

Need context-aware anomaly detection that:
- Understands normal daily/weekly patterns
- Detects novel failure modes (never-seen-before issues)
- Scales to millions of time series
- Provides <10 second alerting latency

### Data Profile

- **Volume**: 10K servers × 50 metrics × 1 sample/minute = 500K data points/minute
- **Pattern types**: Daily cycles, weekly trends, sudden spikes, gradual drift
- **History**: 90 days retention for baseline (6.5B data points)
- **Latency requirement**: <10 seconds from anomaly to alert

## Recommended Solution: STUMPY with Dask for Scale

### Rationale

**Why STUMPY + Dask**:
1. **Scalability**: Dask parallelizes matrix profile across 10K time series
2. **Unsupervised**: No training data needed (infrastructure changes constantly)
3. **Discord discovery**: Finds "most unusual" patterns in each metric
4. **Real-time streaming**: FLOSS for live anomaly detection

```python
import stumpy
import dask
import dask.array as da

# Offline: Build historical baselines (daily job)
def build_baseline(server_metrics):
    """Process 10K servers in parallel with Dask"""
    metrics_dask = da.from_delayed(server_metrics, shape=(10000, 129600, 50))  # 90 days, 1min intervals
    baselines = {}

    for server_id in range(10000):
        server_data = metrics_dask[server_id]
        # Compute matrix profile for each metric
        mp = stumpy.stump(server_data, m=1440)  # 24-hour patterns
        baselines[server_id] = {'mp': mp, 'mean': server_data.mean(), 'std': server_data.std()}

    return baselines

baselines = dask.compute(build_baseline(historical_data))[0]

# Online: Streaming anomaly detection
from stumpy import floss

for server_id, metric_stream in live_metrics():
    # Compare live data to historical baseline
    stream_mp = floss(
        metric_stream,
        m=1440,  # 24-hour windows
        historic=baselines[server_id]['historical'],
        egress=True
    )

    for distance, pattern in stream_mp:
        z_score = (distance - baselines[server_id]['mean']) / baselines[server_id]['std']

        if z_score > 4:  # 4 sigma = very unusual
            # Alert with context
            similar_past_incidents = find_similar_patterns_in_incident_db(pattern)
            alert(
                server=server_id,
                severity='HIGH',
                pattern=pattern,
                similar_incidents=similar_past_incidents,
                anomaly_score=z_score
            )
```

### Architecture

**Components**:
1. **Metrics collection**: Prometheus/Datadog → Time series DB (InfluxDB)
2. **Baseline computation**: Daily Dask job (compute 10K matrix profiles)
3. **Streaming detection**: FLOSS running on 10-20 worker nodes
4. **Alert aggregation**: Dedupe correlated alerts (same root cause)
5. **Incident DB**: Store all alerts + resolution notes (for similarity search)

### Performance Optimization

**Baseline computation** (daily):
- **Single-threaded**: 10K servers × 2 minutes = 333 hours (infeasible)
- **Dask (20 nodes)**: 333 hours / 20 = 16.7 hours (overnight batch)
- **With GPU-STUMP**: 16.7 hours / 10 = 1.7 hours (acceptable)

**Streaming detection**:
- **Latency**: 2-5 seconds per metric update (FLOSS incremental)
- **Throughput**: 500K metrics/minute = 8.3K/second
- **Worker requirement**: 8.3K / 1K per worker = 8-10 worker nodes

### Expected Outcomes

- **Alert volume**: 10K alerts/day → 50 alerts/day (-99.5% noise)
- **True positive rate**: 15% → 85% (+70% more relevant alerts)
- **Time to detection**: 15 minutes → 30 seconds (-97% faster)
- **Missed outages**: 2-3/month → 0-1/month (-67% misses)

### ROI

- **Implementation cost**: $200K (4 months, 3 engineers + Dask cluster)
- **Annual savings**:
  - On-call engineer time: 5 hours/day × $100/hour × 365 = $183K
  - Avoided downtime: 50 hours/year × $10K/hour = $500K
  - Total: $683K/year
- **Payback**: 3.5 months

## Alternative: Prophet + Isolation Forest

**When to use**: If you prefer statistical forecasting for anomaly detection

```python
from fbprophet import Prophet
from sklearn.ensemble import IsolationForest
import pandas as pd

# Train Prophet on each metric to learn normal patterns
for server_id in servers:
    metrics_df = load_metrics(server_id)  # columns: ds (timestamp), y (metric value)

    # Fit Prophet (captures daily/weekly seasonality)
    model = Prophet(daily_seasonality=True, weekly_seasonality=True)
    model.fit(metrics_df)

    # Forecast next hour
    future = model.make_future_dataframe(periods=60, freq='1min')
    forecast = model.predict(future)

    # Real-time: Compare actual to forecast
    actual = get_live_metric(server_id)
    expected = forecast['yhat'].iloc[-1]
    uncertainty = forecast['yhat_upper'].iloc[-1] - forecast['yhat_lower'].iloc[-1]

    if abs(actual - expected) > 3 * uncertainty:
        alert(server=server_id, actual=actual, expected=expected)
```

**Trade-offs**:
- ✅ Easier to understand (forecast vs. actual)
- ✅ Less compute than matrix profile
- ❌ Doesn't find novel patterns (only deviations from forecast)
- ❌ Requires per-metric tuning (seasonality periods)
- ❌ Slower to adapt to changing patterns

## Implementation Gotchas

### Gotcha 1: Alert Correlation
**Problem**: 50 servers fail simultaneously (shared dependency), get 50 alerts
**Solution**: Use topology graph to group correlated failures (1 root cause alert)

### Gotcha 2: Baseline Staleness
**Problem**: Infrastructure changes invalidate old baselines (new deployment, autoscaling)
**Solution**: Incremental baseline updates (exponential moving average of matrix profiles)

### Gotcha 3: Cold Start
**Problem**: New servers have no historical baseline
**Solution**: Use fleet-wide baseline initially, personalize after 7 days of data

### Gotcha 4: Metric Correlation
**Problem**: High CPU and high memory are correlated, get duplicate alerts
**Solution**: Use mSTUMP (multidimensional matrix profile) to detect joint anomalies

## Success Metrics

- **Alert volume**: <100 alerts/day (vs. 10K baseline)
- **Alert precision**: >80% (alerts lead to action)
- **Mean time to detection (MTTD)**: <1 minute
- **Mean time to resolution (MTTR)**: -30% (better context from similar incidents)
- **On-call satisfaction**: >4/5 ("alerts are actionable")

## Production Deployment Checklist

- [ ] **Dask cluster**: 20 nodes for baseline computation, 10 for streaming
- [ ] **GPU nodes**: 5 nodes with NVIDIA T4 (optional, 10x baseline speedup)
- [ ] **Storage**: InfluxDB for 90-day metric history (6.5B points = ~500GB compressed)
- [ ] **Monitoring**: Dashboard showing STUMPY service health, alert rates, latency
- [ ] **Incident DB**: Elasticsearch for similarity search on historical alerts
- [ ] **Integration**: PagerDuty/Slack for alert delivery
- [ ] **Runbook**: Automated incident response for common patterns
- [ ] **Feedback loop**: On-call engineers mark false positives (retrain thresholds)

## References

- STUMPY at scale: Law (2019) - "STUMPY: A Powerful and Scalable Python Library for Time Series Data Mining"
- Dask for parallel matrix profile: https://stumpy.readthedocs.io/en/latest/Tutorial_STUMPY_Basics.html#parallel-computation-with-dask
- Infrastructure anomaly detection: Vallis et al. (2014) - "A Novel Technique for Long-Term Anomaly Detection in the Cloud" (Twitter's approach)
