# PostHog - Provider Analysis

## Overview

PostHog is an open-source product analytics platform built for engineers and product teams who want full control over their data. Founded in 2020, PostHog combines analytics, session replay, feature flags, and A/B testing in a single platform with generous free tiers and self-hosting options.

**Best For**: Developer-first teams, privacy-conscious organizations, and startups needing a full product OS without breaking the bank.

## Core Features

### Event Tracking
- **Autocapture**: Automatically capture all frontend events without manual instrumentation
- **Custom Events**: Manual event tracking for specific actions
- **Property Capture**: Automatic and custom event properties
- **Person Profiles**: Unified user profiles with event history
- **Group Analytics**: Track companies, organizations, or teams (B2B)

### Analytics Capabilities

**Product Analytics**
- **Trends**: Track metrics over time with multiple series
- **Funnels**: Conversion analysis with customizable steps
- **Retention**: Cohort retention curves and tables
- **Paths**: User journey visualization and flow analysis
- **Lifecycle**: New, returning, resurrecting, dormant user tracking
- **Stickiness**: Frequency of usage analysis

**Session Replay**
- Pixel-perfect session recordings
- Console logs and network activity capture
- Privacy masking for sensitive data
- Filter by user properties and events
- 15K free recordings/month, then $0.005 per recording
- Rage click and error detection

**Feature Flags**
- Boolean and multivariate flags
- User property-based targeting
- Rollout percentage control
- Local evaluation for performance
- 1M free requests/month, then $0.0001 per request

**A/B Testing (Experiments)**
- Native experimentation framework
- Statistical significance calculation
- Feature flag integration
- Primary and secondary metrics
- 1M free participants/month

**Data Warehouse** (Beta)
- Query external data sources (Stripe, Postgres, etc.)
- Join product data with business data
- SQL interface for custom analysis

### Advanced Features

**SQL Access**
- Direct SQL queries on event data
- HogQL (SQL-like language for PostHog)
- Custom insights and reports
- Data export capabilities

**Actions & Cohorts**
- Define actions from multiple events
- Create behavioral cohorts
- Export cohorts to external tools
- Dynamic cohort updates

**Dashboards**
- Custom dashboard builder
- Scheduled reports via email
- Public dashboard sharing
- Template library

**Plugins & Apps**
- Extend functionality with community apps
- Data transformation pipelines
- Custom integrations
- Export to warehouses and tools

## Pricing Structure

### Pay-Per-Use Model

PostHog uses transparent usage-based pricing with generous free tiers:

**Product Analytics**
- First 1M events/month: FREE
- After 1M: $0.00031 per event
- Volume discounts after 2M/month
- Estimated costs:
  - 1M events: $0/month
  - 3M events: ~$600/year ($50/month)
  - 10M events: ~$2,200/year ($183/month)

**Session Replay**
- First 15K recordings/month: FREE
- After 15K: $0.005 per recording
- Volume discounts after 50K/month
- Estimated costs:
  - 15K recordings: $0/month
  - 50K recordings: ~$175/month
  - 100K recordings: ~$350/month

**Feature Flags**
- First 1M requests/month: FREE
- After 1M: $0.0001 per request
- Volume discounts at scale
- Local evaluation reduces billable requests

**Experiments (A/B Testing)**
- First 1M participant requests: FREE
- After 1M: $0.0001 per participant request

**Surveys**
- First 1,500 responses/month: FREE
- After 1,500: $0.20 per response

### Self-Hosted (Open Source)
- **Cost**: FREE (MIT license)
- **Requirements**: Infrastructure to host (AWS, GCP, DigitalOcean, etc.)
- **Features**: Full platform capabilities
- **Support**: Community support via GitHub, Slack
- **Best For**: Large organizations with infrastructure teams, privacy-first companies

### PostHog Cloud
- **Cost**: Pay-per-use as outlined above
- **Setup**: Instant, no infrastructure needed
- **Support**: Email support, paid priority support available
- **Data Residency**: US or EU options
- **Best For**: Teams wanting easy setup without infrastructure management

### Billing Controls
- Set spending limits per product (never get surprised)
- Usage alerts at custom thresholds
- Monthly free volume resets (don't lose it)
- No credit card required for free tier

## Key Pricing Advantages

1. **98% Use Free**: Most customers stay within free tier limits
2. **No Event Sampling**: Unlimited queries on all your data
3. **No User Seat Charges**: Unlimited team members
4. **Predictable Costs**: Set billing limits, transparent per-unit pricing
5. **Volume Discounts**: Automatic discounts as usage scales

## Integration Ecosystem

### SDKs & Languages
- JavaScript, TypeScript
- React, Next.js, Vue, Svelte
- iOS (Swift)
- Android (Kotlin/Java)
- React Native, Flutter
- Node.js, Python, Ruby, PHP, Go, Java

### Data Warehouses
- Snowflake
- BigQuery
- Redshift
- ClickHouse (native storage)
- Postgres (external data source)

### CDPs & Data Tools
- Segment
- RudderStack
- Hightouch
- Direct warehouse exports

### Development Tools
- GitHub (code insights, automatic PR comments)
- GitLab
- Sentry (error tracking integration)
- Slack
- Zapier

### Marketing & Business Tools
- Stripe (revenue data sync)
- Salesforce
- HubSpot
- Customer.io
- Intercom

## Compliance & Security

### Certifications
- SOC 2 Type II certified
- GDPR compliant
- ISO 27001 (in progress)
- HIPAA available with self-hosting

### Privacy & Data Governance
- EU data residency option
- Automatic PII detection and masking
- User data deletion via API
- Cookie consent integration
- Anonymous user tracking option
- Self-hosting for complete data control

### Access Controls
- SSO via SAML, Google, GitHub (Cloud)
- Role-based access control (RBAC)
- Project-level permissions
- API key management
- 2FA support

## Implementation

### Setup Complexity
- **Time to First Event**: 5-10 minutes (add snippet, events flow immediately)
- **Autocapture Advantage**: Zero instrumentation needed to start
- **Time to Value**: <1 hour to first meaningful insights
- **Technical Skill**: Low - snippet installation, then UI-driven analysis

### Self-Hosted Deployment
- One-click deploy to AWS, GCP, DigitalOcean
- Docker Compose for local testing
- Kubernetes Helm charts for production
- Estimated setup: 2-4 hours for basic deployment

### Migration Support
- Import from Mixpanel, Amplitude via integrations
- Event migration scripts and documentation
- Community-contributed guides

## Support & Resources

### Documentation
- Comprehensive docs.posthog.com
- Open-source code on GitHub
- Tutorial library and guides
- API reference documentation

### Support Tiers
- **Free Users**: Community Slack, GitHub issues
- **Paid Users**: Email support, priority Slack channel
- **Enterprise** (Custom): Dedicated support, Slack Connect, SLAs

### Community
- Active Slack community (10K+ members)
- GitHub discussions and issues
- Regular community calls and AMAs
- PostHog blog with product analytics content

### Open Source Advantage
- Full transparency of codebase
- Community contributions and plugins
- Self-service bug fixes and feature development
- No vendor lock-in

## Strengths

1. **Generous Free Tier**: 1M events, 15K replays, 1M flags monthly - enough for most startups
2. **All-in-One Platform**: Analytics, replay, flags, experiments in one tool (no separate subscriptions)
3. **Autocapture**: Start analyzing without instrumentation, add custom events later
4. **Self-Hosting**: Full data ownership and control for privacy/compliance
5. **Transparent Pricing**: Clear per-unit costs, billing limits, no hidden fees
6. **Developer-Friendly**: Built by engineers for engineers, excellent DX
7. **No User Limits**: Unlimited team members at no extra cost
8. **Open Source**: MIT license, community-driven, extensible

## Limitations

1. **Newer Platform**: Founded 2020, less mature than Mixpanel/Amplitude (catching up fast)
2. **Advanced Analytics Gap**: Lacks some sophisticated behavioral analysis features vs Amplitude
3. **Enterprise Features**: Less robust governance and compliance vs established players
4. **UI Polish**: More functional than beautiful; learning curve for non-technical users
5. **Support Quality**: Community-driven for free tier; paid support less comprehensive than enterprise competitors
6. **Self-Hosting Complexity**: Requires infrastructure expertise and maintenance overhead

## Competitive Positioning

- **vs Mixpanel**: Cheaper (even for <1M events), self-hostable, includes session replay/flags; Mixpanel easier for non-technical users
- **vs Amplitude**: Much more affordable, all-in-one suite; Amplitude has deeper behavioral analytics
- **vs Heap**: Similar autocapture, better pricing, open-source; Heap more mature
- **vs FullStory/LogRocket**: Broader platform (not just replay), better value; competitors have more polished replay UX

## Ideal Use Cases

1. **Startups**: Free tier supports growth from 0 to product-market fit (1M+ events)
2. **Developer-Led Teams**: Engineers who want full data control and customization
3. **Privacy-First Companies**: Self-hosting for GDPR, HIPAA, or data sovereignty requirements
4. **Budget-Conscious Scale-Ups**: $500-2K/month for all tools vs $5K+ with multiple vendors
5. **Full Product Stack Needed**: Single platform for analytics, replay, flags, and experiments
6. **Open-Source Advocates**: MIT license, contribute features, avoid vendor lock-in

## Not Recommended For

1. **Non-Technical Teams**: Requires some technical comfort; Mixpanel better for pure business users
2. **Enterprise Compliance Needs**: Less mature governance than Amplitude/Mixpanel (improving)
3. **Advanced Behavioral Analytics**: Amplitude has deeper predictive and ML features
4. **White-Glove Support Expectations**: Community support may not meet enterprise SLAs
5. **Complex Multi-Product Portfolios**: Amplitude Portfolio better for cross-app analytics

## Special Considerations

**Open Source Philosophy**: PostHog's MIT license means you can fork, modify, and run forever without dependency on the company. This is unique among major analytics platforms.

**Transparent Roadmap**: Public roadmap and GitHub issues mean you can see what's coming and vote on features.

**Fast-Paced Innovation**: New features ship weekly (autocapture improvements, warehouse connectors, AI insights in development).

**Community-Driven**: Many integrations, plugins, and features contributed by users.
