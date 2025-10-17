# Use Case: Product-Led Growth (PLG) SaaS
## Pattern Analysis for Self-Service B2B Software

**Use Case ID**: UC-2.041-01
**Category**: Product Analytics
**Pattern**: PLG SaaS Company
**Last Updated**: 2025-10-08

---

## 1. USE CASE PROFILE

### Business Context
- **Industry**: B2B SaaS with self-service onboarding
- **Growth Model**: Product-Led Growth (free trial → paid conversion)
- **Customer Segment**: SMB to mid-market businesses
- **Team Size**: 10-50 employees (2-5 person product team)
- **Stage**: Seed to Series A (product-market fit established)
- **Revenue**: $500K-$5M ARR

### Example Companies
- Project management tools (Notion-style)
- Collaboration platforms (Slack-style)
- Developer tools (Vercel, Linear patterns)
- Design/creative tools (Figma-adjacent)

---

## 2. ANALYTICS REQUIREMENTS

### Key Questions to Answer
1. **Activation**: What actions predict trial-to-paid conversion?
2. **Feature Adoption**: Which features drive retention vs churn?
3. **Onboarding Friction**: Where do users drop off in first session?
4. **Expansion**: What usage patterns predict upgrade to higher tiers?
5. **Team Collaboration**: How does multi-user adoption affect retention?

### Technical Specifications
- **Event Volume**: 2M-20M events/month (growing 15-25% monthly)
- **User Base**: 5K-50K monthly active users
- **Data Retention**: 12-24 months historical data
- **Segmentation Needs**: Company/account-level analytics (critical for B2B)
- **Funnel Complexity**: 5-10 critical conversion funnels
- **Cohort Analysis**: Weekly cohort retention tracking
- **Real-time Requirements**: Near real-time dashboards for product team

### Integration Requirements
- SDKs: JavaScript (web app), mobile (if applicable)
- Data warehouse: Nice-to-have but not critical
- CRM integration: HubSpot/Salesforce sync for sales-assist touchpoints
- Reverse ETL: Product signals → CRM for high-intent leads

---

## 3. PROVIDER FIT ANALYSIS

### Mixpanel - 85% Fit

**Strengths:**
- Industry-standard for PLG companies (high credibility)
- Excellent account-level analytics (companies as entities)
- Clean UI that non-technical PMs can use independently
- Strong funnel and retention analysis out-of-box
- $50K startup credit program (covers 150M events/month for 12mo)

**Weaknesses:**
- Pricing becomes expensive post-credit at scale (>20M events/month)
- Limited session replay (need separate tool)
- Learning curve for advanced features

**Cost at Scale:**
- 0-6 months: $0 (startup program)
- 6-12 months: $0 (startup program continues)
- 12-24 months: $3,000-$8,000/year (10-20M events/month)

**Fit Score Breakdown:**
- Feature Fit: 95% (built for this use case)
- Cost Efficiency: 70% (good with credits, pricey after)
- Implementation Speed: 90% (fast SDK integration)
- Scalability: 80% (handles PLG scale well)
- Team Fit: 90% (PM-friendly)

---

### Amplitude - 88% Fit

**Strengths:**
- Best-in-class behavioral cohorts and retention analysis
- MTU pricing can be cheaper than event-based for high-engagement products
- Strong account/group analytics
- Excellent documentation and learning resources
- Acquired June (simple PLG focus) - may integrate best features
- Generous startup program (<$10M funding, <20 employees = 1 year free Growth plan)

**Weaknesses:**
- Steeper learning curve than competitors
- MTU pricing can get expensive if you have many low-engagement users
- Complex pricing model (hard to predict costs)

**Cost at Scale:**
- 0-12 months: $0 (startup program)
- 12-24 months: $5,000-$12,000/year (depends on MTU vs event pricing)

**Fit Score Breakdown:**
- Feature Fit: 95% (analytical depth matches PLG needs)
- Cost Efficiency: 75% (competitive with startup program)
- Implementation Speed: 85% (slightly more complex setup)
- Scalability: 90% (enterprise-proven)
- Team Fit: 85% (requires some analytics sophistication)

---

### PostHog - 78% Fit

**Strengths:**
- All-in-one: Analytics + session replay + feature flags + A/B testing
- Most cost-effective at scale ($0.00045/event after 1M free/month)
- Open-source option for ultimate cost control
- Fast-growing feature set competitive with incumbents
- No MTU vs event pricing confusion - simple event-based billing

**Weaknesses:**
- Less mature than Mixpanel/Amplitude (founded 2020)
- Account-level analytics improving but not as polished
- Fewer integrations than established players
- Open-source self-hosted only recommended to 300K events/month

**Cost at Scale:**
- 0-6 months: $0 (1M events free/month likely covers early stage)
- 6-12 months: $500-$1,500/year (2-5M events/month)
- 12-24 months: $2,500-$8,000/year (10-20M events/month)

**Fit Score Breakdown:**
- Feature Fit: 75% (growing but not feature-complete)
- Cost Efficiency: 95% (best TCO long-term)
- Implementation Speed: 90% (simple SDK)
- Scalability: 75% (proven but less track record)
- Team Fit: 80% (developer-friendly, improving PM UX)

---

### June - 70% Fit (Now Part of Amplitude)

**Strengths:**
- Purpose-built for B2B SaaS PLG
- Simplest onboarding (non-technical friendly)
- Auto-generated reports reduce setup time
- Company-level analytics core feature
- Free up to 1,000 active users/month

**Weaknesses:**
- Limited customization vs Mixpanel/Amplitude
- Acquired by Amplitude (future uncertain)
- Smaller feature set (intentionally simple)
- Less scalable for complex analytics needs

**Cost at Scale:**
- 0-6 months: $0 (under 1K users)
- 6-12 months: $1,788/year ($149/month)
- 12-24 months: $1,788-$3,588/year (depends on user growth)

**Fit Score Breakdown:**
- Feature Fit: 80% (PLG-optimized but limited depth)
- Cost Efficiency: 65% (user-based pricing can get expensive)
- Implementation Speed: 95% (fastest time-to-value)
- Scalability: 60% (may outgrow as analytics mature)
- Team Fit: 95% (easiest for non-technical teams)

---

### Heap - 65% Fit

**Strengths:**
- Automatic event tracking (no manual instrumentation)
- Retroactive analysis (define events after collection)
- Good for teams without dedicated analytics engineering

**Weaknesses:**
- No public pricing (requires sales contact)
- Reports suggest high cost ($30K-$85K/year for startups)
- Auto-tracking can create noise and data bloat
- Less favorable for cost-conscious PLG startups

**Cost at Scale:**
- Estimated: $7,000-$20,000/year minimum (based on user reports)

**Fit Score Breakdown:**
- Feature Fit: 75% (strong features but auto-tracking trade-offs)
- Cost Efficiency: 40% (expensive for startup budgets)
- Implementation Speed: 85% (fast - no event planning needed)
- Scalability: 80% (enterprise-grade)
- Team Fit: 75% (good for non-technical teams)

---

## 4. COST ANALYSIS (24-MONTH TCO)

### Scenario: PLG SaaS Growing from 5K → 30K MAU

**Assumptions:**
- Event volume: 2M → 15M events/month over 24 months
- Team: 3 product/data users
- Retention needs: 24 months historical data

**Provider TCO Comparison:**

| Provider   | Months 0-12 | Months 13-24 | 24-Month Total | Notes                          |
|------------|-------------|--------------|----------------|--------------------------------|
| Mixpanel   | $0          | $6,000       | $6,000         | Startup program year 1         |
| Amplitude  | $0          | $9,000       | $9,000         | Startup program year 1         |
| PostHog    | $300        | $5,500       | $5,800         | Best long-term TCO             |
| June       | $0          | $3,600       | $3,600         | User-based pricing (assuming 3K users) |
| Heap       | $14,000     | $18,000      | $32,000        | Estimated (no public pricing)  |

**Winner: PostHog for cost-conscious; Mixpanel/Amplitude for features+support**

---

## 5. DECISION FRAMEWORK

### Choose Mixpanel If:
- You qualify for startup program ($50K credit)
- Team has limited analytics expertise (need hand-holding)
- Brand credibility matters for fundraising
- Budget allows $500-$1K/month post-program

### Choose Amplitude If:
- You qualify for startup program (1 year free)
- You need deepest behavioral analytics capabilities
- High engagement per user (MTU pricing advantage)
- Analytics sophistication on team

### Choose PostHog If:
- Cost efficiency is top priority
- You value all-in-one platform (session replay + flags)
- Technical team comfortable with newer tools
- Want session replay without separate LogRocket/FullStory cost

### Choose June If:
- Team is non-technical (no data analysts)
- You need insights in <1 day of setup
- Simple analytics needs sufficient
- Under 1,000 active users (free tier)

---

## 6. MIGRATION RISK ASSESSMENT

**Low Risk Window**: First 6 months
- Switching providers is straightforward
- Limited dashboard dependency
- Short data history to migrate

**Medium Risk**: 6-18 months
- Team habits form around specific UIs
- Custom dashboards multiply
- Historical data becomes valuable

**High Risk**: 18+ months
- Deep integration into product development workflow
- Extensive custom reporting
- Cross-functional dependencies
- Switching cost: 40-80 hours engineering + relearning curve

**Recommendation**: Choose provider with 3-5x headroom for growth.

---

## 7. IMPLEMENTATION CHECKLIST

### Week 1: Setup
- [ ] Install SDK (web + mobile if applicable)
- [ ] Define 10-15 core events (sign up, activate feature X, invite teammate, upgrade)
- [ ] Set up user identification (link anonymous → identified)
- [ ] Configure account/company grouping

### Week 2-3: Core Dashboards
- [ ] Activation funnel (sign up → aha moment)
- [ ] Trial conversion funnel
- [ ] Weekly retention cohorts
- [ ] Feature adoption matrix
- [ ] Account health scoring

### Week 4: Operationalize
- [ ] Share dashboards with product/growth team
- [ ] Set up weekly review cadence
- [ ] Configure alerts for key metric drops
- [ ] Document event taxonomy

---

## 8. RECOMMENDED CHOICE

**PRIMARY**: Mixpanel (if startup program eligible) OR PostHog (if cost-sensitive)

**Rationale:**
- Mixpanel provides best balance of features, usability, and support for PLG-focused teams with funding
- PostHog offers superior TCO for teams comfortable with developer-first tools
- Both provide account-level analytics critical for B2B PLG

**BACKUP**: Amplitude (if startup program eligible and team has analytics depth)

**TRIGGER TO SWITCH**: If you exceed free tier limits and TCO crosses $1K/month, re-evaluate PostHog vs staying on current platform

---

END OF USE CASE ANALYSIS
