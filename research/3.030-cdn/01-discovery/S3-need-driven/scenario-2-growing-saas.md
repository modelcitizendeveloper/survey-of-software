# S3 Scenario 2: Growing SaaS (1TB/month)

**Company Profile**: Series A SaaS, product-market fit achieved, scaling operations
**Traffic**: 1TB/month egress, 5-10M requests/month
**Budget**: $50-200/month for CDN
**Priority**: Balance cost and performance, real-time monitoring, room to scale

---

## Business Context

### Company Details
- **Stage**: Series A ($3-10M raised)
- **Team Size**: 10-30 engineers
- **Users**: 50,000-200,000 MAU (Monthly Active Users)
- **Revenue**: $100K-500K MRR ($1.2M-6M ARR)
- **Growth**: 10-20% MoM (predictable growth)

### Technical Environment
- **Stack**: React/Vue SPA + Node.js/Python API + PostgreSQL
- **Infrastructure**: AWS or GCP (multi-region deployment)
- **Static Assets**: Images, CSS, JS bundles (300-500GB/month)
- **API Traffic**: JSON responses (500-700GB/month)
- **Geographic Distribution**: 60% US, 25% Europe, 10% APAC, 5% other

---

## CDN Requirements

### Critical Requirements
1. **Real-time analytics** (24h delay unacceptable, need to monitor traffic in real-time)
2. **Fast cache purge** (<30 seconds, ideally <10 seconds for deployments)
3. **Predictable costs** (budget $50-200/month, need to forecast costs)
4. **DDoS protection** (protect against attacks, 99.9%+ uptime required)
5. **API caching** (cache GET requests, reduce origin load)
6. **SSL/TLS** (free certificates, wildcard SSL for subdomains)

### Nice-to-Have
- Edge compute (for A/B testing, feature flags, auth)
- Image optimization (automatic WebP/AVIF conversion)
- Multi-origin support (failover, blue-green deployments)
- Log streaming (send logs to Datadog, Splunk, S3)

### Non-Requirements
- Enterprise SLAs (99.95%+ uptime not critical yet)
- Lowest latency (<10ms p50 not required)
- Instant purge (<1 second not required)
- Advanced security (WAF nice-to-have, not critical)

---

## CDN Selection Analysis

### Option 1: Cloudflare Pro (Recommended)

**Pricing**: $20/month (unlimited bandwidth) + $5-20/month (add-ons)

**Pros**:
- ✅ **Unlimited bandwidth** (1TB, 10TB, 100TB = same $20/month)
- ✅ **Real-time analytics** (no 24h delay, instant visibility)
- ✅ **310+ PoPs** (excellent global coverage, 22ms p50 latency)
- ✅ **DDoS protection** (unlimited unmetered, all plans)
- ✅ **Free SSL** (Universal SSL + custom certificates)
- ✅ **Predictable costs** ($20/month flat, no bandwidth overages)

**Cons**:
- ⚠️ **30-second purge** (slowest among major CDNs, but adequate)
- ⚠️ **Add-ons cost extra** (Workers $5/month, Argo $5/month, Load Balancing $5/month)
- ⚠️ **No native webhooks** (need Workers for custom webhooks)

**Cost Breakdown**:
- **Base**: $20/month (Pro plan, unlimited bandwidth)
- **Optional Add-Ons**:
  - Workers: $5/month (10M requests, for edge compute)
  - Argo Smart Routing: $5/month + $0.10/GB (30% faster, $105/month for 1TB)
  - Load Balancing: $5/month (2 origins, failover)
  - Image Resizing: $10/month (automatic optimization)
- **Total**: $20-45/month (base + add-ons)

**TCO (5-year)**: $1,200 (base) to $2,700 (all add-ons)

**When to Choose**: Unpredictable traffic (could grow to 10TB/month), need unlimited bandwidth

---

### Option 2: BunnyCDN (Cost-Optimized)

**Pricing**: $50-100/month (1TB × $0.05-0.10/GB, region-dependent)

**Pros**:
- ✅ **Cheapest paid option** ($50-100/month for 1TB)
- ✅ **5-10 second purge** (6× faster than Cloudflare)
- ✅ **Real-time analytics** (included, no 24h delay)
- ✅ **Linear pricing** (predictable: 2TB = $100-200/month)
- ✅ **Simple setup** (straightforward dashboard, pull zones)

**Cons**:
- ⚠️ **Pay-per-GB** (traffic spike = higher costs, unpredictable)
- ⚠️ **Fewer PoPs** (123 vs 310+ Cloudflare, 28ms p50 latency)
- ⚠️ **Community SDKs only** (no official Python/Node.js SDKs)
- ⚠️ **No webhooks** (can't trigger workflows on purge/events)

**Cost Breakdown**:
- **Base**: $50-100/month (1TB bandwidth, region-dependent)
- **Optional Add-Ons**:
  - Optimizer (WAF + Edge Rules): $9.50/month
  - Log Engine (long-term logs): $10/month
  - Edge Scripts (edge compute): $10/month (beta)
- **Total**: $50-130/month (base + add-ons)

**TCO (5-year)**: $3,000-6,000 (base) to $7,800 (all add-ons)

**When to Choose**: Predictable traffic (1-5TB/month), need faster purge (5-10s), cost-conscious

---

### Option 3: AWS CloudFront

**Pricing**: $85/month (1TB × $0.085/GB) + additional AWS services

**Pros**:
- ✅ **Deep AWS integration** (S3 OAI, Lambda@Edge, CloudWatch)
- ✅ **450+ PoPs** (excellent global coverage)
- ✅ **Free SSL** (via ACM - AWS Certificate Manager)
- ✅ **Terraform AWS provider** (IaC-friendly, CloudFormation)
- ✅ **Volume discounts** (>10TB drops to $0.080/GB, >50TB to $0.060/GB)

**Cons**:
- ⚠️ **More expensive than BunnyCDN** ($85 vs $50-100/month)
- ⚠️ **AWS lock-in** (S3 origin, Lambda@Edge, harder to migrate)
- ⚠️ **Complex pricing** (bandwidth + requests + invalidations)
- ⚠️ **Slow purge** (10-60 seconds, variable)

**Cost Breakdown**:
- **Bandwidth**: $85/month (1TB × $0.085/GB)
- **Requests**: ~$0.50/month (5M requests × $0.0075 per 10K)
- **Invalidations**: $0.50/path (first 1,000 paths free/month)
- **Optional Add-Ons**:
  - Origin Shield: $10/month ($0.01 per 10K requests)
  - Lambda@Edge: $30-60/month (1M requests × $0.60 per million)
  - Shield Advanced (DDoS): $3,000/month (overkill)
- **Total**: $85-155/month (base + add-ons, without Shield Advanced)

**TCO (5-year)**: $5,100 (base) to $9,300 (with Lambda@Edge)

**When to Choose**: AWS-heavy workload (S3 origin, Lambda@Edge, CloudWatch), need AWS ecosystem

---

### Option 4: Fastly (Real-Time Requirements)

**Pricing**: $170-230/month (1TB × $0.12-0.18/GB) + $50 minimum

**Pros**:
- ✅ **<1 second purge** (instant purge, unique capability)
- ✅ **Real-time analytics** (included, all plans)
- ✅ **Real-time log streaming** (20+ destinations: Datadog, Splunk, S3, etc.)
- ✅ **VCL scripting** (custom cache logic, advanced routing)
- ✅ **Shopify's CDN** (proven at scale)

**Cons**:
- ⚠️ **2-5× more expensive** than BunnyCDN ($170-230 vs $50-100/month)
- ⚠️ **Fewer PoPs** (100+ vs 310+ Cloudflare)
- ⚠️ **$50 minimum** (expensive for low traffic months)

**Cost Breakdown**:
- **Base**: $170-230/month (1TB × $0.12-0.18/GB + $50 minimum)
- **Requests**: Included (no per-request charges)
- **Log Streaming**: Included (20+ destinations, real-time)
- **VCL Scripting**: Included (custom cache logic)
- **Total**: $170-230/month

**TCO (5-year)**: $10,200-13,800

**When to Choose**: Need <1s purge (real-time content updates, breaking news), worth 2-5× premium

---

## Recommended Architecture

### Phase 1: Initial Deployment (1TB/month)

**CDN Choice**: Cloudflare Pro ($20/month) OR BunnyCDN ($50-100/month)

**Recommendation**: Cloudflare Pro (unlimited bandwidth, predictable $20/month)

**Architecture**:
```
User → Cloudflare Pro (310+ PoPs) → Origin (AWS ALB/ELB)
                ↓
          Real-Time Analytics
          Cache: Static assets (CSS, JS, images)
          Cache: API GET requests (JSON responses)
```

**Setup**:
1. **Cloudflare Pro** ($20/month)
2. **Page Rules** (50 rules on Pro, up from 3 on Free)
   - Cache static assets: `*myapp.com/assets/*` (1 month TTL)
   - Cache API GET: `*api.myapp.com/v1/*` (5 minute TTL, cache by query string)
   - Bypass cache for auth: `*myapp.com/login` (no caching)
3. **SSL/TLS**: Full (Strict) mode (origin has valid SSL certificate)
4. **DDoS Protection**: Enabled by default (unlimited unmetered)

**Cost**: $20/month

---

### Phase 2: Add Edge Compute (A/B Testing, Feature Flags)

**Trigger**: Need A/B testing, feature flags, or edge auth (Months 6-12)

**Add-On**: Cloudflare Workers ($5/month)

**Architecture**:
```
User → Cloudflare Pro + Workers → Origin
                ↓
          Workers: A/B testing (split traffic)
          Workers: Feature flags (serve variants)
          Workers: Edge auth (validate JWT)
```

**Workers Use Cases**:
- **A/B testing**: Route 50% traffic to variant A, 50% to variant B
- **Feature flags**: Serve feature to 10% of users (beta testing)
- **Edge auth**: Validate JWT at edge (reduce origin load)
- **Geo-steering**: Serve different content by country

**Cost**: $20 (Pro) + $5 (Workers) = **$25/month**

---

### Phase 3: Optimize Performance (Argo Smart Routing)

**Trigger**: Need 30% latency reduction, traffic >5TB/month (Year 2+)

**Add-On**: Argo Smart Routing ($5/month + $0.10/GB)

**Architecture**:
```
User → Cloudflare Pro + Argo → Origin
                ↓
          Argo: Smart routing (30% faster)
          Argo: Tiered caching (origin shield)
```

**Argo Benefits**:
- **30% faster** (optimized routing, reduces latency)
- **Tiered caching** (origin shield, reduces origin load 35%)
- **Cost**: $5/month + $0.10/GB = $105/month (1TB), $505/month (5TB)

**When to Enable**: Traffic >5TB/month (Argo cost $505/month justified by improved UX)

**Cost**: $20 (Pro) + $5 (Workers) + $105 (Argo for 1TB) = **$130/month**

---

### Phase 4: Multi-Origin Failover

**Trigger**: Need 99.9%+ uptime, multi-region deployment (Year 2+)

**Add-On**: Cloudflare Load Balancing ($5/month for 2 origins)

**Architecture**:
```
User → Cloudflare Pro + Load Balancing
                ↓
          Primary Origin (US-East)
          Failover Origin (US-West)
          Health Checks (every 60s)
```

**Load Balancing Benefits**:
- **Automatic failover** (primary fails → switch to secondary)
- **Health checks** (monitor origin uptime, 60s intervals)
- **Geo-steering** (route US users to US origin, EU users to EU origin)

**Cost**: $20 (Pro) + $5 (Load Balancing) = **$25/month**

---

## Implementation Guide

### Step-by-Step: Cloudflare Pro Setup

#### 1. Upgrade to Cloudflare Pro
- Log in to Cloudflare dashboard
- Select your site (e.g., myapp.com)
- Click "Upgrade Plan"
- Select "Pro" ($20/month)
- Enter payment details, confirm

#### 2. Configure Real-Time Analytics
- Go to Analytics → Traffic
- Real-time analytics now available (was 24h delay on Free)
- Monitor bandwidth, requests, cache hit rate in real-time

#### 3. Increase Page Rules (3 → 50)
- Go to Rules → Page Rules
- Free tier: 3 rules → Pro tier: 50 rules
- Create rules:
  - `*myapp.com/assets/*` → Cache Level: Cache Everything, Edge TTL: 1 month
  - `*api.myapp.com/v1/users/*` → Cache Level: Cache Everything, Edge TTL: 5 minutes
  - `*myapp.com/login` → Cache Level: Bypass

#### 4. Enable WAF (Optional, $20/month extra)
- Go to Security → WAF
- Enable "Managed Rules" ($20/month on Pro)
- Select rulesets: OWASP Core Ruleset, Cloudflare Managed Ruleset
- Set action: Block (default) or Challenge (CAPTCHA)

**Note**: WAF costs $20/month extra (total $40/month), recommended if experiencing attacks

#### 5. Configure API Caching
```javascript
// Example: Cache API GET requests for 5 minutes
Page Rule: *api.myapp.com/v1/*
  Cache Level: Cache Everything
  Edge Cache TTL: 5 minutes
  Cache Key: Custom (include query string)
  Origin Cache Control: On (respect origin Cache-Control headers)
```

#### 6. Test Caching
```bash
# Test static asset caching
curl -I https://myapp.com/assets/logo.png
# cf-cache-status: HIT (cached) or MISS (not cached)

# Test API caching
curl -I https://api.myapp.com/v1/users/123
# cf-cache-status: HIT (cached) or MISS (not cached)
```

#### 7. Purge Cache (On Deployment)
```bash
# Purge all cache (30 seconds to propagate)
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache" \
  -H "Authorization: Bearer {api_token}" \
  -H "Content-Type: application/json" \
  -d '{"purge_everything":true}'

# Purge specific URLs (30 seconds to propagate)
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache" \
  -H "Authorization: Bearer {api_token}" \
  -H "Content-Type: application/json" \
  -d '{"files":["https://myapp.com/assets/app.js", "https://myapp.com/assets/app.css"]}'
```

**Setup Time**: 2-3 hours (upgrade, configure Page Rules, test caching)

---

### Alternative Setup: BunnyCDN (Cost-Optimized)

#### 1. Create Pull Zone
- Log in to BunnyCDN dashboard
- Go to CDN → Pull Zones
- Click "Add Pull Zone"
- Name: `myapp`
- Origin URL: `https://origin.myapp.com`
- Regions: All regions (global coverage)

#### 2. Configure DNS (CNAME)
- BunnyCDN provides CDN URL: `myapp.b-cdn.net`
- Create CNAME record: `cdn.myapp.com` → `myapp.b-cdn.net`
- OR use custom hostname (requires SSL certificate upload)

#### 3. Enable SSL (Free Let's Encrypt)
- Go to Pull Zone → Security
- Enable "Force SSL" (redirects HTTP → HTTPS)
- Use "Free SSL" (Let's Encrypt, auto-renewal)

#### 4. Configure Caching (Static Assets)
- Go to Pull Zone → Caching
- Cache Expiry: 1 day (static assets), 1 hour (API)
- Query String Caching: Enabled (cache by query string)
- Vary Caching: Enabled (cache by Accept-Encoding, etc.)

#### 5. Configure Perma-Cache (Optional, $9.50/month)
```
Perma-Cache Benefits:
- Extended cache TTL (serve stale content while revalidating)
- Edge rules (custom cache logic)
- WAF (basic web application firewall)
- Cost: $9.50/month
```

#### 6. Purge Cache (On Deployment)
```bash
# Purge all cache (5-10 seconds to propagate)
curl -X POST "https://api.bunny.net/pullzone/{pull_zone_id}/purgeCache" \
  -H "AccessKey: {api_key}"

# Purge specific URLs (5-10 seconds)
curl -X POST "https://api.bunny.net/purge" \
  -H "AccessKey: {api_key}" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://cdn.myapp.com/assets/app.js"}'
```

**Setup Time**: 1-2 hours

---

## Cost Breakdown & TCO

### Scenario: Steady Growth (1TB → 5TB/month over 5 years)

| Year | Traffic/Month | Cloudflare Pro | BunnyCDN | AWS CloudFront | Fastly |
|------|---------------|----------------|----------|----------------|--------|
| **Year 1** | 1TB | $240 ($20/mo) | $600-1,200 ($50-100/mo) | $1,020 ($85/mo) | $2,040-2,760 ($170-230/mo) |
| **Year 2** | 2TB | $240 | $1,200-2,400 | $2,040 | $4,080-5,520 |
| **Year 3** | 3TB | $240 | $1,800-3,600 | $3,060 | $6,120-8,280 |
| **Year 4** | 4TB | $240 | $2,400-4,800 | $4,080 | $8,160-11,040 |
| **Year 5** | 5TB | $240 | $3,000-6,000 | $5,100 | $10,200-13,800 |
| **Total (5-year)** | | **$1,200** | **$9,000-18,000** | **$15,300** | **$30,600-41,400** |

**Winner**: Cloudflare Pro ($1,200 over 5 years, unlimited bandwidth!)

**When to Choose BunnyCDN**: If traffic stays <1TB/month (BunnyCDN $600-1,200/year cheaper than Cloudflare Pro $240/year? No!)

**Insight**: Cloudflare Pro is cheaper than BunnyCDN even at 1TB/month ($20 vs $50-100/month)

---

### Scenario: With Add-Ons (Workers, Argo, Load Balancing)

| Year | Traffic/Month | Cloudflare Pro + All Add-Ons | BunnyCDN + All Add-Ons |
|------|---------------|------------------------------|------------------------|
| **Year 1** | 1TB | $1,560 ($20 Pro + $5 Workers + $105 Argo + $5 LB) | $1,458 ($50-100 base + $9.50 Optimizer + $10 Edge Scripts) |
| **Year 2** | 2TB | $1,800 ($20 + $5 + $205 Argo + $5) | $2,034 ($100-200 base + $19.50 add-ons) |
| **Year 3** | 3TB | $2,040 ($20 + $5 + $305 Argo + $5) | $2,610 |
| **Year 4** | 4TB | $2,280 ($20 + $5 + $405 Argo + $5) | $3,186 |
| **Year 5** | 5TB | $2,520 ($20 + $5 + $505 Argo + $5) | $3,762 |
| **Total (5-year)** | | **$10,200** | **$13,050** |

**Winner**: Cloudflare Pro + Add-Ons ($10,200 vs $13,050 for BunnyCDN)

**Insight**: Argo cost ($0.10/GB) makes Cloudflare more expensive at >5TB/month, but still competitive

---

## Migration Strategy

### Migrating from Cloudflare Free → Cloudflare Pro

**Trigger**: Need real-time analytics, WAF, or 50 Page Rules (up from 3)

**Migration Steps**:
1. Click "Upgrade Plan" in Cloudflare dashboard
2. Select "Pro" ($20/month)
3. Enter payment details
4. Instant upgrade (no downtime)

**Migration Time**: 5 minutes

---

### Migrating from Cloudflare Pro → BunnyCDN

**Trigger**: Traffic stays <1TB/month, want to save $20/month (but lose unlimited bandwidth safety net)

**Migration Steps**:
1. Set up BunnyCDN Pull Zone (origin: current site)
2. Test caching (verify cache headers, purge works)
3. Update DNS CNAME: `cdn.myapp.com` → `myapp.b-cdn.net`
4. Monitor traffic (watch for errors, latency increases)
5. Decommission Cloudflare after 30 days

**Migration Time**: 1-2 days (DNS propagation)

**Risk**: Moderate (lose unlimited bandwidth safety net, traffic spike = higher costs)

---

## Key Recommendations

### Recommended Choice: Cloudflare Pro ($20/month)

**Why**:
- ✅ **Unlimited bandwidth** (1TB, 10TB, 100TB = same $20/month)
- ✅ **Predictable costs** (no bandwidth overages, budget certainty)
- ✅ **Real-time analytics** (no 24h delay, instant visibility)
- ✅ **Room to scale** (if traffic grows to 10TB/month, still $20/month!)
- ✅ **DDoS protection** (unlimited, protect against attacks)

**Trade-Offs**:
- ⚠️ 30-second purge (slower than BunnyCDN 5-10s, but adequate for most deployments)
- ⚠️ Add-ons cost extra (Workers $5/month, Argo $5/month + $0.10/GB)

**Total Cost**: $20/month (base) to $130/month (all add-ons: Workers + Argo for 1TB + Load Balancing)

**5-Year TCO**: $1,200 (base) to $7,800 (all add-ons)

---

### When to Choose BunnyCDN Instead

**Trigger**: Traffic predictable at <1TB/month, need faster purge (5-10s), cost-conscious

**Why**:
- ✅ **Cheaper at <500GB/month** ($25-50 vs Cloudflare Pro $20/month? No, Cloudflare still cheaper!)
- ✅ **5-10 second purge** (6× faster than Cloudflare 30s)
- ✅ **Real-time analytics** (included, no extra cost)

**Trade-Off**: Pay-per-GB pricing (traffic spike = higher costs, less predictable than Cloudflare unlimited)

**When to Choose**: If traffic GUARANTEED <1TB/month AND need 5-10s purge (vs Cloudflare 30s)

**Recommendation**: Stick with Cloudflare Pro (unlimited bandwidth safety net worth $20/month)

---

### When to Choose AWS CloudFront Instead

**Trigger**: AWS-heavy workload (S3 origin, Lambda@Edge, CloudWatch)

**Why**:
- ✅ **Deep AWS integration** (S3 OAI, Lambda@Edge, CloudWatch, Terraform AWS provider)
- ✅ **450+ PoPs** (excellent global coverage)
- ✅ **Volume discounts** (>10TB drops to $0.080/GB, >50TB to $0.060/GB)

**Trade-Off**: More expensive than Cloudflare Pro ($85/month vs $20/month for 1TB)

**When to Choose**: Already using AWS (S3 origin, Lambda, CloudWatch), AWS lock-in acceptable

**Cost Premium**: $65/month ($85 vs $20 Cloudflare) = $780/year = $3,900 over 5 years

**Recommendation**: Only if AWS ecosystem integration critical (S3 OAI, Lambda@Edge)

---

### When to Choose Fastly Instead

**Trigger**: Need <1s purge (real-time content updates, breaking news, stock tickers)

**Why**:
- ✅ **<1 second purge** (instant purge, unique capability)
- ✅ **Real-time log streaming** (20+ destinations, included)
- ✅ **VCL scripting** (custom cache logic, advanced routing)

**Trade-Off**: 2-8× more expensive ($170-230/month vs $20/month Cloudflare)

**Cost Premium**: $150-210/month = $1,800-2,520/year = $9,000-12,600 over 5 years

**Recommendation**: Only if <1s purge is business-critical (breaking news, live sports, real-time apps)

---

## Success Metrics

### 12-Month Check-In

**Metrics to Track**:
- **Bandwidth usage**: Did we stay within budget? (Cloudflare $20/month unlimited = predictable)
- **Cache hit rate**: >90% for static assets, >70% for API GET? (efficient caching)
- **Latency**: p95 TTFB <150ms? (global users)
- **Costs**: $20-130/month? (budget constraint)
- **Incidents**: 0 DDoS-related downtime? (Cloudflare DDoS protection working?)

**Success Criteria**:
- ✅ Bandwidth 1-5TB/month (within budget on Cloudflare Pro $20/month)
- ✅ Cache hit rate >90% (static) + >70% (API)
- ✅ No DDoS incidents (Cloudflare protection working)
- ✅ Real-time analytics enabled (24h delay eliminated)

**Failure Criteria** (triggers migration):
- ❌ Need <1s purge (30s too slow for product) → migrate to Fastly ($170-230/month)
- ❌ Need instant logs (Cloudflare Logpush $5/month not sufficient) → migrate to Fastly (real-time logs included)
- ❌ Traffic >10TB/month + need enterprise SLAs → upgrade to Cloudflare Business ($200/month) or Akamai

---

**Last Updated**: November 12, 2025
**Next Scenario**: E-Commerce (Price Updates, 5TB/month)
