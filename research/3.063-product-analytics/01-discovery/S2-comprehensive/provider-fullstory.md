# FullStory - Provider Analysis

## Overview

FullStory is a digital experience analytics platform that combines session replay with behavioral analytics, heatmaps, and error tracking. Founded in 2014, FullStory serves companies like Icelandair, VMware, and Stack Overflow, specializing in understanding user frustration and optimizing digital experiences.

**Best For**: UX/CX teams prioritizing session replay to understand user struggles, with analytics as a secondary capability.

## Core Features

### Session Replay (Core Strength)

**Pixel-Perfect Recordings**
- Captures every user session with high fidelity
- DOM reconstruction (not video) for privacy and performance
- Console logs and network activity included
- Mobile app replay for iOS and Android

**Replay Features**
- Rage click detection (user frustration signals)
- Dead click identification (non-functional elements)
- Error tracking and JavaScript exceptions
- Search and filter by user properties, events, or issues
- Playback speed controls and skip idle time

**Privacy Controls**
- Automatic PII masking
- CSS-based redaction rules
- GDPR-compliant data handling
- User consent management

### Product Analytics

**Core Analytics**
- Event tracking and custom events
- Funnel analysis for conversion
- Trends and time-series analysis
- Segmentation by user properties
- Retention analysis

**Heatmaps**
- Click heatmaps (aggregate user clicks)
- Scroll depth analysis
- Attention mapping (where users focus)
- Mobile gesture heatmaps

**Dashboards**
- Custom dashboard builder
- Pre-built templates
- Scheduled reports
- Team sharing

**User Insights**
- Individual user profiles with session history
- User journey mapping
- Cross-session tracking
- Behavioral segments

### Developer Tools

**Error Tracking**
- Automatic JavaScript error detection
- Error impact analysis (how many users affected)
- Stack traces and context
- Integration with session replay for debugging

**Page Performance**
- Load time tracking
- Core Web Vitals monitoring
- Slow page identification
- Performance impact on user behavior

### Advanced Features

**Funnel Analysis**
- Multi-step conversion funnels
- Drop-off points with session replay links
- Cohort comparison in funnels
- Time-to-convert analysis

**Segmentation**
- Behavioral segments
- Custom user properties
- Dynamic segment updates
- Export to marketing tools

**Integrations** (Limited)
- Slack for alerts
- JIRA for bug tracking
- Zendesk for support
- Data export to warehouses (add-on)

## Pricing Structure

### Free Plan
- **Volume**: 5,000 sessions (14-day trial of Business plan)
- **Duration**: 14-day trial only
- **Features**: Full Business plan access during trial
- **Limitations**: Not a permanent free tier, trial expires
- **Best For**: Evaluation and proof of concept

### Business Plan
- **Starting Price**: $395/month (reported lowest tier)
- **Typical Price**: $247/month for 75K sessions + 2 months data retention (user-reported)
- **Volume**: Session-based pricing with tiered limits
- **Features**:
  - Product analytics (funnels, trends, segmentation)
  - Session replay
  - Heatmaps
  - Error tracking
  - Developer tools
  - Basic integrations
  - Email support
- **Limitations**: Limited data retention, basic analytics
- **Use Case**: Small to mid-size teams

### Advanced Plan
- **Pricing**: Custom, contact sales (estimated $1K-3K/month)
- **Features**:
  - Everything in Business
  - Advanced analytics (add-ons available)
  - Custom dashboards
  - Extended data retention
  - Priority support
  - Advanced integrations
- **Use Case**: Growing companies with analytics needs

### Enterprise Plan
- **Pricing**: Custom, contact sales (estimated $5K-15K+/month)
- **Features**:
  - Everything in Advanced
  - Unlimited sessions (or very high limits)
  - Custom data retention
  - SSO and advanced security
  - Dedicated CSM
  - SLA guarantees
  - Professional services
  - Custom integrations
- **Use Case**: Large enterprises

### Pricing Model Notes
- **Session-Based**: Pricing by number of sessions captured
- **Opaque Pricing**: Must contact sales for specific quotes
- **Add-On Costs**: Advanced analytics features (funnels, custom dashboards, segmentation) available as add-ons on lower tiers
- **Data Retention**: Lower tiers have limited retention (2-3 months); longer retention costs more
- **Competitive Positioning**: Higher priced than basic session replay tools

## Integration Ecosystem

### Limited Compared to Analytics-First Tools

**Development Tools**
- JIRA (bug tracking from replays)
- GitHub
- Sentry (error tracking)
- Slack (alerts and notifications)

**Support & CX Tools**
- Zendesk
- Intercom
- Salesforce Service Cloud

**Analytics & Data**
- Segment (limited)
- Data warehouse export (add-on)
- BigQuery, Snowflake, Redshift

**Marketing Tools**
- Limited native integrations
- Export segments for use elsewhere

### SDKs & Platforms
- Web (JavaScript)
- iOS (Swift)
- Android (Kotlin/Java)
- React Native
- Flutter (beta)

## Compliance & Security

### Certifications
- SOC 2 Type II
- GDPR compliant
- CCPA support
- ISO 27001

### Privacy & Data Governance
- Automatic PII redaction
- CSS-based privacy rules
- User data deletion APIs
- Data residency options
- Data processing agreements (DPAs)

### Access Controls
- SSO via SAML (Advanced/Enterprise)
- Role-based access control
- Project-level permissions
- Audit logs (Enterprise)

## Implementation

### Setup Complexity
- **Time to First Session**: 15-30 minutes (install script)
- **Time to Value**: 1-2 hours to first meaningful replay insights
- **Technical Skill**: Low - script installation, minimal configuration
- **Performance Impact**: Optimized for minimal page load impact

### Best Practices
- Set up privacy rules before capturing sessions
- Define custom events for analytics
- Configure rage click sensitivity
- Integrate with support tools for faster issue resolution

## Support & Resources

### Documentation
- Help center with guides
- Developer documentation
- Video tutorials
- Integration guides

### Support Tiers
- **Business**: Email support (24-48hr response)
- **Advanced**: Priority email support
- **Enterprise**: Dedicated CSM, phone support, Slack channel, SLAs

### Learning Resources
- FullStory University (training)
- Webinars and demos
- Best practices content
- Customer success resources

## Strengths

1. **Session Replay Quality**: Industry-leading replay fidelity and features
2. **Rage Click Detection**: Unique frustration signals help identify UX issues
3. **Error Tracking**: Combines errors with session context for debugging
4. **Heatmaps**: Aggregate click and scroll data for UX optimization
5. **Privacy Controls**: Robust PII masking and compliance features
6. **Mobile Replay**: Strong iOS and Android replay capabilities
7. **UX/CX Focus**: Purpose-built for understanding user experience

## Limitations

1. **High Cost**: $395+/month expensive vs competitors (PostHog $0-50/month for similar volume)
2. **Analytics Secondary**: Not as deep as Mixpanel/Amplitude for product analytics
3. **Add-On Pricing**: Advanced analytics features (funnels, custom dashboards) cost extra
4. **Limited Integrations**: Fewer third-party integrations vs analytics-first tools
5. **No Experimentation**: No native A/B testing framework
6. **Opaque Pricing**: Must contact sales, frustrating for buyers
7. **Data Retention Costs**: Longer retention periods significantly increase price

## Competitive Positioning

- **vs LogRocket**: Similar session replay focus; LogRocket better for developers (error tracking), FullStory better for UX teams
- **vs PostHog**: More polished replay UX; PostHog much cheaper with broader platform (analytics, flags, experiments)
- **vs Hotjar**: FullStory more robust; Hotjar cheaper and easier for basic heatmaps/replays
- **vs Mixpanel/Amplitude**: Better replay; worse analytics depth and breadth

## Ideal Use Cases

1. **UX/CX Teams**: Optimize user experience with session replays and heatmaps
2. **E-commerce**: Identify checkout friction and abandonment reasons
3. **Support Organizations**: Replicate customer issues for faster resolution
4. **QA Teams**: Catch bugs in production with user session context
5. **Conversion Optimization**: Understand why users don't convert with visual evidence
6. **Design Teams**: Validate design decisions with actual user behavior

## Not Recommended For

1. **Budget-Conscious Startups**: $395+/month too expensive (use PostHog, Hotjar, or Clarity free)
2. **Analytics-First Teams**: Pure analytics needs better served by Mixpanel/Amplitude
3. **Experimentation Focus**: No A/B testing (use Amplitude, PostHog, Optimizely)
4. **High-Volume Apps**: Session-based pricing expensive for millions of sessions
5. **All-in-One Needs**: If you need analytics + replay + flags, PostHog better value
6. **Self-Hosting Requirements**: Cloud-only, no self-hosting option (use PostHog)

## Special Considerations

**Replay vs Analytics Trade-off**: FullStory excels at visual understanding (replay, heatmaps) but lags in quantitative analytics depth. Consider:
- **Replay Priority**: FullStory strong choice for visual insights
- **Analytics Priority**: Mixpanel/Amplitude better for behavioral analysis
- **Both**: PostHog or combine tools (Mixpanel analytics + Hotjar replay)

**Add-On Model Complexity**: FullStory's pricing includes base replay but charges extra for advanced analytics features. Budget for add-ons if you need funnels, custom dashboards, or segmentation.

**Mobile Replay Strength**: FullStory's mobile replay (iOS/Android) is more mature than many competitors, valuable for mobile-first products.

**Enterprise Features Locked**: SSO, advanced security, and compliance features require expensive Enterprise tier.

**Data Retention Costs**: If you need >3 months retention for compliance or analysis, costs increase significantly. Consider alternatives with longer free retention (PostHog: unlimited on self-hosted).
