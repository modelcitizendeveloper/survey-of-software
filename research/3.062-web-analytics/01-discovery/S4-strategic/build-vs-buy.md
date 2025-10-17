# Build vs Buy Decision Framework
## Self-Host vs Managed Service Strategic Analysis

**Created:** October 11, 2025
**Focus:** When to self-host vs. use managed analytics
**Decision Factors:** Cost, maintenance, data sovereignty, scale

---

## Core Trade-Off

**Self-Hosted (Build/DIY):**
- Upfront: 5-30 hours setup + infrastructure provisioning
- Ongoing: 1-5 hours/month maintenance (updates, monitoring, backups)
- Cost: $10-200/mo infrastructure (depends on scale)
- Control: 100% data ownership, zero vendor dependency

**Managed Service (Buy):**
- Upfront: 5-30 minutes signup + script installation
- Ongoing: 0 hours maintenance (vendor handles everything)
- Cost: $0-500/mo subscription (depends on traffic tier)
- Control: Vendor-dependent, API export available (varies)

**The Question:** When does self-hosting total cost (infra + labor) become cheaper than managed pricing?

---

## Break-Even Analysis

### Scenario: 100K Pageviews/Month

**Managed Options:**
- Fathom: $14/mo = $168/year
- Plausible: $19/mo = $228/year
- Simple Analytics: €19/mo = $228/year (€108/year annual = $117/year)

**Self-Hosted Costs:**

**Infrastructure (Monthly):**
- DigitalOcean 4GB Droplet: $24/mo ($288/year)
- AWS t3.medium (4GB): $30/mo ($360/year)
- Hetzner CX21 (4GB, EU): $6/mo ($72/year)
- **Range: $72-360/year**

**Labor (Monthly Maintenance):**
- Optimistic (1 hour/month): 12 hrs/year × $160/hr = $1,920/year
- Realistic (2 hours/month): 24 hrs/year × $160/hr = $3,840/year
- Pessimistic (5 hours/month): 60 hrs/year × $160/hr = $9,600/year
- **Range: $1,920-9,600/year**

**Total Self-Hosted Cost:**
- Best case: $72 (Hetzner) + $1,920 (1 hr/mo) = **$1,992/year**
- Average case: $288 (DO) + $3,840 (2 hrs/mo) = **$4,128/year**
- Worst case: $360 (AWS) + $9,600 (5 hrs/mo) = **$9,960/year**

**Managed vs Self-Hosted (100K pageviews):**
- Fathom $168/year vs. Self-hosted $1,992-9,960/year = **12-59× more expensive to self-host**
- Plausible $228/year vs. Self-hosted $1,992-9,960/year = **9-44× more expensive to self-host**

**Conclusion: Self-hosting NOT worth it at 100K pageviews (managed 9-59× cheaper)**

---

### Scenario: 1M Pageviews/Month

**Managed Options:**
- Fathom: $54/mo = $648/year
- Plausible: $69/mo = $828/year
- PostHog: ~$450/mo (3M events) = $5,400/year
- Matomo Cloud: $69/mo (estimate) = $828/year

**Self-Hosted Costs:**

**Infrastructure (Monthly):**
- DigitalOcean 8GB Droplet: $48/mo ($576/year)
- AWS t3.large (8GB): $60/mo ($720/year)
- Hetzner CX31 (8GB, EU): $11/mo ($132/year)
- **Range: $132-720/year**

**Labor (Same as 100K scenario):**
- Best case: 12 hrs/year × $160 = $1,920/year
- Average case: 24 hrs/year × $160 = $3,840/year
- Worst case: 60 hrs/year × $160 = $9,600/year

**Total Self-Hosted Cost:**
- Best case: $132 (Hetzner) + $1,920 (1 hr/mo) = **$2,052/year**
- Average case: $576 (DO) + $3,840 (2 hrs/mo) = **$4,416/year**
- Worst case: $720 (AWS) + $9,600 (5 hrs/mo) = **$10,320/year**

**Managed vs Self-Hosted (1M pageviews):**
- Fathom $648/year vs. Self-hosted $2,052-10,320/year = **3-16× more expensive to self-host**
- Plausible $828/year vs. Self-hosted $2,052-10,320/year = **2.5-12× more expensive to self-host**
- PostHog $5,400/year vs. Self-hosted $2,052-10,320/year = **0.4-5× (BREAK-EVEN if <2 hrs/mo maintenance)**

**Conclusion: Self-hosting still NOT worth it at 1M pageviews UNLESS maintenance <2 hrs/month OR using expensive managed service (PostHog cloud)**

---

### Scenario: 10M Pageviews/Month

**Managed Options:**
- Fathom: $274/mo = $3,288/year
- Plausible: $249/mo = $2,988/year
- PostHog: ~$13,500/mo (30M events estimate) = $162,000/year
- Matomo Cloud: $499/mo (estimate) = $5,988/year

**Self-Hosted Costs:**

**Infrastructure (Monthly):**
- DigitalOcean 16GB Droplet: $96/mo ($1,152/year)
- AWS t3.xlarge (16GB): $120/mo ($1,440/year)
- Hetzner CX41 (16GB, EU): $21/mo ($252/year)
- **Range: $252-1,440/year**

**Labor (Same maintenance hours, scale doesn't increase much):**
- Best case: 12 hrs/year × $160 = $1,920/year
- Average case: 24 hrs/year × $160 = $3,840/year
- Worst case: 60 hrs/year × $160 = $9,600/year

**Total Self-Hosted Cost:**
- Best case: $252 (Hetzner) + $1,920 (1 hr/mo) = **$2,172/year**
- Average case: $1,152 (DO) + $3,840 (2 hrs/mo) = **$4,992/year**
- Worst case: $1,440 (AWS) + $9,600 (5 hrs/mo) = **$11,040/year**

**Managed vs Self-Hosted (10M pageviews):**
- Plausible $2,988/year vs. Self-hosted $2,172-11,040/year = **BREAK-EVEN if <2 hrs/mo maintenance**
- Fathom $3,288/year vs. Self-hosted $2,172-11,040/year = **BREAK-EVEN if <2 hrs/mo maintenance**
- PostHog $162,000/year vs. Self-hosted $2,172-11,040/year = **15-75× cheaper to self-host**
- Matomo Cloud $5,988/year vs. Self-hosted $2,172-11,040/year = **SELF-HOST CHEAPER if <2.5 hrs/mo**

**Conclusion: Self-hosting WORTH IT at 10M+ pageviews IF maintenance optimized (<2 hrs/month)**

---

## Break-Even Traffic Threshold

**Key Insight:** Self-hosting becomes cost-effective when:

`(Managed Annual Cost) > (Infrastructure + Labor)`

**Solving for traffic:**
- Managed pricing scales linearly with traffic (10× traffic = ~10× cost)
- Self-hosted infrastructure scales sub-linearly (10× traffic = 2-3× infrastructure)
- Labor remains constant (2 hrs/month regardless of 100K or 10M pageviews)

**Break-Even Formula:**
```
Managed Cost = Infra Cost + Labor Cost
Plausible $19/mo × (Traffic/100K) = $24/mo + $320/mo
$19 × (Traffic/100K) = $344
Traffic = 100K × ($344 / $19)
Traffic ≈ 1.8M pageviews/month
```

**Break-Even Points:**
- **Plausible:** 1.8M pageviews/month (if 2 hrs/mo maintenance, Hetzner $11/mo)
- **Fathom:** 2.0M pageviews/month (slightly cheaper managed pricing)
- **PostHog Cloud:** 200K pageviews/month (expensive event-based pricing)

**Strategic Thresholds:**
- <1M pageviews: Always choose managed (9-59× cheaper)
- 1-5M pageviews: Managed still better UNLESS <1 hr/mo maintenance achievable
- 5-10M pageviews: Self-hosting competitive IF DevOps experienced
- >10M pageviews: Self-hosting cheaper (2-75× savings)

---

## When Self-Hosting Makes Sense (Non-Economic Reasons)

### Reason 1: Data Sovereignty (GDPR, HIPAA, Compliance)

**Scenario:** Healthcare SaaS, EU enterprise customer requiring on-premise analytics

**Requirement:** Data cannot leave customer infrastructure (no third-party processors)

**Only Option:** Self-hosted (Matomo, Umami, PostHog on-premise)

**Cost:** Irrelevant (compliance > economics)

**Decision:** Self-host regardless of traffic (even 10K pageviews)

**Example:**
- German healthcare company: GDPR Article 28 requires DPA with all processors
- Managed analytics (Plausible, Fathom) = third-party processor = DPA required
- Self-hosted Matomo on company servers = no third-party = no DPA needed
- **Self-host saves legal complexity (not just money)**

### Reason 2: Existing Infrastructure (Zero Incremental Cost)

**Scenario:** Startup already running PostgreSQL database for main application

**Setup:** Add Umami schema to existing PostgreSQL instance
```sql
-- Umami piggybacks existing database
CREATE DATABASE umami;
-- Add analytics tables to existing PostgreSQL server (0 infra cost)
```

**Incremental Cost:** $0/month (database already paid for, analytics = +50MB disk)

**Maintenance:** 1 hour/quarter (Umami rarely breaks, low-maintenance)

**Break-Even:** Immediate (managed $14-19/mo vs. $0 self-hosted)

**Decision:** Self-host (economic + simplicity)

### Reason 3: Privacy Brand Positioning

**Scenario:** Privacy-focused VPN, encrypted messaging app, developer tool

**Brand Value:** "We self-host analytics (Umami) on our servers. Your data never touches third parties."

**Marketing Advantage:** Trust signal for privacy-conscious customers

**Cost-Benefit:** $2,000/year self-hosting cost < $10,000+/year customer trust value

**Decision:** Self-host for brand alignment (economic secondary)

**Example:**
- ProtonMail self-hosts analytics (privacy brand consistency)
- Referencing Plausible (third-party) = less impactful than "our servers"

### Reason 4: Technical Team Available (Sunk Cost Labor)

**Scenario:** Startup with 2× DevOps engineers managing 20+ services (Kubernetes, databases, monitoring)

**Analytics Setup:** Add Umami to Kubernetes cluster (30 min deployment)

**Ongoing Maintenance:** 1 hour/quarter (updates automated via CI/CD pipeline)

**Labor Cost:** Sunk (DevOps already paid, analytics = +1 service in portfolio)

**Break-Even:** Immediate (managed $14-19/mo vs. marginal labor cost ≈ $0)

**Decision:** Self-host (DevOps expertise eliminates labor cost premium)

### Reason 5: Acquisition Insurance (VC-Backed Vendor Risk)

**Scenario:** Using PostHog free tier (1M events), anticipating acquisition 2026-2028

**Risk:** Free tier eliminated post-acquisition, forced upgrade to $450/mo cloud OR migrate

**Insurance:** Self-host PostHog NOW (pre-acquisition) = acquisition-proof

**Cost:** $50/mo infrastructure + 2 hrs/mo = $680/year (avg case)

**Benefit:** Avoid forced migration (10-20 hours = $1,600-3,200 labor) + price shock ($450/mo = $5,400/year)

**Decision:** Self-host for vendor independence (risk mitigation > short-term economics)

---

## When Managed Service Makes Sense

### Reason 1: Solo Founder / Small Team (Time > Money)

**Scenario:** Solo founder building MVP, wearing 10 hats (engineering, sales, marketing, support)

**Time Constraint:** 0 hours/month available for analytics maintenance

**Opportunity Cost:** 2 hours/month maintenance × $300/hr (founder value) = $600/mo = $7,200/year

**Managed Cost:** Plausible $19/mo = $228/year

**Savings:** $7,200 - $228 = **$6,972/year by choosing managed**

**Decision:** Always managed (time scarcity > cost savings)

### Reason 2: Non-Technical Team

**Scenario:** Marketing agency, blog network, e-commerce site (no DevOps skills)

**Self-Hosting Risk:** Server crashes, analytics goes down for 3 days before noticed, can't troubleshoot

**Downtime Cost:** 3 days missing data = permanent data loss (pageviews not recorded)

**Managed SLA:** Fathom/Plausible 99.9% uptime = 8 hours downtime/year maximum

**Decision:** Managed (reliability > cost)

### Reason 3: Low Traffic (<1M pageviews/month)

**Scenario:** Personal blog, side project, early-stage startup (100K pageviews/month)

**Managed Cost:** Fathom $14/mo = $168/year

**Self-Hosted Cost:** $2,000-10,000/year (infrastructure + labor)

**Savings:** $1,832-9,832/year by choosing managed

**Decision:** Always managed (9-59× cheaper)

### Reason 4: Simplicity Priority (Focus on Core Product)

**Scenario:** SaaS startup, analytics is peripheral (not core product)

**Philosophy:** "We build CRM software, not analytics infrastructure"

**Trade-off:** Pay $19/mo (Plausible) to avoid 2 hrs/month maintenance = buy back 24 hrs/year for core product

**Value:** 24 hours × $200/hr (engineering time) = $4,800/year opportunity cost

**Managed Cost:** $19/mo = $228/year

**ROI:** $4,800 value / $228 cost = **21× return** (time spent on product > analytics)

**Decision:** Managed (focus strategy)

### Reason 5: Vendor Trust (Bootstrapped, Ethical Providers)

**Scenario:** Trust Plausible/Fathom (bootstrapped, profitable, 4-5 year track record)

**Vendor Risk:** 15-20% acquisition probability (low), pricing predictable (+15-30% inflation over 3 years)

**Self-Hosting Motivation:** Weak (vendor trustworthy, lock-in low via CSV export)

**Decision:** Managed (vendor trust reduces self-hosting insurance value)

---

## Self-Hosting Complexity Matrix

| Tool | Setup Time | Complexity | Monthly Maintenance | Best For |
|------|------------|------------|---------------------|----------|
| **Umami** | 15-30 min | Low (Docker Compose, PostgreSQL) | 1 hr/month | Developers, PostgreSQL users, simplest self-host |
| **Plausible** | 30-60 min | Medium (ClickHouse + PostgreSQL) | 2 hrs/month | Privacy-first, moderate traffic (1-5M) |
| **Matomo** | 60-120 min | Medium-High (PHP, MySQL, complex config) | 3-4 hrs/month | Enterprise, GA replacement, feature-rich |
| **PostHog** | 30-60 min | Medium (ClickHouse, Docker Compose) | 2 hrs/month | Product analytics, event-based, scale |
| **GoatCounter** | 20-40 min | Low (Go binary, SQLite/PostgreSQL) | 1 hr/month | Minimalists, low traffic, solo projects |

**Easiest Self-Host:** Umami (15-30 min setup, 1 hr/mo maintenance, PostgreSQL-only dependency)

**Most Complex:** Matomo (60-120 min setup, 3-4 hrs/mo maintenance, PHP/MySQL/plugins)

**Best Features/Complexity Ratio:** PostHog (moderate complexity, maximum features)

---

## Maintenance Reality Check

**Optimistic (1 hour/month):**
- Quarterly software updates (Umami 0.1% breaking changes)
- Automated backups (daily cron, zero intervention)
- Monitoring: Uptime Robot (external, free)
- Security patches: Auto-updates enabled (Ubuntu unattended-upgrades)

**Realistic (2 hours/month):**
- Monthly updates check (30 min)
- Troubleshooting (30 min): Database disk space, slow queries
- Backup verification (15 min): Test restore monthly
- Security review (15 min): Check CVEs, apply patches
- **Total: 1.5-2 hrs/month**

**Pessimistic (5 hours/month):**
- Breaking update: Umami 2.0 → 3.0 migration (4 hours one-time)
- Server crash: DigitalOcean outage, restore from backup (3 hours)
- Database corruption: PostgreSQL WAL recovery (2 hours)
- Security incident: Patch zero-day vulnerability (1 hour)
- **Total: 10 hours/quarter = 3.3 hrs/month average** (includes incidents)

**Key Insight:** Maintenance hours vary wildly. Conservative estimate (2 hrs/mo) safer than optimistic (1 hr/mo).

---

## DIY Analytics (Completely Custom Build)

**Scenario:** "Why pay $14/mo? I'll build my own analytics in 1 weekend."

**Reality Check:**

**Weekend 1 (16 hours): MVP**
- Database schema: `CREATE TABLE pageviews (url, timestamp, referrer, country)`
- JavaScript tracking pixel: `fetch('/api/track', {url: window.location})`
- Backend API: Node.js `/api/track` endpoint (insert into database)
- Basic dashboard: SQL queries + HTML table
- **Cost:** 16 hours × $160/hr = $2,560

**Month 2 (8 hours): Features**
- UTM parameter parsing (`utm_source`, `utm_campaign`)
- Device/browser detection (user agent parsing)
- Geographic IP lookup (MaxMind GeoIP database)
- **Cost:** 8 hours × $160/hr = $1,280

**Month 3 (6 hours): Polish**
- Dashboard charts (Chart.js integration)
- Date range filters
- Export to CSV
- **Cost:** 6 hours × $160/hr = $960

**Ongoing (2 hours/month): Maintenance**
- Bug fixes (referrer parsing edge cases)
- Performance optimization (database indexes)
- Security updates (SQL injection prevention)
- **Cost:** 24 hrs/year × $160/hr = $3,840/year

**Total Cost (Year 1):**
- Development: $2,560 + $1,280 + $960 = $4,800
- Maintenance: $3,840
- Infrastructure: $288 (DigitalOcean)
- **Total: $8,928**

**vs. Plausible $228/year (managed):**
- DIY = **39× more expensive** in Year 1
- DIY ongoing (Year 2+): $3,840 + $288 = $4,128/year vs. Plausible $228 = **18× more expensive**

**Missing Features (DIY vs. Plausible):**
- Real-time dashboard
- Anomaly detection
- Custom event tracking (advanced)
- Team access controls
- Public dashboard sharing
- Mobile app
- SLA guarantees
- **Cost to build all features:** +40-80 hours = $6,400-12,800

**Conclusion: DIY analytics NEVER worth it economically (18-39× more expensive). Only justified if:**
1. Learning experience (educational value > cost)
2. Extreme privacy requirements (zero third-parties, including Plausible self-hosted)
3. Niche use case (custom metrics not available in existing tools)

---

## Hybrid Approach (Best of Both Worlds)

**Strategy:** Start managed, self-host at scale

**Phase 1 (0-1M pageviews):**
- Managed: Plausible $19/mo OR Fathom $14/mo
- Duration: 1-2 years (MVP → product-market fit)
- Cost: $168-456 total
- **Benefits:** Zero maintenance, fast iteration, predictable cost

**Phase 2 (1-5M pageviews):**
- Evaluate self-hosting: Calculate `(Current Managed Cost × 12) vs. (Infra + Labor)`
- Trigger: Managed cost >$500/year AND technical team available
- **Decision Point:** Plausible $828/year vs. Umami self-hosted $2,000-4,000/year = stay managed

**Phase 3 (5-10M+ pageviews):**
- Self-host: Umami, Plausible, or Matomo on-premise
- Migration time: 6-12 hours (export Plausible API → import Umami database)
- Cost: $1,000-5,000/year (infrastructure + maintenance)
- Savings: $2,988/year (Plausible $249/mo) - $4,000/year (self-hosted) = net neutral OR savings if optimized
- **Benefits:** Data sovereignty, cost ceiling (no surprise price increases)

**Optimal Path:**
1. Start: Managed (Fathom $14/mo, 0 hours setup)
2. Grow: Stay managed until 5M+ pageviews (simplicity > cost)
3. Scale: Self-host at 10M+ pageviews (economics + data control)

---

## Decision Framework

**Choose Managed Service When:**
- ✅ Traffic <5M pageviews/month (managed 9-59× cheaper)
- ✅ Solo founder OR non-technical team (time > money)
- ✅ No DevOps capacity (can't maintain infrastructure)
- ✅ Focus on core product (analytics peripheral)
- ✅ Trust vendor (Plausible, Fathom bootstrapped, 15-20% acquisition risk)

**Choose Self-Hosted When:**
- ✅ Traffic >10M pageviews/month (self-host 2-75× cheaper)
- ✅ Data sovereignty required (GDPR, HIPAA, compliance)
- ✅ Existing infrastructure (PostgreSQL already running = $0 incremental)
- ✅ Technical team available (DevOps managing 10+ services already)
- ✅ Privacy brand positioning (self-hosting = marketing value)
- ✅ Vendor risk aversion (VC-backed acquisition insurance)

**Choose DIY (Build from Scratch) When:**
- ✅ Learning goal (educational value > economics)
- ✅ Extreme privacy (zero third-parties, including self-hosted tools)
- ✅ Niche use case (custom metrics unavailable elsewhere)
- ❌ **Never for economic reasons** (DIY 18-39× more expensive than managed)

---

## Recommendation

**Default Choice (90% of use cases):** Managed Service
- **Tool:** Fathom ($14/mo) for cost, Plausible ($19/mo) for open-source insurance
- **Reason:** 9-59× cheaper than self-hosting at typical traffic levels (<5M pageviews)
- **Break-Even:** Self-hosting only cheaper at 10M+ pageviews (rare for most startups)

**Exception (Data Sovereignty):** Self-Hosted
- **Tool:** Umami (easiest), Matomo (most features), PostHog (product analytics)
- **Reason:** Compliance > economics (GDPR Article 28, HIPAA, government contracts)
- **Break-Even:** Immediate (compliance value > cost difference)

**Exception (Existing PostgreSQL):** Self-Hosted Umami
- **Tool:** Umami (piggyback existing database)
- **Reason:** $0 incremental infrastructure cost
- **Break-Even:** Immediate ($0 vs. $14-19/mo managed)

**Strategic Path:** Start managed (Fathom, Plausible), evaluate self-hosting at 5-10M pageviews, migrate if economics justify (rare). Never DIY from scratch (economics never work).
