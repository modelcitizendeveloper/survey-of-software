# S3 Need-Driven Discovery: Recommendations
## Pattern-Based Decision Matrix for Application Monitoring

**Experiment**: 3.060 Application Monitoring / Error Tracking
**Phase**: S3 (Need-Driven Discovery)
**Date**: 2025-10-08

---

## Executive Summary

This document provides a pattern-based decision framework for selecting application monitoring and error tracking services. Based on analysis of 7 core use cases, we've identified clear winner patterns across different technical contexts, budgets, and scales.

**Key Finding:** There is no single "best" monitoring tool - the optimal choice depends on your specific pattern. Match your use case to our recommendations below for the best cost-to-value ratio.

---

## Quick Decision Guide: "If You Are X, Choose Y"

### By Developer Profile

| Profile | Recommended Provider | Monthly Cost | Rationale |
|---------|---------------------|--------------|-----------|
| Solo developer / Bootstrap startup | **Sentry Free Tier** | $0 | Best free tier (5K errors), scales when you do |
| Small team (2-10 devs), Python/Flask SaaS | **Sentry Team** | $26 | Best Flask integration, affordable, APM available |
| Frontend/SPA team | **TrackJS** or **Sentry** | $49-80 | TrackJS for pure frontend, Sentry for full-stack |
| Mobile app developers | **Bugsnag** or **Firebase** | $0-18 | Bugsnag for features, Firebase for free |
| Microservices team (5-20 services) | **New Relic** | $100-500 | Consumption-based cheaper than host-based |
| Large microservices (20+ services) | **Datadog** | $500-5,000 | Best distributed tracing, service maps |
| Enterprise with SOC2/HIPAA | **Datadog** or **New Relic** | $1,000-10,000 | FedRAMP, BAA, compliance features |
| High-volume app (10M+ errors/month) | **New Relic** | $100-1,000 | Consumption-based 5-10x cheaper |

### By Technology Stack

| Stack | Recommended Provider | Why |
|-------|---------------------|-----|
| Python/Flask | **Sentry** | Best Flask integration, automatic SQL/Redis breadcrumbs |
| Node.js/Express | **Sentry** or **Rollbar** | Excellent SDK quality, async support |
| Ruby/Rails | **Honeybadger** or **Sentry** | Honeybadger built for Rails, Sentry more features |
| React/Vue/Next.js | **TrackJS** or **Sentry** | TrackJS smallest bundle (8KB), Sentry for full-stack |
| iOS/Android Native | **Bugsnag** | Mobile-first, best symbolication, stability scores |
| React Native/Flutter | **Bugsnag** or **Sentry** | Both have excellent cross-platform SDKs |
| Microservices (polyglot) | **Datadog** or **New Relic** | OpenTelemetry support, distributed tracing |
| Serverless (Lambda, Cloud Functions) | **Sentry** or **AWS X-Ray** | Sentry for errors, X-Ray for tracing (AWS only) |

### By Budget

| Budget | Recommended Provider | What You Get |
|--------|---------------------|--------------|
| $0/month | **Sentry, Bugsnag, or Firebase** | 5K-7.5K errors/month or unlimited (Firebase) |
| $0-50/month | **Bugsnag Lite ($18)** or **Sentry Team ($26)** | 50K errors/month, unlimited users |
| $50-200/month | **Sentry Business ($80)** or **Honeybadger ($89)** | 500K-600K errors, APM included |
| $200-1,000/month | **New Relic** (3 users + data) | Full observability platform |
| $1,000-10,000/month | **Datadog** or **New Relic** | Enterprise features, compliance |
| $10,000+/month | **Datadog** or **Splunk** | Large-scale, compliance, SIEM |

### By Error Volume

| Error Volume/Month | Best Value Provider | Approximate Cost |
|-------------------|-------------------|------------------|
| <5K errors | **Sentry Free** or **Bugsnag Free** | $0 |
| 5K-50K errors | **Bugsnag Lite** ($18) | $18/month |
| 50K-500K errors | **Sentry Business** ($80) | $80/month |
| 500K-10M errors | **New Relic** (data-based) | $100-500/month |
| 10M-100M errors | **New Relic** (highly favorable) | $500-2,000/month |
| 100M+ errors | **New Relic** (10x cheaper) | $2,000-10,000/month |

### By Compliance Need

| Compliance Requirement | Recommended Provider | Cost Range |
|----------------------|---------------------|------------|
| None (consumer apps) | **Sentry** or **Bugsnag** | $0-200/month |
| SOC2 Type II | **Datadog**, **New Relic**, or **Sentry Enterprise** | $500-5,000/month |
| HIPAA (BAA required) | **Datadog** or **New Relic** | $1,000-10,000/month |
| FedRAMP Moderate | **Datadog** or **New Relic** | $1,500-10,000/month |
| FedRAMP High | **Datadog** or **Splunk** | $3,000-50,000/month |
| HIPAA + full control | **Sentry Self-Hosted** | $156K-336K/year (infra + labor) |

---

## Total Cost of Ownership (TCO) Analysis

### Scenario 1: Solo Developer Side Project

**Profile:**
- 1 developer
- 1,000 users
- Python/Flask SaaS
- 3,000 errors/month
- $0 budget

**Recommendation: Sentry Free Tier**

**12-Month TCO:**
- Subscription: $0
- Integration time: 2 hours × $100/hr = $200 (one-time)
- Maintenance: 0 hours/month
- **Total Year 1: $200**

**Alternatives:**
- Bugsnag Free: $0 (7,500 error limit, more headroom)
- Firebase Crashlytics: $0 (unlimited, but mobile-focused)

---

### Scenario 2: Growing SaaS Startup

**Profile:**
- 5 developers
- 10,000 users
- Python/Flask + React frontend
- 75,000 errors/month
- $100-200/month budget

**Recommendation: Sentry Team Plan ($26/mo)**

**12-Month TCO:**
- Subscription: $312/year
- Integration time: 4 hours × $100/hr = $400 (one-time, backend + frontend)
- Maintenance: 1 hour/month × 12 × $100 = $1,200
- **Total Year 1: $1,912**

**Alternatives:**
- Rollbar Essentials: $290/year (slightly cheaper)
- Bugsnag Lite: $216/year (cheapest, but fewer features)

**Why Sentry wins:** Best Flask/React integration, scales to APM when needed, team is familiar with it.

---

### Scenario 3: Microservices Startup (10 services)

**Profile:**
- 15 developers
- 5-10 services (Python, Node.js, Go)
- Kubernetes deployment
- 100,000 errors/month, 500M traces/month
- $500-2,000/month budget

**Recommendation: New Relic (3 users + 500GB data)**

**12-Month TCO:**
- Subscription: $5,400/year (3 users + 500GB overages)
- Integration time: 16 hours × $100/hr = $1,600 (all services)
- Maintenance: 4 hours/month × 12 × $100 = $4,800
- **Total Year 1: $11,800**

**Alternatives:**
- Datadog APM (30 hosts): $16,560/year (better tracing, more expensive)
- Sentry Enterprise: $2,400-6,000/year (cheaper, but limited APM)

**Why New Relic wins:** Consumption-based pricing cheaper than Datadog's host-based at this scale. All-inclusive features. Good distributed tracing.

---

### Scenario 4: Enterprise SaaS with SOC2

**Profile:**
- 50 developers
- 20+ services
- Need SOC2 Type II compliance
- 1M errors/month
- $2,000-5,000/month budget

**Recommendation: Datadog Enterprise**

**12-Month TCO:**
- Subscription: $55,200/year (100 hosts APM + Infrastructure)
- Integration time: 40 hours × $100/hr = $4,000 (full deployment + compliance)
- Compliance overhead: 20 hours × $100/hr = $2,000 (audit documentation)
- Maintenance: 8 hours/month × 12 × $100 = $9,600
- **Total Year 1: $70,800**

**Alternatives:**
- New Relic Enterprise: $48,000/year (cheaper, but less mature compliance)
- Sentry Enterprise: $24,000/year (SOC2, but no FedRAMP if needed later)

**Why Datadog wins:** Best-in-class compliance (FedRAMP, SOC2, HIPAA, ISO 27001). Future-proof for enterprise growth. Unified observability platform.

---

### Scenario 5: High-Volume Consumer App

**Profile:**
- 30 developers
- 10M monthly active users
- E-commerce platform
- 100M errors/month (high traffic!)
- $1,000-5,000/month budget

**Recommendation: New Relic (5 users + 1TB data)**

**12-Month TCO:**
- Subscription: $21,600/year (5 users + 1TB overages)
- Integration time: 20 hours × $100/hr = $2,000
- Maintenance: 6 hours/month × 12 × $100 = $7,200
- **Total Year 1: $30,800**

**Alternatives:**
- Datadog (200 hosts): $110,400/year (5x more expensive!)
- Sentry Enterprise: $100,000-200,000/year (event-based pricing kills at this scale)
- Bugsnag Enterprise: $60,000-120,000/year (still 3x more than New Relic)

**Why New Relic wins by a landslide:** Consumption-based pricing is 5-10x cheaper than event-based at high volume. Can ingest 100% of errors affordably (no aggressive sampling needed).

---

## Cost Comparison Matrix

### 12-Month TCO by Use Case and Provider

| Use Case | Sentry | Bugsnag | Rollbar | Honeybadger | Datadog | New Relic |
|----------|--------|---------|---------|-------------|---------|-----------|
| Solo Dev (3K errors/mo) | $0 | $0 | $0 | $0 | $552 | $0 |
| Flask SaaS (75K errors/mo) | $312 | $216 | $290 | $468 | $1,104 | $1,200 |
| Frontend SPA (30K errors/mo) | $312 | $216 | $290 | $468 | $1,800 | $1,200 |
| Mobile App (150K sessions/mo) | $312 | $216 | $290 | $468 | $2,700 | $1,200 |
| Microservices (10 svcs) | $2,400 | $2,400 | $3,000 | $2,388 | $5,520 | $1,200 |
| Enterprise SOC2 (30 svcs) | $6,000-24K | N/A | N/A | N/A | $18K-36K | $12K-30K |
| High Volume (100M errors/mo) | $100K-200K | $60K-120K | $108K-180K | N/A | $110K | $21.6K |

**Color coding:**
- **Bold** = Best value for use case
- _Italic_ = Acceptable alternative
- N/A = Not suitable for use case

---

## Feature Coverage by Provider

### Core Error Tracking Features

| Feature | Sentry | Bugsnag | Rollbar | Honeybadger | TrackJS | Datadog | New Relic |
|---------|--------|---------|---------|-------------|---------|---------|-----------|
| Error grouping | ✓✓✓ | ✓✓✓ | ✓✓✓ | ✓✓ | ✓✓✓ | ✓✓ | ✓✓ |
| Stack traces | ✓✓✓ | ✓✓✓ | ✓✓✓ | ✓✓✓ | ✓✓✓ | ✓✓✓ | ✓✓✓ |
| Breadcrumbs | ✓✓✓ | ✓✓ | ✓✓✓ | ✓✓ | ✓✓✓ | ✓✓ | ✓✓ |
| Source maps | ✓✓✓ | ✓✓ | ✓✓ | ✓✓ | ✓✓✓ | ✓✓ | ✓✓ |
| Release tracking | ✓✓✓ | ✓✓✓ | ✓✓ | ✓ | ✓ | ✓✓✓ | ✓✓✓ |
| User context | ✓✓✓ | ✓✓✓ | ✓✓✓ | ✓✓ | ✓✓✓ | ✓✓✓ | ✓✓✓ |
| Custom tags | ✓✓✓ | ✓✓ | ✓✓✓ | ✓✓ | ✓✓ | ✓✓✓ | ✓✓✓ |

### Advanced Features

| Feature | Sentry | Bugsnag | Rollbar | Honeybadger | TrackJS | Datadog | New Relic |
|---------|--------|---------|---------|-------------|---------|---------|-----------|
| Session replay | ✓✓✓ | ✗ | ✗ | ✗ | ✗ | ✓✓✓ | ✓✓ |
| APM / Performance | ✓✓✓ | ✗ | ✗ | ✓✓ | ✗ | ✓✓✓ | ✓✓✓ |
| Distributed tracing | ✓✓ | ✓ | ✗ | ✓ | ✗ | ✓✓✓ | ✓✓✓ |
| Stability scores | ✓ | ✓✓✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Uptime monitoring | ✗ | ✗ | ✗ | ✓✓✓ | ✗ | ✓✓✓ | ✓✓✓ |
| Cron monitoring | ✗ | ✗ | ✗ | ✓✓✓ | ✗ | ✓✓ | ✓✓ |
| Log aggregation | ✗ | ✗ | ✗ | ✗ | ✗ | ✓✓✓ | ✓✓✓ |
| Infrastructure monitoring | ✗ | ✗ | ✗ | ✗ | ✗ | ✓✓✓ | ✓✓✓ |

**Legend:**
- ✓✓✓ = Excellent (best-in-class)
- ✓✓ = Good (fully functional)
- ✓ = Basic (limited)
- ✗ = Not available

---

## Integration Complexity

### Time to First Error

| Provider | Setup Time | Complexity | Notes |
|----------|------------|------------|-------|
| Sentry | 15 min | Low | `pip install`, 3 lines of code |
| Bugsnag | 20 min | Low | SDK install, API key |
| Rollbar | 20 min | Low | SDK install, configuration |
| Honeybadger | 25 min | Low | SDK install, uptime config |
| TrackJS | 10 min | Very Low | CDN or NPM, single script tag |
| Firebase | 30 min | Medium | Firebase setup overhead |
| Datadog | 2 hours | High | Agent deployment, APM config |
| New Relic | 1 hour | Medium | Agent install, instrumentation |

### SDK Bundle Sizes (Frontend)

Critical for frontend performance:

| Provider | Bundle Size (gzipped) | Impact on Core Web Vitals |
|----------|----------------------|---------------------------|
| TrackJS | 8KB | ✓✓✓ Negligible |
| Bugsnag | 15KB | ✓✓ Low |
| Rollbar | 18KB | ✓✓ Low |
| Sentry | 22KB | ✓ Medium |
| Honeybadger | 25KB | ✓ Medium |
| Datadog | 30KB+ | ✗ Significant |

**Recommendation:** For performance-critical frontend apps, use TrackJS (8KB) or Bugsnag (15KB).

---

## Migration Strategies

### From Nothing to Sentry (Bootstrap Path)

**Phase 1: Validation (Months 0-6)**
- Use: Sentry Free Tier ($0)
- Coverage: Backend errors only
- Volume: <5K errors/month
- Cost: $0

**Phase 2: Early Traction (Months 6-12)**
- Use: Sentry Team Plan ($26/mo)
- Coverage: Backend + frontend errors
- Volume: 50K errors/month
- Cost: $312/year

**Phase 3: Growth (Year 2)**
- Use: Sentry Business Plan ($80/mo)
- Coverage: Errors + APM (performance monitoring)
- Volume: 500K errors/month
- Cost: $960/year

**Phase 4: Scale (Year 3+)**
- Evaluate: New Relic or Datadog
- Reason: If exceeding 1M errors/month, consumption-based or host-based pricing becomes cheaper
- Decision point: $21,600/year (New Relic) vs $3,000+/year (Sentry Enterprise negotiated)

### From Event-Based to Consumption-Based (High Volume)

**When to switch:** Paying >$2,000/month on Sentry/Bugsnag/Rollbar

**Migration to New Relic:**
1. **Parallel run** (1 month): Keep existing provider, add New Relic
2. **Compare data** (2 weeks): Ensure feature parity
3. **Gradual cutover** (2 weeks): Move services one-by-one
4. **Cancel old provider** (Month 2): Complete migration

**Expected savings:** 50-80% cost reduction at 50M+ errors/month

### From No Compliance to SOC2 Ready

**Timeline:** 3-6 months before audit

**Steps:**
1. **Month -6:** Choose compliant provider (Datadog, New Relic, or Sentry Enterprise)
2. **Month -5:** Request vendor SOC2 report
3. **Month -4:** Sign BAA if needed (HIPAA)
4. **Month -3:** Deploy monitoring, configure SSO/RBAC
5. **Month -2:** Set up audit logging, data retention policies
6. **Month -1:** Document controls, create runbooks
7. **Month 0:** Audit (provide monitoring evidence)

---

## Common Pitfalls and How to Avoid Them

### Pitfall 1: Exceeding Free Tier Without Noticing

**Problem:** Your app scales from 4K to 15K errors/month, suddenly $26/month charge.

**Solution:**
- Set up billing alerts in provider dashboard
- Monitor error volume weekly
- Optimize error volume (fix bugs, filter noise) before upgrading

### Pitfall 2: Event-Based Pricing at Scale

**Problem:** Start with Sentry at $26/mo, scale to 10M errors/month, now paying $2,000/month.

**Solution:**
- Plan for scale from day one
- Switch to consumption-based (New Relic) or host-based (Datadog) at 1M+ errors/month
- Negotiate volume discounts at $1,000+/month spend

### Pitfall 3: No Sampling Strategy

**Problem:** Sending 100% of errors on event-based pricing = expensive.

**Solution:**
- Sample intelligently (not randomly)
- Priority: 100% critical errors, 50% warnings, 10% info
- Filter noise: bots, third-party scripts, 404s

### Pitfall 4: Ignoring Compliance Early

**Problem:** Build on non-compliant provider, pivot to enterprise customers, must migrate everything.

**Solution:**
- If B2B SaaS, start with SOC2-ready provider (Sentry Enterprise, Datadog, New Relic)
- Even on free tier, Sentry is SOC2 compliant (future-proof)
- Avoid non-compliant tools (Honeybadger, TrackJS) if SOC2 is in roadmap

### Pitfall 5: Over-Engineering for Solo Dev

**Problem:** Solo developer deploys self-hosted Sentry, spends 40 hours on DevOps instead of building product.

**Solution:**
- Use SaaS free tiers (Sentry, Bugsnag)
- Optimize for time-to-value, not cost at this stage
- Self-host only if compliance absolutely requires it

---

## Decision Tree

```
START: What's your primary use case?

├─ Solo developer / Side project?
│  ├─ Budget: $0
│  │  └─ → Sentry Free Tier (5K errors)
│  │     Alternative: Bugsnag Free (7.5K errors)
│  │
│  └─ Budget: $0-50/month
│     └─ → Bugsnag Lite ($18/mo, 50K errors)
│
├─ Backend SaaS (Flask, Rails, Express)?
│  ├─ Python/Flask
│  │  └─ → Sentry (best integration)
│  │
│  ├─ Ruby/Rails
│  │  └─ → Honeybadger (built for Rails) or Sentry
│  │
│  └─ Node.js/Express
│     └─ → Sentry or Rollbar
│
├─ Frontend SPA (React, Vue, Next.js)?
│  ├─ Pure frontend (no backend errors)
│  │  └─ → TrackJS (8KB bundle, best telemetry)
│  │
│  └─ Full-stack (frontend + backend)
│     └─ → Sentry (unified platform)
│
├─ Mobile app (iOS, Android)?
│  ├─ Budget: $0
│  │  └─ → Firebase Crashlytics (free forever)
│  │
│  └─ Budget: $18+/month
│     └─ → Bugsnag (mobile-first, stability scores)
│
├─ Microservices (3-20 services)?
│  ├─ Small (3-10 services)
│  │  └─ → New Relic (consumption-based, cheaper)
│  │
│  └─ Large (10+ services)
│     └─ → Datadog (best distributed tracing, service maps)
│
├─ High volume (10M+ errors/month)?
│  └─ → New Relic (consumption-based 5-10x cheaper)
│
└─ Enterprise with compliance (SOC2, HIPAA)?
   ├─ SOC2 Type II only
   │  └─ → Sentry Enterprise (cheapest) or New Relic
   │
   ├─ HIPAA (BAA required)
   │  └─ → Datadog or New Relic (both provide BAA)
   │
   └─ FedRAMP
      ├─ FedRAMP Moderate
      │  └─ → Datadog or New Relic
      │
      └─ FedRAMP High
         └─ → Datadog or Splunk (only options)
```

---

## Provider Strengths Summary

### Sentry
**Best for:** Flask/Django SaaS, full-stack teams, developers who value community
**Strengths:** Best documentation, largest community, excellent SDKs, generous free tier
**Weaknesses:** Event-based pricing gets expensive at scale (>1M errors/month)
**Sweet spot:** 0-1M errors/month, small-to-medium teams

### Bugsnag
**Best for:** Mobile apps, budget-conscious startups
**Strengths:** Mobile-first, stability scores, cheapest paid tier ($18/mo)
**Weaknesses:** Smaller community, fewer integrations than Sentry
**Sweet spot:** Mobile apps, 0-500K errors/month

### Rollbar
**Best for:** Teams needing spike protection, RQL power users
**Strengths:** Spike protection (no overage), flexible pricing, telemetry
**Weaknesses:** Less feature-rich than Sentry
**Sweet spot:** 0-500K errors/month, unpredictable traffic

### Honeybadger
**Best for:** Rails apps, teams needing uptime + errors + cron in one tool
**Strengths:** All-in-one (errors + uptime + cron + APM), unlimited users, indie-friendly
**Weaknesses:** No SOC2 certification, smaller ecosystem
**Sweet spot:** Rails SaaS, 0-500K errors/month

### TrackJS
**Best for:** JavaScript-heavy frontends (SPAs, PWAs)
**Strengths:** Smallest bundle (8KB), best telemetry timeline, purpose-built for frontend
**Weaknesses:** JavaScript-only, pageview-based pricing (not error-based)
**Sweet spot:** Pure frontend apps, 100K-2M pageviews/month

### Datadog
**Best for:** Large microservices, enterprise compliance, full observability needs
**Strengths:** Best distributed tracing, service maps, compliance (FedRAMP High), unified platform
**Weaknesses:** Expensive ($46/host/month minimum), complex pricing
**Sweet spot:** 20+ services, enterprise scale, compliance requirements

### New Relic
**Best for:** High-volume apps, microservices, teams wanting all-inclusive pricing
**Strengths:** Consumption-based pricing (cheap at scale), all-inclusive features, good distributed tracing
**Weaknesses:** Less polished UI than Datadog, consumption can be unpredictable
**Sweet spot:** 1M+ errors/month, 5-50 services, high data volume

---

## Final Recommendations by Priority

### 1. Cost Optimization
- **Low volume (<1M errors/month):** Sentry or Bugsnag (event-based is fine)
- **High volume (1M+ errors/month):** New Relic (consumption-based 5-10x cheaper)
- **Massive scale (100M+ errors/month):** New Relic or Datadog (avoid event-based)

### 2. Feature Requirements
- **Best error tracking:** Sentry
- **Best mobile:** Bugsnag
- **Best frontend:** TrackJS
- **Best microservices:** Datadog (tracing), New Relic (cost)
- **Best all-in-one:** Honeybadger (errors + uptime + cron)

### 3. Compliance
- **SOC2 Type II:** Sentry Enterprise, Datadog, or New Relic
- **HIPAA:** Datadog or New Relic (both provide BAA)
- **FedRAMP:** Datadog (High), New Relic (Moderate), Splunk (High)

### 4. Team Size
- **Solo developer:** Sentry Free Tier
- **2-10 developers:** Sentry Team ($26/mo) or Bugsnag Lite ($18/mo)
- **10-50 developers:** New Relic or Datadog
- **50+ developers:** Datadog (enterprise features, compliance)

---

## Conclusion

**The One-Line Answer:**

Start with **Sentry free tier** (works for 90% of use cases), upgrade to **Sentry Team at $26/mo** when you outgrow free, then switch to **New Relic** at 1M+ errors/month for cost savings, or **Datadog** if you need enterprise compliance and best-in-class microservices tracing.

**The Three-Tier Strategy:**

1. **Tier 1 (0-1M errors/month):** Sentry (best value, community, SDKs)
2. **Tier 2 (1M-100M errors/month):** New Relic (consumption-based saves 50-80%)
3. **Tier 3 (100M+ errors OR compliance):** Datadog (if budget allows) or New Relic (if cost-sensitive)

**Budget-Based Summary:**

- **$0/month:** Sentry Free, Bugsnag Free, or Firebase (all excellent)
- **$0-50/month:** Bugsnag Lite ($18) or Sentry Team ($26)
- **$50-500/month:** Sentry Business ($80) or New Relic (3 users)
- **$500-5,000/month:** New Relic or Datadog (depending on use case)
- **$5,000+/month:** Datadog (enterprise compliance + full observability)

---

**End of S3 Need-Driven Discovery**

For detailed use case analysis, see individual use-case-*.md files in this directory.
