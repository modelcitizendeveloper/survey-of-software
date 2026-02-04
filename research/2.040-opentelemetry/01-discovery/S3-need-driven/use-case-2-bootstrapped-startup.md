# Use Case 2: Bootstrapped Startup with Growing Traffic

## Scenario Profile

**Context:**
- 2-4 person engineering team
- 100-500 errors/month, 5K-20K daily active users
- 2-3 services (API, background jobs, maybe separate admin app)
- Product-market fit achieved, now scaling
- Profitable or close to it, watching costs carefully
- 12-24 month runway, planning for growth

**Example:**
TechCo has 3 engineers building a B2B SaaS product. They launched 8 months ago and have 200 paying customers. They're using Sentry's free tier but approaching the limit. They have a FastAPI backend, Celery workers, and a Next.js admin portal. They're evaluating whether to upgrade Sentry ($29/mo) or invest time in OpenTelemetry.

## Requirements Analysis

### Functional Requirements

**Must Have:**
- Error tracking across all services (API, workers, frontend)
- Performance monitoring for slow API endpoints
- Request correlation across services
- User impact assessment (which customers affected?)
- Alert fatigue management (group similar errors)

**Nice to Have:**
- Distributed tracing (understand cross-service flows)
- Custom dashboards (SLA monitoring)
- Log aggregation (centralized search)
- Database query performance

**Don't Need (Yet):**
- APM for 10+ services
- Advanced sampling strategies
- Custom retention policies
- Multi-tenant isolation

### Non-Functional Requirements

**Setup Time:** 1-2 days acceptable
- Team can allocate sprint time to infrastructure
- One engineer can own the migration

**Ongoing Maintenance:** <2 hours/month
- Monitoring the monitoring is overhead
- Some maintenance acceptable if saves money

**Budget:** $50-200/month for observability
- Free tier outgrown
- $500/month Datadog budget out of reach
- Willing to pay for value, not for brand

**Vendor Lock-in Concern:** MEDIUM
- 2-3 year horizon (planning for sustainability)
- Want option to optimize costs later
- Don't want to rebuild instrumentation if switching

## Solution Evaluation

### Option A: Upgrade Sentry to Paid Plan

**Pricing:**
- Team plan: $29/month (10K errors, 100K transactions)
- Business plan: $99/month (50K errors, 500K transactions, advanced features)

**Setup Process:**
```python
# Already using Sentry - just upgrade plan
# No code changes needed
# Add more instrumentation for tracing:

import sentry_sdk

sentry_sdk.init(
    dsn="...",
    traces_sample_rate=0.1,  # 10% sampling to stay in budget
    profiles_sample_rate=0.1,
)

# Add custom spans for important operations
with sentry_sdk.start_span(op="database", description="User lookup"):
    user = db.query(User).filter_by(id=user_id).first()
```

**Total Setup Time:** 2-3 hours
- Enable tracing features: 1 hour
- Add custom instrumentation: 1-2 hours
- Test across services: 30 min

**Pros:**
- ✅ Zero migration: Already using Sentry
- ✅ Quick setup: Afternoon of work
- ✅ Great UX: Best-in-class error dashboard
- ✅ Performance insights: Included in paid tier
- ✅ Multi-service support: Works across stack

**Cons:**
- ⚠️ Cost scaling: $99/mo → $299/mo as you grow
- ⚠️ Vendor lock-in: Deeper integration = harder migration
- ⚠️ Limited customization: Can't self-host if needed

**Total Cost Year 1:** $600-1,200 (Team plan)

### Option B: OpenTelemetry + Self-Hosted Backend (Jaeger)

**Setup Process:**

```python
# 1. Install OTel SDK in each service (30 min per service)
pip install opentelemetry-distro opentelemetry-exporter-otlp

# 2. Configure instrumentation (FastAPI example)
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Set up tracer provider
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://jaeger:4317"))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Auto-instrument FastAPI
FastAPIInstrumentor().instrument_app(app)

# 3. Deploy Jaeger (Docker Compose)
# docker-compose.yml
services:
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"  # UI
      - "4317:4317"    # OTLP gRPC
      - "4318:4318"    # OTLP HTTP
    environment:
      - COLLECTOR_OTLP_ENABLED=true
```

**Total Setup Time:** 8-12 hours
- Learn OTel concepts: 2-3 hours
- Instrument 3 services: 2-3 hours
- Deploy Jaeger: 1-2 hours
- Configure collection pipeline: 1 hour
- Test & debug: 2-3 hours
- Document for team: 1 hour

**Pros:**
- ✅ Low cost: $20-40/month (hosting Jaeger)
- ✅ Vendor independence: Can switch backends easily
- ✅ Full control: Customize everything
- ✅ No data limits: Process as many traces as you want

**Cons:**
- ❌ High setup cost: 8-12 hours vs 2-3 hours
- ❌ Ongoing maintenance: Updating Jaeger, managing storage
- ❌ Error tracking gap: Jaeger doesn't do errors well
- ❌ Learning curve: Team needs to learn new tools
- ⚠️ Self-hosting burden: One more thing to monitor

**Total Cost Year 1:**
- Setup: $800-1,200 (12 hours × $100/hr)
- Hosting: $240-480 ($20-40/mo × 12)
- Maintenance: $600-1,200 (1hr/mo × 12 × $100/hr)
- **Total: $1,640-2,880**

### Option C: OpenTelemetry + Managed Backend (Sentry via OTLP)

**Setup Process:**

```python
# 1. Install OTel SDK (same as Option B)
pip install opentelemetry-distro opentelemetry-exporter-otlp

# 2. Configure to send to Sentry's OTLP endpoint
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

provider = TracerProvider()
processor = BatchSpanProcessor(
    OTLPSpanExporter(
        endpoint="https://o123456.ingest.sentry.io/api/7890123/envelope/",
        headers={"Authorization": "Bearer YOUR_TOKEN"}
    )
)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# 3. Auto-instrument
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
FastAPIInstrumentor().instrument_app(app)
```

**Total Setup Time:** 6-8 hours
- Learn OTel concepts: 2 hours
- Instrument 3 services: 2-3 hours
- Configure Sentry OTLP: 1 hour
- Test & debug: 1-2 hours
- Document for team: 1 hour

**Pros:**
- ✅ Vendor independence: Can switch from Sentry later
- ✅ No infrastructure: Managed backend
- ✅ Best of both: Standard instrumentation + great UX
- ✅ Future-proof: Easy to add more backends

**Cons:**
- ⚠️ Higher setup: 6-8 hours vs 2-3 hours
- ⚠️ Same Sentry cost: Still paying $99/month
- ⚠️ Potential gaps: OTLP support may lag native SDK features

**Total Cost Year 1:**
- Setup: $600-800 (8 hours × $100/hr)
- Sentry subscription: $1,188 ($99/mo × 12)
- **Total: $1,788-1,988**

### Option D: OpenTelemetry + Hybrid (Jaeger for traces, Sentry for errors)

**Setup Process:**

```python
# Configure multiple exporters
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

provider = TracerProvider()

# Export traces to Jaeger (self-hosted)
jaeger_exporter = OTLPSpanExporter(endpoint="http://jaeger:4317")
provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))

# Still use Sentry SDK for errors (for now)
import sentry_sdk
sentry_sdk.init(dsn="...", traces_sample_rate=0.0)  # Errors only
```

**Total Setup Time:** 10-14 hours
- Set up OTel for tracing: 8-10 hours
- Configure Sentry for errors only: 1 hour
- Integrate both systems: 2-3 hours

**Pros:**
- ✅ Cost optimization: Free tier Sentry + cheap Jaeger
- ✅ Best tool for each job: Sentry errors, Jaeger tracing
- ✅ Learning investment: Team learns OTel gradually

**Cons:**
- ❌ Complexity: Two systems to manage
- ❌ Correlation gap: Errors and traces not automatically linked
- ⚠️ Maintenance burden: Double the infrastructure

**Total Cost Year 1:**
- Setup: $1,200-1,400 (14 hours × $100/hr)
- Jaeger hosting: $480 ($40/mo × 12)
- Sentry free tier: $0
- Maintenance: $1,200 (1hr/mo × 12 × $100/hr)
- **Total: $2,880-3,080**

## Requirement Fit Analysis

| Requirement | Sentry Paid | OTel+Jaeger | OTel+Sentry | OTel Hybrid |
|-------------|-------------|-------------|-------------|-------------|
| Error tracking | ✅ Excellent | ⚠️ Poor | ✅ Excellent | ✅ Good |
| Performance monitoring | ✅ Good | ✅ Excellent | ✅ Good | ✅ Excellent |
| Multi-service tracing | ✅ Good | ✅ Excellent | ✅ Good | ✅ Excellent |
| User impact | ✅ Built-in | ⚠️ Manual | ✅ Built-in | ✅ Built-in |
| Setup <2 days | ✅ 3 hours | ⚠️ 12 hours | ✅ 8 hours | ❌ 14 hours |
| Maintenance <2hrs/mo | ✅ 0 hours | ⚠️ 2-3 hours | ✅ 0 hours | ⚠️ 2-3 hours |
| Budget <$200/mo | ⚠️ $99/mo | ✅ $40/mo | ⚠️ $99/mo | ✅ $40/mo |
| Vendor independence | ❌ Locked | ✅ Full | ✅ Full | ✅ Full |
| **Total Score** | **7/10** | **6/10** | **8/10** | **7/10** |

## Recommendation: OpenTelemetry + Managed Backend (Option C)

### Why OpenTelemetry Makes Sense Here

**1. Optionality Value Becomes Positive**

```
P(need_to_switch) = 40% (2-3 year horizon, cost pressure)
Switching cost saved = $4,000 (40 hours) - $100 (1 hour) = $3,900
Time horizon discount = 0.8 (longer runway)

Optionality Value = 0.4 × $3,900 × 0.8 = $1,248

Setup cost = 7 hours × $100/hr = $700

ROI = ($1,248 - $700) / $700 = 78% (POSITIVE)
```

The optionality is worth $1,248, and costs $700 to acquire. Good investment.

**2. Cost Scaling Matters**

Current Sentry cost trajectory:
- Today: $99/month (50K errors, 500K transactions)
- 6 months: $299/month (outgrow Business plan)
- 12 months: $799/month (need Enterprise features)

With OTel, backend switching becomes viable:
- Start with Sentry: $99/month
- Switch to self-hosted if >$200/month
- Or try cheaper managed options (Axiom, Honeycomb free tier)

**3. Team Can Absorb Setup Cost**

With 2-4 engineers, allocating 1-2 days for infrastructure is reasonable. This is a one-time investment that pays dividends over 2-3 years.

**4. Multi-Service Architecture Benefits**

With 2-3 services now and likely 5-7 in a year, distributed tracing becomes critical. OTel's auto-instrumentation shines here.

### Implementation Strategy

**Phase 1: Start with OTel + Sentry (Weeks 1-2)**

Migrate existing Sentry setup to OpenTelemetry:

```python
# Before (Sentry SDK):
import sentry_sdk
sentry_sdk.init(dsn="...")
sentry_sdk.capture_exception(error)

# After (OpenTelemetry):
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Auto-instrumentation handles most cases
FastAPIInstrumentor().instrument_app(app)

# Manual instrumentation when needed
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("payment_processing"):
    # Errors automatically captured
    process_payment(order)
```

**Phase 2: Evaluate Backends (Month 3)**

After 90 days with OTel, evaluate:
- Is Sentry cost acceptable? (If yes, stay)
- Can we self-host Jaeger for <$100/month? (If yes, consider switch)
- Does another managed provider fit better? (Axiom, Honeycomb, etc.)

**Phase 3: Optimize (Month 6)**

Once comfortable with OTel:
- Add custom instrumentation for critical paths
- Implement sampling strategies (if cost issue)
- Consider hybrid approach (cheap backend for high-volume data)

### Success Criteria

**Month 1:**
- All 3 services instrumented with OTel
- Traces flowing to Sentry backend
- Error tracking still working
- Team understands OTel basics

**Month 3:**
- Reduced time to debug multi-service issues
- Cost still <$150/month
- Option to switch backends validated (test with Jaeger locally)

**Month 6:**
- Backend switch decision made (stay or move)
- If switched: Migration took <4 hours
- If stayed: Comfortable with decision knowing alternatives exist

## Alternative Path: Defer If Cash-Constrained

If the team is extremely cash-constrained and can't allocate 8 hours:

**Short-term:** Stay on Sentry Team plan ($29/month)
- Limit sampling to stay under limits
- Manually correlate multi-service issues
- Defer investment until Series A or profitability

**Trigger to revisit:**
- Sentry cost >$200/month
- Team grows to 5+ engineers (setup cost amortized)
- Multi-service debugging takes >2 hours/week

## Conclusion

For bootstrapped startups with 2-4 engineers and growing traffic, **OpenTelemetry investment starts making sense**. The 8-hour setup cost is justified by:

1. **Positive optionality ROI**: 78% return on investment
2. **Cost scaling control**: Can switch backends when Sentry gets expensive
3. **Multi-service reality**: Distributed tracing becomes necessary
4. **Team capacity**: Can absorb 1-2 day infrastructure project

Start with OpenTelemetry + Sentry to preserve optionality while maintaining the excellent error tracking UX. Re-evaluate backend choice at 3 and 6 months based on cost trajectory.

This is the **inflection point** where OpenTelemetry transitions from premature optimization to prudent investment.
