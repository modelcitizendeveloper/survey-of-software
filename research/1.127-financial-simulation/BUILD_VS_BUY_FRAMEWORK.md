
# BUILD vs BUY: Financial Scenario Analysis

**Research:** 1.127 (Financial Simulation) + 3.004 (Cash Flow Management SaaS)
**Date:** 2025-01-18
**Question:** When should you BUILD CLI tools vs BUY SaaS for cash flow analysis?

---

## Executive Summary

**You can BUY** commercial platforms (Pulse, Finmark, Causal, Mosaic) for $29-$2,000/month...

**Or you can BUILD** Unix-style CLI tools (fs-parse, fs-scenario, fs-analyze) using Python libraries for FREE

**Decision factors:**
1. **Budget:** Below $750/mo → BUY, Above $1,250/mo → BUILD
2. **Technical team:** No Python developers → BUY
3. **Customization:** Standard reports → BUY, Custom models → BUILD
4. **Infrastructure:** Standalone → BUY, Data warehouse → BUILD

---

## What Commercial Platforms Offer (BUY)

### From 3.004 Research: 8 Platforms, 3 Tiers

**Tier 1: Small Business ($29-89/month)**
- **Pulse** ($29-89/mo) - Cash flow visibility, 13-week forecast
- **Fathom** ($59/mo) - Financial analysis, KPIs

**Tier 2: Startup/SMB ($100-800/month)**
- **Finmark** ($100-200/mo) - Fundraising scenarios, 3-statement model
- **Jirav** ($150-400/mo) - Budget vs actuals, department tracking
- **Causal** ($500-800/mo) - Advanced scenarios, Snowflake integration

**Tier 3: Mid-Market ($800-2,000+/month)**
- **Mosaic** ($2,000+/mo) - Real-time dashboards, metrics automation
- **Dryrun** ($800/mo) - Construction draws, multi-entity
- **PlanGuru** ($300-400/yr) - Grant-funded orgs, annual budgeting

### What Questions They Answer

**Cash Flow Visibility** (All platforms)
- "How much cash do we have?"
- "When will we run out of money?"
- "What's our burn rate?"

**Forecasting** (All except Pulse basics)
- "What will revenue be next quarter?"
- "How much cash will we need for next 12 months?"
- "When do we hit profitability?"

**Scenario Analysis** (Finmark, Causal, Mosaic)
- "What if revenue grows 20% vs 30%?"
- "What if we hire 5 more people?"
- "What if we delay that purchase?"

**Fundraising Support** (Finmark, Causal)
- "How much runway do we have?"
- "How much should we raise?"
- "What's our dilution at different valuations?"

**Operational Metrics** (Jirav, Mosaic, Dryrun)
- "Revenue per employee?"
- "Customer acquisition cost trend?"
- "Cash conversion cycle?"

**Real-time Dashboards** (Mosaic, Causal)
- "What's today's cash balance?"
- "How's this month tracking vs budget?"
- "Which metrics are off-track?"

---

## What You Can BUILD (CLI Tools)

### Our Proposed Tools: fs-parse, fs-scenario, fs-analyze

Using Python libraries (from 1.127 research):
- **pandas** - Data manipulation
- **numpy-financial** - NPV, IRR, PMT
- **Prophet** - Forecasting (optional)
- **scipy.stats** - Monte Carlo (optional)

### Questions You Can Answer

**1. Cash Flow Visibility** ✅
```bash
# Parse QuickBooks export
fs-parse qb_export.csv > baseline.jsonl

# Analyze current state
fs-analyze baseline.jsonl --summary

# Output:
Current Cash: $150K
Burn Rate: -$45K/month
Runway: 3.3 months
```

**2. Simple Forecasting** ✅
```bash
# Linear extrapolation
fs-forecast baseline.jsonl --method linear --periods 12

# Prophet forecasting (seasonal patterns)
fs-forecast baseline.jsonl --method prophet --periods 12
```

**3. Scenario Analysis** ✅
```bash
# Create scenarios
fs-scenario baseline.jsonl --output scenarios.jsonl

# Compare scenarios
fs-analyze scenarios.jsonl

# Output:
Scenario         Cash at 12mo    Break-even    Runway
────────────────────────────────────────────────────
Baseline          $20K           Month 14      16 months
Conservative     -$50K           Never         12 months
Aggressive       $150K           Month 9       20+ months
```

**4. Sensitivity Analysis** ✅
```bash
# Test revenue growth assumptions
fs-analyze scenarios.jsonl --sensitivity revenue_growth_rate

# Output:
Growth Rate    Cash at 12mo    Break-even
───────────────────────────────────────
   10%          -$150K         Never
   15%           -$80K         Month 18
   20%            $20K         Month 14
   25%           $120K         Month 11
   30%           $250K         Month  9
```

**5. Monte Carlo Simulation** ✅
```bash
# Run 10,000 scenarios with uncertainty
fs-analyze scenarios.jsonl --monte-carlo --runs 10000

# Output:
Monte Carlo Results (10,000 runs)
Cash at 12 months:
  5th percentile:   -$80K  (worst case)
  Median:           $150K
  95th percentile:  $420K  (best case)

Probability of running out of cash: 12%
```

**6. Comparison to Actuals** ✅
```bash
# Compare forecast vs reality
fs-analyze scenarios.jsonl --actual actual_2024.jsonl

# Output:
Metric              Projected    Actual     Variance
────────────────────────────────────────────────────
Revenue (Q1)         $300K       $280K      -6.7%
Marketing Spend       $15K        $18K     +20.0%
```

---

## What You CANNOT Easily Build

### Features That Require SaaS

**1. Real-time Data Sync**
- **SaaS:** Mosaic syncs QuickBooks every hour
- **CLI:** Manual export required (could automate with cron)

**2. Collaborative Editing**
- **SaaS:** Multiple users edit budgets simultaneously (Causal, Finmark)
- **CLI:** Git-based collaboration (requires technical users)

**3. Beautiful Dashboards**
- **SaaS:** Click-and-drag chart builders (Mosaic, Jirav)
- **CLI:** ASCII charts or export to matplotlib (not as polished)

**4. Pre-built Templates**
- **SaaS:** SaaS metrics templates, fundraising models (Finmark)
- **CLI:** You build your own (but reusable)

**5. User Management & Permissions**
- **SaaS:** Role-based access control (Jirav, Mosaic)
- **CLI:** File permissions (basic)

**6. Support & Onboarding**
- **SaaS:** Customer success team, live chat
- **CLI:** You're on your own (or community forums)

**7. Mobile Apps**
- **SaaS:** Check cash balance on phone (Pulse, Finmark)
- **CLI:** SSH into server? (impractical)

**8. Integrations**
- **SaaS:** 25+ integrations (Stripe, Salesforce, HubSpot) - Mosaic
- **CLI:** Build your own API connectors (doable but time-consuming)

---

## BUILD vs BUY Decision Framework

### Decision Tree

```
Do you need this for your business?
│
├─ Question 1: Do you have Python developers?
│   │
│   ├─ NO → BUY (training cost > SaaS cost)
│   │
│   └─ YES → Continue to Question 2
│
├─ Question 2: What's your monthly SaaS budget?
│   │
│   ├─ <$300/month (Pulse, Finmark) → BUY
│   │   Reason: SaaS includes UI, support, collaboration
│   │           Time to build CLI tools > small savings
│   │
│   ├─ $300-750/month → DEPENDS (Continue to Question 3)
│   │
│   └─ >$750/month (Causal, Mosaic) → Likely BUILD
│       Reason: 3-year DIY TCO ($11K-23K) < SaaS TCO ($27K-72K)
│
├─ Question 3: Do you need custom models?
│   │
│   ├─ YES (proprietary algorithms, unique business model) → BUILD
│   │   Examples: Multi-sided marketplace dynamics
│   │             Construction industry cash flow timing
│   │             SaaS cohort-based retention modeling
│   │
│   └─ NO (standard cash flow, budgeting) → Continue to Question 4
│
├─ Question 4: Do you have existing data warehouse?
│   │
│   ├─ YES (Snowflake, BigQuery, Redshift) → BUILD
│   │   Reason: SaaS integration limited
│   │           Data already centralized
│   │           Python connects directly to warehouse
│   │
│   └─ NO (Excel, QuickBooks exports) → BUY
│       Reason: SaaS handles integrations for you
│
├─ Question 5: Do you need non-technical users to collaborate?
│   │
│   ├─ YES (CFO + COO + department heads) → BUY
│   │   Reason: CLI tools require technical literacy
│   │
│   └─ NO (solo founder, technical CFO) → BUILD
│       Reason: CLI tools work fine for technical users
│
└─ Question 6: How important is vendor stability?
    │
    ├─ CRITICAL (long-term platform, company depends on it) → BUY (Pulse, Fathom)
    │   Reason: Bootstrapped vendors = 95% 5-year survival
    │           CLI tools = you maintain forever
    │
    └─ FLEXIBLE (willing to rebuild if needed) → BUILD
        Reason: Full control, no vendor lock-in
```

---

## Cost Comparison (3-Year TCO)

### Scenario: Small Startup (10 employees, $1M ARR)

**Option 1: BUY - Finmark**
- Monthly cost: $150/mo
- 3-year TCO: $5,400
- **Includes:** UI, support, templates, unlimited users
- **Setup time:** Day 1 (link QuickBooks, start using)

**Option 2: BUY - Causal**
- Monthly cost: $600/mo
- 3-year TCO: $21,600
- **Includes:** Advanced scenarios, Snowflake integration, real-time dashboards
- **Setup time:** Week 1-2 (data warehouse connections)

**Option 3: BUILD - CLI Tools**
- Development time: 2-3 days (MVP), 1-2 weeks (polished)
- Maintenance: 1-2 hours/month
- 3-year TCO: ~$11,400 (developer time at $150/hr)
  - Initial build: 40 hours × $150 = $6,000
  - Maintenance: 2 hours/month × 36 months × $150 = $10,800
  - **Total:** $16,800 (but amortized over all future use)
- **Includes:** Full customization, no vendor lock-in
- **Setup time:** 2-3 days (parse data, create first scenarios)

**Option 4: HYBRID - Pulse + CLI Tools**
- Pulse for cash visibility: $89/mo × 36 = $3,204
- CLI tools for scenarios: $6,000 (one-time build)
- **Total 3-year TCO:** $9,204
- **Best of both worlds:** UI for executives, CLI for analysis

---

## BUILD Economics (from 1.127)

### Library Costs (FREE - Open Source)

**Core libraries:**
- pandas ($0)
- numpy-financial ($0)
- Prophet ($0 - Meta open source)
- scipy ($0)
- matplotlib ($0)

**Total library cost:** $0

**BUT: Developer time is the cost**

### Developer Time Breakdown

**Phase 1: MVP (2-3 days = 16-24 hours)**
- fs-parse: CSV → JSONL (4-6 hours)
- fs-scenario: Simple TUI (6-8 hours)
- fs-analyze: Basic comparison (6-10 hours)
- **Cost at $150/hr:** $2,400 - $3,600

**Phase 2: Polish (1 week = 40 hours)**
- Better TUI (blessed library)
- Chart generation
- Prophet integration
- **Cost:** $6,000

**Phase 3: Maintenance (ongoing)**
- 1-2 hours/month
- **Annual cost:** $1,800 - $3,600

**3-Year Total:** $16,800 - $21,600

### Breakeven Analysis

**Breakeven vs SaaS:**
- Finmark ($150/mo): Build pays off after 11 months ($1,650 vs $1,650)
- Causal ($600/mo): Build pays off immediately ($6,000 vs $7,200 first year)
- Mosaic ($2,000/mo): Build saves $56,400 over 3 years ($72K vs $16.8K)

**Conclusion:**
- **Below $300/mo SaaS:** BUILD doesn't pay off (time > savings)
- **$300-750/mo SaaS:** Marginal (depends on customization needs)
- **Above $750/mo SaaS:** BUILD pays off significantly

---

## Real-World Scenarios: BUILD vs BUY

### Scenario 1: Solo Founder, Pre-Revenue, Raising Seed

**Need:** 3-statement model for investors, fundraising runway

**3.004 Recommendation:** Finmark ($100/mo)
**BUILD Alternative:** fs-tools (but not worth it - time to build > SaaS cost)

**Verdict:** **BUY Finmark**
- Reason: Templates save weeks, investor-ready outputs
- TCO: $1,200/year vs $6,000 to build
- **Winner:** BUY

---

### Scenario 2: SaaS Startup, Series A, 30 Employees, Snowflake

**Need:** Advanced scenarios, real-time metrics, data warehouse integration

**3.004 Recommendation:** Causal ($800/mo) or Mosaic ($2,000/mo)
**BUILD Alternative:** fs-tools + direct Snowflake queries

**Verdict:** **BUILD**
- Reason: Already have data infrastructure, technical team
- TCO (3 years): $16K (build) vs $28K (Causal) vs $72K (Mosaic)
- **Winner:** BUILD (saves $12K-56K)

---

### Scenario 3: Small Business, 5 Employees, No Technical Team

**Need:** Cash flow visibility, 13-week runway

**3.004 Recommendation:** Pulse ($59/mo)
**BUILD Alternative:** Not feasible (no Python developers)

**Verdict:** **BUY Pulse**
- Reason: No technical capability
- **Winner:** BUY (only option)

---

### Scenario 4: Bootstrapped SaaS, Profitable, Technical Founder

**Need:** Scenario planning, custom retention models

**3.004 Recommendation:** Finmark ($200/mo) or Causal ($500/mo)
**BUILD Alternative:** fs-tools with custom cohort analysis

**Verdict:** **BUILD**
- Reason: Custom retention models not available in SaaS
- Founder can build it themselves (opportunity cost low)
- **Winner:** BUILD (uniqu functionality + learning experience)

---

### Scenario 5: Mid-Market Company, 100 Employees, Finance Team

**Need:** Departmental budgeting, real-time dashboards, executive reporting

**3.004 Recommendation:** Mosaic ($2,000/mo) or Jirav ($400/mo)
**BUILD Alternative:** fs-tools + BI tool (Metabase, Superset)

**Verdict:** **HYBRID**
- Use Jirav for collaboration ($400/mo = $14.4K/3 years)
- Use fs-tools for custom analysis ($6K one-time)
- **Total:** $20.4K vs $72K (Mosaic only)
- **Winner:** HYBRID (saves $51.6K, keeps collaboration)

---

## When to BUILD: Decision Checklist

### ✅ BUILD if you have ALL of these:

1. ✓ Python developers on team (or yourself)
2. ✓ SaaS quote >$750/month (3-year breakeven)
3. ✓ Need custom models (SaaS can't do it)
4. ✓ Existing data infrastructure (warehouse, pipelines)
5. ✓ Technical users only (no need for UI)
6. ✓ Willing to maintain code (ongoing 1-2 hours/month)

### ❌ BUY if you have ANY of these:

1. ✗ No Python developers
2. ✗ SaaS <$300/month (not worth building)
3. ✗ Need collaboration (non-technical stakeholders)
4. ✗ Need mobile app (checking cash on phone)
5. ✗ Need vendor support (customer success, training)
6. ✗ Time-sensitive (need it working today)

---

## Hybrid Approach (Best of Both Worlds)

### Recommendation: Pulse + fs-tools

**Use Pulse for:**
- Daily cash visibility (executives check on phone)
- 13-week runway (board reporting)
- QuickBooks sync (automated)
- **Cost:** $89/mo = $3,204 / 3 years

**Use fs-tools for:**
- Advanced scenario planning (technical team)
- Monte Carlo simulations (risk quantification)
- Custom models (proprietary business logic)
- Sensitivity analysis (what-if testing)
- **Cost:** $6,000 one-time build

**Total 3-Year TCO:** $9,204

**vs Mosaic alone:** $72,000
**Savings:** $62,796 (87%)

---

## Summary: When to BUILD vs BUY

### BUILD When:
- SaaS >$750/month (significant savings)
- Custom models needed (SaaS can't do it)
- Data warehouse exists (integration is easy)
- Technical team available (Python proficiency)
- **Example:** Series A startup with Snowflake → BUILD (saves $56K/3 years)

### BUY When:
- SaaS <$300/month (not worth building)
- No technical team (training cost prohibitive)
- Need collaboration (non-technical users)
- Time-sensitive (need it today, not next week)
- **Example:** Small business, no developers → BUY Pulse ($59/mo)

### HYBRID When:
- Want both UI AND customization
- Have some technical capability
- Budget-conscious but need collaboration
- **Example:** Use Pulse ($89/mo) for executives + fs-tools for analysis

---

## Conclusion

**The question "BUILD vs BUY?" doesn't have one answer.**

**It depends on:**
1. Budget ($750/mo breakpoint)
2. Technical capability (Python developers?)
3. Customization needs (standard vs custom models?)
4. Collaboration needs (technical-only vs executives?)
5. Infrastructure (standalone vs data warehouse?)

**Our CLI tools (fs-parse, fs-scenario, fs-analyze) are NOT a replacement for SaaS for most companies.**

**BUT: For technical teams spending >$750/month on SaaS, CLI tools can:**
- Save $12K-56K over 3 years
- Enable custom models not available in SaaS
- Eliminate vendor lock-in
- Integrate directly with data warehouses

**Novel approach:** Applying Unix philosophy (small, composable tools) to financial analysis fills a gap between expensive SaaS and Excel chaos.
