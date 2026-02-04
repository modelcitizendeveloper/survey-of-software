# S2 Comprehensive: Feature Matrix

**Providers Analyzed**: 6 CDN platforms
**Features Compared**: 44 features across 6 categories
**Last Updated**: November 12, 2025

---

## Summary Table

| Provider | PoP Count | Free Tier | Starting Price | Edge Functions | DDoS Protection | Best For |
|----------|-----------|-----------|----------------|----------------|-----------------|----------|
| **Cloudflare** | 310+ | Unlimited bandwidth | $20/month (Pro) | ✅ Workers | ✅ Unlimited | Free tier, global coverage |
| **Fastly** | 100+ | No | $50/month minimum | ✅ Compute@Edge | ✅ Included | Real-time purge, streaming |
| **BunnyCDN** | 123 | No | $1/month + usage | ✅ Edge Scripts | ✅ Included | Cost-efficiency, simplicity |
| **AWS CloudFront** | 450+ | 1TB/month (12 months) | Pay-per-use | ✅ Lambda@Edge | ⚠️ Shield (extra) | AWS ecosystem integration |
| **Akamai** | 4,100+ | No | Enterprise pricing | ✅ EdgeWorkers | ✅ Enterprise-grade | Enterprise, highest PoP count |
| **Cloudinary** | 300+ (via partners) | 25GB storage, 25GB bandwidth | $89/month (Plus) | ⚠️ Limited | ⚠️ Basic | Media optimization (images/video) |

---

## Category 1: Core CDN Features (10 features)

| Feature | Cloudflare | Fastly | BunnyCDN | AWS CloudFront | Akamai | Cloudinary |
|---------|------------|--------|----------|----------------|--------|------------|
| **Global Edge Network (PoP Count)** | 310+ PoPs in 120+ countries | 100+ PoPs | 123 PoPs in 40+ countries | 450+ PoPs | 4,100+ servers globally | 300+ PoPs (via CDN partners) |
| **HTTP/2 Support** | ✅ All plans | ✅ All plans | ✅ All plans | ✅ All plans | ✅ All plans | ✅ All plans |
| **HTTP/3 (QUIC) Support** | ✅ All plans | ✅ All plans | ✅ All plans | ⚠️ Limited regions | ✅ Enterprise | ✅ All plans |
| **IPv6 Support** | ✅ All plans | ✅ All plans | ✅ All plans | ✅ All plans | ✅ All plans | ✅ All plans |
| **Anycast Routing** | ✅ All plans | ✅ All plans | ✅ All plans | ✅ All plans | ✅ All plans | ⚠️ Via partners |
| **Origin Shield / Origin Pull** | ✅ Argo Tiered Cache ($5/month) | ✅ Shielding included | ✅ Optimizer included | ✅ Origin Shield ($0.01/10K) | ✅ Tiered Distribution | ⚠️ Basic |
| **Cache Control Headers Support** | ✅ Full support | ✅ Full support | ✅ Full support | ✅ Full support | ✅ Full support | ✅ Full support |
| **Query String Handling** | ✅ Custom rules | ✅ Custom rules | ✅ Configurable | ✅ Query string forwarding | ✅ Advanced rules | ✅ Automatic optimization |
| **Stale Content Serving (stale-while-revalidate)** | ✅ All plans | ✅ All plans | ✅ All plans | ✅ All plans | ✅ All plans | ⚠️ Limited |
| **Compression (Gzip, Brotli)** | ✅ Brotli + Gzip | ✅ Brotli + Gzip | ✅ Brotli + Gzip | ✅ Brotli + Gzip | ✅ Brotli + Gzip | ✅ Automatic |
| **WebP/AVIF Automatic Format Conversion** | ⚠️ Image Resizing ($5-10/month) | ⚠️ Image Optimizer (extra) | ⚠️ Optimizer ($9.5/month) | ⚠️ CloudFront Functions (extra) | ⚠️ Image Manager (extra) | ✅ Core feature (all plans) |

**Key Insights**:
- **Cloudflare**: Largest free tier, 310+ PoPs, HTTP/3 on all plans
- **Fastly**: Smallest PoP count (100+) but premium performance, real-time capabilities
- **BunnyCDN**: Cost-effective, 123 PoPs, solid core features
- **AWS CloudFront**: Largest PoP count (450+), deep AWS integration
- **Akamai**: Enterprise-grade, 4,100+ edge servers (most of any CDN)
- **Cloudinary**: Specialized for media, automatic WebP/AVIF conversion included

---

## Category 2: Security Features (8 features)

| Feature | Cloudflare | Fastly | BunnyCDN | AWS CloudFront | Akamai | Cloudinary |
|---------|------------|--------|----------|----------------|--------|------------|
| **SSL/TLS Certificates** | ✅ Free Universal SSL (all plans) | ✅ Free Let's Encrypt + custom | ✅ Free Let's Encrypt | ✅ Free via ACM | ✅ Free + custom | ✅ Free SSL |
| **DDoS Protection (L3/L4)** | ✅ Unlimited unmetered (all plans) | ✅ Included (all plans) | ✅ Included (all plans) | ⚠️ AWS Shield Standard (free), Shield Advanced ($3K/month) | ✅ Enterprise-grade (all plans) | ⚠️ Basic (via CDN partners) |
| **Web Application Firewall (WAF)** | ⚠️ $20/month (Pro+) | ⚠️ $50+/month (Next-Gen WAF add-on) | ⚠️ $9.5/month (Perma-Cache+) | ⚠️ $5/month + $1 per million requests | ⚠️ Enterprise (Kona Site Defender) | ❌ Not included |
| **Rate Limiting / Throttling** | ⚠️ $5/month (10K rules) | ✅ Included (VCL rules) | ⚠️ $9.5/month (Perma-Cache+) | ⚠️ CloudFront Functions (extra) | ✅ Included (Enterprise) | ❌ Not included |
| **Bot Management** | ⚠️ $20/month (Pro), $200/month (Bot Management) | ⚠️ $20+/month (Bot Detection add-on) | ❌ Not included | ⚠️ AWS WAF bot rules ($5+/month) | ✅ Bot Manager (Enterprise) | ❌ Not included |
| **Geo-Blocking / Allow-Listing** | ⚠️ $20/month (Pro+) | ✅ Included (VCL rules) | ✅ Included (all plans) | ✅ Included (geographic restrictions) | ✅ Included (all plans) | ⚠️ Limited |
| **Hotlink Protection** | ✅ All plans | ✅ All plans | ✅ All plans | ⚠️ Requires CloudFront Functions | ✅ All plans | ✅ All plans (signed URLs) |
| **Token Authentication / Signed URLs** | ✅ All plans | ✅ All plans | ✅ All plans | ✅ Signed URLs/cookies | ✅ All plans | ✅ All plans |

**Key Insights**:
- **Cloudflare**: Best free DDoS protection (unlimited unmetered on all plans), WAF starts at $20/month
- **Fastly**: VCL scripting allows custom security rules (rate limiting, geo-blocking) without extra cost
- **BunnyCDN**: Geo-blocking included free (rare), hotlink protection standard
- **AWS CloudFront**: Shield Standard free (basic DDoS), Shield Advanced expensive ($3K/month)
- **Akamai**: Enterprise-grade security (Kona Site Defender, Bot Manager) but requires Enterprise plan
- **Cloudinary**: Minimal security features (not a security-focused CDN), signed URLs for media protection

**Security Winner**: Cloudflare (free tier DDoS protection beats most competitors' paid plans)

---

## Category 3: Performance Features (6 features)

| Feature | Cloudflare | Fastly | BunnyCDN | AWS CloudFront | Akamai | Cloudinary |
|---------|------------|--------|----------|----------------|--------|------------|
| **Cache Purge Speed** | ⚠️ ~30 seconds (global) | ✅ <1 second (instant purge) | ⚠️ 5-10 seconds | ⚠️ 10-60 seconds | ⚠️ 5-30 seconds | ⚠️ 30-60 seconds |
| **Cache Key Customization** | ✅ Custom Cache Keys ($5/month Biz+) | ✅ VCL scripting (all plans) | ✅ Cache rules (all plans) | ✅ Query string/header forwarding | ✅ Advanced rules (Enterprise) | ⚠️ Limited (media-specific) |
| **Edge-Side Includes (ESI)** | ⚠️ Workers required ($5/month) | ✅ Native ESI support | ❌ Not supported | ❌ Not supported | ✅ Native ESI support | ❌ Not supported |
| **HTTP Streaming** | ✅ All plans | ✅ All plans (optimized for streaming) | ✅ All plans | ✅ All plans | ✅ All plans | ✅ Video streaming optimized |
| **WebSocket Support** | ✅ All plans | ✅ All plans | ✅ All plans | ⚠️ Custom origin required | ✅ All plans | ❌ Not supported |
| **Connection Pooling / Keep-Alive Optimization** | ✅ Argo Smart Routing ($5/month) | ✅ Included (all plans) | ✅ Included (all plans) | ✅ Included (all plans) | ✅ Included (all plans) | ⚠️ Via CDN partners |

**Key Insights**:
- **Fastly**: Only CDN with <1 second purge (instant purge), native ESI support, VCL scripting for cache customization
- **Cloudflare**: 30-second purge (slowest among major CDNs), Argo Smart Routing ($5/month) optimizes routing
- **BunnyCDN**: 5-10 second purge (faster than Cloudflare), solid performance features for price
- **AWS CloudFront**: 10-60 second purge, no ESI support
- **Akamai**: Enterprise-grade performance, native ESI, advanced cache rules
- **Cloudinary**: Optimized for video streaming, limited general performance features

**Performance Winner**: Fastly (instant purge is unique, critical for real-time applications)

---

## Category 4: Analytics & Monitoring (6 features)

| Feature | Cloudflare | Fastly | BunnyCDN | AWS CloudFront | Akamai | Cloudinary |
|---------|------------|--------|----------|----------------|--------|------------|
| **Real-Time Analytics Dashboard** | ⚠️ $20/month (Pro) for real-time, Free for 24h delay | ✅ Real-time (all plans) | ✅ Real-time (all plans) | ⚠️ CloudWatch (5-minute delay), Real-time extra | ✅ Real-time (all plans) | ✅ Real-time (all plans) |
| **Traffic Analytics (Bandwidth, Requests, Cache Hit Rate)** | ✅ All plans (24h delay on Free) | ✅ All plans | ✅ All plans | ✅ All plans | ✅ All plans | ✅ All plans |
| **Log Streaming / Log Delivery** | ⚠️ $5/month (Logpush, Enterprise) | ✅ Real-time log streaming (all plans) | ⚠️ $10/month (Log Engine) | ✅ Access logs to S3 (free) | ✅ DataStream (all plans) | ⚠️ Limited logs |
| **Custom Metrics / Webhooks** | ⚠️ Workers Analytics ($5/month) | ✅ Custom VCL metrics | ❌ Not supported | ⚠️ CloudWatch custom metrics (extra) | ✅ Custom metrics (Enterprise) | ⚠️ Basic webhooks |
| **Origin Health Monitoring** | ✅ Health Checks ($5/month for advanced) | ✅ Health checks (all plans) | ✅ Health checks (all plans) | ✅ CloudWatch alarms | ✅ Health monitoring (all plans) | ⚠️ Limited |
| **Alerting (Bandwidth Thresholds, Errors)** | ⚠️ $20/month (Notifications on Pro+) | ✅ Custom alerts (all plans) | ✅ Email alerts (all plans) | ✅ CloudWatch alarms (all plans) | ✅ Alerting (all plans) | ⚠️ Basic alerts |

**Key Insights**:
- **Fastly**: Real-time log streaming on all plans (most generous), custom VCL metrics, instant visibility
- **Cloudflare**: Real-time analytics requires $20/month Pro plan (Free tier has 24h delay), Logpush $5/month
- **BunnyCDN**: Real-time analytics included free, log streaming $10/month (competitive)
- **AWS CloudFront**: Access logs to S3 free (good for long-term storage), CloudWatch has 5-minute delay
- **Akamai**: DataStream for real-time logs, enterprise-grade monitoring
- **Cloudinary**: Media-specific analytics (transformations, bandwidth), limited general monitoring

**Analytics Winner**: Fastly (real-time log streaming + custom metrics on all plans, no extra cost)

---

## Category 5: Edge Computing (4 features)

| Feature | Cloudflare | Fastly | BunnyCDN | AWS CloudFront | Akamai | Cloudinary |
|---------|------------|--------|----------|----------------|--------|------------|
| **Edge Functions / Workers / Serverless at Edge** | ✅ Workers ($5/month, 10M requests) | ✅ Compute@Edge (included, pay-per-use) | ✅ Edge Scripts (beta, $10/month) | ✅ Lambda@Edge (pay-per-request), CloudFront Functions ($0.10/million) | ✅ EdgeWorkers (Enterprise, pay-per-use) | ❌ No edge compute |
| **Edge Key-Value Storage** | ✅ Workers KV ($5/month + $0.50/GB) | ⚠️ Edge Dictionary (key-value config, not storage) | ❌ Not supported | ❌ Not supported | ⚠️ EdgeKV (Enterprise) | ❌ Not supported |
| **Edge Redirect Rules** | ✅ Page Rules (3 free, $5 for 50 rules) | ✅ VCL redirects (all plans) | ✅ Edge rules (all plans) | ⚠️ CloudFront Functions required | ✅ Edge redirects (all plans) | ⚠️ Limited redirects |
| **Edge Image Optimization** | ⚠️ Image Resizing ($5-10/month) | ⚠️ Image Optimizer (add-on) | ⚠️ Optimizer ($9.5/month) | ⚠️ Lambda@Edge + third-party | ⚠️ Image Manager (add-on) | ✅ Core feature (all plans) |

**Key Insights**:
- **Cloudflare Workers**: Most mature edge compute platform, Workers KV for edge storage, $5/month for 10M requests
- **Fastly Compute@Edge**: WebAssembly-based (supports Rust, JS, Go), included with plans, pay-per-use
- **BunnyCDN Edge Scripts**: Beta feature, $10/month, JavaScript-based
- **AWS Lambda@Edge**: Powerful but expensive ($0.60 per million requests), CloudFront Functions cheaper ($0.10/million)
- **Akamai EdgeWorkers**: Enterprise-tier, JavaScript runtime, pay-per-use
- **Cloudinary**: No edge compute (not a general CDN), but edge image optimization is core feature

**Edge Compute Winner**: Cloudflare Workers (most mature, best pricing, Workers KV unique for edge storage)

**Specialty Winner**: Cloudinary (image optimization at edge is built-in, no extra cost)

---

## Category 6: Developer Experience (6 features)

| Feature | Cloudflare | Fastly | BunnyCDN | AWS CloudFront | Akamai | Cloudinary |
|---------|------------|--------|----------|----------------|--------|------------|
| **API Quality** | ✅ REST API, well-documented | ✅ REST API, excellent docs | ✅ REST API, simple docs | ✅ AWS API (boto3, SDKs) | ✅ REST API, comprehensive | ✅ REST API, media-focused |
| **Terraform / IaC Support** | ✅ Official provider | ✅ Official provider | ✅ Community provider (good quality) | ✅ AWS provider (official) | ✅ Official provider | ✅ Official provider |
| **CLI Tools** | ✅ Wrangler (Workers), cloudflared | ✅ Fastly CLI | ✅ Bunny CLI (limited) | ✅ AWS CLI | ✅ Akamai CLI | ✅ Cloudinary CLI |
| **SDK Availability** | ✅ Python, Node.js, Go, PHP, .NET | ✅ Python, Ruby, Perl, Go, Node.js | ⚠️ Limited SDKs (community) | ✅ AWS SDKs (all major languages) | ✅ Python, Node.js, Java, Go | ✅ Python, Node.js, Ruby, PHP, Java, .NET |
| **Webhook Support** | ⚠️ Workers required for webhooks | ✅ Log streaming webhooks | ❌ No webhooks | ⚠️ SNS/EventBridge integration | ✅ Webhooks (Enterprise) | ✅ Webhooks (all plans) |
| **Documentation Quality** | ✅ Excellent (tutorials, examples, community) | ✅ Excellent (VCL docs, guides) | ✅ Good (straightforward, limited depth) | ✅ AWS docs (comprehensive, verbose) | ✅ Enterprise-grade docs | ✅ Excellent (media-focused tutorials) |

**Key Insights**:
- **Cloudflare**: Wrangler CLI for Workers, excellent community docs, official SDKs
- **Fastly**: VCL documentation is best-in-class, log streaming webhooks native
- **BunnyCDN**: Simple API, community Terraform provider (not official), limited SDKs
- **AWS CloudFront**: Deep AWS ecosystem integration (boto3, CloudFormation, etc.), verbose docs
- **Akamai**: Enterprise-grade documentation, CLI tools, comprehensive SDKs
- **Cloudinary**: Best media-specific docs (image/video transformation tutorials), webhooks included

**Developer Experience Winner**: Tie between Cloudflare (Workers ecosystem, Wrangler) and AWS (ecosystem breadth)

---

## Feature Completeness Score (44 Features)

| Provider | Core CDN (11) | Security (8) | Performance (6) | Analytics (6) | Edge Compute (4) | Dev Experience (6) | **Total Score** |
|----------|---------------|--------------|-----------------|---------------|------------------|-------------------|-----------------|
| **Cloudflare** | 10/11 (91%) | 8/8 (100%, some paid) | 6/6 (100%) | 6/6 (100%, some paid) | 4/4 (100%) | 6/6 (100%) | **40/44 (91%)** |
| **Fastly** | 10/11 (91%) | 7/8 (88%) | 6/6 (100%) | 6/6 (100%) | 3/4 (75%) | 6/6 (100%) | **38/44 (86%)** |
| **BunnyCDN** | 10/11 (91%) | 6/8 (75%) | 4/6 (67%) | 5/6 (83%) | 2/4 (50%) | 4/6 (67%) | **31/44 (70%)** |
| **AWS CloudFront** | 10/11 (91%) | 7/8 (88%, some paid) | 4/6 (67%) | 6/6 (100%) | 3/4 (75%) | 6/6 (100%) | **36/44 (82%)** |
| **Akamai** | 11/11 (100%) | 8/8 (100%) | 6/6 (100%) | 6/6 (100%) | 3/4 (75%) | 6/6 (100%) | **40/44 (91%)** |
| **Cloudinary** | 8/11 (73%, media-focused) | 3/8 (38%) | 3/6 (50%) | 4/6 (67%) | 1/4 (25%) | 6/6 (100%) | **25/44 (57%)** |

**Notes**:
- Cloudflare and Akamai tie at 91% (40/44 features), but Cloudflare has more features on free/low-cost tiers
- Fastly scores 86% (38/44), strong in performance and analytics
- AWS CloudFront 82% (36/44), weaknesses in performance (no ESI, slow purge)
- BunnyCDN 70% (31/44), cost-effective but missing advanced features (ESI, edge KV, bot management)
- Cloudinary 57% (25/44), specialized for media (not a general CDN)

---

## Cross-Cutting Insights

### 1. Free Tier Generosity

**Best Free Tier**: Cloudflare
- **Unlimited bandwidth** (no caps)
- DDoS protection (unlimited unmetered)
- 100 Page Rules
- SSL certificates
- **Limitation**: 24-hour analytics delay (real-time requires $20/month Pro)

**Runner-Up**: AWS CloudFront
- 1TB bandwidth/month (12 months, new AWS accounts only)
- 10M HTTP/HTTPS requests
- **Limitation**: Expires after 12 months, then pay-per-use

**Others**:
- Fastly: No free tier (minimum $50/month)
- BunnyCDN: No free tier (pay-per-use, ~$1/month minimum)
- Akamai: Enterprise pricing only (no free tier)
- Cloudinary: 25GB storage + 25GB bandwidth (adequate for small sites)

---

### 2. Pricing Model Comparison

| Provider | Pricing Model | Bandwidth Cost (1TB) | Minimum Monthly | Hidden Costs |
|----------|---------------|----------------------|-----------------|--------------|
| **Cloudflare** | Flat-rate tiers | $0 (Free), $20 (Pro) | $0 (Free), $20 (Pro) | Real-time analytics ($20), Workers ($5), Argo ($5) |
| **Fastly** | Pay-per-use | ~$120-180/TB | $50/month | None (transparent) |
| **BunnyCDN** | Pay-per-use | $5-10/TB (region-dependent) | ~$1/month | Optimizer ($9.5), Edge Scripts ($10) |
| **AWS CloudFront** | Pay-per-use | $85/TB (first 10TB) | $0 (pay-per-use) | Shield Advanced ($3K/month), WAF ($5+), Lambda@Edge |
| **Akamai** | Enterprise custom | Negotiated (est. $500-2K/TB) | Enterprise only | None (bundled) |
| **Cloudinary** | Storage + transformations | $89/month (150GB storage, 150GB bandwidth) | $0 (Free), $89 (Plus) | Overage charges ($0.08/GB bandwidth) |

**Key Insights**:
- **Cheapest per GB**: BunnyCDN ($5-10/TB) is 8-18× cheaper than Fastly ($120-180/TB)
- **Best for unpredictable traffic**: Cloudflare Free (unlimited bandwidth)
- **Best for high volume**: BunnyCDN (linear pricing, no tiers)
- **Most expensive**: Akamai (enterprise pricing, negotiated contracts)
- **Most transparent**: Fastly (no hidden fees), BunnyCDN (simple pricing)

---

### 3. Performance Sweet Spots

**Instant Purge Required**: Fastly
- Only CDN with <1 second purge (critical for real-time apps, news sites, live sports)

**Global Low Latency**: Cloudflare, Akamai
- Cloudflare: 310+ PoPs, Argo Smart Routing ($5/month) optimizes
- Akamai: 4,100+ edge servers (most extensive network)

**Video Streaming**: Cloudinary, Fastly
- Cloudinary: Optimized for video delivery, adaptive bitrate streaming
- Fastly: HTTP streaming, low latency, used by Vimeo, New York Times

**Cost-Optimized Performance**: BunnyCDN
- 5-10 second purge (faster than Cloudflare's 30 seconds)
- $5-10/TB bandwidth (cheapest)

---

### 4. Security Posture

**Best Free Security**: Cloudflare
- Unlimited DDoS protection (free tier)
- Free SSL certificates
- Hotlink protection

**Best Paid Security**: Akamai
- Enterprise-grade DDoS mitigation
- Kona Site Defender (WAF)
- Bot Manager

**Security Weaknesses**:
- BunnyCDN: No bot management
- Cloudinary: Minimal security features (not security-focused)
- AWS CloudFront: Shield Advanced is $3K/month (expensive)

---

### 5. Edge Computing Maturity

**Most Mature**: Cloudflare Workers
- 10+ million websites using Workers
- Workers KV (edge storage)
- Wrangler CLI, excellent docs

**Most Flexible**: Fastly Compute@Edge
- WebAssembly runtime (supports Rust, Go, JS)
- Pay-per-use (no base fee)

**Enterprise Edge**: Akamai EdgeWorkers
- JavaScript runtime
- Enterprise SLAs

**Emerging**: BunnyCDN Edge Scripts
- Beta feature ($10/month)
- JavaScript-based

**No Edge Compute**: Cloudinary (not applicable for media CDN)

---

### 6. Developer Ecosystem

**Best Ecosystem**: AWS CloudFront
- Deep AWS integration (S3, Lambda, Route 53, CloudWatch, CloudFormation)
- Extensive SDKs (all major languages)
- Massive community

**Best Tooling**: Cloudflare
- Wrangler CLI (Workers development)
- Terraform provider
- cloudflared tunnels

**Best for DIY**: Fastly
- VCL scripting (Varnish Configuration Language)
- Custom cache logic without Workers/Functions

**Simplest**: BunnyCDN
- Straightforward API
- Minimal configuration required

---

## Decision Framework: Feature Requirements

### If you need...

**Unlimited free tier**: → Cloudflare (unlimited bandwidth, DDoS protection)

**Instant cache purge (<1 second)**: → Fastly (unique capability)

**Lowest cost per GB**: → BunnyCDN ($5-10/TB, 8-18× cheaper than Fastly)

**Most PoPs (global coverage)**: → Akamai (4,100+ servers) or AWS CloudFront (450+ PoPs)

**Best free DDoS protection**: → Cloudflare (unlimited unmetered, all plans)

**Real-time analytics (free)**: → Fastly, BunnyCDN (Cloudflare requires $20/month Pro)

**Edge compute (mature)**: → Cloudflare Workers (most mature, Workers KV)

**Edge compute (flexible languages)**: → Fastly Compute@Edge (WebAssembly, supports Rust/Go)

**Image/video optimization**: → Cloudinary (core feature, automatic WebP/AVIF)

**Native ESI support**: → Fastly or Akamai (CloudFront and Cloudflare require edge functions)

**Best log streaming**: → Fastly (real-time, all plans) or AWS CloudFront (S3 logs, free)

**AWS ecosystem integration**: → AWS CloudFront (S3 origin, Lambda@Edge, CloudWatch)

**Enterprise SLAs**: → Akamai (99.9%+ uptime guarantees, enterprise support)

**Simplest setup**: → BunnyCDN (minimal configuration, straightforward pricing)

**Best documentation**: → Cloudflare (community + official), Fastly (VCL docs), Cloudinary (media tutorials)

---

## Missing Features / Gaps

### Features NOT supported by any CDN (or rare):

1. **Edge SQL databases**: No CDN offers edge SQL (Workers KV is key-value only)
2. **Edge AI inference**: Emerging (Cloudflare Workers AI beta, not production-ready)
3. **Native GraphQL caching**: Most CDNs cache GraphQL as opaque POST requests (not query-aware)
4. **Multi-CDN orchestration**: No native multi-CDN failover (requires third-party like NS1, Cedexis)

### Features supported by only ONE CDN:

- **Instant purge (<1s)**: Fastly only
- **Workers KV (edge storage)**: Cloudflare only
- **Automatic image format conversion (included)**: Cloudinary only
- **VCL scripting**: Fastly only (others use proprietary languages)

---

## Next Steps

With the feature matrix complete, the next S2 deliverables are:

1. **Pricing TCO analysis** - 4 bandwidth scenarios (10GB, 100GB, 1TB, 10TB/month) over 1, 3, 5 years
2. **Performance benchmarks** - Latency data (p50, p95, p99) from CDNPerf, WebPageTest
3. **Geographic coverage** - PoP distribution maps, regional latency breakdown
4. **Integration ecosystem** - Origin types, API quality, SDK depth
5. **Synthesis** - Cross-cutting insights, decision trees, trade-off analysis

**Time to complete feature matrix**: ~2 hours (44 features × 6 providers = 264 data points)

---

**Last Updated**: November 12, 2025
**Next Deliverable**: Pricing TCO analysis
