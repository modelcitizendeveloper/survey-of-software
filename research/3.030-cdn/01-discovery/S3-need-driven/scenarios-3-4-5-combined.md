# S3 Scenarios 3-5: E-Commerce, News Site, Video Platform

**Combined Scenarios**: High-traffic use cases with specialized requirements
**Last Updated**: November 12, 2025

---

# Scenario 3: E-Commerce Site (5TB/month, Price Updates)

**Company Profile**: Mid-market e-commerce, seasonal traffic, frequent price updates
**Traffic**: 5TB/month egress (10TB during holidays), 50-100M requests/month
**Budget**: $200-1,000/month for CDN
**Priority**: Fast cache purge for price updates, handle traffic spikes, image optimization

---

## Business Context

- **Stage**: Series B e-commerce company ($10-50M revenue)
- **Team Size**: 50-100 engineers
- **Users**: 500K-2M MAU, 50K-200K daily active shoppers
- **Revenue**: $5M-20M MRR ($60M-240M annual GMV)
- **Seasonal Traffic**: 2-5× spike during Black Friday, Cyber Monday, holidays

### Technical Environment
- **Stack**: React/Next.js + Node.js + PostgreSQL + Redis
- **Infrastructure**: Multi-cloud (AWS primary, GCP backup)
- **Product Catalog**: 10K-100K SKUs, 500K-1M product images
- **Traffic Pattern**: 5TB/month avg, 10-15TB during Q4 holidays
- **Critical Operations**: Price updates (hourly), inventory updates (real-time), flash sales

---

## CDN Requirements

### Critical Requirements
1. **Fast cache purge** (<10 seconds for price updates, inventory changes)
2. **Image optimization** (automatic WebP/AVIF, responsive images, lazy loading)
3. **Handle traffic spikes** (2-5× during flash sales, Black Friday)
4. **Predictable costs** (budget $200-1,000/month, with room for holiday spikes)
5. **99.9%+ uptime** (downtime = lost revenue)

### Nice-to-Have
- Edge compute (for A/B testing product pages, personalization)
- Real-time analytics (monitor flash sales performance)
- Multi-origin failover (primary + backup origins)
- API caching (product catalog, search results)

---

## CDN Selection Analysis

### Option 1: Cloudflare Business (Recommended)

**Pricing**: $200/month (unlimited bandwidth)

**Why Cloudflare Business**:
- ✅ **Unlimited bandwidth** (5TB, 10TB, 15TB during holidays = same $200/month)
- ✅ **Priority support** (phone/email, not just community forums)
- ✅ **Load balancing included** (multi-origin failover, health checks)
- ✅ **Image Optimization** (Polish feature, automatic WebP/AVIF)
- ✅ **50 Page Rules → 125 Page Rules** (more granular cache control)
- ✅ **DDoS protection** (unlimited, protect against attacks during flash sales)

**Cons**:
- ⚠️ **30-second purge** (slower than BunnyCDN 5-10s, but adequate for hourly price updates)
- ⚠️ **Image Resizing costs extra** ($10/month, 10K transformations included)

**Cost Breakdown**:
- Base: $200/month (Business plan, unlimited bandwidth)
- Image Resizing: $10/month (10K transformations, then $1 per 1K)
- Workers: $5/month (for edge A/B testing, personalization)
- **Total**: $215/month

**TCO (5-year)**: $12,900

**When to Use**: Unpredictable traffic (holiday spikes), need unlimited bandwidth safety net

---

### Option 2: BunnyCDN (Cost-Optimized)

**Pricing**: $250-500/month (5TB × $0.05-0.10/GB)

**Why BunnyCDN**:
- ✅ **5-10 second purge** (6× faster than Cloudflare, ideal for price updates)
- ✅ **Optimizer ($9.50/month)**: Image optimization, WAF, edge rules
- ✅ **Cheapest at steady traffic** ($250-500/month vs Cloudflare $200/month = comparable!)
- ✅ **Real-time analytics** (included, monitor flash sales)

**Cons**:
- ⚠️ **Pay-per-GB** (holiday spike to 15TB = $750-1,500/month, unpredictable)
- ⚠️ **No automatic failover** (manual multi-origin configuration)
- ⚠️ **Community SDKs only** (no official support)

**Cost Breakdown**:
- Base: $250-500/month (5TB × $0.05-0.10/GB)
- Optimizer: $9.50/month (image optimization, WAF, edge rules)
- Edge Scripts: $10/month (edge compute, beta)
- **Total**: $270-520/month (steady), **$770-1,520/month (holiday spike to 15TB)**

**TCO (5-year)**: $16,200-31,200 (steady) + holiday spikes

**When to Use**: Traffic predictable (<10TB/month), need 5-10s purge (vs Cloudflare 30s)

**Risk**: Holiday traffic spike (15TB) = $750-1,500/month (vs Cloudflare $200/month unlimited)

---

### Option 3: AWS CloudFront + Cloudinary

**Pricing**: $425/month (CloudFront) + $249/month (Cloudinary) = $674/month

**Why This Combo**:
- ✅ **AWS CloudFront**: 450+ PoPs, S3 integration, Lambda@Edge
- ✅ **Cloudinary**: Automatic image optimization (WebP/AVIF, responsive, transformations)
- ✅ **Separation of concerns**: CloudFront for HTML/CSS/JS, Cloudinary for images/video

**Cons**:
- ⚠️ **More expensive** ($674/month vs Cloudflare $200/month)
- ⚠️ **Complex setup** (two CDNs to manage)
- ⚠️ **Slow CloudFront purge** (10-60 seconds)

**Cost Breakdown**:
- CloudFront: $425/month (5TB × $0.085/GB)
- Cloudinary Advanced: $249/month (500GB storage + 500GB bandwidth + transformations)
- **Total**: $674/month

**TCO (5-year)**: $40,440

**When to Use**: AWS-heavy workload + need best-in-class image optimization

---

## Recommended Architecture: Cloudflare Business

**Choice**: Cloudflare Business ($200/month) + Image Resizing ($10/month)

**Architecture**:
```
User → Cloudflare Business (310+ PoPs)
         ↓
    Static Assets (CSS, JS) → Cache 1 month
    Product Images → Image Resizing → Cache 1 week
    Product Pages (HTML) → Cache 1 hour (purge on price update)
    API (Product Catalog) → Cache 5 minutes
         ↓
    Origin (AWS ALB) → Primary (US-East)
                    → Failover (US-West)
```

**Cache Strategy**:
1. **Static assets** (CSS, JS): 1 month TTL, purge on deployment
2. **Product images**: 1 week TTL, Image Resizing (WebP/AVIF automatic)
3. **Product pages**: 1 hour TTL, purge on price update (hourly)
4. **API responses**: 5 minutes TTL, purge on inventory update

**Purge Strategy** (Hourly Price Updates):
```bash
# Purge specific product pages on price update
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache" \
  -H "Authorization: Bearer {api_token}" \
  -d '{"files":[
    "https://shop.com/products/widget-a",
    "https://shop.com/products/widget-b"
  ]}'

# Purge propagation: 30 seconds (acceptable for hourly updates)
```

**Cost**: $200 (Business) + $10 (Image Resizing) = **$210/month**

**5-Year TCO**: $12,600

---

## Key Recommendation: Cloudflare Business

**Why**:
- ✅ **Unlimited bandwidth** (5TB avg, 15TB holiday spike = same $200/month)
- ✅ **Predictable costs** (no surprise bills during Black Friday traffic spike)
- ✅ **30s purge adequate** (hourly price updates, not real-time stock trading)
- ✅ **Image Resizing** ($10/month, automatic WebP/AVIF)
- ✅ **Priority support** (phone/email for Black Friday emergencies)

**Trade-Off**: 30s purge slower than BunnyCDN (5-10s), but unlimited bandwidth during holidays worth it

---

# Scenario 4: News Site (10TB/month, Real-Time Content)

**Company Profile**: Digital news publisher, breaking news, real-time updates
**Traffic**: 10TB/month egress, 100-500M requests/month
**Budget**: $500-2,000/month for CDN
**Priority**: Instant cache purge (<1 second), real-time analytics, global low latency

---

## Business Context

- **Stage**: Established news publisher (digital-first or traditional with digital arm)
- **Team Size**: 20-50 engineers, 100+ journalists
- **Users**: 5M-20M MAU, 500K-2M daily readers
- **Revenue**: $10M-50M annual (ads, subscriptions)
- **Content Cadence**: 50-200 articles/day, breaking news hourly

### Technical Environment
- **Stack**: WordPress/Ghost + Varnish + PostgreSQL/MySQL
- **Infrastructure**: Multi-cloud or dedicated hosting (Fastly, AWS)
- **Content Types**: Articles (HTML), images, videos, live blogs
- **Traffic Pattern**: Spiky (breaking news = 5-10× traffic surge)
- **Critical Requirement**: Instant cache purge (<1 second) for breaking news

---

## CDN Requirements

### Critical Requirements
1. **Instant cache purge** (<1 second for breaking news, corrections)
2. **Real-time analytics** (monitor article performance, traffic surges)
3. **Real-time log streaming** (send logs to analytics platform, compliance)
4. **Global low latency** (<50ms p95 worldwide, readers everywhere)
5. **99.95%+ uptime** (downtime = lost ad revenue, reader trust)

### Nice-to-Have
- Edge compute (for paywalls, personalization, A/B testing headlines)
- Video streaming (for embedded video, live streams)
- DDoS protection (protect against attacks during controversial stories)

---

## CDN Selection Analysis

### Option 1: Fastly (Recommended for Instant Purge)

**Pricing**: $1,200-1,800/month (10TB × $0.12-0.18/GB + $50 minimum)

**Why Fastly**:
- ✅ **<1 second purge** (instant purge, soft purge, surrogate keys) - **UNIQUE CAPABILITY**
- ✅ **Real-time log streaming** (20+ destinations: Splunk, Datadog, S3, BigQuery, etc.)
- ✅ **Real-time analytics** (included, all plans)
- ✅ **VCL scripting** (custom cache logic, paywalls, A/B testing)
- ✅ **Used by**: Vimeo, New York Times, The Guardian, BuzzFeed

**Cons**:
- ⚠️ **2-5× more expensive** than BunnyCDN ($1,200-1,800 vs $500-1,000/month)
- ⚠️ **Fewer PoPs** (100+ vs 310+ Cloudflare)

**Cost Breakdown**:
- Base: $1,200-1,800/month (10TB × $0.12-0.18/GB + $50 minimum)
- Compute@Edge: Included (pay-per-use)
- Log Streaming: Included (20+ destinations, real-time)
- **Total**: $1,200-1,800/month

**TCO (5-year)**: $72,000-108,000

**When to Use**: Breaking news site, need <1s purge (worth 2-5× premium)

---

### Option 2: Cloudflare Business (Cost-Optimized, Slower Purge)

**Pricing**: $200/month (unlimited bandwidth)

**Why Cloudflare Business**:
- ✅ **Unlimited bandwidth** (10TB, 50TB during breaking news = same $200/month)
- ✅ **310+ PoPs** (better global coverage than Fastly 100+)
- ✅ **Priority support** (phone/email for emergencies)
- ✅ **DDoS protection** (unlimited, protect during controversial stories)

**Cons**:
- ⚠️ **30-second purge** (too slow for breaking news, 30× slower than Fastly)
- ⚠️ **No real-time log streaming** (Logpush $5/month, not as comprehensive as Fastly)

**Cost**: $200/month (Business) + $5/month (Logpush) = $205/month

**TCO (5-year)**: $12,300

**When to Use**: News site where 30s purge acceptable (not breaking news, daily articles)

**Trade-Off**: $205/month vs $1,200-1,800/month (6-9× cheaper), but lose <1s purge

---

### Option 3: Akamai (Enterprise, Lowest Latency)

**Pricing**: $1,000-3,000/month (negotiated, 10TB)

**Why Akamai**:
- ✅ **Lowest latency** (8-18ms p50 globally, 4,100+ PoPs)
- ✅ **Fast purge** (5-30s, Enterprise plans <5s)
- ✅ **99.95%+ SLA** (enterprise-grade uptime)
- ✅ **Used by**: CNN, BBC, Reuters (major news publishers)

**Cons**:
- ⚠️ **Most expensive** ($1,000-3,000/month, negotiated pricing)
- ⚠️ **Slower purge than Fastly** (5s vs <1s)

**Cost**: $1,000-3,000/month (enterprise contract)

**TCO (5-year)**: $60,000-180,000

**When to Use**: Enterprise news publisher, need lowest latency + enterprise SLAs

---

## Recommended Architecture: Fastly

**Choice**: Fastly ($1,200-1,800/month)

**Architecture**:
```
User → Fastly (100+ PoPs)
         ↓
    VCL Logic:
      - Breaking news → Purge <1s (instant purge)
      - Paywall → Edge auth (VCL check)
      - A/B test headlines → VCL routing
         ↓
    Article Cache (1 hour TTL, purge on update)
    Image Cache (1 day TTL)
    Video Streaming (HLS/DASH)
         ↓
    Log Streaming → Datadog, Splunk, S3 (real-time)
         ↓
    Origin (WordPress/Ghost)
```

**Purge Strategy** (Breaking News):
```javascript
// Instant purge via surrogate keys
// Breaking news published → purge <1 second

// VCL configuration
sub vcl_recv {
  # Set surrogate key for article
  set req.http.Surrogate-Key = "article-" + req.url.path;
}

// Purge API call (from CMS on article publish)
curl -X PURGE "https://api.fastly.com/service/{service_id}/purge/article-/breaking-news" \
  -H "Fastly-Key: {api_key}"

// Purge propagation: <1 second (globally)
```

**Log Streaming** (Real-Time):
```
Fastly → Datadog (real-time metrics, article performance)
Fastly → S3 (compliance, long-term storage)
Fastly → BigQuery (analytics, reader behavior)
```

**Cost**: $1,200-1,800/month

**5-Year TCO**: $72,000-108,000

---

## Key Recommendation: Fastly

**Why**:
- ✅ **<1s purge** (instant purge for breaking news, unique capability)
- ✅ **Real-time log streaming** (20+ destinations, included)
- ✅ **VCL scripting** (custom paywalls, A/B testing headlines)
- ✅ **Proven at scale** (NYT, The Guardian, BuzzFeed use Fastly)

**Trade-Off**: 6-9× more expensive than Cloudflare ($1,200-1,800 vs $200/month)

**Worth It?**: Yes, if breaking news is core business (instant purge = competitive advantage)

**Alternative**: Cloudflare Business ($200/month) if 30s purge acceptable (daily news, not breaking)

---

# Scenario 5: Video Platform (50TB/month, Streaming)

**Company Profile**: Video streaming platform (UGC or professional content)
**Traffic**: 50TB/month egress, 500M-1B requests/month
**Budget**: $2,000-10,000/month for CDN
**Priority**: Video streaming optimization, adaptive bitrate, global delivery, cost efficiency

---

## Business Context

- **Stage**: Series B/C video platform ($50M-200M valuation)
- **Team Size**: 100-300 engineers
- **Users**: 1M-10M MAU, 100K-1M daily video views
- **Revenue**: $5M-50M annual (ads, subscriptions, creator payouts)
- **Content**: 100K-1M videos, 10TB-100TB video storage

### Technical Environment
- **Stack**: React + Node.js + FFmpeg transcoding + S3/GCS storage
- **Infrastructure**: Multi-cloud (AWS S3, GCP Cloud Storage)
- **Video Formats**: MP4, HLS, DASH (adaptive bitrate streaming)
- **Traffic Pattern**: 50TB/month avg, 100TB during viral videos
- **Critical Requirements**: Low buffering, adaptive bitrate, global delivery

---

## CDN Requirements

### Critical Requirements
1. **Video streaming optimization** (HLS/DASH adaptive bitrate, low buffering)
2. **High throughput** (1-5 Gbps per connection, 4K video support)
3. **Global delivery** (low latency worldwide, <100ms p95)
4. **Cost efficiency** (50TB/month = $500-5,000/month, need competitive pricing)
5. **Storage + CDN integration** (S3/GCS origin, or CDN-native storage)

### Nice-to-Have
- Edge compute (for video thumbnail generation, watermarking)
- Real-time analytics (monitor video performance, buffering rates)
- DRM support (content protection for premium videos)

---

## CDN Selection Analysis

### Option 1: Cloudflare Stream + R2 (Recommended for Cost)

**Pricing**: $750/month (R2) + $200/month (Business) = $950/month

**Why Cloudflare R2**:
- ✅ **Zero egress fees** (R2 $0/GB egress vs S3 $0.085/GB = massive savings)
- ✅ **Cloudflare Stream**: Video hosting + encoding + adaptive bitrate ($5 per 1K minutes stored)
- ✅ **Unlimited bandwidth** (50TB, 100TB = same $200/month for CDN)

**Cost Breakdown**:
- R2 Storage: $15/month (1TB storage × $0.015/GB)
- R2 Egress: **$0** (zero egress fees!)
- Cloudflare Business: $200/month (unlimited bandwidth)
- Cloudflare Stream: $500/month (100K minutes × $5 per 1K minutes stored)
- **Total**: $715/month (if use Cloudflare Stream) OR $215/month (if DIY video hosting with R2)

**TCO (5-year)**: $12,900 (DIY with R2) to $42,900 (Cloudflare Stream)

**When to Use**: Cost-conscious, want zero egress fees, willing to use Cloudflare ecosystem

---

### Option 2: AWS CloudFront + S3 (AWS Ecosystem)

**Pricing**: $4,250/month (CloudFront) + $230/month (S3) = $4,480/month

**Why CloudFront + S3**:
- ✅ **Deep AWS integration** (S3 origin, Lambda@Edge, MediaConvert for transcoding)
- ✅ **450+ PoPs** (excellent global coverage)
- ✅ **Proven at scale** (Netflix, Hulu, Twitch use AWS for video)

**Cons**:
- ⚠️ **Expensive** ($4,480/month vs Cloudflare $215/month = 21× more expensive!)
- ⚠️ **Egress fees** (S3 → CloudFront = $0.085/GB)

**Cost Breakdown**:
- CloudFront: $4,250/month (50TB × $0.085/GB)
- S3 Storage: $230/month (10TB × $0.023/GB)
- S3 Egress: Included (S3 → CloudFront free in same region)
- **Total**: $4,480/month

**TCO (5-year)**: $268,800

**When to Use**: AWS-heavy workload, need MediaConvert transcoding, Lambda@Edge processing

**Trade-Off**: 21× more expensive than Cloudflare R2 ($4,480 vs $215/month)

---

### Option 3: Fastly + S3/GCS (Streaming Optimized)

**Pricing**: $6,000-9,000/month (Fastly) + $230/month (S3) = $6,230-9,230/month

**Why Fastly**:
- ✅ **Streaming-optimized** (HTTP streaming, low latency, used by Vimeo)
- ✅ **1-5 Gbps throughput** (high-quality 4K streaming)
- ✅ **Real-time log streaming** (monitor video performance, buffering rates)
- ✅ **VCL scripting** (custom video routing, geo-blocking, DRM)

**Cons**:
- ⚠️ **Most expensive** ($6,230-9,230/month vs Cloudflare $215/month = 29-43× more expensive!)

**Cost Breakdown**:
- Fastly: $6,000-9,000/month (50TB × $0.12-0.18/GB)
- S3 Storage: $230/month (10TB × $0.023/GB)
- S3 Egress: $4,250/month (50TB × $0.085/GB to Fastly)
- **Total**: $10,480-13,480/month (with S3 egress) OR $6,000-9,000/month (if use GCS + zero egress)

**TCO (5-year)**: $360,000-540,000

**When to Use**: Premium video platform, need lowest buffering rate, Vimeo-level quality

---

### Option 4: BunnyCDN Stream (Best Value)

**Pricing**: $2,500-5,000/month (BunnyCDN) + $100/month (Storage Zones) = $2,600-5,100/month

**Why BunnyCDN Stream**:
- ✅ **Video-optimized** (adaptive bitrate, HLS/DASH encoding)
- ✅ **Cheapest paid option** ($0.05-0.10/GB, 21× cheaper than Fastly)
- ✅ **Storage Zones**: $0.01/GB storage (10× cheaper than S3 $0.023/GB)
- ✅ **Built-in transcoding** (automatic HLS/DASH encoding)

**Cons**:
- ⚠️ **Fewer PoPs** (123 vs 450+ CloudFront)
- ⚠️ **Community SDKs only** (no official support)

**Cost Breakdown**:
- BunnyCDN Bandwidth: $2,500-5,000/month (50TB × $0.05-0.10/GB)
- Storage Zones: $100/month (10TB × $0.01/GB)
- BunnyCDN Stream (encoding): $0.005 per minute (500K minutes = $2,500/month)
- **Total**: $2,600-5,100/month (bandwidth + storage) + $2,500/month (encoding) = $5,100-7,600/month

**TCO (5-year)**: $156,000-228,000 (with encoding) OR $156,000 (if DIY encoding)

**When to Use**: Cost-conscious video platform, need built-in encoding, acceptable quality

---

## Recommended Architecture: Cloudflare R2 + Business

**Choice**: Cloudflare R2 (zero egress) + Cloudflare Business ($200/month)

**Architecture**:
```
User → Cloudflare Business (310+ PoPs)
         ↓
    Video Delivery:
      - HLS/DASH adaptive bitrate
      - Cache video segments (1 week TTL)
      - Range requests (HTTP 206 for seeking)
         ↓
    Cloudflare R2 (zero egress)
      - 10TB video storage ($150/month)
      - $0 egress fees (save $4,250/month vs S3!)
         ↓
    Origin (Transcoding Service)
      - FFmpeg transcoding (HLS/DASH encoding)
      - Upload to R2
```

**Cost**: $150 (R2 storage) + $200 (Cloudflare Business) = **$350/month**

**Savings vs AWS**: $4,480 (AWS) - $350 (Cloudflare) = **$4,130/month savings** = **$49,560/year** = **$247,800 over 5 years!**

**5-Year TCO**: $21,000 (Cloudflare R2 + Business)

---

## Key Recommendation: Cloudflare R2 + Business

**Why**:
- ✅ **Zero egress fees** (R2 $0/GB vs S3 $0.085/GB = $4,250/month savings)
- ✅ **Unlimited bandwidth** (50TB, 100TB = same $200/month CDN)
- ✅ **310+ PoPs** (better coverage than Fastly 100+)
- ✅ **Cost**: $350/month vs AWS $4,480/month (13× cheaper!)

**Trade-Off**: Vendor lock-in (R2 not S3-compatible, migration harder)

**Alternative**: BunnyCDN Stream ($5,100-7,600/month) if need built-in transcoding + avoid Cloudflare lock-in

**Avoid**: AWS CloudFront + S3 ($4,480/month) unless deep in AWS ecosystem (MediaConvert, Lambda@Edge required)

---

# Summary: All 5 Scenarios

| Scenario | Traffic/Month | Recommended CDN | Monthly Cost | 5-Year TCO | Key Reason |
|----------|---------------|-----------------|--------------|------------|------------|
| **1. Startup MVP** | 10-100GB | Cloudflare Free | **$0** | **$0** | Unlimited free bandwidth |
| **2. Growing SaaS** | 1TB | Cloudflare Pro | **$20** | **$1,200** | Unlimited bandwidth, real-time analytics |
| **3. E-Commerce** | 5TB (10TB holidays) | Cloudflare Business | **$210** | **$12,600** | Unlimited bandwidth (handles spikes), Image Resizing |
| **4. News Site** | 10TB | Fastly | **$1,200-1,800** | **$72,000-108,000** | <1s purge (breaking news), real-time logs |
| **5. Video Platform** | 50TB | Cloudflare R2 + Business | **$350** | **$21,000** | Zero egress fees (R2), 13× cheaper than AWS |

**Key Insights**:
- **Cloudflare dominates** Scenarios 1-3 (free tier + unlimited bandwidth)
- **Fastly wins** Scenario 4 (<1s purge for breaking news, worth premium)
- **Cloudflare R2 wins** Scenario 5 (zero egress fees = massive video savings)
- **AWS CloudFront** only if deep in AWS ecosystem (not cost-competitive otherwise)

---

**Last Updated**: November 12, 2025
**Next Phase**: S4 Strategic (positioning frameworks, vendor viability, 5-year outlook)
