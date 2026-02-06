# Provider Profile: Fastly CDN

**Category**: Global Giant - Developer-Focused
**Market Position**: Premium CDN for high-performance applications
**Est. Market Share**: ~5-7%

---

## Overview

**What it is**: Programmable CDN with instant purge, real-time analytics, and edge compute via VCL scripting

**Founded**: 2011
**Headquarters**: San Francisco, CA
**Public**: Yes (NYSE: FSLY, since 2019)
**Employees**: ~1,000

**Key Value Proposition**: "Programmable edge platform" - developer control + performance

---

## Network Infrastructure

**Points of Presence**: 100+ strategic locations
**Total Capacity**: 200+ Tbps
**Network Type**: Anycast + strategic peering
**IPv6 Support**: ✅ Yes

**Geographic Coverage**:
- North America: 40+ locations
- Europe: 30+ locations
- Asia: 20+ locations
- South America: 5+ locations
- Africa: 2+ locations
- Oceania: 3+ locations

**Strategy**: Fewer PoPs but premium locations with best peering

---

## Pricing Structure

### Pay-As-You-Go
**No free tier** - Enterprise-focused pricing

**Bandwidth Pricing**:
- **First 10TB**: ~$0.12/GB = **$120/TB**
- **10-50TB**: ~$0.10/GB = **$100/TB**
- **50-150TB**: ~$0.08/GB = **$80/TB**
- **150TB+**: Custom pricing (volume discounts)

**Requests**:
- **First 10M**: Included
- **Additional**: $0.50 per million requests

**Minimum**: Typically $50-100/month (small projects)

**Example costs**:
- 1TB/month: ~$120/month
- 10TB/month: ~$1,000/month
- 100TB/month: ~$8,000/month

---

### Enterprise Pricing
**Custom contracts**: $5,000-50,000+/month

**Includes**:
- Volume discounts (30-50% off at scale)
- Dedicated account team
- Custom SLAs (99.99%+ uptime)
- Priority support (24/7 phone + email)
- Advanced features (Image Optimizer, Compute@Edge)

---

## Key Features

### 1. VCL (Varnish Configuration Language)
**What**: Programmable caching logic at edge

**Use cases**:
- Custom cache key generation
- A/B testing routing logic
- Request/response transformation
- Authentication/authorization
- Geo-routing based on IP

**Language**: VCL (declarative config language)
**Learning curve**: Moderate (need to learn VCL syntax)

**Example VCL**:
```vcl
sub vcl_recv {
  if (req.url ~ "\.(jpg|png|gif)$") {
    set req.backend = image_backend;
    return(lookup);
  }
}
```

**Lock-in risk**: HIGH - VCL is Fastly-specific (migration requires rewrite)

---

### 2. Instant Purge (<150ms)
**What**: Purge cached content globally in <150ms

**vs Competitors**:
- **Fastly**: <150ms (instant)
- **Cloudflare**: 5-30 seconds
- **AWS CloudFront**: 5-15 minutes (invalidation)

**Use cases**:
- News sites (breaking news needs instant updates)
- E-commerce (flash sales, inventory updates)
- SaaS (real-time config changes)

**Why it matters**: Critical for high-change-rate sites

---

### 3. Real-Time Analytics
**What**: Log streaming in real-time (seconds, not minutes)

**Metrics**:
- Requests per second
- Cache hit rate
- Bandwidth usage
- Error rates
- Origin latency

**Streaming**: Datadog, Splunk, S3, Google BigQuery (real-time log shipping)

**vs Competitors**: Most CDNs = 5-30 minute delay on analytics

---

### 4. Image Optimizer
**What**: On-the-fly image resizing, format conversion, compression

**Pricing**: Add-on (contact sales for pricing)
**Formats**: WebP, AVIF, JPEG, PNG
**Use case**: Responsive images, reduce bandwidth 30-50%

---

### 5. Compute@Edge (Edge Compute)
**What**: Run code at edge (alternative to VCL)

**Languages**: Rust, JavaScript, Go (compiled to WebAssembly)
**Use cases**: Same as Workers/VCL but with modern languages

**Status**: Newer feature (2021+), less mature than VCL

---

## Performance Characteristics

**Latency**:
- Median: 15-25ms (global average)
- Best: <10ms (premium peering in major cities)
- Worst: 50-80ms (remote areas)

**Cache Hit Rate**: 92-97% (highest in industry, aggressive caching)
**Purge Time**: <150ms (fastest in industry)

**Benchmarks** (from CDNPerf.com, 2024 averages):
- Global latency: ~20ms median
- North America: 10-15ms
- Europe: 15-20ms
- Asia: 25-35ms

**vs Competitors**:
- Faster than: AWS CloudFront (30ms), KeyCDN (35ms)
- Comparable to: Cloudflare (20ms)
- Purge: 10-200× faster than all competitors

---

## Integration & Developer Experience

### Setup Time: **30-60 minutes** (CNAME + VCL config)

**Steps**:
1. Sign up + add payment method (5 minutes)
2. Create service (add origin) (5 minutes)
3. Configure VCL (optional but powerful) (15-30 minutes)
4. Add CNAME record at DNS (5 minutes)
5. Test and deploy (10-20 minutes)

**Documentation Quality**: ⭐⭐⭐⭐½ (4.5/5)
- Excellent VCL guides
- Strong API documentation
- Active developer community

**API**: REST API, Terraform provider

---

## Pros

✅ **Instant purge** (<150ms, 10-200× faster than competitors)
✅ **VCL programmability** (custom caching logic, unmatched flexibility)
✅ **Real-time analytics** (log streaming, seconds not minutes)
✅ **High cache hit rates** (92-97%, best in industry)
✅ **Premium peering** (excellent performance despite fewer PoPs)
✅ **Developer-focused** (API-first, great docs, Terraform support)
✅ **Strong support** (known for responsive, knowledgeable support team)

---

## Cons

❌ **Expensive** ($120/TB vs BunnyCDN $10/TB, 12× more expensive)
❌ **No free tier** (pay from day 1)
❌ **VCL learning curve** (need to learn declarative language)
❌ **VCL lock-in** (migration = rewrite caching logic)
❌ **Fewer PoPs** (100 vs Cloudflare 330+, but quality > quantity)
❌ **Complex pricing** (bandwidth + requests + features)
❌ **Stock volatility** (FSLY stock down 80% from 2020 peak, company challenges)

---

## Best Use Cases

### ✅ Excellent For:
- **High-change-rate sites** (news, live sports, flash sales → instant purge critical)
- **SaaS platforms** (need custom caching logic, real-time config updates)
- **Developer-centric teams** (want programmable edge, VCL control)
- **Real-time analytics needs** (log streaming for monitoring/debugging)
- **Premium performance** (willing to pay 2-5× for best hit rates + fastest purge)

### ⚠️ Consider Alternatives For:
- **Cost-sensitive** (BunnyCDN 10× cheaper, Cloudflare free tier)
- **Simple use cases** (static assets only → BunnyCDN or Cloudflare sufficient)
- **Small traffic** (<5TB/month → Cloudflare Pro $20/month better value)
- **Want modern edge compute** (Cloudflare Workers easier than VCL)

---

## Cost Comparison Examples

### Example 1: Small Site (1TB/month)
- **Fastly**: ~$120/month
- **Cloudflare Pro**: $20/month (6× cheaper)
- **BunnyCDN**: $10/month (12× cheaper)
- **Verdict**: Only use Fastly if instant purge/VCL required

### Example 2: Medium Site (10TB/month)
- **Fastly**: ~$1,000/month
- **Cloudflare Business**: $200/month (5× cheaper)
- **BunnyCDN**: $100/month (10× cheaper)
- **Verdict**: Fastly premium = 5-10× cost, justified only for specific needs

### Example 3: Large Site (100TB/month)
- **Fastly**: ~$8,000/month (negotiated)
- **Cloudflare Enterprise**: ~$5,000/month (negotiated)
- **BunnyCDN**: $1,000/month
- **Verdict**: At scale, premium shrinks but still 2-5× more expensive

---

## Notable Customers

- **Stripe** (payments platform)
- **GitHub** (code hosting)
- **Stack Overflow** (Q&A platform)
- **New York Times** (news)
- **Shopify** (e-commerce platform)

**Common pattern**: High-performance SaaS/platforms needing instant purge + custom logic

---

## Migration Considerations

### Migrating TO Fastly:
**Effort**: 4-12 hours (CNAME + VCL config)
**Risk**: Moderate (VCL testing required)

### Migrating FROM Fastly:
**Effort**: 8-20 hours (depends on VCL complexity)
- CNAME change: 10 minutes
- Rewrite VCL logic: 4-16 hours (most effort)
- Test new CDN: 2-4 hours

**Lock-in**: HIGH (VCL is Fastly-specific)

---

## Vendor Viability

**Financial Health**: ⭐⭐⭐ (3/5)
- Public company (NYSE: FSLY)
- Revenue: $500M+ (2024)
- **Challenges**: Stock down 80% from 2020 peak, profitability issues
- **Growth**: Slowing (10-15% YoY vs 30-50% previously)

**Longevity**: 13 years (founded 2011)
**Acquisition Risk**: Moderate (potential target for Cloudflare, Akamai, or private equity)
**5-year survival**: 90% (profitable path unclear)
**10-year survival**: 75% (company challenges, but strong tech)

**Mitigation**: Easy migration away (8-20 hours) if company struggles

---

## Verdict: Premium CDN for Specific Needs

**Rating**: ⭐⭐⭐⭐ (4/5)

**Why**: Best-in-class purge speed + programmability + performance

**When to use**:
- ✅ High-change-rate content (news, sports, flash sales)
- ✅ Need custom caching logic (VCL programmability)
- ✅ Real-time analytics required (log streaming)
- ✅ Budget allows 5-10× premium over cheap CDNs
- ✅ Performance-critical SaaS platform

**When to consider alternatives**:
- ❌ Cost-sensitive (use BunnyCDN or Cloudflare)
- ❌ Static assets only (no need for instant purge)
- ❌ Small traffic (<10TB/month → Cloudflare better value)
- ❌ Prefer modern edge compute (Cloudflare Workers easier than VCL)
