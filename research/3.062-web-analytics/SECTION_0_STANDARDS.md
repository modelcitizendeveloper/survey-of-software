# Section 0: Open Standards Evaluation

**Experiment**: 3.062 Web Analytics
**Tier 2 Standard**: N/A (No open standard exists)
**Date**: October 17, 2025

---

## Does a Tier 2 Open Standard Exist?

❌ **NO** - No portable open standard for web analytics

**Why no standard exists**:

1. **Event model is proprietary**: Each platform defines its own event schema (pageview, click, conversion)
2. **Tracking code is vendor-specific**: Google Analytics `gtag.js`, Plausible `script.js`, custom SDKs
3. **Reporting API is proprietary**: GA4 Data API, Plausible Events API, Matomo Analytics API
4. **Data formats differ**: Event payload structure, custom dimensions, user properties all vary
5. **Query language is proprietary**: GA4 uses custom query syntax, no PromQL equivalent

**Historical attempts at standardization**:
- **Google Analytics Measurement Protocol**: Attempted standard, but GA-specific (not adopted widely)
- **OpenWeb Analytics**: Open source, but not a standard (no interoperability)
- **Common Log Format (CLF)**: Server log format, but not analytics-specific (lacks event tracking)

**Result**: Web analytics is a **vendor lock-in category** by design.

---

## Path 2 Viability Assessment

### Portability Level: ❌ **ZERO** (No standard exists)

**There is NO Path 2 (open standard) for web analytics.**

**Migration between platforms**:
- **Time**: 20-120 hours (reinstall tracking, recreate dashboards, reconfigure goals)
- **Method**: Remove old tracking code, install new tracking code, rebuild reports
- **Code changes**: REQUIRED (different tracking SDKs)
- **Data migration**: NOT POSSIBLE (each platform stores data in proprietary format)
- **Historical data**: LOST (cannot export/import analytics data between platforms)

**Lock-in risk**: **HIGH** (every platform is a silo)

---

## Path 1 (DIY) vs Path 3 (Managed)

### Path 1: DIY Analytics (Server Logs or SQLite)

**What it is**: Parse server logs, store events in PostgreSQL/SQLite, build custom dashboards

**Pros**:
- ✅ Full control (event schema, retention, privacy)
- ✅ Lowest cost ($0 for storage + queries)
- ✅ No external tracking scripts (privacy-friendly, no cookie banners)
- ✅ No data sharing with third parties

**Cons**:
- ❌ Missing features (no conversion funnels, no cohort analysis, no A/B testing)
- ❌ Manual work (query writing, dashboard building, report generation)
- ❌ Limited insights (pageviews only, no click tracking, no heatmaps)
- ❌ No user identification (IP-based, not persistent across sessions)
- ❌ Time investment (40-120 hours to build)

**When to use**:
- Privacy-first (no third-party tracking)
- Simple needs (pageview counts, referrer tracking)
- Budget = $0
- Technical team (can write SQL, build dashboards)

**Implementation options**:

**1. Server log parsing** (simplest):
- Parse Nginx/Apache logs
- Extract: timestamp, path, referrer, user agent, IP
- Store in PostgreSQL or SQLite
- Query with SQL
- **Cost**: $0 (disk space only)
- **Effort**: 8-20 hours (log parser + SQL queries)

**2. Custom event tracking** (more advanced):
- Add JavaScript tracking code (send events to your API)
- Store events in PostgreSQL (timestamp, user_id, event_type, properties)
- Build dashboards with Grafana or Metabase
- **Cost**: $0-50/month (database + dashboard tool)
- **Effort**: 40-80 hours (tracking SDK + API + dashboards)

**DIY analytics stack**:
```
Browser → Custom JS tracker → Your API → PostgreSQL
                                              ↓
                                         Grafana/Metabase (dashboards)
```

**Reality**: DIY analytics is viable for basic tracking, but missing advanced features (funnels, cohorts, heatmaps).

---

### Path 3: Managed Analytics Platforms

**What it is**: Google Analytics, Plausible, Fathom, Matomo - managed services

**Pros**:
- ✅ Turnkey experience (install tracking code, dashboards included)
- ✅ Advanced features (conversion funnels, cohorts, A/B testing, heatmaps)
- ✅ Real-time reporting
- ✅ No maintenance (managed service)

**Cons**:
- ❌ HIGH lock-in (proprietary tracking, no data export, no query portability)
- ❌ Migration = start over (lose historical data, recreate dashboards)
- ❌ Privacy concerns (Google Analytics shares data with Google, GDPR issues)
- ❌ Cost (free to $200/month for privacy-focused, $0-$50K/month for full-featured)

**Provider comparison**:

### **Google Analytics 4 (GA4)**

**Cost**: Free (up to 10M events/month)

**Pros**:
- ✅ Free (for most sites)
- ✅ Full-featured (funnels, cohorts, attribution, BigQuery export)
- ✅ Integrates with Google Ads

**Cons**:
- ❌ Privacy concerns (data shared with Google)
- ❌ GDPR compliance (requires cookie banners, consent management)
- ❌ Complex UI (steep learning curve)
- ❌ Lock-in (proprietary query API, no data export beyond BigQuery)

**Lock-in level**: **VERY HIGH** (Google-specific API, no migration path)

**When to use**: Free tier acceptable, don't care about privacy, okay with Google data sharing

---

### **Plausible Analytics**

**Cost**: $9-49/month (10K-1M pageviews)

**Pros**:
- ✅ Privacy-friendly (no cookies, GDPR compliant, no Google data sharing)
- ✅ Simple UI (easy to use)
- ✅ Lightweight (< 1KB script)
- ✅ Open source (self-hostable)

**Cons**:
- ⚠️ Limited features (no funnels, no cohorts, basic dashboards)
- ⚠️ Lock-in (proprietary API, no data export)
- ⚠️ Cost scales with pageviews ($199/month for 10M pageviews)

**Lock-in level**: **MEDIUM-to-HIGH** (proprietary API, but can self-host)

**When to use**: Privacy-first, simple analytics needs, okay with limited features

---

### **Fathom Analytics**

**Cost**: $14-54/month (100K-10M pageviews)

**Pros**:
- ✅ Privacy-friendly (no cookies, GDPR compliant)
- ✅ Simple UI
- ✅ Lifetime data retention

**Cons**:
- ⚠️ Limited features (no funnels, no cohorts)
- ⚠️ Lock-in (proprietary API, no self-hosting)
- ⚠️ Cost scales with pageviews

**Lock-in level**: **HIGH** (proprietary, cannot self-host)

**When to use**: Privacy-first, willing to pay, okay with limited features

---

### **Matomo (formerly Piwik)**

**Cost**: $19-49/month (50K-1M actions), OR self-hosted (free)

**Pros**:
- ✅ Open source (self-hostable)
- ✅ Full-featured (funnels, cohorts, heatmaps, A/B testing)
- ✅ Privacy-friendly (self-hosted = no data sharing)
- ✅ GDPR compliant

**Cons**:
- ⚠️ Operational burden (self-hosted requires maintenance)
- ⚠️ Lock-in (proprietary API, migration difficult)
- ⚠️ Performance (heavy tracking script, ~20KB)

**Lock-in level**: **MEDIUM** (open source, but proprietary API)

**When to use**: Need full features, privacy-first, okay with self-hosting OR paying for managed

---

### **PostHog**

**Cost**: $0-200/month (1M-10M events), scales beyond

**Pros**:
- ✅ Full-featured (analytics + product analytics + session replay + feature flags)
- ✅ Open source (self-hostable)
- ✅ Developer-friendly (SQL queries, API access)

**Cons**:
- ⚠️ Expensive at scale ($200/month for 10M events, $2K/month for 100M)
- ⚠️ Lock-in (proprietary API, migration difficult)
- ⚠️ Complexity (many features = steeper learning curve)

**Lock-in level**: **MEDIUM** (open source, but proprietary API)

**When to use**: Need product analytics + web analytics combined, okay with cost

---

## Decision Framework

### Choose DIY Analytics (Path 1) if:

✅ **Privacy-first** (no third-party tracking, no data sharing)
✅ **Simple needs** (pageview counts, referrer tracking)
✅ **Budget = $0** (can't afford managed service)
✅ **Technical team** (can write SQL, build dashboards)
✅ **Okay with limited features** (no funnels, no cohorts, no heatmaps)

**Recommended stack**:
- **Simple**: Parse server logs → PostgreSQL → SQL queries
- **Advanced**: Custom JS tracker → PostgreSQL → Grafana dashboards

**Time investment**: 8-80 hours (log parsing to full custom analytics)

---

### Choose Privacy-Focused Analytics (Path 3) if:

✅ **Privacy-first** (GDPR compliant, no Google data sharing)
✅ **Simple needs** (pageviews, referrers, basic dashboards)
✅ **Budget available** ($9-200/month)
✅ **Want turnkey experience** (install script, dashboards included)

**Recommended providers**:
- **Plausible** ($9-49/month): Privacy-first, simple, lightweight
- **Fathom** ($14-54/month): Privacy-first, lifetime data retention
- **Matomo self-hosted** ($50-200/month): Full-featured, self-hosted, open source

---

### Choose Full-Featured Analytics (Path 3) if:

✅ **Need advanced features** (funnels, cohorts, A/B testing, heatmaps, session replay)
✅ **Willing to accept lock-in** (proprietary API, no migration path)
✅ **Budget available** ($0-2,000/month)

**Recommended providers**:
- **Google Analytics 4** (free): Full-featured, free, Google ecosystem
- **PostHog** ($0-2,000/month): Analytics + product analytics + feature flags
- **Matomo Cloud** ($19-49/month): Full-featured, managed, privacy-friendly

---

## Migration Scenarios

### Scenario 1: Google Analytics → Plausible (Full-Featured → Privacy-Focused)

**Motivation**: Improve privacy (GDPR compliance, remove Google tracking)

**Migration effort**: **20-40 hours**

**Steps**:
1. Install Plausible tracking code (1 hour)
2. Remove Google Analytics tracking code (1 hour)
3. Parallel operation (2 weeks - validate Plausible data accuracy)
4. Recreate key dashboards in Plausible (8-20 hours)
   - Note: Many GA4 features NOT available in Plausible (funnels, cohorts)
5. Update team workflows (4-8 hours)
6. Remove Google Analytics (1 hour)

**Challenges**:
- Historical data lost (cannot export GA4 data to Plausible)
- Missing features (funnels, cohorts not in Plausible)
- Dashboard recreation (Plausible dashboards are simpler)

**Cost change**: $0/month → $9-49/month
**When worth it**: Privacy requirements outweigh feature loss

---

### Scenario 2: Plausible → Google Analytics (Privacy → Full-Featured)

**Motivation**: Need advanced features (funnels, cohorts, attribution)

**Migration effort**: **12-24 hours**

**Steps**:
1. Install Google Analytics tracking code (1 hour)
2. Parallel operation (2 weeks)
3. Remove Plausible tracking code (1 hour)
4. Build GA4 dashboards (8-20 hours)
5. Cancel Plausible subscription

**Challenges**:
- Historical data lost
- Privacy loss (Google tracking, GDPR implications)

**Cost change**: $9-49/month → $0/month (but privacy trade-off)

---

### Scenario 3: DIY Analytics → PostHog (DIY → Full-Featured)

**Motivation**: Gain advanced features (funnels, session replay, feature flags)

**Migration effort**: **20-60 hours**

**Steps**:
1. Install PostHog tracking code (2-4 hours)
2. Migrate custom events to PostHog event model (8-20 hours)
   - Map your event schema to PostHog schema
3. Recreate dashboards in PostHog (8-20 hours)
4. Remove DIY tracking code (2-4 hours)
5. Decommission DIY analytics (2-4 hours)

**Challenges**:
- Historical data lost (cannot import into PostHog)
- Event schema mapping (your custom events → PostHog events)

**Cost change**: $0/month → $0-200/month (depending on event volume)
**When worth it**: Need advanced features, willing to pay

---

## Cost Comparison (1M Pageviews, 3 Years)

### Path 1: DIY Analytics (Server Logs)

**Cost**: $0/month (disk space only)
**Year 1-3**: $0
**Total**: **$0** (3 years)

**Operational cost**: ~5-10 hours/month maintenance = $1,500-3,000/month (if valued at $300/hour)
**True TCO**: $0 + $54,000-108,000 = **$54,000-108,000** (3 years)

**Reality**: DIY is "free" only if you don't value engineering time.

---

### Path 3: Plausible (Privacy-Focused)

**Cost**: $19/month (1M pageviews)
**Year 1**: $19 × 12 = $228
**Year 2**: $19 × 12 = $228
**Year 3**: $19 × 12 = $228
**Total**: **$684** (3 years)

**Operational cost**: Near zero (managed)
**True TCO**: **$684** (3 years)

---

### Path 3: Google Analytics 4 (Full-Featured)

**Cost**: $0/month (1M pageviews, free tier)
**Year 1-3**: $0
**Total**: **$0** (3 years)

**Operational cost**: Near zero (managed)
**True TCO**: **$0** (3 years)

**Trade-off**: Privacy (data shared with Google)

---

### Path 3: PostHog (Full-Featured)

**Cost**: $200/month (10M events ≈ 1M pageviews with event tracking)
**Year 1**: $200 × 12 = $2,400
**Year 2**: $200 × 12 = $2,400
**Year 3**: $200 × 12 = $2,400
**Total**: **$7,200** (3 years)

**Operational cost**: Near zero (managed)
**True TCO**: **$7,200** (3 years)

---

### Savings Analysis

**Plausible vs DIY**: $53,316-107,316 saved (when accounting for ops cost)
**Google Analytics vs DIY**: $54,000-108,000 saved (when accounting for ops cost)

**Key insight**: For web analytics, managed platforms are ALWAYS cheaper than DIY when factoring in engineering time.

---

## Recommendation

**Default choice**: Depends on privacy requirements and feature needs

### Privacy-First (GDPR, no Google):
- **Choice**: Plausible ($9-49/month) or Fathom ($14-54/month)
- **Why**: Privacy-friendly, no cookies, GDPR compliant, simple
- **Trade-off**: Limited features (no funnels, no cohorts)

### Full-Featured (Need funnels, cohorts, attribution):
- **Choice**: Google Analytics 4 (free) OR PostHog ($0-200/month)
- **Why**: Full features, turnkey experience
- **Trade-off**: Privacy (GA4) or cost (PostHog)

### DIY (Privacy + Budget = $0):
- **Choice**: Server log parsing → PostgreSQL → SQL queries
- **Why**: Zero cost, full privacy control
- **Trade-off**: Limited features, high engineering time

**Specific recommendation by use case**:

**Startup** (budget-conscious, privacy-aware):
- **Plausible** ($9/month): Privacy-friendly, simple, cheap

**Small Business** (need more features, okay with Google):
- **Google Analytics 4** (free): Full-featured, free

**Privacy-First Business** (GDPR required, need features):
- **Matomo Cloud** ($19-49/month): Full-featured, privacy-friendly, managed

**Product-Focused** (need product analytics + web analytics):
- **PostHog** ($0-200/month): Analytics + session replay + feature flags

---

## When to Avoid Managed Platforms

❌ **Absolute privacy requirement** (no third-party scripts, air-gapped)
- DIY server log parsing is only option
- Accept feature limitations

❌ **Very simple needs** (<1K pageviews, personal blog)
- Free self-hosted solutions (Matomo, PostHog) may be overkill
- Server log parsing may suffice

❌ **Need custom event schema** (proprietary event model)
- DIY analytics with PostgreSQL/ClickHouse
- Build custom tracking + dashboards

---

## Integration with Other Standards

**Related Tier 2 standards**:
- **2.050 PostgreSQL**: Store analytics events (DIY approach)
- **2.040 OpenTelemetry**: Instrument pageview tracking (experimental)

**Related Tier 1 libraries**:
- None directly (web analytics is platform-specific)

**Related Tier 3 services**:
- This experiment (3.062) - Choose web analytics provider
- **3.063 Product Analytics**: Distinct from web analytics (user behavior vs pageviews)
- **3.060 Application Monitoring**: Distinct (system metrics vs user behavior)

---

## Key Takeaways

1. ❌ **No open standard exists** for web analytics (vendor lock-in by design)
2. ❌ **Migration = start over** (lose historical data, recreate dashboards)
3. ✅ **Managed platforms are cheaper** than DIY (when accounting for engineering time)
4. ⚠️ **Privacy vs features trade-off**: Plausible (privacy, limited) vs GA4 (full-featured, Google)
5. ✅ **PostHog is unique**: Analytics + product analytics + feature flags (but expensive)
6. ⚠️ **DIY viable for simple needs**: Server log parsing → PostgreSQL → SQL
7. ❌ **Google Analytics is free** but privacy trade-off (data shared with Google)

**Decision**: For most businesses, use managed platform (Plausible for privacy, GA4 for features). DIY only if absolute privacy requirement or budget = $0.

**Specific choice**: Plausible ($9-49/month) for privacy, Google Analytics 4 (free) for features.
