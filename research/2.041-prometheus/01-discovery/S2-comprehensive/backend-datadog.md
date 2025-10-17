# Datadog: Observability Platform with Prometheus Integration

**Category**: Full Observability Platform (Metrics + Traces + Logs)
**Website**: https://www.datadoghq.com/
**License**: Proprietary (SaaS)
**Maturity**: Enterprise-grade (10,000+ customers)

---

## Overview

Datadog is a **full-stack observability platform** that provides metrics monitoring, distributed tracing, log management, and APM in a single product. It can **ingest Prometheus metrics** but is NOT a Prometheus-native backend.

**Key differentiator**: Full observability in one platform (convenience) vs Prometheus ecosystem (portability)

---

## Prometheus Compatibility

### Exposition Format Support
- ✅ **Ingestion only** - Can scrape Prometheus `/metrics` endpoints
- ✅ Supports OpenMetrics format (Prometheus-based)
- ✅ Datadog Agent autodiscovery for Prometheus endpoints
- ⚠️ Translates Prometheus metrics to Datadog format (one-way)

**Compatibility level**: **Ingestion: YES, Storage: NO**

### PromQL Compatibility
- ❌ **NO native PromQL support**
- ❌ Must use Datadog Query Language (DQL) instead
- ❌ Cannot execute PromQL queries in Datadog dashboards
- ⚠️ Query conversion required (PromQL → DQL)

**Lock-in impact**: **HIGH** - PromQL queries must be rewritten to DQL

---

## Integration Architecture

### How Prometheus Metrics Work in Datadog

```
App exposes /metrics (Prometheus format)
      ↓
Datadog Agent scrapes endpoint
      ↓
Translates Prometheus metrics → Datadog metrics
      ↓
Sends to Datadog backend (proprietary storage)
      ↓
Query with DQL (NOT PromQL)
```

### Prometheus Integration Setup

**Option 1: OpenMetrics Check (Recommended)**
```yaml
# datadog-agent/conf.d/openmetrics.d/conf.yaml
instances:
  - openmetrics_endpoint: http://app:8080/metrics
    namespace: "myapp"
    metrics:
      - "http_requests_total"
      - "http_request_duration_seconds"
```

**Option 2: Prometheus Check (Legacy)**
- Older integration method
- Less efficient than OpenMetrics
- Being deprecated

### Limitations

1. **Default metric limit**: 2,000 metrics per instance
   - Can increase via `max_returned_metrics` option
   - WARNING: All Prometheus metrics count as **custom metrics** ($$)

2. **Wildcard usage**: Avoid `metrics: ['*']` (very expensive)
   - Bills for ALL metrics scraped
   - Recommend explicit metric names

3. **Label mapping**: Prometheus labels → Datadog tags automatically
   - Works well in most cases
   - Some edge cases with label cardinality

4. **No metric_relabel_configs**: Can't filter metrics like Prometheus
   - Must filter at application level or in Datadog UI

---

## Query Language: PromQL vs DQL

### PromQL Example
```promql
rate(http_requests_total{status="200"}[5m])
```

### Datadog DQL Equivalent
```
avg:http_requests_total{status:200}.as_rate()
```

### Key Differences

| Feature | PromQL | Datadog DQL |
|---------|--------|-------------|
| **Rate calculation** | `rate()` | `.as_rate()` or `.as_count()` |
| **Aggregation** | `sum by (label)` | `sum:metric{*} by {tag}` |
| **Filtering** | `{label="value"}` | `{tag:value}` |
| **Time ranges** | `[5m]` | Implicit (set in UI) |
| **Functions** | `histogram_quantile()` | Different syntax |

**Migration effort**: **20-80 hours** to convert PromQL dashboards/alerts to DQL

---

## Cost Analysis

### Pricing Model

**Metrics pricing (as of 2024):**
- **Custom metrics**: ~$0.05 per metric per month
- **Prometheus metrics**: ALL counted as custom metrics
- **Host-based pricing**: $15/host/month (Infrastructure Monitoring)
- **APM**: Additional $31-40/host/month
- **Logs**: $0.10/GB ingested + $1.70/million log events indexed

### Cost Comparison (Prometheus Integration)

**Small scale (100K Prometheus metrics):**
- **Datadog**: $5,000/month (100K custom metrics + hosts)
- **Prometheus + Grafana (self-hosted)**: $150/month
- **VictoriaMetrics**: $50/month
- **Grafana Cloud**: $300/month

**Datadog premium**: **33x more expensive** than self-hosted

**Medium scale (1M Prometheus metrics):**
- **Datadog**: $50,000/month (1M custom metrics + hosts)
- **Prometheus (self-hosted)**: $775/month
- **VictoriaMetrics**: $191/month
- **Grafana Cloud**: $2,000/month

**Datadog premium**: **64x more expensive** than self-hosted

### Real-World Cost Examples

**Coinbase (2023):**
- Received $65M annual bill from Datadog
- Triggered migration away from Datadog
- Cost was primary motivator

**Shopify:**
- Migrated from Datadog to Prometheus + Grafana
- Estimated millions in annual savings
- Apps already exposed Prometheus metrics (migration simplified)

---

## Migration Analysis

### Migration TO Datadog (from Prometheus)

**Effort**: **Medium-High** (40-120 hours)

**Steps:**
1. Install Datadog Agent on all hosts (4-8 hours)
2. Configure OpenMetrics checks for all Prometheus endpoints (8-16 hours)
3. Convert PromQL dashboards to Datadog dashboards (20-60 hours)
4. Convert Prometheus alerts to Datadog monitors (8-16 hours)
5. Test and validate (4-8 hours)
6. Train team on DQL (8-16 hours)

**Challenges:**
- PromQL → DQL conversion (not 1:1 mapping)
- Custom metrics pricing surprises (budget shock)
- Loss of PromQL muscle memory

### Migration FROM Datadog (back to Prometheus)

**Effort**: **High** (80-200 hours)

**Steps:**
1. Deploy Prometheus/VictoriaMetrics infrastructure (8-16 hours)
2. Instrument apps with Prometheus exposition (if not already done) (20-60 hours)
3. Convert Datadog dashboards back to PromQL (40-80 hours)
4. Convert Datadog monitors back to Prometheus alerts (20-40 hours)
5. Historical data export (if needed) (4-12 hours)
6. Retrain team on Prometheus ecosystem (8-16 hours)

**Challenges:**
- DQL → PromQL conversion (manual work)
- Loss of Datadog-specific features (APM, distributed tracing, logs)
- Operational burden shifts back to team

---

## Advantages of Datadog

### What You Get (vs Prometheus Alone)

1. **Full observability** - Metrics + Traces + Logs + APM in one platform
2. **Zero operational burden** - Fully managed SaaS
3. **Enterprise features**:
   - Advanced anomaly detection (ML-based)
   - Security monitoring (SIEM)
   - Real user monitoring (RUM)
   - Synthetic monitoring
   - Network performance monitoring
   - Service catalog and dependency mapping
4. **Rich integrations** - 600+ integrations out-of-box
5. **Superior UI/UX** - Best-in-class dashboarding and visualization
6. **Correlation** - Seamless correlation between metrics, traces, logs
7. **Commercial support** - 24/7 enterprise support
8. **Compliance** - SOC2, HIPAA, PCI-DSS certified

### When Datadog Makes Sense

✅ **Full observability needed** (not just metrics)
✅ **Zero ops burden** (no time to manage Prometheus)
✅ **Enterprise requirements** (compliance, support, SLAs)
✅ **Budget available** ($50K+/year for monitoring)
✅ **Distributed tracing critical** (microservices observability)
✅ **Team prefers SaaS** (avoid self-hosting complexity)

---

## Disadvantages of Datadog

### What You Lose (vs Prometheus)

1. **High lock-in** - Proprietary query language, storage, dashboards
2. **Expensive at scale** - Can reach $100K+ per year easily
3. **No PromQL** - Must learn and use DQL instead
4. **Vendor control** - Pricing, features, roadmap controlled by Datadog
5. **Custom metrics pricing** - Prometheus metrics ALL count as custom ($$)
6. **Migration cost** - 80-200 hours to migrate back out

### When Datadog is a Poor Fit

❌ **Cost-sensitive** (Datadog 10-100x more expensive)
❌ **Portability priority** (high lock-in risk)
❌ **Already have Prometheus expertise** (team knows PromQL)
❌ **Simple metrics monitoring** (Datadog overkill)
❌ **Open source preference** (Datadog is proprietary)

---

## Lock-in Analysis

### Lock-in Risk: **HIGH**

**What's portable:**
- ✅ Prometheus metrics exposition (can still scrape with Prometheus)
- ✅ Metrics data (can export via API, though painful)

**What's NOT portable:**
- ❌ Dashboards (DQL-based, must rewrite)
- ❌ Alerts (Datadog monitors ≠ Prometheus alerts)
- ❌ Query language (DQL ≠ PromQL)
- ❌ APM traces (Datadog-specific format)
- ❌ Logs (Datadog-specific indexing)
- ❌ Integrations (Datadog-specific)

**Migration out effort**: **80-200 hours** (high friction)

---

## Prometheus Integration Strategy

### Best Practice: Hybrid Approach

If using Datadog for full observability, maintain Prometheus portability:

**Option 1: Dual-write**
```
App exposes /metrics (Prometheus)
      ↓
   ┌──────┴──────┐
   ↓             ↓
Datadog Agent   Prometheus (local)
```

**Pros:**
- Preserve Prometheus portability
- Can migrate away from Datadog easier
- PromQL skills maintained

**Cons:**
- Extra operational burden
- Duplicate storage

**Option 2: OpenTelemetry layer**
```
App (OTel SDK)
      ↓
OTel Collector
      ↓
   ┌──────┴──────┐
   ↓             ↓
Datadog        Prometheus Backend
```

**Pros:**
- Future-proof (OTel is standard)
- Easy to switch backends
- Vendor-neutral instrumentation

**Cons:**
- More complex setup
- Extra component to manage

---

## Datadog vs Prometheus Ecosystem

### Comparison Matrix

| Aspect | Datadog | Prometheus + Grafana | Prometheus + Grafana Cloud |
|--------|---------|---------------------|---------------------------|
| **Setup complexity** | Low (SaaS) | Medium (self-hosted) | Low (managed) |
| **Operational burden** | Zero | High | Low |
| **Cost (1M series)** | $50,000/month | $775/month | $2,000/month |
| **Lock-in risk** | HIGH | ZERO | LOW |
| **PromQL support** | NO (DQL only) | YES (native) | YES (native) |
| **Full observability** | YES (all-in-one) | Partial (need separate tools) | Partial |
| **Migration effort** | 40-120 hours (in), 80-200 hours (out) | N/A | 5-15 hours |
| **Enterprise support** | YES (included) | NO (community) | YES (included) |
| **Compliance** | SOC2, HIPAA, PCI | Self-certified | SOC2, HIPAA |

---

## Recommendation

### When to Choose Datadog

**Strong fit:**
- Need full observability (metrics + traces + logs + APM)
- Budget $50K+ per year for monitoring
- Zero tolerance for operational burden
- Enterprise compliance required (SOC2, HIPAA, etc.)
- Distributed microservices (need distributed tracing)
- Team lacks Prometheus expertise

**Migration path**: Prometheus → Datadog
- **Effort**: 40-120 hours
- **Risk**: Medium (reversible, but expensive)
- **Gotcha**: Custom metrics pricing (budget for it)

### When to Avoid Datadog

**Poor fit:**
- Cost-sensitive (<$50K/year budget)
- Already have Prometheus expertise
- Portability is priority
- Simple metrics monitoring (Datadog is overkill)
- Open source preference

**Alternative**: Prometheus + Grafana + Jaeger/Tempo (self-hosted full observability)
- **Cost**: 10-100x cheaper
- **Lock-in**: ZERO
- **Trade-off**: More operational burden

---

## Final Verdict

**Datadog is NOT a Prometheus backend replacement - it's a full observability platform that can ingest Prometheus metrics.**

**Key insights:**
1. ✅ Can scrape Prometheus endpoints (ingestion works)
2. ❌ Cannot query with PromQL (must use DQL)
3. ⚠️ HIGH lock-in (query language, dashboards, alerts)
4. 💰 EXPENSIVE (10-100x more than Prometheus ecosystem)
5. 🎯 VALUE PROP: Full observability, zero ops, enterprise features

**Bottom line:**
- Choose Datadog for **convenience and full observability**
- Choose Prometheus for **cost-efficiency and portability**
- Don't choose Datadog if you ONLY need metrics monitoring

**Portability preservation:**
- If using Datadog, keep apps instrumented with Prometheus format
- Maintain PromQL knowledge (future migration option)
- Consider OpenTelemetry for vendor-neutral instrumentation
