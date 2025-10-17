# Section 0: Open Standards Evaluation

**Experiment**: 3.063 Product Analytics
**Tier 2 Standard**: N/A (No open standard exists)
**Date**: October 17, 2025

---

## Does a Tier 2 Open Standard Exist?

❌ **NO** - No portable open standard for product analytics

**Why no standard exists**:

1. **Event model is proprietary**: Each platform defines its own event schema (user actions, properties, traits)
2. **Tracking SDK is vendor-specific**: Amplitude SDK, Mixpanel SDK, PostHog SDK - all different APIs
3. **Reporting API is proprietary**: Amplitude Analytics API, Mixpanel Insights API, PostHog query API
4. **Funnel/cohort models differ**: How platforms calculate funnels, retention, cohorts varies
5. **User identity model varies**: How users are tracked, merged, and de-duplicated is platform-specific

**Historical attempts**:
- **Segment**: Created abstraction layer (one SDK, send to multiple backends), but NOT a standard (vendor tool)
- **RudderStack**: Similar to Segment (abstraction, not standardization)
- **Common Event Format**: Proposed, never adopted industry-wide

**Result**: Product analytics is a **vendor lock-in category** with NO portability standard.

---

## Path 2 Viability Assessment

### Portability Level: ❌ **ZERO** (No standard exists)

**There is NO Path 2 (open standard) for product analytics.**

**Migration between platforms**:
- **Time**: 40-150 hours (reinstall SDK, migrate events, recreate funnels/cohorts/dashboards)
- **Method**: Remove old SDK, install new SDK, redefine events, rebuild reports
- **Code changes**: REQUIRED (different SDK APIs)
- **Event migration**: DIFFICULT (different event schemas, need transformation)
- **Historical data**: LOST (cannot export/import analytics data between platforms)
- **Funnels/cohorts**: RECREATE from scratch (platform-specific definitions)

**Lock-in risk**: **VERY HIGH** (every platform is a silo)

---

## Path 1 (DIY) vs Path 3 (Managed)

### Path 1: DIY Product Analytics (PostgreSQL + Custom Dashboards)

**What it is**: Store events in PostgreSQL/ClickHouse, build custom funnel/cohort queries, create dashboards

**Pros**:
- ✅ Full control (event schema, retention, privacy)
- ✅ Lowest cost ($0-200/month for database)
- ✅ No vendor lock-in (your database, your queries)
- ✅ Custom analysis (SQL queries, arbitrary funnels/cohorts)

**Cons**:
- ❌ Missing features (no automated retention, no A/B testing, no session replay)
- ❌ Manual work (write SQL for every analysis, build dashboards)
- ❌ No real-time reporting (batch queries)
- ❌ Complex queries (funnels, cohorts require advanced SQL)
- ❌ Time investment (80-200 hours to build)

**When to use**:
- Privacy-first (no third-party tracking, no data sharing)
- Custom analysis needs (arbitrary funnels, proprietary metrics)
- Budget = $0
- Technical team (strong SQL skills, can build dashboards)

**DIY product analytics stack**:
```
App → Custom event tracking → API → PostgreSQL/ClickHouse
                                            ↓
                                      Metabase/Superset (dashboards)
```

**Example SQL for retention cohort**:
```sql
-- Month-over-month retention
WITH cohorts AS (
  SELECT user_id, DATE_TRUNC('month', MIN(created_at)) AS cohort_month
  FROM events
  WHERE event_type = 'signup'
  GROUP BY user_id
),
user_activity AS (
  SELECT user_id, DATE_TRUNC('month', event_timestamp) AS activity_month
  FROM events
  WHERE event_type = 'active'
)
SELECT
  c.cohort_month,
  COUNT(DISTINCT c.user_id) AS cohort_size,
  COUNT(DISTINCT ua.user_id) AS active_users,
  100.0 * COUNT(DISTINCT ua.user_id) / COUNT(DISTINCT c.user_id) AS retention_rate
FROM cohorts c
LEFT JOIN user_activity ua ON c.user_id = ua.user_id
GROUP BY c.cohort_month, ua.activity_month
```

**Reality**: DIY product analytics is viable for simple tracking, but VERY time-intensive for advanced features (funnels, cohorts, retention).

---

### Path 3: Managed Product Analytics Platforms

**What it is**: Amplitude, Mixpanel, PostHog, Heap - turnkey product analytics services

**Pros**:
- ✅ Turnkey experience (install SDK, reports included)
- ✅ Advanced features (funnels, cohorts, retention, A/B testing, session replay)
- ✅ Real-time reporting
- ✅ No maintenance (managed service)
- ✅ User-friendly UI (non-technical users can create reports)

**Cons**:
- ❌ VERY HIGH lock-in (proprietary SDK, event model, reporting API)
- ❌ Migration = start over (lose historical data, recreate analysis)
- ❌ Cost ($0-2,000/month for small/mid-size, $10K-100K+/month at scale)
- ❌ Event-based pricing (unpredictable costs as usage grows)

**Provider comparison**:

### **PostHog**

**Cost**: $0-200/month (1M-10M events), scales beyond

**Pros**:
- ✅ Open source (self-hostable)
- ✅ Full-featured (analytics + session replay + feature flags + A/B testing)
- ✅ SQL query access (advanced users can write custom queries)
- ✅ Developer-friendly

**Cons**:
- ⚠️ Expensive at scale ($200/month for 10M events, $2K+ for 100M events)
- ⚠️ Lock-in (proprietary SDK, API, event model)
- ⚠️ Complexity (many features = steeper learning curve)

**Lock-in level**: **MEDIUM** (open source, can self-host, but proprietary API)

**When to use**: Need full product analytics + session replay + feature flags, okay with open source

---

### **Mixpanel**

**Cost**: $0-89/month (free tier: 20M events/month), $89/month (Growth plan)

**Pros**:
- ✅ Generous free tier (20M events/month)
- ✅ Full-featured (funnels, cohorts, retention, A/B testing)
- ✅ User-friendly UI
- ✅ Established (15+ years, mature product)

**Cons**:
- ⚠️ Lock-in (proprietary SDK, event model, Insights API)
- ⚠️ Cost at scale (Growth plan $89/month, Enterprise $2K+/month)
- ⚠️ No session replay (separate product, Mixpanel Sessions)

**Lock-in level**: **HIGH** (proprietary, cannot self-host)

**When to use**: Need product analytics, generous free tier acceptable

---

### **Amplitude**

**Cost**: $0-2,000/month (free tier: 10M events/month, Growth $50-2,000/month)

**Pros**:
- ✅ Full-featured (funnels, cohorts, retention, behavioral analytics)
- ✅ Advanced features (predictive analytics, recommendations)
- ✅ Free tier (10M events/month)
- ✅ Established (10+ years)

**Cons**:
- ⚠️ Lock-in (proprietary SDK, event model, Analytics API)
- ⚠️ Expensive at scale (Growth $50-2,000/month, Enterprise $10K+/month)
- ⚠️ No session replay (separate integrations needed)

**Lock-in level**: **HIGH** (proprietary, cannot self-host)

**When to use**: Need advanced behavioral analytics, free tier acceptable

---

### **Heap**

**Cost**: $0-3,600/month (free tier: 10K sessions/month, Growth $3,600/month)

**Pros**:
- ✅ Autocapture (tracks all events automatically, no manual instrumentation)
- ✅ Full-featured (funnels, cohorts, session replay)
- ✅ Retroactive analysis (define events after data collection)

**Cons**:
- ⚠️ Lock-in (proprietary SDK, autocapture model)
- ⚠️ Expensive (Growth $3,600/month, Enterprise $10K+/month)
- ⚠️ Autocapture overhead (tracks everything, high event volume)

**Lock-in level**: **VERY HIGH** (autocapture model is unique, migration extremely difficult)

**When to use**: Want autocapture (no manual instrumentation), have budget ($3,600+/month)

---

### **Matomo (Product Analytics Mode)**

**Cost**: $19-49/month (50K-1M actions), OR self-hosted (free)

**Pros**:
- ✅ Open source (self-hostable)
- ✅ Privacy-friendly (self-hosted = no data sharing)
- ✅ GDPR compliant
- ✅ Product analytics features (funnels, cohorts, heatmaps)

**Cons**:
- ⚠️ Less advanced than Amplitude/Mixpanel (simpler funnels, cohorts)
- ⚠️ Operational burden (self-hosted requires maintenance)
- ⚠️ Lock-in (proprietary API, migration difficult)

**Lock-in level**: **MEDIUM** (open source, but proprietary API)

**When to use**: Privacy-first, okay with self-hosting OR paying for managed

---

## Decision Framework

### Choose DIY Product Analytics (Path 1) if:

✅ **Privacy-first** (no third-party tracking, no data sharing)
✅ **Custom analysis needs** (arbitrary funnels, proprietary metrics)
✅ **Budget = $0-200/month** (can't afford managed platforms)
✅ **Technical team with strong SQL skills** (can write complex queries)
✅ **Okay with limited features** (no session replay, no automated retention)

**Recommended stack**:
- **Events**: Custom tracking → API → ClickHouse (fast analytics queries)
- **Dashboards**: Metabase or Superset (open source BI)
- **Funnels/cohorts**: Custom SQL queries

**Time investment**: 80-200 hours (event tracking + dashboards + SQL queries)

---

### Choose Open-Source Platform (PostHog, Matomo) if:

✅ **Want features but avoid lock-in** (self-hosting option)
✅ **Budget available** ($50-200/month self-hosted OR managed)
✅ **Privacy-first** (can self-host to control data)
✅ **Technical team** (can manage self-hosted deployment)

**Recommended**:
- **PostHog** ($0-200/month managed, OR self-hosted): Full-featured, modern, developer-friendly
- **Matomo** ($19-49/month managed, OR self-hosted): Privacy-focused, GDPR compliant

---

### Choose Managed Platform (Amplitude, Mixpanel, Heap) if:

✅ **Need advanced features** (funnels, cohorts, retention, A/B testing, session replay)
✅ **Want turnkey experience** (install SDK, reports included)
✅ **Non-technical users** (product managers need to create reports)
✅ **Budget available** ($0-2,000/month)
✅ **Accept lock-in** (migration = start over)

**Recommended by use case**:

**Generous free tier** (20M events/month):
- **Mixpanel** (free tier): Best free tier, full-featured

**Advanced behavioral analytics**:
- **Amplitude** ($0-2,000/month): Predictive analytics, recommendations

**Autocapture** (no manual instrumentation):
- **Heap** ($3,600+/month): Retroactive analysis, session replay

**All-in-one** (analytics + session replay + feature flags):
- **PostHog** ($0-200/month): Most comprehensive, open source

---

## Migration Scenarios

### Scenario 1: Amplitude → PostHog (Managed → Open Source)

**Motivation**: Reduce lock-in (can self-host), reduce costs

**Migration effort**: **60-150 hours**

**Steps**:
1. Install PostHog SDK (4-12 hours)
   - Replace Amplitude SDK with PostHog SDK in codebase
   - Map Amplitude events to PostHog events
2. Parallel tracking (2 weeks - send events to both platforms)
3. Recreate funnels in PostHog (20-40 hours)
   - Amplitude funnels → PostHog insights
4. Recreate cohorts in PostHog (20-40 hours)
5. Recreate dashboards in PostHog (20-40 hours)
6. Test thoroughly (8-16 hours)
7. Remove Amplitude SDK (2-4 hours)

**Challenges**:
- Historical data lost (cannot export/import between platforms)
- Event schema differences (need mapping)
- Funnel definitions vary (Amplitude vs PostHog)

**Cost change**: $0-2,000/month → $0-200/month (savings depend on event volume)
**When worth it**: Amplitude costs >$500/month, want self-hosting option

---

### Scenario 2: DIY Analytics → Mixpanel (DIY → Managed)

**Motivation**: Gain advanced features (funnels, cohorts, retention), reduce engineering burden

**Migration effort**: **40-80 hours**

**Steps**:
1. Install Mixpanel SDK (4-8 hours)
2. Migrate event tracking to Mixpanel (8-20 hours)
   - Map your custom events to Mixpanel event model
3. Import historical data (20-40 hours)
   - Use Mixpanel Import API (if needed)
   - Note: Limited historical import (only recent data)
4. Build funnels/cohorts in Mixpanel (8-12 hours)
5. Remove DIY tracking (2-4 hours)

**Challenges**:
- Historical data may not fully import (Mixpanel limits)
- Event schema mapping

**Cost change**: $0-200/month → $0-89/month (free tier OR Growth plan)
**When worth it**: Need advanced features, tired of writing SQL

---

### Scenario 3: Mixpanel → Amplitude (Platform → Platform)

**Motivation**: Want advanced behavioral analytics (predictive, recommendations)

**Migration effort**: **60-120 hours**

**Steps**:
1. Install Amplitude SDK (4-12 hours)
2. Parallel tracking (2 weeks)
3. Recreate funnels in Amplitude (20-40 hours)
4. Recreate cohorts in Amplitude (20-40 hours)
5. Recreate dashboards in Amplitude (20-40 hours)
6. Remove Mixpanel SDK (2-4 hours)

**Challenges**:
- Historical data lost
- Funnel/cohort definitions vary

**Cost change**: $0-89/month → $0-2,000/month (depends on event volume)
**When worth it**: Need Amplitude-specific features (predictive analytics)

---

## Cost Comparison (10M Events, 3 Years)

### Path 1: DIY Product Analytics (ClickHouse + Metabase)

**Cost**: $200/month (ClickHouse cluster + Metabase)
**Year 1**: $200 × 12 = $2,400
**Year 2**: $200 × 12 = $2,400
**Year 3**: $200 × 12 = $2,400
**Total**: **$7,200** (3 years)

**Operational cost**: ~20-40 hours/month (queries, dashboards, maintenance) = $6,000-12,000/month
**True TCO**: $7,200 + $216,000-432,000 = **$223,200-439,200** (3 years)

**Reality**: DIY is "cheap" only if you don't value engineering time.

---

### Path 3: PostHog (Open Source Managed)

**Cost**: $200/month (10M events)
**Year 1**: $200 × 12 = $2,400
**Year 2**: $200 × 12 = $2,400
**Year 3**: $200 × 12 = $2,400
**Total**: **$7,200** (3 years)

**Operational cost**: Near zero (managed)
**True TCO**: **$7,200** (3 years)

---

### Path 3: Mixpanel (Managed)

**Cost**: $0/month (free tier, 20M events/month covers 10M events)
**Year 1-3**: $0
**Total**: **$0** (3 years, assuming free tier)

**If exceeding free tier**: $89/month (Growth)
**Total**: $89 × 12 × 3 = **$3,204** (3 years)

**Operational cost**: Near zero (managed)
**True TCO**: **$0-3,204** (3 years)

---

### Path 3: Amplitude (Managed)

**Cost**: $0/month (free tier, 10M events/month)
**Year 1-3**: $0
**Total**: **$0** (3 years, assuming free tier)

**If exceeding free tier**: $50-2,000/month (Growth)
**Total**: $600-24,000/year = **$1,800-72,000** (3 years)

**Operational cost**: Near zero (managed)
**True TCO**: **$0-72,000** (3 years)

---

### Path 3: Heap (Managed)

**Cost**: $3,600/month (Growth plan)
**Year 1**: $3,600 × 12 = $43,200
**Year 2**: $3,600 × 12 = $43,200
**Year 3**: $3,600 × 12 = $43,200
**Total**: **$129,600** (3 years)

**Operational cost**: Near zero (managed)
**True TCO**: **$129,600** (3 years)

---

### Savings Analysis

**Mixpanel vs DIY**: $223,200-439,200 saved (when accounting for engineering time)
**PostHog vs DIY**: $216,000-432,000 saved (when accounting for engineering time)

**Key insight**: For product analytics, managed platforms are ALWAYS cheaper than DIY when factoring in engineering time.

---

## Recommendation

**Default choice**: Depends on budget and feature needs

### Startup (Budget = $0):
- **Choice**: Mixpanel (free tier, 20M events/month) OR Amplitude (free tier, 10M events/month)
- **Why**: Best free tiers, full-featured
- **Trade-off**: Lock-in (but acceptable for free)

### Small Business (Budget = $0-200/month, want flexibility):
- **Choice**: PostHog ($0-200/month)
- **Why**: Open source, can self-host later, full-featured (analytics + session replay + feature flags)
- **Trade-off**: Slightly more expensive than Mixpanel/Amplitude free tiers

### Mid-Size (Budget = $200-2,000/month, need advanced features):
- **Choice**: Amplitude ($50-2,000/month)
- **Why**: Advanced behavioral analytics, predictive features
- **Trade-off**: Expensive, lock-in

### Enterprise (Budget = $3,600+/month, need autocapture):
- **Choice**: Heap ($3,600+/month)
- **Why**: Autocapture (no manual instrumentation), retroactive analysis, session replay
- **Trade-off**: Very expensive, extreme lock-in

### Privacy-First (GDPR, no data sharing):
- **Choice**: Matomo self-hosted (free OR $19-49/month managed)
- **Why**: Self-hosted = full data control, GDPR compliant
- **Trade-off**: Less advanced than Amplitude/Mixpanel

---

## When to Avoid Managed Platforms

❌ **Absolute privacy requirement** (no third-party tracking, air-gapped)
- DIY product analytics (ClickHouse + custom SQL) is only option
- Accept feature limitations + engineering time investment

❌ **Extreme customization needs** (proprietary event model, custom metrics)
- DIY analytics with PostgreSQL/ClickHouse
- Build custom funnels/cohorts with SQL

❌ **Very limited budget** ($0) AND low event volume (<1M events/month)
- Free tiers (Mixpanel, Amplitude) are viable
- Accept lock-in for free features

---

## Integration with Other Standards

**Related Tier 2 standards**:
- **2.050 PostgreSQL**: Store product events (DIY approach)
- **2.040 OpenTelemetry**: Instrument product events (experimental)

**Related Tier 1 libraries**:
- None directly (product analytics is platform-specific)

**Related Tier 3 services**:
- This experiment (3.063) - Choose product analytics provider
- **3.062 Web Analytics**: Distinct from product analytics (pageviews vs user behavior)
- **3.060 Application Monitoring**: Distinct (system metrics vs user behavior)

---

## Key Takeaways

1. ❌ **No open standard exists** for product analytics (vendor lock-in by design)
2. ❌ **Migration = start over** (lose historical data, recreate funnels/cohorts/dashboards)
3. ✅ **Managed platforms cheaper than DIY** (when accounting for engineering time)
4. ✅ **Best free tiers**: Mixpanel (20M events/month), Amplitude (10M events/month)
5. ✅ **PostHog is unique**: Open source, full-featured (analytics + session replay + feature flags)
6. ⚠️ **Heap is most expensive** ($3,600+/month) but unique autocapture
7. ❌ **DIY viable only with strong SQL team** (complex queries for funnels/cohorts)

**Decision**: For most startups, use free tier (Mixpanel or Amplitude). For flexibility, use PostHog (open source). For enterprises, Amplitude (advanced) or Heap (autocapture).

**Specific choice**: Mixpanel (free tier, 20M events) for most use cases, PostHog ($0-200/month) if want open source option.
