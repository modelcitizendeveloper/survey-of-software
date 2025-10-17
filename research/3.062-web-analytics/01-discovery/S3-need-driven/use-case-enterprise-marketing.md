# Use Case: Enterprise Marketing Site

**Traffic:** 10,000,000+ pageviews/month
**Priority:** GDPR compliance, no Google, data ownership
**Technical Skill:** Enterprise IT, compliance requirements

## Scenario Description

An enterprise B2B company with a global marketing website serving customers in regulated industries and jurisdictions. The organization requires strict data governance, compliance certifications, and cannot use consumer analytics platforms.

**Typical Examples:**
- Financial services marketing site
- Healthcare provider website
- Government contractor portal
- Enterprise SaaS (Fortune 500 customers)
- Multi-national corporation website

## Requirements Analysis

### Must-Have Requirements (7 critical)

1. **High capacity: Handle 10M+ pageviews without degradation**
   - Peak traffic spikes during campaigns
   - Global distribution
   - No performance degradation at scale

2. **Data sovereignty: Self-hosted option for compliance**
   - Data must stay in specific jurisdictions
   - No third-party data sharing
   - Full control over data location

3. **SSO integration: SAML/OAuth for enterprise auth**
   - Integrate with Okta, Azure AD, Google Workspace
   - Single sign-on for all users
   - No separate passwords to manage

4. **Advanced access controls: RBAC, audit logs**
   - Role-based permissions (viewer, editor, admin)
   - Audit trail of all data access
   - Compliance-ready access controls

5. **Custom retention: Configure data retention per regulation**
   - GDPR: 30-day to 2-year retention options
   - HIPAA: Specific retention requirements
   - Industry-specific compliance

6. **Dedicated support: SLA with phone/Slack support**
   - 99.9% uptime SLA
   - Priority support channels
   - Dedicated customer success manager

7. **Compliance certifications: SOC2, ISO 27001, GDPR/CCPA**
   - Certified compliance documentation
   - Third-party audits
   - Legal defensibility

### Nice-to-Have Requirements (7 additional)

8. **Real-time dashboards** - Live operations monitoring
9. **Advanced analytics** - Funnels, cohorts, segmentation
10. **API/integrations** - Data warehouse, CRM, BI tools
11. **Multi-site tracking** - Manage 5-10 properties centrally
12. **White-labeling** - Custom branding for client reporting
13. **99.99% SLA** - Enterprise uptime guarantee
14. **Professional services** - Implementation support, training

## Provider Evaluation

### Option 1: PostHog Self-Hosted Enterprise (99% fit) - RECOMMENDED

**Scoring:**
- High capacity: ClickHouse scales to billions ✅ 100%
- Data sovereignty: Self-hosted option ✅ 100%
- SSO integration: SAML (Enterprise) ✅ 100%
- Access controls: RBAC, audit logs (Enterprise) ✅ 100%
- Custom retention: Configurable ✅ 100%
- Dedicated support: Slack/phone (Enterprise) ✅ 100%
- Compliance: SOC2 Type II (cloud), self-hosted for custom ⚠️ 90%
- Real-time: Yes ✅ 100%
- Advanced analytics: Best-in-class funnels, cohorts ✅ 100%
- API/integrations: Comprehensive ✅ 100%
- Multi-site: Projects management ✅ 100%
- White-labeling: Not available ❌ 0%
- 99.99% SLA: Available on Enterprise ✅ 100%
- Professional services: Implementation support ✅ 100%

**Overall: 13.9/14 = 99%**

**Strengths:**
- Open-source foundation (no vendor lock-in, can fork)
- ClickHouse backend scales to billions of events
- Self-hosted = full data sovereignty
- Enterprise plan includes SSO, RBAC, dedicated support
- Modern product analytics (not just web analytics)
- Active development and community

**Gaps:**
- No white-labeling (only needed for agency/multi-tenant use cases)
- Self-hosted SOC2 requires own certification (cloud version is SOC2 certified)

**TCO:**
- Self-hosted: ~$500-1,000/month infrastructure
- Enterprise cloud: ~$2,000+/month (contact sales)
- Professional services: Implementation support included

**Why Recommended:**
PostHog Enterprise provides the compliance, scale, and features required for enterprise marketing while maintaining open-source flexibility. The self-hosted option ensures data sovereignty while the Enterprise plan adds enterprise auth, support, and SLA. Best for technical enterprises that value modern analytics.

### Option 2: Piwik PRO Enterprise (100% fit) - PERFECT COMPLIANCE FIT

**Scoring:**
- High capacity: Handles enterprise scale ✅ 100%
- Data sovereignty: Self-hosted option (paid) ✅ 100%
- SSO integration: SAML/SSO ✅ 100%
- Access controls: Enterprise RBAC ✅ 100%
- Custom retention: Configurable ✅ 100%
- Dedicated support: Phone/Slack SLA ✅ 100%
- Compliance: SOC2, ISO 27001, GDPR-certified ✅ 100%
- Real-time: Yes ✅ 100%
- Advanced analytics: Funnels, cohorts, custom reports ✅ 100%
- API/integrations: Yes ✅ 100%
- Multi-site: Yes ✅ 100%
- White-labeling: Available ✅ 100%
- 99.99% SLA: Yes ✅ 100%
- Professional services: Full implementation support ✅ 100%

**Overall: 14/14 = 100%**

**Strengths:**
- **Perfect compliance fit** - SOC2, ISO 27001, GDPR all certified
- Mature enterprise vendor (100+ employees, 12+ years)
- Purpose-built for regulated industries
- Full professional services
- White-labeling available
- Excellent compliance documentation

**Gaps:**
- None (perfect fit for requirements)

**TCO:**
- €1,408+/month for 10M pageviews = ~$1,500-2,000/month
- Annual: ~$18,000-24,000/year
- Contact for exact enterprise pricing

**Why Alternative:**
Piwik PRO is the gold standard for compliance-first enterprises. If you're in healthcare, finance, or government and need audited certifications, this is the safest choice. Trade-off is higher cost (~$18-24K/year) vs PostHog self-hosted (~$6-12K/year).

### Option 3: Matomo Self-Hosted with Premium (94% fit)

**Scoring:**
- High capacity: Scales with infrastructure ✅ 100%
- Data sovereignty: Full self-hosted control ✅ 100%
- SSO integration: SAML/LDAP (Premium) ✅ 100%
- Access controls: Yes (Premium plugins) ✅ 100%
- Custom retention: Fully configurable ✅ 100%
- Dedicated support: Premium support available ⚠️ 70%
- Compliance: GDPR-certified, SOC2 possible ⚠️ 90%
- Real-time: Yes ✅ 100%
- Advanced analytics: Funnels, cohorts, segmentation ✅ 100%
- API/integrations: Extensive, direct DB access ✅ 100%
- Multi-site: Roll-up reporting ✅ 100%
- White-labeling: Available (Premium) ✅ 100%
- 99.99% SLA: Self-managed (can achieve with HA) ⚠️ 80%
- Professional services: Limited ecosystem ⚠️ 70%

**Overall: 13.1/14 = 94%**

**Strengths:**
- Most cost-effective enterprise option
- Full feature parity with Premium plugins
- Mature, stable platform (15+ years)
- Active community
- Complete self-hosting control

**Gaps:**
- Support quality vs proprietary vendors
- SLA is self-managed (requires HA infrastructure)
- Professional services ecosystem smaller than Piwik PRO

**TCO:**
- Infrastructure: $200-500/month
- Premium plugins: $200-1,000/year
- Total: ~$2,400-7,000/year
- DIY vs Piwik PRO managed support trade-off

**When to Choose:**
Best for budget-conscious enterprises with strong DevOps teams. Saves $12-17K/year vs Piwik PRO but requires self-management. Good for tech companies comfortable with infrastructure.

### Option 4: Matomo Cloud Enterprise (93% fit)

**Scoring:**
- High capacity: Supported (cloud-hosted) ⚠️ 90%
- Data sovereignty: Limited region choice ❌ 30%
- SSO integration: Available on higher tiers ⚠️ 80%
- Access controls: Yes ✅ 100%
- Custom retention: Configurable ✅ 100%
- Dedicated support: Phone/email SLA ✅ 100%
- Compliance: GDPR-certified, EU hosting ⚠️ 90%
- Real-time: Yes ✅ 100%
- Advanced analytics: Full suite ✅ 100%
- API/integrations: Yes ✅ 100%
- Multi-site: Roll-up reporting ✅ 100%
- White-labeling: Available ✅ 100%
- 99.99% SLA: Yes ✅ 100%
- Professional services: Available ✅ 100%

**Overall: 13.0/14 = 93%**

**Strengths:**
- Managed service (no infrastructure burden)
- GDPR-certified with EU hosting
- Full feature set
- Professional support

**Gaps:**
- **Data sovereignty limited** (cloud-hosted, not fully self-hosted)
- Shared infrastructure
- Higher cost than self-hosted

**TCO:**
- $499/month (1M tier) + custom for 10M
- Estimated: $1,500-2,500/month = $18,000-30,000/year

**When to Choose:**
If you want Matomo features but don't want to self-host. Trade-off is less control over data location but simpler operations.

### Option 5: Amplitude Enterprise (81% fit) - DISQUALIFIED

**Scoring:**
- High capacity: Yes (MTU-based) ⚠️ 80%
- Data sovereignty: Cloud-only (no self-hosting) ❌ 0% **DISQUALIFIED**
- SSO integration: SAML ✅ 100%
- Access controls: RBAC ✅ 100%
- Custom retention: Limited to plan tiers ⚠️ 60%
- Dedicated support: CSM, phone ✅ 100%
- Compliance: SOC2, ISO 27001 ✅ 100%
- Real-time: Yes ✅ 100%
- Advanced analytics: Best-in-class ✅ 100%
- API/integrations: Extensive ✅ 100%
- Multi-site: Projects ✅ 100%
- White-labeling: Not available ❌ 0%
- 99.99% SLA: Yes ✅ 100%
- Professional services: Excellent ✅ 100%

**Overall: 11.4/14 = 81%**

**Gaps:**
- **No self-hosting** (disqualifying for data sovereignty requirement)
- Cloud-only (US-based infrastructure)
- MTU pricing model complex

**Disqualified:** Cannot meet data sovereignty must-have requirement.

### Option 6: Google Analytics 360 (65% fit) - NOT RECOMMENDED

**Scoring:**
- High capacity: Unlimited ✅ 100%
- Data sovereignty: Google-hosted only ❌ 0%
- SSO integration: Google Workspace SSO ✅ 100%
- Access controls: Limited RBAC ⚠️ 60%
- Custom retention: Limited options ⚠️ 70%
- Dedicated support: 360 SLA support ✅ 100%
- Compliance: GDPR disputed in EU ❌ 0%
- Real-time: Yes ✅ 100%
- Advanced analytics: Comprehensive ✅ 100%
- API/integrations: BigQuery, extensive ✅ 100%
- Multi-site: Properties/accounts ✅ 100%
- White-labeling: Not available ❌ 0%
- 99.99% SLA: Yes ✅ 100%
- Professional services: Via partners ⚠️ 80%

**Overall: 9.1/14 = 65%**

**Gaps:**
- No self-hosting (disqualifying)
- GDPR compliance risk (EU court rulings)
- No white-labeling
- Google data sharing concerns

**Not Recommended:** Enterprise requirement is often "no Google" due to GDPR concerns and data sharing policies. Even GA360 fails data sovereignty requirements.

## Implementation Guide

### Recommended: PostHog Self-Hosted Enterprise Setup

**Phase 1: Infrastructure Setup (Week 1)**

**Requirements:**
- Kubernetes cluster (EKS, GKE, AKS) or Docker Swarm
- PostgreSQL database (RDS or self-managed)
- ClickHouse cluster (analytics data store)
- Redis (caching)
- Object storage (S3, GCS, Azure Blob)

**Architecture:**
```
┌─────────────────────────────────────────┐
│  Load Balancer (nginx/ALB)              │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│  PostHog App Servers (3+ instances)     │
│  - API                                  │
│  - Web UI                               │
│  - Event ingestion                      │
└─────────────────────────────────────────┘
                    │
        ┌───────────┴────────────┐
        │                        │
┌───────▼────────┐    ┌──────────▼─────────┐
│  PostgreSQL    │    │  ClickHouse        │
│  (metadata)    │    │  (analytics)       │
└────────────────┘    └────────────────────┘
                    │
            ┌───────▼────────┐
            │  Redis         │
            │  (cache)       │
            └────────────────┘
```

**Deployment (Kubernetes with Helm):**
```bash
# Add PostHog Helm repo
helm repo add posthog https://posthog.github.io/charts-clickhouse
helm repo update

# Configure values.yaml
cat > values.yaml <<EOF
cloud: 'private'
env:
  - name: DEPLOYMENT_MODE
    value: 'self-hosted'

postgresql:
  enabled: true
  auth:
    database: posthog

clickhouse:
  enabled: true
  replicas: 3

redis:
  enabled: true

# Enterprise features
enterprise:
  enabled: true
  license: 'YOUR_LICENSE_KEY'

# SSO configuration
saml:
  enabled: true
  metadata_url: 'https://okta.example.com/metadata'
EOF

# Deploy
helm install posthog posthog/posthog -f values.yaml
```

**Phase 2: Enterprise Configuration (Week 2)**

**1. SSO Setup (SAML with Okta):**
```yaml
# In PostHog instance settings
SAML_ENABLED: true
SAML_ENTITY_ID: 'https://analytics.yourcompany.com'
SAML_METADATA_URL: 'https://yourcompany.okta.com/app/metadata'
SAML_ATTRIBUTE_MAPPING:
  email: 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress'
  first_name: 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname'
  last_name: 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname'
```

**2. RBAC Configuration:**
```python
# Define roles
ROLES = {
  'viewer': ['can_view_insights', 'can_view_dashboards'],
  'analyst': ['can_view_insights', 'can_create_insights', 'can_view_dashboards'],
  'admin': ['all_permissions']
}

# Assign users to roles via SSO groups
SSO_GROUP_MAPPING = {
  'okta_analytics_viewers': 'viewer',
  'okta_analytics_analysts': 'analyst',
  'okta_analytics_admins': 'admin'
}
```

**3. Data Retention Policy:**
```sql
-- Configure retention in ClickHouse
-- 90-day retention for GDPR compliance
ALTER TABLE events MODIFY TTL
  toDateTime(timestamp) + INTERVAL 90 DAY;

-- Custom retention for specific event types
ALTER TABLE events MODIFY TTL
  toDateTime(timestamp) + INTERVAL 365 DAY
  WHERE event = 'purchase_completed';
```

**4. Audit Logging:**
```python
# Enable audit logs
AUDIT_LOGGING = True
AUDIT_LOG_EVENTS = [
  'user_login',
  'data_export',
  'settings_changed',
  'user_added',
  'user_removed'
]
```

**Phase 3: Tracking Implementation (Week 3)**

**Multi-site tracking setup:**
```javascript
// Corporate website
posthog.init('PROJECT_TOKEN_CORPORATE', {
  api_host: 'https://analytics.yourcompany.com',
  autocapture: false,
  persistence: 'cookie'
})

// Product documentation
posthog.init('PROJECT_TOKEN_DOCS', {
  api_host: 'https://analytics.yourcompany.com',
  autocapture: false
})

// Regional sites
posthog.init('PROJECT_TOKEN_EU', {
  api_host: 'https://analytics.yourcompany.com',
  persistence_name: 'posthog_eu'
})
```

**GDPR-compliant tracking:**
```javascript
// Respect Do Not Track
if (navigator.doNotTrack === '1') {
  console.log('Tracking disabled per DNT');
} else {
  posthog.init('TOKEN', {
    respect_dnt: true,
    opt_out_capturing_by_default: false,
    // IP anonymization
    property_blacklist: ['$ip'],
    // Sanitize URLs (remove PII)
    sanitize_properties: function(properties) {
      if (properties.$current_url) {
        properties.$current_url = properties.$current_url
          .replace(/email=[^&]+/, 'email=REDACTED')
      }
      return properties
    }
  })
}
```

**Phase 4: Integration & Reporting (Week 4)**

**Data warehouse export:**
```python
# BigQuery export configuration
BIGQUERY_EXPORT = {
  'enabled': True,
  'project_id': 'your-gcp-project',
  'dataset': 'posthog_analytics',
  'table_prefix': 'events_',
  'export_interval': '1h'
}
```

**CRM integration (Salesforce):**
```javascript
// Send high-value events to Salesforce
posthog.capture('demo_requested', {
  company_name: 'Acme Corp',
  company_size: '500-1000',
  industry: 'Financial Services'
})

// Webhook to Salesforce
// Configure in PostHog UI: Webhooks → Add destination
```

**Total Setup Time: 3-4 weeks** (including testing, security review)

## Cost Analysis

### 1-Year Total Cost of Ownership

**PostHog Self-Hosted Enterprise**
- Infrastructure (AWS):
  - EKS cluster: $200/month
  - RDS PostgreSQL: $150/month
  - ClickHouse (3 nodes): $300/month
  - Redis: $50/month
  - Load balancer: $50/month
  - Total infra: $750/month × 12 = $9,000
- Enterprise license: $12,000-24,000/year (contact sales)
- Setup: 3 weeks × 40 hrs × $150/hr = $18,000
- Maintenance: 10 hrs/month × 12 × $150/hr = $18,000
- **Total Year 1: $57,000-69,000** (with time costs)
- **Total Year 1: $21,000-33,000** (cash only)

**Piwik PRO Enterprise**
- Subscription: $1,500/month × 12 = $18,000
- Setup (managed): 1 week × 40 hrs × $150/hr = $6,000
- Maintenance: Minimal (managed) = $0
- **Total Year 1: $24,000**

**Matomo Self-Hosted Premium**
- Infrastructure: $400/month × 12 = $4,800
- Premium plugins: $500/year (SSO, RBAC, etc.)
- Setup: 2 weeks × 40 hrs × $150/hr = $12,000
- Maintenance: 8 hrs/month × 12 × $150/hr = $14,400
- **Total Year 1: $31,700** (with time costs)
- **Total Year 1: $5,300** (cash only)

**Matomo Cloud Enterprise**
- Subscription: $2,000/month × 12 = $24,000
- Setup: 1 week × 40 hrs × $150/hr = $6,000
- Maintenance: Minimal (managed) = $0
- **Total Year 1: $30,000**

### 3-Year Total Cost of Ownership

| Provider | Year 1 | Year 2 | Year 3 | 3-Year Total | Notes |
|----------|--------|--------|--------|--------------|-------|
| PostHog Self-Hosted (cash) | $21-33K | $21-33K | $21-33K | **$63-99K** | Infrastructure + license |
| PostHog Self-Hosted (loaded) | $57-69K | $45-57K | $45-57K | **$147-183K** | Including DevOps time |
| Piwik PRO | $24K | $18K | $18K | **$60K** | Managed, all-inclusive |
| Matomo Self-Hosted (cash) | $5.3K | $5.3K | $5.3K | **$16K** | Cheapest option |
| Matomo Self-Hosted (loaded) | $31.7K | $19.2K | $19.2K | **$70K** | Including DevOps time |
| Matomo Cloud | $30K | $24K | $24K | **$78K** | Managed |

### Cost Optimization Strategies

**1. Open-Source Self-Hosted (Lowest Cash Cost)**
- Matomo Self-Hosted: $16K over 3 years (cash)
- Trade-off: High time cost ($70K loaded), DevOps burden
- Best for: Large enterprises with existing DevOps teams

**2. Managed Open-Source (Balance)**
- Piwik PRO: $60K over 3 years
- PostHog Cloud Enterprise: $72K+ over 3 years (estimated)
- Trade-off: Higher cash cost, zero time cost
- Best for: Enterprises wanting compliance without infrastructure burden

**3. Self-Hosted Enterprise (Best Control)**
- PostHog Self-Hosted: $63-99K over 3 years (cash)
- Trade-off: DevOps required, full control
- Best for: Technical enterprises, data sovereignty critical

## Decision Framework

### Choose PostHog Self-Hosted Enterprise if:
- ✅ Technical enterprise (DevOps capacity)
- ✅ Want modern product analytics
- ✅ Value open-source flexibility
- ✅ Need self-hosting for sovereignty
- ✅ Comfortable with infrastructure management
- ✅ Budget: $21-33K/year (cash) or $57-69K/year (loaded)

**Best for:** Tech companies, startups scaling to enterprise, modern analytics needs

### Choose Piwik PRO Enterprise if:
- ✅ Regulated industry (healthcare, finance, government)
- ✅ Need all compliance certifications (SOC2, ISO 27001, GDPR)
- ✅ Want white-labeling capability
- ✅ Prefer mature, established vendor
- ✅ Don't want to manage infrastructure
- ✅ Budget: $18-24K/year

**Best for:** Regulated industries, compliance-first organizations, want certainty

### Choose Matomo Self-Hosted if:
- ✅ Very budget-conscious ($5K/year cash)
- ✅ Have strong DevOps team
- ✅ Want lowest total cost
- ✅ Don't need latest features
- ✅ Comfortable with DIY support
- ✅ Budget: $5-32K/year depending on time cost

**Best for:** Large enterprises with DevOps, cost-sensitive, mature analytics needs

### Choose Matomo Cloud if:
- ✅ Want Matomo features without self-hosting
- ✅ GDPR compliance sufficient (EU hosting)
- ✅ Budget allows $24-30K/year
- ✅ Prefer managed service
- ✅ Data sovereignty partially acceptable (cloud EU region)

**Best for:** Mid-size enterprises, EU-focused, want managed Matomo

## Migration Path

### Phase 1: Pilot (Month 0-3)
**Approach:** Self-hosted PostHog or Matomo
- Deploy in isolated environment
- Test with one business unit
- Validate compliance requirements
- Prove technical feasibility
- **Decision point:** Self-host vs managed

### Phase 2: Limited Rollout (Month 3-6)
**Approach:** Expand to multiple properties
- Add 2-3 additional sites
- Integrate with SSO
- Configure RBAC
- Set up data retention policies
- **Decision point:** Scale infrastructure or migrate to managed

### Phase 3: Enterprise Rollout (Month 6-12)
**Approach:** Organization-wide deployment
- All web properties
- CRM/data warehouse integrations
- Executive dashboards
- Full team onboarding
- **Decision point:** Optimize costs, consider hybrid approach

### Phase 4: Optimization (Month 12+)
**Evaluate:**
- Cost efficiency: Self-hosted vs managed
- Feature needs: Stay with current or upgrade
- Compliance: Any new requirements
- Team satisfaction: Usability, support quality

**Migration triggers:**
- Compliance audit requires certified vendor → Piwik PRO
- Infrastructure burden too high → Migrate to managed
- Need advanced features → PostHog Enterprise upgrade
- Cost reduction → Matomo self-hosted

## Compliance Checklist

### GDPR Compliance

**Data Processing Agreement (DPA)**
- ✅ Piwik PRO: DPA included
- ✅ PostHog: DPA available (Enterprise)
- ✅ Matomo: DPA available (self-hosted or cloud)

**Right to Access**
- ✅ All providers: Export user data via API
- ✅ Configure: User data export automation

**Right to Erasure (Right to be Forgotten)**
- ✅ PostHog: Delete user data via API
- ✅ Piwik PRO: User deletion features
- ✅ Matomo: Anonymize or delete historical data

**Data Minimization**
- ✅ IP anonymization (all providers support)
- ✅ Disable unnecessary data collection
- ✅ Configure retention periods

**Consent Management**
- ✅ Integrate with OneTrust, Cookiebot, etc.
- ✅ Respect opt-out preferences
- ✅ Cookie-less mode where possible

### SOC2 Compliance

**Certified Providers:**
- ✅ Piwik PRO: SOC2 Type II certified
- ✅ PostHog Cloud: SOC2 Type II certified
- ⚠️ Self-hosted: Must certify your own deployment

**Requirements:**
- Access controls (RBAC) ✅
- Audit logging ✅
- Data encryption (in transit, at rest) ✅
- Incident response procedures ✅
- Vendor risk management ✅

### HIPAA Compliance

**If handling healthcare data:**
- Business Associate Agreement (BAA) required
- ✅ Piwik PRO: BAA available (contact sales)
- ⚠️ Self-hosted: Must configure for HIPAA yourself
- ❌ Most providers: No BAA on standard plans

**HIPAA considerations:**
- PHI must not be in analytics (anonymize)
- Encryption requirements (all traffic, all storage)
- Access logs and monitoring
- Self-hosted often easier for HIPAA compliance

## Real-World Example

### Case Study: Global Financial Services Firm

**Situation:**
- Company: Investment banking, 50,000 employees
- Websites: 12 regional marketing sites + corporate
- Traffic: 15M pageviews/month
- Markets: US, EU, APAC
- Requirements: SOC2, GDPR, no Google, data sovereignty

**Solution: Hybrid PostHog + Piwik PRO**

**Architecture:**
- **Piwik PRO (EU)**: EU marketing sites (GDPR-certified)
  - Cost: €2,500/month
  - Certified compliance for EU customers
  - Local data residency (Frankfurt)

- **PostHog Self-Hosted (US)**: US corporate + product sites
  - Cost: $800/month infrastructure + $15K/year license
  - Data stays in US AWS region
  - Advanced product analytics

**Why hybrid?**
- EU requires certified compliance → Piwik PRO (worth the cost)
- US can self-host → PostHog (better features, lower cost)
- Total: €2,500/month + $800/month = ~$3,500/month
- vs Single solution: $5,000/month for Piwik PRO globally

**Implementation:**
```javascript
// Geo-based routing
if (userRegion === 'EU') {
  // Piwik PRO (GDPR-certified)
  _paq.push(['trackPageView']);
} else if (userRegion === 'US') {
  // PostHog self-hosted
  posthog.capture('$pageview');
}
```

**Results:**
- Passed SOC2 audit (Piwik PRO + self-hosted documentation)
- GDPR compliant in all 27 EU countries
- 40% cost savings vs single global vendor
- Marketing team uses Piwik PRO (simple), product team uses PostHog (advanced)

**Key Learning:** Don't force one tool globally. Use best tool per region/requirement, even if it means managing two systems.

## Common Enterprise Mistakes

### Mistake 1: Assuming GA360 is Compliant
**Problem:** "We pay for GA360, so we're compliant"
**Reality:** GA360 still has GDPR issues, no self-hosting
**Solution:** Evaluate PostHog Enterprise or Piwik PRO

### Mistake 2: Underestimating Self-Hosting Costs
**Problem:** "Self-hosted is free after setup"
**Reality:** Maintenance, updates, monitoring, scaling = $15-30K/year in time
**Solution:** Calculate fully-loaded TCO (cash + time)

### Mistake 3: No Data Retention Policy
**Problem:** Storing analytics data indefinitely
**Reality:** GDPR requires data minimization, defined retention
**Solution:** Configure automated retention (30, 90, 365 days based on data type)

### Mistake 4: Ignoring Audit Logging
**Problem:** No record of who accessed what data
**Reality:** SOC2/HIPAA require audit trails
**Solution:** Enable audit logging from day one

### Mistake 5: Forgetting Data Sovereignty
**Problem:** Using US-hosted cloud for EU customer data
**Reality:** Schrems II ruling invalidates US hosting for EU data
**Solution:** Self-host in EU or use EU-certified vendor (Piwik PRO)

## Next Steps

1. **Assess compliance requirements:**
   - What regulations apply? (GDPR, SOC2, HIPAA, ISO 27001)
   - Data residency requirements? (EU, US, specific countries)
   - Certification deadlines? (upcoming audits)

2. **Calculate budget:**
   - Infrastructure capacity (can you self-host?)
   - Annual budget ($15K-$100K+ range)
   - Time budget (DevOps hours available)

3. **Choose approach:**
   - **Certified compliance needed** → Piwik PRO ($18-24K/year)
   - **Technical team + budget** → PostHog Enterprise Self-Hosted ($21-33K/year)
   - **Very budget-conscious + DevOps** → Matomo Self-Hosted ($5-16K/year)
   - **Want managed simplicity** → Matomo Cloud ($24-30K/year)

4. **Pilot program (Month 1-3):**
   - Deploy to test environment
   - Validate compliance requirements
   - Test SSO, RBAC, retention policies
   - Get security/legal review

5. **Rollout (Month 3-12):**
   - Phase 1: One business unit
   - Phase 2: Additional properties
   - Phase 3: Organization-wide
   - Phase 4: Optimization

## Related Use Cases

- **E-commerce Site**: If you need revenue tracking and attribution
- **Product-Led Growth SaaS**: If you need in-app analytics
- **High-Traffic Blog**: If you need scaled analytics for content sites
