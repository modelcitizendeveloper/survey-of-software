# Pusher Channels

## Overview

**Category**: Managed WebSocket service
**Founded**: 2010 (acquired by MessageBird 2022)
**Focus**: Developer-friendly real-time messaging at scale

## Popularity Metrics

**Production Usage**:
- Used by GitHub, Intercom, DoorDash, The New York Times
- Claimed 1+ trillion messages/year

**Developer Adoption**:
- Client SDKs: 10+ languages
- 300K+ registered developers

## Latency Benchmarks

**Published Numbers** (from Pusher documentation):
- Median message latency: **50-80ms** (same region)
- 95th percentile: **150-200ms**
- 99th percentile: **300-500ms**

**Geographic Distribution**:
- 7 global regions (US East, US West, EU, AP, etc.)
- Cross-region adds ~100-200ms
- Latency scales with distance from nearest cluster

**Fan-out Performance**:
- 1 → 100 subscribers: ~50ms additional overhead
- 1 → 1,000 subscribers: ~100ms additional overhead
- 1 → 10,000 subscribers: ~200-300ms additional overhead

**Reality Check**: Their own docs admit "latency varies with network conditions" - mobile clients on 4G can see 200-400ms total latency.

## Scaling Characteristics

**Concurrent Connections**:
- Per channel: 100K subscribers maximum
- Account level: unlimited (priced per connection)
- Message rate: 100 messages/second per channel

**Message Throughput**:
- Standard plan: 1,000 messages/second burst
- Enterprise: custom negotiated

**Connection Limits**:
- Free tier: 100 concurrent connections
- Pro: 5,000+ concurrent (price scales)

## Cost Model

**Pricing Tiers** (as of 2024):

**Free**:
- 100 concurrent connections
- 200K messages/day
- $0/month

**Startup ($29/month)**:
- 500 concurrent connections
- 1M messages/day
- $0.10 per GB over quota

**Professional ($299/month)**:
- 3,000 concurrent connections
- 7M messages/day
- Support included

**Enterprise** (custom):
- Unlimited connections
- SLA guarantees
- Dedicated infrastructure

**Cost Scenarios**:
- 1,000 devices, 1 event/minute: ~$29-299/month (depends on message size)
- 5,000 devices: ~$299-999/month
- 10,000 devices: Enterprise pricing (likely $2,000-5,000/month)

**Hidden Costs**:
- Bandwidth charges above quota
- Multi-region distribution adds cost
- Message history/replay extra

## Self-Hosted vs Managed

**Managed Only**: Pusher does not offer self-hosted option

**Trade-offs**:
- **Pro**: Zero infrastructure management, global CDN, instant scaling
- **Con**: Vendor lock-in, unpredictable costs at scale, no control over latency optimization

## Production Validation

**Known Deployments**:
- **GitHub**: Used for real-time notifications (2011-2016, migrated to ActionCable)
- **Intercom**: Customer messaging widget
- **DoorDash**: Order status updates

**Community Reports** (Stack Overflow, Reddit):
- Generally reliable for <1K concurrent connections
- Latency variability complaints at scale
- Cost concerns beyond 5K connections
- Occasional regional outages

## Technical Architecture

**Protocol**: WebSocket (with HTTP fallback)
**Fallback**: Long polling for old browsers
**Presence**: Built-in presence channels
**Authentication**: Token-based channel authentication
**Encryption**: TLS by default (wss://)

## Limitations

**Channel Capacity**: 100K subscribers per channel (hard limit)
**Message Size**: 10KB max per message
**Message History**: Not included (paid add-on)
**Regional Routing**: Cannot control which cluster client connects to
**Cold Start**: First connection to channel can add 100-200ms

## Verdict for Low-Latency Use Cases

**Can Pusher achieve <50ms sync?**
- **Same region, ideal network**: Maybe (50-80ms median)
- **Real-world conditions**: Unlikely (100-200ms more realistic)
- **10K fan-out**: No (200-300ms additional overhead)

**Best For**:
- Rapid prototyping
- <1K concurrent connections
- Non-latency-critical updates (notifications, dashboards)

**Not Ideal For**:
- Ultra-low-latency requirements (<50ms)
- Cost-sensitive high-scale deployments (>5K connections)
- Applications requiring guaranteed latency SLAs
