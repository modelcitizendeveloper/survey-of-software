# BaaS Pricing Matrix

## Comprehensive Cost Comparison Across Scales

**Date:** October 10, 2025
**Providers:** Supabase, Firebase, PocketBase, Appwrite, Xata, Nhost

---

## Pricing at Three Scales

### Scale 1: Hobby Project (1K Monthly Active Users)

**Assumptions:**
- 1,000 monthly active users (MAU)
- 1GB database storage
- 10GB monthly bandwidth
- 100K database reads/month
- 10K database writes/month
- 1GB file storage
- 10K function invocations/month

| Provider | Monthly Cost | Free Tier Sufficient? | Notes |
|----------|--------------|------------------------|-------|
| **Supabase** | $0 | ✅ Yes | 500MB DB, 1GB storage, 2GB bandwidth included |
| **Firebase** | $0 | ✅ Yes | 1GB Firestore, 50K reads/day (~1.5M/month) included |
| **PocketBase** | $5-12 | N/A (self-host) | VPS cost only ($5 Hetzner, $12 DigitalOcean) |
| **Appwrite** | $0 | ✅ Yes (self-host) | Self-host free, Cloud $0 tier covers 1K MAU |
| **Xata** | $0 | ✅ Yes | 15GB DB storage (most generous free tier) |
| **Nhost** | $0 | ✅ Yes | 1GB DB, 3GB bandwidth, 10K MAU included |

**Winner at Hobby Scale:** Xata (15GB free) or Firebase/Supabase (comprehensive free tiers)

---

### Scale 2: Growth Stage (10K Monthly Active Users)

**Assumptions:**
- 10,000 monthly active users
- 10GB database storage
- 100GB monthly bandwidth
- 10M database reads/month
- 1M database writes/month
- 10GB file storage
- 500K function invocations/month

| Provider | Monthly Cost | Breakdown | Notes |
|----------|--------------|-----------|-------|
| **Supabase** | $25-50 | Pro plan $25 + overages ~$10-25 | 8GB DB included, $0.125/GB additional, $0.09/GB bandwidth |
| **Firebase** | $60-120 | Blaze pay-as-you-go | 10M reads ($6), 1M writes ($18), 10GB storage ($1.80), 100GB bandwidth ($12-24), Auth free |
| **PocketBase** | $12-24 | VPS only | $12 DigitalOcean droplet or $24 higher-tier VPS |
| **Appwrite** | $15-30 | Cloud Pro plan or self-host | Cloud $15/mo, self-host $12-24 VPS |
| **Xata** | $5-15 | Usage-based | 10GB storage ($5), 100GB bandwidth ($12), no read/write charges |
| **Nhost** | $25-50 | Pro plan + overages | Similar to Supabase pricing model |

**Winner at Growth Scale:** PocketBase ($12-24 self-hosted) or Xata ($5-15 usage-based)

---

### Scale 3: Production Scale (100K Monthly Active Users)

**Assumptions:**
- 100,000 monthly active users
- 100GB database storage
- 1TB (1,000GB) monthly bandwidth
- 1B (1,000M) database reads/month
- 100M database writes/month
- 100GB file storage
- 5M function invocations/month

| Provider | Monthly Cost | Breakdown | Notes |
|----------|--------------|-----------|-------|
| **Supabase** | $200-400 | Pro $25 + massive overages | 92GB extra DB ($11.50), 900GB+ bandwidth ($81+), functions ($6), storage ($2), scales poorly |
| **Firebase** | $600-1,200 | Blaze costs explode | 1B reads ($600), 100M writes ($180), 100GB storage ($18), 1TB bandwidth ($120-240) |
| **PocketBase** | $50-100 | VPS + optimization | Requires load balancing, multiple instances, or vertical scaling to higher-tier VPS |
| **Appwrite** | $100-300 | Self-host infrastructure | Kubernetes cluster, load balancers, backups, monitoring ($100-300/mo) |
| **Xata** | $50-150 | Usage-based | 100GB storage ($50), 1TB bandwidth ($120), no per-request charges helps |
| **Nhost** | $200-400 | Similar to Supabase | Pro plan + overages for storage, bandwidth, MAU |

**Winner at Production Scale:** Self-hosted (PocketBase, Appwrite) or Xata (no per-request charges)

**Insight:** Managed BaaS (Supabase, Firebase) costs explode at scale due to per-read/write and bandwidth pricing. Self-hosting wins at >$500/month spend.

---

## Cost Breakdown by Component

### Database Storage Costs

| Provider | Free Tier | Paid Pricing | Notes |
|----------|-----------|--------------|-------|
| **Supabase** | 500MB | $0.125/GB/month ($1.25 per 10GB) | Reasonable |
| **Firebase** | 1GB | $0.18/GB/month ($1.80 per 10GB) | Higher than Supabase |
| **PocketBase** | Unlimited | VPS storage (~$0.05/GB in VPS cost) | Cheapest (self-host) |
| **Appwrite** | Unlimited (self-host) | Cloud pricing TBD | Self-host cheapest |
| **Xata** | 15GB | $0.50/GB/month ($5 per 10GB) | Most expensive, but includes search |
| **Nhost** | 1GB | $0.20/GB/month ($2 per 10GB) | Middle ground |

**Cheapest:** PocketBase, Appwrite (self-host)
**Best Managed:** Supabase ($0.125/GB)

---

### Bandwidth Costs

| Provider | Free Tier | Paid Pricing | Notes |
|----------|-----------|--------------|-------|
| **Supabase** | 2GB | $0.09/GB ($90 per 1TB) | Reasonable |
| **Firebase** | 10GB | $0.12/GB ($120 per 1TB) | Higher |
| **PocketBase** | Unlimited | VPS bandwidth (~$0.01-0.05/GB) | Cheapest (self-host) |
| **Appwrite** | Unlimited (self-host) | Cloud: $0.10/GB | Self-host cheapest |
| **Xata** | N/A | $0.12/GB ($120 per 1TB) | Similar to Firebase |
| **Nhost** | 3GB | ~$0.10/GB | Similar to Supabase |

**Insight:** Bandwidth is major cost driver at scale (1TB = $90-120/month). Self-hosting with cheap VPS bandwidth wins at high traffic.

---

### Database Operations Costs (Reads/Writes)

| Provider | Pricing Model | Cost per 1M Reads | Cost per 1M Writes |
|----------|---------------|-------------------|---------------------|
| **Supabase** | No per-operation charges | $0 | $0 |
| **Firebase** | Pay per operation | $0.60 | $1.80 |
| **PocketBase** | No per-operation charges | $0 | $0 |
| **Appwrite** | No per-operation charges | $0 | $0 |
| **Xata** | No per-operation charges | $0 | $0 |
| **Nhost** | No per-operation charges | $0 | $0 |

**CRITICAL INSIGHT:** Firebase is the ONLY BaaS with per-read/write charges. This makes Firebase expensive at scale:
- 100M reads/month = $60
- 1B reads/month = $600
- Inefficient queries = massive costs

**Recommendation:** Avoid Firebase for read-heavy apps or apps with unpredictable query patterns.

---

### Authentication Costs

| Provider | Free Tier | Paid Pricing | Notes |
|----------|-----------|--------------|-------|
| **Supabase** | 50K MAU | $0.00325/MAU after 100K | Very affordable |
| **Firebase** | 50K MAU | Free for email/social, SMS $0.01-0.34/verification | SMS expensive |
| **PocketBase** | Unlimited | $0 (self-host) | Included |
| **Appwrite** | Unlimited (self-host) | Cloud: 75K MAU free | Generous |
| **Xata** | N/A | Bring-your-own-auth (Auth0, Clerk) | External cost |
| **Nhost** | 10K MAU | $0.00325/MAU (similar to Supabase) | Affordable |

**Cheapest:** PocketBase, Appwrite (self-host)
**Best Managed:** Supabase, Nhost ($0.00325/MAU)

---

### Serverless Functions Costs

| Provider | Free Tier | Paid Pricing | Notes |
|----------|-----------|--------------|-------|
| **Supabase** | 500K invocations | $2 per 1M invocations | Very affordable |
| **Firebase** | 2M invocations | $0.40 per 1M invocations | Cheapest per-invocation |
| **PocketBase** | N/A | Extensible via Go code (no serverless) | Not applicable |
| **Appwrite** | 750K invocations | Cloud: $0.50 per 1M | Affordable |
| **Xata** | N/A | No built-in functions | Use external (Vercel, Cloudflare) |
| **Nhost** | Included | Usage-based (similar to Supabase) | Affordable |

**Insight:** Serverless function pricing is consistent across BaaS ($0.40-$2 per 1M). Not a major cost driver unless >10M invocations/month.

---

## Cost Inflection Points

### When Does Free Tier End?

| Provider | Free Tier Limit | First Paid Tier Cost | Trigger |
|----------|-----------------|----------------------|---------|
| **Supabase** | 500MB DB, 2GB bandwidth, 50K MAU | $25/month (Pro) | Exceed any limit, or need backups/support |
| **Firebase** | 1GB Firestore, 50K reads/day | $0+ (Blaze pay-as-you-go) | Exceed daily read/write limits |
| **PocketBase** | N/A | $5-12/month (VPS) | Self-host only, no free cloud option |
| **Appwrite** | Unlimited (self-host) | $15/month (Cloud Pro) | Want managed cloud instead of self-host |
| **Xata** | 15GB DB | $0+ (usage-based) | Exceed 15GB storage or bandwidth |
| **Nhost** | 1GB DB, 10K MAU | $25/month (Pro) | Exceed any limit, or need backups/support |

---

### When Does Cost Explode? (Break-Even Analysis)

**Supabase:**
- Sweet spot: $0-500/month (0-50K users)
- Expensive: $500-2K/month (50K-200K users)
- Break-even: $1K/month (self-host PostgreSQL cheaper)

**Firebase:**
- Sweet spot: $0-100/month (0-10K users)
- Expensive: $100-1K/month (10K-100K users, read/write charges add up)
- Break-even: $500/month (self-host PostgreSQL + custom auth cheaper)

**PocketBase:**
- Always cheap: $5-100/month (0-100K users, VPS cost only)
- Hits scaling limit: ~10K concurrent users (SQLite bottleneck)
- Break-even: Never (cheapest option until SQLite limits hit)

**Appwrite:**
- Self-host: $12-300/month (VPS → Kubernetes cluster)
- Cloud: $15-300/month (managed service)
- Break-even: ~$300/month (comparable to Supabase at scale)

---

## Cost Optimization Strategies

### Strategy 1: Start Free, Migrate When Expensive
1. Launch on Supabase free tier (0-1K users)
2. Upgrade to Supabase Pro (1K-10K users, $25-100/month)
3. Migrate to PocketBase self-hosted when cost >$200/month
4. Migrate to self-hosted PostgreSQL when cost >$500/month

### Strategy 2: Self-Host from Day One
1. Deploy PocketBase on $5 VPS (0-5K users)
2. Upgrade VPS to $24/month (5K-20K users)
3. Migrate to PostgreSQL + Docker when SQLite limits hit
4. Scale PostgreSQL horizontally (read replicas, sharding)

**Trade-off:** Strategy 1 = faster launch but higher lock-in. Strategy 2 = more DevOps but lower cost and lock-in.

---

## Hidden Costs

### Supabase Hidden Costs:
- **Bandwidth overages:** $0.09/GB (1TB = $90/month extra)
- **Point-in-Time Recovery (PITR):** $100/month (enterprise feature)
- **Compute upgrades:** Separate charges for higher CPU/RAM instances

### Firebase Hidden Costs:
- **Phone auth SMS:** $0.01-0.34 per verification (10K verifications = $100-3,400/month)
- **Identity Platform (SAML/OIDC):** $0.015/MAU after 50 users (10K users = $150/month)
- **Inefficient queries:** Reading entire collections instead of indexed queries (massive read charges)

### PocketBase Hidden Costs:
- **DevOps time:** 5-10 hours/month for backups, monitoring, updates
- **Learning curve:** 10-20 hours upfront to learn Go extensibility
- **Scaling complexity:** Need to rebuild with PostgreSQL when SQLite limits hit

### Appwrite Hidden Costs:
- **Self-hosting infrastructure:** Load balancers, monitoring, backups ($50-200/month)
- **DevOps time:** 10-20 hours/month for maintenance
- **Migration to SQL:** If need to migrate from NoSQL to PostgreSQL later (80-120 hours)

---

## Final Recommendations by Budget

### Budget: $0/month
**Winner:** Xata (15GB free) or Supabase (500MB free, comprehensive features)
**Use case:** MVP testing, portfolio projects, low-traffic apps

### Budget: $10-50/month
**Winner:** PocketBase ($12 VPS) or Supabase Pro ($25/month)
**Use case:** Indie projects, small SaaS (1K-5K users)

### Budget: $50-200/month
**Winner:** Supabase Pro ($25-100/month with overages) or Appwrite self-hosted ($50-100 infra)
**Use case:** Growing startups (5K-20K users)

### Budget: $200-500/month
**Winner:** Self-hosted PostgreSQL (Render, Railway) or Appwrite Kubernetes
**Use case:** Scaling startups (20K-100K users), BaaS costs too high

### Budget: $500-2,000/month
**Winner:** Self-hosted PostgreSQL on dedicated infrastructure (AWS RDS, DigitalOcean Managed DB)
**Use case:** Established products (100K-1M users), full control needed

---

## Summary Insights

1. **Firebase is expensive at scale** due to per-read/write pricing ($600/month for 1B reads)
2. **Supabase is affordable until $200-500/month**, then self-hosting cheaper
3. **PocketBase is cheapest** ($5-50/month) but hits SQLite scaling limits (~10K concurrent users)
4. **Appwrite self-hosted** is cost-effective but requires DevOps expertise
5. **Xata has best free tier** (15GB) and no per-request charges (good for read-heavy apps)

**General Rule:** Managed BaaS optimal for $0-500/month spend. Self-hosting wins at >$500/month.
