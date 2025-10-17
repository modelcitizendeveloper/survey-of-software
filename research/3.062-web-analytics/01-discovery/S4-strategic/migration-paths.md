# Migration Paths Analysis
## Strategic Transitions Between Web Analytics Providers

**Created:** October 11, 2025
**Focus:** Migration strategies, cost quantification, timing triggers
**Scenarios:** From Google Analytics, between privacy alternatives, self-hosted transitions

---

## Core Migration Scenarios

### 1. From Google Analytics 4 (Cookie-Based → Privacy-First)
### 2. From VC-Backed Free Tier (PostHog, Mixpanel → Stable Alternative)
### 3. From Managed to Self-Hosted (Cost Optimization)
### 4. From Self-Hosted to Managed (Simplicity Optimization)
### 5. Between Privacy-First Providers (Fathom ↔ Plausible ↔ Simple Analytics)
### 6. From Basic to Advanced (Adding Funnels, Cohorts, Session Replay)

---

## Migration 1: From Google Analytics 4 → Privacy-First

### Why Migrate?

**Regulatory Risk (EU Customers)**
- GDPR court rulings: Austria (2022), France (2022), Italy (2023) declared GA4 illegal
- Data transfers to US disputed under Schrems II ruling
- Cookie consent requirements = 30-50% user opt-outs = missing data

**Brand Alignment**
- Developer tools, security products, privacy-focused companies
- GA4 = "privacy insensitive" perception in European markets
- Privacy-first analytics = trust signal, marketing advantage

**Script Performance**
- GA4: 45 KB script (page load impact, SEO penalty)
- Privacy-first: <2 KB scripts (Plausible <1 KB, Fathom 1.6 KB, Umami <2 KB)
- Core Web Vitals improvement: 43 KB savings

**Complexity Reduction**
- GA4: Complex UI, 200+ metrics, overwhelming for small teams
- Privacy-first: 10-15 core metrics, simple dashboard, 5-minute onboarding

### Migration Path: GA4 → Plausible

**Step 1: Pre-Migration (Week 0)**
- Export historical data from GA4 (BigQuery if GA360, limited otherwise)
- Document current dashboard usage: Which reports reviewed weekly/monthly?
- Identify critical metrics: Traffic sources, top pages, conversion goals
- List stakeholders needing analytics access (team accounts needed)

**Step 2: Parallel Tracking (Weeks 1-4)**
- Keep GA4 running (don't remove yet)
- Add Plausible script to website (single line in <head>):
  ```html
  <script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>
  ```
- Configure custom events (match GA4 goals):
  - GA4 "signup" event → Plausible `plausible('Signup')` custom event
  - GA4 "purchase" event → Plausible `plausible('Purchase')` custom event
- Run both tools in parallel for 2-4 weeks (validation period)

**Step 3: Validation (Week 4)**
- Compare data: GA4 vs. Plausible for same 7-day period
- Expected discrepancies:
  - Plausible traffic 100% vs. GA4 50-70% (cookie opt-outs in GA4)
  - Plausible counts all visitors; GA4 loses 30-50% post-consent
- Verify custom events firing correctly (check Plausible dashboard)
- Stakeholder review: "Can we make decisions with Plausible data alone?"

**Step 4: Switchover (Week 5)**
- Remove GA4 script from website
- Update privacy policy: Replace GA4 mention with Plausible
- Remove cookie consent banner (Plausible = cookie-less, GDPR-exempt)
- Archive GA4 property (don't delete immediately; keep 90-day backup)

**Step 5: Post-Migration (Week 6+)**
- Team training: 30-minute Plausible dashboard walkthrough
- Bookmark key views (top pages, traffic sources, custom events)
- Set up email reports (weekly traffic summary)
- Export CSV from Plausible monthly (backup, board reports)

### Migration Complexity: LOW (3-6 hours total)

**Time Breakdown:**
- Export GA4 historical data: 1-2 hours (BigQuery setup or manual export)
- Add Plausible script + custom events: 30 minutes
- Parallel tracking validation: 15 minutes/week × 4 weeks = 1 hour
- Remove GA4, update privacy policy: 30 minutes
- Team training: 30 minutes
- **Total: 3.5-4.5 hours**

**Cost Breakdown:**
- Engineering time: 4 hours × $160/hr = $640
- Plausible subscription: $19/mo (100K pageviews)
- GA4 removal saves: Cookie consent platform $50-200/mo (can remove)
- **Net Cost: $640 one-time - $600-2,400/year savings = Break-even in 3-12 months**

### Migration Complexity: MEDIUM (if GA360 BigQuery exports)

**Additional Steps:**
- BigQuery historical export: 5-10 hours (SQL queries, data transformation)
- Import into data warehouse (Snowflake, BigQuery, PostgreSQL): 3-5 hours
- BI tool integration (Looker, Tableau, Metabase): 2-4 hours
- **Total: 14-23 hours** (GA360 customers only)

### Recommended Targets

| From GA4 | Migrate To | Best For | Cost (100K pageviews) |
|----------|------------|----------|----------------------|
| GA4 (EU customers) | **Plausible** | GDPR compliance, brand alignment, simplicity | $19/mo |
| GA4 (EU customers, budget-conscious) | **Fathom** | Lowest cost privacy-first | $14/mo |
| GA4 (Need funnels) | **Plausible Business** | Privacy + advanced features | $69/mo |
| GA4 (Need product analytics) | **PostHog** (cookie-less mode) | Funnels, cohorts, session replay | $0-18/mo (1M events free) |
| GA4 (Enterprise, self-host) | **Matomo** | GA-like features, full control | $50-100/mo infra |

### Cookie-Less Future Implications

**Near-Term (2025-2026):**
- Chrome third-party cookie phase-out continues (Privacy Sandbox)
- First-party cookies survive BUT consent requirements increase (ePrivacy Directive)
- GA4 requires Consent Mode v2 (2024+) = more complex implementation

**Long-Term (2027-2030):**
- Cookie-less analytics becomes industry standard
- GDPR interpretations tighten (new court rulings)
- Privacy-first tools gain market share (currently 5-10% → projected 20-30%)

**Strategic Insight:** Migrating to cookie-less NOW = future-proof. GA4 compliance burden increases over time; privacy-first tools become simpler.

---

## Migration 2: From VC-Backed Free Tier → Stable Alternative

### Trigger: Acquisition Event (PostHog, Mixpanel, Amplitude)

**PostHog Acquisition Scenario (2026-2028 projected)**
- **Event:** Series C funding announcement OR "strategic partnership" PR OR executive departures
- **Timeline:** 3-6 months from acquisition announcement to integration changes
- **Customer Impact:** Free tier eliminated OR restricted (1M → 100K events), pricing increases 40-180% ($0 → $25-50/mo)
- **Forced Decision:** Pay new pricing OR migrate

**Mixpanel Acquisition Scenario (2025-2027 projected)**
- **Event:** Adobe, Salesforce, or ServiceNow acquisition announcement
- **Timeline:** 6-12 months from acquisition to free tier elimination
- **Customer Impact:** Free tier eliminated (20M events unsustainable), forced upgrade to Growth plan ($25 → $50-100/mo)
- **Forced Decision:** Pay $50-100/mo OR migrate (50-100 hour migration = $8,000-16,000 cost)

### Migration Path: PostHog Free Tier → PostHog Self-Hosted

**Why This Path:** Acquisition-proof (open-source MIT license guarantees community edition continues)

**Step 1: Pre-Migration (Week 0)**
- Export PostHog data (full event export via API or UI)
- Document feature usage: Session replay, feature flags, A/B tests in use?
- Provision infrastructure: AWS, DigitalOcean, Hetzner (4GB RAM, 2 vCPU minimum)
- Choose database: ClickHouse (default, best for scale) OR PostgreSQL (simpler)

**Step 2: Self-Hosted Setup (Week 1)**
- Deploy PostHog self-hosted (Docker Compose):
  ```bash
  git clone https://github.com/PostHog/posthog
  cd posthog
  docker-compose -f docker-compose.hobby.yml up -d
  ```
- Configure environment variables (`DATABASE_URL`, `SECRET_KEY`, `SITE_URL`)
- Import historical data (PostHog API: export from cloud, import to self-hosted)
- Test: Send test events, verify dashboard loading

**Step 3: Cutover (Week 2)**
- Update PostHog snippet in application (change `api_host` to self-hosted URL):
  ```javascript
  posthog.init('YOUR_PROJECT_TOKEN', {
    api_host: 'https://your-posthog-instance.com',
    autocapture: false // Optional: cookie-less mode
  })
  ```
- Monitor self-hosted instance (CPU, memory, disk usage)
- Deactivate PostHog cloud account (after 7-day verification period)

**Migration Complexity: MEDIUM (10-20 hours)**
- **Time Breakdown:**
  - Infrastructure provisioning: 2-3 hours (AWS/DO setup, DNS config)
  - PostHog self-hosted deployment: 3-5 hours (Docker, ClickHouse, troubleshooting)
  - Data export/import: 2-5 hours (API scripts, validation)
  - Application snippet update: 1 hour
  - Testing + monitoring setup: 2-4 hours
  - **Total: 10-18 hours**

**Cost Breakdown:**
- Engineering time: 15 hours × $160/hr = $2,400
- Infrastructure: $50-100/mo (DigitalOcean 8GB Droplet OR AWS t3.medium)
- **Ongoing: $50-100/mo vs. $25-50/mo PostHog cloud post-acquisition**
- **Break-even: 2-4 months** (self-host cheaper at scale)

### Migration Path: Mixpanel Free Tier → Plausible (Privacy-First Alternative)

**Why This Path:** Avoid HIGH lock-in cost (50-100 hours = $8,000-16,000), simplify to privacy-first

**Warning:** Mixpanel = product analytics (funnels, cohorts, user profiles). Plausible = web analytics (pageviews, sources, simple events). **Only migrate if product analytics NOT critical.**

**Step 1: Assess Feature Gap**
- Mixpanel features used: Funnels? Cohorts? Retention? User profiles?
- Plausible limitations: No cohorts, no retention, no user-level tracking
- **Decision Point:** Can you live with basic metrics (pageviews, custom events) OR need product analytics (choose PostHog self-hosted instead)?

**Step 2: If Proceeding (Web Analytics Sufficient)**
- Export Mixpanel data: CSV export via UI (limited) OR API (complex, event-by-event)
- Map Mixpanel events → Plausible custom events:
  - Mixpanel "Signup Completed" → Plausible `plausible('Signup')`
  - Mixpanel "Purchase" → Plausible `plausible('Purchase')`
- Note: Mixpanel user profiles, cohorts, funnels = NOT transferable (feature gap)

**Step 3: Parallel Tracking**
- Add Plausible script alongside Mixpanel (run both for 2-4 weeks)
- Verify custom events firing correctly
- Accept data loss: Mixpanel cohort analysis → manual spreadsheet analysis in Plausible

**Step 4: Switchover**
- Remove Mixpanel SDK from application
- Keep Plausible only
- Stakeholder communication: "We're simplifying to privacy-first analytics. Funnels/cohorts available if needed (upgrade to Plausible Business $69/mo OR PostHog)."

**Migration Complexity: HIGH (50-100 hours if preserving product analytics insights)**

**Why High?**
- Event schema translation: Mixpanel custom properties → Plausible simplified events = 10-20 hours
- Cohort recreation: Mixpanel automatic cohorts → manual CSV exports + spreadsheet analysis = 15-30 hours
- Funnel replacement: Mixpanel visual funnels → Plausible custom event tracking + manual calculation = 10-20 hours
- User profile loss: Mixpanel user-level data → Plausible anonymous aggregates = NOT recoverable
- **Total: 50-100 hours** (if attempting to preserve advanced analytics workflows)

**Alternative: HIGH complexity avoidance → Choose PostHog Self-Hosted instead**
- PostHog offers funnels, cohorts, retention (Mixpanel feature parity)
- Self-hosted = $50-100/mo (vs. Mixpanel post-acquisition $50-100/mo)
- Migration: Mixpanel → PostHog = 20-40 hours (event schema translation, but feature parity)

**Recommendation:** Mixpanel free tier users should migrate to **PostHog self-hosted** (10-20 hours, feature parity) NOT Plausible (50-100 hours, feature loss) UNLESS accepting web analytics downgrade.

---

## Migration 3: From Managed → Self-Hosted (Cost Optimization)

### Trigger: Traffic Growth (Managed Pricing Becomes Expensive)

**Break-Even Analysis:**
- Managed: Plausible $249/mo (10M pageviews) = $2,988/year
- Self-hosted: Umami on $50-100/mo infrastructure + 2 hrs/month maintenance = $600-1,200 infra + $3,840 labor (2 hrs × $160/hr × 12 months) = $4,440-5,040/year

**Insight:** Self-hosted NOT cheaper until maintenance optimized (<1 hr/month) OR infrastructure shared (existing PostgreSQL database).

**When Self-Hosting Makes Sense:**
1. **Data Sovereignty Requirement:** GDPR, HIPAA, government contracts mandate on-premise
2. **Existing Infrastructure:** Already running PostgreSQL/MySQL for main app (analytics = $0 incremental)
3. **Technical Team Available:** DevOps managing 10+ services (analytics = +1, minimal burden)
4. **Very High Traffic:** >10M pageviews where managed $500+/mo > self-hosted $50-100/mo + $160/mo maintenance

### Migration Path: Plausible Cloud → Plausible Self-Hosted

**Step 1: Export Plausible Data**
- API export (all pageviews, events, sources)
- CSV backup (manual export from UI)
- Time: 1-2 hours (API scripting)

**Step 2: Deploy Plausible Self-Hosted**
- **Prerequisites:** Docker, PostgreSQL database, ClickHouse (for high traffic)
- **Command:**
  ```bash
  git clone https://github.com/plausible/hosting
  cd hosting
  # Configure environment variables in plausible-conf.env
  docker-compose up -d
  ```
- Configure: `BASE_URL`, `SECRET_KEY_BASE`, `DATABASE_URL`, `CLICKHOUSE_DATABASE_URL`
- Time: 3-5 hours (includes troubleshooting, DNS setup, SSL certificate)

**Step 3: Import Historical Data**
- Plausible historical data import (via API or database direct insert)
- Time: 2-5 hours (depends on data volume, scripting complexity)

**Step 4: Update Tracking Script**
- Change Plausible script URL from `https://plausible.io/js/script.js` to `https://analytics.yourdomain.com/js/script.js`
- Deploy application update
- Verify events appearing in self-hosted dashboard
- Time: 30 minutes

**Step 5: Deactivate Managed Account**
- After 7-day parallel verification, cancel Plausible Cloud subscription
- Archive cloud data (CSV export for backup)
- Time: 30 minutes

**Migration Complexity: MEDIUM (6-12 hours)**
- **Time Breakdown:**
  - Export data: 1-2 hours
  - Self-hosted deployment: 3-5 hours
  - Historical data import: 2-5 hours
  - Script update + testing: 1 hour
  - **Total: 7-13 hours**

**Cost Breakdown:**
- Engineering time: 10 hours × $160/hr = $1,600 one-time
- Infrastructure: $50-100/mo (DigitalOcean 4GB Droplet)
- Savings: $249/mo (10M tier) - $50-100/mo (infra) = $150-200/mo
- **Break-even: 8-11 months** ($1,600 / $150-200)

**Ongoing Maintenance:**
- Software updates: 1 hour/quarter (4 hours/year)
- Monitoring + backups: Automated (Prometheus, daily DB snapshots)
- Security patches: 1 hour/quarter (4 hours/year)
- **Total: 8-10 hours/year** = $1,280-1,600/year additional labor

**Adjusted Break-Even:**
- Managed: $2,988/year
- Self-hosted: $600-1,200 infra + $1,280-1,600 labor = $1,880-2,800/year
- **Savings: $188-1,108/year** (marginal, only worth it for data sovereignty OR >10M pageviews)

---

## Migration 4: From Self-Hosted → Managed (Simplicity Optimization)

### Trigger: Maintenance Burden Exceeds Cost Savings

**Scenario:** Solo founder self-hosting Umami spends 5 hours/month troubleshooting (server crashes, database corruption, security patches)
- Labor cost: 5 hours × $160/hr × 12 months = $9,600/year
- Infrastructure: $20/mo × 12 = $240/year
- **Total: $9,840/year**

vs. Managed alternatives:
- Fathom: $14/mo × 12 = $168/year
- Plausible: $19/mo × 12 = $228/year
- **Savings: $9,600-9,700/year** by migrating to managed

**When to Migrate:**
1. **Team Change:** DevOps engineer leaves, no one else knows how to maintain analytics server
2. **Downtime Issues:** Analytics server crashed twice in 3 months, missed critical data
3. **Security Concerns:** Can't keep up with PostgreSQL security patches, worried about vulnerabilities
4. **Opportunity Cost:** 5 hours/month maintaining analytics = time not spent building product

### Migration Path: Umami Self-Hosted → Fathom Managed

**Step 1: Export Umami Data**
- Direct database access (PostgreSQL): `SELECT * FROM pageview;`
- Export to CSV (pg_dump or manual query)
- Time: 30 minutes

**Step 2: Sign Up for Fathom**
- Create account: https://usefathom.com
- Add website, receive tracking code
- Time: 5 minutes

**Step 3: Parallel Tracking**
- Add Fathom script alongside Umami (run both for 1-2 weeks)
- Verify data consistency
- Time: 10 minutes

**Step 4: Switchover**
- Remove Umami script from website
- Decommission Umami server (keep 30-day backup, then delete)
- Time: 30 minutes

**Migration Complexity: LOW (1-2 hours)**
- **Time Breakdown:**
  - Export Umami data: 30 minutes
  - Fathom signup + script addition: 15 minutes
  - Parallel tracking validation: 15 minutes
  - Remove Umami, decommission server: 30 minutes
  - **Total: 1.5 hours**

**Cost Breakdown:**
- Engineering time: 2 hours × $160/hr = $320 one-time
- Fathom subscription: $14/mo = $168/year
- Savings: $9,840/year (self-hosted labor) - $168/year (Fathom) = **$9,672/year**
- **Break-even: Immediate** (labor cost eliminated)

**Trade-off Acceptance:**
- Lose: Self-hosted data ownership, direct database access
- Gain: 5 hours/month back (60 hours/year = $9,600 value), zero maintenance, 99.9% uptime SLA

---

## Migration 5: Between Privacy-First Providers (Fathom ↔ Plausible ↔ Simple Analytics)

### Trigger: Price Change, Feature Need, or Acquisition

**Scenario A:** Fathom acquired by Cloudflare (2027 hypothetical), pricing increases 50% ($14 → $21/mo)
**Scenario B:** Need funnels, Plausible Business ($69/mo) too expensive, consider alternatives
**Scenario C:** EU data hosting preference (Simple Analytics Netherlands vs. Fathom Canada)

### Migration Path: Fathom → Plausible

**Step 1: CSV Export from Fathom**
- Fathom dashboard → Export → CSV (historical pageviews, sources, events)
- Time: 15 minutes

**Step 2: Sign Up for Plausible**
- Create account: https://plausible.io
- Add website, receive tracking script
- Time: 5 minutes

**Step 3: Import Historical Data (Optional)**
- Plausible supports CSV import (custom script or API)
- Time: 1-2 hours (if preserving historical continuity)
- **Can skip:** Most users start fresh (historical data in Fathom CSV backup)

**Step 4: Script Swap**
- Replace Fathom script:
  ```html
  <!-- OLD: Fathom -->
  <script src="https://cdn.usefathom.com/script.js" data-site="YOUR_SITE_ID"></script>
  <!-- NEW: Plausible -->
  <script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>
  ```
- Deploy update
- Time: 10 minutes

**Step 5: Custom Events Migration**
- Map Fathom events → Plausible events:
  - Fathom: `fathom.trackGoal('ABCDEF', 0);` → Plausible: `plausible('Signup');`
- Update event tracking code in application
- Time: 1-2 hours (depends on custom event count)

**Migration Complexity: LOW (3-6 hours total)**
- **Time Breakdown:**
  - Fathom CSV export: 15 minutes
  - Plausible signup: 5 minutes
  - Script replacement: 10 minutes
  - Custom events migration: 1-2 hours
  - Historical data import (optional): 1-2 hours
  - **Total: 2-5 hours** (without historical import) OR **3-7 hours** (with historical import)

**Cost Breakdown:**
- Engineering time: 4 hours × $160/hr = $640
- Fathom final month: $14
- Plausible first month: $19
- **Net Cost: $640 one-time + $5/mo increase** ($60/year)

**When Worth It:**
- Fathom price increases >35% ($14 → $19+) = Plausible same cost, open-source benefit
- Need open-source escape hatch (Plausible self-hostable, Fathom closed-source)
- EU data hosting preference (Plausible Germany vs. Fathom Canada)

---

## Migration 6: From Basic → Advanced (Adding Product Analytics Features)

### Trigger: Growth Stage (Need Funnels, Cohorts, Session Replay)

**Scenario:** Startup using Fathom ($14/mo) for 1 year, now Series A funded, need funnel analysis for conversion optimization

**Options:**
1. **Upgrade within provider:** Plausible Growth → Plausible Business ($19 → $69/mo for funnels)
2. **Add product analytics tool:** Keep Fathom (web analytics) + Add PostHog (product analytics)
3. **Migrate to full-featured:** Fathom → PostHog (consolidate)

### Option 1: Plausible Growth → Plausible Business

**Migration:** None (same provider, plan upgrade)
- **Process:** Dashboard → Settings → Upgrade to Business plan
- **Time:** 5 minutes
- **Cost:** $19/mo → $69/mo (+$50/mo = $600/year)
- **Features Added:** Funnels, custom properties (no cohorts, no session replay)

**When Worth It:** Need funnels ONLY, willing to pay $600/year premium, want simplicity (single tool)

### Option 2: Keep Fathom + Add PostHog

**Migration:** Add PostHog for product analytics, keep Fathom for web analytics

**Setup:**
- Fathom: Public website tracking (marketing site pageviews)
- PostHog: Application tracking (post-login user events)

**Implementation:**
- Add PostHog snippet to authenticated application (NOT public website):
  ```javascript
  posthog.init('YOUR_PROJECT_TOKEN', {
    api_host: 'https://app.posthog.com',
    autocapture: false, // Cookie-less mode
    loaded: function(posthog) { posthog.identify(user.id); }
  })
  ```
- Track product events:
  ```javascript
  posthog.capture('Feature Used', { feature: 'Export Report' });
  ```
- Time: 2-4 hours (PostHog integration, event tracking code)

**Cost:**
- Fathom: $14/mo (keep for web analytics)
- PostHog: $0 (1M events free tier) OR $18/mo (if >1M events)
- **Total: $14-32/mo** ($168-384/year)

**Benefits:**
- Best of both worlds: Privacy-first web analytics + product analytics
- PostHog features: Funnels, cohorts, session replay, feature flags
- Cost: $168-384/year vs. $828/year (Plausible Business)

**When Worth It:** Need advanced product analytics (cohorts, session replay), not just funnels

### Option 3: Migrate Fathom → PostHog (Consolidate)

**Why:** Single tool for web + product analytics, $0 cost (free tier)

**Migration:**
- Export Fathom data (CSV backup)
- Remove Fathom script
- Add PostHog script (cookie-less mode for GDPR compliance)
- Configure custom events (map Fathom events → PostHog events)
- Time: 3-6 hours

**Cost:**
- PostHog: $0 (1M events free) OR $18/mo (100K pageviews ≈ 300K-500K events)
- Savings: $14/mo (Fathom) - $0-18/mo (PostHog) = $0-14/mo ($0-168/year)

**Trade-off:**
- Lose: Privacy-first simplicity (PostHog heavier, 5KB script vs. Fathom 1.6KB)
- Gain: Product analytics features (funnels, cohorts, session replay), $0-14/mo savings

**When Worth It:** Budget-conscious, need product analytics, accept cookie-less mode configuration

---

## Migration Triggers & Decision Matrix

| Current Tool | Trigger | Migrate To | Complexity | Cost | Reason |
|--------------|---------|------------|------------|------|--------|
| **GA4** | EU customers, GDPR compliance | Plausible, Fathom | LOW (3-6 hrs) | $640 | Regulatory risk, privacy brand |
| **GA4** | Need funnels + privacy | PostHog (cookie-less) | MEDIUM (10-20 hrs) | $1,600 | Advanced features + GDPR |
| **PostHog Free** | Acquisition (2026-2028) | PostHog Self-Hosted | MEDIUM (10-20 hrs) | $2,400 | Free tier elimination |
| **Mixpanel Free** | Acquisition (2025-2027) | PostHog Self-Hosted | HIGH (20-40 hrs) | $3,200-6,400 | Feature parity, avoid lock-in |
| **Mixpanel Free** | Downgrade to web analytics | Plausible | HIGH (50-100 hrs) | $8,000-16,000 | Feature gap, NOT recommended |
| **Plausible $249/mo** | Cost optimization (10M pageviews) | Umami Self-Hosted | MEDIUM (6-12 hrs) | $1,600 | Break-even 8-11 months |
| **Umami Self-Hosted** | Maintenance burden (5 hrs/mo) | Fathom, Plausible | LOW (1-2 hrs) | $320 | Save $9,600/year labor |
| **Fathom** | Acquisition OR price increase >35% | Plausible | LOW (3-6 hrs) | $640 | Open-source escape, EU hosting |
| **Fathom** | Need funnels | Plausible Business OR PostHog | LOW (2-6 hrs) | $320-960 | Feature upgrade |
| **Plausible Growth** | Need cohorts, session replay | PostHog (add, keep Plausible) | LOW (2-4 hrs) | $320 | Best of both worlds |

---

## Migration Cost Summary

### Low Complexity (3-6 hours, $500-1,000)
- GA4 → Plausible, Fathom, Simple Analytics
- Fathom ↔ Plausible ↔ Simple Analytics (privacy-first swaps)
- Self-hosted → Managed (simplicity migration)

### Medium Complexity (10-20 hours, $1,600-3,200)
- GA4 → PostHog (need product analytics)
- PostHog Free → PostHog Self-Hosted (acquisition escape)
- Managed → Self-hosted (cost optimization, data sovereignty)

### High Complexity (50-100 hours, $8,000-16,000)
- Mixpanel → Plausible (feature gap, event schema translation)
- Amplitude → Any provider (MTU model conversion)
- Heap → Any provider (auto-capture proprietary)

**Strategic Insight:** Privacy-first migrations = LOW complexity (3-6 hours). Product analytics migrations = MEDIUM-HIGH complexity (20-100 hours). Plan accordingly.

---

## Recommended Migration Paths

**From GA4 (EU Customers):** → Plausible ($19/mo) [3-6 hours, $640]
**From GA4 (Need Funnels):** → PostHog (cookie-less mode) [10-20 hours, $1,600]
**From PostHog Free (Acquisition):** → PostHog Self-Hosted [10-20 hours, $2,400]
**From Mixpanel Free (Acquisition):** → PostHog Self-Hosted (NOT Plausible) [20-40 hours, $3,200-6,400]
**From Managed (>10M pageviews):** → Self-Hosted (Umami, Plausible, Matomo) [6-12 hours, $1,600]
**From Self-Hosted (Maintenance burden):** → Fathom, Plausible [1-2 hours, $320]

**Never Migrate:** Mixpanel → Plausible (feature gap too large, 50-100 hours wasted). Choose PostHog self-hosted instead.
