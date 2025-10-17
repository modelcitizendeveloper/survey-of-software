# June - Provider Analysis

## Overview

June is a product analytics platform purpose-built for B2B SaaS companies, offering auto-generated reports focused on company-level (account) analytics rather than individual user behavior. Founded in 2020, June serves product-led growth teams who need quick insights without complex setup.

**Best For**: Early-stage B2B SaaS companies ($1M+ ARR) needing simple, auto-generated company analytics with CRM integrations.

## Core Features

### Auto-Generated Reports (Signature Feature)

**Pre-Built Analytics**
- Active companies report
- Feature adoption tracking
- User engagement metrics
- Retention and churn analysis
- Power users identification
- Time-to-value tracking

**No Configuration Required**
- Reports generate automatically upon setup
- No custom dashboards to build
- Opinionated analytics for SaaS best practices
- Instant insights without analytical expertise

### Company-Level Analytics (B2B Focus)

**Account-Based Tracking**
- Track companies, not just individuals
- Company usage patterns and health scores
- Team engagement within accounts
- Account-level retention and churn

**User Hierarchy**
- Individual users grouped by company
- Role-based analysis within accounts
- Seat usage and expansion signals

### CRM & Business Tool Integrations

**Native Integrations**
- Salesforce (sync companies and usage data)
- HubSpot (bidirectional sync)
- Attio (modern CRM integration)
- Enrichment from CRM data

**Workflow Automation**
- Company and audience alerts
- Usage-based notifications to sales teams
- Automated account scoring
- Trigger-based workflows

### Advanced Features

**Custom Insights**
- SQL queries for custom analysis
- AI-powered query assistance
- Computed traits (derived metrics)
- Custom event tracking beyond auto-generated reports

**Embed API**
- White-label analytics for customer dashboards
- Embed reports in your own product
- Customer-facing usage analytics
- Self-serve customer success

**Alerts & Notifications**
- Company-level alerts (e.g., usage drop)
- Audience-based alerts (segment triggers)
- Slack, email notifications
- Real-time threshold monitoring

## Pricing Structure

### Minimum Viable Customer
- **Target Customers**: Companies with at least $1M ARR
- **Positioning**: Not for very early-stage startups
- **Rationale**: Opinionated that earlier companies need simpler/cheaper tools

### Pricing Model
- **Public Information**: Limited specific pricing details available
- **Custom Pricing**: Contact sales for quotes
- **Setup Fees**: Vary based on implementation complexity

### Estimated Costs
- **Entry Point**: Estimated $500-1,000+/month (based on target customer profile)
- **Scaling**: Likely based on company count or event volume
- **Annual Contracts**: Typical for B2B SaaS tools

### What's Included
- Auto-generated reports
- Company-level analytics
- CRM integrations (Salesforce, HubSpot, Attio)
- Custom insights with SQL & AI
- Computed traits
- 1:1 support and onboarding
- Company and audience alerts
- Embed API for customer-facing analytics

## Integration Ecosystem

### CRM & Sales Tools (Strength)
- Salesforce
- HubSpot
- Attio (modern CRM)
- Bidirectional data sync
- Enrichment from CRM fields

### Development & Data
- Segment (event tracking)
- APIs for custom integrations
- SQL access to underlying data
- Data warehouse export (limited info)

### Communication
- Slack (alerts and notifications)
- Email notifications

### SDKs
- JavaScript
- React
- Node.js
- Other platforms (limited public info)

## Compliance & Security

### Security Features
- Standard SaaS security practices
- Data encryption in transit and at rest
- Access controls

### Privacy & Compliance
- GDPR considerations (EU customers)
- Data processing agreements
- User data deletion capabilities

**Note**: Less public information on certifications (SOC 2, ISO) compared to enterprise-focused competitors.

## Implementation

### Setup Complexity
- **Time to First Insight**: <1 hour (install snippet, reports auto-generate)
- **No Configuration**: Reports appear automatically
- **CRM Integration**: Additional 1-2 hours for Salesforce/HubSpot sync
- **Technical Skill**: Low - simple snippet installation

### Best Practices
- Connect CRM early for enriched company data
- Define key product events for tracking
- Set up alerts for at-risk accounts
- Use Embed API for customer-facing dashboards

### Onboarding
- 1:1 support and onboarding included
- Guided setup process
- Best practices for B2B SaaS analytics

## Support & Resources

### Support
- 1:1 support and onboarding (included in pricing)
- Responsive team (small company, direct access)
- Email and potentially Slack support

### Documentation
- Limited public documentation compared to larger vendors
- Setup guides for integrations
- API documentation for Embed API

### Community
- Smaller user base (newer, niche product)
- No large public community forum
- Product Hunt presence and founder engagement

## Strengths

1. **B2B SaaS Focus**: Purpose-built for company-level analytics, not generic
2. **Auto-Generated Reports**: No setup required, instant insights
3. **CRM Integrations**: Deep Salesforce/HubSpot integration for unified data
4. **Simplicity**: Opinionated approach reduces complexity for early teams
5. **Customer-Facing Analytics**: Embed API enables product-led growth with usage dashboards
6. **1:1 Onboarding**: Included support uncommon at lower price points
7. **SQL + AI**: Custom insights when auto-generated reports aren't enough

## Limitations

1. **Narrow Focus**: Only for B2B SaaS; not suitable for B2C, marketplaces, etc.
2. **Early-Stage Exclusion**: Explicitly not for <$1M ARR companies
3. **Limited Customization**: Auto-generated reports may not fit all use cases
4. **Smaller Ecosystem**: Fewer integrations than Mixpanel/Amplitude
5. **Less Mature**: Founded 2020, less proven than established players
6. **No Experimentation**: No A/B testing framework
7. **No Session Replay**: Pure analytics, no visual debugging
8. **Opaque Pricing**: Must contact sales for quotes

## Competitive Positioning

- **vs Mixpanel/Amplitude**: More opinionated, B2B-focused; less flexible and customizable
- **vs PostHog**: Similar modern approach; PostHog broader platform with replay/flags/experiments
- **vs Pendo**: June pure analytics; Pendo includes guides and NPS
- **vs ChartMogul**: June broader product analytics; ChartMogul focused on SaaS metrics/MRR

## Ideal Use Cases

1. **Product-Led Growth B2B SaaS**: Companies with self-serve signups and trials
2. **Early Growth Stage**: $1M-$10M ARR companies needing quick insights
3. **Non-Technical Product Teams**: PMs who need analytics without data team support
4. **Account Health Monitoring**: Sales/CS teams tracking company engagement
5. **Customer Success Analytics**: Identify at-risk accounts and expansion opportunities
6. **White-Label Analytics**: Embed usage dashboards in your product for customers

## Not Recommended For

1. **Very Early Startups**: <$1M ARR (June explicitly says use something else)
2. **B2C Products**: Individual user behavior focus, not company-level
3. **Complex Custom Analytics**: Limited flexibility vs Mixpanel/Amplitude
4. **Experimentation-Heavy Teams**: No A/B testing (use Amplitude or PostHog)
5. **Budget-Constrained Teams**: Likely more expensive than PostHog, Mixpanel free tiers
6. **Non-SaaS Products**: Purpose-built for SaaS, poor fit for e-commerce, content, etc.

## Special Considerations

**Opinionated Design Philosophy**: June makes product decisions for you (auto-generated reports, B2B focus, ARR requirements). This is:
- **Positive**: Faster time-to-value, less decision paralysis, best practices baked in
- **Negative**: Less flexible, may not fit unique needs, can't customize deeply

**ARR Requirement Context**: June's stance that <$1M ARR companies should use simpler tools is based on:
- Belief that early teams should focus on building, not analytics
- Most startups can use free tiers of Mixpanel, PostHog, or Amplitude
- June's pricing and features optimized for post-PMF scaling phase

**CRM as Source of Truth**: Deep CRM integration means June works best when:
- Salesforce/HubSpot is already set up and maintained
- Company data is clean and up-to-date in CRM
- Product and sales teams collaborate closely

**Customer-Facing Analytics**: Embed API enables unique use case:
- Show customers their own usage data
- Drive product adoption through transparency
- Enable self-serve customer success
- Differentiate with data-driven value demonstration

**Small Team Trade-offs**: As a newer, smaller company, June offers:
- **Pros**: Direct access to team, fast feature requests, 1:1 support
- **Cons**: Less proven, smaller integration ecosystem, uncertainty about long-term viability
