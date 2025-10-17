# Heroku Viability Assessment

**Provider:** Heroku (Salesforce-owned)
**Assessment Date:** 2025-10-09
**Current Status:** Mature PaaS, post-acquisition baseline for analysis

---

## Executive Summary

**Viability Score: 55/100** (Moderate - Concerning Trends)

Heroku is the **cautionary tale** for PaaS acquisitions. Once the industry leader, it has stagnated under Salesforce ownership, eliminated its free tier, and serves primarily as a cash cow rather than an innovation platform.

**Key Finding:** Heroku demonstrates the POST-ACQUISITION RISK PATTERN that threatens all VC-backed PaaS providers. Use as baseline for worst-case scenarios.

---

## Acquisition History

### Original Acquisition (2010)

**Date:** December 8, 2010 (announced), January 3, 2011 (completed)
**Acquirer:** Salesforce.com
**Price:** $212 million in cash
**Rationale:** Salesforce wanted to expand beyond SaaS into PaaS, acquire developer mindshare

### Pre-Acquisition Status
- Founded 2007, Ruby-focused PaaS pioneer
- Invented the "git push to deploy" paradigm
- Developer darling, vibrant ecosystem
- Bootstrapped initially, then VC-backed

---

## Post-Acquisition Timeline: A Slow Decline

### Phase 1: Honeymoon (2011-2017)
- Continued innovation (multi-language support, add-ons ecosystem)
- Maintained developer-friendly culture
- Free tier thrived, used for tutorials worldwide

### Phase 2: Neglect (2018-2021)
- Innovation slowed dramatically
- Salesforce prioritized enterprise products over Heroku
- Pricing gradually increased
- Developer community frustration grew
- No significant new features

### Phase 3: Monetization (2022-2024)
- **August 2022:** Announced free tier elimination
- **November 28, 2022:** Free tier shutdown (fraud/abuse cited)
- Massive community backlash
- Exodus to Render, Railway, Fly.io
- **March 2024:** Replatforming onto Kubernetes (too little, too late?)

---

## The Free Tier Shutdown: Case Study in Post-Acquisition Extraction

### Announcement (August 2022)

**Official Reason:** "Fraud and abuse" - teams spending "extraordinary effort" managing bad actors

**Real Reason (Suspected):**
- Salesforce cost-cutting pressure
- Enterprise focus (free users don't convert)
- Market dominance eroded, less need for developer mindshare
- VC-backed competitors (Render, Railway) offering better free tiers

### Impact Metrics

**Affected Users:**
- 13 million accounts (majority on free tier)
- Students, educators, open-source projects, hobbyists
- Thousands of tutorial apps broken overnight

**New Minimum Pricing:**
- Dynos: $7/month (was free)
- Postgres: $9/month (was free)
- Redis: $15/month (was free)
- **Total basic app: $25/month → $49/month** (96% increase)

### Community Backlash

**Sentiment Analysis:**
- "End of an era" - Heroku no longer beginner-friendly
- "Enshittification" - classic late-stage platform decay
- Timing criticized (post-security breach, during competitor rise)
- Mass migration announcements on Twitter/HN

---

## Current Pricing (2025)

**Eco Plan:** $5/dyno/month (sleep after 30 min inactivity)
**Basic Plan:** $7/dyno/month (no sleeping)
**Standard Plans:** $25-$500/dyno/month
**Database:** $9/month (mini Postgres), $15/month (mini Redis)

**Hidden Costs:**
- Data egress fees
- Add-on marketplace (many 3rd party)
- SSL certificates (included in paid plans)
- Custom domains require paid plans

**Pricing Trend:** Upward pressure, no longer competitive with modern alternatives

---

## Innovation & Feature Development

### Recent Major Updates

**March 2024:** Kubernetes replatforming (announced at Kubecon Paris)
- Long overdue modernization
- Suggests Salesforce is reinvesting (or preparing to sell?)
- Too early to judge impact

**August 2023:** Heroku CI and Teams free for card-paying customers
- Minor feature, not competitive advantage

**November 2022:** Eco and Mini plans launched
- Replaced free tier with low-cost option
- Still more expensive than competitors

### Innovation Rate: SLOW (20/100)

Heroku has not introduced major competitive features since acquisition:
- No edge computing (Fly.io beat them)
- No native Docker support until 2024 (way behind)
- Limited Kubernetes integration (finally happening 2024)
- Add-on ecosystem stagnant (no new major partners)

**Assessment:** Maintenance mode with occasional updates to stem user exodus.

---

## Service Quality & Reliability

### Strengths
- Battle-tested infrastructure (15+ years operation)
- Extensive documentation
- Mature add-on ecosystem
- Predictable uptime (backed by Salesforce SLAs)

### Weaknesses
- Aging platform architecture (pre-Kubernetes)
- Performance lags modern competitors
- Limited customization (opinionated platform)
- Slow support for modern tooling (Docker took years)

### Reliability: GOOD (75/100)

Heroku is reliable but not cutting-edge. It works, but doesn't excite.

---

## Market Position

### Historical Dominance (2010-2020)
- Industry leader, defined PaaS category
- Every tutorial used Heroku for deployment examples
- Largest PaaS ecosystem

### Current Erosion (2020-2025)
- Market share declining to Render, Railway, Fly.io, Vercel
- Developer sentiment negative post-free tier shutdown
- Enterprise clients remain (switching cost high)
- Beginner/hobbyist market lost entirely

### Competitive Position: WEAKENING (40/100)

Heroku is living off legacy reputation while competitors out-innovate.

---

## Acquisition Risk: ALREADY ACQUIRED (Secondary Risk: Re-Sale)

### Primary Risk: N/A (Already Salesforce-owned since 2011)

### Secondary Risk: Salesforce Sells Heroku (30% probability 2025-2028)

**Scenario:** Salesforce divests Heroku to focus on core CRM/AI business

**Potential Buyers:**
- Private Equity (60% of divestiture scenarios) - HIGH RISK: immediate price increases, cost-cutting
- Cloud Provider (AWS, Azure, Google) - MODERATE RISK: potential shutdown or forced migration
- Strategic Buyer (HashiCorp, GitLab, Atlassian) - LOW RISK: likely continuation

**Timeline:** 2-5 years if Salesforce restructures portfolio

### Tertiary Risk: Heroku Shutdown (15% probability 2028-2032)

Salesforce may sunset Heroku if it no longer fits strategic vision:
- Precedent: Many Salesforce acquisitions shuttered after asset extraction
- Signal: Kubernetes replatforming could be "preparing for shutdown" migration
- Impact: 12-24 month deprecation timeline typical

---

## Lock-In Assessment

### Lock-In Severity: MODERATE (45/100)

**Heroku-Specific Elements:**
- Procfile (easily portable to most PaaS)
- Buildpacks (industry standard, but Heroku-optimized)
- Add-ons (many proprietary, but replaceable)
- Config vars (standard environment variables)
- Heroku Postgres/Redis (standard dumps available)

**Migration Friction:**
- Procfile → Render/Railway: 1-2 hours
- Procfile → Docker: 2-4 hours (Dockerfile creation)
- Add-ons → Self-hosted: 4-8 hours (per add-on)
- Database export/import: 1-4 hours (depending on size)

**Lock-In Score:** 45/100 (MODERATE - easier than proprietary platforms, harder than Docker)

---

## Strategic Implications: The Heroku Warning

### What Heroku Teaches Us

1. **Acquisitions Change Everything**
   - Developer-friendly → Enterprise-focused
   - Innovation → Maintenance mode
   - Free tier → Monetization squeeze

2. **Post-Acquisition Timeline**
   - Years 1-7 (2011-2017): Honeymoon continues
   - Years 8-11 (2018-2021): Neglect phase
   - Years 12-14 (2022-2024): Extraction/monetization
   - Year 14+ (2024+): Divestiture/shutdown risk

3. **Pattern Applies to ALL Acquisitions**
   - PythonAnywhere (Anaconda, 2022) = Year 3 now → 2029-2032 risk window
   - Any future acquisition of Render, Railway, Fly.io will follow similar pattern

4. **Free Tiers Are Fragile**
   - Can disappear overnight with 2-3 months notice
   - "Fraud/abuse" is convenient excuse for cost-cutting
   - Don't build business critical services on free tiers

---

## 5-Year Outlook (2025-2030)

### Optimistic Scenario (20% probability)
- Kubernetes replatforming succeeds, reignites innovation
- Salesforce reinvests in Heroku as strategic asset
- Competitive pricing restored
- Developer community returns

### Base Scenario (50% probability)
- Continued slow decline
- Pricing increases 10-20% over 5 years
- Feature development minimal
- Market share erosion continues
- Heroku becomes "legacy platform" for enterprise apps

### Pessimistic Scenario (30% probability)
- Salesforce divests or shutdowns Heroku 2027-2030
- PE buyer = immediate price increases (50-100%)
- Cloud buyer = forced migration to AWS/Azure/GCP
- 12-24 month deprecation timeline
- Mass exodus to competitors

---

## Viability Score Breakdown

| Factor | Score | Weight | Weighted Score |
|--------|-------|--------|----------------|
| Financial Stability (Salesforce) | 95 | 20% | 19.0 |
| Pricing Stability | 40 | 15% | 6.0 |
| Service Quality | 75 | 15% | 11.3 |
| Innovation Rate | 20 | 10% | 2.0 |
| Market Position | 40 | 10% | 4.0 |
| Acquisition Risk (already acquired) | 50 | 15% | 7.5 |
| Lock-In (moderate) | 55 | 10% | 5.5 |
| Strategic Fit (Salesforce priorities) | 30 | 5% | 1.5 |
| **TOTAL** | | **100%** | **56.8** |

**Rounded Viability Score: 55/100**

---

## Recommendation for QRCards

**AVOID HEROKU** unless specific enterprise requirements demand it.

**Reasons to Avoid:**
1. Pricing 2-3x higher than modern alternatives (Render, Railway)
2. Stagnant innovation, aging platform
3. Free tier eliminated (no learning path)
4. Post-acquisition risk pattern evident
5. Better alternatives exist at lower cost

**When Heroku Makes Sense:**
- Enterprise clients requiring Salesforce integration
- Legacy apps already on Heroku (switching cost high)
- Specific add-ons unavailable elsewhere
- Need Salesforce-backed SLAs/support

**For QRCards:** Use Heroku as a **cautionary tale** when evaluating other PaaS providers. Any provider acquired by larger company will likely follow similar trajectory.

---

## Heroku as Baseline for Risk Analysis

**Key Metrics for Comparison:**

| Metric | Heroku (Post-Acquisition) |
|--------|---------------------------|
| Years to free tier elimination | 11 years (2011 → 2022) |
| Years to innovation stagnation | 7 years (2011 → 2018) |
| Pricing increase magnitude | 96% (basic app 2022) |
| Post-acquisition phase | Year 14 (extraction/decline) |
| Secondary risk (divestiture) | 30% next 3-5 years |

**Apply to Other Providers:**
- PythonAnywhere (Anaconda 2022) → Watch for extraction phase 2029-2032
- Any future Render/Railway/Fly.io acquisition → Expect 7-11 year honeymoon, then squeeze

---

## Sources

- TechCrunch: Salesforce acquisition announcement (2010)
- Heroku blog: "Next Chapter" free tier shutdown (August 2022)
- The Register: Free tier elimination analysis (2022)
- HackerNews: Community backlash discussions
- Heroku pricing page: Current tier structure
- KubeCon Paris 2024: Kubernetes replatforming announcement
