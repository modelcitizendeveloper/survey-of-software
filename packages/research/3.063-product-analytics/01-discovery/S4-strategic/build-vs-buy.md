# Build vs. Buy Analysis: Product Analytics

## Executive Summary

Building a self-hosted product analytics solution costs $180K-$350K in Year 1 and $120K-$220K annually thereafter. Break-even occurs at 100M+ events/month or when data sovereignty requirements prohibit SaaS vendors. For most companies (<100M events/month), buying PostHog or Amplitude is 40-60% cheaper than building.

## Total Cost of Ownership (TCO): Build vs. Buy

### Year 1 Costs

| Cost Category | Build (Self-Host) | Buy (PostHog Cloud) | Buy (Amplitude) | Buy (Mixpanel) |
|---------------|-------------------|---------------------|-----------------|----------------|
| **Implementation** | $80K-$150K | $10K-$20K | $15K-$30K | $15K-$30K |
| **Infrastructure** | $24K-$60K | $0 | $0 | $0 |
| **Maintenance** | $40K-$80K | $0 | $0 | $0 |
| **Platform License** | $0 (open-source) | $20K-$50K | $40K-$80K | $40K-$80K |
| **Training** | $20K-$40K | $5K-$10K | $5K-$10K | $5K-$10K |
| **Opportunity Cost** | $15K-$20K | $5K-$8K | $5K-$8K | $5K-$8K |
| **Year 1 Total** | $179K-$350K | $40K-$88K | $70K-$128K | $70K-$128K |

### Year 3 Cumulative Costs

| Vendor/Approach | Year 1 | Year 2 | Year 3 | 3-Year Total | Notes |
|-----------------|--------|--------|--------|--------------|-------|
| **Build (Self-Host)** | $179K-$350K | $120K-$220K | $120K-$220K | $419K-$790K | Infrastructure + maintenance |
| **PostHog Cloud** | $40K-$88K | $25K-$60K | $30K-$75K | $95K-$223K | Usage-based pricing growth |
| **PostHog Self-Host** | $120K-$200K | $80K-$140K | $80K-$140K | $280K-$480K | Hybrid: OSS + infrastructure |
| **Amplitude** | $70K-$128K | $50K-$100K | $60K-$120K | $180K-$348K | Enterprise pricing |
| **Mixpanel** | $70K-$128K | $45K-$90K | $50K-$100K | $165K-$318K | Competitive pricing |

**Break-Even Analysis:**
- **Build breaks even at Year 3** if event volume >200M/month (vendor costs escalate with usage)
- **Build breaks even at Year 2** if data sovereignty requirements prohibit cloud vendors
- **Buy is cheaper** for 95% of companies (<100M events/month)

## Build Approach: Self-Hosted Analytics Stack

### Technology Stack (Open-Source)
**Event Collection & Storage:**
- **PostHog (self-hosted):** Complete analytics platform (MIT license, free)
- **Alternative:** ClickHouse + custom UI ($0 for software, higher engineering cost)

**Infrastructure:**
- **ClickHouse database:** Columnar analytics database (powers PostHog)
- **Kafka/Redis:** Event streaming and queueing
- **Kubernetes/Docker:** Container orchestration
- **S3/GCS:** Long-term event storage

**Infrastructure Costs (AWS/GCP):**
- **Small Scale (<10M events/month):** $2K-$5K/month = $24K-$60K/year
- **Medium Scale (10-100M events/month):** $5K-$12K/month = $60K-$144K/year
- **Large Scale (100M-1B events/month):** $12K-$30K/month = $144K-$360K/year

### Engineering Investment

**Year 1 Implementation (6-12 months):**
- **Setup & Configuration:** 200-400 hours
  - Deploy PostHog self-hosted on Kubernetes
  - Configure ClickHouse cluster (3-5 nodes)
  - Set up event ingestion pipeline (Kafka)
  - Implement monitoring and alerting (Datadog, Grafana)
  - Configure backups and disaster recovery

- **Customization & Integration:** 200-400 hours
  - Custom event schemas and tracking
  - Integration with data warehouse (Snowflake, BigQuery)
  - SSO and user management
  - Custom dashboards and visualizations
  - API integrations with internal tools

**Total Year 1 Engineering:** 400-800 hours × $200/hr = $80K-$160K

**Ongoing Maintenance (Year 2+):**
- **Infrastructure Management:** 10-20 hours/month
  - Database tuning and optimization
  - Scaling for traffic growth
  - Security patches and updates
  - Cost optimization

- **Feature Development:** 10-20 hours/month
  - Custom reports and dashboards
  - New event tracking requirements
  - Integration maintenance
  - User support and training

**Total Ongoing Maintenance:** 20-40 hours/month × $200/hr = $4K-$8K/month = $48K-$96K/year

### Open-Source Options

**Option 1: PostHog Self-Hosted (Recommended)**
- **License:** MIT (free, permissive)
- **Features:** Full product analytics, session replay, feature flags, A/B testing
- **Pros:** Battle-tested, active development, community support
- **Cons:** Still requires infrastructure management, not fully zero-cost

**Cost Breakdown:**
- Software: $0 (open-source)
- Infrastructure: $24K-$144K/year (depends on scale)
- Engineering: $80K-$160K Year 1, $48K-$96K/year ongoing
- **Total:** $104K-$304K Year 1, $72K-$240K/year ongoing

**Option 2: Custom ClickHouse + Metabase/Superset**
- **Components:**
  - ClickHouse: Event storage and analytics queries
  - Metabase or Superset: Dashboard and visualization layer
  - Custom SDKs: Event tracking libraries

- **Pros:** Maximum flexibility, optimized for specific use cases
- **Cons:** High engineering investment (800-1200 hours Year 1), no out-of-box features

**Cost Breakdown:**
- Software: $0 (all open-source)
- Infrastructure: $24K-$144K/year
- Engineering: $160K-$240K Year 1, $96K-$144K/year ongoing
- **Total:** $184K-$384K Year 1, $120K-$288K/year ongoing

**Option 3: Managed ClickHouse + Custom UI**
- **Components:**
  - ClickHouse Cloud (managed service)
  - Custom React/Vue dashboard
  - Event ingestion pipeline

- **Pros:** Reduces infrastructure management burden
- **Cons:** ClickHouse Cloud costs $0.04/GB ingested (can be expensive at scale)

**Cost Breakdown:**
- ClickHouse Cloud: $30K-$180K/year (depends on data volume)
- Custom UI development: $120K-$200K Year 1, $40K-$80K/year ongoing
- **Total:** $150K-$380K Year 1, $70K-$260K/year ongoing

## Buy Approach: SaaS Vendor Comparison

### PostHog Cloud (Usage-Based Pricing)
**Pricing Model:** $0.0001/event (events), $0.005/session (session replay), free tier
**Year 1 Costs (10M events/month):**
- Events: 10M × 12 × $0.0001 = $12K
- Session replay: 100K sessions × 12 × $0.005 = $6K
- Feature flags, A/B testing: Included
- **Total:** ~$20K-$30K (with feature flags and A/B testing usage)

**Scaling Costs:**
- 50M events/month: ~$60K/year
- 100M events/month: ~$120K/year (approaching build break-even)

**Pros:**
- Zero infrastructure management
- Instant setup (days, not months)
- All-in-one platform (analytics + flags + replay)
- Open-source foundation (can migrate to self-hosted)

**Cons:**
- Costs scale linearly with event volume
- Cloud-only concerns for regulated industries

### Amplitude (Contract-Based Pricing)
**Pricing Model:** Tiered contracts based on MTUs (Monthly Tracked Users)
**Year 1 Costs:**
- Growth Plan (10K MTUs): ~$40K-$60K/year
- Enterprise Plan (100K MTUs): ~$80K-$150K/year
- Plus Plan (1M+ MTUs): $200K-$500K+/year

**Pros:**
- Predictable annual costs
- Mature enterprise features (cohorts, behavioral analytics)
- Public company stability

**Cons:**
- Expensive at scale (10x PostHog for large event volumes)
- Contract lock-in (annual commitments)

### Mixpanel (MTU-Based Pricing)
**Pricing Model:** Tiered by MTUs
**Year 1 Costs:**
- Growth Plan (100K MTUs): ~$30K-$50K/year
- Enterprise Plan (1M MTUs): ~$100K-$200K/year

**Pros:**
- Competitive pricing vs. Amplitude
- Strong funnel and retention analytics

**Cons:**
- MTU-based pricing penalizes high-traffic/low-user products
- Moderate acquisition risk (Bain Capital exit pressure)

## Break-Even Analysis

### Scenario 1: Startup (1M events/month, 10K MTUs)
**Build Costs:** $179K-$350K Year 1, $120K-$220K/year ongoing
**Buy Costs (PostHog Cloud):** $2K-$5K/year
**Buy Costs (Amplitude):** $20K-$40K/year

**Recommendation:** Buy (PostHog Cloud) - 50-100x cheaper than building
**Break-Even:** Never (build is always more expensive at this scale)

### Scenario 2: Mid-Market SaaS (20M events/month, 100K MTUs)
**Build Costs:** $220K-$380K Year 1, $140K-$250K/year ongoing
**Buy Costs (PostHog Cloud):** $25K-$40K/year
**Buy Costs (Amplitude):** $80K-$120K/year

**Recommendation:** Buy (PostHog Cloud) - 5-10x cheaper
**Break-Even:** Never at this scale

### Scenario 3: High-Volume Product (100M events/month, 500K MTUs)
**Build Costs:** $280K-$450K Year 1, $180K-$300K/year ongoing
**Buy Costs (PostHog Cloud):** $120K-$180K/year (approaching parity)
**Buy Costs (Amplitude):** $200K-$400K/year

**Recommendation:** Build OR PostHog self-hosted hybrid (cost parity, but build offers more control)
**Break-Even:** Year 2-3 (build becomes cheaper in long term)

### Scenario 4: Enterprise (500M+ events/month, 2M+ MTUs)
**Build Costs:** $350K-$500K Year 1, $220K-$360K/year ongoing
**Buy Costs (PostHog Cloud):** $600K-$900K/year (build is cheaper)
**Buy Costs (Amplitude):** $500K-$1M+/year (build is cheaper)

**Recommendation:** Build (PostHog self-hosted) - 40-60% cost savings
**Break-Even:** Year 1 (build is immediately cheaper)

## When to Build

### Build Makes Sense If:
1. **Event volume >100M/month** (vendor costs exceed build costs)
2. **Data sovereignty requirements** (HIPAA, GDPR, financial services regulations prohibit SaaS)
3. **Unique analytics needs** (vendor features don't match use case)
4. **Strong engineering team** (5+ data engineers available)
5. **Long-term commitment** (3+ year horizon to amortize build costs)

### Build Does NOT Make Sense If:
1. **Event volume <50M/month** (vendor costs are 50-90% cheaper)
2. **Limited engineering resources** (<2 data engineers)
3. **Fast time-to-value needed** (build takes 6-12 months)
4. **Standard analytics use cases** (funnels, retention, cohorts)
5. **Short-term project** (<2 year horizon)

## Hybrid Approach: PostHog Self-Hosted

**Best of Both Worlds:**
- Use PostHog's open-source software (free, full-featured)
- Self-host on own infrastructure (data sovereignty)
- Avoid custom development (leverage PostHog's features)
- Optionally pay for PostHog support ($20K-$50K/year)

**Cost Comparison:**
- PostHog Self-Hosted: $120K-$250K Year 1, $80K-$180K/year ongoing
- Custom Build: $180K-$350K Year 1, $120K-$220K/year ongoing
- PostHog Cloud: $20K-$180K/year (depending on scale)

**Savings vs. Custom Build:** 30-40% cheaper (avoid custom development)
**Savings vs. Cloud at Scale:** 50-70% cheaper (at >100M events/month)

## Recommendation Matrix

| Company Profile | Event Volume | Recommendation | Rationale |
|-----------------|-------------|----------------|-----------|
| **Startup** | <10M/mo | PostHog Cloud | 50-100x cheaper than build |
| **Growth-Stage** | 10-50M/mo | PostHog Cloud or Amplitude | 5-20x cheaper than build |
| **Mid-Market** | 50-100M/mo | PostHog Cloud or Self-Hosted | Approaching break-even |
| **Enterprise** | 100-500M/mo | PostHog Self-Hosted | 40-60% cheaper than cloud |
| **Large Enterprise** | 500M+/mo | PostHog Self-Hosted or Custom | Build is 50-70% cheaper |
| **Regulated Industry** | Any | PostHog Self-Hosted | Data sovereignty required |

## Total Cost of Ownership (3-Year Summary)

| Approach | Year 1 | Year 2 | Year 3 | 3-Year Total | Cost/Million Events |
|----------|--------|--------|--------|--------------|---------------------|
| **Custom Build** | $180K-$350K | $120K-$220K | $120K-$220K | $420K-$790K | $1.17-$2.19/M |
| **PostHog Self-Host** | $120K-$250K | $80K-$180K | $80K-$180K | $280K-$610K | $0.78-$1.69/M |
| **PostHog Cloud (10M/mo)** | $20K-$30K | $25K-$40K | $30K-$50K | $75K-$120K | $0.21-$0.33/M |
| **PostHog Cloud (100M/mo)** | $120K-$180K | $130K-$200K | $140K-$220K | $390K-$600K | $0.11-$0.17/M |
| **Amplitude (100K MTUs)** | $80K-$120K | $90K-$130K | $100K-$140K | $270K-$390K | $0.75-$1.08/M |
| **Mixpanel (100K MTUs)** | $50K-$80K | $55K-$90K | $60K-$100K | $165K-$270K | $0.46-$0.75/M |

**Key Insight:** PostHog Cloud is cheapest for <100M events/month. PostHog Self-Hosted is cheapest for >100M events/month. Custom build rarely makes sense unless event volume >500M/month.

## Conclusion

**For 95% of Companies:** Buy (PostHog Cloud or Amplitude) is 40-90% cheaper than building, with faster time-to-value (days vs. months).

**For High-Volume or Regulated Companies:** Build using PostHog self-hosted (hybrid approach) achieves 40-60% cost savings vs. cloud vendors while avoiding custom development.

**Never Build Custom Unless:** Event volume >500M/month AND strong data engineering team (5+ engineers) AND long-term commitment (3+ years). Even then, PostHog self-hosted is often better than fully custom build.

**Strategic Recommendation:** Start with PostHog Cloud (low cost, fast setup), migrate to PostHog self-hosted if/when you hit 100M events/month. This avoids premature optimization while preserving optionality (open-source enables migration).
