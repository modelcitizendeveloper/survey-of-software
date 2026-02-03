# Provider Profile: BunnyCDN

**Category**: Mid-Market Budget Leader
**Market Position**: Best value for money
**Est. Market Share**: ~2-3% (growing rapidly)

---

## Overview

**What it is**: Cost-effective CDN with 123 PoPs, focused on simplicity and value

**Founded**: 2015
**Headquarters**: Ljubljana, Slovenia (EU-based)
**Public**: No (bootstrapped, profitable)
**Employees**: ~50-100

**Key Value Proposition**: "Fast, reliable, and affordable CDN" - best price/performance ratio

---

## Network Infrastructure

**Points of Presence**: 123 locations globally
**Total Capacity**: Not disclosed (estimated 50+ Tbps)
**Network Type**: Anycast
**IPv6 Support**: ✅ Yes (fully supported)

**Geographic Coverage**:
- Europe: 40+ locations (strongest presence)
- North America: 30+ locations
- Asia: 25+ locations
- South America: 15+ locations
- Africa: 8+ locations
- Oceania: 5+ locations

---

## Pricing Structure

### Pay-As-You-Go (No Monthly Fee)
**Cost**: $0 base + bandwidth usage

**Bandwidth Pricing** (varies by region):
- **Tier 1** (Europe, North America): $0.01/GB = **$10/TB**
- **Tier 2** (Asia, South America): $0.03/GB = **$30/TB**
- **Tier 3** (Africa, Middle East, Oceania): $0.045/GB = **$45/TB**

**Requests**: Included (no per-request fees)

**Minimum**: None (pay only what you use)

**Example costs**:
- 1TB/month (North America): $10/month
- 10TB/month (North America): $100/month
- 100TB/month (North America): $1,000/month

**Compare to Cloudflare Pro**: $20/month (but unlimited bandwidth)
**Compare to AWS CloudFront**: $850/month for 10TB North America

---

### Volume Discounts
**Automatic at scale**:
- >500TB/month: Contact for custom pricing
- >1PB/month: Significant discounts (reported 30-50% off)

---

## Key Features

### 1. Pull Zones (CDN)
**What**: Standard CDN pull zone (cache from origin)

**Features**:
- Automatic cache optimization
- Smart routing (route to fastest PoP)
- HTTP/2, HTTP/3 support
- Brotli compression
- Origin shield (reduce origin requests 50-90%)

**Setup**: 5 minutes (add origin URL, get CDN URL)

---

### 2. Edge Storage (Object Storage)
**What**: Alternative to S3, integrated with CDN

**Pricing**:
- Storage: $0.01/GB/month = **$10/TB**
- Bandwidth: Same as CDN ($0.01-0.045/GB by region)
- **Replication**: $0.01/GB one-time (replicate to multiple regions)

**Use case**: Store + deliver files from CDN (no separate origin needed)

**vs S3**: 50% cheaper storage ($10 vs $23/TB), integrated CDN

---

### 3. Stream (Video CDN)
**What**: Video hosting + transcoding + CDN delivery

**Pricing**:
- Storage: $0.005/GB/month = **$5/TB**
- Bandwidth: Same as CDN ($0.01-0.045/GB)
- Encoding: $0.01/minute of video

**Use case**: YouTube alternative, video hosting with CDN

---

### 4. Bunny Optimizer (Image/JS/CSS Optimization)
**What**: Automatic image compression, lazy loading, minification

**Pricing**: $9.50/month per pull zone
**Compression**: 30-60% reduction (lossy + lossless)

**vs Cloudflare Polish**: Cheaper standalone ($9.50 vs $20/month), similar quality

---

### 5. DDoS Protection
**What**: Basic DDoS mitigation (included)

**Protection types**:
- L3/L4: Network layer attacks (SYN floods, volumetric)
- L7: Basic application layer (rate limiting)

**Limitations**:
- Not as robust as Cloudflare (max mitigation ~100 Gbps vs Cloudflare's Tbps-scale)
- No advanced bot management

**Verdict**: Good enough for most sites, not for mission-critical or high-risk targets

---

## Performance Characteristics

**Latency**:
- Median: 20-30ms (global average)
- Best: 5-10ms (Europe, where strongest presence)
- Worst: 60-100ms (Africa, remote areas)

**Cache Hit Rate**: 85-95% (typical)
**Purge Time**: 5-10 seconds (edge purge)

**Benchmarks** (from CDNPerf.com, 2024 averages):
- Global latency: ~25ms median
- Europe: 10-15ms (excellent, strongest region)
- North America: 20-30ms
- Asia: 30-50ms

**vs Competitors**:
- Comparable to: Cloudflare (20ms), Fastly (20ms)
- Faster than: KeyCDN (35ms), AWS CloudFront (30ms) in Europe
- Slightly slower in Asia/Africa (fewer PoPs)

---

## Integration & Developer Experience

### Setup Time: **5-10 minutes** (CNAME-based)

**Steps**:
1. Sign up (2 minutes)
2. Create Pull Zone (add origin URL) (2 minutes)
3. Add CNAME record at DNS provider (1-5 minutes)
4. Configure caching rules (optional, 5 minutes)

**No DNS migration required** (unlike Cloudflare)

**Documentation Quality**: ⭐⭐⭐⭐ (4/5)
- Good guides and tutorials
- Active community support
- Clear API documentation

**API**: REST API, documentation at docs.bunny.net

**Dashboard**: Simple, intuitive (no overwhelming features)

---

## Pros

✅ **Cheapest bandwidth** ($10/TB for North America/Europe, 10× cheaper than AWS)
✅ **No monthly fee** (pay only bandwidth used)
✅ **Simple pricing** (no hidden fees, no per-request charges)
✅ **Origin shield included** (reduces origin load 50-90%)
✅ **Fast setup** (5-10 minutes, no DNS migration)
✅ **Great European performance** (40+ PoPs, 10-15ms latency)
✅ **Good DX** (simple dashboard, good docs)
✅ **Edge Storage** (cheaper than S3, integrated CDN)
✅ **Excellent support** (responsive via chat, despite small team)

---

## Cons

❌ **No generous free tier** (pay from day 1, but cheap)
❌ **Fewer PoPs** (123 vs Cloudflare 330+, affects remote areas)
❌ **Weaker in Asia/Africa** (30-50ms latency vs Cloudflare 20ms)
❌ **Basic DDoS protection** (not for high-risk targets)
❌ **No WAF** (need separate service if needed)
❌ **No edge compute** (no Workers/Lambda@Edge equivalent)
❌ **Smaller company** (50-100 employees vs Cloudflare 4,000+)

---

## Best Use Cases

### ✅ Excellent For:
- **Cost-conscious startups** (predictable low costs)
- **Media-heavy sites** (images, videos, downloads → save 50-90% vs AWS)
- **European sites** (strongest PoP presence, 10-15ms latency)
- **Static asset delivery** (no need for edge compute)
- **5-100TB/month bandwidth** (sweet spot for cost savings)

### ⚠️ Consider Alternatives For:
- **Free tier needed** (Cloudflare free tier better for <1TB/month)
- **Advanced security** (Cloudflare WAF + DDoS better)
- **Edge compute** (Cloudflare Workers, Fastly VCL)
- **Enterprise SLAs** (BunnyCDN no formal SLAs)

---

## Cost Comparison Examples

### Example 1: Small Site (1TB/month, North America)
- **BunnyCDN**: $10/month
- **Cloudflare Pro**: $20/month (includes more features)
- **AWS CloudFront**: $85/month
- **Verdict**: Cloudflare Pro better value (free SSL, image optimization for +$10)

### Example 2: Medium Site (10TB/month, North America)
- **BunnyCDN**: $100/month
- **Cloudflare Business**: $200/month
- **AWS CloudFront**: $850/month
- **Verdict**: BunnyCDN wins on cost (50-85% cheaper)

### Example 3: Large Site (100TB/month, North America)
- **BunnyCDN**: $1,000/month
- **Cloudflare Enterprise**: ~$3,000-5,000/month (negotiated)
- **AWS CloudFront**: $4,000/month
- **Verdict**: BunnyCDN 70-80% cheaper

---

## Migration Considerations

### Migrating TO BunnyCDN:
**Effort**: 5-10 minutes (CNAME change)
**Risk**: Very low (gradual DNS propagation, easy rollback)

### Migrating FROM BunnyCDN:
**Effort**: 5-10 minutes (CNAME change)
**Risk**: Very low (no vendor lock-in, pure CDN)

**Lock-in**: VERY LOW (simple CNAME, standard caching)

---

## Vendor Viability

**Financial Health**: ⭐⭐⭐½ (3.5/5)
- Bootstrapped, profitable
- Revenue: ~$10-20M estimated (not disclosed)
- Growth: 50%+ YoY (rapid growth)

**Longevity**: 9 years (founded 2015)
**Acquisition Risk**: Moderate (attractive acquisition target for larger CDN)
**5-year survival**: 85% (profitable, growing)
**10-year survival**: 70% (small company risk)

**Risk mitigation**: Easy migration away (5-10 minutes) reduces risk

---

## Verdict: Best Budget CDN

**Rating**: ⭐⭐⭐⭐ (4/5)

**Why**: Unbeatable pricing, good performance, simple to use

**When to use**:
- ✅ Cost is primary concern (save 50-90% vs big CDNs)
- ✅ 5-100TB/month bandwidth (sweet spot)
- ✅ Static asset delivery (images, videos, downloads)
- ✅ European audience (best PoP coverage)
- ✅ Don't need advanced security (WAF, advanced DDoS)

**When to consider alternatives**:
- ❌ Need free tier (Cloudflare free better for <1TB/month)
- ❌ Need WAF + advanced DDoS (Cloudflare better)
- ❌ Need edge compute (Cloudflare Workers, Fastly VCL)
- ❌ Enterprise SLAs required (Cloudflare/Fastly/AWS better)
