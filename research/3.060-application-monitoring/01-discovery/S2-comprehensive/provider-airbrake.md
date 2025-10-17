# Airbrake - Application Monitoring Provider

## Overview

**Provider**: Airbrake (by Rakuten)
**Website**: https://www.airbrake.io
**Founded**: 2008 (originally "Hoptoad")
**Acquired**: Airbrake Technologies (2013), Rakuten (2020)
**Headquarters**: San Francisco, CA
**Type**: SaaS (Cloud-only)

Airbrake is one of the oldest error monitoring services, providing error tracking and performance monitoring for web and mobile applications. Known for reliability, enterprise features, and separate error/performance products with independent pricing.

## Core Capabilities

### Error Monitoring
- **Real-time Error Detection**: Automatic exception and crash capture
- **Stack Traces**: Full call stacks with local variables, context
- **Error Grouping**: Intelligent deduplication and fingerprinting
- **Deployment Tracking**: Release annotations, version comparison
- **Code Insights**: Changed files, trends in error rates, fix rates
- **Error Trends**: Historical charts, spike detection
- **Custom Metadata**: User context, environment data, tags

### Performance Monitoring (Separate Product)
- **Transaction Tracing**: Route-level performance tracking
- **Database Queries**: SQL query performance, N+1 detection
- **Background Jobs**: Worker performance monitoring
- **Memory Profiling**: Memory usage patterns
- **Endpoint Analysis**: Slowest routes, throughput metrics
- **Separate Billing**: Error and performance metered independently

### Deployment Tracking
- **Release Management**: Deploy notifications, version tracking
- **Code Insights**: Files changed, error rate trends post-deploy
- **Regression Detection**: Errors introduced in specific release
- **Version Comparison**: Side-by-side error metrics

## Platform Support

### Backend Languages
- Ruby, JavaScript/Node.js, PHP, Java, .NET (C#), Python, Go, Elixir
- Frameworks: Rails, Express, Laravel, Spring, Django, ASP.NET

### Frontend
- JavaScript, TypeScript
- React, Vue, Angular, Ember
- Source map support

### Mobile
- iOS (Swift, Objective-C)
- Android (Java, Kotlin)
- React Native

### Frameworks
- Ruby on Rails, Laravel, Django, Express, ASP.NET, Spring Boot

## Integrations

### Issue Trackers
- GitHub Issues, GitLab, Jira, Pivotal Tracker, Trello, Asana, Azure DevOps

### Communication & Alerting
- Slack, HipChat, Campfire, PagerDuty, Webhooks

### Source Control
- GitHub, GitLab, Bitbucket: commit tracking, blame

### CI/CD
- GitHub Actions, Jenkins, CircleCI: deploy notifications

### Other
- Datadog, Sumo Logic: forward error data

## Pricing (2025)

### Dev (Free)
- **Cost**: $0/month
- **Errors**: Limited (exact number not disclosed)
- **Performance**: Limited events
- **Users**: 1 user
- **Projects**: 1 project
- **Retention**: 7 days
- **Trial**: 30-day trial with unlimited errors/events
- **Best For**: Testing, small personal projects

### Error Monitoring Tiers

#### Tier 1 (Starter)
- **Cost**: $19/month
- **Errors**: 25K errors/month
- **Users**: Unlimited
- **Projects**: Unlimited
- **Retention**: 30 days
- **Best For**: Small apps, staging environments

#### Tier 2 (Essential)
- **Cost**: $59/month
- **Errors**: 100K errors/month
- **Users**: Unlimited
- **Retention**: 30 days

#### Tier 3 (Startup)
- **Cost**: $129/month
- **Errors**: 300K errors/month
- **Users**: Unlimited
- **Retention**: 30 days

#### Tier 4 (Growth)
- **Cost**: $299/month
- **Errors**: 1M errors/month
- **Users**: Unlimited
- **Retention**: 30 days

#### Tier 5 (Business)
- **Cost**: $799/month
- **Errors**: 5M errors/month
- **Users**: Unlimited
- **Retention**: 90 days

### Performance Monitoring Tiers
- **Separate Pricing**: Billed independently from error monitoring
- **Similar Tier Structure**: $19-$799/month based on event volume
- **Can Mix**: Choose different tiers for errors vs performance

### On-Demand Pricing
- **Cost**: ~20% less than base plan events
- **Automatic**: Pay for overages without upgrading
- **Variable**: Rate depends on current plan tier

## Compliance & Security

- **SOC 2**: Type II certified
- **GDPR**: Data scrubbing, EU compliance
- **Data Filtering**: Customizable PII redaction
- **SSO**: Enterprise plans
- **IP Allowlisting**: Available

## Pros

1. **Separate Products**: Independent error and performance monitoring (pay only for what you need)
2. **Mature Platform**: 15+ years of reliability, battle-tested
3. **Unlimited Users**: No per-seat costs
4. **Unlimited Projects**: No project limits on paid plans
5. **On-Demand Pricing**: Cheaper overages vs forced upgrades
6. **Code Insights**: Detailed deployment impact analysis
7. **Transparent Pricing**: Clear tier structure
8. **Rakuten Backing**: Enterprise stability and resources

## Cons

1. **No Self-Hosting**: Cloud-only, no on-premise option
2. **Separate Billing**: Error + performance = 2 separate bills (confusing)
3. **Limited Innovation**: Slower feature development vs Sentry
4. **Smaller Community**: Less active than Sentry, smaller ecosystem
5. **Basic APM**: Performance monitoring less comprehensive than dedicated APM tools
6. **Retention**: Only 30-90 days, shorter than competitors
7. **Older UI**: Interface feels dated compared to Sentry/Bugsnag
8. **Mobile Support**: Less comprehensive than Bugsnag

## Use Cases

### Ideal For
- Teams needing only error tracking (not performance monitoring)
- Established companies valuing reliability over innovation
- Teams with predictable error volumes (clear tier pricing)
- Ruby on Rails shops (historically strong support)
- Organizations requiring mature, proven platform

### Not Ideal For
- Teams wanting bundled error + performance monitoring
- Organizations needing self-hosting
- Startups wanting cutting-edge features (session replay, profiling)
- Mobile-first applications (better options available)
- Teams requiring long data retention (90+ days)

## Notable Customers

- Shopify, Salesforce, Twitch, Zendesk

## Competitive Positioning

### vs Sentry
- **Advantage**: Simpler pricing tiers, separate error/performance products
- **Disadvantage**: No self-hosting, older UI, fewer features (no replay/profiling)

### vs Rollbar
- **Advantage**: More transparent pricing, longer track record
- **Disadvantage**: Less powerful search, weaker error prioritization

### vs Honeybadger
- **Advantage**: More scalable (higher tier options), enterprise backing
- **Disadvantage**: More expensive at lower tiers, no bundled uptime monitoring

## Recent Updates (2024-2025)

- Improved error grouping algorithms
- Enhanced React and Vue.js support
- Better serverless platform support (AWS Lambda, Vercel)
- Updated deployment tracking UI

## Recommendation Score: 7.0/10

**Solid Choice** for teams wanting established, reliable error monitoring with clear pricing. The separate error/performance products allow cost optimization (pay only for what you need), but this also creates billing complexity. Best suited for mid-sized companies with predictable error volumes who value stability over cutting-edge features. Not the most innovative, but dependable and enterprise-ready.

**Best for**: Conservative engineering teams prioritizing reliability and uptime over feature velocity.
