# Ably: Enterprise Real-time Messaging Platform

**Category**: Managed Service
**Provider**: Ably
**Primary Use Case**: Guaranteed message delivery at scale
**Date Compiled**: December 3, 2025

## Architecture Overview

Ably positions itself as an enterprise-grade real-time messaging platform with guaranteed delivery semantics. Unlike best-effort WebSocket services, Ably focuses on reliability, message ordering, and delivery guarantees across distributed systems.

### Core Components

**Channels**: Pub/sub communication pathways
- **Basic channels**: Standard publish/subscribe
- **Presence channels**: Member tracking and user status
- **Persisted channels**: Message history retention
- **Encrypted channels**: End-to-end encrypted messaging

**Message Delivery Modes**:
- **At-most-once**: Best effort (similar to Pusher)
- **At-least-once**: Guaranteed delivery with potential duplicates
- **Exactly-once**: Idempotent delivery (via message deduplication)

**Client SDKs**: 25+ platform libraries
- Web: JavaScript, TypeScript
- Mobile: iOS, Android, React Native, Flutter
- Server: Node.js, Python, Ruby, Java, Go, .NET, PHP

## Feature Analysis

### Connection Management
- **Connection state recovery**: Automatic reconnection with state sync
- **Connection fallback**: WebSocket → HTTP long-polling → SSE → Comet
- **TLS/SSL**: Standard on all connections
- **Connection heartbeats**: Automatic keepalive

### Message Delivery
- **Delivery guarantee**: Configurable (at-most, at-least, exactly-once)
- **Message ordering**: Guaranteed per channel
- **Message persistence**: Configurable retention (2 minutes to 365 days)
- **Max message size**: 64 KB per message (vs. Pusher's 10 KB)
- **Message deduplication**: Prevents duplicate delivery

### Presence System
- **Member tracking**: Real-time presence with member enter/leave/update events
- **Custom presence data**: Rich user information attached to presence
- **Presence set**: Full member list available on join
- **Scale**: Thousands of members per presence channel

### Advanced Features
- **Message history**: Persistent storage with configurable retention
- **Message delta compression**: Efficient updates for large state objects
- **Token authentication**: Fine-grained capability-based security
- **Webhooks & integrations**: Extensive event streaming options
- **Reactor**: Server-side event processing (queues, functions, streams)
- **Protocol adapters**: MQTT, SSE (Server-Sent Events)

## Portability Assessment

### Lock-in Risk: MEDIUM

**Vendor-Specific Elements**:
1. **Token authentication**: Ably-specific JWT format with capabilities
2. **Connection state recovery**: Proprietary protocol for resuming connections
3. **Message format**: Ably envelope with metadata (ID, timestamp, client ID)
4. **Reactor integrations**: Vendor-specific event processing pipeline

**Migration Path Complexity**:
- **To self-hosted**: Moderate-High effort (state recovery, message persistence complex)
- **To competitor**: Moderate effort (authentication models differ, presence varies)
- **Standard WebSocket**: High effort (lose guarantees, persistence, presence)

**Portable Elements**:
- Standard WebSocket protocol underneath
- Message payloads (JSON/binary) are application-defined
- Channel-based architecture maps to other pub/sub systems
- REST API fallback for interoperability

### Data Portability
- **Message history**: Exportable via History API (REST)
- **Channel configuration**: Available via Control API
- **Analytics data**: Dashboard export, metrics API
- **Presence snapshots**: Ephemeral but queryable

## Latency Benchmarks

### Vendor-Published Data

**Global Infrastructure** (2025):
- 15+ geographic regions (AWS, Google Cloud)
- 350+ edge acceleration points via CDN
- Multi-region routing with automatic failover

**Published Latency Targets**:
- Regional: 25-65ms median round-trip
- Global edge routing: 50-150ms (depending on distance)
- P99 latency: <100ms (intra-region)
- P99.9 latency: <250ms (global)

**Guaranteed Delivery Overhead**:
- At-least-once: +5-15ms vs. at-most-once (persistence overhead)
- Exactly-once: +10-25ms (deduplication overhead)

### Community-Reported Performance

**Low-Latency Scenarios** (financial trading, gaming):
- Median: 30-50ms (same region, at-most-once mode)
- P95: 60-100ms
- Jitter: Very low (±5-8ms)
- Note: Consistently faster than Pusher in community benchmarks

**High-Load Scenarios** (10,000+ concurrent connections):
- Median: 40-70ms (excellent under load)
- P95: 100-180ms
- Graceful degradation with auto-scaling

**Message Persistence Impact**:
- No persistence: 35ms median
- 24-hour retention: 42ms median (+7ms overhead)
- 30-day retention: 45ms median (+10ms overhead)

**Geographic Performance**:
- US East → US West: 70-120ms
- Europe → US East: 90-150ms
- Asia → Europe: 180-280ms
- **Edge acceleration**: Reduces latency by 15-30% on average

### Performance Tuning Options
- **Region selection**: Deploy in multiple regions, route intelligently
- **Message batching**: Bundle multiple messages (Ably supports batch publish)
- **Delta compression**: Reduce payload size for incremental updates
- **Connection multiplexing**: Share connections across channels
- **QoS tuning**: Choose delivery guarantee based on use case

## Cost Analysis

### Pricing Model (2025)

**Free Tier**:
- 200 concurrent connections
- 6 million messages/month
- 2-minute message history
- Community support

**Standard** ($29/month base):
- 200 concurrent connections (included)
- 20 million messages/month (included)
- Overages: $2.50 per 1M messages, $5 per 100 connections
- 24-hour message history
- Email support

**Pro** ($299/month base):
- 1,000 concurrent connections (included)
- 100 million messages/month (included)
- Overages: $2.00 per 1M messages, $4 per 100 connections
- 72-hour message history
- Priority support, SLA

**Enterprise** (Custom pricing):
- Custom connection and message volumes
- Extended message retention (up to 365 days)
- Dedicated infrastructure, multi-region
- 24/7 support, dedicated account team

**Overage Pricing Details**:
- Messages: $2.00-2.50 per million (volume discounts at scale)
- Connections: $4-5 per 100 concurrent connections/month
- Bandwidth: Typically included (egress can have limits at extreme scale)

### Cost Scenarios

**Scenario 1: Small Event** (1,000 concurrent, 2 hours, 20,000 messages)
- Plan required: Pro ($299/month base)
- Connections: 1,000 (included)
- Messages: 20,000 (well within 100M included)
- **Monthly cost**: $299 (if sustained) or ~$10/day pro-rated
- **Note**: Could use Standard + overage: $29 + (800 connections × $0.05) = $69

**Scenario 2: Medium SaaS Dashboard** (5,000 concurrent, 4.8M messages/day)
- Daily messages: 4.8M
- Monthly messages: ~144M
- Plan: Pro base ($299)
- Connection overage: 4,000 × $0.04 = $160
- Message overage: 44M × $0.002 = $88
- **Monthly cost**: $299 + $160 + $88 = $547

**Scenario 3: Large Platform** (10,000 concurrent, 72M messages/day)
- Daily messages: 72M
- Monthly messages: ~2.16B
- Plan: Enterprise (negotiated)
- Estimated based on overage math: $299 + $360 (connections) + $4,120 (messages) = $4,779
- **Actual monthly cost**: $3,000-5,000 (volume discounts in enterprise contract)

### Hidden Costs
- **Bandwidth**: Generous limits, but very high bandwidth can incur charges
- **Message retention**: Extended retention (>72 hours) on Enterprise only
- **Reactor functions**: Serverless processing has separate pricing
- **Support**: Premium support on Enterprise tier

## Operational Considerations

### Developer Experience
**Strengths**:
- Comprehensive documentation with interactive examples
- Excellent debugging tools (protocol inspector, connection diagnostics)
- Rich SDK feature parity across platforms
- Transparent status page with historical data

**Weaknesses**:
- Steeper learning curve than simpler alternatives (Pusher)
- Token authentication configuration complexity
- Pricing can be opaque without calculator

### Scalability
**Horizontal scaling**: Fully managed, automatic
**Vertical scaling**: Transparent to developers
**Rate limiting**: Generous defaults, configurable on Enterprise

**Published Scale**:
- Millions of concurrent connections (Enterprise)
- Billions of messages per day
- Sub-second global failover

### Monitoring & Observability
- **Metrics API**: Comprehensive usage and performance data
- **Real-time stats**: Connection counts, message rates, errors
- **Webhooks**: Channel lifecycle, connection events
- **Integration**: Datadog, New Relic, custom metrics export

## Security & Compliance

### Authentication
- **Token-based**: JWT with capability grants (publish, subscribe, presence, history)
- **Basic auth**: API key (development only)
- **SSO integration**: Enterprise tier

### Encryption
- **TLS in transit**: Standard, enforced
- **End-to-end encryption**: Built-in encrypted channel support
- **At-rest encryption**: For persisted messages

### Compliance
- **SOC 2 Type II**: Yes
- **ISO 27001**: Yes
- **GDPR**: Fully compliant, data residency options
- **HIPAA**: Available on Enterprise tier with BAA

## Comparison to Alternatives

**vs. Pusher**:
- Ably: Guaranteed delivery, message persistence, larger messages (64KB vs 10KB)
- Pusher: Simpler, cheaper for small workloads, no persistence

**vs. Socket.io**:
- Ably: Managed, globally distributed, guaranteed delivery
- Socket.io: Self-hosted, full control, cheaper at massive scale but requires ops

**vs. Firebase**:
- Ably: Database-agnostic, pure messaging, better latency
- Firebase: Integrated database, simpler for mobile apps, Google ecosystem lock-in

## Recommendation Context

**Best For**:
- Applications requiring guaranteed message delivery
- Financial services, healthcare, or regulated industries
- Global user base needing low latency worldwide
- Use cases requiring message history/audit trails
- Teams needing enterprise SLAs and support

**Not Ideal For**:
- Very small projects (generous free tier, but complexity overkill)
- Extremely price-sensitive use cases (self-hosted cheaper at 20K+ connections)
- Simple notification use cases (Ably features underutilized)

## Migration Considerations

**Exiting Ably**:
1. Replace token authentication with new provider's auth mechanism
2. Migrate message persistence logic (if used) to new storage
3. Reimplement connection state recovery (if relied upon)
4. Update client SDKs (vendor-specific)
5. Rebuild Reactor integrations (if used)
6. Export historical message data via History API

**Estimated effort**: 3-6 weeks for complex application with persistence/guarantees

**Entering Ably** (from basic WebSocket):
1. Replace direct WebSocket with Ably SDK
2. Implement token auth server endpoint
3. Migrate channel/room logic to Ably channels
4. Enable persistence/guarantees as needed
5. Configure webhooks for server-side events

**Estimated effort**: 1-3 weeks for greenfield integration

## References & Resources

- Official documentation: https://ably.com/docs
- Pricing calculator: https://ably.com/pricing
- GitHub repositories: https://github.com/ably
- Performance benchmarks: https://ably.com/blog/tag/benchmarks
- Status page: https://status.ably.com
- Community: Stack Overflow, Discord, GitHub Discussions
