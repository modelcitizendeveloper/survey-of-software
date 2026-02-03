# Use Case: Live Auction / Time-Critical Bidding Platform

## Scenario Definition

**Industry Examples**:
- Online auction platforms (eBay Live, Sotheby's online)
- Stock/crypto trading platforms (limit orders, market data)
- Sports betting exchanges (in-play betting)
- Gaming matchmaking (competitive lobbies)
- Flash sale platforms (limited inventory, time-bound)
- Ticket sales (concerts, events with high demand)

**Core Requirement**: Broadcast time-critical events (bids, price updates) to participants with strict fairness guarantees, ensuring no participant has unfair latency advantage, with audit trail for disputes.

## Requirement Analysis

### Scale Requirements

**Concurrent Participants**:
- Small auction: 10-100 bidders
- Medium auction: 100-1,000 bidders
- Large event: 1,000-10,000 bidders
- Viewers (non-bidding): 10x-100x bidders (10K-100K)
- Total connections: 1,000-100,000 concurrent

**Message Patterns**:
- Bid submission: 0.1-10 bids/second (spiky at auction end)
- Price updates: Broadcast 1→N (all bidders)
- Inventory updates: <1/second (flash sales)
- Countdown timer sync: 1/second to all participants

**Auction Duration**:
- Quick auctions: 30 seconds - 5 minutes (flash sales)
- Standard: 1-24 hours with activity extensions
- Trading: 24/7 continuous (order book updates)

**Critical Period**: Last 60-120 seconds (10-100x normal bid rate)

### Performance Requirements

**Latency Targets**:
- **Critical**: <100ms (P95) bid submission to broadcast (fairness)
- **Acceptable**: <200ms (P99)
- **Maximum**: <500ms (legal compliance in some jurisdictions)
- **Timer sync**: <50ms clock drift across all clients

**Fairness Guarantees**:
- **Server timestamp authority**: Server time is canonical (not client)
- **Ordered processing**: Bids processed in server-received order
- **No geographic advantage**: Similar latency for all participants (or compensate)
- **Transparency**: All participants see same data at same time (+/- 100ms)

**Reliability Requirements**:
- **No bid loss**: 100% of valid bids must be processed
- **Idempotency**: Duplicate bid submissions handled correctly
- **Audit trail**: Full history of all bids with timestamps
- **Dispute resolution**: Provable ordering of events

### Cost Constraints

**Business Model**:
- Auction platform: 5-15% commission on sales
- Trading platform: $0.001-0.01 per trade
- Target: WebSocket cost <1% of transaction value

**Per-Auction Economics**:
- Small auction ($10K value): <$10 infrastructure cost
- Large auction ($1M value): <$100 infrastructure cost
- Monthly (100 auctions): $500-5,000/month

**Viewer Support**:
- Read-only viewers can have higher latency (200-500ms acceptable)
- Separate tier for active bidders vs passive viewers

### Technical Constraints

**Legal/Regulatory**:
- Audit logs required (7 years retention in some jurisdictions)
- Fair bidding practices (no latency arbitrage)
- Timestamp accuracy critical for disputes
- Geographic restrictions (e.g., US-only auctions)

**Backend Stack**:
- High-frequency writes (bid log)
- Database: PostgreSQL (ACID compliance) or specialized (FoundationDB)
- Clock synchronization: NTP critical
- Load spikes: 10-100x during final seconds

**Client Environment**:
- 60% desktop web (high-value bidders)
- 30% mobile web
- 10% mobile native apps

## Solution Evaluation

### Option 1: Centrifugo + NATS (Self-Hosted, Ordered Processing)

**Architecture**:
- NATS JetStream for ordered message queue
- Centrifugo for WebSocket connections
- PostgreSQL for bid log (append-only)
- NTP for server time synchronization
- Redis for real-time leaderboard cache

**Latency Analysis**:

Best Case (active bidder, same region):
- Client → Centrifugo: 15-30ms
- NATS ordering: 1-3ms
- PostgreSQL write: 3-10ms
- Broadcast via Centrifugo: 15-30ms
- **Total: 34-73ms (MEETS <100ms)**

Typical Case (100 bidders):
- Client → server: 30-60ms
- NATS + DB write: 5-15ms
- Broadcast: 20-50ms
- **Total: 55-125ms (MEETS <200ms P99)**

Worst Case (10K viewers + 1K bidders, end-of-auction spike):
- DB write queue: 10-50ms (high write load)
- Broadcast to 10K: 100-200ms
- **Total: 140-310ms (MARGINAL for <500ms)**

**Fairness Mechanism**:
```
Bid Flow:
1. Client sends bid with client timestamp (for latency compensation)
2. Server assigns authoritative server timestamp
3. NATS ensures sequential processing (no race conditions)
4. PostgreSQL write (durability)
5. Broadcast to all participants with server timestamp
```

**Cost Modeling**:

Infrastructure (1,000 active bidders, 10K viewers):
- 2x c5.xlarge Centrifugo ($250/month)
- NATS cluster (3 nodes): $150/month
- PostgreSQL (high-write optimized): $100-200/month
- Redis cache: $30-50/month
- **Subtotal: $530-650/month**

Operations:
- Setup: 60-80 hours ($1,200-4,000) - includes fairness logic
- Monitoring: 15-20 hours/month ($300-1,000)
- **Total: $830-1,650/month**

Per-auction cost (100 auctions/month): **$8-17/auction**

**Pros**:
- Guaranteed message ordering (NATS JetStream)
- Lowest latency for bidders (34-73ms)
- Full audit trail (PostgreSQL append-only log)
- Server-authoritative timestamps
- Cost-effective at scale

**Cons**:
- Complex setup (NATS + Centrifugo integration)
- Operational overhead (monitoring, clock sync)
- Not geographically distributed (single-region fairness)
- Manual scaling for large events

**Verdict**: **Best for fairness-critical, high-frequency auctions**

---

### Option 2: Ably (Managed) with Message Ordering

**Architecture**:
- Ably for WebSocket + guaranteed message ordering
- Backend publishes bids to Ably after database write
- PostgreSQL for bid log
- Ably History for dispute resolution

**Latency Analysis**:

Typical Case:
- Client → Ably: 20-50ms
- Ably → backend: 20-40ms
- Backend DB write: 5-15ms
- Backend → Ably publish: 10-30ms
- Ably → all clients: 20-50ms
- **Total: 75-185ms (MEETS <200ms)**

Best Case:
- **Total: 75-115ms (MARGINAL for <100ms)**

**Cost Modeling**:

Pricing: Connection-minutes + messages + history retention

1,000 bidders, 1-hour auction:
- 1,000 × 60 min = 60K connection-minutes
- 1,000 bidders × 10 bids = 10K bid messages
- 10K viewers × 60 min = 600K connection-minutes (viewer tier)
- Ably Standard: $150/month base
- Overage: ~$50-100/auction
- **Per-auction: $50-100**

100 auctions/month:
- **Total: $5,000-10,000/month (EXPENSIVE)**

**Pros**:
- Zero infrastructure operations
- Global edge network (but conflicts with fairness)
- Message ordering guaranteed
- Built-in message history (7-day retention)
- Professional SLA

**Cons**:
- Very expensive at auction scale ($50-100/auction)
- Higher latency than self-hosted (75-185ms)
- Global edge conflicts with fairness (need single region)
- Limited control over timestamp authority

**Verdict**: **Too expensive for auction economics, latency marginal**

---

### Option 3: Socket.IO + Custom Ordering Queue

**Architecture**:
- Socket.IO for WebSocket connections
- Redis Streams for ordered bid queue
- PostgreSQL for bid log
- Custom bid sequencer service

**Latency Analysis**:

Typical Case (100 bidders):
- Client → Socket.IO: 20-50ms
- Redis Streams enqueue: 2-5ms
- Sequencer processing: 5-15ms
- PostgreSQL write: 5-15ms
- Broadcast via Socket.IO: 30-70ms
- **Total: 62-155ms (MEETS <200ms)**

Best Case:
- **Total: 62-100ms (MARGINAL for <100ms)**

**Cost Modeling**:

Infrastructure (1,000 bidders):
- 2x c5.large Socket.IO ($120/month)
- Redis Streams ($50/month)
- PostgreSQL ($100/month)
- **Subtotal: $270/month**

Operations:
- Setup: 50-70 hours ($1,000-3,500) - custom sequencer
- Maintenance: 10-15 hours/month ($200-750)
- **Total: $470-1,020/month**

Per-auction: **$5-10/auction**

**Pros**:
- Node.js ecosystem familiarity
- Reasonable cost ($470-1,020/month)
- Custom control over ordering logic
- Automatic fallback (WebSocket → polling)

**Cons**:
- Must build custom sequencer (complex)
- Node.js performance limitations at high frequency
- Less efficient than Centrifugo/NATS
- No built-in fairness guarantees (must implement)

**Verdict**: **Choose if team strongly prefers Node.js, but Centrifugo better**

---

### Option 4: AWS AppSync (Managed GraphQL Subscriptions)

**Architecture**:
- AppSync for GraphQL subscriptions
- DynamoDB for bid log (single-table design)
- Lambda for bid processing
- CloudWatch for audit logs

**Latency Analysis**:

Typical Case:
- Client → AppSync: 50-100ms
- Lambda execution: 20-100ms (cold start risk)
- DynamoDB write: 10-30ms
- AppSync broadcast: 50-100ms
- **Total: 130-330ms (FAILS <200ms P99)**

**Cost Modeling**:

Pricing: GraphQL operations + data transfer

1,000 bidders, 1-hour auction:
- 1M subscription updates: $4
- DynamoDB writes: $1.25
- Lambda invocations: $0.20
- **Per-auction: ~$5-10**

100 auctions/month:
- **Total: $500-1,000/month**

**Pros**:
- AWS-native (if already on AWS)
- Scales automatically
- Low operational overhead
- Built-in with AppSync subscriptions

**Cons**:
- Latency too high (130-330ms)
- Lambda cold starts unpredictable
- GraphQL overhead (vs binary WebSocket)
- Less control over ordering

**Verdict**: **Not recommended (latency too high for bidding)**

---

## Fairness Guarantee Mechanisms

### Challenge: Geographic Latency Inequality

**Problem**:
- Bidder in New York: 20ms to server
- Bidder in California: 60ms to server
- California bidder has 40ms disadvantage

### Solution 1: Server-Authoritative Timestamps Only

**Implementation**:
```
Client submits bid:
  { bid: $100, clientTime: 1638360000000 }

Server receives and assigns:
  { bid: $100, serverTime: 1638360000050, latency: 50ms }

Server processes bids by serverTime (ignores clientTime)
```

**Pro**: Simple, provably fair (server decides)

**Con**: Higher latency participants still at disadvantage

---

### Solution 2: Latency Compensation

**Implementation**:
```
Server measures round-trip latency on connection:
  clientLatency = (RTT / 2)

Server adjusts bid timestamp:
  effectiveTime = serverTime - clientLatency

Process bids by effectiveTime (compensates for distance)
```

**Pro**: Fairer for distributed participants

**Con**: Complex (latency measurement can be gamed)

**Use For**: High-stakes auctions requiring maximum fairness

---

### Solution 3: Regional Clustering + Offset

**Implementation**:
- Deploy servers in 3 regions (US-East, US-West, EU)
- Each region handles local bidders
- Synchronize bids with timestamp offset adjustment
- Central coordinator resolves conflicts

**Pro**: Lowest latency for all participants

**Con**: Very complex (distributed consensus required)

**Only Use For**: Global platforms with legal requirements

---

## Bid Ordering & Conflict Resolution

### Scenario: Two Bids Arrive "Simultaneously"

**Problem**:
- Bidder A submits $100 at 12:00:00.000
- Bidder B submits $101 at 12:00:00.001
- Who wins?

### Approach 1: Strict Server Time Ordering

**Implementation**:
```
Bids processed by server-received timestamp:
  Bid A: serverTime = 12:00:00.000
  Bid B: serverTime = 12:00:00.001

Winner: Bid B (higher bid, later timestamp)

BUT if Bid B was $99:
  Winner: Bid A (higher bid, earlier timestamp)
```

**Rule**: Highest bid wins. If tied, earliest timestamp wins.

---

### Approach 2: Bid Increment Enforcement

**Implementation**:
```
Current highest bid: $100
Minimum increment: $5

Bid A: $101 → REJECTED (increment too small)
Bid B: $105 → ACCEPTED

Prevents "sniping" with $0.01 increments
```

---

### Approach 3: Auction Extension on Late Bids

**Implementation**:
```
Auction ends at 12:00:00

If bid received after 11:59:50:
  Extend auction by 60 seconds

Prevents "last-second sniping"
```

**Pro**: Fairer (everyone has time to respond)

**Con**: Auction can extend indefinitely (limit extensions)

---

## Audit Trail & Dispute Resolution

### Requirements:
1. Prove bid was submitted at specific time
2. Prove bid was or wasn't processed
3. Prove ordering of bids
4. Retain for 7 years (legal compliance)

### Implementation:

**PostgreSQL Append-Only Log**:
```sql
CREATE TABLE bid_log (
  id BIGSERIAL PRIMARY KEY,
  auction_id UUID NOT NULL,
  user_id UUID NOT NULL,
  bid_amount DECIMAL(12,2) NOT NULL,
  client_timestamp TIMESTAMPTZ NOT NULL,
  server_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  server_sequence BIGSERIAL, -- Guaranteed ordering
  status VARCHAR(20), -- 'accepted', 'rejected', 'outbid'
  rejection_reason TEXT,
  client_ip INET,
  user_agent TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_bid_log_auction ON bid_log(auction_id, server_sequence);
```

**Immutable**: Never UPDATE or DELETE, only INSERT

**Cryptographic Proof** (optional, high-stakes):
```
Generate hash chain:
  bid_hash = SHA256(previous_hash + bid_data + server_timestamp)

Each bid references previous bid's hash
Tampering with any bid breaks chain
```

---

## Viewer vs Bidder Tiers

### Problem: 10K viewers + 1K bidders = expensive

**Solution**: Separate connection tiers

**Tier 1: Active Bidders** (low latency, high cost)
- Dedicated Centrifugo/NATS infrastructure
- <100ms latency guarantee
- Full audit trail
- Price: $1-5/user/auction

**Tier 2: Viewers** (higher latency, low cost)
- Separate WebSocket pool or HTTP polling
- 200-500ms latency acceptable
- Broadcast-only (no bidding capability)
- Price: $0.01-0.10/user/auction

**Implementation**:
```javascript
// Client determines tier
if (user.canBid) {
  connectToBidderWebSocket() // Premium tier
} else {
  connectToViewerWebSocket() // Cheap tier
}
```

---

## Last-Second Surge Handling

### Problem: 100 bidders → 1,000 bids in final 10 seconds

**Challenge**: Database write bottleneck

### Solution 1: Write Batching

**Implementation**:
```
Accept bids to in-memory queue
Process queue sequentially (preserve order)
Batch write to PostgreSQL every 100ms

During surge:
  1,000 bids/10 seconds = 100 bids/second
  Batch writes: 10 batches/second × 100 bids = manageable
```

**Risk**: Server crash loses in-memory queue

**Mitigation**: Replicate queue (NATS JetStream durability)

---

### Solution 2: Pre-Scaling

**Implementation**:
```
Monitor auction end time
Scale up infrastructure 5 minutes before end
  - Add Centrifugo instances
  - Increase PostgreSQL write IOPS
  - Warm up Redis cache

Auto-scale down 10 minutes after auction end
```

**Cost**: Higher for 15 minutes, saves on failures

---

## Clock Synchronization

### Problem: Server clock drift = unfair timestamps

**Requirement**: Server clocks accurate to <10ms

**Solution**: NTP (Network Time Protocol)

**Implementation**:
```bash
# Install chrony (better than ntpd)
apt-get install chrony

# Configure multiple time sources
/etc/chrony/chrony.conf:
  server time.google.com iburst
  server time.cloudflare.com iburst
  server pool.ntp.org iburst

# Monitor clock drift
chronyc tracking
```

**Target**: <5ms offset from true time

**Alert**: If drift >10ms, flag auctions for review

---

## Migration from Polling

### Current State: JavaScript Polling Every 1 Second

**Problems**:
- 1-second latency (unacceptable for bidding)
- Server load: 10K viewers × 1 req/sec = 10K req/sec
- Database load: 10K queries/second

**Migration Strategy**:

**Phase 1: WebSocket for Bidders, Keep Polling for Viewers** (Week 1-2)
- Deploy Centrifugo for bidders only (1K connections)
- Viewers continue polling (10K viewers)
- Test with small auctions

**Phase 2: WebSocket for Viewers (Separate Tier)** (Week 3-4)
- Deploy viewer-tier WebSocket (higher latency acceptable)
- Reduce polling to 10-second fallback

**Phase 3: Deprecate Polling** (Week 5-6)
- Remove polling for modern browsers
- Monitor cost, latency, error rates

---

## Recommendation

### Primary: Centrifugo + NATS (for fairness-critical auctions)

**Rationale**:
- Only option with guaranteed message ordering (NATS JetStream)
- Lowest latency (34-73ms best case)
- Cost-effective ($8-17/auction for 1K bidders)
- Server-authoritative timestamps
- Full audit trail

**When to Choose**:
- High-stakes auctions (>$10K value)
- Fairness critical (legal compliance)
- DevOps capacity available (15-20 hours/month)
- Budget: $1,000-2,000/month for 100 auctions

**Deal-breakers**:
- No DevOps expertise (choose Ably instead)
- Low-value auctions (<$1K, cost not justified)

---

### Alternative: Socket.IO + Redis Streams (for lower stakes)

**Rationale**:
- Node.js familiarity (lower learning curve)
- Acceptable latency (62-155ms)
- Lower cost than Ably ($470-1,020/month)

**When to Choose**:
- Medium-stakes auctions ($1K-10K value)
- Team prefers Node.js
- <200ms latency acceptable
- Budget: $500-1,500/month

**Deal-breakers**:
- <100ms latency required (Centrifugo better)
- High-frequency trading (Node.js not optimal)

---

### Not Recommended: Ably (too expensive), AppSync (too slow)

**Ably**: $5K-10K/month for 100 auctions (cost doesn't match auction economics)

**AppSync**: 130-330ms latency (fails <200ms requirement)

---

## Decision Matrix

| Requirement | Centrifugo + NATS | Socket.IO + Redis | Ably | AppSync |
|-------------|-------------------|-------------------|------|---------|
| **<100ms latency** | ✓ Yes (34-73ms) | Marginal (62-100ms) | Marginal (75-115ms) | ✗ No (130-330ms) |
| **Message ordering** | ✓ Guaranteed (NATS) | Custom (Redis) | ✓ Guaranteed | Limited |
| **Audit trail** | ✓ PostgreSQL | ✓ PostgreSQL | 7-day history | CloudWatch |
| **Fairness** | ✓ Server timestamp | Custom | Custom | Limited |
| **Cost (100 auctions)** | ✓ $800-1,650/mo | ✓ $470-1,020/mo | ✗ $5K-10K/mo | ✓ $500-1K/mo |
| **Setup time** | 8-12 weeks | 6-10 weeks | 2-4 weeks | 2-4 weeks |

**The Bottom Line**: For fairness-critical, high-stakes auctions, Centrifugo + NATS is the only viable option despite complexity. For lower stakes, Socket.IO + Redis offers acceptable trade-offs.
