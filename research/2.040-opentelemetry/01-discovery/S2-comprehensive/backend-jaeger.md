# Backend Analysis: Jaeger

## Overview

**Type**: Self-hosted open-source distributed tracing system
**Primary Use Case**: Microservices tracing and latency analysis
**OpenTelemetry Support**: Native OTLP support (v1.35+)
**Deployment Model**: Self-hosted (Docker, Kubernetes, binary)
**License**: Apache 2.0

## OpenTelemetry Protocol Support

### Native OTLP Support (Recommended)
- **OTLP/gRPC**: Port 4317 (default)
- **OTLP/HTTP**: Port 4318 (default)
- **Version**: Native support since Jaeger v1.35 (2022)
- **Status**: **Primary recommended method** as of 2025

**Evidence**: Jaeger project added native OTLP support and deprecated legacy formats.
Source: https://opentelemetry.io/blog/2023/jaeger-exporter-collector-migration/

### Legacy Formats (Deprecated)
- Jaeger Thrift (deprecated)
- Zipkin format support (legacy)
- Native Jaeger protocol (being phased out)

**Important**: Latest OpenTelemetry Collector distributions no longer include Jaeger-native exporters.

## Configuration Examples

### Direct SDK to Jaeger (OTLP)
```bash
# Environment variables for application
export OTEL_EXPORTER_OTLP_ENDPOINT="http://jaeger:4318"
export OTEL_EXPORTER_OTLP_PROTOCOL="http/protobuf"
export OTEL_SERVICE_NAME="my-service"
```

### OpenTelemetry Collector to Jaeger
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
    timeout: 1s
    send_batch_size: 1024

exporters:
  otlp/jaeger:
    endpoint: jaeger:4317
    tls:
      insecure: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlp/jaeger]
```

## Feature Support Matrix

| Feature | Support | Notes |
|---------|---------|-------|
| Traces | ✅ Full | Primary use case |
| Metrics | ❌ None | Jaeger is traces-only |
| Logs | ❌ None | Not supported |
| Span Events | ✅ Full | Standard OpenTelemetry events |
| Span Links | ✅ Full | Supported in trace view |
| Baggage | ✅ Full | Context propagation works |
| Sampling | ✅ Partial | Head-based only, no tail sampling |
| Service Graphs | ✅ Full | Auto-generated from traces |

## Setup Complexity

### Time to First Trace: **15-30 minutes**

**Steps**:
1. Deploy Jaeger (Docker Compose): 5 minutes
2. Configure application OTLP endpoint: 2 minutes
3. Restart application: 1 minute
4. Verify traces in UI: 2 minutes

**Docker Deployment**:
```bash
docker run -d --name jaeger \
  -e COLLECTOR_OTLP_ENABLED=true \
  -p 16686:16686 \
  -p 4317:4317 \
  -p 4318:4318 \
  jaegertracing/all-in-one:latest
```

**Production Considerations**:
- Storage backend setup (Elasticsearch, Cassandra): +2-4 hours
- Kubernetes deployment with operators: +1-2 hours
- High availability configuration: +4-8 hours

## Limitations and Gaps

### 1. Traces Only
**Impact**: Cannot receive metrics or logs through OTLP
**Workaround**: Use separate backends for metrics/logs
**Portability Impact**: Medium - need multi-backend strategy

### 2. Limited Sampling Options
**Impact**: Only head-based sampling supported
**Workaround**: Use OpenTelemetry Collector for tail sampling
**Portability Impact**: Low - sampling config is collector-level

### 3. No Built-in Alerting
**Impact**: Jaeger is visualization-only, no alerting system
**Workaround**: Export to Prometheus for alerts, or use external monitoring
**Portability Impact**: Low - alerting is separate concern

### 4. Storage Scalability
**Impact**: High-cardinality traces require Elasticsearch/Cassandra tuning
**Workaround**: Careful sampling configuration and retention policies
**Portability Impact**: None - backend storage is internal

### 5. Query Language Limitations
**Impact**: Basic tag-based search, no complex TraceQL support (unlike Tempo)
**Workaround**: Filter at collection time with Collector processors
**Portability Impact**: None - query differences don't affect instrumentation

## Vendor Lock-in Assessment

### Lock-in Risk: **VERY LOW**

**Pure OpenTelemetry**:
- Uses standard OTLP protocol exclusively (2025)
- No proprietary SDKs or agents required
- No vendor-specific attributes needed
- Open-source with Apache 2.0 license

**Migration Path OUT**:
- Change OTLP endpoint URL only
- No code changes required
- No data export needed (switch live)
- **Estimated time**: 30 minutes

**Proprietary Features**: None - Jaeger has no vendor extensions

## Cost Considerations

### Self-Hosted Costs
- **Infrastructure**: Compute + storage (Elasticsearch/Cassandra)
- **Operational Overhead**: 0.25-0.5 FTE for maintenance
- **Scaling**: Storage grows with trace volume, can be expensive

### No Licensing Fees
- Open-source, no per-seat or data ingestion costs
- Storage costs depend on retention policies
- Can scale down by aggressive sampling

## Migration Scenarios

### FROM Jaeger TO Another Backend

**To Grafana Tempo** (30 minutes):
```bash
# Change only the endpoint
export OTEL_EXPORTER_OTLP_ENDPOINT="http://tempo:4318"
# No other changes needed
```

**To Zipkin** (30 minutes):
```yaml
# Collector config change only
exporters:
  zipkin:
    endpoint: "http://zipkin:9411/api/v2/spans"
```

**To Managed Service (Datadog/New Relic)** (1-2 hours):
```bash
# Add authentication headers
export OTEL_EXPORTER_OTLP_ENDPOINT="https://api.datadoghq.com"
export OTEL_EXPORTER_OTLP_HEADERS="api-key=YOUR_KEY"
```

### TO Jaeger FROM Another Backend

**From Any OTLP Source** (30 minutes):
- Simply point OTLP exporter to Jaeger endpoint
- Works for: Zipkin, Tempo, vendor-instrumented apps using OTLP

## Portability Verdict

**TRUE PORTABILITY**: ✅

Jaeger exemplifies OpenTelemetry's portability promise:
- Config-only migration (environment variables)
- No proprietary SDKs or agents
- Standard OTLP protocol exclusively
- Switch to/from Jaeger in under 1 hour

**Limitations**:
- Traces only (not metrics/logs) - requires multi-backend approach
- No tail sampling natively - use Collector for advanced sampling

**Best For**:
- Teams wanting zero vendor lock-in
- Microservices tracing requirements
- Development/staging environments
- Organizations with Kubernetes expertise

**Avoid If**:
- Need unified traces + metrics + logs backend
- Require managed service with SLAs
- Want built-in alerting and anomaly detection
- Lack ops team for self-hosted infrastructure
