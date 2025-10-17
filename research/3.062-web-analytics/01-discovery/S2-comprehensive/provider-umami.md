# Umami Analytics

**Category:** Self-Hosted Open-Source Analytics
**Hosting:** Self-Hosted (cloud hosting available)
**Pricing Model:** Free (open-source) + optional cloud hosting
**Primary Market:** Developers, privacy-conscious self-hosters
**Website:** https://umami.is/

---

## Overview

Umami is a modern, privacy-focused, open-source web analytics platform. It provides essential website insights while prioritizing data privacy and user control through self-hosting. Lightweight and easy to deploy.

**Market Position:** The easiest self-hosted analytics solution for developers who want privacy without complexity.

**Philosophy:** "Own your data. Simple, privacy-focused, and easy to use."

---

## Core Features

### Basic Analytics
- Pageviews, unique visitors, bounce rate
- Referrers and traffic sources
- Pages, countries, devices, browsers, OS
- Real-time tracking

### Advanced Capabilities
- Custom events tracking
- Simple filtering and date ranges
- Multi-website support
- Team collaboration (multi-user)
- Public/shared dashboards

### Integrations
- API for custom integrations
- Export limited to CSV

### Limitations
- **No Advanced Features:** No automatic event capture, segmentation, heatmaps, session recordings
- **No User-Level Tracking:** Privacy by design
- **Limited Reporting:** Cannot create custom reports
- **CSV Export Only:** No advanced data export

---

## Pricing Structure

### Self-Hosted (Free)
**Software Cost:** $0 (open-source, MIT license)

**Infrastructure Costs:**
- **VPS Hosting:** $5-20/month (DigitalOcean, Hetzner, Linode)
- **Database:** PostgreSQL, MySQL, MariaDB (included in VPS)
- **Small sites (<100K events/month):** $5-10/month
- **Medium sites (100K-1M events/month):** $10-30/month
- **Large sites (1M+ events/month):** $50+/month (may need optimization)

**Technical Requirements:**
- Node.js environment
- PostgreSQL, MySQL, or MariaDB
- Docker (recommended deployment)
- Basic server administration skills

### Cloud Hosting (Umami Cloud)
**Pricing:** Available on Umami.is website
- Managed hosting option for those who don't want to self-host
- Pricing not widely published (likely usage-based)

**Cost Comparison (Self-Hosted):**
- **Personal/Blog (10K pageviews):** $5/month (VPS)
- **Small Business (100K pageviews):** $10-15/month
- **Mid-Market (1M pageviews):** $20-50/month
- **Enterprise (10M pageviews):** $100-200/month (optimized infrastructure)

**Total Cost of Ownership:**
- **Direct costs:** $5-50/month (infrastructure)
- **Setup time:** 1-2 hours
- **Maintenance:** 1-2 hours/month (updates, monitoring)

---

## Privacy & Compliance

### GDPR Compliance
**Status:** ✅ **Fully compliant by design**

**Why Compliant:**
- No personal data collected
- No cookies used
- Self-hosted = full data control
- No third-party data sharing
- Anonymous tracking only

### CCPA/PECR
- ✅ Compliant (no personal data)

### Cookie Requirements
- **Cookies:** ZERO
- **Consent:** NOT required

### Data Residency
- **Self-Hosted:** You choose server location
- **Full Control:** Data never leaves your infrastructure

### Impact on Analytics
- **Accuracy:** ~90-95% (depends on ad-blocker setup)
- **Self-Domain Tracking:** Can reduce ad-blocker impact

---

## Implementation

### Self-Hosted Installation

**Docker (Recommended):**
```bash
docker run -d \
  -p 3000:3000 \
  -e DATABASE_URL=postgresql://user:password@db:5432/umami \
  ghcr.io/umami-software/umami:postgresql-latest
```

**Database Support:**
- PostgreSQL (v12.14+)
- MySQL (v8.0+)
- MariaDB (v10.5+)

### JavaScript Tracking Code
```html
<script async src="https://your-umami-instance.com/script.js"
        data-website-id="xxxx-xxxx-xxxx"></script>
```

**Size:** <2KB (extremely lightweight)

### Installation Methods
1. **Docker Compose:** Easiest setup (5-10 minutes)
2. **Railway/Vercel Deploy:** One-click deployment
3. **Manual Installation:** Node.js + database setup
4. **Cloud Providers:** DigitalOcean, Hetzner, etc.

### Difficulty Level
- **Self-Hosted:** 5/10 (requires Docker/server knowledge)
- **One-Click Deploy:** 3/10 (Railway, Vercel)
- **Script Installation:** 1/10 (simple copy-paste)

### Time to First Insights
- **Docker Setup:** 15-30 minutes
- **One-Click Deploy:** 5-10 minutes
- **Data Collection:** Immediate

---

## Data Ownership & Portability

### Data Ownership
- **Complete Ownership:** Your server, your database, your data
- **No Third-Party Access:** Data never leaves your infrastructure

### Data Export
- **Database Access:** Direct SQL database access
- **CSV Export:** Manual export available
- **API:** REST API for custom integrations
- **Raw Data:** Full database control

### Migration Paths
- **To Umami:** Manual import from other platforms
- **From Umami:** Direct database export, CSV
- **Vendor Lock-in:** NONE (open-source, self-hosted)

### Self-Hosting
- **License:** MIT (permissive open-source)
- **Source Code:** https://github.com/umami-software/umami
- **Customization:** Full code access for modifications

---

## Pros and Cons

### Pros ✅
1. **Free & Open-Source:** MIT license, no software costs
2. **Privacy-First:** GDPR-compliant by design
3. **Self-Hosted:** Complete data control
4. **Lightweight:** <2KB tracking script
5. **No Cookies:** Zero consent requirements
6. **Simple Setup:** Docker deployment in minutes
7. **Multi-Database:** PostgreSQL, MySQL, MariaDB support
8. **Modern Interface:** Clean, fast UI
9. **Active Development:** Regular updates, growing community

### Cons ❌
1. **Limited Features:** No advanced analytics (funnels, cohorts, heatmaps)
2. **Self-Hosting Required:** Need technical expertise
3. **Maintenance Overhead:** Updates, backups, monitoring
4. **CSV Export Only:** Limited data export options
5. **Performance at Scale:** May need optimization for high traffic
6. **No Predictive Analytics:** No AI/ML features
7. **Community Support:** No dedicated support (unless cloud)

---

## Best Fit Scenarios

### Ideal For ✅
- **Developers:** Comfortable with self-hosting
- **Privacy-Focused:** Want complete data ownership
- **Budget-Constrained:** Need free solution
- **Simple Analytics Needs:** Basic traffic stats sufficient
- **Self-Hosted Preference:** Want control over infrastructure
- **Side Projects:** Personal blogs, portfolios
- **Open-Source Advocates:** Value transparency

### Not Ideal For ❌
- **Non-Technical Users:** Self-hosting requires expertise
- **Complex Analytics:** Need funnels, cohorts, segmentation
- **Zero Maintenance:** Want managed solution
- **Enterprise Features:** Need SLAs, support
- **High-Volume Sites:** May require optimization work

---

## Strategic Positioning

**Market Position:** The free, simple self-hosted analytics for developers.

**2025 Trends:**
- Growing popularity among indie developers
- One-click deployment options expanding
- Community plugins emerging
- Alternative to paid privacy tools

**Competitive Advantages:**
- Free & open-source (MIT)
- Extremely lightweight (<2KB)
- Modern tech stack (Next.js, React)
- Simple, clean interface

**Key Differentiator:** Easiest self-hosted analytics to deploy and maintain

**Major Limitation:** Feature depth for complex analytics

---

## Comparison with Alternatives

**vs Matomo (Self-Hosted):**
- Features: Matomo wins (more advanced)
- Simplicity: Umami wins (cleaner, lighter)
- Performance: Umami wins (lighter footprint)
- License: Both open-source

**vs Plausible (Cloud):**
- Price: Umami cheaper (free vs $9+/month)
- Features: Tied (similar capabilities)
- Ease: Plausible wins (managed, no setup)
- Control: Umami wins (self-hosted)

**vs Google Analytics:**
- Privacy: Umami wins (GDPR-compliant)
- Features: GA wins (much more advanced)
- Price: Umami cheaper (infrastructure only)
- Setup: GA easier (no hosting needed)

---

## Recommendation Summary

**Use Umami if:**
- You're comfortable with self-hosting
- Budget is $0 for software
- Privacy and data ownership are critical
- You need simple analytics (traffic, referrers, events)
- You want open-source transparency
- You have technical expertise for deployment

**Avoid Umami if:**
- You need advanced features (funnels, cohorts)
- You lack technical resources for hosting
- You want zero maintenance (use cloud analytics)
- You need enterprise support/SLAs
- You require complex reporting

**Migration Considerations:**
- Moving TO Umami: Manual setup, import challenges
- Moving FROM Umami: Easy (database export)

---

**Last Updated:** October 11, 2025
**License:** MIT (Open-Source)
**Compliance:** Fully GDPR/CCPA compliant
**Best For:** Developers wanting free, privacy-first analytics with full control
