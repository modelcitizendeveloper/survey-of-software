# Backend Analysis: Datadog

## Overview

**Type**: Commercial managed observability platform
**Primary Use Case**: Full-stack monitoring (APM, infrastructure, logs, RUM)
**OpenTelemetry Support**: OTLP ingestion available but not native
**Deployment Model**: SaaS (managed service)
**Pricing**: Per-host + data ingestion (usage-based)

## OpenTelemetry Protocol Support

### OTLP Support (Translation Layer)
- **OTLP/gRPC**: Supported via Datadog Agent
- **OTLP/HTTP**: Supported via Datadog Agent
- **Status**: OpenTelemetry is a **translation layer**, not native format

**Key Limitation**: Datadog is NOT OpenTelemetry-native. It has a proprietary agent and data model. OTLP data is converted to Datadog's internal format.

**Evidence**: "Datadog is not an OpenTelemetry-native tool. It has a proprietary agent and data model. OTel is a translation layer, not the native language."
Source: https://uptrace.dev/blog/opentelemetry-compatible-platforms

### Architecture Options

**Option 1: OpenTelemetry Collector → Datadog Agent**
```yaml
exporters:
  datadog:
    api:
      key: "${DD_API_KEY}"
      site: datadoghq.com
```

**Option 2: Direct OTLP to Datadog**
```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="https://api.datadoghq.com"
export OTEL_EXPORTER_OTLP_HEADERS="api-key=${DD_API_KEY}"
```

**Option 3: Datadog Agent with OTLP Receiver (Recommended by Datadog)**
```yaml
# Datadog Agent config
otlp_config:
  receiver:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318
```

## Configuration Examples

### OpenTelemetry SDK with Datadog
```bash
# Environment variables
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4318"
export OTEL_SERVICE_NAME="my-service"
export DD_API_KEY="your-api-key"
export DD_SITE="datadoghq.com"
export DD_ENV="production"
export DD_SERVICE="my-service"
export DD_VERSION="1.0.0"
```

### Collector Configuration
```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 10s

  # Datadog-specific attributes
  resource:
    attributes:
    - key: deployment.environment
      value: production
      action: upsert

exporters:
  datadog:
    api:
      key: "${DD_API_KEY}"
      site: datadoghq.com

    # Required for trace correlation
    host_metadata:
      enabled: true
      hostname_source: config_or_system

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, resource]
      exporters: [datadog]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [datadog]
```

## Feature Support Matrix

| Feature | Support | Notes |
|---------|---------|-------|
| Traces | ✅ Full | Converted to Datadog format |
| Metrics | ✅ Full | Converted to Datadog metrics |
| Logs | ✅ Full | Via Datadog Agent recommended |
| Span Events | ⚠️ Limited | May not map perfectly |
| Trace/Log Correlation | ⚠️ Limited | Best with Datadog SDK |
| Sampling | ✅ Full | Datadog handles server-side |
| Service Catalog | ✅ Full | Auto-generated |
| Custom Dashboards | ⚠️ Proprietary | Datadog-specific queries |
| Profiling | ❌ Requires DD SDK | Not available via OTLP |

## Setup Complexity

### Time to First Trace: **1-2 hours**

**Steps**:
1. Create Datadog account and get API key: 10 minutes
2. Deploy Datadog Agent with OTLP config: 20 minutes
3. Configure application OTLP endpoint: 5 minutes
4. Configure required Datadog tags (env, service, version): 10 minutes
5. Verify data in Datadog UI: 10 minutes
6. Set up dashboards and alerts: 30-60 minutes

**Production Considerations**:
- Kubernetes DaemonSet deployment: +1 hour
- Proper tagging strategy: +2-4 hours
- Log correlation setup: +2-3 hours
- Custom dashboard migration: +4-8 hours

## Limitations and Gaps

### 1. Not OpenTelemetry-Native
**Impact**: OpenTelemetry data is "second class citizen"
**Quote**: "In both New Relic and Datadog, OpenTelemetry data is a 'second class citizen' - neither can devote all their time to OpenTelemetry as they have too many legacy customers."
**Portability Impact**: HIGH - vendor-specific features require Datadog SDK

### 2. Feature Parity Issues
**Impact**: More features available with Datadog SDK than OpenTelemetry SDK
**Evidence**: "Using the OpenTelemetry API with the Datadog SDK provides access to more Datadog features than using the OpenTelemetry SDK alone."
**Portability Impact**: HIGH - pressure to use proprietary SDK

### 3. Trace/Log Correlation Limitations
**Impact**: Automatic correlation doesn't work with pure OpenTelemetry
**Evidence**: "Datadog cannot link traces and logs automatically with the DataDog OpenTelemetry tools."
**Workaround**: Manually inject trace IDs into logs
**Portability Impact**: MEDIUM - requires custom logging setup

### 4. Profiling Unavailable
**Impact**: Continuous profiling requires Datadog SDK, not available via OTLP
**Portability Impact**: HIGH - locks you into Datadog SDK for profiling

### 5. Proprietary Query Language
**Impact**: Dashboards and queries use Datadog-specific syntax
**Evidence**: "Dashboards, monitors, and alerts are all built with Datadog's proprietary tools, meaning migrating away means rebuilding everything from scratch."
**Portability Impact**: CRITICAL - dashboard/alert migration is expensive

### 6. Mixed Instrumentation Warning
**Impact**: Datadog warns against mixing OpenTelemetry and Datadog SDKs
**Evidence**: "Datadog recommends avoiding mixed instrumentation - do not use both a Datadog SDK and an OpenTelemetry SDK to instrument the same application."
**Portability Impact**: HIGH - forces all-or-nothing decision

## Vendor Lock-in Assessment

### Lock-in Risk: **HIGH**

**Proprietary Components**:
- Datadog Agent (recommended over vanilla Collector)
- Datadog SDK for full features (profiling, advanced APM)
- Proprietary query language for dashboards
- Custom tagging conventions (dd.env, dd.service)
- Alert and monitor configurations

**Migration Path OUT** (Complex):
1. Change OTLP endpoint: 30 minutes
2. Remove Datadog-specific tags: 1-2 hours
3. Rebuild dashboards in new platform: 8-20 hours
4. Recreate alerts and monitors: 4-8 hours
5. Test and validate: 4-8 hours
**Total Estimated Time**: **15-35 hours**

**Pressure to Use Datadog SDK**:
- Better features with proprietary SDK
- OpenTelemetry treated as "ingestion pipeline"
- Profiling only works with Datadog SDK

## Cost Considerations

### Pricing Model
- **Host-based pricing**: $15-31/host/month (APM)
- **Data ingestion**: Additional costs for logs, custom metrics
- **Retention**: Extra costs for extended retention
- **Warning**: Can become very expensive at scale

### Lock-in Costs
- Dashboard/alert recreation: 20-40 hours engineering time
- Testing and validation: 10-20 hours
- Training team on new platform: 4-8 hours
- Risk of downtime during migration: potential revenue impact

## Migration Scenarios

### FROM Datadog TO Another Backend

**To Open-Source (Jaeger/Tempo)** (20-30 hours):
```bash
# Easy part: Change endpoint (30 min)
export OTEL_EXPORTER_OTLP_ENDPOINT="http://tempo:4318"

# Hard parts:
# - Recreate dashboards: 8-16 hours
# - Recreate alerts: 4-8 hours
# - Remove Datadog-specific instrumentation: 2-4 hours
# - Test and validate: 4-8 hours
```

**To Another Vendor (New Relic)** (15-25 hours):
```bash
# Endpoint change: 30 min
export OTEL_EXPORTER_OTLP_ENDPOINT="https://otlp.nr-data.net"
export OTEL_EXPORTER_OTLP_HEADERS="api-key=${NEW_RELIC_LICENSE_KEY}"

# Still need to recreate dashboards and alerts
```

### TO Datadog FROM Another Backend

**From Pure OpenTelemetry** (2-4 hours):
```bash
# Add Datadog endpoint and API key
export OTEL_EXPORTER_OTLP_ENDPOINT="https://api.datadoghq.com"
export OTEL_EXPORTER_OTLP_HEADERS="api-key=${DD_API_KEY}"
export DD_ENV="production"
export DD_SERVICE="my-service"

# But: Won't get full Datadog features without SDK migration
```

## Portability Verdict

**PARTIAL PORTABILITY**: ⚠️

**What Works Well**:
- Basic trace/metric ingestion via OTLP
- Config-only changes to START sending to Datadog
- Can run alongside other backends temporarily

**What Breaks Portability**:
- Proprietary dashboards and alerts (20-40 hour migration)
- Pressure to use Datadog SDK for full features
- Trace/log correlation requires manual work
- Profiling unavailable via OpenTelemetry

**Reality Check**:
"Datadog's approach feels like using OTel as an ingestion pipeline, not as a core philosophy."

**Best For**:
- Teams already committed to Datadog ecosystem
- Organizations needing enterprise support
- Full-stack monitoring with single vendor
- Teams not prioritizing portability

**Avoid If**:
- Vendor lock-in is a concern
- Budget is constrained (can get expensive)
- Want pure OpenTelemetry-native experience
- Planning to maintain backend flexibility
