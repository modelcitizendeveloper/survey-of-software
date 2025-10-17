# Fathom Analytics

**Category:** Privacy-First Analytics
**Hosting:** Cloud (managed, EU/CA infrastructure)
**Pricing Model:** Usage-based (pageviews)
**Primary Market:** Privacy-conscious businesses, agencies
**Website:** https://usefathom.com/

---

## Overview

Fathom Analytics is a privacy-first, cookie-free web analytics platform founded in 2018 as a simple, compliant alternative to Google Analytics. Fathom pioneered ad-blocker bypass techniques while maintaining visitor privacy, and focuses on delivering essential insights without complexity.

**Market Position:** Premium privacy analytics, targeting businesses and agencies that value both privacy and complete visitor data (ad-blocker bypass).

**Philosophy:** "Website analytics without compromise" - privacy-first with maximum data coverage.

---

## Core Features

### Basic Analytics
- **Traffic Measurement:** Pageviews, unique visitors, average time, bounce rate
- **Traffic Sources:** Referrers, UTM campaigns, search terms
- **Geographic Data:** Country-level tracking
- **Device Tracking:** Browser, device type, OS
- **Real-time Analytics:** Live visitor dashboard

### Advanced Capabilities
- **Event Tracking:** Custom events with automatic revenue tracking
- **Email Reports:** Scheduled weekly/monthly reports
- **Uptime Monitoring:** Basic website uptime checks (email/Slack/Telegram alerts)
- **Google Analytics Import:** Transfer historical GA data (one-click)
- **Shared Links:** Public/private dashboard sharing
- **Multi-site Dashboard:** Roll-up reporting across properties
- **API Access:** Stats API for custom integrations

### Key Innovation: Ad-Blocker Bypass
- **Proprietary Technology:** Routes tracking through your domain to bypass blockers
- **Privacy-Preserving:** No personal data collected despite bypass
- **Result:** ~99% visitor tracking vs ~70-80% with standard analytics

### Integrations
- **Platforms:** WordPress, Shopify, Webflow, Wix, Squarespace plugins
- **Notifications:** Email, Slack, Telegram (traffic spikes, uptime)
- **Import:** Google Analytics historical data import

### Limitations
- **No User-Level Tracking:** Anonymous by design
- **Country-Level Geo Only:** No city/region data
- **Basic Segmentation:** Limited filtering vs GA
- **No Demographics:** Age, gender, interests not available
- **No Funnels:** Simple goal tracking only

---

## Pricing Structure

### Pricing Tiers (2025)

**All Plans Include:**
- Unlimited websites (up to 50)
- Unlimited team members
- All features (no paywalls)
- Email reports
- Uptime monitoring
- API access
- Ad-blocker bypass
- Lifetime data retention
- EU routing for EU traffic

**Pricing (Monthly):**
- **7-Day Free Trial:** No credit card required
- **Starting at $15/month** for base tier

**Note:** Fathom doesn't publish exact pageview tiers publicly. Pricing is customized based on:
- Total monthly pageviews across all sites
- Number of sites (50+ requires custom pricing)

**Estimated Pricing (Based on Industry Reports):**
- **Up to 100K pageviews:** ~$15/month
- **Up to 250K pageviews:** ~$25/month
- **Up to 500K pageviews:** ~$45/month
- **Up to 1M pageviews:** ~$75/month
- **Above 1M:** Contact for custom pricing

**Additional Sites:**
- First 50 sites included
- $14/month for each additional 50 sites

**Cost Comparison:**
- **Personal/Blog (10K pageviews):** ~$15/month
- **Small Business (100K pageviews):** ~$15-25/month
- **Mid-Market (1M pageviews):** ~$75/month
- **Enterprise (10M pageviews):** Custom pricing (estimated $200-300/month)

**Annual Billing:** Available (typically 10-15% discount)

---

## Privacy & Compliance

### GDPR Compliance
**Status:** ✅ **Fully compliant by design**

**Why Compliant:**
- No personal data collected
- No cookies used
- No persistent identifiers
- Anonymizes IP addresses
- No cross-site/cross-device tracking

**Data Retention:**
- Pseudo-anonymized data: 48 hours (then removed)
- Aggregated stats: Stored indefinitely
- No way to identify individual visitors

### CCPA/PECR Compliance
- **Status:** ✅ Fully compliant
- **Reason:** No personal information collected

### Cookie Requirements
- **Cookies Used:** ZERO
- **Cookie Banner Required:** NO
- **Consent Required:** NO (anonymous tracking)

**Legal Opinion:** Fathom doesn't require consent under GDPR/CCPA.

### Data Residency
- **Company:** Canadian (GDPR adequacy ruling)
- **EU Traffic Routing:** Automatically routed through EU infrastructure
- **Infrastructure:** European-owned for EU visitors
- **Global:** US infrastructure for non-EU traffic

### Impact on Analytics
- **Data Accuracy:** ~98-99% with ad-blocker bypass
- **No Consent Loss:** 100% tracking (no cookie banner declines)
- **Ad-Blocker Impact:** Minimal (~1-2% blocked with bypass enabled)

---

## Implementation

### JavaScript Snippet
```html
<!-- Fathom - simple website analytics -->
<script src="https://cdn.usefathom.com/script.js" data-site="ABCDEFG" defer></script>
<!-- / Fathom -->
```

**Size:** Small, lightweight script (exact size not disclosed)

### Installation Methods
1. **Direct Script:** One-line snippet in HTML
2. **CMS Plugins:** WordPress, Shopify, Webflow, Wix, Squarespace
3. **Framework SDKs:** React, Vue, Next.js libraries
4. **Custom Domain Proxying:** Route through your domain for bypass

### Ad-Blocker Bypass Setup
- **Automatic:** Fathom provides custom subdomain routing
- **Custom Domain:** Use your own subdomain (e.g., stats.yourdomain.com)
- **Result:** Appears as first-party request, bypasses blockers

### Technical Requirements
- JavaScript enabled
- No cookies needed
- No third-party dependencies

### Difficulty Level: 2/10
- **Simple:** One-line script installation
- **Bypass Setup:** Additional DNS configuration (optional)
- **Zero Configuration:** Works immediately

### Time to First Insights
- **Setup:** 5 minutes
- **Data Collection:** Immediate (real-time)
- **Bypass Configuration:** +15-30 minutes (DNS setup)

---

## Data Ownership & Portability

### Data Ownership
- **You Own Your Data:** Fathom processes but doesn't sell/share
- **Privacy:** No access to individual visitor data (anonymized)

### Data Export
- **API Access:** Full Stats API
- **CSV Export:** Manual export available
- **Google Analytics Import:** One-way import from GA

### Migration Paths
- **From GA to Fathom:** Import tool (historical data)
- **From Fathom to Other:** Export via API/CSV
- **Vendor Lock-in:** LOW - Standard export formats

### Self-Hosting
- **Available:** NO - Cloud-only (closed-source)

---

## Pros and Cons

### Pros ✅
1. **Privacy-First:** GDPR/CCPA compliant, no consent needed
2. **Ad-Blocker Bypass:** Industry-leading visitor coverage (~99%)
3. **No Cookies:** Zero cookie banners
4. **Simple Interface:** Clean, easy-to-read dashboard
5. **Uptime Monitoring:** Bonus feature included
6. **EU Routing:** Automatic EU infrastructure for EU traffic
7. **Unlimited Sites/Users:** All tiers include unlimited
8. **GA Import:** Easy migration from Google Analytics
9. **Fast Support:** Responsive customer service
10. **Canadian Company:** GDPR adequacy, not US-based

### Cons ❌
1. **Closed-Source:** No self-hosting, proprietary code
2. **Higher Price:** $15+ vs Plausible $9
3. **Opaque Pricing:** No public pricing tiers
4. **Limited Features:** No funnels, cohorts, advanced segmentation
5. **Country-Level Geo Only:** No city data
6. **No Demographics:** Age, gender not available
7. **Basic Event Tracking:** Not suitable for product analytics
8. **Vendor Lock-in:** No self-hosting option (vs Plausible/Matomo)

---

## Best Fit Scenarios

### Ideal For ✅
- **Agencies:** Managing multiple client sites (unlimited sites)
- **Ad-Blocker Concern:** Need maximum visitor coverage
- **Privacy-Conscious Brands:** GDPR compliance without compromise
- **Simple Analytics Needs:** Traffic, referrers, conversions
- **EU-Focused:** Automatic EU routing valuable
- **GA Migrators:** Easy import from Google Analytics
- **Uptime Monitoring:** Want analytics + uptime in one tool

### Not Ideal For ❌
- **Budget-Constrained:** Plausible cheaper ($9 vs $15)
- **Open-Source Requirement:** Need self-hosting (use Plausible/Umami)
- **Complex Analytics:** Need funnels, cohorts, user journeys
- **Transparent Pricing:** Prefer clear tier structure
- **High-Volume Sites:** Self-hosting more cost-effective

---

## Strategic Positioning

**Market Position:** Premium privacy analytics with ad-blocker bypass as key differentiator.

**2025 Trends:**
- Strong agency adoption (unlimited sites)
- Ad-blocker bypass increasingly valuable
- Canadian jurisdiction attractive post-Privacy Shield
- Competing with Plausible on features, price

**Competitive Advantages:**
- Ad-blocker bypass technology
- Uptime monitoring included
- Canadian jurisdiction
- Unlimited sites/users

**Key Differentiator:** Ad-blocker bypass with privacy preservation

**Major Limitation:** Closed-source, higher pricing than competitors

---

## Comparison with Alternatives

**vs Plausible:**
- Privacy: Tied (both GDPR-compliant)
- Price: Plausible cheaper ($9 vs $15)
- Ad-blocker Bypass: Fathom wins (proprietary tech)
- Open-source: Plausible wins (Fathom closed)
- Features: Tied (similar capabilities)

**vs Google Analytics:**
- Privacy: Fathom wins (GDPR-compliant)
- Features: GA wins (more advanced)
- Price: GA free, Fathom $15+
- Ad-blocker: Fathom wins (bypass vs blocked)

**vs Simple Analytics:**
- Price: Tied (both ~$15)
- Features: Tied (similar)
- Ad-blocker: Fathom wins (bypass tech)
- Transparency: Simple wins (public pricing)

---

## Recommendation Summary

**Use Fathom if:**
- Ad-blocker bypass is critical (maximize visitor coverage)
- You manage multiple sites (agencies)
- You want privacy + uptime monitoring combo
- You value Canadian jurisdiction over EU
- You're willing to pay premium for complete data

**Avoid Fathom if:**
- You need lowest-cost privacy analytics (use Plausible)
- You require open-source/self-hosting
- You need transparent public pricing
- You need advanced features (funnels, cohorts)
- Budget is primary concern

**Migration Considerations:**
- Moving TO Fathom: Easy (GA import tool)
- Moving FROM Fathom: Moderate (API export, closed-source)

---

**Last Updated:** October 11, 2025
**Pricing:** Contact for exact tiers (estimated based on reports)
**Compliance Status:** Fully GDPR/CCPA compliant
**Unique Feature:** Ad-blocker bypass with privacy preservation
