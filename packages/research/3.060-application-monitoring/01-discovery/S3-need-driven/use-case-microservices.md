# Use Case: Microservices Architecture
## Distributed Tracing and Error Tracking

**Pattern**: Multi-service distributed system
**Stack**: Polyglot services (Python, Node.js, Go, Java), Kubernetes, service mesh
**Example**: Event-driven microservices, API gateway + 5+ backend services

---

## Scenario Description

### Who This Is For

- Engineering teams with 3+ microservices
- Distributed systems requiring cross-service tracing
- Event-driven architectures (Kafka, RabbitMQ, SQS)
- Service mesh deployments (Istio, Linkerd)
- Companies transitioning from monolith to microservices

### Typical Architecture

```
API Gateway → User Service → PostgreSQL
           ↓
           → Order Service → MongoDB
           ↓
           → Payment Service → Stripe API
           ↓
           → Notification Service → SendGrid
           ↓
           Message Queue (Kafka/SQS) → Background Workers
```

### Pain Points to Solve

1. Cannot trace requests across service boundaries
2. Errors in one service cascade to others (debugging nightmare)
3. Slow performance - which service is the bottleneck?
4. Database queries from multiple services causing contention
5. Message queue failures (lost events, duplicate processing)
6. Service dependencies unclear (which service calls what?)
7. No single view of distributed transaction health

---

## Requirements Profile

### Must-Have Features

- **Distributed tracing** with trace ID propagation
- **Service dependency map** (automatic topology discovery)
- **Cross-service error correlation** (see entire request path)
- **Span instrumentation** for databases, queues, HTTP calls
- **Performance monitoring** (APM) per service
- **Multi-language SDKs** (Python, Node.js, Go, Java, etc.)
- **OpenTelemetry support** (vendor-neutral instrumentation)

### Nice-to-Have Features

- Service mesh integration (Istio, Envoy)
- Kubernetes metrics and logs correlation
- Anomaly detection (ML-based alerting)
- Flame graphs for performance optimization
- Cost attribution per service
- SLO/SLI tracking (latency, error rate, throughput)

### Budget Reality

- Early microservices (3-5 services): $200-500/month
- Growth (5-15 services): $500-2,000/month
- Scale (15-50 services): $2,000-10,000/month
- Enterprise (50+ services): $10,000+/month

### Scale Profile

- Services: 3-50+
- Hosts/Pods: 10-500+
- Requests: 1M-100M+/day
- Data ingestion: 10GB-1TB+/month

---

## Provider Fit Analysis

### Datadog APM (Score: 95/100)

**Strengths:**
- Best-in-class distributed tracing
- Automatic service map generation
- Deep Kubernetes integration
- Unified platform (APM + Infrastructure + Logs)
- Live tail debugging across services
- Database query tracking with flame graphs
- Deployment tracking (correlate errors with releases)

**Pricing for Microservices:**
- APM: $31/host/month (billed annually)
- Infrastructure: $15/host/month (required for APM)
- Total: ~$46/host/month minimum
- Logs: $0.10/GB ingested
- Typical: 20 hosts = $920/month base

**TCO (12 months):**
- Early (10 hosts): $5,520/year (APM + infra)
- Growth (30 hosts): $16,560/year
- Scale (100 hosts): $55,200/year

**Integration Effort:** 8 hours (agents on all services, APM config, dashboards)

### New Relic (Score: 92/100)

**Strengths:**
- All-inclusive pricing (APM + logs + metrics in one)
- Distributed tracing with trace map
- Service maps and dependencies
- OpenTelemetry native support
- Good Kubernetes observability
- No per-host pricing (consumption-based)

**Pricing for Microservices:**
- Free: 100GB data/month, 1 full user
- Standard: $99/user/month + $0.30/GB over 100GB
- Typical microservices: 3 users + 500GB = $450/month

**TCO (12 months):**
- Early (200GB/month): $1,200/year (1 user + overages)
- Growth (500GB/month): $5,400/year (3 users + overages)
- Scale (2TB/month): $18,000/year (5 users + overages)

**Integration Effort:** 6 hours (agents + APM per service)

### Sentry (Score: 78/100)

**Strengths:**
- Excellent error tracking across services
- Performance monitoring with distributed traces
- Release tracking per service
- Good multi-language SDKs
- Source context for debugging

**Weaknesses:**
- APM not as robust as Datadog/New Relic
- No automatic service maps
- Limited infrastructure monitoring
- Not purpose-built for microservices

**Pricing for Microservices:**
- Business: $80/month (500K errors + performance)
- Enterprise: Custom (for high transaction volume)
- Typical: $200-500/month for distributed system

**TCO (12 months):**
- Early: $960/year (Business tier)
- Growth: $2,400/year (2x Business or Enterprise)
- Scale: $6,000+/year (Enterprise custom)

**Integration Effort:** 4 hours (SDK per service, manual trace propagation)

### Honeybadger (Score: 72/100)

**Strengths:**
- Simple pricing (unlimited users)
- Error tracking + uptime + APM
- Good for smaller microservices setups

**Weaknesses:**
- Limited distributed tracing capabilities
- No automatic service maps
- Basic APM compared to Datadog/New Relic
- Not designed for large-scale microservices

**Pricing for Microservices:**
- Medium ($89/mo): 600K errors/month + APM
- Large ($199/mo): 2.5M errors/month
- Typical: $89-199/month

**TCO (12 months):**
- Early: $1,068/year (Medium)
- Growth: $2,388/year (Large)
- Scale: Not ideal for large microservices

**Integration Effort:** 3 hours (SDK per service)

### AWS X-Ray (Score: 85/100)

**Strengths:**
- Native AWS integration (Lambda, ECS, EKS)
- Distributed tracing with service graph
- Very affordable for AWS-native stacks
- Automatic instrumentation for AWS services
- OpenTelemetry compatible

**Weaknesses:**
- AWS-only (not multi-cloud)
- Basic UI compared to Datadog/New Relic
- Limited alerting capabilities
- Need CloudWatch for logs/metrics

**Pricing for Microservices:**
- $5 per 1 million traces recorded
- $0.50 per 1 million traces retrieved
- Typical: 10M traces/month = $50/month

**TCO (12 months):**
- Early (5M traces): $300/year
- Growth (50M traces): $3,000/year
- Scale (200M traces): $12,000/year

**Integration Effort:** 4 hours (X-Ray daemon + SDK)

### SigNoz (Score: 80/100)

**Strengths:**
- Open-source alternative to Datadog
- OpenTelemetry-native
- Distributed tracing + metrics + logs
- Self-hosted (full control, lower cost at scale)
- Kubernetes-ready

**Weaknesses:**
- Self-managed overhead (DevOps burden)
- Smaller community than commercial tools
- Fewer integrations out-of-box

**Pricing for Microservices:**
- Self-hosted: Free (infrastructure costs only)
- SigNoz Cloud: $0.30/GB ingested
- Typical: 200GB/month = $60/month

**TCO (12 months):**
- Self-hosted: $1,200-3,000/year (k8s infra costs)
- Cloud (200GB): $720/year
- Cloud (1TB): $3,600/year

**Integration Effort:** 12 hours (self-host setup + OpenTelemetry collectors)

---

## Recommendation

### Top Choice: Datadog APM (95/100)

**Why Datadog wins for microservices:**
1. **Best distributed tracing** - Automatic trace ID propagation, flame graphs
2. **Service dependency maps** - Visualize entire architecture automatically
3. **Unified observability** - APM + logs + infrastructure + Kubernetes in one
4. **Production-grade** - Handles billions of spans, battle-tested
5. **Deep integrations** - Every database, queue, framework supported

**When to choose Datadog:**
- Serious microservices deployment (5+ services)
- Need full observability (errors + performance + logs + infra)
- Have budget for best-in-class tooling ($500-10K/month)
- Running on Kubernetes or service mesh
- Multi-language stack (polyglot services)

**Migration Path:**
- Start: APM on 5-10 critical services ($230-460/month)
- Growth: Full coverage on 20-30 services ($920-1,380/month)
- Scale: 50+ services + log aggregation ($2,300+/month)

### Runner-Up: New Relic (92/100)

**When to choose New Relic:**
- Want consumption-based pricing (not per-host)
- Need all-inclusive features (no add-on costs)
- OpenTelemetry-first approach
- Smaller team (fewer users = lower cost)

**Trade-offs vs Datadog:**
- Simpler pricing (easier to predict)
- Less complex setup (fewer product SKUs)
- Slightly less polished UI
- Better for mid-size microservices (5-20 services)

**Cost Advantage:**
- 3 users + 500GB = $5,400/year (vs Datadog $16,560 for 30 hosts)
- Better for data-heavy, fewer-host architectures

### Budget Alternative: AWS X-Ray (85/100)

**When to choose AWS X-Ray:**
- AWS-native stack (Lambda, ECS, EKS)
- Budget-constrained ($50-300/month)
- Simple distributed tracing needs
- Don't need full observability platform

**Trade-offs:**
- Much cheaper ($300/year vs $5,520/year for Datadog)
- AWS-locked (not multi-cloud)
- Basic UI (not as powerful)
- Need to combine with CloudWatch for full picture

---

## Cost Comparison: 12-Month TCO

### Early Microservices (5 services, 10 hosts, 100M traces/month)
- **Datadog**: $5,520/year (10 hosts APM + infra)
- **New Relic**: $1,200/year (1 user + 200GB data)
- **Sentry**: $960/year (Business tier)
- **Honeybadger**: $1,068/year (Medium)
- **AWS X-Ray**: $600/year (100M traces)
- **SigNoz Cloud**: $720/year (200GB)

**Winner: AWS X-Ray ($600), but Datadog worth premium for features**

### Growth Stage (15 services, 30 hosts, 500M traces/month)
- **Datadog**: $16,560/year (30 hosts)
- **New Relic**: $5,400/year (3 users + 500GB)
- **Sentry**: $2,400/year (Enterprise)
- **Honeybadger**: $2,388/year (Large)
- **AWS X-Ray**: $3,000/year (500M traces)
- **SigNoz Cloud**: $3,600/year (1TB)

**Winner: AWS X-Ray ($3,000), but New Relic best full-featured at $5,400**

### Scale Stage (50+ services, 100 hosts, 2B traces/month)
- **Datadog**: $55,200/year (100 hosts)
- **New Relic**: $18,000/year (5 users + 2TB)
- **Sentry**: $6,000+/year (Enterprise custom)
- **Honeybadger**: Not suitable (scale limits)
- **AWS X-Ray**: $12,000/year (2B traces)
- **SigNoz Self-hosted**: $2,000/year (infra only)

**Winner: SigNoz self-hosted ($2K), AWS X-Ray ($12K), New Relic ($18K) before Datadog ($55K)**

---

## OpenTelemetry Strategy

### Vendor-Neutral Instrumentation

For microservices, instrument with **OpenTelemetry** to avoid vendor lock-in:

```python
# Python service example
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# Configure provider
trace.set_tracer_provider(TracerProvider())

# Export to Datadog/New Relic/SigNoz (configurable)
otlp_exporter = OTLPSpanExporter(endpoint="https://your-backend:4317")
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

# Auto-instrument Flask and requests
FlaskInstrumentor().instrument()
RequestsInstrumentor().instrument()
```

**Benefits:**
- Switch vendors easily (change endpoint only)
- Use open-source backends (Jaeger, SigNoz)
- Combine multiple backends (Datadog + Jaeger)

---

## Implementation Guide

### Datadog APM Setup (Recommended)

**Kubernetes Deployment:**
```yaml
# datadog-agent.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: datadog-agent
data:
  apm-enabled: "true"
  logs-enabled: "true"

---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: datadog-agent
spec:
  template:
    spec:
      containers:
      - name: agent
        image: datadog/agent:latest
        env:
        - name: DD_API_KEY
          value: "YOUR_KEY"
        - name: DD_SITE
          value: "datadoghq.com"
        - name: DD_APM_ENABLED
          value: "true"
        - name: DD_LOGS_ENABLED
          value: "true"
```

**Application Instrumentation (Python):**
```python
# requirements.txt
ddtrace

# Launch app with tracer
ddtrace-run python app.py

# Or manual instrumentation
from ddtrace import tracer, patch_all
patch_all()  # Auto-instrument Flask, requests, psycopg2, etc.

@tracer.wrap(service="user-service", resource="get_user")
def get_user(user_id):
    # Custom span for business logic
    return db.query(f"SELECT * FROM users WHERE id={user_id}")
```

**Time to first trace:** 30 minutes (agent + app restart)
**Time to full setup:** 8 hours (all services + dashboards)

---

## Key Takeaways

1. **Datadog for serious microservices** - Best tracing, service maps, worth the cost
2. **New Relic for mid-size setups** - Better pricing for 5-20 services
3. **AWS X-Ray for budget AWS shops** - 10x cheaper, good enough for basic tracing
4. **Use OpenTelemetry** - Avoid vendor lock-in, switch backends easily
5. **Full observability required** - Errors + APM + logs + infra in distributed systems
6. **Budget $500-2K/month** - Microservices monitoring is expensive but critical
