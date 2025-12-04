# WebSocket Implementation Cost Comparison

**Research Tier**: S2 Comprehensive Portability Analysis
**Date Compiled**: December 3, 2025

## Overview

This document compares total cost of ownership (TCO) across WebSocket implementations at three scale points: 1,000, 5,000, and 10,000 concurrent connections. Costs include infrastructure, operational overhead, and hidden fees.

## Cost Model Assumptions

### Connection Profiles

**Small Event** (1,000 concurrent):
- Duration: 2 hours
- Messages per user: 10 messages/hour
- Total messages: 20,000

**Medium SaaS Dashboard** (5,000 concurrent):
- Duration: 8 hours/day (business hours)
- Messages per user: 120 messages/hour (2/minute)
- Daily messages: 4,800,000
- Monthly messages: ~144,000,000

**Large Platform** (10,000 concurrent):
- Duration: 24/7
- Messages per user: 300 messages/hour (5/minute)
- Daily messages: 72,000,000
- Monthly messages: ~2,160,000,000

### Operational Cost Assumptions

**DevOps hourly rate**: $100/hour (blended rate for DevOps engineer)

**Operational time estimates**:
- **Setup**: Initial infrastructure and deployment
- **Ongoing**: Monthly maintenance, updates, monitoring, incident response

## Managed Services Pricing

### Pusher

**Pricing tiers** (2025):
- Free: 200 connections, 200K messages/day
- Sandbox: $29/month (500 connections, unlimited messages)
- Startup: $99/month (1,000 connections, unlimited messages)
- Business: $299/month (2,000 connections, unlimited messages)
- Enterprise: Custom pricing

**Overage**: ~$5 per 100 connections/month (pro-rated)

**1,000 Concurrent** (Small Event, 2 hours):
- **Plan**: Startup ($99/month)
- **Pro-rated**: ~$3.30/day
- **Actual cost**: $99/month if sustained
- **TCO**: $99/month (no ops overhead)

**5,000 Concurrent** (Medium SaaS, 8h/day):
- **Base plan**: Business ($299 for 2,000 connections)
- **Overage**: 3,000 connections × $0.05 = $150
- **TCO**: $449/month (no ops overhead)

**10,000 Concurrent** (Large Platform, 24/7):
- **Plan**: Enterprise (negotiated)
- **Estimated**: $1,500-3,000/month
- **TCO**: $1,500-3,000/month

**Hidden costs**: None (egress included)

### Ably

**Pricing tiers** (2025):
- Free: 200 connections, 6M messages/month
- Standard: $29/month base (200 connections, 20M messages included)
- Pro: $299/month base (1,000 connections, 100M messages included)
- Enterprise: Custom

**Overages**:
- Connections: $4-5 per 100/month
- Messages: $2.00-2.50 per million

**1,000 Concurrent** (Small Event, 20K messages):
- **Option 1**: Pro ($299, all included)
- **Option 2**: Standard + overages ($29 + $40 connections = $69)
- **TCO**: $69/month (choosing Option 2)

**5,000 Concurrent** (Medium SaaS, 144M messages/month):
- **Base**: Pro ($299, 1K connections, 100M messages included)
- **Connection overage**: 4,000 × $0.04 = $160
- **Message overage**: 44M × $0.002 = $88
- **TCO**: $547/month

**10,000 Concurrent** (Large Platform, 2.16B messages/month):
- **Plan**: Enterprise (negotiated)
- **Calculated overage**: $299 + $360 (connections) + $4,120 (messages) = $4,779
- **Actual (negotiated)**: $3,000-5,000/month
- **TCO**: $3,000-5,000/month

**Hidden costs**: Bandwidth at extreme scale, Reactor functions separate pricing

### Supabase Realtime

**Pricing tiers** (2025):
- Free: 500MB DB, 2GB bandwidth, 50K MAU
- Pro: $25/month (8GB DB, 250GB bandwidth)
- Enterprise: Custom

**Overages** (Pro):
- Database: $0.125/GB/month
- Bandwidth: $0.09/GB

**Note**: Realtime is included with database; no separate WebSocket pricing

**1,000 Concurrent** (Small Event, 20K messages):
- **Plan**: Pro ($25/month, assumes existing Supabase usage)
- **Bandwidth**: ~20MB (negligible)
- **TCO**: $25/month (if already using Supabase DB)
- **Marginal Realtime cost**: $0

**5,000 Concurrent** (Medium SaaS, 4.8M messages/day):
- **Plan**: Pro ($25/month)
- **Bandwidth**: ~150GB/month = $13.50 overage
- **Database**: Minimal (assume $0.25)
- **TCO**: $38.75/month

**10,000 Concurrent** (Large Platform, 72M messages/day):
- **Plan**: Pro or Enterprise
- **Bandwidth**: ~2,160GB/month = $194.40 overage
- **Database**: ~10GB = $1.25
- **TCO**: $220/month (Pro) or Enterprise negotiation
- **Risk**: Connection pooling may be needed (Postgres limits)

**Hidden costs**: Postgres connection limits may require pgBouncer or connection pooling

**Value proposition**: Extremely cheap if already using Supabase database; expensive if not

## Self-Hosted Pricing

### Socket.io

**Infrastructure**:

**1,000 Concurrent** (Small Event):
- **Single server**: 2 vCPU, 4GB RAM
- **Cloud cost**: $30-40/month (AWS t3.medium, DigitalOcean droplet)
- **Setup time**: 40-80 hours
- **Ongoing ops**: 10-20 hours/month

**Cost breakdown**:
- Infrastructure: $30/month
- Setup: $4,000-8,000 (one-time)
- Ongoing ops: $1,000-2,000/month
- **TCO (first month)**: $5,030-10,030
- **TCO (steady state)**: $1,030-2,030/month

**5,000 Concurrent** (Medium SaaS):
- **Infrastructure**: 2 app servers + Redis ($120/month)
- **Monitoring**: $100/month
- **Setup time**: 60-100 hours
- **Ongoing ops**: 15 hours/month

**Cost breakdown**:
- Infrastructure: $220/month
- Setup: $6,000-10,000 (one-time)
- Ongoing ops: $1,500/month
- **TCO (first month)**: $7,720-11,720
- **TCO (steady state)**: $1,720/month

**10,000 Concurrent** (Large Platform):
- **Infrastructure**: 5 app servers + Redis HA ($400/month)
- **Monitoring + logging**: $300/month
- **Setup time**: 80-120 hours
- **Ongoing ops**: 20 hours/month

**Cost breakdown**:
- Infrastructure: $700/month
- Setup: $8,000-12,000 (one-time)
- Ongoing ops: $2,000/month
- **TCO (first month)**: $10,700-14,700
- **TCO (steady state)**: $2,700/month

### Centrifugo

**Infrastructure**:

**1,000 Concurrent** (Small Event):
- **Single server**: 2 vCPU, 4GB RAM (Memory engine, no Redis)
- **Cloud cost**: $30-40/month
- **Setup time**: 20-40 hours (simpler than Socket.io)
- **Ongoing ops**: 8-15 hours/month

**Cost breakdown**:
- Infrastructure: $35/month
- Setup: $2,000-4,000 (one-time)
- Ongoing ops: $800-1,500/month
- **TCO (first month)**: $2,835-5,535
- **TCO (steady state)**: $835-1,535/month

**5,000 Concurrent** (Medium SaaS):
- **Infrastructure**: Single server + Redis ($160/month)
- **Monitoring**: $100/month (Grafana Cloud or self-hosted Prometheus)
- **Setup time**: 30-50 hours
- **Ongoing ops**: 10 hours/month

**Cost breakdown**:
- Infrastructure: $260/month
- Setup: $3,000-5,000 (one-time)
- Ongoing ops: $1,000/month
- **TCO (first month)**: $4,260-6,260
- **TCO (steady state)**: $1,260/month

**10,000 Concurrent** (Large Platform):
- **Infrastructure**: 3 servers + Redis HA ($600/month)
- **Monitoring**: $200/month
- **Setup time**: 50-80 hours
- **Ongoing ops**: 15 hours/month

**Cost breakdown**:
- Infrastructure: $800/month
- Setup: $5,000-8,000 (one-time)
- Ongoing ops: $1,500/month
- **TCO (first month)**: $7,300-10,300
- **TCO (steady state)**: $2,300/month

## Total Cost of Ownership Summary

### 1,000 Concurrent Connections (Small Event)

| Implementation | Setup Cost | Monthly Steady State | Notes |
|----------------|------------|---------------------|-------|
| **Supabase** | $0 | $25 | If already using Supabase DB |
| **Pusher** | $0 | $99 | Easiest to start |
| **Ably** | $0 | $69 | Good balance |
| **Centrifugo** | $2K-4K | $835-1,535 | Requires ops capacity |
| **Socket.io** | $4K-8K | $1,030-2,030 | Higher ops overhead |

**Winner (low scale)**: Managed services (Supabase if applicable, otherwise Ably)

### 5,000 Concurrent Connections (Medium SaaS)

| Implementation | Setup Cost | Monthly Steady State | Break-Even (Months) |
|----------------|------------|---------------------|---------------------|
| **Supabase** | $0 | $39 | N/A (cheapest) |
| **Pusher** | $0 | $449 | - |
| **Ably** | $0 | $547 | - |
| **Centrifugo** | $3K-5K | $1,260 | Never (if counting ops) |
| **Socket.io** | $6K-10K | $1,720 | Never (if counting ops) |

**Winner (medium scale)**:
- **With ops capacity**: Supabase (if using DB) or Ably
- **Without ops capacity**: Ably (better features than Pusher for similar price)

**Note**: Self-hosted options don't break even when counting ops time at this scale

### 10,000 Concurrent Connections (Large Platform)

| Implementation | Setup Cost | Monthly Steady State | Annual TCO (Year 1) |
|----------------|------------|---------------------|---------------------|
| **Supabase** | $0 | $220 | $2,640 |
| **Pusher** | $0 | $1,500-3,000 | $18,000-36,000 |
| **Ably** | $0 | $3,000-5,000 | $36,000-60,000 |
| **Centrifugo** | $5K-8K | $2,300 | $32,600-35,600 |
| **Socket.io** | $8K-12K | $2,700 | $40,400-44,400 |

**Winner (large scale)**:
- **Database-centric use case**: Supabase ($220/month is unbeatable)
- **General-purpose**: Pusher ($1,500-3,000) or Centrifugo ($2,300 with ops)
- **Performance-critical**: Centrifugo (faster + cheaper than Ably)

**Note**: At this scale, self-hosted options start becoming competitive

## Break-Even Analysis

### Self-Hosted vs. Managed (Excluding Setup Costs)

**Centrifugo vs. Ably** (ignoring setup):

| Concurrent | Centrifugo/mo | Ably/mo | Savings |
|------------|---------------|---------|---------|
| 1,000 | $835-1,535 | $69 | Ably wins |
| 5,000 | $1,260 | $547 | Ably wins |
| 10,000 | $2,300 | $3,000-5,000 | Centrifugo wins |
| 50,000 | $5,000 | $15,000+ | Centrifugo wins (67% savings) |
| 100,000 | $8,000 | $30,000+ | Centrifugo wins (73% savings) |

**Break-even point**: ~8,000-10,000 concurrent connections

### Operational Capacity Consideration

**If you DON'T have DevOps capacity**:
- Self-hosted options cost MORE when counting ops time at contractor rates
- Managed services are cheaper up to 20,000+ concurrent connections

**If you DO have DevOps capacity** (salaried team):
- Self-hosted options become cheaper at 8,000-10,000+ concurrent
- Savings increase dramatically at scale (50K+: 60-70% savings)

## Hidden Costs Checklist

### Managed Services

**Pusher**:
- None (egress included, straightforward pricing)

**Ably**:
- Bandwidth overage at extreme scale
- Reactor functions (separate pricing)
- Extended message retention (Enterprise only)

**Supabase**:
- Bandwidth overage (can grow quickly)
- Postgres connection pooling infrastructure
- Database storage if persisting real-time data

### Self-Hosted

**Socket.io & Centrifugo**:
- **Setup time**: 20-120 hours (amortize over project lifetime)
- **Learning curve**: Team unfamiliarity with infrastructure
- **Monitoring tools**: Prometheus, Grafana, logging services ($100-300/month)
- **Security updates**: Ongoing patching and maintenance
- **Incident response**: On-call costs if 24/7 uptime required
- **Scaling overhead**: Load testing, performance tuning

## Cost Optimization Strategies

### Managed Services

1. **Right-size your plan**: Don't over-provision connections
2. **Use broadcast for ephemeral data**: Avoid persisting unnecessary messages (Ably)
3. **Optimize message payloads**: Reduce bandwidth charges
4. **Negotiate enterprise contracts**: Volume discounts at scale
5. **Choose correct region**: Avoid cross-region pricing

### Self-Hosted

1. **Start with single server**: Delay Redis/multi-server until needed
2. **Use memory engine**: Centrifugo's memory engine avoids Redis costs
3. **Self-host monitoring**: Prometheus + Grafana (free) vs. managed ($200+/month)
4. **Reserved instances**: 30-60% cloud cost savings for committed usage
5. **Spot instances**: For non-critical workloads (70-90% savings)

## Recommendation by Budget

### Minimal Budget (<$100/month)
- **Supabase** (if using Supabase DB): $25-39/month
- **Ably** (small scale): $69/month
- **Pusher** (if simplicity preferred): $99/month

### Moderate Budget ($100-500/month)
- **Ably**: Best features, reliability, scalability
- **Pusher**: Simpler, adequate features
- **Supabase**: If database-centric

### Large Budget ($1,000+/month)
- **Self-hosted (Centrifugo)**: Best performance, lower long-term cost
- **Managed (Ably)**: If no DevOps capacity
- **Pusher**: If simplicity outweighs cost

### Enterprise Budget ($5,000+/month)
- **Self-hosted (Centrifugo)**: 60-70% cost savings vs. managed
- **Managed**: Only if operational overhead unacceptable

## 3-Year TCO Projection (10,000 Concurrent)

| Implementation | Year 1 | Year 2 | Year 3 | Total (3 years) |
|----------------|--------|--------|--------|-----------------|
| **Supabase** | $2,640 | $2,640 | $2,640 | $7,920 |
| **Pusher** | $18,000 | $18,000 | $18,000 | $54,000 |
| **Ably** | $36,000 | $36,000 | $36,000 | $108,000 |
| **Centrifugo** | $35,600 | $27,600 | $27,600 | $90,800 |
| **Socket.io** | $44,400 | $32,400 | $32,400 | $109,200 |

**Long-term winner (general-purpose)**: Pusher ($54K) or Centrifugo ($90.8K with ops)
**Long-term winner (database-centric)**: Supabase ($7.9K)

## Conclusion

**Cost-effective choices by scale**:

- **<1K connections**: Managed services (Supabase $25, Ably $69, Pusher $99)
- **1K-5K connections**: Managed services still optimal (Ably or Pusher)
- **5K-10K connections**: Transition point (Pusher $1.5K-3K vs. Centrifugo $2.3K)
- **10K-50K connections**: Self-hosted starts winning (Centrifugo 30-50% cheaper)
- **50K+ connections**: Self-hosted strongly preferred (60-70% savings)

**Critical factor**: Operational capacity
- **Without DevOps**: Managed services cheaper until 20K+ connections
- **With DevOps**: Self-hosted cheaper at 10K+ connections
