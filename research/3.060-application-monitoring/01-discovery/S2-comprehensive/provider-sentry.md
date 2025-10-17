# Sentry - Application Monitoring Provider

## Overview

**Provider**: Sentry
**Website**: https://sentry.io
**Founded**: 2015 (open-sourced 2008)
**Headquarters**: San Francisco, CA
**Type**: SaaS + Self-Hosted (Open Source)

Sentry is a developer-first error tracking and performance monitoring platform that helps developers detect, triage, and resolve issues in real-time. Originally an open-source project, Sentry has become the industry leader in application monitoring with both cloud-hosted and self-hosted deployment options.

## Core Capabilities

### Error Tracking
- **Real-time Error Capture**: Automatic exception and error detection across all platforms
- **Stack Traces**: Full call stacks with file names, line numbers, function contexts
- **Source Maps**: Support for minified JavaScript, TypeScript, React Native
- **Error Grouping**: Intelligent deduplication using fingerprinting algorithm
- **Breadcrumbs**: Automatic capture of user actions, network requests, console logs
- **Release Tracking**: Deploy annotations, commit tracking, regression detection
- **Issue Ownership**: Auto-assign errors to code owners via CODEOWNERS integration

### Performance Monitoring
- **Distributed Tracing**: End-to-end transaction traces across microservices
- **Database Monitoring**: SQL query tracking, N+1 detection, slow query alerts
- **Web Vitals**: LCP, FID, CLS tracking for frontend performance
- **API Performance**: Endpoint latency, throughput, error rates
- **Custom Instrumentation**: Manual transaction creation, span tracking
- **Performance Alerts**: Threshold-based alerting for degraded endpoints

### Session Replay (Beta/Add-on)
- Video-like reproduction of user sessions
- DOM event capture, mouse movements, clicks, scrolls
- Privacy controls for PII masking
- Linked to error events for context

### Profiling (Beta)
- Code-level performance profiling
- Flamegraph visualization
- Function-level CPU time analysis
- Available for Python, PHP, Node.js, iOS, Android

## Platform Support

### Backend Languages
- Python, JavaScript/Node.js, Ruby, PHP, Java, Go, .NET (C#), Elixir, Rust
- Frameworks: Django, Flask, Rails, Laravel, Spring Boot, Express, Next.js

### Frontend
- JavaScript, TypeScript, React, Vue, Angular, Svelte, Next.js, Remix
- Automatic breadcrumb capture for DOM events
- Source map upload via CLI or build plugins

### Mobile
- iOS (Swift, Objective-C), Android (Java, Kotlin)
- React Native, Flutter, Xamarin, Unity
- Crash reporting, ANR detection, slow frames

### Serverless
- AWS Lambda, Google Cloud Functions, Azure Functions
- Vercel, Netlify, Cloudflare Workers

## Integrations

### Issue Trackers
- GitHub Issues, GitLab Issues, Jira, Linear, Asana, Azure DevOps
- Two-way sync: create issues, link errors, track resolution

### Communication & Alerting
- Slack, Microsoft Teams, Discord, PagerDuty, OpsGenie, Webhooks

### Source Control
- GitHub, GitLab, Bitbucket: commit tracking, suspect commits, code owners

### CI/CD
- GitHub Actions, GitLab CI, CircleCI: deploy tracking, release automation

## Pricing (2025)

### Developer (Free)
- **Cost**: $0/month
- **Errors**: 5K errors/month
- **Performance**: 10K transactions/month
- **Replays**: 50 replays/month
- **Users**: Unlimited
- **Retention**: 30 days
- **Best For**: Personal projects, small apps, staging environments

### Team
- **Base Cost**: $29/month (pay-as-you-go)
- **Errors**: 50K errors included, then $0.000232/error
- **Performance**: 100K transactions included, then $0.0003/transaction
- **Replays**: $5 per 1K replays
- **Users**: Unlimited
- **Retention**: 90 days
- **Features**: Error tracking, performance monitoring, release tracking, basic integrations
- **Best For**: Startups, growing teams, production apps

### Business
- **Base Cost**: Custom pricing (estimated $99-299/month)
- **Errors**: 100K+ errors negotiated
- **Performance**: 1M+ transactions negotiated
- **Users**: Unlimited
- **Retention**: 90 days
- **Features**: Priority support, data forwarding, advanced integrations
- **Best For**: Established companies, multiple products

### Enterprise
- **Cost**: Custom (estimated $1K-10K+/month)
- **Volume**: Millions to billions of events
- **Features**: SSO/SAML, SCIM provisioning, data residency (EU/US), SLA, dedicated support
- **Retention**: Custom (up to 365 days)
- **Self-Hosted**: Available with support contract
- **Best For**: Large enterprises, regulated industries, high-volume platforms

### Self-Hosted (Open Source)
- **Cost**: $0 (infrastructure costs only)
- **License**: Business Source License (BSL)
- **Support**: Community (paid support available)
- **Features**: Full feature parity with cloud version
- **Requirements**: Docker, PostgreSQL, Redis, ~4GB RAM minimum
- **Best For**: Cost-conscious teams, data sovereignty requirements, high-scale operations

## Compliance & Security

- **Certifications**: SOC 2 Type II, ISO 27001, Privacy Shield
- **GDPR**: EU data residency, data deletion, DPA available
- **Data Scrubbing**: Automatic PII detection and redaction
- **IP Allowlisting**: Enterprise feature
- **Audit Logs**: Enterprise feature

## Pros

1. **Open Source**: Self-hosting option with full feature parity
2. **Developer Experience**: Best-in-class UI, excellent documentation
3. **Platform Coverage**: Widest language/framework support
4. **Performance Monitoring**: Integrated APM without separate product
5. **Active Development**: Frequent feature releases, strong community
6. **Generous Free Tier**: 5K errors/month for unlimited projects
7. **Release Tracking**: Deploy annotations, suspect commits, regression detection
8. **Customization**: Extensive SDK customization, hooks, filters

## Cons

1. **Pricing Complexity**: Event-based model can be unpredictable at scale
2. **Cost at Scale**: Can become expensive for high-volume apps (10M+ errors/month)
3. **Self-Hosting Overhead**: Requires DevOps expertise, infrastructure management
4. **Feature Fragmentation**: Some features (replays, profiling) are add-ons or beta
5. **Alert Fatigue**: Default settings can generate high alert volume
6. **Learning Curve**: Advanced features require configuration expertise
7. **License Change**: Moved from Apache to BSL (still self-hostable but not fully open source)

## Use Cases

### Ideal For
- Startups needing generous free tier
- Teams requiring self-hosting for compliance
- Multi-platform apps (web + mobile + backend)
- Open-source projects (free team accounts)
- Companies valuing developer experience

### Not Ideal For
- Simple apps with minimal error volume (overkill)
- Teams needing pure APM without error tracking
- Budget-constrained teams at high scale (10M+ events)
- Teams wanting simple, flat-rate pricing

## Notable Customers

- Atlassian, Cloudflare, Disney+, GitHub, Microsoft, Netlify, Peloton, Uber

## Recent Updates (2024-2025)

- LLM Monitoring (Beta): Error tracking for AI/ML applications
- Cron Monitoring: Scheduled job monitoring and alerting
- Improved Error Grouping: Machine learning-based fingerprinting
- Session Replay GA: Video-like user session reproduction
- Trace Explorer: Advanced search and filtering for performance data

## Recommendation Score: 9.5/10

**Best Overall Choice** for most development teams due to comprehensive features, platform coverage, self-hosting option, and strong community. The free tier is generous enough for most small projects, and pricing scales reasonably for mid-sized teams. Self-hosting provides an escape hatch for cost-conscious or compliance-driven organizations.
