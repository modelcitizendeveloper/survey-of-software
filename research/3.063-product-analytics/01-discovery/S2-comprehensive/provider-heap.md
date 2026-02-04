# Heap - Provider Analysis

## Overview

Heap is a product analytics platform distinguished by its automatic event capture technology, enabling retroactive analysis without manual instrumentation. Founded in 2013, Heap serves companies like Microsoft, Twilio, and Eventbrite, specializing in reducing setup friction and enabling instant insights.

**Best For**: Teams wanting zero-instrumentation setup, retroactive analysis, and reducing engineering dependencies for analytics.

## Core Features

### Automatic Event Tracking (Signature Feature)

**Autocapture Technology**
- Automatically captures ALL user interactions (clicks, page views, form submissions, etc.)
- No manual event tagging or instrumentation required
- Retroactive event definition - analyze past behavior without prior setup
- Just install code snippet and start capturing immediately

**Benefits**:
- Reduces time to value from weeks to minutes
- Eliminates "we forgot to track that" scenarios
- Allows analysts to explore data without engineering tickets
- Prevents data gaps from missed instrumentation

**Limitations**:
- Can capture excessive noise without proper filtering
- Storage costs higher due to capturing everything
- Requires retroactive cleanup and organization

### Analytics Capabilities

**Funnel Analysis**
- Multi-step conversion funnels with automatic step detection
- Drop-off analysis at each stage
- Compare cohorts within funnels
- Time-to-convert metrics

**Retention & Engagement**
- Cohort retention curves
- Frequency and recency analysis
- User lifecycle tracking (new, active, churned)
- Custom retention definitions

**User Segmentation**
- Behavioral segments based on captured events
- User property enrichment from integrations
- Dynamic segment updates
- Segment export to marketing tools

**Path Analysis**
- User journey visualization
- Most common paths to conversion
- Exit and abandonment points
- Session-based flow analysis

**Dashboards & Reports**
- Custom dashboard builder
- Scheduled email reports
- Team sharing and collaboration
- Pre-built templates

### Advanced Features

**Data Enrichment**
- Unlimited enrichment data sources
- Salesforce, HubSpot, and other CRM integrations
- Combine product behavior with customer data
- Automatic property backfilling

**Data Science Tools** (Higher Tiers)
- SQL access to raw event data
- Custom query builder
- Data export to warehouses
- API access for programmatic analysis

**Session Replay** (Add-On or Partner Integration)
- Not native to Heap, requires third-party tools
- Can correlate replay sessions with Heap events
- Limited compared to dedicated replay tools

**A/B Testing Integration**
- Integrates with external experimentation platforms
- Track experiment variants as cohorts
- Analyze variant performance
- Not a native A/B testing tool (unlike Amplitude/PostHog)

## Pricing Structure

### Free Plan
- **Volume**: Up to 10K monthly sessions
- **Features**:
  - Core analytics charts
  - Unlimited enrichment sources
  - Guides integrations (in-app messaging)
  - 6 months data history
  - SSO support
- **Limitations**: Very low volume, limited data retention

### Growth Plan
- **Starting Price**: $3,600/year (~$300/month) estimated
- **Volume**: Higher session limits (custom based on needs)
- **Features**:
  - Everything in Free
  - Extended data retention (12+ months)
  - Advanced analytics features
  - More team seats
  - Email support
- **Use Case**: Small to mid-size teams

### Pro Plan
- **Pricing**: Custom, estimated $2K-5K/month
- **Volume**: Significant session capacity
- **Features**:
  - Everything in Growth
  - SQL access to data
  - Advanced integrations
  - Priority support
  - Custom data retention
- **Use Case**: Growing companies with analytical needs

### Premier Plan
- **Pricing**: Custom, estimated $5K-15K+/month
- **Volume**: Enterprise-scale sessions
- **Features**:
  - Everything in Pro
  - Dedicated success manager
  - Advanced security and compliance
  - Custom SLAs
  - Professional services
  - Unlimited data retention
- **Use Case**: Large enterprises

### Pricing Model Notes
- **Session-Based**: Pricing by monthly sessions, not events or MTUs
- **Opaque Pricing**: Must contact sales for specific quotes (frustrating for buyers)
- **High Cost Perception**: User reviews cite $2K+/month minimum, expensive vs competitors
- **Annual Commitments**: Typically requires annual contracts
- **No Transparent Tiers**: Unlike Mixpanel/PostHog, no public pricing calculator

## Integration Ecosystem

### SDKs & Platforms
- Web (JavaScript)
- iOS (Swift/Objective-C)
- Android (Java/Kotlin)
- React Native
- Server-side SDKs (limited compared to competitors)

### Data Destinations
- Salesforce
- Marketo
- HubSpot
- Optimizely (for A/B testing)
- Google Ads, Facebook Ads
- Data warehouses (Redshift, BigQuery, Snowflake)

### CDPs
- Segment
- mParticle
- Can send Heap data to CDPs for activation

### BI & Visualization
- Tableau
- Looker
- Mode Analytics
- Direct SQL access on higher tiers

## Compliance & Security

### Certifications
- SOC 2 Type II
- GDPR compliant
- CCPA support
- ISO 27001

### Privacy & Data Governance
- Automatic PII redaction
- Data retention controls
- User deletion APIs (GDPR/CCPA right to be forgotten)
- Data processing agreements (DPAs)
- EU data residency options

### Access Controls
- SSO (SAML) on all plans
- Role-based access control
- Project-level permissions
- Audit logs (higher tiers)

## Implementation

### Setup Complexity
- **Time to First Event**: 10-15 minutes (install snippet, events auto-captured)
- **Time to Value**: <1 hour - immediate insights from autocapture
- **Technical Skill**: Minimal - just snippet installation, no event instrumentation
- **Ongoing Maintenance**: Low - no need to update tracking as product changes

### Best Practices
- Define important events retroactively after observing user behavior
- Set up data governance for event naming conventions
- Use enrichment sources to add business context
- Regularly clean up unused auto-captured events

### Migration
- Import historical data from other analytics tools
- Segment integration for parallel tracking during migration
- Professional services available for complex migrations (Premier)

## Support & Resources

### Documentation
- Help center with guides and tutorials
- Video training library
- API documentation (higher tiers)
- Integration setup guides

### Support Levels
- **Free**: Email support with slow response
- **Growth**: Standard email support
- **Pro**: Priority email support
- **Premier**: Dedicated CSM, Slack channel, phone support, custom SLAs

### Learning Resources
- Heap University (training courses)
- Webinars and product tours
- Best practices guides
- Customer success content

## Strengths

1. **Zero-Instrumentation Setup**: Fastest time-to-first-insight in the industry
2. **Retroactive Analysis**: Define and analyze events from historical data without prior tracking
3. **Reduce Engineering Dependency**: Analysts can explore without creating engineering tickets
4. **Data Completeness**: Never miss tracking critical user actions
5. **Easy for Non-Technical Users**: Low barrier to entry for business analysts
6. **Strong Data Enrichment**: Unlimited enrichment sources integrate business context

## Limitations

1. **High Cost**: Expensive compared to competitors ($3,600/year minimum vs PostHog free)
2. **Opaque Pricing**: Must contact sales, no transparent pricing calculator
3. **Session-Based Pricing**: Less predictable than event-based for high-traffic sites
4. **No Native Experimentation**: Must integrate with external A/B testing tools
5. **Limited Session Replay**: Not a core feature, requires third-party tools
6. **Data Volume Challenges**: Capturing everything can create storage and noise issues
7. **Server-Side Limitations**: Primarily client-side capture, limited backend tracking

## Competitive Positioning

- **vs Mixpanel**: Easier setup with autocapture; Mixpanel has better UX and more features
- **vs Amplitude**: Simpler for non-technical users; Amplitude has deeper behavioral analytics
- **vs PostHog**: Similar autocapture; PostHog much cheaper with broader feature set (flags, replay, experiments)
- **vs Pendo**: Pure analytics; Pendo includes in-app guides natively

## Ideal Use Cases

1. **Rapid Prototyping**: Teams needing immediate insights without instrumentation delays
2. **Non-Technical Analytics Teams**: Business analysts without access to engineering resources
3. **Exploratory Analysis**: Companies wanting to discover patterns retroactively
4. **Agile Product Teams**: Fast-moving teams where manual tracking lags product changes
5. **Client-Side Heavy Apps**: Web and mobile apps where most interactions happen in UI
6. **Data Completeness Priority**: Organizations where missing data is unacceptable

## Not Recommended For

1. **Budget-Conscious Startups**: $300+/month too expensive vs PostHog/Mixpanel free tiers
2. **Backend-Heavy Products**: Limited server-side tracking vs event-based tools
3. **Experimentation-Focused Teams**: No native A/B testing (use Amplitude or PostHog)
4. **Session Replay Needs**: Not a core feature (use FullStory, LogRocket, or PostHog)
5. **Transparent Pricing Requirements**: Opaque pricing frustrates buyers (use PostHog/Mixpanel)
6. **Developer-First Teams**: Developers often prefer explicit instrumentation control

## Special Considerations

**Autocapture Trade-offs**: While powerful, automatic capture can lead to:
- Data bloat and increased storage costs
- Noise requiring filtering and cleanup
- Less semantic meaning than intentionally named events
- Privacy concerns if not properly configured

**Retroactive Analysis Caveat**: Can only analyze events that autocapture detected. Custom backend events or properties still require instrumentation.

**Best Combined With**: Many teams use Heap alongside experimentation platforms (Optimizely, VWO) and session replay tools (FullStory) to fill feature gaps.

**Competitive Pressure**: PostHog now offers autocapture + replay + flags + experiments at a fraction of Heap's cost, creating significant competitive pressure.
