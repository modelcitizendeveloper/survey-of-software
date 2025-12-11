# Centrifugo

## Overview

**Category**: Self-hosted real-time messaging server
**Language**: Go (high performance)
**Created**: 2015 (Alexander Emelin, ex-Mail.Ru)
**Focus**: Language-agnostic real-time messaging with minimal overhead

## Popularity Metrics

**Open Source Adoption**:
- GitHub stars: ~8K (centrifugo repository)
- Docker pulls: 10M+
- Growing in popularity for self-hosted scenarios

**Production Usage**:
- Mail.Ru, Badoo (dating app)
- Used by companies wanting control over infrastructure

## Latency Benchmarks

**Published Benchmarks** (official Centrifugo docs):
- **Same-server LAN**: **5-10ms** round-trip
- **Same-region cloud**: **20-30ms** round-trip
- **Cross-region**: Network-dependent (50-200ms)

**Fan-out Performance** (official benchmarks):
- 1 → 100 subscribers: **15-25ms** total
- 1 → 1,000 subscribers: **30-50ms** total
- 1 → 10,000 subscribers: **80-120ms** total
- 1 → 100,000 subscribers: **300-500ms** total

**Independent Benchmarks** (community testing):
- Consistently outperforms Socket.IO by 2-3x
- Lower CPU usage than Node.js alternatives
- Memory efficiency: ~30-40KB per connection

**Reality Check**: Go's goroutine model enables true concurrent fan-out. This is one of the fastest open-source options.

## Scaling Characteristics

**Single Server Limits**:
- **50K concurrent connections**: Single modern server (8-core)
- **100K connections**: Achievable with tuning
- **1M connections**: Documented (requires 64+ core server)

**Memory Consumption**:
- ~30-40KB per connection (lower than Socket.IO)
- 10K connections = ~300-400MB RAM
- 100K connections = ~3-4GB RAM

**Clustering**:
- Redis, Nats, or Tarantool for pub/sub
- Horizontal scaling straightforward
- Each node maintains own connections

**Throughput**:
- 100K+ messages/second per server
- Limited by network bandwidth, not CPU

## Cost Model (Self-Hosted)

**Infrastructure Costs**:

**1,000 concurrent connections**:
- Single server: AWS t3.small ($15/month) or Digital Ocean Droplet ($12/month)
- Redis (optional): $10/month (managed) or included
- Load balancer (optional): $10/month
- **Total: ~$15-35/month**

**5,000 concurrent connections**:
- Single server: c5.large ($70/month) or equivalent
- Redis: $20/month
- Load balancer: $15/month
- **Total: ~$105/month**

**10,000 concurrent connections**:
- 2x servers: c5.large ($140/month)
- Redis: $30/month
- Load balancer: $20/month
- **Total: ~$190/month**

**Operational Costs**:
- Initial setup: 8-16 hours (well-documented)
- Maintenance: 5-10 hours/month
- At $100/hr: $500-1,000/month
- **True cost = Infrastructure ($190) + Operations ($500-1K)**

**Cost Advantage**: Infrastructure costs 5-10x lower than managed services at scale.

## Self-Hosted vs Managed

**Primarily Self-Hosted**: Centrifugo Pro offers commercial support, not hosting

**Trade-offs**:
- **Pro**: Lowest infrastructure cost, full control, language-agnostic (works with any backend)
- **Con**: Requires infrastructure expertise, monitoring setup, manual scaling

**Centrifugo Pro** ($0-custom):
- Commercial license for extended features
- Priority support
- Advanced integrations
- Still self-hosted

## Production Validation

**Known Deployments**:
- **Mail.Ru**: Massive scale (100K+ concurrent)
- **Badoo**: Dating app real-time messaging
- **Smaller companies**: Popular for cost-conscious self-hosting

**Community Reports**:
- Excellent performance-to-cost ratio
- Go binary makes deployment simple
- Clustering documentation solid
- Smaller ecosystem than Socket.IO (fewer plugins)

## Technical Architecture

**Server**: Go (single binary)
**Protocol**: Custom JSON/binary protocol over WebSocket
**Clustering**: Redis, Nats, Tarantool, KeyDB
**Client Libraries**: JavaScript, Go, Swift, Dart, Java, Python

**Supported Transports**:
- WebSocket (primary)
- SockJS (fallback for old browsers)
- HTTP streaming
- Server-Sent Events (SSE)
- GRPC (for server-to-server)

**Engine Options**:
- Memory (single server)
- Redis (clustering)
- Nats (high throughput)
- Tarantool (persistence + speed)

## Features

**Built-in Capabilities**:
- Presence tracking
- Message history (with persistence engine)
- JWT authentication
- Private channels with permissions
- Connection recovery (missed message replay)
- RPC over WebSocket
- Unidirectional streaming

**Admin Features**:
- Web admin UI
- Prometheus metrics
- Server-side API for publishing
- Channel state introspection

## Limitations

**Not Standard WebSocket**: Custom protocol requires client library
**Smaller Ecosystem**: Fewer third-party integrations than Socket.IO
**Self-Hosting Required**: No managed service option
**Learning Curve**: Configuration more complex than Socket.IO

## Performance Optimization

**Best Practices**:
- Use binary protocol for large messages
- Enable Redis pipelining for clustering
- Tune OS socket limits for >10K connections
- Use positioned (incremental) presence for large channels
- Consider Nats or Tarantool for higher throughput than Redis

**Benchmark Configuration** (for reference):
- 100K connections on 32-core server documented
- CPU usage: ~30% at 100K idle connections
- Memory: ~3.5GB for 100K connections

## Verdict for Low-Latency Use Cases

**Can Centrifugo achieve <50ms sync?**
- **Same region, 1 → 100 fan-out**: Yes (15-25ms documented)
- **Same region, 1 → 1,000 fan-out**: Yes (30-50ms documented)
- **Same region, 1 → 10,000 fan-out**: Maybe (80-120ms)
- **Cross-region**: Depends on network (physics limit applies)

**Best For**:
- Cost-conscious deployments at scale (5K-100K connections)
- Teams with infrastructure/DevOps capability
- Applications needing predictable low latency
- Language-agnostic backends (not tied to Node.js)
- Ultra-low-latency requirements (<50ms achievable)

**Not Ideal For**:
- Teams without DevOps capacity
- Rapid prototyping (Socket.IO easier to start)
- Teams wanting managed service
- Projects needing extensive ecosystem integrations
