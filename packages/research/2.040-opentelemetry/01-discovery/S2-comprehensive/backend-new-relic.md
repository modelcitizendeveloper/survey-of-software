# Backend Analysis: New Relic

## Overview

**Type**: Commercial managed observability platform
**Primary Use Case**: Full-stack APM and infrastructure monitoring
**OpenTelemetry Support**: Native OTLP ingestion, major contributor
**Deployment Model**: SaaS (managed service)
**Pricing**: Data ingest + user-based pricing

## OpenTelemetry Protocol Support

### Native OTLP Support
- **OTLP/gRPC**: Supported but not recommended
- **OTLP/HTTP with Protobuf**: **Recommended** (more robust)
- **TLS Requirement**: Must use TLS 1.2+
- **Status**: Native OTLP endpoint, preferred method

**Key Strength**: New Relic is a top contributor to OpenTelemetry and provides native OTLP ingest.

**Evidence**: "New Relic is a top contributor to OpenTelemetry and enables AWS customers to achieve a standardized set of practices for collecting metrics and traces."
Source: Multiple AWS and OpenTelemetry documentation sources

### Protocol Recommendation
New Relic explicitly recommends OTLP/HTTP over gRPC:
- More robust in production
- Better error handling
- No performance degradation

## Configuration Examples

### Direct SDK to New Relic
```bash
# Environment variables for application
export OTEL_EXPORTER_OTLP_ENDPOINT="https://otlp.nr-data.net:4318"
export OTEL_EXPORTER_OTLP_PROTOCOL="http/protobuf"
export OTEL_EXPORTER_OTLP_HEADERS="api-key=YOUR_LICENSE_KEY"
export OTEL_SERVICE_NAME="my-service"

# Optional but recommended for better organization
export OTEL_RESOURCE_ATTRIBUTES="service.name=my-service,deployment.environment=production"
```

### OpenTelemetry Collector to New Relic
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
    send_batch_size: 1000

  # Required to avoid rate limits
  memory_limiter:
    check_interval: 1s
    limit_mib: 512

  resource:
    attributes:
    - key: deployment.environment
      value: production
      action: upsert

exporters:
  otlp/newrelic:
    endpoint: "otlp.nr-data.net:4318"
    headers:
      api-key: "${NEW_RELIC_LICENSE_KEY}"
    timeout: 30s  # Important: increase from default

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch, resource]
      exporters: [otlp/newrelic]
    metrics:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [otlp/newrelic]
    logs:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [otlp/newrelic]
```

### Regional Endpoints
```bash
# US endpoint
export OTEL_EXPORTER_OTLP_ENDPOINT="https://otlp.nr-data.net:4318"

# EU endpoint
export OTEL_EXPORTER_OTLP_ENDPOINT="https://otlp.eu01.nr-data.net:4318"
```

## Feature Support Matrix

| Feature | Support | Notes |
|---------|---------|-------|
| Traces | ✅ Full | Native OTLP support |
| Metrics | ✅ Full | Native OTLP support |
| Logs | ✅ Full | Native OTLP support |
| Span Events | ⚠️ Limited | May not map perfectly |
| Trace/Log Correlation | ⚠️ Limited | Better with New Relic agent |
| Sampling | ✅ Full | Server-side sampling available |
| Service Maps | ✅ Full | Auto-generated |
| Custom Dashboards | ⚠️ Proprietary | NRQL query language |
| Distributed Tracing | ✅ Full | Core feature |
| APM Features | ⚠️ Segregated | OTLP data separate from APM UI |

## Setup Complexity

### Time to First Trace: **1-2 hours**

**Steps**:
1. Create New Relic account and get license key: 10 minutes
2. Configure OTLP endpoint and headers: 5 minutes
3. Configure batch processing (avoid rate limits): 15 minutes
4. Restart application: 5 minutes
5. Verify data in New Relic UI: 10 minutes
6. Navigate UI to find OTLP data: 15 minutes
7. Create initial dashboards: 30-60 minutes

**Production Considerations**:
- Timeout configuration (larger payloads): +30 minutes
- Batch size optimization (rate limits): +1 hour
- Resource attributes strategy: +1-2 hours
- Dashboard and alert setup: +4-8 hours

## Limitations and Gaps

### 1. OpenTelemetry Data is "Second Class Citizen"
**Impact**: OTLP data segregated from main APM experience
**Evidence**: "OpenTelemetry data is segregated in New Relic and not included in the APM experience."
**Quote**: "In both New Relic and Datadog, OpenTelemetry data is a 'second class citizen'."
**Portability Impact**: MEDIUM - pressure to use New Relic agent for full features

### 2. Rate Limits and Payload Restrictions
**Impact**: Requests rejected when rate limits exceeded
**Requirement**: Must configure appropriate batch sizes
**Evidence**: "New Relic imposes rate limits, and when exceeded, requests will be rejected with an error status code."
**Portability Impact**: MEDIUM - requires careful collector tuning

### 3. Attribute Processing Changes (2025)
**Impact**: Changes rolling out June 2, 2025 affect data storage
**Evidence**: "Given New Relic's usage based pricing model, this change means that records that were previously dropped will now be stored and contribute to data usage."
**Portability Impact**: HIGH - may increase costs unexpectedly

### 4. Timeout Considerations
**Impact**: Default timeouts may be too short for large payloads
**Evidence**: "If your application produces large payloads, you may need to increase the default timeout settings to avoid export errors."
**Workaround**: Increase exporter timeout to 30s+
**Portability Impact**: LOW - configuration tweak

### 5. Proprietary Query Language (NRQL)
**Impact**: Dashboards and alerts use New Relic Query Language
**Portability Impact**: HIGH - dashboards don't transfer to other platforms

### 6. Requires TLS 1.2
**Impact**: Must configure TLS, though most SDKs handle this automatically
**Portability Impact**: NONE - modern best practice

## Vendor Lock-in Assessment

### Lock-in Risk: **MEDIUM-HIGH**

**OpenTelemetry Support**:
- ✅ Native OTLP ingestion (no translation)
- ✅ Major contributor to OpenTelemetry project
- ✅ Good documentation for OTLP "happy path"
- ⚠️ OTLP data segregated from main APM UI

**Proprietary Components**:
- ⚠️ NRQL query language for dashboards
- ⚠️ New Relic agent for full APM features
- ⚠️ Alert and monitor configurations
- ⚠️ Custom integrations and plugins

**Migration Path OUT** (Moderate-Complex):
1. Change OTLP endpoint and headers: 30 minutes
2. Remove rate limit workarounds: 1 hour
3. Recreate dashboards (NRQL → new platform): 8-16 hours
4. Recreate alerts: 4-8 hours
5. Test and validate: 4-8 hours
**Total Estimated Time**: **18-33 hours**

**Pressure to Use New Relic Agent**:
- OTLP data not in main APM UI
- Some features only available with agent
- APM experience is separate from OTLP experience

## Cost Considerations

### Pricing Model
- **Data ingest**: $0.30 per GB ingested (traces, metrics, logs)
- **User-based**: $99-549 per user/month depending on tier
- **Free tier**: 100 GB/month ingest included
- **Warning**: Usage-based pricing can be unpredictable

### Rate Limit Implications
- Must batch carefully to avoid rejections
- Large payloads increase timeout needs
- Attribute processing changes (2025) may increase storage costs

### Lock-in Costs
- Dashboard/alert recreation: 12-24 hours engineering time
- Testing and validation: 8-16 hours
- Team retraining: 4-8 hours
- **Total**: 24-48 hours (~$4,800-9,600 at $200/hr)

## Migration Scenarios

### FROM New Relic TO Another Backend

**To Open-Source (Tempo/Jaeger)** (20-30 hours):
```bash
# Easy part: Change endpoint (30 min)
export OTEL_EXPORTER_OTLP_ENDPOINT="http://tempo:4318"
# Remove authentication headers
unset OTEL_EXPORTER_OTLP_HEADERS

# Hard parts:
# - Remove rate limit workarounds: 1 hour
# - Recreate dashboards: 8-16 hours
# - Recreate alerts: 4-8 hours
# - Validate: 4-8 hours
```

**To Another Vendor (Datadog)** (15-25 hours):
```bash
# Endpoint change: 30 min
export OTEL_EXPORTER_OTLP_ENDPOINT="https://api.datadoghq.com"
export OTEL_EXPORTER_OTLP_HEADERS="api-key=${DD_API_KEY}"

# Dashboard/alert migration: 12-20 hours
```

### TO New Relic FROM Another Backend

**From Pure OpenTelemetry (Jaeger/Tempo)** (2-4 hours):
```bash
# Add New Relic endpoint and license key
export OTEL_EXPORTER_OTLP_ENDPOINT="https://otlp.nr-data.net:4318"
export OTEL_EXPORTER_OTLP_HEADERS="api-key=${NEW_RELIC_LICENSE_KEY}"

# Configure batch processing to avoid rate limits: 1-2 hours
# Build dashboards and alerts: +4-8 hours
```

**From Proprietary SDK** (4-8 hours):
- Remove proprietary SDK: 2-4 hours
- Add OpenTelemetry SDK: 1-2 hours
- Configure New Relic endpoint: 30 minutes
- Tune batch processing: 1-2 hours

## Portability Verdict

**PARTIAL PORTABILITY**: ⚠️

**What Works Well**:
- Native OTLP ingestion (no translation layer)
- Major contributor to OpenTelemetry
- Comprehensive documentation for OTLP
- Config-only changes for basic migration (2-4 hours)

**What Breaks Portability**:
- OTLP data segregated from main APM UI
- Proprietary NRQL query language (12-16 hour migration)
- Rate limits require careful tuning
- Attribute processing changes may increase costs

**Reality Check**:
"The New Relic team does a great job of documenting a happy path for OpenTelemetry data. [But] OpenTelemetry data is segregated in New Relic and not included in the APM experience."

**Instrumentation vs Analytics Split**:
- Instrumentation: Pure OpenTelemetry (portable)
- Analytics/Dashboards: Proprietary NRQL (not portable)
- Total migration: 18-33 hours

**Best For**:
- Teams already using New Relic
- Organizations needing enterprise support
- Projects with generous free tier usage (100GB/month)
- Teams comfortable with NRQL

**Avoid If**:
- Want unified APM experience with OpenTelemetry
- Vendor lock-in is a major concern
- Need predictable costs (usage-based can spike)
- Prefer pure OpenTelemetry-native backends

## OpenTelemetry Commitment

**Evidence of Strong Commitment**:
- Top contributor to OpenTelemetry project
- Native OTLP endpoint (no translation)
- Comprehensive OTLP documentation
- Recommends OTLP as primary ingestion method

**But with Caveats**:
- OTLP data not fully integrated into APM UI
- Still maintains proprietary agent for "full" experience
- Query layer remains proprietary (NRQL)

**Verdict**: New Relic supports OpenTelemetry well but treats it as a secondary path alongside their primary APM agent.
