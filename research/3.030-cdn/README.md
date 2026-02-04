# 3.030-cdn: Content Delivery Network (CDN) Services

## Experiment Classification
- **Tier**: 3 (Managed Services - Convenience)
- **Category**: 3.030-039 (Content Delivery & Storage)
- **Domain**: CDN and global content distribution services

## Research Question
**"Which CDN service provides the best combination of cost, performance, and features for different use cases?"**

## Scope
Evaluate CDN providers across three paths:
- **Path 1 (DIY)**: Self-hosted reverse proxy (Nginx, Varnish) - baseline for comparison
- **Path 2 (Open Standards)**: **DOES NOT EXIST** - no portable CDN standard
- **Path 3 (Managed Services)**: Cloud CDN providers (Cloudflare, Fastly, AWS, BunnyCDN, etc.)

## Experiment Structure

### Root Level Documents
- **DOMAIN_EXPLAINER.md** - Business-focused explanation of CDN concepts
- **SECTION_0_STANDARDS.md** - Analysis of why no open CDN standard exists
- **metadata.yaml** - Experiment metadata and relationships
- **README.md** - This file

### 01-discovery/
**MPSE S1-S4 methodology results**

#### S1-rapid/ ✅ COMPLETE
- **approach.md** - Research methodology and quick comparison
- **provider-cloudflare.md** - #1 recommendation (free tier → enterprise)
- **provider-bunnycdn.md** - #2 recommendation (budget-friendly)
- **provider-fastly.md** - Premium option (instant purge, programmable)
- **recommendation.md** - Decision matrix and use case guidance

**Status**: ✅ **S1 Complete** (90 minutes, 8 providers evaluated)

#### S2-comprehensive/ ⏸️ PENDING
- Detailed pricing matrix (all providers, all tiers)
- Feature comparison matrix (SSL, WAF, image optimization, edge compute)
- Performance benchmarks (latency by region, cache hit rates)
- Integration complexity analysis

**Estimated effort**: 3-4 hours

#### S3-need-driven/ ⏸️ PENDING
- Use case guides (e-commerce, SaaS, media, API caching)
- Traffic volume guides (<1TB, 1-10TB, 10-50TB, 50TB+)
- Geographic optimization (Europe, Asia, global)
- Migration guides (CloudFront → Cloudflare, etc.)

**Estimated effort**: 2-3 hours

#### S4-strategic/ ⏸️ PENDING
- Vendor viability analysis (financial health, acquisition risk)
- Lock-in assessment (migration complexity per provider)
- Multi-CDN strategies (when and how)
- Future trends (edge compute, HTTP/3, WebAssembly)

**Estimated effort**: 2-3 hours

---

## Providers Evaluated (S1)

### Global Giants (200+ PoPs):
1. **Cloudflare** - Free tier, 330+ PoPs, integrated security (🏆 **Recommended** for most)
2. **AWS CloudFront** - 450+ PoPs, tight AWS integration
3. **Fastly** - 100+ PoPs, instant purge, programmable VCL
4. **Akamai** - 4,100+ servers, enterprise-only

### Mid-Market (50-150 PoPs):
5. **BunnyCDN** - 123 PoPs, $10/TB bandwidth (🏆 **Recommended** for budget)
6. **KeyCDN** - 50+ PoPs, $40/TB bandwidth
7. **StackPath** - 50+ PoPs, security-focused

### Platform-Integrated:
8. **Vercel Edge** - Included with hosting, Next.js optimized
9. **Netlify Edge** - Included with hosting, Jamstack optimized
10. **Google Cloud CDN** - GCP integration

---

## Key Findings (S1)

### 1. No Open Standard Exists
- **Path 2 (Open Standards) = NOT AVAILABLE** for CDNs
- Migration between CDNs = 4-20 hours (moderate lock-in)
- HTTP caching headers standardized, but CDN config proprietary

### 2. Cost Varies 10-12×
- **Cheapest**: BunnyCDN ($10/TB) for pure bandwidth
- **Best value**: Cloudflare Pro ($2/TB effective) with unlimited bandwidth + features
- **Most expensive**: Fastly ($100-160/TB) for premium features

### 3. Three Clear Winners
- **Cloudflare**: Best for 80% of teams (free → enterprise scale)
- **BunnyCDN**: Best for cost optimization (10× cheaper)
- **Fastly**: Best for specific needs (instant purge, high-change-rate sites)

### 4. "Free" Can Be Free
- Cloudflare Free tier = genuinely unlimited bandwidth (reasonable use)
- 330+ PoPs + DDoS protection + SSL = $0/month
- Most startups never need to upgrade

### 5. Bandwidth ≠ Total Cost
- Origin egress fees matter (S3 → CloudFront costs money)
- Request fees add up (some CDNs charge per 10k requests)
- Purge/invalidation fees (AWS charges per path)

---

## Research Dividend

**Before**: Unclear which CDN to choose, or whether CDN is even needed
**After**: Clear decision framework based on:
- Traffic volume (1TB vs 100TB)
- Budget constraints ($0 vs $10,000/month)
- Feature needs (security, edge compute, instant purge)
- Platform integration (Vercel/Netlify built-in vs standalone)

**Time saved**: 4-8 hours of research per decision-maker

---

## Integration with Other Tiers

### Tier 2 (Open Standards):
- **2.051 S3 API**: CDN can pull from S3-compatible storage (origin integration)
- **No CDN standard exists** (documented in SECTION_0_STANDARDS.md)

### Tier 3 (Related Services):
- **3.031 Object Storage**: CDN origin (S3, R2, Azure Blob)
- **3.010 WAF/Security**: Many CDNs include WAF (Cloudflare, Fastly)
- **3.032 Image Processing**: Image CDNs combine processing + delivery
- **3.050 PaaS**: Vercel/Netlify include integrated CDN

---

## Quick Decision Guide

### Q: Which CDN should I use?

**If starting new project:**
→ Cloudflare Free (upgrade later if needed)

**If cost is primary concern:**
→ BunnyCDN ($10/TB vs $85-120/TB competitors)

**If on Vercel/Netlify:**
→ Use built-in CDN (zero-config, included)

**If high-change-rate site (news, flash sales):**
→ Fastly (instant purge <150ms)

**If AWS-centric stack:**
→ AWS CloudFront (tight integration)

**If need security + CDN bundle:**
→ Cloudflare Pro/Business (WAF + DDoS included)

---

## Next Steps

### To Complete S2 (Comprehensive):
1. Build detailed pricing matrix (all providers, all volume tiers)
2. Create feature comparison matrix (SSL, WAF, image optimization, analytics)
3. Run performance benchmarks (latency by region, cache hit rates)
4. Document integration complexity (setup time, API quality)

### To Complete S3 (Need-Driven):
1. Write use case guides (e-commerce, SaaS, media, API caching)
2. Create traffic volume guides (<1TB, 1-10TB, 10-50TB, 50TB+)
3. Document migration paths (CloudFront → Cloudflare, etc.)

### To Complete S4 (Strategic):
1. Analyze vendor financial health (acquisition risk)
2. Assess lock-in per provider (migration hours)
3. Document multi-CDN strategies (DNS-based, meta-CDN)
4. Identify future trends (edge compute, HTTP/3)

**Total remaining effort**: ~7-10 hours to complete S2-S4

---

## Current Status

**Progress**: S1 Complete (90 minutes invested)
**Remaining**: S2-S4 (7-10 hours estimated)
**Confidence**: 8/10 (High - clear market leaders, mature category)

**Deliverables so far**:
- DOMAIN_EXPLAINER.md (~2,600 tokens)
- SECTION_0_STANDARDS.md (~2,000 tokens)
- S1 approach + 3 provider profiles + recommendations (~3,500 tokens)
- **Total**: ~8,100 tokens across 6 documents

**Ready for**: Decision-making on CDN selection (S1 sufficient for most teams)
**Optional**: S2-S4 for deeper analysis or complex requirements
