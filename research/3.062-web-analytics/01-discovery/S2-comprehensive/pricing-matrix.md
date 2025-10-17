# Pricing Comparison Matrix

**Experiment:** 3.062-web-analytics
**Phase:** S2 Comprehensive Analysis
**Last Updated:** October 11, 2025

---

## Pricing Overview by Provider

This matrix compares pricing across standardized traffic tiers to help you estimate costs for your use case.

**Standardized Tiers:**
- **Personal/Blog:** 10,000 pageviews/month
- **Small Business:** 100,000 pageviews/month
- **Mid-Market:** 1,000,000 pageviews/month
- **Enterprise:** 10,000,000+ pageviews/month

**Note:** Some providers use "hits" (pageviews + events) or "events" instead of pageviews. We've normalized where possible.

---

## Cost Comparison Table

| Provider | 10K/mo | 100K/mo | 1M/mo | 10M/mo | Free Tier? | Billing Model |
|----------|--------|---------|-------|--------|------------|---------------|
| **Google Analytics 4** | FREE | FREE | FREE | FREE* | ✅ | Free (GA360 = $150K+/year) |
| **Plausible** | $9 | $19 | $69 | $249 | ❌ | Pageviews |
| **Matomo Cloud** | N/A** | $29 | $99 | $449 | ❌ | Hits (pageviews + events) |
| **Matomo Self-Hosted** | $5-10*** | $20-50*** | $100-200*** | $500-1,500*** | ✅ | Infrastructure only |
| **Fathom** | $15 | $15-25 | ~$75 | Custom | ❌ | Pageviews (opaque) |
| **Simple Analytics** | FREE†/ $15 | $15-40 | $40+ | $750+ | ✅ | Tiered |
| **Umami** | $5-10*** | $10-15*** | $20-50*** | $100-200*** | ✅ | Infrastructure only |
| **PostHog** | FREE | FREE | FREE | ~$1,500-2,000 | ✅ (1M events) | Events |
| **Cloudflare** | FREE | FREE | FREE | FREE | ✅ | Always free |
| **Piwik PRO** | N/A†† | €35+ | Custom | $50K-300K+ | ❌‡ | Tiered + Enterprise |
| **Adobe Analytics** | N/A | N/A | N/A | $100K-500K+ | ❌ | Enterprise only |
| **Mixpanel** | FREE | FREE | $140-620 | $1,500-2,289 | ✅ (1M events) | Events |

**Footnotes:**
- *GA4 free tier samples data at high volumes; GA360 ($150K-500K/year) for unsampled
- **Matomo Cloud minimum: 50K hits/month ($23/mo)
- ***Self-hosted = infrastructure costs (VPS, server, etc.)
- †Simple Analytics Free: 5 sites, 1 month retention only
- ††Piwik PRO minimum: €35/month Business plan (was free Core until Dec 2025)
- ‡Piwik PRO Core (free) discontinued December 2025

---

## Detailed Pricing Breakdown

### Privacy-First Analytics

#### Plausible Analytics
**Pricing Model:** Pageview-based, all features included

| Tier | Monthly | Annual | Websites | Features |
|------|---------|--------|----------|----------|
| 10K PV | $9 | $90 | Unlimited | All |
| 100K PV | $19 | $190 | Unlimited | All |
| 200K PV | $29 | $290 | Unlimited | All |
| 500K PV | $49 | $490 | Unlimited | All |
| 1M PV | $69 | $690 | Unlimited | All |
| 2M PV | $99 | $990 | Unlimited | All |
| 5M PV | $149 | $1,490 | Unlimited | All |
| 10M PV | $249 | $2,490 | Unlimited | All |

**Annual Discount:** 2 months free (16.7% savings)

**All Tiers Include:**
- Unlimited sites & users
- Event tracking, funnels, goals
- API access
- Email reports
- Infinite data retention
- EU data residency

**Self-Hosted (Community Edition):**
- FREE (open-source)
- Infrastructure costs: $5-50/month

---

#### Fathom Analytics
**Pricing Model:** Pageview-based (exact tiers not publicly disclosed)

**Estimated Pricing:**
- Entry tier: $15/month
- ~100K pageviews: $15-25/month
- ~1M pageviews: ~$75/month
- 10M+: Contact for custom pricing

**Additional Sites:**
- First 50 sites included
- +$14/month per additional 50 sites

**All Tiers Include:**
- Unlimited sites (up to 50)
- Unlimited users
- Event tracking
- Uptime monitoring
- Email/Slack reports
- API access
- Ad-blocker bypass
- Lifetime data retention
- EU routing for EU traffic

**Trial:** 7 days free (no credit card)

---

#### Simple Analytics
**Pricing Model:** Tiered subscription

| Tier | Price/Mo | Users | Websites | Retention | API |
|------|----------|-------|----------|-----------|-----|
| **Free** | $0 | 1 | 5 | 1 month | ❌ |
| **Simple** | $15 | 1 | 10 | 3 years | ❌ |
| **Team** | $40 | 2 | 20 | 5 years | ✅ |
| **Enterprise** | $750+ | Custom | Custom | Custom | ✅ |

**Trial:** 14 days free (no credit card)

**Pageview Limits:** Not clearly specified per tier

---

#### Cloudflare Web Analytics
**Pricing:** FREE forever

**Includes:**
- Unlimited websites
- Unlimited pageviews
- Basic analytics
- Performance monitoring
- Core Web Vitals
- 6-month data retention (only)

**Limitations:**
- No events/goals
- No API
- 6-month retention maximum
- No advanced features

---

### Full-Featured Analytics

#### Google Analytics 4 (GA4)
**Standard (Free):**
- $0/month
- 10 million events/month (soft limit)
- Data sampling at high volumes
- 14-month data retention max
- All standard features
- BigQuery export (limited)

**Google Analytics 360 (Enterprise):**
- $150,000 - $500,000/year (negotiable)
- 1 billion events/month
- Unsampled reports
- 50-month data retention
- SLA guarantees
- Dedicated support
- BigQuery streaming export

**Pricing Factors (GA360):**
- Base platform fee: ~$150K/year
- Volume discounts available
- Implementation: $20K-100K+
- Training: $5K-20K
- **Total first-year cost:** $200K-500K+

---

#### Matomo
**Pricing Model:** Dual - Cloud (SaaS) or Self-Hosted (free software)

**Matomo Cloud (Monthly, billed annually):**

| Monthly Hits | Price/Mo | Max Sites | Tier |
|--------------|----------|-----------|------|
| 50K | $23 | 30 | Starter |
| 100K | $29 | 30 | Business |
| 500K | $59 | 50 | Business |
| 1M | $99 | 100 | Business |
| 5M | $249 | Unlimited | Enterprise |
| 10M | $449 | Unlimited | Enterprise |
| 50M | $1,290 | Unlimited | Enterprise |
| 100M | $1,990 | Unlimited | Enterprise |

**"Hits" = pageviews + events + downloads + outbound clicks (typically 2-3x pageviews)**

**Premium Plugins (Add-ons):**
- Heatmaps & Session Recording: $199-899/year
- A/B Testing: $199-899/year
- Form Analytics: $99-499/year
- Media Analytics: $99-499/year

**Matomo On-Premise (Self-Hosted):**
- **Software:** FREE (GPL v3)
- **Infrastructure:** $5-500+/month depending on scale
- **Maintenance:** 2-5 hours/month
- **Premium Plugins:** Same pricing as cloud (optional)

**Total Cost Examples (Self-Hosted):**
- 100K pageviews: $20-50/month (VPS)
- 1M pageviews: $100-200/month (larger VPS)
- 10M pageviews: $500-1,500/month (dedicated infrastructure)

---

### Self-Hosted Open-Source

#### Umami
**Software:** FREE (MIT license, open-source)

**Infrastructure Costs (Self-Hosted):**
- **Small site (<100K events):** $5-10/month (basic VPS)
- **Medium site (100K-1M events):** $10-30/month
- **Large site (1M-10M events):** $50-200/month
- **Very large (10M+ events):** $200+/month (requires optimization)

**Requirements:**
- VPS with 2GB RAM minimum
- PostgreSQL, MySQL, or MariaDB
- Docker recommended

**Cloud Hosting (Umami Cloud):**
- Managed option available
- Pricing not widely published (contact for quote)

**Total Cost of Ownership:**
- Direct: $5-50/month (infrastructure)
- Setup: 1-2 hours
- Maintenance: 1-2 hours/month

---

### Product Analytics Platforms

#### PostHog
**Pricing Model:** Usage-based (events)

**Free Tier:**
- 1 million events/month FREE
- 10K session replays
- Unlimited users
- All features

**Paid Pricing:**
- Product Analytics: $0.00031/event (after free tier)
- Session Replay: $0.005/replay
- Feature Flags: $0.0001/request
- Surveys: $0.20/response

**Cost Examples:**
- 1M events/month: **FREE**
- 3M events/month: ~$620/month
- 10M events/month: ~$1,500-2,000/month
- 20M events/month: ~$2,289/month

**Notes:**
- Anonymous events: 4x cheaper than identified
- No storage fees, no monthly minimums
- Self-hosted: FREE (infrastructure costs only)

**Startup Program:**
- First year FREE
- Early-stage companies (<5 years, <$8M funding)

---

#### Mixpanel
**Pricing Model:** Event-based

**Free Plan:**
- 1M events/month
- 10K session replays
- Unlimited seats
- Basic features

**Growth Plan:**
- Starts at $20+/month
- $140 for 1.5M events
- $2,289 for 20M events

**Enterprise Plan:**
- Starts at $833+/month
- Unlimited events
- Advanced features
- Can reach $200K/year at scale

**Startup Program:**
- First year free
- <5 years old, <$8M funding

---

### Enterprise Platforms

#### Piwik PRO
**Pricing Model:** Tiered + Custom Enterprise

**Business Plan:**
- **Starting:** €35/month (~$38/month)
- Small to mid-size businesses
- Core analytics + Tag Manager + Consent Manager
- EU cloud (Sweden)

**Enterprise Tiers:**

1. **Trusted Insights**
   - Growth-oriented organizations
   - Advanced analytics, cross-channel integration
   - Up to 500M monthly actions
   - Price: Custom (estimated $25K-50K/year)

2. **Secure Intelligence**
   - Highly regulated industries
   - Maximum security, unlimited reporting
   - Private cloud hosting options
   - Price: Custom (estimated $50K-100K/year)

3. **On-Premise/Ultimate**
   - Full on-premise deployment
   - Complete customization
   - Price: Custom (estimated $100K-300K+/year)

**Note:** Free "Core" plan discontinued December 2025

---

#### Adobe Analytics
**Pricing Model:** Enterprise custom pricing

**Tiers:**
- **Select:** ~$100,000/year (basic enterprise)
- **Prime:** ~$150,000-250,000/year (advanced features)
- **Ultimate:** ~$250,000-500,000+/year (predictive intelligence)

**Total First-Year Cost:**
- Platform: $100K-500K
- Implementation: $50K-200K
- Training: $10K-50K
- **Total:** $200K-750K+

**Pricing Factors:**
- Product capabilities (CJA, Web, Mobile, Content, Product)
- Data volume
- Number of users/seats
- Support level (Select/Prime/Ultimate)

**Target Market:** Fortune 500, large enterprises only

---

## Cost Comparison by Use Case

### Personal Blog (10K pageviews/month)
| Provider | Monthly Cost | Annual Cost | Notes |
|----------|--------------|-------------|-------|
| **Cloudflare** | $0 | $0 | Free, 6-month retention |
| **Google Analytics** | $0 | $0 | Free, GDPR concerns |
| **Simple Analytics** | $0 (Free tier) | $0 | 5 sites, 1-month retention |
| **PostHog** | $0 | $0 | 1M events free |
| **Umami (self-hosted)** | $5-10 | $60-120 | Infrastructure |
| **Plausible** | $9 | $90 | Best paid option |
| **Fathom** | $15 | $180 | Ad-blocker bypass |

**Recommendation:** Cloudflare (free) or Plausible ($9) if paying

---

### Small Business (100K pageviews/month)
| Provider | Monthly Cost | Annual Cost | Notes |
|----------|--------------|-------------|-------|
| **Google Analytics** | $0 | $0 | Free, compliance work |
| **Cloudflare** | $0 | $0 | Free, basic features |
| **PostHog** | $0 | $0 | If <1M events |
| **Umami (self-hosted)** | $10-15 | $120-180 | Infrastructure |
| **Plausible** | $19 | $190 | Clean, simple |
| **Fathom** | $15-25 | $180-300 | Ad-blocker bypass |
| **Matomo Cloud** | $29 | $348 | Full features |
| **Simple Analytics** | $15-40 | $180-480 | Depends on tier |

**Recommendation:** Plausible ($19) or Matomo Cloud ($29) for full features

---

### Mid-Market (1M pageviews/month)
| Provider | Monthly Cost | Annual Cost | Notes |
|----------|--------------|-------------|-------|
| **Google Analytics** | $0 | $0 | Free, may sample data |
| **Cloudflare** | $0 | $0 | Too basic |
| **Umami (self-hosted)** | $20-50 | $240-600 | Infrastructure |
| **Simple Analytics** | $40+ | $480+ | Limited features |
| **Plausible** | $69 | $690 | Clean privacy analytics |
| **Fathom** | ~$75 | ~$900 | Privacy + ad-block bypass |
| **Matomo Cloud** | $99 | $1,188 | Full GA-like features |
| **Matomo Self-Hosted** | $100-200 | $1,200-2,400 | If you can manage |

**Recommendation:** Plausible ($69) for privacy-first, Matomo Cloud ($99) for full features

---

### Enterprise (10M pageviews/month)
| Provider | Monthly Cost | Annual Cost | Notes |
|----------|--------------|-------------|-------|
| **Google Analytics (Free)** | $0 | $0 | Data sampling likely |
| **Plausible** | $249 | $2,490 | Privacy-first, simple |
| **Matomo Cloud** | $449 | $5,388 | Full features, GDPR |
| **Matomo Self-Hosted** | $500-1,500 | $6K-18K | Infrastructure + ops |
| **PostHog** | ~$1,500-2,000 | ~$18K-24K | If event-based |
| **Piwik PRO** | Custom | $50K-300K+ | Regulated industries |
| **Google Analytics 360** | $12,500+ | $150K-500K | Unsampled, SLA |
| **Adobe Analytics** | $8,300+ | $100K-500K+ | Full enterprise suite |

**Recommendation:**
- Privacy-first: Plausible ($249) or Matomo Self-Hosted
- Full-featured GDPR: Matomo Cloud ($449) or Piwik PRO
- Unsampled enterprise: GA360 or Adobe (if budget allows)

---

## Hidden Costs to Consider

### Implementation & Setup
- **DIY (Simple Tools):** 1-4 hours of dev time
- **GA4 Proper Setup:** $5K-50K (GDPR compliance, goals, tracking plan)
- **Matomo Enterprise:** $10K-50K (consultant, configuration)
- **Adobe/Enterprise:** $50K-200K+ (implementation partners)

### Maintenance (Self-Hosted)
- **Time:** 1-5 hours/month (updates, monitoring, backups)
- **Human Cost:** $50-500/month (opportunity cost or outsourced)
- **Infrastructure Scaling:** Costs increase with traffic

### Compliance & Legal
- **Cookie Consent Tool:** $0-500/month (if needed for GA4)
- **Legal Review:** $2K-10K (privacy policy, GDPR compliance)
- **DPO/Privacy Team:** Ongoing cost for large organizations

### Training
- **Simple Tools:** Minimal (self-service)
- **GA4:** $1K-10K (courses, consultants)
- **Enterprise:** $10K-50K+ (vendor training, enablement)

---

## Total Cost of Ownership (TCO) Examples

### Small Business Scenario (100K pageviews/month)

**Option 1: Google Analytics (Free)**
- Platform: $0
- Cookie consent tool: $10-30/month
- Legal review: $2K one-time
- Compliance overhead: 5-10 hours/month
- **TCO Year 1:** $2,000-5,000

**Option 2: Plausible ($19/month)**
- Platform: $228/year
- No consent needed: $0
- No compliance overhead: 0 hours
- **TCO Year 1:** $228

**Winner:** Plausible (lower TCO, less headache)

---

### Enterprise Scenario (10M pageviews/month)

**Option 1: Matomo Self-Hosted**
- Infrastructure: $1,000/month ($12K/year)
- Implementation: $20K one-time
- Maintenance: 5 hours/month ($3K/year opportunity cost)
- **TCO Year 1:** $35,000

**Option 2: Matomo Cloud ($449/month)**
- Platform: $5,388/year
- No infrastructure management
- **TCO Year 1:** $5,388

**Option 3: Google Analytics 360**
- Platform: $150K/year
- Implementation: $50K one-time
- Training: $10K
- **TCO Year 1:** $210,000

**Winner:** Depends on needs
- Lowest cost: Matomo Cloud ($5,388)
- Most control: Matomo Self-Hosted ($35K)
- Unsampled enterprise: GA360 ($210K)

---

## Pricing Model Summary

| Provider | Model | Free Tier | Best For |
|----------|-------|-----------|----------|
| **Google Analytics** | Free | ✅ Unlimited | Zero budget, accepting GDPR work |
| **Plausible** | Per-pageview | ❌ | Predictable privacy analytics |
| **Matomo** | Hits (Cloud) / Infra (Self) | ✅ Self-hosted | Full features + privacy |
| **Fathom** | Per-pageview (opaque) | ❌ | Ad-blocker bypass + privacy |
| **Simple Analytics** | Tiered | ✅ Limited | Small projects |
| **Umami** | Infrastructure only | ✅ | Developer self-hosters |
| **PostHog** | Per-event | ✅ 1M events | Product analytics needs |
| **Cloudflare** | Always free | ✅ | Basic analytics, zero budget |
| **Piwik PRO** | Tiered + Enterprise | ❌ | Regulated industries |
| **Adobe** | Enterprise custom | ❌ | Fortune 500 only |

---

**Next:** See privacy-matrix.md for GDPR compliance comparison
