# Backend Analysis: Zipkin

## Overview

**Type**: Open-source distributed tracing system
**Primary Use Case**: Simple, lightweight tracing for microservices
**OpenTelemetry Support**: OTLP supported, also legacy Zipkin protocol
**Deployment Model**: Self-hosted (Docker, Kubernetes, standalone JAR)
**License**: Apache 2.0

## OpenTelemetry Protocol Support

### OTLP Support
- **OTLP/gRPC**: Supported via collector translation
- **OTLP/HTTP**: Supported via collector translation
- **Status**: OTLP ingestion works but requires translation

**Note**: Zipkin natively uses Zipkin format, not OTLP. OpenTelemetry Collector translates OTLP to Zipkin format.

### Native Zipkin Protocol
- **Zipkin v2 API**: POST /api/v2/spans (JSON or protobuf)
- **Port**: 9411 (default HTTP endpoint)
- **Format**: Zipkin JSON or protobuf

**Evidence**: "Zipkin can also ingest data from OpenTelemetry-instrumented applications" via protocol conversion.
Source: https://signoz.io/blog/jaeger-vs-zipkin/

## Configuration Examples

### OpenTelemetry SDK to Zipkin (via Collector)
```bash
# Application sends OTLP to Collector
export OTEL_EXPORTER_OTLP_ENDPOINT="http://collector:4318"
export OTEL_SERVICE_NAME="my-service"
```

### OpenTelemetry Collector to Zipkin
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

exporters:
  zipkin:
    endpoint: "http://zipkin:9411/api/v2/spans"
    format: json  # or proto
    # Optional: customize service name
    default_service_name: "my-service"

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [zipkin]
```

### Direct Zipkin Export (Some SDKs)
```bash
# Some OpenTelemetry SDKs support direct Zipkin export
# Python example
export OTEL_TRACES_EXPORTER=zipkin
export OTEL_EXPORTER_ZIPKIN_ENDPOINT="http://zipkin:9411/api/v2/spans"
```

## Feature Support Matrix

| Feature | Support | Notes |
|---------|---------|-------|
| Traces | ✅ Full | Primary use case |
| Metrics | ❌ None | Zipkin is traces-only |
| Logs | ❌ None | Not supported |
| Span Events | ⚠️ Limited | Converted to annotations |
| Span Links | ⚠️ Limited | May not map perfectly |
| Baggage | ⚠️ Limited | Zipkin baggage format differs |
| Sampling | ✅ Basic | Head-based sampling only |
| Service Graphs | ✅ Full | Auto-generated dependency graph |
| Query | ✅ Basic | Tag-based search, simple UI |

## Setup Complexity

### Time to First Trace: **10-15 minutes**

**Docker Deployment**:
```bash
# Simplest possible setup
docker run -d -p 9411:9411 openzipkin/zipkin
```

**With OpenTelemetry Collector**:
```bash
# 1. Start Zipkin
docker run -d --name zipkin -p 9411:9411 openzipkin/zipkin

# 2. Configure and start Collector (see config above): 5 minutes
# 3. Point application to Collector: 2 minutes
# 4. View traces at http://localhost:9411: 2 minutes
```

**Docker Compose**:
```yaml
version: '3'
services:
  zipkin:
    image: openzipkin/zipkin:latest
    ports:
      - "9411:9411"
    environment:
      - STORAGE_TYPE=mem  # or mysql, elasticsearch, cassandra

  otel-collector:
    image: otel/opentelemetry-collector-contrib:latest
    command: ["--config=/etc/otel-collector-config.yaml"]
    volumes:
      - ./otel-collector-config.yaml:/etc/otel-collector-config.yaml
    ports:
      - "4317:4317"
      - "4318:4318"
```

**Production Considerations**:
- Storage backend setup (MySQL, Elasticsearch): +2-4 hours
- Kubernetes deployment: +1-2 hours
- High availability: +4-6 hours

## Limitations and Gaps

### 1. Not OTLP-Native
**Impact**: Requires protocol translation from OTLP to Zipkin format
**Portability Impact**: LOW - translation is handled by Collector
**Note**: Some semantic information may be lost in translation

### 2. Traces Only
**Impact**: Cannot receive metrics or logs
**Workaround**: Use separate backends for metrics/logs
**Portability Impact**: MEDIUM - need multi-backend strategy

### 3. Limited Sampling Options
**Impact**: Only head-based sampling supported
**Workaround**: Use OpenTelemetry Collector for tail sampling
**Portability Impact**: LOW - sampling config is collector-level

### 4. Basic Query Capabilities
**Impact**: Simple tag-based search, no complex query language
**Comparison**: Less powerful than TraceQL (Tempo) or BubbleUp (Honeycomb)
**Portability Impact**: NONE - query differences don't affect instrumentation

### 5. In-Memory Storage Default
**Impact**: Default storage is in-memory (not persistent)
**Workaround**: Configure MySQL, Elasticsearch, or Cassandra backend
**Portability Impact**: NONE - backend storage is internal

### 6. Simple UI
**Impact**: Basic visualization, less feature-rich than Jaeger
**Evidence**: "Jaeger handles approximately 2,000 spans per second with proper backend optimization, supports TraceQL for complex filtering."
**Comparison**: Zipkin is simpler but also more limited
**Portability Impact**: NONE - UI doesn't affect instrumentation

## Vendor Lock-in Assessment

### Lock-in Risk: **VERY LOW**

**Pure OpenTelemetry (via Collector)**:
- ✅ Application uses standard OTLP
- ✅ No proprietary SDKs required
- ✅ No vendor-specific attributes needed
- ✅ Open-source with Apache 2.0 license

**Migration Path OUT**:
1. Change Collector exporter from zipkin to otlp: 5 minutes
2. Point to new backend endpoint: 2 minutes
3. No code changes required
**Total Estimated Time**: **10-15 minutes**

**Proprietary Features**: None - Zipkin has no vendor extensions

**Note**: If using Zipkin SDK directly (not via OpenTelemetry), migration is harder (4-8 hours to instrument with OpenTelemetry).

## Cost Considerations

### Self-Hosted Costs
- **Infrastructure**: Compute + storage (MySQL/Elasticsearch)
- **Operational Overhead**: 0.1-0.25 FTE for maintenance
- **Scaling**: Simpler than Jaeger, lighter resource usage
- **Benefit**: Lightweight, easy to run

### No Licensing Fees
- Open-source, no per-seat or data ingestion costs
- Storage costs depend on retention policies
- Generally cheaper to run than Jaeger (simpler architecture)

### Comparison
- **Zipkin**: Simplest, lightest, least features
- **Jaeger**: More features, heavier, more complex
- **Tempo**: Most scalable, requires object storage

## Migration Scenarios

### FROM Zipkin TO Another Backend

**To Jaeger/Tempo** (15-30 minutes):
```yaml
# Change Collector exporter only
exporters:
  otlp/jaeger:
    endpoint: "jaeger:4317"
    tls:
      insecure: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlp/jaeger]  # changed from zipkin
```

**To Managed Service (Honeycomb)** (30 minutes):
```yaml
exporters:
  otlp/honeycomb:
    endpoint: "api.honeycomb.io:443"
    headers:
      "x-honeycomb-team": "${HONEYCOMB_API_KEY}"

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlp/honeycomb]
```

**Application Code Changes**: NONE (if using OTLP already)

### TO Zipkin FROM Another Backend

**From Any OpenTelemetry Source** (15 minutes):
```yaml
# Just add Zipkin exporter to Collector
exporters:
  zipkin:
    endpoint: "http://zipkin:9411/api/v2/spans"
```

**From Jaeger** (15 minutes):
- Change collector exporter: 5 minutes
- Restart collector: 1 minute
- Verify traces in Zipkin: 5 minutes

## Portability Verdict

**TRUE PORTABILITY**: ✅

Zipkin works well with OpenTelemetry's portability promise:
- Config-only migration (collector configuration)
- No proprietary SDKs or agents needed
- Switch to/from Zipkin in under 30 minutes
- Lightweight and simple

**Key Advantages**:
- Simplest to deploy and operate
- Very lightweight resource usage
- Mature and stable (existed before OpenTelemetry)
- Good for development/testing environments

**Limitations**:
- Traces only (not metrics/logs)
- OTLP requires translation (minor semantic loss)
- Basic query capabilities
- Simpler UI compared to alternatives

**Best For**:
- Small teams wanting simple tracing
- Development and testing environments
- Budget-conscious projects
- Teams wanting minimal operational overhead
- Existing Zipkin users migrating to OpenTelemetry

**Avoid If**:
- Need unified traces + metrics + logs backend
- Want advanced query capabilities (use Tempo)
- Require high-scale production tracing (use Jaeger/Tempo)
- Need sophisticated visualizations
- Want managed service (Zipkin is self-hosted only)

## Jaeger vs Zipkin Comparison

**When to Choose Zipkin Over Jaeger**:
- Prefer simplicity over features
- Lighter resource requirements
- Easier to understand and maintain
- Faster initial setup

**When to Choose Jaeger Over Zipkin**:
- Need native OTLP support (no translation)
- Want more sophisticated UI
- Require adaptive sampling
- Need better scaling for high volumes

**Portability**: Both are equally portable with OpenTelemetry Collector

## OpenTelemetry Commitment

**Evidence**:
- Zipkin predates OpenTelemetry (since 2012)
- Compatible with OpenTelemetry via protocol translation
- Can ingest data from OpenTelemetry-instrumented applications
- Active community, stable project

**Reality**:
Zipkin is not OpenTelemetry-native (uses its own format), but the Collector bridge works well. For new projects, Jaeger (native OTLP) or Tempo might be better choices.

**Verdict**: Zipkin is a good choice for simplicity, but Jaeger/Tempo have better OpenTelemetry integration.
