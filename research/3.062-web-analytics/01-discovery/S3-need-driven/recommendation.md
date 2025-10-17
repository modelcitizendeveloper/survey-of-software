# S3 Cross-Use-Case Recommendations

**Experiment:** 3.062-web-analytics
**Phase:** S3 Need-Driven Discovery
**Date:** October 11, 2025

## Executive Summary

After analyzing web analytics solutions across five distinct use cases, clear patterns emerge. The "best" analytics tool depends entirely on your specific requirements: budget, privacy stance, technical capacity, and feature needs.

**Key Finding:** One provider dominates multiple categories: **PostHog** offers exceptional value for startups and growth-stage companies through its generous free tier (1M events/month) with features that typically cost $450+/month. For privacy-first use cases, **Plausible** sets the standard with GDPR Article 6(1)(f) certification and <1KB script.

## Quick Decision Matrix

### By Budget

**$0 (Free Tier)**
- **Product/SaaS:** PostHog Free Tier (1M events, includes funnels, cohorts, session replay)
- **Content/Docs:** GoatCounter (unlimited, custom events, open-source)
- **Simple Stats:** Cloudflare Web Analytics (unlimited pageviews, Cloudflare reliability)

**<$30/month**
- **Privacy-first:** Plausible $19/month (or $9/month annual for Simple Analytics)
- **Simplicity:** Fathom $14/month (unlimited users/retention)
- **Self-hosted:** Umami ~$10-20/month infrastructure

**$30-$100/month**
- **Growth SaaS:** PostHog Cloud ~$450/month (3M events) OR Plausible Business $69/month
- **E-commerce:** PostHog Cloud (funnels + cohorts + revenue tracking)

**Enterprise ($1,000+/month)**
- **Compliance-critical:** Piwik PRO $1,500-2,000/month (SOC2, ISO 27001, GDPR certified)
- **Technical Enterprise:** PostHog Self-Hosted $500-1,000/month infra + $1,000-2,000/month license
- **Cost-optimized:** Matomo Self-Hosted $200-500/month infra + plugins

### By Privacy Requirements

**GDPR Certification Required**
1. **Plausible** - Article 6(1)(f) certified, legal docs available
2. **Piwik PRO** - Full compliance suite (SOC2, ISO 27001, GDPR)
3. **Matomo** - GDPR-certified, self-hosted option

**Privacy-Conscious (Cookie-less)**
1. **Plausible** - <1KB, no cookies, EU hosting
2. **Fathom** - Cookie-less, Canada/EU servers
3. **Simple Analytics** - GDPR-first, Netherlands hosting
4. **GoatCounter** - No tracking, no identifiers

**Don't Care About Privacy**
- Google Analytics 4 (free, but GDPR risks in EU)
- Any provider works

### By Technical Capacity

**Non-Technical Team**
- **Cloudflare** - One-click if using Cloudflare
- **Fathom** - 2-minute setup, zero configuration
- **Plausible** - Simple script tag, beautiful UI

**Developer-Friendly**
- **PostHog** - Event-based, API-first, modern stack
- **GoatCounter** - Developer-focused, minimal
- **Plausible** - Open-source, clean API

**DevOps Capacity (Can Self-Host)**
- **Umami** - Simple Docker deployment
- **Matomo** - Mature, feature-rich
- **PostHog** - Advanced, ClickHouse-based

### By Feature Requirements

**Basic (Pageviews, Sources, Devices)**
- Cloudflare, GoatCounter, Fathom, Plausible, Simple Analytics

**Funnels + Cohorts (Product Analytics)**
- PostHog (free tier or paid), Mixpanel, Matomo, Piwik PRO

**E-commerce (Revenue Tracking)**
- PostHog (event properties), Matomo (e-commerce plugin), GA4 (enhanced e-commerce)

**Enterprise (SSO, RBAC, Compliance)**
- Piwik PRO, PostHog Enterprise, Matomo Premium

## Provider Rankings by Use Case

### Personal Blog (<10K pageviews)
1. **GoatCounter** (96%) - Free, custom events, open-source
2. **Cloudflare** (87%) - Free, Cloudflare reliability, basic features
3. **Plausible** (99%) - $9/month, most polished, slight cost concern

**Winner:** GoatCounter (perfect fit for free tier + custom events)

### SaaS Landing Page (100K pageviews)
1. **PostHog Free** (94%) - Free with funnels (critical advantage)
2. **Fathom** (93%) - $14/month, simple, no funnels
3. **Plausible** (93%) - $19/month, requires $69/month upgrade for funnels

**Winner:** PostHog Free Tier (only free option with funnel analysis)

### E-commerce (1M pageviews)
1. **PostHog Cloud** (97%) - Best funnels/cohorts/revenue tracking
2. **Matomo Self-Hosted** (90%) - E-commerce features, cost-effective
3. **Mixpanel Free** (89%) - Generous free tier, 90-day retention limit

**Winner:** PostHog Cloud (purpose-built for conversion tracking, worth $450/month cost)

### Enterprise Marketing (10M+ pageviews)
1. **Piwik PRO** (100%) - Perfect compliance fit, all certifications
2. **PostHog Enterprise** (99%) - Open-source + enterprise features, no white-labeling
3. **Matomo Self-Hosted** (94%) - Cost-effective, self-managed SLA

**Winner:** Piwik PRO for regulated industries, PostHog Enterprise for tech companies

### Developer Documentation
1. **GoatCounter** (97%) - Free, open-source, developer-friendly
2. **Plausible** (98%) - <1KB script, polished UI, $9/month
3. **Umami** (93%) - Self-hosted control, minimal cost

**Winner:** GoatCounter for OSS, Plausible for commercial docs

## Provider Deep Dives

### PostHog: The Startup Champion

**Strengths:**
- **Exceptional free tier:** 1M events/month with funnels, cohorts, session replay
- **Event-based analytics:** Superior for SaaS and product-led growth
- **Open-source:** No vendor lock-in, can self-host
- **Modern stack:** ClickHouse backend scales to billions
- **Y Combinator pedigree:** Built by founders for founders

**Ideal For:**
- Startups (free tier covers most needs)
- Product-led growth SaaS
- Technical teams comfortable with events
- E-commerce (revenue tracking via event properties)

**Avoid If:**
- Need <2KB script (PostHog is ~5KB)
- Require GDPR certification (capable but not certified)
- Non-technical team (event tracking has learning curve)

**Pricing:**
- Free: 1M events/month
- Paid: ~$0.00045/event (~$450/month for 1M events)
- Self-hosted: $500-1,000/month infrastructure + license

**Best Use Cases:** 2/5
- SaaS Landing Page ✅
- E-commerce ✅
- (Also wins Product-Led Growth, Growth SaaS)

### Plausible: The Privacy Standard

**Strengths:**
- **GDPR certified:** Only Article 6(1)(f) certified option
- **Lightweight:** <1KB script (fastest)
- **Beautiful UI:** Most polished dashboard
- **Open-source:** AGPLv3, can self-host
- **Bootstrapped:** No VC pressure, sustainable model

**Ideal For:**
- Privacy-conscious brands
- EU customers (GDPR documentation required)
- Landing pages (fast load times)
- Anyone who values polish + privacy

**Avoid If:**
- Need cohort retention analysis (not available)
- Need funnels but budget <$69/month (Business plan required)
- Tight budget and can't self-host (GoatCounter cheaper at free)

**Pricing:**
- Growth: $9/month (10K pageviews) to $249/month (10M)
- Business: $69/month (includes funnels) to $499/month
- Self-hosted: Free (infrastructure costs only)
- OSS discount: 33% off

**Best Use Cases:** 1/5
- Enterprise Marketing ✅ (tied with others for privacy compliance)
- (Also strong in all privacy-first scenarios)

### GoatCounter: The OSS Hero

**Strengths:**
- **Completely free:** Donation-supported, no limits
- **Open-source:** Self-host or use hosted
- **Developer-friendly:** Built by developer for developers
- **Custom events:** Rare for free tier
- **Privacy-first:** No tracking, no cookies

**Ideal For:**
- Open-source projects
- Personal blogs and side projects
- Developer documentation
- Anyone with $0 budget who needs custom events

**Avoid If:**
- Need 99.9%+ SLA (solo developer = 95-98% uptime)
- Need advanced features (funnels, cohorts)
- Prefer polished UI over functionality

**Pricing:**
- Free: Unlimited (donations appreciated)
- Self-hosted: Infrastructure costs only

**Best Use Cases:** 2/5
- Personal Blog ✅
- Developer Documentation ✅

### Fathom: The Simple Choice

**Strengths:**
- **Simplest privacy analytics:** Cookie-less by default
- **Lowest privacy-first pricing:** $14/month for 100K
- **Unlimited users and retention:** Best value for teams
- **Uptime monitoring:** Bonus feature included
- **1.6KB script:** Fast loading

**Ideal For:**
- Non-technical teams
- Privacy-first businesses
- Teams needing unlimited users
- Bootstrapped startups (affordable)

**Avoid If:**
- Need funnels (not available)
- Need cohort analysis (not available)
- Want open-source (proprietary)

**Pricing:**
- $14/month (100K pageviews) to $274/month (10M)
- All features included at every tier

**Best Use Cases:** 0/5 (Strong second place in multiple categories)
- SaaS Landing Page (93%, second to PostHog)
- Others (always in top 3)

### Matomo: The Self-Hosted Veteran

**Strengths:**
- **Mature platform:** 15+ years, proven stability
- **Feature-rich:** E-commerce, funnels, cohorts via plugins
- **Self-hosted:** Full data ownership
- **Cost-effective:** $5-30K/year vs $60-100K for alternatives

**Ideal For:**
- Enterprises with DevOps capacity
- Cost-conscious organizations
- Data sovereignty requirements
- E-commerce (purpose-built plugins)

**Avoid If:**
- No DevOps resources (maintenance burden)
- Need lightweight script (22.8KB is heavy)
- Want cutting-edge features (development slower than PostHog)

**Pricing:**
- Self-hosted: Free + infrastructure ($50-500/month)
- Cloud: $19/month (50K) to $2,500/month (enterprise)
- Premium plugins: $199-999/year each

**Best Use Cases:** 0/5 (Strong alternative in enterprise)
- Enterprise Marketing (94%, cost-effective option)
- E-commerce (90%, self-hosted alternative)

### Piwik PRO: The Compliance Champion

**Strengths:**
- **Perfect compliance:** SOC2, ISO 27001, GDPR all certified
- **White-labeling:** Only option with client reporting
- **Enterprise focus:** 100+ employees, mature vendor
- **Full support:** Dedicated CSM, professional services

**Ideal For:**
- Regulated industries (healthcare, finance, government)
- Enterprises requiring audit documentation
- Agencies needing white-labeling
- Maximum compliance assurance

**Avoid If:**
- Budget <$18K/year (expensive)
- Don't need compliance certifications
- Prefer open-source solutions

**Pricing:**
- €1,408+/month for 10M pageviews
- ~$18,000-24,000/year
- Contact sales for exact pricing

**Best Use Cases:** 1/5
- Enterprise Marketing ✅ (100% perfect fit for compliance)

### Cloudflare: The Free Simplicity

**Strengths:**
- **Free forever:** No limits
- **Cloudflare reliability:** 99.99%+ SLA
- **Zero setup:** One-click if using Cloudflare
- **Lightweight:** Minimal script impact

**Ideal For:**
- Sites already using Cloudflare
- Absolute zero budget
- Basic stats sufficient
- Maximum reliability needed

**Avoid If:**
- Need custom events (not available)
- Want data export (not available)
- Prefer open-source (proprietary)
- Need advanced analytics

**Pricing:**
- Free: Unlimited

**Best Use Cases:** 0/5 (Strong second place)
- Personal Blog (87%, free alternative to GoatCounter)
- Developer Documentation (62%, basic stats only)

## Cross-Cutting Insights

### 1. The "Free Tier Trap"

**Observation:** Free tiers are exceptionally generous in 2025
- PostHog: 1M events/month (worth ~$450/month)
- Mixpanel: 20M events/month
- Cloudflare: Unlimited pageviews
- GoatCounter: Unlimited (donation-supported)

**Trap:** Dependency risk
- Free tiers can change (price increases, feature restrictions)
- VC-backed companies may pivot (acquisition, sunset)
- Solo developer projects may be abandoned

**Mitigation:**
- Use free tiers for validation (0-12 months)
- Plan migration path before dependency is critical
- Choose open-source where possible (can self-host)
- Consider paid options from bootstrapped companies (more stable)

**Recommendation:** Start with free tier, upgrade when product-market fit proven OR revenue justifies cost.

### 2. The Privacy-Feature Trade-off

**Observation:** Privacy often means fewer features

**Privacy-first tools** (Plausible, Fathom, Simple Analytics):
- ✅ Cookie-less, GDPR compliant
- ✅ Lightweight scripts (<2KB)
- ✅ Simple setup
- ❌ No/limited funnels
- ❌ No cohort analysis
- ❌ Limited segmentation

**Full-featured tools** (PostHog, Mixpanel, GA4):
- ✅ Funnels, cohorts, segmentation
- ✅ User-level tracking
- ✅ Advanced analytics
- ❌ Heavier scripts (5-45KB)
- ⚠️ Privacy configuration required
- ⚠️ May need cookie consent

**Sweet Spot:** PostHog with cookie-less mode
- Disable persistence: `persistence: 'memory'`
- Get funnels + cohorts without cookies
- Trade-off: Less accurate user identification

**Recommendation:** Choose based on priority
- Privacy > Features → Plausible, Fathom
- Features > Privacy → PostHog, Mixpanel
- Both important → PostHog cookie-less mode (compromise)

### 3. The Self-Hosted Paradox

**Observation:** Self-hosting saves money on paper but costs time

**Cash Cost:**
- PostHog Cloud: $450/month ($5,400/year)
- PostHog Self-Hosted: $200/month infra ($2,400/year)
- Savings: $3,000/year (56%)

**Time Cost:**
- Setup: 1 week (40 hours) × $150/hr = $6,000
- Maintenance: 10 hours/month × 12 × $150/hr = $18,000/year
- Total Year 1: $2,400 + $6,000 + $18,000 = $26,400

**Reality Check:**
- Self-hosted saves cash but costs time
- Break-even requires very high traffic OR very low time cost
- DevOps time often underestimated

**When Self-Hosting Makes Sense:**
- Large enterprises (existing DevOps team, time cost amortized)
- Data sovereignty requirements (no choice)
- Very high traffic (5M+ pageviews = $2,000+/month cloud)
- Existing infrastructure (minimal incremental cost)

**When Managed Makes Sense:**
- Startups (focus on product, not infrastructure)
- Small teams (no DevOps capacity)
- Budget allows (cloud cost < engineering time cost)

**Recommendation:**
- <1M pageviews: Use managed ($0-450/month)
- 1-10M pageviews: Evaluate (cloud vs self-hosted trade-off)
- >10M pageviews: Self-host (cost savings justified)

### 4. The Event Explosion Problem

**Observation:** Event-based pricing can escalate unpredictably

**Example:** E-commerce site with 1M pageviews/month
- Basic tracking: 1M pageviews = 1M events
- Add e-commerce: Product view, add-to-cart, checkout, purchase = 4M events
- Add search: Search query events = +500K events
- Add engagement: Scroll depth, time on page = +1M events
- **Total:** 6.5M events (6.5x initial estimate)

**PostHog Pricing:**
- 1M events: $0 (free tier)
- 3M events: ~$450/month
- 6.5M events: ~$1,100/month
- Went from free to $1,100/month by adding events

**Mitigation Strategies:**
1. **Sample non-critical events** (e.g., track 10% of scroll events)
2. **Aggregate on client** (send summary, not individual events)
3. **Event budget** (prioritize critical events, skip vanity metrics)
4. **Switch to self-hosted** (when cloud costs exceed infra + time)

**Recommendation:**
- Start lean (core events only)
- Monitor usage (set alerts at 80% of tier limit)
- Calculate cost per event ($0.00045 for PostHog)
- Self-host if monthly cost exceeds $500-1,000

### 5. The Google Analytics Dilemma

**Observation:** GA4 is free and powerful, but increasingly problematic

**Pros:**
- Free (unlimited traffic)
- Feature-rich (funnels, cohorts, BigQuery export)
- Familiar (most marketers know it)
- Google Ads integration

**Cons:**
- GDPR issues (EU court rulings against GA)
- 45KB script (page load impact)
- Cookie consent required (conversion friction)
- Privacy concerns (data sharing with Google)
- Data sampling (at high volumes)

**Use Cases Where GA4 Still Makes Sense:**
- US-only traffic (no GDPR concerns)
- Heavy Google Ads usage (attribution value)
- Enterprise with legal clearance (risk accepted)

**Use Cases Where GA4 Should Be Avoided:**
- EU customers (legal risk)
- Privacy-conscious audience (brand alignment)
- Landing pages (script size hurts conversion)
- Developer tools (audience will notice and complain)

**Migration Pattern (Common):**
- 2020-2022: Everyone used Google Analytics
- 2022-2023: GDPR rulings → panic
- 2023-2024: Migration to Plausible, Fathom, PostHog
- 2024-2025: New projects start with privacy-first

**Recommendation:** Avoid GA4 for new projects unless specific Google Ads integration requirement.

### 6. The OSS Discount Reality

**Observation:** Open-source projects get discounts, but often still too expensive

**Plausible:** 33% discount for OSS
- Regular: $9/month (10K pageviews)
- OSS: $6/month (33% off)
- Reality: $6/month is still expensive for unfunded OSS

**Alternatives for OSS:**
- GoatCounter: Free (donation-supported)
- Umami: Free (self-host for $5/month infra)
- Cloudflare: Free (basic features)

**When OSS Discount Matters:**
- Well-funded OSS projects (sponsorship, grants)
- Commercial open-source (has revenue)
- High-traffic OSS docs (10K+ pageviews, worth paying)

**When It Doesn't Help:**
- Hobby projects (no budget at all)
- Early-stage OSS (pre-community)
- Small documentation sites (<1K pageviews)

**Recommendation:** OSS projects should start with GoatCounter (free), upgrade to Plausible with discount when traffic justifies (~10K+ pageviews).

## Strategic Recommendations

### For Startups (Pre-Revenue)

**Phase 1: Validation (Month 0-6)**
- **Use:** PostHog Free Tier OR GoatCounter
- **Why:** Zero cost, full features (funnels, events)
- **Track:** Signups, activation, core user actions
- **Decision Point:** If exceed 1M events OR get funding

**Phase 2: Early Growth (Month 6-12)**
- **Use:** PostHog Paid OR Plausible
- **Why:** Scale with revenue, professional appearance
- **Track:** Full funnel, cohort retention, revenue attribution
- **Decision Point:** If traffic >1M/month OR need enterprise features

**Phase 3: Scale (Month 12+)**
- **Use:** Self-hosted PostHog OR Matomo
- **Why:** Cost optimization at scale
- **Track:** Same as before, optimized infra
- **Decision Point:** Cost vs time trade-off

### For Enterprises

**Compliance-First:**
- **Use:** Piwik PRO ($18-24K/year)
- **Why:** All certifications, audit-ready
- **Best for:** Healthcare, finance, government

**Cost-Optimized:**
- **Use:** Matomo Self-Hosted ($5-16K/year)
- **Why:** Lowest total cost with DevOps
- **Best for:** Large enterprises with infrastructure

**Feature-First:**
- **Use:** PostHog Enterprise Self-Hosted ($21-33K/year)
- **Why:** Modern analytics + open-source
- **Best for:** Tech companies, data-driven orgs

### For Privacy-Conscious Brands

**Certified Compliance:**
- **Use:** Plausible ($72-228/year)
- **Why:** GDPR Article 6(1)(f) certified
- **Best for:** EU customers, legal scrutiny

**Maximum Privacy:**
- **Use:** Self-hosted Umami or Matomo
- **Why:** Full data sovereignty
- **Best for:** Zero data sharing requirement

**Balanced:**
- **Use:** Fathom ($168-3,288/year)
- **Why:** Privacy-first, simple, affordable
- **Best for:** Non-technical teams

### For High-Traffic Sites (5M+ pageviews)

**Free Option:**
- **Use:** Cloudflare Web Analytics
- **Why:** Unlimited, free, reliable
- **Trade-off:** Basic features only

**Self-Hosted:**
- **Use:** Umami ($240-600/year) OR Matomo ($1,200-7,000/year)
- **Why:** Predictable cost vs $2,000-3,000/month cloud
- **Trade-off:** Maintenance burden

**Cloud (If Budget Allows):**
- **Use:** PostHog Cloud (~$2,250/month for 15M events)
- **Why:** Zero maintenance, full features
- **Trade-off:** Expensive at scale

## Final Recommendations

### The "Best Overall" Doesn't Exist

**There is no universal best analytics tool.** The right choice depends on:
1. Budget ($0 vs $10/month vs $1,000/month)
2. Privacy requirements (cookie-less vs user tracking)
3. Technical capacity (can self-host vs managed only)
4. Feature needs (basic stats vs funnels/cohorts)
5. Traffic volume (10K vs 10M pageviews)

### The "Safe Bet" Recommendations

**For 80% of Use Cases:**
- **Free tier needed:** PostHog (full features) or GoatCounter (simple + open-source)
- **Can pay <$30/month:** Plausible (privacy + polish) or Fathom (simplicity)
- **Enterprise:** Piwik PRO (compliance) or PostHog Enterprise (features)

**These choices cover most scenarios and have minimal regret risk.**

### The Decision Framework

```
1. What's your budget?
   $0 → PostHog Free Tier, GoatCounter, or Cloudflare
   <$30/month → Plausible or Fathom
   <$100/month → PostHog paid, Plausible Business, or self-hosted
   Enterprise → Piwik PRO or PostHog Enterprise

2. What features do you need?
   Basic stats → GoatCounter, Cloudflare, Fathom
   Funnels → PostHog, Plausible Business, Matomo
   Cohorts → PostHog, Mixpanel, Matomo
   Everything → PostHog, Piwik PRO

3. Privacy stance?
   GDPR certified required → Plausible, Piwik PRO
   Privacy-first → Fathom, Simple Analytics, GoatCounter
   Don't care → Any option

4. Can you self-host?
   Yes + want to → Umami, Matomo, PostHog
   No → Cloudflare, Plausible, Fathom, PostHog Cloud

5. Traffic volume?
   <100K → Any free or paid option
   100K-1M → Paid managed or free tiers
   1M-10M → Consider self-hosted for cost
   >10M → Self-hosted recommended
```

## Quick Start Guide

### If You're Not Sure, Start Here:

**Open-Source Project or Personal Blog:**
→ **GoatCounter** (free, open-source, custom events)

**Bootstrapped Startup or SaaS:**
→ **PostHog Free Tier** (free with funnels, worth $450/month)

**Privacy-Conscious Brand:**
→ **Plausible** ($9-19/month, GDPR certified, <1KB script)

**Enterprise:**
→ **Piwik PRO** (compliance) or **PostHog Enterprise** (features)

**Documentation Site:**
→ **GoatCounter** (OSS) or **Plausible** (commercial)

**E-commerce:**
→ **PostHog Cloud** (best funnel + revenue tracking)

**Developer Tool:**
→ **PostHog Free Tier** (event-based, technical audience)

### Migration Path

Most projects follow this evolution:
1. **Month 0-6:** Free tier (PostHog, GoatCounter, Cloudflare)
2. **Month 6-12:** Paid managed ($10-100/month)
3. **Month 12-24:** Optimize (self-host if traffic warrants)
4. **Month 24+:** Enterprise features (if needed)

**Key Trigger Points:**
- Revenue >$50K/month → Justify paid analytics
- Pageviews >1M/month → Consider self-hosting
- EU customers + legal review → Switch to certified (Plausible, Piwik PRO)
- Need compliance → Enterprise tier or certified vendor

## Conclusion

The web analytics landscape in 2025 offers excellent options for every use case. The days of "just use Google Analytics" are over. Privacy-first alternatives are mature, affordable, and often superior.

**Key Takeaways:**

1. **Free tiers are exceptional** - PostHog, GoatCounter, Cloudflare offer incredible value
2. **Privacy is a feature** - Cookie-less analytics reduce friction and build trust
3. **Self-hosting saves money at scale** - But only if you have DevOps capacity
4. **Event-based pricing requires careful planning** - Monitor usage to avoid cost explosions
5. **One size doesn't fit all** - Match provider to your specific requirements

**The Future:**
- Privacy regulations will continue tightening (use privacy-first now)
- Free tiers may become less generous (have migration plan)
- Self-hosting will grow (as cloud costs increase)
- Open-source will win (transparency and control matter)

**Start simple, measure what matters, migrate when needed.**
