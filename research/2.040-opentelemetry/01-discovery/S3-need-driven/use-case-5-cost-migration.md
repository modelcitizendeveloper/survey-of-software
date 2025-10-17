# Use Case 5: Cost Optimization Migration

## Scenario Profile

**Context:**
- Currently on expensive managed APM (Datadog, New Relic, Dynatrace)
- Observability costs growing faster than revenue
- Bill shock: $5K/month → $15K/month in 12 months
- Management pressure to reduce cloud spend
- Can't sacrifice observability (business-critical)
- Need to justify any change with ROI analysis

**Example:**
StartupX raised Series A last year and has been growing 20% MoM. They're on Datadog and the bill has grown from $2K/month to $12K/month. CFO is asking why observability costs are growing faster than revenue (10% MoM vs 20% MoM). Engineering team needs to either optimize Datadog usage or migrate to cheaper alternative without losing critical tracing capabilities.

## Requirements Analysis

### Functional Requirements

**Must Maintain:**
- Current error tracking quality
- Distributed tracing across 8-10 services
- Performance monitoring (p95, p99 latencies)
- Existing dashboards and alerts
- Team knowledge and workflows

**Can Sacrifice:**
- Advanced features rarely used (APM Profiler, Session Replay)
- Unlimited retention (90 days is enough vs 1 year)
- Fancy UI (functional is OK vs beautiful)
- Some integrations (keep critical ones only)

**Migration Requirements:**
- Zero downtime migration (parallel operation required)
- Historical data preserved (at least 90 days)
- Gradual rollout (service by service)
- Rollback plan if issues found

### Non-Functional Requirements

**Migration Time:** 2-4 weeks acceptable
- Engineering time valuable but cost savings justify
- Can allocate 1 engineer full-time for 2-4 weeks

**Break-even:** <6 months
- If migration takes >6 months to break even, not worth it
- CFO wants to see savings in next quarter

**Cost Target:** <$3K/month (75% reduction)
- Current: $12K/month
- Target: <$3K/month
- Acceptable: <$5K/month (60% reduction)

**Risk Tolerance:** LOW
- Production observability is critical
- Can't afford gaps in monitoring
- Rollback plan mandatory

## Cost Analysis: Current State

### Datadog Cost Breakdown

**Current Bill: $12,000/month**

| Component | Cost/month | Usage | Why Expensive? |
|-----------|-----------|--------|----------------|
| Infrastructure (10 hosts) | $1,500 | 10 hosts × $15/host/mo | Base cost |
| APM (8 services) | $4,800 | 800K spans/mo × $0.006/span | High trace volume |
| Log Management | $3,600 | 1.2TB/mo × $3/GB | Verbose logging |
| Custom Metrics | $1,200 | 200 custom metrics × $6/metric | Business metrics |
| Synthetics | $600 | 100 checks × $6/check | Uptime monitoring |
| Security Monitoring | $300 | Compliance feature | Nice-to-have |
| **Total** | **$12,000** | | |

**Cost Growth Drivers:**
1. **Span volume growing 10% MoM** (new features → more traces)
2. **Log volume growing 15% MoM** (more debugging, more services)
3. **Metrics growing 5% MoM** (more monitoring as complexity increases)

**Projected Costs:**
- 6 months: $18,000/month (50% increase)
- 12 months: $28,000/month (133% increase)
- 24 months: $60,000/month (400% increase)

This is unsustainable for a Series A company.

## Solution Evaluation

### Option A: Optimize Datadog Usage (Stay)

**Optimization Strategies:**

1. **Aggressive sampling** (reduce APM cost by 80%):
   ```python
   # Before: 100% sampling
   sentry_sdk.init(traces_sample_rate=1.0)  # $4,800/mo

   # After: 10% sampling for most requests, 100% for errors
   def traces_sampler(sampling_context):
       if sampling_context.get("parent_sampled") is not None:
           return sampling_context["parent_sampled"]

       if sampling_context.get("transaction_context", {}).get("name", "").startswith("/health"):
           return 0.0  # Never sample health checks

       if "error" in sampling_context.get("transaction_context", {}).get("tags", {}):
           return 1.0  # Always sample errors

       return 0.1  # Sample 10% of normal traffic

   sentry_sdk.init(traces_sampler=traces_sampler)  # $960/mo (80% reduction)
   ```

2. **Log reduction** (reduce logs by 60%):
   ```python
   # Filter out noisy logs
   import logging

   # Before: All logs sent to Datadog
   # After: Only WARN+ in production
   if os.getenv("ENV") == "production":
       logging.basicConfig(level=logging.WARNING)  # Skip INFO/DEBUG
   else:
       logging.basicConfig(level=logging.DEBUG)

   # Result: 1.2TB → 0.5TB logs ($3,600 → $1,500/mo)
   ```

3. **Metric reduction** (cut 50% of custom metrics):
   ```python
   # Audit current metrics, remove unused ones
   # 200 metrics → 100 metrics ($1,200 → $600/mo)
   ```

4. **Remove nice-to-have features**:
   - Disable Synthetics: -$600/mo (use free UptimeRobot instead)
   - Disable Security Monitoring: -$300/mo (not critical)

**Projected Optimized Cost:**
- Infrastructure: $1,500 (no change)
- APM: $960 (80% reduction via sampling)
- Logs: $1,500 (60% reduction via filtering)
- Metrics: $600 (50% reduction)
- **Total: $4,560/month (62% reduction)**

**Pros:**
- ✅ Zero migration effort: Configuration changes only
- ✅ No risk: Stay on working system
- ✅ Quick wins: Savings in 1 week
- ✅ Reversible: Can turn features back on if needed

**Cons:**
- ⚠️ Reduced visibility: 10% sampling misses some issues
- ⚠️ Still expensive: $4,560/mo = $54,720/year
- ⚠️ Temporary fix: Growth will push costs back up
- ❌ Still locked in: Datadog has pricing power

**Break-even:** Immediate (no migration cost)
**Risk:** LOW

### Option B: Migrate to OpenTelemetry + Self-Hosted

**Architecture:**

```yaml
# Self-hosted stack in Kubernetes
- OpenTelemetry Collector (free)
- Grafana Tempo for traces (free)
- Grafana Loki for logs (free)
- Prometheus for metrics (free)
- Grafana for dashboards (free)

# Infrastructure cost: $300-500/month (compute + storage)
```

**Migration Process:**

**Week 1: Setup Infrastructure**
```bash
# Deploy observability stack
kubectl apply -f observability-stack/

# Components:
# - otel-collector (2 replicas for HA)
# - tempo (with S3 backend)
# - loki (with S3 backend)
# - prometheus
# - grafana

# Total time: 30-40 hours
```

**Week 2-3: Migrate Services**
```python
# Before (Datadog):
import datadog
datadog.initialize()
datadog.api.Event.create(...)

# After (OpenTelemetry):
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

provider = TracerProvider()
processor = BatchSpanProcessor(
    OTLPSpanExporter(endpoint="http://otel-collector:4317")
)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Auto-instrument (FastAPI example)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
FastAPIInstrumentor().instrument_app(app)

# Migrate service by service:
# Day 1-2: Service A
# Day 3-4: Service B
# Day 5-6: Service C
# Day 7-8: Service D
# Day 9-10: Services E-H (parallel)

# Total time: 60-80 hours
```

**Week 4: Dashboards & Alerts**
```python
# Recreate critical dashboards in Grafana
# Migrate alert rules to Prometheus AlertManager

# Total time: 30-40 hours
```

**Total Migration Time:** 120-160 hours (3-4 weeks)

**Costs:**

| Component | Setup Cost | Monthly Cost | Annual Cost |
|-----------|-----------|--------------|-------------|
| Migration labor | $18,000 (120 hrs × $150/hr) | - | - |
| Infrastructure | - | $400 | $4,800 |
| Maintenance | - | $1,200 (8 hrs × $150/hr) | $14,400 |
| **Total Year 1** | **$18,000** | **$1,600** | **$37,200** |
| **Total Year 2** | - | **$1,600** | **$19,200** |

**Cost Comparison:**

| Solution | Year 1 | Year 2 | 2-Year Total |
|----------|--------|--------|--------------|
| Datadog (current) | $144,000 | $216,000 | $360,000 |
| Datadog (optimized) | $54,720 | $75,000 | $129,720 |
| Self-hosted OTel | $37,200 | $19,200 | $56,400 |

**Savings vs Datadog current:** $303,600 over 2 years (84% reduction)
**Savings vs Datadog optimized:** $73,320 over 2 years (56% reduction)

**Break-even:** Month 3 (vs optimized Datadog)

**Pros:**
- ✅ Massive cost savings: 84% reduction
- ✅ Vendor independence: Never locked in again
- ✅ No usage limits: Instrument everything
- ✅ Control: Full customization

**Cons:**
- ❌ High upfront cost: $18K migration
- ❌ Ongoing ops: 8 hours/month maintaining infrastructure
- ⚠️ Feature gaps: Need to build some tools
- ⚠️ UX downgrade: Grafana less polished than Datadog

**Risk:** MEDIUM (self-hosting operational burden)

### Option C: Migrate to OpenTelemetry + Cheap Managed Backend

**Managed Backend Options:**

| Provider | Pricing | Estimated Cost | Features |
|----------|---------|----------------|----------|
| Grafana Cloud | $0.50/GB traces | $800/mo | Good, integrated |
| Axiom | $0.25/GB | $600/mo | Simple, affordable |
| Honeycomb Free | Free for 20M events | $0/mo* | Limited, OK for startup |
| Sentry Performance | $0.005/transaction | $1,200/mo | Great errors, OK traces |

**Recommended: Grafana Cloud**

**Migration Process:**

```python
# Same instrumentation as Option B, different export endpoint
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

provider = TracerProvider()
processor = BatchSpanProcessor(
    OTLPSpanExporter(
        endpoint="https://otlp-gateway-prod-us-east-1.grafana.net/otlp",
        headers={"Authorization": f"Bearer {GRAFANA_CLOUD_API_KEY}"}
    )
)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
```

**Total Migration Time:** 80-100 hours (2-3 weeks)
- No infrastructure setup needed (vs self-hosted)
- Same service instrumentation: 60-80 hours
- Dashboard creation in Grafana Cloud: 20 hours

**Costs:**

| Component | Setup Cost | Monthly Cost | Annual Cost |
|-----------|-----------|--------------|-------------|
| Migration labor | $13,500 (90 hrs × $150/hr) | - | - |
| Grafana Cloud | - | $800 | $9,600 |
| Maintenance | - | $300 (2 hrs × $150/hr) | $3,600 |
| **Total Year 1** | **$13,500** | **$1,100** | **$26,700** |
| **Total Year 2** | - | **$1,100** | **$13,200** |

**Cost Comparison:**

| Solution | Year 1 | Year 2 | 2-Year Total |
|----------|--------|--------|--------------|
| Datadog (current) | $144,000 | $216,000 | $360,000 |
| Datadog (optimized) | $54,720 | $75,000 | $129,720 |
| Self-hosted OTel | $37,200 | $19,200 | $56,400 |
| **Managed OTel** | **$26,700** | **$13,200** | **$39,900** |

**Savings vs Datadog current:** $320,100 over 2 years (89% reduction)
**Savings vs Datadog optimized:** $89,820 over 2 years (69% reduction)

**Break-even:** Month 2 (vs optimized Datadog)

**Pros:**
- ✅ Best cost savings: 89% reduction vs current Datadog
- ✅ Lowest setup cost: $13.5K (vs $18K self-hosted)
- ✅ Minimal maintenance: 2 hours/month (vs 8 hours self-hosted)
- ✅ Vendor independence: Can switch backends later
- ✅ No ops burden: Backend managed

**Cons:**
- ⚠️ Still monthly cost: $1,100/mo (vs $1,600/mo self-hosted)
- ⚠️ Data leaves infrastructure: If that's a concern

**Risk:** LOW (managed service reliability)

## Recommendation: OpenTelemetry + Grafana Cloud (Option C)

### Why This Is The Optimal Cost Migration Path

**1. Best Total Cost of Ownership**

```
2-Year Analysis:

Current Path (Datadog):
- Year 1: $144,000
- Year 2: $216,000 (50% growth)
- Total: $360,000

Optimized Datadog:
- Year 1: $54,720
- Year 2: $75,000 (growth resumes)
- Total: $129,720
- Effort: 20 hours optimization

Self-Hosted OTel:
- Year 1: $37,200 (includes $18K setup)
- Year 2: $19,200
- Total: $56,400
- Effort: 120 hours setup + 96 hours/year maintenance

Managed OTel (Grafana Cloud):
- Year 1: $26,700 (includes $13.5K setup)
- Year 2: $13,200
- Total: $39,900
- Effort: 90 hours setup + 24 hours/year maintenance

Winner: Managed OTel saves $89,820 vs optimized Datadog
```

**2. Fastest Break-Even**

```
Monthly Savings vs Optimized Datadog:
- Optimized Datadog: $4,560/month
- Managed OTel: $1,100/month
- Monthly savings: $3,460/month

Break-even:
Migration cost: $13,500
Break-even months: $13,500 / $3,460 = 3.9 months

CFO sees savings in Q2 (next quarter)!
```

**3. Minimal Risk**

- Grafana Cloud is enterprise-ready (SOC 2 certified)
- Managed service = no operational burden
- Can run parallel with Datadog during migration (validate before cutting over)
- Rollback plan: Keep Datadog active for 1 extra month during validation

**4. Future Optionality**

If Grafana Cloud becomes expensive later:
- Switch to self-hosted: 2-3 days (already using OTel)
- Switch to Honeycomb/Axiom: 1 day (just change exporter endpoint)
- Switch back to Datadog: 1 week (if needed)

### Implementation Plan

**Pre-Migration (1 week before):**

1. **Get buy-in** (2 hours):
   - Present cost analysis to CFO/CTO
   - Show $320K savings over 2 years
   - Explain 4-month break-even

2. **Trial Grafana Cloud** (1 week):
   - Sign up for free trial
   - Migrate 1 non-critical service
   - Validate dashboards look good
   - Confirm costs match estimates

3. **Plan rollout** (4 hours):
   - Order services by migration priority
   - Schedule team availability
   - Prepare rollback procedure

**Week 1: Foundation**

Day 1-2: **Setup**
- Create Grafana Cloud account
- Configure OTLP endpoint
- Set up initial dashboards

Day 3-5: **Migrate First Service** (low-risk)
```python
# Pick least critical service first (e.g., background worker)
# This builds confidence before touching API

# 1. Add OpenTelemetry SDK
pip install opentelemetry-distro opentelemetry-exporter-otlp

# 2. Configure instrumentation
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

provider = TracerProvider(
    resource=Resource.create({"service.name": "background-worker"})
)
processor = BatchSpanProcessor(
    OTLPSpanExporter(
        endpoint="https://otlp-gateway-prod-us-east-1.grafana.net/otlp",
        headers={"Authorization": f"Bearer {GRAFANA_API_KEY}"}
    )
)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# 3. Auto-instrument
from opentelemetry.instrumentation.celery import CeleryInstrumentor
CeleryInstrumentor().instrument()

# 4. Deploy and validate
# Keep Datadog agent running in parallel
# Compare traces between Datadog and Grafana Cloud
```

**Week 2: Main Services**

Day 6-7: **Migrate Service B** (API Gateway)
Day 8-9: **Migrate Service C** (User Service)
Day 10-12: **Migrate Services D-H** (5 remaining services in parallel)

**Week 3: Validation & Cutover**

Day 13-15: **Parallel Operation**
- Both Datadog and OTel running
- Compare observability quality
- Fix any gaps found

Day 16-17: **Dashboard Migration**
```python
# Recreate critical dashboards in Grafana
# Priorities:
# 1. Service health overview
# 2. Error rate per service
# 3. Latency (p95, p99) per endpoint
# 4. Dependency map

# Alerts:
# 1. Error rate spike
# 2. Latency degradation
# 3. Service down
```

Day 18-19: **Team Training**
- Show team new Grafana interface
- Document how to find traces
- Update runbooks with new links

Day 20: **Cutover**
- Turn off Datadog agents
- Validate alerts working
- Celebrate $10K/month savings!

**Week 4: Optimization**

Day 21-23: **Cost Optimization**
```yaml
# Implement sampling to stay under $1K/month if needed
processors:
  probabilistic_sampler:
    sampling_percentage: 50  # Start with 50%, adjust based on volume

# Monitor actual usage:
# Target: <$1,000/month Grafana Cloud bill
```

Day 24-25: **Documentation**
- Document migration for future reference
- Create troubleshooting guide
- Update architecture diagrams

### Success Metrics

**Week 1:**
- ✅ 1 service migrated successfully
- ✅ Traces appearing in Grafana Cloud
- ✅ Team can find and use traces

**Week 3:**
- ✅ All 8 services migrated
- ✅ Dashboards recreated
- ✅ Alerts functioning

**Month 2:**
- ✅ Datadog decommissioned
- ✅ Grafana Cloud bill <$1,200/month
- ✅ Monthly savings: $10,800 ($12K - $1.2K)

**Month 6 (Break-even):**
- ✅ Total savings: $54,000 (6 months × $9K/mo net savings)
- ✅ Migration paid for: $13.5K setup cost recovered
- ✅ Pure profit from here: $9K/month savings

**Year 1:**
- ✅ Annual savings: $117,300 ($144K Datadog - $26.7K OTel)
- ✅ ROI: 770% ($117.3K savings / $13.5K setup = 8.7×)

## Risk Mitigation

**Risk 1: Migration takes longer than estimated**
- **Likelihood:** Medium
- **Impact:** High (labor cost increases)
- **Mitigation:**
  - Keep Datadog active during migration (budget 2 extra months = $24K)
  - If exceeds 160 hours, pause and reassess
- **Rollback:** Stay on Datadog if migration cost exceeds $25K

**Risk 2: Grafana Cloud more expensive than estimated**
- **Likelihood:** Low
- **Impact:** Medium
- **Mitigation:**
  - Monitor usage daily in first month
  - Implement sampling if approaching $1.5K/month
- **Fallback:** Switch to Honeycomb (cheaper) or self-hosted

**Risk 3: Feature gaps in Grafana Cloud**
- **Likelihood:** Medium
- **Impact:** Medium
- **Mitigation:**
  - Identify must-have features before migration
  - Test in trial period
- **Fallback:** Use hybrid (Grafana for traces, Sentry for errors)

**Risk 4: Team productivity drop**
- **Likelihood:** Low
- **Impact:** High
- **Mitigation:**
  - Training sessions before cutover
  - Keep Datadog read-only for 2 weeks after cutover
  - Document common workflows
- **Fallback:** Extend Datadog overlap if team struggling

## Alternative: Phased Approach

If risk tolerance is very low:

**Phase 1 (Month 1): Optimize Datadog**
- Implement sampling, log filtering
- Reduce cost to $4,560/month
- Zero risk, immediate savings

**Phase 2 (Month 2-3): Pilot OTel**
- Migrate 2 services to OTel + Grafana Cloud
- Validate approach
- Keep majority on Datadog

**Phase 3 (Month 4-6): Full Migration**
- If pilot successful, migrate remaining services
- Decommission Datadog

This spreads risk but delays savings.

## Conclusion

For cost-constrained companies on expensive APM, **migrating to OpenTelemetry + Grafana Cloud is the optimal path**:

1. **89% cost reduction**: $144K/year → $13.2K/year (after Year 1)
2. **Fast break-even**: 4 months
3. **Low risk**: Managed service, parallel operation during migration
4. **Future-proof**: Can switch backends anytime

**StartupX Action Plan:**
- Week 1: Get CFO approval (show $320K 2-year savings)
- Week 2: Start Grafana Cloud trial
- Week 3-5: Execute migration (allocate 1 engineer full-time)
- Week 6: Decommission Datadog
- Result: $10K/month savings, $120K/year recurring savings

This is a **no-brainer cost optimization** with 770% ROI in Year 1.
