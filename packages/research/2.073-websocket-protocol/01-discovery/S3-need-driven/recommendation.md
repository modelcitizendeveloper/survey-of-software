# S3 Need-Driven Recommendations: WebSocket Protocol

## Executive Summary

**Core Finding**: WebSocket implementation choice depends entirely on specific operational requirements, not theoretical capabilities. The "best" solution varies by use case scale, latency tolerance, operational capacity, and budget constraints.

**Key Insight**: Self-hosted solutions (Centrifugo, Socket.IO) offer lowest latency and cost at scale, but require DevOps investment. Managed services (Ably, Pusher) trade higher cost and latency for zero operations. Backend-integrated solutions (Supabase) excel for database-driven real-time sync.

## Decision Framework by Use Case

### Use Case 1: Live Event Synchronization (1K-10K users, <100ms target)

**Requirement Summary**:
- Scale: 1,000-10,000 concurrent devices
- Latency: <100ms desired, <200ms acceptable
- Pattern: Broadcast-heavy (1→N, N=1000+)
- Duration: Event-based (hours, not 24/7)

**Primary Recommendation: Centrifugo (Self-Hosted)**

**Rationale**:
- Latency: 50-85ms (MEETS <100ms requirement)
- Cost: $330-590/month for 5K-10K users
- Full infrastructure control
- Scales predictably

**When to Choose**:
- DevOps capacity available (5-10 hours/month)
- Budget: $500-1,000/month operational
- <100ms latency requirement
- Multiple events per month (cost amortization)

**Alternative: Ably (Managed)**

**When to Choose**:
- Launch timeline <4 weeks
- No DevOps capacity
- Global user base (multi-region required)
- Acceptable: 70-110ms latency, $600-3,000/month at scale

**Decision Criteria**:

| Factor | Centrifugo | Ably |
|--------|------------|------|
| Latency | ✓ 50-85ms | Marginal (70-110ms) |
| Cost (10K users) | ✓ $390-590/mo | ✗ $2K-3K/mo |
| Setup time | 2-3 weeks | 1-2 days |
| Operations | 5-10 hrs/mo | Zero |
| Control | Full | Limited |

**The Bottom Line**: Choose Centrifugo if you have DevOps capacity and <100ms requirement. Choose Ably if you need instant deployment and can accept 70-110ms latency.

---

### Use Case 2: SaaS Real-Time Dashboard (500-5K users, <200ms acceptable)

**Requirement Summary**:
- Scale: 500-5,000 concurrent users
- Latency: <200ms acceptable
- Pattern: Per-user subscriptions (filtered data)
- Duration: 24/7, spiky during business hours
- Database integration critical

**Primary Recommendation: Supabase Realtime (PostgreSQL-based SaaS)**

**Rationale**:
- Integrated solution (DB + auth + realtime)
- Automatic tenant filtering (row-level security)
- Cost: $25-599/month for 500-5K users
- Latency: 60-200ms (acceptable)
- Zero separate infrastructure

**When to Choose**:
- Using PostgreSQL as primary database
- Team size <10 engineers
- Budget: $500-1,000/month
- Latency: <200ms acceptable

**Alternative 1: Ably (Non-PostgreSQL backends)**

**When to Choose**:
- Using MySQL, MongoDB, or other database
- Global user base (multi-region)
- Lower latency desired (60-110ms)
- Budget: $750-1,500/month at 5K users

**Alternative 2: Socket.IO (Cost optimization at scale)**

**When to Choose**:
- DevOps capacity available (10 hours/month)
- >5K users (cost savings justify complexity)
- Node.js expertise on team
- Cost: $450-750/month vs $599-1,500 for managed

**Decision Criteria**:

| Factor | Supabase | Ably | Socket.IO |
|--------|----------|------|-----------|
| PostgreSQL | ✓ Perfect | Works | Works |
| Other DBs | ✗ No | ✓ Yes | ✓ Yes |
| Latency | 60-200ms | 60-110ms | 56-170ms |
| Cost (5K users) | ✓ $599/mo | $750-1.2K/mo | ✓ $450-750/mo |
| Setup time | 3-5 days | 3-5 days | 2-4 weeks |
| Operations | Zero | Zero | 10 hrs/mo |

**The Bottom Line**: For PostgreSQL-based SaaS with <5K users, Supabase offers best cost-to-value. For larger scale or non-PostgreSQL, choose Ably (managed) or Socket.IO (self-hosted with DevOps).

---

### Use Case 3: Collaborative Document Editing (2-50 editors, <100ms target)

**Requirement Summary**:
- Scale: 2-50 concurrent editors per document
- Latency: <100ms for responsive UX
- Pattern: Operational Transform (OT) or CRDT
- Duration: Session-based (15 minutes - 8 hours)
- Offline support critical

**Primary Recommendation: Socket.IO + ShareDB (OT Framework)**

**Rationale**:
- Proven OT implementation (battle-tested)
- Latency: 45-95ms (MEETS <100ms)
- Cost: $420-1,040/month for 5K connections
- Full control over conflict resolution
- Server-authoritative (easier reasoning)

**When to Choose**:
- Building production collaborative editor
- Need server-authoritative conflict resolution
- Team has DevOps capacity (10-15 hours/month)
- Budget: $500-1,500/month at 5K users

**Alternative 1: Yjs (CRDT, Offline-First)**

**Rationale**:
- Lowest latency (11-35ms P2P, 45-95ms via server)
- Offline-first architecture (best UX)
- CRDT simplicity (no complex OT)
- Lowest cost ($240-720/month)

**When to Choose**:
- Offline support critical
- Advanced engineering team (CRDT experience)
- <50ms latency desired (P2P mode)
- Want peer-to-peer option

**Alternative 2: Ably + Custom OT Logic**

**When to Choose**:
- Global user base (multi-region)
- Small team (<5 engineers, no DevOps)
- Willing to build OT logic yourself
- Budget: $750-1,200/month at 20K users

**Decision Criteria**:

| Factor | ShareDB | Yjs | Ably + OT |
|--------|---------|-----|-----------|
| Latency | 45-95ms | ✓ 11-95ms | 60-140ms |
| Offline | Manual | ✓ Built-in | Manual |
| OT/CRDT | ✓ OT built-in | ✓ CRDT | Build yourself |
| Cost (5K users) | $420-1K/mo | ✓ $240-720/mo | $200-300/mo |
| Setup time | 8-12 weeks | ✓ 4-8 weeks | 4-8 weeks |
| Operations | 10-15 hrs/mo | 5-10 hrs/mo | Zero |

**The Bottom Line**: ShareDB (OT) is safest for production. Yjs (CRDT) offers best latency and offline support. Avoid Firepad (latency too high, maintenance concerns).

---

### Use Case 4: Live Auction / Bidding Platform (100-10K bidders, <100ms critical)

**Requirement Summary**:
- Scale: 100-10,000 concurrent bidders
- Latency: <100ms critical (fairness)
- Pattern: Broadcast with strict ordering
- Duration: Minutes to hours (event-based)
- Fairness guarantees required

**Primary Recommendation: Centrifugo + NATS (Self-Hosted, Ordered)**

**Rationale**:
- Guaranteed message ordering (NATS JetStream)
- Latency: 34-73ms (MEETS <100ms requirement)
- Cost: $830-1,650/month for 1K bidders + 10K viewers
- Server-authoritative timestamps
- Full audit trail (PostgreSQL)

**When to Choose**:
- High-stakes auctions (>$10K value)
- Fairness critical (legal compliance)
- DevOps capacity available (15-20 hours/month)
- Budget: $1,000-2,000/month for 100 auctions

**Alternative: Socket.IO + Redis Streams (Lower Stakes)**

**When to Choose**:
- Medium-stakes auctions ($1K-10K value)
- Team prefers Node.js
- <200ms latency acceptable
- Budget: $500-1,500/month

**Not Recommended**:
- **Ably**: Too expensive ($5K-10K/month for 100 auctions)
- **AppSync**: Too slow (130-330ms latency)

**Decision Criteria**:

| Factor | Centrifugo + NATS | Socket.IO + Redis |
|--------|-------------------|-------------------|
| Latency | ✓ 34-73ms | 62-155ms |
| Ordering | ✓ Guaranteed (NATS) | Custom (Redis) |
| Fairness | ✓ Server timestamp | Custom |
| Audit trail | ✓ PostgreSQL | ✓ PostgreSQL |
| Cost (100 auctions) | ✓ $830-1,650/mo | ✓ $470-1,020/mo |
| Setup time | 8-12 weeks | 6-10 weeks |

**The Bottom Line**: For fairness-critical, high-stakes auctions, Centrifugo + NATS is the only viable option despite complexity. For lower stakes, Socket.IO + Redis offers acceptable trade-offs.

---

## General Recommendations by Constraint

### By Latency Requirement

**<50ms (Exceptional)**:
- **Solution**: Yjs (CRDT, P2P mode)
- **Cost**: $240-720/month
- **Use Case**: Collaborative editing, offline-first
- **Caveat**: P2P not always possible (NAT, firewalls)

**<100ms (Critical)**:
- **Solution**: Centrifugo (self-hosted)
- **Cost**: $330-1,650/month (depends on scale)
- **Use Case**: Live events, auctions, real-time dashboards
- **Caveat**: Requires DevOps (5-15 hours/month)

**<200ms (Acceptable)**:
- **Solution**: Ably or Supabase (managed)
- **Cost**: $150-1,500/month (depends on scale)
- **Use Case**: SaaS dashboards, notifications
- **Caveat**: Higher cost than self-hosted

**<500ms (Tolerable)**:
- **Solution**: Pusher or polling
- **Cost**: $0-299/month
- **Use Case**: Non-critical updates, leaderboards
- **Caveat**: Not suitable for interactive use cases

---

### By Budget Constraint

**<$500/month**:
- **Small scale (<1K users)**: Pusher ($0-299), Supabase ($25)
- **Self-hosted**: Socket.IO ($200-500 infra + ops)
- **Caveat**: Limited scale, may need migration later

**$500-1,500/month**:
- **Medium scale (1K-5K users)**: Supabase ($599), Ably ($750), Socket.IO ($450-750)
- **Recommended**: Supabase (if PostgreSQL), Socket.IO (if DevOps)

**$1,500-5,000/month**:
- **Large scale (5K-20K users)**: Ably ($1.5K-3K), Centrifugo ($690-1,650)
- **Recommended**: Centrifugo (best cost-performance)

**>$5,000/month**:
- **Enterprise scale (>20K users)**: Custom self-hosted infrastructure
- **Consider**: Multi-region deployment, dedicated team

---

### By Team Size & Expertise

**Team <5 engineers, no DevOps**:
- **Recommendation**: Managed services (Pusher, Ably, Supabase)
- **Rationale**: Operational burden too high for small teams
- **Cost**: 2-3x self-hosted, but total cost of ownership lower

**Team 5-15 engineers, moderate DevOps**:
- **Recommendation**: Socket.IO (self-hosted)
- **Rationale**: Cost savings justify operational overhead
- **Investment**: 10-20 hours/month DevOps

**Team >15 engineers, strong DevOps**:
- **Recommendation**: Centrifugo or custom (self-hosted)
- **Rationale**: Maximum control, lowest cost at scale
- **Investment**: Can amortize across multiple projects

---

### By Database Type

**PostgreSQL**:
- **Best**: Supabase Realtime (integrated, row-level security)
- **Alternative**: Ably or Socket.IO (if Supabase limits reached)

**MySQL, MongoDB, other**:
- **Best**: Ably (database-agnostic)
- **Alternative**: Socket.IO (custom integration)

**No database (stateless)**:
- **Best**: Pusher or Ably (pure messaging)
- **Alternative**: Centrifugo (lightweight)

---

## Migration Recommendations

### From Polling → WebSocket

**Timeline**: 6-9 weeks
**Cost**: $5K-15K (engineering time)
**Recommended path**:
1. Start with managed service (Pusher/Ably) for quick deployment
2. Keep polling as fallback
3. Gradual rollout (10% → 50% → 100%)
4. Migrate to self-hosted later if cost justified

---

### From Self-Hosted → Managed

**Timeline**: 6-10 weeks
**Cost**: $8K-20K (engineering time)
**When to migrate**: DevOps burden >20 hours/month OR team shrinking
**Recommended path**:
1. Proof of concept with 5% traffic
2. Dual publishing (old + new)
3. Gradual migration
4. Decommission self-hosted

---

### From Managed → Self-Hosted

**Timeline**: 8-10 weeks
**Cost**: $10K-30K (engineering time)
**When to migrate**: Monthly cost >$2K AND DevOps capacity available
**Recommended path**:
1. Deploy self-hosted in parallel (2-4 weeks setup)
2. Dual publishing
3. Gradual migration (monitor closely)
4. Cancel managed service

**Break-even**: 2-3 months after migration

---

## Cost-Performance Matrix

| Solution | Setup Time | Monthly Cost (5K users) | Latency (P95) | Operations | Best For |
|----------|------------|-------------------------|---------------|------------|----------|
| **Yjs (CRDT)** | 4-8 weeks | $240-720 | 11-95ms | 5-10 hrs/mo | Offline-first, collaborative |
| **Centrifugo** | 2-3 weeks | $330-1,650 | 50-85ms | 5-15 hrs/mo | Live events, auctions |
| **Socket.IO** | 1-2 weeks | $450-1,020 | 56-170ms | 10-15 hrs/mo | Node.js teams, cost optimization |
| **Supabase** | 3-5 days | $599 | 60-200ms | Zero | PostgreSQL-based SaaS |
| **Ably** | 3-5 days | $750-1,500 | 60-110ms | Zero | Global, multi-region |
| **Pusher** | 1-2 days | $299-1,500 | 120-260ms | Zero | Rapid MVP, small scale |

---

## The Honest Assessment: Can You Achieve Your Requirements?

### <50ms Latency at 10,000 Devices: NO

**Physics Reality**:
- Network RTT: 15-100ms (cannot be improved)
- Fan-out overhead: 100-200ms for 10K devices
- Best achievable: 80-120ms (Centrifugo, same region)

**Only achievable with**:
- P2P connections (Yjs WebRTC, <100 peers)
- Streaming broadcast (first 100 devices <50ms, rest 100-200ms)
- Same-datacenter testing (not real-world)

---

### <100ms Latency at 5,000 Devices: YES (with caveats)

**Achievable with**:
- Centrifugo or Yjs (self-hosted)
- Same-region deployment (all users <500km from server)
- WiFi/wired connections (not 4G/3G)
- Cost: $330-1,650/month

**Not achievable with**:
- Managed services (add 20-50ms overhead)
- Global/multi-region (cross-region latency)
- Mobile networks (4G adds 50-150ms baseline)

---

### <200ms Latency at Any Scale: YES

**Achievable with**:
- Any solution (managed or self-hosted)
- Multi-region deployment acceptable
- Mixed network conditions (WiFi, 4G)
- Cost: $150-1,500/month (depends on service)

---

### Zero Operational Overhead: YES (but trade-offs)

**Achievable with**:
- Managed services (Pusher, Ably, Supabase)
- Cost premium: 2-3x self-hosted
- Latency premium: +20-50ms
- Vendor lock-in risk

**Trade-off**: Pay more, get less control, but zero operations

---

## Final Recommendations

### For Startups & MVPs

**Start with**: Pusher or Supabase (managed)
**Rationale**: Fast deployment, low risk, predictable costs
**Timeline**: 1-5 days to production
**Cost**: $0-599/month
**Migrate to**: Ably or self-hosted when >1K users

---

### For Growth-Stage SaaS

**Start with**: Supabase (if PostgreSQL) or Ably (if other DB)
**Rationale**: Balance of cost, latency, operations
**Timeline**: 3-5 days to production
**Cost**: $599-1,500/month at 5K users
**Migrate to**: Socket.IO or Centrifugo when >5K users (cost optimization)

---

### For Enterprise / High-Scale

**Start with**: Centrifugo or Socket.IO (self-hosted)
**Rationale**: Lowest cost at scale, full control
**Timeline**: 2-4 weeks to production
**Cost**: $450-1,650/month at 5K-20K users
**Invest in**: DevOps capacity (10-20 hours/month)

---

### For Time-Critical / Fairness-Driven

**Start with**: Centrifugo + NATS (ordered messaging)
**Rationale**: Only option with guaranteed ordering + low latency
**Timeline**: 8-12 weeks to production
**Cost**: $830-1,650/month
**Critical for**: Auctions, trading, competitive gaming

---

### For Offline-First / Collaborative

**Start with**: Yjs (CRDT) or ShareDB (OT)
**Rationale**: Purpose-built for conflict-free collaboration
**Timeline**: 4-12 weeks (depends on complexity)
**Cost**: $240-1,040/month
**Choose Yjs if**: Offline critical, lowest latency desired
**Choose ShareDB if**: Server-authoritative, proven production

---

## Decision Tree

```
Need WebSocket?
├─ Latency requirement?
│  ├─ <50ms → Yjs (CRDT, P2P) OR Same-region Centrifugo
│  ├─ <100ms → Centrifugo (self-hosted) OR Ably (managed)
│  ├─ <200ms → Supabase OR Ably OR Socket.IO
│  └─ <500ms → Pusher OR polling fallback
│
├─ Database integration?
│  ├─ PostgreSQL → Supabase Realtime (best integration)
│  ├─ Other DB → Ably OR Socket.IO (custom)
│  └─ No DB → Pusher OR Ably (pure messaging)
│
├─ Team size?
│  ├─ <5 engineers → Managed (Pusher, Ably, Supabase)
│  ├─ 5-15 engineers → Socket.IO (moderate DevOps)
│  └─ >15 engineers → Centrifugo (full control)
│
├─ Budget?
│  ├─ <$500/mo → Pusher OR Supabase ($0-599)
│  ├─ $500-1.5K/mo → Ably OR Socket.IO
│  └─ >$1.5K/mo → Centrifugo (self-hosted)
│
└─ Special requirements?
   ├─ Offline-first → Yjs (CRDT) OR Firebase
   ├─ Collaborative editing → ShareDB (OT) OR Yjs
   ├─ Fairness/ordering → Centrifugo + NATS
   └─ Global multi-region → Ably (managed edge)
```

---

## Key Takeaways

1. **No one-size-fits-all**: Use case requirements determine best solution
2. **Latency vs Cost trade-off**: Self-hosted achieves lowest latency, managed has zero ops
3. **Migration is common**: Start managed, migrate to self-hosted at scale (6-10 week timeline)
4. **DevOps investment**: Self-hosted requires 10-20 hours/month operational capacity
5. **Physics constraints**: <50ms at 10K devices is not achievable, <100ms requires careful architecture
6. **Database integration**: Supabase excels for PostgreSQL, Ably for database-agnostic

**The Bottom Line**: Choose managed services (Pusher, Ably, Supabase) for rapid deployment and small teams. Migrate to self-hosted (Centrifugo, Socket.IO) when scale justifies operational investment (typically >5K users or >$1.5K/month costs).
