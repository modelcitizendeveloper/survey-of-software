# Observability Standards Integration: OpenTelemetry + Prometheus

**Experiments Synthesized**: 2.040 (OpenTelemetry), 2.041 (Prometheus)
**Date**: October 17, 2025
**Theme**: How CNCF observability standards work together for vendor-neutral monitoring

---

## Executive Summary

**Key Insight**: OpenTelemetry and Prometheus are **complementary, not competing** standards.

**The Integration:**
- **OpenTelemetry**: Vendor-neutral instrumentation (metrics + traces + logs)
- **Prometheus**: De-facto metrics format and query language (metrics only)
- **Together**: Instrument with OTel, store in Prometheus-compatible backend

**Bottom Line**: Use both. OpenTelemetry for future-proof instrumentation, Prometheus for proven metrics ecosystem.

---

## The Two Standards

### 2.040: OpenTelemetry (Telemetry Collection Framework)

**What it is**: Unified API/SDK for collecting metrics, traces, and logs

**Governance**: CNCF Graduated (2021)

**Scope**: Full observability stack
- **Metrics**: Counters, gauges, histograms (Prometheus-compatible)
- **Traces**: Distributed tracing (spans, context propagation)
- **Logs**: Structured logging

**Key characteristic**: **Instrumentation layer** - collects telemetry, doesn't store it

**Backend agnostic**: Export to 40+ backends (Prometheus, Jaeger, Datadog, Grafana Cloud, etc.)

### 2.041: Prometheus (Metrics Format & Storage)

**What it is**: Metrics exposition format + query language + storage backend

**Governance**: CNCF Graduated (2018)

**Scope**: Metrics only
- **Exposition format**: Text-based /metrics endpoint
- **PromQL**: Powerful query language
- **Storage**: Time-series database
- **Scraping**: Pull-based collection

**Key characteristic**: **End-to-end metrics solution** - collection + storage + query

**30+ compatible backends**: Prometheus, VictoriaMetrics, Thanos, Mimir, Grafana Cloud, AWS AMP, etc.

---

## How They Work Together

### Integration Pattern 1: OTel Instrumentation → Prometheus Storage

```
Application (OTel SDK)
      ↓
Expose metrics in Prometheus format
      ↓
Prometheus (or compatible backend) scrapes
      ↓
Query with PromQL
```

**How it works:**
- App uses OpenTelemetry SDK for instrumentation
- OTel SDK exposes metrics at `/metrics` endpoint (Prometheus format)
- Prometheus backend scrapes the endpoint
- Query with PromQL

**Benefits:**
- ✅ Future-proof instrumentation (OTel is vendor-neutral)
- ✅ Proven metrics backend (Prometheus ecosystem)
- ✅ Best of both worlds

**When to use:** New applications wanting maximum flexibility

### Integration Pattern 2: OTel Collector → Prometheus Remote Write

```
Application (OTel SDK)
      ↓
OTel Collector
      ↓
Prometheus remote_write
      ↓
Prometheus-compatible backend
```

**How it works:**
- App sends metrics to OpenTelemetry Collector (push)
- OTel Collector transforms/filters metrics
- OTel Collector sends to Prometheus via remote_write API

**Benefits:**
- ✅ Centralized collection (OTel Collector)
- ✅ Advanced filtering/transformation
- ✅ Can send to multiple backends simultaneously

**When to use:** Complex environments, need metric transformation, multi-backend export

### Integration Pattern 3: Prometheus OTLP Ingestion (NEW in 3.0)

```
Application (OTel SDK)
      ↓
OTLP (OpenTelemetry Protocol)
      ↓
Prometheus 3.0 (native OTLP ingestion)
      ↓
Query with PromQL
```

**How it works:**
- App sends metrics via OTLP (OTel native protocol)
- Prometheus 3.0 ingests OTLP directly
- Stores as Prometheus metrics, query with PromQL

**Benefits:**
- ✅ Native OTel support in Prometheus
- ✅ No need for separate exporter
- ✅ Official convergence path

**When to use:** Prometheus 3.0+ environments, want OTel instrumentation with Prometheus storage

**Status**: Beta in Prometheus v2.47.0 (Sept 2023), production-ready in Prometheus 3.0 (2024)

---

## Decision Matrix: Which Standard to Use?

### Scenario 1: Metrics Only, Simple Deployment

**Recommendation**: **Prometheus** exposition format (skip OTel)

**Why:**
- Simpler (no OTel Collector needed)
- Prometheus client libraries are mature and simple
- Direct scraping is easier to debug

**Implementation:**
```python
# Use Prometheus client library directly
from prometheus_client import Counter, start_http_server

requests = Counter('http_requests_total', 'Total requests')

start_http_server(8000)  # Expose /metrics
```

**Trade-off**: Locked to metrics only (can't add traces/logs easily later)

### Scenario 2: Metrics Only, Want Future Flexibility

**Recommendation**: **OpenTelemetry** instrumentation → Prometheus storage

**Why:**
- OTel SDK is future-proof (can add traces/logs later)
- Still get Prometheus ecosystem benefits
- Minimal overhead

**Implementation:**
```python
# Use OTel SDK, export Prometheus format
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader

# OTel instrumentation
meter = metrics.get_meter(__name__)
requests = meter.create_counter("http_requests_total")

# Export as Prometheus format
reader = PrometheusMetricReader()
provider = MeterProvider(metric_readers=[reader])
```

**Trade-off**: Slightly more complex setup, but more flexible

### Scenario 3: Full Observability (Metrics + Traces + Logs)

**Recommendation**: **OpenTelemetry** for all signals

**Why:**
- Unified instrumentation API
- Single SDK for metrics, traces, logs
- Vendor-neutral across all signals

**Implementation:**
```python
# OTel SDK for metrics + traces + logs
from opentelemetry import metrics, trace

meter = metrics.get_meter(__name__)
tracer = trace.get_tracer(__name__)

# Metrics
requests = meter.create_counter("http_requests_total")

# Traces
with tracer.start_as_current_span("process_request"):
    # ... your code ...
    pass

# Export metrics to Prometheus, traces to Jaeger
```

**Storage backends:**
- Metrics → Prometheus/VictoriaMetrics
- Traces → Jaeger/Tempo
- Logs → Loki

**Trade-off**: More components to manage, but full observability

### Scenario 4: Already Using Prometheus, Want to Add Traces

**Recommendation**: Add **OpenTelemetry** for traces, keep Prometheus for metrics

**Why:**
- Don't rewrite existing metrics instrumentation
- Add OTel SDK for traces only
- Dual approach is fine

**Implementation:**
- Keep existing Prometheus metrics
- Add OTel SDK for distributed tracing
- Run both in parallel

**Trade-off**: Two instrumentation approaches, but pragmatic

---

## Convergence Timeline

### Historical Context

**2016**: Prometheus CNCF Incubating
**2017**: OpenMetrics project created (standardize Prometheus format)
**2018**: Prometheus CNCF Graduated
**2019**: OpenTelemetry formed (merger of OpenCensus + OpenTracing)
**2021**: OpenTelemetry CNCF Graduated
**2022**: OpenMetrics CNCF Incubating
**2023**: Prometheus adds OTLP ingestion (v2.47.0)
**2024**: OpenMetrics merged back into Prometheus (standard validated)
**2024**: Prometheus 3.0 beta (OTel integration priority)

### Current State (2025)

**Prometheus position**:
> "We want to be the default store for OpenTelemetry metrics" - Prometheus Team, 2024

**OpenTelemetry position**:
> "Prometheus metrics are a strict subset of OpenTelemetry metrics" - OTel Docs

**Result**: **Convergence, not competition**

---

## Compatibility Matrix

### OpenTelemetry Metrics → Prometheus

| OTel Metric Type | Prometheus Equivalent | Compatible? |
|------------------|----------------------|-------------|
| Counter | Counter | ✅ 100% |
| UpDownCounter | Gauge | ✅ 100% |
| Histogram | Histogram | ✅ 100% |
| Exponential Histogram | Native Histogram (Prom 3.0) | ✅ New in Prom 3.0 |
| Summary | Summary | ✅ 100% |

**Compatibility**: **100%** - All OTel metrics can be stored in Prometheus

### Prometheus Metrics → OpenTelemetry

| Prometheus Type | OTel Equivalent | Compatible? |
|-----------------|-----------------|-------------|
| Counter | Counter | ✅ 100% |
| Gauge | UpDownCounter | ✅ 100% |
| Histogram | Histogram | ✅ 100% |
| Summary | Summary | ✅ 100% |

**Compatibility**: **100%** - All Prometheus metrics are valid OTel metrics

**Key insight**: Prometheus metrics are a **subset** of OTel metrics. You can use OTel and still get full Prometheus compatibility.

---

## Backend Compatibility

### Which Backends Support Both?

| Backend | Prometheus Format | OTLP (OTel) | Query Language |
|---------|-------------------|-------------|----------------|
| **Prometheus 3.0** | ✅ Native | ✅ Native | PromQL |
| **VictoriaMetrics** | ✅ Native | ✅ Via Collector | MetricsQL (PromQL+) |
| **Grafana Mimir** | ✅ Native | ✅ Via Collector | PromQL |
| **Grafana Cloud** | ✅ Native | ✅ Native | PromQL |
| **AWS AMP** | ✅ Native | ⚠️ Partial | PromQL |
| **Datadog** | ✅ Ingest | ✅ Ingest | DQL (proprietary) |
| **Jaeger** | ❌ | ✅ Native | N/A (traces) |
| **Tempo** | ❌ | ✅ Native | TraceQL |

**Key finding**: Most Prometheus backends can accept OTel metrics (via collector or native OTLP)

---

## Cost & Lock-in Comparison

### Pure Prometheus Ecosystem

**Instrumentation**: Prometheus client library (Python, Go, Java, etc.)
**Collection**: Prometheus scraping (pull-based)
**Storage**: Prometheus, VictoriaMetrics, Thanos, Mimir
**Query**: PromQL
**Lock-in**: **ZERO** (all open standards, CNCF graduated)
**Cost (1M series)**: $191-800/month (self-hosted)

### OpenTelemetry + Prometheus Backend

**Instrumentation**: OpenTelemetry SDK
**Collection**: OTel Collector OR Prometheus scraping
**Storage**: Prometheus-compatible backend (same as above)
**Query**: PromQL (for metrics), TraceQL (for traces)
**Lock-in**: **ZERO** (all open standards, CNCF graduated)
**Cost (1M series)**: $191-800/month (self-hosted) + OTel Collector overhead (~$50/month)

### OpenTelemetry + Observability Platform

**Instrumentation**: OpenTelemetry SDK
**Collection**: OTel Collector
**Storage**: Datadog, New Relic, Dynatrace
**Query**: Vendor query language (DQL, NRQL)
**Lock-in**: **HIGH** (query language, dashboards proprietary)
**Cost (1M series)**: $50,000+/month

---

## Architectural Patterns

### Pattern 1: Prometheus-First (Simplest)

```
[App] → /metrics (Prometheus format)
           ↓
      [Prometheus]
           ↓
      [Grafana]
```

**Pros**:
- Simplest architecture
- Fewest components
- Direct scraping (easy to debug)

**Cons**:
- Metrics only (no traces/logs)
- Prometheus client library lock-in (minor)

**Best for**: Metrics-only monitoring, simple deployments

### Pattern 2: OTel-First, Prometheus Storage (Recommended)

```
[App] → OTel SDK
           ↓
    OTel Collector
           ↓
   ┌───────┴───────┐
   ↓               ↓
Prometheus      Jaeger
(metrics)      (traces)
   ↓               ↓
      [Grafana]
```

**Pros**:
- Future-proof (OTel is vendor-neutral)
- Can add traces/logs later
- Centralized collection (OTel Collector)
- Can export to multiple backends

**Cons**:
- Extra component (OTel Collector)
- Slightly more complex

**Best for**: New deployments, want full observability, maintain portability

### Pattern 3: Prometheus 3.0 Native OTLP (Future-Proof)

```
[App] → OTel SDK → OTLP
           ↓
   [Prometheus 3.0]
    (native OTLP)
           ↓
      [Grafana]
```

**Pros**:
- Simplest with OTel (no collector needed)
- Native integration in Prometheus 3.0
- Future-proof instrumentation

**Cons**:
- Requires Prometheus 3.0 (not all backends support yet)
- Metrics only (still need separate traces/logs backends)

**Best for**: Prometheus 3.0+ environments, OTel instrumentation, metrics-only

### Pattern 4: Full LGTM Stack (Grafana Cloud)

```
[App] → OTel SDK
           ↓
    OTel Collector
           ↓
    Grafana Cloud
    (LGTM Stack)
    - Mimir (metrics)
    - Tempo (traces)
    - Loki (logs)
           ↓
      [Grafana]
```

**Pros**:
- Full observability (metrics + traces + logs)
- Managed (zero ops)
- Prometheus-compatible (PromQL, TraceQL)
- Zero lock-in (can export data, PromQL portable)

**Cons**:
- Cost ($2,000-20,000/month depending on scale)
- Managed service dependency

**Best for**: Companies wanting full observability without operational burden, maintain portability

---

## Recommendation by Scenario

### Startup: Metrics Only, Budget-Conscious

**Choice**: **Prometheus** client library + VictoriaMetrics

**Why**:
- Simplest (no OTel complexity)
- Cheapest ($50-191/month)
- Fastest to production (4 hours)

**When to reconsider**: When you need traces (then add OTel)

### Small Business: Metrics + Basic Traces

**Choice**: **OpenTelemetry** SDK + Prometheus (metrics) + Jaeger (traces)

**Why**:
- Future-proof (OTel)
- Full observability
- Still self-hosted (cost-effective)

**Cost**: $300-500/month (self-hosted)

### Mid-Size: Full Observability, Managed

**Choice**: **OpenTelemetry** SDK + Grafana Cloud (LGTM stack)

**Why**:
- Zero ops burden
- Full observability
- Prometheus-compatible (portability maintained)

**Cost**: $2,000-20,000/month (managed)

### Enterprise: Full Observability, Scale

**Choice**: **OpenTelemetry** SDK + Grafana Mimir/Tempo/Loki (self-hosted) OR Grafana Cloud

**Why**:
- Proven at billions of metrics/traces
- Enterprise support available
- Compliance (SOC2, HIPAA)

**Cost**: $2,500/month (self-hosted cluster) or $20,000+/month (managed)

---

## Migration Strategies

### From Prometheus to OpenTelemetry

**Phase 1**: Add OTel SDK alongside Prometheus client (parallel operation)
**Phase 2**: Gradually migrate metrics to OTel
**Phase 3**: Remove Prometheus client library
**Effort**: 40-80 hours (depends on app count)

### From Datadog to OTel + Prometheus

**Phase 1**: Instrument apps with OTel SDK (20-60 hours)
**Phase 2**: Deploy Prometheus/VictoriaMetrics (2-4 hours)
**Phase 3**: Migrate dashboards from Datadog to Grafana (40-80 hours)
**Phase 4**: Cancel Datadog
**Effort**: 80-150 hours
**Savings**: $49,000+/month (at 1M series)

### From CloudWatch to OTel + Prometheus

**Phase 1**: Instrument apps with OTel SDK (20-60 hours)
**Phase 2**: Deploy Prometheus backend (2-4 hours)
**Phase 3**: Create Grafana dashboards (8-20 hours)
**Phase 4**: Stop sending to CloudWatch
**Effort**: 30-85 hours

---

## Bottom Line

**The Integration Story:**

1. **OpenTelemetry**: Instrumentation standard (how to collect metrics/traces/logs)
2. **Prometheus**: Storage + query standard (where to store metrics, how to query)
3. **Together**: Best of both worlds (vendor-neutral instrumentation + proven metrics ecosystem)

**Recommendation for New Projects:**

Use **OpenTelemetry SDK** for instrumentation, export to **Prometheus-compatible backend** for storage.

**Why:**
- Future-proof (OTel is CNCF standard for observability)
- Portable (Prometheus ecosystem is CNCF standard for metrics)
- Flexible (can add traces/logs later via OTel)
- Zero lock-in (both are open standards)

**Specific stack:**
- **Instrumentation**: OpenTelemetry SDK (Python/Go/Java/etc.)
- **Metrics backend**: VictoriaMetrics (cost-optimal) or Grafana Cloud (managed)
- **Traces backend**: Jaeger (self-hosted) or Tempo (managed via Grafana Cloud)
- **Logs backend**: Loki (Grafana Cloud) or self-hosted
- **Visualization**: Grafana

**Cost**: $300-2,000/month (self-hosted to managed, 1M series + traces + logs)

**Lock-in**: **ZERO** (all CNCF graduated standards)

---

## Key Takeaways

1. ✅ **OpenTelemetry and Prometheus are complementary** - use both
2. ✅ **Prometheus is THE metrics standard** - 30+ backends, 10+ years stable
3. ✅ **OpenTelemetry is THE instrumentation standard** - future-proof, vendor-neutral
4. ✅ **Integration is official** - Prometheus 3.0 has native OTLP support
5. ✅ **Zero lock-in possible** - Both are CNCF graduated, open standards
6. ✅ **Cost-effective** - $300-2,000/month vs $50K+/month for proprietary platforms

**Final recommendation**: Start with OTel + Prometheus. You can't go wrong with two CNCF graduated standards.
