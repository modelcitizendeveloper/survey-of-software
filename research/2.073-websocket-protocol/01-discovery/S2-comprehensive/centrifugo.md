# Centrifugo: Scalable Real-time Messaging Server

**Category**: Self-Hosted / Open Source
**Provider**: Centrifugo (open source, Go-based)
**Primary Use Case**: High-performance real-time messaging server
**Date Compiled**: December 3, 2025

## Architecture Overview

Centrifugo is a self-hosted real-time messaging server written in Go, designed for high performance and horizontal scalability. It provides a language-agnostic server that client applications connect to via WebSocket, with backend systems publishing messages via API or library integrations.

### Core Components

**Centrifugo Server** (Go binary):
- Standalone executable (no runtime dependencies)
- WebSocket, SockJS (fallback), HTTP streaming, SSE support
- Built-in scalability with Redis, KeyDB, or Nats engines
- Rich admin web UI for monitoring and debugging

**Client SDKs**:
- JavaScript (centrifuge-js)
- Go, Python, Ruby, PHP, Java, Swift, Dart (Flutter)
- Protocol: JSON or Protobuf

**Backend Integration**:
- HTTP API (publish messages from server)
- GRPC API (high-performance publishing)
- Client libraries (Go, Python, etc.)

**Engines** (for scaling):
- **Memory**: Single-server mode (no external dependencies)
- **Redis**: Horizontal scaling with Redis pub/sub
- **KeyDB**: Redis-compatible, multi-threaded alternative
- **Nats**: Alternative message broker for scaling

## Feature Analysis

### Connection Management
- **Auto-reconnection**: Built into client libraries
- **Connection expiration**: Configurable token TTL with refresh
- **TLS/SSL**: Standard configuration via config file
- **Connection limits**: Configurable per-server, tested to 1M+ connections

### Message Delivery
- **Delivery guarantee**: At-most-once (default), at-least-once (with history + recovery)
- **Message ordering**: Guaranteed per channel (offset-based sequencing)
- **Max message size**: Configurable (default 64KB, can increase)
- **Idempotency**: Supported via message offset tracking

### Channel System
- **Namespaces**: Logical grouping with separate configuration
- **Private channels**: Server-side token validation
- **User-specific channels**: Route messages to specific users
- **Channel patterns**: Wildcard subscriptions (pattern channels)

### Advanced Features
- **History & recovery**: Message persistence with configurable retention
- **Presence**: Track online users per channel
- **Join/Leave messages**: Automatic notifications
- **Online status**: Track user connection state
- **Delta compression**: Efficiently send incremental updates (fossil delta)
- **RPC**: Client → Server RPC calls over WebSocket
- **Unidirectional transport**: Server → Client only mode (no client publish)

## Portability Assessment

### Lock-in Risk: LOW

**Vendor-Specific Elements**:
1. **Centrifugo protocol**: Client-server message format (JSON or Protobuf)
2. **Token format**: JWT with Centrifugo-specific claims
3. **Admin UI**: Centrifugo-specific monitoring interface

**Migration Path Complexity**:
- **To managed service**: Moderate (map channels to service concepts, reimplement auth)
- **To other self-hosted**: Low-Moderate (similar architectures, standardize on WebSocket)
- **To raw WebSocket**: Low (protocol is simple, can wrap/unwrap)

**Portable Elements**:
- **Open source**: MIT license, fork-friendly
- **Stateless server**: Easy to containerize and orchestrate
- **Standard WebSocket**: Can intercept/proxy at protocol level
- **Language-agnostic**: Backend can be any language (HTTP/GRPC API)

### Data Portability
- **Complete control**: Self-hosted, all data in your infrastructure
- **Message history**: Stored in Redis (exportable)
- **Configuration**: JSON/YAML config files (version control friendly)
- **No vendor lock**: Can migrate to any infrastructure

## Latency Benchmarks

### Published Benchmarks

**Single-server performance** (official benchmarks, 2024-2025):
- **Connections**: 1,000,000+ concurrent on single server (64GB RAM)
- **Messages/sec**: 100,000+ (with Redis engine)
- **CPU efficiency**: Go's efficiency shines (vs. Node.js)
- **Memory**: ~700 bytes per connection (idle)

**Latency characteristics** (same region):
- **Memory engine**: 3-8ms median round-trip (fastest possible)
- **Redis engine**: 8-20ms median (+ Redis pub/sub latency)
- **KeyDB engine**: 6-15ms median (better than Redis due to multi-threading)

### Community-Reported Performance

**Low-Latency Scenarios** (trading systems, gaming):
- Median: 8-15ms (same data center, Redis engine)
- P95: 20-35ms
- P99: 40-80ms
- **Jitter**: Very low (±3-5ms) due to Go's runtime efficiency

**High-Load Scenarios** (100,000+ concurrent connections):
- Median: 10-25ms (excellent performance under load)
- P95: 30-60ms
- **Graceful degradation**: Go's goroutines handle concurrency well

**Horizontal Scaling (Redis-based)**:
- Median: 12-28ms (includes Redis pub/sub overhead)
- Redis latency becomes dominant factor (optimize Redis placement)

**Geographic Performance**:
- Deploy servers in multiple regions
- Expected: 5-20ms intra-region, 80-250ms cross-region (network-bound)
- **Fastest self-hosted option** based on benchmarks

### Performance Tuning Options
- **Engine selection**: Memory (fastest, single-server), Redis (scalable), Nats (alternative)
- **Protobuf encoding**: 2-3x faster than JSON encoding
- **Connection sharding**: Multiple Centrifugo instances with client-side routing
- **Redis optimization**: Use KeyDB or Redis Enterprise for lower latency
- **Compression**: Enable for large messages (trade CPU for bandwidth)

## Cost Analysis

### Infrastructure Requirements

**Single Server** (medium deployment):
- **Compute**: 4 vCPU, 8GB RAM (handles ~50K connections)
- **Cloud cost**: $60-100/month (AWS c5.xlarge, DigitalOcean CPU-optimized)
- **Network**: Typically included

**Multi-Server** (horizontal scaling):
- **Compute**: 3-5 Centrifugo servers ($300-500/month)
- **Redis/KeyDB**: Managed instance ($100-300/month) or self-hosted ($50-100)
- **Load balancer**: $20-50/month
- **Total**: $420-850/month for 100,000+ concurrent connections

**Enterprise Scale** (very large deployment):
- **Compute**: Auto-scaling, 10-20 instances ($1,000-2,000/month)
- **Redis**: High-availability cluster ($500-1,000/month)
- **Monitoring**: $100-300/month
- **Total**: $1,600-3,300/month for 500,000+ concurrent connections

### Operational Costs

**DevOps/Engineering**:
- **Setup**: 20-40 hours (simpler than Socket.io due to single binary)
- **Ongoing**: 8-15 hours/month (monitoring, updates)
- **Cost estimate**: $2,500-5,000 setup + $800-1,500/month ongoing

**Third-Party Services**:
- **Monitoring**: Prometheus + Grafana (free/self-hosted) or $50-200/month (managed)
- **Logging**: $50-150/month
- **Total**: $100-350/month

### Cost Scenarios

**Scenario 1: Small Event** (1,000 concurrent, 2 hours)
- Infrastructure: Single server ($80/month or $2.66/day)
- Memory engine (no Redis needed)
- **Event cost**: $2.66 (pro-rated)
- **vs. Pusher**: 30x cheaper

**Scenario 2: Medium SaaS Dashboard** (5,000 concurrent, 4.8M messages/day)
- Infrastructure: Single server + Redis ($160/month)
- Monitoring: $100/month (Grafana Cloud)
- Ops time: $1,000/month (10 hours)
- **Monthly cost**: $1,260
- **vs. Ably**: Comparable to Ably ($547), higher with ops time

**Scenario 3: Large Platform** (10,000 concurrent, 72M messages/day)
- Infrastructure: 3 servers + Redis HA ($600/month)
- Monitoring: $200/month
- Ops time: $1,500/month (15 hours)
- **Monthly cost**: $2,300
- **vs. Ably**: Cheaper than Ably ($3-5K), better performance

### Break-Even Analysis

**When Centrifugo becomes economical**:
- **Small scale** (<1K): Managed services easier (unless extreme latency needs)
- **Medium scale** (5K-10K): Comparable to managed, faster performance
- **Large scale** (50K+): Significantly cheaper than managed (40-60% savings)
- **Extreme scale** (500K+): Massive savings (70-80% cheaper than managed)

**Critical advantage**: Lower ops overhead than Socket.io (single binary vs. Node.js ecosystem)

## Operational Considerations

### Developer Experience
**Strengths**:
- Excellent documentation with examples
- Single binary deployment (no runtime dependencies)
- Built-in admin UI (monitoring, debugging)
- Active community and commercial support available
- Prometheus metrics out-of-the-box

**Weaknesses**:
- Smaller community than Socket.io (less Stack Overflow content)
- Requires understanding client-server architecture (not just library)
- Go knowledge helpful but not required (server is pre-built binary)

### Scalability
**Vertical scaling**: Single server can handle 100K+ connections
**Horizontal scaling**: Redis/Nats engines for distributed deployments
**Excellent scalability**: Go's concurrency model handles load efficiently

**Scaling strategies**:
1. **Single server (Memory engine)**: Up to 50-100K connections
2. **Single server (Redis engine)**: Up to 200K connections with offloaded pub/sub
3. **Multi-server (Redis/Nats)**: Millions of connections

### Monitoring & Observability
**Built-in**:
- Admin web UI (real-time stats, debugging)
- Prometheus metrics endpoint
- Health check endpoints
- Debug mode with verbose logging

**Recommended stack**:
- Prometheus + Grafana (metrics dashboards)
- Loki (log aggregation)
- Alertmanager (alerts)

### Deployment
**Containerization**: Docker image provided, or build custom
**Orchestration**: Kubernetes-friendly (stateless with Redis)
**Cloud platforms**: Any compute platform (AWS, GCP, Azure, DigitalOcean)
**Binary deployment**: Single executable, minimal dependencies

## Security & Compliance

### Authentication
- **JWT tokens**: Standard JWT with Centrifugo-specific claims
- **Connection tokens**: Short-lived, server-issued
- **Subscription tokens**: Private channel authorization
- **Proxy mode**: Delegate auth to backend via HTTP callbacks

### Encryption
- **TLS in transit**: Configure via config file or reverse proxy
- **End-to-end**: Application-level (encrypt payloads)

### Compliance
- **Self-hosted**: Full control over compliance requirements
- **Data residency**: Deploy in required regions
- **Audit logs**: Custom implementation via logging

## Comparison to Alternatives

**vs. Socket.io**:
- Centrifugo: Better performance (Go vs. Node.js), lower memory, better observability
- Socket.io: Larger community, JavaScript ecosystem familiarity

**vs. Pusher/Ably**:
- Centrifugo: Self-hosted, faster, cheaper at scale
- Managed: Zero ops, global infrastructure, easier to start

**vs. Supabase Realtime**:
- Centrifugo: General-purpose, database-agnostic, faster
- Supabase: Database-driven, integrated with Postgres, simpler for DB use cases

## Recommendation Context

**Best For**:
- Performance-critical applications (gaming, trading, real-time collaboration)
- Large-scale deployments (10K+ connections) with ops capacity
- Teams wanting better performance than Socket.io with similar control
- Cost-sensitive projects at scale
- Low-latency requirements (<20ms)
- Organizations with Go expertise (for customization)

**Not Ideal For**:
- Teams without DevOps resources
- Rapid prototyping (managed services faster to start)
- Very small projects (<500 connections)
- Organizations requiring 24/7 support (unless paying for commercial support)

## Migration Considerations

**Exiting Centrifugo**:
1. Replace client library (centrifuge-js → new provider)
2. Migrate publish logic (HTTP/GRPC API → new API)
3. Remap channels/namespaces to new concepts
4. Replace JWT token generation
5. Migrate message history (if used)

**Estimated effort**: 2-4 weeks for medium application

**Entering Centrifugo** (from managed service):
1. Deploy Centrifugo server (single binary or Docker)
2. Configure Redis for scaling (if needed)
3. Implement JWT token generation on backend
4. Integrate client libraries
5. Set up monitoring (Prometheus + Grafana)
6. Migrate publish logic to Centrifugo API

**Estimated effort**: 3-6 weeks including infrastructure and testing

## Commercial Support

**Centrifugo PRO**:
- Commercial license available
- Priority support from maintainers
- Additional features (analytics, advanced monitoring)
- Consulting services

**Cost**: Custom pricing (contact vendor)

## References & Resources

- Official documentation: https://centrifugal.dev
- GitHub: https://github.com/centrifugal/centrifugo
- Admin UI demo: https://centrifugo.herokuapp.com (username: admin, password: admin)
- Benchmarks: https://centrifugal.dev/docs/server/benchmark
- Community: GitHub Discussions, Telegram, Stack Overflow
- Blog: https://centrifugal.dev/blog (performance deep-dives, case studies)
