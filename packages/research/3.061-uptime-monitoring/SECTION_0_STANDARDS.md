# Section 0: Open Standards Evaluation

**Experiment**: 3.061 Uptime Monitoring
**Tier 2 Standard**: N/A (No open standard exists)
**Date**: October 17, 2025

---

## Does a Tier 2 Open Standard Exist?

❌ **NO** - No portable open standard for uptime monitoring

**Why no standard exists**:

1. **Check configuration is proprietary**: Each platform defines checks differently (frequency, locations, timeouts, retry logic)
2. **Alert rules are vendor-specific**: How to define when to alert, who to alert, escalation policies vary
3. **Status page format is proprietary**: Public status pages have no standard format
4. **Historical data model differs**: How uptime percentage, downtime incidents are stored/calculated
5. **Multi-location checking**: How to distribute checks globally, aggregate results - no standard

**Partial standards that exist**:
- **HTTP/HTTPS**: Standard protocols for checking web services (but HOW to check is not standardized)
- **ICMP Ping**: Standard protocol for network reachability (but not sufficient for application monitoring)
- **Health check endpoints**: `/health`, `/status` common patterns, but NOT standardized

**Result**: Uptime monitoring is a **vendor lock-in category** with no portability standard.

---

## Path 2 Viability Assessment

### Portability Level: ❌ **ZERO** (No standard exists)

**There is NO Path 2 (open standard) for uptime monitoring.**

**Migration between platforms**:
- **Time**: 4-20 hours (reconfigure checks, recreate alert rules, update status page)
- **Method**: Manually recreate checks in new platform
- **Code changes**: MINIMAL (if using health check endpoints)
- **Historical data**: LOST (cannot export/import uptime history)
- **Alert rules**: RECREATE from scratch

**Lock-in risk**: **MEDIUM** (relatively easy to migrate, but historical data lost)

---

## Path 1 (DIY) vs Path 3 (Managed)

### Path 1: DIY Uptime Monitoring (Cron + Curl Scripts)

**What it is**: Write cron scripts to check URLs, send alerts on failure

**Pros**:
- ✅ Full control (check logic, alert rules, data retention)
- ✅ Lowest cost ($0-20/month for monitoring server)
- ✅ No vendor lock-in (your scripts, your server)
- ✅ Privacy-friendly (no third-party monitoring)

**Cons**:
- ❌ Single point of failure (if monitoring server goes down, checks stop)
- ❌ Missing features (no multi-location checks, no status page, no incident history)
- ❌ Manual work (write scripts, configure alerting)
- ❌ Limited alerting (email only, no SMS/Slack/PagerDuty)
- ❌ Time investment (8-40 hours to build)

**When to use**:
- Simple needs (check 1-5 URLs)
- Budget = $0
- Technical team (can write bash/Python scripts)
- Okay with limited features

**DIY uptime monitoring stack**:
```bash
#!/bin/bash
# Simple uptime check script (cron every 5 minutes)

URL="https://example.com"
RESPONSE=$(curl -o /dev/null -s -w "%{http_code}" $URL)

if [ "$RESPONSE" != "200" ]; then
  # Send alert (email, Slack webhook, etc.)
  echo "DOWN: $URL returned $RESPONSE" | mail -s "Alert: Site Down" admin@example.com
fi
```

**Limitations**:
- Single location (no global checks)
- No retry logic (false positives)
- No status page
- No historical data (unless you store it)

**Reality**: DIY uptime monitoring is viable for simple checks, but missing advanced features (multi-location, status page, incident tracking).

---

### Path 3: Managed Uptime Monitoring Services

**What it is**: UptimeRobot, Pingdom, Uptime.com, Better Uptime - turnkey monitoring services

**Pros**:
- ✅ Turnkey experience (configure checks via UI, alerts included)
- ✅ Multi-location checks (global distributed checks)
- ✅ Status pages (public/private status pages)
- ✅ Alert integrations (email, SMS, Slack, PagerDuty, webhooks)
- ✅ Incident history (uptime percentage, downtime tracking)
- ✅ No maintenance (managed service)

**Cons**:
- ⚠️ MEDIUM lock-in (check config proprietary, but easy to migrate)
- ⚠️ Cost ($0-100/month for small/mid-size)
- ⚠️ Historical data lost on migration

**Provider comparison**:

### **UptimeRobot**

**Cost**: $0-58/month (free tier: 50 checks @ 5-min interval, Pro $7/month: 50 checks @ 1-min)

**Pros**:
- ✅ Generous free tier (50 checks)
- ✅ Multi-location checks (13 locations)
- ✅ Status pages (public/private)
- ✅ Alert integrations (email, SMS, Slack, webhooks)
- ✅ Simple UI

**Cons**:
- ⚠️ Limited customization (check logic is basic)
- ⚠️ 5-minute intervals on free tier (1-minute on Pro)

**Lock-in level**: **LOW** (easy to migrate, standard HTTP checks)

**When to use**: Simple uptime monitoring, budget-conscious ($0-58/month)

---

### **Pingdom**

**Cost**: $15-110/month (Starter: 10 checks, Advanced: 50 checks)

**Pros**:
- ✅ Established (20+ years, mature product)
- ✅ Multi-location checks (100+ locations)
- ✅ Advanced checks (transaction monitoring, real browser checks)
- ✅ Detailed reporting (performance metrics, uptime trends)

**Cons**:
- ⚠️ Expensive (no free tier, $15/month minimum)
- ⚠️ Limited checks on lower tiers (10 checks on Starter)

**Lock-in level**: **LOW** (standard checks, easy to migrate)

**When to use**: Need advanced features (transaction monitoring), have budget ($15-110/month)

---

### **Better Uptime** (formerly Uptime.com)

**Cost**: $0-100/month (free tier: 10 checks @ 3-min, Team $42/month: 30 checks @ 1-min)

**Pros**:
- ✅ Free tier (10 checks)
- ✅ Status pages (beautiful, customizable)
- ✅ Incident management (timeline, post-mortems)
- ✅ On-call scheduling (built-in)
- ✅ Modern UI

**Cons**:
- ⚠️ Limited free tier (10 checks @ 3-min intervals)
- ⚠️ Cost scales quickly ($42/month for 30 checks)

**Lock-in level**: **LOW** (standard checks, easy to migrate)

**When to use**: Need status pages + incident management, have budget ($0-100/month)

---

### **Uptime.com** (legacy, now Better Uptime)

**Cost**: $0-350/month (free tier: 5 checks @ 1-min, Professional $60/month: 25 checks)

**Pros**:
- ✅ Multi-location checks (30+ locations)
- ✅ Advanced checks (API monitoring, SSL checks)
- ✅ Integrations (PagerDuty, Slack, webhooks)

**Cons**:
- ⚠️ Limited free tier (5 checks)
- ⚠️ Expensive ($60/month for 25 checks)

**Lock-in level**: **LOW** (standard checks)

**When to use**: Need advanced checks (API, SSL), have budget

---

### **Checkly**

**Cost**: $0-94/month (free tier: 5 checks @ 5-min, Team $94/month: 30 checks @ 1-min)

**Pros**:
- ✅ Developer-friendly (checks-as-code, Playwright support)
- ✅ API monitoring (REST API, GraphQL)
- ✅ Browser checks (real browser, JavaScript execution)
- ✅ Multi-location checks (20+ locations)

**Cons**:
- ⚠️ Expensive ($94/month for 30 checks)
- ⚠️ Limited free tier (5 checks @ 5-min)

**Lock-in level**: **MEDIUM** (checks-as-code proprietary)

**When to use**: Need browser checks (Playwright), API monitoring, developer-friendly

---

## Decision Framework

### Choose DIY Uptime Monitoring (Path 1) if:

✅ **Very simple needs** (check 1-5 URLs, basic HTTP checks)
✅ **Budget = $0**
✅ **Technical team** (can write bash/Python scripts)
✅ **Okay with single location** (no global distributed checks)
✅ **Okay with limited alerting** (email only, no SMS/Slack)

**Recommended stack**:
- **Simple**: Cron + curl + email alerts
- **Advanced**: Custom script + PostgreSQL (store history) + Grafana (dashboard)

**Time investment**: 8-40 hours

---

### Choose Free Tier Managed (UptimeRobot, Better Uptime) if:

✅ **Small scale** (10-50 checks)
✅ **Budget = $0** (free tier acceptable)
✅ **Want turnkey experience** (configure checks via UI)
✅ **Need multi-location checks** (global distributed)
✅ **Need status pages** (public/private)

**Recommended**:
- **UptimeRobot** (free: 50 checks @ 5-min): Best free tier
- **Better Uptime** (free: 10 checks @ 3-min): Status pages + incident management

---

### Choose Paid Managed (Pingdom, Better Uptime, Checkly) if:

✅ **Need advanced features** (transaction monitoring, browser checks, API monitoring)
✅ **Need faster checks** (1-minute intervals)
✅ **Need status pages** (customizable, branded)
✅ **Budget available** ($15-100/month)

**Recommended by use case**:

**Basic uptime** (HTTP checks, status pages):
- **UptimeRobot Pro** ($7/month): 50 checks @ 1-min, cheapest

**Advanced uptime** (transaction monitoring, performance):
- **Pingdom** ($15-110/month): Transaction monitoring, 100+ locations

**Developer-friendly** (browser checks, API monitoring):
- **Checkly** ($0-94/month): Playwright support, checks-as-code

**Status pages + incident management**:
- **Better Uptime** ($0-100/month): Beautiful status pages, on-call scheduling

---

## Migration Scenarios

### Scenario 1: DIY Cron → UptimeRobot (DIY → Managed)

**Motivation**: Gain multi-location checks, status pages, better alerting

**Migration effort**: **4-8 hours**

**Steps**:
1. Create UptimeRobot account (30 minutes)
2. Configure checks in UptimeRobot (2-4 hours)
   - Add URLs from cron scripts
   - Set check intervals (5-min free, 1-min Pro)
   - Configure alert contacts
3. Test alerts (1-2 hours)
4. Set up status page (1 hour)
5. Disable cron scripts (30 minutes)

**Cost change**: $0/month → $0-7/month (free or Pro)

**When worth it**: Need multi-location checks, status pages, better alerting

---

### Scenario 2: UptimeRobot → Better Uptime (Basic → Advanced)

**Motivation**: Better status pages, incident management, on-call scheduling

**Migration effort**: **4-12 hours**

**Steps**:
1. Create Better Uptime account (30 minutes)
2. Recreate checks in Better Uptime (2-4 hours)
   - Manually re-enter check URLs, intervals, timeouts
3. Configure alert rules (2-4 hours)
4. Set up status page (1-2 hours)
5. Configure on-call schedule (1-2 hours)
6. Parallel operation (1 week validation)
7. Cancel UptimeRobot (30 minutes)

**Challenges**:
- Historical data lost (cannot export from UptimeRobot)
- Check config needs manual recreation

**Cost change**: $0-7/month → $0-42/month

**When worth it**: Need better status pages, incident management

---

### Scenario 3: Pingdom → Checkly (Traditional → Developer-Friendly)

**Motivation**: Want checks-as-code, browser checks (Playwright)

**Migration effort**: **8-20 hours**

**Steps**:
1. Create Checkly account (30 minutes)
2. Write checks-as-code (4-12 hours)
   - Convert Pingdom checks to Checkly code format
   - Add browser checks (Playwright scripts)
3. Configure alert integrations (2-4 hours)
4. Test thoroughly (2-4 hours)
5. Cancel Pingdom

**Challenges**:
- Check format different (Pingdom UI → Checkly code)
- Browser checks need Playwright scripts

**Cost change**: $15-110/month → $0-94/month (depends on check count)

**When worth it**: Want checks-as-code, need browser checks

---

## Cost Comparison (50 Checks, 1-Minute Intervals, 3 Years)

### Path 1: DIY Cron Scripts

**Cost**: $20/month (monitoring server)
**Year 1**: $20 × 12 = $240
**Year 2**: $20 × 12 = $240
**Year 3**: $20 × 12 = $240
**Total**: **$720** (3 years)

**Operational cost**: ~2-5 hours/month maintenance = $600-1,500/month (if valued at $300/hour)
**True TCO**: $720 + $21,600-54,000 = **$22,320-54,720** (3 years)

**Reality**: DIY is "cheap" only if you don't value engineering time.

---

### Path 3: UptimeRobot Pro

**Cost**: $7/month (50 checks @ 1-min)
**Year 1**: $7 × 12 = $84
**Year 2**: $7 × 12 = $84
**Year 3**: $7 × 12 = $84
**Total**: **$252** (3 years)

**Operational cost**: Near zero (managed)
**True TCO**: **$252** (3 years)

---

### Path 3: Better Uptime Team

**Cost**: $42/month (30 checks @ 1-min)
**Note**: 50 checks would require higher tier ($79/month estimate)
**Year 1**: $79 × 12 = $948
**Year 2**: $79 × 12 = $948
**Year 3**: $79 × 12 = $948
**Total**: **$2,844** (3 years)

**Operational cost**: Near zero (managed)
**True TCO**: **$2,844** (3 years)

---

### Path 3: Pingdom Advanced

**Cost**: $110/month (50 checks @ 1-min)
**Year 1**: $110 × 12 = $1,320
**Year 2**: $110 × 12 = $1,320
**Year 3**: $110 × 12 = $1,320
**Total**: **$3,960** (3 years)

**Operational cost**: Near zero (managed)
**True TCO**: **$3,960** (3 years)

---

### Savings Analysis

**UptimeRobot vs DIY**: $22,068-54,468 saved (when accounting for engineering time)
**Better Uptime vs DIY**: $19,476-51,876 saved (when accounting for engineering time)

**Key insight**: For uptime monitoring, managed services are ALWAYS cheaper than DIY when factoring in engineering time.

---

## Recommendation

**Default choice**: Depends on check count and budget

### Startup (<10 Checks):
- **Choice**: UptimeRobot Free (50 checks @ 5-min) or Better Uptime Free (10 checks @ 3-min)
- **Why**: Free, multi-location, status pages
- **Trade-off**: 3-5 minute intervals (not 1-minute)

### Small Business (10-50 Checks, Need 1-Minute):
- **Choice**: UptimeRobot Pro ($7/month, 50 checks @ 1-min)
- **Why**: Cheapest 1-minute monitoring ($7/month)
- **Trade-off**: Basic features (no advanced transaction monitoring)

### Mid-Size (50+ Checks, Need Advanced):
- **Choice**: Better Uptime ($42-100/month) or Pingdom ($110/month)
- **Why**: Status pages, incident management, transaction monitoring
- **Trade-off**: More expensive

### Developer-Focused (Need Browser Checks, API Monitoring):
- **Choice**: Checkly ($0-94/month)
- **Why**: Checks-as-code, Playwright support, developer-friendly
- **Trade-off**: More expensive, steeper learning curve

### DIY (Budget = $0, <5 Checks):
- **Choice**: Cron + curl scripts
- **Why**: Zero cost
- **Trade-off**: Single location, limited alerting, high engineering time

---

## When to Avoid Managed Platforms

❌ **Very simple needs** (<5 checks, single URL)
- DIY cron script may suffice
- Managed platform is overkill

❌ **Absolute privacy requirement** (no third-party monitoring)
- DIY monitoring from your own server
- Accept feature limitations

❌ **Need custom check logic** (proprietary health checks)
- DIY scripts with custom logic
- Managed platforms have limited customization

---

## Integration with Other Standards

**Related Tier 2 standards**:
- **2.050 PostgreSQL**: Store uptime history (DIY approach)
- **2.040 OpenTelemetry**: Instrument uptime metrics (experimental)
- **2.041 Prometheus**: Blackbox Exporter for Prometheus-based uptime monitoring (DIY)

**Related Tier 1 libraries**:
- None directly (uptime monitoring is HTTP-based, no special libraries)

**Related Tier 3 services**:
- This experiment (3.061) - Choose uptime monitoring provider
- **3.060 Application Monitoring**: Complement uptime (system metrics + synthetic checks)
- **3.010 WAF/Security**: Protect endpoints that uptime monitors check

---

## Key Takeaways

1. ❌ **No open standard exists** for uptime monitoring (vendor lock-in by design, but LOW lock-in in practice)
2. ⚠️ **Migration is easy** (4-20 hours), but historical data lost
3. ✅ **Managed platforms cheaper than DIY** (when accounting for engineering time)
4. ✅ **Best free tier**: UptimeRobot (50 checks @ 5-min)
5. ✅ **Cheapest 1-minute**: UptimeRobot Pro ($7/month, 50 checks)
6. ⚠️ **Better Uptime best for status pages** ($0-100/month)
7. ⚠️ **Checkly best for developers** (checks-as-code, Playwright)
8. ❌ **DIY viable only for very simple needs** (<5 checks, budget = $0)

**Decision**: For most businesses, use managed platform (UptimeRobot for budget, Better Uptime for status pages, Checkly for developers). DIY only if very simple needs or absolute privacy requirement.

**Specific choice**: UptimeRobot Pro ($7/month) for most use cases, Better Uptime ($0-100/month) if need better status pages.
