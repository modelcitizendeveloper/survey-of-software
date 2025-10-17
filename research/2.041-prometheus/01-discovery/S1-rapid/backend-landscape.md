# Prometheus-Compatible Backends Landscape

**Discovery Date**: October 17, 2025
**Source**: Web search, vendor documentation
**Scope**: Quick survey of Prometheus exposition format compatible backends

---

## Backend Categories

### 1. Self-Hosted Open Source (DIY)

| Backend | Prometheus Compat | PromQL Compat | Notable Features | Maturity |
|---------|-------------------|---------------|------------------|----------|
| **Prometheus** | ✅ Reference | ✅ Native | Original implementation, single-node | Graduated CNCF |
| **VictoriaMetrics** | ✅ Native | ✅ Full | High performance, clustering, multi-ingestion | Production |
| **Thanos** | ✅ Native | ✅ Full | Long-term S3 storage, global query | CNCF Sandbox |
| **Cortex** | ✅ Native | ✅ Full | Multi-tenant, horizontally scalable | CNCF Sandbox |
| **Grafana Mimir** | ✅ Native | ✅ Full | Fork of Cortex, Grafana Labs backed | Production |
| **M3DB** | ✅ Native | ✅ Full | Uber's metrics backend, distributed | Production |

**Key Differences:**
- **Prometheus**: Single-node, local storage, simple deployment
- **VictoriaMetrics**: Resource-efficient, clustering out-of-box, accepts multiple protocols
- **Thanos**: Sidecar model, object storage (S3/GCS), infinite retention
- **Cortex/Mimir**: Multi-tenant, horizontally scalable, complex distributed system
- **M3DB**: Uber-scale, distributed, tag-based indexing

**When to use:**
- **Prometheus**: <1M active series, single team, simple setup
- **VictoriaMetrics**: Want clustering + efficiency, reduce costs
- **Thanos/Cortex/Mimir**: >10M active series, need infinite retention, multi-tenant
- **M3DB**: Uber-scale requirements, need distributed coordination

---

### 2. Managed Prometheus Services

| Service | Prometheus Compat | PromQL Compat | Pricing Model | Lock-in Risk |
|---------|-------------------|---------------|---------------|--------------|
| **Grafana Cloud** | ✅ Native | ✅ Full | $8/month + usage | LOW (can export) |
| **AWS Managed Prometheus (AMP)** | ✅ Native | ✅ Full | Pay-per-sample | MEDIUM (AWS ecosystem) |
| **Google Cloud Managed Prometheus (GMP)** | ✅ Native | ✅ Full | Pay-per-sample | MEDIUM (GCP ecosystem) |
| **Azure Monitor (Prometheus)** | ✅ Native | ✅ Full | Pay-per-GB | MEDIUM (Azure ecosystem) |

**Key characteristics:**
- Fully managed Prometheus storage
- Native Prometheus remote_write ingestion
- PromQL query compatibility
- No need to manage storage/retention

**Use cases:**
- Already using cloud provider (AWS/GCP/Azure)
- Want managed Prometheus without self-hosting complexity
- Need cloud-native integration (Kubernetes monitoring in cloud)

---

### 3. Observability Platforms (Prometheus Ingestion Support)

| Platform | Prometheus Compat | PromQL Compat | Primary Use | Notes |
|----------|-------------------|---------------|-------------|-------|
| **Datadog** | ✅ Ingestion | ⚠️ Partial | Full observability | Translates to Datadog metrics, uses DD query language |
| **New Relic** | ✅ Ingestion | ⚠️ Partial | Full observability | Prometheus endpoint support, NRQL for queries |
| **Elastic APM** | ✅ Ingestion | ⚠️ Partial | Elastic stack | Stores in Elasticsearch, Kibana for viz |
| **Dynatrace** | ✅ Ingestion | ⚠️ Limited | Enterprise APM | Ingests Prometheus, uses Dynatrace query |
| **Splunk** | ✅ Ingestion | ⚠️ Limited | Enterprise observability | Accepts Prometheus metrics |

**Key characteristics:**
- Accept Prometheus metrics via remote_write or scraping
- **WARNING**: Most do NOT support PromQL natively
- Translate Prometheus metrics to proprietary format
- Use their own query languages (Datadog DQL, New Relic NRQL, etc.)

**Lock-in risk**: **MEDIUM-HIGH**
- Can ingest Prometheus metrics (portable in)
- Cannot query with PromQL (not portable out)
- Migration back to Prometheus ecosystem requires dashboard/alert rewrite

**Use cases:**
- Need full observability (metrics + traces + logs) in one platform
- Enterprise-grade support and features
- Willing to accept lock-in for convenience

---

### 4. Time-Series Databases (Prometheus-Compatible)

| Database | Prometheus Compat | PromQL Compat | Primary Use | Notes |
|----------|-------------------|---------------|-------------|-------|
| **InfluxDB** | ⚠️ Adapter | ⚠️ Translator | General TSDB | Can accept Prometheus via adapter |
| **TimescaleDB** | ⚠️ Extension | ⚠️ Extension | PostgreSQL-based | Promscale extension (deprecated 2023) |
| **ClickHouse** | ⚠️ Integration | ⚠️ Limited | Analytics DB | Can store Prometheus metrics |

**Key characteristics:**
- Not designed primarily for Prometheus
- Can integrate via adapters/extensions
- Better suited for generic time-series use cases

**Use cases:**
- Already using the database for other purposes
- Need SQL-based metrics querying
- Non-Prometheus-first architecture

---

## Backend Selection Matrix

### By Scale

| Active Series | Recommended Backend | Why |
|---------------|---------------------|-----|
| <100K | Prometheus | Simple, single-node sufficient |
| 100K-1M | Prometheus or VictoriaMetrics | VM more efficient at scale |
| 1M-10M | VictoriaMetrics or Thanos | Need clustering or long-term storage |
| 10M+ | Thanos, Cortex, Mimir, M3DB | Distributed systems required |

### By Operational Preference

| Preference | Recommended Backend | Why |
|------------|---------------------|-----|
| Self-hosted simplicity | Prometheus | Battle-tested, simple deployment |
| Self-hosted efficiency | VictoriaMetrics | Lower resource usage, clustering built-in |
| Self-hosted scale | Thanos or Mimir | Proven at massive scale |
| Managed cloud-native | AWS AMP, GCP GMP, Azure Monitor | Integrate with cloud provider |
| Managed vendor-neutral | Grafana Cloud | Prometheus-native, multi-cloud |
| Full observability platform | Datadog, New Relic | Metrics + traces + logs in one |

### By Portability Priority

| Priority | Recommended Backend | Lock-in Risk |
|----------|---------------------|--------------|
| Maximum portability | Prometheus, VictoriaMetrics, Thanos, Mimir | ZERO (pure Prometheus ecosystem) |
| Cloud-native portability | AWS AMP, GCP GMP, Grafana Cloud | LOW (Prometheus-compatible) |
| Convenience over portability | Datadog, New Relic, Elastic | MEDIUM-HIGH (proprietary query, storage) |

---

## Cost Migration Example (Shopify)

**Case study**: Shopify migrated from Datadog to self-hosted Prometheus + Grafana

**Motivation**:
- Datadog costs scaling exponentially
- Wanted more control over data
- Needed long-term retention

**Migration**:
- Already using Prometheus exposition format in apps
- Switched from Datadog agent scraping to Prometheus scraping
- Deployed Grafana for visualization
- Estimated savings: Millions per year

**Key insight**: Because apps were already exposing Prometheus metrics, switching backends was infrastructure change, NOT code change

---

## Compatibility Notes

### Full Prometheus Ecosystem (Zero Lock-in)
✅ Prometheus, VictoriaMetrics, Thanos, Cortex, Mimir, M3DB, Grafana Cloud

**Characteristics:**
- Native Prometheus exposition format
- Full PromQL support (or 95%+ compatible)
- Can switch between these backends with minimal friction (1-20 hours config/query adjustments)

### Prometheus Ingestion (Low-Medium Lock-in)
⚠️ AWS AMP, GCP GMP, Azure Monitor, Datadog, New Relic, Elastic

**Characteristics:**
- Accept Prometheus metrics (portable IN)
- May not support full PromQL (migration OUT requires work)
- Cloud provider lock-in (AWS/GCP/Azure) or vendor lock-in (Datadog/New Relic)

### Adapter-based (Medium-High Lock-in)
⚠️ InfluxDB, TimescaleDB, ClickHouse

**Characteristics:**
- Require adapters or extensions
- Not first-class Prometheus support
- Use for hybrid use cases (Prometheus + other data)

---

## Next Steps for S2

**Deep-dive per backend:**
1. VictoriaMetrics vs Prometheus (resource usage, clustering)
2. Thanos vs Cortex vs Mimir (scalability, operational complexity)
3. AWS AMP vs GCP GMP vs Grafana Cloud (cost, features, lock-in)
4. Datadog/New Relic Prometheus ingestion (PromQL compatibility, migration paths)

**Migration testing:**
- Instrument sample app with Prometheus metrics
- Switch between backends (Prometheus → VictoriaMetrics → Grafana Cloud → Datadog)
- Document config changes, dashboard rewrites, query translation

**Cost analysis:**
- Self-hosted vs managed pricing at different scales
- Egress costs, storage costs, query costs
- Break-even points for migration
