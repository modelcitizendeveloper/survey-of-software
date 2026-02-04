# S1 Rapid Library Search - Quick Recommendations

**Experiment:** 3.062-web-analytics
**Phase:** S1 - Rapid Library Search
**Date:** October 11, 2025

---

## Top Choices by Use Case

### For Privacy-First Projects (No Cookie Banners)

**Winner: Plausible Analytics** ($9+/month)
- Best balance of features, privacy, and ease of use
- 15K+ paying customers, proven solution
- Open-source with self-hosting option
- Recommended for: EU businesses, privacy-conscious brands

**Runner-up: Cloudflare Web Analytics** (Free)
- Completely free, zero tracking
- No Cloudflare account required
- Recommended for: Small sites, personal projects, maximum privacy

**Budget option: GoatCounter** (Free, donation-supported)
- Open-source, self-hostable
- Indie/community project
- Recommended for: Personal blogs, open-source projects

---

### For Full-Featured Analytics (Advanced Tracking)

**Winner: Google Analytics 4** (Free)
- Industry standard, most comprehensive free tier
- Strong marketing attribution and Google Ads integration
- Recommended for: Marketing-heavy businesses, Google ecosystem users

**Privacy-friendly alternative: Matomo** (Free self-hosted, $23+/month cloud)
- Most feature-rich privacy-focused option
- 100% data ownership
- Recommended for: Enterprises needing GA4-like features with data sovereignty

---

### For Self-Hosted / Data Sovereignty

**Winner: Umami** (Free self-hosted)
- Modern stack (Next.js, React), easy to deploy
- Lightweight and fast
- Recommended for: Developers, startups with technical capacity

**Enterprise option: Matomo** (Free self-hosted)
- Most mature self-hosted solution (since 2007)
- Advanced features: heatmaps, session recording, funnels
- Recommended for: Regulated industries, large organizations

---

### For Developer Platform Integration

**Vercel users: Vercel Analytics** (Included with Pro plan)
- Native integration, zero config
- Core Web Vitals tracking
- Use when: Already on Vercel platform

**Netlify users: Netlify Analytics** ($9/month)
- Server-side analytics, no JS required
- No privacy concerns
- Use when: Already on Netlify platform

---

### For Product Teams (App/SaaS Analytics)

**Winner: PostHog** (Free 1M events/month)
- All-in-one: analytics + session replay + feature flags + experiments
- Generous free tier
- Recommended for: Startups, product teams building apps

**Note:** Mixpanel and similar product analytics tools are borderline out-of-scope per S0 definition but worth considering for SaaS/app-heavy use cases.

---

## Quick Decision Framework

### Question 1: What's your budget?

- **$0:** Google Analytics 4, Cloudflare Web Analytics, GoatCounter, Umami (self-hosted)
- **$10-20/month:** Plausible, Fathom, Simple Analytics
- **Self-host:** Umami, Matomo (infrastructure costs only)
- **Enterprise:** Adobe Analytics, GA4 360 (custom pricing)

### Question 2: How important is privacy?

- **Critical (no cookies):** Plausible, Fathom, Simple Analytics, Cloudflare, GoatCounter
- **Important (configurable):** Matomo, Umami, PostHog
- **Standard (full tracking):** Google Analytics 4, Adobe Analytics

### Question 3: What features do you need?

- **Basic (traffic, referrers):** Plausible, Fathom, Simple Analytics, Cloudflare
- **Advanced (funnels, segments, heatmaps):** Matomo, Google Analytics 4, PostHog
- **Product analytics:** PostHog, Mixpanel

### Question 4: Where's your audience?

- **EU/GDPR-sensitive:** Plausible, Fathom, Matomo (EU hosting)
- **Enterprise/regulated:** Self-hosted Matomo, Umami
- **Global/standard:** Google Analytics 4, any cloud option

---

## Top 5 Overall Recommendations

### 1. Plausible Analytics
**Best all-around privacy-first choice**
- Simple, fast, privacy-compliant
- Proven with 15K+ customers
- $9/month entry point

### 2. Google Analytics 4
**Best for full-featured free analytics**
- Industry standard
- Comprehensive features
- Free tier sufficient for most

### 3. Matomo
**Best for self-hosted with advanced features**
- Data sovereignty
- Feature parity with GA4
- Free (self-hosted) or managed

### 4. Cloudflare Web Analytics
**Best completely free option**
- Zero cost, zero tracking
- No limitations
- Maximum privacy

### 5. Umami
**Best for developers wanting to self-host**
- Modern tech stack
- Easy deployment
- Free with generous cloud tier

---

## Red Flags & Considerations

### Avoid if...

- **Google Analytics 4** → You're targeting privacy-conscious EU markets without consent infrastructure
- **Adobe Analytics** → You're a small business (overkill, expensive, complex)
- **Self-hosted solutions** → You lack DevOps capacity to maintain infrastructure
- **Privacy-focused tools** → You need advanced segmentation, attribution, or funnel analysis
- **Platform analytics (Vercel/Netlify)** → You're not on those platforms (vendor lock-in)

### Consider combinations...

Many teams use **two tools**:
- GA4 (comprehensive data) + Plausible (privacy-friendly public dashboard)
- PostHog (product analytics) + Cloudflare (web traffic)
- Matomo (main analytics) + Hotjar (qualitative insights)

---

## Next Steps

This rapid search identified **15 providers** across categories. For deeper analysis:

1. **S2 (Comprehensive):** Feature matrices, exact pricing tiers, integration details
2. **S3 (Need-Driven):** Match specific use cases to solutions
3. **S4 (Strategic):** Decision frameworks, migration paths, future-proofing

---

**S1 Phase Complete**
- 15 providers identified
- 4 main categories covered
- Quick recommendations provided
- Ready for S2 deep-dive analysis
