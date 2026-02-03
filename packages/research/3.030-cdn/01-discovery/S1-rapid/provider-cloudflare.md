# Provider Profile: Cloudflare CDN

**Category**: Global Giant
**Market Position**: #1 for startups/SMBs, strong enterprise presence
**Est. Market Share**: ~20-25% (web traffic served)

---

## Overview

**What it is**: Global CDN with 330+ PoPs, integrated security (WAF, DDoS), and edge compute platform

**Founded**: 2009
**Headquarters**: San Francisco, CA
**Public**: Yes (NYSE: NET, since 2019)
**Employees**: ~4,000+

**Key Value Proposition**: "Make the Internet faster and safer" - bundled CDN + security + performance

---

## Network Infrastructure

**Points of Presence**: 330+ cities in 120+ countries
**Total Capacity**: 310+ Tbps (as of 2024)
**Network Type**: Anycast (single IP, route to nearest PoP)
**IPv6 Support**: ✅ Yes (fully supported)

**Geographic Coverage**:
- North America: 100+ cities
- Europe: 100+ cities
- Asia: 80+ cities
- South America: 20+ cities
- Africa: 20+ cities
- Oceania: 10+ cities

---

## Pricing Structure

### Free Plan
**Cost**: $0/month

**Includes**:
- Unlimited bandwidth (reasonable use)
- DDoS protection (unmetered)
- SSL/TLS certificates (Universal SSL)
- CDN caching for static assets
- 3 Page Rules
- Basic analytics

**Limitations**:
- No image optimization
- No Workers (edge compute) or KV storage
- Basic WAF rules only
- 24-hour log retention
- Community support only

**Best for**: Startups, personal sites, testing

---

### Pro Plan
**Cost**: $20/month per domain

**Adds to Free**:
- Image optimization (Polish, Mirage)
- Mobile optimization
- 20 Page Rules
- WAF custom rules (5)
- Advanced DDoS protection
- Email support (24/7)

**Best for**: Small businesses, growing sites

---

### Business Plan
**Cost**: $200/month per domain

**Adds to Pro**:
- 50 Page Rules
- Cloudflare Workers (10M requests/month included)
- Advanced WAF (100 custom rules)
- 100% uptime SLA
- PCI compliance
- Dedicated SSL certificates
- Priority support (chat + email)

**Best for**: Mid-market, e-commerce, SaaS

---

### Enterprise Plan
**Cost**: Custom pricing ($5,000-50,000+/month)

**Adds to Business**:
- Unlimited Page Rules
- Workers Unbound (pay-per-use edge compute)
- China Network access (200+ PoPs in China)
- Bot Management
- Advanced DDoS mitigation
- 100% uptime SLA + financial credits
- Custom contracts, volume discounts
- Dedicated account team (CSM, TAM)

**Best for**: Enterprises, high-traffic sites (>10TB/month)

---

## Key Features

### 1. Edge Compute (Cloudflare Workers)
**What**: Run JavaScript/WebAssembly at edge (330+ locations)

**Use cases**:
- A/B testing at edge
- Geo-redirect (route by country)
- API composition (combine multiple APIs)
- Authentication/authorization logic
- Dynamic content generation

**Pricing**: $5/month (10M requests), then $0.50 per million requests
**Language**: JavaScript, TypeScript, Rust (via Wasm)

**Lock-in risk**: HIGH - Workers code is Cloudflare-specific (migration requires rewrite)

---

### 2. Cloudflare R2 (Object Storage)
**What**: S3-compatible object storage with zero egress fees

**Pricing**:
- Storage: $0.015/GB/month ($15/TB)
- Operations: $4.50 per million Class A (write), $0.36 per million Class B (read)
- **Egress: $0** (no data transfer out fees)

**Integration**: R2 as CDN origin = zero origin egress costs

---

### 3. Image Optimization
**What**: Automatic image resizing, format conversion (WebP, AVIF), compression

**Pricing**: Pro plan ($20/month) or $20/month add-on
**Use case**: Reduce image bandwidth 30-50%, faster load times

---

### 4. DDoS Protection
**What**: Unmetered DDoS mitigation (included on all plans)

**Protection types**:
- L3/L4: Network layer (SYN floods, UDP amplification)
- L7: Application layer (HTTP floods, slow loris)
- Largest mitigated: 3.8 Tbps (record as of 2024)

**Value**: Saves $1,000-10,000/month vs dedicated DDoS services

---

### 5. WAF (Web Application Firewall)
**What**: Block malicious traffic (SQL injection, XSS, etc.)

**Tiers**:
- Free: OWASP core ruleset
- Pro: 5 custom rules
- Business: 100 custom rules + advanced bot protection
- Enterprise: Unlimited + managed rulesets

---

## Performance Characteristics

**Latency**:
- Median: 10-30ms (global average)
- Best: <5ms (major cities)
- Worst: 50-100ms (rural/remote areas)

**Cache Hit Rate**: 90-95% (typical for static assets)
**Purge Time**: 5-30 seconds (global purge)

**Benchmarks** (from CDNPerf.com, 2024 averages):
- Global latency: ~20ms median
- North America: 10-15ms
- Europe: 15-25ms
- Asia: 20-40ms

**vs Competitors**:
- Faster than: AWS CloudFront (30ms), KeyCDN (35ms)
- Comparable to: Fastly (20ms), BunnyCDN (25ms)

---

## Integration & Developer Experience

### Setup Time: **10-30 minutes** (DNS-based)

**Steps**:
1. Sign up (2 minutes)
2. Add domain (2 minutes)
3. Update nameservers at registrar (5-15 minutes for propagation)
4. Configure caching rules (5-10 minutes)

**Documentation Quality**: ⭐⭐⭐⭐⭐ (5/5)
- Excellent guides, tutorials
- Active community forum
- Good API documentation

**API**: REST API, Terraform provider, Pulumi

---

## Pros

✅ **Free tier is incredibly generous** (many sites never need to upgrade)
✅ **Unified security + CDN** (DDoS + WAF included, no separate services)
✅ **330+ PoPs worldwide** (excellent global coverage)
✅ **Developer-friendly** (Workers, API, Terraform)
✅ **Integrated ecosystem** (R2, Workers KV, Stream, Pages)
✅ **Fast setup** (10-30 minutes, DNS-based)
✅ **Strong performance** (20ms median latency)

---

## Cons

❌ **No origin shield on Free/Pro** (can increase origin requests → higher origin costs)
❌ **Workers lock-in** (code is Cloudflare-specific, migration = rewrite)
❌ **Enterprise pricing opaque** (need to contact sales)
❌ **Cache purge not instant** (5-30 seconds vs Fastly's 150ms)
❌ **Limited control on Free** (3 Page Rules only)
❌ **DNS required** (must use Cloudflare nameservers for CDN, or CNAME setup with limitations)

---

## Best Use Cases

### ✅ Excellent For:
- **Startups** (free tier → scale to paid as needed)
- **Global applications** (users worldwide)
- **Security-conscious** (DDoS + WAF included)
- **Developer-friendly sites** (Workers for edge logic)
- **Static sites** (Cloudflare Pages + CDN)

### ⚠️ Consider Alternatives For:
- **High-change-rate sites** (Fastly's instant purge better for news/e-commerce flash sales)
- **Pure CDN without DNS migration** (AWS CloudFront, BunnyCDN allow origin-only setup)
- **Cost optimization at scale** (BunnyCDN cheaper for 50TB+/month pure bandwidth)

---

## Migration Considerations

### Migrating TO Cloudflare:
**Effort**: 10-30 minutes (DNS change)
**Risk**: Low (gradual DNS propagation, rollback easy)

### Migrating FROM Cloudflare:
**Effort**: 2-8 hours (depends on Workers usage)
- DNS change: 10 minutes
- Rewrite Workers: 2-6 hours (if using edge compute)
- Test cache behavior: 1-2 hours

**Lock-in**: MODERATE (DNS + Workers)

---

## Vendor Viability

**Financial Health**: ⭐⭐⭐⭐⭐ (5/5)
- Public company (NYSE: NET)
- Revenue: $1.3B+ (2024)
- Growth: 30% YoY
- Profitable (adjusted EBITDA positive)

**Longevity**: 15 years (founded 2009)
**Acquisition Risk**: Low (valuable standalone company)
**5-year survival**: 99%
**10-year survival**: 95%

---

## Verdict: Top Choice for Most Teams

**Rating**: ⭐⭐⭐⭐½ (4.5/5)

**Why**: Unbeatable free tier, integrated security, fast global network, excellent DX

**When to use**:
- ✅ Starting a new project (use free tier)
- ✅ Need DDoS protection + CDN (saves $1,000+/month vs separate services)
- ✅ Global user base (330+ PoPs)
- ✅ Want edge compute (Workers)

**When to consider alternatives**:
- ❌ Pure cost optimization at scale (BunnyCDN cheaper at 50TB+/month)
- ❌ Need instant cache purge (Fastly 150ms vs Cloudflare 5-30s)
- ❌ Already on AWS ecosystem (CloudFront tighter integration)
