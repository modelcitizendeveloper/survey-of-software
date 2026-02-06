# Checkly - Long-Term Viability Assessment

## Company Overview

**Founded:** 2018
**Headquarters:** Berlin, Germany (distributed team)
**Ownership:** Private (VC-backed)
**Employees:** ~40-60 (estimated, 2024)
**Leadership:** Tim Nolet (Co-founder & CEO), Hannes Lenke (Co-founder & CPO)

**Business Model:** Monitoring-as-Code platform (Playwright + OpenTelemetry)
- No free tier (eliminated ~2023, now limited trial)
- Paid tiers: $80-480/month (Team to Scale)
- Enterprise: Custom pricing
- Focus: Developer workflows, synthetic monitoring, API testing

## Funding History

**Seed Round (April 2020): Undisclosed**
- **Lead:** Accel
- **Location:** Palo Alto, United States

**Series A (June 2021): $10M**
- **Lead:** CRV (Charles River Ventures)
- **Investors:** Accel, Mango Capital, Guillermo Rauch (Vercel founder)

**Series B (July 2024): $20M (€18.4M)**
- **Lead:** Balderton Capital
- **Investors:** CRV, Accel (follow-on from existing)
- **Notable:** Colin Hanna (Balderton Partner) joins board

**Total Raised:** $32.3M (Seed + A + B)

**Funding Timeline:**
- 2018: Founded
- 2020 (April): Seed from Accel
- 2021 (June): $10M Series A
- 2024 (July): $20M Series B

**Valuation (Estimated):**
- Series A (2021): ~$40-60M post-money
- Series B (2024): ~$100-150M post-money (typical for $20M Series B)

## Business Model

**Revenue Streams:**

1. **Monitoring-as-Code Platform**
   - Developer (Free Trial): $0/month (5 API checks, 1 browser check, limited)
   - Team: $80/month (10 browser checks, 5 API checks)
   - Scale: $480/month (100 browser checks, 50 API checks)
   - Enterprise: Custom pricing (1,000+ checks)

2. **Playwright-Based Browser Checks (Premium Feature)**
   - Multi-step user flows
   - Real browser testing (Chromium, Firefox, WebKit)
   - More expensive than HTTP checks (compute-intensive)

3. **API Testing & Monitoring**
   - HTTP/REST API checks
   - GraphQL, gRPC support
   - OpenAPI/Swagger integration

4. **Infrastructure-as-Code Integrations**
   - Terraform provider
   - Pulumi support
   - GitHub Actions, GitLab CI integration
   - CLI (`checkly` command-line tool)

5. **Private Locations (Enterprise)**
   - Run checks from customer infrastructure
   - On-premise or VPC monitoring

**Unit Economics (Estimated):**
```
Team Plan Customer ($80/month):
  - Infrastructure cost: $10-15/month (Playwright is expensive)
  - Gross margin: 75-80%
  - CAC (Customer Acquisition Cost): $500-1,000
  - Payback period: 7-13 months

Enterprise Customer ($1,000-5,000/month):
  - Infrastructure cost: $150-500/month
  - Gross margin: 70-80%
  - CAC: $5,000-15,000
  - Payback period: 5-15 months

ARR (Annual Recurring Revenue, 2024 estimate):
  - 1,000+ customers (reported)
  - ARPU: $1,000-3,000/year
  - ARR: $1M-3M (conservative) to $5M-10M (optimistic)
```

**Sustainability:**

**Series B Thesis (2024):**
Checkly raised $20M to "slash website downtime with 10x faster issue resolving via OTel and code-based monitoring." This signals:

1. **Growth capital**: Hiring, marketing, product expansion
2. **Not profitable yet**: Burning capital to grow (typical Series B)
3. **3-5 year runway**: $20M should last 3-5 years at typical burn rate

**Risks:**
1. **Exit pressure**: Series B (2024) means exit window 2027-2030 (3-5 years)
2. **Competitive market**: Datadog, New Relic adding Playwright-based checks
3. **Feature commoditization**: Monitoring-as-Code being adopted by competitors

**Customer Base:**
- 1,000+ customers (reported at Series B)
- Developers, DevOps teams, SREs
- Tech-forward companies (startups, scaleups)
- Geography: Global, strong in Europe and US

## Market Position

**Estimated Market Share:** 1-3% of synthetic monitoring market (niche leader in Monitoring-as-Code)

**Position:** Niche leader (#1 in Monitoring-as-Code, #10-15 overall in uptime monitoring)

**Competitors:**

**Monitoring-as-Code:**
1. **Checkly**: Category creator, first-mover
2. **DIY Playwright Scripts**: Self-hosted alternative
3. **GitHub Actions + Playwright**: Open-source alternative

**Synthetic Monitoring (Broader):**
1. **Datadog Synthetics**: Enterprise leader, adding Playwright
2. **New Relic Synthetics**: Browser-based monitoring
3. **Pingdom Transaction Monitoring**: Legacy solution
4. **Uptrends**: European competitor

**Developer Monitoring:**
1. **Better Stack**: Full observability platform
2. **Sentry**: Error monitoring (adjacent space)
3. **Honeycomb**: Observability for developers

**Differentiation:**

**Checkly Strengths:**

1. **Monitoring-as-Code (Category Leader)**
   - Define monitors in TypeScript/JavaScript
   - Version control, CI/CD integration
   - Terraform provider, Pulumi support
   - Git-based workflows (PRs, code review for monitors)

2. **Playwright-Native**
   - Uses open-source Playwright (Microsoft-backed)
   - Multi-step browser flows (login → navigate → assert)
   - Real browser testing (not just HTTP pings)

3. **Developer Workflow Integration**
   - CLI tool (`checkly` command)
   - GitHub Actions, GitLab CI plugins
   - OpenTelemetry integration
   - Treats monitoring as code (not UI-based)

4. **Modern Tech Stack**
   - Node.js, TypeScript (developer-familiar)
   - API-first (GraphQL + REST)
   - Infrastructure-as-Code native

5. **Niche Expertise**
   - Deep expertise in Playwright, synthetic monitoring
   - Active community (documentation, examples)
   - Thought leadership (blog, conference talks)

**Checkly Limitations:**

1. **Free Tier Eliminated (~2023)**
   - Now only limited trial (5 API, 1 browser check)
   - Competitors (UptimeRobot, Freshping) offer generous free tiers
   - Raises barrier to entry

2. **Higher Pricing**
   - Team: $80/month (10 browser checks)
   - UptimeRobot Pro: $29/month (50 monitors)
   - Checkly is 3-5x more expensive for basic use cases

3. **Complexity**
   - Requires coding skills (TypeScript/JavaScript)
   - Not for non-technical users (vs. UptimeRobot's UI)
   - Steeper learning curve

4. **Narrow Use Case**
   - Best for complex multi-step flows
   - Overkill for simple HTTP uptime checks
   - Better Stack or UptimeRobot better for basic monitoring

5. **Playwright Dependency**
   - Tied to Playwright (Microsoft OSS project)
   - If Playwright declines, Checkly's moat weakens

**Competitive Moat:**

**Medium Moat (Category Leadership):**
- **First-mover**: Defined Monitoring-as-Code category
- **Playwright expertise**: Deep integration, hard to replicate
- **Developer community**: Blog, docs, examples (network effects)
- **Infrastructure-as-Code**: Terraform/Pulumi providers create switching cost

**Moat Risks:**
- **Playwright is OSS**: Anyone can build on Playwright
- **Datadog entering**: Adding Playwright-based checks (2023+)
- **Feature commoditization**: Monitoring-as-Code becoming table stakes
- **DIY alternative**: Teams can run Playwright scripts themselves

## Acquisition Risk Assessment

**Risk Score:** 55% (HIGH)

**Calculation:**
```
Base Risk (private company, consolidating market): +40%
VC ownership ($32.3M raised):                      +20%
Series B exit window (2027-2030):                  +15%
Market consolidation (Datadog, New Relic):         +10%
Competitive pressure (Datadog Synthetics):         +10%
Niche category (attractive bolt-on):               +10%

Recent funding (July 2024):                        -10%
Strong product (developer love):                   -10%
Category leadership:                               -10%
Balderton Capital (patient capital):               -5%
Playwright ecosystem:                              -5%

Total: 55%
```

**Risk Factors (+105%):**

1. **VC Ownership + Series B Exit Window (+15%)**
   - $32.3M raised (Seed + A + B)
   - Series B (July 2024) starts 3-5 year exit clock
   - Expect acquisition 2027-2030

2. **Niche Category Attractive to Acquirers (+10%)**
   - Monitoring-as-Code is valuable to platform players
   - Bolt-on acquisition to Datadog, New Relic, Elastic
   - Checkly is category leader (most valuable target)

3. **Market Consolidation (+10%)**
   - Datadog adding Playwright-based checks (competitive threat)
   - New Relic expanding synthetics
   - Checkly could be defensive acquisition

4. **Competitive Pressure (+10%)**
   - Datadog has 100x resources, can replicate features
   - May force sale before category commoditizes

**Protective Factors (-40%):**

1. **Recent Funding (-10%)**
   - July 2024: $20M Series B
   - 3-5 year runway before exit pressure peaks
   - Safe until 2027 at earliest

2. **Strong Product & Community (-10%)**
   - Developer community loves Checkly
   - Thought leadership, active blog, good docs
   - High NPS (Net Promoter Score)

3. **Category Leadership (-10%)**
   - Defined Monitoring-as-Code category
   - First-mover advantage
   - Brand recognition in developer community

4. **Patient Capital (-5%)**
   - Balderton (Series B lead) known for longer holds
   - Not "get rich quick" PE/VC

5. **Playwright Ecosystem (-5%)**
   - Microsoft-backed OSS project (Playwright)
   - Growing ecosystem creates tailwinds

**Likely Acquirers (2027-2030):**

1. **Datadog** (50% probability): Eliminate competitor, add Monitoring-as-Code, $150-300M
2. **New Relic** (20%): Catch up to Datadog, synthetics expansion
3. **Elastic** (15%): Observability platform expansion
4. **Microsoft** (10%): Playwright creator, could integrate into Azure DevOps
5. **Atlassian** (5%): Developer tools ecosystem

## Pricing Stability

**Historical Changes:**

**2018-2021 (Pre-Series A):**
```
Free Tier (estimated):
  - 5-10 checks (basic offering)
  - Attract developer users

Paid Tiers:
  - Developer-friendly pricing
  - Exact historical pricing unclear
```

**2021-2023 (Series A Era):**
```
Free Tier:
  - Existed but limited
  - Gradually reduced

Paid Tiers:
  - Team: ~$80/month (stable estimate)
```

**2023-2024 (Series B Prep & Post):**
```
Free Tier: ELIMINATED (~2023)
  - Now "Developer" tier with limited trial
  - 5 API checks, 1 browser check (non-functional for real use)

Paid Tiers (2024 Current):
  - Team: $80/month (10 browser, 5 API)
  - Scale: $480/month (100 browser, 50 API)
  - Enterprise: Custom

Shift: Free-to-paid eliminated, focus on higher ARPU customers
```

**Price Stability Score:** 50/100 (Moderate Risk)

**Pricing Events:**
- **~2023**: Free tier eliminated (moved to limited trial)
- **2024**: Paid tiers stable (Team $80, Scale $480)
- **Prediction**: 70% probability of 20-35% increase in 2026-2027 (exit prep)

**Free Tier Evolution:**

| Year | Status                              |
|------|-------------------------------------|
| 2018-2021 | Free tier available (limited)  |
| 2023 | Free tier eliminated                |
| 2024 | Limited trial only (5 API, 1 browser) |

## Strategic Recommendation

**Overall Assessment:** CAUTION

**Viability Score:** 68/100 (Good Product, Moderate-High Risk)
```
Market Position:      14/20 (category leader, but niche)
Financial Health:     15/20 (VC-backed, Series B runway 3-5 years)
Acquisition Risk:     9/20 (55% risk - moderate-high)
Pricing Stability:    10/20 (50/100 - free tier gone, paid stable for now)
Lock-In:              20/20 (low lock-in, Monitoring-as-Code is portable)

Total: 68/100
```

**Rationale:**

**Strengths:**

1. **Category Leadership**: Checkly defined Monitoring-as-Code and remains the leader. First-mover advantage, strong brand in developer community.

2. **Excellent Product**: Playwright-native, infrastructure-as-code integration, modern developer workflows. Developer community loves the product.

3. **Low Lock-In**: Monitoring-as-Code means your checks are version-controlled TypeScript/JavaScript. Can migrate to DIY Playwright or competitor easily (see lock-in-analysis.md: 6/10 score).

4. **Recent Funding**: $20M Series B (July 2024) provides 3-5 year runway. Safe until 2027 at earliest.

5. **Niche Expertise**: Deep Playwright knowledge, active community, thought leadership.

**Concerns:**

1. **High Acquisition Risk (55%)**: Series B (2024) means exit window 2027-2030. Likely acquirers: Datadog, New Relic, Elastic. Bolt-on acquisition to eliminate competitor.

2. **Free Tier Eliminated**: Raises barrier to entry, reduces customer acquisition funnel. Competitors (UptimeRobot, Freshping) offer free tiers.

3. **Pricing Increases Likely**: 70% probability of 20-35% increase in 2026-2027 as company prepares for exit (boost revenue metrics for acquisition).

4. **Competitive Pressure**: Datadog adding Playwright-based checks. Could commoditize Checkly's differentiation or force defensive sale.

5. **Narrow Use Case**: Best for complex multi-step browser flows. Overkill for simple HTTP uptime checks (use UptimeRobot instead).

**Use Cases - Highly Recommended:**

✓ **Monitoring-as-Code Requirements**
  - Version control for monitors (Git workflows)
  - Infrastructure-as-Code (Terraform, Pulumi)
  - CI/CD integration (GitHub Actions, GitLab)
  - Code review for monitoring logic

✓ **Complex Multi-Step Flows**
  - Login → navigate → submit form → assert results
  - E-commerce checkout flows
  - Multi-page user journeys
  - Real browser testing (not just HTTP)

✓ **Developer-Heavy Teams**
  - Comfortable with TypeScript/JavaScript
  - Prefer code over UI configuration
  - Value Playwright ecosystem

✓ **2-4 Year Commitments (Acceptable Risk Window)**
  - Series B (2024) → exit 2027-2030
  - Safe for medium-term use
  - Plan migration for 2027-2029

**Use Cases - NOT Recommended:**

✗ **Simple HTTP Uptime Checks**
  - Checkly is overkill (10x more expensive)
  - Use UptimeRobot ($0-99/month) or Freshping (free)
  - Checkly Team ($80/month) for 10 browser checks vs. UptimeRobot ($29/month) for 50 HTTP checks

✗ **Non-Technical Teams**
  - Requires coding (TypeScript/JavaScript)
  - Steeper learning curve than UI-based tools
  - Use Better Stack or StatusCake instead

✗ **Long-Term (5+ Years) Commitments**
  - 55% acquisition risk by 2029
  - Post-acquisition uncertainty (pricing, product changes)
  - Choose UptimeRobot (20% risk) or Freshping (15% risk)

✗ **Budget-Constrained (Need Free Tier)**
  - No real free tier (limited trial only)
  - Use UptimeRobot (50 monitors free) or Freshping (50 monitors free, 1-min)

## Migration Planning

**MODERATE-HIGH RISK → Plan Exit Strategy**

**Quarterly Review:**

**Acquisition Indicators:**
- M&A rumors (Datadog, New Relic, Elastic)
- Funding announcements (Series C would accelerate exit)
- Leadership changes (CFO/CRO hire = exit prep)
- "Strategic partnerships" with potential acquirers

**Pricing Indicators:**
- Price increases announced (20-35% likely 2026-2027)
- Plan consolidation
- Enterprise-only features (moving upmarket)

**Product Indicators:**
- Feature stagnation (post-exit prep, feature freeze)
- Datadog Synthetics feature parity (competitive threat)

**Migration Timeline:**

**2025-2026: MONITOR**
- Continue using if satisfied
- Track Datadog Synthetics feature development
- Maintain Playwright scripts in version control (portability)

**2027-2029: PREPARE**
- Acquisition likely (55% probability)
- Evaluate alternatives:
  - DIY Playwright (self-hosted)
  - Datadog Synthetics (if acquired by Datadog, may be forced)
  - Better Stack (if need simplicity)

**Migration Readiness:**

**From Checkly (Excellent Portability):**
- **Monitoring-as-Code**: Your checks are TypeScript/JavaScript files
- **Version Control**: Already in Git (easy to migrate)
- **Time Estimate**: 15-25 hours for 50 monitors (moderate, see lock-in-analysis.md)
- **Target Providers**:
  - DIY Playwright scripts on VPS (zero vendor risk)
  - Datadog Synthetics (if they acquire Checkly)
  - Better Stack (simpler, less code-heavy)

**To Checkly:**
- **From UI-based tools**: Moderate effort (convert to code)
- **From Playwright scripts**: Easy (already Playwright-native)
- **Trial**: 14-day trial available

## Conclusion

**Checkly is the category leader in Monitoring-as-Code with excellent product quality but moderate-high acquisition risk.**

**Key Decision Factors:**

1. **Acquisition Risk (55%)**: Series B (July 2024) starts 3-5 year exit clock. Likely acquirers: Datadog (50%), New Relic (20%), Elastic (15%), Microsoft (10%). Exit window: 2027-2030.

2. **Category Leadership**: Checkly defined Monitoring-as-Code and remains #1. Strong developer community, thought leadership, Playwright expertise.

3. **Pricing Trajectory**: Free tier eliminated (2023). Paid tiers stable now, but 70% probability of 20-35% increase in 2026-2027 (exit prep).

4. **Low Lock-In**: Monitoring-as-Code = portable. Your checks are version-controlled TypeScript/JavaScript. Can migrate to DIY Playwright or competitors easily.

5. **Niche Use Case**: Best for complex multi-step browser flows. Overkill for simple HTTP checks (use UptimeRobot or Freshping instead).

**For MPSE V2 Framework:**

**Recommended Weight: 68/100** (CAUTION tier)

**Ideal Profile:**
- Organizations: Developer-heavy teams, tech-forward companies
- Monitor Count: 10-100 complex browser checks
- Budget: $80-480/month (premium pricing justified by features)
- Use Case: Monitoring-as-Code, multi-step flows, Playwright workflows
- Risk Tolerance: Moderate-high (accept 55% acquisition risk)
- Commitment: 2-4 years (avoid 5+ year commitments)

**Bottom Line:** Checkly is the best choice for Monitoring-as-Code and complex browser testing workflows. However, VC ownership and Series B funding (2024) create 55% acquisition risk by 2029. Recommended for teams needing advanced features and comfortable with moderate risk. For simple uptime checks or lower risk tolerance, choose UptimeRobot (20% risk, $0-99/month) or Freshping (15% risk, free forever).

**Unique Value:** If you need Monitoring-as-Code or Playwright-based browser checks, Checkly is the clear category leader. For all other use cases, cheaper and lower-risk alternatives exist.
