# S3: Need-Driven Discovery - Redis Hosting Use Case Patterns

**Experiment**: 2.033 - Redis Hosting Services
**Stage**: S3 - Need-Driven Discovery (Generic Use Case Patterns)
**Date**: 2025-10-10
**Methodology**: MPSE Stage 3 - Generic problem patterns with parameters, NOT application-specific

---

## Table of Contents
1. [Use Case Pattern Taxonomy](#use-case-pattern-taxonomy)
2. [Pattern Catalog by Scale](#pattern-catalog-by-scale)
3. [Pattern Catalog by Context](#pattern-catalog-by-context)
4. [Decision Framework](#decision-framework)
5. [Migration Patterns](#migration-patterns)

---

## Use Case Pattern Taxonomy

### Classification Dimensions

1. **Scale Profile**
   - Hobby: <100 users, <10K requests/day
   - Early Stage: 100-1K users, 10K-100K requests/day
   - Growth: 1K-10K users, 100K-1M requests/day
   - Scale: >10K users, >1M requests/day

2. **Traffic Pattern**
   - Steady: Predictable, consistent load
   - Spiky: Variable, unpredictable peaks
   - Seasonal: Predictable peaks (holidays, business hours)
   - Bursty: Extreme short-term spikes (viral events)

3. **Data Persistence Requirement**
   - Ephemeral: Cache only, data loss acceptable
   - Semi-persistent: Important but recoverable (session storage)
   - Critical: Must persist (job queue, user data)
   - Archive: Long-term retention (analytics, audit logs)

4. **Geographic Distribution**
   - Single Region: All users in one geography
   - Multi-Region: Users across continents
   - Edge: Global with edge caching needs
   - Distributed: Multi-datacenter for compliance/resilience

5. **Team Context**
   - Solo Founder: Limited time, maximize productivity
   - Small Team (2-5): Focus on product, minimal ops
   - Growth Team (5-20): Dedicated ops possible, but expensive
   - Enterprise (>20): Dedicated infrastructure team

---

## Pattern Catalog by Scale

### Pattern 1: Hobby/MVP - Session Storage

#### **Problem Definition**
Store user session data (auth tokens, shopping carts, temporary state) for small application.

#### **Parameters**
- **Users**: <100 concurrent
- **Memory**: 10-50MB
- **Request Rate**: <1K requests/day
- **Persistence**: Semi-persistent (session timeout acceptable)
- **Budget**: $0-10/month

#### **Provider Recommendations**

**Option 1: Render Free Tier** (25MB)
```yaml
# render.yaml
services:
  - type: web
    name: my-app
    env: python
    envVars:
      - key: REDIS_URL
        value: redis://localhost:6379  # Built-in free Redis
```

**Pros**:
- $0/month
- No credit card required
- Internal network (low latency)
- Zero configuration

**Cons**:
- 25MB limit (tight for >50 users)
- No persistence guarantees
- Single instance (no failover)

**When to upgrade**: >50 concurrent users OR need persistence

---

**Option 2: Upstash Free Tier** (256MB, 10K requests/day)
```python
import redis

r = redis.Redis(
    host='your-region.upstash.io',
    port=6379,
    password='your-token',
    ssl=True
)

# Session storage
r.setex(f"session:{user_id}", 3600, session_data)  # 1-hour TTL
```

**Pros**:
- Larger free tier (256MB)
- Global edge caching
- REST API option (serverless-friendly)
- Credit card required but no charges

**Cons**:
- Public internet (slightly higher latency)
- Request limit (10K/day)
- Younger company (less proven)

**When to upgrade**: >10K requests/day OR >256MB

---

#### **Implementation Pattern**

```python
from flask import Flask, session
from flask_session import Session
import redis

app = Flask(__name__)

# Session configuration
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=6379,
    password=os.getenv('REDIS_PASSWORD')
)
Session(app)

@app.route('/login', methods=['POST'])
def login():
    # Session automatically stored in Redis
    session['user_id'] = user.id
    session['username'] = user.username
    return redirect('/dashboard')
```

#### **Cost Projection**
- **Render free**: $0/month (sufficient for <50 users)
- **Upgrade trigger**: When you have 50+ concurrent users, upgrade to Render Starter ($7/month, 256MB)

---

### Pattern 2: Early Stage SaaS - API Rate Limiting

#### **Problem Definition**
Implement rate limiting to prevent API abuse and ensure fair usage across customers.

#### **Parameters**
- **Users**: 100-1,000 API customers
- **Memory**: 50-200MB (counter storage)
- **Request Rate**: 10K-100K requests/day
- **Persistence**: Ephemeral (counters reset acceptable)
- **Geographic**: Preferably global (edge caching)
- **Budget**: $0-20/month

#### **Provider Recommendations**

**Option 1: Upstash** (Edge Caching)
```python
import redis

# Upstash global edge caching
r = redis.Redis(
    host='global.upstash.io',
    port=6379,
    password='your-token',
    ssl=True
)

def check_rate_limit(api_key: str, limit: int = 1000) -> bool:
    """
    Check if API key is within rate limit.
    Uses sliding window algorithm.
    """
    key = f"ratelimit:{api_key}:{int(time.time() // 3600)}"  # Hourly window

    current = r.incr(key)

    if current == 1:
        r.expire(key, 3600)  # 1-hour expiry

    return current <= limit
```

**Why Upstash**:
- Global edge = low-latency rate limit checks
- Pay-per-request pricing (scales with usage)
- No connection pooling needed (REST API option)

**Cost**:
- Free tier: 10K requests/day (sufficient for early stage)
- Paid: $0.20 per 100K requests (~$6/month at 100K requests/day)

---

**Option 2: Render Starter** ($7/month, 256MB)
```python
# Same implementation, but Render-hosted Redis
r = redis.Redis.from_url(os.getenv('REDIS_URL'))

def check_rate_limit(api_key: str, limit: int = 1000) -> bool:
    # Same sliding window algorithm
    key = f"ratelimit:{api_key}:{int(time.time() // 3600)}"
    current = r.incr(key)
    if current == 1:
        r.expire(key, 3600)
    return current <= limit
```

**Why Render**:
- Fixed pricing (predictable cost)
- Internal network (if API is on Render)
- Simple setup

**Cost**: $7/month flat

---

#### **Advanced: Multi-Tier Rate Limiting**

```python
# Different limits per customer tier
RATE_LIMITS = {
    'free': 100,      # 100 requests/hour
    'starter': 1000,  # 1K requests/hour
    'pro': 10000,     # 10K requests/hour
    'enterprise': None  # Unlimited
}

def check_rate_limit(api_key: str, tier: str) -> bool:
    limit = RATE_LIMITS.get(tier)

    if limit is None:
        return True  # Enterprise = no limit

    key = f"ratelimit:{api_key}:{int(time.time() // 3600)}"
    current = r.incr(key)

    if current == 1:
        r.expire(key, 3600)

    if current > limit:
        # Log abuse attempt
        r.incr(f"ratelimit:violations:{api_key}")
        return False

    return True
```

#### **Cost Projection**
- **Early stage** (10K-100K req/day): Upstash free tier or Render $7/month
- **Upgrade trigger**: >100K requests/day → Consider Redis Cloud or scale Upstash

---

### Pattern 3: Growing SaaS - Background Job Queue (Celery/RQ)

#### **Problem Definition**
Process background tasks (emails, reports, data processing) asynchronously using Redis as message broker.

#### **Parameters**
- **Users**: 1,000-10,000
- **Memory**: 500MB-2GB (job queue + results)
- **Job Volume**: 10K-100K jobs/day
- **Persistence**: **CRITICAL** (job loss = user-facing failures)
- **Reliability**: High (need replication/backups)
- **Budget**: $15-50/month

#### **Provider Recommendations**

**Option 1: Render Standard** ($15/month, 1GB with replication)
```python
# Celery configuration
from celery import Celery

app = Celery('tasks', broker=os.getenv('REDIS_URL'))

app.conf.update(
    result_backend=os.getenv('REDIS_URL'),
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    # Persistence settings
    broker_transport_options={
        'visibility_timeout': 3600,  # 1 hour
        'fanout_prefix': True,
        'fanout_patterns': True,
    }
)

@app.task
def send_email(user_id, subject, body):
    # Long-running task
    email_service.send(user_id, subject, body)
```

**Why Render Standard**:
- Replication included (high availability)
- Daily backups
- Internal network (zero-latency task submission)
- Simple pricing

**Cost**: $15/month

---

**Option 2: Redis Cloud** ($25-50/month, 500MB-1GB)
```python
# Same Celery config, but Redis Cloud URL
app = Celery('tasks', broker=os.getenv('REDIS_CLOUD_URL'))

# Redis Cloud advantages
app.conf.update(
    # Enable persistence (RDB + AOF)
    broker_transport_options={
        'visibility_timeout': 3600,
    },
    # Result backend with longer retention
    result_expires=86400,  # 24 hours
)
```

**Why Redis Cloud**:
- Enterprise reliability (99.99% SLA)
- Advanced monitoring (slow queries, memory alerts)
- Point-in-time recovery
- Redis modules (if needed for complex workflows)

**Cost**: $25-50/month (depending on memory needs)

---

#### **Job Queue Patterns**

**Pattern A: Priority Queues**
```python
# High-priority tasks (user-facing)
@app.task(queue='high_priority')
def send_password_reset(user_id):
    # Must complete quickly
    pass

# Low-priority tasks (background)
@app.task(queue='low_priority')
def generate_monthly_report(org_id):
    # Can take hours
    pass
```

**Pattern B: Scheduled Tasks**
```python
from celery.schedules import crontab

app.conf.beat_schedule = {
    'send-daily-digest': {
        'task': 'tasks.send_daily_digest',
        'schedule': crontab(hour=8, minute=0),  # 8am daily
    },
}
```

**Pattern C: Retry Logic**
```python
@app.task(bind=True, max_retries=3)
def flaky_api_call(self, user_id):
    try:
        external_api.call(user_id)
    except APIException as exc:
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=60 * 2**self.request.retries)
```

#### **Cost Projection**
- **Growing** (10K-100K jobs/day): Render Standard $15/month or Redis Cloud $25/month
- **Upgrade trigger**: >100K jobs/day OR >1GB memory → Redis Cloud $50/month or self-hosted

---

### Pattern 4: Scale Application - Real-Time Analytics / Leaderboards

#### **Problem Definition**
Track real-time metrics (user activity, leaderboards, counters) with high write throughput.

#### **Parameters**
- **Users**: 10,000-100,000
- **Memory**: 5-20GB (counters, sorted sets, time-series data)
- **Write Rate**: 1M-10M writes/day
- **Read Rate**: 100K-1M reads/day
- **Persistence**: Semi-persistent (tolerate some data loss)
- **Budget**: $50-200/month

#### **Provider Recommendations**

**Option 1: Redis Cloud** (with RedisTimeSeries module)
```python
import redis
from redistimeseries.client import Client

rts = Client(
    host='redis-cloud-host',
    port=6379,
    password='password'
)

# Track page views over time
rts.create('pageviews:total', retention_msecs=86400000)  # 24-hour retention

def track_pageview(page_id: str):
    """Increment pageview counter"""
    timestamp = int(time.time() * 1000)
    rts.add('pageviews:total', timestamp, 1)
    rts.incrby(f'pageviews:{page_id}', timestamp, 1)

# Query pageviews in last hour
def get_pageviews_last_hour():
    end = int(time.time() * 1000)
    start = end - (3600 * 1000)  # 1 hour ago
    return rts.range('pageviews:total', start, end)
```

**Why Redis Cloud**:
- RedisTimeSeries module (optimized for time-series)
- High write throughput
- Advanced monitoring

**Cost**: $100-200/month (10GB with replication)

---

**Option 2: Self-Hosted Redis** on dedicated server
```python
# Same code, but self-hosted Redis with RedisTimeSeries module

# Deploy on Hetzner dedicated server
# - 64GB RAM
# - $40-60/month
# - Install Redis + RedisTimeSeries module
```

**Why Self-Hosted**:
- Cost optimization ($40/month vs $200/month managed)
- Full control (custom modules, configuration tuning)
- Dedicated resources

**Trade-off**: Requires Redis ops expertise (10-20 hours/month)

**Cost**: $40-60/month (server) + ops time

---

#### **Leaderboard Pattern**

```python
def update_leaderboard(user_id: str, score: int):
    """Update user score in leaderboard (sorted set)"""
    r.zadd('leaderboard:global', {user_id: score})

def get_top_players(count: int = 10):
    """Get top N players"""
    return r.zrevrange('leaderboard:global', 0, count - 1, withscores=True)

def get_user_rank(user_id: str):
    """Get user's rank (1-indexed)"""
    rank = r.zrevrank('leaderboard:global', user_id)
    return rank + 1 if rank is not None else None

# Time-boxed leaderboards (weekly, monthly)
def update_weekly_leaderboard(user_id: str, score: int):
    week = datetime.now().strftime('%Y-W%U')
    key = f'leaderboard:{week}'
    r.zadd(key, {user_id: score})
    r.expire(key, 604800)  # 7-day TTL
```

#### **Cost Projection**
- **Scale** (1M-10M events/day): Redis Cloud $100-200/month OR self-hosted $40-60/month
- **Break-even**: If ops time <5 hours/month, self-hosted cheaper

---

## Pattern Catalog by Context

### Context 1: Solo Founder Bootstrap

#### **Constraints**
- Time: <5 hours/month on infrastructure
- Budget: $0-20/month
- Expertise: Limited Redis ops knowledge
- Priority: Ship features, not infrastructure

#### **Decision Framework**

```
START: What's your hosting platform?

├─ Render
│   └─ Use Render Redis free tier (25MB) or Starter ($7/month)
│
├─ Vercel/Cloudflare Workers
│   └─ Use Upstash (serverless-friendly REST API)
│
├─ AWS/GCP/Azure
│   └─ Use platform-native Redis (but consider cost)
│
└─ Self-Hosted VPS
    └─ Install Redis on same VPS (saves $7-15/month)
        └─ Only if comfortable with Linux/Docker
```

**Recommended Stack**:
- **Hosting**: Render or Railway
- **Redis**: Render free tier → Render Starter ($7/month when needed)
- **Why**: Zero ops, focus on product

#### **Anti-Pattern**: Using AWS ElastiCache
- **Why avoid**: No free tier, complex pricing, requires VPC knowledge
- **Cost**: $12/month minimum (vs $0-7 for Render)

---

### Context 2: VC-Backed Startup (Post-Seed)

#### **Constraints**
- Team: 3-10 engineers
- Budget: $500-2K/month infrastructure
- Scale: 1K-10K users
- Priority: Growth > cost optimization

#### **Decision Framework**

**Phase 1: MVP → PMF** (0-1K users)
- **Redis**: Render Standard ($15/month) or Redis Cloud ($25/month)
- **Why**: Simple, reliable, scales easily
- **Upgrade trigger**: >10K users OR >$50/month Redis costs

**Phase 2: PMF → Scale** (1K-10K users)
- **Redis**: Redis Cloud ($50-200/month) OR hybrid (Render + Upstash)
- **Why**: Need reliability, monitoring, support
- **Upgrade trigger**: >$200/month Redis costs

**Phase 3: Scale** (>10K users)
- **Redis**: Consider self-hosted OR Redis Cloud enterprise
- **Why**: Margin optimization matters at scale
- **Break-even**: Self-hosted if >$500/month cloud costs

#### **Recommended Stack**:
- **Early**: Redis Cloud (reliability + support)
- **Growth**: Stay on Redis Cloud (focus on product)
- **Scale**: Evaluate self-hosted (if ops team exists)

---

### Context 3: Enterprise SaaS

#### **Constraints**
- Team: 20+ engineers, dedicated ops
- Budget: $5K-50K/month infrastructure
- Scale: 100K+ users
- Compliance: SOC2, HIPAA, PCI-DSS required
- Priority: Reliability, compliance, control

#### **Decision Framework**

**Option 1: AWS ElastiCache** (VPC-isolated)
```
Why:
✅ VPC isolation (compliance requirement)
✅ Deep AWS integration (IAM, CloudWatch)
✅ Enterprise SLAs
✅ Multi-AZ failover

Cost: $500-5K/month (depends on scale)
```

**Option 2: Redis Cloud Enterprise**
```
Why:
✅ Redis modules (JSON, Search, Graph)
✅ 99.99% SLA
✅ 24/7 support
✅ Compliance certifications (SOC2, HIPAA)

Cost: $1K-10K/month (depends on scale)
```

**Option 3: Self-Hosted Redis Cluster**
```
Why:
✅ Full control (custom modules, configuration)
✅ Cost optimization ($500/month for multi-TB cluster)
✅ Air-gapped deployment (compliance)

Trade-off: Requires 1-2 FTE ops engineers

Cost: $500/month (infrastructure) + $200K/year (2 engineers)
```

#### **Recommended Stack**:
- **Compliance-first**: AWS ElastiCache or Redis Cloud
- **Cost-optimized**: Self-hosted (if ops team exists)
- **Hybrid**: Redis Cloud for critical + self-hosted for non-critical

---

### Context 4: Serverless/Edge Applications

#### **Constraints**
- Architecture: Vercel, Cloudflare Workers, AWS Lambda
- Connection Model: Stateless (no persistent connections)
- Geographic: Global users (need edge caching)
- Budget: Pay-per-use preferred

#### **Decision Framework**

**Only viable option: Upstash**

```python
# Cloudflare Worker example
import { Redis } from '@upstash/redis'

const redis = new Redis({
  url: 'https://your-region.upstash.io',
  token: 'your-token'
})

export default {
  async fetch(request) {
    // Serverless-friendly (HTTP, no connection pooling)
    const value = await redis.get('key')
    return new Response(value)
  }
}
```

**Why Upstash is only choice**:
- REST API (no connection pooling needed)
- Edge caching (global read replicas)
- Pay-per-request (scales to zero)
- Serverless-native

**Alternative**: Cloudflare KV (not Redis, but similar use case)

#### **Cost Projection**:
- **Low traffic**: Free tier (10K req/day)
- **Medium traffic**: $10-50/month (100K-1M req/day)
- **High traffic**: $100+/month (>1M req/day)

---

## Decision Framework

### Step 1: Assess Your Context

Answer these questions:

1. **What is your team size?**
   - [ ] Solo founder / <3 engineers
   - [ ] Small team (3-10 engineers)
   - [ ] Growth team (10-50 engineers)
   - [ ] Enterprise (>50 engineers)

2. **What is your current scale?**
   - [ ] Hobby (<100 users)
   - [ ] Early stage (100-1K users)
   - [ ] Growing (1K-10K users)
   - [ ] Scale (>10K users)

3. **What is your hosting platform?**
   - [ ] Render / Railway / Heroku
   - [ ] Vercel / Cloudflare Workers (serverless)
   - [ ] AWS / GCP / Azure
   - [ ] Self-hosted VPS

4. **What is your budget?**
   - [ ] $0 (free tier only)
   - [ ] $0-20/month
   - [ ] $20-100/month
   - [ ] $100-500/month
   - [ ] >$500/month

5. **What is your Redis use case?**
   - [ ] Session storage (ephemeral)
   - [ ] API rate limiting (ephemeral)
   - [ ] Job queue (critical persistence)
   - [ ] Real-time analytics (high throughput)
   - [ ] Cache (eviction acceptable)
   - [ ] Pub/sub (connection stability)

---

### Step 2: Apply Decision Matrix

| Context | Scale | Budget | Recommendation |
|---------|-------|--------|----------------|
| **Solo founder, Render** | Hobby | $0 | Render free tier |
| **Solo founder, Render** | Early | $0-20 | Render Starter ($7/month) |
| **Solo founder, Vercel** | Any | $0-20 | Upstash (serverless) |
| **Startup, any platform** | Early | $20-100 | Redis Cloud or Render Standard |
| **Startup, growing** | Growth | $100-500 | Redis Cloud ($50-200/month) |
| **Enterprise, AWS** | Scale | $500+ | AWS ElastiCache |
| **Enterprise, multi-cloud** | Scale | $1K+ | Redis Cloud Enterprise |
| **High scale, ops team** | Scale | Cost-sensitive | Self-hosted |

---

### Step 3: Validate with Metrics

**Track these metrics to validate your choice**:

1. **Cost per 1K requests**: Should be <$0.01
2. **P99 latency**: Should be <10ms for same-region
3. **Uptime**: Should be >99.9%
4. **Ops time**: Should be <5 hours/month (for managed services)

**Upgrade triggers**:
- Monthly Redis cost >$200 → Consider self-hosted
- P99 latency >50ms → Consider regional provider or edge caching
- Downtime >1 hour/month → Upgrade to replicated tier
- Ops time >10 hours/month → Upgrade to better managed service

---

## Migration Patterns

### Pattern 1: Free Tier → Paid Tier (Same Provider)

**Scenario**: Outgrow Render free tier (25MB), upgrade to Starter (256MB)

**Process**:
1. Upgrade plan in dashboard (takes ~2 minutes)
2. Brief restart (data preserved if persistence enabled)
3. Update connection string if needed
4. Monitor for 24 hours

**Downtime**: <5 minutes

**Cost**: $0 → $7/month

---

### Pattern 2: Platform-Integrated → Dedicated (Render → Redis Cloud)

**Scenario**: Need Redis modules or better monitoring

**Process**:
1. Create Redis Cloud instance
2. Enable dual-write (write to both Render + Redis Cloud)
3. Backfill data (RDB export from Render)
4. Switch reads to Redis Cloud (with Render fallback)
5. Monitor for 48 hours
6. Remove Render Redis writes
7. Cancel Render Redis plan

**Downtime**: Zero (if done correctly)

**Cost**: $7/month (Render) → $25-50/month (Redis Cloud)

---

### Pattern 3: Managed → Self-Hosted (Cost Optimization)

**Scenario**: Redis Cloud costs >$200/month, have ops team

**Process**:
1. Provision dedicated server (Hetzner, DigitalOcean)
2. Install Redis + modules
3. Configure replication, backups, monitoring
4. Enable dual-write
5. Migrate traffic gradually (10% → 50% → 100%)
6. Cancel managed service

**Downtime**: Zero (if done correctly)

**Cost**: $200/month (Redis Cloud) → $40-60/month (self-hosted) + ops time

**Break-even**: If ops time <20 hours/month, self-hosted cheaper

---

### Pattern 4: Single-Region → Multi-Region (Global Expansion)

**Scenario**: Users in US + Europe, need low-latency globally

**Process**:
1. Keep primary Redis in US (write master)
2. Add read replica in Europe (Redis Cloud or Upstash)
3. Route reads to nearest region (DNS/load balancer)
4. Writes go to US (eventual consistency acceptable)

**Downtime**: Zero

**Cost**: 2× the cost of single-region

**Alternative**: Upstash (built-in global edge caching)

---

## Summary: Quick Reference Table

| Use Case | Hobby | Early Stage | Growth | Scale |
|----------|-------|-------------|--------|-------|
| **Session Storage** | Render free | Render $7 | Render $15 | Redis Cloud $50 |
| **API Rate Limit** | Upstash free | Upstash $6 | Upstash $20 | Upstash $50 or Redis Cloud |
| **Job Queue** | Render free | Render $15 | Redis Cloud $50 | Redis Cloud $200 or self-hosted |
| **Real-Time Analytics** | N/A | Redis Cloud $25 | Redis Cloud $100 | Self-hosted $40-60 |
| **Cache** | Render free | Upstash $6 | Upstash $20 | Upstash edge or self-hosted |
| **Pub/Sub** | Render free | Redis Cloud $25 | Redis Cloud $50 | AWS ElastiCache or Redis Cloud |

---

**Status**: ✅ S3 Complete - Generic use case patterns with decision frameworks
**Next Stage**: S4 Strategic Discovery (vendor viability, market trends)
