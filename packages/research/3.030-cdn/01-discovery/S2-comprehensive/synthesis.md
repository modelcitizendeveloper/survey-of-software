# S2 Comprehensive: Synthesis

**Cross-Cutting Insights**: Decision frameworks, trade-off analysis, provider positioning
**Data Sources**: Feature matrix, pricing TCO, performance benchmarks, geographic coverage, integration ecosystem
**Last Updated**: November 12, 2025

---

## Executive Summary: Provider Positioning

| Provider | Sweet Spot | Cost Range (1TB/month) | Key Strengths | Key Weaknesses | Best For |
|----------|------------|------------------------|---------------|----------------|----------|
| **Cloudflare** | 0GB → 10TB/month (free tier) | **$0** (Free) → $20/month (Pro) | Unlimited free bandwidth, 310+ PoPs, DDoS protection | 24h analytics delay (Free), 30s purge (slowest) | Free tier, unpredictable traffic, budget-constrained |
| **BunnyCDN** | 100GB → 100TB/month (cost-focused) | **$50-100/month** | Cheapest paid ($5-10/TB), 5-10s purge, transparent pricing | 123 PoPs (fewer than competitors), no webhooks, community SDKs | Cost-conscious, predictable traffic, linear scaling |
| **AWS CloudFront** | Any scale (AWS ecosystem) | **$85/month** (1TB) | 450+ PoPs, deep AWS integration (S3, Lambda, CloudWatch), free tier (1TB/12mo) | More expensive than BunnyCDN, 10-60s purge, no ESI | AWS-heavy workloads, S3 origin, Lambda@Edge needs |
| **Fastly** | 1TB+ (real-time apps) | **$170-230/month** | <1s purge (instant, unique), real-time logs, VCL scripting, Shopify's CDN | $50 minimum (expensive for <100GB), 2-5× more expensive than BunnyCDN | Real-time apps, news sites, instant purge required |
| **Akamai** | 10TB+ (enterprise) | **$500-2,000/month** | 4,100+ PoPs (most), 8-18ms latency (fastest), 99.9%+ SLA, enterprise support | Most expensive, enterprise pricing (no transparency), overkill for <10TB | Fortune 500, mission-critical, lowest latency, enterprise SLAs |
| **Cloudinary** | Media sites (any scale) | **$0** (Free) → $89/month (Plus) | Media-specific (image/video), automatic format conversion (WebP/AVIF), transformations | Not a general CDN, 35ms latency (slowest), overage charges | Image/video sites, media transformation, adaptive bitrate streaming |

**Key Insight**: No universal winner - choice depends on traffic volume, budget, technical requirements, and ecosystem lock-in.

---

## Decision Framework 1: Traffic Volume & Budget

### Traffic-Based Recommendations

#### 0-10GB/month (Small Site: Blog, Portfolio, Documentation)

**Winner**: Cloudflare Free
- **Cost**: $0 (unlimited bandwidth)
- **Performance**: 22ms p50 latency (excellent for free)
- **Trade-offs**: 24-hour analytics delay, 30-second purge
- **TCO (5-year)**: $0

**Runner-Up**: Cloudinary Free (media-specific sites)
- **Cost**: $0 (25GB bandwidth + 25GB storage)
- **Performance**: Automatic image optimization (WebP/AVIF)
- **TCO (5-year)**: $0

**Avoid**: Fastly ($50/month minimum = $3,000 over 5 years for 10GB)

---

#### 10GB-100GB/month (Growing Site: Small SaaS, E-Commerce, API)

**Winner**: Cloudflare Free (still free!)
- **Cost**: $0 (unlimited bandwidth)
- **Performance**: 22ms p50 latency, 95-98% cache hit rate
- **Upgrade Path**: Cloudflare Pro ($20/month) if need real-time analytics
- **TCO (5-year)**: $0 (Free) or $1,200 (Pro)

**Best Paid Option**: BunnyCDN
- **Cost**: $5-10/month (100GB × $0.05-0.10/GB)
- **Performance**: 28ms p50 latency, 5-10s purge (faster than Cloudflare)
- **TCO (5-year)**: $300-600

**Avoid**: Fastly ($62/month = $3,720 over 5 years, 6-12× more expensive than BunnyCDN)

---

#### 100GB-1TB/month (Mid-Size Site: Mid-Market SaaS, High-Traffic E-Commerce)

**Winner**: Cloudflare Free or Pro
- **Cost**: $0 (Free) or $20/month (Pro with real-time analytics)
- **Performance**: 22ms p50 latency, unlimited bandwidth
- **TCO (5-year)**: $0 (Free) or $1,200 (Pro)

**Best Paid Option**: BunnyCDN
- **Cost**: $50-100/month (1TB × $0.05-0.10/GB)
- **Performance**: 28ms p50 latency, 94-97% cache hit rate
- **TCO (5-year)**: $3,000-6,000

**When to Choose AWS CloudFront**: If deep in AWS ecosystem (S3 origin, Lambda@Edge, CloudWatch)
- **Cost**: $85/month (1TB)
- **TCO (5-year)**: $5,100

**When to Choose Fastly**: If need instant purge (<1 second) for real-time apps
- **Cost**: $170-230/month
- **TCO (5-year)**: $10,200-13,800 (2-3× more expensive than BunnyCDN, worth it for instant purge?)

---

#### 1TB-10TB/month (High-Traffic Site: Major SaaS, Video Streaming, Global API)

**Winner**: BunnyCDN
- **Cost**: $500-1,000/month (10TB × $0.05-0.10/GB)
- **Performance**: 28ms p50 latency, linear pricing
- **TCO (5-year)**: $30,000-60,000

**When to Choose Cloudflare Business**: If need priority support
- **Cost**: $200/month (unlimited bandwidth)
- **TCO (5-year)**: $12,000 (5× cheaper than BunnyCDN at 10TB!)

**When to Choose AWS CloudFront**: If AWS-heavy workload
- **Cost**: $850/month (10TB)
- **TCO (5-year)**: $51,000

**When to Choose Fastly**: If real-time requirements (instant purge, live sports, news)
- **Cost**: $1,200-1,800/month
- **TCO (5-year)**: $72,000-108,000

**When to Choose Akamai**: If need enterprise SLA, lowest latency (8-18ms p50)
- **Cost**: $500-2,000/month (negotiated)
- **TCO (5-year)**: $30,000-120,000

---

#### 10TB+/month (Enterprise: Fortune 500, Global Video Platform, Massive API)

**Winner**: Cloudflare Enterprise or Akamai
- **Cloudflare Enterprise**: $2,000-5,000/month (99.95% SLA, dedicated support, unlimited bandwidth)
  - **TCO (5-year)**: $120,000-300,000
- **Akamai**: $500-2,000/month (negotiated, 4,100+ PoPs, 8-18ms latency, enterprise SLAs)
  - **TCO (5-year)**: $30,000-120,000 (volume discounts)

**Cost-Conscious Option**: BunnyCDN (still cheapest at scale)
- **Cost**: $5,000-10,000/month (100TB × $0.05-0.10/GB)
- **TCO (5-year)**: $300,000-600,000

**When to Choose Fastly**: If real-time critical (news, stock trading, live events)
- **Cost**: $12,000-18,000/month (100TB × $0.12-0.18/GB)
- **TCO (5-year)**: $720,000-1,080,000

---

## Decision Framework 2: Feature Requirements

### Critical Feature: Instant Cache Purge (<1 Second)

**Only Option**: Fastly
- **Purge Speed**: <1 second (soft purge, surrogate keys)
- **Use Cases**: News sites, live sports, stock tickers, real-time APIs
- **Cost Premium**: 2-5× more expensive than BunnyCDN
- **Worth It?**: Yes, if purge speed is business-critical (breaking news, price updates)

**Alternatives** (if <1s not required):
- BunnyCDN: 5-10 seconds (6× faster than Cloudflare, adequate for e-commerce)
- Cloudflare: ~30 seconds (adequate for blogs, most sites)

---

### Critical Feature: Free Tier (Unpredictable Traffic)

**Winner**: Cloudflare Free
- **Bandwidth**: Unlimited (no caps)
- **Features**: DDoS protection, SSL, 100 Page Rules, 310+ PoPs
- **Limitations**: 24-hour analytics delay, 30-second purge
- **Use Cases**: MVP, startups, personal blogs, open-source projects

**Runner-Up**: AWS CloudFront Free Tier (12 months only)
- **Bandwidth**: 1TB/month (12 months, new AWS accounts)
- **Features**: Standard CloudFront features, free SSL
- **Expiration**: After 12 months, switches to pay-per-use ($0.085/GB)

---

### Critical Feature: Lowest Latency (Global)

**Winner**: Akamai
- **Latency**: 8-18ms p50 (fastest globally)
- **PoPs**: 4,100+ servers (most extensive network)
- **Cost**: $500-2,000/month (enterprise pricing)
- **Use Cases**: Mission-critical apps, Fortune 500, lowest latency required

**Runner-Up**: Fastly
- **Latency**: 10-20ms p50 (excellent, despite fewer PoPs)
- **PoPs**: 100+ (strategic placement)
- **Cost**: $170-230/month (1TB)

---

### Critical Feature: Edge Compute (Mature)

**Winner**: Cloudflare Workers
- **Runtime**: JavaScript, Rust, C/C++ (WASM)
- **Storage**: Workers KV ($5/month), Durable Objects
- **Cost**: $5/month (10M requests)
- **Ecosystem**: Largest (10M+ websites using Workers)
- **Use Cases**: A/B testing, auth, edge redirects, personalization

**Runner-Up**: Fastly Compute@Edge
- **Runtime**: WASM (Rust, Go, JavaScript, C, etc.)
- **Cost**: Pay-per-use (included with plans)
- **Use Cases**: Complex edge logic, streaming, custom VCL replacement

---

### Critical Feature: Media Optimization (Images/Video)

**Winner**: Cloudinary
- **Automatic Transformations**: WebP/AVIF, adaptive bitrate, lazy loading
- **Cost**: $0 (Free) → $89/month (Plus)
- **Use Cases**: Image-heavy sites, video streaming, media sharing
- **Advantage**: Built-in (no custom edge functions required)

**DIY Alternatives**:
- Cloudflare Image Resizing ($5-10/month) + Workers
- BunnyCDN Optimizer ($9.5/month)
- AWS CloudFront + Lambda@Edge (custom)

---

### Critical Feature: Real-Time Analytics & Logs

**Winner**: Fastly
- **Analytics**: Real-time (all plans)
- **Log Streaming**: 20+ destinations (Splunk, Datadog, S3, BigQuery, etc.)
- **Cost**: Included (no extra fees)
- **Use Cases**: Monitoring, debugging, compliance, real-time dashboards

**Runner-Up**: BunnyCDN
- **Analytics**: Real-time (all plans)
- **Log Streaming**: Log Engine ($10/month)
- **Cost**: $10/month (cheaper than Cloudflare $5/month Logpush)

**Avoid**: Cloudflare Free (24-hour analytics delay, real-time requires $20/month Pro)

---

### Critical Feature: AWS Ecosystem Integration

**Winner**: AWS CloudFront
- **Integration**: S3 (OAI), Lambda@Edge, CloudWatch, Route 53, ACM, CloudFormation
- **Cost**: $85/month (1TB)
- **Use Cases**: AWS-heavy workloads, S3 origin, Lambda@Edge functions
- **Advantage**: Seamless AWS integration (boto3, Terraform AWS provider)

**Alternative**: Cloudflare + R2 (if want to avoid AWS)
- **R2**: $0 egress fees (vs $0.085/GB for S3 + CloudFront)
- **Cost**: $15/month (1TB storage) + $0 egress = $15/month (vs $108/month for S3 + CloudFront)

---

## Decision Framework 3: Geographic Coverage

### If Your Users Are Primarily In...

**North America**: Any CDN adequate (even Fastly 40 PoPs sufficient)
- **Best**: Akamai (1,200+ PoPs, Tier 2/3 cities)
- **Best Free**: Cloudflare (110+ PoPs)
- **Best Cost**: BunnyCDN (45+ PoPs, $5-10/TB)

**Europe**: Any CDN adequate
- **Best**: Akamai (1,500+ PoPs)
- **Best Free**: Cloudflare (100+ PoPs, GDPR-compliant)
- **Best Cost**: BunnyCDN (50+ PoPs)

**Asia-Pacific**: Larger CDNs recommended (Akamai, AWS, Cloudflare)
- **Best**: Akamai (1,000+ PoPs)
- **Best Free**: Cloudflare (70+ PoPs)
- **Avoid**: BunnyCDN/Fastly (20 PoPs = 50-100ms latency increase)

**South America**: Akamai, AWS CloudFront, Cloudflare only
- **Best**: Akamai (200+ PoPs)
- **Best Free**: Cloudflare (15+ PoPs)
- **Avoid**: Fastly (3 PoPs), BunnyCDN (5 PoPs)

**Africa**: Akamai or Cloudflare only
- **Best**: Akamai (150+ PoPs)
- **Only Free Option**: Cloudflare (10+ PoPs)
- **Avoid**: All others (1-10 PoPs, 100-300ms latency)

**Middle East**: Akamai or AWS CloudFront
- **Best**: Akamai (50+ PoPs)
- **Runner-Up**: AWS CloudFront (10+ PoPs)
- **Avoid**: Fastly/BunnyCDN (1 PoP = 100-200ms latency)

**Global (Multi-Region)**: Akamai, Cloudflare, AWS CloudFront
- **Best**: Akamai (4,100+ PoPs, best global coverage)
- **Best Free**: Cloudflare (310+ PoPs, 120+ countries)
- **Best AWS**: AWS CloudFront (450+ PoPs)

---

## Trade-Off Analysis

### Trade-Off 1: Cost vs Performance

**Cheapest (BunnyCDN)** vs **Fastest (Akamai)**:
- BunnyCDN: $50-100/month (1TB), 28ms p50 latency, 123 PoPs
- Akamai: $500-2,000/month (1TB), 14ms p50 latency, 4,100+ PoPs
- **Cost Difference**: 5-20× more expensive
- **Latency Improvement**: 14ms faster (50% reduction)
- **Worth It?**: Only if latency is business-critical (milliseconds matter for high-frequency trading, gaming, etc.)

**Sweet Spot**: Cloudflare Free ($0) or BunnyCDN ($50-100/month) for 99% of use cases

---

### Trade-Off 2: Free Tier Generosity vs Features

**Cloudflare Free** vs **Cloudflare Pro**:
- Free: Unlimited bandwidth, 24h analytics delay, 30s purge, no WAF
- Pro ($20/month): Real-time analytics, WAF ($20 extra), Image Resizing ($5-10/month)
- **Cost Difference**: $240/year (Pro) + $60-120/year (add-ons) = $300-360/year
- **Value**: Real-time analytics worth $240/year if monitoring critical

**Worth It?**: Upgrade to Pro when traffic >100GB/month OR real-time analytics required

---

### Trade-Off 3: Instant Purge (Fastly) vs Cost (BunnyCDN)

**Fastly (<1s purge)** vs **BunnyCDN (5-10s purge)**:
- Fastly: $170-230/month (1TB), <1 second purge, real-time logs
- BunnyCDN: $50-100/month (1TB), 5-10 second purge, real-time analytics
- **Cost Difference**: 2-5× more expensive ($120-130/month premium)
- **Purge Speed Improvement**: 5-10 seconds faster (instant vs near-instant)
- **Worth It?**: Only if <1s purge is business-critical (news sites, stock tickers, live sports)

**Sweet Spot**: BunnyCDN (5-10s purge adequate for 99% of use cases, including e-commerce price updates)

---

### Trade-Off 4: Edge Compute Maturity (Cloudflare) vs Real-Time Logs (Fastly)

**Cloudflare Workers** vs **Fastly Compute@Edge + Logs**:
- Cloudflare: $5/month (Workers), Workers KV, largest ecosystem, Logpush $5/month (Enterprise)
- Fastly: Pay-per-use (Compute@Edge included), real-time log streaming (20+ destinations, included)
- **Cost Difference**: Cloudflare cheaper ($10/month for Workers + Logpush) vs Fastly ($50 minimum + bandwidth)
- **Feature Difference**: Cloudflare has Workers KV (edge storage), Fastly has native log streaming

**Trade-Off**: Cloudflare for edge compute maturity (Workers KV, Durable Objects), Fastly for logging + real-time requirements

---

### Trade-Off 5: AWS Ecosystem (CloudFront) vs Zero Egress (Cloudflare R2)

**AWS S3 + CloudFront** vs **Cloudflare R2 + Cloudflare CDN**:
- AWS: $23 (1TB S3 storage) + $850 (10TB egress) = **$873/month**
- Cloudflare: $15 (1TB R2 storage) + $0 (egress) = **$15/month**
- **Cost Difference**: 58× cheaper ($858/month savings!)
- **Trade-Off**: AWS ecosystem lock-in (Lambda, CloudWatch, etc.) vs vendor lock-in (Cloudflare R2)

**Worth It?**: If NOT heavily invested in AWS, Cloudflare R2 is massively cheaper (zero egress fees)

---

## Provider Positioning Matrix

### 2×2 Matrix: Cost vs Features

```
         High Features
              │
              │   Akamai (Enterprise)
              │   ├─ 4,100+ PoPs
              │   ├─ 8-18ms latency
              │   └─ Enterprise SLAs
              │
              │   Fastly (Real-Time)
              │   ├─ <1s purge
              │   ├─ Real-time logs
              │   └─ VCL scripting
              │
High Cost ────┼──────────────────── Low Cost
              │
              │   Cloudflare (Balanced)
              │   ├─ Unlimited bandwidth
              │   ├─ Workers KV
              │   └─ 310+ PoPs
              │
              │   BunnyCDN (Cost-Focused)
              │   ├─ $5-10/TB
              │   ├─ 123 PoPs
              │   └─ Simple features
              │
         Low Features
```

**Quadrants**:
1. **High Cost, High Features**: Akamai (enterprise), Fastly (real-time)
2. **Low Cost, High Features**: Cloudflare (free tier with 310+ PoPs, Workers)
3. **Low Cost, Low Features**: BunnyCDN (cheapest paid, basic features)
4. **High Cost, Low Features**: None (no CDN occupies this quadrant)

**Insight**: Cloudflare dominates "Low Cost, High Features" quadrant (best value)

---

## Critical Insights (Top 10)

### 1. Cloudflare Free Tier is Unbeatable (0GB → 10TB/month)

**Finding**: Cloudflare Free supports unlimited bandwidth, even at 10TB/month ($0 vs $500-1,000 for BunnyCDN)
- **Limitation**: 24-hour analytics delay, 30-second purge
- **Recommendation**: Start with Cloudflare Free, upgrade to Pro ($20/month) when need real-time analytics

---

### 2. BunnyCDN is Cheapest Paid Option (2-5× Cheaper)

**Finding**: BunnyCDN $5-10/TB vs Fastly $120-180/TB (12-36× cheaper) or Akamai $50-200/TB (5-40× cheaper)
- **Trade-Off**: Fewer PoPs (123 vs 4,100 Akamai), no webhooks, community SDKs
- **Recommendation**: BunnyCDN for cost-conscious, predictable traffic (100GB → 100TB/month)

---

### 3. Fastly is Only CDN with <1 Second Purge

**Finding**: Fastly <1s purge vs BunnyCDN 5-10s, Cloudflare 30s, AWS 10-60s
- **Use Case**: Real-time apps (news, live sports, stock tickers, breaking news)
- **Cost Premium**: 2-5× more expensive than BunnyCDN
- **Recommendation**: Only choose Fastly if <1s purge is business-critical

---

### 4. Akamai Has Lowest Latency (8-18ms p50)

**Finding**: Akamai 8-18ms vs Fastly 10-20ms, Cloudflare 15-25ms, BunnyCDN 20-35ms
- **PoPs**: 4,100+ servers (41× more than Fastly 100+)
- **Cost**: $500-2,000/month (5-20× more expensive than BunnyCDN)
- **Recommendation**: Akamai for enterprise, mission-critical, lowest latency required

---

### 5. Cloudflare R2 Eliminates Egress Fees (58× Cheaper than S3 + CloudFront)

**Finding**: R2 $15/month (1TB storage + 10TB egress) vs S3 + CloudFront $873/month
- **Savings**: $858/month ($10,296/year, $51,480 over 5 years!)
- **Trade-Off**: Vendor lock-in (R2 not S3-compatible for migration)
- **Recommendation**: If NOT invested in AWS, use R2 (massive cost savings)

---

### 6. AWS CloudFront Best for AWS Ecosystem (S3, Lambda, CloudWatch)

**Finding**: CloudFront + S3 OAI, Lambda@Edge, CloudWatch seamless integration
- **Cost**: $85/month (1TB) vs $50-100/month (BunnyCDN)
- **Trade-Off**: More expensive, but AWS ecosystem lock-in worth it if using S3, Lambda, etc.
- **Recommendation**: CloudFront if already using AWS (S3 origin, Lambda@Edge, CloudWatch)

---

### 7. Geographic Coverage Varies 41× (Akamai 4,100 PoPs vs Fastly 100)

**Finding**: Akamai 4,100+ PoPs vs Fastly 100+ PoPs (41× difference)
- **Impact**: Tier 1 cities (all CDNs adequate), Tier 2/3 cities (Akamai 50-100ms faster)
- **Underserved Regions**: Africa (Fastly 1 PoP), South America (Fastly 3 PoPs), Middle East (Fastly 1 PoP)
- **Recommendation**: Akamai or Cloudflare for global coverage (especially Africa, South America)

---

### 8. Edge Compute Maturity: Cloudflare Workers (10M+ Websites)

**Finding**: Cloudflare Workers has largest ecosystem (Workers KV, Durable Objects, 10M+ sites)
- **Cost**: $5/month (10M requests) vs AWS Lambda@Edge $0.60/million (6× cheaper for high volume)
- **Alternatives**: Fastly Compute@Edge (WASM, Rust/Go), AWS CloudFront Functions ($0.10/million)
- **Recommendation**: Cloudflare Workers for mature edge compute (Workers KV, ecosystem), Fastly Compute@Edge for WASM/Rust

---

### 9. Real-Time Analytics: Fastly Includes, Cloudflare Charges $20/month

**Finding**: Fastly real-time analytics + log streaming (included) vs Cloudflare $20/month (Pro) + $5/month (Logpush)
- **Cost Difference**: $300/year (Cloudflare Pro + Logpush) vs $0 (Fastly included)
- **Trade-Off**: Fastly $50 minimum ($600/year) vs Cloudflare Pro $240/year (but Fastly includes logs)
- **Recommendation**: Fastly if real-time analytics + logs critical, Cloudflare Free if 24h delay acceptable

---

### 10. Media Optimization: Cloudinary Built-In vs DIY (Cloudflare, BunnyCDN)

**Finding**: Cloudinary automatic WebP/AVIF, transformations (included) vs Cloudflare Image Resizing ($5-10/month) + Workers
- **Cost**: Cloudinary $0 (Free) → $89/month (Plus) vs Cloudflare $5-15/month (Image Resizing + Workers)
- **Trade-Off**: Cloudinary media-specific (not general CDN) vs Cloudflare general CDN + DIY optimization
- **Recommendation**: Cloudinary for media-heavy sites (automatic transformations), Cloudflare + Workers for DIY

---

## Decision Trees

### Decision Tree 1: Budget-First Approach

```
Start: What's your monthly budget?

├─ $0 (Free)
│  └─ Cloudflare Free (unlimited bandwidth, 310+ PoPs)
│     ├─ Limitation: 24h analytics delay
│     ├─ Limitation: 30s purge
│     └─ Use Case: MVP, startups, personal blogs
│
├─ $5-100/month (Cost-Conscious)
│  └─ BunnyCDN ($5-10/TB)
│     ├─ Strength: Cheapest paid, linear pricing
│     ├─ Limitation: 123 PoPs (fewer than competitors)
│     └─ Use Case: Cost-focused, predictable traffic
│
├─ $100-500/month (Balanced)
│  ├─ AWS CloudFront (if AWS ecosystem)
│  │  ├─ Strength: S3 integration, Lambda@Edge, 450+ PoPs
│  │  ├─ Cost: $85/month (1TB)
│  │  └─ Use Case: AWS-heavy workloads
│  │
│  └─ Fastly (if real-time requirements)
│     ├─ Strength: <1s purge, real-time logs
│     ├─ Cost: $170-230/month (1TB)
│     └─ Use Case: News, live sports, real-time apps
│
└─ $500+/month (Enterprise)
   └─ Akamai
      ├─ Strength: 4,100+ PoPs, 8-18ms latency, enterprise SLAs
      ├─ Cost: $500-2,000/month (negotiated)
      └─ Use Case: Fortune 500, mission-critical
```

---

### Decision Tree 2: Feature-First Approach

```
Start: What's your critical feature?

├─ Instant Purge (<1 second)
│  └─ Fastly (only CDN with <1s purge)
│     └─ Cost: $170-230/month (1TB)
│
├─ Lowest Latency (Global)
│  └─ Akamai (8-18ms p50, 4,100+ PoPs)
│     └─ Cost: $500-2,000/month
│
├─ Free Tier (Unlimited Bandwidth)
│  └─ Cloudflare Free ($0, unlimited bandwidth)
│     └─ Limitation: 24h analytics delay
│
├─ Edge Compute (Mature)
│  └─ Cloudflare Workers ($5/month, Workers KV, Durable Objects)
│     └─ Alternative: Fastly Compute@Edge (WASM, Rust/Go)
│
├─ Media Optimization (Images/Video)
│  └─ Cloudinary ($0 Free → $89/month Plus)
│     └─ Strength: Automatic WebP/AVIF, transformations
│
├─ AWS Ecosystem Integration
│  └─ AWS CloudFront ($85/month for 1TB)
│     └─ Strength: S3 OAI, Lambda@Edge, CloudWatch
│
├─ Real-Time Analytics + Logs
│  └─ Fastly (included, 20+ log destinations)
│     └─ Alternative: BunnyCDN ($10/month Log Engine)
│
└─ Cheapest Paid Option
   └─ BunnyCDN ($5-10/TB, linear pricing)
      └─ Strength: 2-5× cheaper than competitors
```

---

### Decision Tree 3: Geographic Coverage-First

```
Start: Where are your users?

├─ North America (US, Canada)
│  └─ Any CDN adequate (even Fastly 40 PoPs sufficient)
│     ├─ Best Free: Cloudflare (110+ PoPs)
│     └─ Best Cost: BunnyCDN (45+ PoPs)
│
├─ Europe (EU, UK)
│  └─ Any CDN adequate
│     ├─ Best Free: Cloudflare (100+ PoPs, GDPR)
│     └─ Best Cost: BunnyCDN (50+ PoPs)
│
├─ Asia-Pacific (Japan, Singapore, Australia)
│  ├─ Best: Akamai (1,000+ PoPs)
│  ├─ Best Free: Cloudflare (70+ PoPs)
│  └─ Avoid: BunnyCDN/Fastly (20 PoPs = higher latency)
│
├─ South America (Brazil, Argentina)
│  ├─ Best: Akamai (200+ PoPs)
│  ├─ Best Free: Cloudflare (15+ PoPs)
│  └─ Avoid: Fastly (3 PoPs), BunnyCDN (5 PoPs)
│
├─ Africa
│  ├─ Best: Akamai (150+ PoPs)
│  ├─ Only Free: Cloudflare (10+ PoPs)
│  └─ Avoid: All others (1-10 PoPs, 100-300ms latency)
│
└─ Global (Multi-Region)
   ├─ Best: Akamai (4,100+ PoPs, best coverage)
   ├─ Best Free: Cloudflare (310+ PoPs, 120+ countries)
   └─ Best AWS: AWS CloudFront (450+ PoPs)
```

---

## Summary Scorecard (All Providers)

| Category | Cloudflare | BunnyCDN | AWS CloudFront | Fastly | Akamai | Cloudinary |
|----------|------------|----------|----------------|--------|--------|------------|
| **Cost (1TB/month)** | $0-20 (★★★★★) | $50-100 (★★★★★) | $85 (★★★★☆) | $170-230 (★★☆☆☆) | $500-2K (★☆☆☆☆) | $89-289 (★★★☆☆) |
| **Performance (Latency)** | 22ms (★★★★☆) | 28ms (★★★☆☆) | 25ms (★★★★☆) | 18ms (★★★★★) | 14ms (★★★★★) | 35ms (★★☆☆☆) |
| **Purge Speed** | 30s (★★☆☆☆) | 5-10s (★★★★☆) | 10-60s (★★☆☆☆) | <1s (★★★★★) | 5-30s (★★★★☆) | 30-60s (★★☆☆☆) |
| **Geographic Coverage** | 310 PoPs (★★★★★) | 123 PoPs (★★★☆☆) | 450 PoPs (★★★★★) | 100 PoPs (★★★☆☆) | 4,100 PoPs (★★★★★) | 300 PoPs (★★★★☆) |
| **Edge Compute** | Workers (★★★★★) | Edge Scripts (★★☆☆☆) | Lambda@Edge (★★★★☆) | Compute@Edge (★★★★☆) | EdgeWorkers (★★★★☆) | None (★☆☆☆☆) |
| **Integration Ecosystem** | 8.5/10 (★★★★☆) | 5.4/10 (★★☆☆☆) | 9/10 (★★★★★) | 9/10 (★★★★★) | 8.4/10 (★★★★☆) | 8.3/10 (★★★★☆) |
| **Real-Time Analytics** | $20/mo (★★★☆☆) | Included (★★★★★) | 5-min delay (★★★☆☆) | Included (★★★★★) | Included (★★★★★) | Included (★★★★☆) |
| **Free Tier** | Unlimited (★★★★★) | None (★☆☆☆☆) | 1TB/12mo (★★★☆☆) | None (★☆☆☆☆) | None (★☆☆☆☆) | 25GB (★★★☆☆) |

**Overall Winner**: Depends on use case
- **Best Value**: Cloudflare (free tier + features)
- **Best Cost**: BunnyCDN (cheapest paid)
- **Best Performance**: Akamai (lowest latency) or Fastly (instant purge)
- **Best Ecosystem**: AWS CloudFront or Fastly (tie)
- **Best for Media**: Cloudinary

---

## Final Recommendations (By Use Case)

### 1. Startup / MVP (Budget: $0)
→ **Cloudflare Free**
- Unlimited bandwidth, 310+ PoPs, DDoS protection
- Upgrade to Pro ($20/month) when need real-time analytics

### 2. Small SaaS (Budget: $50-100/month, 1TB traffic)
→ **BunnyCDN** ($50-100/month)
- Cheapest paid, 5-10s purge, linear pricing
- Alternative: Cloudflare Free ($0, unlimited bandwidth)

### 3. News Site / Real-Time Content
→ **Fastly** ($170-230/month for 1TB)
- <1s purge (unique), real-time logs, instant updates
- Worth 2-5× premium if purge speed critical

### 4. Video Streaming Platform
→ **Fastly** or **Cloudinary**
- Fastly: HTTP streaming, 1-5 Gbps throughput, used by Vimeo
- Cloudinary: Media-specific, adaptive bitrate, transformations

### 5. E-Commerce Site (Price Updates)
→ **BunnyCDN** ($50-100/month)
- 5-10s purge (adequate for price updates), cheap, reliable
- Alternative: Cloudflare Free (30s purge acceptable)

### 6. AWS-Heavy Application
→ **AWS CloudFront** ($85/month for 1TB)
- S3 OAI, Lambda@Edge, CloudWatch integration
- Worth cost premium for AWS ecosystem lock-in

### 7. Image-Heavy Site (Photography, E-Commerce)
→ **Cloudinary** ($0 Free → $89/month)
- Automatic WebP/AVIF, transformations, responsive images
- Alternative: Cloudflare + Workers (DIY)

### 8. Global Enterprise (Mission-Critical)
→ **Akamai** ($500-2,000/month)
- 8-18ms latency (fastest), 4,100+ PoPs, 99.9%+ SLA
- Worth enterprise pricing for lowest latency + SLAs

### 9. Cost-Conscious Global App
→ **Cloudflare Free** or **BunnyCDN**
- Cloudflare: $0 (unlimited bandwidth, 310+ PoPs)
- BunnyCDN: $50-100/month (linear pricing, 123 PoPs)

### 10. Multi-Cloud Strategy (Avoid AWS Lock-In)
→ **Cloudflare R2** + **Cloudflare CDN**
- $15/month (1TB storage) + $0 egress = $15/month
- vs S3 + CloudFront: $873/month (58× cheaper!)

---

## Next Steps: S2 → S3 Transition

S2 Comprehensive is now complete. The next phase is **S3 Need-Driven**: Business scenarios.

**S3 Deliverables** (5 generic scenarios):
1. **Startup (MVP, <100GB/month)**: Cloudflare Free vs BunnyCDN
2. **Growing SaaS (1TB/month)**: BunnyCDN vs AWS CloudFront vs Cloudflare Pro
3. **E-Commerce (Price Updates, 5TB/month)**: BunnyCDN vs Fastly (purge speed trade-off)
4. **News Site (Real-Time, 10TB/month)**: Fastly vs Akamai (instant purge vs lowest latency)
5. **Video Platform (Streaming, 50TB/month)**: Fastly vs Cloudinary vs Akamai

**Time to complete S2**: ~7 hours (feature matrix 2h, pricing 1.5h, performance 1.5h, geographic 1h, integration 1h)

---

**Last Updated**: November 12, 2025
**Next Phase**: S3 Need-Driven (business scenarios)
