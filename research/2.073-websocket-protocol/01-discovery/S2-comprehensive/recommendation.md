# WebSocket Implementation Recommendations

**Research Tier**: S2 Comprehensive Portability Analysis
**Date Compiled**: December 3, 2025

## Decision Framework

Choosing a WebSocket implementation requires evaluating:

1. **Performance requirements**: Latency tolerance, throughput needs
2. **Scale**: Current and projected concurrent connections
3. **Operational capacity**: DevOps resources available
4. **Budget**: Infrastructure and operational costs
5. **Portability requirements**: Lock-in tolerance, migration likelihood
6. **Feature needs**: Presence, persistence, guarantees, database integration

## Recommendations by Use Case

### Real-Time Collaboration (Google Docs, Figma-style)

**Requirements**:
- Latency: <50ms for smooth experience
- Throughput: Moderate (100-500 messages/sec per room)
- Presence: Required (who's online, cursor positions)
- Conflict resolution: Application-level (WebSocket only transports)

**Recommended**: **Centrifugo** (self-hosted)
- **Latency**: 3-15ms (Memory/KeyDB engine)
- **Presence**: Built-in, performant
- **Cost**: $835-1,535/month at 1K users
- **Portability**: Low lock-in, open source

**Alternative**: **Ably** (managed)
- **Latency**: 30-50ms (acceptable, borderline)
- **Presence**: Excellent (1000s of members)
- **Cost**: $69/month at 1K users
- **Trade-off**: Higher latency, but zero ops

**Avoid**:
- Pusher (presence limited to 100 members)
- Supabase (80-150ms latency too high)

### Multiplayer Gaming

**Requirements**:
- **Fast-paced games**: <30ms latency
- **Turn-based games**: <100ms latency
- Throughput: High (1000s of messages/sec)
- Presence: Often required (player lists)

**Recommended**: **Centrifugo (Memory engine)** (self-hosted)
- **Latency**: 3-8ms (ideal for fast-paced)
- **Throughput**: 100,000+ messages/sec
- **Cost**: Deploy in same region as players
- **Setup**: Deploy in player geographic clusters

**Alternative (turn-based)**: **Socket.io** (self-hosted)
- **Latency**: 10-25ms (adequate for turn-based)
- **Community**: Large gaming community, many examples
- **Cost**: Lower ops overhead for smaller games

**Avoid**:
- All managed services (too much overhead for fast-paced)
- Supabase (database intermediation unacceptable)

### Live Dashboard / Business Intelligence

**Requirements**:
- Latency: <200ms acceptable (human perception)
- Data source: Often database-driven
- Scale: 100-5,000 concurrent users
- Persistence: Often needed for historical data

**Recommended**: **Supabase Realtime** (managed)
- **Latency**: 80-150ms (perfectly adequate)
- **Integration**: Direct Postgres change streaming
- **Cost**: $25-220/month (extremely cheap)
- **Best fit**: If already using Postgres database

**Alternative**: **Pusher** (managed)
- **Latency**: 35-60ms
- **Simplicity**: Easiest to integrate
- **Cost**: $99-449/month
- **Trade-off**: No database integration, more expensive

**Alternative (high scale)**: **Centrifugo** (self-hosted)
- **Best for**: 10,000+ users, custom data pipelines
- **Cost**: $2,300/month at 10K users (vs. $3K-5K managed)

### Chat / Messaging Application

**Requirements**:
- Latency: <200ms acceptable
- Persistence: Required (message history)
- Presence: Helpful (online status)
- Scale: Variable (100 to 100,000s users)

**Recommended**: **Ably** (managed)
- **Latency**: 30-50ms
- **Persistence**: Built-in (2min to 365 days)
- **Presence**: Excellent
- **Delivery guarantees**: At-least-once available
- **Cost**: $69 (1K users) to $3K-5K (10K users)

**Alternative (budget-conscious)**: **Supabase Realtime** (managed)
- **Cost**: $25-220/month (if using Supabase for message storage)
- **Trade-off**: No built-in persistence in Realtime (use Postgres)
- **Best fit**: Small to medium chat apps on Supabase

**Alternative (large scale)**: **Centrifugo** (self-hosted)
- **Cost**: $2,300/month at 10K users (40% cheaper than Ably)
- **Persistence**: Built-in with Redis
- **Trade-off**: Requires ops capacity

### Notifications / Push Updates

**Requirements**:
- Latency: <500ms tolerable
- Throughput: Often spiky (breaking news, alerts)
- Scale: Can be massive (millions of users)
- Persistence: Usually not required

**Recommended**: **Pusher** (managed)
- **Simplicity**: Easiest integration for simple broadcasts
- **Scalability**: Automatic, handles spikes
- **Cost**: $99 (1K users) to $1,500-3K (10K users)
- **Best fit**: Simple notification use cases

**Alternative (budget)**: **Supabase Realtime Broadcast** (managed)
- **Cost**: $25-220/month
- **Latency**: 40-80ms (Broadcast mode, no DB)
- **Trade-off**: Smaller ecosystem, less mature

**Alternative (extreme scale)**: **Centrifugo** (self-hosted)
- **Best for**: Millions of concurrent connections
- **Cost**: 60-70% cheaper than managed at 50K+ users
- **Trade-off**: Requires significant ops investment

### Financial Trading / High-Frequency Updates

**Requirements**:
- Latency: <10ms critical, <20ms acceptable
- Reliability: Extremely high uptime required
- Throughput: Very high (10,000s messages/sec)
- Compliance: Often regulated industry

**Recommended**: **Centrifugo (Memory engine)** (self-hosted)
- **Latency**: 3-8ms (ONLY option meeting requirement)
- **Deployment**: Same data center as clients
- **Compliance**: Full control for regulatory requirements
- **Cost**: Higher ops overhead, but necessary for performance

**Setup requirements**:
- Deploy in financial data center (co-location)
- Use Protobuf encoding (faster than JSON)
- Disable unnecessary features (minimize latency)
- Redundant infrastructure (high availability)

**Avoid**: Any managed service or database-intermediated solution

### IoT / Device Telemetry

**Requirements**:
- Scale: Often massive (100,000s of devices)
- Throughput: Varies (periodic vs. continuous streaming)
- Protocols: Often MQTT (WebSocket alternative)
- Cost sensitivity: High (margins often thin)

**Recommended**: **AWS IoT Core** or **Azure Web PubSub**
- **Reason**: Purpose-built for IoT (not covered in deep analysis)
- **Protocols**: MQTT over WebSocket
- **Pricing**: Per-message pricing optimized for IoT

**Alternative (general WebSocket)**: **Centrifugo** (self-hosted)
- **Cost**: Extremely low per-device cost at scale
- **Flexibility**: Custom device protocols possible
- **Trade-off**: More complex than IoT-specific services

**Avoid**: General managed services (Pusher, Ably) - too expensive per device

## Recommendations by Scale

### Small Scale (<1,000 Concurrent)

**Best choice**: **Managed services** (zero ops overhead)

**Priority ranking**:
1. **Supabase** ($25/month) - if using Supabase database
2. **Ably** ($69/month) - best features for price
3. **Pusher** ($99/month) - simplest integration

**Rationale**: Setup cost and ops overhead of self-hosted not justified at this scale

### Medium Scale (1,000-5,000 Concurrent)

**Best choice**: **Managed services** (unless extreme latency needs)

**Priority ranking**:
1. **Supabase** ($25-39/month) - if database-driven, unbeatable price
2. **Ably** ($69-547/month) - best balance of features and reliability
3. **Pusher** ($99-449/month) - if simplicity preferred over features

**Self-hosted consideration**: Only if <20ms latency required (Centrifugo)

### Large Scale (5,000-10,000 Concurrent)

**Transition point**: Self-hosted becomes competitive

**With DevOps capacity**:
1. **Centrifugo** ($1,260-2,300/month) - best performance, comparable cost
2. **Ably** ($547-5,000/month) - if ops capacity unavailable

**Without DevOps capacity**:
1. **Pusher** ($449-3,000/month) - simpler than Ably, cheaper at high end
2. **Ably** ($547-5,000/month) - better features, more expensive

**Database-driven**:
- **Supabase** ($39-220/month) - still drastically cheaper if applicable

### Very Large Scale (10,000-50,000+ Concurrent)

**Best choice**: **Self-hosted** (60-70% cost savings)

**Priority ranking**:
1. **Centrifugo** - best performance, lower ops overhead than Socket.io
2. **Socket.io** - if already invested in Node.js ecosystem
3. **Managed services** - only if ops capacity absolutely unavailable

**Cost comparison at 50K concurrent**:
- Centrifugo: ~$5,000/month (with ops)
- Ably: ~$15,000/month
- Pusher: ~$10,000/month

**Savings**: 50-67% with self-hosted

## Recommendations by Team Capacity

### No DevOps / Small Startup Team

**Recommendation**: **Managed services only**

**Choice logic**:
- **Database-driven use case**: Supabase
- **Need reliability + features**: Ably
- **Need simplicity**: Pusher

**Rationale**: Self-hosted ops overhead exceeds cost savings at small scale

### DevOps Team (1-2 engineers)

**Recommendation**: **Managed services until 5,000-10,000 users**

**Threshold**: Switch to self-hosted at 8,000-10,000 concurrent connections
- **Before threshold**: Focus DevOps on core product infrastructure
- **After threshold**: Self-hosted WebSocket becomes cost-justified

**Choice**: Centrifugo (lower ops overhead than Socket.io)

### Mature DevOps Team (3+ engineers)

**Recommendation**: **Self-hosted at any scale requiring <20ms latency**

**Choice logic**:
- **Performance-critical**: Centrifugo (always)
- **Cost-sensitive**: Centrifugo at 5,000+ users
- **Rapid prototyping**: Managed for MVP, migrate later

**Rationale**: Ops capacity exists; leverage it for cost savings and performance

## Recommendations by Portability Priority

### Maximum Portability (minimize lock-in)

**Recommendation**: **Socket.io** or **Centrifugo** (self-hosted)

**Rationale**:
- Open source (can fork, maintain indefinitely)
- Standard protocols underneath
- Complete data and infrastructure control
- Clear migration paths

**Trade-off**: Operational overhead

### Balanced Portability

**Recommendation**: **Ably**

**Rationale**:
- Standard JWT authentication (portable)
- Good data export capabilities
- Documented migration patterns
- Reasonable feature set without excessive proprietary lock-in

**Trade-off**: More expensive than self-hosted at scale

### Portability Secondary

**Recommendation**: **Supabase** or **Pusher**

**Rationale**: Optimize for current problem, accept future migration cost

**Supabase**:
- If database-driven, incredible value
- High lock-in to Postgres/Supabase, but database portability separate concern

**Pusher**:
- Fastest to integrate
- Moderate lock-in (proprietary auth, channel conventions)

## Decision Trees

### Primary Decision Tree

```
START
  |
  Do you need <20ms latency?
  |-- YES → Centrifugo (Memory engine)
  |
  |-- NO → Do you have DevOps capacity?
      |
      |-- NO → Managed services
      |   |
      |   |-- Database-driven? → Supabase
      |   |-- Need guarantees/history? → Ably
      |   |-- Need simplicity? → Pusher
      |
      |-- YES → What scale?
          |
          |-- <5K concurrent → Managed (Ably or Pusher)
          |-- 5K-10K concurrent → Transition zone (evaluate both)
          |-- >10K concurrent → Self-hosted (Centrifugo)
```

### Feature-Driven Decision Tree

```
START
  |
  Do you need guaranteed delivery?
  |-- YES → Ably (at-least-once, exactly-once)
  |
  |-- NO → Do you need message persistence?
      |
      |-- YES → Ably (managed) or Centrifugo (self-hosted)
      |
      |-- NO → Do you need presence tracking?
          |
          |-- YES (>100 members) → Ably or Centrifugo
          |-- YES (<100 members) → Pusher OK
          |-- NO → Cost optimize
              |
              |-- Database-driven? → Supabase
              |-- Large scale? → Centrifugo
              |-- Small scale? → Pusher
```

## Anti-Recommendations

### Don't Choose Supabase If...
- Real-time needs are NOT database-driven
- You need <50ms latency
- You're not using Postgres
- You need >10K concurrent without Enterprise tier

### Don't Choose Pusher If...
- You need presence channels >100 members
- You need message persistence/history
- You need guaranteed delivery
- Budget is extremely tight at large scale (>10K)

### Don't Choose Ably If...
- You need <20ms latency
- Budget is minimal (<$100/month)
- Use case is extremely simple (Pusher adequate)
- You have DevOps capacity and >50K concurrent (self-hosted cheaper)

### Don't Choose Socket.io If...
- You lack DevOps capacity
- You need <10ms latency (Centrifugo faster)
- You need built-in message persistence (DIY required)
- You need guaranteed delivery (DIY required)

### Don't Choose Centrifugo If...
- You lack DevOps capacity
- Scale is very small (<1K concurrent)
- You need extensive community support (Socket.io larger)
- Setup timeline is days (managed services instant)

## Migration Paths

### Starting with Managed, Plan for Self-Hosted

**Strategy**: Abstract your WebSocket implementation

1. Create internal API layer: `RealtimeService.publish()`, `RealtimeService.subscribe()`
2. Implement with managed service (Pusher/Ably) initially
3. When scale justifies: Swap implementation to Centrifugo/Socket.io
4. Client code remains unchanged (abstraction layer handles differences)

**Estimated migration time**: 2-4 weeks when abstraction layer exists

### Starting with Self-Hosted, Add Managed for Global Reach

**Strategy**: Hybrid deployment

1. Self-hosted in primary region (Centrifugo)
2. Managed service for global edge (Ably)
3. Route clients based on geography

**Use case**: Optimize latency globally without managing global infrastructure

## Final Recommendations Summary

| Use Case | <1K Users | 1K-5K Users | 5K-10K Users | >10K Users |
|----------|-----------|-------------|--------------|------------|
| **Database-driven** | Supabase | Supabase | Supabase | Supabase/Centrifugo |
| **Collaboration** | Ably | Ably | Centrifugo | Centrifugo |
| **Gaming** | Centrifugo | Centrifugo | Centrifugo | Centrifugo |
| **Chat/Messaging** | Ably | Ably | Ably | Ably/Centrifugo |
| **Notifications** | Pusher | Pusher | Pusher | Centrifugo |
| **Trading/HFT** | Centrifugo | Centrifugo | Centrifugo | Centrifugo |
| **General-purpose** | Ably/Pusher | Ably | Ably/Centrifugo | Centrifugo |

**Key takeaway**: Start with managed services (Ably or Pusher), migrate to self-hosted (Centrifugo) at 5K-10K+ users if you have DevOps capacity.
