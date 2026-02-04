# Ably Realtime

## Overview

**Category**: Managed real-time messaging platform
**Founded**: 2015
**Focus**: Enterprise-grade reliability with latency guarantees

## Popularity Metrics

**Production Usage**:
- Used by HubSpot, Verizon, Hopin, Split.io
- Claimed 5+ billion messages/day

**Developer Adoption**:
- GitHub: ~4.5K stars (ably-js client)
- 25+ SDKs across languages/platforms
- SOC 2 Type 2 certified

## Latency Benchmarks

**Published SLA** (from Ably documentation):
- Median latency: **50-65ms** (same region, 1-1 messaging)
- 95th percentile: **<100ms** (contractual SLA for Enterprise)
- 99th percentile: **<200ms**

**Geographic Distribution**:
- 15+ global regions (AWS, GCP, Azure)
- Auto-routing to nearest edge
- Cross-region: +100-150ms

**Fan-out Performance** (documented benchmarks):
- 1 → 100 subscribers: **60-80ms** total
- 1 → 1,000 subscribers: **80-120ms** total
- 1 → 10,000 subscribers: **150-250ms** total
- 1 → 100,000 subscribers: **300-500ms** total

**Independent Benchmarks** (Ably vs Pusher, 2022):
- Ably: 65ms median (same region)
- Pusher: 95ms median (same region)
- Test: 1K concurrent connections, 10 msg/sec

**Reality Check**: They publish actual latency distributions, not just marketing claims. Real-world latency monitoring available in dashboard.

## Scaling Characteristics

**Concurrent Connections**:
- Per channel: 100K+ subscribers
- Account level: millions (priced per connection-minute)
- Auto-scaling across regions

**Message Throughput**:
- 1,000-10,000 messages/second per channel
- Global peak: 250K+ messages/second sustained

**Connection Stability**:
- Automatic reconnection with message continuity
- Exactly-once or at-least-once delivery guarantees
- 99.999% uptime SLA (Enterprise)

## Cost Model

**Pricing Structure** (as of 2024):

**Free**:
- 200 concurrent connections
- 6M messages/month
- $0/month

**Standard ($29/month base)**:
- Pay-as-you-go: $2.50 per 1M messages
- $1.00 per million connection-minutes
- Bandwidth: included up to quota

**Pro ($299/month base)**:
- Discounted rates
- Support SLA
- Message history included

**Enterprise** (custom):
- Volume discounts
- Latency SLAs
- Dedicated infrastructure options

**Cost Scenarios** (approximate):
- **1,000 devices, continuous connection (24/7), 1 msg/min**:
  - Connection-minutes: 1K × 43,200 min/month = 43.2M connection-minutes = $43/month
  - Messages: 1K × 60 × 24 × 30 = 43.2M messages = $108/month
  - **Total: ~$150/month**

- **5,000 devices**: ~$750/month
- **10,000 devices**: ~$1,500/month

**Note**: Connection-minute pricing means idle connections still cost money.

## Self-Hosted vs Managed

**Managed Only**: No self-hosted option

**Trade-offs**:
- **Pro**: Global edge network, automatic scaling, guaranteed SLAs, built-in features (presence, history)
- **Con**: Vendor lock-in, connection-minute pricing penalizes persistent connections, premium cost

## Production Validation

**Known Deployments**:
- **HubSpot**: Real-time CRM updates (millions of connections)
- **Hopin**: Live event platform (100K+ concurrent at scale)
- **Split.io**: Feature flag synchronization

**Community Reports**:
- Generally excellent reliability reviews
- Latency monitoring appreciated
- Cost concerns for high-volume persistent connections
- Great developer experience

## Technical Architecture

**Protocol**: WebSocket (with SSE, MQTT fallback)
**Fallback**: Multiple transport options (SSE, Comet, polling)
**Presence**: Built-in with state synchronization
**Message History**: Included (2 minutes free, extended with plan)
**Encryption**: TLS + optional message-level encryption
**Guarantees**: At-most-once, at-least-once, or exactly-once delivery

**Edge Network**:
- Multi-cloud (AWS, GCP, Azure)
- Automatic failover
- Connection state recovery

## Advanced Features

**Delta Compression**: Reduces bandwidth for repeated similar messages
**Message Continuity**: Automatic replay on reconnection
**Channel Rules**: Server-side filtering/routing
**Integrations**: Native Kafka, RabbitMQ, AWS Kinesis bridges

## Limitations

**Connection-Minute Pricing**: Persistent connections can get expensive
**Vendor Lock-In**: Proprietary protocol extensions
**Latency Floor**: Still bound by physics (geographic distance)
**Cost at Scale**: Premium pricing vs self-hosted alternatives

## Verdict for Low-Latency Use Cases

**Can Ably achieve <50ms sync?**
- **Same region, 1-1 messaging**: Yes (50-65ms median documented)
- **Same region, 1 → 100 fan-out**: Yes (60-80ms documented)
- **Same region, 1 → 1,000 fan-out**: No (80-120ms)
- **Cross-region**: No (100-200ms+)

**Best For**:
- Enterprise applications requiring SLAs
- Global distribution with automatic routing
- Applications needing exactly-once delivery
- Teams willing to pay for reliability

**Not Ideal For**:
- Cost-sensitive deployments at high scale
- Applications with long-lived persistent connections (connection-minute pricing hurts)
- Teams wanting full infrastructure control
