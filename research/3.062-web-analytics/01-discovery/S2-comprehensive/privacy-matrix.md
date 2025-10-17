# Privacy & Compliance Comparison Matrix

**Experiment:** 3.062-web-analytics
**Phase:** S2 Comprehensive Analysis
**Last Updated:** October 11, 2025

---

## Privacy Compliance Overview

This matrix compares privacy and compliance capabilities across web analytics providers, critical for EU businesses and privacy-conscious organizations.

**Compliance Standards Covered:**
- GDPR (EU General Data Protection Regulation)
- CCPA (California Consumer Privacy Act)
- PECR (Privacy and Electronic Communications Regulations)
- HIPAA (Health Insurance Portability and Accountability Act)

**Legend:**
- ✅ = Fully compliant by design
- ⚠️ = Compliant with configuration required
- ❌ = Not compliant or significant challenges
- N/A = Not applicable

---

## GDPR Compliance Matrix

| Provider | GDPR Status | Consent Required? | Cookie-Free Option | Data Residency | IP Anonymization | DPA Available |
|----------|-------------|-------------------|-------------------|----------------|------------------|---------------|
| **Google Analytics 4** | ⚠️ Requires config | ✅ YES (EU) | ❌ No | ❌ US/Global | ✅ Default | ✅ Yes |
| **Plausible** | ✅ Compliant | ❌ NO | ✅ YES | ✅ EU only | ✅ Always | ✅ Yes |
| **Matomo Cloud** | ✅ Compliant | ⚠️ Configurable | ✅ YES | ✅ EU (Germany) | ✅ Configurable | ✅ Yes |
| **Matomo Self-Hosted** | ✅ Compliant | ⚠️ Configurable | ✅ YES | ✅ Your choice | ✅ Configurable | N/A (self-owned) |
| **Fathom** | ✅ Compliant | ❌ NO | ✅ YES | ✅ EU routing | ✅ Always | ✅ Yes |
| **Simple Analytics** | ✅ Compliant | ❌ NO | ✅ YES | ✅ EU only | ✅ Always | ✅ Yes |
| **Umami** | ✅ Compliant | ❌ NO | ✅ YES | ✅ Your choice | ✅ Always | N/A (self-hosted) |
| **PostHog** | ⚠️ Requires config | ✅ YES (EU) | ❌ No | ⚠️ US (EU option) | ✅ Configurable | ✅ Yes |
| **Cloudflare** | ✅ Compliant | ❌ NO | ✅ YES | ⚠️ Edge/Global | ✅ Always | ✅ Yes |
| **Piwik PRO** | ✅ Compliant | ⚠️ Managed | ✅ YES | ✅ EU (Sweden) | ✅ Advanced | ✅ Yes |
| **Adobe Analytics** | ⚠️ Requires config | ✅ YES (EU) | ❌ No | ❌ US/Global | ✅ Configurable | ✅ Yes |
| **Mixpanel** | ⚠️ Requires config | ✅ YES (EU) | ❌ No | ❌ US (EU option) | ✅ Configurable | ✅ Yes |

---

## Cookie Requirements

| Provider | Uses Cookies? | Cookie Duration | Cookie Type | Cookie Banner Needed? | LocalStorage Used? |
|----------|---------------|-----------------|-------------|-----------------------|-------------------|
| **Google Analytics 4** | ✅ YES | 2 years | First-party | ✅ YES (EU) | ❌ No |
| **Plausible** | ❌ NO | N/A | None | ❌ NO | ❌ No |
| **Matomo** | ⚠️ Optional | 13 months | First-party | ⚠️ If cookies enabled | ⚠️ Optional |
| **Fathom** | ❌ NO | N/A | None | ❌ NO | ❌ No |
| **Simple Analytics** | ❌ NO | N/A | None | ❌ NO | ❌ No |
| **Umami** | ❌ NO | N/A | None | ❌ NO | ❌ No |
| **PostHog** | ✅ YES | 365 days | First-party | ✅ YES (EU) | ✅ YES |
| **Cloudflare** | ❌ NO | N/A | None | ❌ NO | ❌ No |
| **Piwik PRO** | ⚠️ Managed | Configurable | First-party | ⚠️ Consent Mgr | ⚠️ Optional |
| **Adobe** | ✅ YES | Configurable | First-party | ✅ YES (EU) | ⚠️ Optional |
| **Mixpanel** | ✅ YES | 365 days | First-party | ✅ YES (EU) | ✅ YES |

---

## Data Anonymization Methods

| Provider | IP Anonymization | User Fingerprinting | Cross-Site Tracking | Personal Data Collected | Data Retention Control |
|----------|------------------|---------------------|---------------------|-------------------------|------------------------|
| **Google Analytics 4** | ✅ Default (GA4) | ⚠️ Optional (Google Signals) | ⚠️ If Google Signals on | ⚠️ With User-ID | ✅ 2-14 months |
| **Plausible** | ✅ Always (no IP stored) | ❌ None | ❌ None | ❌ None | ✅ Infinite |
| **Matomo** | ✅ Configurable (1-4 bytes) | ⚠️ Minimal | ❌ Optional disable | ⚠️ Configurable | ✅ Configurable |
| **Fathom** | ✅ Always (48h hash) | ❌ None | ❌ None | ❌ None | ✅ Infinite |
| **Simple Analytics** | ✅ Always | ❌ None | ❌ None | ❌ None | ✅ Per tier |
| **Umami** | ✅ Always | ❌ None | ❌ None | ❌ None | ✅ Infinite |
| **PostHog** | ✅ Configurable | ⚠️ Optional | ⚠️ Configurable | ⚠️ With identification | ✅ Configurable |
| **Cloudflare** | ✅ Always | ❌ None | ❌ None | ❌ None | ⚠️ 6 months fixed |
| **Piwik PRO** | ✅ Advanced options | ⚠️ Minimal | ❌ Optional | ⚠️ Consent-based | ✅ Configurable |
| **Adobe** | ✅ Configurable | ⚠️ Optional | ⚠️ Configurable | ⚠️ With User-ID | ✅ Configurable |
| **Mixpanel** | ✅ Configurable | ⚠️ Optional | ⚠️ Configurable | ✅ User profiles | ✅ Configurable |

---

## Data Residency Options

| Provider | Default Location | EU Hosting Option | On-Premise Option | Data Transfer Mechanism | Self-Hosted Option |
|----------|------------------|-------------------|-------------------|-------------------------|-------------------|
| **Google Analytics 4** | US/Global | ❌ No guarantee | ❌ No | ⚠️ US (Privacy Framework) | ❌ No |
| **Plausible** | EU (Germany) | ✅ Default | ❌ No | ✅ EU-only | ✅ Yes (Community Edition) |
| **Matomo Cloud** | EU (Germany) | ✅ Default | ✅ Yes (On-Premise) | ✅ EU or self-controlled | ✅ Yes |
| **Fathom** | Canada/EU routing | ✅ Auto EU routing | ❌ No | ✅ EU for EU traffic | ❌ No |
| **Simple Analytics** | EU | ✅ Default | ❌ No | ✅ EU-only | ❌ No |
| **Umami** | Your choice | ✅ Your choice | ✅ Yes | ✅ Your control | ✅ Yes (only option) |
| **PostHog** | US | ✅ EU option available | ✅ Yes | ⚠️ US default, EU opt-in | ✅ Yes |
| **Cloudflare** | Edge/Global | ⚠️ Edge network | ❌ No | ⚠️ Global edge | ❌ No |
| **Piwik PRO** | EU (Sweden) | ✅ Default | ✅ Yes (Enterprise) | ✅ EU or on-premise | ✅ Yes (Enterprise) |
| **Adobe** | US/Global | ⚠️ Negotiable | ❌ No | ⚠️ US-based | ❌ No |
| **Mixpanel** | US | ✅ EU option | ❌ No | ⚠️ US default | ❌ No |

---

## Consent Management

| Provider | Built-in Consent Manager | Cookie-less Mode | Impact Without Consent | Consent Mode v2 (Google) | Granular Consent Options |
|----------|-------------------------|------------------|------------------------|--------------------------|-------------------------|
| **Google Analytics 4** | ❌ (use external CMP) | ❌ No | ⚠️ Cannot track | ✅ Required March 2024 | ✅ Via Consent Mode |
| **Plausible** | N/A (no consent needed) | ✅ YES | ❌ N/A | N/A | N/A |
| **Matomo** | ✅ Built-in options | ✅ YES | ⚠️ Reduced accuracy | N/A | ✅ Yes |
| **Fathom** | N/A (no consent needed) | ✅ YES | ❌ N/A | N/A | N/A |
| **Simple Analytics** | N/A (no consent needed) | ✅ YES | ❌ N/A | N/A | N/A |
| **Umami** | N/A (no consent needed) | ✅ YES | ❌ N/A | N/A | N/A |
| **PostHog** | ⚠️ Manual implementation | ❌ No | ⚠️ Cannot track EU | N/A | ⚠️ DIY |
| **Cloudflare** | N/A (no consent needed) | ✅ YES | ❌ N/A | N/A | N/A |
| **Piwik PRO** | ✅ Integrated (Cookie Info) | ✅ YES | ⚠️ Anonymous mode | N/A | ✅ Advanced |
| **Adobe** | ⚠️ Via Adobe Experience Platform | ❌ No | ⚠️ Cannot track | ⚠️ Integrates with Google | ✅ Yes |
| **Mixpanel** | ❌ (use external) | ❌ No | ⚠️ Cannot track EU | N/A | ⚠️ DIY |

---

## CCPA Compliance

| Provider | CCPA Compliant? | Do Not Sell Support | Data Deletion API | Privacy Rights Automation | California-Specific Features |
|----------|----------------|---------------------|-------------------|--------------------------|------------------------------|
| **Google Analytics 4** | ⚠️ Requires config | ✅ Via settings | ✅ Yes | ⚠️ Manual | ⚠️ Via configuration |
| **Plausible** | ✅ Yes | N/A (no personal data) | N/A | N/A | ✅ No data collected |
| **Matomo** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Built-in tools | ✅ Configurable |
| **Fathom** | ✅ Yes | N/A (no personal data) | N/A | N/A | ✅ No data collected |
| **Simple Analytics** | ✅ Yes | N/A (no personal data) | N/A | N/A | ✅ No data collected |
| **Umami** | ✅ Yes | N/A (no personal data) | ⚠️ DIY (self-hosted) | ⚠️ DIY | ✅ No data collected |
| **PostHog** | ⚠️ Requires config | ✅ Via settings | ✅ Yes | ⚠️ Manual | ⚠️ Via configuration |
| **Cloudflare** | ✅ Yes | N/A (no personal data) | N/A | N/A | ✅ No data collected |
| **Piwik PRO** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Advanced | ✅ Built-in |
| **Adobe** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Platform features | ✅ Enterprise tools |
| **Mixpanel** | ⚠️ Requires config | ✅ Via settings | ✅ Yes | ⚠️ Manual | ⚠️ Via configuration |

---

## Additional Privacy Standards

| Provider | HIPAA Compliant? | SOC 2 Certified? | ISO 27001? | Privacy Shield (replaced by DPF) | LGPD (Brazil)? |
|----------|------------------|------------------|------------|----------------------------------|----------------|
| **Google Analytics 4** | ❌ No | ✅ Yes | ✅ Yes | ⚠️ Data Privacy Framework | ⚠️ With config |
| **Plausible** | ⚠️ Not certified (but privacy-first) | ❌ Not disclosed | ❌ Not disclosed | ✅ EU-only, N/A | ✅ Yes |
| **Matomo** | ⚠️ Via self-hosted | ⚠️ Cloud version | ⚠️ Available | ✅ EU hosting | ✅ Yes |
| **Fathom** | ⚠️ Not certified | ❌ Not disclosed | ❌ Not disclosed | ✅ Canadian adequacy | ✅ Yes |
| **Simple Analytics** | ❌ Not disclosed | ❌ Not disclosed | ❌ Not disclosed | ✅ EU-only | ✅ Yes |
| **Umami** | ⚠️ DIY (self-hosted) | N/A | N/A | N/A (self-hosted) | ⚠️ DIY |
| **PostHog** | ⚠️ Via self-hosted | ✅ Yes | ⚠️ In progress | ⚠️ US-based | ⚠️ With config |
| **Cloudflare** | ⚠️ Not for analytics | ✅ Yes | ✅ Yes | ⚠️ Global edge | ⚠️ With config |
| **Piwik PRO** | ✅ Yes (certified) | ✅ Yes | ✅ Yes | ✅ EU hosting | ✅ Yes |
| **Adobe** | ✅ Yes (with BAA) | ✅ Yes | ✅ Yes | ⚠️ Data Privacy Framework | ✅ Yes |
| **Mixpanel** | ❌ No | ✅ Yes | ⚠️ Available | ⚠️ US-based | ⚠️ With config |

---

## Impact on Data Collection Accuracy

**Privacy-First (Cookie-Free) Impact:**

| Provider | Ad Blocker Impact | Consent Decline Impact | Data Loss Estimate | Visitor Coverage |
|----------|-------------------|------------------------|-------------------|------------------|
| **Google Analytics 4** | ⚠️ 20-30% blocked | ⚠️ 20-40% decline (EU) | ⚠️ 30-50% data loss (EU) | 50-70% (EU) |
| **Plausible** | ⚠️ 5-10% blocked | ✅ N/A (no consent) | ⚠️ 5-10% loss | 90-95% |
| **Matomo** | ⚠️ 10-15% blocked | ⚠️ If consent required | ⚠️ 10-30% loss | 70-90% |
| **Fathom** | ✅ 1-2% blocked (bypass) | ✅ N/A (no consent) | ⚠️ 1-5% loss | 95-99% |
| **Simple Analytics** | ⚠️ 5-10% blocked | ✅ N/A (no consent) | ⚠️ 5-10% loss | 90-95% |
| **Umami** | ⚠️ 5-10% blocked | ✅ N/A (no consent) | ⚠️ 5-10% loss | 90-95% |
| **PostHog** | ⚠️ 15-20% blocked | ⚠️ 20-40% decline (EU) | ⚠️ 30-50% loss (EU) | 50-80% |
| **Cloudflare** | ⚠️ 5-10% blocked | ✅ N/A (no consent) | ⚠️ 5-10% loss | 90-95% |
| **Piwik PRO** | ⚠️ 10-15% blocked | ⚠️ Managed consent | ⚠️ 10-20% loss | 80-90% |
| **Adobe** | ⚠️ 15-25% blocked | ⚠️ 20-40% decline (EU) | ⚠️ 30-50% loss (EU) | 50-70% (EU) |
| **Mixpanel** | ⚠️ 15-20% blocked | ⚠️ 20-40% decline (EU) | ⚠️ 30-50% loss (EU) | 50-80% |

**Key Insights:**
- **Cookie-free tools** (Plausible, Fathom, Simple, Umami, Cloudflare): 90-99% visitor coverage
- **Cookie-based with consent** (GA4, PostHog, Adobe, Mixpanel): 50-80% coverage in EU
- **Fathom's ad-blocker bypass:** Best coverage (95-99%)
- **Google Analytics:** Worst coverage in EU due to GDPR concerns + ad blockers

---

## Legal Risk Assessment

| Provider | EU Legal Risk | US Legal Risk | Regulatory Scrutiny | DPA Rulings Against | Future-Proofing |
|----------|---------------|---------------|---------------------|---------------------|-----------------|
| **Google Analytics 4** | 🔴 HIGH | ✅ LOW | 🔴 HIGH | ✅ Multiple EU DPAs | 🔴 LOW |
| **Plausible** | ✅ LOW | ✅ LOW | ✅ LOW | ❌ None | ✅ HIGH |
| **Matomo** | ✅ LOW | ✅ LOW | ✅ LOW | ❌ None | ✅ HIGH |
| **Fathom** | ✅ LOW | ✅ LOW | ✅ LOW | ❌ None | ✅ HIGH |
| **Simple Analytics** | ✅ LOW | ✅ LOW | ✅ LOW | ❌ None | ✅ HIGH |
| **Umami** | ✅ LOW | ✅ LOW | ✅ LOW | ❌ None | ✅ HIGH |
| **PostHog** | ⚠️ MEDIUM | ✅ LOW | ⚠️ MEDIUM | ❌ None (yet) | ⚠️ MEDIUM |
| **Cloudflare** | ✅ LOW | ✅ LOW | ✅ LOW | ❌ None | ✅ HIGH |
| **Piwik PRO** | ✅ LOW | ✅ LOW | ✅ LOW | ❌ None | ✅ HIGH |
| **Adobe** | ⚠️ MEDIUM | ✅ LOW | ⚠️ MEDIUM | ⚠️ Some scrutiny | ⚠️ MEDIUM |
| **Mixpanel** | ⚠️ MEDIUM | ✅ LOW | ⚠️ MEDIUM | ❌ None (yet) | ⚠️ MEDIUM |

**Risk Factors:**
- **Google Analytics:** Multiple EU Data Protection Authority rulings declaring it unlawful
- **US-based processing:** Ongoing legal challenges to EU-US Data Privacy Framework
- **Cookie-free tools:** Minimal legal risk (no personal data = no GDPR issues)

---

## Privacy Compliance Checklist

### ✅ Automatically GDPR-Compliant (No Configuration Needed)
- **Plausible:** Cookie-free, no personal data, EU-hosted
- **Fathom:** Cookie-free, 48h anonymization, EU routing
- **Simple Analytics:** Cookie-free, no personal data, EU-hosted
- **Umami:** Cookie-free, self-hosted, no personal data
- **Cloudflare:** Cookie-free, no personal data, edge network

**These tools require NO cookie banner and NO consent popup.**

---

### ⚠️ GDPR-Compliant with Configuration
- **Matomo:** Enable IP anonymization, cookie-less mode, EU hosting
- **Piwik PRO:** Use built-in consent manager, configure retention
- **PostHog:** Configure IP anonymization, EU hosting option, consent implementation

**These tools CAN be compliant but require setup.**

---

### 🔴 GDPR Challenges (Significant Configuration Required)
- **Google Analytics 4:**
  - Enable Consent Mode v2
  - Disable Google Signals
  - Set 2-month retention
  - Use cookie consent banner
  - Still faces legal challenges in EU

- **Adobe Analytics:**
  - Complex consent configuration
  - US data processing concerns
  - Requires Data Processing Agreement
  - Privacy team involvement needed

- **Mixpanel:**
  - Cookie consent required
  - US data processing
  - Manual privacy configuration
  - Limited GDPR features

**These tools require extensive work and may still face legal risks.**

---

## Recommendations by Privacy Requirement

### Maximum Privacy (Zero Risk)
**Top Choices:**
1. **Plausible** - Best balance of features + privacy
2. **Fathom** - Ad-blocker bypass + privacy
3. **Umami** - Free self-hosted option
4. **Cloudflare** - Free, basic features

**Why:** No cookies, no consent needed, no personal data, EU hosting (or self-hosted)

---

### GDPR-Compliant with Advanced Features
**Top Choices:**
1. **Matomo (Self-Hosted or Cloud)** - GA-equivalent with privacy
2. **Piwik PRO** - Enterprise GDPR compliance (regulated industries)

**Why:** Full analytics features + GDPR compliance + EU hosting + data ownership

---

### Accept Configuration Complexity
**If you must use:**
1. **Google Analytics 4** - Free but requires consent management + configuration
2. **PostHog** - Product analytics focus, configure for privacy

**Why:** Free or feature-rich, but significant compliance work needed

---

## Privacy-First Migration Path

**From Google Analytics to Privacy-First:**

1. **Immediate (Low Budget):**
   - Cloudflare Web Analytics (free, basic)
   - Umami (self-hosted, free)

2. **Best Privacy + Features (<$100/month):**
   - Plausible ($9-69/month depending on traffic)
   - Fathom ($15-75/month depending on traffic)

3. **Need GA-Like Features (GDPR-compliant):**
   - Matomo Cloud ($29-449/month)
   - Matomo Self-Hosted (infrastructure costs only)

4. **Enterprise + Regulated Industry:**
   - Piwik PRO (€35/month - $300K+/year)
   - Matomo On-Premise (custom infrastructure)

---

**Last Updated:** October 11, 2025
**Legal Disclaimer:** This is technical analysis, not legal advice. Consult with privacy lawyers for compliance decisions.
