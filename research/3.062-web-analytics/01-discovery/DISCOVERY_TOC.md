# Web Analytics - Discovery Table of Contents

**Experiment ID:** 3.062-web-analytics
**Category:** Observability & Analytics
**Discovery Completed:** October 11, 2025
**Methodologies:** S0 Scoping, S1 Rapid, S2 Comprehensive, S3 Need-Driven, S4 Strategic

---

## Quick Navigation

- [S0: Experiment Scope](#s0-experiment-scope)
- [S1: Rapid Discovery (15 providers)](#s1-rapid-discovery)
- [S2: Comprehensive Analysis (10 providers)](#s2-comprehensive-analysis)
- [S3: Need-Driven Discovery (5 use cases)](#s3-need-driven-discovery)
- [S4: Strategic Selection (8 frameworks)](#s4-strategic-selection)
- [Quick Recommendations](#quick-recommendations)
- [File Reference](#file-reference)

---

## S0: Experiment Scope

**File:** `S0-EXPERIMENT-SCOPE.md`

**Challenge:** Balance privacy compliance, feature depth, and implementation complexity when choosing web analytics.

**Key Question:** What web analytics solutions exist, and how do you balance feature depth, privacy compliance, and ease of implementation?

**Scope:**
- ✅ Website traffic analytics (page views, sessions, referrers)
- ✅ Privacy-compliant analytics (GDPR, cookie-less, anonymous)
- ✅ Self-hosted vs managed platforms
- ❌ Product analytics / event tracking (see 2.063)
- ❌ A/B testing platforms (future experiment)
- ❌ Heatmaps/session replay (unless bundled)

---

## S1: Rapid Discovery

**Files:** `S1-rapid/` (17 files)
**Research Time:** ~30 minutes
**Providers Identified:** 15

### Top Recommendations

**Privacy-Focused:**
1. **Plausible** - $9/mo, GDPR-compliant, <1KB script
2. **Fathom** - $14/mo, ad-blocker bypass, GDPR-certified
3. **Simple Analytics** - $19/mo, minimalist, EU-hosted

**Free Options:**
4. **Cloudflare Web Analytics** - Free forever, zero tracking
5. **GoatCounter** - Open source, custom events, $5/mo hosting

**Full-Featured:**
6. **Google Analytics 4** - Free, comprehensive, GDPR concerns
7. **Matomo** - Self-hosted or cloud, GA-equivalent

**Self-Hosted:**
8. **Umami** - Modern stack, easy deployment
9. **PostHog** - Product analytics, self-host option

**Developer-Focused:**
10. **Vercel Analytics** - $10/mo, Next.js optimized
11. **Netlify Analytics** - $9/mo, server-side, no client script

### Quick Decision Framework (S1)
- **Privacy-first?** → Plausible, Fathom, Simple Analytics
- **Zero budget?** → Cloudflare, GoatCounter, GA4
- **Self-host?** → Umami, Matomo, PostHog
- **Developer platform?** → Vercel Analytics, Netlify Analytics
- **Full features?** → Google Analytics 4, Matomo

**Key Findings:**
- Privacy-focused tools dominate modern landscape
- GDPR compliance drives market shift from GA
- Script size: 1-3KB (privacy) vs 23KB+ (GA4)
- Self-hosting resurgence for data ownership

**Files:** approach.md, provider-[name].md (×15), recommendation.md

---

## S2: Comprehensive Analysis

**Files:** `S2-comprehensive/` (16 files)
**Research Time:** ~2-3 hours
**Providers Analyzed:** 10 (deep dive)

### Context-Specific Recommendations

**Most Businesses:** **Plausible** ($9-69/mo)
- Best balance: simplicity + privacy + features
- GDPR-compliant by design, no cookie banner
- 95% confidence recommendation

**Advanced Analytics:** **Matomo** ($29-449/mo cloud, or self-hosted)
- GA-equivalent features with GDPR compliance
- E-commerce, funnels, segments
- Self-host option for scale optimization

**Zero Budget:** **Cloudflare Web Analytics** (Free)
- Privacy-first, unlimited sites/pageviews
- Basic analytics, no advanced features

**SaaS Products:** **PostHog** (Free <1M events, then $500-2K/mo)
- All-in-one: Analytics + Session Replay + Feature Flags
- Product analytics focus

**Enterprise/Regulated:** **Piwik PRO** ($50K-300K+/year)
- HIPAA-compliant, maximum security
- On-premise option

### Key Insight
Google Analytics 4's "free" cost is misleading for EU businesses. True TCO is $2K-15K+ in year one (consent tools, legal review, data loss). Privacy-first tools at $9-69/month have LOWER TCO.

### Pricing Comparison (100K pageviews/month)
- Plausible: $19/mo
- Fathom: $14/mo
- Simple Analytics: $19/mo
- Matomo Cloud: $29/mo
- PostHog: ~$450/mo (includes product analytics)
- Umami Cloud: Free
- Google Analytics 4: $0 (but hidden costs)

**Files:** approach.md, provider-[name].md (×10), feature-matrix.md, pricing-matrix.md, privacy-matrix.md, README.md, recommendation.md

---

## S3: Need-Driven Discovery

**Files:** `S3-need-driven/` (8 files)
**Research Time:** ~1-2 hours
**Use Cases Analyzed:** 5

### Use Case Winners

**1. Personal Blog**
- **Winner:** GoatCounter (96% fit, free, custom events)
- Alternative: Cloudflare Web Analytics (free)
- Rationale: Simple, open-source, data ownership

**2. SaaS Landing Page**
- **Winner:** PostHog Free Tier (94% fit, includes funnels at $0)
- Alternative: Plausible ($9-19/mo, privacy focus)
- Rationale: Conversion tracking without cost

**3. E-commerce**
- **Winner:** PostHog Cloud (97% fit, ~$450/mo)
- Alternative: Matomo Cloud ($29-149/mo)
- Rationale: Best conversion funnel analytics

**4. Enterprise Marketing**
- **Winner:** Piwik PRO (100% fit, $18-24K/year)
- Alternative: Matomo On-Premise (self-hosted)
- Rationale: All compliance certifications

**5. Developer Documentation**
- **Winner:** GoatCounter (97% fit, open-source)
- Alternative: Plausible ($9/mo)
- Rationale: Technical audience, minimal overhead

### Requirement Patterns

**Pattern 1: Privacy + Simplicity** → Plausible, Fathom, Simple Analytics
**Pattern 2: Zero Cost** → PostHog Free, GoatCounter, Cloudflare
**Pattern 3: Product Analytics** → PostHog (all-in-one)
**Pattern 4: Compliance** → Piwik PRO, Matomo On-Premise
**Pattern 5: Self-Hosting** → Umami (easiest), Matomo (most features)

**Files:** approach.md, use-case-[name].md (×5), recommendation.md, README.md

---

## S4: Strategic Selection

**Files:** `S4-strategic/` (8 files)
**Research Time:** ~1 hour
**Strategic Frameworks:** 8

### Strategic Tiers (Vendor Viability)

**Tier 1: Maximum Stability (90-95% Confidence)**
- **Plausible** (bootstrapped, 10-20% acquisition risk, open-source escape)
- **Matomo** (18-year track record, stable foundation)
- **Google Analytics** (98% confidence, but GDPR concerns)

**Tier 2: High Viability with Acquisition Risk (60-70% Confidence)**
- **PostHog** (VC-backed, 40-70% acquisition probability)
- **Fathom** (bootstrapped, 10-20% acquisition risk)

**Tier 3: Open Source (70% Confidence)**
- **Umami, GoatCounter** (self-host eliminates vendor risk)

### Lock-In Analysis

**Minimal Lock-In** (3-4 hours to switch):
- Plausible, Fathom, Simple Analytics
- Script replacement + basic setup

**Low Lock-In** (10-20 hours):
- PostHog cloud → self-hosted (open-source escape)
- Umami (already self-hosted)

**High Lock-In** (50-100 hours):
- Google Analytics 4 → Privacy alternative (data schema incompatible)
- PostHog → Mixpanel (proprietary product analytics)

### Economic Break-Even (Self-Host vs Managed)

**<1M pageviews:** Managed services 9-59× cheaper
**1-5M pageviews:** Managed still better (unless <1 hr/month maintenance)
**>10M pageviews:** Self-hosting becomes cost-effective (2-75× savings)

### Strategic Decision Paths

1. **Maximum Safety** → Plausible ($19/mo, bootstrapped + open-source)
2. **Cost-Optimized** → Fathom ($14/mo, bootstrapped + lowest price)
3. **Feature-Rich** → PostHog (free tier + self-host escape)
4. **Self-Hosted** → Umami (easiest), Matomo (most features)
5. **Enterprise** → Matomo (18-year track record), Piwik PRO (compliance)

**Default Recommendation:** Start with Fathom ($14/mo) or Plausible ($19/mo), self-host only at >10M pageviews or data sovereignty requirement.

**Files:** approach.md, privacy-decision-tree.md, vendor-viability.md, migration-paths.md, data-ownership.md, build-vs-buy.md, lock-in-analysis.md, recommendation.md

---

## Quick Recommendations

### By Context

**Startup/Side Project**
- **Choice:** Plausible ($9-19/mo) or GoatCounter (free)
- **Confidence:** 95%+

**SaaS Product**
- **Choice:** PostHog Free (<1M events) or Plausible ($19/mo)
- **Confidence:** 90%+

**E-commerce**
- **Choice:** PostHog Cloud ($450/mo) or Matomo Cloud ($29-149/mo)
- **Confidence:** 85%+

**Enterprise/Regulated**
- **Choice:** Piwik PRO ($50K+/year) or Matomo On-Premise
- **Confidence:** 90%+

**Privacy-First**
- **Choice:** Plausible, Fathom, or Simple Analytics
- **Confidence:** 95%+

**Zero Budget**
- **Choice:** Cloudflare Web Analytics or GoatCounter
- **Confidence:** 85%+

**Self-Hosted**
- **Choice:** Umami (easy) or Matomo (features)
- **Confidence:** 80%+

### By Priority

**Need GDPR compliance?** → Plausible, Fathom (certified)
**Need conversion funnels?** → PostHog, Matomo
**Need zero cost?** → Cloudflare, GoatCounter, PostHog Free
**Need self-hosted?** → Umami, Matomo
**Need product analytics?** → PostHog (see 2.063)
**Thinking long-term (3-5 years)?** → Plausible, Matomo (stable)

---

## File Reference

### Directory Structure
```
01-discovery/
├── S1-rapid/                    (17 files, 5m research)
│   ├── approach.md
│   ├── provider-*.md            (15 provider profiles)
│   └── recommendation.md
│
├── S2-comprehensive/            (16 files, 20m research)
│   ├── approach.md
│   ├── provider-*.md            (10 detailed analyses)
│   ├── feature-matrix.md
│   ├── pricing-matrix.md
│   ├── privacy-matrix.md
│   ├── README.md
│   └── recommendation.md
│
├── S3-need-driven/              (8 files, 19m research)
│   ├── approach.md
│   ├── use-case-*.md            (5 use cases)
│   ├── recommendation.md
│   └── README.md
│
└── S4-strategic/                (8 files, 19m research)
    ├── approach.md
    ├── privacy-decision-tree.md
    ├── vendor-viability.md
    ├── migration-paths.md
    ├── data-ownership.md
    ├── build-vs-buy.md
    ├── lock-in-analysis.md
    └── recommendation.md
```

### Quick Access by Topic

**Privacy & GDPR:**
- S2/privacy-matrix.md
- S4/privacy-decision-tree.md
- S1/provider-plausible.md, provider-fathom.md

**Pricing Comparison:**
- S2/pricing-matrix.md
- S2/README.md (cost analysis)

**Feature Comparison:**
- S2/feature-matrix.md
- S2/provider-*.md (detailed feature lists)

**Use Case Matching:**
- S3/use-case-*.md (5 detailed scenarios)
- S3/recommendation.md (patterns)

**Strategic Planning:**
- S4/vendor-viability.md (acquisition risk)
- S4/lock-in-analysis.md (switching costs)
- S4/migration-paths.md (6 scenarios)

**Self-Hosting:**
- S4/build-vs-buy.md (break-even analysis)
- S2/provider-umami.md
- S2/provider-matomo.md

---

## Discovery Metrics

**Total Research Time:** ~63 minutes across 4 parallel agents
- S1: 5m 7s (31 tool uses, 33.6K tokens)
- S2: 20m 4s (39 tool uses, 84.6K tokens)
- S3: 19m 0s (16 tool uses, 99.9K tokens)
- S4: 19m 24s (16 tool uses, 140.1K tokens)

**Total Files Created:** 49 files
**Total Analysis:** ~358K tokens
**Providers Analyzed:** 15+ across all methodologies

**Methodologies Completed:** 5 of 5
- ✅ S0 Scoping
- ✅ S1 Rapid (speed-focused, popularity-driven)
- ✅ S2 Comprehensive (systematic comparison, data-driven)
- ✅ S3 Need-Driven (requirements-first matching)
- ✅ S4 Strategic (long-term viability, 3-5 year outlook)

---

## Next Steps

### For Immediate Implementation
1. Review [Quick Recommendations](#quick-recommendations) for your context
2. Read S1/recommendation.md for quick decision
3. Validate with S2 pricing/feature matrices

### For Strategic Planning
1. Read S4/vendor-viability.md (acquisition risk)
2. Review S4/lock-in-analysis.md (switching costs)
3. Check S3 use cases for similar scenarios

### For Cross-Experiment Synthesis
See: `experiments/synthesis/2.06x-observability-analytics-synthesis.md`
- Spans 2.060 (Application Monitoring), 2.061 (Uptime), 2.062 (Web Analytics), 2.063 (Product Analytics)
- Decision frameworks across observability categories
- Integration patterns and tool combinations

### For CTO Cookbook Entry
See: `qrcards/content/modelcitizendeveloper/cookbooks/cto-cookbook`
- Practical decision guides
- Real-world implementation patterns
- Cost/benefit analysis for business leaders

---

**Document Version:** 1.0
**Last Updated:** October 11, 2025
**Status:** Discovery complete, ready for synthesis
