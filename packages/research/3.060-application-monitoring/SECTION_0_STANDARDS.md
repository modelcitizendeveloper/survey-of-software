# Section 0: Open Standards Evaluation

**Experiment**: 3.060 Application Monitoring
**Tier 2 Standards**: 2.040 OpenTelemetry + 2.041 Prometheus (Observability Portability)
**Date**: October 17, 2025

---

## Does a Tier 2 Open Standard Exist?

✅ **YES** - **OpenTelemetry + Prometheus** as observability portability standards

**Standard References**:
- [2.040-opentelemetry](../../2.040-opentelemetry/) - Instrumentation standard
- [2.041-prometheus](../../2.041-prometheus/) - Metrics format standard
- [Synthesis: How they work together](../../synthesis/OBSERVABILITY_STANDARDS_2.040_2.041.md)

**What they standardize**:
- **OpenTelemetry**: Instrumentation API/SDK for metrics, traces, logs (CNCF Graduated 2021)
- **Prometheus**: Metrics exposition format + PromQL query language (CNCF Graduated 2018)
- **Integration**: OTel for instrumentation → Prometheus-compatible backend for storage

**Key insight**: They're **complementary, not competing** - OTel collects, Prometheus stores/queries

**Governance**: Cloud Native Computing Foundation (CNCF Graduated projects)

---

## Path 2 Viability Assessment

### Portability Level: ✅ **HIGH**

**OpenTelemetry instrumentation** (write once, export anywhere):
- 40+ backend targets (Prometheus, Jaeger, Tempo, Grafana Cloud, VictoriaMetrics, AWS AMP, etc.)
- Vendor-neutral SDK (metrics + traces + logs)
- Zero code changes to switch backends (config change only)

**Prometheus metrics ecosystem** (30+ compatible backends):
- **Self-hosted**: Prometheus, VictoriaMetrics, Thanos, Mimir
- **Managed**: Grafana Cloud, AWS AMP, Google Cloud Managed Prometheus
- **Platforms**: Datadog, New Relic (can ingest Prometheus format)
- **Query portability**: PromQL works across all backends

### Migration Complexity

**Within OTel/Prometheus ecosystem** (VictoriaMetrics → Grafana Cloud):
- **Time**: 5-15 hours (deploy new backend, update config, migrate dashboards)
- **Method**: Change exporter endpoint, import dashboards
- **Code changes**: ZERO (apps still use OTel SDK)
- **Dashboard changes**: Minimal (PromQL portable)

**Lock-in risk**: **LOW** (within open standards ecosystem)

**Gotchas**:
- PromQL portable, but vendor extensions (MetricsQL, LogQL) create soft lock-in
- Dashboard JSON format differs between backends (Grafana vs others)
- Backend-specific features (VictoriaMetrics optimizations, Tempo TraceQL) create soft dependencies

---

## Path 1 (DIY) vs Path 2 (Standard) vs Path 3 (Managed)

### Path 1: DIY Logging/Metrics (Custom Scripts)

**What it is**: Custom logging to files, cron scripts for health checks, manual log parsing

**Pros**:
- ✅ Zero cost (disk space only)
- ✅ Full control (log format, retention)
- ✅ No external dependencies

**Cons**:
- ❌ Manual work (no dashboards, no alerting, no aggregation)
- ❌ No distributed tracing (impossible to debug microservices)
- ❌ Doesn't scale (log files grow unbounded, no search)
- ❌ No historical analysis (hard to query past data)

**When to use**:
- Single server, <10 requests/day
- Debugging during development only
- Budget = $0, can't afford monitoring

**Reality**: This is NOT viable for production systems. You need structured monitoring.

---

### Path 2: OpenTelemetry + Prometheus Ecosystem (Standards)

**What it is**: Use OTel SDK for instrumentation, Prometheus-compatible backend for storage

**Pros**:
- ✅ LOW lock-in (switch backends in 5-40 hours)
- ✅ 40+ OTel backends, 30+ Prometheus backends
- ✅ CNCF graduated standards (10+ years proven)
- ✅ PromQL portable across ecosystem
- ✅ Cost-effective ($191-2,000/month for 1M series)
- ✅ Full observability (metrics + traces + logs via OTel)

**Cons**:
- ⚠️ Operational burden (self-hosted Prometheus/VictoriaMetrics requires maintenance)
- ⚠️ Learning curve (OTel SDK, PromQL, Grafana dashboards)
- ⚠️ Component management (OTel Collector, storage backend, visualization)

**When to use**:
- Want portability (avoid vendor lock-in)
- Medium-to-long-term project (portability pays off)
- Have technical team (can learn OTel + PromQL)
- Budget-conscious ($191-2,000/month vs $50K+/month)

**Backend options**:

**Self-hosted** (cheapest, most control):
- **VictoriaMetrics**: $191/month (1M series) - Best cost/performance
- **Prometheus**: $775/month (1M series) - Reference implementation
- **Thanos**: $500-1,500/month - Prometheus with long-term storage
- **Mimir**: $800-2,000/month - Prometheus at scale

**Managed** (convenience, still portable):
- **Grafana Cloud**: $2,000-20,000/month - Full LGTM stack (Loki + Grafana + Tempo + Mimir)
- **AWS AMP**: $1,500-3,000/month - Managed Prometheus on AWS
- **Google Cloud Managed Prometheus**: Similar to AWS AMP

**Key benefit**: Can start with VictoriaMetrics ($191/month), migrate to Grafana Cloud ($2K/month) when ready for managed. Zero code changes.

---

### Path 3: Observability Platforms (Proprietary)

**What it is**: Datadog, New Relic, Dynatrace - full-stack platforms

**Pros**:
- ✅ Managed convenience (zero ops burden)
- ✅ Full observability (metrics + traces + logs + APM + RUM)
- ✅ Turnkey experience (5-minute setup, pre-built dashboards)
- ✅ Enterprise features (anomaly detection, ML-based alerts)
- ✅ Support (24/7, SLAs, compliance certifications)

**Cons**:
- ❌ HIGH lock-in (proprietary query languages - DQL, NRQL)
- ❌ Expensive ($50,000-500,000+/month at scale)
- ❌ Migration out is costly (80-200 hours to rewrite dashboards/alerts)
- ❌ Pricing opacity (per-metric, per-span, per-GB ingestion)

**When to use**:
- Enterprise budget ($50K+/month monitoring budget)
- Zero tolerance for operational burden
- Need full-stack features (APM, RUM, security monitoring)
- Accept lock-in for convenience

**Cost example (1M active metrics)**:
- **Datadog**: $50,000/month ($600K/year)
- **New Relic**: $40,000-60,000/month
- **Dynatrace**: $60,000+/month

**Lock-in mechanisms**:
- **Query language**: DQL (Datadog), NRQL (New Relic) - NOT portable
- **Dashboards**: Vendor-specific JSON format
- **Alerts**: Vendor-specific configuration
- **Integrations**: Vendor-specific APIs

**Migration out**: 80-200 hours (rewrite queries, dashboards, alerts)

---

### Hybrid Approach (Standards + Selective Platform Use)

**Pattern**: Use OTel/Prometheus for core monitoring, add specialized tools for specific needs

**Example**:
- **Core monitoring**: OpenTelemetry + VictoriaMetrics ($191/month)
- **Real User Monitoring (RUM)**: PostHog or Sentry (frontend-specific)
- **Error tracking**: Sentry ($26-80/month) - specialized error grouping
- **Synthetic monitoring**: Checkly or UptimeRobot ($15-100/month)

**Benefit**: Get OTel/Prometheus portability for core monitoring, use specialized tools where they excel

**Cost**: $300-500/month (vs $50K/month for Datadog doing everything)

---

## Decision Framework

### Choose OpenTelemetry + Prometheus (Path 2) if:

✅ **Portability is priority** (want to switch backends easily)
✅ **Medium-to-long-term project** (portability investment pays off)
✅ **Budget-conscious** ($191-2,000/month vs $50K+/month)
✅ **Technical team** (can learn OTel SDK, PromQL)
✅ **Want flexibility** (self-hosted → managed migration path)

**Recommended stack**:
- **Instrumentation**: OpenTelemetry SDK
- **Metrics backend**: VictoriaMetrics (cost-optimal) or Grafana Cloud (managed)
- **Traces backend**: Jaeger (self-hosted) or Tempo (Grafana Cloud)
- **Logs backend**: Loki (Grafana Cloud) or self-hosted
- **Visualization**: Grafana

### Choose Observability Platform (Path 3) if:

⚠️ **Enterprise budget**: $50K+/month monitoring budget available
⚠️ **Zero ops tolerance**: Can't manage infrastructure
⚠️ **Need full-stack features**: APM, RUM, security monitoring, ML alerts
⚠️ **Compliance**: SOC2/HIPAA required AND vendor provides certification
⚠️ **Accept lock-in**: Convenience > portability trade-off

**When platform features justify cost**:
- **Datadog APM**: Automatic code-level profiling, flame graphs
- **New Relic AI**: ML-based anomaly detection
- **Dynatrace**: Auto-discovery, root cause analysis

### Hybrid Approach (Best of Both)

**When to use**: Want portability for core monitoring, need specific platform features

**Example setup**:
1. **Apps expose Prometheus /metrics** (preserve portability)
2. **Send metrics to both**:
   - VictoriaMetrics (cost-effective, portable)
   - Datadog (convenience, full features)
3. **Benefit**: Can leave Datadog anytime (Prometheus /metrics still available)

**Real-world pattern**: Many companies do this specifically to maintain negotiating leverage with Datadog

---

## Migration Paths

### Scenario 1: VictoriaMetrics → Grafana Cloud (Standards → Managed)

**Motivation**: Reduce operational burden, get managed LGTM stack

**Migration effort**: **5-15 hours**

**Steps**:
1. Create Grafana Cloud account (1 hour)
2. Update OTel Collector to send to Grafana Cloud endpoints (2 hours)
3. Import dashboards to Grafana Cloud (2-4 hours)
4. Migrate alerts (2-4 hours)
5. Parallel operation for validation (1 week)
6. Decommission VictoriaMetrics (1 hour)

**Code changes**: ZERO (apps still use OTel SDK, only exporter config changes)
**Dashboard changes**: Minimal (PromQL portable, may need minor adjustments)

**Cost change**: $191/month → $2,000/month (10x increase for zero ops burden)

**When worth it**: Team spending >20 hours/month managing VictoriaMetrics

---

### Scenario 2: Datadog → OpenTelemetry + VictoriaMetrics (Platform → Standards)

**Motivation**: Reduce costs (Datadog $50K/month → VictoriaMetrics $191/month)

**Migration effort**: **80-150 hours**

**Steps**:
1. Instrument apps with OpenTelemetry SDK (20-60 hours)
   - Replace Datadog agent/SDK with OTel SDK
   - Add /metrics endpoint for Prometheus scraping
2. Deploy VictoriaMetrics + Grafana (2-4 hours)
3. Deploy Jaeger for traces (2-4 hours)
4. Migrate dashboards from Datadog to Grafana (40-80 hours)
   - Rewrite DQL queries to PromQL
   - Recreate dashboard layouts
5. Migrate alerts (20-40 hours)
   - Rewrite Datadog alert conditions to Prometheus alerting rules
6. Parallel operation (2 weeks validation)
7. Cancel Datadog

**Challenges**:
- Query rewrite (DQL → PromQL) - languages are different
- Dashboard recreation (Datadog JSON → Grafana JSON)
- Lost features (Datadog APM, RUM need alternatives)

**Cost savings**: $49,809/month ($597,708/year)
**ROI**: Migration pays for itself in <1 month

**When worth it**: Datadog costs >$2K/month, long-term project, technical team available

---

### Scenario 3: CloudWatch → OpenTelemetry + Prometheus (Cloud-Native → Standards)

**Motivation**: Reduce costs, increase visibility (CloudWatch expensive, limited queries)

**Migration effort**: **30-85 hours**

**Steps**:
1. Instrument apps with OpenTelemetry SDK (20-60 hours)
2. Deploy VictoriaMetrics (2-4 hours)
3. Create Grafana dashboards (8-20 hours)
4. Set up alerting (4-8 hours)
5. Stop sending to CloudWatch

**Cost change**:
- **Before**: CloudWatch $500-2,000/month (varies by usage)
- **After**: VictoriaMetrics $191/month + Grafana (free self-hosted)

**Savings**: $300-1,800/month

---

### Scenario 4: Self-hosted Prometheus → Grafana Cloud (Self-hosted → Managed)

**Motivation**: Reduce operational burden

**Migration effort**: **8-20 hours**

**Steps**:
1. Create Grafana Cloud account (1 hour)
2. Configure Prometheus remote_write to Grafana Cloud (2-4 hours)
3. Import dashboards to Grafana Cloud (2-4 hours)
4. Migrate alerts (2-4 hours)
5. Parallel operation (1 week)
6. Decommission self-hosted Prometheus (1 hour)

**Cost change**: $775/month (self-hosted) → $2,000/month (managed)
**When worth it**: Team spending >10 hours/month on Prometheus operations

---

## Provider-Specific Lock-in Risks

### Grafana Cloud (Managed OTel + Prometheus)

**Standard features** (portable):
- Prometheus metrics storage (100% PromQL compatible)
- OTLP ingestion (OpenTelemetry native)
- Grafana dashboards (export JSON)

**Proprietary features** (lock-in):
- Grafana Cloud-specific plugins
- Hosted alerting (Grafana alerting rules)
- Grafana Cloud integrations

**Migration away**: 5-15 hours (export dashboards, reconfigure endpoints)
**Lock-in level**: **LOW** (mostly configuration changes)

---

### AWS Managed Prometheus (AMP)

**Standard features** (portable):
- Prometheus remote_write (100% compatible)
- PromQL queries
- Standard exposition format

**Proprietary features** (lock-in):
- AWS IAM authentication
- Integration with AWS services (CloudWatch, ECS, EKS)
- AWS-specific alerting (Amazon Managed Grafana integration)

**Migration away**: 12-24 hours (replace IAM auth, reconfigure integrations)
**Lock-in level**: **MEDIUM** (AWS-specific auth and integrations)

---

### Datadog

**Standard features** (portable):
- Can ingest Prometheus metrics (via agent)
- Can ingest OTLP (via agent)

**Proprietary features** (lock-in):
- DQL query language (NOT PromQL)
- Datadog dashboards (proprietary JSON)
- Datadog alerts (proprietary format)
- Datadog APM (proprietary SDK)
- Datadog integrations (100+ proprietary)

**Migration away**: 80-200 hours (rewrite queries, dashboards, alerts)
**Lock-in level**: **HIGH** (query language, dashboards, entire platform proprietary)

---

### New Relic

**Standard features** (portable):
- Can ingest Prometheus metrics (via agent)
- Can ingest OTLP (via agent)

**Proprietary features** (lock-in):
- NRQL query language (NOT PromQL)
- New Relic dashboards (proprietary)
- New Relic alerts (proprietary)
- New Relic APM (proprietary SDK)

**Migration away**: 80-200 hours
**Lock-in level**: **HIGH**

---

## Cost Comparison (1M Active Metrics, 3 Years)

### Path 2: OpenTelemetry + VictoriaMetrics

**Year 1**: $191/month × 12 = $2,292
**Year 2**: $191/month × 12 = $2,292
**Year 3**: $191/month × 12 = $2,292
**Total**: **$6,876** (3 years)

**Operational cost**: ~5-10 hours/month maintenance = $1,500-3,000/month (if valued at $300/hour)
**True TCO**: $6,876 + $54,000-108,000 = **$60,876-114,876** (3 years)

---

### Path 2: OpenTelemetry + Grafana Cloud (Managed)

**Year 1**: $2,000/month × 12 = $24,000
**Year 2**: $2,000/month × 12 = $24,000
**Year 3**: $2,000/month × 12 = $24,000
**Total**: **$72,000** (3 years)

**Operational cost**: Near zero (managed)
**True TCO**: **$72,000** (3 years)

---

### Path 3: Datadog

**Year 1**: $50,000/month × 12 = $600,000
**Year 2**: $50,000/month × 12 = $600,000 (assume no price increase)
**Year 3**: $50,000/month × 12 = $600,000
**Total**: **$1,800,000** (3 years)

**Operational cost**: Near zero (managed)
**True TCO**: **$1,800,000** (3 years)

---

### Savings Analysis

**VictoriaMetrics vs Datadog**: $1,793,124 saved (99.6% reduction)
**Grafana Cloud vs Datadog**: $1,728,000 saved (96% reduction)

**Even accounting for operational burden** (VictoriaMetrics + $108K ops cost):
- VictoriaMetrics total: $114,876
- Datadog total: $1,800,000
- **Savings**: $1,685,124 (93.6% reduction)

---

## Recommendation

**Default choice**: **OpenTelemetry + Prometheus ecosystem** (Path 2)

**Why**:
- ✅ LOW lock-in (5-40 hour migrations within ecosystem)
- ✅ 40+ OTel backends, 30+ Prometheus backends (flexibility)
- ✅ CNCF graduated standards (10+ years stable)
- ✅ Cost-effective ($191-2,000/month vs $50K+/month)
- ✅ Full observability (metrics + traces + logs via OTel)
- ✅ Growth path (VictoriaMetrics → Grafana Cloud when ready)

**Specific recommendations by company size**:

**Startup** (<$1M ARR):
- **Choice**: VictoriaMetrics self-hosted ($191/month)
- **Why**: Minimize costs, learn ecosystem
- **When to reconsider**: Series A+ ($2K/month budget available)

**Small Business** ($1-10M ARR):
- **Choice**: VictoriaMetrics self-hosted OR Grafana Cloud
- **Why**: Cost-optimal, portability maintained
- **Decision**: Self-hosted if have technical team, Grafana Cloud if prefer managed

**Mid-Size** ($10-100M ARR):
- **Choice**: Grafana Cloud (LGTM stack)
- **Why**: Full observability, managed, still portable
- **Cost**: $2,000-20,000/month (scale-dependent)

**Enterprise** ($100M+ ARR):
- **Choice**: Grafana Cloud OR self-hosted Mimir/Tempo/Loki
- **Why**: Proven at billions of metrics, enterprise support
- **Alternative**: Datadog if need full platform and have $500K+/year budget

---

## When to Avoid OpenTelemetry + Prometheus

❌ **Team has zero technical expertise AND zero budget for learning** (2-4 weeks learning curve)
- Mitigation: Hire consultant for setup ($5K-15K one-time)

❌ **Need full-stack platform features AND have $50K+/month budget**
- Datadog/New Relic may justify cost for enterprise features
- Mitigation: Still expose Prometheus /metrics for future flexibility

❌ **Very simple needs** (<10K metrics, single server)
- Cloud provider monitoring (CloudWatch, Azure Monitor) may suffice
- OTel/Prometheus may be overkill

❌ **Short-term project** (<6 months lifespan)
- Portability investment won't pay off
- Quick platform setup (Datadog) may be pragmatic

---

## Integration with Other Standards

**Related Tier 2 standards**:
- **2.050 PostgreSQL**: Store metrics metadata in PostgreSQL
- **2.051 S3 API**: Long-term metrics storage (Thanos, Mimir use S3)

**Related Tier 1 libraries**:
- **1.XXX Monitoring Libraries**: prometheus_client, opentelemetry-sdk

**Related Tier 3 services**:
- This experiment (3.060) - Choose monitoring backend
- **3.061 Uptime Monitoring**: Synthetic checks (complement metrics)
- **3.062 Web Analytics**: User behavior (distinct from system metrics)

---

## Key Takeaways

1. ✅ **OpenTelemetry + Prometheus ARE the portability standards** for observability
2. ✅ **Complementary, not competing** - OTel instruments, Prometheus stores/queries
3. ✅ **40+ OTel backends, 30+ Prometheus backends** - true portability
4. ✅ **5-40 hour migrations** within ecosystem vs 80-200 hours to leave platforms
5. ✅ **96-99% cost savings** vs proprietary platforms (Grafana Cloud vs Datadog)
6. ⚠️ **Operational burden exists** for self-hosted (5-10 hours/month)
7. ✅ **Managed options available** that maintain portability (Grafana Cloud)
8. ❌ **Platform lock-in is REAL** - DQL/NRQL are NOT portable

**Decision**: When in doubt, choose OpenTelemetry + Prometheus. Portability is insurance against future constraints.

**Specific stack**: OTel SDK → VictoriaMetrics (start cheap) → Grafana Cloud (when ready for managed)
