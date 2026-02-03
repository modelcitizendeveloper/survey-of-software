# Content Delivery Network (CDN) Services: Business-Focused Explainer

**Date**: 2025-11-09
**Audience**: Business stakeholders, finance, non-technical decision-makers
**Purpose**: Explain CDN concepts and provider landscape in business terms

---

## What is a CDN?

**Simple Explanation**: A CDN is a network of servers around the world that stores copies of your website/app content closer to your users, making everything load faster.

**More Specifically**:
- Distributes your static files (images, CSS, JavaScript, videos) to 200+ locations worldwide
- Users download from the nearest server (Tokyo user gets files from Tokyo, not from your US server)
- Reduces load times from 3-5 seconds to 200-500ms
- Protects against traffic spikes and DDoS attacks

**Business Use Cases**:
- Faster website/app loading (better user experience → higher conversion)
- Global reach (serve users in Asia/Europe as fast as US users)
- Handle viral traffic spikes (product launch, Black Friday)
- Reduce origin server load (CDN serves 80-95% of traffic)
- Security (DDoS protection, bot mitigation)

**Not** a CDN:
- **Web hosting** (CDN caches files, doesn't replace your server)
- **Object storage** (CDN delivers files fast, storage keeps them long-term)

---

## Key Technical Concepts (Business Terms)

### 1. Cache Hit Rate (Efficiency Metric)

**What it is**: Percentage of requests served from CDN cache vs your origin server

**Analogy**: Like a retail store's inventory efficiency—90% cache hit rate means 90% of customer requests fulfilled from nearby CDN, only 10% need to go to your warehouse (origin server)

**Typical Rates**:
- **Good**: 85-95% cache hit rate (images, CSS, JS)
- **Poor**: <70% cache hit rate (misconfigured, too many dynamic requests)

**Business Impact**:
- Higher cache hit rate = lower origin server costs (smaller server needed)
- 95% cache hit rate means 20× less traffic to your server

---

### 2. PoPs (Points of Presence)

**What it is**: Number of data centers where CDN stores your files

**Analogy**: Like retail stores—more locations = closer to customers = faster delivery

**Typical Ranges**:
- **Global giants**: 200-300+ PoPs (Cloudflare, Fastly, AWS CloudFront)
- **Regional players**: 50-100 PoPs (BunnyCDN, KeyCDN)
- **Specialized**: 10-30 PoPs (focused on specific regions)

**Business Impact**:
- More PoPs = faster load times globally
- Fewer PoPs = cheaper pricing, good enough for regional businesses

---

### 3. Bandwidth (Data Transfer)

**What it is**: The volume of data delivered by the CDN to your users

**Analogy**: Like shipping volume—delivering 10TB of images/videos to users costs based on bandwidth usage

**Pricing Models**:
- **Pay-as-you-go**: $0.01-0.05/GB ($10-50 per TB)
- **Volume tiers**: Cheaper per GB as you scale (e.g., $0.04/GB first 10TB, $0.02/GB at 500TB+)
- **Flat rate**: Unlimited bandwidth for fixed monthly fee (BunnyCDN style)
- **Included bandwidth**: X TB/month included in base price

**Typical Usage**:
- Small site: 100GB-1TB/month ($5-50/month)
- Medium site: 10-50TB/month ($200-1,500/month)
- Large site: 100TB+/month ($2,000-10,000+/month)

---

### 4. Origin Shield (Cost Optimization)

**What it is**: An extra caching layer between CDN edge servers and your origin server

**Analogy**: Like a regional distribution center—edge locations (retail stores) request from regional center, not from main warehouse, reducing duplicate requests

**Business Impact**:
- Reduces origin server requests by 50-90%
- Lowers origin bandwidth costs (especially important with cloud storage egress fees)
- Example: 10 edge servers requesting same file = 1 request to origin (vs 10 without shield)

---

### 5. DDoS Protection

**What it is**: CDN automatically blocks malicious traffic and traffic spikes

**Analogy**: Like security guards filtering out troublemakers before they reach your store

**Business Value**:
- Prevents website downtime from attacks
- Saves cost of dedicated DDoS mitigation services ($500-5,000/month)
- Many CDNs include basic DDoS protection free (Cloudflare especially)

**Protection Levels**:
- **Basic** (included): L3/L4 DDoS (volumetric attacks)
- **Advanced** (paid): L7 DDoS (application attacks), bot management, WAF
- **Enterprise**: Dedicated IP, custom rules, 24/7 response team

---

## Cost Comparison Framework

### Cost Components:
1. **Bandwidth** (primary cost): Data delivered to users
2. **Requests** (secondary): Number of file requests (usually pennies, but adds up)
3. **Additional features**: SSL, image optimization, WAF, analytics

### Pricing Examples (10TB/month bandwidth):

**Budget Option**:
- **BunnyCDN**: ~$10-50/month (depends on region)
- **KeyCDN**: ~$40-80/month
- **Good for**: Startups, small businesses, regional sites

**Mid-Tier Option**:
- **Cloudflare Pro/Business**: $20-200/month + bandwidth
- **Fastly**: $50-500/month (pay-as-you-go)
- **Good for**: Growing businesses, global reach needed

**Enterprise Option**:
- **AWS CloudFront**: $80-200/month for 10TB
- **Akamai**: $500-5,000+/month (volume discounts at scale)
- **Good for**: Large enterprises, mission-critical applications

---

## Decision Framework: When Do You Need a CDN?

### ✅ Strong Need (Use CDN):
- Global user base (users in multiple continents)
- Heavy media site (images, videos, downloads)
- Performance-critical (e-commerce, SaaS products)
- Traffic spikes (product launches, viral content)
- Security concerns (DDoS attacks)

### ⚠️ Maybe (Evaluate Cost/Benefit):
- Regional user base (80%+ users in one region)
- Lightweight site (mostly text, few images)
- Low traffic (<10,000 visitors/month)
- Already fast enough (load times <1 second)

### ❌ Skip (Not Needed):
- Internal tools (employees only, no public traffic)
- Development environments
- Very small sites (<1,000 visitors/month)
- API-only backend (no static assets)

---

## CDN vs Object Storage vs Hosting

**Confusion Point**: CDNs, object storage, and web hosting overlap but serve different purposes.

| Need | Solution | Example |
|------|----------|---------|
| **Store files long-term** | Object Storage (3.031) | AWS S3, Backblaze B2 |
| **Deliver files fast globally** | CDN (3.030) | Cloudflare, Fastly |
| **Run application code** | Web Hosting / PaaS (3.050) | Render, Vercel, AWS |
| **All three bundled** | Integrated platform | Cloudflare (storage + CDN), Vercel (hosting + CDN) |

**Typical Stack**:
- Origin: Object storage (S3) OR web server (Render)
- CDN: Cloudflare / Fastly (caches and delivers content)
- Result: Users get files from nearest CDN edge, CDN fetches from origin only on cache miss

---

## Integration Relationships

**Upstream Dependencies** (What CDN pulls from):
- **3.031 Object Storage**: S3, R2, Azure Blob (CDN caches files from storage)
- **3.050 PaaS**: Render, Vercel, Fly.io (CDN caches dynamic site output)
- **3.040 Databases**: Postgres, Redis (CDN caches API responses)

**Downstream Consumers** (What uses CDN):
- **End users**: Browsers, mobile apps (download files from CDN edges)
- **Other CDNs**: Multi-CDN strategies (use 2+ CDNs for redundancy)

**Complementary Services**:
- **3.032 Image Processing**: Cloudinary, ImageKit (often include CDN)
- **3.010 WAF**: Cloudflare, Fastly (CDN + security bundle)

---

## Key Providers at a Glance

### Global Giants (200+ PoPs):
1. **Cloudflare** - Free tier generous, integrated security, developer-friendly
2. **AWS CloudFront** - Tight AWS integration, enterprise features
3. **Fastly** - Edge compute (VCL), real-time purging, developer-focused
4. **Akamai** - Enterprise-only, massive scale, legacy leader

### Mid-Market (50-150 PoPs):
5. **BunnyCDN** - Budget-friendly ($10-50 for 10TB), great value
6. **KeyCDN** - Simple pricing, good performance
7. **StackPath** - Security-focused, includes WAF

### Platform-Integrated:
8. **Vercel Edge** - Built into Vercel hosting, optimized for Next.js
9. **Netlify Edge** - Built into Netlify hosting
10. **Google Cloud CDN** - Tight GCP integration

---

## Common Gotchas

### 1. "Free CDN" Isn't Always Free
- Cloudflare free tier: Great for caching, but no origin shield, basic DDoS only
- Most free tiers have bandwidth caps (10-50GB/month)
- Read fine print on what's included

### 2. Egress Fees from Origin
- CDN might be cheap, but origin egress fees can be expensive
- Example: AWS CloudFront cheap, but S3 → CloudFront egress costs money
- Solution: Use Cloudflare R2 (zero egress) or origin shield

### 3. Cache Configuration Complexity
- Misconfigured cache = poor hit rate = high origin load
- Need proper cache headers (Cache-Control, Expires)
- Testing/debugging caching issues takes time

### 4. Purge/Invalidation Costs
- Some CDNs charge per purge operation (AWS CloudFront: $0.005 per path)
- Frequent cache clears = surprising costs
- Plan purge strategy (versioned URLs vs cache purging)

---

## Next Steps

After reading this explainer:
1. **Assess need**: Do you have global users or performance issues? (See Decision Framework)
2. **Estimate bandwidth**: Check current bandwidth usage (ask hosting provider or check analytics)
3. **Review S1-S4 research**: Detailed provider comparison, pricing, feature analysis
4. **Integration check**: Does your stack already include CDN? (Vercel/Netlify include it)

**Related Research**:
- **3.031 Object Storage**: Where CDN pulls files from (origin)
- **3.010 WAF/Security**: CDN security features overlap with WAF
- **3.032 Image Processing**: Image CDNs combine processing + delivery
