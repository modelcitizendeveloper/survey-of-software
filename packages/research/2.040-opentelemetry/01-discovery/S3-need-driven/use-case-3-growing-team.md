# Use Case 3: Growing Team with Distributed Services

## Scenario Profile

**Context:**
- 5-15 person engineering team across 2-3 squads
- 500-5,000 errors/month, 50K-200K daily active users
- 5-10 microservices (API gateway, user service, payment service, notification service, etc.)
- Established product, optimizing for growth and reliability
- Series A funded or strongly profitable
- SLA commitments to customers (99.9% uptime)

**Example:**
GrowthCorp has 8 engineers building a fintech platform. They have 5 microservices in production, with plans to add 3 more this quarter. They're currently on Datadog ($800/month) and finding it expensive, but they need sophisticated distributed tracing. They're evaluating whether OpenTelemetry can reduce costs while maintaining observability.

## Requirements Analysis

### Functional Requirements

**Must Have:**
- Distributed tracing across all services (understand request flows)
- Service dependency mapping (which service calls which?)
- Error attribution (which service caused the failure?)
- Performance bottleneck identification (slowest span in trace)
- SLA monitoring (p95, p99 latencies per service)
- Alert routing to correct team (user-service team vs payment-service team)

**Nice to Have:**
- Custom business metrics (conversion rate per endpoint)
- Log correlation with traces (see logs for specific trace)
- Database query analysis (slow queries per service)
- Deployment markers (correlate performance changes with deploys)
- Cost attribution per service (which team's service is expensive?)

**Critical:**
- Multi-tenant isolation (if SaaS with enterprise customers)
- Compliance logging (if handling PII, financial data)
- Incident retrospectives (what happened during outage?)

### Non-Functional Requirements

**Setup Time:** 1-2 weeks acceptable
- Can dedicate infrastructure sprint
- Platform team can own rollout
- Gradual service-by-service migration

**Ongoing Maintenance:** 4-8 hours/month
- Platform engineer owns observability
- Maintenance acceptable if significantly cheaper

**Budget:** $500-2,000/month for observability
- Current Datadog cost: $800/month and growing
- Willing to pay for value, but $3K+/month concerning
- Developer time expensive ($150/hr loaded cost)

**Vendor Lock-in Concern:** HIGH
- 3-5 year horizon (established company)
- Vendor acquisition risk (happened to Lightstep, Honeycomb talks)
- Cost optimization important (show ROI to investors/board)
- Multi-cloud strategy (AWS today, maybe GCP/Azure later)

## Solution Evaluation

### Option A: Stay on Datadog (Status Quo)

**Current State:**
- All services instrumented with Datadog APM
- Excellent distributed tracing UI
- Log aggregation included
- Infrastructure monitoring integrated

**Pricing Trajectory:**
- Today: $800/month (8 hosts, APM for 5 services)
- 6 months: $1,500/month (15 hosts, 10 services, more logs)
- 12 months: $2,800/month (25 hosts, 15 services, retention increases)
- 24 months: $5,000+/month (scale continues)

**Pros:**
- ✅ Zero migration: Already working
- ✅ Best-in-class UX: Excellent dashboards
- ✅ All-in-one: APM + logs + infrastructure
- ✅ Team knows it: No learning curve

**Cons:**
- ❌ Cost scaling: Exponential with growth
- ❌ Vendor lock-in: Deep integration, hard to leave
- ❌ Usage anxiety: Developers limit instrumentation to control costs
- ⚠️ Acquisition risk: Cisco acquired Datadog competitors

**Total Cost Year 1:** $14,400 (average $1,200/month)
**Total Cost Year 2:** $36,000 (average $3,000/month)

### Option B: OpenTelemetry + Self-Hosted (Jaeger + Tempo)

**Migration Strategy:**

```python
# 1. Set up collection infrastructure (Week 1)
# Deploy OpenTelemetry Collector
# docker-compose.yml
services:
  otel-collector:
    image: otel/opentelemetry-collector-contrib:latest
    volumes:
      - ./otel-collector-config.yaml:/etc/otel-collector-config.yaml
    command: ["--config=/etc/otel-collector-config.yaml"]
    ports:
      - "4317:4317"  # OTLP gRPC
      - "4318:4318"  # OTLP HTTP

  # Jaeger for traces
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"

  # Grafana Tempo for long-term trace storage
  tempo:
    image: grafana/tempo:latest
    volumes:
      - ./tempo.yaml:/etc/tempo.yaml
      - tempo-data:/var/tempo
    ports:
      - "3200:3200"

# 2. Instrument services (Week 2-3, parallel)
# Service 1: API Gateway (Python/FastAPI)
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

provider = TracerProvider(
    resource=Resource.create({"service.name": "api-gateway"})
)
processor = BatchSpanProcessor(
    OTLPSpanExporter(endpoint="http://otel-collector:4317")
)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

FastAPIInstrumentor().instrument_app(app)

# Service 2: User Service (Node.js/Express)
const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-grpc');
const { registerInstrumentations } = require('@opentelemetry/instrumentation');
const { HttpInstrumentation } = require('@opentelemetry/instrumentation-http');
const { ExpressInstrumentation } = require('@opentelemetry/instrumentation-express');

const provider = new NodeTracerProvider({
  resource: { attributes: { 'service.name': 'user-service' } }
});

provider.addSpanProcessor(
  new BatchSpanProcessor(
    new OTLPTraceExporter({ url: 'http://otel-collector:4317' })
  )
);

provider.register();

registerInstrumentations({
  instrumentations: [
    new HttpInstrumentation(),
    new ExpressInstrumentation(),
  ],
});

# Repeat for remaining 8 services...
```

**Total Setup Time:** 80-120 hours (2-3 weeks)
- Infrastructure setup: 20-30 hours
  - OTel Collector configuration: 8 hours
  - Jaeger/Tempo deployment: 4 hours
  - Grafana dashboards: 8-10 hours
  - Testing collection pipeline: 8 hours
- Service instrumentation: 40-60 hours
  - 8 hours per service × 5 services: 40 hours
  - Testing & debugging: 20 hours
- Migration from Datadog: 20-30 hours
  - Remove Datadog agents: 10 hours
  - Recreate dashboards in Grafana: 10-20 hours

**Pros:**
- ✅ Cost savings: $200-400/month (vs $1,200/month Datadog)
- ✅ Full vendor independence: Can switch backends anytime
- ✅ No usage limits: Instrument everything
- ✅ Complete control: Custom retention, sampling, etc.

**Cons:**
- ❌ High setup cost: 80-120 hours ($12K-18K developer time)
- ❌ Ongoing maintenance: 8-10 hours/month ($1,200-1,500/mo)
- ❌ UX gap: Grafana not as polished as Datadog
- ❌ Operational burden: One more thing to monitor
- ⚠️ Team training: Learning curve for new tools

**Total Cost Year 1:**
- Setup: $15,000 (100 hours × $150/hr)
- Infrastructure: $3,600 ($300/mo × 12 for hosting)
- Maintenance: $18,000 (10 hrs/mo × 12 × $150/hr)
- **Total: $36,600**

**Break-even:** Never in Year 1 (loses to Datadog)

### Option C: OpenTelemetry + Managed Backend (Honeycomb, Axiom, or Lightstep)

**Migration Strategy:**

```python
# Same instrumentation as Option B, but export to managed backend
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

provider = TracerProvider(
    resource=Resource.create({"service.name": "api-gateway"})
)
processor = BatchSpanProcessor(
    OTLPSpanExporter(
        endpoint="https://api.honeycomb.io/v1/traces",
        headers={"x-honeycomb-team": "YOUR_API_KEY"}
    )
)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
```

**Managed Backend Options:**

**Honeycomb:**
- Free tier: 20M events/month
- Pro tier: $0.50 per million events (likely $200-400/mo)
- Excellent OTel support, great for microservices

**Axiom:**
- Free tier: 500GB ingestion/month
- Pro tier: $0.25 per GB (likely $300-500/mo)
- Logs + traces in one platform

**Grafana Cloud:**
- Free tier: 50GB traces/month
- Pay-as-you-go: $0.50 per GB (likely $150-300/mo)
- Integrated with Grafana ecosystem

**Total Setup Time:** 60-80 hours
- Service instrumentation: 40-60 hours (same as Option B)
- Backend configuration: 10-15 hours (much easier than self-hosted)
- Dashboard creation: 10-15 hours (using backend's UI)

**Pros:**
- ✅ Vendor independence: Can switch backends
- ✅ No infrastructure: Managed service
- ✅ Better UX: Purpose-built observability tools
- ✅ Predictable costs: Usage-based pricing
- ✅ Lower maintenance: 2-3 hours/month

**Cons:**
- ⚠️ Still significant setup: 60-80 hours
- ⚠️ Monthly cost: $200-500/month (less than Datadog but not free)
- ⚠️ Feature gaps: May lack some Datadog features

**Total Cost Year 1:**
- Setup: $10,500 (70 hours × $150/hr)
- Subscription: $4,200 ($350/mo average × 12)
- Maintenance: $5,400 (3 hrs/mo × 12 × $150/hr)
- **Total: $20,100**

**Break-even vs Datadog:** Month 14 (Year 2)

### Option D: Hybrid OpenTelemetry (OTel for new services, Datadog for legacy)

**Strategy:**
- Keep existing 5 services on Datadog (avoid migration cost)
- Instrument 5 new services with OpenTelemetry + Honeycomb
- Gradually migrate old services as time permits

**Total Setup Time:** 40-50 hours
- New service instrumentation: 30-40 hours (5 services × 6-8 hours)
- Dual-platform dashboards: 10 hours

**Pros:**
- ✅ Lower initial cost: Only instrument new services
- ✅ Risk mitigation: Keep working system in place
- ✅ Gradual learning: Team learns OTel over time

**Cons:**
- ❌ Dual costs: Paying for both Datadog and Honeycomb
- ❌ Split observability: Hard to trace across platforms
- ⚠️ Technical debt: Still need to migrate eventually

**Total Cost Year 1:**
- Setup: $6,750 (45 hours × $150/hr)
- Datadog (legacy): $9,600 ($800/mo × 12)
- Honeycomb (new): $2,400 ($200/mo × 12)
- **Total: $18,750**

## Requirement Fit Analysis

| Requirement | Datadog | OTel+Self-Hosted | OTel+Managed | Hybrid |
|-------------|---------|------------------|--------------|--------|
| Distributed tracing | ✅ Excellent | ✅ Good | ✅ Excellent | ⚠️ Split |
| Service dependency map | ✅ Built-in | ⚠️ Manual | ✅ Built-in | ⚠️ Partial |
| Error attribution | ✅ Excellent | ✅ Good | ✅ Good | ⚠️ Split |
| Performance analysis | ✅ Excellent | ✅ Good | ✅ Excellent | ⚠️ Split |
| SLA monitoring | ✅ Built-in | ⚠️ Custom | ✅ Built-in | ⚠️ Manual |
| Setup <2 weeks | ✅ Done | ❌ 2-3 weeks | ✅ 1.5 weeks | ✅ 1 week |
| Maintenance <8hrs/mo | ✅ 0 hours | ❌ 10 hours | ✅ 3 hours | ⚠️ 5 hours |
| Cost <$2K/mo | ⚠️ $1,200 | ✅ $300 | ✅ $350 | ⚠️ $1,000 |
| Vendor independence | ❌ Locked | ✅ Full | ✅ Full | ⚠️ Partial |
| **Total Score** | **7/10** | **6/10** | **9/10** | **6/10** |

## Recommendation: OpenTelemetry + Managed Backend (Option C)

### Why This Is The Sweet Spot

**1. Positive Long-Term ROI**

```
Year 1 Costs:
- Datadog: $14,400
- OTel+Managed: $20,100
- Difference: -$5,700 (OTel more expensive)

Year 2 Costs:
- Datadog: $36,000
- OTel+Managed: $9,600 (subscription + maintenance only)
- Difference: +$26,400 (OTel saves $26K)

3-Year Total:
- Datadog: $86,400 ($14.4K + $36K + $36K)
- OTel+Managed: $39,300 ($20.1K + $9.6K + $9.6K)
- Savings: $47,100
```

For a growing team with 3-5 year horizon, this is **$47K in savings**.

**2. Optionality Value Extremely High**

```
P(need_to_switch) = 60% (cost pressure, vendor uncertainty)
Switching cost saved = $12,000 (80 hours Datadog→New) - $200 (2 hours OTel backend switch)
Time horizon discount = 0.9 (stable company)

Optionality Value = 0.6 × $11,800 × 0.9 = $6,372

Setup cost = 70 hours × $150/hr = $10,500

ROI over 3 years = ($6,372 + $47,100) / $10,500 = 509%
```

This is a **5× return on investment** over 3 years.

**3. Team Can Absorb Migration**

With 5-15 engineers, dedicating 2-3 weeks for infrastructure is reasonable:
- Platform engineer leads migration (full-time for 2 weeks)
- Service owners instrument their services (1 day each)
- Parallel execution: 5 services instrumented simultaneously

**4. Scale Demands Better Observability**

With 5-10 microservices:
- Distributed tracing is mandatory, not nice-to-have
- Service dependency understanding critical
- Performance bottlenecks span multiple services

OpenTelemetry's context propagation and auto-instrumentation excel here.

### Implementation Strategy

**Week 1: Infrastructure & Pilot**

1. **Choose managed backend** (spend 4 hours evaluating):
   - Honeycomb if trace-heavy workload
   - Axiom if logs + traces needed
   - Grafana Cloud if already using Grafana

2. **Deploy OTel Collector** (optional but recommended):
   ```yaml
   # Centralized collector for all services
   receivers:
     otlp:
       protocols:
         grpc:
         http:

   processors:
     batch:
       timeout: 10s
       send_batch_size: 1024

     # Sampling for cost control
     probabilistic_sampler:
       sampling_percentage: 10

   exporters:
     otlp/honeycomb:
       endpoint: "api.honeycomb.io:443"
       headers:
         "x-honeycomb-team": "${HONEYCOMB_API_KEY}"

   service:
     pipelines:
       traces:
         receivers: [otlp]
         processors: [batch, probabilistic_sampler]
         exporters: [otlp/honeycomb]
   ```

3. **Pilot with one service** (least critical):
   - Instrument non-critical service
   - Test trace generation
   - Validate backend dashboards
   - Get team feedback

**Week 2-3: Rollout**

1. **Service-by-service migration**:
   - Day 1-2: Service A (e.g., API Gateway)
   - Day 3-4: Service B (e.g., User Service)
   - Day 5-6: Service C (e.g., Payment Service)
   - Day 7-8: Service D (e.g., Notification Service)
   - Day 9-10: Service E (e.g., Admin Service)

2. **Parallel Datadog during transition**:
   - Keep Datadog running for 2-4 weeks
   - Compare traces between systems
   - Confidence-build before turning off Datadog

3. **Team training** (ongoing):
   - Lunch & learn on OpenTelemetry concepts
   - Document common patterns (custom spans, context propagation)
   - Create runbook for troubleshooting

**Week 4: Optimize**

1. **Dashboard creation**:
   - Service-level SLAs (p95, p99 latencies)
   - Error rates per service
   - Service dependency graph
   - Top slowest endpoints

2. **Sampling strategy**:
   - 100% sampling for errors
   - 10% sampling for successful requests
   - Adjust based on cost vs visibility trade-off

3. **Alerting setup**:
   - Integrate with PagerDuty/Slack
   - Route alerts to correct team
   - Define SLO-based alerts

### Success Criteria

**Month 1:**
- All 5 services instrumented with OTel
- Traces flowing to managed backend
- Datadog can be turned off
- Team comfortable with new dashboards

**Month 3:**
- Time-to-resolution for incidents improved (better traces)
- Cost stable at <$400/month
- No regrets about backend choice

**Month 6:**
- Backend switch validated (test with local Jaeger)
- Team prefers OTel traces over old Datadog
- Instrumentation stable (minimal updates needed)

**Month 12:**
- 3 new services instrumented with OTel in <4 hours each
- Total observability cost <$500/month (vs $2,800/month Datadog)
- Annual savings: ~$25K

## Risk Mitigation

**Risk 1: Migration takes longer than estimated**
- **Mitigation**: Keep Datadog active during transition (budget $2K for 2 extra months)
- **Fallback**: Rollback to Datadog if >150 hours spent

**Risk 2: Managed backend doesn't meet needs**
- **Mitigation**: 30-day trial of Honeycomb/Axiom before committing
- **Fallback**: Switch to different OTel-compatible backend (2-3 hours)

**Risk 3: Team struggles with new tools**
- **Mitigation**: Invest in training (allocate 10 hours/engineer)
- **Fallback**: Hire consultant for 1 week to accelerate learning

**Risk 4: Hidden costs (data volume higher than expected)**
- **Mitigation**: Start with aggressive sampling (10%), adjust up as needed
- **Fallback**: Self-host Jaeger for high-volume services

## Conclusion

For growing teams with 5-15 engineers and distributed services, **OpenTelemetry + managed backend is the optimal choice**. The upfront investment pays off through:

1. **Cost savings**: $47K over 3 years vs Datadog
2. **Vendor independence**: 2-hour backend switch vs 80-hour migration
3. **Scale readiness**: Instrumentation works for 100+ services
4. **Team growth**: Learning investment benefits new hires

This is the use case where OpenTelemetry shines brightest: Complex enough to justify the setup, established enough to make the investment, growing enough to need the optionality.

**Action**: Allocate 2-3 week sprint for migration, budget $350-500/month for managed backend, plan to save $25K+/year.
