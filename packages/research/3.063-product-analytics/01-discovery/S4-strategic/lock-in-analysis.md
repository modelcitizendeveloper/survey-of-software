# Vendor Lock-In and Migration Analysis: Product Analytics

## Executive Summary

Migration complexity for product analytics vendors ranges from 40 hours (simple event tracking) to 500+ hours (complex implementations with custom integrations). PostHog offers lowest lock-in risk (open-source, self-hosted option), while FullStory and Heap present highest complexity (proprietary session replay data formats).

## Migration Complexity Matrix

| Provider | Migration Hours | Data Export | API Quality | Lock-In Risk | Switching Cost |
|----------|----------------|-------------|-------------|--------------|----------------|
| **PostHog** | 40-80 hrs | Excellent (full self-host) | Excellent (open-source) | Very Low | $8K-$16K |
| **Amplitude** | 80-120 hrs | Good (REST API, raw data) | Good (documented) | Low | $16K-$24K |
| **Mixpanel** | 100-150 hrs | Moderate (rate limits) | Moderate | Moderate | $20K-$30K |
| **Pendo** | 120-180 hrs | Moderate (analytics only) | Moderate (guides locked) | Moderate-High | $24K-$36K |
| **Heap** | 150-250 hrs | Poor (autocapture proprietary) | Limited (Contentsquare) | High | $30K-$50K |
| **FullStory** | 200-300 hrs | Poor (session replay proprietary) | Limited | Very High | $40K-$60K |
| **LogRocket** | 150-250 hrs | Poor (session replay) | Limited | High | $30K-$50K |

**Assumptions:** Migration hours based on 10M events/month, 50 custom events, 20 integrations, 5 dashboards. Switching cost assumes $200/hr blended rate (engineering + analytics).

## Data Export Capabilities

### Tier 1: Excellent Portability
**PostHog**
- **Export Method:** Full database export (self-hosted), S3/GCS export (cloud)
- **Data Format:** ClickHouse SQL, JSON, CSV
- **Historical Data:** Unlimited (self-hosted owns all data)
- **Rate Limits:** None (self-hosted), generous (cloud)
- **Proprietary Lock-In:** Zero (MIT open-source license)
- **Migration Time:** 40-80 hours (re-implement event tracking, rebuild dashboards)

**Assessment:** Best-in-class portability. Self-hosted option means complete data ownership.

### Tier 2: Good Portability
**Amplitude**
- **Export Method:** Export API, Amazon S3 export, Snowflake integration
- **Data Format:** JSON, CSV
- **Historical Data:** Full export available (may require Enterprise plan)
- **Rate Limits:** Moderate (100K events/day for API, unlimited for S3 export)
- **Proprietary Lock-In:** Low (standard event schema)
- **Migration Time:** 80-120 hours (re-instrument events, rebuild cohorts/dashboards)

**Assessment:** Public company transparency ensures data access. Export API well-documented.

**Mixpanel**
- **Export Method:** Raw Data Export API, data pipelines
- **Data Format:** JSON, CSV
- **Historical Data:** Available (retention varies by plan)
- **Rate Limits:** Moderate (100 requests/hour for export API)
- **Proprietary Lock-In:** Low-Moderate (standard events, but cohort logic proprietary)
- **Migration Time:** 100-150 hours (re-instrument, rebuild funnels/retention charts)

**Assessment:** Mature export capabilities but rate limits can slow large migrations.

### Tier 3: Moderate Portability
**Pendo**
- **Export Method:** Analytics API, limited data export
- **Data Format:** JSON
- **Historical Data:** Analytics data available, in-app guide data locked
- **Rate Limits:** Restrictive (API throttling)
- **Proprietary Lock-In:** Moderate-High (product adoption features not portable)
- **Migration Time:** 120-180 hours (analytics portable, guides must be rebuilt)

**Assessment:** Analytics data exportable, but in-app guides and product adoption workflows are locked in.

### Tier 4: Poor Portability
**Heap (Contentsquare)**
- **Export Method:** Data Export API (limited), Snowflake Sync
- **Data Format:** JSON (autocapture schema proprietary)
- **Historical Data:** Available but autocapture data structure difficult to map
- **Rate Limits:** Restrictive
- **Proprietary Lock-In:** High (autocapture data model unique to Heap)
- **Migration Time:** 150-250 hours (must re-instrument events, can't replicate autocapture)

**Assessment:** Autocapture convenience creates migration complexity. Historical data hard to port.

**FullStory**
- **Export Method:** Data Export API, BigQuery export (Enterprise)
- **Data Format:** JSON (session replay proprietary)
- **Historical Data:** Event data exportable, session replays locked in proprietary format
- **Rate Limits:** Restrictive
- **Proprietary Lock-In:** Very High (session replay videos non-portable)
- **Migration Time:** 200-300 hours (session replay must be re-recorded, can't migrate historical)

**Assessment:** Session replay data is permanently locked. Event data exportable but replays lost.

**LogRocket**
- **Export Method:** API (limited), manual export
- **Data Format:** JSON (session replay proprietary)
- **Historical Data:** Event data exportable, session replays locked
- **Rate Limits:** Restrictive
- **Proprietary Lock-In:** Very High (session replay videos non-portable)
- **Migration Time:** 150-250 hours (similar to FullStory)

**Assessment:** Similar to FullStory - session replay creates permanent lock-in.

## API Compatibility and Alternative Integrations

### Industry Standards
**Segment Compatibility:** All major vendors integrate with Segment/mParticle
- Advantage: Can switch analytics vendors without re-instrumenting
- Limitation: Adds cost (~$10K-$120K/year for Segment)
- Migration Benefit: Switching from Amplitude → Mixpanel via Segment = 10-20 hours (just config)

**Snowflake/BigQuery Integration:**
- **PostHog:** Native ClickHouse, can export to data warehouse
- **Amplitude:** Direct Snowflake integration (enterprise)
- **Mixpanel:** Data warehouse export available
- **Pendo, Heap, FullStory, LogRocket:** Varying levels of support

**Benefit:** Data warehouse integration reduces lock-in - can query raw data directly.

### Event Tracking Standards
**Common SDKs:**
- Most vendors support JavaScript, iOS, Android, React Native, Flutter SDKs
- Event schemas are largely compatible (event name, properties, user ID, timestamp)
- Exception: Heap/FullStory autocapture has unique data model

**Migration Path:** Switch from manual event tracking vendor (Amplitude → Mixpanel) is easier than from autocapture (Heap → Amplitude) because autocapture logic must be re-implemented manually.

## Migration Complexity Breakdown

### Phase 1: Data Export (10-30% of total time)
**Tasks:**
- Export historical event data (API or bulk export)
- Export user profiles and cohorts
- Export dashboard configurations and queries
- Export integration configurations

**Complexity Factors:**
- API rate limits (can extend timeline from days to weeks)
- Data volume (10M events vs. 1B events)
- Historical retention (1 year vs. 5 years)

**Time Estimate:**
- **Low complexity (PostHog, Amplitude):** 10-20 hours
- **Medium complexity (Mixpanel, Pendo):** 20-40 hours
- **High complexity (Heap, FullStory):** 40-80 hours

### Phase 2: Re-Instrumentation (40-50% of total time)
**Tasks:**
- Update event tracking SDKs (swap libraries)
- Re-implement custom events (if schema differs)
- Rebuild autocapture logic (if migrating from Heap/FullStory)
- Test event firing and data accuracy

**Complexity Factors:**
- Number of platforms (web, iOS, Android, backend)
- Custom event volume (10 events vs. 500 events)
- Autocapture dependency (Heap/FullStory hardest to migrate from)
- Engineering team bandwidth

**Time Estimate:**
- **Low complexity (Amplitude → Mixpanel via Segment):** 10-20 hours
- **Medium complexity (Mixpanel → Amplitude, manual re-instrument):** 60-100 hours
- **High complexity (Heap → Amplitude, rebuild autocapture):** 120-200 hours

### Phase 3: Dashboard and Analysis Rebuild (20-30% of total time)
**Tasks:**
- Recreate key dashboards and reports
- Rebuild funnels, retention charts, cohorts
- Reconfigure alerts and notifications
- Train team on new platform

**Complexity Factors:**
- Dashboard count (5 dashboards vs. 50 dashboards)
- Custom metrics and calculations
- User permissions and access controls
- Organizational change management

**Time Estimate:**
- **Low complexity (few dashboards):** 20-40 hours
- **Medium complexity (standard analytics):** 40-80 hours
- **High complexity (extensive custom reporting):** 80-150 hours

### Phase 4: Integration and Workflow Migration (10-20% of total time)
**Tasks:**
- Reconnect downstream tools (data warehouse, BI, activation)
- Rebuild automated workflows and alerts
- Update documentation and runbooks
- Parallel run and validation

**Time Estimate:**
- **Low complexity (minimal integrations):** 10-20 hours
- **Medium complexity (10-20 integrations):** 20-40 hours
- **High complexity (complex workflows):** 40-80 hours

## Switching Cost Analysis

### Direct Costs
**Engineering Time:**
- Migration hours × blended rate ($150-$250/hr)
- Example: 150 hours × $200/hr = $30,000

**Data Export/Transfer:**
- API costs for bulk export (if usage-based pricing)
- Data transfer fees (egress from cloud providers)
- Estimate: $500-$5,000 depending on volume

**Parallel Running:**
- Overlap period where both vendors are active (1-3 months)
- Cost: 1-3 months of duplicate subscriptions (~$5K-$30K)

**Total Direct Costs:** $8K-$60K depending on vendor complexity

### Indirect Costs
**Opportunity Cost:**
- Engineering time diverted from product development
- Estimate: 2-6 weeks of engineering bandwidth

**Analysis Disruption:**
- Historical data discontinuity (before/after migration)
- Retraining analytics team on new platform
- Lost productivity during transition

**Risk Costs:**
- Data loss or corruption during migration
- Event tracking gaps during cutover
- Business decision delays due to incomplete analytics

**Total Indirect Costs:** 20-50% of direct costs (~$2K-$30K)

### Total Switching Costs by Vendor

| From Vendor | To PostHog | To Amplitude | To Mixpanel | Total Cost Range |
|-------------|------------|--------------|-------------|------------------|
| **PostHog** | N/A | $16K-$24K | $20K-$30K | $16K-$30K |
| **Amplitude** | $16K-$24K | N/A | $12K-$20K | $12K-$24K |
| **Mixpanel** | $20K-$30K | $16K-$24K | N/A | $16K-$30K |
| **Pendo** | $24K-$36K | $24K-$36K | $30K-$40K | $24K-$40K |
| **Heap** | $30K-$50K | $30K-$50K | $35K-$55K | $30K-$55K |
| **FullStory** | $40K-$60K | $40K-$60K | $45K-$65K | $40K-$65K |
| **LogRocket** | $30K-$50K | $30K-$50K | $35K-$55K | $30K-$55K |

**Key Insight:** Migrating FROM autocapture/session replay vendors (Heap, FullStory, LogRocket) is 2-3x more expensive than migrating between manual event tracking vendors (Amplitude ↔ Mixpanel).

## Lock-In Mitigation Strategies

### Strategy 1: Use Customer Data Platform (CDP)
**Implementation:**
- Route all events through Segment, mParticle, or RudderStack
- Configure analytics vendor as destination (not source)
- Switching vendors = change destination config (10-20 hours)

**Pros:**
- Dramatically reduces switching costs (80-90% reduction)
- Enables multi-vendor strategy (send to Amplitude + PostHog simultaneously)
- Single SDK to maintain

**Cons:**
- Adds $10K-$120K/year CDP cost
- Some vendor-specific features unavailable (autocapture, session replay)
- Additional latency in event delivery

**Best For:** Companies with >$500K/year analytics spend, frequent vendor evaluation needs

### Strategy 2: Data Warehouse as Source of Truth
**Implementation:**
- Export all events to Snowflake/BigQuery/Databricks
- Use reverse ETL or direct queries for analytics
- Analytics vendor supplements warehouse, not replaces

**Pros:**
- Complete data ownership and portability
- Vendor-agnostic analysis (SQL, Python, BI tools)
- Historical data preserved forever

**Cons:**
- Requires data engineering expertise
- Higher infrastructure costs
- Slower time-to-insight vs. dedicated analytics platform

**Best For:** Large enterprises, data-mature organizations, regulated industries

### Strategy 3: Multi-Vendor Strategy
**Implementation:**
- Primary vendor for production analytics (Amplitude, Mixpanel)
- Secondary vendor for specific use cases (PostHog for feature flags, LogRocket for session replay)
- Overlap creates migration optionality

**Pros:**
- Reduces single-vendor dependency
- Can gradually shift traffic from primary to secondary
- Competitive pressure keeps pricing in check

**Cons:**
- Higher total cost (2 subscriptions)
- Team must learn multiple platforms
- Data synchronization challenges

**Best For:** High-risk vendor situations (FullStory, LogRocket), hedge against acquisition

### Strategy 4: Open-Source Foundation
**Implementation:**
- Choose open-source vendor (PostHog) or self-hosted option
- Full control of infrastructure and data
- Can fork project if vendor direction changes

**Pros:**
- Zero lock-in risk (can self-host forever)
- No acquisition impact (community maintains open-source)
- Data sovereignty and compliance control

**Cons:**
- Self-hosting requires infrastructure expertise
- Cloud version still has vendor risk (though less than proprietary)
- May lack some enterprise features of proprietary vendors

**Best For:** Developer-centric organizations, data sovereignty requirements, long-term stability priority

## Vendor-Specific Migration Recommendations

### FROM Heap (High Lock-In Risk)
**Challenge:** Autocapture data model is proprietary, can't replicate in other tools
**Recommendation:**
1. Export event data to data warehouse (Snowflake integration)
2. Rebuild critical events manually in new vendor (can't port autocapture logic)
3. Accept historical data discontinuity for autocapture events
4. Budget 150-250 hours for migration
**Best Alternative:** PostHog (has autocapture) or Amplitude (manual events but robust)

### FROM FullStory/LogRocket (Very High Lock-In Risk)
**Challenge:** Session replay videos are proprietary, non-exportable
**Recommendation:**
1. Accept permanent loss of historical session replays
2. Export event data (separate from replays)
3. Start new session replay recording in target vendor
4. Consider decoupling: Amplitude (analytics) + separate session replay tool
5. Budget 200-300 hours for migration
**Best Alternative:** PostHog (includes session replay) or separate vendors

### FROM Mixpanel/Amplitude (Moderate Lock-In Risk)
**Challenge:** Proprietary cohort logic, dashboard configurations
**Recommendation:**
1. Use data warehouse integration for historical data preservation
2. Re-implement events in new SDK (100-150 hours)
3. Rebuild dashboards (funnels, retention easily replicated)
4. Consider Segment to reduce future switching costs
**Best Alternative:** Each other (Amplitude ↔ Mixpanel), or PostHog for cost savings

### FROM Pendo (Moderate-High Lock-In Risk)
**Challenge:** In-app guides and product adoption workflows locked in
**Recommendation:**
1. Export analytics data (available via API)
2. Rebuild in-app guides in new tool (Appcues, Chameleon, or PostHog feature flags)
3. Product adoption analytics must be recreated from scratch
4. Budget 120-180 hours
**Best Alternative:** Amplitude + separate in-app guidance tool, or PostHog

## Conclusion

**Lowest Lock-In Risk:** PostHog (open-source, self-hosted option) and Amplitude (good export API, standard event model)

**Highest Lock-In Risk:** FullStory and LogRocket (session replay videos non-portable), Heap (autocapture proprietary)

**Best Practice:** Use Segment/RudderStack CDP or data warehouse integration to reduce lock-in by 80-90%. Switching costs drop from $30K-$60K to $5K-$10K with proper abstraction layer.

**Strategic Recommendation:** For new implementations, choose PostHog (lowest lock-in) or Amplitude (good balance of features and portability). Avoid FullStory/LogRocket unless session replay is critical and you accept permanent lock-in.
