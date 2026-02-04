# S1: Rapid Discovery - Redis Hosting Services

**Experiment**: 2.033 - Redis Hosting Services
**Stage**: S1 - Rapid Discovery (Service Landscape)
**Date**: 2025-10-10
**Methodology**: MPSE Stage 1 - Quick service ecosystem scan

---

## What is Redis Hosting?

**Redis** (Remote Dictionary Server) is an in-memory data structure store used as:
- **Cache**: Fast key-value lookups (session storage, API responses)
- **Message broker**: Pub/sub, job queues (Celery, RQ)
- **Database**: Persistent storage with snapshots/AOF
- **Real-time**: Leaderboards, rate limiting, counters

**Why Host It?**
- Redis is open-source (you can self-host)
- But: Requires operational expertise (replication, backups, monitoring)
- Managed services trade cost for convenience

---

## Redis Hosting Service Landscape

### 🏆 **Tier 1: Purpose-Built Redis Providers**

#### **1. Upstash**
- **URL**: upstash.com
- **Positioning**: Serverless Redis with per-request pricing
- **Founded**: 2021 (relatively new)
- **Unique Feature**: Pay-per-request (not monthly cap)
- **Free Tier**: 10K requests/day, 256MB storage
- **Pricing**: $0.20 per 100K requests
- **Best For**: Serverless apps, unpredictable traffic

**Why Consider**:
- No monthly minimum (true pay-as-you-go)
- Edge caching (global read replicas)
- REST API (no Redis client needed)

**Concerns**:
- Young company (3 years old, VC-backed)
- Limited track record vs Redis Labs

---

#### **2. Redis Cloud (Redis Labs)**
- **URL**: redis.com/redis-enterprise-cloud
- **Positioning**: Official Redis company's managed offering
- **Founded**: 2011 (Redis Labs, now Redis Inc.)
- **Unique Feature**: Redis modules (RedisJSON, RediSearch, RedisGraph)
- **Free Tier**: 30MB, 30 connections
- **Pricing**: $5/month (100MB), scales to enterprise
- **Best For**: Production workloads, Redis expertise

**Why Consider**:
- Official Redis company (most Redis knowledge)
- Advanced features (RedisJSON, RedisSearch)
- Enterprise-grade reliability

**Concerns**:
- More expensive than alternatives
- Enterprise focus (overkill for small projects)

---

#### **3. Redis Enterprise (Self-Managed)**
- **URL**: redis.com/redis-enterprise/software
- **Positioning**: Self-hosted Redis with enterprise features
- **Model**: License + your infrastructure
- **Pricing**: Contact sales (expensive)
- **Best For**: Large enterprises, compliance requirements

**Skip unless**: Multi-million dollar company with dedicated ops team

---

### 🔧 **Tier 2: Cloud Provider Managed Redis**

#### **4. AWS ElastiCache for Redis**
- **URL**: aws.amazon.com/elasticache
- **Positioning**: AWS-native Redis
- **Free Tier**: None (paid only)
- **Pricing**: $0.017/hour (~$12/month) for t4g.micro (0.5GB)
- **Best For**: Already on AWS, need VPC integration

**Why Consider**:
- Deep AWS integration (VPC, IAM, CloudWatch)
- Global infrastructure
- Battle-tested at scale

**Concerns**:
- No free tier
- Complex pricing (instance + data transfer)
- AWS lock-in

---

#### **5. Google Cloud Memorystore**
- **URL**: cloud.google.com/memorystore
- **Positioning**: GCP-native Redis
- **Free Tier**: None
- **Pricing**: $0.049/GB-hour (~$35/month for 1GB)
- **Best For**: Already on GCP

**Concerns**:
- More expensive than AWS
- Limited global availability

---

#### **6. Azure Cache for Redis**
- **URL**: azure.microsoft.com/en-us/services/cache
- **Positioning**: Azure-native Redis
- **Free Tier**: None
- **Pricing**: $0.026/hour (~$19/month for 0.25GB Basic)
- **Best For**: Already on Azure, .NET ecosystem

---

### 🚀 **Tier 3: Platform-Integrated Redis**

#### **7. Render Redis**
- **URL**: render.com/docs/redis
- **Positioning**: Redis bundled with PaaS
- **Free Tier**: 25MB (included with web services)
- **Pricing**: $7/month (256MB Starter), $15/month (1GB Standard)
- **Best For**: Render users, simple deployments

**Why Consider**:
- Seamless integration with Render apps
- Free tier included (no credit card)
- Simple pricing, no surprises

**Concerns**:
- Platform lock-in (Render-specific)
- Limited features vs Redis Cloud

---

#### **8. Heroku Redis**
- **URL**: heroku.com/redis
- **Positioning**: Redis add-on for Heroku
- **Free Tier**: 25MB (hobby tier)
- **Pricing**: $15/month (premium-0, 100MB)
- **Best For**: Heroku users

**Concerns**:
- Heroku ecosystem sunset concerns (Salesforce ownership)
- More expensive than alternatives

---

#### **9. Railway Redis**
- **URL**: railway.app/redis
- **Positioning**: Redis template on Railway
- **Free Tier**: $5 credit/month (covers ~100MB Redis)
- **Pricing**: Usage-based ($0.15/GB-hour + $0.10/GB-transfer)
- **Best For**: Railway users, hobby projects

---

#### **10. Fly.io Redis (Tigris)**
- **URL**: fly.io/docs/reference/tigris
- **Positioning**: Distributed Redis alternative (Tigris, not Redis)
- **Free Tier**: None (pay-as-you-go)
- **Pricing**: $0.0025/GB-hour (~$1.80/GB-month)
- **Best For**: Fly.io users, global distribution

**Note**: Fly.io uses Tigris (S3-compatible storage), not true Redis

---

#### **11. Vercel KV (Powered by Upstash)**
- **URL**: vercel.com/storage/kv
- **Positioning**: Redis for Vercel serverless functions
- **Free Tier**: 256MB, 10K requests/day
- **Pricing**: Same as Upstash ($0.20 per 100K requests)
- **Best For**: Vercel users, edge caching

**Note**: Vercel KV is Upstash under the hood

---

#### **12. Supabase (No Native Redis)**
- **Status**: Supabase does NOT offer Redis hosting
- **Alternative**: Use PostgreSQL with LISTEN/NOTIFY for pub/sub
- **Recommendation**: Pair Supabase with Upstash if Redis needed

---

### 🛠️ **Tier 4: DIY / Self-Hosted**

#### **13. DigitalOcean Managed Redis**
- **URL**: digitalocean.com/products/managed-databases-redis
- **Positioning**: Simple managed Redis on DO
- **Free Tier**: None
- **Pricing**: $15/month (1GB, single node)
- **Best For**: DigitalOcean droplet users

---

#### **14. Linode (Akamai) Managed Redis**
- **URL**: linode.com/products/databases
- **Positioning**: Managed Redis on Linode/Akamai
- **Free Tier**: None
- **Pricing**: ~$15/month (1GB)
- **Best For**: Linode users, predictable pricing

---

#### **15. Self-Hosted Redis on VPS**
- **Providers**: Hetzner ($5/month), DigitalOcean ($6/month), Linode ($5/month)
- **Approach**: Install Redis on your own VPS
- **Cost**: $5-10/month (VPS) + time
- **Best For**: Full control, learning, scale optimization

**Setup Cost**: 2-4 hours initial, 2-4 hours/month maintenance

---

## Quick Comparison Matrix

| Provider | Free Tier | Starter Price | 1GB Price | Standout Feature |
|----------|-----------|---------------|-----------|------------------|
| **Upstash** | 256MB, 10K req/day | $0.20/100K req | ~$20/month | Pay-per-request, serverless |
| **Redis Cloud** | 30MB | $5/month (100MB) | $50/month | Official Redis, modules |
| **AWS ElastiCache** | None | $12/month (0.5GB) | $50/month | AWS ecosystem |
| **Render Redis** | 25MB (free) | $7/month (256MB) | $15/month | PaaS integration |
| **Heroku Redis** | 25MB | $15/month (100MB) | $80/month | Heroku add-on |
| **Railway** | $5 credit | ~$10/month (1GB) | ~$10/month | Usage-based |
| **DigitalOcean** | None | $15/month (1GB) | $15/month | Simple pricing |
| **Self-Hosted** | N/A | $5/month (VPS) | $5-10/month | Full control |

---

## Quick Selection Guide

### **Choose Upstash if:**
- Serverless/edge functions (Vercel, Cloudflare Workers)
- Unpredictable traffic (pay-per-request better than fixed monthly)
- Need global read replicas
- Want REST API access (no Redis client required)

### **Choose Redis Cloud if:**
- Production workload with consistent traffic
- Need Redis modules (RedisJSON, RediSearch)
- Want official Redis company support
- Budget allows ($50+/month)

### **Choose Render Redis if:**
- Already using Render for hosting
- Simple cache/session storage
- Want free tier with no credit card
- Budget-conscious ($0-7/month)

### **Choose AWS ElastiCache if:**
- Already on AWS
- Need VPC integration
- Enterprise compliance requirements
- Willing to pay for AWS ecosystem

### **Choose Self-Hosted if:**
- High scale (>10GB Redis)
- Full control requirements
- Team has Redis ops expertise
- Cost optimization ($5/month VPS vs $50/month managed)

---

## Pricing Patterns

### **Free Tiers** (Solo founders, hobby projects)
1. **Render**: 25MB free (no credit card)
2. **Upstash**: 256MB + 10K requests/day (credit card required)
3. **Redis Cloud**: 30MB free
4. **Railway**: $5 credit/month (covers ~100MB)

**Best**: Render (no credit card) or Upstash (largest free tier)

---

### **Low Budget** ($0-10/month)
1. **Render**: $0 (25MB free) or $7/month (256MB)
2. **Redis Cloud**: $5/month (100MB)
3. **Self-Hosted VPS**: $5-10/month (unlimited, but DIY)

**Best**: Render free tier for most small apps

---

### **Growing** ($10-50/month)
1. **Upstash**: ~$20/month (1GB equiv, usage-based)
2. **Render**: $15/month (1GB)
3. **DigitalOcean**: $15/month (1GB)
4. **AWS ElastiCache**: $50/month (1GB + data transfer)

**Best**: Render or DigitalOcean (simple pricing)

---

### **Production Scale** ($50-200/month)
1. **Redis Cloud**: $50-200/month (1-10GB)
2. **AWS ElastiCache**: $50-150/month (1-5GB)
3. **Self-Hosted**: $10-40/month (dedicated server)

**Best**: Redis Cloud (features) or self-hosted (cost)

---

## Common Use Case Patterns

### **1. Session Storage**
- **Scale**: Small-medium (100MB-1GB)
- **Recommendation**: Render ($7/month) or Upstash (pay-per-request)
- **Why**: Simple, predictable, low stakes

### **2. API Rate Limiting**
- **Scale**: Small (10-100MB)
- **Recommendation**: Upstash (edge caching) or Render free tier
- **Why**: Global distribution matters, low memory needs

### **3. Job Queue (Celery, RQ)**
- **Scale**: Medium (1-10GB)
- **Recommendation**: Redis Cloud or DigitalOcean
- **Why**: Persistence important, predictable traffic

### **4. Real-Time Analytics**
- **Scale**: Large (10-100GB)
- **Recommendation**: Self-hosted or Redis Cloud enterprise
- **Why**: High memory needs, cost optimization critical

### **5. Pub/Sub (Chat, Notifications)**
- **Scale**: Small-medium (100MB-1GB)
- **Recommendation**: Redis Cloud or Upstash
- **Why**: Connection stability matters, latency-sensitive

### **6. Cache (CDN, Page Caching)**
- **Scale**: Medium (1-10GB)
- **Recommendation**: Upstash (edge) or Render
- **Why**: Global distribution helpful, eviction acceptable

---

## Red Flags & Vendor Concerns

### 🚩 **Upstash**: Young Company Risk
- Founded 2021 (3 years old)
- VC-funded (Series A, $8M raised)
- **Risk**: Acquisition or shutdown possible
- **Mitigation**: Data portability (Redis protocol compatible)

### 🚩 **Heroku**: Ecosystem Uncertainty
- Salesforce ownership (divesting non-core)
- Pricing higher than alternatives
- **Risk**: Further price increases or sunset
- **Mitigation**: Plan migration path

### 🚩 **Railway**: Sustainability Concerns
- Generous free tier ($5/month credit)
- **Risk**: Free tier reduction (common pattern)
- **Mitigation**: Budget for $10/month paid tier

### 🚩 **Redis Cloud**: Pricing Complexity
- Entry price low ($5/month), scales steeply
- Enterprise sales pressure
- **Risk**: Bill shock at scale
- **Mitigation**: Set billing alerts, understand pricing

### 🚩 **AWS ElastiCache**: Hidden Costs
- Data transfer fees can double bill
- Complex pricing calculator
- **Risk**: Unexpected costs ($50/month → $150/month)
- **Mitigation**: Enable cost explorer, budget alerts

---

## Ecosystem Maturity Assessment

### **Strengths**
✅ Multiple mature options (Redis Labs, AWS, DigitalOcean)
✅ Free tiers widely available (Render, Upstash, Redis Cloud)
✅ Redis protocol standardization (easy migration)
✅ Clear pricing tiers for different scales

### **Gaps**
❌ No dominant "obvious choice" (fragmented market)
❌ Serverless Redis still emerging (Upstash leading, but new)
❌ Global distribution expensive (Redis Cloud only)
❌ Limited Redis module support outside Redis Cloud

### **Trends**
📈 Serverless Redis adoption (pay-per-request models)
📈 PaaS-integrated Redis (Render, Railway, Vercel KV)
📉 Self-hosting Redis (complexity not worth it for most)
📉 Heroku Redis (ecosystem decline)

---

## Decision Framework

### **Step 1: Assess Your Scale**

**Hobby/MVP (<100 users)**:
- Memory: <100MB
- Requests: <10K/day
- **Recommendation**: Render free tier (25MB) or Upstash free (256MB)

**Early Stage (100-1K users)**:
- Memory: 100MB-1GB
- Requests: 10K-100K/day
- **Recommendation**: Render $7/month or Redis Cloud $5-15/month

**Growing (1K-10K users)**:
- Memory: 1-10GB
- Requests: 100K-1M/day
- **Recommendation**: Redis Cloud or DigitalOcean managed

**Scale (>10K users)**:
- Memory: 10-100GB
- Requests: 1M+/day
- **Recommendation**: Self-hosted or Redis Cloud enterprise

---

### **Step 2: Evaluate Hosting Context**

**Already on Render?** → Use Render Redis
**Already on Vercel?** → Use Vercel KV (Upstash)
**Already on AWS?** → Consider ElastiCache (but expensive)
**Platform-agnostic?** → Upstash or Redis Cloud

---

### **Step 3: Budget Reality Check**

| Monthly Budget | Best Options |
|----------------|--------------|
| **$0** | Render free (25MB), Upstash free (256MB), Railway ($5 credit) |
| **$5-10** | Render $7/month (256MB), Redis Cloud $5/month (100MB) |
| **$10-50** | Render $15/month (1GB), DigitalOcean $15/month, Upstash usage |
| **$50-200** | Redis Cloud, AWS ElastiCache, self-hosted |
| **$200+** | Self-hosted (dedicated), Redis Cloud enterprise |

---

## Common Gotchas

### **Gotcha 1: Free Tier Limits (Storage)**
- Render: 25MB (enough for ~50K sessions)
- Upstash: 256MB (enough for ~500K sessions)
- Redis Cloud: 30MB (tight for anything beyond toy apps)

**Watch for**: Eviction policies when memory full

---

### **Gotcha 2: Connection Limits**
- Free tiers: 10-30 concurrent connections
- **Problem**: Web apps with connection pooling can hit limits
- **Solution**: Use connection pooling efficiently or upgrade

---

### **Gotcha 3: Persistence vs Ephemeral**
- Some services (Render free) may not persist data
- **Problem**: Redis restarts = data loss
- **Solution**: Check persistence guarantees or use Redis as cache only

---

### **Gotcha 4: Data Transfer Costs**
- AWS ElastiCache: Data transfer OUT charged separately
- **Problem**: High read volume = high bills
- **Solution**: Use VPC peering (free data transfer) or consider alternatives

---

### **Gotcha 5: Redis Version Support**
- Some managed services lag behind latest Redis (7.x)
- **Problem**: Missing features (SEARCH, JSON module)
- **Solution**: Check version compatibility before choosing

---

## Next Steps for Deep Dive (S2)

1. **Benchmark performance**: Latency tests across providers
2. **Pricing calculators**: Real-world cost models (100MB, 1GB, 10GB scenarios)
3. **Feature comparison**: Redis modules, persistence, replication
4. **Migration complexity**: How easy to switch between providers?
5. **Operational requirements**: Monitoring, alerting, backup strategies

---

## Research Questions

1. **Serverless economics**: When does pay-per-request beat fixed monthly?
2. **Global distribution**: How much does edge caching improve latency?
3. **Persistence trade-offs**: RDB vs AOF vs no persistence?
4. **Connection pooling**: Best practices to avoid hitting limits?
5. **Migration paths**: How portable is data between Redis providers?

---

**Status**: ✅ S1 Complete - Service landscape mapped
**Next Stage**: S2 Comprehensive Discovery (technical deep-dive)
**Confidence**: High - mature ecosystem with clear trade-offs
