# Use Case: Consumer Mobile App
## Pattern Analysis for High-Volume Mobile Applications

**Use Case ID**: UC-2.041-02
**Category**: Product Analytics
**Pattern**: Consumer Mobile App
**Last Updated**: 2025-10-08

---

## 1. USE CASE PROFILE

### Business Context
- **Industry**: Consumer mobile applications (iOS + Android)
- **Growth Model**: Viral/paid acquisition → engagement → monetization
- **Customer Segment**: Direct-to-consumer (B2C)
- **Team Size**: 5-30 employees (1-3 person product team early stage)
- **Stage**: Pre-seed to Series A
- **Revenue Model**: Freemium, subscriptions, in-app purchases, or ads
- **User Base**: 10K-500K+ monthly active users (high volume potential)

### Example Apps
- Social networking apps
- Fitness/health tracking apps
- Gaming/entertainment apps
- Lifestyle/utility apps
- Content consumption apps

---

## 2. ANALYTICS REQUIREMENTS

### Key Questions to Answer
1. **User Acquisition**: Which channels drive highest-quality users?
2. **Onboarding**: What % of installs complete onboarding? Where do they drop?
3. **Engagement**: What is D1/D7/D30 retention by cohort?
4. **Monetization**: Which behaviors predict subscription conversion?
5. **Feature Usage**: Which features drive daily active usage?
6. **Session Patterns**: How long/frequent are sessions? What drives re-opens?
7. **Platform Differences**: iOS vs Android behavior patterns

### Technical Specifications
- **Event Volume**: 500K-50M+ events/month (high event density per user)
- **User Base**: 10K-500K monthly active users (potential for rapid growth)
- **Data Retention**: 6-12 months (shorter than B2B due to user churn)
- **Segmentation Needs**: User-level (not account-level like B2B)
- **Funnel Complexity**: 3-7 critical funnels (simpler than B2B)
- **Cohort Analysis**: Daily/weekly retention cohorts essential
- **Real-time Requirements**: Real-time monitoring for acquisition campaigns

### Integration Requirements
- SDKs: iOS (Swift), Android (Kotlin/Java), potentially React Native/Flutter
- Attribution: AppsFlyer, Adjust, or Branch integration critical
- Push Notifications: Integration with Firebase/OneSignal
- A/B Testing: Built-in experimentation or Optimizely integration
- Data Warehouse: Usually not needed at early stage

---

## 3. PROVIDER FIT ANALYSIS

### Amplitude - 90% Fit

**Strengths:**
- Industry leader for mobile consumer apps (Peloton, Headspace use it)
- MTU pricing model favors high-engagement apps (many events per user)
- Excellent mobile SDKs (iOS, Android, React Native, Flutter)
- Strong retention/cohort analysis purpose-built for mobile
- Behavioral cohorting helps identify power users
- Startup program: 1 year free Growth plan (<$10M funding)

**Weaknesses:**
- MTU pricing can hurt apps with many low-engagement users
- Learning curve steeper than simpler alternatives
- May be overkill for very early-stage MVPs

**Cost at Scale:**
- 0-12 months: $0 (startup program if eligible)
- 12-24 months: $4,000-$15,000/year (50K-200K MTU)

**Fit Score Breakdown:**
- Feature Fit: 95% (mobile-first feature set)
- Cost Efficiency: 80% (MTU model matches high-engagement)
- Implementation Speed: 85% (mature SDKs)
- Scalability: 95% (handles massive mobile scale)
- Team Fit: 85% (requires some analytics knowledge)

---

### Mixpanel - 88% Fit

**Strengths:**
- Historically strong in mobile (Instagram, Uber used early)
- Event-based pricing can be cheaper for sporadic-use apps
- Clean UI for mobile-specific funnels
- Strong mobile SDK support
- Startup program: $50K credit (covers 150M events for 12mo)
- Good A/B testing integration

**Weaknesses:**
- Event-based pricing can get expensive for high-engagement apps
- Less mobile-specialized than Amplitude (more general-purpose)
- Credit system vs MTU adds pricing complexity

**Cost at Scale:**
- 0-12 months: $0 (startup program)
- 12-24 months: $3,000-$10,000/year (10-30M events/month)

**Fit Score Breakdown:**
- Feature Fit: 90% (strong mobile support)
- Cost Efficiency: 80% (competitive with credits)
- Implementation Speed: 90% (simple SDK integration)
- Scalability: 90% (proven at scale)
- Team Fit: 90% (PM-friendly)

---

### PostHog - 75% Fit

**Strengths:**
- Most cost-effective option (30-50% cheaper at scale)
- Event-based pricing simple and predictable
- Mobile SDKs improving rapidly
- Session replay now supports mobile (newer feature)
- All-in-one: Analytics + feature flags + A/B testing
- $0.00045/event after 1M free/month

**Weaknesses:**
- Less mature mobile SDKs than Amplitude/Mixpanel
- Fewer mobile-specific features (no automatic screen tracking parity)
- Smaller community for mobile-specific questions
- Attribution integrations less established

**Cost at Scale:**
- 0-12 months: $500-$2,000/year (2-5M events/month)
- 12-24 months: $4,000-$12,000/year (10-30M events/month)

**Fit Score Breakdown:**
- Feature Fit: 70% (improving but not mobile-specialized)
- Cost Efficiency: 95% (best long-term TCO)
- Implementation Speed: 80% (SDK setup straightforward)
- Scalability: 80% (cloud handles scale well)
- Team Fit: 75% (more developer-oriented)

---

### Heap - 60% Fit

**Strengths:**
- Automatic event capture (no manual mobile instrumentation)
- Retroactive analysis useful for fast-moving mobile teams
- Good for teams without mobile analytics engineers

**Weaknesses:**
- Auto-capture on mobile creates massive event bloat (expensive)
- No public pricing (reports of $30K-$85K/year)
- Mobile auto-capture less reliable than web
- Privacy concerns with auto-capture on mobile (app store policies)

**Cost at Scale:**
- Estimated: $15,000-$50,000/year (based on user reports)

**Fit Score Breakdown:**
- Feature Fit: 65% (auto-capture trade-offs on mobile)
- Cost Efficiency: 35% (prohibitive for lean mobile teams)
- Implementation Speed: 85% (fast but risky without planning)
- Scalability: 75% (handles scale but costly)
- Team Fit: 70% (good for non-technical but expensive)

---

### Firebase Analytics (Google) - 70% Fit

**Strengths:**
- FREE unlimited events
- Native integration with Firebase ecosystem (Auth, Database, Cloud Messaging)
- Automatic screen tracking
- Built-in attribution via Google Ads
- Google Analytics 4 integration

**Weaknesses:**
- Limited behavioral analysis (not true product analytics)
- Basic cohort/funnel capabilities
- Data ownership concerns (Google property)
- Limited export options without BigQuery
- UI less sophisticated than dedicated tools

**Cost at Scale:**
- Always free

**Fit Score Breakdown:**
- Feature Fit: 60% (basic analytics, not behavioral depth)
- Cost Efficiency: 100% (free)
- Implementation Speed: 95% (if already using Firebase)
- Scalability: 100% (Google infrastructure)
- Team Fit: 85% (simple UI)

---

## 4. COST ANALYSIS (24-MONTH TCO)

### Scenario: Consumer Mobile App Growing from 10K → 150K MAU

**Assumptions:**
- Event volume: 1M → 15M events/month over 24 months
- High engagement: Average 50 events/user/month
- iOS + Android support
- 2 product team members using analytics

**Provider TCO Comparison:**

| Provider         | Months 0-12 | Months 13-24 | 24-Month Total | Notes                               |
|------------------|-------------|--------------|----------------|-------------------------------------|
| Amplitude        | $0          | $8,000       | $8,000         | MTU pricing favorable for engagement|
| Mixpanel         | $0          | $7,000       | $7,000         | Event pricing, startup credits      |
| PostHog          | $1,200      | $8,000       | $9,200         | No startup program but cheap early  |
| Heap             | $25,000     | $35,000      | $60,000        | Estimated, no public pricing        |
| Firebase Analytics| $0         | $0           | $0             | Free but limited                    |

**Winner: Amplitude or Mixpanel (both $0 year 1 with programs), Firebase for ultra-lean**

---

## 5. DECISION FRAMEWORK

### Choose Amplitude If:
- You qualify for startup program (1 year free)
- High-engagement app (gaming, social, fitness)
- Team needs sophisticated retention/cohort analysis
- Mobile-first company with growth ambitions
- Budget allows $500-$1,500/month after free year

### Choose Mixpanel If:
- You qualify for startup program ($50K credit)
- Lower engagement app (utility, sporadic use)
- Team prefers simpler UI than Amplitude
- Event-based pricing better matches your usage
- Similar budget as Amplitude post-program

### Choose PostHog If:
- Cost efficiency is critical priority
- You need feature flags + A/B testing + analytics in one
- Technical team comfortable with newer platforms
- Don't qualify for Amplitude/Mixpanel startup programs
- Willing to trade some mobile specialization for cost

### Choose Firebase Analytics If:
- Pre-revenue MVP stage (need free solution)
- Already using Firebase ecosystem
- Basic analytics sufficient (not behavioral depth)
- Plan to upgrade to dedicated tool after product-market fit
- Zero budget for analytics tools

---

## 6. PRICING MODEL SELECTION

### MTU (Monthly Tracked Users) - Amplitude
**Best for:**
- High engagement apps (many events per user)
- Social networks, gaming, fitness tracking
- Apps with core daily usage loop

**Example Math:**
- 100K MAU × 100 events/user/month = 10M events
- Amplitude MTU pricing: ~$5K/year
- Mixpanel event pricing: ~$7K/year
- **Amplitude wins**

### Event-Based - Mixpanel, PostHog
**Best for:**
- Lower engagement apps (weekly/monthly usage)
- Utility apps, content consumption
- Apps with high user counts but low event density

**Example Math:**
- 200K MAU × 20 events/user/month = 4M events
- Mixpanel event pricing: ~$3K/year
- Amplitude MTU pricing: ~$8K/year
- **Mixpanel/PostHog wins**

---

## 7. MOBILE-SPECIFIC IMPLEMENTATION TIPS

### Week 1: SDK Integration
- [ ] Install native SDKs (iOS + Android or cross-platform)
- [ ] Configure user identification (device ID → user ID after login)
- [ ] Set up automatic screen view tracking
- [ ] Test event delivery on both platforms

### Week 2: Core Event Instrumentation
- [ ] App install/open events
- [ ] Onboarding completion steps
- [ ] Core feature usage events (5-10 key actions)
- [ ] Subscription/purchase events
- [ ] Screen view tracking

### Week 3: Attribution & Cohorts
- [ ] Integrate attribution partner (AppsFlyer/Adjust)
- [ ] Configure acquisition source tracking
- [ ] Set up cohort analysis by acquisition date
- [ ] Create retention dashboards (D1, D7, D30)

### Week 4: Dashboards
- [ ] Acquisition funnel (install → onboarding → activated)
- [ ] Engagement metrics (DAU/MAU, session length/frequency)
- [ ] Monetization funnel (free → trial → paid)
- [ ] Feature adoption matrix
- [ ] Platform comparison (iOS vs Android)

---

## 8. CRITICAL SUCCESS METRICS

**Activation Metrics:**
- % of installs that complete onboarding
- Time to first value (aha moment)

**Engagement Metrics:**
- D1/D7/D30 retention by cohort
- DAU/MAU ratio (stickiness)
- Session frequency and duration

**Monetization Metrics:**
- % of users who start trial/subscribe
- Time from install to conversion
- LTV by acquisition channel

---

## 9. MIGRATION RISK ASSESSMENT

**Low Risk Window**: First 3-6 months
- Mobile apps iterate fast - switching early is easier
- Limited historical data dependency

**Medium Risk**: 6-12 months
- Cohort data becomes valuable
- Team builds muscle memory on specific tool

**High Risk**: 12+ months
- Deep attribution integration
- Historical cohort comparisons essential
- Cross-functional dependencies (marketing, product, eng)

**Recommendation**: Mobile apps should choose carefully upfront - migration pain is high due to SDK changes across iOS/Android.

---

## 10. RECOMMENDED CHOICE

**PRIMARY**: Amplitude (if startup program eligible)

**Rationale:**
- Purpose-built for high-engagement consumer mobile apps
- MTU pricing aligns with mobile usage patterns
- Industry standard (easier to hire analysts who know it)
- Strongest mobile SDKs and retention features

**SECONDARY**: Mixpanel (if event-based pricing is better match)

**Rationale:**
- Better for lower-engagement apps
- Simpler UI may fit smaller teams
- Comparable feature set for mobile

**BUDGET OPTION**: Firebase Analytics → upgrade to Amplitude/Mixpanel at $10K MRR

**Rationale:**
- Start free with Firebase for MVP
- Migrate to proper product analytics once revenue justifies cost
- Avoid premature optimization

---

## 11. COMMON PITFALLS TO AVOID

1. **Over-instrumentation**: Don't track 100+ events day 1. Start with 10-15 core events.
2. **Platform fragmentation**: Ensure iOS/Android event parity (same event names/properties).
3. **Ignoring attribution**: Mobile apps NEED attribution integration from day 1.
4. **Wrong pricing model**: Test MTU vs event-based math before committing.
5. **Privacy non-compliance**: Respect App Store privacy requirements (permission tracking).

---

END OF USE CASE ANALYSIS
