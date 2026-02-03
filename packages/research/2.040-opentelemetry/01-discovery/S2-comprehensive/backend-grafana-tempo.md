# Backend Analysis: Grafana Tempo

## Overview

**Type**: Open-source distributed tracing backend
**Primary Use Case**: Cost-effective, scalable tracing with object storage
**OpenTelemetry Support**: Native OTLP, OpenTelemetry-first design
**Deployment Model**: Self-hosted or Grafana Cloud (managed)
**License**: AGPL v3

## OpenTelemetry Protocol Support

### Native OTLP Support
- **OTLP/gRPC**: Port 4317 (default, preferred)
- **OTLP/HTTP**: Port 4318 (fully supported)
- **Status**: **Native first-class support** - primary ingestion method

**Key Strength**: Tempo was designed with OpenTelemetry as the native protocol from day one.

**Evidence**: Grafana has embraced OpenTelemetry across their stack, with Tempo designed specifically for OTLP ingestion.
Source: https://grafana.com/docs/opentelemetry/

### Additional Protocol Support
- Jaeger (gRPC, Thrift)
- Zipkin (HTTP, JSON)
- OpenCensus

**Note**: While legacy protocols are supported, OTLP is the recommended approach.

## Configuration Examples

### Direct SDK to Tempo
```bash
# Environment variables for application
export OTEL_EXPORTER_OTLP_ENDPOINT="http://tempo:4318"
export OTEL_EXPORTER_OTLP_PROTOCOL="http/protobuf"
export OTEL_SERVICE_NAME="my-service"
```

### OpenTelemetry Collector to Tempo
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
    timeout: 5s
    send_batch_size: 1024

  # Optional: Tail sampling for cost control
  tail_sampling:
    decision_wait: 10s
    policies:
      - name: error-traces
        type: status_code
        status_code:
          status_codes: [ERROR]
      - name: slow-traces
        type: latency
        latency:
          threshold_ms: 1000

exporters:
  otlp/tempo:
    endpoint: "tempo:4317"
    tls:
      insecure: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, tail_sampling]
      exporters: [otlp/tempo]
```

### Tempo Configuration (tempo.yaml)
```yaml
server:
  http_listen_port: 3200

distributor:
  receivers:
    otlp:
      protocols:
        grpc:
          endpoint: 0.0.0.0:4317
        http:
          endpoint: 0.0.0.0:4318

storage:
  trace:
    backend: s3  # or gcs, azure, local
    s3:
      bucket: tempo-traces
      endpoint: s3.amazonaws.com
    pool:
      max_workers: 100
      queue_depth: 10000
```

### Grafana Cloud Tempo
```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="https://tempo-prod-01-prod-us-east-0.grafana.net:443"
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Basic $(echo -n 'user:password' | base64)"
```

## Feature Support Matrix

| Feature | Support | Notes |
|---------|---------|-------|
| Traces | ✅ Full | Primary use case |
| Metrics | ❌ None | Use Mimir/Prometheus |
| Logs | ❌ None | Use Loki |
| Span Events | ✅ Full | Standard OpenTelemetry events |
| Span Links | ✅ Full | Supported and queryable |
| Baggage | ✅ Full | Context propagation works |
| Sampling | ✅ Full | Head-based and tail sampling |
| Service Graphs | ✅ Full | Generated via metrics-generator |
| TraceQL | ✅ Full | Powerful query language |
| Backend Search | ✅ Full | Tag-based and TraceQL queries |

## Setup Complexity

### Time to First Trace: **20-30 minutes (self-hosted)**

**Docker Compose Setup**:
```yaml
version: "3"
services:
  tempo:
    image: grafana/tempo:latest
    command: ["-config.file=/etc/tempo.yaml"]
    volumes:
      - ./tempo.yaml:/etc/tempo.yaml
      - tempo-data:/tmp/tempo
    ports:
      - "3200:3200"  # Tempo HTTP
      - "4317:4317"  # OTLP gRPC
      - "4318:4318"  # OTLP HTTP

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana

volumes:
  tempo-data:
  grafana-data:
```

**Steps**:
1. Deploy Tempo with Docker Compose: 5 minutes
2. Configure Grafana data source: 5 minutes
3. Configure application OTLP endpoint: 2 minutes
4. Restart application: 1 minute
5. Query traces in Grafana: 5 minutes

**Production Considerations**:
- Object storage setup (S3/GCS/Azure): +1-2 hours
- Kubernetes deployment: +2-3 hours
- High availability (multi-replica): +4-6 hours
- Metrics-generator for service graphs: +1 hour

## Limitations and Gaps

### 1. Traces Only
**Impact**: No metrics or logs storage
**Workaround**: Use Grafana stack (Mimir for metrics, Loki for logs)
**Portability Impact**: LOW - encourages multi-backend approach

### 2. Requires Grafana for Visualization
**Impact**: Tempo has no standalone UI, requires Grafana
**Workaround**: Grafana is free and open-source
**Portability Impact**: NONE - Grafana supports multiple backends

### 3. Object Storage Dependency (Production)
**Impact**: Production deployments require S3/GCS/Azure for scalability
**Workaround**: Local storage for dev/testing
**Portability Impact**: NONE - backend storage is internal

### 4. TraceQL Learning Curve
**Impact**: New query language to learn (not standard OpenTelemetry)
**Benefit**: More powerful than basic tag search
**Portability Impact**: MEDIUM - queries don't transfer to other backends

### 5. Metrics-Generator Configuration
**Impact**: Service graphs require additional Tempo configuration
**Workaround**: Well-documented in Tempo docs
**Portability Impact**: NONE - doesn't affect instrumentation

## Vendor Lock-in Assessment

### Lock-in Risk: **VERY LOW**

**Pure OpenTelemetry**:
- ✅ Uses standard OTLP protocol exclusively
- ✅ No proprietary SDKs or agents required
- ✅ No vendor-specific attributes needed
- ✅ Open-source with AGPL license

**Migration Path OUT**:
1. Change OTLP endpoint URL: 30 minutes
2. No code changes required
3. No data export needed (switch live)
4. Recreate dashboards in new UI: 4-8 hours
**Total Estimated Time**: **5-9 hours**

**Proprietary Features**:
- TraceQL query language (but instrumentation is standard)
- Service graphs configuration (Tempo-specific)

**Grafana Lock-in Consideration**:
- Grafana dashboards use Grafana query syntax
- But Grafana supports many backends (Tempo, Jaeger, Zipkin, etc.)
- Switching from Tempo to another backend in Grafana: 5 minutes

## Cost Considerations

### Self-Hosted Costs
- **Infrastructure**: Compute + object storage (S3/GCS)
- **Operational Overhead**: 0.25-0.5 FTE for maintenance
- **Scaling**: Object storage is cheap ($0.023/GB/month on S3)
- **Benefit**: Most cost-effective self-hosted option

### Grafana Cloud Costs
- **Pricing**: $0.50 per GB ingested (traces)
- **Retention**: 30 days included
- **Free tier**: 50GB/month traces

### Cost Comparison
- **Tempo + S3**: Most cost-effective for high volumes
- **Jaeger + Elasticsearch**: More expensive at scale
- **Commercial vendors**: 5-10x more expensive

## Migration Scenarios

### FROM Tempo TO Another Backend

**To Jaeger** (30 minutes):
```bash
# Change only the endpoint
export OTEL_EXPORTER_OTLP_ENDPOINT="http://jaeger:4318"
# No other changes needed
```

**To Managed Service (Honeycomb)** (1-2 hours):
```bash
# Add authentication
export OTEL_EXPORTER_OTLP_ENDPOINT="https://api.honeycomb.io"
export OTEL_EXPORTER_OTLP_HEADERS="x-honeycomb-team=${API_KEY}"
```

**Dashboard Migration**:
- Grafana supports multiple trace backends
- Can point Grafana at new backend: 5-10 minutes
- Or recreate dashboards in new UI: 4-8 hours

### TO Tempo FROM Another Backend

**From Jaeger** (30 minutes):
```bash
# Just change the endpoint
export OTEL_EXPORTER_OTLP_ENDPOINT="http://tempo:4318"
```

**From Any OTLP Source** (30 minutes):
- Simply point OTLP exporter to Tempo endpoint
- Works for: Zipkin, commercial vendors using OTLP

**From Proprietary SDK (Datadog)** (4-8 hours):
- Remove proprietary SDK: 2-4 hours
- Add OpenTelemetry SDK: 1-2 hours
- Configure Tempo endpoint: 30 minutes
- Validate: 1-2 hours

## Portability Verdict

**TRUE PORTABILITY**: ✅

Tempo exemplifies OpenTelemetry's portability promise:
- Config-only migration (environment variables)
- No proprietary SDKs or agents
- Standard OTLP protocol exclusively
- Switch to/from Tempo in under 1 hour

**Key Advantages**:
- Most cost-effective self-hosted option
- Powerful TraceQL query language
- Part of unified Grafana observability stack
- Strong OpenTelemetry commitment

**Limitations**:
- Traces only (not metrics/logs) - use Grafana stack
- Requires Grafana for visualization
- TraceQL queries don't transfer (but instrumentation does)

**Best For**:
- Teams wanting zero vendor lock-in
- Cost-conscious organizations (object storage is cheap)
- Existing Grafana users
- Kubernetes-native environments
- High trace volumes (scales well)

**Avoid If**:
- Need unified traces + metrics + logs in single backend
- Want standalone UI (not Grafana)
- Lack ops team for self-hosted infrastructure
- Prefer fully managed service

## OpenTelemetry Commitment

**Evidence of Strong Commitment**:
- Tempo designed from day one with OTLP as primary protocol
- Grafana Labs is a major OpenTelemetry contributor
- Supports all OTLP signal types through Grafana stack
- Active development aligned with OpenTelemetry standards

**Integration with Grafana Stack**:
- **Tempo**: Traces (OpenTelemetry)
- **Mimir**: Metrics (Prometheus/OpenTelemetry)
- **Loki**: Logs (can ingest OTLP logs)
- **Grafana**: Unified visualization layer

**Verdict**: Tempo is one of the most OpenTelemetry-friendly backends, especially for self-hosted deployments.
