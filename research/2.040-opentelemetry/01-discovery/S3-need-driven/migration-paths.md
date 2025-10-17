# Migration Paths to OpenTelemetry

## Overview

This document provides practical migration paths from various observability solutions to OpenTelemetry. Each path includes time estimates, code examples, break-even analysis, and decision criteria.

## Path 1: DIY Logging → OpenTelemetry

### Current State: Custom Logging

**Typical Setup:**
```python
# Custom structured logging
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'service': 'user-service',
            'request_id': getattr(record, 'request_id', None),
            'user_id': getattr(record, 'user_id', None),
        }
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        return json.dumps(log_data)

# Usage
logger = logging.getLogger(__name__)
logger.info('User logged in', extra={'user_id': '123', 'request_id': 'abc'})
```

**Problems:**
- No distributed tracing (can't follow requests across services)
- Manual correlation (grep for request_id)
- No performance metrics (only logs)
- Limited tooling (command-line analysis)

### Migration to OpenTelemetry

**Step 1: Add OpenTelemetry Tracing (2-3 hours)**

```python
# Install
pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp

# Setup
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

# Configure
resource = Resource.create({"service.name": "user-service"})
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(
    OTLPSpanExporter(endpoint="http://localhost:4317")
)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

# Usage (replaces manual request_id logging)
@app.route('/api/users/<user_id>')
def get_user(user_id):
    with tracer.start_as_current_span("get_user") as span:
        span.set_attribute("user.id", user_id)

        # Your code here
        user = fetch_user(user_id)

        span.set_attribute("user.country", user.country)
        return jsonify(user)
```

**Benefits gained:**
- ✅ Automatic request correlation (trace_id, span_id)
- ✅ Distributed tracing across services
- ✅ Performance timing (automatic duration tracking)
- ✅ Structured context (spans with attributes)

**Step 2: Add Auto-Instrumentation (30 min)**

```python
# Auto-instrument framework
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI()
FastAPIInstrumentor().instrument_app(app)

# Auto-instruments:
# - All HTTP requests/responses
# - Database queries (via SQLAlchemy, psycopg2, etc.)
# - Redis calls
# - HTTP client calls (requests, httpx)
# - Async tasks (Celery)
```

**Benefits gained:**
- ✅ Zero-code instrumentation for common libraries
- ✅ Database query tracing
- ✅ External API call tracing
- ✅ Async task tracing

**Step 3: Migrate Custom Logs to Spans (1-2 hours)**

```python
# Before (custom logging):
logger.info('Processing payment', extra={
    'user_id': user_id,
    'amount': amount,
    'currency': currency,
})

# After (OpenTelemetry spans):
with tracer.start_as_current_span("process_payment") as span:
    span.set_attribute("user.id", user_id)
    span.set_attribute("payment.amount", amount)
    span.set_attribute("payment.currency", currency)

    # Process payment
    result = payment_gateway.charge(amount, currency)

    span.set_attribute("payment.status", result.status)
```

**Benefits gained:**
- ✅ Logs are now part of trace (contextual)
- ✅ Hierarchical structure (parent/child spans)
- ✅ Automatic timing of operations
- ✅ Errors automatically captured

**Step 4: Deploy Backend (1-2 hours)**

**Option A: Managed (Grafana Cloud, Honeycomb)**
- Sign up: 10 min
- Configure exporter endpoint: 10 min
- Deploy: 10 min
- Total: 30 min

**Option B: Self-Hosted (Jaeger)**
```bash
# Docker Compose
docker-compose up -d jaeger

# Or Kubernetes
kubectl apply -f jaeger-all-in-one.yaml

# Total: 1-2 hours
```

### Total Migration Time: 3-4 hours (for one service)

**Time Breakdown:**
- Setup OpenTelemetry SDK: 30 min
- Add manual instrumentation: 1 hour
- Add auto-instrumentation: 30 min
- Migrate custom logs: 1 hour
- Deploy backend: 30-60 min
- Testing: 30 min

### Break-Even Analysis

**Cost of DIY Logging:**
- Development time: ~2 hours/month maintaining custom logging
- Debugging time: ~5 hours/month grepping logs for issues
- **Total: 7 hours/month = $1,050/month (@ $150/hr)**

**Cost of OpenTelemetry:**
- Setup: 4 hours ($600 one-time)
- Backend: $0-100/month (self-hosted) or $200-500/month (managed)
- Maintenance: ~1 hour/month ($150/month)

**Break-even:**
```
One-time cost: $600
Monthly savings: $1,050 - $150 - $300 (backend) = $600/month

Break-even: $600 / $600 = 1 month
```

**Verdict:** Pays for itself in 1 month. **Strong recommend.**

### Decision Criteria

**Migrate if:**
- ✅ Have 2+ services (distributed tracing valuable)
- ✅ Spend >3 hours/month debugging with logs
- ✅ Growing complexity (more services planned)

**Stay with DIY if:**
- ❌ Single monolith (no distributed system)
- ❌ <10 errors/month (minimal debugging)
- ❌ Shutting down project in <6 months

## Path 2: Sentry → OpenTelemetry

### Current State: Sentry SDK

**Typical Setup:**
```python
import sentry_sdk

sentry_sdk.init(
    dsn="https://...@sentry.io/...",
    traces_sample_rate=1.0,
)

# Error tracking
try:
    risky_operation()
except Exception as e:
    sentry_sdk.capture_exception(e)

# Custom transaction
with sentry_sdk.start_transaction(name="payment_flow"):
    process_payment()
```

**Current Cost:**
- Free tier: $0/month (5K errors)
- Team tier: $29/month (10K errors)
- Business tier: $99/month (50K errors)

### Migration to OpenTelemetry + Backend

**Option A: Keep Sentry as Backend (via OTLP)**

Sentry supports OpenTelemetry ingestion, so you can:
1. Replace Sentry SDK with OpenTelemetry SDK
2. Export to Sentry via OTLP
3. Keep using Sentry UI

**Migration Steps:**

**Step 1: Install OpenTelemetry (30 min)**
```python
# Remove Sentry SDK
pip uninstall sentry-sdk

# Install OpenTelemetry
pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp

# Configure for Sentry
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

provider = TracerProvider()
processor = BatchSpanProcessor(
    OTLPSpanExporter(
        endpoint="https://o123456.ingest.sentry.io/api/7890123/envelope/",
        headers={"Authorization": f"Bearer {SENTRY_AUTH_TOKEN}"}
    )
)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
```

**Step 2: Migrate Error Tracking (2-3 hours per service)**
```python
# Before (Sentry):
try:
    risky_operation()
except Exception as e:
    sentry_sdk.capture_exception(e)
    sentry_sdk.set_context("user", {"id": user_id, "email": email})

# After (OpenTelemetry):
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

try:
    with tracer.start_as_current_span("risky_operation") as span:
        span.set_attribute("user.id", user_id)
        span.set_attribute("user.email", email)
        risky_operation()
except Exception as e:
    span = trace.get_current_span()
    span.record_exception(e)
    span.set_status(StatusCode.ERROR, str(e))
    raise  # Re-raise to let error propagate
```

**Step 3: Migrate Transactions (1-2 hours)**
```python
# Before (Sentry):
with sentry_sdk.start_transaction(name="payment_flow") as transaction:
    transaction.set_tag("user_id", user_id)
    process_payment()

# After (OpenTelemetry):
with tracer.start_as_current_span("payment_flow") as span:
    span.set_attribute("user.id", user_id)
    process_payment()
```

**Step 4: Deploy (30 min)**
- Update environment variables
- Deploy to production
- Validate errors appear in Sentry

**Total Migration Time: 20-30 hours (for typical app with 3-5 services)**

**Time Breakdown:**
- Planning: 2 hours
- Service 1 migration: 5 hours
- Service 2 migration: 4 hours (learning curve)
- Service 3-5 migration: 3 hours each (9 hours total)
- Testing: 4 hours
- Documentation: 2 hours

**Option B: Switch to Different Backend**

If migrating away from Sentry entirely:

**Popular Alternatives:**
- **Grafana Cloud**: $0.50/GB traces (~$300-800/mo)
- **Honeycomb**: $0.50/M events (~$200-600/mo)
- **Axiom**: $0.25/GB (~$200-500/mo)
- **Self-hosted Jaeger**: $50-200/mo infrastructure

**Additional Migration Time:** +10-15 hours
- Set up new backend: 3-5 hours
- Recreate dashboards: 5-8 hours
- Migrate alerting: 2-3 hours

**Total Migration Time: 30-45 hours**

### Break-Even Analysis

**Scenario: Sentry Business Plan ($99/month)**

**Option A: OTel + Sentry Backend**
- Migration cost: 25 hours × $150/hr = $3,750
- Ongoing cost: $99/month (same Sentry plan)
- Benefit: Can switch backends later (2 hours work)
- Break-even: Only if you later switch backends

**Future switching value:**
```
P(need to switch) = 30% (over 3 years)
Switching cost saved = 30 hours × $150 = $4,500
Present value = 0.3 × $4,500 = $1,350

ROI = $1,350 / $3,750 = 36% (marginal)
```

**Option B: OTel + Cheaper Backend**
- Migration cost: 40 hours × $150/hr = $6,000
- Old cost: $99/month Sentry
- New cost: $50/month (self-hosted Jaeger + $200/mo managed alternative)
- Monthly savings: $49/month

**Break-even:**
```
One-time cost: $6,000
Monthly savings: $49/month

Break-even: $6,000 / $49 = 122 months (10 years)
```

**Verdict:** Not worth it for cost alone.

**Option C: OTel + Much Cheaper Backend (High Volume)**

If Sentry is expensive due to volume:
- Current Sentry: $799/month (Enterprise plan)
- Self-hosted OTel: $300/month
- Monthly savings: $499/month

**Break-even:**
```
One-time cost: $6,000
Monthly savings: $499/month

Break-even: $6,000 / $499 = 12 months
```

**Verdict:** Worth it if Sentry >$500/month.

### Decision Criteria

**Migrate from Sentry if:**
- ✅ Sentry cost >$500/month (cost optimization)
- ✅ Multi-service architecture (distributed tracing valuable)
- ✅ Want vendor independence (strategic)
- ✅ Need features Sentry doesn't have (custom backends)

**Stay on Sentry if:**
- ❌ Cost <$100/month (migration not worth it)
- ❌ Love Sentry UX (best-in-class error tracking)
- ❌ Small team (<5 engineers) (complexity not worth it)
- ❌ Single service (distributed tracing not needed)

## Path 3: Datadog → OpenTelemetry

### Current State: Datadog APM

**Typical Setup:**
```python
from ddtrace import tracer

# Auto-instrumentation (Datadog agent)
# ddtrace-run python app.py

# Manual instrumentation
@tracer.wrap(service="user-service", resource="get_user")
def get_user(user_id):
    span = tracer.current_span()
    span.set_tag("user.id", user_id)
    # ...
```

**Current Cost (example):**
- 10 hosts × $31/host = $310/month
- APM for 8 services × $800/service = $6,400/month
- Logs 500GB × $3/GB = $1,500/month
- **Total: $8,210/month = $98,520/year**

### Migration to OpenTelemetry

**Step 1: Parallel Instrumentation (Week 1-2, 40-60 hours)**

Run Datadog and OpenTelemetry in parallel:

```python
# Keep Datadog (during transition)
from ddtrace import tracer as dd_tracer

# Add OpenTelemetry
from opentelemetry import trace as otel_trace

otel_tracer = otel_trace.get_tracer(__name__)

# Instrument with both (temporarily)
def get_user(user_id):
    # Datadog span
    with dd_tracer.trace("get_user"):
        # OpenTelemetry span
        with otel_tracer.start_as_current_span("get_user") as span:
            span.set_attribute("user.id", user_id)
            # Your code
```

**Benefits:**
- ✅ Zero risk: Datadog still working
- ✅ Validation: Compare traces between systems
- ✅ Gradual rollout: Service by service

**Cost during parallel period:** ~$10K/month (Datadog + OTel backend)

**Step 2: Deploy OpenTelemetry Collector (Week 1, 10-15 hours)**

```yaml
# OTel Collector configuration
receivers:
  otlp:
    protocols:
      grpc:
      http:

processors:
  batch:
    timeout: 10s

  # Sampling to control costs
  probabilistic_sampler:
    sampling_percentage: 20

exporters:
  # Export to managed backend (e.g., Grafana Cloud)
  otlp/grafana:
    endpoint: "https://otlp-gateway.grafana.net/otlp"
    headers:
      authorization: "Bearer ${GRAFANA_API_KEY}"

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, probabilistic_sampler]
      exporters: [otlp/grafana]
```

**Step 3: Migrate Services (Week 2-4, 60-100 hours)**

Migrate one service at a time:

```python
# Remove Datadog instrumentation
# from ddtrace import tracer  # DELETE

# Add OpenTelemetry
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Setup (once per service)
provider = TracerProvider(
    resource=Resource.create({"service.name": "user-service"})
)
processor = BatchSpanProcessor(
    OTLPSpanExporter(endpoint="http://otel-collector:4317")
)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Auto-instrumentation (replaces ddtrace-run)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
FastAPIInstrumentor().instrument_app(app)

# Manual instrumentation (updated)
tracer = trace.get_tracer(__name__)

def get_user(user_id):
    with tracer.start_as_current_span("get_user") as span:
        span.set_attribute("user.id", user_id)
        # Your code
```

**Migrate in order:**
1. Least critical service (test migration process)
2. Medium complexity services (build confidence)
3. Critical services (well-validated migration)

**Time per service:**
- Simple service (REST API): 6-8 hours
- Complex service (many custom spans): 10-15 hours
- Very complex (custom metrics, etc.): 20-30 hours

**Step 4: Migrate Dashboards (Week 4-5, 30-40 hours)**

Recreate Datadog dashboards in new backend:

```
Datadog Dashboard: Service Overview
├─ Request rate
├─ Error rate
├─ Latency (p50, p95, p99)
├─ Apdex score
└─ Dependency map

Grafana Equivalent:
├─ Panel: Request rate (PromQL query)
├─ Panel: Error rate (PromQL query)
├─ Panel: Latency heatmap
├─ Panel: Service graph
└─ Alerts: Same thresholds
```

**Step 5: Decommission Datadog (Week 6, 5-10 hours)**

- Remove Datadog agents
- Cancel Datadog subscription
- Archive historical Datadog data (if needed)
- Update documentation

### Total Migration Time: 150-200 hours (1-1.5 months for team of 3-4)

**Time Breakdown:**
- Planning & setup: 20 hours
- OTel Collector deployment: 15 hours
- Migrate 8 services: 80 hours (10 hrs/service avg)
- Dashboard migration: 35 hours
- Testing & validation: 30 hours
- Documentation: 10 hours
- Decommission Datadog: 10 hours

### Cost Analysis

**Current State (Datadog):**
- Monthly: $8,210
- Annual: $98,520

**Migration Cost:**
- Labor: 175 hours × $150/hr = $26,250
- Parallel period (2 months): 2 × $1,500 = $3,000 (OTel backend during overlap)
- **Total one-time: $29,250**

**New State (OpenTelemetry + Grafana Cloud):**
- Grafana Cloud: $1,200/month
- Maintenance: 5 hours/month × $150 = $750/month
- **Total monthly: $1,950**

**Savings:**
- Monthly: $8,210 - $1,950 = $6,260/month
- Annual: $75,120/year

**Break-even:**
```
One-time cost: $29,250
Monthly savings: $6,260

Break-even: $29,250 / $6,260 = 4.7 months
```

**3-Year Savings:**
```
Year 1: $75,120 - $29,250 = $45,870
Year 2: $75,120
Year 3: $75,120

Total 3-year savings: $196,110
```

**ROI:** 670% over 3 years ($196K savings / $29K cost)

### Decision Criteria

**Migrate from Datadog if:**
- ✅ Datadog cost >$3K/month (strong ROI)
- ✅ Team has 40+ hours/month for 1-2 months (capacity for migration)
- ✅ Want vendor independence (strategic value)
- ✅ Growing cost concern (exponential growth trajectory)

**Optimize Datadog first if:**
- ⚠️ Haven't implemented sampling (can reduce cost 50-80%)
- ⚠️ Haven't removed unused metrics (easy wins)
- ⚠️ Running on high sampling rate (100% → 10%)

**Stay on Datadog if:**
- ❌ Cost <$1K/month (migration not worth effort)
- ❌ Team <3 engineers (complexity not worth it)
- ❌ Love Datadog UX (willing to pay premium)
- ❌ Short-term project (<2 years)

## Path 4: Backend Switching (OpenTelemetry to OpenTelemetry)

### Scenario: Already using OpenTelemetry

**Current State:**
```python
# App code (instrumented with OpenTelemetry)
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

@app.route('/api/users')
def get_users():
    with tracer.start_as_current_span("get_users"):
        # Your code
        ...
```

**Current Backend:** Jaeger (self-hosted)
**New Backend:** Grafana Cloud (managed)

### Migration Time: 1-3 hours (!!)

**Step 1: Add New Exporter (30 min)**

```python
# Add Grafana Cloud exporter (alongside existing Jaeger)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Keep Jaeger temporarily
jaeger_exporter = JaegerExporter(...)

# Add Grafana Cloud
grafana_exporter = OTLPSpanExporter(
    endpoint="https://otlp-gateway.grafana.net/otlp",
    headers={"Authorization": f"Bearer {GRAFANA_API_KEY}"}
)

# Export to both (during validation)
provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
provider.add_span_processor(BatchSpanProcessor(grafana_exporter))
```

**Step 2: Validate (1 hour)**
- Check traces appear in Grafana Cloud
- Compare trace quality (Jaeger vs Grafana)
- Validate dashboards work

**Step 3: Remove Old Exporter (30 min)**
```python
# Remove Jaeger exporter
# provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))  # DELETE

# Keep only Grafana
provider.add_span_processor(BatchSpanProcessor(grafana_exporter))
```

**Step 4: Decommission Old Backend (1 hour)**
- Shut down Jaeger
- Archive historical data
- Update documentation

### Total Migration Time: 2-3 hours

**This is the POWER of OpenTelemetry: Backend switching is trivial.**

### Cost Comparison

**Jaeger (self-hosted):**
- Infrastructure: $300/month
- Maintenance: 8 hours/month × $150 = $1,200/month
- **Total: $1,500/month**

**Grafana Cloud:**
- Subscription: $800/month
- Maintenance: 2 hours/month × $150 = $300/month
- **Total: $1,100/month**

**Savings:** $400/month = $4,800/year

**Migration cost:** 3 hours × $150 = $450

**Break-even:** 1.1 months (immediate ROI)

## Summary: Migration Decision Matrix

| Current State | Target State | Time | Cost | Break-Even | Recommend? |
|--------------|-------------|------|------|-----------|------------|
| DIY Logging | OTel + Managed | 3-4 hrs | $600 + $300/mo | 1 month | ✅ Yes |
| Sentry (<$100/mo) | OTel + Backend | 25 hrs | $3,750 | Never (for cost) | ❌ No |
| Sentry (>$500/mo) | OTel + Backend | 40 hrs | $6,000 | 12 months | ✅ Yes |
| Datadog (<$1K/mo) | OTel + Managed | 150 hrs | $25K | 18+ months | ⚠️ Maybe |
| Datadog (>$3K/mo) | OTel + Managed | 150 hrs | $25K | 4-5 months | ✅ Yes |
| Jaeger | Grafana Cloud | 3 hrs | $450 | 1 month | ✅ Yes |
| Grafana Cloud | Honeycomb | 2 hrs | $300 | 1-2 months | ✅ Easy |

## Key Insights

### 1. Backend Switching is OpenTelemetry's Superpower

**Without OpenTelemetry:**
- Sentry → Datadog: 40-60 hours (rewrite instrumentation)
- Datadog → New Relic: 60-80 hours (different SDK)

**With OpenTelemetry:**
- Any backend → Any backend: 2-3 hours (change exporter)

This is worth $5K-10K in saved migration costs **every time you switch**.

### 2. Break-Even Gets Better Over Time

Year 1: Pay migration cost
Year 2+: Pure savings

The longer your time horizon, the better OpenTelemetry ROI.

### 3. Start with Managed Backend

Don't self-host initially:
- Faster setup (2-3 hours vs 20-30 hours)
- Lower maintenance (2 hrs/mo vs 8 hrs/mo)
- Can always switch to self-hosted later (if cost justified)

Managed → Self-hosted is easy. Self-hosted → Managed is easy. Start with simplicity.

### 4. Migration Doesn't Have to Be All-or-Nothing

**Hybrid approaches work:**
- OTel for new services, Datadog for legacy
- OTel for traces, Sentry for errors
- Gradual service-by-service migration

This reduces risk and spreads migration effort over time.

## Conclusion

**OpenTelemetry is worth migrating to if:**
1. Current observability cost >$500/month (cost optimization)
2. Multi-service architecture (distributed tracing value)
3. >2 year time horizon (long-term ROI)
4. Vendor independence matters (strategic)

**The best migration path:**
1. Start with high-cost scenario (migrate from expensive Datadog)
2. Use managed backend initially (Grafana Cloud, Honeycomb)
3. Migrate service-by-service (gradual, low risk)
4. Optimize backend later (can switch easily)

**The migration investment pays for itself through:**
- Reduced monthly observability costs (50-85% savings)
- Future flexibility (2-hour backend switches vs 40-hour migrations)
- Better observability (distributed tracing, better tooling)

Total 3-year ROI: **300-700%** for most organizations.
