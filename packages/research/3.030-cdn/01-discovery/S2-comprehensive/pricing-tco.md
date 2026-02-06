# S2 Comprehensive: Pricing & TCO Analysis

**Bandwidth Scenarios**: 4 traffic levels (10GB, 100GB, 1TB, 10TB per month)
**Time Horizons**: 1-year, 3-year, 5-year TCO
**Providers Analyzed**: 6 CDN platforms
**Last Updated**: November 12, 2025

---

## Executive Summary

| Scenario | Traffic/Month | Cheapest Provider | Monthly Cost | Most Expensive | Cost Variance |
|----------|---------------|-------------------|--------------|----------------|---------------|
| **Small Site** | 10GB | Cloudflare Free | $0 | Fastly | $50 (minimum) | Infinite (free vs paid) |
| **Growing Site** | 100GB | BunnyCDN | $1-2 | Fastly | $80-100 | 40-100× |
| **Mid-Size** | 1TB | BunnyCDN | $5-10 | Fastly | $120-180 | 12-36× |
| **High-Traffic** | 10TB | BunnyCDN | $50-100 | Akamai | $500-2,000 | 5-40× |

**Key Insight**: Cost variance is 5-100× between cheapest (BunnyCDN, Cloudflare Free) and most expensive (Fastly, Akamai) providers.

---

## Scenario 1: Small Site (10GB/month egress)

**Use Case**: Personal blog, small business site, documentation site, portfolio

### Monthly Costs by Provider

| Provider | Plan | Monthly Cost | Bandwidth Cap | Features Unlocked | Notes |
|----------|------|--------------|---------------|-------------------|-------|
| **Cloudflare** | Free | **$0** | Unlimited | DDoS, SSL, 100 Page Rules, 24h analytics delay | **Best free tier** |
| **Cloudflare** | Pro | $20 | Unlimited | Real-time analytics, image resizing, WAF ($20 extra) | Overkill for 10GB |
| **BunnyCDN** | Pay-per-use | **$0.50-1** | Pay-per-GB ($0.05-0.10/GB) | All core features, no analytics delay | Cheapest paid option |
| **AWS CloudFront** | Free Tier (12mo) | **$0** (1st year) | 1TB (12 months) | Standard features, free SSL | Expires after 12 months |
| **AWS CloudFront** | Pay-per-use | $0.85 | Pay-per-GB ($0.085/GB) | Standard features | After free tier expires |
| **Fastly** | Starter | **$50** | Pay-per-GB (~$0.12/GB) | All features, real-time analytics | $50 minimum (high for 10GB) |
| **Akamai** | Enterprise | N/A | Negotiated | Enterprise features | Not cost-effective for <10GB |
| **Cloudinary** | Free | **$0** | 25GB bandwidth + 25GB storage | Media optimization, transformations | **Media-specific, adequate for small sites** |
| **Cloudinary** | Plus | $89 | 150GB bandwidth + 150GB storage | Advanced transformations, webhooks | Overkill for 10GB |

### 1-Year, 3-Year, 5-Year TCO (10GB/month)

| Provider | Plan | 1-Year TCO | 3-Year TCO | 5-Year TCO | Effective Monthly (5-year) |
|----------|------|------------|------------|------------|---------------------------|
| **Cloudflare** | Free | **$0** | **$0** | **$0** | **$0** |
| **Cloudinary** | Free | **$0** | **$0** | **$0** | **$0** (media only) |
| **AWS CloudFront** | Free Tier → Pay | $0 (1st yr) + $10.20 (2nd yr) | $20.40 | $40.80 | $0.68/month |
| **BunnyCDN** | Pay-per-use | $6-12 | $18-36 | $30-60 | $0.50-1/month |
| **Fastly** | Starter | $600 | $1,800 | $3,000 | $50/month |

**Winner**: Cloudflare Free ($0 TCO) or Cloudinary Free (media sites)

**Best Paid Option**: BunnyCDN ($30-60 over 5 years)

**Avoid**: Fastly ($3,000 over 5 years for 10GB = $50/month minimum is 100× more expensive than BunnyCDN)

---

## Scenario 2: Growing Site (100GB/month egress)

**Use Case**: SaaS startup, e-commerce site, news blog, API backend

### Monthly Costs by Provider

| Provider | Plan | Monthly Cost | Bandwidth Cost | Extra Fees | Total Monthly | Notes |
|----------|------|--------------|----------------|------------|---------------|-------|
| **Cloudflare** | Free | $0 | $0 (unlimited) | None | **$0** | Still free! 24h analytics delay |
| **Cloudflare** | Pro | $20 | $0 (unlimited) | None | **$20** | Real-time analytics, recommended tier |
| **BunnyCDN** | Pay-per-use | $0 | $5-10 (100GB × $0.05-0.10) | None | **$5-10** | Cheapest paid option |
| **AWS CloudFront** | Pay-per-use | $0 | $8.50 (100GB × $0.085) | None | **$8.50** | After free tier expires |
| **Fastly** | Starter | $50 | $12 (100GB × ~$0.12) | None | **$62** | $50 minimum + bandwidth |
| **Akamai** | Enterprise | N/A | Negotiated | N/A | **Est. $100-200** | Overkill for 100GB |
| **Cloudinary** | Plus | $89 | $0 (150GB included) | None | **$89** | Media-specific, 150GB included |

### 1-Year, 3-Year, 5-Year TCO (100GB/month)

| Provider | Plan | 1-Year TCO | 3-Year TCO | 5-Year TCO | Effective Monthly (5-year) | Notes |
|----------|------|------------|------------|------------|---------------------------|--------|
| **Cloudflare** | Free | **$0** | **$0** | **$0** | **$0** | 24h analytics delay, unlimited bandwidth |
| **BunnyCDN** | Pay-per-use | $60-120 | $180-360 | $300-600 | $5-10/month | Cheapest paid option |
| **Cloudflare** | Pro | $240 | $720 | $1,200 | $20/month | Real-time analytics, recommended |
| **AWS CloudFront** | Pay-per-use | $102 | $306 | $510 | $8.50/month | Simple, predictable |
| **Fastly** | Starter | $744 | $2,232 | $3,720 | $62/month | $50 minimum overhead |
| **Cloudinary** | Plus | $1,068 | $3,204 | $5,340 | $89/month | Media-specific (150GB included) |

**Winner**: Cloudflare Free ($0 TCO, unlimited bandwidth)

**Best Paid Option**: BunnyCDN ($300-600 over 5 years) or AWS CloudFront ($510)

**When to Upgrade from Free**: If you need real-time analytics (Cloudflare Pro $20/month = $1,200 over 5 years)

**Avoid**: Fastly ($3,720 over 5 years) is 6-12× more expensive than BunnyCDN

---

## Scenario 3: Mid-Size Site (1TB/month egress)

**Use Case**: Mid-market SaaS, high-traffic e-commerce, video streaming, API at scale

### Monthly Costs by Provider

| Provider | Plan | Base Plan Cost | Bandwidth Cost (1TB) | Extra Features | Total Monthly | Notes |
|----------|------|----------------|----------------------|----------------|---------------|-------|
| **BunnyCDN** | Pay-per-use | $0 | $50-100 (1TB × $0.05-0.10) | None | **$50-100** | Cheapest overall |
| **Cloudflare** | Free | $0 | $0 (unlimited) | None | **$0** | Still free! No bandwidth cap |
| **Cloudflare** | Pro | $20 | $0 (unlimited) | None | **$20** | Real-time analytics recommended at this scale |
| **Cloudflare** | Business | $200 | $0 (unlimited) | Priority support, 50 Page Rules | **$200** | Overkill unless need support |
| **AWS CloudFront** | Pay-per-use | $0 | $85 (1TB × $0.085) | None | **$85** | First 10TB tier pricing |
| **Fastly** | Starter | $50 | $120-180 (1TB × $0.12-0.18) | None | **$170-230** | Instant purge, real-time logs |
| **Akamai** | Enterprise | N/A | Negotiated (est. $500-2K/TB) | None | **$500-2,000** | Enterprise pricing, volume discounts |
| **Cloudinary** | Advanced | $249 | $0 (500GB included) + $0.08/GB overage | Advanced features | **$249 + $40** (500GB overage) = **$289** | Media-specific |

### 1-Year, 3-Year, 5-Year TCO (1TB/month)

| Provider | Plan | 1-Year TCO | 3-Year TCO | 5-Year TCO | Effective Monthly (5-year) | Notes |
|----------|------|------------|------------|------------|---------------------------|--------|
| **Cloudflare** | Free | **$0** | **$0** | **$0** | **$0** | **Unbeatable free tier** |
| **Cloudflare** | Pro | $240 | $720 | $1,200 | $20/month | Real-time analytics, recommended |
| **BunnyCDN** | Pay-per-use | $600-1,200 | $1,800-3,600 | $3,000-6,000 | $50-100/month | Cheapest paid, linear scaling |
| **AWS CloudFront** | Pay-per-use | $1,020 | $3,060 | $5,100 | $85/month | Predictable, AWS integration |
| **Fastly** | Starter | $2,040-2,760 | $6,120-8,280 | $10,200-13,800 | $170-230/month | Instant purge, real-time logs |
| **Cloudflare** | Business | $2,400 | $7,200 | $12,000 | $200/month | Priority support |
| **Cloudinary** | Advanced | $3,468 | $10,404 | $17,340 | $289/month | Media-specific (500GB + overage) |
| **Akamai** | Enterprise | $6,000-24,000 | $18,000-72,000 | $30,000-120,000 | $500-2,000/month | Enterprise SLAs, negotiated |

**Winner**: Cloudflare Free ($0 TCO, unlimited bandwidth, still viable at 1TB!)

**Best Paid Option**: BunnyCDN ($3,000-6,000 over 5 years) is 2-5× cheaper than Fastly

**When to Choose Fastly**: If you need instant purge (<1 second) or real-time log streaming (worth $10,200-13,800 vs $3,000-6,000 for BunnyCDN?)

**When to Choose AWS CloudFront**: If you're deep in AWS ecosystem (S3 origin, Lambda@Edge, CloudWatch)

**Avoid**: Akamai unless you need enterprise SLAs ($30K-120K over 5 years)

---

## Scenario 4: High-Traffic Site (10TB/month egress)

**Use Case**: Major SaaS platform, video streaming service, global API, gaming CDN

### Monthly Costs by Provider

| Provider | Plan | Base Plan Cost | Bandwidth Cost (10TB) | Volume Discounts | Total Monthly | Notes |
|----------|------|----------------|------------------------|------------------|---------------|-------|
| **BunnyCDN** | Pay-per-use | $0 | $500-1,000 (10TB × $0.05-0.10) | Volume discounts available | **$500-1,000** | Cheapest, linear pricing |
| **Cloudflare** | Free | $0 | $0 (unlimited) | None | **$0** | **Still free at 10TB!** |
| **Cloudflare** | Business | $200 | $0 (unlimited) | None | **$200** | Priority support recommended |
| **Cloudflare** | Enterprise | Custom | $0 (unlimited) | SLA, dedicated support | **$2,000-5,000/month** | Enterprise features, 99.95% uptime |
| **AWS CloudFront** | Pay-per-use | $0 | $850 (10TB × $0.085) | None (first 10TB tier) | **$850** | Next 40TB drops to $0.080/GB |
| **Fastly** | Professional | Custom | $1,200-1,800 (10TB × $0.12-0.18) | Volume discounts | **$1,200-1,800** | Instant purge, real-time, custom contracts |
| **Akamai** | Enterprise | Custom | Negotiated (est. $0.05-0.20/GB) | Heavy volume discounts | **$500-2,000** | Enterprise SLAs, global peering |
| **Cloudinary** | Enterprise | Custom | Negotiated | Custom features | **$1,000-5,000** | Media-specific (video streaming) |

### 1-Year, 3-Year, 5-Year TCO (10TB/month)

| Provider | Plan | 1-Year TCO | 3-Year TCO | 5-Year TCO | Effective Monthly (5-year) | Notes |
|----------|------|------------|------------|------------|---------------------------|--------|
| **Cloudflare** | Free | **$0** | **$0** | **$0** | **$0** | **Unbelievable free tier** (10TB!) |
| **Cloudflare** | Business | $2,400 | $7,200 | $12,000 | $200/month | Priority support, unlimited bandwidth |
| **BunnyCDN** | Pay-per-use | $6,000-12,000 | $18,000-36,000 | $30,000-60,000 | $500-1,000/month | Cheapest paid, volume discounts |
| **AWS CloudFront** | Pay-per-use | $10,200 | $30,600 | $51,000 | $850/month | AWS integration, predictable |
| **Fastly** | Professional | $14,400-21,600 | $43,200-64,800 | $72,000-108,000 | $1,200-1,800/month | Instant purge, custom SLAs |
| **Cloudflare** | Enterprise | $24,000-60,000 | $72,000-180,000 | $120,000-300,000 | $2,000-5,000/month | Enterprise SLA, 99.95% uptime |
| **Akamai** | Enterprise | $6,000-24,000 | $18,000-72,000 | $30,000-120,000 | $500-2,000/month | Enterprise, volume discounts |
| **Cloudinary** | Enterprise | $12,000-60,000 | $36,000-180,000 | $60,000-300,000 | $1,000-5,000/month | Video streaming (media-specific) |

**Winner**: Cloudflare Free ($0 TCO, even at 10TB/month!)

**Best Paid Option**: BunnyCDN ($30,000-60,000 over 5 years) is 2-5× cheaper than Fastly, Akamai

**When to Choose Fastly**: If you need instant purge + enterprise SLA ($72K-108K over 5 years)

**When to Choose Akamai**: If you need 99.9%+ SLA, global peering, enterprise support ($30K-120K over 5 years)

**When to Choose Cloudflare Enterprise**: If you need 99.95% uptime SLA, dedicated support ($120K-300K over 5 years)

**When to Choose AWS CloudFront**: If you're deep in AWS ecosystem, predictable costs ($51K over 5 years)

---

## Hidden Costs Analysis

### Cloudflare Hidden Costs

| Feature | Cost | When You Need It | Workaround |
|---------|------|------------------|------------|
| **Real-time analytics** | $20/month (Pro) | If 24h delay unacceptable | Use third-party analytics (Google Analytics) |
| **Image Resizing** | $5-10/month | If serving images at multiple sizes | Pre-generate sizes, use Cloudinary |
| **Workers** | $5/month (10M requests) | If need edge compute | Use origin server logic |
| **Argo Smart Routing** | $5/month + $0.10/GB | If need optimized routing | Accept default routing |
| **Load Balancing** | $5/month (2 origins) | If need multi-origin failover | DNS-based failover |
| **Rate Limiting** | $5/month (10K rules) | If need DDoS/bot protection | Use WAF ($20/month Pro) |

**Total Potential Hidden Costs**: $45/month ($540/year) if you enable all features

---

### Fastly Hidden Costs

| Feature | Cost | When You Need It | Notes |
|---------|------|------------------|-------|
| **Minimum charge** | $50/month | Always (even 1GB usage) | No workaround (pricing floor) |
| **Log streaming** | Included | Real-time logs | No extra cost (unlike Cloudflare $5/month) |
| **Image Optimizer** | Add-on pricing | If serving images | Extra cost, not included |
| **Next-Gen WAF** | Add-on pricing | If need WAF | Extra cost (Signal Sciences acquisition) |

**Total Potential Hidden Costs**: $50/month minimum (not hidden, but inflexible)

---

### BunnyCDN Hidden Costs

| Feature | Cost | When You Need It | Workaround |
|---------|------|------------------|------------|
| **Optimizer** (Edge Rules + WAF) | $9.50/month | If need advanced features | Use basic features only |
| **Log Engine** | $10/month | If need long-term log storage | Use basic analytics |
| **Edge Scripts** | $10/month | If need edge compute | Use origin server logic |

**Total Potential Hidden Costs**: $29.50/month ($354/year) if you enable all features

---

### AWS CloudFront Hidden Costs

| Feature | Cost | When You Need It | Workaround |
|---------|------|------------------|------------|
| **Shield Advanced** | $3,000/month | If need advanced DDoS protection | Use Shield Standard (free, basic) |
| **WAF** | $5/month + $1/million requests | If need web application firewall | Use security groups, NACLs |
| **Lambda@Edge** | $0.60/million requests | If need edge compute | Use CloudFront Functions ($0.10/million) |
| **Origin Shield** | $0.01/10K requests | If need origin caching | Skip origin shield |
| **Real-time logs** | $0.01/million log lines | If need <1 minute latency | Use standard logs (5-minute delay, free) |

**Total Potential Hidden Costs**: $3,000+/month if Shield Advanced enabled (otherwise minimal)

---

### Akamai Hidden Costs

| Feature | Cost | When You Need It | Notes |
|---------|------|------------------|-------|
| **Image Manager** | Add-on pricing | If serving images | Bundled in some contracts |
| **Bot Manager** | Add-on pricing | If need bot detection | Bundled in some contracts |
| **EdgeWorkers** | Pay-per-use | If need edge compute | Bundled in some contracts |

**Total Potential Hidden Costs**: Highly negotiable (enterprise contracts bundle features)

---

### Cloudinary Hidden Costs

| Feature | Cost | When You Need It | Workaround |
|---------|------|------------------|------------|
| **Overage charges** | $0.08/GB bandwidth | If exceed plan limits | Upgrade to higher tier |
| **Storage overage** | $0.18/GB storage | If exceed storage limits | Delete old assets |
| **Transformations overage** | $0.002/transformation | If exceed transformation limits | Cache transformed images |

**Total Potential Hidden Costs**: Variable (depends on overages)

---

## Cost Drivers Analysis

### What Drives CDN Costs?

1. **Bandwidth (egress)**: Primary cost driver for pay-per-use CDNs (BunnyCDN, AWS, Fastly)
   - Cloudflare exception: Unlimited bandwidth (flat-rate tiers)

2. **Requests**: Secondary cost driver (Fastly charges per request, AWS charges per 10K requests)
   - Most CDNs: Requests are free or negligible (<$1/million)

3. **Geographic distribution**: Bandwidth costs vary by region
   - BunnyCDN: $0.01/GB (Tier 1 regions like US/EU) to $0.12/GB (Oceania, South Africa)
   - AWS CloudFront: $0.085/GB (US/EU) to $0.170/GB (India)

4. **Storage** (if using CDN's object storage):
   - BunnyCDN Storage Zones: $0.01/GB/month
   - Cloudflare R2: $0.015/GB/month (egress free)
   - AWS S3 + CloudFront: $0.023/GB storage + $0.085/GB egress

5. **Features**: Add-ons (WAF, edge compute, image optimization, real-time analytics)
   - Cloudflare: $5-45/month in add-ons
   - BunnyCDN: $10-29.50/month in add-ons
   - AWS: $3,000/month for Shield Advanced (major outlier)

6. **Support**: Enterprise plans include priority/dedicated support
   - Cloudflare Enterprise: $2,000-5,000/month (includes support)
   - Akamai: Support bundled in enterprise contracts

---

## TCO Optimization Strategies

### Strategy 1: Start with Cloudflare Free (0GB → 10TB/month)

**When**: MVP, small site, unpredictable traffic, budget-constrained
**TCO**: $0 (unlimited bandwidth)
**Trade-offs**: 24-hour analytics delay, no edge compute (without Workers $5/month)
**Exit Strategy**: Upgrade to Cloudflare Pro ($20/month) when need real-time analytics

---

### Strategy 2: BunnyCDN for Predictable Growth (100GB → 100TB/month)

**When**: Cost-conscious, predictable traffic, want linear pricing
**TCO**: $5-10/TB (cheapest paid option)
**Trade-offs**: No instant purge, smaller PoP count (123 vs 310+ Cloudflare)
**Exit Strategy**: Stay with BunnyCDN (scales linearly) or move to Akamai for enterprise SLAs

---

### Strategy 3: AWS CloudFront for AWS Ecosystem (any scale)

**When**: Already using S3, Lambda, Route 53, CloudWatch
**TCO**: $85/TB (first 10TB), drops to $20/TB (>5PB/month)
**Trade-offs**: More expensive than BunnyCDN, but deep AWS integration
**Exit Strategy**: Stay with AWS (ecosystem lock-in), or multi-CDN with Cloudflare

---

### Strategy 4: Fastly for Real-Time Requirements (1TB+/month)

**When**: News site, live sports, stock trading, real-time apps (need <1s purge)
**TCO**: $120-180/TB
**Trade-offs**: 2-5× more expensive than BunnyCDN, but instant purge unique
**Exit Strategy**: Stay with Fastly (instant purge is unique), or move to Akamai for enterprise

---

### Strategy 5: Akamai for Enterprise SLAs (10TB+/month)

**When**: Fortune 500, mission-critical, 99.9%+ uptime required, regulatory compliance
**TCO**: $500-2,000/month (negotiated)
**Trade-offs**: Most expensive, but enterprise support + SLAs + largest network (4,100+ PoPs)
**Exit Strategy**: Stay with Akamai (enterprise lock-in)

---

### Strategy 6: Cloudinary for Media Sites (any scale)

**When**: Photo sharing, video streaming, media-heavy site
**TCO**: $0 (25GB free) → $89/month (150GB) → $249/month (500GB)
**Trade-offs**: Media-specific (not general CDN), overage charges
**Exit Strategy**: Stay with Cloudinary (media expertise), or DIY with BunnyCDN + image optimization library

---

## Cost Comparison Table (5-Year TCO Summary)

| Traffic/Month | Cloudflare Free | Cloudflare Pro | BunnyCDN | AWS CloudFront | Fastly | Akamai | Cloudinary |
|---------------|-----------------|----------------|----------|----------------|--------|--------|------------|
| **10GB** | $0 | $1,200 | $30-60 | $40.80 (after free tier) | $3,000 | N/A | $0 (free tier) |
| **100GB** | $0 | $1,200 | $300-600 | $510 | $3,720 | $6,000-12,000 | $5,340 (Plus) |
| **1TB** | $0 | $1,200 | $3,000-6,000 | $5,100 | $10,200-13,800 | $30,000-120,000 | $17,340 (Advanced) |
| **10TB** | $0 | $12,000 (Business) | $30,000-60,000 | $51,000 | $72,000-108,000 | $30,000-120,000 | $60,000-300,000 |

**Key Takeaways**:
- **0-10TB/month**: Cloudflare Free ($0) is unbeatable
- **100GB-10TB/month**: BunnyCDN is cheapest paid option (2-5× cheaper than competitors)
- **10TB+/month**: BunnyCDN still cheapest, but Akamai/Fastly offer enterprise features worth premium
- **Media sites**: Cloudinary free tier (25GB) adequate for small sites, paid tiers expensive vs BunnyCDN

---

## Pricing Model Comparison

| Provider | Pricing Model | Pros | Cons | Best For |
|----------|---------------|------|------|----------|
| **Cloudflare** | Flat-rate tiers ($0, $20, $200, Enterprise) | Unlimited bandwidth, predictable | 24h analytics delay on Free, features gated by tier | Unpredictable traffic, budget-constrained |
| **BunnyCDN** | Pay-per-use (linear $0.05-0.10/GB) | Cheapest, transparent, scales linearly | No enterprise features (SLAs, support) | Cost-conscious, predictable growth |
| **AWS CloudFront** | Pay-per-use (tiered $0.085-0.020/GB) | AWS integration, volume discounts | More expensive than BunnyCDN | AWS ecosystem lock-in |
| **Fastly** | Pay-per-use + $50 minimum | Transparent, no hidden fees | $50 minimum expensive for <100GB | Real-time requirements, high traffic |
| **Akamai** | Enterprise negotiated | Volume discounts, bundled features | Opaque pricing, high minimums | Enterprise SLAs, Fortune 500 |
| **Cloudinary** | Tiered plans (storage + bandwidth + transformations) | Media-specific, bundled features | Overage charges, expensive at scale | Media-heavy sites (images/video) |

---

## Next Steps

With pricing TCO analysis complete, the next S2 deliverables are:

1. **Performance benchmarks** - Latency data (p50, p95, p99) from CDNPerf, WebPageTest
2. **Geographic coverage** - PoP distribution maps, regional latency breakdown
3. **Integration ecosystem** - Origin types, API quality, SDK depth
4. **Synthesis** - Cross-cutting insights, decision trees, trade-off analysis

**Time to complete pricing TCO**: ~1.5 hours (4 scenarios × 6 providers × 3 time horizons)

---

**Last Updated**: November 12, 2025
**Next Deliverable**: Performance benchmarks
