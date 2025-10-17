# Use Case 6: Multi-Cloud Portability

## Scenario Profile

**Context:**
- Running workloads across multiple cloud providers (AWS + GCP, or AWS + Azure)
- Strategic decision for vendor negotiation leverage
- Disaster recovery requirements (region/provider redundancy)
- Cost optimization through cloud arbitrage
- Want observability that works consistently everywhere
- Current cloud-specific tools don't span providers

**Example:**
DataCo runs primary production on AWS but is expanding to GCP for new Asian markets. They have 15 services on AWS and planning 10 new services on GCP. Using CloudWatch for AWS and Cloud Operations for GCP creates siloed observability. They need unified tracing across clouds but don't want to be locked into Datadog's multi-cloud premium pricing.

## Requirements Analysis

### Functional Requirements

**Must Have:**
- Single pane of glass: View traces across AWS + GCP services
- Cross-cloud tracing: Request flows from AWS → GCP → AWS
- Consistent instrumentation: Same code works on any cloud
- Cloud-agnostic storage: Traces accessible regardless of cloud
- Service mesh compatibility: Work with Istio/Linkerd across clouds

**Nice to Have:**
- Cost comparison: AWS vs GCP observability costs
- Performance comparison: Latency AWS vs GCP
- Cloud-specific enrichment: Instance metadata from each cloud
- Multi-region: Same tool for us-east-1 and asia-southeast-1

**Critical:**
- No vendor lock-in: Can switch clouds without rewriting observability
- No cloud-specific APIs: Don't use CloudWatch SDK or Cloud Operations SDK

### Non-Functional Requirements

**Setup Time:** 1-2 months acceptable
- Complex architecture requires planning
- Need to deploy infrastructure in both clouds

**Cloud-Neutrality:** CRITICAL
- Must work identically on AWS, GCP, Azure, on-prem
- No cloud-specific dependencies
- Portable instrumentation code

**Cost Target:** <$3K/month combined
- Currently: AWS CloudWatch ($500/mo) + GCP Cloud Operations ($400/mo) = $900/mo
- But: Siloed, no cross-cloud tracing
- Willing to pay more for unified view, but not 10×

**Vendor Lock-in Concern:** EXTREME
- Entire architecture designed to avoid cloud lock-in
- Observability can't become the lock-in point
- Need to prove portability (actually test migration)

## Solution Evaluation

### Option A: Cloud-Native Tools (CloudWatch + Cloud Operations)

**Current State:**
- AWS services: CloudWatch Traces (X-Ray)
- GCP services: Cloud Operations (Cloud Trace)
- **Problem:** Two separate systems, no unified view

**Architecture:**
```
AWS Services:
  ├── CloudWatch Logs
  ├── X-Ray Traces
  └── CloudWatch Metrics

GCP Services:
  ├── Cloud Logging
  ├── Cloud Trace
  └── Cloud Monitoring

Cross-cloud request:
  API Gateway (AWS) → User Service (GCP) → DB (AWS)

  Trace appears in:
  - X-Ray (AWS portions only)
  - Cloud Trace (GCP portions only)
  ❌ No unified trace showing full request flow
```

**To get unified view, need custom integration:**

```python
# Export both to common backend (e.g., Datadog)
# AWS: CloudWatch → Lambda → Datadog
# GCP: Cloud Operations → Pub/Sub → Cloud Function → Datadog

# But now you're paying:
# - AWS CloudWatch: $500/mo
# - GCP Cloud Operations: $400/mo
# - Datadog multi-cloud: $5K-10K/mo
# Total: $5.9K-10.9K/mo
```

**Pros:**
- ✅ Native integration: Works out-of-box per cloud
- ✅ Cloud optimized: Best performance on each cloud
- ✅ Free tier: Basic usage included

**Cons:**
- ❌ Siloed: No cross-cloud trace visibility
- ❌ Vendor lock-in: Code tied to cloud APIs
- ❌ Expensive to unify: Need aggregator like Datadog
- ❌ Complex: Maintain 2 different systems

**Total Cost (Unified):** $5.9K-10.9K/month with Datadog aggregation

### Option B: Enterprise Multi-Cloud APM (Datadog, Dynatrace)

**Architecture:**
```python
# Datadog agent on both AWS and GCP
# AWS:
import datadog
datadog.initialize(api_key="...", app_key="...")

# GCP:
import datadog
datadog.initialize(api_key="...", app_key="...")

# Same code, works everywhere
# Unified dashboard shows cross-cloud traces
```

**Pricing:**
- Multi-cloud requires Enterprise tier
- AWS hosts: 10 × $31/host/mo = $310/mo
- GCP hosts: 8 × $31/host/mo = $248/mo
- APM traces: 15 services × $800/mo = $12,000/mo
- Multi-cloud features: +$2,000/mo premium
- **Total: $14,558/month**

**Pros:**
- ✅ Unified view: Single dashboard for all clouds
- ✅ Cross-cloud tracing: Full request flows visible
- ✅ Enterprise support: 24/7 help
- ✅ Cloud-agnostic code: Same SDK everywhere

**Cons:**
- ❌ Extremely expensive: $175K/year
- ❌ Vendor lock-in: Now locked into Datadog instead of cloud
- ⚠️ Multi-cloud surcharge: Paying premium for feature you need
- ⚠️ Defeats purpose: Avoided cloud lock-in, got vendor lock-in

**Total Cost:** $175K/year (negates multi-cloud cost savings)

### Option C: OpenTelemetry + Self-Hosted Backend

**Architecture:**

```yaml
# OpenTelemetry Collector deployed in both clouds
# Tempo backend in one cloud (or distributed)

# AWS Deployment:
apiVersion: v1
kind: ConfigMap
metadata:
  name: otel-collector-config
data:
  config.yaml: |
    receivers:
      otlp:
        protocols:
          grpc:
          http:

    processors:
      # Add cloud context
      resource:
        attributes:
          - key: cloud.provider
            value: "aws"
          - key: cloud.region
            value: "${AWS_REGION}"

      batch:
        timeout: 10s

    exporters:
      # Export to centralized Tempo
      otlp/tempo:
        endpoint: tempo.central.com:4317
        tls:
          insecure: false

    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: [resource, batch]
          exporters: [otlp/tempo]

# GCP Deployment (identical config, different cloud.provider):
apiVersion: v1
kind: ConfigMap
metadata:
  name: otel-collector-config
data:
  config.yaml: |
    receivers:
      otlp:
        protocols:
          grpc:
          http:

    processors:
      resource:
        attributes:
          - key: cloud.provider
            value: "gcp"
          - key: cloud.region
            value: "${GCP_REGION}"

      batch:
        timeout: 10s

    exporters:
      otlp/tempo:
        endpoint: tempo.central.com:4317
        tls:
          insecure: false

    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: [resource, batch]
          exporters: [otlp/tempo]
```

**Service Instrumentation (Cloud-Agnostic):**

```python
# This EXACT code runs on AWS, GCP, Azure, on-prem
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

# Cloud metadata detected automatically
resource = Resource.create({
    "service.name": "user-service",
    "service.version": "1.2.3",
    # cloud.provider, cloud.region added by collector
})

provider = TracerProvider(resource=resource)

# Export to local collector (on same cloud)
processor = BatchSpanProcessor(
    OTLPSpanExporter(endpoint="http://otel-collector:4317")
)

provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Auto-instrument
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
FastAPIInstrumentor().instrument_app(app)

# Works identically on AWS, GCP, anywhere!
```

**Cross-Cloud Trace Example:**

```
User Request → API Gateway (AWS)
                ↓ trace_id: abc123
              User Service (GCP)
                ↓ trace_id: abc123
              Database (AWS)

Tempo shows unified trace:
┌─────────────────────────────────────────┐
│ Trace: abc123                           │
│ Duration: 245ms                         │
├─────────────────────────────────────────┤
│ ► API Gateway (AWS)           120ms    │
│   ├─ User Service (GCP)       95ms     │
│   │  └─ Database (AWS)        30ms     │
└─────────────────────────────────────────┘

Filtered by cloud:
- AWS spans: 150ms (61%)
- GCP spans: 95ms (39%)
```

**Total Setup Time:** 120-160 hours (4-6 weeks)
- Deploy collectors (both clouds): 30 hours
- Deploy Tempo (central): 30 hours
- Networking (VPC peering, etc.): 30 hours
- Instrument 15 AWS services: 45 hours
- Instrument 10 GCP services: 30 hours
- Dashboard & testing: 20 hours

**Costs:**

| Component | AWS Cost | GCP Cost | Total/Month |
|-----------|----------|----------|-------------|
| OTel Collectors (2 per cloud) | $100 | $100 | $200 |
| Tempo backend (EKS) | $400 | - | $400 |
| Storage (S3) | $200 | - | $200 |
| Networking (inter-cloud) | $150 | $150 | $300 |
| **Total Infrastructure** | **$850** | **$250** | **$1,100** |
| Maintenance (10 hrs/mo) | - | - | $1,500 |
| **Grand Total** | | | **$2,600/mo** |

**Total Cost Year 1:**
- Setup: $20,000 (140 hours × $150/hr)
- Infrastructure: $13,200 ($1,100/mo × 12)
- Maintenance: $18,000 ($1,500/mo × 12)
- **Total: $51,200**

**Pros:**
- ✅ Truly cloud-agnostic: Same code anywhere
- ✅ Unified traces: Cross-cloud visibility
- ✅ Vendor independent: No Datadog lock-in
- ✅ Cost effective: $2,600/mo vs $14,558/mo Datadog
- ✅ Portable: Can move to Azure tomorrow

**Cons:**
- ❌ High setup: 140 hours of work
- ❌ Operational burden: Maintain multi-cloud infrastructure
- ⚠️ Networking complexity: VPC peering, cross-cloud data transfer
- ⚠️ Single point of failure: Tempo in one cloud

**Risk:** MEDIUM-HIGH (networking complexity, multi-cloud operations)

### Option D: OpenTelemetry + Managed Backend (Best of Both Worlds)

**Architecture:**

```python
# Services instrumented with OpenTelemetry (cloud-agnostic)
# Export to managed backend (Grafana Cloud, Honeycomb)

# AWS Service:
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

processor = BatchSpanProcessor(
    OTLPSpanExporter(
        endpoint="https://otlp-gateway.grafana.net/otlp",
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
)

# GCP Service (IDENTICAL code):
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

processor = BatchSpanProcessor(
    OTLPSpanExporter(
        endpoint="https://otlp-gateway.grafana.net/otlp",
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
)

# Same backend, works from any cloud
```

**Total Setup Time:** 80-100 hours (2-3 weeks)
- No infrastructure setup (managed backend)
- Instrument 15 AWS services: 45 hours
- Instrument 10 GCP services: 30 hours
- Dashboards & testing: 15 hours

**Costs:**

| Component | Cost/Month |
|-----------|------------|
| Grafana Cloud (3GB/day traces) | $1,500 |
| Maintenance (3 hrs/mo) | $450 |
| **Total** | **$1,950/mo** |

**Total Cost Year 1:**
- Setup: $13,500 (90 hours × $150/hr)
- Subscription: $18,000 ($1,500/mo × 12)
- Maintenance: $5,400 ($450/mo × 12)
- **Total: $36,900**

**Pros:**
- ✅ Cloud-agnostic: Same instrumentation code
- ✅ Unified view: Cross-cloud traces
- ✅ No ops burden: Managed backend
- ✅ Vendor independent: Can switch backends
- ✅ Fastest setup: 90 hours vs 140 hours self-hosted
- ✅ Cost effective: $1,950/mo vs $14,558/mo Datadog

**Cons:**
- ⚠️ Monthly cost: $1,950/mo (vs $2,600/mo self-hosted)
- ⚠️ Data egress: Sending traces out of cloud (minimal cost)

**Risk:** LOW (managed service, no multi-cloud ops complexity)

## Requirement Fit Analysis

| Requirement | Cloud-Native | Datadog | OTel+Self-Hosted | OTel+Managed |
|-------------|--------------|---------|------------------|--------------|
| Single pane of glass | ❌ Siloed | ✅ Unified | ✅ Unified | ✅ Unified |
| Cross-cloud tracing | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |
| Consistent instrumentation | ❌ Cloud-specific | ⚠️ Vendor SDK | ✅ Standard | ✅ Standard |
| Cloud-agnostic storage | ❌ No | ⚠️ Vendor | ✅ Self-hosted | ✅ Portable |
| No vendor lock-in | ⚠️ Cloud lock-in | ❌ Datadog lock-in | ✅ Open source | ✅ Standard |
| Setup <2 months | ✅ Quick | ✅ Quick | ⚠️ 4-6 weeks | ✅ 2-3 weeks |
| Cost <$3K/mo | ❌ $10K unified | ❌ $14.5K | ⚠️ $2.6K | ✅ $1.95K |
| **Total Score** | **2/10** | **5/10** | **8/10** | **10/10** |

## Recommendation: OpenTelemetry + Managed Backend (Option D)

### Why This Is Perfect for Multi-Cloud

**1. Achieves Core Goal: Cloud Portability**

```python
# This code runs IDENTICALLY on:
# - AWS EC2
# - AWS EKS
# - GCP Compute Engine
# - GCP GKE
# - Azure VMs
# - Azure AKS
# - On-premises Kubernetes
# - Your laptop

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

# Zero cloud-specific code!
```

**2. Significant Cost Savings vs Datadog**

```
2-Year Cost Comparison:

Datadog Multi-Cloud:
- Year 1: $175,000
- Year 2: $220,000 (growth)
- Total: $395,000

OTel + Managed:
- Year 1: $36,900 (includes setup)
- Year 2: $23,400 (subscription + maintenance)
- Total: $60,300

Savings: $334,700 (85% reduction)
```

**3. True Vendor Independence**

**Scenario: Need to switch clouds**

```
Without OpenTelemetry (cloud-native tools):
- Rewrite instrumentation for new cloud
- Migrate historical data
- Retrain team on new tools
- Time: 3-6 months
- Cost: $200K-500K

With OpenTelemetry:
- Deploy OTel Collector on new cloud
- Deploy existing service code (no changes!)
- Point to same backend
- Time: 1-2 weeks
- Cost: $10K-20K
```

**Scenario: Backend provider raises prices**

```
Without OpenTelemetry:
- Locked in, must pay
- Migration would cost $100K+

With OpenTelemetry:
- Switch exporters (change 1 line of code)
- Grafana → Honeycomb: 2 days
- Grafana → Self-hosted: 1 week
- Cost: $5K-15K
```

**4. Operational Simplicity**

Managed backend avoids multi-cloud ops complexity:
- No VPC peering between clouds
- No cross-cloud data transfer complexity
- No "which cloud is Tempo in?" decisions
- Backend handles high availability

### Implementation Strategy

**Week 1: Foundation**

**Day 1-2: Choose Managed Backend**

Evaluate based on multi-cloud support:

| Backend | Multi-Cloud Support | Pricing | Verdict |
|---------|-------------------|---------|---------|
| Grafana Cloud | ✅ Excellent (OTLP from anywhere) | $0.50/GB | ✅ Recommended |
| Honeycomb | ✅ Excellent (OTLP) | $0.50/M events | ✅ Good alternative |
| Axiom | ✅ Good (OTLP) | $0.25/GB | ✅ Cheapest |
| Lightstep | ✅ Excellent (OTel founders) | $1.00/GB | ⚠️ Expensive |

**Recommendation: Grafana Cloud**
- Best multi-cloud story
- Integrated logs + traces + metrics
- Good price/performance

**Day 3-5: Pilot Service (AWS)**

```python
# Pick one AWS service for pilot
# Instrument with OpenTelemetry
# Validate traces appear in Grafana Cloud

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

# Automatically detects AWS metadata
resource = Resource.create({
    "service.name": "api-gateway",
    # These are auto-detected:
    # "cloud.provider": "aws",
    # "cloud.region": "us-east-1",
    # "cloud.account.id": "123456789012"
})

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(
    OTLPSpanExporter(
        endpoint="https://otlp-gateway-prod-us-east-1.grafana.net/otlp",
        headers={"Authorization": f"Bearer {GRAFANA_API_KEY}"}
    )
)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Success: Traces appear in Grafana with AWS metadata
```

**Week 2-3: AWS Services Migration**

Migrate remaining 14 AWS services:
- 3 services/day
- 5 days = 15 services
- Use same instrumentation pattern as pilot

**Week 4-5: GCP Services Migration**

Migrate 10 GCP services:
- **Key insight:** Code is IDENTICAL to AWS!
- Only difference: Collector auto-detects GCP metadata

```python
# This is the SAME code from AWS service!
# No changes needed for GCP

from opentelemetry import trace
# ... exact same imports ...

resource = Resource.create({
    "service.name": "user-service",
    # Auto-detected (now GCP values):
    # "cloud.provider": "gcp",
    # "cloud.region": "asia-southeast1",
    # "cloud.account.id": "my-gcp-project"
})

# Export to SAME Grafana Cloud instance
processor = BatchSpanProcessor(
    OTLPSpanExporter(
        endpoint="https://otlp-gateway-prod-us-east-1.grafana.net/otlp",
        headers={"Authorization": f"Bearer {GRAFANA_API_KEY}"}
    )
)

# That's it! Works perfectly from GCP.
```

**Week 6: Cross-Cloud Validation**

**Test cross-cloud request flows:**

```bash
# Trigger request: AWS → GCP → AWS
curl https://api-gateway-aws.com/api/users/123

# Trace should show:
# 1. API Gateway (AWS) - 50ms
#    ├─ 2. User Service (GCP) - 40ms
#    │  └─ 3. Database (AWS) - 20ms
#    └─ Total: 110ms

# Verify in Grafana:
# - Single unified trace (abc123)
# - Spans labeled with cloud.provider
# - Latency breakdown by cloud
```

**Create dashboards:**

```
Dashboard: Multi-Cloud Overview
├─ Total Requests: 10,000/hr
├─ By Cloud:
│  ├─ AWS: 6,500/hr (65%)
│  └─ GCP: 3,500/hr (35%)
├─ Cross-Cloud Requests: 2,000/hr (20%)
├─ Latency:
│  ├─ AWS-only requests: p95 = 45ms
│  ├─ GCP-only requests: p95 = 50ms
│  └─ Cross-cloud requests: p95 = 120ms
└─ Cost Analysis:
   ├─ AWS observability: $850/mo (collector + egress)
   └─ GCP observability: $650/mo (collector + egress)
```

### Success Criteria

**Week 2:**
- ✅ Pilot AWS service instrumented
- ✅ Traces in Grafana Cloud with AWS metadata
- ✅ Team comfortable with OpenTelemetry

**Week 5:**
- ✅ All 15 AWS services instrumented
- ✅ All 10 GCP services instrumented
- ✅ Cross-cloud traces working

**Month 3:**
- ✅ Unified dashboards in use
- ✅ Cost <$2,000/month
- ✅ Zero cloud-specific code in services

**Month 6 (Portability Test):**
- ✅ Deploy 1 service to Azure (validate portability)
- ✅ Same code works without modification
- ✅ Traces from AWS, GCP, Azure in single view

**Year 1:**
- ✅ Saved $138K vs Datadog ($175K - $37K)
- ✅ Can add new clouds in days, not months
- ✅ Team confident in multi-cloud strategy

## Multi-Cloud Best Practices

### 1. Cloud Resource Attributes

```python
# OpenTelemetry auto-detects cloud metadata
# But you can override or supplement:

from opentelemetry.sdk.resources import Resource

resource = Resource.create({
    # Your attributes
    "service.name": "user-service",
    "service.version": "1.2.3",
    "deployment.environment": "production",

    # Cloud attributes (auto-detected or manual)
    "cloud.provider": "aws",  # or "gcp", "azure"
    "cloud.region": "us-east-1",
    "cloud.availability_zone": "us-east-1a",
    "cloud.account.id": "123456789012",

    # Useful for cost allocation
    "team": "user-team",
    "cost_center": "engineering",
})
```

### 2. Cross-Cloud Context Propagation

```python
# Ensure trace context propagates across clouds
# Use W3C Trace Context (cloud-agnostic standard)

from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.b3 import B3MultiFormat

# W3C Trace Context (recommended)
set_global_textmap(B3MultiFormat())

# Now requests from AWS → GCP carry trace context
# Works even across service meshes (Istio)
```

### 3. Cost Monitoring

```yaml
# Add custom span attributes for cost analysis
processors:
  resource:
    attributes:
      - key: cloud.cost_per_hour
        value: "0.05"  # Compute instance cost
      - key: data_egress_cost
        value: "0.01"  # Per GB egress

# Analyze in Grafana:
# - Which cloud is cheaper for which workload?
# - Cross-cloud requests: Is network cost worth it?
```

## Conclusion

For multi-cloud architectures, **OpenTelemetry + managed backend is the only viable solution** that achieves true portability while maintaining unified observability.

**Key Advantages:**
1. **Cloud agnostic**: Same code runs on AWS, GCP, Azure, on-prem
2. **Cost effective**: $1,950/mo vs $14,558/mo Datadog (87% savings)
3. **Vendor independent**: Can switch backends or clouds easily
4. **Unified view**: Cross-cloud traces in single dashboard
5. **Future-proof**: Add clouds without rewriting instrumentation

**DataCo Action Plan:**
- Week 1-2: Pilot with 1 AWS service → Grafana Cloud
- Week 3-4: Migrate remaining AWS services
- Week 5-6: Migrate GCP services (same code!)
- Month 3: Decommission CloudWatch + Cloud Operations
- Result: $12K/month savings, true multi-cloud portability

This is **the right way** to do multi-cloud observability in 2025.
