# Application Monitoring - S2 Comprehensive Discovery

## Overview
Comprehensive discovery and analysis of Application Monitoring / Error Tracking services (experiment 3.060).

## Files Created

### Core Documentation
- **approach.md** (171 lines) - Comprehensive research methodology and evaluation framework
- **recommendation.md** (380 lines) - Final recommendations with decision matrix by use case

### Comparison Matrices
- **pricing-matrix.md** (222 lines) - Pricing comparison across 4 volume tiers (10K, 100K, 1M, 10M errors/month)
- **feature-matrix.md** (215 lines) - Feature comparison across error tracking, APM, integrations, compliance

### Provider Profiles (Modular, Reusable)
- **provider-sentry.md** (183 lines) - Sentry: Industry leader, open-source, self-hosting option
- **provider-rollbar.md** (196 lines) - Rollbar: ML-powered error grouping, impact analysis
- **provider-bugsnag.md** (183 lines) - Bugsnag: Mobile-first, stability scoring, release health
- **provider-honeybadger.md** (211 lines) - Honeybadger: Best value, bundled uptime monitoring
- **provider-airbrake.md** (206 lines) - Airbrake: Mature platform, separate error/performance products
- **provider-trackjs.md** (198 lines) - TrackJS: Frontend-only, unlimited errors (pageview-based)
- **provider-raygun.md** (190 lines) - Raygun: All-in-one (errors + RUM + APM), AI resolution
- **provider-datadog.md** (224 lines) - Datadog: Enterprise observability, infrastructure correlation

## Key Findings

### Top Recommendation: Sentry (9.5/10)
- Best free tier: 5K errors + 10K transactions/month
- Only viable self-hosting option (open-source)
- Widest platform coverage (web + mobile + backend)
- Integrated APM (performance monitoring included)

### Runner-Up #1: Honeybadger (8.5/10 - Best Value)
- Best pricing: $26/month for errors + uptime + cron monitoring
- Bundled features (no separate products)
- Best for Ruby/Elixir applications
- Transparent, predictable pricing

### Runner-Up #2: Bugsnag (8.0/10 - Best for Mobile)
- Industry-leading mobile crash reporting
- Stability scoring (30-day app health metrics)
- Best iOS/Android symbolication
- Release health tracking

### Specialized Recommendations
- **Frontend-Only**: TrackJS (unlimited errors, pageview-based pricing)
- **All-in-One**: Raygun (errors + RUM + APM in one platform)
- **Enterprise**: Datadog (unified observability, $46+/host/month)

## Pricing Summary

| Provider | Free Tier | 100K Errors | 1M Errors | 10M Errors |
|----------|-----------|-------------|-----------|------------|
| Sentry | $0 (5K) | ~$29 | ~$232-300 | $1K-3K |
| Honeybadger | $0 (1K) | $26 | $80 + overages | $500+ |
| Rollbar | $0 (5K, 1 proj) | $59 | $299 | $799-2K |
| Bugsnag | Contact | ~$50-100 | ~$200-400 | $1K-5K |
| Airbrake | Trial only | $59 | $299 | $799-2K |
| TrackJS | Trial only | $49-99 | ~$299+ | $500-1.5K |
| Raygun | Trial only | ~$40-80 | ~$150-300 | $500-2K |
| Datadog | Trial only | $46/host | $460-920 | $4.6K-23K+ |

## Decision Matrix

### Use Case → Recommendation
- **Bootstrapped Startup**: Sentry Free → Honeybadger Team ($26/month)
- **Growing SaaS**: Sentry Team/Business
- **Mobile-First**: Bugsnag
- **Ruby/Rails**: Honeybadger
- **Frontend-Heavy**: TrackJS
- **Enterprise (100+ hosts)**: Sentry Self-Hosted or Datadog

## Research Methodology
- Web search for 2025 pricing and features
- Official provider documentation analysis
- Third-party reviews and comparisons
- Pricing transparency evaluation
- Feature parity testing across platforms

## Total Files: 12
- 1 approach document
- 8 provider profiles (modular, <225 lines each)
- 2 comparison matrices
- 1 comprehensive recommendation

All files designed for modularity and reuse across future experiments.
