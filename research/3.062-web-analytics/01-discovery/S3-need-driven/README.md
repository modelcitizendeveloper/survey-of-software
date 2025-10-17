# S3 Need-Driven Discovery: Web Analytics

**Experiment:** 3.062-web-analytics
**Phase:** S3 (Need-Driven Discovery)
**Completed:** October 11, 2025
**Status:** Complete

## Overview

This directory contains targeted, use-case-driven analysis of web analytics solutions. Unlike S1 (rapid overview) and S2 (comprehensive landscape), S3 starts with specific scenarios and matches them to the best-fit solutions.

**Methodology:** Requirements-first matching. Define explicit needs, score providers against those needs, recommend based on fit percentage.

## What's Inside

### Core Documents

1. **[approach.md](./approach.md)** - Methodology overview
   - Need-driven discovery principles
   - Scoring framework (requirements satisfaction %)
   - Gap analysis approach
   - Decision trees and migration triggers

2. **[recommendation.md](./recommendation.md)** - Cross-use-case synthesis
   - Quick decision matrix (by budget, privacy, features)
   - Provider rankings across all use cases
   - Strategic insights and trade-offs
   - Final recommendations and migration paths

### Use Case Analyses

3. **[use-case-personal-blog.md](./use-case-personal-blog.md)**
   - **Scenario:** <10K pageviews/month, zero budget, side project
   - **Winner:** GoatCounter (96% fit, free with custom events)
   - **Alternative:** Cloudflare (87% fit, maximum reliability)
   - **Key Insight:** Free tiers are sufficient for validation

4. **[use-case-saas-landing-page.md](./use-case-saas-landing-page.md)**
   - **Scenario:** 100K pageviews/month, bootstrapped startup, need conversion tracking
   - **Winner:** PostHog Free Tier (94% fit, free with funnels)
   - **Alternative:** Fathom (93% fit, $14/month, simple but no funnels)
   - **Key Insight:** PostHog free tier offers $450/month worth of features at $0

5. **[use-case-ecommerce.md](./use-case-ecommerce.md)**
   - **Scenario:** 1M pageviews/month, need revenue tracking and attribution
   - **Winner:** PostHog Cloud (97% fit, ~$450/month, best funnels + cohorts)
   - **Alternative:** Matomo Self-Hosted (90% fit, $50-100/month, maintenance burden)
   - **Key Insight:** Advanced e-commerce analytics justify $450/month cost via 0.5% conversion improvement

6. **[use-case-enterprise-marketing.md](./use-case-enterprise-marketing.md)**
   - **Scenario:** 10M+ pageviews/month, GDPR/SOC2 required, data sovereignty
   - **Winner:** Piwik PRO (100% fit, $18-24K/year, all certifications)
   - **Alternative:** PostHog Enterprise Self-Hosted (99% fit, $21-33K/year, open-source)
   - **Key Insight:** Compliance certifications worth premium for regulated industries

7. **[use-case-developer-docs.md](./use-case-developer-docs.md)**
   - **Scenario:** Technical documentation, privacy-conscious audience, minimal overhead
   - **Winner:** GoatCounter (97% fit, free, open-source, developer-friendly)
   - **Alternative:** Plausible (98% fit, $9/month, <1KB script, polished)
   - **Key Insight:** Developer audience appreciates transparency (open-source) and minimal tracking

## Key Findings

### Provider Dominance by Category

**PostHog** - 3/5 use cases
- SaaS Landing Page (94%)
- E-commerce (97%)
- Enterprise Marketing (99%)
- Strength: Free tier + funnels/cohorts unique combination

**GoatCounter** - 2/5 use cases
- Personal Blog (96%)
- Developer Documentation (97%)
- Strength: Free + custom events + open-source

**Plausible** - Strong second place in most categories
- Privacy-first positioning
- GDPR certification
- <1KB script

**Piwik PRO** - 1/5 use cases
- Enterprise Marketing (100% perfect fit)
- Strength: All compliance certifications (SOC2, ISO 27001, GDPR)

### Cross-Cutting Insights

1. **Free tiers are exceptional**
   - PostHog: 1M events/month (worth ~$450/month)
   - GoatCounter: Unlimited (donation-supported)
   - Cloudflare: Unlimited pageviews
   - Use free for validation (0-12 months)

2. **Privacy vs features trade-off is real**
   - Privacy-first tools: Simple, lightweight, limited features
   - Full-featured tools: Heavy scripts, configuration required
   - Sweet spot: PostHog cookie-less mode (compromise)

3. **Self-hosting saves cash but costs time**
   - PostHog Cloud: $450/month ($5,400/year)
   - PostHog Self-Hosted: $200/month infra + $1,500/month time = $20,400/year
   - Only makes sense at scale (>5M pageviews) OR with existing DevOps

4. **Event-based pricing can explode**
   - 1M pageviews ≠ 1M events
   - E-commerce tracking: 3-6x multiplier
   - Monitor usage, set alerts, sample non-critical events

5. **Google Analytics is declining**
   - GDPR court rulings
   - 45KB script (page load impact)
   - Privacy concerns growing
   - New projects avoid GA4

## Quick Decision Guide

### By Budget

**$0:** PostHog Free Tier, GoatCounter, Cloudflare
**<$30/month:** Plausible ($19), Fathom ($14), Simple Analytics ($9 annual)
**<$100/month:** PostHog paid, Plausible Business ($69), self-hosted options
**Enterprise:** Piwik PRO ($1,500-2,000/month), PostHog Enterprise

### By Privacy Requirement

**GDPR Certified:** Plausible, Piwik PRO
**Cookie-less:** Plausible, Fathom, Simple Analytics, GoatCounter
**Privacy-capable:** PostHog cookie-less mode, Matomo
**Don't care:** Any option (but avoid GA4 for EU customers)

### By Feature Need

**Basic stats:** GoatCounter, Cloudflare, Fathom
**Conversion tracking:** PostHog, Plausible Business, Matomo
**Product analytics:** PostHog, Mixpanel
**Enterprise compliance:** Piwik PRO, PostHog Enterprise

### By Technical Capacity

**Non-technical:** Cloudflare, Fathom, Plausible
**Developer-friendly:** PostHog, GoatCounter, Plausible
**Can self-host:** Umami, Matomo, PostHog

## Comparison Matrix

| Provider | Free Tier | Paid From | Funnels | Cohorts | Open Source | GDPR Cert | Script Size | Best For |
|----------|-----------|-----------|---------|---------|-------------|-----------|-------------|----------|
| PostHog | 1M events | $450/mo | ✅ | ✅ | ✅ | ⚠️ | ~5KB | SaaS, E-commerce |
| Plausible | ❌ | $9/mo | $69/mo | ❌ | ✅ | ✅ | <1KB | Privacy-first |
| GoatCounter | Unlimited | Donations | ❌ | ❌ | ✅ | ❌ | 3.5KB | OSS, Blogs |
| Fathom | ❌ | $14/mo | ❌ | ❌ | ❌ | ⚠️ | 1.6KB | Simple, Privacy |
| Cloudflare | Unlimited | Free | ❌ | ❌ | ❌ | ⚠️ | Minimal | Basic, Free |
| Matomo | Self-host | $19/mo | Plugin | ⚠️ | ✅ | ✅ | 22.8KB | Self-hosted |
| Piwik PRO | ❌ | $1,500/mo | ✅ | ✅ | ❌ | ✅ | Medium | Enterprise |
| Umami | Self-host | Infra only | ❌ | ❌ | ✅ | ❌ | <2KB | Self-hosted |
| Simple Analytics | ❌ | $9/mo annual | ❌ | ❌ | ❌ | ⚠️ | ~2KB | Privacy, Budget |
| Mixpanel | 20M events | Usage | ✅ | ✅ | ❌ | ⚠️ | Medium | Product analytics |

Legend:
- ✅ = Available/Yes
- ❌ = Not available
- ⚠️ = Partial/Conditional

## Cost Comparison (1M pageviews/month)

| Provider | Monthly Cost | Annual Cost | 3-Year Cost | Notes |
|----------|--------------|-------------|-------------|-------|
| Cloudflare | $0 | $0 | $0 | Basic features only |
| GoatCounter | $0 | $0 | $0 | Donation-supported |
| PostHog Free | $0 | $0 | $0 | If <1M events |
| Fathom | $54 | $648 | $1,944 | Unlimited users |
| Plausible | $69 | $828 | $2,484 | Business plan (with funnels) |
| Umami Self-Hosted | ~$20 | $240 | $720 | Infrastructure only |
| PostHog Cloud | ~$450 | $5,400 | $16,200 | Assumes 3M events |
| Matomo Self-Hosted | ~$100 | $1,200 | $3,600 | Infra + plugins |
| Piwik PRO | $1,500 | $18,000 | $54,000 | Enterprise compliance |

## Migration Paths

### Typical Evolution

**Month 0-6: Validation**
- Start: PostHog Free Tier OR GoatCounter
- Goal: Validate product-market fit
- Cost: $0
- Trigger: Hit limits OR get funding

**Month 6-12: Growth**
- Upgrade: PostHog Paid OR Plausible/Fathom
- Goal: Scale with revenue
- Cost: $14-450/month
- Trigger: Need enterprise features OR >1M pageviews

**Month 12-24: Optimization**
- Consider: Self-hosted (Umami, Matomo, PostHog)
- Goal: Cost efficiency at scale
- Cost: $50-200/month (vs $450+)
- Trigger: Cloud costs >$500/month

**Month 24+: Enterprise**
- Upgrade: PostHog Enterprise OR Piwik PRO
- Goal: Compliance, SSO, advanced features
- Cost: $1,500-2,000/month
- Trigger: Enterprise customers, compliance requirements

### Common Migrations

**From Google Analytics:**
1. Privacy concerns → Plausible, Fathom, Simple Analytics
2. GDPR requirements → Plausible (certified), Matomo self-hosted
3. Need funnels + privacy → PostHog cookie-less mode

**From Free Tier:**
1. Exceed limits → PostHog paid, Mixpanel paid
2. Need SLA → Fathom, Plausible (managed)
3. Cost optimization → Self-hosted Umami, Matomo

**Between Providers:**
1. Cost reduction → Managed to self-hosted
2. Privacy upgrade → Basic to certified (Plausible, Piwik PRO)
3. Feature upgrade → Web analytics to product analytics (PostHog, Mixpanel)

## Implementation Time Estimates

| Provider | Setup Time | Maintenance | Complexity |
|----------|------------|-------------|------------|
| Cloudflare | 5 min | 0 hrs/month | Trivial |
| GoatCounter | 10 min | 0 hrs/month | Simple |
| Fathom | 10 min | 0 hrs/month | Simple |
| Plausible | 10 min | 0 hrs/month | Simple |
| PostHog Cloud | 15 min | 0 hrs/month | Moderate |
| Umami Self-Hosted | 30 min | 1-2 hrs/month | Moderate |
| Matomo Self-Hosted | 1 hour | 2-4 hrs/month | Complex |
| PostHog Self-Hosted | 1 week | 5-10 hrs/month | Complex |
| Piwik PRO | 1 week | 0 hrs/month (managed) | Complex |

## How to Use This Research

### Step 1: Identify Your Use Case

Match your situation to one of the analyzed scenarios:
- **Personal Blog**: <10K pageviews, side project, zero budget
- **SaaS Landing Page**: 100K pageviews, bootstrapped, need conversions
- **E-commerce**: 1M pageviews, need revenue tracking
- **Enterprise**: 10M+ pageviews, compliance required
- **Developer Docs**: Technical audience, privacy-conscious

### Step 2: Review Recommendations

Read the specific use case file for:
- Detailed requirements analysis
- Provider scoring (% fit)
- Implementation guides
- Cost analysis
- Decision frameworks

### Step 3: Validate Assumptions

Check if the analysis assumptions match your situation:
- Traffic volume (10K vs 100K vs 1M)
- Budget constraints ($0 vs $30/month vs $1,000/month)
- Feature requirements (basic vs funnels vs cohorts)
- Privacy needs (GDPR vs cookie-less vs don't care)
- Technical capacity (can self-host vs managed only)

### Step 4: Start Trial

Most providers offer free trials:
- PostHog: Free tier (1M events)
- Plausible: 30-day free trial
- Fathom: 7-day free trial
- GoatCounter: Free forever
- Cloudflare: Free forever

### Step 5: Implement and Monitor

- Track key metrics (conversion, engagement)
- Monitor costs (usage, overages)
- Assess team satisfaction (usability, support)
- Plan for growth (migration triggers)

## Related Documents

### In This Experiment

- **S0-EXPERIMENT-SCOPE.md**: Challenge definition and discovery questions
- **S1 Rapid Discovery**: Quick overview of top providers
- **S2 Comprehensive Discovery**: Full landscape analysis
- **S4 Strategic Discovery**: Decision frameworks and vendor strategy
- **SYNTHESIS**: Executive summary (coming soon)

### Reference Documents

- **MONOLITHIC_REFERENCE/S3_NEED_DRIVEN_DISCOVERY.md**: Original comprehensive analysis (74KB)
- **WEB_ANALYTICS_EXPLAINER.md**: Conceptual overview of web analytics
- **PROVIDER_UNIVERSE.md**: Complete provider catalog

## Questions or Need Help?

If you're unsure which provider to choose:

1. **Start with the Quick Decision Guide** (above)
2. **Read the matching use case file** (most similar to your situation)
3. **Review the recommendation.md** (cross-cutting insights)
4. **Try free tiers** (PostHog, GoatCounter, Cloudflare)

**Most common starting point:** PostHog Free Tier (if need funnels) or GoatCounter (if basic stats sufficient)

## Document Statistics

- **Total Use Cases Analyzed:** 5
- **Providers Evaluated:** 14 (PostHog, Plausible, Fathom, GoatCounter, Cloudflare, Umami, Matomo, Piwik PRO, Simple Analytics, Mixpanel, Amplitude, Heap, Counter.dev, Google Analytics 4)
- **Requirements Assessed:** 60+ across all use cases
- **Total Analysis:** ~40,000 words
- **Research Time:** ~8 hours (includes original monolithic analysis)

## Updates and Maintenance

**Last Updated:** October 11, 2025

**Update Triggers:**
- Major provider pricing changes
- New compliance regulations (GDPR, CCPA updates)
- Significant product feature launches
- Market consolidation (acquisitions, shutdowns)

**Next Review:** Q1 2026 (or as triggered by major changes)

---

**Note:** This research represents a snapshot in time (October 2025). Pricing, features, and recommendations may change. Always verify current information with provider documentation before making decisions.
