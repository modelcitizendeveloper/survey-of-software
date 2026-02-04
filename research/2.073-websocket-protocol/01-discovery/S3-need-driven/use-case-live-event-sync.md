# Use Case: Live Event Synchronization

## Scenario Definition

**Industry Examples**:
- Conference mobile apps (1,000-5,000 attendees)
- Sports event scoreboards (5,000-50,000 viewers)
- Live concert/festival apps (10,000-100,000 attendees)
- Political rally/election results (variable, spike to 50K+)
- Breaking news broadcasts (10,000-1M+ concurrent)

**Core Requirement**: Synchronize event state (scores, announcements, results) to thousands of devices simultaneously with minimal latency for competitive experience.

## Requirement Analysis

### Scale Requirements

**Concurrent Connections**:
- Minimum viable: 1,000 devices
- Target scale: 5,000-10,000 devices
- Peak capacity: 20,000 devices (2x headroom)
- Geographic: Single region or global (determines architecture)

**Message Patterns**:
- Broadcast-heavy: 1 source → N recipients (N = 1,000-10,000)
- Message frequency: 10-100 events/minute during active periods
- Message size: 100-500 bytes (JSON state updates)
- Peak burst: 1,000 messages/second during critical moments

**Duration**:
- Event lifetime: 2-8 hours typical
- Connection duration: 30 minutes - 4 hours (user attention span)
- Annual frequency: 10-200 events/year (affects cost model)

### Performance Requirements

**Latency Targets**:
- **Desired**: <50ms (P95) from source to all devices
- **Acceptable**: <100ms (P95)
- **Maximum**: <200ms (P99)
- **Critical**: No message loss (eventual consistency acceptable)

**Network Conditions**:
- 40% WiFi (20-50ms baseline)
- 50% 4G/5G (50-150ms baseline)
- 10% 3G/poor network (200-500ms baseline)

**Consistency Model**:
- Eventual consistency acceptable
- Order preservation required (within 1-second window)
- No strong consistency needed

### Cost Constraints

**Budget Model**: Event-based vs monthly operational

**Per-Event Economics**:
- Target: <$50/event for 5,000 users = $0.01/user
- Acceptable: <$200/event for 10,000 users = $0.02/user
- Monthly amortized: $500-2,000/month for 10-20 events

**Infrastructure vs Operations**:
- Prefer higher infra cost vs operational complexity
- Acceptable DevOps: 5-10 hours/month setup + monitoring
- Zero-ops premium: Willing to pay 2-3x for managed

### Technical Constraints

**Client Environment**:
- 60% mobile (iOS/Android native apps)
- 30% mobile web (Progressive Web App)
- 10% desktop web

**Existing Backend**:
- REST API (Node.js, Python, or Go)
- Database: PostgreSQL or MongoDB
- Cloud: AWS, GCP, or Azure
- CDN: Cloudflare or AWS CloudFront

**Team Expertise**:
- Backend: Node.js or Python (strong)
- DevOps: Docker/Kubernetes (moderate)
- Real-time systems: Limited (first WebSocket deployment)

## Solution Evaluation

### Option 1: Centrifugo (Self-Hosted) + Redis

**Architecture**:
- 2-3 Centrifugo server instances (Go binary)
- Redis Cluster for pub/sub (3-node)
- Load balancer with sticky sessions
- Same-region deployment initially

**Latency Analysis**:

Best Case (same region, WiFi):
- Network RTT: 20-30ms
- Centrifugo processing: 2-5ms
- Fan-out to 5K devices: 30-50ms
- **Total: 50-85ms (MEETS <100ms target)**

Typical Case (mixed network):
- Network RTT: 50-100ms (4G baseline)
- Centrifugo processing: 2-5ms
- Fan-out: 30-50ms
- **Total: 80-155ms (MEETS <200ms P99)**

Worst Case (poor network):
- Network RTT: 200-400ms (3G)
- Processing: 5-10ms
- Fan-out: 50-80ms
- **Total: 255-490ms (degrades gracefully)**

**Cost Modeling**:

Infrastructure (5,000 devices):
- 2x c5.large instances ($120/month)
- Redis 3-node cluster ($50/month)
- Load balancer ($20/month)
- **Subtotal: $190/month**

Operations (monthly):
- Initial setup: 20 hours ($400-1,000 one-time)
- Monitoring/maintenance: 5 hours/month ($100-250)
- On-call/incidents: 2 hours/month ($40-100)
- **Subtotal: $140-350/month**

**Total: $330-540/month or $16-27/event (20 events/year)**

Scale to 10,000 devices:
- 3x c5.large instances ($180/month)
- Redis cluster ($70/month)
- **Total: $390-590/month or $20-30/event**

**Pros**:
- Lowest latency option (50-85ms achievable)
- Full infrastructure control
- Open source (no vendor lock-in)
- Scales predictably

**Cons**:
- Requires Go/Redis expertise
- 20+ hours initial setup
- Operational responsibility (monitoring, updates)
- No built-in geographic distribution

**Verdict**: **Best for <100ms requirement with DevOps capacity**

---

### Option 2: Ably (Managed Service)

**Architecture**:
- Managed global edge network
- Auto-scaling connection handling
- Built-in geographic routing
- Simple SDK integration

**Latency Analysis**:

Best Case (same region):
- Network RTT: 20-30ms
- Ably edge processing: 20-30ms
- Fan-out: 30-50ms
- **Total: 70-110ms (MEETS <200ms, MARGINAL for <100ms)**

Typical Case:
- Network RTT: 50-100ms
- Ably processing: 30-50ms
- Fan-out: 40-60ms
- **Total: 120-210ms (MARGINAL for <200ms P99)**

**Cost Modeling**:

Pricing Model: Connection-minutes + message count

5,000 devices, 2-hour event:
- 5,000 connections × 120 minutes = 600,000 connection-minutes
- 10 messages/minute × 120 min = 1,200 messages/device = 6M messages
- Ably Standard: $150/month base + $0.02/1K messages
- **Per event: ~$30-50**
- **Monthly (20 events): $600-1,000**

10,000 devices, 4-hour event:
- 10,000 × 240 min = 2.4M connection-minutes
- **Per event: ~$100-150**
- **Monthly (20 events): $2,000-3,000**

**Pros**:
- Zero operational overhead
- Built-in global distribution
- SLA guarantees (99.999% uptime)
- Instant deployment (hours, not weeks)

**Cons**:
- Higher cost at scale (3-5x self-hosted)
- Latency overhead (20-30ms vs Centrifugo)
- Less infrastructure control
- Vendor lock-in risk

**Verdict**: **Best for rapid deployment, acceptable latency tolerance**

---

### Option 3: Socket.IO (Self-Hosted) + Redis

**Architecture**:
- 3-4 Node.js Socket.IO servers
- Redis Pub/Sub adapter
- NGINX load balancer
- Horizontal scaling via PM2 or Kubernetes

**Latency Analysis**:

Best Case:
- Network RTT: 20-30ms
- Socket.IO + Node.js: 10-20ms (higher than Go)
- Fan-out: 40-70ms
- **Total: 70-120ms (MEETS <200ms)**

Typical Case:
- Network RTT: 50-100ms
- Processing: 15-30ms
- Fan-out: 50-80ms
- **Total: 115-210ms (MARGINAL)**

**Cost Modeling**:

Infrastructure (5,000 devices):
- 3x c5.large ($180/month) - Node.js needs more instances
- Redis cluster ($50/month)
- Load balancer ($20/month)
- **Subtotal: $250/month**

**Total: $390-600/month or $20-30/event (20 events/year)**

**Pros**:
- Node.js familiarity (lower learning curve)
- Large ecosystem/community
- Automatic fallback (WebSocket → polling)
- Better than managed services for latency

**Cons**:
- Higher latency than Centrifugo (Node.js overhead)
- More instances needed (vs Go)
- Less efficient at scale
- Operational complexity similar to Centrifugo

**Verdict**: **Choose if team strongly prefers Node.js over Go**

---

### Option 4: Pusher (Managed Service)

**Architecture**:
- Managed multi-region infrastructure
- Channel-based pub/sub
- Simple HTTP API for publishing
- Client SDKs for all platforms

**Latency Analysis**:

Typical Case:
- Network RTT: 50-100ms
- Pusher processing: 50-80ms (higher than Ably)
- Fan-out: 50-100ms
- **Total: 150-280ms (FAILS <200ms P99)**

**Cost Modeling**:

Pricing: Connection count + message count

5,000 connections:
- Business plan: $299/month unlimited messages
- **Per event: $15 (20 events/month)**
- **Monthly: $299**

10,000 connections:
- Enterprise: Custom pricing (~$500-1,000/month)

**Pros**:
- Easiest setup (30-minute integration)
- Generous free tier (100 connections)
- Great documentation
- Startup-friendly pricing

**Cons**:
- Highest latency (150-280ms)
- Does NOT meet <200ms P99 requirement
- Limited control over routing
- Cost increases sharply >5K connections

**Verdict**: **Only for prototype/MVP, NOT production at scale**

---

## Can <50ms Synchronization Be Achieved?

### Physics Analysis

**Network RTT Breakdown**:
- Same city (0-50km): 5-15ms
- Same region (50-500km): 15-40ms
- Cross-region (500-3000km): 40-150ms
- Cross-continent (3000-12000km): 100-300ms

**Server Processing** (per message):
- Centrifugo (Go): 0.5-2ms
- Socket.IO (Node.js): 2-8ms
- Managed services: 10-30ms (infrastructure overhead)

**Fan-out Overhead** (1 → N broadcast):
- N = 100: +10-20ms
- N = 1,000: +30-50ms
- N = 5,000: +60-100ms
- N = 10,000: +100-200ms

### The Honest Answer

**<50ms to ALL devices simultaneously: NO**

Breakdown for 5,000 devices, same region:
- Best network RTT: 15-30ms
- Centrifugo processing: 2-5ms
- Fan-out overhead: 60-100ms
- **Total: 77-135ms**

**<50ms to FIRST devices (streaming fan-out): MAYBE**

With optimized streaming broadcast:
- Network RTT: 15-30ms
- Start broadcasting immediately: 2-5ms
- First 100 devices: 17-35ms (**ACHIEVES <50ms**)
- Next 1,000 devices: 30-70ms
- Last 4,000 devices: 77-135ms

### Infrastructure Requirements for Near-50ms

**Required Setup**:
1. **Geographic Concentration**: All users within 500km radius
2. **Optimized Server**: Centrifugo on c5.2xlarge or larger
3. **Binary Protocol**: Avoid JSON, use MessagePack or Protobuf
4. **Connection Pre-warming**: Establish connections before event
5. **Fan-out Optimization**: Stream broadcast, not batch
6. **Network Quality**: Require WiFi (exclude 3G/4G)

**Infrastructure Topology**:
```
User Devices (5K)
     ↓
Load Balancer (sticky sessions)
     ↓
Centrifugo Cluster (3 instances, same AZ)
     ↓
Redis Pub/Sub (same AZ, <1ms latency)
     ↓
Publisher (event source)
```

**Cost for Optimal Setup**:
- 3x c5.2xlarge ($400/month)
- Redis ElastiCache r5.large ($150/month)
- Same-AZ deployment (minimize inter-AZ latency)
- **Total: $550-900/month infrastructure**

**Realistic Latency**: 60-90ms P50, 90-130ms P95

---

## Fallback Strategies for Network Issues

### Strategy 1: Graceful Degradation (WebSocket → Long Polling)

**Implementation**:
- Socket.IO's automatic fallback
- Client detects WebSocket failure
- Switches to HTTP long polling (1-5 second delay)

**Trade-offs**:
- Latency: 1-5 seconds (vs 50-200ms)
- Server load: 10-50x higher (connection overhead)
- User experience: Degraded but functional

**When to Use**: Mobile networks with restrictive firewalls

---

### Strategy 2: Message Buffering + Retry

**Implementation**:
- Client buffers last 10 messages
- On reconnect, requests missed messages by timestamp
- Server maintains 5-minute message history

**Trade-offs**:
- Memory: 100KB per connection (10 messages × 10KB)
- Complexity: Moderate (deduplication logic)
- Reliability: High (no message loss)

**When to Use**: Intermittent network (train, tunnel, elevator)

---

### Strategy 3: Offline Mode + Sync on Reconnect

**Implementation**:
- Client maintains local state
- Shows last-known state during disconnect
- Banner: "Connection lost, reconnecting..."
- Full state sync on reconnect

**Trade-offs**:
- UX: Clear indication of stale data
- Complexity: Low (simple state cache)
- Reliability: Medium (full state may be large)

**When to Use**: Non-critical updates (polls, leaderboards)

---

### Strategy 4: Multi-Path Redundancy

**Implementation**:
- Primary: WebSocket connection
- Backup: HTTP polling every 10 seconds
- Tertiary: SMS alerts for critical events (goal scored)

**Trade-offs**:
- Cost: 2-3x (duplicate infrastructure)
- Reliability: Very high (triple redundancy)
- Complexity: High (state reconciliation)

**When to Use**: Mission-critical events (election results, trading)

---

## Migration Path from Polling

### Current State: HTTP Polling Every 5 Seconds

**Problems with Polling**:
- Server load: 5,000 devices × 12 requests/min = 60K req/min
- Latency: 2.5 second average delay (5-second interval)
- Inefficiency: 95% of requests return "no change"
- Cost: Database query every request

### Migration Steps

**Phase 1: Hybrid (Polling + WebSocket coexistence)**
- Week 1: Deploy Centrifugo/Ably infrastructure
- Week 2: Add WebSocket to 10% of clients (feature flag)
- Week 3: Monitor latency, error rates, server load
- Week 4: Expand to 50% of clients

**Client-Side Logic**:
```
if (supportsWebSocket && featureFlag.enabled) {
  useWebSocketConnection()
} else {
  usePollingFallback() // existing code
}
```

**Phase 2: WebSocket Primary (Polling fallback)**
- Week 5: Enable WebSocket for 100% of clients
- Keep polling as fallback for connection failures
- Reduce polling interval to 30 seconds (backup)

**Phase 3: Polling Deprecation**
- Week 8: Remove polling for modern clients
- Keep for legacy browsers (<5% of users)
- Monitor for edge case failures

### Risk Mitigation

**Rollback Plan**:
- Feature flag: Instant disable of WebSocket
- Polling still operational during migration
- No database schema changes (stateless)

**Monitoring**:
- WebSocket connection success rate (target: >95%)
- Latency distribution (P50, P95, P99)
- Message delivery rate (target: 100%)
- Server resource usage (CPU, memory, network)

---

## Recommendation

### Primary: Centrifugo (Self-Hosted) for Production

**Rationale**:
- Only option achieving <100ms consistently
- Cost-effective at scale ($25-30/event for 10K users)
- Full control over latency optimization
- Open source (no vendor lock-in)

**When to Choose**:
- DevOps capacity available (5-10 hours/month)
- Budget: $500-1,000/month operational
- <100ms latency requirement
- >1,000 concurrent devices

**Deal-breakers**:
- No DevOps expertise (choose Ably instead)
- <1 month to launch (choose Pusher MVP → migrate later)

---

### Alternative: Ably (Managed) for Rapid Deployment

**Rationale**:
- Zero operational overhead
- 70-110ms latency acceptable for many use cases
- Built-in global distribution
- Professional support + SLA

**When to Choose**:
- Launch timeline: <2 weeks
- Team size: <5 engineers
- Budget: <$1,000/month acceptable
- Global user base (multi-region required)

**Deal-breakers**:
- Strict <100ms requirement (Ably marginal)
- >10K concurrent users (cost becomes prohibitive)
- Need infrastructure customization

---

### Not Recommended: Pusher

**Reason**: Latency does not meet <200ms P99 requirement at scale

**Only Use For**: Prototype/MVP with <1,000 users

---

## Decision Matrix

| Requirement | Centrifugo | Ably | Socket.IO | Pusher |
|-------------|------------|------|-----------|--------|
| **<50ms latency** | Partial (60-90ms) | No (70-110ms) | No (70-120ms) | No (150-280ms) |
| **<100ms latency** | ✓ Yes | Marginal | Marginal | No |
| **<200ms P99** | ✓ Yes | ✓ Yes | ✓ Yes | No |
| **5K devices** | ✓ $190/mo | ✓ $600/mo | ✓ $250/mo | ✓ $299/mo |
| **10K devices** | ✓ $250/mo | ✓ $2K/mo | ✓ $410/mo | ✗ Enterprise |
| **Zero ops** | No | ✓ Yes | No | ✓ Yes |
| **Setup time** | 2-3 weeks | 1-2 days | 1-2 weeks | 1 day |

**The Bottom Line**: For <100ms at 5K-10K scale, Centrifugo is the only viable option. For <200ms with zero operations, choose Ably.
