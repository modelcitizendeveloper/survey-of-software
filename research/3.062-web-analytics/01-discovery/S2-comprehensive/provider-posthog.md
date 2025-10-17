# PostHog

**Category:** Product Analytics Platform (with Web Analytics)
**Hosting:** Cloud or Self-Hosted
**Pricing Model:** Usage-based (events)
**Primary Market:** Product engineers, developers, SaaS
**Website:** https://posthog.com/

---

## Overview

PostHog is an all-in-one product analytics platform designed for product engineers. It combines web analytics, product analytics, session replay, feature flags, A/B testing, and surveys in a single platform. Open-source with generous free tier.

**Market Position:** "The only product analytics platform built to natively work with session replay, feature flags, experiments, and surveys."

**Target Audience:** Product teams and engineers building SaaS applications.

---

## Core Features

### Product Analytics Suite
- **Web Analytics:** Pageviews, sessions, traffic sources
- **Product Analytics:** Event tracking, autocapture (tracks every click/pageview automatically)
- **Funnels:** Multi-step conversion analysis
- **Retention Analysis:** Cohort retention tracking
- **User Paths:** Journey visualization
- **Dashboards:** Custom insights and reports

### Integrated Tools
- **Session Replay:** Watch user sessions
- **Feature Flags:** Feature toggles and gradual rollouts
- **A/B Testing:** Built-in experimentation platform
- **Surveys:** In-app user surveys
- **Error Tracking:** JavaScript error monitoring
- **Data Warehouse/CDP:** Customer data platform features

### Advanced Capabilities
- **Autocapture:** Automatic event tracking (no manual instrumentation)
- **Group Analytics:** Company/account-level tracking
- **SQL Query:** Direct SQL access to data
- **API Access:** Comprehensive API
- **Self-Hosting:** Full-featured self-hosted option

---

## Pricing Structure

### Pricing Model (2025)
**Usage-based pricing across multiple products:**

**Free Tier (Generous):**
- **1 million events/month** free
- 10K session replays
- Unlimited seats
- All features included
- No credit card for free tier

**Paid Tiers:**
- **Product Analytics:** From $0.00031/event (after free tier)
- **Session Replay:** From $0.005/replay
- **Feature Flags:** From $0.0001/request
- **Experiments:** Included with Product Analytics
- **Surveys:** From $0.20/response

**Cost Examples:**
- **1M events/month:** FREE
- **3M events/month:** ~$620/month (estimate)
- **10M events/month:** ~$1,500-2,000/month
- **20M events/month:** ~$2,289/month (reported)

**Notes:**
- Anonymous events: 4x cheaper than identified events
- Very high free tier (1M events covers most small-medium products)
- No storage fees, no monthly minimums

**Startup Program:**
- Early-stage companies (<5 years, <$8M funding)
- First year FREE on Startup Plan

### Self-Hosted
**Cost:** FREE (open-source, MIT license)
- Infrastructure costs only ($50-500/month depending on scale)
- Full feature parity with cloud
- Community support

---

## Privacy & Compliance

### GDPR Compliance
**Status:** ⚠️ **Can be compliant with configuration**

- **Cookie-based tracking:** Default uses cookies
- **Consent required:** YES (EU)
- **Privacy features:** IP anonymization, data retention controls
- **Self-hosted:** Full GDPR control when self-hosted

### Data Residency
- **Cloud:** US-based (also EU option available)
- **Self-Hosted:** Your choice

### Cookie Requirements
- **Cookies:** YES (default tracking)
- **Consent:** Required in EU

---

## Implementation

### JavaScript SDK
```html
<script>
  !function(t,e){...}(window,document,'posthog');
  posthog.init('YOUR_PROJECT_API_KEY',{api_host:'https://app.posthog.com'})
</script>
```

**Features:**
- Autocapture enabled by default
- Manual event tracking
- User identification
- Feature flag evaluation

### Installation
- **Direct Script:** Copy-paste snippet
- **NPM Package:** For React, Vue, Next.js, etc.
- **Mobile SDKs:** iOS, Android, React Native
- **Backend SDKs:** Python, Node, Ruby, PHP, Go
- **Self-Hosted:** Docker Compose deployment

**Difficulty:** 3/10 (simple for basic, complex for advanced)
**Time to Setup:** 10-30 minutes

---

## Data Ownership & Portability

- **Cloud:** Data accessible via API
- **Self-Hosted:** Complete ownership
- **Export:** SQL access, CSV export, data warehouse integrations
- **Vendor Lock-in:** LOW (open-source, self-hostable)

---

## Pros and Cons

### Pros ✅
1. **All-in-One:** Analytics + Replay + Flags + Experiments + Surveys
2. **Generous Free Tier:** 1M events/month free
3. **Autocapture:** No manual event instrumentation needed
4. **Open-Source:** Transparent, self-hostable (MIT license)
5. **Product-Focused:** Built for SaaS product teams
6. **Session Replay:** Included (see user sessions)
7. **Developer-Friendly:** SQL access, comprehensive APIs
8. **No Seat Limits:** Unlimited users on all plans

### Cons ❌
1. **Not Privacy-First:** Uses cookies, requires consent (EU)
2. **Product Analytics Focus:** More than needed for simple web analytics
3. **Complexity:** Steeper learning curve than simple analytics
4. **Pricing Complexity:** Usage-based can be unpredictable
5. **Event-Based Pricing:** Costs scale with events (not pageviews)
6. **Not GDPR-by-Default:** Requires configuration for compliance

---

## Best Fit Scenarios

### Ideal For ✅
- **SaaS Products:** Need product analytics + web analytics
- **Product Teams:** Want funnels, retention, user paths
- **Feature Flags Needed:** Combined analytics + flags
- **Session Replay:** Want to watch user sessions
- **Developers:** Appreciate autocapture, SQL access, APIs
- **Growing Startups:** Generous free tier, startup program

### Not Ideal For ❌
- **Simple Websites:** Overkill for blog/marketing site
- **Privacy-First Focus:** Not designed for cookie-less tracking
- **EU Privacy-Critical:** Better alternatives for GDPR-first
- **Marketing Sites:** Use web analytics instead (Plausible, etc.)

---

## Recommendation Summary

**Use PostHog if:**
- You're building a SaaS product
- You need product analytics + web analytics combined
- You want session replay, feature flags, experiments
- You have generous free tier needs (<1M events)
- You're a developer-focused team

**Avoid PostHog if:**
- You need simple web analytics only
- Privacy-first is critical (EU-focused)
- You want cookie-less tracking
- You're tracking a marketing website (not product)

---

**Last Updated:** October 11, 2025
**Category:** Product Analytics (not pure web analytics)
**Best For:** SaaS product teams needing comprehensive product insights
