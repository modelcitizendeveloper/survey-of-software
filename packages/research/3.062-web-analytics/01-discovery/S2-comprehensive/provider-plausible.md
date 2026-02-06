# Plausible Analytics

**Category:** Privacy-First Analytics
**Hosting:** Cloud (EU-based) or Self-Hosted
**Pricing Model:** Usage-based (pageviews)
**Primary Market:** Privacy-conscious SMBs, blogs, SaaS
**Website:** https://plausible.io/

---

## Overview

Plausible Analytics is a lightweight, open-source, privacy-first web analytics platform designed as a simple, GDPR-compliant alternative to Google Analytics. Founded in 2019, Plausible has gained significant traction among privacy-conscious website owners who want clean insights without cookies, tracking, or privacy concerns.

**Market Position:** Leading privacy-first alternative to Google Analytics, targeting developers and privacy-aware businesses who want simple analytics without compliance overhead.

**Philosophy:** "All essential insights on one page in one minute" - radical simplicity with zero configuration needed.

---

## Core Features

### Basic Analytics
- **Traffic Measurement:** Pageviews, unique visitors, visit duration, bounce rate
- **Traffic Sources:** Referrers (top sources, top pages, UTM campaigns)
- **Geographic Data:** Country-level tracking (no city-level to protect privacy)
- **Device Tracking:** Browser, OS, device type (desktop/mobile/tablet)
- **Real-time Analytics:** Live visitor count

### Advanced Capabilities
- **Goals & Conversions:** Custom event tracking, pageview goals, custom events
- **Funnels:** Multi-step conversion funnel analysis
- **Custom Properties:** Event metadata for deeper insights
- **Outbound Link Tracking:** Clicks to external sites
- **404 Error Tracking:** Identify broken pages
- **File Downloads:** Track PDF, ZIP, etc. downloads
- **Engagement Metrics:** Scroll depth, time on page

### Integrations
- **Email Reports:** Weekly/monthly automated reports
- **Slack/Webhook:** Traffic spike notifications
- **API Access:** Stats API for custom dashboards
- **Import from GA:** One-click import of Google Analytics historical data
- **Shared Links:** Public/private dashboard sharing

### Limitations
- **No User-Level Data:** Cannot track individual users (by design)
- **No Demographics:** No age, gender data (privacy-focused)
- **No Attribution Modeling:** Basic first-touch attribution only
- **No Cohort Analysis:** Cannot track user cohorts over time
- **Limited Filtering:** Simpler segmentation vs GA4

---

## Pricing Structure

### Cloud-Hosted (Managed)

**Pricing Tiers (Monthly):**
- **Up to 10K pageviews:** $9/month
- **Up to 100K pageviews:** $19/month
- **Up to 200K pageviews:** $29/month
- **Up to 500K pageviews:** $49/month
- **Up to 1M pageviews:** $69/month
- **Up to 2M pageviews:** $99/month
- **Up to 5M pageviews:** $149/month
- **Up to 10M pageviews:** $249/month
- **Above 10M:** Custom enterprise pricing

**Annual Billing:** 2 months free (pay for 10, get 12)

**Included in All Tiers:**
- Unlimited websites
- Unlimited team members
- All features (no feature paywalls)
- Email/Slack reports
- API access
- Historical data retention (infinite)
- EU data residency

**Cost Comparison:**
- **Personal/Blog (10K pageviews):** $9/month ($90/year annual)
- **Small Business (100K pageviews):** $19/month ($190/year annual)
- **Mid-Market (1M pageviews):** $69/month ($690/year annual)
- **Enterprise (10M pageviews):** $249/month ($2,490/year annual)

### Self-Hosted (Community Edition)

**Cost:** FREE (open-source)
- **Infrastructure:** Your own server costs ($5-50/month depending on scale)
- **Maintenance:** Self-managed updates, backups, monitoring
- **Features:** All features from cloud version
- **Support:** Community support only

**Hosting Requirements:**
- VPS with 2GB RAM minimum
- PostgreSQL or ClickHouse database
- Docker deployment recommended

**Estimated Total Cost (Self-Hosted):**
- **Small site:** $5-10/month (basic VPS)
- **Medium site:** $20-50/month (larger VPS)
- **Large site:** $100+/month (dedicated infrastructure)

---

## Privacy & Compliance

### GDPR Compliance
**Status:** ✅ **Fully compliant by design**

**Why Compliant:**
- No personal data collected
- No cookies used
- No persistent identifiers
- No cross-site tracking
- No cross-device tracking
- All data anonymized at collection

**Data Processing:**
- Daily rotating hash of IP + User-Agent (anonymized)
- IP address never stored
- No user fingerprinting

### CCPA/PECR Compliance
- **Status:** ✅ Fully compliant
- **Reason:** No personal information collected

### Cookie Requirements
- **Cookies Used:** ZERO
- **Cookie Banner Required:** NO
- **Consent Required:** NO (anonymous tracking)

**Legal Opinion:** Most privacy lawyers agree Plausible doesn't require consent notices under GDPR/CCPA due to fully anonymized data collection.

### Data Residency
- **Cloud Infrastructure:** 100% EU-based (Hetzner, Germany)
- **Data Processing:** Never leaves EU
- **Company Location:** Estonia (EU)
- **Compliance:** EU data residency guaranteed

### Impact on Analytics
- **Data Accuracy:** ~95-98% of visitors tracked (ad blockers less aggressive)
- **No Consent Loss:** 100% of visitors tracked (no cookie banner declines)
- **Ad Blocker Impact:** ~5-10% blocked (better than GA at ~20-30%)

---

## Implementation

### JavaScript Snippet
```html
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>
```

**That's it!** Single line, 1.9KB script (75x smaller than Google Analytics).

### Installation Methods
1. **Direct Script:** One-line snippet in HTML header
2. **CMS Plugins:** WordPress, Ghost, Hugo, etc.
3. **Framework Integrations:** Next.js, Nuxt, SvelteKit plugins
4. **Proxy Script:** Optional self-proxying to avoid ad blockers
5. **Self-Hosted:** Docker deployment on your infrastructure

### Technical Requirements
- JavaScript enabled
- No third-party cookies needed
- Works with all modern browsers
- Respects Do Not Track (if configured)

### Difficulty Level: 1/10
- **Simplest installation possible:** Single line of code
- **Zero configuration:** Works out of the box
- **No complexity:** No goals, views, filters to set up initially

### Time to First Insights
- **Setup:** 2 minutes (copy-paste script)
- **Data collection:** Immediate (real-time)
- **Meaningful data:** 24 hours

---

## Data Ownership & Portability

### Data Ownership
- **Cloud Version:** You own your data, Plausible processes it
- **Self-Hosted:** Complete ownership and control
- **Privacy:** Plausible cannot sell or share your data

### Data Export
- **API Access:** Full Stats API for all data
- **CSV Export:** Manual export available
- **Database Access:** Self-hosted version = direct DB access
- **Google Analytics Import:** Import historical GA data on signup

### Migration Paths
- **From GA to Plausible:** Import tool available (historical data)
- **From Plausible to Other:** Export via API, CSV
- **Vendor Lock-in:** LOW - Open-source, standard formats

### Self-Hosting
- **Available:** YES - Community Edition (CE)
- **License:** AGPL v3 (open-source)
- **Migration:** Can move between cloud and self-hosted anytime

---

## Pros and Cons

### Pros ✅
1. **Privacy-First:** GDPR/CCPA compliant by design, no consent needed
2. **Simple Interface:** One-page dashboard, zero learning curve
3. **Lightweight:** 1.9KB script (75x smaller than GA), fast page loads
4. **No Cookies:** Zero cookie banners needed
5. **EU Data Residency:** All data stays in EU
6. **Open Source:** Transparent code, self-hosting option
7. **Unlimited Everything:** Sites, users, data retention on all tiers
8. **Better Ad-Block Resistance:** Lower block rates than GA
9. **Predictable Pricing:** Clear pageview-based pricing
10. **Great Support:** Responsive team, active community

### Cons ❌
1. **Limited Features:** No user-level tracking, cohorts, advanced segmentation
2. **Basic Attribution:** First-touch only, no multi-touch models
3. **No Demographics:** Age, gender, interests not available
4. **Country-Level Only:** No city-level geo data
5. **Paid Service:** $9+/month vs free GA (though cheaper than compliance overhead)
6. **Learning Curve:** Different metrics than GA (transition adjustment)
7. **No Predictive Analytics:** No AI/ML features
8. **Limited Integrations:** Fewer third-party integrations than GA

---

## Best Fit Scenarios

### Ideal For ✅
- **EU-Focused Businesses:** Need GDPR compliance without headaches
- **Privacy-Conscious Brands:** Value visitor privacy, avoid tracking
- **Blogs & Content Sites:** Need simple traffic stats
- **SaaS Landing Pages:** Track conversions without cookies
- **Developer Projects:** Want lightweight, fast analytics
- **Marketing Agencies:** Manage multiple client sites
- **No Google Ads:** Don't need Google ecosystem integration
- **Simple Needs:** Pageviews, referrers, top content sufficient

### Not Ideal For ❌
- **Complex Funnels:** Need detailed user journey tracking
- **User Segmentation:** Require cohort analysis, user-level data
- **Demographics:** Need age, gender, interest targeting
- **Multi-Touch Attribution:** Complex marketing attribution
- **Zero Budget:** Need completely free solution
- **Enterprise Analytics:** Require unsampled data, advanced features

---

## Strategic Positioning

**Market Position:** Leading privacy-first analytics, successfully positioned as "Simple Analytics without privacy concerns."

**2025 Trends:**
- Growing EU adoption due to GA GDPR issues
- Increasing enterprise trials (moving from GA)
- Competitive pricing vs Fathom/Simple Analytics
- Strong open-source community

**Competitive Advantages:**
- Open-source (transparency + self-hosting)
- Aggressive pricing ($9 entry point)
- EU data residency
- Simplest interface in category

**Key Differentiator:** Privacy compliance + simplicity + affordability

**Major Limitation:** Feature depth for complex analytics needs

---

## Comparison with Alternatives

**vs Google Analytics:**
- Privacy: Plausible wins (GDPR compliant)
- Features: GA wins (more advanced)
- Price: GA free, Plausible paid
- Simplicity: Plausible wins (1 dashboard)
- Compliance: Plausible wins (no consent needed)

**vs Fathom Analytics:**
- Privacy: Tied (both privacy-first)
- Price: Plausible cheaper ($9 vs $15)
- Features: Tied (similar feature sets)
- Open-source: Plausible wins (Fathom closed-source)

**vs Matomo:**
- Privacy: Tied (both GDPR-compliant)
- Simplicity: Plausible wins (Matomo complex)
- Features: Matomo wins (more advanced)
- Price: Plausible more predictable

---

## Recommendation Summary

**Use Plausible if:**
- EU privacy compliance is critical
- You want simple, clean analytics
- You value visitor privacy
- You don't need user-level tracking
- You want to avoid cookie banners
- You prefer lightweight scripts
- You're willing to pay for privacy/simplicity

**Avoid Plausible if:**
- You need free analytics (use GA or self-host)
- You require advanced segmentation
- You need demographics/interests
- You need multi-touch attribution
- You have complex funnel analysis needs

**Migration Considerations:**
- Moving TO Plausible: Easy (import GA data)
- Moving FROM Plausible: Easy (API export)

---

**Last Updated:** October 11, 2025
**Pricing Verified:** October 2025
**Compliance Status:** Fully GDPR/CCPA compliant
