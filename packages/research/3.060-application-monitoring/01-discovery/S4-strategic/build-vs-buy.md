# Build vs Buy: Error Tracking Economic Analysis

**Experiment**: 3.060-application-monitoring
**Phase**: S4 - Strategic Discovery
**Date**: 2025-10-08

## Executive Summary: Break-Even Analysis

| Solution | Year 1 Cost | Year 3 Cost | Break-Even Point | Recommendation |
|----------|-------------|-------------|------------------|----------------|
| **Sentry SaaS** | $6,000 - $24,000 | $18,000 - $72,000 | Baseline | SMB to Enterprise |
| **Self-Hosted Sentry** | $18,000 - $35,000 | $30,000 - $65,000 | > $2,000/month SaaS | Mid-market+ |
| **DIY Error Tracking** | $80,000 - $150,000 | $120,000 - $250,000 | > $5,000/month SaaS | Enterprise only |
| **Honeybadger** | $2,400 - $12,000 | $7,200 - $36,000 | Small teams | Bootstrapped/SMB |

**Key Insight**: Buy SaaS unless spending > $2,000/month (then self-hosted Sentry). Never DIY unless spending > $5,000/month or unique compliance requirements.

## Option 1: Buy SaaS (Sentry, Rollbar, Bugsnag, etc.)

### Sentry SaaS Pricing Model

**Team Plan** ($26/month):
- 50K errors/month, 1GB attachments
- Suitable for: Small startups (1-5 engineers)
- **Annual Cost**: $312

**Business Plan** ($80/month base + usage):
- 100K errors/month included, then $0.000045/error
- 10GB attachments, 90-day retention
- Suitable for: Growing startups (5-20 engineers)
- **Annual Cost**: $960 - $6,000 (depends on error volume)

**Enterprise Plan** (Custom pricing):
- Unlimited errors (soft limits), custom retention
- SSO, SLAs, dedicated support
- Suitable for: Mid-market to enterprise (20+ engineers)
- **Estimated Annual Cost**: $12,000 - $100,000+

**Typical Pricing Trajectory**:
- **Year 1** (10 engineers, 5 services): $3,000 - $12,000
- **Year 2** (20 engineers, 15 services): $8,000 - $30,000
- **Year 3** (30 engineers, 25 services): $15,000 - $60,000

### Honeybadger SaaS Pricing (Lower-Cost Alternative)

**Small Plan** ($49/month):
- 100K events/month, 10 projects
- Suitable for: Bootstrapped startups
- **Annual Cost**: $588

**Medium Plan** ($99/month):
- 500K events/month, 25 projects
- **Annual Cost**: $1,188

**Large Plan** ($249/month):
- 2M events/month, unlimited projects
- **Annual Cost**: $2,988

**Typical Pricing Trajectory**:
- **Year 1** (10 engineers): $600 - $2,400
- **Year 2** (20 engineers): $1,200 - $3,600
- **Year 3** (30 engineers): $2,400 - $7,200

### SaaS Total Cost of Ownership (3 Years)

**Sentry (Typical Mid-Market)**:
- Subscription: $18,000 - $72,000 (3 years cumulative)
- Integration/setup: $5,000 - $10,000 (Year 1 only)
- Training: $3,000 - $6,000 (Year 1, minimal ongoing)
- Operations: $0 (fully managed)
- **Total 3-Year TCO**: $26,000 - $88,000

**Honeybadger (Typical SMB)**:
- Subscription: $7,200 - $36,000 (3 years)
- Integration/setup: $3,000 - $6,000
- Training: $2,000 - $4,000
- Operations: $0
- **Total 3-Year TCO**: $12,200 - $46,000

## Option 2: Self-Hosted Sentry (Open-Source)

### Infrastructure Costs

**Cloud Infrastructure** (AWS/GCP/Azure):
- **Small** (< 1M events/month): $300-500/month
  - 2x t3.large (app servers): $150/month
  - RDS PostgreSQL (db.t3.medium): $100/month
  - ElastiCache Redis (cache.t3.medium): $50/month
  - S3 storage: $20-50/month
  - Load balancer: $20/month
  - Data transfer: $30-50/month

- **Medium** (1-5M events/month): $800-1,200/month
  - 4x t3.xlarge (app servers): $500/month
  - RDS PostgreSQL (db.r5.xlarge): $400/month
  - ElastiCache Redis (cache.r5.large): $150/month
  - S3 storage: $100-200/month
  - Load balancer + data transfer: $100-150/month

- **Large** (5M+ events/month): $2,000-4,000/month
  - 8x c5.2xlarge (app servers): $1,500/month
  - RDS PostgreSQL (db.r5.4xlarge): $1,500/month
  - ElastiCache Redis cluster: $400/month
  - S3 storage: $300-500/month
  - Load balancer + CDN + data transfer: $300-500/month

### Engineering Costs

**Initial Setup** (40-80 hours):
- Infrastructure as code (Terraform/CloudFormation): 20-30h
- Docker/Kubernetes deployment: 15-25h
- Database setup, migrations: 10-15h
- SSL, authentication, networking: 10-15h
- Monitoring, logging, alerting: 10-20h
- **Cost**: $4,000 - $8,000 (at $100/hr)

**Ongoing Operations** (2-5 hours/month):
- Version upgrades: 1-2h/month
- Scaling adjustments: 0.5-1h/month
- Security patching: 0.5-1h/month
- Incident response: 0.5-2h/month (variable)
- Monitoring/optimization: 0.5-1h/month
- **Cost**: $200 - $500/month ($2,400 - $6,000/year)

### Self-Hosted Sentry Total Cost of Ownership (3 Years)

**Small Deployment** (< 1M events/month):
- Infrastructure: $10,800 - $18,000 (3 years)
- Initial setup: $4,000 - $8,000
- Operations: $7,200 - $18,000 (3 years)
- Backup/DR: $1,000 - $3,000 (3 years)
- **Total 3-Year TCO**: $23,000 - $47,000

**Medium Deployment** (1-5M events/month):
- Infrastructure: $28,800 - $43,200
- Initial setup: $6,000 - $10,000
- Operations: $10,800 - $21,600
- Backup/DR: $3,000 - $6,000
- **Total 3-Year TCO**: $48,600 - $80,800

**Large Deployment** (5M+ events/month):
- Infrastructure: $72,000 - $144,000
- Initial setup: $8,000 - $12,000
- Operations: $14,400 - $28,800
- Backup/DR: $6,000 - $12,000
- **Total 3-Year TCO**: $100,400 - $196,800

### Self-Hosted Break-Even Analysis

**When self-hosted makes sense**:
- Sentry SaaS > $500-1,000/month → Consider self-hosted small
- Sentry SaaS > $2,000/month → Self-hosted likely cheaper (medium deployment)
- Sentry SaaS > $5,000/month → Self-hosted definitely cheaper (large deployment)

**Example Break-Even Calculation**:
- Sentry Business Plan: ~$2,500/month ($30,000/year)
- Self-hosted medium: ~$1,600/month ($19,200/year)
- **Savings**: ~$10,800/year (~36% cost reduction)
- **Break-even**: Month 4-6 (after initial setup amortized)

## Option 3: DIY Error Tracking (Build from Scratch)

### Engineering Effort Estimate

**Year 1: MVP Development** (800-1,200 hours):
1. **Error Ingestion API** (120-180h):
   - REST/gRPC endpoints for error submission
   - Rate limiting, authentication, validation
   - Multi-language SDK scaffolding

2. **Data Storage & Indexing** (150-250h):
   - PostgreSQL schema design
   - Elasticsearch indexing for search
   - Time-series optimization
   - Retention policies

3. **Error Grouping & Fingerprinting** (200-300h):
   - Stack trace parsing and normalization
   - Intelligent error grouping algorithms
   - Duplicate detection
   - Fingerprint stability across versions

4. **Web UI** (250-350h):
   - Error list views, search, filtering
   - Error detail pages with stack traces
   - Source code context display
   - User authentication and authorization

5. **Alerting & Notifications** (100-150h):
   - Alert rule engine
   - Slack, email, PagerDuty integrations
   - Alert throttling and deduplication

6. **SDK Development** (150-200h):
   - JavaScript SDK
   - Python SDK
   - Ruby/Rails SDK
   - Basic instrumentation

7. **Infrastructure & Operations** (80-120h):
   - Deployment automation
   - Monitoring and logging
   - Backup and disaster recovery
   - Security hardening

**Year 1 Total**: 1,050-1,550 hours

**Year 1 Cost**: $105,000 - $155,000 (at $100/hr fully-loaded engineer cost)

### Ongoing Maintenance & Feature Development

**Year 2-3: Maintenance & Enhancements** (400-600 hours/year):
- Bug fixes and stability: 100-150h/year
- Performance optimization: 80-120h/year
- Security updates: 60-90h/year
- New SDK support: 80-120h/year
- Feature additions: 80-120h/year

**Year 2-3 Cost**: $40,000 - $60,000/year

### DIY Total Cost of Ownership (3 Years)

**Engineering Costs**:
- Year 1 (MVP): $105,000 - $155,000
- Year 2 (maintenance): $40,000 - $60,000
- Year 3 (maintenance): $40,000 - $60,000
- **Total**: $185,000 - $275,000

**Infrastructure Costs** (same as self-hosted Sentry):
- Year 1: $3,600 - $14,400
- Year 2: $3,600 - $14,400
- Year 3: $3,600 - $14,400
- **Total**: $10,800 - $43,200

**Operations Costs** (dedicated DevOps attention):
- Year 1: $8,000 - $12,000
- Year 2: $6,000 - $10,000
- Year 3: $6,000 - $10,000
- **Total**: $20,000 - $32,000

**DIY 3-Year TCO**: $215,800 - $350,200

### DIY Break-Even Analysis

**When DIY makes sense**:
- Sentry SaaS > $6,000/month ($72,000/year) → DIY possibly justifiable
- Unique compliance requirements (data sovereignty, airgap environments)
- Massive scale (> 50M events/month) with specialized needs

**Example Break-Even Calculation**:
- Sentry Enterprise: ~$8,000/month ($96,000/year, $288,000 over 3 years)
- DIY: ~$250,000 over 3 years (mid-range estimate)
- **Savings**: $38,000 over 3 years (~13% savings)
- **Break-even**: Year 2.5 (marginal savings, high risk)

**Why DIY Usually Doesn't Make Sense**:
- Feature parity takes 3-5 years (Sentry has 10+ years of development)
- Opportunity cost (engineers could build product features)
- Compounding feature gap (Sentry adds features faster than DIY can catch up)
- No economies of scale (Sentry amortizes costs across 100K+ customers)

## Decision Matrix: Build vs Buy

### Choose SaaS (Sentry, Honeybadger) If:
- Team < 50 engineers
- Spending < $2,000/month on error tracking
- Want rapid deployment (days, not months)
- Prefer vendor-managed operations
- Need latest features without engineering investment
- Value ecosystem integrations (Jira, Slack, etc.)

**Best Providers**:
- **Sentry**: Feature-rich, multi-language, open-source escape hatch
- **Honeybadger**: Lower cost, indie stability, Ruby/Elixir strength

### Choose Self-Hosted Sentry If:
- Spending $2,000-5,000/month on SaaS error tracking
- Have DevOps capacity for operations (2-5h/month)
- Data sovereignty requirements (regional compliance)
- Want cost control at scale (> 5M events/month)
- Prefer open-source transparency
- Willing to accept maintenance burden for cost savings

**Estimated Savings**: 30-50% vs. Sentry SaaS at scale

### Choose DIY If (Rarely):
- Spending > $6,000/month on SaaS ($72K+/year)
- Unique requirements impossible with commercial tools
- Airgap/classified environments (no internet access)
- Massive scale (> 100M events/month) with custom needs
- Multi-year engineering investment acceptable
- Opportunity cost of not building features is low

**Realistic Use Cases**:
- Government/defense contractors (compliance)
- Financial services (regulatory requirements)
- Tech giants with specialized needs (Facebook, Google scale)

## Hybrid Approach: Sentry Self-Hosted + Commercial Support

**Sentry Business Source License (BSL)**:
- Free self-hosted for < 10K users (generous limit)
- Commercial license for > 10K users (~$100K+/year)
- Professional support available ($50K-200K/year)

**Hybrid TCO** (3 years with commercial support):
- Infrastructure: $30,000 - $80,000
- Commercial license: $300,000 - $600,000 (if > 10K users)
- Professional support: $150,000 - $600,000
- Operations: $20,000 - $40,000
- **Total**: $500,000 - $1,320,000

**When hybrid makes sense**:
- Enterprise scale (> 100 engineers, > 10K users)
- Need self-hosted + vendor support
- Compliance requires on-prem with SLA backing
- Budget for $200K+/year software spend

## Strategic Recommendations

### For Startups (< 20 engineers):
**Choose**: Sentry SaaS (Team/Business plan) or Honeybadger
- **Cost**: $300 - $6,000/year
- **Rationale**: Fastest time-to-value, lowest ops burden

### For Mid-Market (20-100 engineers):
**Choose**: Sentry SaaS (Business/Enterprise) if < $2,000/month
**Choose**: Self-hosted Sentry if > $2,000/month
- **SaaS Cost**: $12,000 - $50,000/year
- **Self-hosted Cost**: $15,000 - $30,000/year
- **Rationale**: Break-even point makes self-hosted attractive

### For Enterprise (100+ engineers):
**Choose**: Self-hosted Sentry (community) if budget-conscious
**Choose**: Sentry Enterprise + commercial support if SLA-critical
**Avoid**: DIY unless unique compliance requirements
- **Self-hosted Cost**: $30,000 - $100,000/year
- **Enterprise SaaS**: $80,000 - $300,000/year
- **Rationale**: Scale economics favor self-hosted, unless SLA critical

### Never Choose DIY Unless:
1. Spending > $6,000/month on SaaS ($72K+/year)
2. Compliance requires airgap/classified environment
3. Unique requirements impossible with Sentry/alternatives
4. Engineering team idle (no better use of time)

**Bottom Line**: Buy SaaS for < $2,000/month. Self-host Sentry for $2,000-6,000/month (30-50% savings). Never DIY unless > $6,000/month or unique compliance. Honeybadger offers budget alternative for small teams.
