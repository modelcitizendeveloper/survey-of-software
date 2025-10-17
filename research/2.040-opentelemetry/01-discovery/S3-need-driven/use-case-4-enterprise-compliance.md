# Use Case 4: Enterprise with Compliance Requirements

## Scenario Profile

**Context:**
- 50-200 person engineering organization across 10-20 teams
- 5,000-50,000 errors/month, 500K-5M daily active users
- 20-50 microservices with complex interdependencies
- Regulated industry (Healthcare/HIPAA, Finance/PCI-DSS, Enterprise SaaS/SOC 2)
- Strict data governance, audit requirements, security reviews
- Multi-cloud or hybrid cloud infrastructure
- Enterprise contracts with SLA penalties

**Example:**
HealthTech Inc. has 80 engineers building a HIPAA-compliant telehealth platform. They have 35 microservices across AWS and on-premise infrastructure. They're currently on Splunk ($15K/month) which is expensive but meets compliance requirements. Security team requires all observability data to stay within controlled boundaries. They need to evaluate whether OpenTelemetry can meet compliance while reducing costs.

## Requirements Analysis

### Functional Requirements

**Must Have:**
- Distributed tracing across 20-50 services
- End-to-end request tracking (patient interaction → database)
- Performance SLA monitoring (contractual obligations)
- Anomaly detection (unusual patterns indicating security issues)
- Multi-environment support (dev, staging, prod, DR)
- Role-based access control (RBAC) for traces/logs
- Audit trail of who accessed what observability data

**Compliance-Specific:**
- PII redaction in traces (patient names, SSNs, etc.)
- Data residency controls (GDPR, HIPAA data location requirements)
- Retention policies (keep 90 days for audit, then delete)
- Encryption in transit and at rest
- Access logging (who viewed which patient's traces?)
- Data sovereignty (EU customer data stays in EU)

**Integration Requirements:**
- SSO/SAML integration (corporate identity provider)
- API access for security tools (SIEM integration)
- Alert routing to incident management (PagerDuty, ServiceNow)
- Custom metric export for compliance dashboards

### Non-Functional Requirements

**Setup Time:** 2-6 months acceptable
- Requires security review (2-4 weeks)
- Compliance validation (2-4 weeks)
- Gradual rollout across teams (8-12 weeks)
- Documentation for auditors

**Ongoing Maintenance:** 40-80 hours/month
- Dedicated platform/SRE team (2-4 engineers)
- Compliance monitoring
- Access review quarterly
- Vendor security assessment annual

**Budget:** $5K-50K/month for observability
- Current Splunk: $15K/month
- Willing to pay for compliance-ready solution
- Cost reduction important but not primary driver

**Vendor Lock-in Concern:** CRITICAL
- 5-10 year horizon (enterprise systems last long)
- Vendor stability crucial (can't have observability go dark)
- Acquisition risk unacceptable (happened to Splunk/Cisco)
- Multi-cloud/hybrid strategy (AWS + on-prem + maybe Azure)
- Exit planning required (legal/procurement mandate)

## Solution Evaluation

### Option A: Enterprise APM (Datadog, Dynatrace, New Relic)

**Example: Datadog Enterprise**

**Pricing:**
- Base: $5K-10K/month for infrastructure monitoring
- APM: +$10K-20K/month for 50 services
- Log management: +$5K-15K/month
- Security monitoring: +$5K-10K/month
- **Total: $25K-55K/month**

**Compliance Features:**
- ✅ SOC 2 Type II certified
- ✅ HIPAA/HITECH compliant
- ✅ PCI-DSS compliant
- ✅ SSO/SAML support
- ✅ RBAC built-in
- ✅ Data residency options (EU/US regions)
- ✅ Audit logging

**Pros:**
- ✅ Compliance certifications: Ready for auditors
- ✅ Enterprise support: 24/7 support, TAM, SLAs
- ✅ Feature complete: Everything needed out-of-box
- ✅ Security reviewed: Passed enterprise security reviews
- ✅ Proven at scale: Used by Fortune 500

**Cons:**
- ❌ Extreme cost: $300K-660K/year
- ❌ Vendor lock-in: Deep integration, very hard to leave
- ❌ Cost unpredictability: Pricing changes, usage spikes
- ❌ Acquisition risk: Vendor consolidation in market
- ⚠️ Data control: Data stored in vendor cloud

**Total Cost Year 1:** $300K-660K
**Total Cost 3 Years:** $900K-2M

### Option B: OpenTelemetry + Self-Hosted Compliant Backend

**Architecture:**

```yaml
# Self-hosted on Kubernetes in your VPC/data center
# Full control over data, compliance-ready

# 1. OpenTelemetry Collector (PII Redaction)
receivers:
  otlp:
    protocols:
      grpc:
      http:

processors:
  # PII redaction processor
  attributes:
    actions:
      - key: patient.name
        action: delete
      - key: patient.ssn
        action: hash
      - key: patient.email
        action: redact
        pattern: '.*@.*'
        replacement: 'redacted@example.com'

  # Add compliance metadata
  resource:
    attributes:
      - key: compliance.region
        value: "us-east-1"
      - key: compliance.classification
        value: "phi"

  # Sampling for cost control
  probabilistic_sampler:
    sampling_percentage: 20

exporters:
  # Grafana Tempo for traces
  otlp/tempo:
    endpoint: tempo:4317

  # Grafana Loki for logs
  loki:
    endpoint: http://loki:3100/loki/api/v1/push

  # Prometheus for metrics
  prometheus:
    endpoint: prometheus:9090

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [attributes, resource, probabilistic_sampler]
      exporters: [otlp/tempo]
    logs:
      receivers: [otlp]
      processors: [attributes, resource]
      exporters: [loki]

# 2. Storage Layer (Tempo + S3-compatible)
# tempo.yaml
storage:
  trace:
    backend: s3  # or on-prem object storage
    s3:
      bucket: traces-phi-data
      endpoint: s3.amazonaws.com
      # Server-side encryption
      sse:
        type: aws:kms
        kms_key_id: arn:aws:kms:us-east-1:123456789012:key/...
    # Retention policy (HIPAA: 6 years)
    retention: 2190h  # 90 days active, then archive
    archive:
      enabled: true
      retention: 52560h  # 6 years

# 3. Access Control (Grafana with auth)
# grafana.ini
[auth.generic_oauth]
enabled = true
client_id = YOUR_CLIENT_ID
client_secret = YOUR_CLIENT_SECRET
auth_url = https://sso.company.com/oauth/authorize
token_url = https://sso.company.com/oauth/token

[users]
allow_sign_up = false
auto_assign_org = true
auto_assign_org_role = Viewer

[rbac]
enabled = true
# Define roles: compliance-auditor, developer, sre, security

# 4. Audit Logging
[log]
mode = file
level = info
# Log all access to traces containing PHI
filters = access:phi

[auditing]
enabled = true
path = /var/log/grafana/audit.log
# Keep 7 years for HIPAA compliance
max_days = 2555
```

**Service Instrumentation:**

```python
# Python service with compliance-aware instrumentation
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

# Define service metadata
resource = Resource.create({
    "service.name": "patient-service",
    "service.namespace": "healthcare",
    "deployment.environment": "production",
    "compliance.classification": "phi",  # Protected Health Information
    "compliance.region": "us-east-1",
})

# Configure tracer with compliance context
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(
    OTLPSpanExporter(
        endpoint="http://otel-collector:4317",
        # mTLS for secure transport
        credentials=ssl.create_default_context(cafile="/path/to/ca.crt")
    )
)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)

# Instrument with PII-aware attributes
@app.route('/api/patients/<patient_id>')
def get_patient(patient_id):
    with tracer.start_as_current_span("get_patient") as span:
        # Safe: Patient ID is hashed
        span.set_attribute("patient.id", patient_id)

        # UNSAFE: Don't do this! PII in spans
        # span.set_attribute("patient.name", patient.name)  # ❌

        # Safe: Use redacted flag
        span.set_attribute("patient.has_insurance", bool(patient.insurance))

        patient = fetch_patient(patient_id)
        return jsonify(patient)
```

**Total Setup Time:** 400-600 hours (3-6 months)
- Infrastructure setup: 80-120 hours
  - Kubernetes deployment: 20 hours
  - OTel Collector configuration: 20 hours
  - Tempo/Loki/Grafana setup: 20 hours
  - Backup/DR setup: 20 hours
- Security hardening: 80-120 hours
  - mTLS configuration: 20 hours
  - RBAC implementation: 30 hours
  - Encryption at rest: 20 hours
  - Audit logging: 20 hours
- Compliance validation: 80-120 hours
  - PII redaction testing: 30 hours
  - Retention policy implementation: 20 hours
  - Access control testing: 30 hours
  - Documentation for auditors: 40 hours
- Service instrumentation: 160-240 hours
  - 4-6 hours per service × 40 services: 160-240 hours
- Security review: 60-80 hours (external)
  - Penetration testing: 40 hours
  - Compliance audit: 40 hours

**Pros:**
- ✅ Full data control: Data never leaves your infrastructure
- ✅ Cost predictable: Infrastructure cost only, no per-event pricing
- ✅ Compliance customizable: Implement exactly what auditors require
- ✅ Vendor independence: Open-source stack, no vendor lock-in
- ✅ Multi-cloud works: Same stack AWS + on-prem

**Cons:**
- ❌ Massive setup cost: 500 hours = $75K-150K developer time
- ❌ Ongoing ops burden: 40-80 hrs/month = $6K-12K/month
- ❌ Compliance on you: Must maintain certifications yourself
- ❌ Feature gaps: Need to build some tools (anomaly detection, etc.)
- ⚠️ Expertise required: Team needs deep OTel + compliance knowledge

**Total Cost Year 1:**
- Setup: $112,500 (500 hours × $150/hr + $37,500 security review)
- Infrastructure: $36,000 ($3K/mo × 12)
- Maintenance: $108,000 (60 hrs/mo × 12 × $150/hr)
- **Total: $256,500**

**Total Cost Year 2-3:** $144,000/year (infra + maintenance only)

**3-Year Total:** $544,500

### Option C: OpenTelemetry + Compliant Managed Backend

**Vendor Options:**

**Grafana Cloud Enterprise:**
- HIPAA/SOC 2 compliant
- Data residency options
- RBAC built-in
- Pricing: $5K-15K/month depending on volume

**Honeycomb Enterprise:**
- SOC 2 Type II
- SSO/SAML
- Fine-grained access control
- Pricing: $8K-20K/month

**Splunk Observability Cloud:**
- HIPAA/PCI compliant
- Legacy Splunk migration path
- Enterprise security features
- Pricing: $10K-25K/month

**Example: Grafana Cloud Enterprise**

**Setup Process:**

```python
# 1. Service instrumentation (same as Option B)
# Instrument 40 services with OpenTelemetry

# 2. Configure OTel Collector for PII redaction (on your infra)
receivers:
  otlp:
    protocols:
      grpc:

processors:
  # PII redaction (runs in YOUR infrastructure before cloud)
  attributes:
    actions:
      - key: patient.name
        action: delete
      - key: patient.ssn
        action: hash

  # Add compliance metadata
  resource:
    attributes:
      - key: compliance.classification
        value: "phi"

exporters:
  # Export to Grafana Cloud (already compliant)
  otlp/grafana:
    endpoint: otlp-gateway-prod-us-east-1.grafana.net:443
    headers:
      authorization: "Bearer ${GRAFANA_CLOUD_API_KEY}"

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [attributes, resource]
      exporters: [otlp/grafana]
```

**Total Setup Time:** 200-300 hours (1.5-3 months)
- Infrastructure setup: 20-30 hours (just OTel Collector, not backend)
- Security configuration: 40-60 hours (PII redaction, mTLS)
- Compliance validation: 60-80 hours (vendor audit review, BAA signing)
- Service instrumentation: 160-240 hours (same as Option B)
- Security review: 40-60 hours (lighter, vendor has certifications)

**Pros:**
- ✅ Compliance certifications: Vendor maintains SOC 2/HIPAA
- ✅ Vendor independence: Can switch backends (2-3 days work)
- ✅ Lower ops burden: Backend managed, you just instrument
- ✅ Feature complete: Enterprise features built-in
- ✅ Faster setup: 200 hours vs 500 hours self-hosted

**Cons:**
- ⚠️ Data leaves infrastructure: Vendor stores data (but compliant)
- ⚠️ Cost: $60K-180K/year (less than Datadog, more than self-hosted)
- ⚠️ Vendor dependency: Still reliant on one vendor's uptime
- ⚠️ Customization limits: Can't customize backend behavior

**Total Cost Year 1:**
- Setup: $45,000 (250 hours × $150/hr + $7,500 security review)
- Subscription: $120,000 ($10K/mo × 12)
- Maintenance: $36,000 (20 hrs/mo × 12 × $150/hr)
- **Total: $201,000**

**Total Cost Year 2-3:** $156,000/year (subscription + maintenance)

**3-Year Total:** $513,000**

### Option D: Hybrid (OpenTelemetry + Multiple Backends by Sensitivity)

**Strategy:**
- High-sensitivity data (PHI): Self-hosted Tempo (full control)
- Medium-sensitivity (non-PHI business data): Grafana Cloud
- Low-sensitivity (dev/staging): Honeycomb free tier

```yaml
# OTel Collector routes to different backends by data classification
receivers:
  otlp:
    protocols:
      grpc:

processors:
  # Route based on resource attributes
  routing:
    from_attribute: compliance.classification
    table:
      - value: phi
        exporters: [otlp/tempo-self-hosted]
      - value: business
        exporters: [otlp/grafana-cloud]
      - value: dev
        exporters: [otlp/honeycomb]

exporters:
  # PHI data: Self-hosted (full control)
  otlp/tempo-self-hosted:
    endpoint: tempo.internal:4317

  # Business data: Managed (convenience)
  otlp/grafana-cloud:
    endpoint: otlp-gateway-prod-us-east-1.grafana.net:443
    headers:
      authorization: "Bearer ${GRAFANA_API_KEY}"

  # Dev/staging: Free tier (cost optimization)
  otlp/honeycomb:
    endpoint: api.honeycomb.io:443
    headers:
      x-honeycomb-team: "${HONEYCOMB_API_KEY}"

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [routing]
      exporters: [otlp/tempo-self-hosted, otlp/grafana-cloud, otlp/honeycomb]
```

**Total Setup Time:** 300-400 hours
**Total Cost Year 1:** $180,000
**3-Year Total:** $480,000

## Requirement Fit Analysis

| Requirement | Datadog Enterprise | OTel+Self-Hosted | OTel+Managed | Hybrid |
|-------------|-------------------|------------------|--------------|--------|
| Distributed tracing | ✅ Excellent | ✅ Good | ✅ Excellent | ✅ Excellent |
| Compliance certs | ✅ Pre-certified | ⚠️ DIY | ✅ Pre-certified | ⚠️ Partial |
| Data control | ⚠️ Vendor cloud | ✅ Full control | ⚠️ Vendor cloud | ✅ PHI controlled |
| PII redaction | ✅ Built-in | ✅ Custom | ✅ Custom | ✅ Custom |
| RBAC/SSO | ✅ Enterprise | ✅ DIY | ✅ Built-in | ✅ Mixed |
| Audit logging | ✅ Built-in | ✅ Custom | ✅ Built-in | ✅ Mixed |
| Setup <6 months | ✅ 1 month | ⚠️ 4-6 months | ✅ 2-3 months | ⚠️ 3-4 months |
| Vendor independence | ❌ Locked | ✅ Full | ✅ Full | ✅ Full |
| Cost <$300K/yr | ❌ $300K-660K | ✅ $180K | ✅ $200K | ✅ $160K |
| **Total Score** | **7/10** | **7/10** | **9/10** | **8/10** |

## Recommendation: OpenTelemetry + Compliant Managed Backend (Option C)

### Why This Is The Enterprise Sweet Spot

**1. Cost Savings with Acceptable Setup**

```
3-Year Costs:
- Datadog Enterprise: $1,350,000 (average case)
- OTel + Managed: $513,000
- Savings: $837,000 (62% reduction)

Setup Time:
- Datadog: 40 hours (procurement, contracts, deployment)
- OTel + Managed: 250 hours
- Delta: 210 hours ($31,500 one-time cost)

ROI: ($837,000 - $31,500) / $31,500 = 2,557% over 3 years
```

Saving **$837K over 3 years** easily justifies the 250-hour setup investment.

**2. Vendor Independence is Critical for Enterprise**

**Risk Scenario:** Vendor acquired or discontinues product
- **With Datadog:** 6-12 month migration, $500K-1M cost, high business risk
- **With OTel:** 2-3 day backend switch, $5K-10K cost, minimal risk

**Example:** Splunk acquired by Cisco → many enterprises migrating due to uncertainty
- Those on proprietary Splunk SDK: 12-18 month painful migration
- Those on OpenTelemetry: Switch to Grafana Cloud in 1 week

**3. Compliance Requirements Met**

Managed backends like Grafana Cloud Enterprise provide:
- ✅ SOC 2 Type II certification (auditor-approved)
- ✅ HIPAA Business Associate Agreement (BAA) available
- ✅ PCI-DSS compliant if needed
- ✅ Data residency options (US, EU regions)
- ✅ Audit logging built-in

You still control PII redaction (in your OTel Collector before cloud), but vendor handles infrastructure compliance.

**4. Operational Burden Acceptable**

With dedicated platform team (2-4 engineers):
- 20 hrs/month monitoring observability pipeline
- 40 hrs/quarter compliance reviews
- Significantly less than 60 hrs/month for full self-hosted

### Implementation Strategy

**Month 1-2: Foundation & Security Review**

1. **Vendor selection** (Week 1-2):
   - RFP to Grafana Cloud, Honeycomb, Splunk Observability
   - Evaluate compliance certifications
   - Legal review of BAA (Business Associate Agreement)
   - Security review of vendor SOC 2 reports

2. **Pilot architecture** (Week 3-4):
   - Deploy OTel Collector in staging
   - Implement PII redaction rules
   - Configure mTLS to vendor
   - Test 2-3 non-critical services

3. **Compliance validation** (Week 5-6):
   - Validate PII redaction works
   - Test access controls (RBAC)
   - Audit trail testing
   - Document for security team

4. **Security approval** (Week 7-8):
   - Present architecture to security/compliance team
   - Address concerns
   - Get sign-off for production rollout

**Month 3-4: Production Rollout**

1. **Wave 1: Non-PHI services** (Week 9-12):
   - Instrument 10 services with lowest sensitivity
   - Services that don't handle PHI (e.g., marketing site, billing)
   - Build confidence with team

2. **Wave 2: Medium-sensitivity services** (Week 13-16):
   - Instrument 15 services with business data
   - Services with customer data but not PHI
   - Validate tracing across service boundaries

**Month 5-6: PHI Services & Complete Migration**

1. **Wave 3: PHI services** (Week 17-20):
   - Instrument remaining 15 services handling PHI
   - Extra validation of PII redaction
   - Security team review of each service

2. **Documentation & training** (Week 21-24):
   - Runbooks for troubleshooting
   - Training for developers on OTel best practices
   - Compliance documentation for auditors
   - Incident response procedures

3. **Decommission legacy** (Week 25-26):
   - Turn off Splunk/Datadog
   - Archive historical data
   - Update contracts

### Success Criteria

**Month 3:**
- 10 non-PHI services instrumented
- Security review passed
- Team trained on OpenTelemetry basics

**Month 6:**
- All 40 services instrumented
- Legacy APM decommissioned
- Compliance validated (internal audit)
- Cost <$12K/month

**Month 12:**
- Annual security audit passed
- New services instrumented in <4 hours
- Zero compliance incidents
- Backend switch validated (test switch to different vendor)
- Annual cost: $156K (vs $450K Datadog)

**Year 3:**
- Savings recognized: $837K over 3 years
- Vendor independence proven (possibly switched backends once)
- Observability infrastructure stable
- Team expertise in OpenTelemetry mature

## Compliance-Specific Implementation Details

### PII Redaction Patterns

```yaml
# OTel Collector processors for common PII
processors:
  attributes:
    actions:
      # Names
      - key: patient.first_name
        action: delete
      - key: patient.last_name
        action: delete

      # Identifiers
      - key: patient.ssn
        action: hash  # One-way hash for correlation without exposure
      - key: patient.mrn
        action: hash

      # Contact info
      - key: patient.email
        pattern: '([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
        action: redact
        replacement: 'redacted@example.com'

      - key: patient.phone
        pattern: '\d{3}-\d{3}-\d{4}'
        action: redact
        replacement: 'XXX-XXX-XXXX'

      # Addresses
      - key: patient.address
        action: truncate
        max_length: 0  # Remove entirely

      # Keep these (safe)
      - key: patient.age_range
        action: keep  # "18-25", "26-35" - not PII
      - key: patient.state
        action: keep  # State-level OK for analytics
```

### Retention Policies by Regulation

```yaml
# HIPAA: 6 years from creation or last use
storage:
  trace:
    retention: 52560h  # 6 years

# GDPR: Right to be forgotten
# Implement patient ID → trace ID mapping for deletion
erasure:
  enabled: true
  api_endpoint: /api/v1/erasure
  # When patient requests deletion, delete all traces containing patient.id

# SOC 2: Audit trail for 7 years
audit_logs:
  retention: 61320h  # 7 years
```

### Access Control Matrix

| Role | View Traces | View PHI Traces | Export Data | Admin |
|------|-------------|-----------------|-------------|-------|
| Developer | ✅ | ❌ | ❌ | ❌ |
| SRE | ✅ | ⚠️ (on-call only) | ❌ | ❌ |
| Compliance Auditor | ✅ | ✅ | ✅ | ❌ |
| Security Team | ✅ | ✅ | ✅ | ✅ |
| Platform Team | ✅ | ⚠️ (break-glass) | ❌ | ✅ |

## Conclusion

For enterprises with compliance requirements, **OpenTelemetry + compliant managed backend is the optimal choice**. It provides:

1. **Massive cost savings**: $837K over 3 years vs proprietary APM
2. **Vendor independence**: 2-day backend switch vs 12-month migration
3. **Compliance ready**: Vendor certifications + your PII controls
4. **Operational efficiency**: Platform team manages, not entire infra team

The setup investment (250 hours = $37.5K) pays for itself in **3 months** of cost savings vs Datadog Enterprise.

**Action for HealthTech Inc.:**
- Start RFP process with Grafana Cloud, Honeycomb Enterprise, Splunk Observability
- Allocate 2 engineers × 3 months for migration
- Budget $10K/month for managed backend
- Target completion: Q2 2025
- Expected annual savings: $279K

This is not just a technical decision—it's a **strategic cost optimization with enterprise-grade risk mitigation**.
