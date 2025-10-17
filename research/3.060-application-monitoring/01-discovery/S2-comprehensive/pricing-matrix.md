# Application Monitoring Pricing Matrix

## Overview

This matrix compares pricing across major application monitoring providers at different volume tiers. Pricing is based on 2025 publicly available information and estimates where exact pricing requires sales contact.

## Pricing by Volume Tier

### Micro Tier: 10K Errors/Month
**Use Case**: Personal projects, small apps, staging environments

| Provider | Monthly Cost | Included Events | Users | Retention | Notes |
|----------|--------------|-----------------|-------|-----------|-------|
| Sentry | $0 (Free) | 5K errors + 10K transactions | Unlimited | 30 days | Best free tier |
| Honeybadger | $0 (Free) | 1K errors | 1 user | 7 days | Solo developer only |
| Rollbar | $0 (Free) | 5K events | Unlimited | 30 days | 1 project limit |
| Airbrake | $19 | 25K errors | Unlimited | 30 days | No free tier with meaningful volume |
| Bugsnag | Contact Sales | Unknown | Unknown | Unknown | No transparent free tier |
| TrackJS | $49 | 100K pageviews (unlimited errors) | Unlimited | 30 days | Pageview-based |
| Raygun | $40 (est.) | 50K events (est.) | Unlimited | 30 days | Contact sales |
| Datadog APM | N/A | Minimum 1 host | Unlimited | 15 days | $46/host minimum (APM + Infra) |

**Winner**: Sentry (5K errors free with performance monitoring)

---

### Small Tier: 100K Errors/Month
**Use Case**: Growing startups, single product, production apps

| Provider | Monthly Cost | Included Events | Users | Retention | Notes |
|----------|--------------|-----------------|-------|-----------|-------|
| Sentry | ~$29 (PAYG) | 50K base + overages | Unlimited | 90 days | $0.000232/error overage |
| Honeybadger | $26 | 25K errors | Unlimited | 90 days | $0.0003/error overage |
| Rollbar | $59 (est.) | 100K events | Unlimited | 30 days | Essentials tier |
| Airbrake | $59 | 100K errors | Unlimited | 30 days | Tier 2 (Essential) |
| Bugsnag | ~$50-100 (est.) | 50K-100K events | Unlimited | Unknown | Contact sales |
| TrackJS | $49-99 (est.) | 100K-500K pageviews | Unlimited | 30-90 days | Unlimited errors |
| Raygun | ~$40-80 (est.) | 100K events | Unlimited | 30 days | Contact sales |
| Datadog APM | $46/host | Based on hosts, not events | Unlimited | 15 days | APM ($31) + Infra ($15) |

**Winner**: Honeybadger ($26/month with uptime monitoring bundled)

---

### Medium Tier: 1M Errors/Month
**Use Case**: Established products, multiple services, high traffic

| Provider | Monthly Cost | Included Events | Users | Retention | Notes |
|----------|--------------|-----------------|-------|-----------|-------|
| Sentry | ~$232-300 (est.) | PAYG or reserved volume | Unlimited | 90 days | Contact for Business plan |
| Honeybadger | $80 | 125K errors + overages | Unlimited | 90 days | $0.0006/error overage |
| Rollbar | $299 | 1M events | Unlimited | 90 days | Tier 4 (Growth) |
| Airbrake | $299 | 1M errors | Unlimited | 30 days | Tier 4 (Growth) |
| Bugsnag | ~$200-400 (est.) | 1M events | Unlimited | Unknown | Contact sales |
| TrackJS | ~$299+ (est.) | 2M+ pageviews | Unlimited | 90 days | Unlimited errors |
| Raygun | ~$150-300 (est.) | 1M events | Unlimited | 30 days | Contact sales |
| Datadog APM | $460-920 | N/A (10-20 hosts est.) | Unlimited | 15 days | $46/host × host count |

**Winner**: Rollbar or Airbrake ($299/month for 1M errors)

---

### Large Tier: 10M Errors/Month
**Use Case**: Enterprise, high-traffic platforms, multiple products

| Provider | Monthly Cost | Included Events | Users | Retention | Notes |
|----------|--------------|-----------------|-------|-----------|-------|
| Sentry | $1,000-3,000 (est.) | Custom negotiated | Unlimited | 90-365 days | Enterprise plan |
| Honeybadger | $500+ (custom) | 500K+ errors + overages | Unlimited | Custom | Enterprise plan |
| Rollbar | $799-2,000+ | 5M-10M+ events | Unlimited | 90-365 days | Tier 5 + custom |
| Airbrake | $799-2,000+ | 5M-10M+ errors | Unlimited | 90 days | Tier 5 + custom |
| Bugsnag | $1,000-5,000 (est.) | 10M+ events | Unlimited | Custom | Enterprise plan |
| TrackJS | $500-1,500 (est.) | 10M+ pageviews | Unlimited | 90 days | Enterprise plan |
| Raygun | $500-2,000 (est.) | 10M+ events | Unlimited | Custom | Enterprise plan |
| Datadog APM | $4,600-23,000+ | N/A (100-500 hosts est.) | Unlimited | 15-90 days | $46/host × host count |

**Winner**: Sentry Self-Hosted ($0 + infrastructure costs)

---

## Free Tier Comparison

| Provider | Errors/Month | Performance | Projects | Users | Retention | Best For |
|----------|--------------|-------------|----------|-------|-----------|----------|
| Sentry | 5K | 10K transactions | Unlimited | Unlimited | 30 days | Best overall free tier |
| Honeybadger | 1K | Limited | Unlimited | 1 user | 7 days | Solo developers |
| Rollbar | 5K | No | 1 project | Unlimited | 30 days | Single project testing |
| Airbrake | Trial only | Trial only | Trial only | Trial only | Trial only | No permanent free tier |
| Bugsnag | Unknown | Unknown | Unknown | Unknown | Unknown | No transparent free tier |
| TrackJS | Trial only | N/A | Trial only | Trial only | Trial only | No permanent free tier |
| Raygun | Trial only | Trial only | Trial only | Trial only | Trial only | No permanent free tier |
| Datadog | Trial only | Trial only | Trial only | Trial only | 14 days | No permanent free tier |

**Winner**: Sentry (most generous free tier: 5K errors + 10K transactions)

---

## Enterprise Pricing Features

| Provider | SSO/SAML | Self-Hosting | Data Residency | SLA | Dedicated Support | Min. Price/Month |
|----------|----------|--------------|----------------|-----|-------------------|------------------|
| Sentry | Yes | Yes (open-source) | EU/US | Yes | Yes | $1,000+ (est.) |
| Honeybadger | Business+ | No | Limited | Enterprise | Enterprise | $500+ |
| Rollbar | Enterprise | No | No | Enterprise | Enterprise | $799+ |
| Airbrake | No | No | No | No | Priority only | $799+ |
| Bugsnag | Yes | No | EU available | Yes | Yes | $1,000+ (est.) |
| TrackJS | Enterprise | No | No | Enterprise | Enterprise | $500+ (est.) |
| Raygun | Yes | No | EU/US | Yes | Yes | $500+ (est.) |
| Datadog | Yes | Limited | EU/US/Gov | Yes | Yes | $5,000+ (est.) |

**Winner**: Sentry (self-hosting option + comprehensive enterprise features)

---

## Cost per Million Events (1M Errors/Month)

| Provider | Monthly Cost | Cost per 1M Events | Notes |
|----------|--------------|-------------------|-------|
| Sentry | ~$232-300 | $232-300 | PAYG or reserved volume |
| Honeybadger | ~$528 | $528 | 125K base + 875K overage @ $0.0006 |
| Rollbar | $299 | $299 | Tier 4 plan |
| Airbrake | $299 | $299 | Tier 4 plan |
| Bugsnag | ~$200-400 | $200-400 | Estimated, contact sales |
| TrackJS | ~$299+ | N/A | Pageview-based, not event-based |
| Raygun | ~$150-300 | $150-300 | Estimated, contact sales |
| Datadog APM | Variable | N/A | Host-based pricing, not event-based |

**Winner**: Rollbar/Airbrake ($299 flat rate for 1M errors)

---

## Self-Hosting Cost Comparison

### Sentry Self-Hosted
- **Software Cost**: $0 (Business Source License)
- **Infrastructure**: ~$50-200/month (4-8GB RAM, PostgreSQL, Redis)
- **Scale**: ~$500-2,000/month at enterprise scale (multi-node)
- **Support**: Optional paid support contracts
- **Break-Even**: ~1M+ events/month vs SaaS

### Other Providers
- **Honeybadger**: No self-hosting option
- **Rollbar**: No self-hosting option
- **Airbrake**: No self-hosting option
- **Bugsnag**: No self-hosting option
- **TrackJS**: No self-hosting option
- **Raygun**: No self-hosting option
- **Datadog**: Limited on-premise (contact sales, expensive)

**Winner**: Sentry (only viable self-hosting option)

---

## Pricing Model Comparison

| Provider | Pricing Model | Predictability | Overage Handling | Best For |
|----------|---------------|----------------|------------------|----------|
| Sentry | Event-based (PAYG) | Medium | Automatic pay-as-you-go | Variable volume |
| Honeybadger | Event-based (tiers + overage) | High | Optional overages, then stop | Predictable volume |
| Rollbar | Event-based (tiers) | High | On-demand pricing (~20% discount) | Volume-based teams |
| Airbrake | Event-based (tiers) | High | On-demand pricing (~20% discount) | Predictable volume |
| Bugsnag | Event-based (custom) | Low | Custom plans for spikes | Unpredictable/seasonal |
| TrackJS | Pageview-based | High | Pageview-based (no error limits) | Frontend-only |
| Raygun | Event-based (dynamic) | Medium | Dynamic scaling, no hard limits | All-in-one platform |
| Datadog | Host-based | Medium | Span ingestion limits | Infrastructure-heavy |

---

## Total Cost of Ownership (3-Year)

### Startup Scenario (100K errors/month)
| Provider | Year 1 | Year 2 | Year 3 | 3-Yr Total | Notes |
|----------|--------|--------|--------|------------|-------|
| Sentry | $348 | $348 | $348 | $1,044 | Team plan PAYG |
| Honeybadger | $312 | $312 | $312 | $936 | Team plan |
| Rollbar | $708 | $708 | $708 | $2,124 | Essentials plan |
| Airbrake | $708 | $708 | $708 | $2,124 | Tier 2 plan |

**Winner**: Honeybadger ($936 over 3 years)

### Mid-Sized Scenario (1M errors/month)
| Provider | Year 1 | Year 2 | Year 3 | 3-Yr Total | Notes |
|----------|--------|--------|--------|------------|-------|
| Sentry | $3,000 | $3,000 | $3,000 | $9,000 | Business plan (est.) |
| Honeybadger | $960 | $960 | $960 | $2,880 | Business + overages |
| Rollbar | $3,588 | $3,588 | $3,588 | $10,764 | Growth plan |
| Airbrake | $3,588 | $3,588 | $3,588 | $10,764 | Tier 4 plan |

**Winner**: Honeybadger ($2,880 over 3 years)

### Enterprise Scenario (10M errors/month)
| Provider | Year 1 | Year 2 | Year 3 | 3-Yr Total | Notes |
|----------|--------|--------|--------|------------|-------|
| Sentry (SaaS) | $24,000 | $24,000 | $24,000 | $72,000 | Enterprise plan (est.) |
| Sentry (Self-Hosted) | $12,000 | $12,000 | $12,000 | $36,000 | Infrastructure only |
| Datadog APM | $55,200 | $55,200 | $55,200 | $165,600 | 100 hosts @ $46/host |

**Winner**: Sentry Self-Hosted ($36,000 over 3 years)

---

## Recommendations by Budget

### $0/month: Free Tier
- **Best**: Sentry (5K errors + 10K transactions)
- **Runner-up**: Rollbar (5K events, 1 project)

### $0-50/month: Bootstrapped Startup
- **Best**: Honeybadger ($26/month for 25K errors + uptime monitoring)
- **Runner-up**: Sentry Team ($29/month PAYG)

### $50-300/month: Growing Startup
- **Best**: Rollbar ($59-299 for 100K-1M errors)
- **Runner-up**: Airbrake ($59-299 for 100K-1M errors)

### $300-1,000/month: Established Company
- **Best**: Sentry Business (custom pricing, reserved volume)
- **Runner-up**: Bugsnag (stability metrics for mobile-first)

### $1,000+/month: Enterprise
- **Best**: Sentry Self-Hosted (cost control at scale)
- **Runner-up**: Datadog (unified observability platform)
