# Prometheus-Compatible Backends: Comprehensive Comparison Matrix

**Date**: October 17, 2025
**Backends Analyzed**: 8 major backends across self-hosted, managed, and platform categories

---

## Quick Reference Matrix

| Backend | Type | Prom Format | PromQL | Lock-in | Cost (1M series) | Migration In | Migration Out |
|---------|------|-------------|--------|---------|------------------|--------------|---------------|
| **Prometheus** | Self-hosted | ✅ 100% | ✅ 100% | ZERO | $775/mo | N/A | N/A |
| **VictoriaMetrics** | Self-hosted | ✅ 100% | ✅ 100%+ | LOW | $191/mo | 5-15h | 4-12h |
| **Thanos** | Self-hosted | ✅ 100% | ✅ 100% | ZERO | $400-800/mo | 20-40h | 8-16h |
| **Grafana Mimir** | Self-hosted | ✅ 100% | ✅ 100% | LOW | $600-1000/mo | 20-40h | 8-16h |
| **Grafana Cloud** | Managed | ✅ 100% | ✅ 100% | LOW | $2,000/mo | 5-15h | 5-15h |
| **AWS AMP** | Managed | ✅ 100% | ✅ 100% | MEDIUM | $1,500-3,000/mo | 8-20h | 12-24h |
| **Datadog** | Platform | ✅ Ingest | ❌ DQL only | HIGH | $50,000/mo | 40-120h | 80-200h |
| **New Relic** | Platform | ✅ Ingest | ⚠️ Partial | HIGH | $30,000-60,000/mo | 40-120h | 80-200h |

---

## Detailed Comparison

### 1. Prometheus Compatibility

#### Exposition Format Support

| Backend | Support Level | Notes |
|---------|--------------|-------|
| **Prometheus** | ✅ 100% Reference | Defines the standard |
| **VictoriaMetrics** | ✅ 100% + extras | Also: Graphite, InfluxDB, DataDog formats |
| **Thanos** | ✅ 100% Native | Uses Prometheus codebase |
| **Grafana Mimir** | ✅ 100% Native | Fork of Cortex (Prometheus-based) |
| **Grafana Cloud** | ✅ 100% Native | Managed Prometheus/Mimir |
| **AWS AMP** | ✅ 100% Native | Managed Prometheus-compatible |
| **Datadog** | ⚠️ Ingest only | Translates to proprietary format |
| **New Relic** | ⚠️ Ingest only | Translates to NRDB format |

#### PromQL Query Language Support

| Backend | Support Level | Query Language | Notes |
|---------|--------------|----------------|-------|
| **Prometheus** | ✅ 100% Reference | PromQL | Defines the standard |
| **VictoriaMetrics** | ✅ 100%+ Enhanced | MetricsQL (PromQL superset) | All PromQL works + extra functions |
| **Thanos** | ✅ 100% Compatible | PromQL | Uses Prometheus query engine |
| **Grafana Mimir** | ✅ 100% Compatible | PromQL | Full PromQL support |
| **Grafana Cloud** | ✅ 100% Compatible | PromQL | Native PromQL |
| **AWS AMP** | ✅ 95%+ Compatible | PromQL | Minor edge cases |
| **Datadog** | ❌ NO | DQL (Datadog Query Language) | Must rewrite all queries |
| **New Relic** | ⚠️ Limited | NRQL (New Relic Query Language) | Some PromQL translation available |

---

### 2. Resource Efficiency (1M Active Series)

| Backend | RAM | CPU | Storage (30 days) | Notes |
|---------|-----|-----|-------------------|-------|
| **Prometheus** | 8-12 GB | 2-5 cores | ~66 GB | Baseline |
| **VictoriaMetrics** | 400-800 MB | 0.2-0.5 cores | ~4.5 GB | **20x less RAM, 10x less CPU, 15x less storage** |
| **Thanos** | 8-12 GB | 2-5 cores | ~66 GB (S3) | Similar to Prometheus, but S3 storage cheaper |
| **Grafana Mimir** | 10-15 GB | 3-6 cores | ~50 GB (object storage) | Distributed, more overhead |
| **Grafana Cloud** | N/A (managed) | N/A (managed) | N/A (managed) | Pay-per-sample pricing |
| **AWS AMP** | N/A (managed) | N/A (managed) | N/A (managed) | Pay-per-sample pricing |
| **Datadog** | N/A (SaaS) | N/A (SaaS) | N/A (SaaS) | Pay-per-custom-metric pricing |
| **New Relic** | N/A (SaaS) | N/A (SaaS) | N/A (SaaS) | Pay-per-metric pricing |

---

### 3. Cost Analysis (Monthly)

#### Small Scale (100K Active Series)

| Backend | Infrastructure | Total Cost | Notes |
|---------|---------------|------------|-------|
| **Prometheus** | $150 (2vCPU, 8GB) | $150/mo | Self-hosted |
| **VictoriaMetrics** | $50 (1vCPU, 2GB) | $50/mo | **67% savings vs Prometheus** |
| **Thanos** | $200 (Prom + S3) | $200/mo | S3 storage costs |
| **Grafana Mimir** | $250 (cluster) | $250/mo | Cluster overhead |
| **Grafana Cloud** | N/A | $300/mo | ~$3/1K series |
| **AWS AMP** | N/A | $400-600/mo | ~$4-6/1K series |
| **Datadog** | N/A | $5,000/mo | ~$50/1K series (custom metrics) |
| **New Relic** | N/A | $3,000-5,000/mo | ~$30-50/1K series |

#### Medium Scale (1M Active Series)

| Backend | Infrastructure | Total Cost | Cost per 1K Series |
|---------|---------------|------------|-------------------|
| **Prometheus** | $775 (8vCPU, 32GB) | $775/mo | $0.78 |
| **VictoriaMetrics** | $191 (2vCPU, 4GB) | $191/mo | $0.19 (**75% savings**) |
| **Thanos** | $400-800 (cluster + S3) | $600/mo | $0.60 |
| **Grafana Mimir** | $600-1000 (cluster) | $800/mo | $0.80 |
| **Grafana Cloud** | N/A | $2,000/mo | $2.00 |
| **AWS AMP** | N/A | $1,500-3,000/mo | $1.50-3.00 |
| **Datadog** | N/A | $50,000/mo | $50.00 (**64x more expensive**) |
| **New Relic** | N/A | $30,000-60,000/mo | $30-60.00 |

#### Large Scale (10M Active Series)

| Backend | Infrastructure | Total Cost | Notes |
|---------|---------------|------------|-------|
| **Prometheus** | Not recommended | N/A | Doesn't scale well to 10M |
| **VictoriaMetrics** | $800 (cluster: 6vCPU, 16GB) | $800/mo | Best cost efficiency |
| **Thanos** | $1,500-2,500 (cluster + S3) | $2,000/mo | Production-proven at scale |
| **Grafana Mimir** | $2,000-3,000 (cluster) | $2,500/mo | Enterprise-grade |
| **Grafana Cloud** | N/A | $15,000-20,000/mo | Managed convenience |
| **AWS AMP** | N/A | $12,000-25,000/mo | Cloud-native integration |
| **Datadog** | N/A | $500,000+/mo | See Coinbase $65M/year |
| **New Relic** | N/A | $300,000-500,000/mo | Enterprise pricing |

---

### 4. Operational Complexity

| Backend | Deployment | Scaling | Operational Burden | Expertise Required |
|---------|------------|---------|-------------------|-------------------|
| **Prometheus** | ⭐ Simple | ⭐⭐ Vertical only | ⭐⭐ Low | Basic (1-2 weeks) |
| **VictoriaMetrics** | ⭐ Simple | ⭐⭐⭐⭐ Excellent | ⭐⭐ Low | Basic (1-2 weeks) |
| **Thanos** | ⭐⭐⭐ Complex | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐ High | Advanced (4-8 weeks) |
| **Grafana Mimir** | ⭐⭐⭐ Complex | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐ High | Advanced (4-8 weeks) |
| **Grafana Cloud** | ⭐ Managed | ⭐⭐⭐⭐⭐ Auto | ⭐ Zero | Minimal (days) |
| **AWS AMP** | ⭐ Managed | ⭐⭐⭐⭐⭐ Auto | ⭐ Zero | Minimal (days) |
| **Datadog** | ⭐ SaaS | ⭐⭐⭐⭐⭐ Auto | ⭐ Zero | Medium (2-4 weeks for DQL) |
| **New Relic** | ⭐ SaaS | ⭐⭐⭐⭐⭐ Auto | ⭐ Zero | Medium (2-4 weeks for NRQL) |

---

### 5. Lock-in Risk Analysis

| Backend | Format Lock-in | Query Lock-in | Dashboard Lock-in | Overall Risk | Migration Out Effort |
|---------|---------------|---------------|-------------------|--------------|---------------------|
| **Prometheus** | ZERO | ZERO | ZERO | **ZERO** | N/A |
| **VictoriaMetrics** | ZERO | LOW | ZERO | **LOW** | 4-12 hours |
| **Thanos** | ZERO | ZERO | ZERO | **ZERO** | 8-16 hours (config) |
| **Grafana Mimir** | ZERO | ZERO | ZERO | **LOW** | 8-16 hours (config) |
| **Grafana Cloud** | ZERO | ZERO | LOW | **LOW** | 5-15 hours |
| **AWS AMP** | ZERO | LOW | MEDIUM | **MEDIUM** | 12-24 hours (AWS integration) |
| **Datadog** | ZERO* | HIGH | HIGH | **HIGH** | 80-200 hours |
| **New Relic** | ZERO* | HIGH | HIGH | **HIGH** | 80-200 hours |

*\*Format: Apps still expose Prometheus format, but Datadog/NewRelic translate to proprietary storage*

---

### 6. Feature Comparison

| Feature | Prometheus | VictoriaMetrics | Thanos | Mimir | Grafana Cloud | AWS AMP | Datadog | New Relic |
|---------|------------|-----------------|--------|-------|---------------|---------|---------|-----------|
| **Metrics** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Distributed Tracing** | ❌ | ❌ | ❌ | ❌ | ✅ (Tempo) | ❌ | ✅ | ✅ |
| **Logs** | ❌ | ❌ | ❌ | ❌ | ✅ (Loki) | ❌ | ✅ | ✅ |
| **APM** | ❌ | ❌ | ❌ | ❌ | ⚠️ (add-on) | ❌ | ✅ | ✅ |
| **Multi-tenancy** | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Long-term storage** | ⚠️ Limited | ✅ Excellent | ✅ S3 | ✅ Object storage | ✅ | ✅ | ✅ | ✅ |
| **Downsampling** | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| **Anomaly detection** | ❌ | ✅ Basic | ❌ | ⚠️ Grafana | ✅ | ❌ | ✅ Advanced | ✅ Advanced |
| **Alerting** | ✅ Basic | ✅ vmalert | ✅ | ✅ | ✅ Advanced | ✅ Basic | ✅ Advanced | ✅ Advanced |

---

### 7. Scalability Limits

| Backend | Max Active Series | Horizontal Scaling | Storage Limit | Query Performance |
|---------|-------------------|-------------------|---------------|-------------------|
| **Prometheus** | ~10M (single node) | ❌ Federation only | Local disk | Good (<1M series) |
| **VictoriaMetrics** | ~10M (single), billions (cluster) | ✅ Native clustering | Unlimited | Excellent |
| **Thanos** | Billions | ✅ Native | Unlimited (S3) | Good (global query overhead) |
| **Grafana Mimir** | Billions | ✅ Native | Unlimited (object storage) | Excellent |
| **Grafana Cloud** | Billions | ✅ Auto-scaling | Unlimited | Excellent |
| **AWS AMP** | 1B per workspace | ✅ Auto-scaling | Unlimited | Good |
| **Datadog** | Unlimited | ✅ Auto-scaling | Unlimited | Excellent |
| **New Relic** | Unlimited | ✅ Auto-scaling | Unlimited | Excellent |

---

### 8. Migration Effort Summary

#### Migration Time Matrix (hours)

| From → To | Prometheus | VictoriaMetrics | Thanos | Mimir | Grafana Cloud | AWS AMP | Datadog |
|-----------|------------|-----------------|--------|-------|---------------|---------|---------|
| **Prometheus** | - | 5-15 | 20-40 | 20-40 | 5-15 | 8-20 | 40-120 |
| **VictoriaMetrics** | 4-12 | - | 16-30 | 16-30 | 5-15 | 8-20 | 40-120 |
| **Thanos** | 8-16 | 8-16 | - | 12-24 | 8-20 | 12-24 | 40-120 |
| **Grafana Cloud** | 5-15 | 5-15 | 8-20 | 8-20 | - | 12-24 | 40-120 |
| **Datadog** | 80-200 | 80-200 | 80-200 | 80-200 | 80-200 | 80-200 | - |

**Key insights:**
- Prometheus ecosystem backends (Prometheus, VM, Thanos, Mimir, Grafana Cloud): **5-40 hours** to switch
- Cloud providers (AWS AMP): **8-24 hours** to switch
- Observability platforms (Datadog, New Relic): **40-120 hours** to adopt, **80-200 hours** to leave

---

## Decision Framework

### Choose Based on Priority

#### Priority: **Cost Efficiency**
**Winner**: **VictoriaMetrics** (75% cheaper than Prometheus, 10-100x cheaper than Datadog)

#### Priority: **Portability / Zero Lock-in**
**Winner**: **Prometheus** or **Thanos** (pure Prometheus ecosystem, CNCF projects)

#### Priority: **Scalability**
**Winners**: **Thanos**, **Grafana Mimir** (proven to billions of series)

#### Priority: **Simplicity**
**Winner**: **Prometheus** (single binary, simple deployment) or **Grafana Cloud** (fully managed)

#### Priority: **Full Observability**
**Winner**: **Datadog** or **New Relic** (metrics + traces + logs + APM all-in-one)

#### Priority: **Operational Burden = Zero**
**Winners**: **Grafana Cloud**, **AWS AMP**, **Datadog** (fully managed)

---

## Recommendation by Use Case

### Startup (<100K series, cost-sensitive)
**Recommended**: **Prometheus** (self-hosted) or **VictoriaMetrics** (more efficient)
- **Why**: Simple, free/cheap, learn Prometheus ecosystem
- **Migration later**: Easy to scale to any Prometheus-compatible backend

### Small Business (100K-1M series, some budget)
**Recommended**: **VictoriaMetrics** (self-hosted) or **Grafana Cloud**
- **Why**: VictoriaMetrics = best cost/performance, Grafana Cloud = managed ease
- **Avoid**: Datadog (too expensive at this scale)

### Mid-size Company (1M-10M series, full observability needed)
**Recommended**: **Grafana Cloud** (LGTM stack) or **VictoriaMetrics + Jaeger + Loki** (self-hosted)
- **Why**: Full observability without Datadog prices
- **Alternative**: Datadog if budget allows ($50K+/year) and want zero ops

### Enterprise (10M+ series, compliance required)
**Recommended**: **Grafana Mimir** (self-hosted), **Grafana Cloud** (managed), or **Datadog** (full platform)
- **Why**: Proven at scale, enterprise features, compliance certifications
- **Trade-off**: Operational complexity (Mimir) vs Cost (Grafana Cloud) vs Lock-in (Datadog)

### Cloud-Native AWS Shop
**Recommended**: **AWS Managed Prometheus (AMP)** + **AWS X-Ray** + **CloudWatch Logs**
- **Why**: Native AWS integration, IAM-based auth, familiar billing
- **Trade-off**: Medium lock-in (AWS ecosystem), but better than Datadog

---

## Final Summary

**Three tiers of Prometheus backends:**

**Tier 1: Pure Prometheus Ecosystem (ZERO lock-in)**
- Prometheus, VictoriaMetrics, Thanos, Grafana Mimir
- PromQL native, full portability
- Easy migration between them (5-40 hours)

**Tier 2: Managed Prometheus-Compatible (LOW-MEDIUM lock-in)**
- Grafana Cloud, AWS AMP, GCP Managed Prometheus
- PromQL compatible, some vendor integration
- Medium migration effort (8-24 hours)

**Tier 3: Observability Platforms (HIGH lock-in)**
- Datadog, New Relic, Dynatrace
- Ingest Prometheus but use proprietary query/storage
- High migration effort (80-200 hours to leave)

**Bottom line**: Stay in Tier 1-2 for portability, go to Tier 3 only if full observability platform value justifies lock-in and cost.
